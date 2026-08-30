---
name: review-literature-matrix
description: Local subskill under psych-literature-review-workflow for full-text reading matrices and evidence extraction. Chinese-first; use only inside the literature review workflow.
---

# 阅读矩阵分 skill

## 目标

作为本工作流唯一逐篇深读入口，把3–4级全文按三轮七章节合同写入三表，并生成必要的教授汇报级阅读总结。

## 适用场景

- 已完成文献筛选，准备阅读全文。
- 需要为综述写作、证据综合、星图和来源对齐提供底层数据。

## 输入

文献筛选表、PDF 全文、纳入文献清单、综述协议和章节框架草案。开始前完整读取 `../../references/literature-operations-contract.md` 与 `../../references/deep-reading-contract.md`，并对齐矩阵、账本和主张表字段。

## 执行步骤

1. 只处理4级全文和实际承担理论、测量、方法、关键反例或正文主张的3级全文；摘要只允许 blocked/待核验。
2. 先标记论文类型、综述角色和适用报告规范，再按公共合同完成三轮阅读及摘要、引言、方法、数据、结果、讨论、结论七章节审计。
3. 综述覆盖层增加理论谱系、原始/二手来源、研究间异质性、共识/争议/空白、证据槽、边界条件和补检索触发。
4. 将作者主张、结果事实和本综述推断分开记录；论文级事实写入矩阵，身份/全文包/家族写入账本，单一主张、位置、上限和写作卡写入主张表；逐篇MD不得产生三表之外的新事实。
5. 4级全文及被正式论证使用的3级全文，按 `../../templates/深度阅读报告模板_deep_reading_report.md` 生成派生阅读总结。
6. Reviewer B 真正独立复核；本 skill 完成单篇判断后，跨研究比较交由综合阶段。

## 输出文件

- `文献阅读矩阵_literature_matrix.csv`
- `文献阅读矩阵_literature_matrix.xlsx`
- `文献阅读矩阵_literature_matrix.md`
- `证据覆盖台账_evidence_ledger.csv`
- `质量评价表_quality_appraisal.csv`
- `主张证据对应表_claim_evidence_map.csv`
- `矛盾与空白登记表_contradiction_gap_register.csv`
- 必要的 `candidate_id_首位作者年份_中文短题名_阅读总结.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 核心文献是否阅读全文？
- 三轮与七章节状态是否满足 `deep-reading-contract.md` 的教授汇报gate？
- 可引用位置是否可追溯？
- 质量评价是否与相关性评级分开？
- 主张证据对应表是否能支撑正文写作？
- 阅读矩阵、证据账本和主张表能否联合回到报告身份、PDF位置、写作表述与禁止边界？
- 是否保留零/相反/混合结果，并按研究家族而非报告数综合？

## 失败与停止条件

- 没有全文，不得做强引用。
- 没有阅读矩阵，不得写正式综述正文。
- 核心章节缺少证据时，必须回到检索或筛选阶段。

## 安全边界

不伪造页码、结果、样本、工具、统计方法或证据强度。

## 完成条件

完成三表和质量评价原位更新，并仅为符合生成条件的文献形成派生阅读总结；跨研究综合仍由后续阶段完成。
