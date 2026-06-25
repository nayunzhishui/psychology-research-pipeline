---
name: review-literature-matrix
description: Local subskill under psych-literature-review-workflow for full-text reading matrices and evidence extraction. Chinese-first; use only inside the literature review workflow.
---

# 阅读矩阵分 skill

## 目标

把阅读全文后的信息结构化为证据矩阵、质量评价表和主张证据对应表。

## 适用场景

- 已完成文献筛选，准备阅读全文。
- 需要为综述写作、证据综合、星图和来源对齐提供底层数据。

## 输入

文献筛选表、PDF 全文、纳入文献清单、综述协议和章节框架草案。

## 执行步骤

1. 对 4 级核心文献全文精读，记录页码/章节/表图位置。
2. 提取理论框架、样本、人群、测量工具、研究设计、统计方法、核心发现、局限和可引用位置。
3. 评价方法质量、证据强度、引用风险和适合写入章节。
4. 建立主张证据对应表。
5. 标记矛盾证据、空白和需要补充检索的问题。

## 输出文件

- `文献阅读矩阵_literature_matrix.csv`
- `文献阅读矩阵_literature_matrix.xlsx`
- `文献阅读矩阵_literature_matrix.md`
- `质量评价表_quality_appraisal.csv`
- `主张证据对应表_claim_evidence_map.csv`
- `矛盾与空白登记表_contradiction_gap_register.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 核心文献是否阅读全文？
- 可引用位置是否可追溯？
- 质量评价是否与相关性评级分开？
- 主张证据对应表是否能支撑正文写作？

## 失败与停止条件

- 没有全文，不得做强引用。
- 没有阅读矩阵，不得写正式综述正文。
- 核心章节缺少证据时，必须回到检索或筛选阶段。

## 安全边界

不伪造页码、结果、样本、工具、统计方法或证据强度。

## 完成条件

完成阅读矩阵、质量评价表、主张证据对应表和矛盾与空白登记表。