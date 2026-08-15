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

文献阅读矩阵、机制矩阵、方法评价、预处理与分析评价、唯一主张证据对应表。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 按证据层级整理：行为、主观、神经、心理生理、理论模型。
2. 区分描述、个体间关联、时间预测、实验操纵、纵向个体内变化和因果效应；神经激活、相关、中介或时间先后本身不证明机制。
3. 提取支持、零、相反和混合证据，连同任务、对照、模态、预处理、ROI/全脑、校正、解析灵活性和边界条件。
4. 每个机制主张以一个 `claim_id × candidate_id/report_id` 配对写入唯一主张表，记录证据位置、构念匹配、估计层级、结果方向、Reviewer 状态和 `claim_ceiling`。
5. 对脑区/网络/成分主张执行反向推断检查；跨模态整合注明空间、时间与测量层级不可直接互换。
6. Reviewer B 独立复核后，按研究家族而非报告数综合并更新机制模型。

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
- 是否控制反向推断、分析灵活性和同一研究多报告重复计数？

## 失败与停止条件

- 没有机制矩阵，不得写机制综述正文。
- 没有来源支持，不得写强机制主张。
- 方法质量不足时，必须降级机制解释。

## 安全边界

不伪造脑区、网络、ERP 成分、fMRI 激活、PSG 分期、眼动指标、NIRS 指标、心理生理指标或机制链。

## 完成条件

生成机制矩阵、机制模型说明、主张证据对应表、矛盾与空白登记表和机制证据强度表。
