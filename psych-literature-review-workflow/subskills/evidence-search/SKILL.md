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

综述方向、概念边界、纳排标准草案、关键词、数据库权限、Zotero collection。

## 执行步骤

1. 构建中英文关键词和布尔检索式。
2. 按数据库分别检索并记录日期、检索式、限制条件和结果数。
3. 记录去重、初筛、补充追溯和手动检索。
4. 建立候选文献表，标注文献类型和初步用途。
5. 按检索饱和规则判断是否继续检索。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普；用户明确要求时再加入并记录理由。

## 输出文件

- `检索式记录_queries.md`
- `检索记录_search_log.csv`
- `候选文献表_candidate_records.csv`
- `检索饱和记录_search_saturation_log.csv`
- `证据空白备忘录_evidence_gap_memo.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否覆盖核心构念、人群、测量、方法和证据类型？
- 是否记录每个数据库的检索式和结果数？
- 是否记录补充追溯和手动检索？
- 是否有明确检索饱和依据？

## 失败与停止条件

- 没有检索记录，不得声称完成正式综述。
- 没有纳排标准，不得进入系统综述或范围综述预备。
- 检索式无法覆盖核心概念时停止。
- 用户要求伪造检索结果时停止。

## 安全边界

不绕过付费墙，不使用盗版论文站，不伪造 DOI、PMID、题录、检索结果或数据库记录。

## 完成条件

形成检索式、检索记录、候选文献表、检索饱和记录和证据空白备忘录。