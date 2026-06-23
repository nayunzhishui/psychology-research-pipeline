#!/usr/bin/env python3
"""Append a structured event to a research pipeline run."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--status", required=True, choices=["started", "completed", "failed", "blocked", "warning"])
    parser.add_argument("--tool", default="codex")
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--decision")
    parser.add_argument("--reason")
    parser.add_argument("--error")
    parser.add_argument("--next-gate")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    state_path = run_dir / "state.json"
    if not state_path.is_file():
        parser.error(f"state.json missing: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": state["run_id"],
        "stage": args.stage,
        "action": args.action,
        "status": args.status,
        "tool": args.tool,
        "inputs": args.input,
        "outputs": args.output,
        "decision": args.decision,
        "reason": args.reason,
        "error": args.error,
        "next_gate": args.next_gate,
    }
    log_path = run_dir / "logs" / "events.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps(event, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
