---
name: psych-data-analysis
description: Audit and analyze longitudinal psychology data reproducibly under a frozen analysis plan, preserving raw files and producing scoring checks, participant flow, missingness, psychometrics, measurement invariance, panel models, mediation or group comparisons, diagnostics, robustness results, code, and a machine-readable analysis manifest. Use for SPSS/CSV/statistical data after methods freeze or when $psychology-research-pipeline delegates analysis.
---

# Psychology Data Analysis

Keep raw data immutable. Work from scripted copies or derived datasets and never expose participant-level sensitive rows in reports.

## Execution order

1. Hash and inventory source files. Capture software, packages, versions, locale, seeds, code paths, and the frozen plan.
2. Validate IDs, duplicates, wave linkage, impossible values, labels, types, missing codes, scoring, reverse items, ranges, and derived-variable provenance.
3. Produce participant flow, attrition/missingness tables, distributions, zero proportions, floor/ceiling effects, and descriptive statistics by wave and relevant group.
4. Evaluate reliability and construct comparability. Run longitudinal measurement invariance before latent mean/path comparison when applicable.
5. Fit the preregistered primary model. Save syntax/code, convergence information, fit, estimates, confidence intervals, and diagnostics.
6. Run only planned secondary, mediation, subgroup, sex/gender, and sensitivity analyses. Label any necessary deviation before interpreting its result.
7. Compare robustness results against the primary conclusion and explain material changes.
8. Re-run from clean inputs where feasible and reconcile every manuscript-bound value with generated output.

## Longitudinal safeguards

- Do not interpret CLPM paths as within-person effects.
- In RI-CLPM, report random-intercept relations separately from within-person autoregressive and cross-lagged paths.
- Test group differences directly; differing significance labels are insufficient.
- Inspect skew and zero inflation for NSSI. Use a documented robust/ordinal/count/two-part alternative when continuous-normal assumptions fail.
- Report failed convergence, inadmissible solutions, boundary estimates, low power, and model uncertainty.
- Do not choose the “best” model solely by significance or suppress null models.

## Deliverables

Write `08_analysis/data_audit.md`, `08_analysis/results.md`, `08_analysis/analysis_manifest.json`, executable code/syntax, and generated tables/figures. The results file separates preregistered, secondary, exploratory, and sensitivity findings. Never hand-edit numerical outputs without regenerating or logging the correction.
