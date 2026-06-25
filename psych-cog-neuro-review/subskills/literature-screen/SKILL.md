---
name: cog-neuro-literature-screen
description: Local subskill under psych-cog-neuro-review for screening cognitive neuroscience literature.
---

# Cog Neuro Literature Screen / 认知神经科学文献筛选分 skill

本分 skill 用于认知神经科学文献的分类、纳排和相关性评级。

## 分类

综述/元分析、理论机制、范式/任务、EEG/ERP、fMRI、PSG/睡眠、眼动、生理指标、行为实验、临床/发展证据、方法学文章。

## 1–4 级相关性

| 等级 | 含义 | 处理 |
|---|---|---|
| 4 | 核心机制、核心范式、核心指标或关键实证证据 | 全文精读 |
| 3 | 直接相关，支持某一机制或方法模块 | 重点阅读 |
| 2 | 背景相关或方法参考 | 选择性阅读 |
| 1 | 边缘相关 | 记录排除或背景用途 |

## 输出

- `classification.csv`
- `screening_table.csv`
- `relevance_ratings.csv`
- `exclusion_reason_register.csv`