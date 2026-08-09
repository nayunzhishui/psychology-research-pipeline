#!/usr/bin/env python3
"""Deterministic task state for bounded research roles; never changes stage state."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

from contracts import RoleResult, TaskEnvelope


ROLE_STAGES = {
    "evidence": {"02_search", "03_library", "04_synthesis"},
    "research-design": {"00_scope", "01_protocol", "05_methods"},
    "data-measurement": {"05_methods", "06_data"},
    "statistics": {"07_analysis"},
    "result-verification": {"07_analysis", "08_results", "10_alignment"},
    "manuscript-submission": {"09_manuscript", "10_alignment", "11_review"},
}


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def model_validate(model, payload: dict) -> dict:
    if hasattr(model, "model_validate"):
        value = model.model_validate(payload)
        return value.model_dump(mode="json")
    return json.loads(model.parse_obj(payload).json())


def task_dir(run_dir: Path) -> Path:
    return run_dir / "日志" / "受控任务_controlled_tasks"


def append_event(run_dir: Path, event: dict) -> None:
    path = run_dir / "日志" / "事件记录_events.jsonl"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def dispatch(run_dir: Path, spec_path: Path) -> tuple[dict, int]:
    state_path = run_dir / "状态记录_state.json"
    if not state_path.is_file():
        return {"status": "blocked", "stop_reason": f"run state missing: {state_path}"}, 3
    state = json.loads(state_path.read_text(encoding="utf-8"))
    try:
        envelope = model_validate(TaskEnvelope, json.loads(spec_path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {"status": "blocked", "stop_reason": f"invalid task envelope: {exc}"}, 3
    if envelope["run_id"] != state["run_id"]:
        return {"status": "blocked", "stop_reason": "task run_id differs from run state"}, 3
    if envelope["stage"] not in ROLE_STAGES[envelope["role"]]:
        return {"status": "blocked", "stop_reason": "role is not permitted for requested stage"}, 3
    if any(item["sensitive"] for item in envelope["inputs"]):
        return {"status": "blocked", "stop_reason": "sensitive artifacts are forbidden in controlled task envelopes"}, 3
    for item in envelope["inputs"]:
        path = Path(item["path"]).expanduser().resolve()
        if not path.is_file() or sha256(path) != item["sha256"]:
            return {"status": "blocked", "stop_reason": f"task input provenance mismatch: {path}"}, 3
    tasks = task_dir(run_dir)
    tasks.mkdir(parents=True, exist_ok=True)
    path = tasks / f"{envelope['task_id']}.json"
    if path.exists():
        return {"status": "blocked", "stop_reason": f"task already exists: {envelope['task_id']}"}, 3
    record = {
        "schema_version": 1,
        "status": "dispatched",
        "created_at": now(),
        "updated_at": now(),
        "envelope": envelope,
        "attempts": [],
        "next_attempt": 1,
        "stage_state_at_dispatch": state.get("current_stage"),
    }
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    append_event(run_dir, {
        "timestamp": now(), "run_id": state["run_id"], "stage": envelope["stage"],
        "action": "dispatch-controlled-task", "status": "started", "tool": "research-orchestrator",
        "task_id": envelope["task_id"], "role": envelope["role"],
        "inputs": [item["sha256"] for item in envelope["inputs"]],
    })
    return {"status": "dispatched", "task_id": envelope["task_id"], "task_state": str(path.resolve())}, 0


def resume(run_dir: Path, task_id: str, result_path: Path) -> tuple[dict, int]:
    path = task_dir(run_dir) / f"{task_id}.json"
    if not path.is_file():
        return {"status": "blocked", "stop_reason": f"controlled task missing: {task_id}"}, 3
    record = json.loads(path.read_text(encoding="utf-8"))
    try:
        result = model_validate(RoleResult, json.loads(result_path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {"status": "blocked", "stop_reason": f"invalid role result: {exc}"}, 3
    if result["task_id"] != task_id:
        return {"status": "blocked", "stop_reason": "role result task_id mismatch"}, 3
    if result["attempt"] != record["next_attempt"]:
        return {"status": "blocked", "stop_reason": "role result attempt is not the expected attempt"}, 3
    if any(item["sensitive"] for item in [*result["inputs"], *result["outputs"]]):
        return {"status": "blocked", "stop_reason": "sensitive artifacts are forbidden in controlled role results"}, 3
    for item in [*result["inputs"], *result["outputs"]]:
        artifact = Path(item["path"]).expanduser().resolve()
        if not artifact.is_file() or sha256(artifact) != item["sha256"]:
            return {"status": "blocked", "stop_reason": f"role result provenance mismatch: {artifact}"}, 3
    record["attempts"].append({**result, "recorded_at": now(), "result_source_sha256": sha256(result_path)})
    envelope = record["envelope"]
    code = 0
    if result["status"] == "complete":
        needs_approval = envelope["human_approval_required"] or result["human_approval_required"]
        record["status"] = "awaiting-approval" if needs_approval else "complete"
        stop_reason = "human approval required" if needs_approval else ""
    elif result["status"] == "blocked":
        record["status"] = "blocked"
        stop_reason = result["stop_reason"]
        code = 3
    else:
        retryable = result["error_class"] in {"tool-transient", "network-transient", "format-repair"}
        significance_driven = result["error_class"] == "significance-driven" or "significan" in result["stop_reason"].lower()
        if retryable and not significance_driven and result["attempt"] <= envelope["max_retries"]:
            record["status"] = "retrying"
            record["next_attempt"] = result["attempt"] + 1
            stop_reason = result["stop_reason"]
        else:
            record["status"] = "blocked"
            if retryable and result["attempt"] > envelope["max_retries"]:
                stop_reason = f"retry limit exceeded after attempt {result['attempt']}: {result['stop_reason']}"
            elif significance_driven:
                stop_reason = "significance-driven retries are forbidden"
            else:
                stop_reason = result["stop_reason"]
            code = 3
    record["updated_at"] = now()
    record["stop_reason"] = stop_reason
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    run_state = json.loads((run_dir / "状态记录_state.json").read_text(encoding="utf-8"))
    append_event(run_dir, {
        "timestamp": now(), "run_id": run_state["run_id"], "stage": envelope["stage"],
        "action": "resume-controlled-task", "status": record["status"],
        "tool": "research-orchestrator", "task_id": task_id, "role": envelope["role"],
        "attempt": result["attempt"], "error_class": result["error_class"],
        "stop_reason": stop_reason,
    })
    return {
        "status": record["status"], "task_id": task_id, "attempt": result["attempt"],
        "next_attempt": record["next_attempt"], "stop_reason": stop_reason,
        "task_state": str(path.resolve()),
    }, code


def verify(run_dir: Path, task_id: str) -> tuple[dict, int]:
    path = task_dir(run_dir) / f"{task_id}.json"
    if not path.is_file():
        return {"status": "blocked", "stop_reason": f"controlled task missing: {task_id}"}, 3
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("status") != "complete" or not record.get("attempts"):
        return {"status": "blocked", "stop_reason": f"task is not complete: {record.get('status')}"}, 3
    artifacts = [*record["envelope"].get("inputs", []), *record["attempts"][-1].get("outputs", [])]
    errors = []
    for item in artifacts:
        artifact = Path(item["path"]).expanduser().resolve()
        if not artifact.is_file() or sha256(artifact) != item["sha256"]:
            errors.append(f"artifact provenance mismatch: {artifact}")
    if errors:
        return {"status": "blocked", "task_id": task_id, "stop_reason": "; ".join(errors)}, 3
    return {
        "status": "verified", "task_id": task_id, "role": record["envelope"]["role"],
        "stage": record["envelope"]["stage"], "attempts": len(record["attempts"]),
        "task_state": str(path.resolve()),
    }, 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    dispatch_parser = subparsers.add_parser("dispatch")
    dispatch_parser.add_argument("--run-dir", required=True)
    dispatch_parser.add_argument("--spec", required=True)
    resume_parser = subparsers.add_parser("resume")
    resume_parser.add_argument("--run-dir", required=True)
    resume_parser.add_argument("--task-id", required=True)
    resume_parser.add_argument("--result", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--run-dir", required=True)
    verify_parser.add_argument("--task-id", required=True)
    args = parser.parse_args()
    if args.command == "dispatch":
        payload, code = dispatch(Path(args.run_dir).resolve(), Path(args.spec).resolve())
    elif args.command == "resume":
        payload, code = resume(Path(args.run_dir).resolve(), args.task_id, Path(args.result).resolve())
    else:
        payload, code = verify(Path(args.run_dir).resolve(), args.task_id)
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
