---
name: psych-review-workflow
description: Use this skill to run a standalone Chinese-first psychology literature-review workflow for general psychology, health psychology, clinical psychology, developmental psychology, psychometrics, and related topics. It supports broad-direction exploration, focused protocol freeze, saturated-but-bounded literature search, Chrome/Zotero Connector ingestion, folder fallback, classification, 1–4 relevance rating, quality appraisal, CSV/Excel/Markdown reading matrices, HTML reference star map, APA 7 manuscript writing, sentence/paragraph-to-source alignment, and simulated Chinese/English journal review. Do not use it to fabricate sources, bypass paywalls, save credentials, run unattended mass downloading, submit real manuscripts, or write prose unsupported by the evidence matrix.
---

# Psychology Review Workflow / 心理学综述写作工作流

本 skill 是一个**独立的通用心理学综述工作流**，不是 `psych-literature-review-workflow` 的路由或精简替代。它主要服务普通心理学、健康心理学、临床心理学、发展心理学、精神病理学、心理测量、干预与应用心理学等综述项目。

默认语言为中文，必要英文保留于数据库检索式、英文题名、量表名、理论名、变量名、DOI/PMID、APA 引文和参考文献表。

当主题明显涉及 EEG/ERP、fMRI、PSG、眼动、神经机制、实验范式或脑区网络时，可以改用或借鉴 `psych-cog-neuro-review`；但本 skill 仍可处理其中的普通心理学综述部分。

## 1. 适用场景

使用本 skill，当用户提出以下任务之一：

- 只给出宽泛研究方向，需要先搜集综述、方法学文章和核心理论文章，帮助聚焦综述方向。
- 已有聚焦后的综述主题，需要进行正式检索、Zotero 入库、分类筛选、阅读全文、矩阵整理和综述写作。
- 需要中文为主、APA 第 7 版兼容的心理学综述稿。
- 需要输出导师汇报版简表、文献阅读矩阵、HTML 文献星图、正文—参考文献对齐表和模拟投稿审稿意见。

不要使用本 skill，当任务只是：

- 临时解释概念、润色单段文字、写邮件或生成普通参考文献列表。
- 用户要求伪造文献、伪造 DOI、伪造页码、伪造审稿意见或伪造投稿结果。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制、出版社条款或使用盗版 PDF 来源。
- 用户要求真实提交投稿系统、支付版面费、联系编辑或执行真实投稿动作。

## 2. 默认综述类型

默认运行方式为：**半系统化叙述综述 / 整合型综述**。

可按用户要求切换为：

- narrative review / 叙述性综述
- theoretical review / 理论综述
- scoping review / 范围综述
- systematic review / 系统综述
- methodological review / 方法学综述
- measurement review / 测量工具综述
- meta-analysis-prep review / 元分析预备综述

不要在没有正式协议、完整检索日志、纳排标准、筛查记录和偏倚风险评价时，把文章声称为“系统综述”。若只是借鉴 PRISMA 的透明性原则，应写作“半系统化叙述综述”或“透明化叙述综述”。

## 3. 运行模式

首次运行时选择一个模式，并写入 `state.json` 与 `logs/decisions.md`。

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 早期选题、课程综述、快速方向判断 | 阶段 00、01、02 简化版，阶段 04–06 可抽样完成 | 聚焦建议、初步文献表、简版框架 |
| `standard` | 研究生综述、学位论文综述、中文期刊预备稿 | 阶段 00–11 全流程；单人筛查可接受但需声明 | 完整矩阵、正文草稿、引用对齐、模拟审稿 |
| `strict` | 范围综述、系统综述、英文投稿预备稿、高风险引用核查 | 正式协议、完整检索日志、严格纳排、质量评价、完整对齐 | 可审计检索链、PRISMA 风格追踪、严格审计报告 |

不要静默降低用户要求的模式。若条件不允许完成 `strict`，必须记录 blocker，并在用户同意或明确说明假设后降级。

## 4. 总原则

1. **先探索聚焦，再正式综述**：主题未聚焦时，不直接大规模下载全文。
2. **证据先于写作**：正式写作必须来自题录、全文、阅读卡、证据矩阵和来源位置。
3. **广覆盖但有停止规则**：正式检索应尽可能覆盖主题，直到新增文献不再提供新的理论、方法、测量、人群、关键发现、争议或高质量证据。这里的停止不是数学意义的穷尽，而是综述写作价值饱和。
4. **分类阅读**：先分类，再评级，再阅读全文；不要把所有文献平铺成普通参考文献表。
5. **相关度与质量分开**：1–4 级表示与主题贴合度，不等于方法质量。方法质量另行评价。
6. **正文写作时同步引文对齐**：不要等写完后才补引用。每个事实性、定义性、理论性、方法性或结论性主张在写作时就绑定来源。
7. **中文优先，英文溯源**：说明、判断标准、矩阵、审稿意见默认中文；检索、题录和 APA 信息保持英文准确。
8. **模拟投稿必须标注模拟性质**：不得把模拟反馈写成真实期刊意见。

## 5. 与仓库其他 skills 的关系

本 skill 保持独立，但可以借鉴或调用仓库中其他能力：

- `psych-literature-review-workflow`：更完整的新总控范式，可作为流程一致性参考。
- `psych-cog-neuro-review`：当综述涉及认知神经科学、脑机制、实验范式、生理指标时参考。
- `psych-zotero-ingest`：用于 Zotero 入库、合法全文获取、PDF 核验和重复项处理。
- `source-alignment` 类子 skill：用于正文—参考文献逐句/逐段对齐。

当不同 skill 的约束冲突时，以用户在当前任务中明确确认的约束为准。若无特别说明，本 skill 的默认数据库范围与运行目录采用下文规定。

## 6. 启动时的需求沟通

首次运行时先简短询问，除非用户已经给出答案。用户未回答时，可以用默认值继续，但必须在 `logs/decisions.md` 中记录为 `assumption`。

必要问题：

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 目标综述类型：叙述综述、理论综述、范围综述、系统综述、方法学综述、测量综述，还是默认半系统化叙述综述？
3. 运行模式：`lite`、`standard`、`strict`，默认 `standard`。
4. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿。
5. 核心边界：构念、人群、年龄段、临床/非临床、研究设计、是否纳入干预、是否纳入神经机制。
6. 文献获取方式：是否允许 Codex 使用 Chrome + Zotero Connector；Zotero 目标 collection 名称；若失败是否下载到文件夹由用户手动导入。
7. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 7. 默认运行目录

默认建立一个运行目录：

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

优先搜集：

- 最近 5–10 年综述、系统综述、范围综述、元分析。
- 经典理论文章、概念界定文章、共识/指南。
- 研究方法类文章、测量工具文章、量表验证文章。
- 近 3 年高相关实证文章，用于判断前沿趋势。

输出 `focus_options.md`，每个候选方向包括：中文题目、英文题目、核心研究问题、适合综述类型、文献基础、章节雏形、写作优势、写作风险、与用户研究方向的贴合度、是否建议继续。

同时输出导师汇报版简表：

```csv
候选方向,核心问题,文献基础,创新点,风险,推荐等级,下一步建议
```

聚焦方向确认前，不进入正式大范围下载或 Zotero 批量入库。

## 10. 阶段 01：聚焦与协议冻结

用户确定聚焦后的综述方向后，进入协议冻结。协议至少包括：

- 暂定题目，中英文各一版。
- 综述类型及理由。
- 研究问题，可使用 PCC、PEO、PICO、SPIDER 或自定义心理学综述框架。
- 核心构念定义、同义词、英文缩写、中文译名、量表名。
- 纳入标准：人群、年龄、样本、研究设计、语言、年份、全文状态、文献类型。
- 排除标准：无关人群、非心理学主题、纯评论、无法定位证据、重复报告等。
- 检索数据库与补充检索。
- Zotero collection 名称和文件夹备选方案。
- 计划输出和目标格式。
- 质量评价工具选择。
- 停止规则和修订规则。

默认数据库范围：

- PubMed
- PsycINFO
- Web of Science
- Crossref
- Google Scholar（辅助检索，不单独声称完整）
- CNKI
- 期刊官网
- Zotero 本地库

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求或项目需要，可作为附加数据库，并在协议中记录理由。

协议冻结后才能进入正式检索。后续若修改范围，必须记录 amendment：修改内容、原因、影响哪些阶段。

## 11. 阶段 02：正式大范围检索

正式检索目标是覆盖主题领域，而不是只拿几篇好写的文章。

执行步骤：

1. 为每个核心概念建立英文、中文、缩写、量表名、诊断术语、相关理论名。
2. 生成宽检索式和窄检索式。不同数据库使用不同语法，不要把一个检索式复制到所有平台。
3. 每个数据库记录：平台、日期、检索式、过滤器、结果数、导出文件、备注。
4. 导出题录并统一字段：DOI、PMID、title、authors、year、journal、abstract、keywords、URL、database、query_id。
5. 去重顺序：DOI → PMID → 标准化标题 + 第一作者 + 年份。保留每条记录的全部来源 provenance。
6. 对核心 seed papers 做 backward citation chasing 和 forward citation chasing。
7. 用新增价值停止规则判断是否继续：连续一轮新增文献不再增加新理论、新量表、新人群、新方法、新关键发现、新争议或新高质量综述；关键综述和高相关实证文章的参考文献已追踪；主要数据库均完成检索并记录局限；仍缺失的证据类型已记录为 gap。

严禁把 Google Scholar、ResearchGate 或任意网页结果说成“完整检索”。

## 12. 阶段 03：Chrome + Zotero / 文件夹备选获取

优先方案：Codex 使用 Chrome 中用户已登录的合法学术访问环境，调用 Zotero Connector 将文献导入本地 Zotero 的指定 collection。

边界：

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认、数据库授权。
- 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。按批次处理，并在异常警告时停止。
- 不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

每篇文献必须验证：题名、作者、年份、DOI/PMID、Zotero parent item、附件 key、PDF 是否可读、首页题名是否匹配、页数是否合理。

备选方案：当 Zotero Connector 不可用或用户希望手动导入时，将合法获取的 PDF、RIS/BibTeX、导入清单保存到用户指定文件夹，由用户手动导入 Zotero。

## 13. 阶段 04：分类、初筛与 1–4 级相关性

先分类，再决定阅读深度。

### 文献类型分类

至少使用以下类型，可多标签：

- `review_systematic`：系统综述/元分析。
- `review_scoping`：范围综述。
- `review_narrative`：叙述综述/理论综述。
- `theory_conceptual`：理论、概念、模型文章。
- `methods_measurement`：方法学、量表、测量、心理计量文章。
- `empirical_cross_sectional`：横断实证研究。
- `empirical_longitudinal`：纵向、队列、追踪研究。
- `empirical_experimental`：实验、任务范式、神经科学研究。
- `intervention_trial`：干预、随机对照、临床试验。
- `qualitative_mixed`：质性或混合方法。
- `commentary_guideline`：评论、共识、指南、立场文件。

### 相关性等级

相关性等级是“对当前综述主题的使用价值”，不是学术质量。

| 等级 | 名称 | 判定标准 | 阅读处理 |
|---|---|---|---|
| 4 | 核心文献 | 直接对应综述核心构念 + 目标人群/情境 + 关键理论、测量、方法或结果；若不引用会明显削弱综述 | 全文精读，进入矩阵和星图核心层 |
| 3 | 重要相关 | 至少直接支持一个核心板块，如概念史、测量、机制、方法、特定人群或争议；与主题略有间接 | 全文重点读，进入矩阵 |
| 2 | 背景/边缘 | 与大领域相关，但人群、构念、方法或结论与主题距离较远；可用于背景、定义或方法参考 | 摘要 + 关键段落阅读，必要时保留 |
| 1 | 弱相关/排除 | 与主题不符、证据位置无法定位、重复、非学术来源、仅标题相似、无可用摘要或全文且不能支持主张 | 记录原因，通常不进入正文引用 |

等级判断必须给出理由，至少包括：主题贴合、人群贴合、方法贴合、证据用途、局限。

除相关性等级外，同时给出辅助评分：

```csv
paper_id,relevance_level,method_quality,sample_fit,theory_contribution,evidence_strength,citation_value,network_connectivity,review_role,decision,reason
```

各辅助评分使用 1–4 分，不能用一个总分替代具体判断。

## 14. 阶段 05：深度阅读与文献矩阵

对 3–4 级文献进行结构化精读。2 级文献只在其确有背景价值时提取。1 级文献不作为正文证据。

### 质量评价原则

按研究设计选择工具，不使用单一“总分”替代判断：

- 系统综述/元分析：PRISMA 报告完整性、AMSTAR 2/JBI 相关条目。
- 范围综述：PRISMA-ScR/JBI 范围综述方法。
- 叙述综述：SANRA 思路，重点看论题重要性、检索透明度、引用支持、科学推理和呈现质量。
- 观察性研究：STROBE/JBI，重点看样本、测量、混杂、缺失、统计模型和外推性。
- 量表/测量研究：COSMIN 思路，重点看结构效度、信度、测量不变性、跨文化适配。
- 随机或干预研究：CONSORT/CONSORT-SPI、干预描述、随机化、盲法、依从性、缺失和不良事件。
- 质性研究：COREQ/CASP，重点看抽样、资料收集、编码、研究者反思、饱和度和可追溯性。
- 神经科学/实验范式：任务效度、刺激控制、样本量、预处理、统计阈值、多重比较和可重复性。

### 文献矩阵推荐字段

输出 CSV、Excel、Markdown 三种格式。使用稳定 ID，优先 DOI；无 DOI 时使用 PMID；再无则使用规范化标题 + 第一作者 + 年份。

```csv
paper_id,study_id,zotero_key,bibtex_key,citation_apa,year,document_type,relevance_level,relevance_reason,method_quality,sample_fit,theory_contribution,evidence_strength,citation_value,network_connectivity,quality_domains,quality_concerns,review_role,constructs,population,age_range,country_or_region,sample_size,design,measures,methods_or_analysis,key_findings,effect_or_result_summary,mechanism_claim,limitations,contradictions,relation_to_topic,usable_for_sections,evidence_location,short_quote,claim_id,notes
```

`evidence_location` 必须尽量精确到页码、章节、段落、表格或图号。`short_quote` 只保留必要短引文；优先用中文转述，保留英文原文片段用于核查。不得大量复制原文。

## 15. 阶段 06：证据综合

综合不是逐篇罗列，而是建立“主张—证据—限制”的结构。

输出至少包括：

- `claim_evidence_map.csv`：每个核心主张对应哪些文献、证据强度、反证、可写位置。
- `contradictions.md`：不同研究结论冲突、原因假设、方法差异。
- `gap_register.md`：概念缺口、测量缺口、样本缺口、设计缺口、机制缺口、实践缺口。
- `methods_lessons.md`：可复用的研究设计、量表、统计方法、任务范式。

标记证据状态：`convergent`、`mixed`、`limited`、`indirect`、`contradictory`、`absent`。`absent` 不得写成已知结论。

## 16. 阶段 07：HTML 文献星图

生成单文件 HTML：

```text
07_star_map/reference_star_map.html
```

目标：帮助用户看到文献网络，而不是只看表格。

节点类型：

- `topic_seed`：用户聚焦后的主题核心。
- `construct`：核心构念、相关构念、理论模型。
- `method`：测量工具、统计模型、实验范式、神经指标。
- `paper_core`：4 级核心文献。
- `paper_important`：3 级重要文献。
- `paper_background`：2 级背景文献。
- `gap`：证据缺口。
- `controversy`：争议或矛盾证据。

边类型：`defines`、`measures`、`tests`、`reviews`、`supports`、`contradicts`、`method_for`、`cites_or_extends`。

默认权重：

```text
paper_weight =
  0.30 * relevance_score +
  0.20 * quality_score +
  0.15 * conceptual_coverage +
  0.15 * citation_network_role +
  0.10 * recency_or_update_value +
  0.10 * writing_utility
```

以 `topic_seed` 为初始激活点，沿边向理论、测量、方法和实证文献扩散。激活随路径长度衰减；支持边和方法边增加相邻节点激活；矛盾边不删除节点，而是标记为争议节点并提高审稿风险提示；多条独立路径到达同一文献时，提高可见度。不要把扩散结果解释为因果关系。

HTML 应包含：搜索框、节点图例、筛选等级、点击节点显示 APA 引文/摘要/证据位置/可用于哪个章节、导出 JSON 的提示。

## 17. 阶段 08：写作架构

写作前先建立章节—证据计划。

默认综述结构，可按主题调整：

1. 标题、摘要、关键词。
2. 引言：问题背景 → 研究重要性 → 现有综述不足 → 本综述目的。
3. 概念界定与理论基础：核心概念、相邻概念、理论模型、历史演变。
4. 测量与操作化：主要工具、维度、信效度、跨文化/年龄适用性、测量争议。
5. 研究现状：按主题、机制、人群或研究设计组织，不逐篇罗列。
6. 方法学评价：样本、设计、测量、统计、实验范式、偏倚来源。
7. 关键机制或整合模型：提出证据支持的整合框架，清楚标注推论层级。
8. 争议与不一致：结论冲突、测量差异、样本差异、文化差异、因果限制。
9. 研究缺口与未来方向：具体到可检验问题、设计建议、变量/测量/样本建议。
10. 结论：保守总结，不夸大实践意义。

若综述主题是“人格功能损害”，默认重点包括：概念与 DSM-5 AMPD/LPFS、OPD 结构轴、STiP-5.1/LoPF-Q 等测量、青少年适用性、自伤/自杀相关证据、情绪调节机制、发展精神病理学视角、临床评估与干预启示。

## 18. 阶段 09：APA 风格综述写作

写作规则：

- 使用 APA 第 7 版作者—年份引文格式。
- 正文每个事实性主张必须连接 `claim_id`。
- 不写没有证据的“研究表明”。
- 不把横断相关写成因果。
- 不把成人样本结论直接外推到青少年。
- 不把临床样本结论直接外推到普通群体。
- 不把一种量表测到的构念当成整个理论构念。
- 中文稿中保留首次出现英文术语和缩写。
- 引文密集段落要合并成论证，不要一篇一段。
- 对争议、空白和方法限制的表述应明确，不用过度确定语气。

产物：

```text
09_manuscript/manuscript.md
09_manuscript/manuscript.docx
09_manuscript/references.bib
09_manuscript/apa_references.md
09_manuscript/tables/
09_manuscript/figures/
```

## 19. 阶段 10：原文—参考文献一一对齐

对齐分两步：写作中实时对齐，写完后全稿审计。

写作中，每段写作前读取 `citation_plan.csv`，每写一个主张就标注 `claim_id`，对应矩阵中的 `paper_id` 和 `evidence_location`。

写完后生成：

```text
10_alignment/source_alignment_table.csv
10_alignment/source_alignment_table.xlsx
10_alignment/claim_audit.md
```

推荐字段：

```csv
alignment_id,manuscript_section,manuscript_page,manuscript_paragraph,manuscript_sentence,claim_text,claim_type,citation_in_text,paper_id,zotero_key,bibtex_key,source_title,source_page,source_section,source_paragraph_or_table,source_evidence_summary,short_quote,evidence_role,alignment_status,risk_note,fix_needed
```

要求：

- `manuscript_page` 在 Markdown 阶段可先用章节和段落号；导出 DOCX/PDF 后再补页码。
- `source_page` 优先用 PDF 页码；若电子文献无页码，使用章节、段落、表图编号。
- `claim_type` 可为：定义、理论、方法、测量、实证结果、争议、研究缺口、推论。
- `alignment_status` 可为：`verified`、`needs_page`、`weak_support`、`overstated`、`missing_source`、`citation_not_used`。
- 任何 `missing_source` 或 `overstated` 必须修改正文或删除主张。
- 参考文献表只保留正文实际引用文献；正文引用必须全部出现在参考文献表。

## 20. 阶段 11：模拟投稿与意见审核

模拟投稿不是实际投稿。若涉及目标期刊 scope、article type、word limit、reference style、open science、AI policy、fees 或伦理要求，必须核查期刊当前官方说明，不得只凭记忆。

步骤：

1. 根据主题、文章类型、语言、方法和篇幅筛选 2–3 个可能期刊。
2. 分别模拟中文心理学核心期刊和 SSCI/英文心理学期刊审稿路径，除非用户只指定一种。
3. 写 `journal_fit_memo.md`：推荐目标、理由、风险、格式差距。
4. 进行模拟编辑初筛：范围、创新性、综述类型匹配、方法透明度、引用完整性、伦理和学术诚信。
5. 分角色模拟审稿：理论/领域专家、方法学与心理测量专家、临床/发展或应用方向专家、写作与 APA 格式审稿、反方审稿人。
6. 输出模拟决定：`minor revision`、`major revision`、`reject and resubmit` 或 `not ready`。不要轻易给 `accept`。
7. 生成 `revision_matrix.csv`：意见、严重度、证据、修改位置、操作、状态。
8. 按证据完成修改，并再次运行引用、格式、方法、逻辑和过度推论审计。

## 21. 失败条件

出现以下情况时，必须停止或降级报告，不能继续声称完成：

- 没有冻结综述主题就开始正式大规模下载。
- 检索式、数据库、日期、结果数无法复现。
- 用摘要代替可获得全文来支持精确主张。
- 文献等级没有理由。
- 质量评价只给总分，没有设计域判断。
- 正文引用与参考文献不一致。
- 主张无法定位到原文页码/章节/段落。
- 将横断、相关、回顾性或小样本结果写成因果结论。
- 对青少年、临床样本、文化差异、测量不变性等问题没有边界说明。
- 使用未授权 PDF、盗版来源、cookie、账号密码或突破访问限制。
- 将模拟审稿意见表述为真实反馈。

## 22. 最终回复格式

每次阶段结束，向用户简洁报告：

```text
完成阶段：
核心产物：
关键发现：
证据缺口：
风险/限制：
下一步建议：
需要用户确认的问题：
```

不要输出冗长过程日志；日志保存在运行目录。用户需要详细日志时再提供。
