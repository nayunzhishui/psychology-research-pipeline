---
name: review-literature-screen
description: Local subskill under psych-literature-review-workflow for classification, eligibility screening, and 1-4 relevance rating. Chinese-first; use only inside the literature review workflow.
---

# 文献筛选分 skill

## 目标

对候选文献进行分类、纳排、相关性评级和排除理由登记，为阅读矩阵和证据综合奠定基础。

## 适用场景

- 已有候选文献表、Zotero 题录或 PDF 清单。
- 需要按综述协议执行初筛、全文筛选和 1–4 级相关性评级。

## 输入

候选文献表、检索记录、纳排标准、Zotero 题录、PDF 全文清单。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 对历轮已见主表去重并核验题录；同一研究的不同报告保留并关联，不能当重复删除。
2. 按文献类型分类：综述/元分析、理论、方法学、测量、横断、纵向、实验、干预、质性/混合方法、指南/共识。
3. 按纳排标准记录纳入、排除或待定。
4. 按 1–4 级评估主题相关性，相关性不等于方法质量。
5. 在证据计数前预识别研究家族；未知使用 `family-uncertain-<candidate_id>`。
6. 登记排除理由和需复核文献；不得按结果方向、引用数、期刊声望或全文可得性偷换科学纳排判断。
7. Reviewer B 在看不到 A 结论时按冻结规则独立复核；冲突保留待裁决。

## 输出文件

- `文献筛选表_literature_screening.csv`
- `文献分类表_literature_classification.csv`
- `相关性评级表_relevance_ratings.csv`
- `排除理由登记表_exclusion_reason_register.csv`
- `筛选复核清单_screening_review_queue.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否有清晰纳排标准？
- 排除理由是否可追溯？
- 相关性评级是否独立于方法质量？
- 是否标记需要全文复核的文献？
- 是否完成研究家族预识别与真正独立 Reviewer B？

## 失败与停止条件

- 没有纳排标准，不得执行正式筛选。
- 没有筛选记录，不得声称文献覆盖充分。
- 排除理由不清时不得进入证据综合。

## 安全边界

不伪造筛选数量、排除理由、全文状态或文献分类。

## 完成条件

生成筛选表、分类表、相关性评级表、排除理由登记表和复核清单。
