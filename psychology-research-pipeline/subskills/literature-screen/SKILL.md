---
name: empirical-literature-screen
description: Local subskill under psychology-research-pipeline for screening and extracting literature that supports empirical psychology papers. Use only inside the empirical workflow.
---

# Empirical Literature Screen / 实证论文文献筛选分 skill

本分 skill 只属于 `psychology-research-pipeline`，用于实证论文中的文献筛选、小综述和证据提取。它不是独立综述入口。

## 目标

把检索到的理论、综述、方法、量表和实证文章筛选成能服务研究问题、变量模型、方法设计和引言写作的证据材料。

## 分类

至少区分：综述/元分析、理论概念、方法测量、横断实证、纵向实证、实验研究、干预研究、质性/混合方法、指南/共识。

## 相关性 1–4 级

| 等级 | 含义 | 处理 |
|---|---|---|
| 4 | 核心文献，直接支撑研究问题、变量模型、方法或关键假设 | 全文精读，进入矩阵和引言核心引用 |
| 3 | 重要相关，支持某一章节或方法选择 | 摘要、方法、结果和讨论重点阅读 |
| 2 | 背景相关，提供概念边界或补充证据 | 选择性阅读 |
| 1 | 边缘相关，只能用于背景或排除理由 | 记录后通常不进入正文核心 |

## 输出

- `screening_table.csv`
- `classification.csv`
- `literature_matrix.csv`
- `literature_matrix.xlsx`
- `literature_matrix.md`
- `claim_evidence_map.csv`
- `mini_review.md`

## 质量要求

相关性评分与方法质量评分分开。不得把仅看摘要的文献当成全文精读文献；不得用边缘文献支撑核心假设。