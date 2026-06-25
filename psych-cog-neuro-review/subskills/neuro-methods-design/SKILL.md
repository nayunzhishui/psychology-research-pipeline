---
name: cog-neuro-methods-design
description: Local subskill under psych-cog-neuro-review for evaluating cognitive neuroscience methods and modality choices in review projects. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 神经生理方法评价分 skill

## 目标

提取和评价认知神经科学文献中的 EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理和行为任务方法，服务综述中的方法质量判断。

## 适用场景

- 综述需要比较不同神经/生理指标的证据质量。
- 需要判断某种指标是否能支持特定机制主张。

## 输入

文献方法部分、阅读矩阵、范式评价表、预处理与分析信息、设备和采样参数。

## 执行步骤

1. 提取研究使用的模态、设备、采样率、任务、指标和分析单元。
2. 记录关键参数：EEG 电极/ERP 时间窗、fMRI ROI/全脑、PSG 分期、眼动指标、NIRS 通道、心理生理指标。
3. 评价方法与机制问题的匹配度。
4. 标记报告不充分、预处理不透明和统计风险。
5. 输出方法评价和综述写作建议。

## 输出文件

- `神经生理方法方案_neuro_methods_plan.md`
- `神经生理方法评价_neuro_methods_evaluation.md`
- `方法参数提取表_method_parameters.csv`
- `指标适配度评价表_modality_fit_rating.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 方法参数是否足以评价证据质量？
- 指标是否能支持目标机制？
- 报告是否透明？
- 是否区分行为、主观、神经和生理证据层级？

## 失败与停止条件

- 文献缺失关键方法参数时，不得做强方法比较。
- 指标不能支持机制主张时，必须降级解释。
- 用户要求伪造脑区、成分、睡眠阶段、眼动或 NIRS 结果时停止。

## 安全边界

不伪造 EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理或行为任务方法信息。

## 完成条件

形成方法评价、参数提取表、指标适配度评价表和写作建议。