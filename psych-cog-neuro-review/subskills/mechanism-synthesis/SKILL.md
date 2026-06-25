---
name: cog-neuro-mechanism-synthesis
description: Local subskill under psych-cog-neuro-review for cognitive neuroscience mechanism synthesis and evidence grading. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 机制整合分 skill

## 目标

整合行为、主观量表、神经/生理指标和理论模型，形成可追溯的认知神经机制解释。

## 适用场景

- 综述需要解释脑区、网络、ERP 成分、睡眠阶段、眼动、NIRS 或心理生理指标与心理构念之间的关系。
- 需要比较不同研究的机制证据强度和矛盾发现。

## 输入

文献阅读矩阵、机制矩阵、方法评价、预处理与分析评价、主张证据对应表。

## 执行步骤

1. 按证据层级整理：行为、主观、神经、心理生理、理论模型。
2. 区分相关、预测、实验操纵、纵向变化和因果推断。
3. 提取支持证据、矛盾证据、边界条件和方法限制。
4. 建立机制模型和主张证据对应表。
5. 标注机制主张的证据强度和引用风险。

## 输出文件

- `机制矩阵_neural_mechanism_matrix.csv`
- `机制模型说明_mechanism_model.md`
- `主张证据对应表_claim_evidence_map.csv`
- `矛盾与空白登记表_contradiction_gap_register.csv`
- `机制证据强度表_mechanism_evidence_rating.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否分层整合行为、主观、神经和生理证据？
- 机制主张是否有来源支持？
- 是否处理矛盾证据？
- 是否避免从相关结果推断因果？

## 失败与停止条件

- 没有机制矩阵，不得写机制综述正文。
- 没有来源支持，不得写强机制主张。
- 方法质量不足时，必须降级机制解释。

## 安全边界

不伪造脑区、网络、ERP 成分、fMRI 激活、PSG 分期、眼动指标、NIRS 指标、心理生理指标或机制链。

## 完成条件

生成机制矩阵、机制模型说明、主张证据对应表、矛盾与空白登记表和机制证据强度表。