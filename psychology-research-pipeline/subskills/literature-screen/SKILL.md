---
name: empirical-literature-screen
description: Local subskill under psychology-research-pipeline for screening and extracting literature that supports empirical psychology papers. Chinese-first; use only inside the empirical workflow.
---

# 文献筛选分 skill

## 目标

把候选文献筛选、分类、评级并提取为能支撑实证论文引言、方法和讨论的证据矩阵。

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
5. 按“分层阅读＋三轮六模块”执行：第一轮定位理论、问题、结论和参考文献网络；第二轮核验方法、数据、测量、分析、结果、表图和补充材料；第三轮反核偏倚、边界、家族、写作主张和证据位置。摘要只能形成 blocked/待核验记录。
6. 除样本、测量、设计、模型、估计对象、效应/零/反向结果、偏倚和位置外，矩阵还要结构化记录理论动机/假设、作者声称的创新、数据清理/排除、量表信效度/计分、缺失处理、协变量、模型诊断、稳健性/敏感性、关键参考文献追踪、与本项目结果的关系及段落级用途。
7. Reviewer B 在看不到 A 判断时独立复核；冲突保留并裁决。同一 Agent 再提示一次不算独立 Reviewer B。
8. 每条准备写入小综述或正文的主张，以一个 `claim_id × candidate_id/report_id` 配对写入唯一主张表；同时记录论文一句话结论、段落功能、谨慎转述、并列/对照来源、与本项目结果的关系和禁止措辞，正文不超过 `claim_ceiling`。
9. 按研究而非报告综合一致、零、相反、混合和不可判定结果，并据此更新证据缺口和下一轮检索建议。

## 输出文件

- `文献筛选表_literature_screening.csv`
- `文献分类表_literature_classification.csv`
- `相关性评级表_relevance_ratings.csv`
- `排除理由登记表_exclusion_reason_register.csv`
- `文献阅读矩阵_literature_matrix.csv`
- `文献阅读矩阵_literature_matrix.xlsx`
- `证据覆盖台账_evidence_ledger.csv`
- `小综述_mini_review.md`
- `主张证据对应表_claim_evidence_map.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否区分主题相关性和方法质量？
- 核心文献是否完成用途匹配的全文阅读并记录页码/章节/表图？
- 三轮适用状态是否均为 complete，且参考文献、表图和补充材料已按用途核验？
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

生成筛选表、分类表、相关性评级表、阅读矩阵、小综述和主张证据对应表，并列明证据空白。
