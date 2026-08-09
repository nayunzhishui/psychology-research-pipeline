#!/usr/bin/env python3
"""Build a disposable retrieval index from verified evidence-ledger records."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from contracts import EvidenceLedgerRecord


INDEXABLE_STATUSES = {"fulltext-verified", "claim-verified"}
SAFE_FIELDS = (
    "evidence_id", "candidate_id", "title", "doi", "zotero_item_key",
    "study_design", "sample", "measures", "waves", "claim_ids",
    "evidence_location", "correction_status", "verification_status",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_record(payload: dict) -> dict:
    if hasattr(EvidenceLedgerRecord, "model_validate"):
        record = EvidenceLedgerRecord.model_validate(payload)  # type: ignore[attr-defined]
        return record.model_dump(mode="json")  # type: ignore[attr-defined]
    return json.loads(EvidenceLedgerRecord.parse_obj(payload).json())


def build_index(run_dir: Path, ledger: Path) -> dict:
    if not ledger.is_file():
        raise SystemExit(f"evidence ledger missing: {ledger}")
    records: list[dict] = []
    with ledger.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(validate_record(json.loads(line)))
            except Exception as exc:
                raise SystemExit(f"invalid evidence ledger record at line {line_number}: {exc}") from exc

    verified = sorted(
        (record for record in records if record["verification_status"] in INDEXABLE_STATUSES),
        key=lambda record: record["evidence_id"],
    )
    index_dir = run_dir / ".cache" / "retrieval-index"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "index.json"
    index_payload = {
        "schema_version": 1,
        "purpose": "rebuildable auxiliary locator; not an evidence source or decision authority",
        "source_ledger": str(ledger.resolve()),
        "source_sha256": sha256(ledger),
        "records": [{field: record[field] for field in SAFE_FIELDS} for record in verified],
    }
    index_path.write_text(json.dumps(index_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_dir = run_dir / "04_文献筛选与小综述"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "证据账本索引清单_evidence_index_manifest.json"
    result = {
        "schema_version": 1,
        "status": "complete",
        "ledger": str(ledger.resolve()),
        "ledger_sha256": sha256(ledger),
        "index": str(index_path.resolve()),
        "index_sha256": sha256(index_path),
        "included_verified": len(verified),
        "excluded_unverified": len(records) - len(verified),
        "guardrail": "Retrieval output is only a locator; inclusion, claims, and numbers require ledger verification.",
    }
    manifest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--ledger", required=True)
    args = parser.parse_args()
    print(json.dumps(build_index(Path(args.run_dir).resolve(), Path(args.ledger).resolve()), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
