---
name: psych-literature-review-workflow
description: Use this skill to run a reusable Chinese-first psychology literature-review workflow from broad research-direction exploration to focused protocol, saturated literature collection, Chrome/Zotero Connector ingestion, classification, relevance rating, full-text evidence matrix, HTML reference star map, APA-style review writing, sentence/paragraph-to-source alignment, and simulated submission review. 适用于人格功能损害、健康心理学、临床心理学、认知神经科学、发展心理学等方向的综述写作，也可迁移到其他心理学综述主题。不要用于伪造文献、绕过付费墙、无人值守批量下载、真实投稿提交，或脱离证据矩阵的自由写作。
---

# Psychology Literature Review Workflow / 心理学文献综述写作工作流

本 skill 用于把一个宽泛研究方向推进为可聚焦、可检索、可审计、可写作、可模拟投稿的综述项目。默认服务心理学、健康心理学、临床心理学、认知神经科学、精神病理学、发展心理学等方向。当前默认示例主题可以是“人格功能损害（impairment in personality functioning）”，但 skill 本身必须保持通用，可复用于其他综述。

除必要英文外，所有工作说明、判断标准、阶段报告、阅读矩阵、写作建议、审稿意见默认使用中文。英文保留于：数据库检索式、英文题名、量表名、理论名、变量名、DOI/PMID、APA 引文、参考文献表和必要术语。

## 1. 适用场景

使用本 skill，当用户提出以下任务之一：

- 只给出一个宽研究方向，需要先检索综述、方法学文章和核心理论文章，帮助用户聚焦综述方向。
- 已经给出聚焦后的综述主题，需要进入正式文献检索、Zotero 入库、全文阅读、证据矩阵和综述写作。
- 需要制作中文为主、APA 第 7 版兼容的心理学综述稿。
- 需要输出 CSV、Excel、Markdown 阅读矩阵，HTML 文献星图，正文—参考文献精确对齐表，以及模拟投稿审稿意见。

不要使用本 skill，当任务只是：

- 临时解释一个概念、润色单个段落、写邮件或做普通摘要。
- 用户要求凭空补文献、伪造页码、伪造 DOI、伪造审稿意见或伪造投稿结果。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制、出版社限制或使用盗版 PDF 来源。
- 用户要求真实提交投稿系统、代替作者联系编辑、支付版面费或执行真实投稿动作。

## 2. 默认综述类型

默认支持多类综述，但默认运行方式为：**半系统化叙述综述 / 整合型综述**。

可根据用户要求切换为：

- narrative review / 叙述性综述
- theoretical review / 理论综述
- scoping review / 范围综述
- systematic review / 系统综述
- methodological review / 方法学综述
- measurement review / 测量工具综述
- meta-analysis-prep review / 元分析预备综述

不要在没有正式协议、完整检索日志、纳排标准、筛查记录和偏倚风险评价时，把文章声称为“系统综述”。如果只是吸收 PRISMA 的透明性原则，应写作“半系统化叙述综述”或“透明化叙述综述”。

## 3. 总原则

1. **先探索聚焦，再正式综述**：主题未聚焦时，不直接大规模下载全文。先用高质量综述、方法学文章、理论文章帮助用户确定边界。
2. **证据先于写作**：正式写作必须来自题录、全文、阅读卡、证据矩阵和来源位置，不得先写后找文献硬配。
3. **广覆盖但有停止规则**：正式检索应尽可能完整覆盖主题，直到新增文献不能再提供新的理论、方法、测量、人群、关键发现、争议或高质量证据。
4. **分类阅读**：先分类，再评级，再阅读全文；不要把所有文献平铺成普通参考文献表。
5. **相关度与质量分开**：1–4 级表示与主题贴合度，不等于方法质量。方法质量另行评价。
6. **正文写作时同步引文对齐**：不要等写完后才补引用。每个实质性主张在写作时就绑定来源。
7. **模拟审稿必须标注模拟性质**：不能让用户误以为是真实期刊反馈。

## 4. 与仓库其他 skills 的关系

如果仓库中存在以下 skills，可优先复用；本 skill 保留总控责任：

- `psych-review-workflow`：可作为既有综述总控流程参考。
- `psych-cog-neuro-review`：当主题偏认知神经科学、脑机制、ERP/EEG、fMRI、PSG 等时，可借用其机制综述逻辑。
- `psych-zotero-ingest`：用于 Zotero 入库、合法全文获取、PDF 核验和重复项处理。
- `psych-review-source-alignment` 或同类子 skill：用于正文—参考文献逐句/逐段对齐。

如果这些 skills 与本 skill 冲突，以本 skill 中用户已确认的约束为准，尤其是：中文优先、两阶段流程、默认数据库范围、1–4 级相关度、HTML 星图、APA 第 7 版、模拟投稿审稿。

## 5. 启动时的需求沟通

首次运行时先简短询问，除非用户已经给出答案。用户未回答时，可以使用默认值继续，但必须在 `logs/decisions.md` 中记录为 `assumption`。

必要问题：

1. 当前是宽研究方向，还是已经聚焦后的综述主题？
2. 目标综述类型：叙述综述、理论综述、范围综述、系统综述、方法学综述、测量综述，还是默认半系统化叙述综述？
3. 目标用途：课程作业、开题、学位论文综述、中文期刊、英文期刊、投稿预备稿？
4. 核心边界：核心构念、目标人群、年龄段、临床/非临床、研究设计、是否纳入干预、是否纳入神经机制。
5. 文献获取方式：是否允许 Codex 使用 Chrome + Zotero Connector；Zotero 目标 collection 名称；若失败是否下载到文件夹由用户手动导入。
6. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 6. 默认运行目录

默认建立一个运行目录：

```text
review_runs/<YYYYMMDD>_<short_topic>/
├── state.json
├── manifest.json
├── logs/
│   └── decisions.md
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

## 7. 阶段总览

| 阶段 | 名称 | 目标 | 主要产物 |
|---|---|---|---|
| 00 | 宽方向探索 | 从宽方向中识别可写综述方向 | `scoping_brief.md`, `seed_reviews.csv`, `seed_methods.csv`, `focus_options.md` |
| 01 | 聚焦与协议冻结 | 把聚焦主题转为可执行综述协议 | `review_protocol.md`, `concept_map.md`, `inclusion_exclusion.md` |
| 02 | 正式大范围检索 | 饱和式搜集符合主题的文献 | `queries.md`, `search_log.csv`, `candidate_records.csv` |
| 03 | Zotero/全文获取 | 用 Chrome + Zotero Connector 入库，备选为文件夹手动导入 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与初筛 | 分类文献并给出 1–4 级主题符合程度 | `classification.csv`, `relevance_ratings.csv`, `screening_log.csv` |
| 05 | 全文阅读矩阵 | 深读全文并建立证据矩阵 | `literature_matrix.csv`, `literature_matrix.xlsx`, `literature_matrix.md`, `quality_appraisal.csv` |
| 06 | 证据综合 | 汇总理论、方法、发现、矛盾和空白 | `claim_evidence_map.csv`, `contradictions.md`, `gap_register.md` |
| 07 | HTML 文献星图 | 基于激活扩散模型建立参考文献网络 | `reference_star_map.html`, `star_map_data.json`, `weighting_notes.md` |
| 08 | 写作架构 | 设计综述板块和论证链 | `section_plan.md`, `argument_map.md`, `citation_plan.csv` |
| 09 | APA 综述正文 | 写作中文为主、APA 7 兼容的综述稿 | `manuscript.md`, `manuscript.docx`, `references.bib`, `apa_references.md` |
| 10 | 原文—引用对齐 | 精确核查正文与参考文献来源 | `source_alignment_table.csv`, `source_alignment_table.xlsx`, `claim_audit.md` |
| 11 | 模拟投稿审稿 | 模拟中文/英文期刊投稿前审查 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

## 8. 阶段 00：宽方向探索

当用户只给出研究方向时，先做探索式检索。目标不是完整下载，而是帮助用户聚焦。

优先搜集：

- 最近 5–10 年综述、系统综述、范围综述、元分析。
- 经典理论文章、概念界定文章、共识/指南。
- 研究方法类文章、测量工具文章、量表验证文章。
- 近 3 年高相关实证文章，用于判断前沿趋势。

输出 `focus_options.md`，每个候选方向必须包括：

- 中文题目建议
- 英文题目建议
- 核心研究问题
- 适合的综述类型
- 文献基础是否充足
- 可能章节结构
- 写作优势
- 写作风险
- 与用户研究方向的贴合度
- 是否建议继续

还要输出一个**导师汇报版简表**：

```csv
候选方向,核心问题,文献基础,创新点,风险,推荐等级,下一步建议
```

## 9. 阶段 01：聚焦与协议冻结

用户确定聚焦后的综述方向后，进入协议阶段。

协议必须包括：

- 暂定中文题目和英文题目。
- 综述类型及理由。
- 研究问题，可使用 PCC、PEO、PICO、SPIDER 或心理学自定义框架。
- 核心构念定义、同义词、英文缩写、中文译名、常见量表。
- 纳入标准：人群、年龄、样本、研究设计、语言、年份、全文状态、文献类型。
- 排除标准：主题不符、非心理学主题、纯评论、无法定位证据、重复报告、非授权全文等。
- 检索数据库与补充检索。
- Zotero collection 名称与文件夹备选方案。
- 阅读矩阵字段。
- 质量评价标准。
- 新增价值停止规则。
- AI 使用说明与人工复核位置。

协议冻结后才能进入正式大范围检索。后续修改必须记录 amendment：修改内容、原因、影响阶段。

## 10. 阶段 02：正式大范围检索

默认数据库范围：

- PubMed
- PsycINFO，由用户通过学校权限导出或提供题录
- Web of Science，由用户通过学校权限导出或提供题录
- Crossref
- Google Scholar，辅助检索和引文追踪
- CNKI，用于中文综述、中文量表和中文研究
- 期刊官网
- Zotero 本地库

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed。只有用户明确要求时才加入。

执行要求：

1. 为每个核心概念建立英文、中文、缩写、量表名、诊断术语、理论名。
2. 生成宽检索式和窄检索式。不同数据库使用对应语法，不能把一个检索式复制到所有平台。
3. 每次检索记录：数据库、平台、日期、检索式、过滤器、结果数、导出文件、备注。
4. 导出字段至少包括：DOI、PMID、title、authors、year、journal、abstract、keywords、URL、database、query_id。
5. 去重顺序：DOI → PMID → 标准化标题 + 第一作者 + 年份。
6. 对核心 seed papers 做 backward citation chasing 和 forward citation chasing。

### 新增价值停止规则

正式检索可停止，只有在以下条件同时基本满足时：

- 连续一轮新增文献不再增加新理论、新测量、新方法、新人群、新关键发现、新争议或高质量综述。
- 关键综述、方法学文章和 4 级核心实证文章的参考文献已追踪。
- 默认数据库均已检索，未检索数据库有明确原因。
- 新增文献主要为重复、低相关、低质量或只重复既有结论。
- 停止理由已经写入 `02_search/search_saturation_note.md`。

不要把“时间不够”伪装成检索饱和。时间不足时写为 limitation。

## 11. 阶段 03：Chrome + Zotero Connector 入库与全文获取

默认边界：

- Codex 可以使用用户已登录的 Chrome 页面和 Zotero Connector。
- 用户自己处理学校账号、VPN、图书馆代理、统一认证、MFA、验证码、数据库权限确认。
- Codex 不查看、不记录、不保存账号、密码、验证码、密钥、cookie、token、浏览器配置或数据库凭证。
- Codex 不绕过付费墙、数据库限制、robots 限制或出版社限制。
- Codex 不进行无人值守高频批量下载。

优先流程：

1. 打开文献 DOI、PubMed、期刊官网、数据库页面或学校代理后的合法页面。
2. 使用 Zotero Connector 保存题录和 PDF 到指定 collection。
3. 保存后核验：题名、作者、年份、期刊、DOI、collection、PDF 附件、PDF 可读性。
4. 已存在题录时不重复导入；如仅缺 PDF，则只补充合法 PDF。
5. PDF 必须检查：扩展名、文件大小、`%PDF-` 签名、第一页可读、页数合理、标题/DOI 匹配，不能是 HTML 登录页。

备选流程：

- 若 Zotero Connector 失败，将题录 RIS/BibTeX 和 PDF 保存到：

```text
literature/00_待导入Zotero/
```

- 输出 `manual_import_instructions.md`，由用户手动导入 Zotero。

禁止：

- 删除、合并、重命名、移动或覆盖 Zotero 现有记录。
- 把 PDF、Zotero 数据库、下载全文、cookie、账号文件提交到 GitHub。
- 使用盗版全文源、影子图书馆、PDF bot、泄露凭证或非授权镜像。

## 12. 阶段 04：分类与 1–4 级主题符合程度

先分类，再看摘要和方法，再评级。

### 文献分类

默认分类：

- 综述类：narrative review, systematic review, scoping review, meta-analysis
- 理论/概念类：conceptual paper, theoretical framework, consensus/guideline
- 研究方法类：methodological paper, design paper, analytic strategy
- 测量工具类：scale development, validation, measurement invariance
- 实证文章类：cross-sectional, longitudinal, experimental, clinical, intervention
- 神经/生理机制类：EEG/ERP, fMRI, psychophysiology, PSG, endocrine/immunological markers
- 干预类：CBT, ACT, mindfulness, self-compassion, digital intervention 等
- 中文本土化研究类：中文修订、中文样本、文化适配
- 边缘相关类：背景可用但不进入核心论证

### 主题符合程度 1–4 级

| 等级 | 含义 | 使用方式 |
|---|---|---|
| 1级 | 背景相关，只能用于引言、背景或边缘说明 | 不进入核心证据链，除非用于定义背景 |
| 2级 | 涉及核心概念之一，但人群、方法、变量或问题不完全匹配 | 可支持某个次级章节或补充说明 |
| 3级 | 直接服务综述某一核心章节 | 可作为主要证据纳入阅读矩阵 |
| 4级 | 高度核心，理论、方法、测量或结论对综述主线不可替代 | 必须阅读全文，优先进入星图核心节点 |

### 辅助评分

每篇文献另行评价：

- 方法质量：1–4
- 样本适配度：1–4
- 理论贡献：1–4
- 证据强度：1–4
- 引用价值：1–4
- 与其他文献连接度：1–4

不要把低相关但高质量的文献误判为核心文献；也不要把高相关但低质量的实证研究作为强证据。

## 13. 阶段 05：全文阅读矩阵

所有 3–4 级文献必须优先阅读全文。2 级文献视章节需要深读。1 级通常只读摘要和关键段落。

矩阵必须同时输出三种格式：

```text
05_matrix/literature_matrix.csv
05_matrix/literature_matrix.xlsx
05_matrix/literature_matrix.md
```

默认字段：

```csv
source_id,citation_key,authors,year,title,journal,doi,document_type,review_role,relevance_level,method_quality,sample_fit,theory_contribution,evidence_strength,citation_value,network_connectivity,core_constructs,population,age_range,country_or_culture,study_design,sample_size,measures,methods_or_tasks,analysis_strategy,key_findings,limitations,contradictions,usable_claims,source_page,source_section,source_paragraph_or_table,exact_evidence_excerpt,possible_review_section,notes,needs_human_check
```

阅读标准：

- 综述/元分析：看检索范围、纳排标准、质量评价、核心结论、异质性、争议与空白。
- 理论文章：看概念定义、理论边界、机制路径、可检验命题、与相邻概念区别。
- 方法/测量文章：看工具结构、信效度、样本、适用人群、跨文化适配、局限。
- 实证文章：看样本、设计、变量、测量、统计模型、效应方向、显著性、效应量、稳健性、局限。
- 神经/生理文章：区分任务、指标、时间窗/脑区、生理解释、心理功能推断边界。

## 14. 阶段 06：证据综合

在写正文前，必须先综合证据。

输出：

- `claim_evidence_map.csv`：每个未来正文主张对应哪些文献支持。
- `contradictions.md`：不一致结果、矛盾解释和可能原因。
- `gap_register.md`：研究空白、方法空白、理论空白、人群空白。
- `section_evidence_summary.md`：每个章节能写什么，不能写什么。

每条主张标注：

- 证据类型：定义、理论、方法、测量、实证、元分析、综述、推论。
- 支持强度：直接、部分、间接、矛盾、不足。
- 是否能写进正文。
- 是否需要人工复核。

## 15. 阶段 07：HTML 参考文献星图

基于文献矩阵制作 HTML 星图，不是简单画图。星图应体现激活扩散模型思想：核心文献、理论、变量、方法和证据之间通过权重连接，用户点击一个节点能看到其激活的相关文献和概念。

输出：

```text
07_star_map/reference_star_map.html
07_star_map/star_map_data.json
07_star_map/weighting_notes.md
```

### 节点类型

- 文献节点：paper/review/meta-analysis/method/measurement
- 理论节点：theory/framework/model
- 概念节点：construct/concept
- 变量节点：predictor/mediator/moderator/outcome
- 方法节点：design/task/statistical method
- 测量节点：scale/interview/diagnostic tool/physiological index
- 结论节点：finding/claim

### 边类型

- 引用关系
- 共同概念
- 理论归属
- 变量路径
- 方法相似性
- 测量工具相同
- 证据支持
- 证据矛盾
- 人群或样本相似

### 权重规则

每篇文献的核心权重建议计算为：

```text
core_weight = 0.30 * relevance_level
            + 0.20 * evidence_strength
            + 0.15 * method_quality
            + 0.15 * citation_value
            + 0.10 * network_connectivity
            + 0.10 * recency_or_classic_value
```

所有分数归一化到 0–1。经典理论文献虽然不新，也可以因 `classic_value` 获得高权重。新文献只有在提供新理论、新方法、新证据或新争议时才提高权重。

### 激活扩散展示

HTML 至少支持：

- 按文献类型筛选。
- 按主题符合程度 1–4 级筛选。
- 点击核心文献，突出其连接的理论、变量、方法和相关文献。
- 显示每个节点的摘要、证据角色、推荐写入章节。
- 区分支持性边和矛盾性边。
- 输出图例和权重说明。

## 16. 阶段 08：写作架构

正式写作前先冻结结构。默认综述板块：

1. 题目
2. 摘要
3. 关键词
4. 引言：研究背景、问题提出、综述必要性
5. 概念界定：核心概念、相邻概念、术语边界
6. 理论基础：主要理论模型与发展脉络
7. 测量与操作化：量表、访谈、诊断标准、实验或生理指标
8. 主要实证发现：按主题、机制、人群或方法分组
9. 方法学评价：样本、设计、测量、统计、文化适配、因果推断局限
10. 争议与不一致结果：证据冲突及解释
11. 整合性框架：提出综述整合模型或路径图
12. 研究空白与未来方向
13. 结论
14. 参考文献

如果目标是中文核心期刊，可调整为中文期刊常见结构；如果目标是英文期刊，保留 APA 7 标题层级与英文摘要兼容结构。

## 17. 阶段 09：APA 第 7 版综述正文写作

正文默认中文写作，符合 APA 第 7 版兼容要求。

硬性要求：

- 正文所有实质性主张必须来自 `claim_evidence_map.csv`、`literature_matrix` 或全文证据。
- 写作时同步填写 `citation_plan.csv`，记录每个段落将使用哪些来源。
- 不得把综述文献中的概括性结论伪装成原始实证证据。
- 不得将相关结果写成因果关系，除非研究设计支持因果推断。
- 不得夸大脑区激活、生理指标或统计显著性的心理意义。
- 首次出现英文术语时使用“中文（English term, abbreviation）”。
- 参考文献按 APA 第 7 版处理作者、年份、题名大小写、期刊名、卷期页码、DOI。

正文产物：

```text
09_manuscript/manuscript.md
09_manuscript/manuscript.docx
09_manuscript/references.bib
09_manuscript/apa_references.md
09_manuscript/apa_format_check.md
```

## 18. 阶段 10：综述原文—参考文献对齐

写完后必须生成精确对齐表。对齐精度需要达到：综述中的哪一页、哪一段、哪一句，对应参考文献中的哪一页、哪一段、哪一处表格/图/结果。

输出 CSV 和 Excel：

```text
10_alignment/source_alignment_table.csv
10_alignment/source_alignment_table.xlsx
10_alignment/claim_audit.md
```

表头使用：

```csv
review_page,review_paragraph_id,review_sentence_id,review_sentence_or_claim,claim_type,in_text_citation,source_id,citation_key,source_author_year,source_title,source_page,source_section,source_paragraph_or_table,source_exact_evidence,evidence_type,support_strength,does_source_support_exact_claim,problem_type,revision_suggestion,needs_human_check
```

支持强度：

- `direct`：原文直接支持该句。
- `partial`：只支持一部分，需要缩窄表述。
- `indirect`：支持前提，不直接支持结论。
- `review_only`：综述支持背景判断，但不能替代原始实证。
- `contradictory`：原文与正文表述冲突。
- `unsupported`：未找到支持。
- `overextended`：正文表述超过原文证据。

若任何核心主张为 `unsupported`、`contradictory` 或 `overextended`，不能标记最终完成，必须给出修改建议。

## 19. 阶段 11：模拟投稿与意见审核

默认同时模拟两类期刊：

- 中文心理学核心期刊 / CSSCI 方向
- SSCI / 英文心理学期刊方向

输出：

```text
11_submission_review/journal_fit_memo.md
11_submission_review/editorial_screening.md
11_submission_review/simulated_reviews.md
11_submission_review/revision_matrix.csv
11_submission_review/author_response_template.md
```

模拟审稿模块包括：

1. 期刊定位与适配度分析。
2. 编辑初筛：主题适配、创新性、结构、篇幅、伦理和格式。
3. 理论贡献审稿。
4. 方法学审稿。
5. 文献完整性审稿。
6. APA 格式审稿。
7. 引文准确性和来源对齐审稿。
8. 中文表达和低 AI 痕迹审稿。
9. 修改意见清单。
10. 作者回复模板。

必须明确写明：这些意见是模拟审稿意见，不是真实期刊反馈。

## 20. 质量门槛

每阶段完成前检查：

- 是否有阶段产物。
- 是否记录输入、输出、假设和未解决问题。
- 是否保留检索式、日期、数据库、结果数。
- 是否区分证据、推论和建议。
- 是否所有 3–4 级文献都进入阅读矩阵或有排除理由。
- 是否所有正文主张都有来源位置。
- 是否所有参考文献都在正文中被使用，正文引用也都进入参考文献表。
- 是否有人工复核标记。

如果阶段门槛失败，不要继续进入下一阶段；先修复或记录限制。

## 21. 默认输出清单

完整运行结束后，至少输出：

- `focus_options.md`：方向聚焦建议。
- `review_protocol.md`：综述协议。
- `search_log.csv`：检索日志。
- `zotero_manifest.csv`：Zotero 入库记录。
- `classification.csv`：文献分类。
- `relevance_ratings.csv`：1–4 级主题符合程度。
- `literature_matrix.csv`、`.xlsx`、`.md`：文献阅读矩阵。
- `reference_star_map.html`：HTML 文献星图。
- `claim_evidence_map.csv`：主张—证据表。
- `manuscript.md` 和 `manuscript.docx`：综述正文。
- `apa_references.md`：APA 参考文献。
- `source_alignment_table.csv` 和 `.xlsx`：正文—文献对齐表。
- `simulated_reviews.md`：模拟审稿意见。
- `revision_matrix.csv`：修改矩阵。

## 22. 当前用户默认偏好

如果用户没有另行说明，按以下默认值执行：

- 语言：中文为主，必要英文保留。
- 综述类型：支持多类型，默认半系统化叙述综述/整合综述。
- 当前示例方向：人格功能损害，但不写死为唯一主题。
- 数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar、CNKI、期刊官网、Zotero 本地库。
- 不默认加入：Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed。
- 文献获取：Chrome + Zotero Connector；失败后下载到文件夹，由用户手动导入。
- 文件夹：使用 `literature/00_待导入Zotero/` 等目录结构。
- 相关度等级：1–4 级。
- 文献矩阵：CSV、Excel、Markdown 都要。
- 星图：HTML，展示文献、概念、变量、理论、方法、测量和结论的多层网络。
- 写作：APA 第 7 版兼容。
- 引文对齐：精确到综述页码、段落、句子，以及参考文献页码、章节/段落/表图。
- 模拟投稿：中文核心和 SSCI/英文心理学期刊两套都模拟。
