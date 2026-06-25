---
name: review-source-alignment
description: Local subskill under psych-literature-review-workflow for sentence/paragraph-to-source alignment in review writing.
---

# Review Source Alignment / 综述来源对齐分 skill

本分 skill 负责正文—参考文献—原文证据的一一对应核查。

## 对齐表字段

综述页码、综述段落、综述原句、支撑文献、文献页码、文献章节/段落/表图、原文短摘录、证据类型、支持程度、是否过度推断、是否需要复核。

## 支持程度

- direct：原文直接支持。
- partial：部分支持，需要限定表述。
- unsupported：不支持，应删除或重写。
- overextended：过度外推，应降级或补充证据。

## 输出

- `source_alignment_table.csv`
- `source_alignment_table.xlsx`
- `claim_audit.md`
- `citation_risk_report.md`