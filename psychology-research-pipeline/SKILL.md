---
name: psychology-research-pipeline
description: Use this standalone Chinese-first main skill folder for end-to-end empirical psychology paper workflows. 这是“心理学实证论文工作流”，用于问卷、实验、干预、纵向/横断、心理测量、临床/健康/发展心理学等实证论文；本 skill 被选中后必须在本主 skill 文件夹范围内独立完成任务，可使用本目录下 subskills/、templates/、checklists/、rubrics/、examples/，但不依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板；本地生成文件默认使用“中文主名_英文兼容名.扩展名”；不要用于单纯综述写作、认知神经科学专用项目、伪造数据/文献、绕过权限、无人值守批量下载或真实投稿提交。
---

# 心理学实证论文工作流

本 skill 是三个主工作流之一，定位为**心理学实证论文从选题到投稿预备的独立工作流**。它服务于含数据、实验、问卷、干预、测量或统计分析的论文项目。文献综述在本流程中只服务于研究问题、理论模型、变量选择、方法设计和论文引言，不替代完整独立综述项目。

默认语言为中文。必要英文保留于数据库检索式、量表名、变量名、统计方法、软件输出、APA 引文、参考文献、文件扩展名和国际报告规范。

## 1. 独立调用原则

本 skill 被用户或 Codex 选中后，应**在本主 skill 文件夹范围内独立完成实证论文工作流**，范围包括主 `SKILL.md` 与本目录下的 `subskills/`、`templates/`、`checklists/`、`rubrics/`、`examples/`。不得把任务转交、拆分或依赖其他主 skill、旧顶层辅助 skill、总索引或共享模板。

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流。核心产物是研究方案、变量模型、数据分析、结果、讨论和投稿预备稿。
- `psych-cog-neuro-review`：认知神经科学工作流。适合 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合主题。
- `psych-literature-review-workflow`：新的通用综述工作流。适合不以神经/生理指标为核心的心理学综述项目。

若用户目标是单纯综述，不使用本 skill。若用户目标是普通心理学实证论文，使用本 skill。若实证研究中偶然涉及神经或生理术语，本 skill 仍独立处理方法边界、报告规范和写作，不要求调用其他 skill。

## 2. 内部分工

### subskills/

分 skill 负责执行细节。推荐顺序：

1. `project-scope`：选题、研究问题、假设、变量模型。
2. `evidence-search`：理论、方法、量表和实证依据检索。
3. `zotero-ingest`：Chrome + Zotero Connector 入库和 PDF/题录核验。
4. `literature-screen`：文献分类、筛选、小综述和证据矩阵。
5. `methods-design`：样本、量表、任务、伦理、开放科学和分析计划。
6. `data-analysis`：数据审计、统计分析、结果解释和偏离记录。
7. `reporting-standards`：STROBE、CONSORT/SPIRIT、APA JARS、测量研究和开放科学报告规范。
8. `manuscript-write`：APA 实证论文写作。
9. `source-alignment`：正文主张、参考文献、统计数字、表图和方法描述对齐。
10. `submission-review`：顶刊预备强度的模拟投稿审稿和修改矩阵。

### templates/ checklists/ rubrics/ examples/

- `templates/`：提供可直接填写的研究方案、矩阵、分析计划、来源对齐和审稿模板。
- `checklists/`：提供强制检查清单，包括 APA JARS、STROBE、CONSORT/SPIRIT、开放科学、统计分析和停止条件。
- `rubrics/`：提供 1–5 分评分标准，区分“学位论文可用”“普通期刊可用”“高水平期刊可用”“顶刊预备强度”。
- `examples/`：提供 lite/standard/strict 启动示例和高强度模拟审稿示例。

## 3. 本地文件命名

本地运行时，文件夹名和文件名默认采用：

```text
中文主名_英文兼容名.扩展名
```

示例：

```text
文献阅读矩阵_literature_matrix.csv
统计分析计划_statistical_analysis_plan.md
来源对齐表_source_alignment_table.csv
模拟审稿意见_simulated_reviews.md
```

若因软件或脚本限制必须使用纯英文名，必须在 `日志/决策记录_decisions.md` 中记录原因，并提供中文对照。

## 4. 运行模式

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 课程论文、早期选题、研究设计草案 | 选题、简检索、变量模型、方法草案 | 项目定标、种子文献、假设、方法草案 |
| `standard` | 本科/研究生实证论文、普通投稿预备 | 00–11 全流程，含文献、方法、分析、写作和审稿 | 研究协议、分析计划、论文草稿 |
| `strict` | 投稿级实证论文、高风险数据/临床主题、注册报告预备 | 冻结协议、完整检索日志、分析计划、代码/数据审计、引用对齐 | 可审计实证论文包 |
| `top-journal-prep` | 顶刊预备审查强度 | 在 strict 基础上增加反对性审稿、开放科学审计、理论贡献评分和不可投稿风险清单 | 顶刊预备度报告、全角色模拟审稿、修改矩阵 |

不得承诺发表顶级文章。只能提供顶刊预备审查强度的流程、材料和质量控制。

## 5. 启动时必须确认

1. 当前是宽研究方向、已定题目，还是已有数据/实验材料？
2. 研究类型：横断、纵向、实验、干预、混合方法、心理测量、临床/健康心理学研究。
3. 目标用途：课程论文、毕业论文、开题、学位论文、中文期刊、英文期刊、注册报告或顶刊预备。
4. 核心变量：自变量、因变量、中介、调节、协变量、分组变量、核心量表或任务。
5. 样本与对象：年龄、人群、临床/非临床、招募来源、样本量或已有 N。
6. 数据状态：无数据、已有问卷、已有实验数据、已有 SPSS/Excel/CSV/Mplus/AMOS 输出。
7. 分析工具：SPSS、PROCESS、AMOS、Mplus、R、Python、JASP 或其他。
8. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero collection；失败时是否使用文件夹手动导入。
9. 输出格式：Markdown、DOCX、CSV、Excel、图表、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问；用户未回答时，可以用假设继续，但必须写入 `日志/决策记录_decisions.md`。

## 6. 默认运行目录

```text
实证论文运行/<日期>_<简短主题>/
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
│   └── 05_论文引用/
├── 00_项目定标/
├── 01_标准与协议/
├── 02_证据检索/
├── 03_Zotero与全文获取/
├── 04_文献筛选与小综述/
├── 05_方法设计/
├── 06_数据管理/
├── 07_统计分析/
├── 08_结果与图表/
├── 09_论文正文/
├── 10_对齐审计/
└── 11_模拟投稿审稿/
```

不要覆盖旧文件。修订版使用 `_v2`、`_v3`，并记录修订原因。

## 7. 阶段总览

| 阶段 | 名称 | 主要产物 |
|---|---|---|
| 00 | 项目定标 | `项目定标简报_project_brief.md`, `研究问题与假设_research_questions_hypotheses.md`, `构念变量关系表_construct_variable_map.csv` |
| 01 | 标准与协议 | `实证研究协议_empirical_protocol.md`, `报告规范计划_reporting_plan.md`, `伦理与开放科学_ethics_open_science.md` |
| 02 | 证据检索 | `检索式记录_queries.md`, `检索记录_search_log.csv`, `候选文献表_candidate_records.csv` |
| 03 | Zotero/全文获取 | `Zotero入库清单_zotero_manifest.csv`, `PDF全文清单_pdf_manifest.csv`, `全文获取报告_acquisition_report.md` |
| 04 | 文献筛选与小综述 | `文献筛选表_literature_screening.csv`, `文献阅读矩阵_literature_matrix.csv/xlsx/md`, `小综述_mini_review.md` |
| 05 | 方法设计 | `方法设计方案_methods_plan.md`, `测量工具表_measurement_table.csv`, `统计分析计划_statistical_analysis_plan.md` |
| 06 | 数据管理 | `数据字典_data_dictionary.csv`, `数据质量审计_data_audit.md`, `数据清理记录_cleaning_log.md` |
| 07 | 统计分析 | `统计分析报告_analysis_report.md`, `分析偏离记录_analysis_deviation_log.csv`, `结果表格_results_tables.md` |
| 08 | 结果与图表 | `结果写作稿_results.md`, `图表计划_figure_table_plan.md`, `稳健性检查_robustness_checks.md` |
| 09 | 论文写作 | `论文正文_manuscript.md`, `论文正文_manuscript.docx`, `APA参考文献_apa_references.md` |
| 10 | 对齐与审计 | `来源对齐表_source_alignment_table.csv`, `数字核查报告_numeric_audit.md`, `主张核查报告_claim_audit.md` |
| 11 | 模拟投稿审稿 | `模拟审稿意见_simulated_reviews.md`, `修改矩阵_revision_matrix.csv`, `作者回复草稿_response_to_reviewers.md` |

## 8. 强制停止条件

遇到以下情况必须停止并汇报，不得继续生成“完成稿”：

- 没有数据，不得写结果。
- 没有统计输出，不得写 p 值、效应量、置信区间或模型拟合指标。
- 没有全文，不得做强引用或页码级来源对齐。
- 没有量表来源，不得写“采用某量表”或声称信效度。
- 没有伦理信息，不得声称伦理合规。
- 没有期刊官网核查，不得生成最终投稿结论。
- 没有来源对齐，不得声称“可投稿”。
- 发现数据、引文、方法或统计结果无法核验时，必须生成 `停止原因与补救清单_stop_reason_and_fix.md`。

## 9. 顶刊预备质量门槛

顶刊预备不是发表承诺，而是审查强度。必须至少经过以下 gate：

1. 研究问题清晰、理论贡献明确，非重复性选题。
2. 样本、设计、测量和分析计划能支持研究推论。
3. 数据质量、缺失、异常、反向计分和剔除标准可审计。
4. 统计模型、效应量、置信区间、稳健性检查和探索性分析标注清楚。
5. 开放科学材料、数据、代码、协议和限制说明明确。
6. 每个关键主张都有来源或数据输出支撑。
7. 模拟审稿包括主编、理论、方法、统计、测量、开放科学、格式和反对性审稿。
8. 不满足 gate 时，不得写“可直接投稿”，只能写“待补充后再评估”。

## 10. Chrome + Zotero 边界

用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据；不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制；不使用盗版论文站、影子图书馆、PDF bot 或泄露账号；不无人值守高速批量下载；不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 11. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在关键引用、方法、数据、伦理、统计或报告问题未解决时声称“可直接投稿”。