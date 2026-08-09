# Initialize a project-local R library and replace the seed lock with exact versions.
options(repos = c(CRAN = "https://cloud.r-project.org"))
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv")
renv::activate()

core <- c(
  "readr", "dplyr", "psych", "lavaan", "semTools", "simsem", "jsonlite",
  "targets", "mice", "powRICLPM", "effectsize", "performance", "parameters",
  "clubSandwich"
)
missing <- core[!vapply(core, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) renv::install(missing)
renv::snapshot(type = "all", prompt = FALSE)

status <- data.frame(
  package = core,
  installed = vapply(core, requireNamespace, logical(1), quietly = TRUE),
  version = vapply(core, function(x) {
    if (requireNamespace(x, quietly = TRUE)) as.character(utils::packageVersion(x)) else NA_character_
  }, character(1))
)
write.csv(status, "r-environment-status.csv", row.names = FALSE)
if (!all(status$installed)) stop("R environment remains incomplete")
