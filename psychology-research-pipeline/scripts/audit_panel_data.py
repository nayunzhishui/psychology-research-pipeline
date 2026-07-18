#!/usr/bin/env python3
"""Privacy-safe structural audit for wide longitudinal SPSS/CSV panel data."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
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
    "duplicate-id": ("critical", ["source-verified", "deduplicated", "excluded"]),
    "sex-code": ("major", ["source-verified", "corrected", "excluded"]),
    "score-range": ("major", ["source-verified", "corrected", "excluded"]),
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


def audit_ids(frame, id_by_wave: dict) -> dict:
    result = {"by_wave": {}, "rowwise_mismatch": {}}
    waves = list(id_by_wave)
    for wave, variable in id_by_wave.items():
        values = frame[variable].dropna().astype(str)
        result["by_wave"][wave] = {
            "variable": variable, "nonmissing": int(len(values)),
            "unique": int(values.nunique()), "duplicate_rows": int(values.duplicated().sum()),
        }
    for left, right in zip(waves, waves[1:]):
        left_values = frame[id_by_wave[left]]
        right_values = frame[id_by_wave[right]]
        comparable = left_values.notna() & right_values.notna()
        mismatch = comparable & left_values.astype(str).ne(right_values.astype(str))
        result["rowwise_mismatch"][f"{left}-{right}"] = {
            "comparable": int(comparable.sum()), "mismatch": int(mismatch.sum())
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


def audit_relation(frame, relation: dict) -> dict:
    import pandas as pd
    columns = [relation["target"], *relation["coefficients"]]
    data = frame[columns].apply(pd.to_numeric, errors="coerce").dropna()
    predicted = relation.get("intercept", 0)
    for variable, coefficient in relation["coefficients"].items():
        predicted = predicted + coefficient * data[variable]
    error = (data[relation["target"]] - predicted).abs()
    tolerance = relation.get("tolerance", 1e-6)
    return {
        "name": relation["name"], "n": int(len(data)),
        "exact_count": int((error <= tolerance).sum()),
        "mismatch_count": int((error > tolerance).sum()),
        "max_abs_error": finite_or_none(error.max()) if len(error) else None,
        "flag": bool(len(error) and (error > tolerance).any()),
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
        lines.append(f"- {pair}：可比较 {item['comparable']}，行内不一致 {item['mismatch']}。")
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
    for relation in spec.get("score_relations", []):
        variables.add(relation["target"])
        variables.update(relation["coefficients"])

    frame, shape = load_frame(data_path, sorted(variables))
    ids = audit_ids(frame, spec.get("id_by_wave", {}))
    sex = audit_sex(frame, spec)
    measures = [measure_summary(frame[item["variable"]], item) for item in spec.get("measures", [])]
    relations = [audit_relation(frame, item) for item in spec.get("score_relations", [])]
    issues = []
    private_records = []
    salt = secrets.token_hex(32)
    id_variables = list(spec.get("id_by_wave", {}).values())
    for pair, item in ids["rowwise_mismatch"].items():
        if item["mismatch"]:
            message = f"{pair} 存在 {item['mismatch']} 行 ID 不一致，需核验合并。"
            issue = make_issue("linkage", message)
            issues.append(issue)
            left_wave, right_wave = pair.split("-")
            left_var, right_var = spec["id_by_wave"][left_wave], spec["id_by_wave"][right_wave]
            comparable = frame[left_var].notna() & frame[right_var].notna()
            mismatch = comparable & frame[left_var].astype(str).ne(frame[right_var].astype(str))
            for row_index in frame.index[mismatch]:
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
        if item["extreme_high_count"]:
            issue = make_issue("extreme-value", f"{item['wave']} `{item['variable']}` 有 {item['extreme_high_count']} 个基于宽松 IQR 规则的极端高值，需回查原始题项。")
            issues.append(issue)
            numeric = __import__("pandas").to_numeric(frame[item["variable"]], errors="coerce")
            q1, q3 = numeric.quantile(0.25), numeric.quantile(0.75)
            extreme = numeric.notna() & numeric.gt(q3 + 10 * (q3 - q1))
            for row_index in frame.index[extreme]:
                private_records.append(private_record(
                    issue, row_index, [frame.at[row_index, value] for value in id_variables], salt, item["variable"],
                ))
    for item in relations:
        if item["flag"]:
            issue = make_issue("scoring-formula", f"{item['name']} 有 {item['mismatch_count']} 行不符合预设公式。")
            issues.append(issue)
            relation = next(value for value in spec.get("score_relations", []) if value["name"] == item["name"])
            pd = __import__("pandas")
            columns = [relation["target"], *relation["coefficients"]]
            comparable = frame[columns].apply(pd.to_numeric, errors="coerce").dropna()
            predicted = relation.get("intercept", 0)
            for variable, coefficient in relation["coefficients"].items():
                predicted = predicted + coefficient * comparable[variable]
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
        "ids": ids, "sex": sex, "measures": measures, "score_relations": relations,
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
