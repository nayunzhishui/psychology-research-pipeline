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

文献筛选表、PDF 全文、纳入文献清单、综述协议和章节框架草案。开始前完整读取 `../../references/literature-operations-contract.md` 并对齐矩阵、账本和主张表字段。

## 执行步骤

1. 核心直接证据执行六遍精读；理论、测量和方法文献按用途精读；摘要只允许 blocked/待核验。
2. 提取稳定报告/研究/家族 ID、理论、样本、测量、设计、分析模型、估计对象、效应/零/相反/混合结果、局限和 PDF 页码/表图。
3. 分领域评价选择、测量、时间顺序、混杂、缺失、分析、选择性报告和适用性；相关性、权威性、新近性与方法质量分开。
4. 每个 `claim_id × candidate_id/report_id` 单独写入唯一主张表，记录证据载体、位置、构念匹配、估计层级、方向、表述上限和 Reviewer 状态。
5. Reviewer B 真正独立复核；冲突裁决后按研究而非报告综合矛盾、空白和补检索问题。

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
- 是否保留零/相反/混合结果，并按研究家族而非报告数综合？

## 失败与停止条件

- 没有全文，不得做强引用。
- 没有阅读矩阵，不得写正式综述正文。
- 核心章节缺少证据时，必须回到检索或筛选阶段。

## 安全边界

不伪造页码、结果、样本、工具、统计方法或证据强度。

## 完成条件

完成阅读矩阵、质量评价表、主张证据对应表和矛盾与空白登记表。
