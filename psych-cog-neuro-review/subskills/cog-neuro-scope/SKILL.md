---
name: cog-neuro-scope
description: Local subskill under psych-cog-neuro-review for cognitive neuroscience review scoping and mechanism-boundary classification. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 方向定标分 skill

## 目标

把认知神经科学宽方向聚焦为可检索、可评价、可写作的综述问题和机制边界。

## 适用场景

- 用户只有宽方向，需要形成机制综述、理论综述、方法学综述或范式综述主题。
- 用户已有题目，但脑机制、实验范式、神经/生理指标或目标人群边界不清。

## 输入

研究方向、核心构念、人群、可能范式、神经/生理指标、目标用途、已有文献或导师要求。

## 执行步骤

1. 判断综述类型：机制、理论、方法学、范式、指标、范围、系统综述预备或元分析预备。
2. 明确构念、人群、任务范式、神经/生理指标和机制层级。
3. 输出 2–4 个候选综述问题，比较创新性、可检索性、证据量和风险。
4. 推荐主方向，并列出备选方向和放弃理由。

## 输出文件

- `方向定标简报_cog_neuro_scope.md`
- `机制范围说明_mechanism_scope.md`
- `候选综述问题_candidate_review_questions.md`
- `导师汇报版简表_supervisor_brief.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 机制问题是否清晰？
- 范式和指标是否与构念匹配？
- 人群和证据类型是否明确？
- 是否能形成检索式和纳排标准？

## 失败与停止条件

- 无法界定机制边界时停止。
- 主题缺乏可检索文献时停止。
- 用户要求凭空写脑机制时停止。

## 安全边界

不承诺发表；不把初步方向写成最终结论；不凭空声称某脑区、网络或成分参与某机制。

## 完成条件

形成推荐方向、备选方向、机制边界、初步证据基础和待确认问题。