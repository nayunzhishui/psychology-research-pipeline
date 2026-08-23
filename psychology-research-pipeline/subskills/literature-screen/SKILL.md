---
name: empirical-literature-screen
description: Local subskill under psychology-research-pipeline for screening and extracting literature that supports empirical psychology papers. Chinese-first; use only inside the empirical workflow.
---

# 文献筛选分 skill

## 目标

把候选文献去重、分类、纳排和评级，并将3–4级全文路由到唯一深度阅读入口。

## 适用场景

- 已有候选文献表或 Zotero 题录，需要去重、分类、纳排和评级。
- 需要为实证论文形成小综述、阅读矩阵和主张证据对应表。

## 输入

- `候选文献表_candidate_records.csv`
- Zotero 导出的 BibTeX/RIS/CSV
- 已获取全文 PDF 或可访问网页
- 项目定标和研究假设
- 开始前完整读取 `../../references/literature-operations-contract.md`，并核对矩阵、证据账本和主张表字段。

## 执行步骤

1. 按历轮已见主表去重并核验题录；记录级去重不能删除同一研究的不同报告。
2. 按综述/元分析、理论、方法测量、横断、纵向、实验、干预、质性/混合方法、指南/共识分类。
3. 按公共合同的1–4级评估主题相关性和阅读深度；相关性不等于方法质量。
4. 在证据计数前按作者群、队列、机构、招募年份、样本、年龄、波次、量表和随访期预识别研究家族；不确定者用 `family-uncertain-<candidate_id>`。
5. 记录全文状态和阅读范围；摘要只能形成 blocked/待核验记录，不能确认效应或方法细节。
6. 将3–4级全文交给 `../deep-reading/`；筛选阶段不重复提取七章节、写作卡、质量综合或Reviewer B结论。

## 输出文件

- `文献筛选表_literature_screening.csv`
- `文献分类表_literature_classification.csv`
- `相关性评级表_relevance_ratings.csv`
- `排除理由登记表_exclusion_reason_register.csv`
- 现有候选表中的筛选、分类、相关性、全文状态和深读路由字段

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否区分主题相关性和方法质量？
- 3–4级全文是否已明确路由到深读入口？
- 排除文献是否记录理由？
- 是否先完成研究家族识别，且关键主张能从主张表回到矩阵和全文？
- Reviewer B 是否真正独立，冲突是否保留裁决轨迹？

## 失败与停止条件

- 没有筛选记录，不得进入正式写作。
- 没有全文，不得做强引用或页码级来源对齐。
- 核心假设没有 3–4 级文献支撑时，必须回到证据检索阶段。
- 文献矩阵字段缺失严重时，不得生成论文引言定稿。

## 安全边界

不伪造文献、页码、DOI、研究结果或量表信息；不把未读全文说成已精读。

## 完成条件

完成题录去重、纳排、分类、评级、全文状态和深读路由；不得把筛选完成表述为全文精读完成。
