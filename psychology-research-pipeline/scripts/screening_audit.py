#!/usr/bin/env python3
"""Audit independent dual-reviewer screening and produce PRISMA/risk-of-bias artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def audit(source: Path, output_dir: Path, reviewers: list[str], adjudicator: str) -> tuple[dict, int]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"candidate_id", "stage", "reviewer", "decision", "reason", "decided_at"}
    if not rows or required - set(rows[0]):
        return {"status": "blocked", "errors": ["screening input missing required rows or columns"]}, 3
    allowed = {"include", "exclude", "uncertain"}
    errors = [f"invalid decision: {row['decision']}" for row in rows if row["decision"] not in allowed]
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["candidate_id"], row["stage"]), []).append(row)
    consensus, conflicts, unresolved, missing_dual = [], 0, 0, 0
    for (candidate_id, stage), items in grouped.items():
        by_reviewer = {row["reviewer"]: row for row in items}
        missing = [name for name in reviewers if name not in by_reviewer]
        if missing:
            missing_dual += 1
            consensus.append({"candidate_id": candidate_id, "stage": stage, "decision": "pending", "basis": "missing-reviewer", "reason": "; ".join(missing)})
            continue
        first, second = (by_reviewer[name] for name in reviewers)
        if first["decision"] == second["decision"]:
            decision, basis = first["decision"], "dual-agreement"
            reason = first["reason"] if first["reason"] == second["reason"] else f"{first['reason']} | {second['reason']}"
        else:
            conflicts += 1
            if adjudicator in by_reviewer:
                decision, basis, reason = by_reviewer[adjudicator]["decision"], "adjudicated", by_reviewer[adjudicator]["reason"]
            else:
                decision, basis, reason = "pending", "unresolved-conflict", f"{first['decision']} vs {second['decision']}"
                unresolved += 1
        consensus.append({"candidate_id": candidate_id, "stage": stage, "decision": decision, "basis": basis, "reason": reason})
    output_dir.mkdir(parents=True, exist_ok=True)
    consensus_path = output_dir / "双人筛选裁决表_dual_screening_consensus.csv"
    with consensus_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "stage", "decision", "basis", "reason"])
        writer.writeheader(); writer.writerows(consensus)
    counts = {
        "records_screened": len({row["candidate_id"] for row in rows}),
        "screening_records": len(rows), "conflicts": conflicts,
        "unresolved_conflicts": unresolved, "missing_dual_review": missing_dual,
        "included": sum(row["decision"] == "include" for row in consensus),
        "excluded": sum(row["decision"] == "exclude" for row in consensus),
        "pending": sum(row["decision"] == "pending" for row in consensus),
    }
    prisma_path = output_dir / "PRISMA计数_prisma_counts.json"
    prisma_path.write_text(json.dumps({"schema_version": 1, **counts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    risk_path = output_dir / "偏倚风险评估_risk_of_bias.csv"
    included_ids = sorted({row["candidate_id"] for row in consensus if row["decision"] == "include"})
    fields = ["candidate_id", "design_tool", "selection", "attrition", "measurement", "confounding", "selective_reporting", "analysis", "overall", "reviewer", "evidence_location", "status"]
    with risk_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for candidate_id in included_ids:
            writer.writerow({"candidate_id": candidate_id, "status": "pending-independent-assessment"})
    status = "blocked" if errors or unresolved or missing_dual else "complete"
    payload = {
        "status": status, **counts, "errors": errors,
        "consensus": str(consensus_path.resolve()), "prisma_counts": str(prisma_path.resolve()),
        "risk_of_bias_template": str(risk_path.resolve()),
    }
    return payload, 3 if status == "blocked" else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--reviewers", nargs=2, required=True)
    parser.add_argument("--adjudicator", required=True)
    args = parser.parse_args()
    payload, code = audit(Path(args.input).resolve(), Path(args.output_dir).resolve(), args.reviewers, args.adjudicator)
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
