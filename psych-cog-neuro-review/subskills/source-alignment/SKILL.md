---
name: cog-neuro-source-alignment
description: Local subskill under psych-cog-neuro-review for aligning cognitive neuroscience mechanism claims with exact source evidence. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 机制来源对齐分 skill

## 目标

核查认知神经科学综述中的机制主张、脑区/网络/成分/指标表述、方法评价和参考文献原文是否一致。

## 适用场景

- 综述正文已经形成草稿。
- 需要检查每个机制主张是否有原文、页码、表图或结果部分支持。

## 输入

综述正文、参考文献、文献阅读矩阵、机制矩阵、方法评价、PDF 全文或网页原文。

## 执行步骤

1. 拆分正文中的机制主张、方法主张、结果主张和理论解释。
2. 为每条主张绑定文献来源和原文位置。
3. 判断支持程度：direct、partial、unsupported、overextended。
4. 核查脑区、网络、ERP 成分、睡眠阶段、眼动指标、NIRS 指标和心理生理指标是否准确。
5. 输出未支持主张、过度推断和修改建议。

## 输出文件

- `来源对齐表_source_alignment_table.csv`
- `机制主张审计_mechanism_claim_audit.md`
- `方法审计报告_method_audit.md`
- `未支持主张清单_unsupported_claims.md`
- `修改行动表_revision_actions.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 每个关键机制主张是否绑定来源？
- 原文位置是否可追溯？
- 是否存在过度推断？
- 指标名称和结果方向是否准确？

## 失败与停止条件

- 没有全文，不得做页码级强引用。
- 没有来源对齐，不得声称“可投稿”。
- unsupported 机制主张未处理前不得生成终稿。

## 安全边界

不得为了对齐而伪造页码、文献、原文内容、脑区结果、ERP 成分、fMRI 激活、PSG 分期、眼动/NIRS/心理生理指标或 DOI。

## 完成条件

完成来源对齐表、机制主张审计、方法审计、未支持主张清单和修改行动表。