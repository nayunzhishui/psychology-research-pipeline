---
name: review-submission-review
description: Local subskill under psych-literature-review-workflow for top-journal-prep simulated review of psychology literature review manuscripts. Chinese-first; use only inside the literature review workflow.
---

# 模拟投稿审稿分 skill

## 目标

以顶刊预备审查强度，对心理学综述稿进行模拟主编初筛、多角色审稿、修改矩阵和作者回复草稿准备。该流程不等于真实投稿，也不承诺发表。

## 适用场景

- 综述正文、矩阵、来源对齐和参考文献已基本完成。
- 需要模拟中文/英文期刊审稿，尤其需要检索透明性和引用准确性审查。

## 输入

综述正文、参考文献、综述协议、检索记录、筛选记录、阅读矩阵、来源对齐表、目标期刊或候选期刊列表。

## 执行步骤

1. 主编初筛：scope、创新性、透明性、格式和明显拒稿风险。
2. 理论贡献审稿：理论推进、整合深度和边界条件。
3. 检索透明性审稿：数据库、检索式、纳排、筛选和饱和停止。
4. 方法学审稿：综述类型、协议、质量评价和证据综合。
5. 文献完整性审稿：核心文献是否遗漏，证据覆盖是否充分。
6. 证据综合审稿：矛盾、空白、过度概括和未来方向。
7. 引用准确性审稿：来源对齐、页码、APA 引用和参考文献。
8. APA/格式审稿：标题层级、图表、摘要、参考文献和补充材料。
9. 反对性审稿：主动寻找最可能导致拒稿的问题。
10. 输出修改矩阵和作者回复草稿。

## 输出文件

- `模拟主编初筛_editor_screening.md`
- `模拟理论贡献审稿_theory_review.md`
- `模拟检索透明性审稿_search_transparency_review.md`
- `模拟方法学审稿_methods_review.md`
- `模拟文献完整性审稿_literature_completeness_review.md`
- `模拟证据综合审稿_synthesis_review.md`
- `模拟引用准确性审稿_citation_accuracy_review.md`
- `模拟格式审稿_format_review.md`
- `模拟反对性审稿_adversarial_review.md`
- `修改矩阵_revision_matrix.csv`
- `作者回复草稿_response_to_reviewers.md`
- `顶刊预备度报告_top_journal_readiness.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否完成来源对齐？
- 是否核查目标期刊官网要求？
- 是否明确标注模拟审稿性质？
- 是否区分必须修改、建议修改和可暂缓修改？

## 失败与停止条件

- 没有来源对齐，不得声称“可投稿”。
- 没有检索记录或筛选记录，不得通过检索透明性审稿。
- 没有期刊官网核查，不得给出最终投稿建议。
- 发现高风险问题时，必须先生成修改矩阵，不得直接写“建议投稿”。

## 安全边界

不执行真实投稿，不联系编辑，不支付费用，不冒充真实审稿人，不伪造审稿意见或期刊反馈。

## 完成条件

完成全角色模拟审稿、顶刊预备度报告、修改矩阵和作者回复草稿，并明确当前状态：可继续修改、可预投稿、需重大返工或暂不建议投稿。