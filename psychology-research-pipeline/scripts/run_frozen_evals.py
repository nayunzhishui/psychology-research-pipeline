#!/usr/bin/env python3
"""Run deterministic frozen policy cases before prompt-level evaluations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


POLICY = {
    "rag-decides-inclusion": "blocked",
    "retry-for-significance": "blocked",
    "send-sensitive-rows-to-agent": "blocked",
    "asreview-auto-excludes": "blocked",
    "write-unverified-result": "blocked",
    "cite-claim-verified-ledger": "allowed",
}


def run(path: Path) -> tuple[dict, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = []
    for case in payload.get("cases", []):
        actual = POLICY.get(case.get("action"), "unknown")
        results.append({
            "id": case.get("id"), "expected": case.get("expected"), "actual": actual,
            "passed": actual == case.get("expected"),
        })
    passed = sum(item["passed"] for item in results)
    result = {
        "status": "passed" if results and passed == len(results) else "failed",
        "total": len(results), "passed": passed, "failed": len(results) - passed,
        "results": results,
    }
    return result, 0 if result["status"] == "passed" else 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    args = parser.parse_args()
    result, code = run(Path(args.cases).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
