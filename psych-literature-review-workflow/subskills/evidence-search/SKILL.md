---
name: review-evidence-search
description: Local subskill under psych-literature-review-workflow for transparent literature-review evidence search.
---

# Review Evidence Search / 综述证据检索分 skill

本分 skill 用于正式综述检索，服务叙述综述、理论综述、范围综述、方法学综述、测量综述和系统综述预备。

## 默认数据库

PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。

## 输出

- `review_protocol.md`
- `queries.md`
- `database_search_log.csv`
- `candidate_records.csv`
- `search_saturation_log.csv`

## 饱和停止规则

新增文献若连续不能提供新理论、新方法、新测量、新人群、新争议、新证据或高质量引用价值，才可记录为综述写作价值饱和；这不是数学意义上的穷尽。