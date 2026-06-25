---
name: empirical-evidence-search
description: Local subskill under psychology-research-pipeline for evidence search supporting empirical psychology papers. Chinese-first; use only inside the empirical workflow.
---

# Empirical Evidence Search / 实证论文证据检索分 skill

本分 skill 只服务实证论文的理论、方法、量表和实证依据检索，不替代完整综述。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。

## 检索对象

- 核心理论与概念界定
- 综述/元分析
- 方法学与测量工具文章
- 与变量模型直接相关的实证研究
- 目标人群和研究设计相关证据

## 输出

- `queries.md`
- `search_log.csv`
- `candidate_records.csv`
- `seed_papers.csv`
- `evidence_gap_memo.md`

## 质量要求

记录数据库、检索式、日期、结果数、筛选理由和局限。所有事实性结论必须可追溯到题录或全文。