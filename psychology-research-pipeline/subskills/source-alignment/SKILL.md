---
name: empirical-source-alignment
description: Local subskill under psychology-research-pipeline for claim-source-data alignment in empirical psychology manuscripts. Use only inside the empirical workflow.
---

# Empirical Source Alignment / 实证论文来源与数据对齐分 skill

本分 skill 只属于 `psychology-research-pipeline`，用于核查实证论文中的正文主张、参考文献、统计数字、表格、图和方法描述是否一致。

## 对齐对象

- 理论主张 ↔ 文献来源
- 方法描述 ↔ 研究方案、量表、任务和数据字典
- 统计结果 ↔ 软件输出、分析脚本和结果表
- 讨论解释 ↔ 研究设计允许的推论边界
- 参考文献 ↔ 正文引用

## 对齐表字段

正文页码、正文段落、正文原句、主张类型、支撑来源或数据输出、来源页码/表图/输出位置、支持程度、是否过度推断、是否需要复核、修改建议。

## 支持程度

- `direct`：来源或数据直接支持。
- `partial`：部分支持，需要限定表述。
- `unsupported`：不支持，应删除或重写。
- `overextended`：过度外推，应降级或补充证据。

## 输出

- `source_alignment_table.csv`
- `source_alignment_table.xlsx`
- `numeric_audit.md`
- `claim_audit.md`
- `unsupported_claims.md`
- `revision_actions.csv`

## 禁止

不得为了对齐而伪造页码、文献、统计结果、图表或软件输出。