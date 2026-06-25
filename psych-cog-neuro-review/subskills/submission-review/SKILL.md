---
name: cog-neuro-submission-review
description: Local subskill under psych-cog-neuro-review for top-journal-prep simulated review of cognitive neuroscience review manuscripts. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 模拟投稿审稿分 skill

## 目标

以顶刊预备审查强度，对认知神经科学综述稿进行模拟主编初筛、多角色审稿、修改矩阵和作者回复草稿准备。该流程不等于真实投稿，也不承诺发表。

## 适用场景

- 综述正文、检索记录、筛选记录、机制矩阵、方法评价和来源对齐已基本完成。
- 需要模拟认知神经科学、神经心理学、情绪神经科学、睡眠研究或心理生理方向的期刊审稿。

## 输入

综述正文、参考文献、综述协议、检索记录、筛选记录、机制矩阵、方法评价、预处理透明性评价、来源对齐表、目标期刊或候选期刊列表。

## 执行步骤

1. 主编初筛：scope、机制贡献、方法透明性、格式和明显拒稿风险。
2. 理论机制审稿：机制模型、理论贡献、边界条件。
3. 实验范式审稿：任务、刺激、流程、行为指标和范式适配度。
4. 神经/生理方法审稿：EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理方法质量。
5. 预处理与分析审稿：预处理透明性、统计模型、校正、效应量和探索性分析标注。
6. 统计审稿：证据强度、稳健性、样本量和结果解释边界。
7. 开放科学审稿：数据、代码、材料、协议、预注册和限制说明。
8. 引用与机制对齐审稿：机制主张、原文位置、引用风险和过度推断。
9. APA/格式审稿：标题层级、图表、摘要、参考文献和补充材料。
10. 反对性审稿：主动寻找最可能导致拒稿的问题。
11. 输出修改矩阵和作者回复草稿。

## 输出文件

- `模拟主编初筛_editor_screening.md`
- `模拟理论机制审稿_mechanism_review.md`
- `模拟实验范式审稿_paradigm_review.md`
- `模拟神经生理方法审稿_neuro_methods_review.md`
- `模拟预处理分析审稿_preprocessing_analysis_review.md`
- `模拟统计审稿_statistical_review.md`
- `模拟开放科学审稿_open_science_review.md`
- `模拟机制对齐审稿_mechanism_alignment_review.md`
- `模拟格式审稿_format_review.md`
- `模拟反对性审稿_adversarial_review.md`
- `修改矩阵_revision_matrix.csv`
- `作者回复草稿_response_to_reviewers.md`
- `顶刊预备度报告_top_journal_readiness.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否完成机制来源对齐？
- 是否核查目标期刊官网要求？
- 是否明确标注模拟审稿性质？
- 是否区分必须修改、建议修改和可暂缓修改？

## 失败与停止条件

- 没有来源对齐，不得声称“可投稿”。
- 没有机制矩阵或方法评价，不得通过机制和方法审稿。
- 没有期刊官网核查，不得给出最终投稿建议。
- 发现高风险问题时，必须先生成修改矩阵，不得直接写“建议投稿”。

## 安全边界

不执行真实投稿，不联系编辑，不支付费用，不冒充真实审稿人，不伪造审稿意见或期刊反馈。

## 完成条件

完成全角色模拟审稿、顶刊预备度报告、修改矩阵和作者回复草稿，并明确当前状态：可继续修改、可预投稿、需重大返工或暂不建议投稿。