---
name: review-literature-screen
description: Local subskill under psych-literature-review-workflow for classification, eligibility screening, and 1-4 relevance rating.
---

# Review Literature Screen / 综述文献筛选分 skill

本分 skill 负责去重、分类、纳排和相关性评级。

## 文献分类

综述/元分析、理论文章、方法学文章、测量工具文章、横断实证、纵向实证、实验研究、干预研究、质性/混合方法、指南/共识。

## 相关性 1–4 级

| 等级 | 含义 | 处理 |
|---|---|---|
| 4 | 高度核心，直接支撑综述主线 | 全文精读，进入核心矩阵 |
| 3 | 直接相关，支撑某一章节 | 重点阅读摘要、方法、结果、讨论 |
| 2 | 背景相关或概念相关 | 选择性阅读 |
| 1 | 边缘相关 | 记录排除或仅背景使用 |

## 输出

- `classification.csv`
- `screening_decision_log.csv`
- `exclusion_reason_register.csv`
- `relevance_ratings.csv`