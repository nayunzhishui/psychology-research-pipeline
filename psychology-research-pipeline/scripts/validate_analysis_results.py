#!/usr/bin/env python3
"""Validate machine-readable model output and generate traceable result artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def resolved_path(value: object, base: Path) -> Path:
    path = Path(str(value)).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def validate_execution_provenance(run_dir: Path, source: Path) -> tuple[dict, list[str]]:
    """Bind model output to the immutable manifest produced by analysis_runner."""
    manifest_path = run_dir / "07_统计分析" / "分析执行清单_analysis_execution_manifest.json"
    if not manifest_path.is_file():
        return {}, [f"analysis execution manifest missing: {manifest_path}"]
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return {}, [f"invalid analysis execution manifest: {exc}"]

    errors: list[str] = []
    if payload.get("schema_version") != 2 or payload.get("status") != "executed":
        errors.append("analysis execution manifest is not a completed schema-v2 execution")
    if payload.get("executor") != "analysis_runner.py":
        errors.append("analysis execution manifest has an unrecognized executor")
    for key in ["inputs", "software", "packages", "code_files", "executions", "outputs"]:
        if not isinstance(payload.get(key), list) or not payload[key]:
            errors.append(f"analysis execution manifest has no {key}")
    if payload.get("random_seed") in {None, "", "not-reported"}:
        errors.append("analysis execution manifest has no random seed")

    for index, item in enumerate(payload.get("inputs", []), 1):
        if not isinstance(item, dict):
            errors.append(f"analysis input record {index} is not an object")
            continue
        input_path = resolved_path(item.get("path", ""), manifest_path.parent)
        if not input_path.is_file() or input_path.stat().st_size == 0:
            errors.append(f"analysis input missing or empty: {input_path}")
        elif item.get("sha256") != sha256(input_path) or item.get("bytes") != input_path.stat().st_size:
            errors.append(f"analysis input provenance mismatch: {input_path}")

    code_manifest = resolved_path(payload.get("code_manifest", ""), manifest_path.parent)
    if not code_manifest.is_file():
        errors.append(f"analysis code manifest missing: {code_manifest}")
    elif payload.get("code_manifest_sha256") != sha256(code_manifest):
        errors.append("analysis code manifest hash mismatch")

    code_hashes = payload.get("code_hashes", {})
    code_paths: set[Path] = set()
    for raw_path in payload.get("code_files", []):
        code_path = resolved_path(raw_path, manifest_path.parent)
        code_paths.add(code_path)
        if not code_path.is_file():
            errors.append(f"executed analysis code missing: {code_path}")
        elif code_hashes.get(str(code_path)) != sha256(code_path):
            errors.append(f"executed analysis code hash mismatch: {code_path}")

    executed_paths: set[Path] = set()
    for index, execution in enumerate(payload.get("executions", []), 1):
        if not isinstance(execution, dict):
            errors.append(f"execution record {index} is not an object")
            continue
        code_path = resolved_path(execution.get("code_file", ""), manifest_path.parent)
        executed_paths.add(code_path)
        if execution.get("exit_code") != 0:
            errors.append(f"execution record {index} has nonzero exit code")
        if not code_path.is_file() or execution.get("code_sha256") != sha256(code_path):
            errors.append(f"execution code hash mismatch: {code_path}")
        log_path = resolved_path(execution.get("log", ""), manifest_path.parent)
        if not log_path.is_file() or log_path.stat().st_size == 0:
            errors.append(f"execution log missing or empty: {log_path}")
        elif execution.get("log_sha256") != sha256(log_path):
            errors.append(f"execution log hash mismatch: {log_path}")
    if code_paths and executed_paths != code_paths:
        errors.append("execution records do not cover exactly the declared code files")

    for index, package in enumerate(payload.get("packages", []), 1):
        if not isinstance(package, dict) or not str(package.get("name", "")).strip() or str(package.get("version", "")).strip() in {"", "NA", "<NA>"}:
            errors.append(f"package provenance is incomplete at record {index}")
    for index, software in enumerate(payload.get("software", []), 1):
        if not isinstance(software, dict) or not str(software.get("name", "")).strip() or not str(software.get("version", "")).strip():
            errors.append(f"software provenance is incomplete at record {index}")

    output_paths: set[Path] = set()
    for index, output in enumerate(payload.get("outputs", []), 1):
        if not isinstance(output, dict):
            errors.append(f"output record {index} is not an object")
            continue
        output_path = resolved_path(output.get("path", ""), manifest_path.parent)
        output_paths.add(output_path)
        if not output_path.is_file() or output_path.stat().st_size == 0:
            errors.append(f"executed output missing or empty: {output_path}")
            continue
        if output.get("sha256") != sha256(output_path):
            errors.append(f"executed output hash mismatch: {output_path}")
        if output.get("bytes") != output_path.stat().st_size:
            errors.append(f"executed output byte count mismatch: {output_path}")

    source = source.resolve()
    if source not in output_paths:
        errors.append("model output is not listed in the analysis execution outputs")
    elif payload.get("model_output_sha256") != sha256(source):
        errors.append("model output hash differs from the analysis execution manifest")
    declared_model = resolved_path(payload.get("model_output", ""), manifest_path.parent)
    if declared_model != source:
        errors.append("validated model output is not the execution manifest model_output")
    return payload, errors


def validate(payload: dict) -> list[str]:
    required = {"schema_version", "analysis_id", "sample_n", "primary_model", "estimator", "converged", "post_check", "fit", "parameters", "deviations", "diagnostics"}
    errors = [f"model output fields missing: {sorted(required - set(payload))}"] if required - set(payload) else []
    if errors:
        return errors
    if payload["schema_version"] != 1:
        errors.append("model output schema_version must be 1")
    if not isinstance(payload["sample_n"], int) or payload["sample_n"] <= 0:
        errors.append("sample_n must be a positive integer")
    if payload["converged"] is not True:
        errors.append("primary model did not converge")
    if payload["post_check"] is not True:
        errors.append("primary model failed post-estimation checks")
    for name, value in payload.get("fit", {}).items():
        if not finite_number(value):
            errors.append(f"fit value is not finite: {name}")
    missing_fit = {"cfi", "rmsea", "srmr"} - set(payload.get("fit", {}))
    if missing_fit:
        errors.append(f"required fit indices missing: {sorted(missing_fit)}")
    diagnostics = payload.get("diagnostics", {})
    if diagnostics.get("negative_variances") != 0:
        errors.append(f"model diagnostics report negative variances: {diagnostics.get('negative_variances')}")
    if diagnostics.get("inadmissible_standardized") != 0:
        errors.append(f"model diagnostics report inadmissible standardized estimates: {diagnostics.get('inadmissible_standardized')}")
    if not payload.get("parameters"):
        errors.append("no model parameters supplied")
    seen = set()
    fields = ["estimate", "se", "ci_low", "ci_high", "p_value"]
    for index, item in enumerate(payload.get("parameters", []), 1):
        result_id = str(item.get("result_id", "")).strip()
        if not result_id or result_id in seen:
            errors.append(f"parameter {index} has missing or duplicate result_id")
        seen.add(result_id)
        for field in fields:
            if not finite_number(item.get(field)):
                errors.append(f"parameter {result_id or index} has non-finite {field}")
        if all(finite_number(item.get(field)) for field in ["estimate", "ci_low", "ci_high"]):
            if not item["ci_low"] <= item["estimate"] <= item["ci_high"]:
                errors.append(f"parameter {result_id or index} estimate lies outside its interval")
        if finite_number(item.get("se")) and item["se"] < 0:
            errors.append(f"parameter {result_id or index} has negative standard error")
        if finite_number(item.get("p_value")) and not 0 <= item["p_value"] <= 1:
            errors.append(f"parameter {result_id or index} p_value is outside [0, 1]")
        if item.get("role") not in {"primary", "secondary", "exploratory", "robustness"}:
            errors.append(f"parameter {result_id or index} has invalid role")
        if "standardized" in item and not finite_number(item.get("standardized")):
            errors.append(f"parameter {result_id or index} has non-finite standardized estimate")
    return errors


def replace_template(path: Path, text: str) -> None:
    if path.exists():
        current = path.read_text(encoding="utf-8", errors="ignore")
        if "__REQUIRED__" not in current and current.strip() and current != text:
            raise SystemExit(f"refusing to overwrite completed artifact: {path}")
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def generate(run_dir: Path, source: Path) -> dict:
    if not source.is_file():
        return {"status": "blocked", "errors": [f"model output missing: {source}"]}
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "blocked", "errors": [f"invalid model output JSON: {exc}"]}
    execution, provenance_errors = validate_execution_provenance(run_dir, source)
    errors = provenance_errors + validate(payload)
    if errors:
        return {"status": "blocked", "errors": errors}

    analysis_dir = run_dir / "07_统计分析"
    results_dir = run_dir / "08_结果与图表"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    verified_results = {"sample_n": payload["sample_n"]}
    for item in payload["parameters"]:
        rid = item["result_id"]
        verified_results.update({
            f"{rid}.estimate": item["estimate"], f"{rid}.se": item["se"],
            f"{rid}.ci_low": item["ci_low"], f"{rid}.ci_high": item["ci_high"],
            f"{rid}.p_value": item["p_value"],
        })
        rows.append(
            f"| {rid} | {item.get('term', '')} | {item['role']} | {item['estimate']} | "
            f"{item['se']} | [{item['ci_low']}, {item['ci_high']}] | {item['p_value']} |"
        )
    verified_path = results_dir / "已验证结果_verified_results.json"
    verified_path.write_text(json.dumps(verified_results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    table = (
        "# 结果表格\n\n## 样本流\n\n"
        f"分析样本量为 {payload['sample_n']}；样本流须与正文和图表保持一致。\n\n"
        "## 描述统计\n\n描述统计由对应分析输出提供，不在此自动推断。\n\n"
        "## 测量模型\n\n测量模型结论须引用测量不变性输出。\n\n"
        "## 主要模型\n\n| result_id | term | role | estimate | SE | 95% CI | p |\n"
        "|---|---|---|---:|---:|---|---:|\n" + "\n".join(rows) +
        "\n\n## 组间检验\n\n只报告直接的约束检验，不比较分组显著性。\n\n"
        "## 稳健性\n\n稳健性结果见独立检查文件。"
    )
    report = (
        "# 统计分析报告\n\n## 环境与输入\n\n"
        f"输入 `{source.name}`，SHA-256 `{sha256(source)}`；估计量为 {payload['estimator']}。\n\n"
        f"## 样本和描述\n\n最终分析样本量为 {payload['sample_n']}。\n\n"
        "## 测量模型\n\n测量模型及跨波可比性必须由相应输出单独支持。\n\n"
        f"## 主要模型\n\n{payload['primary_model']} 已收敛，post-check 通过；估计与效应及区间见结果表格。\n\n"
        "## 次要与探索性分析\n\n按 role 字段区分主要、次要与探索性结果。\n\n"
        "## 诊断与稳健性\n\n收敛与估计后检查通过；稳健性只按输入记录报告。\n\n"
        f"## 偏离\n\n已登记偏离 {len(payload['deviations'])} 项。"
    )
    robustness = payload.get("robustness", [])
    robustness_lines = "\n".join(f"- {item.get('name')}: {item.get('conclusion')}" for item in robustness) or "- 未提供稳健性输出；不得声称已完成。"
    results_text = (
        "# 结果写作稿\n\n## 参与者与流失\n\n"
        f"主要模型分析样本量为 {payload['sample_n']}；流失机制需另据数据审计报告。\n\n"
        "## 描述与测量\n\n描述统计和测量不变性不得从结构模型结果反推。\n\n"
        "## 主要结果\n\n主要结果均来自已验证参数表，属于纵向预测关联，不自动构成因果证据。\n\n"
        "## 次要结果\n\n按预先指定的 role 字段呈现。\n\n## 稳健性\n\n见稳健性检查文件。\n\n"
        "## 探索性结果与偏离\n\n探索性结果和偏离必须明确标记。"
    )
    figure_plan = (
        "# 图表计划\n\n## 正文表\n\n主要参数表及置信区间。\n\n## 正文图\n\n仅绘制不泄露个体轨迹的汇总图。\n\n"
        "## 补充材料\n\n模型诊断、完整参数与稳健性分析。\n\n## 隐私与可访问性\n\n不展示可识别个体数据；图形使用可辨色彩和文本说明。"
    )
    robustness_text = (
        "# 稳健性检查\n\n## 预设检查\n\n仅接受计划或偏离记录中定义的分析。\n\n## 结果\n\n" + robustness_lines +
        "\n\n## 与主结论关系\n\n不得仅凭显著性变化判断一致性。\n\n## 未解决风险\n\n未提供的检查保持未解决状态。"
    )
    replace_template(analysis_dir / "统计分析报告_analysis_report.md", report)
    replace_template(analysis_dir / "结果表格_results_tables.md", table)
    replace_template(results_dir / "结果写作稿_results.md", results_text)
    replace_template(results_dir / "图表计划_figure_table_plan.md", figure_plan)
    replace_template(results_dir / "稳健性检查_robustness_checks.md", robustness_text)
    deviation_path = analysis_dir / "分析偏离记录_analysis_deviation_log.csv"
    if "__REQUIRED__" in deviation_path.read_text(encoding="utf-8", errors="ignore"):
        lines = ["deviation_id,timestamp,planned,actual,reason,impact,exploratory,manuscript_disclosure,decision"]
        if payload["deviations"]:
            for index, item in enumerate(payload["deviations"], 1):
                values = [f"DEV-{index:03d}", item.get("timestamp", "not-reported"), item.get("planned", ""), item.get("actual", ""), item.get("reason", ""), item.get("impact", ""), str(item.get("exploratory", True)), item.get("manuscript_disclosure", "required"), item.get("decision", "review")]
                lines.append(",".join(json.dumps(value, ensure_ascii=False) for value in values))
        else:
            lines.append("DEV-000,not-applicable,no deviation,no deviation,none,none,false,无偏离,verified")
        deviation_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    generated_outputs = [verified_path, analysis_dir / "统计分析报告_analysis_report.md", analysis_dir / "结果表格_results_tables.md"]
    execution_outputs = [resolved_path(item["path"], analysis_dir) for item in execution["outputs"]]
    outputs = list(dict.fromkeys([*execution_outputs, *generated_outputs]))
    code_manifest_path = resolved_path(execution["code_manifest"], analysis_dir)
    code_manifest = json.loads(code_manifest_path.read_text(encoding="utf-8"))
    data_files: list[str] = []
    file_hashes: dict[str, str] = {}
    if code_manifest.get("data"):
        data_path = resolved_path(code_manifest["data"], code_manifest_path.parent)
        data_files.append(str(data_path))
        file_hashes[str(data_path)] = code_manifest.get("data_sha256", "")
    for raw_path in code_manifest.get("data_files", []):
        data_path = resolved_path(raw_path, code_manifest_path.parent)
        if str(data_path) not in data_files:
            data_files.append(str(data_path))
        file_hashes[str(data_path)] = code_manifest.get("file_hashes", {}).get(raw_path, "")
    spec_path = resolved_path(code_manifest.get("spec", ""), code_manifest_path.parent) if code_manifest.get("spec") else None
    spec = {}
    if spec_path and spec_path.is_file():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    execution_manifest_path = analysis_dir / "分析执行清单_analysis_execution_manifest.json"
    manifest = {
        "schema_version": 2, "data_files": data_files, "file_hashes": file_hashes,
        "software": execution["software"], "packages": execution["packages"],
        "code_files": execution["code_files"], "code_hashes": execution["code_hashes"],
        "random_seed": execution.get("random_seed"),
        "analysis_plan": str(spec_path) if spec_path else payload["analysis_id"],
        "analysis_id": payload["analysis_id"], "deviations": payload["deviations"],
        "outputs": [str(path.resolve()) for path in outputs],
        "output_hashes": {str(path.resolve()): sha256(path) for path in outputs},
        "executions": execution["executions"],
        "execution_manifest": str(execution_manifest_path.resolve()),
        "execution_manifest_sha256": sha256(execution_manifest_path),
        "model_output": str(source.resolve()), "model_output_sha256": sha256(source),
        "execution_status": "verified",
        "converged": True, "post_check": True,
    }
    manifest_path = analysis_dir / "分析清单_analysis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "verified", "verified_results": str(verified_path.resolve()),
        "analysis_manifest": str(manifest_path.resolve()),
        "execution_manifest": str(execution_manifest_path.resolve()), "outputs": manifest["outputs"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    result = generate(Path(args.run_dir).resolve(), Path(args.input).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "verified" else 3


if __name__ == "__main__":
    raise SystemExit(main())
