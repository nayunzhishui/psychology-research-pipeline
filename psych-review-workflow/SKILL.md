---
name: psych-review-workflow
description: Use this skill to run a reusable psychology literature-review workflow from broad topic exploration to focused review protocol, exhaustive literature collection, Zotero ingestion, screening, evidence matrix, HTML reference star map, APA-style manuscript drafting, source alignment, and simulated submission review. 适用于心理学、健康心理学、临床心理学、认知神经科学等方向的中文主导综述写作；可用于“人格功能损害”等具体主题，也可迁移到其他综述主题。不要用于伪造文献、绕过付费墙、无人值守批量下载、真实投稿提交或脱离证据矩阵的自由写作。
---

# Psychology Review Workflow / 心理学综述写作工作流

本 skill 用于把一个初始研究方向推进为可投稿或可作为学位论文基础的综述稿。默认语言以中文为主，保留必要英文术语、数据库检索式、APA 引文和英文题录字段。

它不是单纯“帮我写一篇综述”的写作器，而是一个可审计的综述研究流程：先帮用户聚焦选题，再系统搜集、筛查、阅读、建矩阵、建文献星图，最后基于证据写作、对齐引用并模拟投稿审稿。

## 适用场景

使用本 skill，当用户提出以下任务之一：

- 给出一个较宽研究方向，希望先通过综述和方法文献来聚焦选题。
- 已有聚焦后的综述主题，希望进行正式文献检索、Zotero 入库、阅读矩阵和综述写作。
- 需要为心理学、健康心理学、临床心理学、认知神经科学、发展心理学、精神病理学等方向建立可复用综述管道。
- 需要输出 APA 风格综述稿、参考文献、文献阅读矩阵、证据—主张对齐表、HTML 文献星图和模拟审稿意见。

不要使用本 skill，当任务只是：

- 修改单个段落、润色一封邮件、临时解释一个概念。
- 用户只需要一张普通参考文献表，不需要流程化检索和证据审计。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制或使用盗版 PDF 来源。
- 用户要求真实投稿、代替作者提交系统、支付版面费、联系编辑或伪造审稿意见。

## 基本原则

1. **先聚焦，再正式综述**：不要在主题尚模糊时直接大规模下载全文。先通过探索式检索帮助用户确定边界。
2. **证据优先于写作**：正式写作只能来自已验证的题录、全文、阅读矩阵和证据位置。
3. **中文理解，英文溯源**：解释、阶段报告和写作建议以中文为主；检索式、题录、DOI、英文量表名、APA 引文保持英文准确性。
4. **广覆盖但有停止规则**：正式检索要尽可能覆盖主题领域，但不能无限抓取。停止条件必须基于新增文献是否继续提供新的理论、方法、测量、样本、结论或矛盾证据。
5. **分类阅读而不是堆文献**：先按综述类、理论类、方法/测量类、实证类、干预类、元分析/系统综述类等分类，再分层阅读。
6. **等级判断不等于质量评分**：相关性等级 1–4 只表示与当前综述主题的贴合度；方法质量需要另按研究设计评价。
7. **不伪造引用**：正文中每一个事实性、定义性、理论性、方法性或结论性主张，都必须能回到具体文献、页码、章节/段落或表图。
8. **模拟投稿必须明确标注**：所有编辑意见、审稿意见和决策均为模拟，不得表述为真实期刊反馈。

## 与现有 psych-* skills 的关系

若仓库中已有以下技能，可以复用其阶段能力，但本 skill 对综述任务保留总控责任：

- `$psych-evidence-search`：正式检索、检索日志、候选题录。
- `$psych-zotero-ingest`：Zotero 入库、合法全文获取、附件核验。
- `$psych-literature-screen`：筛查、质量评价、阅读卡、证据矩阵。
- `$psych-mini-review`：简短证据综合与 claim-evidence map。
- `$psych-manuscript-write`：手稿写作、引用核查、APA 风格修订。
- `$psych-submission-review`：投稿适配、模拟审稿、修改矩阵。

当这些技能不足以覆盖“探索聚焦”“HTML 文献星图”“逐句引用对齐”等任务时，由本 skill 自行执行并保存对应产物。

## 启动时先问用户的关键问题

首次运行时，先用简洁中文询问，除非用户已经给出答案。用户没有完全回答时，可以用默认值继续，但必须记录为 `assumption`。

1. 综述类型：叙述综述、范围综述、系统综述、方法学综述、理论综述、整合综述，还是先不确定？
2. 当前阶段：只是一个宽研究方向，还是已经有聚焦后的综述题目？
3. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿？
4. 主题边界：核心构念、目标人群、年龄段、临床/非临床样本、研究设计、是否包含干预或神经机制。
5. 检索范围：年份、语言、数据库、是否纳入中文文献、是否需要灰色文献。
6. 文献获取：Zotero 目标 collection 名称；是否允许使用 Chrome + Zotero Connector；没有权限时是否改为下载到指定文件夹后手动导入。
7. 输出格式：Markdown、DOCX、HTML、CSV、BibTeX、APA 7 参考文献、投稿模拟报告。
8. 写作约束：字数、中文/英文比例、目标期刊或学校格式、是否要求低 AI 痕迹、是否有不可使用的理论或技术。

## 总体阶段

默认建立一个运行目录：

```text
review_runs/<YYYYMMDD>_<short_topic>/
```

每个阶段追加写入：

```text
state.json
manifest.json
logs/events.jsonl
```

不要覆盖旧文件；修订版使用 `_v2`、`_v3` 或在日志中记录覆盖授权。

| 阶段 | 名称 | 主要产物 |
|---|---|---|
| 00 | 宽方向探索 | `00_exploration/scoping_brief.md`, `seed_reviews.csv`, `seed_methods.csv` |
| 01 | 聚焦与协议冻结 | `01_protocol/review_protocol.md`, `concept_map.md`, `inclusion_exclusion.md` |
| 02 | 正式检索 | `02_search/search_log.csv`, `queries.md`, `candidates.csv` |
| 03 | Zotero/全文获取 | `03_library/zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与初筛 | `04_screening/classification.csv`, `screening_log.csv`, `relevance_ratings.csv` |
| 05 | 深度阅读矩阵 | `05_matrix/evidence_matrix.csv`, `reading_cards/`, `quality_appraisal.csv` |
| 06 | 证据综合 | `06_synthesis/claim_evidence_map.csv`, `contradictions.md`, `gap_register.md` |
| 07 | 文献星图 | `07_star_map/reference_star_map.html`, `star_map_data.json`, `weighting_notes.md` |
| 08 | 写作架构 | `08_outline/section_plan.md`, `argument_map.md`, `citation_plan.csv` |
| 09 | 综述正文 | `09_manuscript/manuscript.md`, `references.bib`, `apa_references.md` |
| 10 | 原文—引用对齐 | `10_alignment/source_alignment_table.csv`, `claim_audit.md` |
| 11 | 模拟投稿与审稿 | `11_submission/journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

## 阶段 00：宽方向探索

用户只给出一个大方向时，先做探索式检索，不进入正式全文下载。

目标：找出该方向的核心概念、研究流派、常用测量、主要争议、代表性综述、代表性方法文章、近年高频主题，并向用户提供 2–5 个可聚焦的综述方向。

执行步骤：

1. 将用户方向拆成概念块：核心构念、相关构念、目标人群、机制、测量、方法、临床/教育/社会背景。
2. 优先搜集：
   - 最近 5–10 年的综述、系统综述、范围综述、元分析。
   - 经典理论文章、共识/指南、测量工具与方法学文章。
   - 近 3 年新兴实证研究，用于判断趋势。
3. 生成候选聚焦方向，每个方向包括：
   - 可能题目；
   - 核心问题；
   - 可写性；
   - 文献量风险；
   - 方法/测量基础；
   - 与用户研究兴趣的贴合度；
   - 不建议写的原因或边界。
4. 与用户确认聚焦方向。如果用户不想反复沟通，选择“文献基础最稳 + 写作风险最低 + 与心理学主题最贴合”的方向继续。

产物：

```text
00_exploration/scoping_brief.md
00_exploration/seed_reviews.csv
00_exploration/seed_methods.csv
00_exploration/focus_options.md
```

## 阶段 01：聚焦与协议冻结

聚焦后的综述方向必须转化为可执行协议。

协议至少包括：

- 暂定题目，中英文各一版。
- 综述类型及理由。
- 研究问题，可使用 PCC、PEO、PICO、SPIDER 或自定义心理学综述框架。
- 核心构念定义、同义词、英文缩写、中文译名、量表名。
- 纳入标准：人群、年龄、样本、研究设计、语言、年份、全文状态、文献类型。
- 排除标准：无关人群、非心理学主题、纯评论、无法定位证据、重复报告等。
- 检索数据库与补充检索：PubMed、PsycINFO、Web of Science、Scopus、OpenAlex、Crossref、Google Scholar、CNKI、万方、SinoMed，以及引文追踪。
- Zotero collection 名称和文件夹备选方案。
- 计划输出和目标格式。
- 质量评价工具选择。
- 停止规则和修订规则。

协议冻结后才能进入正式大范围检索。后续若修改范围，必须记录 amendment：修改内容、原因、影响哪些阶段。

## 阶段 02：正式大范围检索

正式检索目标是覆盖主题领域，而不是只拿几篇好写的文章。

执行步骤：

1. 为每个核心概念建立英文、中文、缩写、量表名、诊断术语、相关理论名。
2. 生成宽检索式和窄检索式。不同数据库使用不同语法，不要把一个检索式复制到所有平台。
3. 每个数据库记录：平台、日期、检索式、过滤器、结果数、导出文件、备注。
4. 导出题录并统一字段：DOI、PMID、title、authors、year、journal、abstract、keywords、URL、database、query_id。
5. 去重顺序：DOI → PMID → 标准化标题 + 第一作者 + 年份。保留每条记录的全部来源 provenance。
6. 对核心 seed papers 做 backward citation chasing 和 forward citation chasing。
7. 用“新增价值停止规则”判断是否继续：
   - 连续一轮新增文献不再增加新理论、新量表、新人群、新方法、新关键发现、新争议或新高质量综述；
   - 关键综述和高相关实证文章的参考文献已追踪；
   - 主要数据库均完成检索并记录局限；
   - 仍缺失的证据类型已明确记录为 gap，而不是继续无限搜索。

严禁把 Google Scholar、ResearchGate 或任意网页结果说成“完整检索”。

## 阶段 03：Chrome + Zotero / 文件夹备选获取

优先方案：Codex 使用 Chrome 中用户已登录的合法学术访问环境，调用 Zotero Connector 将文献导入本地 Zotero 的指定 collection。

边界：

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认、数据库授权。
- 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。按批次处理，并在异常警告时停止。

每篇文献必须验证：题名、作者、年份、DOI/PMID、Zotero parent item、附件 key、PDF 是否可读、首页题名是否匹配、页数是否合理。

备选方案：当 Zotero Connector 不可用或用户希望手动导入时，将合法获取的 PDF、RIS/BibTeX、导入清单保存到用户指定文件夹。不得把 PDF、Zotero 数据库、账号信息提交到 GitHub。

## 阶段 04：分类、初筛与 1–4 级相关性

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

## 阶段 05：深度阅读与文献矩阵

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

使用稳定 ID，优先 DOI；无 DOI 时使用 PMID；再无则使用规范化标题 + 第一作者 + 年份。

```csv
paper_id,study_id,zotero_key,bibtex_key,citation_apa,year,document_type,relevance_level,relevance_reason,quality_domains,quality_concerns,review_role,constructs,population,age_range,country_or_region,sample_size,design,measures,methods_or_analysis,key_findings,effect_or_result_summary,mechanism_claim,limitations,contradictions,relation_to_topic,usable_for_sections,evidence_location,short_quote,claim_id,notes
```

`evidence_location` 必须尽量精确到页码、章节、段落、表格或图号。`short_quote` 只保留必要短引文；优先用中文转述，保留英文原文片段用于核查。

## 阶段 06：证据综合

综合不是逐篇罗列，而是建立“主张—证据—限制”的结构。

输出至少包括：

- `claim_evidence_map.csv`：每个核心主张对应哪些文献、证据强度、反证、可写位置。
- `contradictions.md`：不同研究结论冲突、原因假设、方法差异。
- `gap_register.md`：概念缺口、测量缺口、样本缺口、设计缺口、机制缺口、实践缺口。
- `methods_lessons.md`：可复用的研究设计、量表、统计方法、任务范式。

标记证据状态：

- `convergent`：多篇高相关文献支持。
- `mixed`：方向不一致或依赖样本/测量/方法。
- `limited`：证据少但直接相关。
- `indirect`：间接支持，需要谨慎表述。
- `contradictory`：存在直接反证。
- `absent`：当前没有可靠证据，不得写成已知结论。

## 阶段 07：HTML 文献星图

生成一个单文件 HTML：

```text
07_star_map/reference_star_map.html
```

目标：帮助用户看到文献网络，而不是只看表格。

### 节点类型

- `topic_seed`：用户聚焦后的主题核心。
- `construct`：核心构念、相关构念、理论模型。
- `method`：测量工具、统计模型、实验范式、神经指标。
- `paper_core`：4 级核心文献。
- `paper_important`：3 级重要文献。
- `paper_background`：2 级背景文献。
- `gap`：证据缺口。
- `controversy`：争议或矛盾证据。

### 边类型

- `defines`：定义/概念来源。
- `measures`：测量工具或操作化。
- `tests`：实证检验。
- `reviews`：综述整合。
- `supports`：支持某主张。
- `contradicts`：反驳或限制某主张。
- `method_for`：提供方法。
- `cites_or_extends`：引文链或理论延伸。

### 权重规则

不得只用引用次数或期刊名决定权重。默认权重：

```text
paper_weight =
  0.30 * relevance_score +
  0.20 * quality_score +
  0.15 * conceptual_coverage +
  0.15 * citation_network_role +
  0.10 * recency_or_update_value +
  0.10 * writing_utility
```

解释：

- `relevance_score`：1–4 级相关性归一化。
- `quality_score`：按设计质量域综合判断，不是简单总分。
- `conceptual_coverage`：是否覆盖定义、机制、测量、人群或争议的关键位置。
- `citation_network_role`：是否为 seed paper、被多篇核心文献引用、连接两个文献群。
- `recency_or_update_value`：近年新证据、方法更新、最新综述；经典理论可手动保留高权重。
- `writing_utility`：是否可直接支持正文关键段落。

### 激活扩散模型思路

以 `topic_seed` 为初始激活点，沿边向理论、测量、方法和实证文献扩散。扩散时：

- 激活随路径长度衰减。
- 支持边和方法边增加相邻节点激活。
- 矛盾边不删除节点，而是标记为争议节点并提高审稿风险提示。
- 多条独立路径到达同一文献时，提高该文献在星图中的可见度。
- 不把扩散结果解释为因果关系；它只是“综述写作中的证据连接强度”。

HTML 应包含：搜索框、节点图例、筛选等级、点击节点显示 APA 引文/摘要/证据位置/可用于哪个章节、导出 JSON 的提示。

## 阶段 08：写作架构

写作前先建立章节—证据计划。

默认综述结构，可按主题调整：

1. 标题、摘要、关键词。
2. 引言：问题背景 → 研究重要性 → 现有综述不足 → 本综述目的。
3. 概念界定与理论基础：核心概念、相邻概念、理论模型、历史演变。
4. 测量与操作化：主要工具、维度、信效度、跨文化/年龄适用性、测量争议。
5. 研究现状：按主题、机制、人群或研究设计组织，不逐篇罗列。
6. 方法学评价：样本、设计、测量、统计、神经/实验范式、偏倚来源。
7. 关键机制或整合模型：提出证据支持的整合框架，清楚标注推论层级。
8. 争议与不一致：结论冲突、测量差异、样本差异、文化差异、因果限制。
9. 研究缺口与未来方向：具体到可检验问题、设计建议、变量/测量/样本建议。
10. 结论：保守总结，不夸大实践意义。

若综述主题是“人格功能损害”，默认重点包括：概念与 DSM-5 AMPD/LPFS、OPD 结构轴、STiP-5.1/LoPF-Q 等测量、青少年适用性、自伤/自杀相关证据、情绪调节机制、发展精神病理学视角、临床评估与干预启示。

## 阶段 09：APA 风格综述写作

写作规则：

- 使用 APA 7 作者—年份引文格式。
- 正文每个事实性主张必须连接 `claim_id`。
- 不写没有证据的“研究表明”。
- 不把横断相关写成因果。
- 不把成人样本结论直接外推到青少年。
- 不把临床样本结论直接外推到普通群体。
- 不把一种量表测到的构念当成整个理论构念。
- 中文稿中保留首次出现英文术语和缩写：如 人格功能水平（Level of Personality Functioning, LPF）。
- 引文密集段落要合并成论证，不要一篇一段。
- 对争议、空白和方法限制的表述应明确，不用过度确定语气。

产物：

```text
09_manuscript/manuscript.md
09_manuscript/references.bib
09_manuscript/apa_references.md
09_manuscript/tables/
09_manuscript/figures/
```

## 阶段 10：原文—参考文献一一对齐

对齐分两步：写作中实时对齐，写完后全稿审计。

### 写作中实时对齐

每段写作前读取 `citation_plan.csv`，每写一个主张就标注 `claim_id`，对应矩阵中的 `paper_id` 和 `evidence_location`。

### 写完后输出对齐表

生成：

```text
10_alignment/source_alignment_table.csv
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

## 阶段 11：模拟投稿与意见审核

模拟投稿不是实际投稿。

步骤：

1. 根据主题、文章类型、语言、方法和篇幅筛选 2–3 个可能期刊。
2. 核查期刊当前 scope、article type、word limit、reference style、open science、AI policy、fees、伦理要求。
3. 写 `journal_fit_memo.md`：推荐目标、理由、风险、格式差距。
4. 进行模拟编辑初筛：范围、创新性、综述类型匹配、方法透明度、引用完整性、伦理和学术诚信。
5. 分角色模拟审稿：
   - 理论/领域专家；
   - 方法学与心理测量专家；
   - 临床/发展或认知神经方向专家；
   - 写作与 APA 格式审稿；
   - 反方审稿人，专门寻找最强拒稿理由。
6. 输出模拟决定：`minor revision`、`major revision`、`reject and resubmit` 或 `not ready`。不要轻易给 `accept`。
7. 生成 `revision_matrix.csv`：意见、严重度、证据、修改位置、操作、状态。
8. 按证据完成修改，并再次运行引用、格式、方法、逻辑和过度推论审计。

## 失败条件

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

## 最终回复格式

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
