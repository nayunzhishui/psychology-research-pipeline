---
name: psych-literature-review-workflow
description: Use this standalone Chinese-first main skill folder for psychology literature-review workflows. 这是“心理学通用综述工作流”，适用于叙述综述、整合型综述、理论综述、范围综述、方法学综述、测量综述、系统综述预备和元分析预备；本 skill 被选中后必须在本主 skill 文件夹范围内独立完成任务，可使用本目录下 subskills/、templates/、checklists/、rubrics/、examples/，但不依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板；本地生成文件默认使用“中文主名_英文兼容名.扩展名”；不要用于实证数据分析、认知神经科学专用实验设计、伪造文献、绕过付费墙、无人值守批量下载、真实投稿提交，或脱离证据矩阵的自由写作。
---

# 心理学通用综述工作流

本 skill 是三个主工作流之一，定位为**通用心理学文献综述写作独立工作流**。它用于把宽泛研究方向推进为可聚焦、可检索、可审计、可写作、可模拟投稿的综述项目。默认服务心理学、健康心理学、临床心理学、发展心理学、精神病理学、心理测量、心理干预、普通认知心理学等方向。

默认语言为中文。必要英文保留于数据库检索式、英文题名、量表名、理论名、变量名、DOI/PMID、APA 引文、参考文献表、文件扩展名和固定术语。

## 1. 独立调用原则

本 skill 被用户或 Codex 选中后，应**在本主 skill 文件夹范围内独立完成通用心理学综述工作流**，范围包括主 `SKILL.md` 与本目录下的 `subskills/`、`templates/`、`checklists/`、`rubrics/`、`examples/`。不得把任务转交、拆分或依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板。

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流，用于含数据、实验、问卷、干预、心理测量或统计分析的论文项目。
- `psych-cog-neuro-review`：认知神经科学工作流，用于 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合主题。
- `psych-literature-review-workflow`：通用心理学综述工作流，用于不以神经/生理指标或实验数据分析为核心的心理学综述。

## 2. 支持的综述类型

支持：叙述综述、整合型综述、理论综述、范围综述、方法学综述、测量综述、系统综述预备、元分析预备。

不要在没有正式协议、完整检索日志、纳排标准、筛查记录和偏倚/质量评价时，把文章声称为“系统综述”。如果只是吸收 PRISMA 的透明性原则，应写作“透明化叙述综述”“整合型综述”或“系统综述预备”。

## 3. 内部分工

### subskills/

1. `review-scope`：宽方向探索和综述聚焦。
2. `evidence-search`：正式综述检索和检索饱和记录。
3. `zotero-ingest`：Chrome + Zotero Connector 入库。
4. `literature-screen`：分类、纳排和 1–4 级相关性评级。
5. `literature-matrix`：全文阅读矩阵和证据提取。
6. `star-map`：基于阅读矩阵和激活扩散权重制作 HTML 文献星图。
7. `source-alignment`：正文—参考文献—原文证据对齐。
8. `manuscript-write`：APA 综述正文写作。
9. `submission-review`：顶刊预备强度的模拟综述审稿。
10. `mini-review`：早期小综述或课程小综述。
11. `old-workflow-migration`：旧版综述流程迁移和兼容，不作为主入口。

### templates/ checklists/ rubrics/ examples/

- `templates/`：综述方向、协议、检索、筛选、矩阵、星图、正文、来源对齐和审稿模板。
- `checklists/`：PRISMA 2020、PRISMA-ScR、检索透明性、检索饱和、筛选、矩阵、来源对齐、投稿前和停止条件检查表。
- `rubrics/`：综述选题、检索透明性、文献完整性、证据综合、理论贡献、引用风险、写作质量和顶刊预备度评分表。
- `examples/`：不同模式、不同综述类型和顶刊级模拟审稿启动示例。

## 4. 本地文件命名

本地运行时，文件夹名和文件名默认采用：

```text
中文主名_英文兼容名.扩展名
```

示例：

```text
综述协议_review_protocol.md
文献阅读矩阵_literature_matrix.csv
文献星图_literature_star_map.html
来源对齐表_source_alignment_table.csv
模拟审稿意见_simulated_reviews.md
```

若因软件或脚本限制必须使用纯英文名，必须在 `日志/决策记录_decisions.md` 中记录原因，并提供中文对照。

## 5. 运行模式

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 早期选题、课程综述、快速方向判断 | 方向聚焦、种子文献、简版框架 | 方向聚焦简报、种子文献表、简版综述 |
| `standard` | 研究生综述、学位论文综述、中文期刊预备稿 | 00–11 全流程；单人筛查可接受但需声明 | 完整矩阵、正文草稿、引用对齐、模拟审稿 |
| `strict` | 范围综述、系统综述预备、英文投稿预备稿、高风险引用核查 | 正式协议、完整检索日志、严格纳排、质量评价、完整对齐 | 可审计综述包、PRISMA 风格追踪、严格审计报告 |
| `top-journal-prep` | 顶刊预备审查强度 | strict 基础上增加反对性审稿、文献完整性审计、理论贡献评分和不可投稿风险清单 | 顶刊预备度报告、全角色模拟审稿、修改矩阵 |

不得承诺发表顶级文章。只能提供顶刊预备审查强度的流程、材料和质量控制。

## 6. 启动时必须确认

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 综述类型：叙述综述、整合型综述、理论综述、范围综述、方法学综述、测量综述、系统综述预备、元分析预备。
3. 运行模式：`lite`、`standard`、`strict`、`top-journal-prep`。
4. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿。
5. 核心边界：核心构念、目标人群、年龄段、临床/非临床、研究设计、是否纳入干预、是否纳入神经机制。
6. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero 目标 collection；失败时是否下载到文件夹由用户手动导入。
7. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问；用户未回答时，可以使用默认值继续，但必须在 `日志/决策记录_decisions.md` 中记录为 assumption。

## 7. 默认数据库范围

默认数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助检索，不单独声称完整）、CNKI、期刊官网、Zotero 本地库。

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求或项目需要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 8. 默认运行目录

```text
综述运行/<日期>_<简短主题>/
├── 状态记录_state.json
├── 文件清单_manifest.json
├── 日志/
│   ├── 决策记录_decisions.md
│   └── 事件记录_events.jsonl
├── 文献/
│   ├── 00_待导入Zotero/
│   ├── 01_已导入Zotero/
│   ├── 02_全文PDF/
│   ├── 03_题录导出/
│   ├── 04_阅读矩阵/
│   ├── 05_文献星图/
│   └── 06_综述正文/
├── 00_宽方向探索/
├── 01_聚焦与协议/
├── 02_正式检索/
├── 03_Zotero与全文获取/
├── 04_文献筛选/
├── 05_阅读矩阵/
├── 06_证据综合/
├── 07_文献星图/
├── 08_综述框架/
├── 09_综述正文/
├── 10_引用对齐/
└── 11_模拟投稿审稿/
```

不要覆盖旧文件。修订版使用 `_v2`、`_v3`，并在日志中说明修订原因。

## 9. 阶段总览

| 阶段 | 名称 | 主要产物 |
|---|---|---|
| 00 | 宽方向探索 | `综述方向聚焦_review_scope.md`, `种子综述文献表_seed_reviews.csv`, `综述方向候选方案_focus_options.md` |
| 01 | 聚焦与协议 | `综述协议_review_protocol.md`, `概念关系图_concept_map.md`, `纳入排除标准_inclusion_exclusion.md` |
| 02 | 正式检索 | `检索式记录_queries.md`, `检索记录_search_log.csv`, `候选文献表_candidate_records.csv`, `检索饱和记录_search_saturation_log.csv` |
| 03 | Zotero/全文获取 | `Zotero入库清单_zotero_manifest.csv`, `PDF全文清单_pdf_manifest.csv`, `全文获取报告_acquisition_report.md` |
| 04 | 文献筛选 | `文献筛选表_literature_screening.csv`, `相关性评级表_relevance_ratings.csv`, `排除理由登记表_exclusion_reason_register.csv` |
| 05 | 阅读矩阵 | `文献阅读矩阵_literature_matrix.csv/xlsx/md`, `质量评价表_quality_appraisal.csv`, `主张证据对应表_claim_evidence_map.csv` |
| 06 | 证据综合 | `证据综合备忘录_synthesis_memo.md`, `矛盾与空白登记表_contradiction_gap_register.csv` |
| 07 | 文献星图 | `文献星图_literature_star_map.html`, `星图权重表_star_map_weights.csv`, `星图说明_star_map_notes.md` |
| 08 | 综述框架 | `综述框架_review_outline.md`, `章节主张表_section_claims.md`, `图表计划_figure_table_plan.md` |
| 09 | 综述正文 | `综述正文_manuscript.md`, `综述正文_manuscript.docx`, `APA参考文献_apa_references.md` |
| 10 | 引用对齐 | `来源对齐表_source_alignment_table.csv`, `未支持主张清单_unsupported_claims.md`, `引用风险报告_citation_risk_report.md` |
| 11 | 模拟投稿审稿 | `模拟审稿意见_simulated_reviews.md`, `修改矩阵_revision_matrix.csv`, `作者回复草稿_response_to_reviewers.md` |

## 10. 强制停止条件

遇到以下情况必须停止并汇报，不得继续生成“完成稿”：

- 没有检索记录，不得声称完成正式综述。
- 没有纳排标准，不得声称完成范围综述或系统综述预备。
- 没有筛选记录，不得声称文献覆盖充分。
- 没有全文，不得做强引用或页码级来源对齐。
- 没有阅读矩阵，不得写正式综述正文。
- 没有来源对齐，不得声称“可投稿”。
- 没有期刊官网核查，不得生成最终投稿结论。
- 发现伪造文献、错误 DOI、无法核验来源或过度推断时，必须生成 `停止原因与补救清单_stop_reason_and_fix.md`。

## 11. 顶刊预备质量门槛

顶刊预备不是发表承诺，而是审查强度。必须至少经过以下 gate：

1. 综述主题重要、边界清晰、理论贡献明确。
2. 检索策略、数据库、时间、检索式和限制条件可追溯。
3. 纳排标准、筛选记录和排除理由透明。
4. 文献阅读矩阵、质量评价、主张证据对应表完整。
5. 证据综合能处理矛盾、空白和边界条件。
6. 文献星图和权重规则基于矩阵，不凭空添加关系。
7. 每个关键主张都有来源、页码/章节/表图或原文位置支持。
8. 模拟审稿包括主编、理论、检索透明性、方法、文献完整性、证据综合、引用准确性、格式和反对性审稿。

## 12. Chrome + Zotero 边界

用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据；不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制；不使用盗版论文站、影子图书馆、PDF bot 或泄露账号；不无人值守高速批量下载；不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 13. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在关键检索、筛选、矩阵、来源对齐、APA 或投稿规范问题未解决时声称“可直接投稿”。