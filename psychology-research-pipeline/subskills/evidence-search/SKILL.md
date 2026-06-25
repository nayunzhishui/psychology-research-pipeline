---
name: empirical-evidence-search
description: Local subskill under psychology-research-pipeline for empirical psychology evidence search. Chinese-first; use only inside the empirical workflow.
---

# 证据检索分 skill

## 目标

为实证论文的理论依据、变量模型、量表选择、方法设计和引言写作提供可追溯证据。

## 适用场景

- 需要检索核心理论、综述/元分析、量表/方法文章和直接相关实证研究。
- 需要建立种子文献表、候选文献表和检索记录。
- 需要为后续文献筛选、方法设计和写作提供证据基础。

## 输入

- 项目定标结果、变量模型、关键词、中英文术语。
- 用户可访问的数据库、Zotero collection、已有文献或 DOI/PMID。

## 执行步骤

1. 拆分检索主题：核心构念、变量关系、人群、测量工具、研究设计、方法学证据。
2. 构建中英文检索式，记录数据库、日期、检索式和结果数。
3. 优先识别高质量综述、元分析、理论文章、方法学文章和量表来源。
4. 建立候选文献表，初步标注用途：理论、方法、测量、实证、背景。
5. 明确证据空白和需要继续检索的问题。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普；用户明确要求时再加入并记录理由。

## 输出文件

- `检索式记录_queries.md`
- `检索记录_search_log.csv`
- `候选文献表_candidate_records.csv`
- `种子文献表_seed_papers.csv`
- `证据空白备忘录_evidence_gap_memo.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 检索式是否覆盖构念、变量、人群、方法和测量？
- 是否记录数据库、日期、检索式和结果数？
- 是否区分综述、理论、方法、量表和实证文献？
- 是否明确哪些文献只能作背景、哪些可支撑核心假设？

## 失败与停止条件

- 没有检索记录时不得进入正式写作。
- 没有量表来源文献时不得声称“采用某量表”。
- 没有全文时不得做页码级强引用。
- 数据库权限或 Zotero 导入失败时，生成 `全文获取失败清单_failed_ingest_queue.csv`。

## 安全边界

不绕过付费墙、MFA、验证码或出版社条款；不使用盗版论文站；不伪造 DOI、PMID、题录或引用。

## 完成条件

形成可追溯检索记录、候选文献表、种子文献表和证据空白备忘录，并标明下一步筛选优先级。