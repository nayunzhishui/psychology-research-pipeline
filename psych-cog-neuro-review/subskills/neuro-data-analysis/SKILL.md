---
name: cog-neuro-data-analysis
description: Local subskill under psych-cog-neuro-review for extracting and evaluating cognitive neuroscience preprocessing and analysis transparency in review projects. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 预处理与分析评价分 skill

## 目标

从认知神经科学文献中提取预处理、分析和统计信息，评价其透明性、可重复性和机制解释风险。

## 适用场景

- 综述需要评价 EEG/ERP、fMRI、PSG、眼动、NIRS 或心理生理研究的方法透明性。
- 需要比较预处理管线、统计模型和结果解释边界。

## 输入

方法部分、补充材料、分析脚本或作者报告的预处理与统计信息、阅读矩阵。

## 执行步骤

1. 提取预处理步骤：滤波、伪迹、分段、基线、配准、平滑、分期、眼动事件、通道处理等。
2. 提取分析策略：ROI、时间窗、频段、网络、行为指标、混合模型、校正方法和效应量。
3. 判断探索性与验证性分析是否区分。
4. 评价报告透明性、可重复性和统计风险。
5. 输出预处理透明性评价和分析方法评价。

## 输出文件

- `预处理计划_preprocessing_plan.md`
- `预处理透明性评价_preprocessing_transparency.md`
- `分析方法评价_analysis_methods_evaluation.md`
- `分析参数提取表_analysis_parameters.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 预处理步骤是否可追溯？
- 分析参数是否足以复核？
- 多重比较或统计校正是否说明？
- 探索性分析是否标注？

## 失败与停止条件

- 文献未报告关键预处理信息时，不得评价为高透明度。
- 没有统计方法说明时，不得写强机制结论。
- 用户要求伪造分析参数或统计结果时停止。

## 安全边界

不伪造预处理步骤、时间窗、ROI、频段、睡眠分期、眼动事件、NIRS 通道或统计输出。

## 完成条件

形成预处理透明性评价、分析方法评价和分析参数提取表。