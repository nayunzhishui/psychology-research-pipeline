# 资源索引

本索引用于 `psych-cog-neuro-review` 运行时选择内部资源。仅在本主 skill 文件夹内使用，不调用其他主 skill。

## 读取顺序

1. 先读主 `SKILL.md`，确认综述类型、机制边界、运行模式和停止条件。
2. 再读 `subskills/README.md`，确认分 skill 顺序。
3. 按当前阶段读取对应 `subskills/<name>/SKILL.md`。
4. 需要生成文件时读取 `中文文件命名规范.md`。
5. 需要标准化输出时读取 `templates/`。
6. 需要方法质量控制时读取 `checklists/`。
7. 需要评分判断时读取 `rubrics/`。
8. 用户需要启动提示或示例时读取 `examples/`。

## 阶段资源对应

| 阶段 | 分 skill | 模板 | 检查表 | 评分表 |
|---|---|---|---|---|
| 方向定标 | `cog-neuro-scope` | `方向定标模板_cog_neuro_scope.md` | `认知神经顶刊级总检查表_top_journal_gate.md` | `机制理论贡献评分表_mechanism_contribution.md` |
| 证据检索 | `evidence-search` | `机制矩阵模板_neural_mechanism_matrix.csv` | `严格停止条件清单_stop_conditions.md` | `机制引用风险评分表_mechanism_citation_risk.md` |
| Zotero 入库 | `zotero-ingest` | 无固定模板，按清单输出 | `严格停止条件清单_stop_conditions.md` | 无 |
| 文献筛选 | `literature-screen` | `机制矩阵模板_neural_mechanism_matrix.csv` | `认知神经顶刊级总检查表_top_journal_gate.md` | `神经生理方法质量评分表_neuro_methods_quality.md` |
| 范式评价 | `paradigm-design` | `实验范式评价模板_paradigm_evaluation.md` | `实验范式质量检查表_paradigm_quality.md` | `实验范式质量评分表_paradigm_quality.md` |
| 神经/生理方法评价 | `neuro-methods-design` | `神经生理方法方案模板_neuro_methods_plan.md` | `EEG_ERP报告检查表_eeg_erp_reporting.md`、`fMRI报告检查表_fmri_reporting.md`、`PSG睡眠研究检查表_psg_sleep_reporting.md`、`眼动研究检查表_eye_tracking_reporting.md`、`NIRS报告检查表_nirs_reporting.md`、`心理生理指标检查表_psychophysiology_reporting.md` | `神经生理方法质量评分表_neuro_methods_quality.md` |
| 预处理与分析评价 | `neuro-data-analysis` | `预处理计划模板_preprocessing_plan.md`、`统计分析计划模板_statistical_analysis_plan.md` | `预处理与分析检查表_preprocessing_analysis.md` | `预处理透明性评分表_preprocessing_transparency.md` |
| 机制整合 | `mechanism-synthesis` | `机制矩阵模板_neural_mechanism_matrix.csv` | `机制主张来源对齐检查表_mechanism_alignment.md` | `行为神经整合质量评分表_behavior_neural_integration.md` |
| 来源对齐 | `source-alignment` | `来源对齐表模板_source_alignment_table.csv` | `机制主张来源对齐检查表_mechanism_alignment.md` | `机制引用风险评分表_mechanism_citation_risk.md` |
| 模拟审稿 | `submission-review` | `模拟审稿意见模板_simulated_reviews.md`、`修改矩阵模板_revision_matrix.csv` | `认知神经顶刊级总检查表_top_journal_gate.md`、`严格停止条件清单_stop_conditions.md` | `顶刊预备度评分表_top_journal_readiness.md` |

## 文件命名

所有本地运行产物默认使用“中文主名_英文兼容名.扩展名”。若必须使用纯英文文件名，必须在 `日志/决策记录_decisions.md` 记录原因。

## 定位提醒

本 workflow 综述优先。实验范式、神经/生理方法、预处理与分析计划主要用于文献质量评价、方法学比较和机制证据审查；不默认作为新实证实验项目主入口。