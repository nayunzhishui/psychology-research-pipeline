---
name: cog-neuro-paradigm-design
description: Local subskill under psych-cog-neuro-review for extracting, comparing, and evaluating cognitive neuroscience tasks and paradigms in review projects. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 实验范式评价分 skill

## 目标

从纳入文献中提取、比较和评价实验范式与任务设计，服务认知神经科学综述中的方法学评价和机制解释。

## 适用场景

- 综述涉及 Go/No-Go、Stop-signal、n-back、Stroop、Flanker、IAT/GNAT、恐惧条件化、情绪记忆、睡眠实验等范式。
- 需要比较任务刺激、流程、指标和机制解释是否一致。

## 输入

文献阅读矩阵、方法部分原文、实验任务描述、刺激材料、行为指标、神经/生理指标。

## 执行步骤

1. 提取范式名称、任务流程、刺激类型、条件设置、试次数、时序和行为指标。
2. 比较不同研究中范式变体和关键差异。
3. 评价范式与目标构念和神经/生理指标的匹配度。
4. 标记可能影响结果解释的设计差异。
5. 输出范式评价和综述写作建议。

## 输出文件

- `实验范式设计_paradigm_design.md`
- `实验范式评价_paradigm_evaluation.md`
- `范式比较表_paradigm_comparison.csv`
- `任务指标表_task_measure_table.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 范式是否与构念匹配？
- 时序、刺激、条件和行为指标是否清楚？
- 不同研究是否可比较？
- 范式差异是否影响机制解释？

## 失败与停止条件

- 文献未报告任务关键参数时，不得做强比较。
- 范式与构念不匹配时，必须降级机制解释。
- 用户要求凭空补全任务参数时停止。

## 安全边界

不伪造任务流程、刺激、试次数、时序、行为指标或实验条件。

## 完成条件

形成范式评价、比较表、任务指标表和写作建议。