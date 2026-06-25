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

综述正文、参考文献、文献阅读矩阵、主张证据对应表、PDF 全文或网页原文。

## 执行步骤

1. 拆分正文中的定义性、理论性、事实性、方法性、结论性主张。
2. 为每条主张绑定支撑文献、页码/章节/段落/表图。
3. 判断支持程度：direct、partial、unsupported、overextended。
4. 对 unsupported 和 overextended 主张提出删除、降级、补证据或重写建议。
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
- unsupported 主张未处理前不得生成终稿。

## 安全边界

不得为了对齐而伪造页码、文献、原文内容、DOI 或参考文献。

## 完成条件

完成来源对齐表、未支持主张清单、引用风险报告和修改行动表。