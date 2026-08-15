#!/usr/bin/env python3
"""Create a privacy-safe, rescored analysis dataset from a verified measurement map."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
from datetime import datetime
from pathlib import Path

from audit_panel_data import load_frame


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expand(selector: dict) -> list[str]:
    width = int(selector.get("width", 0))
    prefix = selector.get("prefix", "")
    return [
        selector["template"].format(item=f"{prefix}{str(index).zfill(width) if width else index}")
        for index in range(int(selector["start"]), int(selector["end"]) + 1)
    ]


def valid_numeric(frame, variables: list[str], limits: list[float]):
    import pandas as pd
    numeric = frame[variables].apply(pd.to_numeric, errors="coerce")
    invalid = numeric.notna() & (numeric.lt(limits[0]) | numeric.gt(limits[1]))
    return numeric.mask(invalid), invalid


def prorated_sum(items, minimum_fraction: float = 0.8):
    minimum = max(1, math.ceil(items.shape[1] * minimum_fraction))
    valid = items.notna().sum(axis=1)
    score = items.sum(axis=1, min_count=minimum) * items.shape[1] / valid.where(valid > 0)
    return score, minimum


def standardized_item_names(stem: str, wave: str, count: int) -> list[str]:
    return [f"{stem}_item{index:02d}_{wave.lower()}" for index in range(1, count + 1)]


def normalized_id(value: object) -> str | None:
    if value is None:
        return None
    match = re.fullmatch(r"([A-Za-z]+)0*(\d+)", str(value).strip())
    return f"{match.group(1).lower()}{int(match.group(2))}" if match else None


def prepare(data_path: Path, map_path: Path, output_dir: Path) -> dict:
    import pandas as pd

    config = json.loads(map_path.read_text(encoding="utf-8"))
    constructs = config["constructs"]
    identifiers = config.get("identifiers_and_covariates", {})
    id_by_wave = identifiers.get("id_by_wave", {})
    sex_by_wave = identifiers.get("sex_by_wave", {})
    required = set(id_by_wave.values()) | set(sex_by_wave.values())
    depression = constructs["depressive_symptoms"]
    nssi = constructs["nssi"]
    conflict = constructs["interparental_conflict"]
    for selector in depression["raw_selectors"].values():
        required.update(expand(selector))
    for selector in nssi["frequency_selectors"].values():
        required.update(expand(selector))
    for selector in nssi["severity_selectors"].values():
        required.update(expand(selector))
    for selector in conflict["raw_selectors"].values():
        required.update(expand(selector))

    frame, shape = load_frame(data_path, sorted(required))
    base_output = pd.DataFrame(index=frame.index)
    output_parts: list = [base_output]
    invalid_total = 0
    invalid_by_construct: dict[str, dict[str, int]] = {}
    scoring: dict[str, dict[str, object]] = {}

    t1_id = frame[id_by_wave["T1"]].astype("string") if id_by_wave.get("T1") else pd.Series(pd.NA, index=frame.index)
    base_output["school_code"] = t1_id.str.extract(r"^([A-Za-z])", expand=False).str.lower()
    t1_sex = pd.to_numeric(frame[sex_by_wave["T1"]], errors="coerce") if sex_by_wave.get("T1") else pd.Series(pd.NA, index=frame.index)
    base_output["sex_analysis"] = t1_sex.where(t1_sex.isin([1, 2]))
    normalized_ids = pd.DataFrame({wave: frame[variable].map(normalized_id) for wave, variable in id_by_wave.items()})
    id_unique_counts = normalized_ids.nunique(axis=1, dropna=True)
    valid_sex = pd.DataFrame({
        wave: pd.to_numeric(frame[variable], errors="coerce").where(pd.to_numeric(frame[variable], errors="coerce").isin([1, 2]))
        for wave, variable in sex_by_wave.items()
    })

    for wave, selector in depression["raw_selectors"].items():
        variables = expand(selector)
        items, invalid = valid_numeric(frame, variables, depression["response_range"])
        reverse = [index for index in depression.get("reverse_items", []) if index <= len(variables)]
        for index in reverse:
            items.iloc[:, index - 1] = sum(depression["response_range"]) - items.iloc[:, index - 1]
        names = standardized_item_names("depression", wave, len(variables))
        output_parts.append(items.set_axis(names, axis=1))
        score, minimum = prorated_sum(items)
        output_parts.append(score.rename(depression["analysis_scores"][wave]).to_frame())
        invalid_count = int(invalid.sum().sum())
        invalid_total += invalid_count
        invalid_by_construct.setdefault("depression", {})[wave] = invalid_count
        scoring.setdefault("depression", {})[wave] = {"items": len(variables), "minimum_valid": minimum, "reverse_items": reverse}

    for wave, frequency_selector in nssi["frequency_selectors"].items():
        frequency_variables = expand(frequency_selector)
        severity_variables = expand(nssi["severity_selectors"][wave])
        frequency, invalid_frequency = valid_numeric(frame, frequency_variables, nssi["frequency_range"])
        severity, invalid_severity = valid_numeric(frame, severity_variables, nssi["severity_range"])
        severity.columns = frequency.columns
        severity = severity.mask(frequency.eq(0) & severity.isna(), 0)
        products = frequency.to_numpy() * severity.to_numpy()
        product_items = pd.DataFrame(products, index=frame.index)
        names = standardized_item_names("nssi", wave, len(frequency_variables))
        product_items.columns = names
        output_parts.append(product_items)
        score, minimum = prorated_sum(product_items)
        output_parts.append(score.rename(nssi["analysis_scores"][wave]).to_frame())
        invalid_count = int(invalid_frequency.sum().sum() + invalid_severity.sum().sum())
        invalid_total += invalid_count
        invalid_by_construct.setdefault("nssi", {})[wave] = invalid_count
        scoring.setdefault("nssi", {})[wave] = {
            "items": len(frequency_variables), "minimum_valid": minimum,
            "zero_frequency_missing_severity": "product set to zero",
        }

    reverse_conflict = conflict.get("high_conflict_reverse_items", [])
    for wave, selector in conflict["raw_selectors"].items():
        variables = expand(selector)
        items, invalid = valid_numeric(frame, variables, conflict["response_range"])
        reverse = [index for index in reverse_conflict if index <= len(variables)]
        for index in reverse:
            items.iloc[:, index - 1] = sum(conflict["response_range"]) - items.iloc[:, index - 1]
        names = standardized_item_names("conflict", wave, len(variables))
        output_parts.append(items.set_axis(names, axis=1))
        score, minimum = prorated_sum(items)
        output_parts.append(score.rename(conflict["analysis_scores"][wave]).to_frame())
        invalid_count = int(invalid.sum().sum())
        invalid_total += invalid_count
        invalid_by_construct.setdefault("conflict", {})[wave] = invalid_count
        scoring.setdefault("conflict", {})[wave] = {"items": len(variables), "minimum_valid": minimum, "reverse_items": reverse}

    output = pd.concat(output_parts, axis=1)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "分析就绪数据_analysis_ready.csv"
    temp_path = output_path.with_suffix(".csv.tmp")
    output.to_csv(temp_path, index=False, encoding="utf-8-sig")
    os.replace(temp_path, output_path)
    report = {
        "schema_version": 1, "status": "prepared",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_sha256": sha256(data_path), "measurement_map_sha256": sha256(map_path),
        "source_shape": shape, "rows": int(len(output)), "columns": int(len(output.columns)),
        "analysis_data": str(output_path.resolve()), "analysis_data_sha256": sha256(output_path),
        "invalid_cells_set_missing": invalid_total,
        "invalid_cells_by_construct_wave": invalid_by_construct,
        "scoring": scoring,
        "sex_policy": "T1 measured sex only; invalid or missing T1 values remain missing",
        "id_policy": "raw IDs excluded; only anonymized first-letter school_code retained",
        "id_linkage_summary": {
            "all_available_equal_after_format_normalization": int(id_unique_counts.eq(1).sum()),
            "two-values-with-majority-candidate": int(id_unique_counts.eq(2).sum()),
            "all-different": int(id_unique_counts.ge(3).sum()),
        },
        "sex_summary": {
            "t1_valid": int(base_output["sex_analysis"].notna().sum()),
            "t1_missing_or_invalid": int(base_output["sex_analysis"].isna().sum()),
            "cross_wave_valid_disagreement": int(valid_sex.nunique(axis=1, dropna=True).gt(1).sum()),
        },
        "missing_rule": "prorated sum when at least 80% of construct items are valid",
        "privacy": "No participant identifier or raw row-level self-harm field is exported.",
    }
    report_path = output_dir / "分析数据派生报告_analysis_data_derivation.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    report["report"] = str(report_path.resolve())
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--measurement-map", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = prepare(
        Path(args.data).expanduser().resolve(),
        Path(args.measurement_map).expanduser().resolve(),
        Path(args.output_dir).expanduser().resolve(),
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
