# 资源索引

本索引用于 `psych-literature-review-workflow` 运行时选择内部资源。仅在本主 skill 文件夹内使用，不调用其他主 skill。

## 读取顺序

1. 先读主 `SKILL.md`，确认综述类型、运行模式和停止条件。
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
| 方向聚焦 | `review-scope` | `综述方向聚焦模板_review_scope.md` | `叙述综述透明化检查表_narrative_review_transparency.md` | `综述选题质量评分表_review_topic_quality.md` |
| 综述协议 | `review-scope` / `evidence-search` | `综述协议模板_review_protocol.md` | `PRISMA_2020检查表_prisma_2020.md`、`PRISMA_ScR检查表_prisma_scr.md` | `检索透明性评分表_search_transparency.md` |
| 检索 | `evidence-search` | `检索记录模板_search_log.csv` | `综述检索透明性检查表_search_transparency.md`、`检索饱和停止条件_search_saturation_stop.md` | `检索透明性评分表_search_transparency.md` |
| 筛选 | `literature-screen` | `文献筛选表模板_literature_screening.csv` | `文献筛选检查表_literature_screening.md` | `文献完整性评分表_literature_completeness.md` |
| 阅读矩阵 | `literature-matrix` | `文献阅读矩阵模板_literature_matrix.csv`、`主张证据对应表模板_claim_evidence_map.csv` | `阅读矩阵检查表_literature_matrix.md` | `证据综合质量评分表_synthesis_quality.md` |
| 文献星图 | `star-map` | `文献星图权重表模板_star_map_weights.csv` | `阅读矩阵检查表_literature_matrix.md` | `证据综合质量评分表_synthesis_quality.md` |
| 正文写作 | `manuscript-write` | `综述正文模板_review_manuscript.md` | `整合型综述质量检查表_integrative_review_quality.md` | `综述写作质量评分表_review_writing_quality.md`、`理论贡献评分表_theoretical_contribution.md` |
| 来源对齐 | `source-alignment` | `来源对齐表模板_source_alignment_table.csv` | `来源对齐检查表_source_alignment.md` | `引用风险评分表_citation_risk.md` |
| 模拟审稿 | `submission-review` | `模拟审稿意见模板_simulated_reviews.md`、`修改矩阵模板_revision_matrix.csv` | `投稿前检查表_submission_readiness.md`、`严格停止条件清单_stop_conditions.md` | `顶刊预备度评分表_top_journal_readiness.md` |

## 文件命名

所有本地运行产物默认使用“中文主名_英文兼容名.扩展名”。若必须使用纯英文文件名，必须在 `日志/决策记录_decisions.md` 记录原因。