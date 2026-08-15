#!/usr/bin/env python3
"""Generate the fixed longitudinal-SEM model ladder from a frozen specification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


STEP_IDS = [
    "data-and-scoring-freeze",
    "sample-and-wave-flow",
    "descriptives-and-missingness",
    "longitudinal-measurement-invariance",
    "traditional-clpm-comparator",
    "primary-ri-clpm",
    "stationarity-constraint-tests",
    "sex-group-measurement-invariance",
    "sex-group-direct-constraint-tests",
    "multiple-imputation-sensitivity",
    "cluster-robust-or-multilevel-sensitivity",
    "zero-heavy-outcome-sensitivity",
    "power-and-parameter-recovery",
    "independent-result-verification",
]

PACKAGES = {
    "core": [
        "lavaan", "semTools", "psych", "mice", "simsem", "powRICLPM",
        "effectsize", "performance", "parameters", "clubSandwich",
    ],
    "conditional": [
        "OpenMx", "blavaan", "brms", "tidySEM", "semPlot", "lme4",
        "marginaleffects", "emmeans", "DeclareDesign",
    ],
    "reserve": ["metafor", "metaSEM", "robvis"],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(spec_path: Path, output: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    errors = []
    if spec.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if len(spec.get("waves", [])) < 3:
        errors.append("at least three waves are required for the RI-CLPM workflow")
    if len(spec.get("constructs", [])) < 2:
        errors.append("at least two constructs are required")
    if not str(spec.get("analysis_id", "")).strip():
        errors.append("analysis_id is required")
    if not str(spec.get("missing_strategy", "")).strip():
        errors.append("missing_strategy is required")
    if errors:
        result = {"status": "blocked", "errors": errors}
        print(json.dumps(result, ensure_ascii=False))
        return result
    steps = [{
        "order": index,
        "step_id": step_id,
        "status": "pending",
        "human_approval_required": step_id in {
            "data-and-scoring-freeze", "primary-ri-clpm", "independent-result-verification",
        },
        "stop_on_failure": True,
    } for index, step_id in enumerate(STEP_IDS, 1)]
    payload = {
        "schema_version": 1,
        "analysis_id": spec["analysis_id"],
        "spec": str(spec_path.resolve()),
        "spec_sha256": sha256(spec_path),
        "status": "draft-human-approval-required",
        "analysis_classification": "confirmatory",
        "model_ladder": steps,
        "packages": PACKAGES,
        "restrictions": [
            "do not inspect primary results before plan approval",
            "do not retry or change models for statistical significance",
            "do not infer causality from observational longitudinal associations",
        ],
        "context": {
            "waves": spec["waves"], "constructs": spec["constructs"],
            "group_variable": spec.get("group_variable"),
            "cluster_variable": spec.get("cluster_variable"),
            "missing_strategy": spec["missing_strategy"],
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": payload["status"], "output": str(output.resolve()), "steps": len(steps)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = generate(Path(args.spec).resolve(), Path(args.output).resolve())
    if result["status"] == "blocked":
        return 3
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
