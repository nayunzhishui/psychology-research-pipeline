---
name: cog-neuro-manuscript-write
description: Local subskill under psych-cog-neuro-review for writing cognitive neuroscience review manuscripts. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 综述正文写作分 skill

## 目标

基于文献阅读矩阵、机制矩阵、方法评价和来源对齐要求，写作 APA 第 7 版兼容的认知神经科学综述正文。

## 适用场景

- 已完成检索、筛选、阅读矩阵、机制整合和方法评价。
- 需要写作机制综述、理论综述、方法学综述、范式综述或指标综述。

## 输入

综述协议、文献阅读矩阵、机制矩阵、方法评价、预处理透明性评价、主张证据对应表、综述框架。

## 执行步骤

1. 制定章节结构和论证顺序。
2. 按矩阵写作，不先写后找文献硬配。
3. 分层呈现行为、主观、神经/生理和理论证据。
4. 处理矛盾证据、方法局限和未来方向。
5. 为后续来源对齐保留章节主张表。

## 输出文件

- `综述框架_review_outline.md`
- `章节主张表_section_claims.md`
- `图表计划_figure_table_plan.md`
- `综述正文_manuscript.md`
- `综述正文_manuscript.docx`
- `APA参考文献_apa_references.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 正文是否来自矩阵？
- 是否分层报告行为、主观、神经和生理证据？
- 是否避免从相关结果推断因果？
- 是否避免凭空写脑机制？
- 是否为机制来源对齐保留主张表？

## 失败与停止条件

- 没有阅读矩阵和机制矩阵，不得写正式机制综述正文。
- 没有主张证据对应表，不得生成投稿级正文。
- 关键机制缺少证据时，必须回到检索或矩阵阶段。

## 安全边界

不伪造文献、引用、页码、脑机制、实验范式、神经/生理指标或理论贡献。

## 完成条件

生成综述框架、章节主张表、图表计划、综述正文和 APA 参考文献。