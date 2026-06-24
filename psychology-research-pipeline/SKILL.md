---
name: psychology-research-pipeline
description: Use this standalone Chinese-first skill for end-to-end empirical psychology paper workflows, including project scoping, research-question refinement, evidence search, Zotero ingestion, literature screening, hypothesis and variable-model construction, ethics/open-science planning, methods design, data management, statistical analysis, APA manuscript writing, source alignment, and simulated submission review. 这是“心理学实证论文工作流”，用于问卷、实验、干预、纵向/横断、心理测量、临床/健康/发展心理学等实证论文；本 skill 被选中后必须独立完成任务，不依赖其他 skill、总索引或共享模板；不要用于单纯综述写作、认知神经科学专用项目、伪造数据/文献、绕过权限、无人值守批量下载或真实投稿提交。
---

# Psychology Empirical Paper Workflow / 心理学实证论文工作流

本 skill 是三个主工作流之一，定位为**心理学实证论文从选题到投稿预备的独立工作流**。它服务于含数据、实验、问卷、干预、测量或统计分析的论文项目。文献综述在本流程中只服务于研究问题、理论模型、变量选择、方法设计和论文引言，不替代完整的独立综述项目。

默认语言为中文。必要英文保留于数据库检索式、量表名、统计方法、软件输出、APA 引文、参考文献、变量名和国际报告规范。

## 1. 独立调用原则

本 skill 被用户或 Codex 选中后，应**独立完成实证论文工作流**，不得把任务转交、拆分或依赖其他 skill。可以在边界判断时说明其他主 skill 更适合，但一旦继续使用本 skill，就必须在本文件范围内完成任务。

当前三个主 skill 的边界仅用于选择，不用于运行时互相调用：

- `psychology-research-pipeline`：心理学实证论文工作流。核心产物是研究方案、变量模型、数据分析、结果、讨论和投稿预备稿。
- `psych-cog-neuro-review`：认知神经科学工作流。适合 EEG/ERP、fMRI、PSG、眼动、生理指标、实验范式、脑机制或行为—神经整合主题。
- `psych-literature-review-workflow`：新的通用综述工作流。适合不以神经/生理指标为核心的心理学综述项目。

若用户目标是单纯综述，不使用本 skill。若用户目标是普通心理学实证论文，使用本 skill。若实证研究中偶然涉及神经或生理术语，本 skill 仍独立处理方法边界、报告规范和写作，不要求调用其他 skill。

`psych-review-workflow` 若仍存在，仅为旧版辅助/历史兼容材料，不作为三个主 skill 之一。

## 2. 适用场景

使用本 skill，当用户需要：

- 从研究兴趣推进到实证研究问题、假设和变量模型。
- 设计问卷研究、实验研究、干预研究、纵向/横断研究、临床/健康心理学研究、发展心理学研究或心理测量研究。
- 为实证论文检索理论、综述、方法和实证证据，并进行 Zotero 入库、筛选和小综述写作。
- 制定样本方案、量表/任务选择、研究程序、伦理与开放科学计划。
- 整理数据、制定统计分析计划、执行或解释分析、写 APA 论文和模拟投稿审稿。

不要使用本 skill，当任务只是：

- 单纯写综述、范围综述、系统综述或文献矩阵。
- 临时解释概念、润色单段文字、改参考文献格式。
- 用户要求伪造数据、伪造统计结果、伪造问卷来源、伪造伦理审批、伪造 DOI、伪造审稿意见。
- 用户要求绕过数据库权限、验证码、MFA、付费墙、下载限制或出版社条款。
- 用户要求真实投稿、支付费用、联系编辑或代替作者完成投稿系统操作。

## 3. 运行模式

首次运行时选择一个模式，并写入 `state.json` 和 `logs/decisions.md`。

| 模式 | 适用任务 | 最低要求 | 典型输出 |
|---|---|---|---|
| `lite` | 课程论文、早期选题、研究设计草案 | 选题、简检索、变量模型、方法草案 | project brief, seed papers, hypotheses, methods sketch |
| `standard` | 本科/研究生实证论文、普通投稿预备 | 00–11 全流程，含文献、方法、分析、写作和审稿 | research protocol, analysis plan, manuscript draft |
| `strict` | 投稿级实证论文、高风险数据/临床主题、注册报告预备 | 冻结协议、完整检索日志、分析计划、代码/数据审计、引用对齐 | auditable empirical paper package |

不要静默降低用户要求的模式。若数据、权限、时间或材料不支持 `strict`，记录 blocker，并明确降级假设。

## 4. 启动时的需求沟通

首次运行时先简短询问，除非用户已经给出答案。用户未回答时，可以用默认值继续，但必须记录为 `assumption`。

必要问题：

1. 当前是宽研究方向、已定题目，还是已有数据/实验材料？
2. 研究类型：横断、纵向、实验、干预、混合方法、心理测量、临床/健康心理学研究。
3. 目标用途：课程论文、毕业论文、开题、学位论文、中文期刊、英文期刊、注册报告。
4. 核心变量：自变量、因变量、中介、调节、协变量、分组变量、核心量表或任务。
5. 样本与对象：年龄、人群、临床/非临床、招募来源、样本量或已有 N。
6. 数据状态：无数据、已有问卷、已有实验数据、已有 SPSS/Excel/CSV/Mplus/AMOS 输出。
7. 分析工具：SPSS、PROCESS、AMOS、Mplus、R、Python、JASP 或其他。
8. 文献获取方式：是否允许 Chrome + Zotero Connector；Zotero collection；失败时是否使用文件夹手动导入。
9. 输出格式：Markdown、DOCX、CSV、Excel、图表、APA 参考文献、模拟审稿报告。

用户已明确回答时，不要重复询问。

## 5. 默认运行目录

```text
empirical_runs/<YYYYMMDD>_<short_topic>/
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
│   └── 05_论文引用/
├── 00_scope/
├── 01_standards_protocol/
├── 02_evidence_search/
├── 03_library_acquisition/
├── 04_screening_synthesis/
├── 05_methods_design/
├── 06_data_management/
├── 07_analysis/
├── 08_results_figures/
├── 09_manuscript/
├── 10_alignment_audit/
└── 11_submission_review/
```

不要覆盖旧文件。修订版使用 `_v2`、`_v3`，并记录修订原因。

## 6. 阶段总览

| 阶段 | 名称 | 目标 | 主要产物 |
|---|---|---|---|
| 00 | 项目定标 | 将兴趣转成可研究问题 | `project_brief.md`, `rq_hypotheses.md`, `construct_variable_map.csv`, `导师汇报版简表.md` |
| 01 | 标准与协议 | 确定报告规范、伦理与开放科学边界 | `empirical_protocol.md`, `reporting_plan.md`, `ethics_open_science.md` |
| 02 | 证据检索 | 为实证研究问题搜集核心理论、方法和实证证据 | `queries.md`, `search_log.csv`, `candidate_records.csv` |
| 03 | Zotero/全文获取 | 合法入库、去重、PDF 核验 | `zotero_manifest.csv`, `pdf_manifest.csv`, `acquisition_report.md` |
| 04 | 文献筛选与小综述 | 分类、评级、提取证据，服务引言和方法 | `screening_table.csv`, `literature_matrix.csv/xlsx/md`, `mini_review.md`, `claim_evidence_map.csv` |
| 05 | 方法设计 | 确定样本、量表、任务、程序和分析计划 | `methods_plan.md`, `measurement_table.csv`, `statistical_analysis_plan.md` |
| 06 | 数据管理 | 审计数据结构、变量命名、缺失与异常 | `data_dictionary.csv`, `data_audit.md`, `cleaning_log.md` |
| 07 | 统计分析 | 按冻结计划分析并记录偏离 | `analysis_script`, `analysis_outputs/`, `analysis_report.md`, `analysis_deviation_log.md` |
| 08 | 结果与图表 | 写作结果、表格、图和稳健性检查 | `results.md`, `tables/`, `figures/`, `robustness_checks.md` |
| 09 | 论文写作 | APA 兼容论文草稿 | `manuscript.md`, `manuscript.docx`, `references.bib`, `apa_references.md` |
| 10 | 对齐与审计 | 核查主张、引用、数字、表图和方法一致性 | `source_alignment_table.csv/xlsx`, `numeric_audit.md`, `claim_audit.md` |
| 11 | 模拟投稿审稿 | 模拟中文/英文期刊投稿前审查 | `journal_fit_memo.md`, `simulated_reviews.md`, `revision_matrix.csv` |

不要随意重排阶段。若某阶段失败，在同阶段修复；只有记录原因和影响范围后，才回到前一阶段。

## 7. 文献模块要求

文献检索是实证论文的支撑模块，不是独立综述替代品。

默认数据库：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普；用户明确要求时再作为附加数据库并记录理由。

文献分类至少包括：综述/元分析、理论概念、方法测量、横断实证、纵向实证、实验研究、干预研究、质性/混合方法、指南/共识。

相关性 1–4 级：

| 等级 | 含义 | 处理 |
|---|---|---|
| 4 | 核心文献，直接支撑研究问题、变量模型、方法或关键假设 | 全文精读，进入矩阵和引言核心引用 |
| 3 | 重要相关，支持某一章节或方法选择 | 摘要+方法+关键结果精读，必要时全文 |
| 2 | 背景相关，提供概念、边界或补充证据 | 摘要/讨论选择性阅读 |
| 1 | 边缘相关，只能用于背景或排除理由 | 记录后通常不进入正文核心 |

同时单独评价：方法质量、样本适配度、理论贡献、证据强度、引用价值、与本研究变量模型的连接度。

阅读矩阵至少包括：题录、DOI/PMID、研究类型、样本、人群、变量、测量工具、研究设计、统计方法、核心发现、局限、可引用位置、与本研究关系、相关性等级、质量评价、是否进入正文。

## 8. 方法与分析硬约束

- 先冻结研究问题、假设、变量和分析计划，再写结果。
- 不从相关关系推出因果；区分横断、纵向、实验和干预设计的推论边界。
- 不根据显著性事后改假设；探索性分析必须标注为 exploratory。
- 不伪造样本量、描述统计、信效度、模型拟合、p 值、置信区间、效应量或图表。
- 缺失值、异常值、反向计分、量表总分/维度分、排除标准和协变量处理必须记录。
- PROCESS、AMOS、Mplus、R 或 Python 输出要与正文数字逐项核对。
- 样本量、power analysis、可行性和伦理风险必须独立说明。

建议产物：`power_analysis_plan.md`, `sample_size_decision_log.md`, `variable_codebook.csv`, `missing_data_plan.md`, `assumption_checklist.md`, `analysis_deviation_log.md`。

## 9. 写作结构

默认 APA 第 7 版兼容：

1. Title / 中文题目与英文题目
2. Abstract / 摘要
3. Introduction / 引言：问题、理论、文献空白、研究目的与假设
4. Method / 方法：被试、工具、程序、伦理、数据分析
5. Results / 结果：描述统计、信效度、相关、模型、主分析、补充分析
6. Discussion / 讨论：主要发现、理论意义、实践意义、局限、未来方向
7. References / 参考文献
8. Tables and Figures / 表图
9. Supplementary materials / 补充材料

每个事实性、理论性、方法性或结果解释性主张都必须绑定来源或分析产物。写作时同步建立 `source_alignment_table`，不要写完后硬补引用。

## 10. Chrome + Zotero 边界

- 用户本人处理校园 VPN、统一认证、MFA、验证码、付费确认和数据库授权。
- Codex 不读取、不保存、不记录账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不绕过付费墙、下载限制、机器人检测、数据库条款或出版社限制。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载；遇到异常警告立即停止。
- 不把 PDF、Zotero 数据库、浏览器材料或账号信息提交到 GitHub。

## 11. 模拟投稿与最终审核

默认模拟两套审查：中文心理学/医学心理学相关期刊，以及英文心理学/健康心理学/临床心理学期刊。期刊 scope、格式、版面费、开放获取、AI policy 和投稿要求必须联网核查，不能依赖旧知识。

最终完成前必须通过：

- 文献与正文主张对齐。
- 数据、代码、表格、图和正文数字一致。
- 方法、伦理、统计计划和结果一致。
- APA 引文与参考文献一致。
- 结果解释没有超出设计允许范围。
- 模拟审稿意见已标注为模拟，不冒充真实期刊反馈。

## 12. 完成条件

只有在用户要求的阶段完成、关键 gate 通过、未解决风险列明后，才结束。返回运行目录、完成阶段、生成/修改文件、主要结论、验证结果、未解决 blocker 和下一步建议。不得在仍有关键引用、方法、数据、伦理、统计或报告问题时声称“可直接投稿”。
