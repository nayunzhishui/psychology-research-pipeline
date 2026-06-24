---
name: psych-cog-neuro-review
description: Use this standalone Chinese-first skill for psychology and cognitive-neuroscience literature reviews involving mechanisms, experimental paradigms, behavioral-neural integration, EEG/ERP, fMRI, PSG, sleep, emotion, memory, cognitive control, threat/reward processing, and related methods. It supports broad-direction exploration, focused protocol freeze, bilingual search, Chrome/Zotero Connector ingestion, folder fallback, screening, 1–4 relevance rating, cognitive-neuroscience evidence extraction, quality appraisal, CSV/Excel/Markdown matrices, HTML reference star map, APA 7 manuscript drafting, source alignment, and simulated Chinese/English journal review. Do not use it to fabricate sources, bypass access restrictions, save credentials, automate unauthorized downloads, or write unsupported neural-mechanism claims.
---

# Cognitive Neuroscience Psychology Review / 认知神经科学心理学综述

本 skill 是一个**独立的认知神经科学/脑机制综述增强工作流**，不是普通综述 skill 的路由。它适用于心理学与认知神经科学交叉主题，尤其是包含实验范式、生理/神经指标、行为—神经机制整合、发展或临床神经机制的综述。

默认语言为中文，必要英文保留于实验范式、脑区、神经网络、统计指标、数据库检索式、题录、APA 引文和参考文献。

## 1. 适用场景

使用本 skill，当综述主题涉及以下至少一类内容：

- EEG/ERP、fMRI、PSG、眼动、皮电、心率变异性或其他生理/神经指标。
- 认知控制、情绪加工、记忆、注意、威胁/奖赏加工、睡眠与情绪、发展认知神经科学。
- 实验范式：Go/No-Go、n-back、IAT/GNAT、情绪图片记忆、恐惧条件化、消退、再巩固、睡眠实验、nap protocol 等。
- 需要把行为结果、神经指标、理论机制和心理学变量整合进同一综述。

不要使用本 skill，当任务只是：

- 普通心理学综述，不涉及机制、实验或神经/生理指标。
- 仅需要解释单个概念、润色单段文字或整理普通参考文献。
- 用户要求伪造文献、伪造 DOI、伪造页码、伪造神经机制证据或伪造审稿意见。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制、出版社条款或使用盗版 PDF 来源。
- 用户要求真实投稿、支付版面费、联系编辑或执行真实投稿动作。

## 2. 默认定位

- 默认综述类型：`mixed mechanism review` / 混合型机制综述。
- 默认运行模式：`standard`。
- 默认输出风格：中文核心期刊综述草稿 + 英文 Q1 review 结构兼容。
- 默认 topic pack：无。只有当主题涉及 REM sleep、emotional memory、fear conditioning、extinction、memory consolidation、reconsolidation、dream affect、PSG 或 sleep-dependent affective processing 时，才加载 `topic_packs/rem_emotional_memory/`。
- Zotero 默认使用 Chrome + Zotero Connector；失败时使用文件夹备选方案，由用户手动导入。

如果用户明确要求系统综述、范围综述或元分析预备综述，需要升级协议、检索日志、纳排记录和质量评价强度；不能仅因主题较窄就自动声称系统综述。

## 3. 运行模式

读取或参考 `templates/run_mode_policy.md`。选择一个模式并写入 `state.json`、`00_exploration/review_scope.md` 或 `01_protocol/review_protocol.md`。

| Mode | Use case | Required minimum | Typical output |
|---|---|---|---|
| `lite` | 快速机制综述、课程论文、早期选题、初步文献图谱 | 00、01 简化版、02 检索草图、04 初筛、05 抽样矩阵、06 初步综合 | scope, seed papers, initial matrix, outline |
| `standard` | 研究生综述、中文核心预备稿、普通机制综述 | 00–11 全流程；单人筛查可接受但需说明；Zotero collection verification expected when available | full auditable review run, matrix, star map, Word draft, source alignment |
| `strict` | 系统综述、范围综述、外文 Q1 review 预备稿、高风险引用核查 | 正式协议、完整检索日志、严格筛查、质量评价、Zotero/PDF acquisition manifest、完整对齐 | PRISMA-style traceability, formal quality tools, complete audit |

不要静默降低用户要求的模式。若 access、时间或工具限制导致 `strict` 不可完成，记录 blocker，并在用户确认或明确说明假设后降级。

## 4. 语言与写作政策

- 工作流说明、检索记录、阅读矩阵、证据综合、写作建议、审稿意见优先使用中文。
- 文献题名、量表名、实验范式、脑区、神经网络、统计指标、数据库字段保留英文原文。
- 首次出现的重要术语使用“中文解释 + English term”，例如“事件相关电位（event-related potentials, ERP）”。
- 正文默认先产出中文综述草稿；如用户指定，可追加英文 Q1 review preparatory draft。
- 避免机械翻译神经科学术语；优先使用本领域通行表达。

## 5. 启动时的需求沟通

首次运行时先询问，除非用户已经给出答案。用户未完全回答时，可用默认值继续，但必须记录为 `assumption`。

必要问题：

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 综述类型：混合型机制综述、叙述综述、理论综述、范围综述、系统综述、测量综述、元分析预备综述。
3. 运行模式：`lite`、`standard`、`strict`，默认 `standard`。
4. 目标用途：课程作业、开题、学位论文综述、中文核心期刊、英文 Q1 review、投稿预备稿。
5. 核心边界：构念、人群、年龄段、临床/非临床、human/animal/computational、实验范式、神经/生理指标。
6. 是否纳入 REM/sleep 证据，是否加载 REM/emotional memory topic pack。
7. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero 目标 collection 名称；失败时是否下载到文件夹由用户手动导入。
8. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 6. 默认数据库范围

默认数据库与通用综述 workflow 保持一致：

- PubMed
- PsycINFO
- Web of Science
- Crossref
- Google Scholar（辅助检索，不单独声称完整）
- CNKI
- 期刊官网
- Zotero 本地库

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求或某一认知神经科学主题确有必要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 7. 运行目录

默认建立一个运行目录：

```text
review_runs/<YYYYMMDD>_<short_topic>_cog_neuro/
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
│   └── reading_cards/
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
| 00 | 宽方向探索 | 从认知神经科学方向中识别可写综述方向 | `scoping_brief.md`, `seed_reviews.csv`, `seed_methods.csv`, `focus_options.md`, `导师汇报版简表.md` |
| 01 | 聚焦与协议冻结 | 把聚焦主题转为机制综述协议 | `review_protocol.md`, `concept_map.md`, `mechanism_scope.md`, `inclusion_exclusion.md` |
| 02 | 正式检索 | 建立双语概念块和数据库检索日志 | `queries.md`, `database_search_log.csv`, `candidate_records.csv` |
| 03 | Zotero/全文获取 | 合法入库、去重、PDF 核验 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与筛查 | 分类文献并给出 1–4 级相关性 | `classification.csv`, `screening_table.csv`, `relevance_ratings.csv` |
| 05 | 矩阵与质量评价 | 提取普通文献矩阵和神经机制矩阵 | `literature_matrix.csv/xlsx/md`, `neural_mechanism_matrix.csv/xlsx/md`, `quality_appraisal.csv` |
| 06 | 证据综合 | 形成机制链、矛盾、空白和 claim-evidence map | `claim_evidence_map.csv`, `mechanism_synthesis.md`, `evidence_gap_register.csv` |
| 07 | HTML 文献星图 | 基于激活扩散模型建立文献—构念—机制网络 | `reference_star_map.html`, `star_map_data.json`, `weighting_notes.md` |
| 08 | 写作架构 | 冻结章节、论证路径、图表和允许主张 | `section_argument_plan.md`, `review_outline.md`, `citation_plan.csv` |
| 09 | 正文写作 | 写作 APA 7 兼容的中文综述稿 | `review_draft.md`, `review_draft.docx`, `references.bib`, `apa_references.md` |
| 10 | 来源对齐 | 段落/句子—原文来源核查 | `source_alignment_table.csv/xlsx`, `claim_audit.md`, `unsupported_or_overstated_claims.md` |
| 11 | 模拟投稿审稿 | 模拟中文/英文期刊投稿前审查 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

不要随意重排阶段。若某一阶段失败，在同阶段修复；只有记录原因和影响范围后，才回到前一阶段。

## 9. 阶段 00：宽方向探索

用户只给出宽方向时，先做探索式检索，不进入正式全文下载。

目标：找出核心概念、研究流派、实验范式、常用测量、神经/生理指标、主要争议、代表性综述、代表性方法文章和近年前沿趋势，并向用户提供 2–5 个可聚焦方向。

优先搜集：

- 最近 5–10 年综述、系统综述、范围综述、元分析。
- 经典理论文章、概念界定文章、共识/指南。
- 方法学文章：实验范式、EEG/ERP、fMRI、PSG、眼动、心理测量、统计方法。
- 近 3 年高相关实证研究，用于判断前沿趋势。

每个候选方向必须包括：中文题目、英文题目、核心研究问题、机制链雏形、适合综述类型、文献基础、数据/方法风险、可能章节结构、与用户方向贴合度、是否建议继续。

输出导师汇报版简表：

```csv
候选方向,核心问题,机制链,文献基础,方法基础,创新点,风险,推荐等级,下一步建议
```

聚焦方向确认前，不进入正式大范围下载或 Zotero 批量入库。

## 10. 阶段 01：聚焦与协议冻结

聚焦后的综述方向必须转化为可执行协议。协议至少包括：

- 暂定题目，中英文各一版。
- 综述类型及理由。
- 研究问题，可使用 PCC、PEO、PICO、SPIDER 或自定义机制综述框架。
- 核心构念、相邻构念、英文缩写、中文译名、量表名、实验范式。
- 机制边界：认知过程、情绪过程、发展阶段、临床状态、脑区/网络、时间窗口。
- 纳入标准：人群、年龄、样本、研究设计、语言、年份、全文状态、文献类型。
- 排除标准：无关人群、非心理学主题、纯评论、无法定位证据、重复报告、神经指标不可解释等。
- 数据库范围、检索式策略和引文追踪计划。
- Zotero collection 名称和文件夹备选方案。
- 质量评价工具选择。
- 停止规则、修订规则和 AI 使用边界。

协议冻结后才能进入正式检索。后续若修改范围，必须记录 amendment：修改内容、原因、影响哪些阶段。

## 11. 阶段 02：正式检索

构建双语概念块和数据库特异检索式，不要把一个检索式复制到所有平台。

检索日志必须记录：数据库、平台、日期、检索式、过滤器、结果数、导出文件、备注。

检索应包含：

- 核心心理学构念和同义词。
- 实验范式和任务名称。
- 神经/生理指标，如 EEG、ERP、fMRI、PSG、eye tracking、HRV 等。
- 关键脑区、网络或时间成分，如 amygdala、hippocampus、vmPFC、ACC、LPP、P3、theta 等。
- 目标人群和年龄阶段。
- 测量工具、量表名、临床术语。

用新增价值停止规则判断是否继续：新增文献不再提供新的机制链、任务范式、神经指标、样本类型、测量工具、关键发现、矛盾证据或高质量综述时，可以停止并记录为“综述写作价值饱和”。

## 12. 阶段 03：Chrome + Zotero / 文件夹备选获取

优先方案：Codex 使用 Chrome 中用户已登录的合法学术访问环境，调用 Zotero Connector 将文献导入本地 Zotero 的指定 collection。

边界：

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认、数据库授权。
- 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。按批次处理，并在异常警告时停止。
- Zotero 操作只做添加或附件补全；不删除、合并、重命名、移动或覆盖既有记录。
- 不把 PDF、Zotero 数据库、浏览器材料、token、cookie 或账号信息提交到 GitHub。

每篇文献必须验证：题名、作者、年份、DOI/PMID、Zotero parent item、附件 key、PDF 可读性、首页题名匹配、页数合理、是否误下载登录页或 HTML。

备选方案：当 Zotero Connector 不可用或用户希望手动导入时，将合法获取的 PDF、RIS/BibTeX、导入清单保存到用户指定文件夹，由用户手动导入 Zotero。

## 13. 阶段 04：分类、筛查与 1–4 级相关性

先分类，再决定阅读深度。

### 文献类型分类

至少使用以下类型，可多标签：

- `review_systematic`：系统综述/元分析。
- `review_scoping`：范围综述。
- `review_narrative`：叙述综述/理论综述。
- `theory_conceptual`：理论、概念、模型文章。
- `methods_measurement`：方法学、量表、测量、心理计量文章。
- `empirical_behavioral`：行为实证研究。
- `empirical_eeg_erp`：EEG/ERP 研究。
- `empirical_fmri`：fMRI/脑成像研究。
- `empirical_sleep_psg`：睡眠/PSG 研究。
- `empirical_eye_tracking_psychophysiology`：眼动/心理生理研究。
- `intervention_trial`：干预、随机对照、临床试验。
- `animal_computational`：动物或计算模型。
- `qualitative_mixed`：质性或混合方法。
- `commentary_guideline`：评论、共识、指南、立场文件。

### 相关性等级

相关性等级表示“对当前机制综述主题的使用价值”，不是学术质量。

| 等级 | 名称 | 判定标准 | 阅读处理 |
|---|---|---|---|
| 4 | 核心机制文献 | 同时匹配核心构念/人群/机制或关键方法；能直接支撑综述主线、机制图或关键章节 | 全文精读，进入矩阵和星图核心层 |
| 3 | 重要相关文献 | 直接支持概念、测量、范式、机制链、人群差异或争议之一；与主题略有间接 | 全文重点读，进入矩阵 |
| 2 | 背景/方法参考 | 与大领域相关，但构念、人群、机制或指标距离较远；可用于背景或方法说明 | 摘要 + 关键段落阅读，必要时保留 |
| 1 | 弱相关/排除 | 与主题不符、无法定位证据、重复、非学术来源、仅标题相似、无可用摘要或全文 | 记录原因，通常不进入正文引用 |

等级判断必须给出理由，至少包括：主题贴合、人群贴合、机制贴合、方法/指标贴合、证据用途、局限。

同时给出辅助评分：

```csv
paper_id,relevance_level,method_quality,sample_fit,mechanism_contribution,evidence_strength,citation_value,network_connectivity,review_role,decision,reason
```

各辅助评分使用 1–4 分，不能用一个总分替代具体判断。

## 14. 阶段 05：提取、矩阵与质量评价

对 3–4 级文献进行结构化精读。2 级文献只在其确有背景或方法价值时提取。1 级文献不作为正文证据。

输出 CSV、Excel、Markdown 三种矩阵：

```text
05_matrix/literature_matrix.csv
05_matrix/literature_matrix.xlsx
05_matrix/literature_matrix.md
05_matrix/neural_mechanism_matrix.csv
05_matrix/neural_mechanism_matrix.xlsx
05_matrix/neural_mechanism_matrix.md
05_matrix/quality_appraisal.csv
```

### 通用文献矩阵字段

```csv
paper_id,study_id,zotero_key,bibtex_key,citation_apa,year,document_type,relevance_level,relevance_reason,method_quality,sample_fit,mechanism_contribution,evidence_strength,citation_value,network_connectivity,quality_domains,quality_concerns,review_role,constructs,population,age_range,country_or_region,sample_size,design,measures,methods_or_analysis,key_findings,effect_or_result_summary,limitations,contradictions,relation_to_topic,usable_for_sections,evidence_location,short_quote,claim_id,notes
```

### 认知神经科学机制矩阵字段

```csv
paper_id,paradigm_or_task,stimuli,control_condition,cognitive_process,emotion_process,encoding_consolidation_retrieval_phase,neural_method,neural_indicator,brain_region_or_network,time_window,preprocessing,statistical_threshold,multiple_comparison_correction,behavioral_outcome,neural_outcome,brain_behavior_link,mechanism_claim,causal_status,replicability_concern,evidence_location,claim_id
```

`evidence_location` 必须尽量精确到页码、章节、段落、结果段、表格或图号。`short_quote` 只保留必要短引文；优先中文转述，不得大量复制原文。

### 质量评价原则

按研究设计选择工具，不使用单一总分替代判断：

- 系统综述/元分析：PRISMA 报告完整性、AMSTAR 2/JBI 相关条目。
- 范围综述：PRISMA-ScR/JBI 范围综述方法。
- 叙述/机制综述：SANRA 思路 + 机制链透明度。
- 观察性研究：STROBE/JBI，关注样本、测量、混杂、缺失、统计模型和外推性。
- 量表/测量研究：COSMIN 思路，关注结构效度、信度、测量不变性、跨文化适配。
- 随机或干预研究：CONSORT/CONSORT-SPI。
- EEG/ERP：任务效度、试次数、伪迹处理、基线、成分窗口、ROI、统计阈值、多重比较、可重复性。
- fMRI：预处理、运动控制、ROI/whole-brain、阈值、cluster correction、功能连接、样本量、报告完整性。
- PSG/睡眠：睡眠分期、REM/NREM 指标、睡眠剥夺或 nap 方案、混杂睡眠变量、实验时序。
- 动物/计算模型：species/model boundary、可迁移性、模型假设和人类推断边界。

## 15. 阶段 06：证据综合

综合不是逐篇罗列，而是建立“构念—方法—机制—证据—限制”的结构。

输出至少包括：

- `claim_evidence_map.csv`：每个核心主张对应哪些文献、证据强度、反证、可写位置。
- `mechanism_synthesis.md`：机制链、时间过程、脑区/网络、行为指标与理论解释。
- `contradictions.md`：不同研究结论冲突、原因假设、方法差异。
- `evidence_gap_register.csv`：概念缺口、测量缺口、样本缺口、设计缺口、机制缺口、实践缺口。
- `methods_lessons.md`：可复用的实验设计、量表、统计方法、神经指标。

标记证据状态：`convergent`、`mixed`、`limited`、`indirect`、`contradictory`、`absent`。`absent` 不得写成已知结论。

## 16. 阶段 07：HTML 文献星图

生成单文件 HTML：

```text
07_star_map/reference_star_map.html
```

节点类型：

- `topic_seed`：用户聚焦后的主题核心。
- `construct`：核心构念、相关构念、理论模型。
- `mechanism`：机制链、过程阶段、脑区/网络。
- `method`：测量工具、统计模型、实验范式、神经/生理指标。
- `paper_core`：4 级核心机制文献。
- `paper_important`：3 级重要文献。
- `paper_background`：2 级背景文献。
- `gap`：证据缺口。
- `controversy`：争议或矛盾证据。

边类型：`defines`、`measures`、`tests`、`localizes`、`supports`、`contradicts`、`method_for`、`brain_behavior_links`、`cites_or_extends`。

默认权重：

```text
paper_weight =
  0.25 * relevance_score +
  0.20 * quality_score +
  0.20 * mechanism_specificity +
  0.15 * citation_network_role +
  0.10 * recency_or_update_value +
  0.10 * writing_utility
```

以 `topic_seed` 为初始激活点，沿边向理论、测量、机制、神经指标和实证文献扩散。激活随路径长度衰减；支持边、方法边和 brain-behavior link 增加相邻节点激活；矛盾边不删除节点，而是标记为争议节点并提高审稿风险提示；多条独立路径到达同一文献时，提高可见度。不要把扩散结果解释为因果关系。

HTML 应包含：搜索框、节点图例、筛选等级、方法/指标筛选、点击节点显示 APA 引文/摘要/证据位置/可用于哪个章节、导出 JSON 的提示。

## 17. 阶段 08：写作架构

写作前先冻结章节—证据计划。

默认结构，可按主题调整：

1. 标题、摘要、关键词。
2. 引言：问题背景 → 机制争议 → 现有综述不足 → 本综述目的。
3. 概念界定与理论基础：核心概念、相邻概念、理论模型、发展脉络。
4. 测量与实验范式：量表、任务、刺激、控制条件、信效度、范式争议。
5. 行为证据：反应时、正确率、d′、偏向、记忆成绩、评分指标等。
6. 神经/生理证据：EEG/ERP、fMRI、PSG、眼动或其他指标。
7. 行为—神经机制整合：脑区/网络、时间过程、任务阶段、理论解释。
8. 人群差异与发展/临床边界：年龄、临床状态、文化、药物、样本限制。
9. 方法学评价与不一致结果：样本量、统计阈值、多重比较、任务效度、可重复性。
10. 整合模型与未来方向：具体到可检验机制、实验设计、指标和样本建议。
11. 结论：保守总结，不夸大神经机制或实践意义。

写作前必须生成 `citation_plan.csv`，明确每个章节允许使用哪些 `claim_id`。

## 18. 阶段 09：APA 风格正文写作

写作规则：

- 使用 APA 第 7 版作者—年份引文格式。
- 每个事实性、定义性、理论性、方法性、神经机制性或结论性主张必须连接 `claim_id`。
- 不写没有证据的“研究表明”。
- 不把横断相关或相关性神经影像写成因果。
- 不把脑区激活写成“证明机制”。应写为 convergent、indirect、limited 或 mixed evidence。
- 不把成人样本结论直接外推到青少年、儿童、老年人或临床群体。
- 不把动物或计算模型结果直接写成人类心理机制。
- 不把一种任务或量表测到的指标当成整个理论构念。
- 引文密集段落要合并成论证，不要一篇一段。
- 对争议、空白和方法限制的表述应明确，不用过度确定语气。

产物：

```text
09_manuscript/review_draft.md
09_manuscript/review_draft.docx
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
10_alignment/unsupported_or_overstated_claims.md
```

推荐字段：

```csv
alignment_id,manuscript_section,manuscript_page,manuscript_paragraph,manuscript_sentence,claim_text,claim_type,citation_in_text,paper_id,zotero_key,bibtex_key,source_title,source_page,source_section,source_paragraph_or_table,source_evidence_summary,short_quote,evidence_role,alignment_status,risk_note,fix_needed
```

要求：

- `manuscript_page` 在 Markdown 阶段可先用章节和段落号；导出 DOCX/PDF 后再补页码。
- `source_page` 优先用 PDF 页码；若电子文献无页码，使用章节、段落、表图编号。
- `claim_type` 可为：定义、理论、方法、测量、实验结果、神经结果、脑—行为关系、争议、研究缺口、推论。
- `alignment_status` 可为：`verified`、`needs_page`、`weak_support`、`overstated`、`missing_source`、`citation_not_used`。
- 任何 `missing_source` 或 `overstated` 必须修改正文或删除主张。
- 参考文献表只保留正文实际引用文献；正文引用必须全部出现在参考文献表。

## 20. 阶段 11：模拟投稿与意见审核

模拟投稿不是实际投稿。若涉及目标期刊 scope、article type、word limit、reference style、open science、AI policy、fees 或伦理要求，必须核查期刊当前官方说明，不得只凭记忆。

步骤：

1. 根据主题、文章类型、语言、方法和篇幅筛选 2–3 个可能期刊。
2. 分别模拟中文心理学/神经科学相关期刊和 SSCI/英文心理学或认知神经科学期刊审稿路径，除非用户只指定一种。
3. 写 `journal_fit_memo.md`：推荐目标、理由、风险、格式差距。
4. 进行模拟编辑初筛：范围、创新性、综述类型匹配、方法透明度、引用完整性、伦理和学术诚信。
5. 分角色模拟审稿：理论/领域专家、认知神经科学方法专家、心理测量/统计专家、写作与 APA 格式审稿、反方审稿人。
6. 输出模拟决定：`minor revision`、`major revision`、`reject and resubmit` 或 `not ready`。不要轻易给 `accept`。
7. 生成 `revision_matrix.csv`：意见、严重度、证据、修改位置、操作、状态。
8. 按证据完成修改，并再次运行引用、格式、方法、逻辑、神经机制过度推论审计。

## 21. 认知神经科学提取要求

每篇纳入研究在可获得时提取：

- experimental paradigm/task: fear conditioning, extinction, emotional picture memory, word-pair memory, facial emotion task, Go/No-Go, n-back, IAT/GNAT, sleep lab protocol, nap protocol
- sample: age, sex/gender, clinical status, medication, sleep quality, trauma/depression/anxiety status, culture/language
- REM/sleep variables: REM duration, REM latency, REM density, awakenings, polysomnography, sleep deprivation, nap/night sleep, dream report
- cognitive process: encoding, consolidation, reconsolidation, extinction, retrieval, attentional bias, affective evaluation, regulation
- behavioral indicators: accuracy, reaction time, hit/false alarm, d′, bias, recall/recognition, valence/arousal ratings
- EEG/ERP indicators: P1, N1, N2, P3, LPP, ERN, FRN, N400, theta, alpha, beta, gamma, sleep spindles, slow oscillations, REM theta
- fMRI/brain indicators: amygdala, hippocampus, vmPFC, dlPFC, ACC, insula, striatum, DMN, salience network, frontoparietal network, functional connectivity
- statistical claims: effect size, confidence interval, correction method, model type, preregistration, robustness, null findings

## 22. 写作与推理规则

- 区分 evidence、inference、recommendation。
- 不从横断相关或相关性神经影像推断因果。
- 不声称某脑区“证明”某心理机制。
- 区分成人、青少年、儿童、老年、临床、高风险和健康样本。
- 区分 human、animal 和 computational evidence。
- 区分 emotion memory enhancement、emotion regulation、fear extinction 和 general memory consolidation。
- 有 primary study 时，不把 review 当作 primary empirical evidence 引用。
- 不把 null 或 mixed evidence 写成正向确定结论。
- 避免“近年来，随着……”这类无证据开头。
- 避免“具有重要理论和实践意义”这类空泛结尾，除非段落已说明具体意义。
- 优先使用段落级论证：claim → evidence pattern → limitation/contrast → implication。

## 23. 失败条件

出现以下情况时，必须停止或降级报告，不能继续声称完成：

- 没有冻结综述主题就开始正式大规模下载。
- 检索式、数据库、日期、结果数无法复现。
- 用摘要代替可获得全文支持精确主张。
- 文献等级没有理由。
- 质量评价只给总分，没有设计域判断。
- 认知神经机制没有原文页码/章节/结果段支持。
- 将脑区激活、ERP 成分或功能连接写成直接因果证明。
- 将成人、动物或计算模型结论直接外推到目标人群。
- 正文引用与参考文献不一致。
- 主张无法定位到原文页码/章节/段落/表图。
- 使用未授权 PDF、盗版来源、cookie、账号密码或突破访问限制。
- 将模拟审稿意见表述为真实反馈。

## 24. 最终回复格式

每次阶段结束，向用户简洁报告：

```text
完成阶段：
核心产物：
关键发现：
机制证据状态：
证据缺口：
风险/限制：
下一步建议：
需要用户确认的问题：
```

不要输出冗长过程日志；日志保存在运行目录。用户需要详细日志时再提供。
