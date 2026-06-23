# Stage contracts

## Contents

1. Run layout
2. Gate contracts
3. Shared identifiers
4. Handoff rules

## Run layout

Each run lives at `<project>/research-pipeline/<run-id>/`:

```text
state.json
manifest.json
logs/events.jsonl
01_scope/
02_protocol/
03_search/
04_library/
05_screening/
06_synthesis/
07_methods/
08_analysis/
09_manuscript/
10_review/
```

Artifacts are UTF-8. CSV files use one header row and RFC 4180 quoting. Dates are ISO 8601. Use `unknown` rather than an invented value.

## Gate contracts

### 01 Scope

Required: `project_brief.md`, `research_question.md`.

Pass when the primary RQ is answerable with observed waves and variables; constructs map to measures; population and time frame are clear; claims and exclusions are bounded; sensitive-data handling is stated; unresolved critical assumptions are absent.

### 02 Standards

Required: `reporting_plan.md`, `protocol.md`.

Pass when the study type, governing reporting checklists, ethics/open-science plan, hypotheses, primary/secondary outcomes, inclusion rules, search bounds, and protocol-deviation policy are frozen. Journal-specific instructions must be verified at execution time.

### 03 Search

Required: `search_log.csv`, `candidates.csv`.

`search_log.csv` minimum columns: `search_id,database,platform,query,filters,run_at,result_count,export_file,notes`.

`candidates.csv` minimum columns: `candidate_id,title,authors,year,doi,pmid,source,abstract,landing_url,database,search_id,dedup_status`.

Pass when each concept has controlled vocabulary and free-text terms; at least two appropriate sources are searched unless justified; exact queries and counts are logged; candidates are deduplicated; no automated source is misrepresented as exhaustive.

### 04 Acquire

Required: `zotero_manifest.csv`, `acquisition_report.md`.

Manifest minimum columns: `candidate_id,zotero_item_key,title,year,doi,collection,attachment_key,attachment_status,validation_status,source_url,notes`.

Allowed status: `complete`, `metadata-only`, `duplicate-skipped`, `access-blocked`, `failed-validation`.

Pass when every included candidate has a status; metadata matches the source; the named collection is verified; `complete` items have a readable PDF child; temporary files are retained when verification fails.

### 05 Screen

Required: `screening_log.csv`, `evidence_matrix.csv`.

Screening minimum columns: `candidate_id,stage,decision,reason,reviewer_basis,full_text_available,decided_at`.

Evidence minimum columns: `study_id,candidate_id,citation,design,country,sample,waves,intervals,constructs,measures,analysis,main_findings,effect_data,limitations,quality,doi,zotero_item_key,evidence_location`.

Pass when title/abstract and full-text decisions have explicit reasons; duplicate reports of one sample are linked; study quality is design-appropriate; evidence locations support extracted claims.

### 06 Synthesize

Required: `mini_review.md`, `claim_evidence_map.csv`.

Claim map minimum columns: `claim_id,claim_text,claim_type,study_ids,support_level,contradictions,verification_status,manuscript_destination`.

Pass when synthesis is thematic rather than paper-by-paper; direct evidence is separated from interpretation; contradictory and null results are retained; no claim lacks traceable evidence; gaps are not merely “few studies.”

### 07 Methods

Required: `methods_plan.md`, `analysis_plan.md`.

Pass when measures/scoring, participant flow, missingness, estimand, model specification, assumptions, estimator, covariates, sex/gender analysis, multiplicity, diagnostics, sensitivity analyses, model comparison, output tables, and deviation rules are specified before outcome analysis.

### 08 Analyze

Required: `data_audit.md`, `results.md`, `analysis_manifest.json`.

Manifest minimum keys: `data_files`, `file_hashes`, `software`, `packages`, `code_files`, `random_seed`, `analysis_plan`, `deviations`, `outputs`.

Pass when IDs/waves/scoring/missingness are audited; code runs from clean inputs; estimates, uncertainty, fit and diagnostics are reported; robustness checks are reconciled; deviations are labeled; no identifying rows are emitted.

### 09 Write

Required: `manuscript.md`, `references.bib`, `citation_audit.md`.

Pass when title through references are complete; every empirical claim maps to a verified citation or result; methods match code; results match outputs; causal language is calibrated; abstract contains no unsupported values; tables/figures are referenced; limitations and ethics are explicit.

### 10 Review

Required: `editorial_decision.md`, `reviewer_report.md`, `revision_matrix.csv`, `final_audit.md`.

Revision matrix minimum columns: `comment_id,severity,source,comment,response,action,artifact,location,status,evidence`.

Pass when journal fit is reasoned; independent editorial, methods/statistics, domain, and integrity reviews are represented; decision matches defects; every required revision is resolved or explicitly declined with rationale; final citation, reporting, ethics, and reproducibility audits pass.

## Shared identifiers

- `run_id`: immutable per run.
- `candidate_id`: assigned at retrieval and retained through Zotero and screening.
- `study_id`: groups multiple reports from the same sample/study.
- `claim_id`: connects synthesis, manuscript, and review.
- Zotero item keys and BibTeX keys are different; store both when used.

## Handoff rules

Every stage handoff states inputs consumed, outputs produced, decisions frozen, unresolved noncritical issues, and assumptions the next stage must not silently change. If an upstream change invalidates a downstream artifact, mark it stale in `manifest.json` and rerun its gate.
