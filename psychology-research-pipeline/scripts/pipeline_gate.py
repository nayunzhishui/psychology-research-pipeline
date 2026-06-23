#!/usr/bin/env python3
"""Validate stage artifacts and advance a research pipeline state."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


STAGES = [
    "01_scope", "02_protocol", "03_search", "04_library", "05_screening",
    "06_synthesis", "07_methods", "08_analysis", "09_manuscript", "10_review",
]

REQUIRED = {
    "01_scope": ["01_scope/project_brief.md", "01_scope/research_question.md"],
    "02_protocol": ["02_protocol/reporting_plan.md", "02_protocol/protocol.md"],
    "03_search": ["03_search/search_log.csv", "03_search/candidates.csv"],
    "04_library": ["04_library/zotero_manifest.csv", "04_library/acquisition_report.md"],
    "05_screening": ["05_screening/screening_log.csv", "05_screening/evidence_matrix.csv"],
    "06_synthesis": ["06_synthesis/mini_review.md", "06_synthesis/claim_evidence_map.csv"],
    "07_methods": ["07_methods/methods_plan.md", "07_methods/analysis_plan.md"],
    "08_analysis": ["08_analysis/data_audit.md", "08_analysis/results.md", "08_analysis/analysis_manifest.json"],
    "09_manuscript": ["09_manuscript/manuscript.md", "09_manuscript/references.bib", "09_manuscript/citation_audit.md"],
    "10_review": ["10_review/editorial_decision.md", "10_review/reviewer_report.md", "10_review/revision_matrix.csv", "10_review/final_audit.md"],
}

CSV_HEADERS = {
    "03_search/search_log.csv": {"search_id", "database", "query", "run_at", "result_count"},
    "03_search/candidates.csv": {"candidate_id", "title", "year", "doi", "database", "dedup_status"},
    "04_library/zotero_manifest.csv": {"candidate_id", "zotero_item_key", "attachment_status", "validation_status"},
    "05_screening/screening_log.csv": {"candidate_id", "stage", "decision", "reason"},
    "05_screening/evidence_matrix.csv": {"study_id", "candidate_id", "design", "sample", "main_findings", "evidence_location"},
    "06_synthesis/claim_evidence_map.csv": {"claim_id", "claim_text", "study_ids", "verification_status"},
    "10_review/revision_matrix.csv": {"comment_id", "severity", "comment", "response", "status"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def atomic_json(path: Path, payload: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def validate_file(run_dir: Path, relative: str) -> list[str]:
    path = run_dir / relative
    errors: list[str] = []
    if not path.is_file():
        return [f"missing: {relative}"]
    if path.stat().st_size == 0:
        return [f"empty: {relative}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    if "__REQUIRED__" in text or "[TODO]" in text:
        errors.append(f"placeholder remains: {relative}")
    if path.suffix.lower() == ".md" and len(text.strip()) < 80:
        errors.append(f"too little content: {relative}")
    if path.suffix.lower() == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
        expected = CSV_HEADERS.get(relative, set())
        actual = set(rows[0].keys()) if rows else set(csv.DictReader(text.splitlines()).fieldnames or [])
        missing = expected - actual
        if missing:
            errors.append(f"missing CSV columns in {relative}: {sorted(missing)}")
        if not rows:
            errors.append(f"no data rows: {relative}")
    if path.suffix.lower() == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON {relative}: {exc}")
    if relative.endswith("references.bib") and "@" not in text:
        errors.append(f"no BibTeX entries: {relative}")
    return errors


def append_gate_event(run_dir: Path, state: dict, stage: str, passed: bool, errors: list[str]) -> None:
    event = {
        "timestamp": now(), "run_id": state["run_id"], "stage": stage,
        "action": "gate_check", "status": "completed" if passed else "failed",
        "tool": "pipeline_gate.py", "inputs": REQUIRED[stage], "outputs": [],
        "decision": "pass" if passed else "revise", "reason": None,
        "error": None if passed else "; ".join(errors), "next_gate": stage,
    }
    with (run_dir / "logs" / "events.jsonl").open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--stage", required=True, choices=STAGES)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--advance", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    state_path = run_dir / "state.json"
    manifest_path = run_dir / "manifest.json"
    if not state_path.is_file():
        parser.error(f"state.json missing: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    errors = [error for relative in REQUIRED[args.stage] for error in validate_file(run_dir, relative)]
    passed = not errors
    append_gate_event(run_dir, state, args.stage, passed, errors)
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
    index = STAGES.index(args.stage)
    if index == len(STAGES) - 1:
        state["status"] = "complete"
        state["current_stage"] = None
    else:
        state["current_stage"] = STAGES[index + 1]
    state["updated_at"] = now()
    atomic_json(state_path, state)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {"schema_version": 1, "run_id": state["run_id"], "artifacts": []}
    by_path = {item["path"]: item for item in manifest.get("artifacts", [])}
    for relative in REQUIRED[args.stage]:
        path = run_dir / relative
        by_path[relative] = {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size, "status": "validated"}
    manifest["artifacts"] = [by_path[key] for key in sorted(by_path)]
    atomic_json(manifest_path, manifest)
    print(f"ADVANCED TO: {state['current_stage'] or 'complete'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
