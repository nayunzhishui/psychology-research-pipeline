---
name: review-evidence-search
description: Local subskill under psych-literature-review-workflow for transparent psychology literature review evidence search. Chinese-first; use only inside the literature review workflow.
---

# 证据检索分 skill

## 目标

为综述建立可追溯、可复核、边界清楚的文献检索链。

## 适用场景

- 需要正式检索叙述综述、整合型综述、理论综述、范围综述、方法学综述、测量综述或系统综述预备。
- 需要记录数据库、检索式、日期、结果数、去重和饱和停止依据。

## 输入

综述方向、概念边界、纳排标准草案、关键词、数据库权限、Zotero collection，以及现有阅读矩阵、证据账本、缺口、检索计划和历轮原始导出。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 由综述问题、已读证据和证据槽缺口构建概念块/query family；为每个数据库冻结可直接执行的专用语法和停止条件。
2. 默认在用户已合法登录的内置浏览器检索；兼容性不足时回退到授权外置浏览器。记录日期、平台、精确检索式、限制、结果数和不可变原始导出。
3. 将本轮全部结果追加到唯一候选主表，再与历轮全部已见题录求差集；不能只对 Zotero、PDF 或上一轮纳入项查重。
4. 仅新增题录进入筛选；记录级去重与研究家族识别分开，补充追溯和手动检索各有独立 `search_id`。
5. 根据证据覆盖和增量相关记录判断饱和，不以固定篇数、引用数或期刊声望替代停止判断。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普；用户明确要求时再加入并记录理由。

## 输出文件

- `检索式记录_queries.md`
- `检索记录_search_log.csv`
- `候选文献表_candidate_records.csv`
- `检索饱和记录_search_saturation_log.csv`
- `证据空白备忘录_evidence_gap_memo.md`
- `缺PDF下载队列_freepaper.csv`（仅在筛选保留项入库并核验附件后生成）

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否覆盖核心构念、人群、测量、方法和证据类型？
- 是否记录每个数据库的检索式和结果数？
- 是否记录补充追溯和手动检索？
- 是否有明确检索饱和依据？
- 是否保存历轮全部已见记录，且本轮差集包含检索过但未入库的旧记录？

## 失败与停止条件

- 没有检索记录，不得声称完成正式综述。
- 没有纳排标准，不得进入系统综述或范围综述预备。
- 检索式无法覆盖核心概念时停止。
- 用户要求伪造检索结果时停止。

## 安全边界

不绕过付费墙，不使用盗版论文站，不伪造 DOI、PMID、题录、检索结果或数据库记录。

## 完成条件

形成检索式、检索记录、候选文献表、检索饱和记录和证据空白备忘录。
