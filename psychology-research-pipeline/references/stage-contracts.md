# 阶段契约

## 目录与标识

每次运行位于 `<项目>/实证论文运行/<run-id>/`。使用 UTF-8、ISO 8601 时间和 RFC 4180 CSV。未知值写 `unknown`，不得猜测。

稳定标识：`run_id`、`candidate_id`、`study_id`、`claim_id`。Zotero item key 与 BibTeX key 分开保存。

## 阶段 gate

### 00_scope — `00_项目定标`

必需：`项目定标简报_project_brief.md`、`研究问题与假设_research_questions_hypotheses.md`、`构念变量关系表_construct_variable_map.csv`。

通过条件：主要问题、目标人群、波次、构念、观察变量、主要估计对象和推论边界明确；数据能回答问题；关键未知项已解决或阻断。

### 01_protocol — `01_标准与协议`

必需：`实证研究协议_empirical_protocol.md`、`报告规范计划_reporting_plan.md`、`伦理与开放科学_ethics_open_science.md`。

通过条件：假设、主要/次要结局、纳排、分析族、偏离政策、伦理事实、数据共享限制和适用规范冻结。不得伪造伦理审批号。

### 02_search — `02_证据检索`

必需：`检索式记录_queries.md`、`检索记录_search_log.csv`、`候选文献表_candidate_records.csv`。

检索表至少包含 `search_id,database,platform,query,filters,run_at,result_count,export_file,notes`；候选表至少包含 `candidate_id,title,authors,year,doi,pmid,source,abstract,landing_url,database,search_id,dedup_status`。

### 03_library — `03_Zotero与全文获取`

必需：`Zotero入库清单_zotero_manifest.csv`、`PDF全文清单_pdf_manifest.csv`、`全文获取报告_acquisition_report.md`。

通过条件：每个候选有 `complete`、`metadata-only`、`duplicate-skipped`、`access-blocked` 或 `failed-validation` 状态；complete 项具有可读 PDF 子附件且题录一致。

### 04_synthesis — `04_文献筛选与小综述`

必需：`文献筛选表_literature_screening.csv`、`文献阅读矩阵_literature_matrix.csv`、`小综述_mini_review.md`、`主张证据对应表_claim_evidence_map.csv`。

通过条件：纳排理由、同一研究多报告关联、证据位置、相关性与方法质量分开记录；矛盾和零结果未被删除；关键主张可追溯。

### 05_methods — `05_方法设计`

必需：`方法设计方案_methods_plan.md`、`测量工具表_measurement_table.csv`、`统计分析计划_statistical_analysis_plan.md`。

通过条件：样本流、计分、信效度、测量不变性、估计对象、模型、估计量、缺失、异常、协变量、聚类、性别比较、多重检验、诊断、稳健性、输出和偏离规则均预先定义。

### 06_data — `06_数据管理`

必需：`数据字典_data_dictionary.csv`、`数据质量审计_data_audit.md`、`数据清理记录_cleaning_log.csv`。

通过条件：源文件哈希、ID、波次连接、重复、异常编码、范围、反向计分、总分公式、缺失、流失、分布、零膨胀、聚类和隐私风险完成审计；所有修订可追溯且未覆盖原始数据。结构化 issue 只能使用其声明的处置类型；ID 错配、重复和计分错误不得用分布或模型适配解除。需要行级定位时使用被 `.gitignore` 排除的 `.private/` 伪匿名登记。

### 07_analysis — `07_统计分析`

必需：`统计分析报告_analysis_report.md`、`分析偏离记录_analysis_deviation_log.csv`、`分析清单_analysis_manifest.json`、`结果表格_results_tables.md`。

manifest 必须记录源文件及哈希、软件与包版本、代码文件、随机种子、冻结计划、偏离和输出。通过条件：代码从只读源数据真实执行；代码和输出哈希匹配；模型识别和收敛；不存在未处理的负方差或不可接受标准化估计；估计、不确定性、拟合、诊断和偏离完整。生成代码不等于完成分析。

### 08_results — `08_结果与图表`

必需：`结果写作稿_results.md`、`图表计划_figure_table_plan.md`、`稳健性检查_robustness_checks.md`。

通过条件：正文、表和图数字一致；主要与探索性结果分开；零结果和相反结果报告；稳健性与主结果关系得到解释。

### 09_manuscript — `09_论文正文`

必需：`论文正文_manuscript.md`、`参考文献_references.bib`、`APA参考文献_apa_references.md`。

通过条件：题目至声明完整；方法与代码一致；结果与输出一致；观察性推论措辞克制；敏感人群、伦理、数据和代码可用性说明明确。

### 10_alignment — `10_对齐审计`

必需：`来源对齐表_source_alignment_table.csv`、`数字核查报告_numeric_audit.md`、`主张核查报告_claim_audit.md`。

通过条件：所有关键主张为 direct/qualified；unsupported/overextended 均已删除、降级或补证；样本量、系数、区间、p 值、拟合和表图逐项核对。

### 11_review — `11_模拟投稿审稿`

必需：`模拟审稿意见_simulated_reviews.md`、`修改矩阵_revision_matrix.csv`、`作者回复草稿_response_to_reviewers.md`、`最终审计_final_audit.md`。

通过条件：目标期刊官网与文章类型已实时核查；URL 属于声明的期刊或出版商官方域名；政策页面快照、核查日期与 SHA-256 完整；理论、方法、统计、测量、开放科学和完整性审查均有结论；重大问题已解决或明确拒绝并说明理由；模拟性质醒目标注。

## 交接与失效

每阶段记录输入、输出、冻结决策、未决非关键问题和下一阶段不得静默改变的假设。上游变更使下游产物失效时，在 `文件清单_manifest.json` 标为 `stale`，回到最早受影响阶段重新通过 gate。

## 机器接口与返回码

统一入口为 `scripts/pipeline.py`。成功返回 `0`；证据不足、审计 flag 未决、模型输出无效或投稿条件不满足返回 `3`；阶段 gate 内容不合格返回 `1`；命令或路径参数错误返回 `2`。标准输出优先为 UTF-8 JSON，便于自动编排和复核。

`verify-run` 检查十二阶段但不推进；`autopilot` 从 `current_stage` 开始逐项 `advance`，在第一个失败 gate 停止。自动推进不得把模板存在、代码已生成或模拟审稿等同于研究内容有效、分析已执行或真实期刊认可。
