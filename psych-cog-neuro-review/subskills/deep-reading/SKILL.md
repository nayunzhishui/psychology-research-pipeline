---
name: cog-neuro-deep-reading
description: Local subskill for professor-level three-pass, seven-section reading of level-3 and level-4 cognitive neuroscience papers. Use only inside psych-cog-neuro-review after screening and full-text verification.
---

# 认知神经科学深度阅读

## 职责

这是本工作流唯一逐篇全文提取入口。开始前完整读取 `../../references/literature-operations-contract.md` 与 `../../references/deep-reading-contract.md`。单篇事实在此提取；方法子skill做跨研究方法评价，机制综合做跨研究整合，来源对齐只复核。

## 输入与门禁

- 冻结的综述问题、机制边界、纳排标准和证据槽。
- 已核验题录、研究家族和可访问全文。
- 现有阅读矩阵、证据账本、机制矩阵和唯一主张表。
- 只处理4级全文和实际承担理论、范式、测量、方法、关键反例或正文主张的3级全文。

## 执行

1. 完成公共三轮阅读及摘要、引言、方法、数据、结果、讨论、结论七章节审计。
2. 认知神经覆盖层核验任务/对照/试次、模态与采集、预处理、伪迹/排除、ROI/全脑、时间窗/频带、多重比较、分析灵活性、交叉验证/泄漏、反向推断和跨模态尺度。
3. 记录行为、主观、神经和生理结果是否收敛，机制措辞不得超过设计与模态允许的 `claim_ceiling`。
4. 论文级事实写入矩阵，身份/全文/家族写入账本，机制主张与写作卡写入主张表；需要跨研究比较的内容交给后续子skill。
5. 按 `../../templates/reading_card.md` 为全部4级全文和被正式论证使用的3级全文生成派生阅读总结。
6. Reviewer B 独立复核；关键主张未达 `agreed/adjudicated` 时不得无标记进入正文。

## 完成条件

- 七章节与领域覆盖层均有状态和PDF位置。
- 零、相反和混合结果、方法不透明处及替代解释未被删去。
- 只有满足公共合同全部条件时才设置 `professor_briefing_status=ready`。
