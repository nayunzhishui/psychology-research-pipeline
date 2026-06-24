---
name: psych-cog-neuro-review
description: Use this standalone Chinese-first cognitive-neuroscience psychology workflow for review, empirical, and experimental projects involving mechanisms, experimental paradigms, behavioral-neural integration, EEG/ERP, fMRI, PSG, eye-tracking, psychophysiology, sleep, emotion, memory, cognitive control, threat/reward processing, and related methods. It supports broad-direction exploration, focused protocol freeze, evidence search, Chrome/Zotero Connector ingestion, folder fallback, screening, 1–4 relevance rating, cognitive-neuroscience evidence extraction, neural/physiological mechanism matrices, experimental design, task/protocol planning, preprocessing/analysis planning, APA 7 writing, source alignment, and simulated Chinese/English journal review. 这是“认知神经科学工作流”，本 skill 被选中后必须独立完成任务，不依赖其他 skill、总索引或共享模板；不要用于普通综述、普通问卷论文、伪造神经机制/数据/文献、绕过权限、保存凭据、无人值守批量下载或真实投稿提交。
---

# Cognitive Neuroscience Psychology Workflow / 认知神经科学工作流

本 skill 是三个主工作流之一，定位为**认知神经科学、脑机制、实验范式和行为—神经/生理整合研究的独立工作流**。它可以服务两类任务：

1. 认知神经科学综述：机制综述、理论综述、方法学综述、测量/范式综述、范围综述或系统综述预备。
2. 认知神经科学实证/实验项目：实验范式设计、神经/生理指标选择、数据预处理计划、统计分析计划和论文写作。

它不是普通综述 skill 的路由，也不是一般心理学实证论文 skill 的替代。本 skill 被选中后，必须在本文件范围内完整执行，不调用其他主 skill，也不作为其他主 skill 的子模块。

默认语言为中文。必要英文保留于实验范式、脑区、神经网络、神经/生理指标、预处理术语、统计模型、数据库检索式、题录、APA 引文和参考文献。

## 1. 独立调用原则

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流，用于普通心理学问卷、实验、干预、测量、临床/健康/发展心理学实证论文。
- `psych-cog-neuro-review`：认知神经科学工作流，用于 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合主题。
- `psych-literature-review-workflow`：新的通用综述工作流，用于不以神经/生理指标为核心的心理学综述。

若用户已经选择本 skill，就由本 skill 独立完成认知神经科学综述或实证/实验项目。不要写“调用另一个 skill”“转交给另一个 skill”“由其他 skill 调用本模块”。如发现用户目标明显不适合本 skill，只说明边界并请求用户确认是否仍按本 skill 执行。

`psych-review-workflow` 若仍存在，仅为旧版辅助/历史兼容材料，不作为三个主 skill 之一。

## 2. 适用场景

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

## 3. 运行模式

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

默认数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助检索，不单独声称完整）、CNKI、期刊官网、Zotero 本地库。

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

## 8. 文献与证据评级

正式阅读前先分类，再做 1–4 级相关性评级。相关性只表示与主题贴合度，不等同于方法质量。

| 等级 | 含义 | 处理 |
|---|---|---|
| 4 | 核心机制、核心范式、核心指标或关键实证证据 | 全文精读，进入机制矩阵和核心论证 |
| 3 | 直接支持某一机制、方法、范式或章节 | 摘要+方法+结果精读，必要时全文 |
| 2 | 背景相关，支持概念边界或方法背景 | 选择性阅读 |
| 1 | 边缘相关或用于排除理由 | 记录，不作为核心证据 |

同时单独评价：方法质量、样本适配度、神经/生理指标可靠性、范式有效性、统计/预处理透明度、理论贡献、引用价值、连接度。

神经/生理机制矩阵至少包括：文献、研究类型、样本、人群、范式、刺激、任务流程、行为指标、神经/生理指标、预处理方法、统计模型、关键发现、脑区/成分/频段/网络、理论机制、局限、可引用位置、证据强度。

## 9. 实验与分析硬约束

- 区分行为任务、主观量表、神经/生理指标和理论机制，不混同层级。
- 不用单一脑区或 ERP 成分过度解释复杂心理机制。
- 不伪造脑区激活、ERP 成分、频段效应、fMRI cluster、PSG 分期、眼动指标或预处理结果。
- 实验设计必须说明刺激、任务、试次、随机化、平衡、排除标准、样本量和伦理风险。
- EEG/ERP、fMRI、PSG、眼动和心理生理数据必须写明预处理决策、伪迹处理、排除标准、主要指标和分析模型。
- 若只是综述，不得暗示自己拥有原始神经数据。

建议产物：`task_paradigm_design.md`, `preprocessing_decision_log.md`, `eeg_erp_reporting_checklist.md`, `fmri_reporting_checklist.md`, `psg_sleep_reporting_checklist.md`, `eye_tracking_reporting_checklist.md`, `psychophysiology_reporting_checklist.md`。

## 10. HTML 星图与机制图

若用户要求星图，使用文献矩阵和机制矩阵生成 HTML 图。节点包括文献、理论、范式、变量、神经/生理指标、脑区/成分/频段/网络、核心结论。边包括引用关系、共同范式、共同指标、共同理论、变量路径和机制链。

权重建议：主题相关度 × 证据质量 × 机制贡献 × 方法透明度 × 连接度 × 新近性 × 权威性。必须说明权重只是辅助可视化，不等于真实因果强度。

## 11. 写作结构

根据任务类型生成综述或实证论文，但均需 APA 第 7 版兼容。

综述默认结构：引言、概念边界、理论与机制模型、范式与测量、主要证据、方法学评价、不一致发现、整合模型、未来方向、结论。

实证/实验论文默认结构：标题、摘要、引言、方法、结果、讨论、参考文献、表图、补充材料。

每个事实性、理论性、方法性或结果解释性主张都必须绑定来源或分析产物。写作时同步建立 `source_alignment_table`，不要写完后硬补引用。

## 12. Chrome + Zotero 边界

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。
- Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载；遇到异常警告立即停止。
- 不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 13. 模拟投稿与最终审核

默认模拟两套审查：中文心理学/认知神经科学相关期刊，以及英文心理学/认知神经科学/神经科学期刊。期刊 scope、格式、版面费、开放获取、AI policy 和投稿要求必须联网核查，不能依赖旧知识。

最终完成前必须通过：

- 文献与正文主张对齐。
- 神经/生理机制解释没有超出证据层级。
- 方法、预处理、统计计划和结果一致。
- APA 引文与参考文献一致。
- 综述或实证论文的任务类型表述准确。
- 模拟审稿意见已标注为模拟，不冒充真实期刊反馈。

## 14. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在仍有关键引用、方法、数据、伦理、统计或报告问题时声称“可直接投稿”。
