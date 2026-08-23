from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOTS = (
    REPO_ROOT / "psychology-research-pipeline",
    REPO_ROOT / "psych-literature-review-workflow",
    REPO_ROOT / "psych-cog-neuro-review",
)

CORE_CANDIDATE_FIELDS = {
    "candidate_id",
    "first_author",
    "source_databases",
    "search_ids",
    "raw_export_files",
    "first_seen_round",
    "last_seen_round",
    "appearance_count",
    "normalized_title",
    "identity_key",
    "record_status",
}

CORE_CLAIM_FIELDS = {
    "claim_id",
    "candidate_id",
    "study_id",
    "report_id",
    "study_family_id",
    "support_status",
    "claim_ceiling",
    "support_carrier_type",
    "support_carrier_value",
    "fulltext_location",
    "construct_match",
    "estimand_level",
    "result_direction",
    "reviewer_status",
    "paper_one_sentence_conclusion",
    "paragraph_function",
    "cautious_paraphrase",
    "comparison_or_companion_sources",
    "relation_to_project_results",
    "prohibited_wording",
}

CORE_MATRIX_FIELDS = {
    "reading_level",
    "reading_scope",
    "pass1_orientation_status",
    "pass2_methods_results_status",
    "pass3_critical_writing_status",
    "research_question",
    "study_hypotheses",
    "claimed_novelty",
    "theory_framework",
    "data_source",
    "data_cleaning_exclusions",
    "measurement_reliability_validity",
    "scoring_details",
    "missing_data_handling",
    "covariates",
    "model_diagnostics",
    "robustness_sensitivity",
    "key_references_to_trace",
    "relation_to_project_results",
    "paragraph_level_use",
}

CORE_LEDGER_FIELDS = {
    "candidate_id",
    "report_id",
    "study_id",
    "study_family_id",
    "title",
    "doi",
    "database",
    "search_id",
    "source_record_id",
    "fulltext_status",
    "correction_status",
    "retraction_status",
    "family_status",
    "fulltext_location",
    "reviewer_status",
    "verified_at",
}


def _header(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return set(next(csv.reader(handle)))


def test_literature_contract_is_identical_and_routed_by_all_main_skills() -> None:
    contracts = [
        root / "references" / "literature-operations-contract.md"
        for root in SKILL_ROOTS
    ]
    texts = [path.read_text(encoding="utf-8") for path in contracts]
    assert texts[0] == texts[1] == texts[2]
    assert "历轮全部已见题录" in texts[0]
    assert "Reviewer B" in texts[0]
    assert "Zotero.Attachments.importFromFile" in texts[0]
    assert "三轮六模块" in texts[0]
    assert "paper_one_sentence_conclusion" in texts[0]

    for root in SKILL_ROOTS:
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
        assert "references/literature-operations-contract.md" in skill_text
        assert "_v2`、`_v3`" not in skill_text


def test_candidate_matrix_and_claim_templates_cover_shared_contract() -> None:
    candidate_templates = (
        SKILL_ROOTS[0] / "templates" / "候选文献表模板_candidate_records.csv",
        SKILL_ROOTS[1] / "templates" / "候选文献表模板_candidate_records.csv",
        SKILL_ROOTS[2] / "templates" / "candidate_records.csv",
    )
    claim_templates = (
        SKILL_ROOTS[0] / "templates" / "主张证据对应表模板_claim_evidence_map.csv",
        SKILL_ROOTS[1] / "templates" / "主张证据对应表模板_claim_evidence_map.csv",
        SKILL_ROOTS[2] / "templates" / "claim_evidence_map.csv",
    )
    matrix_templates = (
        SKILL_ROOTS[0] / "templates" / "文献阅读矩阵模板_literature_matrix.csv",
        SKILL_ROOTS[1] / "templates" / "文献阅读矩阵模板_literature_matrix.csv",
        SKILL_ROOTS[2] / "templates" / "literature_matrix.csv",
    )
    ledger_templates = (
        SKILL_ROOTS[0] / "templates" / "证据覆盖台账模板_evidence_ledger.csv",
        SKILL_ROOTS[1] / "templates" / "证据覆盖台账模板_evidence_ledger.csv",
        SKILL_ROOTS[2] / "templates" / "evidence_ledger.csv",
    )

    for path in candidate_templates:
        assert CORE_CANDIDATE_FIELDS <= _header(path), path
    for path in claim_templates:
        assert CORE_CLAIM_FIELDS <= _header(path), path
    for path in matrix_templates:
        assert CORE_MATRIX_FIELDS <= _header(path), path
    for path in ledger_templates:
        assert CORE_LEDGER_FIELDS <= _header(path), path


def test_zotero_subskills_do_not_prefer_connector_for_batch_ingest() -> None:
    for root in SKILL_ROOTS:
        text = (root / "subskills" / "zotero-ingest" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "Connector 仅" in text or "Connector 只" in text
        assert "三方查重" in text
        assert "缺 PDF" in text
        assert "新建父条目" in text


def test_repository_has_no_retired_fourth_workflow() -> None:
    if (REPO_ROOT / ".git").exists():
        retired = REPO_ROOT / "psych-review-workflow"
        assert not retired.exists() or not any(path.is_file() for path in retired.rglob("*"))
