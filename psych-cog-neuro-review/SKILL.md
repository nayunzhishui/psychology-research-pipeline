---
name: psych-cog-neuro-review
description: Use this skill to run a reusable Chinese-first psychology and cognitive neuroscience literature review workflow, including bilingual search, screening, neural mechanism extraction, synthesis, manuscript drafting, Word/CSV/BibTeX/RIS outputs, and paragraph-to-source alignment audit. 适用于 REM 与情绪记忆等认知神经科学方向综述；不要用于未检索、未筛选、无来源支持的自由写作。
---

# Cognitive Neuroscience Psychology Review / 认知神经科学心理学综述

## Purpose

Use this skill to produce reusable, source-backed literature reviews in psychology and cognitive neuroscience. The default use case is a publishable review in Chinese core-journal style or an English Q1-review preparatory style. The workflow is general, but it is optimized for topics such as REM sleep, emotional memory, memory consolidation, affective neuroscience, cognitive control, threat/reward processing, EEG/ERP, fMRI, and behavioral-neural mechanism integration.

## Language policy

- 工作流说明、检索记录、阅读矩阵、证据综合、写作备注优先使用中文。
- 文献题名、量表名、实验范式、脑区、神经网络、统计指标、数据库字段保留英文原文。
- 首次出现的重要术语使用“中文解释 + 英文原词”，例如“快速眼动睡眠（rapid eye movement sleep, REM sleep）”。
- 正文可以写成中文核心综述风格，也可以输出英文 Q1 review preparatory draft；默认先产出中文综述草稿。

## Required inputs

- research topic and target review type
- population, age range, clinical/non-clinical boundary, species boundary if relevant
- target language: Chinese, English, or bilingual
- target style: 中文核心综述, 外文 Q1 review, thesis literature review, proposal review
- database access plan: PubMed, Web of Science, PsycINFO, Scopus, CNKI, Google Scholar, Semantic Scholar, Crossref, Zotero local library
- available source files: PDF, RIS, BibTeX, CSV, Word, Zotero export, notes

When inputs are incomplete, proceed with a documented assumption and mark it in `00_scope/review_scope.md`; do not silently narrow the review.

## Output structure

Create or update the following run directory. Keep machine-readable files in CSV/Markdown and export user-facing drafts to Word when possible.

```text
<project-root>/cog_neuro_review_run/
├── 00_scope/
│   └── review_scope.md
├── 01_search/
│   ├── search_strategy.md
│   ├── database_search_log.csv
│   └── candidate_records.bib_or_ris_note.md
├── 02_screen/
│   └── screening_table.csv
├── 03_extract/
│   ├── literature_matrix.csv
│   └── neural_mechanism_matrix.csv
├── 04_synthesis/
│   ├── concept_theory_framework.md
│   └── claim_evidence_map.csv
├── 05_write/
│   ├── review_outline.md
│   ├── review_draft.md
│   └── review_draft.docx
├── 06_audit/
│   ├── paragraph_source_alignment_matrix.csv
│   ├── reference_consistency_check.csv
│   └── unsupported_or_overstated_claims.md
└── logs/
    └── decisions.md
```

## Workflow

1. **Define scope.** Use `templates/project_intake.md`. Clarify review type, target journal level, population, intervention/exposure/task, outcomes, and neuroscience methods. For REM and emotional memory, separate REM sleep, NREM sleep, sleep deprivation, nap studies, fear conditioning, extinction, emotional reactivity, and memory consolidation.
2. **Build bilingual search strategy.** Use `templates/search_strategy.md`. Include English and Chinese search terms. Run or prepare queries for PubMed, Web of Science, PsycINFO, Scopus, CNKI, Google Scholar, Semantic Scholar, Crossref, and Zotero. Record exact database, query, filters, date, result count, and access status.
3. **Acquire and verify records.** Import or read BibTeX/RIS/PDF/Zotero exports. Verify DOI/PMID/title/year/journal. Do not fabricate metadata. If full text is unavailable, mark `full_text_status=abstract_only`.
4. **Screen studies.** Use `templates/screening_table.csv`. Record inclusion/exclusion decisions with explicit reasons. Keep reviews, meta-analyses, primary empirical studies, Chinese papers, and methodological papers distinguishable.
5. **Extract evidence.** Use `templates/literature_matrix.csv` for general study information and `templates/neural_mechanism_matrix.csv` for cognitive neuroscience details. Separate behavioral outcomes, subjective ratings, physiological indicators, EEG/ERP, fMRI, lesion/TMS, and computational measures.
6. **Synthesize before writing.** Build `04_synthesis/claim_evidence_map.csv` before drafting prose. Group evidence by construct, mechanism, method, sample, task, temporal process, and finding pattern. Do not organize the review as one paper per paragraph.
7. **Write the review.** Use `templates/review_outline.md` and `templates/writing_style_rules.md`. Produce `review_draft.md` first, then export `review_draft.docx` when tooling is available. Every empirical or definitional claim must be traceable to a source.
8. **Run the source-alignment subskill.** After the draft is complete, read and apply `subskills/source-alignment/SKILL.md`. Produce a paragraph-to-source matrix showing which review paragraph is supported by which source passage, page, section, table, result, or quoted source excerpt.
9. **Audit references.** Use `templates/reference_audit.csv`. Check that every in-text citation appears in the reference list and every reference-list item is cited or intentionally retained as background.
10. **Revise for publishable style.** Tighten the argument, remove unsupported claims, reduce generic AI-like transitions, and preserve uncertainty where evidence is mixed.

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
- Every database query and filter is logged.
- Screening exclusions have reasons.
- Each major claim appears in `claim_evidence_map.csv`.
- Each paragraph in `review_draft.md` has a stable ID such as `P001`.
- `paragraph_source_alignment_matrix.csv` links every claim paragraph to source passages or marks it as unsupported.
- `unsupported_or_overstated_claims.md` is empty or contains a revision plan.
- Reference metadata are checked against DOI/PMID/Crossref/PubMed/CNKI/Zotero where available.

## Completion

Return the run directory, completed artifacts, unresolved evidence gaps, unsupported claims removed or revised, and the next action. Do not claim the review is submission-ready while any source-alignment, reference, or scope gate remains open.
