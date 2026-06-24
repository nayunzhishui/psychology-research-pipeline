---
name: psych-cog-neuro-review
description: Use this standalone Chinese-first cognitive-neuroscience psychology workflow for review and empirical/experimental projects involving mechanisms, experimental paradigms, behavioral-neural integration, EEG/ERP, fMRI, PSG, eye-tracking, psychophysiology, sleep, emotion, memory, cognitive control, threat/reward processing, and related methods. It supports broad-direction exploration, focused protocol freeze, bilingual evidence search, Chrome/Zotero Connector ingestion, folder fallback, screening, 1–4 relevance rating, cognitive-neuroscience evidence extraction, neural/physiological mechanism matrices, experimental design, task/protocol planning, preprocessing/analysis planning, APA 7 writing, source alignment, and simulated Chinese/English journal review. 这是“认知神经科学工作流”，不是普通综述 skill 的路由；不要用于伪造神经机制、伪造数据、绕过权限、保存凭据、无人值守批量下载或真实投稿提交。
---

# Cognitive Neuroscience Psychology Workflow / 认知神经科学工作流

本 skill 是三个主工作流之一，定位为**认知神经科学、脑机制、实验范式和行为—神经/生理整合研究的专用工作流**。它可以服务两类任务：

1. 认知神经科学综述：机制综述、理论综述、方法学综述、测量/范式综述、范围综述或系统综述预备。
2. 认知神经科学实证/实验项目：实验范式设计、神经/生理指标选择、数据预处理计划、统计分析计划和论文写作。

它不是普通综述 skill 的路由，也不是一般心理学实证论文 skill 的替代。若任务是普通心理学综述，使用 `psych-literature-review-workflow`；若任务是普通心理学实证论文，使用 `psychology-research-pipeline`；若任务涉及 EEG/ERP、fMRI、PSG、眼动、生理指标、实验任务或脑机制整合，使用本 skill 或由其他主 skill 调用本 skill 的专用模块。

默认语言为中文，必要英文保留于实验范式、脑区、神经网络、神经/生理指标、预处理术语、统计模型、数据库检索式、题录、APA 引文和参考文献。

## 1. 适用场景

使用本 skill，当主题涉及以下至少一类内容：

- EEG/ERP、fMRI、PSG、眼动、皮电、心率变异性、呼吸、内分泌、神经影像或其他神经/生理指标。
- 认知控制、情绪加工、记忆、注意、威胁/奖赏加工、睡眠与情绪、发展认知神经科学、临床认知神经机制。
- 实验范式：Go/No-Go、Stop-signal、n-back、Stroop、Flanker、IAT/GNAT、情绪图片记忆、恐惧条件化、消退、再巩固、睡眠实验、nap protocol 等。
- 需要整合行为结果、主观量表、神经/生理指标、理论机制和心理学变量。
- 需要设计或审查认知神经科学实验，而不仅是阅读文献。

不要使用本 skill，当任务只是：

- 普通心理学综述，不涉及机制、实验或神经/生理指标。
- 普通问卷实证论文，不涉及认知神经科学专用方法。
- 临时解释概念、润色单段文字或整理普通参考文献。
- 用户要求伪造文献、伪造 DOI、伪造页码、伪造数据、伪造脑区结果、伪造 ERP 成分、伪造 fMRI 激活、伪造 PSG 分期或伪造审稿意见。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制、出版社条款或使用盗版 PDF 来源。
- 用户要求真实投稿、支付版面费、联系编辑或执行真实投稿动作。

## 2. 与另外两个主 skill 的边界

当前三个主 skill 为：

1. `psychology-research-pipeline`：心理学实证论文工作流。
2. `psych-cog-neuro-review`：认知神经科学工作流。
3. `psych-literature-review-workflow`：新的通用综述工作流。

本 skill 与其他 skill 的协作规则：

- 当 `psychology-research-pipeline` 的实证项目包含 EEG/ERP、fMRI、PSG、眼动、生理指标或实验范式时，本 skill 提供范式、指标、预处理、神经机制和报告规范模块。
- 当 `psych-literature-review-workflow` 的综述主题明显涉及脑机制、实验范式或神经/生理证据时，本 skill 提供机制矩阵、范式分类、神经指标评价和机制写作模块。
- 若用户要求完整的认知神经科学项目，本 skill 可独立总控。
- `psych-review-workflow` 仅为旧版辅助材料，不作为主 skill。

## 3. 默认定位与运行模式

默认定位：**mixed cognitive-neuroscience workflow / 混合型认知神经科学工作流**。

首次运行时选择一个模式，并写入 `state.json` 和 `logs/decisions.md`。

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 课程综述、早期选题、实验范式初步设计 | 方向探索、seed papers、初步机制图、方法草案 | scoping brief, seed matrix, paradigm sketch |
| `standard` | 研究生综述、实验设计、中文/英文论文预备 | 00–11 全流程；单人筛查可接受但需声明 | evidence matrix, mechanism model, methods plan, draft |
| `strict` | 系统综述/范围综述、注册报告、投稿级实验项目、高风险引用核查 | 正式协议、完整检索日志、严格筛查、质量评价、预处理/分析计划、完整对齐 | auditable review or empirical package |

不要静默降低用户要求的模式。若 access、时间、数据或工具限制导致 `strict` 不可完成，记录 blocker，并在用户确认或明确说明假设后降级。

## 4. 启动时的需求沟通

首次运行时先询问，除非用户已经给出答案。用户未完全回答时，可用默认值继续，但必须记录为 `assumption`。

必要问题：

1. 当前任务是综述、实验设计、实证论文，还是已有数据分析？
2. 当前是宽方向，还是已经聚焦后的主题/题目？
3. 目标用途：课程作业、开题、学位论文、中文期刊、英文期刊、注册报告、投稿预备。
4. 核心边界：构念、人群、年龄段、临床/非临床、human/animal/computational、实验范式、神经/生理指标。
5. 是否已有实验材料、量表、刺激、程序、E-Prime/PsychoPy 任务、EEG/fMRI/PSG/眼动数据或分析输出。
6. 运行模式：`lite`、`standard`、`strict`，默认 `standard`。
7. 是否纳入 REM/sleep 证据，是否加载 REM/emotional memory topic pack。
8. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero 目标 collection；失败时是否下载到文件夹由用户手动导入。
9. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 5. 默认数据库范围

默认数据库与三个主 workflow 保持一致：

- PubMed
- PsycINFO
- Web of Science
- Crossref
- Google Scholar（辅助检索，不单独声称完整）
- CNKI
- 期刊官网
- Zotero 本地库

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求，或某一认知神经科学主题确有必要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 6. 默认运行目录

```text
cog_neuro_runs/<YYYYMMDD>_<short_topic>/
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
│   └── 06_正文与方法/
├── 00_scope/
├── 01_protocol/
├── 02_search/
├── 03_library/
├── 04_screening/
├── 05_evidence_matrix/
├── 06_mechanism_model/
├── 07_design_or_synthesis/
├── 08_analysis_plan/
├── 09_manuscript/
├── 10_alignment_audit/
└── 11_submission_review/
```

不要覆盖旧文件。修订版使用 `_v2`、`_v3`，并在日志中说明修订原因。

## 7. 阶段总览

| 阶段 | 名称 | 目标 | 主要产物 |
|---|---|---|---|
| 00 | 方向与任务定标 | 判断是综述、实验设计还是实证论文；确定边界 | `scope_brief.md`, `task_type.md`, `导师汇报版简表.md` |
| 01 | 协议冻结 | 冻结综述/实验/实证项目协议 | `protocol.md`, `concept_map.md`, `mechanism_scope.md`, `inclusion_exclusion.md` |
| 02 | 证据检索 | 双语检索理论、综述、方法和实证证据 | `queries.md`, `database_search_log.csv`, `candidate_records.csv` |
| 03 | Zotero/全文获取 | 合法入库、去重、PDF 核验 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 分类与筛查 | 分类文献并给出 1–4 级相关性 | `classification.csv`, `screening_table.csv`, `relevance_ratings.csv` |
| 05 | 证据矩阵 | 提取普通矩阵和神经/生理机制矩阵 | `literature_matrix.csv/xlsx/md`, `neural_mechanism_matrix.csv/xlsx/md`, `quality_appraisal.csv` |
| 06 | 机制模型 | 整合行为—神经—心理变量机制链 | `mechanism_model.md`, `claim_evidence_map.csv`, `contradiction_gap_register.csv` |
| 07 | 设计或综合 | 综述则生成章节架构；实证则生成实验/方法设计 | `review_outline.md` 或 `experimental_design_plan.md` |
| 08 | 预处理与分析计划 | 为 EEG/fMRI/PSG/眼动/行为数据制定分析计划 | `preprocessing_plan.md`, `statistical_analysis_plan.md`, `reporting_plan.md` |
| 09 | 正文写作 | 写作综述或实证论文草稿 | `manuscript.md`, `manuscript.docx`, `references.bib`, `apa_references.md` |
| 10 | 来源与方法审计 | 核查主张、引用、数字、方法和神经机制证据 | `source_alignment_table.csv/xlsx`, `method_audit.md`, `claim_audit.md` |
| 11 | 模拟投稿审稿 | 模拟中文/英文期刊投稿前审查 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

若任务只是综述，可以跳过实验材料制作和数据分析执行，但不能跳过证据矩阵、机制模型、来源对齐和模拟审稿。若任务是实证/实验项目，不能只写综述而忽略设计、预处理、分析和报告规范。

## 8. 阶段 00：方向与任务定标

用户只给出宽方向时，先做探索式检索，不进入正式全文下载。

目标：找出核心概念、研究流派、实验范式、常用测量、神经/生理指标、主要争议、代表性综述、代表性方法文章和近年前沿趋势，并向用户提供 2–5 个可聚焦方向或实验问题。

优先搜集：

- 最近 5–10 年综述、系统综述、范围综述、元分析。
- 经典理论文章、概念界定文章、共识/指南。
- 方法学文章：实验范式、EEG/ERP、fMRI、PSG、眼动、心理测量、统计方法。
- 近 3 年高相关实证研究，用于判断前沿趋势。

输出导师汇报版简表：

```csv
候选方向,核心问题,关键范式/指标,文献基础,创新点,风险,推荐等级,下一步建议
```

## 9. 阶段 01：协议冻结

协议至少包括：

- 暂定题目，中英文各一版。
- 任务类型：综述、实验设计、实证论文、已有数据分析。
- 研究问题与假设。
- 核心构念、理论模型、同义词、量表名、实验范式、神经/生理指标。
- 人群、年龄、临床/非临床、human/animal/computational 边界。
- 纳入/排除标准。
- 检索数据库与补充检索。
- Zotero collection 和文件夹备选方案。
- 如果是实证/实验项目：样本方案、任务流程、刺激材料、记录设备、预处理、统计分析计划。
- 质量评价工具、停止规则、修订规则。

协议冻结后才能进入正式检索或正式实验设计。后续若修改范围，必须记录 amendment。

## 10. 阶段 02：证据检索

正式检索目标是覆盖主题领域，而不是只拿几篇好写的文章。

执行步骤：

1. 为每个核心概念建立英文、中文、缩写、量表名、任务名、脑区、神经网络、ERP 成分、fMRI contrast、PSG 指标等检索词。
2. 生成宽检索式和窄检索式。不同数据库使用不同语法。
3. 每个数据库记录：平台、日期、检索式、过滤器、结果数、导出文件、备注。
4. 导出题录并统一字段：DOI、PMID、title、authors、year、journal、abstract、keywords、URL、database、query_id。
5. 去重顺序：DOI → PMID → 标准化标题 + 第一作者 + 年份。保留 provenance。
6. 对核心 seed papers 做 backward citation chasing 和 forward citation chasing。
7. 使用新增价值停止规则：连续一轮新增文献不再增加新理论、新范式、新指标、新人群、新方法、新关键发现、新争议或新高质量证据。

严禁把 Google Scholar、ResearchGate 或任意网页结果说成“完整检索”。

## 11. 阶段 03：Chrome + Zotero / 文件夹备选

优先方案：Codex 使用 Chrome 中用户已登录的合法学术访问环境，调用 Zotero Connector 将文献导入本地 Zotero 的指定 collection。

边界：

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。
- 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。按批次处理，并在异常警告时停止。
- 不把 PDF、Zotero 数据库、浏览器材料、数据文件或账号信息提交到 GitHub。

每篇文献必须验证：题名、作者、年份、DOI/PMID、Zotero parent item、附件 key、PDF 是否可读、首页题名是否匹配、页数是否合理。

## 12. 阶段 04：分类、初筛与 1–4 级相关性

先分类，再决定阅读深度。

文献类型至少包括：

- `review_systematic`：系统综述/元分析。
- `review_scoping`：范围综述。
- `review_narrative`：叙述综述/理论综述。
- `theory_conceptual`：理论、概念、模型文章。
- `methods_paradigm`：实验范式、任务设计、刺激材料文章。
- `methods_neurophysiology`：EEG/ERP、fMRI、PSG、眼动、生理记录或预处理文章。
- `methods_measurement`：量表、心理测量、问卷验证。
- `empirical_behavioral`：行为实证研究。
- `empirical_neural`：神经/生理实证研究。
- `intervention_trial`：干预、随机对照、临床试验。
- `qualitative_mixed`：质性或混合方法。
- `commentary_guideline`：评论、共识、指南、立场文件。

相关性等级是“对当前主题的使用价值”，不是学术质量。

| 等级 | 名称 | 判定标准 | 阅读处理 |
|---|---|---|---|
| 4 | 核心文献 | 直接对应核心构念、目标人群/任务、关键神经/生理指标、理论机制或主要结果 | 全文精读，进入矩阵和星图核心层 |
| 3 | 重要相关 | 支持一个核心板块，如概念、范式、机制、测量、方法或证据链 | 阅读摘要、方法、结果、讨论；必要时全文精读 |
| 2 | 背景相关 | 与主题有交集，但人群、指标、任务或理论边界不完全匹配 | 摘要和关键段落阅读 |
| 1 | 边缘相关 | 只提供一般背景、相邻概念或排除理由 | 记录后通常不纳入正文核心引用 |

辅助评分：方法质量、样本适配度、理论贡献、神经/生理指标适配度、范式适配度、证据强度、引用价值、与其他文献连接度。

## 13. 阶段 05：认知神经科学证据矩阵

输出 CSV、Excel、Markdown 三种格式。

普通阅读矩阵字段：

```csv
stable_id,文献类型,相关性等级,方法质量,样本适配度,理论贡献,证据强度,引用价值,核心构念,人群/样本,研究设计,主要发现,局限,可引用位置,适合写入章节,是否需要复核
```

神经/生理机制矩阵字段：

```csv
stable_id,范式/任务,刺激材料,行为指标,神经/生理指标,脑区/网络,ERP成分/频段,fMRI contrast,PSG/睡眠指标,眼动/自主神经指标,采集设备,预处理流程,统计模型,关键结果,机制解释,替代解释,局限,可支持主张,页码/图表位置,是否需要复核
```

不要把“某脑区激活”直接写成确定机制。必须区分观察结果、统计关联、机制解释和作者推论。

## 14. 阶段 06：机制模型与 HTML 星图

机制模型至少包括：

- 核心心理构念。
- 行为指标。
- 神经/生理指标。
- 理论机制。
- 人群与情境边界。
- 证据强度。
- 矛盾结果和替代解释。

HTML 文献星图基于激活扩散模型：

- 节点：文献、理论、构念、范式、任务、脑区/网络、神经/生理指标、核心发现。
- 边：引用关系、共同变量、共同范式、共同指标、机制链条、结果一致/冲突。
- 权重：主题贴合度 × 方法质量 × 证据强度 × 神经/生理指标适配度 × 连接度 × 新近性/经典性。
- 输出：`reference_star_map.html`、`star_map_data.json`、`weighting_notes.md`。

星图用于辅助理解，不得替代全文阅读和方法质量评价。

## 15. 阶段 07：综述架构或实验设计

如果任务是综述，默认板块：

1. 引言与问题提出。
2. 概念界定与理论边界。
3. 核心实验范式与测量方法。
4. 行为证据。
5. 神经/生理证据。
6. 行为—神经机制整合。
7. 矛盾结果、方法学问题与替代解释。
8. 整合模型。
9. 未来研究方向。
10. 结论。

如果任务是实验/实证项目，方法设计至少包括：

- 研究问题与假设。
- 被试、人群、纳入/排除标准、样本量依据。
- 任务范式、刺激材料、试次数、block、随机化、反应窗口。
- 神经/生理采集设备、采样率、通道/ROI、事件标记、同步方案。
- 问卷、行为指标、神经/生理指标、主要/次要结局。
- 伦理、安全、疲劳、诱发负性情绪、退出机制。
- 预注册/开放科学计划。

## 16. 阶段 08：预处理与分析计划

根据方法类型制定分析计划：

- EEG/ERP：滤波、重参考、坏道、ICA/伪迹处理、epoch、baseline、成分窗口、ROI/电极群、multiple comparisons。
- fMRI：slice timing、motion correction、normalization、smoothing、first-level/second-level、ROI/whole-brain、multiple comparisons。
- PSG/sleep：睡眠分期、REM/NREM 指标、arousal、睡眠结构、nap protocol、评分一致性。
- 眼动：注视、扫视、兴趣区、瞳孔、眨眼/丢失数据处理。
- 行为数据：正确率、反应时、d′、c、D-score、混合模型、重复测量 ANOVA、Bayesian/robust analysis。
- 问卷数据：反向计分、信度、CFA/ESEM、相关、回归、中介/调节、SEM。

任何探索性分析必须标注 exploratory。不要在看到结果后倒推假设。

## 17. 阶段 09：写作规范

默认 APA 第 7 版兼容。根据任务类型写作：

- 综述稿：引言、理论/机制、方法证据、实证证据、整合模型、局限、未来方向、结论。
- 实证稿：引言、方法、结果、讨论、参考文献、表图、补充材料。

每个事实性、定义性、理论性、方法性、结果性或机制性主张，写作时就绑定来源或分析产物。不要写完后硬补引用。

## 18. 阶段 10：来源、方法与机制审计

必须输出：

```csv
正文页码,正文段落,正文原句,支撑文献/分析产物,来源页码/图表/段落,原文证据短摘录,证据类型,支持强度,是否存在过度推论,是否需要复核
```

同时核查：

- 神经机制主张是否超出原文证据。
- 行为结果、神经指标、统计结果是否一致。
- 方法部分是否足以复现。
- 预处理和分析计划是否与报告结果一致。
- APA 引文和参考文献是否一致。

## 19. 阶段 11：模拟投稿审稿

默认模拟两套审查：中文心理学/认知神经科学相关期刊，以及英文心理学/认知神经科学期刊。期刊 scope、格式、版面费、开放获取、AI policy 和投稿要求必须联网核查，不能依赖旧知识。

审稿模块包括：

- 编辑初筛。
- 理论贡献审稿。
- 方法学/范式审稿。
- 神经/生理指标审稿。
- 统计与可复现性审稿。
- APA 格式审稿。
- 引文准确性审稿。
- 修改意见清单。
- 作者回复模板。

模拟反馈必须标注为模拟，不得冒充真实期刊意见。

## 20. 安全边界

- 不伪造文献、DOI、页码、PDF、数据、ERP 成分、脑区激活、fMRI contrast、PSG 指标、眼动指标、统计结果或审稿意见。
- 不绕过数据库权限、验证码、MFA、付费墙、下载限制或出版社条款。
- 不保存账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。
- 不把 Zotero 数据库、PDF、浏览器凭据、受限全文或敏感原始数据提交到 GitHub。
- 不真实投稿、支付费用或联系编辑，除非用户另行明确授权并在操作时确认。
- 不把相关或共激活直接写成因果机制；机制推论必须标注证据等级和替代解释。

## 21. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在仍有关键引用、方法、数据、伦理、预处理、统计或机制推论问题时声称“可直接投稿”。
