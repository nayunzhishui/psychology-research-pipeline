#!/usr/bin/env python3
"""Import an ASReview-like score file as a ranking-only human review queue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_queue(source: Path, output: Path) -> dict:
    rows = []
    with source.open("r", encoding="utf-8-sig") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not str(row.get("candidate_id", "")).strip():
                raise SystemExit(f"candidate_id missing at line {number}")
            try:
                score = float(row["score"])
            except (KeyError, TypeError, ValueError) as exc:
                raise SystemExit(f"numeric score missing at line {number}") from exc
            rows.append({"candidate_id": row["candidate_id"], "score": score})
    rows.sort(key=lambda item: (-item["score"], item["candidate_id"]))
    records = [
        {"candidate_id": item["candidate_id"], "rank": rank, "score": item["score"], "decision": "human-review-required"}
        for rank, item in enumerate(rows, 1)
    ]
    payload = {
        "schema_version": 1,
        "authority": "ranking-only",
        "records": records,
        "guardrail": "No automated include/exclude decision is permitted.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "complete", "authority": "ranking-only", "output": str(output.resolve()), "count": len(records)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(build_queue(Path(args.input).resolve(), Path(args.output).resolve()), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
