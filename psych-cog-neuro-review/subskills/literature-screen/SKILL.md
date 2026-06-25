---
name: cog-neuro-literature-screen
description: Local subskill under psych-cog-neuro-review for screening cognitive neuroscience literature. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 文献筛选分 skill

## 目标

对认知神经科学候选文献进行分类、纳排、相关性评级和方法质量初评。

## 适用场景

- 已有候选文献表或 Zotero 题录。
- 需要区分理论、范式、方法、指标和机制证据。

## 输入

候选文献表、检索记录、纳排标准、PDF 全文清单、机制边界说明。

## 执行步骤

1. 去重并核验题录。
2. 按理论/综述/元分析/方法学/范式/EEG/ERP/fMRI/PSG/眼动/NIRS/心理生理/行为研究分类。
3. 按 1–4 级评估主题相关性。
4. 初评方法质量、指标适配度和机制证据强度。
5. 登记排除理由和需复核文献。

## 输出文件

- `文献筛选表_literature_screening.csv`
- `文献分类表_literature_classification.csv`
- `相关性评级表_relevance_ratings.csv`
- `方法质量初评表_method_quality_initial.csv`
- `排除理由登记表_exclusion_reason_register.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否区分主题相关性和方法质量？
- 是否标记神经/生理指标类型？
- 是否登记排除理由？
- 是否识别需全文复核文献？

## 失败与停止条件

- 没有纳排标准，不得正式筛选。
- 没有筛选记录，不得声称文献覆盖充分。
- 核心机制缺少 3–4 级文献支撑时，必须回到检索阶段。

## 安全边界

不伪造筛选数量、排除理由、全文状态、方法类型或机制证据。

## 完成条件

生成筛选表、分类表、相关性评级表、方法质量初评表和排除理由登记表。