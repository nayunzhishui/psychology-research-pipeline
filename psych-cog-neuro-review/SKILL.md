---
name: psych-cog-neuro-review
description: Use this skill to run an auditable Chinese-first psychology and cognitive neuroscience review pipeline, including scope definition, reporting standards, protocol freeze, bilingual search, record acquisition, Zotero/library verification, screening, quality appraisal, evidence extraction, pre-writing synthesis, manuscript drafting, Word/CSV/BibTeX/RIS outputs, and paragraph-to-source alignment audit. 适用于 REM 与情绪记忆等认知神经科学方向综述；不要用于未检索、未筛选、无来源支持的自由写作。
---

# Cognitive Neuroscience Psychology Review / 认知神经科学心理学综述

## Purpose

Use this skill to produce reusable, source-backed literature reviews in psychology and cognitive neuroscience. The default use case is a publishable Chinese-core-journal review or an English Q1-review preparatory draft. The workflow is general, but it is optimized for REM sleep, emotional memory, memory consolidation, affective neuroscience, cognitive control, threat/reward processing, EEG/ERP, fMRI, PSG, and behavioral-neural mechanism integration.

This skill mirrors the upstream psychology-research-pipeline logic before empirical data analysis and empirical manuscript writing: scope → standards/protocol → search → acquire/library → screen → extract/appraise → synthesize/prewrite → write → audit. It adapts those steps for a review article rather than an empirical dataset.

## Load only what is needed

- Read `references/review_stage_contracts.md` before starting or resuming a run.
- Read `templates/project_intake.md` for topic scoping.
- Read `templates/review_protocol.md` before any database search or screening.
- Read `templates/search_strategy.md` before database-specific query construction.
- Read `templates/writing_style_rules.md` before drafting prose.
- Read `subskills/source-alignment/SKILL.md` only after a complete draft exists.
- Do not load all templates into context unless the current stage requires them.

## Language policy

- 工作流说明、检索记录、阅读矩阵、证据综合、写作备注优先使用中文。
- 文献题名、量表名、实验范式、脑区、神经网络、统计指标、数据库字段保留英文原文。
- 首次出现的重要术语使用“中文解释 + English term”，例如“快速眼动睡眠（rapid eye movement sleep, REM sleep）”。
- 正文默认先产出中文综述草稿；如用户指定，可追加英文 Q1 review preparatory draft。

## Required inputs

- research topic and target review type: narrative review, theoretical review, scoping review, systematic review, mechanism review, measurement review, or mixed review
- population, age range, clinical/non-clinical boundary, human/animal/computational boundary
- target language: Chinese, English, or bilingual
- target style: 中文核心综述, 外文 Q1 review, thesis literature review, proposal review
- database access plan: PubMed, Web of Science, PsycINFO, Scopus, CNKI, Google Scholar, Semantic Scholar, Crossref, Zotero local library
- available source files: PDF, RIS, BibTeX, CSV, Word, Zotero export, notes
- whether meta-analysis or quantitative evidence summary is planned; default is no formal meta-analysis unless user explicitly asks

When inputs are incomplete, continue with documented assumptions and mark them in `00_scope/review_scope.md`; do not silently narrow the review.

## Run structure

Create or update one run directory. Keep machine-readable files in CSV/Markdown and export user-facing drafts to Word when possible.

```text
<project-root>/cog_neuro_review_run/
├── state.json
├── manifest.json
├── logs/
│   └── decisions.md
├── 00_scope/
│   ├── workspace_inventory.md
│   ├── review_scope.md
│   └── concept_map.md
├── 01_protocol/
│   ├── reporting_plan.md
│   ├── review_protocol.md
│   └── review_stage_gates.md
├── 02_search/
│   ├── search_strategy.md
│   ├── database_search_log.csv
│   ├── candidate_records.csv
│   └── candidate_records.bib_or_ris_note.md
├── 03_library/
│   ├── library_acquisition_manifest.csv
│   ├── zotero_collection_plan.md
│   └── acquisition_report.md
├── 04_screening/
│   ├── screening_table.csv
│   ├── prisma_flow_counts.csv
│   └── exclusion_reason_dictionary.md
├── 05_extraction/
│   ├── literature_matrix.csv
│   ├── neural_mechanism_matrix.csv
│   ├── quality_appraisal.csv
│   └── reading_cards/
├── 06_synthesis/
│   ├── prewriting_synthesis_plan.md
│   ├── concept_theory_framework.md
│   ├── claim_evidence_map.csv
│   └── evidence_gap_register.csv
├── 07_prewrite/
│   ├── review_methods_plan.md
│   ├── section_argument_plan.md
│   └── stage_handoff.md
├── 08_manuscript/
│   ├── review_outline.md
│   ├── review_draft.md
│   └── review_draft.docx
└── 09_audit/
    ├── paragraph_source_alignment_matrix.csv
    ├── reference_consistency_check.csv
    └── unsupported_or_overstated_claims.md
```

## Ordered stages

| Stage | Purpose | Required result |
|---|---|---|
| 00 Scope / 项目定标 | define review type, constructs, populations, mechanisms, boundaries, seed literature, and feasibility | `review_scope.md`, `concept_map.md` |
| 01 Protocol / 规范与协议 | choose PRISMA/PRISMA-S/PRISMA-ScR or narrative-review standard as applicable; freeze RQ, inclusion/exclusion, databases, search bounds, extraction plan, AI-use policy | `reporting_plan.md`, `review_protocol.md` |
| 02 Search / 检索 | build bilingual concept blocks and database-specific queries; record exact dates/counts/filters | `search_strategy.md`, `database_search_log.csv`, `candidate_records.csv` |
| 03 Acquire / 获取与文献库 | verify metadata, DOI/PMID/CNKI/Zotero keys, PDF availability, duplicates, attachments, and access states | `library_acquisition_manifest.csv`, `acquisition_report.md` |
| 04 Screen / 筛查 | title-abstract and full-text screening with explicit reasons; PRISMA-style flow counts when relevant | `screening_table.csv`, `prisma_flow_counts.csv` |
| 05 Extract / 提取与质量评价 | extract study, sample, method, result, neural mechanism, and source-location fields; appraise quality | `literature_matrix.csv`, `neural_mechanism_matrix.csv`, `quality_appraisal.csv` |
| 06 Synthesize / 证据综合 | produce thematic synthesis, contradictions, null findings, gaps, and claim-evidence mapping before prose | `prewriting_synthesis_plan.md`, `claim_evidence_map.csv`, `evidence_gap_register.csv` |
| 07 Prewrite / 脱稿前计划 | freeze section logic, review-methods paragraph, argument hierarchy, figures/tables, and allowed claims before drafting | `review_methods_plan.md`, `section_argument_plan.md`, `stage_handoff.md` |
| 08 Manuscript / 正文写作 | draft review in Chinese-first publishable style and export Word when possible | `review_draft.md`, `review_draft.docx` |
| 09 Audit / 源文献对应核查 | map each paragraph/claim to source passages and audit references | `paragraph_source_alignment_matrix.csv`, `reference_consistency_check.csv` |

Do not reorder stages. Loop within the current stage when a gate fails. Reopen an earlier stage only with a logged reason and a dependency-impact note.

## Stage execution contract

For every stage:

1. Read prior artifacts and state; do not reconstruct facts from memory.
2. Append a short event to `logs/decisions.md` with inputs, action, outputs, decisions, unresolved items, and next gate.
3. Save only into the current stage directory unless updating `state.json`, `manifest.json`, or the log.
4. Separate evidence, inference, recommendation, and unresolved items.
5. Run the stage gate from `references/review_stage_contracts.md` manually or with the user's validation scripts if available.
6. Fix failures in the same stage. Never mark a failed gate complete.
7. After a pass, write a concise handoff stating what the next stage must not silently change.

## Stage-specific instructions

### 00 Scope / 项目定标

Use `templates/project_intake.md`. Clarify review type, target journal level, topic boundaries, population, developmental stage, species boundary, exposure/task/process, outcomes, neuroscience methods, and expected contribution.

For REM and emotional memory, explicitly separate:

- REM sleep, NREM sleep, total sleep time, sleep deprivation, nap studies, and sleep quality
- emotional memory, fear conditioning, extinction, reconsolidation, affective reactivity, and general memory consolidation
- encoding, consolidation, retrieval, extinction, and regulation phases
- healthy adults, adolescents, older adults, clinical samples, trauma/anxiety/depression samples, animal studies, and computational models

### 01 Protocol / 规范与协议

Use `templates/review_protocol.md`. Select the governing standard based on review type:

- systematic review or meta-analysis: PRISMA 2020 plus PRISMA-S for search reporting
- scoping review: PRISMA-ScR plus PRISMA-S where search transparency matters
- narrative/theoretical/mechanism review: use a transparent protocol adapted from PRISMA concepts without falsely calling the review systematic
- Chinese core-style review: still freeze scope, search range, inclusion/exclusion, evidence-extraction fields, and citation-audit policy

Do not claim preregistration, PROSPERO registration, dual screening, or exhaustive search unless evidence exists.

### 02 Search / 检索

Use `templates/search_strategy.md` and `templates/database_search_log.csv`. Build bilingual concept blocks and database-specific syntax. Do not paste one query everywhere. Record exact database, platform, query, filters, run date, result count, export path, and notes.

Required sources unless access blocks them: PubMed, Web of Science, PsycINFO, Scopus, CNKI, Google Scholar, Semantic Scholar, Crossref, Zotero local library. When a source is not searched, log the reason.

### 03 Acquire / 获取与文献库

Use `templates/library_acquisition_manifest.csv` and `templates/zotero_tags.md`. Verify title, authors, year, journal/source, DOI, PMID, CNKI identifier, Zotero item key, attachment status, and duplicate group. Full text unavailable is an access state, not an exclusion reason.

Do not automate paywall bypass, CAPTCHA, institutional login, or unauthorized scraping. The user handles access decisions.

### 04 Screen / 筛查

Use `templates/screening_table.csv` and `templates/prisma_flow_counts.csv`. Apply frozen criteria consistently. Record one primary exclusion reason from a controlled list. Keep primary empirical studies, reviews/meta-analyses, theoretical papers, methods papers, and Chinese papers distinguishable.

### 05 Extract / 提取与质量评价

Use `templates/literature_matrix.csv`, `templates/neural_mechanism_matrix.csv`, `templates/quality_appraisal.csv`, and `templates/reading_card.md`. Extract only claims that can be located in the full text. Store page, section, table, figure, result paragraph, or short quote fragment under `evidence_location`.

### 06 Synthesize / 证据综合

Use `templates/prewriting_synthesis_plan.md`, `templates/claim_evidence_map.csv`, and `templates/evidence_gap_register.csv`. Group evidence by construct, mechanism, method, sample, task, temporal process, and finding pattern. Retain contradictions and null findings. Do not organize the review as one paper per paragraph.

### 07 Prewrite / 脱稿前计划

Use `templates/review_methods_plan.md`, `templates/review_outline.md`, and `templates/stage_handoff.md`. Before prose writing, freeze:

- section-level argument path
- which claims are allowed, tentative, prohibited, or background-only
- planned figures/tables, including mechanisms and evidence maps
- how review methods will be described
- how REM/sleep evidence will be separated from general memory and emotion-regulation evidence
- how source-alignment paragraph IDs will be assigned

### 08 Manuscript / 正文写作

Use `templates/review_outline.md` and `templates/writing_style_rules.md`. Produce `review_draft.md` first, then export `review_draft.docx` when tooling is available. Every empirical or definitional claim must be traceable to a `claim_id` and source record.

### 09 Audit / 源文献对应核查

Read and apply `subskills/source-alignment/SKILL.md`. Produce a paragraph-to-source matrix showing which review paragraph is supported by which source passage, page, section, table, result, or short quote fragment. Then use `templates/reference_audit.csv` to check citation consistency.

## Cognitive neuroscience extraction requirements

For each eligible study, extract fields when available:

- experimental paradigm/task: fear conditioning, extinction, emotional picture memory, word-pair memory, facial emotion task, Go/No-Go, n-back, IAT/GNAT, sleep lab protocol, nap protocol
- sample: age, sex/gender, clinical status, medication, sleep quality, trauma/depression/anxiety status, culture/language
- REM/sleep variables: REM duration, REM latency, REM density, awakenings, polysomnography, sleep deprivation, nap/night sleep, dream report
- cognitive process: encoding, consolidation, reconsolidation, extinction, retrieval, attentional bias, affective evaluation, regulation
- behavioral indicators: accuracy, reaction time, hit/false alarm, d′, bias, recall/recognition, valence/arousal ratings
- EEG/ERP indicators: P1, N1, N2, P3, LPP, ERN, FRN, N400, theta, alpha, beta, gamma, sleep spindles, slow oscillations, REM theta
- fMRI/brain indicators: amygdala, hippocampus, vmPFC, dlPFC, ACC, insula, striatum, DMN, salience network, frontoparietal network, functional connectivity
- statistical claims: effect size, confidence interval, correction method, model type, preregistration, robustness, null findings

## Writing and reasoning rules

- Separate evidence, inference, and recommendation.
- Do not infer causality from cross-sectional associations or correlational neuroimaging.
- Do not state that a brain region “proves” a mechanism; write in terms of convergent, indirect, or limited evidence.
- Distinguish adult, adolescent, child, older-adult, clinical, high-risk, and healthy samples.
- Distinguish human, animal, and computational evidence.
- Distinguish emotion memory enhancement, emotion regulation, fear extinction, and general memory consolidation.
- Do not cite a review as if it were the primary empirical study when the primary study is available.
- Do not turn null or mixed evidence into a positive conclusion.
- Do not translate all terms mechanically; keep established English terms where precision is better.
- Avoid generic openings such as “近年来，随着……不断发展” unless a specific historical claim is supported.
- Avoid empty endings such as “具有重要理论和实践意义” unless the paragraph states the exact theoretical or methodological implication.
- Prefer paragraph-level argument: claim → evidence pattern → limitation/contrast → implication.

## Quality gates

Before finishing, verify:

- `review_scope.md` contains explicit boundaries and assumptions.
- `review_protocol.md` freezes review type, RQ, search bounds, inclusion/exclusion, extraction fields, quality-appraisal plan, and deviation policy.
- Every database query and filter is logged.
- Every acquired record has metadata status, attachment status, and deduplication status.
- Screening exclusions have reasons.
- Every included study has at least one source-location field before being used for a claim.
- Each major claim appears in `claim_evidence_map.csv`.
- Section logic and allowed/prohibited claims are frozen before drafting.
- Each paragraph in `review_draft.md` has a stable ID such as `P001`.
- `paragraph_source_alignment_matrix.csv` links every claim paragraph to source passages or marks it as unsupported.
- `unsupported_or_overstated_claims.md` is empty or contains a revision plan.
- Reference metadata are checked against DOI/PMID/Crossref/PubMed/CNKI/Zotero where available.

## Completion

Return the run directory, completed stages, changed artifacts, unresolved evidence gaps, unsupported claims removed or revised, and the next action. Do not claim the review is submission-ready while any protocol, search, screening, extraction, synthesis, source-alignment, reference, or scope gate remains open.
