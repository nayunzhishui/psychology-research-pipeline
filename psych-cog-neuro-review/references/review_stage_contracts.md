# Review stage contracts / 综述阶段合同

## Purpose

This file adapts the psychology-research-pipeline stage logic to a literature-review workflow. It covers all steps before review drafting and audit, especially the steps equivalent to empirical-project work before data analysis and empirical manuscript writing. Stage 03 also mirrors the repository-level Zotero ingest workflow: legal metadata/PDF acquisition, Zotero collection verification, duplicate checking, and manifest-based reporting.

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

Artifacts are UTF-8. CSV files use one header row and RFC 4180 quoting. Use `unknown` rather than an invented value. Dates use ISO 8601. Never commit PDFs, Zotero databases, browser artifacts, credentials, cookies, or tokens.

## Run mode contract

The run must declare one mode in `state.json` and `00_scope/review_scope.md`.

| Mode | Gate strength | Minimum expectation |
|---|---|---|
| `lite` | exploratory | transparent assumptions, at least two academic sources when searching, no claim of exhaustiveness; Zotero import optional |
| `standard` | default | complete 00–09 workflow, reproducible search log, screening reasons, Zotero/library status where available, extraction with source locations, paragraph-source audit |
| `strict` | publication-grade traceability | formal protocol, database-specific search, stronger screening/appraisal, bounded Zotero/PDF acquisition manifest, PRISMA-style counts, formal quality tools where applicable |

A run may move from `lite` to `standard` or from `standard` to `strict`. Downgrades require a decision log entry and must be visible in the final handoff.

## Gate contracts

### 00 Scope

Required: `workspace_inventory.md`, `review_scope.md`, `concept_map.md`.

Pass when the run mode, review type, topic boundary, population/species boundary, developmental/clinical boundary, core constructs, neuroscience methods, seed papers, source availability, Zotero acquisition need, and excluded claims are explicit. For REM and emotional memory, REM sleep, NREM sleep, sleep deprivation, sleep quality, emotional memory, fear extinction, encoding, consolidation, retrieval, and reconsolidation must not be collapsed into one vague construct.

### 01 Protocol

Required: `reporting_plan.md`, `review_protocol.md`, `review_stage_gates.md`.

Pass when review type, reporting standard, databases, languages, year range, inclusion/exclusion criteria, full-text handling, Zotero/library policy, extraction fields, quality-appraisal plan, AI-use policy, deviation policy, target output style, and run-mode-specific gates are frozen. Do not claim systematic/scoping status unless the protocol supports it.

### 02 Search

Required: `search_strategy.md`, `database_search_log.csv`, `candidate_records.csv`.

`database_search_log.csv` minimum columns: `search_id,database,platform,query,filters,run_at,result_count,export_file,notes`.

`candidate_records.csv` minimum columns: `candidate_id,title,authors,year,doi,pmid,cnki_id,wanfang_id,vip_id,source,abstract,landing_url,database,search_id,dedup_status,record_status`.

Pass when bilingual concept blocks exist; database-specific queries are reproducible; exact counts, dates, and filters are logged; citation chasing and Zotero/library searches are separately logged; no convenience source is described as exhaustive. For `standard` and `strict`, English sources normally include PubMed, Web of Science, PsycINFO, Scopus, Google Scholar, Semantic Scholar, Crossref, Zotero; Chinese sources normally include CNKI, 万方, 维普. Unsearched sources require a reason.

### 03 Acquire

Required: `library_acquisition_manifest.csv`, `zotero_manifest.csv`, `zotero_collection_plan.md`, `acquisition_report.md`.

`zotero_manifest.csv` minimum columns: `candidate_id,zotero_item_key,title,year,doi,collection,attachment_key,attachment_status,validation_status,source_url,notes`.

`library_acquisition_manifest.csv` minimum columns: `candidate_id,study_id,zotero_item_key,bibtex_key,parent_item_key,attachment_key,title,authors,year,doi,pmid,cnki_id,wanfang_id,vip_id,source,collection,collection_key,attachment_status,full_text_status,validation_status,acquisition_status,dedup_group,source_url,local_path,temporary_file_state,notes`.

Allowed Zotero acquisition statuses: `complete`, `metadata-only`, `duplicate-skipped`, `access-blocked`, `failed-validation`, `manual_needed`, `user_provided`.

Allowed normalized attachment/full-text statuses: `readable_pdf`, `metadata_only`, `abstract_only`, `access_blocked`, `duplicate_skipped`, `failed_validation`, `manual_needed`, `user_provided`.

Pass when every retained candidate has metadata and access status; the exact Zotero collection key/name is verified when Zotero is used; duplicates are grouped rather than deleted; matching is attempted by DOI, PMID, then normalized title + first author + year; readable PDF claims are validated; full-text availability is not confused with scientific eligibility; temporary or failed records remain traceable. Fail the gate if any import relies on paywall bypass, CAPTCHA bypass, credential/cookie extraction, shadow-library access, or unattended high-frequency downloading.

### 04 Screen

Required: `screening_table.csv`, `prisma_flow_counts.csv`, `exclusion_reason_dictionary.md`.

Screening minimum columns: `candidate_id,stage,decision,primary_reason,secondary_reason,reviewer_basis,full_text_available,decided_at,notes`.

Pass when title/abstract and full-text screening decisions have explicit reasons; unavailable full text is an access state; study type is labeled; duplicate reports from one study are linked; no inclusion/exclusion decision is based on desired findings, citation count, or journal prestige alone.

### 05 Extract

Required: `literature_matrix.csv`, `neural_mechanism_matrix.csv`, `quality_appraisal.csv`, and reading cards for central studies.

Pass when extracted claims contain source locations; sample, design, measures, task, analysis, main findings, limitations, quality judgments, and neuroscience indicators are recorded where available; primary studies and review/theory papers are separated; null and contradictory findings are retained. Quality appraisal must record both custom judgment and whether formal tools were used or intentionally not used.

### 06 Synthesize

Required: `prewriting_synthesis_plan.md`, `concept_theory_framework.md`, `claim_evidence_map.csv`, `evidence_gap_register.csv`.

Claim map minimum columns: `claim_id,claim_text,claim_type,source_role,study_ids,candidate_ids,evidence_locations,support_level,contradictions,verification_status,manuscript_destination,allowed_wording`.

Pass when synthesis is thematic/mechanistic rather than one-paper-per-paragraph; direct evidence is separated from interpretation; contradictions and limitations are explicit; every planned claim is supported or marked tentative/unsupported; gaps are methodological or theoretical rather than simply “few studies.”

### 07 Prewrite

Required: `review_methods_plan.md`, `section_argument_plan.md`, `stage_handoff.md`.

Pass when the review-methods paragraph, section-level argument path, planned figures/tables, paragraph ID policy, allowed/prohibited claims, manuscript format, and citation strategy are frozen before drafting. For non-systematic reviews, the method description must be transparent without overclaiming exhaustiveness.

### 08 Manuscript

Required: `review_outline.md`, `review_draft.md`, `review_draft.docx` when document tooling is available. `manuscript_format_check.md` is required when the run asks for Word output.

Pass when every empirical, theoretical, methodological, or definitional judgment maps to `claim_id` or a source ID; each paragraph has a stable ID; section logic follows `section_argument_plan.md`; manuscript format follows Chinese-core or Q1-review plan; causal and mechanism language is calibrated; AI-like filler phrases are removed.

### 09 Audit

Required: `paragraph_source_alignment_matrix.csv`, `reference_consistency_check.csv`, `unsupported_or_overstated_claims.md`.

Pass when every claim-bearing paragraph is mapped to source passages or marked unsupported; reference list and in-text citations match; unsupported or overstated claims are revised, deleted, or explicitly listed as blockers.

## Shared identifiers

- `review_run_id`: immutable per run.
- `search_id`: one database query or citation-chasing operation.
- `candidate_id`: assigned at retrieval and retained through library, Zotero, screening, extraction, citation, and audit.
- `study_id`: groups multiple reports from the same sample/study.
- `claim_id`: connects synthesis, manuscript, and paragraph-source audit.
- `paragraph_id`: stable manuscript paragraph ID, e.g., `P001`.
- `zotero_item_key`, `parent_item_key`, `attachment_key`, and `bibtex_key` are different; store them separately when used.

## Validation contract

When local execution is available, run:

```bash
python psych-cog-neuro-review/scripts/validate_run.py <path-to-cog_neuro_review_run>
```

Validation checks are supportive, not a replacement for scholarly judgment. A passing script does not prove the review is correct; it only confirms that required files, headers, and key IDs are structurally coherent.

## Handoff rules

Every stage handoff states inputs consumed, outputs produced, decisions frozen, unresolved noncritical issues, and assumptions the next stage must not silently change. If an upstream change invalidates a downstream artifact, mark it stale in `manifest.json` and rerun its gate.
