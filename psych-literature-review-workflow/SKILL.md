---
name: psych-literature-review-workflow
description: Use this standalone Chinese-first main skill folder for psychology literature-review workflows, from broad research-direction exploration to focused review protocol, saturated-but-bounded literature collection, Chrome/Zotero Connector ingestion, folder fallback, classification, 1–4 relevance rating, full-text evidence matrix, HTML reference star map, APA-style review writing, sentence/paragraph-to-source alignment, and simulated Chinese/English submission review. 这是“新的通用综述工作流”，适用于人格功能损害、健康心理学、临床心理学、发展心理学、心理测量、精神病理学、普通认知心理学等综述主题；本 skill 被选中后必须在本主 skill 文件夹范围内独立完成任务，可使用本目录下 subskills/，但不依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板；不要用于实证数据分析、认知神经科学专用实验设计、伪造文献、绕过付费墙、无人值守批量下载、真实投稿提交，或脱离证据矩阵的自由写作。
---

# Psychology Literature Review Workflow / 新的通用综述工作流

本 skill 是三个主工作流之一，定位为**通用心理学文献综述写作独立工作流**。它用于把宽泛研究方向推进为可聚焦、可检索、可审计、可写作、可模拟投稿的综述项目。默认服务心理学、健康心理学、临床心理学、发展心理学、精神病理学、心理测量、心理干预、普通认知心理学等方向。当前可用于“人格功能损害（impairment in personality functioning）”等主题，但不能写死为某一个主题。

默认语言为中文。必要英文保留于数据库检索式、英文题名、量表名、理论名、变量名、DOI/PMID、APA 引文、参考文献表和必要术语。

## 1. 独立调用原则

本 skill 被用户或 Codex 选中后，应**在本主 skill 文件夹范围内独立完成通用心理学综述工作流**，范围包括主 `SKILL.md` 与本目录下的 `subskills/`。不得把任务转交、拆分或依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板。可以在边界判断时说明其他主 skill 更适合，但一旦继续使用本 skill，就必须在本主 skill 文件夹范围内完成任务。

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流，用于含数据、实验、问卷、干预、心理测量或统计分析的论文项目。
- `psych-cog-neuro-review`：认知神经科学工作流，用于 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合主题。
- `psych-literature-review-workflow`：新的通用综述工作流，用于不以神经/生理指标或实验数据分析为核心的心理学综述。

若用户目标是普通心理学综述，且不以神经/生理指标、实验范式或脑机制为核心，使用本 skill。若主题包含少量神经机制背景，但综述核心仍是心理学概念、测量、发展、临床或健康心理学证据，本 skill 仍可独立处理，不调用其他 skill。

## 2. 内部分 skill 结构

本目录下的 `subskills/` 是本主工作流的一部分。Codex 可在本 skill 被选中后，按阶段读取并使用这些分 skill。分 skill 不作为顶层入口，也不得跨主 skill 使用。

推荐顺序：

1. `subskills/review-scope`：宽方向探索和综述聚焦。
2. `subskills/evidence-search`：正式综述检索和饱和停止日志。
3. `subskills/zotero-ingest`：Chrome + Zotero Connector 入库。
4. `subskills/literature-screen`：分类、纳排和 1–4 级相关性评级。
5. `subskills/literature-matrix`：全文阅读矩阵和证据提取。
6. `subskills/star-map`：基于阅读矩阵和激活扩散权重制作 HTML 文献星图。
7. `subskills/source-alignment`：正文—参考文献—原文证据对齐。
8. `subskills/manuscript-write`：APA 综述正文写作。
9. `subskills/submission-review`：中文/英文期刊模拟审稿。
10. `subskills/mini-review`：早期小综述或课程小综述。
11. `subskills/old-review-workflow`：旧版综述流程迁移和兼容；不得作为第四个主 skill。

## 3. 适用场景

使用本 skill，当用户提出以下任务之一：

- 只给出一个宽研究方向，需要先检索综述、方法学文章和核心理论文章，帮助用户聚焦综述方向。
- 已经给出聚焦后的综述主题，需要进入正式文献检索、Zotero 入库、全文阅读、证据矩阵和综述写作。
- 需要制作中文为主、APA 第 7 版兼容的心理学综述稿。
- 需要输出导师汇报版简表、CSV/Excel/Markdown 阅读矩阵、HTML 文献星图、正文—参考文献精确对齐表，以及模拟投稿审稿意见。

不要使用本 skill，当任务只是临时解释概念、润色单段文字、写邮件、普通摘要、处理实证数据、跑统计模型或写实证论文结果；也不要用于伪造文献、伪造页码、伪造 DOI、伪造审稿意见、绕过权限、下载盗版 PDF、真实投稿系统操作。

## 4. 默认综述类型与运行模式

默认运行方式为：**半系统化叙述综述 / 整合型综述**。可根据用户要求切换为 narrative review、theoretical review、scoping review、systematic review、methodological review、measurement review 或 meta-analysis-prep review。

不要在没有正式协议、完整检索日志、纳排标准、筛查记录和偏倚风险评价时，把文章声称为“系统综述”。如果只是吸收 PRISMA 的透明性原则，应写作“半系统化叙述综述”或“透明化叙述综述”。

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 早期选题、课程综述、快速方向判断 | 阶段 00、01、02 简化版，阶段 04–06 可抽样完成 | 聚焦建议、初步文献表、简版框架 |
| `standard` | 研究生综述、学位论文综述、中文期刊预备稿 | 阶段 00–11 全流程；单人筛查可接受但需声明 | 完整矩阵、正文草稿、引用对齐、模拟审稿 |
| `strict` | 范围综述、系统综述、英文投稿预备稿、高风险引用核查 | 正式协议、完整检索日志、严格纳排、质量评价、完整对齐 | 可审计检索链、PRISMA 风格追踪、严格审计报告 |

## 5. 总原则

1. **先探索聚焦，再正式综述**：主题未聚焦时，不直接大规模下载全文。先用高质量综述、方法学文章、理论文章帮助用户确定边界。
2. **证据先于写作**：正式写作必须来自题录、全文、阅读卡、证据矩阵和来源位置，不得先写后找文献硬配。
3. **广覆盖但有停止规则**：正式检索应尽可能完整覆盖主题，直到新增文献不能再提供新的理论、方法、测量、人群、关键发现、争议或高质量证据。这里的停止不是数学意义上的穷尽，而是综述写作价值饱和。
4. **分类阅读**：先分类，再评级，再阅读全文；不要把所有文献平铺成普通参考文献表。
5. **相关度与质量分开**：1–4 级表示与主题贴合度，不等于方法质量。方法质量另行评价。
6. **正文写作时同步引文对齐**：不要等写完后才补引用。每个事实性、定义性、理论性、方法性或结论性主张在写作时就绑定来源。
7. **模拟审稿必须标注模拟性质**：不能让用户误以为是真实期刊反馈。
8. **中文优先，英文溯源**：说明、判断标准、矩阵、审稿意见默认中文；检索、题录和 APA 信息保持英文准确。

## 6. 启动时的需求沟通

首次运行时先简短询问，除非用户已经给出答案。用户未回答时，可以使用默认值继续，但必须在 `logs/decisions.md` 中记录为 `assumption`。

必要问题：

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 目标综述类型：叙述综述、理论综述、范围综述、系统综述、方法学综述、测量综述，还是默认半系统化叙述综述？
3. 运行模式：`lite`、`standard`、`strict`，默认 `standard`。
4. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿？
5. 核心边界：核心构念、目标人群、年龄段、临床/非临床、研究设计、是否纳入干预、是否纳入神经机制。
6. 文献获取方式：是否允许 Codex 使用 Chrome + Zotero Connector；Zotero 目标 collection 名称；若失败是否下载到文件夹由用户手动导入。
7. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

## 7. 默认数据库范围

默认数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助检索，不单独声称完整）、CNKI、期刊官网、Zotero 本地库。

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求或项目需要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 8. 默认运行目录

```text
review_runs/<YYYYMMDD>_<short_topic>/
├── state.json
├── manifest.json
├── logs/
│   ├── decisions.md
│   └── events.jsonl
├── literature/
│   ├── 00_待导入Zotero/
│   ├── 01_已导入Zotero/
│   ├── 02_全文PDF/
│   ├── 03_题录导出/
│   ├── 04_阅读矩阵/
│   ├── 05_星图/
│   └── 06_综述正文/
├── 00_exploration/
├── 01_protocol/
├── 02_search/
├── 03_library/
├── 04_screening/
├── 05_matrix/
├── 06_synthesis/
├── 07_star_map/
├── 08_outline/
├── 09_manuscript/
├── 10_alignment/
└── 11_submission_review/
```

不要覆盖旧文件。修订版使用 `_v2`、`_v3`，并在日志中说明修订原因。

## 9. 阶段总览

| 阶段 | 名称 | 目标 | 主要产物 |
|---|---|---|---|
| 00 | 宽方向探索 | 从宽方向中识别可写综述方向 | `scoping_brief.md`, `seed_reviews.csv`, `seed_methods.csv`, `focus_options.md`, `导师汇报版简表.md` |
| 01 | 聚焦与协议冻结 | 把聚焦主题转为可执行综述协议 | `review_protocol.md`, `concept_map.md`, `inclusion_exclusion.md` |
| 02 | 正式大范围检索 | 饱和式搜集符合主题的文献 | `queries.md`, `search_log.csv`, `candidate_records.csv`, `search_saturation_log.csv` |
| 03 | Zotero/全文获取 | Chrome + Zotero Connector 入库，备选为文件夹手动导入 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与初筛 | 分类文献并给出 1–4 级主题符合程度 | `classification.csv`, `relevance_ratings.csv`, `screening_log.csv`, `exclusion_reason_register.csv` |
| 05 | 全文阅读矩阵 | 深读全文并建立证据矩阵 | `literature_matrix.csv`, `literature_matrix.xlsx`, `literature_matrix.md`, `quality_appraisal.csv` |
| 06 | 证据综合 | 汇总理论、方法、发现、矛盾和空白 | `claim_evidence_map.csv`, `contradiction_gap_register.csv`, `synthesis_memo.md` |
| 07 | HTML 文献星图 | 以矩阵为基础制作参考文献星图 | `literature_star_map.html`, `star_map_weights.csv`, `star_map_notes.md` |
| 08 | 综述框架 | 制定章节结构、论证顺序和图表计划 | `review_outline.md`, `section_claims.md`, `figure_table_plan.md` |
| 09 | 正文写作 | 按 APA 第 7 版写作中文综述 | `manuscript.md`, `manuscript.docx`, `references.bib`, `apa_references.md` |
| 10 | 引用对齐 | 精确核查正文与来源 | `source_alignment_table.csv`, `source_alignment_table.xlsx`, `unsupported_claims.md` |
| 11 | 模拟投稿审稿 | 模拟中文核心与英文期刊审稿 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv`, `author_response_draft.md` |

## 10. 核心输出标准

文献相关性 1–4 级：1=边缘背景，2=概念/背景相关，3=直接支撑某一章节，4=核心主线证据。质量评价另行记录方法质量、样本适配度、理论贡献、证据强度、引用价值和连接度。

阅读矩阵至少包括：题录、DOI/PMID、研究类型、理论框架、样本、人群、测量工具、研究设计、统计方法、核心发现、局限、可引用位置、适合写入章节、证据类型、主题相关度、方法质量和引用风险。

引用对齐表至少包括：综述页码、综述段落、综述原句、支撑文献、文献页码、文献章节/段落/表图、原文短摘录、证据类型、支持程度、是否过度推断、是否需要复核。

HTML 文献星图必须以矩阵为依据，节点可包含文献、理论、变量、测量、方法、人群、发现和争议；权重必须记录在 `star_map_weights.csv` 和 `star_map_notes.md`。

## 11. Chrome + Zotero 边界

用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据；不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制；不使用盗版论文站、影子图书馆、PDF bot 或泄露账号；不无人值守高速批量下载；不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 12. 模拟投稿与最终审核

默认模拟两套审查：中文心理学核心/相关期刊，以及英文心理学/临床/健康/发展/测量相关期刊。期刊 scope、格式、版面费、开放获取、AI policy 和投稿要求必须联网核查。模拟审稿意见必须标注为模拟，不冒充真实期刊反馈。

## 13. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在关键引用、检索、筛查、矩阵、对齐或 APA 问题未解决时声称“可直接投稿”。