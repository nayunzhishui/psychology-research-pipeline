# REM 与情绪记忆综述 Codex Prompt 示例

请调用 `psych-cog-neuro-review`，为我建立一个可复用的心理学/认知神经科学文献综述工作流。本次主题为：REM sleep and emotional memory（快速眼动睡眠与情绪记忆）。

## 研究目标

我需要写一篇偏可投稿风格的综述，中文核心综述风格优先，同时保留未来扩展为外文 Q1 review 的结构。请用中文进行工作流说明、文献矩阵整理和正文草稿写作；专业术语、脑区、范式、数据库字段保留英文原词，并在首次出现时给出中文解释。

## 必须执行的阶段

请不要直接写正文。先按以下阶段建立可审计流程：

1. `00_scope`：项目定标、工作区盘点、概念边界、研究问题。
2. `01_protocol`：选择综述类型和报告规范，冻结检索范围、纳入排除标准、提取字段、质量评价计划和 AI 使用规则。
3. `02_search`：生成中英文检索式，分别适配不同数据库语法，记录每个数据库检索日期、筛选条件、结果数量和导出文件。
4. `03_library`：核查 DOI/PMID/CNKI ID/Zotero item key、PDF 状态、重复文献和元数据一致性。
5. `04_screening`：标题摘要筛查、全文筛查、纳排理由和 PRISMA-style flow counts。
6. `05_extraction`：生成阅读矩阵、神经机制矩阵、质量评价表和核心文献阅读卡。
7. `06_synthesis`：在写作前生成证据综合计划、claim-evidence map、证据缺口表。
8. `07_prewrite`：冻结综述方法段、章节论证路径、允许/禁止的结论、图表计划和段落 ID 策略。
9. `08_manuscript`：完成 Markdown 综述草稿和 Word 草稿。
10. `09_audit`：执行段落—来源对应矩阵和参考文献一致性核查。

## 数据库范围

请覆盖以下数据库或资料来源：PubMed、Web of Science、PsycINFO、Scopus、CNKI、Google Scholar、Semantic Scholar、Crossref、Zotero 本地库。所有检索式、检索日期、筛选条件、结果数量、导出数量都必须记录。无法访问的数据库必须记录原因，不得假装已经检索。

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

1. `00_scope/workspace_inventory.md`
2. `00_scope/review_scope.md`
3. `00_scope/concept_map.md`
4. `01_protocol/reporting_plan.md`
5. `01_protocol/review_protocol.md`
6. `02_search/search_strategy.md`
7. `02_search/database_search_log.csv`
8. `02_search/candidate_records.csv`
9. `03_library/library_acquisition_manifest.csv`
10. `03_library/acquisition_report.md`
11. `04_screening/screening_table.csv`
12. `04_screening/prisma_flow_counts.csv`
13. `05_extraction/literature_matrix.csv`
14. `05_extraction/neural_mechanism_matrix.csv`
15. `05_extraction/quality_appraisal.csv`
16. `06_synthesis/prewriting_synthesis_plan.md`
17. `06_synthesis/claim_evidence_map.csv`
18. `06_synthesis/evidence_gap_register.csv`
19. `07_prewrite/review_methods_plan.md`
20. `07_prewrite/section_argument_plan.md`
21. `08_manuscript/review_outline.md`
22. `08_manuscript/review_draft.md`
23. `08_manuscript/review_draft.docx`
24. `09_audit/paragraph_source_alignment_matrix.csv`
25. `09_audit/reference_consistency_check.csv`
26. `09_audit/unsupported_or_overstated_claims.md`

## 写作规则

- 不要编造文献、DOI、PMID、CNKI ID、样本量或研究结论。
- 不要把综述文献当成原始研究引用。
- 不要把相关性或神经影像关联写成因果。
- 不要用“近年来，随着……”等空泛开头。
- 每段必须有明确论点、证据和限制。
- 每个实证判断必须能回到文献来源。
- 对神经机制使用谨慎表达，如“提示”“可能反映”“与……相关”。
- 对 REM 和情绪记忆的关系，要区分编码、巩固、提取、消退、再巩固等阶段。
- 未读全文不得写“全文指出”。

## 额外要求

综述正文写完后，必须调用 `subskills/source-alignment/SKILL.md`，生成“综述原文—参考文献原文对应矩阵”。矩阵需要精确到：综述第几段、第几句话/论点、引用了哪篇文献、对应文献的哪一页/哪一节/哪一段/哪一个表格或结果、支持强度如何、是否存在过度推断。

在最终回复中，请给我：完成了哪些阶段和文件、哪些结论证据强、哪些结论证据弱、哪些引用或段落还需要人工核查、哪些阶段门控没有通过。
