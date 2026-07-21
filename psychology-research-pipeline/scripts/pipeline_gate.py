#!/usr/bin/env python3
"""Validate stage artifacts and advance schema-v2 research pipeline state."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

from pipeline_schema import CSV_HEADERS, PLACEHOLDER, SCHEMA_VERSION, STAGE_BY_ID, STAGE_IDS, STAGES, relative_artifacts


SEMANTIC_GROUPS = {
    "00_scope": [["估计对象"], ["推论边界"], ["主要研究问题"]],
    "01_protocol": [["主要", "primary"], ["偏离"], ["伦理"], ["开放科学", "数据可用性"]],
    "05_methods": [["估计对象"], ["缺失"], ["测量不变性", "不适用"], ["性别", "不适用"], ["聚类", "不适用"], ["多重", "multiplicity", "不适用"], ["稳健性"]],
    "06_data": [["ID", "标识"], ["重复"], ["计分"], ["缺失"], ["流失", "不适用"], ["分布"], ["隐私"]],
    "07_analysis": [["收敛", "不适用"], ["估计", "效应"], ["区间", "置信"], ["偏离"]],
    "08_results": [["主要结果"], ["稳健性"], ["探索性", "无探索性"]],
    "09_manuscript": [["摘要"], ["方法"], ["结果"], ["讨论"], ["声明"]],
    "10_alignment": [["样本量"], ["p值", "p 值"], ["表图"], ["unsupported"], ["overextended"]],
    "11_review": [["模拟性质"], ["目标期刊"], ["方法"], ["统计"], ["开放科学"], ["最终状态"]],
}


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing: {path.name}"]
    if path.stat().st_size == 0:
        return [f"empty: {path.name}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    if PLACEHOLDER in text or "[TODO]" in text:
        errors.append(f"placeholder remains: {path.name}")
    suffix = path.suffix.lower()
    if suffix == ".md" and len(text.strip()) < 120:
        errors.append(f"too little content: {path.name}")
    elif suffix == ".csv":
        headers, rows = read_csv(path)
        expected = set(CSV_HEADERS.get(path.name, []))
        missing = expected - set(headers)
        if missing:
            errors.append(f"missing CSV columns in {path.name}: {sorted(missing)}")
        if not rows:
            errors.append(f"no data rows: {path.name}")
    elif suffix == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON {path.name}: {exc}")
    elif suffix == ".bib" and "@" not in text:
        errors.append(f"no BibTeX entries: {path.name}")
    return errors


def validate_semantics(stage_id: str, paths: list[Path], strict: bool) -> list[str]:
    if not strict:
        return []
    corpus = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in paths if path.suffix.lower() in {".md", ".csv"})
    errors = []
    for alternatives in SEMANTIC_GROUPS.get(stage_id, []):
        if not any(term.lower() in corpus.lower() for term in alternatives):
            errors.append(f"semantic evidence missing for {stage_id}: {' / '.join(alternatives)}")
    return errors


def validate_analysis_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return errors
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return errors
    required = {
        "schema_version", "data_files", "file_hashes", "software", "packages", "code_files",
        "code_hashes", "random_seed", "analysis_plan", "deviations", "outputs", "output_hashes",
        "executions", "execution_manifest", "execution_manifest_sha256", "model_output",
        "model_output_sha256", "execution_status",
    }
    missing = required - set(payload)
    if missing:
        errors.append(f"analysis manifest keys missing: {sorted(missing)}")
        return errors
    if payload.get("schema_version") != 2 or payload.get("execution_status") != "verified":
        errors.append("analysis manifest is not a verified schema-v2 manifest")
    for key in ["data_files", "software", "packages", "code_files", "executions", "outputs"]:
        if not isinstance(payload.get(key), list) or not payload[key]:
            errors.append(f"analysis manifest has no {key}")
    if payload.get("random_seed") in {None, "", "not-reported"}:
        errors.append("analysis manifest has no random seed")
    if not str(payload.get("analysis_plan", "")).strip():
        errors.append("analysis manifest has no frozen analysis plan")
    for raw_path in payload.get("data_files", []):
        source = Path(raw_path).expanduser()
        if not source.is_absolute():
            source = (path.parent / source).resolve()
        if not source.is_file():
            errors.append(f"analysis source missing: {raw_path}")
            continue
        expected_hash = payload.get("file_hashes", {}).get(str(source), payload.get("file_hashes", {}).get(raw_path))
        if not expected_hash or expected_hash != sha256(source):
            errors.append(f"analysis source hash mismatch: {raw_path}")
    for raw_path in payload.get("code_files", []):
        code_path = Path(raw_path).expanduser()
        if not code_path.is_absolute():
            code_path = (path.parent / code_path).resolve()
        if not code_path.is_file():
            errors.append(f"analysis code missing: {raw_path}")
        elif payload.get("code_hashes", {}).get(str(code_path), payload.get("code_hashes", {}).get(raw_path)) != sha256(code_path):
            errors.append(f"analysis code hash mismatch: {raw_path}")
    for raw_path in payload.get("outputs", []):
        output_path = Path(raw_path).expanduser()
        if not output_path.is_absolute():
            output_path = (path.parent / output_path).resolve()
        if not output_path.is_file() or output_path.stat().st_size == 0:
            errors.append(f"analysis output missing or empty: {raw_path}")
        elif payload.get("output_hashes", {}).get(str(output_path), payload.get("output_hashes", {}).get(raw_path)) != sha256(output_path):
            errors.append(f"analysis output hash mismatch: {raw_path}")

    execution_path = Path(payload.get("execution_manifest", "")).expanduser()
    if not execution_path.is_absolute():
        execution_path = (path.parent / execution_path).resolve()
    expected_execution_path = path.parent / "分析执行清单_analysis_execution_manifest.json"
    if execution_path != expected_execution_path.resolve():
        errors.append("analysis manifest does not reference the canonical execution manifest")
    if not execution_path.is_file():
        errors.append(f"analysis execution manifest missing: {execution_path}")
        return errors
    if payload.get("execution_manifest_sha256") != sha256(execution_path):
        errors.append("analysis execution manifest hash mismatch")
        return errors
    try:
        execution = json.loads(execution_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid analysis execution manifest: {exc}")
        return errors
    if execution.get("schema_version") != 2 or execution.get("status") != "executed" or execution.get("executor") != "analysis_runner.py":
        errors.append("analysis execution manifest is not a completed runner execution")
    for key in ["inputs", "software", "packages", "code_files", "executions", "outputs"]:
        if not isinstance(execution.get(key), list) or not execution[key]:
            errors.append(f"analysis execution manifest has no {key}")
    if payload.get("software") != execution.get("software") or payload.get("packages") != execution.get("packages"):
        errors.append("analysis software/package provenance differs from execution manifest")
    if payload.get("code_files") != execution.get("code_files") or payload.get("code_hashes") != execution.get("code_hashes"):
        errors.append("analysis code provenance differs from execution manifest")
    if payload.get("executions") != execution.get("executions"):
        errors.append("analysis execution records differ from execution manifest")
    if payload.get("random_seed") != execution.get("random_seed"):
        errors.append("analysis random seed differs from execution manifest")

    code_manifest = Path(str(execution.get("code_manifest", ""))).expanduser().resolve()
    if not code_manifest.is_file() or execution.get("code_manifest_sha256") != sha256(code_manifest):
        errors.append("analysis code manifest provenance mismatch")
    for index, item in enumerate(execution.get("inputs", []), 1):
        if not isinstance(item, dict):
            errors.append(f"analysis input record {index} is not an object")
            continue
        input_path = Path(str(item.get("path", ""))).expanduser().resolve()
        if not input_path.is_file() or input_path.stat().st_size == 0:
            errors.append(f"analysis execution input missing or empty: {input_path}")
        elif not item.get("sha256") or item["sha256"] != sha256(input_path) or item.get("bytes") != input_path.stat().st_size:
            errors.append(f"analysis execution input provenance mismatch: {input_path}")
    for index, item in enumerate(execution.get("packages", []), 1):
        if not isinstance(item, dict) or not str(item.get("name", "")).strip() or str(item.get("version", "")).strip() in {"", "NA", "<NA>"}:
            errors.append(f"analysis package provenance incomplete at record {index}")
    for index, item in enumerate(execution.get("software", []), 1):
        if not isinstance(item, dict) or not str(item.get("name", "")).strip() or not str(item.get("version", "")).strip():
            errors.append(f"analysis software provenance incomplete at record {index}")
            continue
        executable = Path(str(item.get("executable", ""))).expanduser().resolve()
        if not executable.is_file() or not item.get("executable_sha256") or item["executable_sha256"] != sha256(executable):
            errors.append(f"analysis software executable provenance mismatch: {executable}")

    code_paths = {Path(value).expanduser().resolve() for value in execution.get("code_files", [])}
    executed_paths: set[Path] = set()
    for index, item in enumerate(execution.get("executions", []), 1):
        if not isinstance(item, dict):
            errors.append(f"execution record {index} is not an object")
            continue
        code_path = Path(str(item.get("code_file", ""))).expanduser().resolve()
        executed_paths.add(code_path)
        if item.get("exit_code") != 0:
            errors.append(f"execution record has nonzero exit code: {code_path}")
        if not code_path.is_file() or item.get("code_sha256") != sha256(code_path):
            errors.append(f"execution code hash mismatch: {code_path}")
        log_path = Path(str(item.get("log", ""))).expanduser().resolve()
        if not log_path.is_file() or log_path.stat().st_size == 0:
            errors.append(f"execution log missing or empty: {log_path}")
        elif not item.get("log_sha256") or item["log_sha256"] != sha256(log_path):
            errors.append(f"execution log hash mismatch: {log_path}")
    if code_paths and executed_paths != code_paths:
        errors.append("execution records do not cover exactly the declared code files")

    execution_outputs: dict[Path, dict] = {}
    for index, item in enumerate(execution.get("outputs", []), 1):
        if not isinstance(item, dict):
            errors.append(f"execution output record {index} is not an object")
            continue
        output_path = Path(str(item.get("path", ""))).expanduser().resolve()
        execution_outputs[output_path] = item
        if not output_path.is_file() or output_path.stat().st_size == 0:
            errors.append(f"executed output missing or empty: {output_path}")
        elif not item.get("sha256") or item["sha256"] != sha256(output_path) or item.get("bytes") != output_path.stat().st_size:
            errors.append(f"executed output provenance mismatch: {output_path}")
    model_output = Path(payload.get("model_output", "")).expanduser().resolve()
    declared_model_output = Path(execution.get("model_output", "")).expanduser().resolve()
    if model_output != declared_model_output or model_output not in execution_outputs:
        errors.append("model output is not bound to an execution output record")
    elif payload.get("model_output_sha256") != sha256(model_output) or execution.get("model_output_sha256") != sha256(model_output):
        errors.append("model output hash mismatch across analysis provenance")
    return errors


def validate_alignment(path: Path) -> list[str]:
    if not path.is_file():
        return []
    _, rows = read_csv(path)
    errors = []
    for index, row in enumerate(rows, start=2):
        support = (row.get("支持程度") or "").strip().lower()
        status = (row.get("处理状态") or "").strip().lower()
        if support in {"unsupported", "overextended"} and status not in {"resolved", "已解决", "删除", "降级", "补证"}:
            errors.append(f"unresolved {support} claim at {path.name}:{index}")
    return errors


def validate_review(path: Path) -> list[str]:
    if not path.is_file():
        return []
    _, rows = read_csv(path)
    errors = []
    for index, row in enumerate(rows, start=2):
        severity = (row.get("severity") or "").strip().lower()
        status = (row.get("status") or "").strip().lower()
        if severity in {"critical", "major", "致命", "重大"} and status not in {"resolved", "closed", "已解决", "已关闭"}:
            errors.append(f"unresolved {severity} review item at {path.name}:{index}")
    return errors


def validate_literature_controls(run_dir: Path, stage_id: str, strict: bool) -> list[str]:
    if not strict:
        return []
    errors = []
    if stage_id == "02_search":
        search_dir = run_dir / "02_证据检索"
        plan = search_dir / "检索计划_search_plan.json"
        ingest = search_dir / "题录导入清单_evidence_import_manifest.json"
        candidates = search_dir / "候选文献表_candidate_records.csv"
        for path in [plan, ingest]:
            if not path.is_file():
                errors.append(f"strict literature control missing: {path.name}")
        if ingest.is_file():
            try:
                payload = json.loads(ingest.read_text(encoding="utf-8"))
                if payload.get("candidate_records_sha256") != sha256(candidates):
                    errors.append("candidate records hash differs from evidence import manifest")
                if not payload.get("source_exports"):
                    errors.append("evidence import manifest contains no immutable source exports")
                if payload.get("search_id") == "zotero-library" or any(
                    Path(item.get("path", "")).name == "zotero-library.bib"
                    for item in payload.get("source_exports", [])
                ):
                    errors.append("whole-library Zotero integration export is not admissible project evidence")
            except json.JSONDecodeError:
                errors.append(f"invalid JSON {ingest.name}")
    elif stage_id == "04_synthesis":
        synthesis_dir = run_dir / "04_文献筛选与小综述"
        coverage = synthesis_dir / "证据覆盖审计_evidence_coverage_audit.json"
        dedupe = synthesis_dir / "文献去重清单_evidence_dedupe_manifest.json"
        family = synthesis_dir / "研究家族识别清单_study_family_manifest.json"
        for path in [coverage, dedupe, family]:
            if not path.is_file():
                errors.append(f"strict literature control missing: {path.name}")
        for path in [coverage, dedupe, family]:
            if not path.is_file():
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                errors.append(f"invalid JSON {path.name}")
                continue
            source = Path(payload.get("source", ""))
            if not source.is_file():
                errors.append(f"literature manifest source missing for {path.name}: {source}")
            elif payload.get("source_sha256") != sha256(source):
                errors.append(f"literature manifest source hash mismatch: {path.name}")
            if path == coverage:
                requirements = Path(payload.get("requirements", ""))
                if not requirements.is_file():
                    errors.append(f"coverage requirements missing: {requirements}")
                elif payload.get("requirements_sha256") != sha256(requirements):
                    errors.append("coverage requirements hash mismatch")
                if payload.get("status") != "ready" or payload.get("missing_core_slots"):
                    errors.append(f"core evidence coverage is blocked: {payload.get('missing_core_slots', [])}")
    return errors


def validate_presearch_controls(run_dir: Path, stage_id: str, strict: bool) -> list[str]:
    if not strict or stage_id not in {"00_scope", "01_protocol"}:
        return []
    path = run_dir / "01_标准与协议" / "检索前准备审计_presearch_readiness.json"
    if not path.is_file():
        return [f"strict pre-search control missing: {path.name}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON {path.name}: {exc}"]
    errors = []
    source = Path(payload.get("protocol_source", ""))
    if not source.is_file():
        errors.append(f"pre-search protocol source missing: {source}")
    elif payload.get("protocol_sha256") != sha256(source):
        errors.append("pre-search protocol hash mismatch")
    if not payload.get("ready_for_search") or payload.get("status") != "ready":
        errors.append("pre-search readiness is blocked")
    if payload.get("blocking_items"):
        errors.append(f"unresolved pre-search blockers: {[item.get('id') for item in payload['blocking_items']]}")
    approval = payload.get("approval", {})
    if approval.get("scope_status") != "approved" or approval.get("protocol_status") != "frozen":
        errors.append("scope/protocol approval is not frozen")
    if payload.get("approval_errors") or payload.get("ethics_errors"):
        errors.append("approval or ethics verification remains unresolved")
    return errors


def append_gate_event(run_dir: Path, state: dict, stage_id: str, passed: bool, errors: list[str]) -> None:
    event = {
        "timestamp": now(), "run_id": state["run_id"], "stage": stage_id,
        "action": "gate_check", "status": "completed" if passed else "failed",
        "tool": "pipeline_gate.py", "inputs": relative_artifacts(STAGE_BY_ID[stage_id]), "outputs": [],
        "decision": "pass" if passed else "revise", "reason": None,
        "error": None if passed else "; ".join(errors), "next_gate": stage_id,
    }
    log_path = run_dir / "日志" / "事件记录_events.jsonl"
    log_path.parent.mkdir(exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--stage", required=True, choices=STAGE_IDS)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--advance", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    state_path = run_dir / "状态记录_state.json"
    manifest_path = run_dir / "文件清单_manifest.json"
    if not state_path.is_file():
        parser.error(f"状态记录_state.json missing: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("schema_version") != SCHEMA_VERSION:
        parser.error(f"Unsupported schema version: {state.get('schema_version')}; expected {SCHEMA_VERSION}")

    stage = STAGE_BY_ID[args.stage]
    paths = [run_dir / relative for relative in relative_artifacts(stage)]
    errors = [error for path in paths for error in validate_file(path)]
    strict = state.get("mode") in {"strict", "top-journal-prep"}
    errors.extend(validate_semantics(args.stage, paths, strict))
    errors.extend(validate_presearch_controls(run_dir, args.stage, strict))
    errors.extend(validate_literature_controls(run_dir, args.stage, strict))
    if args.stage == "07_analysis":
        errors.extend(validate_analysis_manifest(run_dir / stage["dir"] / "分析清单_analysis_manifest.json"))
    elif args.stage == "10_alignment":
        errors.extend(validate_alignment(run_dir / stage["dir"] / "来源对齐表_source_alignment_table.csv"))
    elif args.stage == "11_review":
        errors.extend(validate_review(run_dir / stage["dir"] / "修改矩阵_revision_matrix.csv"))

    append_gate_event(run_dir, state, args.stage, not errors, errors)
    if errors:
        print("GATE FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GATE PASSED")
    if args.check:
        return 0
    if state.get("current_stage") != args.stage:
        parser.error(f"Cannot advance {args.stage}; current stage is {state.get('current_stage')}")

    if args.stage not in state["completed_stages"]:
        state["completed_stages"].append(args.stage)
    index = STAGE_IDS.index(args.stage)
    if index == len(STAGES) - 1:
        state["status"] = "complete"
        state["current_stage"] = None
    else:
        state["current_stage"] = STAGE_IDS[index + 1]
    state["updated_at"] = now()
    atomic_json(state_path, state)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_path = {item["path"]: item for item in manifest.get("artifacts", [])}
    for path in paths:
        relative = path.relative_to(run_dir).as_posix()
        by_path[relative] = {
            "path": relative, "sha256": sha256(path), "bytes": path.stat().st_size,
            "status": "validated", "stage": args.stage,
        }
    manifest["artifacts"] = [by_path[key] for key in sorted(by_path)]
    atomic_json(manifest_path, manifest)
    print(f"ADVANCED TO: {state['current_stage'] or 'complete'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
