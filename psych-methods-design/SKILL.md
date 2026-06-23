---
name: psych-methods-design
description: Convert a psychology research question, evidence synthesis, instruments, and observed data structure into a defensible study method and frozen statistical analysis plan, including psychometrics, missingness, longitudinal modeling, mediation, sex/gender comparison, diagnostics, sensitivity analyses, power, and reproducibility. Use before outcome analysis or when $psychology-research-pipeline delegates methods.
---

# Psychology Methods Design

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
