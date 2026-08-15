library(targets)

tar_option_set(packages = c("readr", "lavaan", "semTools", "jsonlite"))

list(
  tar_target(frozen_manifest, jsonlite::read_json("06_数据管理/冻结清单_freeze_manifest.json")),
  tar_target(frozen_data, readr::read_csv(frozen_manifest$frozen_data, show_col_types = FALSE)),
  tar_target(analysis_manifest, jsonlite::read_json("07_统计分析/分析代码清单_analysis_code_manifest.json")),
  tar_target(
    verified_results,
    {
      if (!identical(analysis_manifest$execution_status, "verified")) {
        stop("Analysis outputs are not independently verified")
      }
      jsonlite::read_json("08_结果与图表/模型结果_已验证_results.json")
    }
  )
)
