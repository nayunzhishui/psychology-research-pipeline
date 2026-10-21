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
    "paragraph_id",
    "argument_role",
    "warrant_text",
    "counterevidence_handling",
    "drafting_status",
    "figure_ids",
    "figure_role",
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
    "legacy_reading_status",
    "abstract_status",
    "introduction_status",
    "methods_status",
    "data_status",
    "results_status",
    "discussion_status",
    "conclusion_status",
    "references_trace_status",
    "professor_briefing_status",
    "abstract_audit",
    "introduction_gap",
    "procedure_ethics",
    "discussion_interpretation",
    "paper_type",
    "reporting_standard_applicable",
    "author_claim",
    "results_demonstrate",
    "reader_inference",
    "source_package_status",
    "consistency_audit_status",
    "briefing_2min",
    "anticipated_professor_questions",
    "key_figure_ids",
    "figure_claim_audit",
    "figure_data_traceability",
    "figure_redraw_or_reuse_plan",
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
    assert "deep-reading-contract.md" in texts[0]

    for root in SKILL_ROOTS:
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
        assert "references/literature-operations-contract.md" in skill_text
        assert "_v2`、`_v3`" not in skill_text


def test_deep_reading_contract_and_entrypoints_are_synchronized() -> None:
    contracts = [root / "references" / "deep-reading-contract.md" for root in SKILL_ROOTS]
    texts = [path.read_text(encoding="utf-8") for path in contracts]
    assert texts[0] == texts[1] == texts[2]
    for marker in (
        "### 摘要",
        "### 引言",
        "### 方法",
        "### 数据",
        "### 结果",
        "### 讨论",
        "### 结论",
        "professor_briefing_status",
        "Reviewer B",
        "阅读笔记",
        "证据提纲",
        "reading-note-style.md",
        "knowledge-vault-contract.md",
    ):
        assert marker in texts[0]
    assert "阅读总结.md" not in texts[0]

    entrypoints = (
        SKILL_ROOTS[0] / "subskills" / "deep-reading" / "SKILL.md",
        SKILL_ROOTS[1] / "subskills" / "literature-matrix" / "SKILL.md",
        SKILL_ROOTS[2] / "subskills" / "deep-reading" / "SKILL.md",
    )
    for path in entrypoints:
        text = path.read_text(encoding="utf-8")
        assert "deep-reading-contract.md" in text
        assert "reading-note-style.md" in text
        assert "七章节" in text

    note_templates = (
        SKILL_ROOTS[0] / "templates" / "阅读笔记模板_reading_note.md",
        SKILL_ROOTS[1] / "templates" / "阅读笔记模板_reading_note.md",
        SKILL_ROOTS[2] / "templates" / "reading_card.md",
    )
    for path in note_templates:
        assert path.exists(), path
        template_text = path.read_text(encoding="utf-8")
        assert "一句话结论" in template_text
        assert "关键图表怎么读" in template_text
        assert "#page=" in template_text
        assert "派生视图" not in template_text
    for root in SKILL_ROOTS[:2]:
        retired = root / "templates" / "深度阅读报告模板_deep_reading_report.md"
        assert not retired.exists(), retired


def test_reading_note_style_and_vault_contracts_are_synchronized() -> None:
    for name, markers in (
        ("reading-note-style.md", ("不许出现的写法", "常用译名", "#page=")),
        ("knowledge-vault-contract.md", ("激活扩散", "userIgnoreFilters", "关联")),
    ):
        texts = [(root / "references" / name).read_text(encoding="utf-8") for root in SKILL_ROOTS]
        assert texts[0] == texts[1] == texts[2], name
        for marker in markers:
            assert marker in texts[0], (name, marker)


def test_shared_reading_scripts_are_synchronized() -> None:
    for name in (
        "format_reading_matrix.py",
        "export_evidence_outline.py",
        "init_knowledge_vault.py",
        "spreading_activation.py",
    ):
        texts = [(root / "scripts" / name).read_text(encoding="utf-8") for root in SKILL_ROOTS]
        assert texts[0] == texts[1] == texts[2], name


def test_outline_concept_and_vault_entrypoints_exist() -> None:
    outline_templates = (
        SKILL_ROOTS[0] / "templates" / "证据提纲模板_evidence_outline.md",
        SKILL_ROOTS[1] / "templates" / "证据提纲模板_evidence_outline.md",
        SKILL_ROOTS[2] / "templates" / "evidence_outline.md",
    )
    for path in outline_templates:
        text = path.read_text(encoding="utf-8")
        assert "#### 主张" in text, path
        assert "**证据**" in text, path
    concept_templates = (
        SKILL_ROOTS[0] / "templates" / "概念卡模板_concept_card.md",
        SKILL_ROOTS[1] / "templates" / "概念卡模板_concept_card.md",
        SKILL_ROOTS[2] / "templates" / "concept_card.md",
    )
    for path in concept_templates:
        text = path.read_text(encoding="utf-8")
        assert "## 关联" in text, path
        assert "spreading_activation.py" in text, path
    for root in SKILL_ROOTS:
        assert (root / "subskills" / "knowledge-vault" / "SKILL.md").exists(), root
        assert "knowledge-vault-contract.md" in (root / "SKILL.md").read_text(encoding="utf-8"), root


def test_writing_contract_and_manuscript_entrypoints_are_synchronized() -> None:
    contracts = [
        root / "references" / "evidence-grounded-writing-contract.md"
        for root in SKILL_ROOTS
    ]
    texts = [path.read_text(encoding="utf-8") for path in contracts]
    assert texts[0] == texts[1] == texts[2]
    for marker in (
        "写作前论证包",
        "文章类型路由",
        "主张 → 证据综合 → 推理桥梁",
        "作者主张",
        "认知神经科学综述",
        "不计算总分",
    ):
        assert marker in texts[0]

    for root in SKILL_ROOTS:
        main_text = (root / "SKILL.md").read_text(encoding="utf-8")
        manuscript_text = (
            root / "subskills" / "manuscript-write" / "SKILL.md"
        ).read_text(encoding="utf-8")
        assert "references/evidence-grounded-writing-contract.md" in main_text
        assert "evidence-grounded-writing-contract.md" in manuscript_text


def test_figure_contract_and_figure_entrypoints_are_synchronized() -> None:
    contracts = [
        root / "references" / "evidence-figure-contract.md"
        for root in SKILL_ROOTS
    ]
    texts = [path.read_text(encoding="utf-8") for path in contracts]
    assert texts[0] == texts[1] == texts[2]
    for marker in (
        "figure_id,claim_ids,figure_question",
        "颜色不作为唯一编码",
        "关键图反向阅读",
        "实证心理学",
        "通用心理学综述",
        "认知神经科学综述",
        "不设置固定图数",
        "qa-passed",
        "版权、再利用与图像生成",
        "参与者`n`",
        "森林图",
    ):
        assert marker in texts[0]

    for root in SKILL_ROOTS:
        main_text = (root / "SKILL.md").read_text(encoding="utf-8")
        manuscript_text = (
            root / "subskills" / "manuscript-write" / "SKILL.md"
        ).read_text(encoding="utf-8")
        source_text = (
            root / "subskills" / "source-alignment" / "SKILL.md"
        ).read_text(encoding="utf-8")
        review_text = (
            root / "subskills" / "submission-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        assert "references/evidence-figure-contract.md" in main_text
        assert "evidence-figure-contract.md" in manuscript_text
        assert "evidence-figure-contract.md" in source_text
        assert "evidence-figure-contract.md" in review_text


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


def test_writing_templates_support_paragraph_level_argument_audit() -> None:
    source_alignment_templates = (
        SKILL_ROOTS[0] / "templates" / "来源对齐表模板_source_alignment_table.csv",
        SKILL_ROOTS[1] / "templates" / "来源对齐表模板_source_alignment_table.csv",
        SKILL_ROOTS[2] / "templates" / "来源对齐表模板_source_alignment_table.csv",
    )
    required = {
        "paragraph_id",
        "claim_id",
        "argument_role",
        "warrant_text",
        "counterevidence_handling",
        "reviewer_status",
        "figure_id",
        "figure_source_pointer",
        "figure_caption_audit",
        "figure_final_size_status",
    }
    for path in source_alignment_templates:
        assert required <= _header(path), path

    cog_templates = (
        SKILL_ROOTS[2] / "templates" / "review_outline.md",
        SKILL_ROOTS[2] / "templates" / "prewriting_synthesis_plan.md",
        SKILL_ROOTS[2] / "templates" / "review_methods_plan.md",
    )
    for path in cog_templates:
        assert "REM 与情绪记忆" not in path.read_text(encoding="utf-8"), path


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
