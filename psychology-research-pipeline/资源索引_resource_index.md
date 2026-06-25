# 资源索引

本索引用于 `psychology-research-pipeline` 运行时选择内部资源。仅在本主 skill 文件夹内使用，不调用其他主 skill。

## 读取顺序

1. 先读主 `SKILL.md`，确认任务边界、运行模式和停止条件。
2. 再读 `subskills/README.md`，确认分 skill 顺序。
3. 按当前阶段读取对应 `subskills/<name>/SKILL.md`。
4. 需要生成文件时读取 `中文文件命名规范.md`。
5. 需要标准化输出时读取 `templates/`。
6. 需要质量控制时读取 `checklists/`。
7. 需要评分判断时读取 `rubrics/`。
8. 用户需要启动提示或示例时读取 `examples/`。

## 阶段资源对应

| 阶段 | 分 skill | 模板 | 检查表 | 评分表 |
|---|---|---|---|---|
| 项目定标 | `project-scope` | `项目定标模板_project_brief.md`、`研究问题与假设模板_research_questions_hypotheses.md` | `启动需求检查表_startup_questions.md` | `研究问题质量评分表_research_question_quality.md`、`理论贡献评分表_theoretical_contribution.md` |
| 证据检索 | `evidence-search` | `检索记录模板_search_log.csv` | `顶刊级总检查表_top_journal_gate.md` | `引用风险评分表_citation_risk.md` |
| 文献筛选 | `literature-screen` | `文献筛选表模板_literature_screening.csv`、`文献阅读矩阵模板_literature_matrix.csv` | `来源对齐检查表_source_alignment.md` | `引用风险评分表_citation_risk.md` |
| 方法设计 | `methods-design` | `方法设计方案模板_methods_plan.md`、`测量工具表模板_measurement_table.csv`、`统计分析计划模板_statistical_analysis_plan.md` | `APA_JARS报告检查表_apa_jars.md`、`STROBE观察性研究检查表_strobe.md`、`CONSORT_SPIRIT干预试验检查表_consort_spirit.md`、`量表与测量质量检查表_measurement_quality.md` | `方法质量评分表_method_quality.md`、`测量质量评分表_measurement_quality.md` |
| 数据分析 | `data-analysis` | `数据字典模板_data_dictionary.csv`、`分析偏离记录模板_analysis_deviation_log.csv` | `数据质量检查表_data_quality.md`、`统计分析检查表_statistical_analysis.md` | `统计证据强度评分表_statistical_evidence.md` |
| 来源对齐 | `source-alignment` | `来源对齐表模板_source_alignment_table.csv` | `来源对齐检查表_source_alignment.md` | `引用风险评分表_citation_risk.md` |
| 模拟审稿 | `submission-review` | `模拟审稿意见模板_simulated_reviews.md`、`修改矩阵模板_revision_matrix.csv` | `投稿前检查表_submission_readiness.md`、`严格停止条件清单_stop_conditions.md` | `写作质量评分表_manuscript_quality.md`、`顶刊预备度评分表_top_journal_readiness.md` |

## 文件命名

所有本地运行产物默认使用“中文主名_英文兼容名.扩展名”。若必须使用纯英文文件名，必须在 `日志/决策记录_decisions.md` 记录原因。