#!/usr/bin/env python3
"""Deterministic DOI/title deduplication for empirical evidence records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value)
    match = re.search(r"10\.\d{4,9}/\S+", value)
    return (match.group(0) if match else value).rstrip(".,;:)]} ")


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(char for char in value if char.isalnum())


def canonical_identity(row: dict[str, str]) -> tuple[str, str]:
    doi = normalize_doi(row.get("doi", ""))
    if doi:
        return "doi", doi
    pmid = normalize_text(row.get("pmid", ""))
    if pmid:
        return "pmid", pmid
    openalex_id = normalize_text(row.get("openalex_id", "").rsplit("/", 1)[-1])
    if openalex_id:
        return "openalex_id", openalex_id
    author = re.split(r"[,;]", row.get("authors", ""), maxsplit=1)[0]
    title = normalize_text(row.get("title", ""))
    if not title:
        return "insufficient_metadata", normalize_text(row.get("candidate_id", ""))
    return "title_author_year", "|".join([
        title, normalize_text(author), row.get("year", "").strip(),
    ])


def canonical_key(row: dict[str, str]) -> str:
    field, value = canonical_identity(row)
    return f"{field}:{value}"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dedupe(source: Path, output_dir: Path) -> dict:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    required = {"candidate_id", "title", "authors", "year", "doi"}
    missing = required - set(fields)
    if missing:
        return {"status": "blocked", "errors": [f"missing columns: {sorted(missing)}"]}

    output_dir.mkdir(parents=True, exist_ok=True)
    output_fields = fields + [name for name in [
        "study_id", "canonical_key", "duplicate_of", "duplicate_match_field", "dedup_status",
    ] if name not in fields]
    unique_rows = []
    duplicate_rows = []
    seen: dict[str, dict[str, str]] = {}
    for row in rows:
        row = dict(row)
        row["doi"] = normalize_doi(row.get("doi", ""))
        match_field, match_value = canonical_identity(row)
        key = f"{match_field}:{match_value}"
        row["canonical_key"] = key
        if key in seen:
            row["study_id"] = seen[key]["study_id"]
            row["duplicate_of"] = seen[key]["candidate_id"]
            row["duplicate_match_field"] = match_field
            row["dedup_status"] = "duplicate"
            duplicate_rows.append(row)
        else:
            row["study_id"] = f"study-{len(unique_rows) + 1:04d}"
            row["duplicate_of"] = ""
            row["duplicate_match_field"] = ""
            row["dedup_status"] = "unique"
            seen[key] = row
            unique_rows.append(row)

    deduplicated_path = output_dir / "去重候选文献_deduplicated_candidates.csv"
    duplicate_path = output_dir / "重复文献记录_duplicate_records.csv"
    for path, records in [(deduplicated_path, unique_rows), (duplicate_path, duplicate_rows)]:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=output_fields)
            writer.writeheader()
            writer.writerows(records)
    review_pairs = []
    for left_index, left in enumerate(unique_rows):
        for right in unique_rows[left_index + 1:]:
            left_title, right_title = normalize_text(left.get("title", "")), normalize_text(right.get("title", ""))
            if not left_title or not right_title:
                continue
            similarity = SequenceMatcher(None, left_title, right_title).ratio()
            left_author = normalize_text(re.split(r"[,;]", left.get("authors", ""), maxsplit=1)[0])
            right_author = normalize_text(re.split(r"[,;]", right.get("authors", ""), maxsplit=1)[0])
            years = {left.get("year", "").strip(), right.get("year", "").strip()} - {""}
            if similarity >= 0.92 and (left_author == right_author or len(years) == 1):
                review_pairs.append({
                    "left_candidate_id": left["candidate_id"], "right_candidate_id": right["candidate_id"],
                    "title_similarity": f"{similarity:.4f}", "same_first_author": str(left_author == right_author).lower(),
                    "review_status": "pending", "review_decision": "", "reviewer": "", "reviewed_at": "",
                })
    review_path = output_dir / "疑似重复人工复核_fuzzy_duplicate_candidates.csv"
    review_fields = ["left_candidate_id", "right_candidate_id", "title_similarity", "same_first_author", "review_status", "review_decision", "reviewer", "reviewed_at"]
    with review_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields)
        writer.writeheader(); writer.writerows(review_pairs)
    manifest = {
        "schema_version": 1, "status": "complete", "source": str(source.resolve()),
        "source_sha256": file_hash(source), "input_records": len(rows),
        "unique_records": len(unique_rows), "duplicate_records": len(duplicate_rows),
        "fuzzy_review_candidates": len(review_pairs),
        "deduplicated_file": str(deduplicated_path.resolve()),
        "duplicate_file": str(duplicate_path.resolve()),
        "fuzzy_review_file": str(review_path.resolve()),
    }
    manifest_path = output_dir / "文献去重清单_evidence_dedupe_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = dedupe(Path(args.input).resolve(), Path(args.output_dir).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "complete" else 3


if __name__ == "__main__":
    raise SystemExit(main())
