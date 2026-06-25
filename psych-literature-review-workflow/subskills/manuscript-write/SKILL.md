---
name: review-manuscript-write
description: Local subskill under psych-literature-review-workflow for APA-style psychology review manuscript writing. Chinese-first; use only inside the literature review workflow.
---

# 综述正文写作分 skill

## 目标

基于阅读矩阵、证据综合和来源对齐要求，写作 APA 第 7 版兼容的心理学综述正文。

## 适用场景

- 已完成综述协议、检索、筛选、阅读矩阵和证据综合。
- 需要形成中文为主、引用可追溯的综述正文。

## 输入

综述协议、文献阅读矩阵、主张证据对应表、证据综合备忘录、综述框架、APA 参考文献。

## 执行步骤

1. 制定章节结构、论证顺序和图表计划。
2. 按证据矩阵写作，不先写后找文献硬配。
3. 每个关键主张同步绑定来源。
4. 区分共识、争议、空白、方法局限和未来方向。
5. 输出正文、参考文献和待对齐主张清单。

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
- 是否处理矛盾证据？
- 是否区分理论推断和实证发现？
- 是否避免过度概括？
- 是否为后续来源对齐保留主张表？

## 失败与停止条件

- 没有阅读矩阵，不得写正式综述正文。
- 没有主张证据对应表，不得生成投稿级正文。
- 关键章节缺少证据时，必须回到检索或矩阵阶段。

## 安全边界

不伪造文献、引用、页码、理论贡献或研究空白。

## 完成条件

生成综述框架、章节主张表、图表计划、综述正文和 APA 参考文献。