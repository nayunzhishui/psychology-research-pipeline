#!/usr/bin/env python3
"""Privacy-safe structural audit for wide longitudinal SPSS/CSV panel data."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import secrets
from datetime import datetime
from pathlib import Path


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_frame(path: Path, usecols: list[str]):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("pandas is required for panel audit") from exc
    if path.suffix.lower() == ".sav":
        try:
            import pyreadstat
        except ImportError as exc:
            raise SystemExit("pyreadstat is required for .sav audit; install it in the selected Python environment") from exc
        _, full_metadata = pyreadstat.read_sav(str(path), metadataonly=True)
        frame, _ = pyreadstat.read_sav(str(path), usecols=usecols)
        return frame, {"rows": full_metadata.number_rows, "columns": full_metadata.number_columns}
    if path.suffix.lower() == ".csv":
        full_columns = pd.read_csv(path, nrows=0).columns
        frame = pd.read_csv(path, usecols=usecols)
        return frame, {"rows": len(frame), "columns": len(full_columns)}
    raise SystemExit(f"Unsupported data type: {path.suffix}")


def finite_or_none(value):
    value = float(value)
    return value if math.isfinite(value) else None


ISSUE_RULES = {
    "linkage": ("critical", ["source-verified", "rematched", "excluded"]),
    "linkage-format": ("major", ["source-verified", "normalized", "rematched", "excluded"]),
    "duplicate-id": ("critical", ["source-verified", "deduplicated", "excluded"]),
    "sex-code": ("major", ["source-verified", "corrected", "excluded"]),
    "score-range": ("major", ["source-verified", "corrected", "rescored", "excluded"]),
    "item-range": ("major", ["source-verified", "set-missing", "corrected", "excluded"]),
    "distribution": ("major", ["analysis-accommodation", "not-applicable"]),
    "extreme-value": ("major", ["source-verified", "corrected", "excluded"]),
    "scoring-formula": ("critical", ["corrected", "rescored", "excluded"]),
}


def make_issue(category: str, message: str) -> dict:
    severity, allowed = ISSUE_RULES[category]
    stable = hashlib.sha256(f"{category}|{message}".encode("utf-8")).hexdigest()[:12]
    return {
        "issue_id": f"issue-{stable}", "category": category, "severity": severity,
        "message": message, "allowed_resolutions": allowed,
    }


def private_record(issue: dict, row_index: int, identifiers: list[object], salt: str, variable: str) -> dict:
    normalized = f"row={row_index}|" + "|".join("" if value is None else str(value) for value in identifiers)
    pseudonym = hashlib.sha256(f"{salt}|{normalized}".encode("utf-8")).hexdigest()[:20]
    return {
        "type": "row-issue", "issue_id": issue["issue_id"], "category": issue["category"],
        "row_index": int(row_index) + 2, "pseudonym": pseudonym, "variable": variable,
        "raw_identifiers_included": False,
    }


def measure_summary(series, spec: dict) -> dict:
    import pandas as pd
    numeric = pd.to_numeric(series, errors="coerce")
    observed = numeric.dropna()
    below = int((observed < spec["expected_min"]).sum()) if "expected_min" in spec else 0
    above = int((observed > spec["expected_max"]).sum()) if "expected_max" in spec else 0
    q1 = observed.quantile(0.25) if len(observed) else float("nan")
    q3 = observed.quantile(0.75) if len(observed) else float("nan")
    extreme_threshold = q3 + 10 * (q3 - q1) if len(observed) else float("nan")
    extreme_high = int((observed > extreme_threshold).sum()) if len(observed) and q3 > q1 else 0
    zero_percent = finite_or_none(numeric.eq(0).mean() * 100)
    return {
        "construct": spec["construct"], "wave": spec["wave"], "variable": spec["variable"],
        "n": int(observed.size), "missing": int(numeric.isna().sum()), "unique": int(observed.nunique()),
        "min": finite_or_none(observed.min()) if len(observed) else None,
        "max": finite_or_none(observed.max()) if len(observed) else None,
        "mean": finite_or_none(observed.mean()) if len(observed) else None,
        "sd": finite_or_none(observed.std()) if len(observed) > 1 else None,
        "zero_percent": zero_percent,
        "zero_heavy": bool(zero_percent is not None and zero_percent >= 30),
        "extreme_high_count": extreme_high,
        "below_expected": below, "above_expected": above,
        "flag": below > 0 or above > 0,
    }


def normalize_id(value: object, config: dict) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    if config.get("mode") == "alpha-prefix-integer-suffix":
        match = re.fullmatch(r"([A-Za-z]+)0*(\d+)", text)
        if match:
            return f"{match.group(1).lower()}{int(match.group(2))}"
    return text


def audit_ids(frame, id_by_wave: dict, normalization: dict | None = None) -> dict:
    normalization = normalization or {}
    result = {"by_wave": {}, "rowwise_mismatch": {}}
    waves = list(id_by_wave)
    for wave, variable in id_by_wave.items():
        values = frame[variable].dropna().astype(str)
        result["by_wave"][wave] = {
            "variable": variable, "nonmissing": int(len(values)),
            "unique": int(values.nunique()), "duplicate_rows": int(values.duplicated().sum()),
            "normalized_unique": int(values.map(lambda value: normalize_id(value, normalization)).nunique()),
        }
    for left, right in zip(waves, waves[1:]):
        left_values = frame[id_by_wave[left]]
        right_values = frame[id_by_wave[right]]
        comparable = left_values.notna() & right_values.notna()
        mismatch = comparable & left_values.astype(str).ne(right_values.astype(str))
        normalized_left = left_values.map(lambda value: normalize_id(value, normalization))
        normalized_right = right_values.map(lambda value: normalize_id(value, normalization))
        normalized_mismatch = comparable & normalized_left.ne(normalized_right)
        result["rowwise_mismatch"][f"{left}-{right}"] = {
            "comparable": int(comparable.sum()),
            "mismatch": int(mismatch.sum()),
            "raw_mismatch": int(mismatch.sum()),
            "format_only_candidates": int((mismatch & ~normalized_mismatch).sum()),
            "normalized_mismatch": int(normalized_mismatch.sum()),
        }
    return result


def audit_sex(frame, spec: dict) -> dict:
    allowed = set(spec.get("allowed_sex_values", []))
    result = {}
    for wave, variable in spec.get("sex_by_wave", {}).items():
        values = frame[variable].dropna()
        invalid = values[~values.isin(allowed)]
        result[wave] = {
            "variable": variable, "nonmissing": int(len(values)), "missing": int(frame[variable].isna().sum()),
            "invalid_count": int(len(invalid)), "invalid_values": sorted({str(value) for value in invalid.tolist()}),
        }
    return result


def relation_terms(relation: dict) -> tuple[float, dict[str, float], list[tuple[str, str, float]]]:
    if "sum" in relation:
        config = relation["sum"]
        variables = item_variables({"selector": config["selector"]})
        reverse = {int(index) for index in config.get("reverse_items", [])}
        reverse_constant = float(config.get("reverse_constant", 0))
        coefficients = {
            variable: (-1.0 if index in reverse else 1.0)
            for index, variable in enumerate(variables, start=1)
        }
        intercept = float(relation.get("intercept", 0)) + reverse_constant * len(reverse)
        return intercept, coefficients, []
    if "product_sum" in relation:
        config = relation["product_sum"]
        left = item_variables({"selector": config["left_selector"]})
        right = item_variables({"selector": config["right_selector"]})
        if len(left) != len(right):
            raise ValueError(f"product relation has unequal item counts: {relation['name']}")
        return float(relation.get("intercept", 0)), {}, [
            (left_item, right_item, 1.0) for left_item, right_item in zip(left, right)
        ]
    return (
        float(relation.get("intercept", 0)),
        {key: float(value) for key, value in relation.get("coefficients", {}).items()},
        [(item["left"], item["right"], float(item.get("coefficient", 1))) for item in relation.get("products", [])],
    )


def audit_relation(frame, relation: dict) -> dict:
    import pandas as pd
    intercept, coefficients, products = relation_terms(relation)
    columns = list(dict.fromkeys([
        relation["target"], *coefficients,
        *(variable for left, right, _ in products for variable in (left, right)),
    ]))
    data = frame[columns].apply(pd.to_numeric, errors="coerce").dropna()
    predicted = intercept
    for variable, coefficient in coefficients.items():
        predicted = predicted + coefficient * data[variable]
    for left, right, coefficient in products:
        predicted = predicted + coefficient * data[left] * data[right]
    error = (data[relation["target"]] - predicted).abs()
    tolerance = relation.get("tolerance", 1e-6)
    return {
        "name": relation["name"], "n": int(len(data)),
        "exact_count": int((error <= tolerance).sum()),
        "mismatch_count": int((error > tolerance).sum()),
        "max_abs_error": finite_or_none(error.max()) if len(error) else None,
        "flag": bool(len(error) and (error > tolerance).any()),
    }


def item_variables(spec: dict) -> list[str]:
    if "variables" in spec:
        return spec["variables"]
    selector = spec["selector"]
    width = int(selector.get("width", 0))
    prefix = selector.get("prefix", "")
    return [
        selector["template"].format(item=f"{prefix}{str(index).zfill(width) if width else index}")
        for index in range(int(selector["start"]), int(selector["end"]) + 1)
    ]


def audit_item_set(frame, spec: dict) -> dict:
    import pandas as pd
    variables = item_variables(spec)
    data = frame[variables].apply(pd.to_numeric, errors="coerce")
    invalid = data.notna() & (
        data.lt(spec.get("expected_min", -math.inf)) |
        data.gt(spec.get("expected_max", math.inf))
    )
    by_variable = {
        variable: {
            "nonmissing": int(data[variable].notna().sum()),
            "invalid_count": int(invalid[variable].sum()),
            "min": finite_or_none(data[variable].min()) if data[variable].notna().any() else None,
            "max": finite_or_none(data[variable].max()) if data[variable].notna().any() else None,
        }
        for variable in variables
    }
    return {
        "construct": spec["construct"], "wave": spec["wave"],
        "item_count": len(variables),
        "expected_min": spec.get("expected_min"), "expected_max": spec.get("expected_max"),
        "invalid_cell_count": int(invalid.sum().sum()),
        "affected_row_count": int(invalid.any(axis=1).sum()),
        "by_variable": by_variable,
        "flag": bool(invalid.any().any()),
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# 数据质量审计", "", "> 本报告仅输出汇总统计，不输出参与者 ID 或行级自伤数据。", "",
        "## 文件与结构", "",
        f"- 文件：`{report['data_file']}`", f"- SHA-256：`{report['sha256']}`",
        f"- 行数：{report['shape']['rows']}", f"- 列数：{report['shape']['columns']}", "",
        "## ID、重复与波次连接", "",
    ]
    for wave, item in report["ids"]["by_wave"].items():
        lines.append(f"- {wave} `{item['variable']}`：非缺失 {item['nonmissing']}，唯一 {item['unique']}，重复行 {item['duplicate_rows']}。")
    for pair, item in report["ids"]["rowwise_mismatch"].items():
        lines.append(
            f"- {pair}：可比较 {item['comparable']}，原始不一致 {item['raw_mismatch']}，"
            f"仅格式候选 {item['format_only_candidates']}，规范化后仍不一致 {item['normalized_mismatch']}。"
        )
    lines.extend(["", "## 性别编码", ""])
    for wave, item in report["sex"].items():
        lines.append(f"- {wave} `{item['variable']}`：缺失 {item['missing']}，异常 {item['invalid_count']}，异常值 {item['invalid_values']}。")
    lines.extend(["", "## 核心变量分布与范围", ""])
    for item in report["measures"]:
        lines.append(
            f"- {item['wave']} {item['construct']} `{item['variable']}`：n={item['n']}，缺失={item['missing']}，"
            f"范围={item['min']}–{item['max']}，零值={item['zero_percent']:.1f}%，"
            f"低于预期={item['below_expected']}，高于预期={item['above_expected']}，极端高值={item['extreme_high_count']}。"
        )
    lines.extend(["", "## 原始题项范围", ""])
    for item in report["item_sets"]:
        lines.append(
            f"- {item['wave']} {item['construct']}：题项 {item['item_count']}，"
            f"异常单元格 {item['invalid_cell_count']}，受影响行 {item['affected_row_count']}。"
        )
    lines.extend(["", "## 总分公式核验", ""])
    for item in report["score_relations"]:
        lines.append(f"- {item['name']}：n={item['n']}，匹配={item['exact_count']}，不匹配={item['mismatch_count']}，最大误差={item['max_abs_error']}。")
    lines.extend(["", "## 分析就绪结论与阻断项", ""])
    if report["flags"]:
        lines.extend(f"- [ ] {flag}" for flag in report["flags"])
    else:
        lines.append("- 未发现本规格定义的结构性阻断项；仍需核验量表来源、计分语法、波次日期和伦理材料。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--fail-on-flags", action="store_true")
    parser.add_argument("--private-register", help="Local ignored JSONL row-issue register")
    args = parser.parse_args()

    data_path = Path(args.data).expanduser().resolve()
    spec_path = Path(args.spec).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not data_path.is_file() or not spec_path.is_file():
        parser.error("data and spec must exist")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    variables = set(spec.get("id_by_wave", {}).values()) | set(spec.get("sex_by_wave", {}).values())
    variables |= {item["variable"] for item in spec.get("measures", [])}
    for item_set in spec.get("item_sets", []):
        variables.update(item_variables(item_set))
    for relation in spec.get("score_relations", []):
        variables.add(relation["target"])
        _, coefficients, products = relation_terms(relation)
        variables.update(coefficients)
        variables.update(variable for left, right, _ in products for variable in (left, right))

    frame, shape = load_frame(data_path, sorted(variables))
    ids = audit_ids(frame, spec.get("id_by_wave", {}), spec.get("id_normalization"))
    sex = audit_sex(frame, spec)
    measures = [measure_summary(frame[item["variable"]], item) for item in spec.get("measures", [])]
    item_sets = [audit_item_set(frame, item) for item in spec.get("item_sets", [])]
    relations = [audit_relation(frame, item) for item in spec.get("score_relations", [])]
    issues = []
    private_records = []
    salt = secrets.token_hex(32)
    id_variables = list(spec.get("id_by_wave", {}).values())
    for pair, item in ids["rowwise_mismatch"].items():
        left_wave, right_wave = pair.split("-")
        left_var, right_var = spec["id_by_wave"][left_wave], spec["id_by_wave"][right_wave]
        comparable = frame[left_var].notna() & frame[right_var].notna()
        raw_mismatch = comparable & frame[left_var].astype(str).ne(frame[right_var].astype(str))
        normalized_left = frame[left_var].map(lambda value: normalize_id(value, spec.get("id_normalization", {})))
        normalized_right = frame[right_var].map(lambda value: normalize_id(value, spec.get("id_normalization", {})))
        normalized_mismatch = comparable & normalized_left.ne(normalized_right)
        format_only = raw_mismatch & ~normalized_mismatch
        if item["format_only_candidates"]:
            message = f"{pair} 有 {item['format_only_candidates']} 行仅在预设 ID 格式规范化后相符，需保留源值并核验映射。"
            issue = make_issue("linkage-format", message)
            issues.append(issue)
            for row_index in frame.index[format_only]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, variable] for variable in id_variables],
                    salt, f"{left_var}|{right_var}",
                ))
        if item["normalized_mismatch"]:
            message = f"{pair} 规范化后仍有 {item['normalized_mismatch']} 行 ID 不一致，需核验合并。"
            issue = make_issue("linkage", message)
            issues.append(issue)
            for row_index in frame.index[normalized_mismatch]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, variable] for variable in id_variables],
                    salt, f"{left_var}|{right_var}",
                ))
    for wave, item in ids["by_wave"].items():
        if item["duplicate_rows"]:
            message = f"{wave} 存在 {item['duplicate_rows']} 个重复 ID 行。"
            issue = make_issue("duplicate-id", message)
            issues.append(issue)
            variable = item["variable"]
            duplicated = frame[variable].notna() & frame[variable].astype(str).duplicated(keep=False)
            for row_index in frame.index[duplicated]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, variable,
                ))
    for wave, item in sex.items():
        if item["invalid_count"]:
            issue = make_issue("sex-code", f"{wave} 存在 {item['invalid_count']} 个异常性别编码。")
            issues.append(issue)
            variable = item["variable"]
            invalid = frame[variable].notna() & ~frame[variable].isin(set(spec.get("allowed_sex_values", [])))
            for row_index in frame.index[invalid]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, variable,
                ))
    for item in measures:
        if item["flag"]:
            issue = make_issue("score-range", f"{item['wave']} `{item['variable']}` 有 {item['below_expected']} 个低值和 {item['above_expected']} 个高值超出预设范围。")
            issues.append(issue)
            measure_spec = next(value for value in spec["measures"] if value["variable"] == item["variable"])
            numeric = __import__("pandas").to_numeric(frame[item["variable"]], errors="coerce")
            invalid = numeric.notna() & (
                numeric.lt(measure_spec.get("expected_min", -math.inf)) |
                numeric.gt(measure_spec.get("expected_max", math.inf))
            )
            for row_index in frame.index[invalid]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, item["variable"],
                ))
        if item["construct"].startswith("self_harm") and item["zero_heavy"]:
            issues.append(make_issue("distribution", f"{item['wave']} `{item['variable']}` 零值比例为 {item['zero_percent']:.1f}%，需预设非正态/两部分等分布方案。"))
        measure_spec = next(value for value in spec["measures"] if value["variable"] == item["variable"])
        if item["extreme_high_count"] and measure_spec.get("flag_extremes", False):
            issue = make_issue("extreme-value", f"{item['wave']} `{item['variable']}` 有 {item['extreme_high_count']} 个基于宽松 IQR 规则的极端高值，需回查原始题项。")
            issues.append(issue)
            numeric = __import__("pandas").to_numeric(frame[item["variable"]], errors="coerce")
            q1, q3 = numeric.quantile(0.25), numeric.quantile(0.75)
            extreme = numeric.notna() & numeric.gt(q3 + 10 * (q3 - q1))
            for row_index in frame.index[extreme]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, item["variable"],
                ))
    for item, item_spec in zip(item_sets, spec.get("item_sets", [])):
        if not item["flag"]:
            continue
        issue = make_issue(
            "item-range",
            f"{item['wave']} {item['construct']} 原始题项有 {item['invalid_cell_count']} 个单元格超出预设范围。",
        )
        issues.append(issue)
        pd = __import__("pandas")
        variables_for_set = item_variables(item_spec)
        data = frame[variables_for_set].apply(pd.to_numeric, errors="coerce")
        invalid = data.notna() & (
            data.lt(item_spec.get("expected_min", -math.inf)) |
            data.gt(item_spec.get("expected_max", math.inf))
        )
        for row_index in frame.index[invalid.any(axis=1)]:
            affected = [variable for variable in variables_for_set if bool(invalid.at[row_index, variable])]
            private_records.append(private_record(
                issue, row_index, [frame.at[row_index, value] for value in id_variables],
                salt, "|".join(affected),
            ))
    for item in relations:
        if item["flag"]:
            issue = make_issue("scoring-formula", f"{item['name']} 有 {item['mismatch_count']} 行不符合预设公式。")
            issues.append(issue)
            relation = next(value for value in spec.get("score_relations", []) if value["name"] == item["name"])
            pd = __import__("pandas")
            intercept, coefficients, products = relation_terms(relation)
            columns = list(dict.fromkeys([
                relation["target"], *coefficients,
                *(variable for left, right, _ in products for variable in (left, right)),
            ]))
            comparable = frame[columns].apply(pd.to_numeric, errors="coerce").dropna()
            predicted = intercept
            for variable, coefficient in coefficients.items():
                predicted = predicted + coefficient * comparable[variable]
            for left, right, coefficient in products:
                predicted = predicted + coefficient * comparable[left] * comparable[right]
            mismatch = (comparable[relation["target"]] - predicted).abs().gt(relation.get("tolerance", 1e-6))
            for row_index in comparable.index[mismatch]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, relation["target"],
                ))

    flags = [item["message"] for item in issues]
    private_path = None
    if args.private_register:
        private_path = Path(args.private_register).expanduser().resolve()
        private_path.parent.mkdir(parents=True, exist_ok=True)
        header = {
            "type": "metadata", "schema_version": 1, "data_sha256": sha256(data_path),
            "salt_sha256": hashlib.sha256(salt.encode("utf-8")).hexdigest(),
            "privacy": "local-only; pseudonymized identifiers; never submit or commit",
        }
        with private_path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in [header, *private_records]:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    report = {
        "schema_version": 1, "profile": spec.get("profile"), "generated_at": now(),
        "data_file": str(data_path), "sha256": sha256(data_path),
        "spec_file": str(spec_path), "spec_sha256": sha256(spec_path), "shape": shape,
        "ids": ids, "sex": sex, "measures": measures, "item_sets": item_sets,
        "score_relations": relations,
        "issues": issues, "private_register": str(private_path) if private_path else None,
        "flags": flags, "privacy": "aggregate-only; no participant IDs or row-level self-harm records",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "数据质量审计_data_audit.json"
    md_path = output_dir / "数据质量审计_data_audit.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    md_path.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    print(md_path)
    print(json_path)
    return 2 if args.fail_on_flags and flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
