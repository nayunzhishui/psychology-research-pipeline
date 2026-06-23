---
name: psych-literature-screen
description: Use this skill to screen psychology literature at title-abstract and full-text levels, record inclusion and exclusion decisions, link multiple reports from the same study, assess study quality, and build evidence matrices. 适用于文献筛查、纳入排除、阅读卡和证据矩阵；不要用于重新检索数据库或下载 PDF。 Use this skill after search/acquisition, for corpus organization and reading, or when $psychology-research-pipeline delegates screening. Do not use this skill to replace unavailable full text with abstract-only claims unless that limitation is explicitly recorded.
---

# Psychology Literature Screening and Reading / 心理学文献筛查与阅读

Apply the frozen inclusion/exclusion criteria consistently. Do not use citation count or journal prestige as a proxy for methodological quality.

## Workflow

1. Calibrate criteria on a small mixed sample. Clarify ambiguous rules before bulk screening and log any protocol amendment.
2. Screen title/abstract without using desired findings as a criterion. Record one primary exclusion reason from a controlled list.
3. Retrieve and screen full text. `Unavailable` is an access state, not a scientific exclusion reason.
4. Link multiple papers from the same sample under one `study_id`; retain every report-level `candidate_id`.
5. Appraise quality with a design-appropriate framework. Evaluate selection, measurement, temporal ordering, confounding, missingness/attrition, analysis, selective reporting, and applicability. Preserve domain judgments instead of a context-free total score.
6. Read included papers in passes: citation/abstract; question/theory; methods/sample/measures; estimates/results; limitations; relevance.
7. Extract only claims that can be located in the full text. Store page, section, table, figure, or quote fragment under `evidence_location`; keep verbatim excerpts short.
8. Write `05_screening/screening_log.csv`, `05_screening/evidence_matrix.csv`, and optional reading cards keyed by `study_id`.

## Reading-card minimum

Capture WHY (problem/rationale), HOW (design/sample/measures/analysis), WHAT (estimates and uncertainty), validity threats, relation to the target model, contradictions, reusable methods, and citation identifiers.

## Gates

Fail when decisions lack reasons, one study is counted multiple times, abstracts substitute for available full text, quality judgments lack evidence, null results disappear, or extracted claims have no source location. If only one screener is available, state that limitation; do not claim independent dual screening.
