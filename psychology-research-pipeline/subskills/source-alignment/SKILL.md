---
name: empirical-source-alignment
description: Local subskill under psychology-research-pipeline for claim-source-data alignment in empirical psychology manuscripts. Chinese-first; use only inside the empirical workflow.
---

# 来源对齐分 skill

## 目标

核查实证论文中的正文主张、参考文献、统计数字、图表、方法描述和数据输出是否一一对应。

## 适用场景

- 论文正文已经形成草稿，需要投稿前核查。
- 需要检查理论主张是否有文献支持、结果数字是否与统计输出一致。
- 需要生成来源对齐表、数字核查报告和未支持主张清单。

## 输入

- 论文正文、参考文献、文献阅读矩阵、主张证据对应表。
- 统计分析报告、原始输出、结果表格、图表和方法设计方案。

## 执行步骤

1. 拆分正文中的事实性、理论性、方法性、结果性和解释性主张。
2. 为每条主张绑定文献来源、页码/章节/表图，或绑定数据输出位置。
3. 判断支持程度：direct、partial、unsupported、overextended。
4. 核查 p 值、效应量、置信区间、样本量、模型拟合、表图数字。
5. 对 unsupported 和 overextended 主张给出删除、降级、补证据或重写建议。
6. 输出投稿前对齐审计结论。

## 输出文件

- `来源对齐表_source_alignment_table.csv`
- `来源对齐表_source_alignment_table.xlsx`
- `数字核查报告_numeric_audit.md`
- `主张核查报告_claim_audit.md`
- `未支持主张清单_unsupported_claims.md`
- `修改行动表_revision_actions.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 每个关键主张是否有来源或数据输出支撑？
- 文献页码/章节/表图是否可追溯？
- 统计数字是否与输出一致？
- 讨论是否超出研究设计允许的推论？
- APA 正文引用与参考文献是否一致？

## 失败与停止条件

- 没有全文，不得做页码级强引用。
- 没有统计输出，不得确认统计数字。
- 来源对齐未完成，不得声称“可投稿”。
- unsupported 主张未处理前不得生成终稿。

## 安全边界

不得为了对齐而伪造页码、文献、统计结果、图表、软件输出或 DOI。

## 完成条件

完成来源对齐表、数字核查报告、主张核查报告和修改行动表；所有关键 unsupported/overextended 主张均已给出处理建议。