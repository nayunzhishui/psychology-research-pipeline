#!/usr/bin/env python3
"""Generate auditable R analysis files for longitudinal panel models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def data_columns(path: Path) -> list[str]:
    if path.suffix.lower() == ".csv":
        import pandas as pd
        return list(pd.read_csv(path, nrows=0).columns)
    if path.suffix.lower() == ".sav":
        try:
            import pyreadstat
        except ImportError as exc:
            raise SystemExit("pyreadstat is required to inspect .sav columns") from exc
        _, metadata = pyreadstat.read_sav(str(path), metadataonly=True)
        return list(metadata.column_names)
    raise SystemExit(f"Unsupported analysis data type: {path.suffix}")


def validate_spec(spec: dict, columns: list[str]) -> list[str]:
    errors = []
    waves = spec.get("waves", [])
    constructs = spec.get("constructs", {})
    if len(waves) < 3:
        errors.append("RI-CLPM requires at least three waves")
    if len(constructs) < 2:
        errors.append("longitudinal structural analysis requires at least two constructs")
    required = []
    for name, config in constructs.items():
        variables = config.get("variables", {})
        missing_waves = [wave for wave in waves if wave not in variables]
        if missing_waves:
            errors.append(f"{name} missing wave variables: {missing_waves}")
        required.extend(variables.values())
        if spec.get("measurement_mode", "score-comparability") == "item-level":
            indicators = config.get("indicators", {})
            for wave in waves:
                wave_indicators = indicators.get(wave, [])
                if len(wave_indicators) < 2:
                    errors.append(f"{name} requires at least two item indicators at {wave}")
                required.extend(wave_indicators)
    for optional in [spec.get("group_variable"), spec.get("cluster_variable")]:
        if optional:
            required.append(optional)
    missing_columns = sorted(set(required) - set(columns))
    if missing_columns:
        errors.append(f"analysis variables missing from data: {missing_columns}")
    if len(required) != len(set(required)):
        errors.append("analysis variables must map uniquely unless an explicit time-invariant variable is used")
    return errors


def invariance_syntax(spec: dict) -> tuple[str, str, str]:
    configural: list[str] = []
    metric: list[str] = []
    scalar: list[str] = []
    for construct, config in spec["constructs"].items():
        for wave in spec["waves"]:
            items = config["indicators"][wave]
            factor = f"{construct}_{wave}"
            configural.append(f"{factor} =~ " + " + ".join(items))
            labelled = [f"l_{construct}_{index + 1}*{item}" for index, item in enumerate(items)]
            metric.append(f"{factor} =~ " + " + ".join(labelled))
            scalar.append(f"{factor} =~ " + " + ".join(labelled))
            scalar.extend(f"{item} ~ i_{construct}_{index + 1}*1" for index, item in enumerate(items))
        waves = spec["waves"]
        indicator_count = len(config["indicators"][waves[0]])
        for item_index in range(indicator_count):
            for wave_index in range(1, len(waves)):
                previous = config["indicators"][waves[wave_index - 1]][item_index]
                current = config["indicators"][waves[wave_index]][item_index]
                residual = f"{previous} ~~ {current}"
                configural.append(residual)
                metric.append(residual)
                scalar.append(residual)
    return "\n".join(configural), "\n".join(metric), "\n".join(scalar)


def r_path(path: Path) -> str:
    return str(path).replace("\\", "/").replace('"', '\\"')


def model_syntax(spec: dict) -> str:
    waves = spec["waves"]
    constructs = spec["constructs"]
    lines = ["# Random intercepts"]
    for name, config in constructs.items():
        variables = [config["variables"][wave] for wave in waves]
        lines.append(f"RI_{name} =~ " + " + ".join(f"1*{variable}" for variable in variables))
    lines.append("\n# Within-person latent components and zero residual variances")
    for name, config in constructs.items():
        for wave in waves:
            variable = config["variables"][wave]
            lines.append(f"w_{name}_{wave} =~ 1*{variable}")
            lines.append(f"{variable} ~~ 0*{variable}")
    lines.append("\n# Stationary autoregressive and cross-lagged paths")
    for index in range(1, len(waves)):
        current, previous = waves[index], waves[index - 1]
        for target in constructs:
            predictors = [f"ar_{target}*w_{target}_{previous}"]
            predictors.extend(
                f"cl_{target}_from_{source}*w_{source}_{previous}"
                for source in constructs if source != target
            )
            lines.append(f"w_{target}_{current} ~ " + " + ".join(predictors))
    lines.append("\n# Within-wave covariances")
    names = list(constructs)
    for wave in waves:
        for left_index, left in enumerate(names):
            for right in names[left_index + 1:]:
                lines.append(f"w_{left}_{wave} ~~ w_{right}_{wave}")
    lines.append("\n# Random-intercept covariances and orthogonality")
    for left_index, left in enumerate(names):
        for right in names[left_index + 1:]:
            lines.append(f"RI_{left} ~~ RI_{right}")
        for within_construct in names:
            for wave in waves:
                lines.append(f"RI_{left} ~~ 0*w_{within_construct}_{wave}")
    return "\n".join(lines)


def write(path: Path, text: str) -> str:
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return str(path.resolve())


def generate(data: Path, spec_path: Path, output_dir: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    columns = data_columns(data)
    errors = validate_spec(spec, columns)
    if errors:
        return {"status": "blocked", "errors": errors, "code_files": []}
    output_dir.mkdir(parents=True, exist_ok=True)
    code_dir = output_dir / "code"
    code_dir.mkdir(exist_ok=True)
    data_ref = r_path(data.resolve())
    model = model_syntax(spec)
    estimator = spec.get("estimator", "MLR")
    missing = spec.get("missing", "FIML").lower()
    cluster = spec.get("cluster_variable")
    group = spec.get("group_variable")
    construct_vars = [variable for config in spec["constructs"].values() for variable in config["variables"].values()]
    indicator_vars = [
        item for config in spec["constructs"].values()
        for items in config.get("indicators", {}).values() for item in items
    ]

    environment = f'''# Generated; do not edit results by hand.
required_packages <- c("readr", "dplyr", "psych", "lavaan", "semTools", "simsem", "jsonlite")
missing_packages <- required_packages[!vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing_packages)) stop("Install required R packages: ", paste(missing_packages, collapse = ", "))
dat <- readr::read_csv("{data_ref}", show_col_types = FALSE)
required_variables <- c({', '.join(json.dumps(name) for name in construct_vars + indicator_vars + [value for value in [group, cluster] if value])})
if (length(setdiff(required_variables, names(dat)))) stop("Missing variables: ", paste(setdiff(required_variables, names(dat)), collapse = ", "))
set.seed({int(spec.get('random_seed', 20260718))})
'''
    if spec.get("measurement_mode", "score-comparability") == "item-level":
        configural_model, metric_model, scalar_model = invariance_syntax(spec)
        measurement = f'''source("00_environment.R")
# Longitudinal measurement-invariance sequence; equality labels link item positions across waves.
configural_model <- '
{configural_model}
'
metric_model <- '
{metric_model}
'
scalar_model <- '
{scalar_model}
'
fit_configural <- lavaan::cfa(configural_model, data = dat, estimator = "{estimator}", missing = "{missing}", std.lv = TRUE)
fit_metric <- lavaan::cfa(metric_model, data = dat, estimator = "{estimator}", missing = "{missing}", std.lv = TRUE)
fit_scalar <- lavaan::cfa(scalar_model, data = dat, estimator = "{estimator}", missing = "{missing}", std.lv = TRUE)
fits <- list(configural = fit_configural, metric = fit_metric, scalar = fit_scalar)
if (any(!vapply(fits, lavInspect, logical(1), "converged"))) stop("A measurement-invariance model did not converge")
fit_table <- do.call(rbind, lapply(names(fits), function(name) cbind(model = name, as.data.frame(t(fitMeasures(fits[[name]], c("cfi", "rmsea", "srmr")))))))
fit_table$delta_cfi <- c(NA, diff(fit_table$cfi))
fit_table$delta_rmsea <- c(NA, diff(fit_table$rmsea))
write.csv(fit_table, "../measurement_invariance_fit.csv", row.names = FALSE)
capture.output(lavaan::lavTestLRT(fit_configural, fit_metric, fit_scalar), file = "../measurement_invariance_lrt.txt")
# Decide configural/metric/scalar or partial invariance from preregistered criteria; do not rely on chi-square alone.
'''
    else:
        measurement = f'''source("00_environment.R")
# Measurement gate. Use item-level invariance when indicator mappings are available;
# otherwise document score comparability before structural analysis.
measurement_mode <- {json.dumps(spec.get('measurement_mode', 'score-comparability'))}
score_summary <- psych::describe(dat[c({', '.join(json.dumps(name) for name in construct_vars)})])
write.csv(score_summary, "../measurement_score_summary.csv")
# A documented score-comparability decision is required before structural interpretation.
'''
    cluster_arg = f', cluster = "{cluster}"' if cluster else ""
    ri = f'''source("00_environment.R")
riclpm_model <- '
{model}
'
fit_riclpm <- lavaan::sem(riclpm_model, data = dat, estimator = "{estimator}", missing = "{missing}"{cluster_arg})
if (!lavInspect(fit_riclpm, "converged")) stop("RI-CLPM did not converge")
if (any(lavInspect(fit_riclpm, "post.check") == FALSE)) stop("RI-CLPM post-estimation check failed")
write.csv(parameterEstimates(fit_riclpm, standardized = TRUE, ci = TRUE), "../ri_clpm_parameters.csv", row.names = FALSE)
write.csv(as.data.frame(t(fitMeasures(fit_riclpm))), "../ri_clpm_fit.csv", row.names = FALSE)
saveRDS(fit_riclpm, "../ri_clpm_fit.rds")
'''
    if group:
        group_code = f'''source("02_ri_clpm.R")
fit_group_free <- lavaan::sem(riclpm_model, data = dat, group = "{group}", estimator = "{estimator}", missing = "{missing}"{cluster_arg})
fit_group_equal <- lavaan::sem(riclpm_model, data = dat, group = "{group}", group.equal = c("regressions"), estimator = "{estimator}", missing = "{missing}"{cluster_arg})
comparison <- lavaan::lavTestLRT(fit_group_equal, fit_group_free)
capture.output(comparison, file = "../sex_group_constraint_test.txt")
# Interpret the constrained-vs-free test; never compare separate group p-values.
'''
    else:
        group_code = '# No group variable configured. Record sex/gender comparison as not applicable.\n'
    zero_constructs = [name for name, config in spec["constructs"].items() if config.get("distribution") == "zero-heavy"]
    distribution_models = []
    for name in zero_constructs:
        config = spec["constructs"][name]
        for index in range(1, len(spec["waves"])):
            current, previous = spec["waves"][index], spec["waves"][index - 1]
            predictors = [f"{name}_any_{previous}"] + [
                other["variables"][previous] for other_name, other in spec["constructs"].items() if other_name != name
            ]
            binary_formula = f"{name}_any_{current} ~ " + " + ".join(predictors)
            positive_formula = f"{config['variables'][current]} ~ " + " + ".join(
                [config["variables"][previous], *predictors[1:]]
            )
            distribution_models.extend([
                f'binary_fits[["{name}_{current}"]] <- glm(stats::as.formula({json.dumps(binary_formula)}), data = dat, family = binomial())',
                f'positive_data <- dat[dat[["{config["variables"][current]}"]] > 0, , drop = FALSE]',
                f'if (nrow(positive_data) > 0) positive_fits[["{name}_{current}"]] <- glm(stats::as.formula({json.dumps(positive_formula)}), data = positive_data, family = Gamma(link = "log"))',
            ])
    distribution = f'''source("00_environment.R")
# zero-heavy constructs: {', '.join(zero_constructs) or 'none'}
# Generate occurrence and positive-part variables for preregistered two-part sensitivity analyses.
zero_heavy <- c({', '.join(json.dumps(name) for name in zero_constructs)})
''' + "\n".join(
        f'dat <- dat %>% mutate({name}_any_{wave} = as.integer({config["variables"][wave]} > 0), {name}_positive_{wave} = ifelse({config["variables"][wave]} > 0, {config["variables"][wave]}, NA_real_))'
        for name, config in spec["constructs"].items() if name in zero_constructs for wave in spec["waves"]
    ) + '''
binary_fits <- list()
positive_fits <- list()
''' + "\n".join(distribution_models) + '''
saveRDS(list(binary = binary_fits, positive = positive_fits), "../distribution_sensitivity_fits.rds")
# These are distributional sensitivity analyses, not replacements for the preregistered primary model.
'''
    power = f'''source("00_environment.R")
# Simulation-based power / parameter recovery scaffold.
target_n <- {int(spec.get('sample_size', 882))}
replications <- {int(spec.get('power_replications', 1000))}
if (replications < 500) warning("Use at least 500 replications for final sensitivity analysis")
riclpm_model <- '
{model}
'
simulation_plan <- list(n = target_n, replications = replications, model = riclpm_model)
saveRDS(simulation_plan, "../power_simulation_plan.rds")
# Supply theory-based population parameters before claiming achieved power.
'''
    descriptives = f'''source("00_environment.R")
descriptives <- psych::describe(dat[c({', '.join(json.dumps(name) for name in construct_vars)})])
write.csv(descriptives, "../descriptives.csv")
missingness <- data.frame(variable = names(dat), missing_n = colSums(is.na(dat)), missing_percent = colMeans(is.na(dat)) * 100)
write.csv(missingness, "../missingness.csv", row.names = FALSE)
'''
    export_output = f'''source("00_environment.R")
fit_riclpm <- readRDS("../ri_clpm_fit.rds")
parameter_table <- lavaan::parameterEstimates(fit_riclpm, standardized = TRUE, ci = TRUE)
regressions <- parameter_table[parameter_table$op == "~", , drop = FALSE]
parameters <- lapply(seq_len(nrow(regressions)), function(index) {{
  row <- regressions[index, ]
  list(
    result_id = paste0(row$lhs, "_on_", row$rhs), term = paste(row$rhs, "->", row$lhs),
    role = "primary", estimate = unname(row$est), se = unname(row$se),
    ci_low = unname(row$ci.lower), ci_high = unname(row$ci.upper),
    p_value = unname(row$pvalue), standardized = unname(row$std.all)
  )
}})
variances <- parameter_table[parameter_table$op == "~~" & parameter_table$lhs == parameter_table$rhs, , drop = FALSE]
inadmissible <- sum(!is.na(parameter_table$std.all) & abs(parameter_table$std.all) > 1)
fit_values <- lavaan::fitMeasures(fit_riclpm, c("cfi", "rmsea", "srmr"))
model_output <- list(
  schema_version = 1, analysis_id = "{spec.get('analysis_id', 'model-primary')}",
  sample_n = lavaan::lavInspect(fit_riclpm, "nobs"), primary_model = "RI-CLPM",
  estimator = "{estimator}", converged = isTRUE(lavaan::lavInspect(fit_riclpm, "converged")),
  post_check = isTRUE(lavaan::lavInspect(fit_riclpm, "post.check")),
  fit = as.list(fit_values), parameters = parameters, deviations = list(),
  diagnostics = list(
    negative_variances = sum(variances$est < 0, na.rm = TRUE),
    inadmissible_standardized = inadmissible, warnings = list()
  )
)
jsonlite::write_json(model_output, "../model_output.json", auto_unbox = TRUE, pretty = TRUE, null = "null")
'''
    code_files = [
        write(code_dir / "00_environment.R", environment),
        write(code_dir / "01_measurement_gate.R", measurement),
        write(code_dir / "02_ri_clpm.R", ri),
        write(code_dir / "03_sex_group_comparison.R", group_code),
        write(code_dir / "04_distribution_sensitivity.R", distribution),
        write(code_dir / "05_power_simulation.R", power),
        write(code_dir / "06_descriptives_missingness.R", descriptives),
        write(code_dir / "07_export_machine_output.R", export_output),
    ]
    expected_outputs = [
        output_dir / ("measurement_invariance_fit.csv" if spec.get("measurement_mode") == "item-level" else "measurement_score_summary.csv"),
        output_dir / "ri_clpm_parameters.csv", output_dir / "ri_clpm_fit.csv", output_dir / "ri_clpm_fit.rds",
        output_dir / "distribution_sensitivity_fits.rds", output_dir / "power_simulation_plan.rds",
        output_dir / "descriptives.csv", output_dir / "missingness.csv",
        output_dir / "model_output.json",
    ]
    if spec.get("measurement_mode") == "item-level":
        expected_outputs.append(output_dir / "measurement_invariance_lrt.txt")
    if group:
        expected_outputs.append(output_dir / "sex_group_constraint_test.txt")
    manifest = {
        "schema_version": 1, "status": "ready", "profile": spec.get("profile"),
        "data": str(data.resolve()), "data_sha256": sha256(data),
        "spec": str(spec_path.resolve()), "spec_sha256": sha256(spec_path),
        "code_files": code_files, "code_hashes": {path: sha256(Path(path)) for path in code_files},
        "estimator": estimator, "missing": spec.get("missing", "FIML"),
        "group_variable": group, "cluster_variable": cluster,
        "measurement_gate": spec.get("measurement_mode", "score-comparability"),
        "expected_outputs": [str(path.resolve()) for path in expected_outputs],
        "execution_status": "not-run", "blocked_reasons": [],
    }
    manifest_path = output_dir / "分析代码清单_analysis_code_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = generate(Path(args.data).resolve(), Path(args.spec).resolve(), Path(args.output_dir).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "ready" else 3


if __name__ == "__main__":
    raise SystemExit(main())
