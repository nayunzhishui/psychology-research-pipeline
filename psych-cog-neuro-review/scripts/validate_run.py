#!/usr/bin/env python3
"""Validate a psych-cog-neuro-review run directory.

This script checks structure, key CSV headers, Zotero acquisition artifacts,
and lightweight ID continuity. It does not judge scholarly correctness.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REQUIRED_DIRS = [
    "00_scope",
    "01_protocol",
    "02_search",
    "03_library",
    "04_screening",
    "05_extraction",
    "06_synthesis",
    "07_prewrite",
    "08_manuscript",
    "09_audit",
]

REQUIRED_FILES_BY_MODE = {
    "lite": [
        "00_scope/review_scope.md",
        "02_search/search_strategy.md",
        "05_extraction/literature_matrix.csv",
        "06_synthesis/prewriting_synthesis_plan.md",
        "07_prewrite/section_argument_plan.md",
    ],
    "standard": [
        "00_scope/review_scope.md",
        "01_protocol/review_protocol.md",
        "02_search/database_search_log.csv",
        "02_search/candidate_records.csv",
        "03_library/library_acquisition_manifest.csv",
        "03_library/zotero_manifest.csv",
        "03_library/zotero_collection_plan.md",
        "03_library/acquisition_report.md",
        "04_screening/screening_table.csv",
        "05_extraction/literature_matrix.csv",
        "05_extraction/neural_mechanism_matrix.csv",
        "05_extraction/quality_appraisal.csv",
        "06_synthesis/claim_evidence_map.csv",
        "07_prewrite/review_methods_plan.md",
        "07_prewrite/section_argument_plan.md",
        "08_manuscript/review_draft.md",
        "09_audit/paragraph_source_alignment_matrix.csv",
    ],
    "strict": [
        "00_scope/review_scope.md",
        "01_protocol/reporting_plan.md",
        "01_protocol/review_protocol.md",
        "02_search/database_search_log.csv",
        "02_search/candidate_records.csv",
        "03_library/library_acquisition_manifest.csv",
        "03_library/zotero_manifest.csv",
        "03_library/zotero_collection_plan.md",
        "03_library/acquisition_report.md",
        "04_screening/screening_table.csv",
        "04_screening/prisma_flow_counts.csv",
        "05_extraction/literature_matrix.csv",
        "05_extraction/neural_mechanism_matrix.csv",
        "05_extraction/quality_appraisal.csv",
        "06_synthesis/claim_evidence_map.csv",
        "06_synthesis/evidence_gap_register.csv",
        "07_prewrite/review_methods_plan.md",
        "07_prewrite/section_argument_plan.md",
        "08_manuscript/review_draft.md",
        "09_audit/paragraph_source_alignment_matrix.csv",
        "09_audit/unsupported_or_overstated_claims.md",
    ],
}

CSV_HEADERS = {
    "02_search/database_search_log.csv": [
        "search_id",
        "database",
        "platform",
        "query",
        "filters",
        "run_at",
        "result_count",
        "export_file",
        "notes",
    ],
    "02_search/candidate_records.csv": [
        "candidate_id",
        "title",
        "authors",
        "year",
        "doi",
        "pmid",
        "cnki_id",
        "wanfang_id",
        "vip_id",
        "source",
        "abstract",
        "landing_url",
        "database",
        "search_id",
        "dedup_status",
        "record_status",
    ],
    "03_library/zotero_manifest.csv": [
        "candidate_id",
        "zotero_item_key",
        "title",
        "year",
        "doi",
        "collection",
        "attachment_key",
        "attachment_status",
        "validation_status",
        "source_url",
        "notes",
    ],
    "03_library/library_acquisition_manifest.csv": [
        "candidate_id",
        "study_id",
        "zotero_item_key",
        "bibtex_key",
        "parent_item_key",
        "attachment_key",
        "title",
        "authors",
        "year",
        "doi",
        "pmid",
        "cnki_id",
        "wanfang_id",
        "vip_id",
        "source",
        "collection",
        "collection_key",
        "attachment_status",
        "full_text_status",
        "validation_status",
        "acquisition_status",
        "dedup_group",
        "source_url",
        "local_path",
        "temporary_file_state",
        "notes",
    ],
    "05_extraction/quality_appraisal.csv": [
        "study_id",
        "candidate_id",
        "citation",
        "study_type",
        "run_mode",
        "custom_appraisal_framework",
        "formal_tool_used",
        "formal_tool_reason",
        "formal_tool_result",
        "sample_quality",
        "design_quality",
        "measurement_quality",
        "neuroscience_method_quality",
        "sleep_method_quality",
        "analysis_quality",
        "confounding_bias",
        "selective_reporting_risk",
        "applicability_to_review",
        "overall_judgment",
        "judgment_basis",
        "evidence_location",
        "notes",
    ],
    "09_audit/paragraph_source_alignment_matrix.csv": [
        "review_paragraph_id",
        "review_sentence_or_claim_id",
        "review_claim_text",
        "claim_type",
        "is_claim_bearing",
        "in_text_citation",
        "claim_id",
        "source_id",
        "citation_key",
        "source_author_year",
        "source_title",
        "source_location",
        "page_or_location",
        "source_passage_excerpt",
        "support_strength",
        "evidence_role",
        "does_source_support_exact_claim",
        "problem_type",
        "revision_suggestion",
        "notes",
    ],
}

FORBIDDEN_PATH_HINTS = [
    "zotero.sqlite",
    "storage/",
    "downloads/",
    ".pdf",
    "cookie",
    "token",
    "password",
]


def read_mode(root: Path) -> str:
    state_path = root / "state.json"
    if not state_path.exists():
        return "standard"
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "standard"
    mode = str(data.get("run_mode", "standard")).strip().lower()
    return mode if mode in REQUIRED_FILES_BY_MODE else "standard"


def read_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            return []


def check_header(path: Path, expected: list[str]) -> list[str]:
    if not path.exists():
        return []
    actual = read_header(path)
    missing = [col for col in expected if col not in actual]
    return missing


def collect_ids(path: Path, column: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if column not in (reader.fieldnames or []):
            return set()
        return {
            str(row.get(column, "")).strip()
            for row in reader
            if str(row.get(column, "")).strip()
            and not str(row.get(column, "")).strip().startswith("__")
        }


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_run.py <path-to-cog_neuro_review_run>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        print(f"ERROR: run directory does not exist: {root}", file=sys.stderr)
        return 2

    mode = read_mode(root)

    for rel in REQUIRED_DIRS:
        if not (root / rel).exists():
            errors.append(f"missing directory: {rel}")

    for rel in REQUIRED_FILES_BY_MODE[mode]:
        if not (root / rel).exists():
            errors.append(f"missing required file for {mode}: {rel}")

    for rel, expected in CSV_HEADERS.items():
        missing = check_header(root / rel, expected)
        if missing:
            errors.append(f"missing CSV columns in {rel}: {', '.join(missing)}")

    candidate_ids = collect_ids(root / "02_search/candidate_records.csv", "candidate_id")
    library_candidate_ids = collect_ids(root / "03_library/library_acquisition_manifest.csv", "candidate_id")
    zotero_candidate_ids = collect_ids(root / "03_library/zotero_manifest.csv", "candidate_id")

    if candidate_ids and library_candidate_ids:
        orphan_library = library_candidate_ids - candidate_ids
        if orphan_library:
            warnings.append(f"library records not found in candidate_records: {len(orphan_library)}")

    if zotero_candidate_ids and library_candidate_ids:
        orphan_zotero = zotero_candidate_ids - library_candidate_ids
        if orphan_zotero:
            warnings.append(f"zotero_manifest records not found in library_acquisition_manifest: {len(orphan_zotero)}")

    for row in read_rows(root / "03_library/library_acquisition_manifest.csv"):
        local_path = str(row.get("local_path", "")).strip().lower()
        temporary_state = str(row.get("temporary_file_state", "")).strip().lower()
        if local_path and any(hint in local_path for hint in FORBIDDEN_PATH_HINTS):
            warnings.append("library manifest contains local/PDF/Zotero path hints; confirm these are not committed artifacts")
            break
        if temporary_state in {"committed", "uploaded", "git"}:
            errors.append("temporary_file_state suggests a temporary/full-text artifact was committed")
            break

    claim_ids = collect_ids(root / "06_synthesis/claim_evidence_map.csv", "claim_id")
    audit_claim_ids = collect_ids(root / "09_audit/paragraph_source_alignment_matrix.csv", "claim_id")
    if claim_ids and audit_claim_ids:
        unaudited = claim_ids - audit_claim_ids
        if unaudited:
            warnings.append(f"claim IDs not found in paragraph-source audit: {len(unaudited)}")

    print(f"Run mode: {mode}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
