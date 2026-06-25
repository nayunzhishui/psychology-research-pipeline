---
name: empirical-project-scope
description: Local subskill under psychology-research-pipeline for empirical psychology project scoping. Use only when the main empirical workflow is already selected. Chinese-first.
---

# Empirical Project Scope / 实证项目定标分 skill

本分 skill 只属于 `psychology-research-pipeline`，不得作为顶层独立入口，也不得调用其他主 skill。

## 目标

把宽泛研究兴趣转化为可执行的心理学实证论文项目。

## 启动问题

1. 当前是兴趣方向、初步题目、开题方案，还是已有数据？
2. 研究类型：横断、纵向、实验、干预、混合方法、心理测量、临床/健康/发展心理学研究。
3. 目标用途：课程论文、毕业论文、开题、中文期刊、英文期刊、注册报告。
4. 核心构念、目标人群、样本来源、可用工具、时间限制。

## 输出

- `project_brief.md`
- `research_question_options.md`
- `rq_hypotheses.md`
- `construct_variable_map.csv`
- `导师汇报版简表.md`

## 标准

研究问题必须同时满足：清晰构念、可测变量、明确人群、可行设计、可检验假设、伦理可接受、数据分析可落地。

## 停止条件

当研究问题、变量角色、样本范围、研究设计和最低分析路径均已明确时停止，并把未决问题写入 `logs/decisions.md`。