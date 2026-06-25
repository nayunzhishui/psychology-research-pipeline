---
name: review-star-map
description: Local subskill under psych-literature-review-workflow for building an HTML literature star map from review matrices. Use only inside the literature-review workflow.
---

# Review Star Map / 文献星图分 skill

本分 skill 只属于 `psych-literature-review-workflow`，用于基于阅读矩阵和证据矩阵制作 HTML 参考文献星图。

## 输入

- `literature_matrix.csv` 或 `literature_matrix.xlsx`
- `quality_appraisal.csv`
- `claim_evidence_map.csv`
- `search_saturation_log.csv`

## 节点

节点可包括：文献、理论、核心构念、变量、测量工具、研究方法、人群、关键发现、争议点和研究空白。

## 边

边可表示：共同构念、引用关系、方法相似性、变量路径、理论归属、证据支持、结果矛盾和研究空白连接。

## 权重

默认使用激活扩散模型思路分配权重：

`综合权重 = 主题相关度 × 证据质量 × 理论贡献 × 方法价值 × 连接度 × 新近性 × 权威性`

权重不是统计真值，而是综述写作中的导航指标。所有权重规则必须写入 `star_map_notes.md`。

## 输出

- `literature_star_map.html`
- `star_map_weights.csv`
- `star_map_nodes.csv`
- `star_map_edges.csv`
- `star_map_notes.md`

## 质量要求

星图必须以阅读矩阵为依据，不得凭空添加未读文献或未证实的理论关系。