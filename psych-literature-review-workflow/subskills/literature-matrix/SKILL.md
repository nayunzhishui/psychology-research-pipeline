---
name: review-literature-matrix
description: Local subskill under psych-literature-review-workflow for full-text reading matrices and evidence extraction.
---

# Review Literature Matrix / 综述阅读矩阵分 skill

本分 skill 用于阅读全文后的结构化提取。

## 矩阵字段

题录、DOI/PMID、研究类型、理论框架、核心构念、样本、人群、研究设计、测量工具、统计方法、核心发现、局限、可引用位置、证据类型、适合写入章节、主题相关度、方法质量、证据强度、引用风险。

## 输出格式

必须同时支持 CSV、Excel 和 Markdown。

## 输出

- `literature_matrix.csv`
- `literature_matrix.xlsx`
- `literature_matrix.md`
- `quality_appraisal.csv`
- `claim_evidence_map.csv`

## 要求

不要把摘要表当作全文矩阵。4 级核心文献必须尽量读取全文，并记录页码、章节、段落或表图位置。