---
name: psych-literature-review-workflow
description: Use this standalone Chinese-first psychology literature-review workflow to move from broad research-direction exploration to focused review protocol, saturated-but-bounded literature collection, Chrome/Zotero Connector ingestion, folder fallback, classification, 1–4 relevance rating, full-text evidence matrix, HTML reference star map, APA-style review writing, sentence/paragraph-to-source alignment, and simulated Chinese/English submission review. 这是“新的通用综述工作流”，适用于人格功能损害、健康心理学、临床心理学、发展心理学、心理测量、精神病理学、普通认知心理学等综述主题；不要用于实证数据分析、认知神经科学专用实验设计、伪造文献、绕过付费墙、无人值守批量下载、真实投稿提交，或脱离证据矩阵的自由写作。
---

# Psychology Literature Review Workflow / 新的通用综述工作流

本 skill 是三个主工作流之一，定位为**通用心理学文献综述写作工作流**。它用于把一个宽泛研究方向推进为可聚焦、可检索、可审计、可写作、可模拟投稿的综述项目。默认服务心理学、健康心理学、临床心理学、发展心理学、精神病理学、心理测量、心理干预、普通认知心理学等方向。当前可用于“人格功能损害（impairment in personality functioning）”等主题，但不能写死为某一个主题。

默认语言为中文，必要英文保留于数据库检索式、英文题名、量表名、理论名、变量名、DOI/PMID、APA 引文、参考文献表和必要术语。

## 1. 与另外两个主 skill 的边界

当前三个主 skill 为：

1. `psychology-research-pipeline`：心理学实证论文工作流。
2. `psych-cog-neuro-review`：认知神经科学工作流。
3. `psych-literature-review-workflow`：新的通用综述工作流。

边界规则：

- 若用户目标是**写一篇综述**，且不以神经/生理指标、实验范式或脑机制为核心，使用本 skill。
- 若用户目标是**完成含数据或实验的心理学实证论文**，使用 `psychology-research-pipeline`。
- 若综述主题明显涉及 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合，可使用 `psych-cog-neuro-review`，或由本 skill 调用其认知神经科学专用模块。
- `psych-review-workflow` 若仍存在，仅作为旧版辅助/历史兼容材料，不作为三个主 skill 之一。

## 2. 适用场景

使用本 skill，当用户提出以下任务之一：

- 只给出一个宽研究方向，需要先检索综述、方法学文章和核心理论文章，帮助用户聚焦综述方向。
- 已经给出聚焦后的综述主题，需要进入正式文献检索、Zotero 入库、全文阅读、证据矩阵和综述写作。
- 需要制作中文为主、APA 第 7 版兼容的心理学综述稿。
- 需要输出导师汇报版简表、CSV/Excel/Markdown 阅读矩阵、HTML 文献星图、正文—参考文献精确对齐表，以及模拟投稿审稿意见。

不要使用本 skill，当任务只是：

- 临时解释一个概念、润色单个段落、写邮件或做普通摘要。
- 用户要求凭空补文献、伪造页码、伪造 DOI、伪造审稿意见或伪造投稿结果。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制、出版社限制或使用盗版 PDF 来源。
- 用户要求真实提交投稿系统、代替作者联系编辑、支付版面费或执行真实投稿动作。
- 用户要求处理实证数据、跑统计模型或写实证论文结果，这类任务应转入 `psychology-research-pipeline`。

## 3. 默认综述类型与运行模式

默认运行方式为：**半系统化叙述综述 / 整合型综述**。

可根据用户要求切换为：

- narrative review / 叙述性综述
- theoretical review / 理论综述
- scoping review / 范围综述
- systematic review / 系统综述
- methodological review / 方法学综述
- measurement review / 测量工具综述
- meta-analysis-prep review / 元分析预备综述

不要在没有正式协议、完整检索日志、纳排标准、筛查记录和偏倚风险评价时，把文章声称为“系统综述”。如果只是吸收 PRISMA 的透明性原则，应写作“半系统化叙述综述”或“透明化叙述综述”。

运行模式：

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 早期选题、课程综述、快速方向判断 | 阶段 00、01、02 简化版，阶段 04–06 可抽样完成 | 聚焦建议、初步文献表、简版框架 |
| `standard` | 研究生综述、学位论文综述、中文期刊预备稿 | 阶段 00–11 全流程；单人筛查可接受但需声明 | 完整矩阵、正文草稿、引用对齐、模拟审稿 |
| `strict` | 范围综述、系统综述、英文投稿预备稿、高风险引用核查 | 正式协议、完整检索日志、严格纳排、质量评价、完整对齐 | 可审计检索链、PRISMA 风格追踪、严格审计报告 |

## 4. 总原则

1. **先探索聚焦，再正式综述**：主题未聚焦时，不直接大规模下载全文。先用高质量综述、方法学文章、理论文章帮助用户确定边界。
2. **证据先于写作**：正式写作必须来自题录、全文、阅读卡、证据矩阵和来源位置，不得先写后找文献硬配。
3. **广覆盖但有停止规则**：正式检索应尽可能完整覆盖主题，直到新增文献不能再提供新的理论、方法、测量、人群、关键发现、争议或高质量证据。这里的停止不是数学意义上的穷尽，而是综述写作价值饱和。
4. **分类阅读**：先分类，再评级，再阅读全文；不要把所有文献平铺成普通参考文献表。
5. **相关度与质量分开**：1–4 级表示与主题贴合度，不等于方法质量。方法质量另行评价。
6. **正文写作时同步引文对齐**：不要等写完后才补引用。每个事实性、定义性、理论性、方法性或结论性主张在写作时就绑定来源。
7. **模拟审稿必须标注模拟性质**：不能让用户误以为是真实期刊反馈。
8. **中文优先，英文溯源**：说明、判断标准、矩阵、审稿意见默认中文；检索、题录和 APA 信息保持英文准确。

## 5. 启动时的需求沟通

首次运行时先简短询问，除非用户已经给出答案。用户未回答时，可以使用默认值继续，但必须在 `logs/decisions.md` 中记录为 `assumption`。

必要问题：

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 目标综述类型：叙述综述、理论综述、范围综述、系统综述、方法学综述、测量综述，还是默认半系统化叙述综述？
3. 运行模式：`lite`、`standard`、`strict`，默认 `standard`。
4. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿？
5. 核心边界：核心构念、目标人群、年龄段、临床/非临床、研究设计、是否纳入干预、是否纳入神经机制。
6. 文献获取方式：是否允许 Codex 使用 Chrome + Zotero Connector；Zotero 目标 collection 名称；若失败是否下载到文件夹由用户手动导入。
7. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 6. 默认数据库范围

默认数据库：

- PubMed
- PsycINFO
- Web of Science
- Crossref
- Google Scholar（辅助检索，不单独声称完整）
- CNKI
- 期刊官网
- Zotero 本地库

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求或项目需要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 7. 默认运行目录

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

## 8. 阶段总览

| 阶段 | 名称 | 目标 | 主要产物 |
|---|---|---|---|
| 00 | 宽方向探索 | 从宽方向中识别可写综述方向 | `scoping_brief.md`, `seed_reviews.csv`, `seed_methods.csv`, `focus_options.md`, `导师汇报版简表.md` |
| 01 | 聚焦与协议冻结 | 把聚焦主题转为可执行综述协议 | `review_protocol.md`, `concept_map.md`, `inclusion_exclusion.md` |
| 02 | 正式大范围检索 | 饱和式搜集符合主题的文献 | `queries.md`, `search_log.csv`, `candidate_records.csv` |
| 03 | Zotero/全文获取 | Chrome + Zotero Connector 入库，备选为文件夹手动导入 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与初筛 | 分类文献并给出 1–4 级主题符合程度 | `classification.csv`, `relevance_ratings.csv`, `screening_log.csv` |
| 05 | 全文阅读矩阵 | 深读全文并建立证据矩阵 | `literature_matrix.csv`, `literature_matrix.xlsx`, `literature_matrix.md`, `quality_appraisal.csv` |
| 06 | 证据综合 | 汇总理论、方法、发现、矛盾和空白 | `claim_evidence_map.csv`, `contradictions.md`, `gap_register.md` |
| 07 | HTML 文献星图 | 基于激活扩散模型建立参考文献网络 | `reference_star_map.html`, `star_map_data.json`, `weighting_notes.md` |
| 08 | 写作架构 | 设计综述板块和论证链 | `section_plan.md`, `argument_map.md`, `citation_plan.csv` |
| 09 | APA 综述正文 | 写作中文为主、APA 7 兼容的综述稿 | `manuscript.md`, `manuscript.docx`, `references.bib`, `apa_references.md` |
| 10 | 原文—引用对齐 | 精确核查正文与参考文献来源 | `source_alignment_table.csv`, `source_alignment_table.xlsx`, `claim_audit.md` |
| 11 | 模拟投稿审稿 | 模拟中文/英文期刊投稿前审查 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

## 9. 阶段 00：宽方向探索

当用户只给出研究方向时，先做探索式检索。目标不是完整下载，而是帮助用户聚焦。

优先搜集：最近 5–10 年综述、系统综述、范围综述、元分析；经典理论文章、概念界定文章、共识/指南；研究方法类文章、测量工具文章、量表验证文章；近 3 年高相关实证文章。

输出 `focus_options.md`，每个候选方向包括：中文题目、英文题目、核心研究问题、适合综述类型、文献基础、章节雏形、写作优势、写作风险、与用户研究方向的贴合度、是否建议继续。

同时输出导师汇报版简表：

```csv
候选方向,核心问题,文献基础,创新点,风险,推荐等级,下一步建议
```

聚焦方向确认前，不进入正式大范围下载或 Zotero 批量入库。

## 10. 阶段 01：聚焦与协议冻结

协议至少包括：暂定题目、综述类型及理由、研究问题、核心构念定义、同义词、英文缩写、中文译名、量表名、纳入标准、排除标准、检索数据库、Zotero collection、文件夹备选方案、计划输出、质量评价工具、停止规则和修订规则。

协议冻结后才能进入正式检索。后续若修改范围，必须记录 amendment：修改内容、原因、影响哪些阶段。

## 11. 阶段 02：正式大范围检索

执行步骤：

1. 为每个核心概念建立英文、中文、缩写、量表名、诊断术语、相关理论名。
2. 生成宽检索式和窄检索式。不同数据库使用不同语法，不要把一个检索式复制到所有平台。
3. 每个数据库记录：平台、日期、检索式、过滤器、结果数、导出文件、备注。
4. 导出题录并统一字段：DOI、PMID、title、authors、year、journal、abstract、keywords、URL、database、query_id。
5. 去重顺序：DOI → PMID → 标准化标题 + 第一作者 + 年份。保留每条记录的 provenance。
6. 对核心 seed papers 做 backward citation chasing 和 forward citation chasing。
7. 用新增价值停止规则判断是否继续。

严禁把 Google Scholar、ResearchGate 或任意网页结果说成“完整检索”。

## 12. 阶段 03：Chrome + Zotero / 文件夹备选获取

优先方案：Codex 使用 Chrome 中用户已登录的合法学术访问环境，调用 Zotero Connector 将文献导入本地 Zotero 的指定 collection。

边界：用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认、数据库授权；Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据；不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制；不使用盗版论文站、影子图书馆、PDF bot 或泄露账号；不无人值守高速批量下载；不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

每篇文献必须验证：题名、作者、年份、DOI/PMID、Zotero parent item、附件 key、PDF 是否可读、首页题名是否匹配、页数是否合理。

## 13. 阶段 04：分类、初筛与 1–4 级相关性

先分类，再决定阅读深度。至少分类为：系统综述/元分析、范围综述、叙述/理论综述、理论概念、方法测量、横断实证、纵向实证、实验研究、干预研究、质性/混合方法、评论/共识/指南。

相关性等级：

| 等级 | 名称 | 判定标准 | 阅读处理 |
|---|---|---|---|
| 4 | 核心文献 | 直接对应综述核心构念、目标人群/情境和关键理论、测量、方法或结果；若不引用会明显削弱综述 | 全文精读，进入矩阵和星图核心层 |
| 3 | 重要相关 | 至少直接支持一个核心板块，如概念界定、机制、测量、方法或主要实证证据 | 阅读摘要、方法、结果、讨论；必要时全文精读 |
| 2 | 背景相关 | 与主题有交集，但人群、变量、方法或理论边界不完全匹配 | 摘要和关键段落阅读 |
| 1 | 边缘相关 | 只提供一般背景、相邻概念或排除理由 | 记录后通常不纳入正文核心引用 |

同时评分：方法质量、样本适配度、理论贡献、证据强度、引用价值、与其他文献连接度。

## 14. 阶段 05：全文阅读矩阵

输出 CSV、Excel、Markdown 三种格式。核心字段：

```csv
stable_id,文献类型,相关性等级,方法质量,样本适配度,理论贡献,证据强度,引用价值,核心构念,人群/样本,研究设计,测量/任务,统计方法,主要发现,局限,可引用位置,适合写入章节,是否需要复核
```

短摘录只保留必要证据，不大量复制原文。

## 15. 阶段 06–07：综合与 HTML 星图

证据综合必须区分：定义性证据、理论性证据、方法性证据、实证发现、反证/矛盾、局限、未来方向。

HTML 文献星图基于激活扩散模型：

- 节点：文献、理论、构念、变量、方法、测量工具、核心结论。
- 边：引用关系、共同概念、变量路径、方法相似性、证据支持/冲突。
- 权重：主题贴合度 × 方法质量 × 证据强度 × 连接度 × 新近性/经典性。
- 输出：`reference_star_map.html`、`star_map_data.json`、`weighting_notes.md`。

星图用于辅助理解，不替代全文阅读和质量评价。

## 16. 阶段 08–09：写作架构与 APA 综述正文

默认板块：引言与问题提出；概念界定与术语边界；理论模型与发展脉络；测量工具与操作化；主要实证发现；方法学评价；争议与不一致结果；整合性理论框架；研究空白与未来方向；结论。

正文默认中文写作，兼容 APA 第 7 版。每个实质性主张写作时同步绑定来源。不要写完后硬补引用。

## 17. 阶段 10：原文—引用对齐

必须输出：

```csv
综述页码,综述段落,综述原句,支撑文献,文献页码,文献章节/段落/表图,原文证据短摘录,证据类型,支持强度,是否需要复核
```

标记 direct、partial、unsupported、overextended。对无法定位页码或段落的来源，必须标注需要复核，不能强行通过。

## 18. 阶段 11：模拟投稿与审稿

默认模拟两套：中文心理学核心/相关期刊，以及 SSCI/英文心理学期刊。期刊 scope、格式、版面费、开放获取、AI policy 和投稿要求必须联网核查，不能依赖旧知识。

审稿模块包括：编辑初筛、理论贡献审稿、方法学审稿、文献完整性审稿、APA 格式审稿、引文准确性审稿、修改意见清单、作者回复模板。

模拟反馈必须标注为模拟，不得冒充真实期刊意见。

## 19. 安全边界

- 不伪造文献、DOI、页码、PDF、样本、统计结果、审稿意见或期刊反馈。
- 不绕过数据库权限、验证码、MFA、付费墙、下载限制或出版社条款。
- 不保存账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。
- 不把 Zotero 数据库、PDF、浏览器凭据或受限全文提交到 GitHub。
- 不真实投稿、支付费用或联系编辑，除非用户另行明确授权并在操作时确认。

## 20. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在仍有关键引用、方法、伦理、检索或报告问题时声称“可直接投稿”。
