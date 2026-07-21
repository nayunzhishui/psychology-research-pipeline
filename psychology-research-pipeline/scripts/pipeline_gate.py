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
    required = {"schema_version", "data_files", "file_hashes", "software", "packages", "code_files", "random_seed", "analysis_plan", "deviations", "outputs"}
    missing = required - set(payload)
    if missing:
        errors.append(f"analysis manifest keys missing: {sorted(missing)}")
        return errors
    for raw_path in payload.get("data_files", []):
        source = Path(raw_path).expanduser()
        if not source.is_absolute():
            source = (path.parent / source).resolve()
        if not source.is_file():
            errors.append(f"analysis source missing: {raw_path}")
            continue
        expected_hash = payload.get("file_hashes", {}).get(raw_path)
        if expected_hash and expected_hash != sha256(source):
            errors.append(f"analysis source hash mismatch: {raw_path}")
    for raw_path in payload.get("code_files", []):
        code_path = Path(raw_path).expanduser()
        if not code_path.is_absolute():
            code_path = (path.parent / code_path).resolve()
        if not code_path.is_file():
            errors.append(f"analysis code missing: {raw_path}")
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
