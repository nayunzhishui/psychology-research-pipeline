# Review stage contracts / 综述阶段合同

## Purpose

This file adapts the psychology-research-pipeline stage logic to a literature-review workflow. It covers all steps before review drafting and audit, especially the steps equivalent to empirical-project work before data analysis and empirical manuscript writing.

## Run layout

Each run lives at `<project-root>/cog_neuro_review_run/` unless the user specifies another folder.

```text
state.json
manifest.json
logs/decisions.md
00_scope/
01_protocol/
02_search/
03_library/
04_screening/
05_extraction/
06_synthesis/
07_prewrite/
08_manuscript/
09_audit/
```

Artifacts are UTF-8. CSV files use one header row and RFC 4180 quoting. Use `unknown` rather than an invented value. Dates use ISO 8601.

## Gate contracts

### 00 Scope

Required: `workspace_inventory.md`, `review_scope.md`, `concept_map.md`.

Pass when the review type, topic boundary, population/species boundary, developmental/clinical boundary, core constructs, neuroscience methods, seed papers, source availability, and excluded claims are explicit. For REM and emotional memory, REM sleep, NREM sleep, sleep deprivation, sleep quality, emotional memory, fear extinction, encoding, consolidation, retrieval, and reconsolidation must not be collapsed into one vague construct.

### 01 Protocol

Required: `reporting_plan.md`, `review_protocol.md`, `review_stage_gates.md`.

Pass when review type, reporting standard, databases, languages, year range, inclusion/exclusion criteria, full-text handling, extraction fields, quality-appraisal plan, AI-use policy, deviation policy, and target output style are frozen. Do not claim systematic/scoping status unless the protocol supports it.

### 02 Search

Required: `search_strategy.md`, `database_search_log.csv`, `candidate_records.csv`.

`database_search_log.csv` minimum columns: `search_id,database,platform,query,filters,run_at,result_count,export_file,notes`.

`candidate_records.csv` minimum columns: `candidate_id,title,authors,year,doi,pmid,cnki_id,source,abstract,landing_url,database,search_id,dedup_status,record_status`.

Pass when bilingual concept blocks exist; database-specific queries are reproducible; exact counts, dates, and filters are logged; at least two appropriate academic databases are used unless justified; citation chasing and Zotero/library searches are separately logged; no convenience source is described as exhaustive.

### 03 Acquire

Required: `library_acquisition_manifest.csv`, `zotero_collection_plan.md`, `acquisition_report.md`.

Manifest minimum columns: `candidate_id,study_id,zotero_item_key,bibtex_key,title,year,doi,pmid,cnki_id,collection,attachment_status,full_text_status,validation_status,dedup_group,source_url,notes`.

Allowed attachment/full-text status: `readable_pdf`, `metadata_only`, `abstract_only`, `access_blocked`, `duplicate_skipped`, `failed_validation`, `user_provided`.

Pass when every retained candidate has a metadata and access status; duplicates are grouped rather than deleted; full-text availability is not confused with scientific eligibility; temporary or failed records remain traceable.

### 04 Screen

Required: `screening_table.csv`, `prisma_flow_counts.csv`, `exclusion_reason_dictionary.md`.

Screening minimum columns: `candidate_id,stage,decision,primary_reason,secondary_reason,reviewer_basis,full_text_available,decided_at,notes`.

Pass when title/abstract and full-text screening decisions have explicit reasons; unavailable full text is an access state; study type is labeled; duplicate reports from one study are linked; no inclusion/exclusion decision is based on desired findings, citation count, or journal prestige alone.

### 05 Extract

Required: `literature_matrix.csv`, `neural_mechanism_matrix.csv`, `quality_appraisal.csv`, and reading cards for central studies.

Pass when extracted claims contain source locations; sample, design, measures, task, analysis, main findings, limitations, quality judgments, and neuroscience indicators are recorded where available; primary studies and review/theory papers are separated; null and contradictory findings are retained.

### 06 Synthesize

Required: `prewriting_synthesis_plan.md`, `concept_theory_framework.md`, `claim_evidence_map.csv`, `evidence_gap_register.csv`.

Claim map minimum columns: `claim_id,claim_text,claim_type,source_role,study_ids,candidate_ids,evidence_locations,support_level,contradictions,verification_status,manuscript_destination,allowed_wording`.

Pass when synthesis is thematic/mechanistic rather than one-paper-per-paragraph; direct evidence is separated from interpretation; contradictions and limitations are explicit; every planned claim is supported or marked tentative/unsupported; gaps are methodological or theoretical rather than simply “few studies.”

### 07 Prewrite

Required: `review_methods_plan.md`, `section_argument_plan.md`, `stage_handoff.md`.

Pass when the review-methods paragraph, section-level argument path, planned figures/tables, paragraph ID policy, allowed/prohibited claims, and citation strategy are frozen before drafting. For non-systematic reviews, the method description must be transparent without overclaiming exhaustiveness.

### 08 Manuscript

Required: `review_outline.md`, `review_draft.md`, `review_draft.docx` when document tooling is available.

Pass when every empirical or definitional claim maps to `claim_id` or a source ID; each paragraph has a stable ID; section logic follows `section_argument_plan.md`; causal and mechanism language is calibrated; AI-like filler phrases are removed.

### 09 Audit

Required: `paragraph_source_alignment_matrix.csv`, `reference_consistency_check.csv`, `unsupported_or_overstated_claims.md`.

Pass when every claim-bearing paragraph is mapped to source passages or marked unsupported; reference list and in-text citations match; unsupported or overstated claims are revised, deleted, or explicitly listed as blockers.

## Shared identifiers

- `review_run_id`: immutable per run.
- `search_id`: one database query or citation-chasing operation.
- `candidate_id`: assigned at retrieval and retained through library, screening, extraction, citation, and audit.
- `study_id`: groups multiple reports from the same sample/study.
- `claim_id`: connects synthesis, manuscript, and paragraph-source audit.
- `paragraph_id`: stable manuscript paragraph ID, e.g., `P001`.
- `zotero_item_key` and `bibtex_key` are different; store both when used.

## Handoff rules

Every stage handoff states inputs consumed, outputs produced, decisions frozen, unresolved noncritical issues, and assumptions the next stage must not silently change. If an upstream change invalidates a downstream artifact, mark it stale in `manifest.json` and rerun its gate.
