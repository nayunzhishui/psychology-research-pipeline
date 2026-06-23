---
name: psych-methods-design
description: Use this skill to translate psychology research questions, evidence synthesis, measures, and dataset structure into a frozen methods plan, analysis plan, estimands, model sequence, missing-data plan, and robustness strategy. 适用于方法设计和统计分析计划冻结；不要用于执行数据分析或改写结果。 Use this skill before outcome analysis or when $psychology-research-pipeline delegates methods. Do not use this skill to choose methods after seeing results or to justify post hoc model shopping.
---

# Psychology Methods Design / 心理学方法设计

Design for the estimand and observed data, not for a preferred significant result.

## Inputs

Require the project brief, frozen protocol, reporting plan, mini-review, construct-variable map, instrument/scoring evidence, and metadata-only data audit. Read the main pipeline's `references/psychology-standards.md`.

## Workflow

1. Restate primary/secondary estimands and map each to population, variables, waves, and contrasts.
2. Define participant flow, inclusion/exclusion, scoring, reverse items, valid ranges, derived variables, reliability, and longitudinal measurement invariance.
3. Specify missingness and attrition analyses, missing-data assumptions, and handling.
4. Choose a primary model and justify identification, estimator, constraints, covariates, time spacing, residual structure, and uncertainty.
5. For panel data, explicitly separate between-person and within-person effects. Predefine whether CLPM, RI-CLPM, growth, ALT-SR, DSEM, ordinal/count, or two-part alternatives address the question.
6. Specify longitudinal mediation only with defensible temporal ordering and indirect-effect uncertainty. Avoid causal mediation language unless assumptions and design support it.
7. For sex/gender differences, define the measured construct, coding, comparability tests, multi-group constraints, and formal difference tests.
8. Plan diagnostics, model comparison, sensitivity/robustness analyses, multiplicity control, influential-case checks, and failure alternatives.
9. Assess feasibility with simulation-based power/sensitivity when closed-form power is inadequate.
10. Freeze tables, figures, code outputs, seeds, software, version capture, and deviation rules before outcome modeling.

## Output

Write `07_methods/methods_plan.md` as manuscript-ready methods specifications and `07_methods/analysis_plan.md` as an executable ordered plan. Include decision rationales, assumptions, fallback models, and interpretations permitted or prohibited.

Fail the gate for unresolved scoring, unidentified models, post hoc covariate fishing, unplanned subgroup analysis, an estimator incompatible with the outcome, or a method selected only because a seed paper used it.
