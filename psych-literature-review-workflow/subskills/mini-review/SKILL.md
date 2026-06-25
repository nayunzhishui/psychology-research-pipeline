---
name: review-mini-review
description: Local subskill under psych-literature-review-workflow for short, bounded mini-reviews and early topic exploration. Chinese-first; use only inside the literature review workflow.
---

# 小综述分 skill

## 目标

在早期选题、课程作业或导师沟通中，快速形成边界清楚、证据有限但不夸大的小综述。

## 适用场景

- 需要快速了解某一方向。
- 需要 5–20 篇核心文献的初步整合。
- 需要为正式综述做选题预备。

## 输入

研究方向、初步关键词、种子文献、目标字数、用途和时间限制。

## 执行步骤

1. 明确小综述边界和限制。
2. 检索或整理少量种子文献。
3. 分类文献并提取核心观点。
4. 写作简短综述，明确证据范围有限。
5. 输出下一步正式检索计划。

## 输出文件

- `小综述范围_mini_review_scope.md`
- `种子文献表_seed_literature_table.csv`
- `小综述_mini_review.md`
- `下一步检索计划_next_search_plan.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否声明检索范围有限？
- 是否避免声称覆盖全部文献？
- 是否指出下一步需要补充的检索？

## 失败与停止条件

- 文献少于基本支撑量时不得写强结论。
- 用户要求写成系统综述时，必须转入正式综述流程。

## 安全边界

不把小综述伪装成系统综述、范围综述或完整证据综合。

## 完成条件

形成小综述、种子文献表和下一步检索计划。