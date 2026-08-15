---
name: review-source-alignment
description: Local subskill under psych-literature-review-workflow for sentence/paragraph-to-source alignment in review writing. Chinese-first; use only inside the literature review workflow.
---

# 来源对齐分 skill

## 目标

核查综述正文中的每个关键主张是否有原文来源支持，并识别未支持、部分支持和过度推断主张。

## 适用场景

- 综述正文已形成草稿。
- 需要检查正文—参考文献—原文位置是否一致。
- 需要生成引用风险报告和未支持主张清单。

## 输入

综述正文、参考文献、文献阅读矩阵、唯一主张证据对应表、PDF 全文或网页原文。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 拆分正文中的定义性、理论性、事实性、方法性、结论性主张。
2. 每条主张按一个 `claim_id × candidate_id/report_id` 配对绑定研究家族、页码/章节/段落/表图和证据载体。
3. 使用公共合同的 `confirmed/partial/rejected/blocked`、`claim_ceiling`、`construct_match`、`estimand_level`、`result_direction` 和 Reviewer 状态。
4. 对 rejected、blocked、单独 partial、超表述上限或 Reviewer B 未通过的主张提出删除、降级、补证据、复核或重写建议。
5. 核查正文引用与参考文献一致性。

## 输出文件

- `来源对齐表_source_alignment_table.csv`
- `来源对齐表_source_alignment_table.xlsx`
- `未支持主张清单_unsupported_claims.md`
- `引用风险报告_citation_risk_report.md`
- `修改行动表_revision_actions.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 每个关键主张是否绑定来源？
- 原文位置是否可追溯？
- 是否存在过度推断？
- APA 正文引用与参考文献是否一致？

## 失败与停止条件

- 没有全文，不得做页码级强引用。
- 没有来源对齐，不得声称“可投稿”。
- rejected、blocked、超上限或 Reviewer B 未通过的关键主张未处理前不得生成终稿。

## 安全边界

不得为了对齐而伪造页码、文献、原文内容、DOI 或参考文献。

## 完成条件

完成来源对齐表、未支持主张清单、引用风险报告和修改行动表。
