---
name: psych-cog-neuro-review
description: Use this standalone Chinese-first main skill folder for cognitive neuroscience review workflows. 这是“认知神经科学综述工作流”，用于围绕脑机制、实验范式、行为—神经/生理整合、EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理、睡眠、情绪、记忆、认知控制、威胁/奖赏加工等主题开展综述；本 skill 被选中后必须在本主 skill 文件夹范围内独立完成任务，可使用本目录下 subskills/、templates/、checklists/、rubrics/、examples/，但不依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板；本地生成文件默认使用“中文主名_英文兼容名.扩展名”；不要用于普通综述、普通问卷论文、伪造神经机制/数据/文献、绕过权限、保存凭据、无人值守批量下载或真实投稿提交。
---

# 认知神经科学综述工作流

本 skill 是三个主工作流之一，定位为**认知神经科学、脑机制、实验范式和行为—神经/生理整合主题的综述工作流**。本轮强化的核心是综述：机制综述、理论综述、方法学综述、测量/范式综述、范围综述、系统综述预备和元分析预备。

实验范式、神经/生理方法、预处理与分析计划在本 skill 中主要用于评价文献质量、提取方法信息、比较研究设计和写作方法学综述；除非用户另行明确要求，不把本 skill 当作新实证实验项目的主入口。

默认语言为中文。必要英文保留于实验范式、脑区、神经网络、成分名、预处理术语、统计模型、数据库检索式、题录、DOI/PMID、APA 引文和参考文献。

## 1. 独立调用原则

本 skill 被用户或 Codex 选中后，应**在本主 skill 文件夹范围内独立完成认知神经科学综述工作流**，范围包括主 `SKILL.md` 与本目录下的 `subskills/`、`templates/`、`checklists/`、`rubrics/`、`examples/`。不得把任务转交、拆分或依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板。

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流，用于普通心理学问卷、实验、干预、测量、临床/健康/发展心理学实证论文。
- `psych-cog-neuro-review`：认知神经科学综述工作流，用于 EEG/ERP、fMRI、PSG、眼动、NIRS、生理指标、实验范式、脑机制或行为—神经整合主题的综述。
- `psych-literature-review-workflow`：通用心理学综述工作流，用于不以神经/生理指标为核心的心理学综述。

## 2. 支持的综述类型

支持：机制综述、理论综述、方法学综述、实验范式综述、测量/指标综述、范围综述、系统综述预备、元分析预备。

不要在没有正式协议、完整检索日志、纳排标准、筛查记录、方法质量评价和来源对齐时，把文章声称为“系统综述”或“可投稿终稿”。

## 3. 内部分工

### subskills/

1. `cog-neuro-scope`：方向与任务定标，明确综述问题和机制边界。
2. `evidence-search`：认知神经科学理论、范式、指标和实证证据检索。
3. `zotero-ingest`：Zotero 入库和 PDF/题录核验。
4. `literature-screen`：认知神经科学文献分类和评级。
5. `paradigm-design`：实验范式提取、比较和质量评价。
6. `neuro-methods-design`：EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理等方法评价。
7. `neuro-data-analysis`：预处理与分析方案提取和透明性评价。
8. `mechanism-synthesis`：行为—神经/生理机制整合。
9. `source-alignment`：机制主张与原文证据对齐。
10. `manuscript-write`：认知神经科学综述正文写作。
11. `submission-review`：顶刊预备强度的模拟综述审稿。

### templates/ checklists/ rubrics/ examples/

- `templates/`：方向定标、机制矩阵、范式提取、神经/生理方法、预处理计划、来源对齐和审稿模板。
- `checklists/`：EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理、实验范式、预处理与分析、机制对齐和停止条件检查表。
- `rubrics/`：机制理论贡献、范式质量、神经/生理方法质量、预处理透明性、行为—神经整合、机制引用风险和顶刊预备度评分表。
- `examples/`：认知神经综述、范式综述、EEG/ERP、fMRI、睡眠与情绪记忆、顶刊级模拟审稿示例。

## 4. 本地文件命名

本地运行时，文件夹名和文件名默认采用：

```text
中文主名_英文兼容名.扩展名
```

示例：

```text
机制矩阵_neural_mechanism_matrix.csv
实验范式设计_paradigm_design.md
神经生理方法方案_neuro_methods_plan.md
预处理计划_preprocessing_plan.md
来源对齐表_source_alignment_table.csv
```

若因软件或脚本限制必须使用纯英文名，必须在 `日志/决策记录_decisions.md` 中记录原因，并提供中文对照。

## 5. 运行模式

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 早期选题、课程综述、机制方向判断 | 方向定标、种子文献、初步机制图 | 方向定标简报、种子矩阵、机制草图 |
| `standard` | 研究生综述、学位论文综述、中文/英文论文预备 | 检索、筛选、矩阵、机制整合、正文、来源对齐 | 证据矩阵、机制模型、综述草稿 |
| `strict` | 范围综述、系统综述预备、投稿级机制综述 | 正式协议、完整检索日志、严格筛查、质量评价、完整对齐 | 可审计综述包、方法质量审计、机制来源对齐 |
| `top-journal-prep` | 顶刊预备审查强度 | strict 基础上增加反对性审稿、机制贡献评分、方法透明性评分和不可投稿风险清单 | 顶刊预备度报告、全角色模拟审稿、修改矩阵 |

不得承诺发表顶级文章。只能提供顶刊预备审查强度的流程、材料和质量控制。

## 6. 启动时必须确认

1. 当前是宽方向，还是已经聚焦后的认知神经科学综述主题？
2. 综述类型：机制综述、理论综述、方法学综述、范式综述、指标综述、范围综述、系统综述预备、元分析预备。
3. 核心边界：构念、人群、年龄段、临床/非临床、human/animal/computational、实验范式、神经/生理指标。
4. 目标用途：课程作业、开题、学位论文、中文期刊、英文期刊、投稿预备。
5. 运行模式：`lite`、`standard`、`strict`、`top-journal-prep`。
6. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero 目标 collection；失败时是否下载到文件夹由用户手动导入。
7. 输出格式：Markdown、DOCX、CSV、Excel、HTML、BibTeX/RIS、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问；用户未回答时，可以使用默认值继续，但必须记录为 assumption。

## 7. 默认数据库范围

默认数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助检索，不单独声称完整）、CNKI、期刊官网、Zotero 本地库。

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。若用户明确要求，或某一认知神经科学主题确有必要，可作为附加数据库，并在协议中记录理由、检索式、结果数和局限。

## 8. 默认运行目录

```text
认知神经科学运行/<日期>_<简短主题>/
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
│   ├── 05_机制图与星图/
│   └── 06_正文与方法/
├── 00_方向与任务定标/
├── 01_协议冻结/
├── 02_证据检索/
├── 03_Zotero与全文获取/
├── 04_分类与筛查/
├── 05_证据矩阵/
├── 06_机制模型/
├── 07_范式与方法评价/
├── 08_预处理与分析评价/
├── 09_正文写作/
├── 10_来源与方法审计/
└── 11_模拟投稿审稿/
```

## 9. 阶段总览

| 阶段 | 名称 | 主要产物 |
|---|---|---|
| 00 | 方向与任务定标 | `方向定标简报_cog_neuro_scope.md`, `机制范围说明_mechanism_scope.md` |
| 01 | 协议冻结 | `综述协议_review_protocol.md`, `概念关系图_concept_map.md`, `纳入排除标准_inclusion_exclusion.md` |
| 02 | 证据检索 | `检索式记录_queries.md`, `数据库检索记录_database_search_log.csv`, `候选文献表_candidate_records.csv` |
| 03 | Zotero/全文获取 | `Zotero入库清单_zotero_manifest.csv`, `PDF全文清单_pdf_manifest.csv`, `全文获取报告_acquisition_report.md` |
| 04 | 分类与筛查 | `文献筛选表_literature_screening.csv`, `相关性评级表_relevance_ratings.csv` |
| 05 | 证据矩阵 | `文献阅读矩阵_literature_matrix.csv/xlsx/md`, `机制矩阵_neural_mechanism_matrix.csv`, `质量评价表_quality_appraisal.csv` |
| 06 | 机制模型 | `机制模型说明_mechanism_model.md`, `主张证据对应表_claim_evidence_map.csv` |
| 07 | 范式与方法评价 | `实验范式评价_paradigm_evaluation.md`, `神经生理方法评价_neuro_methods_evaluation.md` |
| 08 | 预处理与分析评价 | `预处理透明性评价_preprocessing_transparency.md`, `分析方法评价_analysis_methods_evaluation.md` |
| 09 | 正文写作 | `综述正文_manuscript.md`, `综述正文_manuscript.docx`, `APA参考文献_apa_references.md` |
| 10 | 来源与方法审计 | `来源对齐表_source_alignment_table.csv`, `机制主张审计_mechanism_claim_audit.md`, `方法审计报告_method_audit.md` |
| 11 | 模拟投稿审稿 | `模拟审稿意见_simulated_reviews.md`, `修改矩阵_revision_matrix.csv`, `作者回复草稿_response_to_reviewers.md` |

## 10. 强制停止条件

遇到以下情况必须停止并汇报，不得继续生成“完成稿”：

- 没有检索记录，不得声称完成正式综述。
- 没有纳排标准，不得声称完成范围综述或系统综述预备。
- 没有全文，不得做强引用或页码级来源对齐。
- 没有阅读矩阵和机制矩阵，不得写机制综述正文。
- 没有方法信息，不得评价 EEG/ERP、fMRI、PSG、眼动、NIRS 或心理生理证据质量。
- 没有来源对齐，不得声称“可投稿”。
- 发现伪造脑区结果、ERP 成分、fMRI 激活、PSG 分期、眼动指标、NIRS 指标、统计结果或文献来源时，必须生成 `停止原因与补救清单_stop_reason_and_fix.md`。

## 11. 顶刊预备质量门槛

顶刊预备不是发表承诺，而是审查强度。必须至少经过以下 gate：

1. 机制问题重要、边界清晰、理论贡献明确。
2. 检索策略、数据库、时间、检索式和限制条件可追溯。
3. 文献筛选、方法质量评价和机制矩阵完整。
4. 神经/生理方法、预处理与分析透明性可评价。
5. 行为结果、主观量表、神经/生理指标和理论机制分层整合。
6. 每个脑区、网络、ERP 成分、睡眠阶段、眼动指标、NIRS 指标或心理生理指标主张都有来源支持。
7. 模拟审稿包括主编、理论机制、实验范式、神经/生理方法、预处理与分析、统计、开放科学、引用机制对齐、格式和反对性审稿。

## 12. Chrome + Zotero 边界

用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据；不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制；不使用盗版论文站、影子图书馆、PDF bot 或泄露账号；不无人值守高速批量下载；不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 13. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在关键机制证据、方法、预处理、统计或引用问题未解决时声称“可直接投稿”。