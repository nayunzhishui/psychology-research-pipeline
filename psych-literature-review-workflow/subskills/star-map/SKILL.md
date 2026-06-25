---
name: review-star-map
description: Local subskill under psych-literature-review-workflow for building an HTML literature star map from review matrices. Chinese-first; use only inside the literature review workflow.
---

# 文献星图分 skill

## 目标

基于阅读矩阵和主张证据对应表制作 HTML 文献星图，帮助理解理论、方法、变量、证据和空白之间的关系。

## 适用场景

- 已有文献阅读矩阵和质量评价表。
- 需要可视化核心文献、理论、变量、方法、发现、争议和研究空白。

## 输入

`文献阅读矩阵_literature_matrix.csv/xlsx`、`质量评价表_quality_appraisal.csv`、`主张证据对应表_claim_evidence_map.csv`、`检索饱和记录_search_saturation_log.csv`。

## 执行步骤

1. 从矩阵中提取节点：文献、理论、构念、变量、测量、方法、人群、发现、争议和空白。
2. 生成边：共同构念、理论归属、方法相似、变量路径、证据支持、结果矛盾和空白连接。
3. 记录权重规则：主题相关度、证据质量、理论贡献、方法价值、连接度、新近性和权威性。
4. 输出 HTML 星图、节点表、边表和权重说明。

## 输出文件

- `文献星图_literature_star_map.html`
- `星图权重表_star_map_weights.csv`
- `星图节点表_star_map_nodes.csv`
- `星图边表_star_map_edges.csv`
- `星图说明_star_map_notes.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 星图关系是否来自矩阵？
- 权重规则是否写明？
- 是否避免把可视化权重误当作统计真值？
- 是否标注证据空白和矛盾关系？

## 失败与停止条件

- 没有阅读矩阵，不得生成星图。
- 关系无法追溯到文献矩阵时不得加入星图。
- 权重规则缺失时不得输出最终 HTML。

## 安全边界

不凭空添加未读文献、未证实关系或不存在的理论联系。

## 完成条件

输出 HTML 星图、节点表、边表、权重表和星图说明。