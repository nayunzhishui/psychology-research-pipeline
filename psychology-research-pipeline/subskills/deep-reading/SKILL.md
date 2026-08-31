---
name: empirical-deep-reading
description: Local subskill for professor-level three-pass, seven-section reading of level-3 and level-4 empirical psychology papers. Use only inside psychology-research-pipeline after screening and full-text verification.
---

# 实证论文深度阅读

## 职责

这是本工作流唯一的逐篇全文提取入口。开始前完整读取 `../../references/literature-operations-contract.md` 和 `../../references/deep-reading-contract.md`。筛选负责分级，本 skill 负责深读；跨研究综合、正文写作和来源复核分别留给后续阶段。

## 输入与门禁

- 已冻结的研究问题、构念边界、纳排口径和证据槽。
- 题录身份、研究家族状态及可核验全文。
- 现有阅读矩阵、证据账本和唯一主张表。
- 仅处理4级全文和实际承担理论、测量、方法、关键反例或正文主张的3级全文；无全文者标记 `blocked`。

## 执行

1. 先标记论文类型、本轮用途和适用报告规范，再按公共合同完成三轮阅读和摘要、引言、方法、数据、结果、讨论、结论七章节审计；核心结论由表图承担时同时读取`../../references/evidence-figure-contract.md`并完成关键图反向阅读。
2. 实证覆盖层必须核验构念操作化、样本与招募、波次/间隔、信效度与计分、缺失/失访、协变量/聚类、估计对象、模型诊断、稳健性以及与本项目结果的关系。
3. 将作者主张、结果事实和本项目推断分开记录；论文级事实写入阅读矩阵，身份/全文包/家族写入证据账本，准备写作的单一主张及写作卡写入主张表；不得只写MD。
4. 4级全文以及被正式论证使用的3级全文，使用 `../../templates/深度阅读报告模板_deep_reading_report.md` 生成派生阅读总结。
5. Reviewer B 独立复核；未达到 `agreed` 或 `adjudicated` 的关键主张不得无标记进入正文。

## 完成条件

- 三表身份一致且七章节状态可追溯。
- 关键数字、零/反向/混合结果和限制具有PDF位置。
- `professor_briefing_status=ready` 仅在公共合同全部条件满足后设置。
- 未达到gate时保留 `needs-section-audit`、`blocked` 或 `A-only/B-pending`，不得沿用旧“六遍完成”直接宣称通过。

## 输出

- 原位更新现有阅读矩阵、证据账本和主张表。
- 按需生成最少数量的 `candidate_id_首位作者年份_中文短题名_阅读总结.md`。
