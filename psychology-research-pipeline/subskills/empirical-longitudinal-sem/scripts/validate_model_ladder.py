#!/usr/bin/env python3
"""Fail closed when a longitudinal-SEM plan omits or reorders a required gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_analysis_plan import STEP_IDS


def validate(path: Path) -> tuple[dict, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    steps = payload.get("model_ladder", [])
    observed = [item.get("step_id") for item in steps]
    errors = []
    missing = [step for step in STEP_IDS if step not in observed]
    if missing:
        errors.append(f"missing required steps: {missing}")
    if observed != STEP_IDS:
        errors.append("model ladder order differs from the required fail-closed sequence")
    for index, item in enumerate(steps, 1):
        if item.get("order") != index:
            errors.append(f"invalid order value for {item.get('step_id')}")
        if item.get("stop_on_failure") is not True:
            errors.append(f"stop_on_failure must be true for {item.get('step_id')}")
    result = {"status": "valid" if not errors else "blocked", "errors": errors, "observed_steps": observed}
    return result, 0 if not errors else 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    result, code = validate(Path(args.plan).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
