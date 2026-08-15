---
name: cog-neuro-evidence-search
description: Local subskill under psych-cog-neuro-review for cognitive neuroscience evidence search. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# 证据检索分 skill

## 目标

为认知神经科学综述建立可追溯的理论、范式、指标、方法和实证证据检索链。

## 适用场景

- 需要检索 EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理或行为任务相关证据。
- 需要记录检索式、数据库、结果数、补充追溯和证据空白。

## 输入

综述问题、机制边界、关键词、范式名称、指标名称、目标人群、数据库权限、Zotero collection，以及现有机制矩阵、证据账本、缺口和历轮原始导出。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 拆分检索主题：构念、机制、范式、指标、脑区/网络、方法和人群。
2. 由已读证据和机制槽缺口构建 query family，数据库专用检索式分别覆盖模态、范式、预处理、统计校正、ROI/全脑、时频/成分和反向证据。
3. 默认用已合法登录的内置浏览器检索并导出，页面不兼容时回退到授权外置浏览器；记录精确语法、日期、限制、结果数和不可变原始导出。
4. 将本轮全部结果追加到唯一候选主表，与历轮全部已见题录求差集；不能只对 Zotero/PDF 或已纳入报告查重。
5. 仅新增记录进入筛选；记录级去重与同研究多报告识别分开，标注理论、范式、方法、机制和背景用途。
6. 按机制证据槽、方法透明性和增量相关记录更新缺口与停止条件；不因脑区显著性或期望机制方向调整检索。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。用户明确要求时，可加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普，并记录理由。

## 输出文件

- `检索式记录_queries.md`
- `数据库检索记录_database_search_log.csv`
- `候选文献表_candidate_records.csv`
- `种子方法学文献表_seed_methods.csv`
- `证据空白备忘录_evidence_gap_memo.md`
- `缺PDF下载队列_freepaper.csv`（仅在父条目和附件状态核验后生成）

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否覆盖机制、范式、指标和方法？
- 是否记录每个数据库的检索式和结果数？
- 是否区分方法学证据与实证证据？
- 是否记录反向证据和矛盾证据？
- 是否对历轮全部已见题录求差集，并保留检索过但未入库的旧记录？

## 失败与停止条件

- 没有检索记录，不得声称完成正式综述。
- 检索式无法覆盖核心机制或指标时停止。
- 用户要求伪造检索结果、脑区结果或文献时停止。

## 安全边界

不绕过付费墙，不使用盗版论文站，不伪造 DOI、PMID、题录、检索结果或神经机制证据。

## 完成条件

形成检索式、检索记录、候选文献表、种子方法学文献表和证据空白备忘录。
