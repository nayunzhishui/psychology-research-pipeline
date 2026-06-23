# REM 与情绪记忆综述 Codex Prompt 示例

请调用 `psych-cog-neuro-review`，为我建立一个可复用的心理学/认知神经科学文献综述工作流。本次主题为：REM sleep and emotional memory（快速眼动睡眠与情绪记忆）。

## 研究目标

我需要写一篇偏可投稿风格的综述，中文核心综述风格优先，同时保留未来扩展为外文 Q1 review 的结构。请用中文进行工作流说明、文献矩阵整理和正文草稿写作；专业术语、脑区、范式、数据库字段保留英文原词，并在首次出现时给出中文解释。

## 数据库范围

请覆盖以下数据库或资料来源：PubMed、Web of Science、PsycINFO、Scopus、CNKI、Google Scholar、Semantic Scholar、Crossref、Zotero 本地库。所有检索式、检索日期、筛选条件、结果数量、导出数量都必须记录。

## 文献范围

请同时纳入英文和中文文献。优先关注：

- REM sleep / rapid eye movement sleep
- emotional memory / affective memory
- fear memory / fear conditioning / extinction
- memory consolidation / reconsolidation
- EEG/ERP、fMRI、PSG、behavioral studies
- amygdala、hippocampus、vmPFC、dlPFC、ACC、insula、functional connectivity

## 输出文件

请至少生成：

1. `00_scope/review_scope.md`
2. `01_search/search_strategy.md`
3. `01_search/database_search_log.csv`
4. `02_screen/screening_table.csv`
5. `03_extract/literature_matrix.csv`
6. `03_extract/neural_mechanism_matrix.csv`
7. `04_synthesis/claim_evidence_map.csv`
8. `05_write/review_outline.md`
9. `05_write/review_draft.md`
10. `05_write/review_draft.docx`
11. `06_audit/paragraph_source_alignment_matrix.csv`
12. `06_audit/reference_consistency_check.csv`
13. `06_audit/unsupported_or_overstated_claims.md`

## 写作规则

- 不要编造文献、DOI、PMID、样本量或研究结论。
- 不要把综述文献当成原始研究引用。
- 不要把相关性或神经影像关联写成因果。
- 不要用“近年来，随着……”等空泛开头。
- 每段必须有明确论点、证据和限制。
- 每个实证判断必须能回到文献来源。
- 对神经机制使用谨慎表达，如“提示”“可能反映”“与……相关”。
- 对 REM 和情绪记忆的关系，要区分编码、巩固、提取、消退、再巩固等阶段。

## 额外要求

综述正文写完后，必须调用 `subskills/source-alignment/SKILL.md`，生成“综述原文—参考文献原文对应矩阵”。矩阵需要精确到：综述第几段、第几句话/论点、引用了哪篇文献、对应文献的哪一页/哪一节/哪一段/哪一个表格或结果、支持强度如何、是否存在过度推断。

在最终回复中，请给我：完成了哪些文件、哪些结论证据强、哪些结论证据弱、哪些引用或段落还需要人工核查。
