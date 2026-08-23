# 文献操作核心合同

本合同统一“检索—题录—Zotero—PDF—阅读—证据—补检索—方法判断—模拟审稿”的可审计操作。领域 skill 可增加字段和门槛，但不得降低本合同。三个主 skill 必须各自携带本文件，运行时不跨 skill 依赖。

## 1. 文件治理与状态

1. 执行前盘点现有正式文件、上轮结果和本轮拟写入内容；先识别唯一活动运行、历史归档和临时区。
2. 文件默认使用“中文主名_英文兼容名.扩展名”；同一稳定职责只保留一个正式文件。
3. 优先追加记录、更新状态、补字段或原位重建；不得为“最新版”、日期或单批结果创建 `_v2`、`_v3`、平行清单或平行主运行。
4. 原始数据和数据库原始导出只读。刷新派生汇总时保留轮次、来源和变更记录，不删除或无痕覆盖旧结果。
5. 新文件只在现有文件无法承载且审计、软件接口或明确交付确有必要时创建，数量最少；记录路径、用途、不能复用的文件及原因。临时转换只进既有临时区，结束时清理。
6. 文件存在不等于阶段完成。超时、浏览器状态不明或脚本返回不完整时写 `unknown`/`needs-verification`，不得写成功。

## 2. 检索路线

### 路径 4：默认路径

使用 Codex 可控的内置浏览器和用户已完成的合法机构登录：

1. Codex 在数据库页面执行检索、筛选和结果核对。
2. 从数据库导出 RIS、BibTeX 或 CSV；原始导出不可覆盖，并登记数据库、平台、精确检索式、过滤器、执行时间、结果数和导出路径。
3. 本地解析原始导出，写入“历轮全部已见题录”主表。
4. 对已见主表做差集后，只有真正新增且筛选保留的题录进入 Zotero 父条目导入。
5. Codex不代替用户处理登录、MFA、验证码、许可确认或付费，也不读取 cookie、token 或凭据。

### 路径 3：浏览器兼容回退

当内置浏览器无法完成数据库导出或页面兼容性不足时，使用用户明确授权控制的外置浏览器执行同一检索和导出；下载 PDF 可由用户在其已认证浏览器中完成。路径 3 与路径 4 使用同一日志、候选主表和去重规则，不能形成平行数据链。

### Zotero Connector 的边界

Connector 仅适合单篇页面或数据库无法提供结构化批量导出时的补充保存。批量题录应优先使用数据库原始导出后本地导入父条目。Connector 不能替代原始检索结果、历轮已见主表或数据库检索日志。

## 3. 每轮检索与历轮查重

每轮固定顺序：

```text
冻结的检索问题与数据库专用检索式
→ 本轮数据库原始导出
→ 追加到历轮全部已见题录主表
→ 与历轮已见记录求差集
→ 仅新增题录进入筛选
→ 筛选保留项进入父条目清单和 Zotero
→ 核验 Zotero 附件状态与 PDF 全文清单
→ 原位重建当前缺 PDF 下载队列
```

“已见”包括历轮原始检索中出现但后来未筛选、被排除或未入 Zotero 的记录。只拿 Zotero 父条目或 PDF 状态查重是不合格的。原始导出丢失且无法恢复时必须披露重复风险，不得宣称已完成历轮排除。

查重优先级：DOI → PMID/数据库稳定 ID → 规范题名 + 首位作者 + 年份。记录级去重与同一研究多报告识别是两件事：前者合并题录身份，后者保留各报告并用研究家族关联。

### 候选文献主表

优先复用 `候选文献表_candidate_records.csv`。最低字段为：

```text
candidate_id,title,authors,first_author,year,doi,pmid,database_ids,
source_databases,search_ids,raw_export_files,first_seen_round,last_seen_round,
appearance_count,screening_status,zotero_item_key,zotero_attachment_status,
normalized_title,identity_key,record_status,notes
```

- `candidate_id` 稳定且不复用。
- 多数据库、多轮命中追加到复数字段，不能覆盖首次来源。
- 每个原始导出必须能追溯到 `search_id` 和批次/轮次。
- 检索日志最低字段：`search_id,database,platform,query,filters,run_at,result_count,export_file,notes`。

## 4. 阅读反馈驱动的补检索

新一轮正式检索前，联合读取当前阅读矩阵、证据覆盖台账、证据缺口、小综述和上一轮检索日志。检索计划逐项写明：

- 触发它的已读证据或证据槽缺口；
- 精准问题、优先级、概念块和目标证据类型；
- 每个数据库可直接执行的专用语法；
- 停止条件；
- 与历轮全部已见题录的去重基准。

不得机械沿用上一轮检索式，不得因主结果方向或显著性调整检索方向，不得用相邻或更宽泛构念悄悄替代冻结构念。优先更新现有检索计划、检索日志和缺口文件，不为每轮另建同用途备忘录。

## 5. 父条目、附件与 PDF 队列

### 父条目导入

1. 导入前对“候选主表 + 父条目清单 + Zotero 目标集合”三方查重。
2. 结构化 RIS/BibTeX/CSV 只导入筛选保留的新增父条目；默认不随题录导入附件。
3. 导入后核验父条目 key、题名、作者、年份、DOI、目标集合和父/附件关系。
4. 本轮导入日志必须区分 `imported`、`duplicate-skipped`、`failed-validation`、`unknown`。
5. 超时后先实时查询 Zotero 再重试，禁止因状态不明生成重试副本。

`Zotero入库清单_zotero_manifest.csv`最低字段：

```text
candidate_id,zotero_item_key,title,year,doi,collection,attachment_key,
attachment_status,validation_status,source_url,notes
```

### 缺 PDF 下载队列

通用的当前队列优先原位重建；用户明确要求独立批次交付时，才最少新增一个批次队列。推荐字段：

```text
batch,candidate_id,doi,url,title,year,evidence_role,search_family,
zotero_collection,zotero_item_key,pdf_status,notes
```

队列只列筛选保留、父条目身份明确且当前没有可读正文 PDF 的记录。队列不是失败清单，也不能据此宣称已尝试下载。

### 下载后核验与挂载

用户表示下载完成后：

1. 读取下载目录、本批队列、父条目清单和 Zotero 附件状态。
2. 按 DOI 优先；无 DOI 时按规范题名 + 首位作者 + 年份建立唯一映射。
3. 验证 `%PDF-` 文件头、合理页数、首页题名/作者/DOI；HTML 错误页、补充材料、损坏文件或错文不得作为正文 PDF。
4. 不新建父条目。脚本使用 `Zotero.Items.getByLibraryAndKey(1, key)` 取得父条目，已有可读 PDF 时跳过，使用 `Zotero.Attachments.importFromFile({file, parentItemID: parent.id})` 挂载。
5. 脚本逐条捕获 `parent-not-found`、`file-not-found`、`already-has-pdf`、`ambiguous-match` 和导入异常，并返回 `imported/skipped/failed` 明细。
6. 根据脚本返回值只读核验附件可打开后，再更新 Zotero/PDF 清单和队列；不删除用户下载文件。

唯一下载失败清单只统计实际执行过下载的批次。以上轮未解决项和本轮实际下载队列为母集；只有正文 PDF 验证通过且唯一映射到既有父条目后才移除。最低字段：

```text
batch,zotero_item_key,doi,url,title,download_status,failure_reason,last_checked
```

## 6. 阅读、研究家族与证据结构

固定顺序：定标冻结 → 字段对齐 → 研究家族预识别 → 分层精读与主张入账 → 设计适配质量评价 → 独立 Reviewer B → 按研究综合。

### 分层阅读

按用途和相关性决定阅读深度，不按期刊声望、引用数或结果方向分层：

1. **1级：明显排除或弱相关**。只读题名、摘要和关键词，记录排除理由，不进入证据综合。
2. **2级：背景或相邻构念**。读摘要、引言、讨论/结论和关键参考文献，提取背景用途与边界；不能承担核心效应主张。
3. **3级：重要理论、测量或方法文献**。执行三轮用途匹配的全文定向阅读，重点核验对应理论、量表、方法、适用条件和限制。
4. **4级：核心直接证据**。完整执行三轮六模块深读，进入阅读矩阵、证据账本、主张表和 Reviewer B 复核。

摘要只能形成 `blocked` 或待全文核验记录，不能确认效应、方法细节或强主张。所有全文纳入论文至少完成与其用途匹配的三轮阅读；没有全文者保持 `blocked`。

### 三轮六模块

“六模块”不要求机械阅读全文六次。默认用三轮覆盖全部模块；只有结果冲突、精确统计量引用、复杂模型/元分析/测量学、研究家族歧义或 Reviewer 冲突时，才增加定向复核。

1. **第一轮：论文定位与理论网络**。阅读题名、作者、年份、期刊、DOI、摘要、关键词、引言、理论框架、研究问题/假设、讨论/结论和参考文献表。记录论文问题、理论动机、作者声称的创新、与项目关系、证据角色、初步构念匹配/主张上限，以及需追踪的原始理论、量表、方法、同研究报告和遗漏直接证据。
2. **第二轮：方法、数据与结果核验**。阅读样本/招募、数据来源、波次/间隔、纳排/失访/缺失、构念操作化、量表信效度与计分、数据清理、协变量/聚类、统计模型/估计对象、结果、表图、附录/补充材料、零/相反结果和敏感性分析。记录效应量、区间、精确 p、模型诊断、稳健性及准确页码/表图位置。
3. **第三轮：批判性复核与写作转化**。反核摘要—结果—结论一致性，判断替代解释、混杂、各偏倚域、同一研究家族、支持/零/相反/混合证据、本项目允许与禁止的表述、`claim_ceiling`、谨慎转述、段落用途和待 Reviewer B 事项。

三轮状态使用 `not-started`、`in-progress`、`complete`、`blocked` 或 `not-applicable`；只有适用轮次均完成、关键证据位置可追溯且未把待核验项写成事实时，才能标记深读完成。

### 稳定标识与家族

每篇报告保留唯一 `candidate_id` 和 `report_id`；同一队列共享 `study_id` 和 `study_family_id`。按队列名称、作者群、国家/地区、机构、招募年份、样本量、年龄、波次、量表和随访期识别多报告。不能确认时使用 `family-uncertain-<candidate_id>`，不能留空或把全部未知报告并入一个家族。

### 阅读矩阵

公共最低字段：

```text
study_id,candidate_id,report_id,study_family_id,citation,design,country,
sample_n,age_or_grade,waves,wave_intervals,constructs,measures,analysis_model,
estimand_level,primary_results,null_opposite_mixed_results,effect_estimates,
bias_selection,bias_measurement,bias_temporality,bias_confounding,
bias_missingness,bias_analysis,bias_reporting,applicability,fulltext_location,
family_status,reviewer_a_status,reviewer_b_status,adjudication_status,
claim_ceiling,construct_match,screening_status,verified_at,source_pdf,
reading_level,reading_scope,pass1_orientation_status,pass2_methods_results_status,
pass3_critical_writing_status,research_question,study_hypotheses,claimed_novelty,
theory_framework,data_source,data_cleaning_exclusions,
measurement_reliability_validity,scoring_details,missing_data_handling,covariates,
model_diagnostics,robustness_sensitivity,key_references_to_trace,
relation_to_project_results,paragraph_level_use
```

领域 skill 应追加其专用字段，不能用一个自由文本总评替代结构化样本、测量、分析、结果、偏倚和位置字段。

### 证据账本与主张表

研究/报告级题录、来源和复核状态进入唯一证据账本；主张—来源多对多关系进入唯一 `主张证据对应表_claim_evidence_map.csv`。每行只表示一个 `claim_id × candidate_id/report_id` 配对。

主张表最低字段：

```text
claim_id,claim_text,claim_type,candidate_id,study_id,report_id,study_family_id,
support_status,claim_ceiling,support_carrier_type,support_carrier_value,
fulltext_location,construct_match,estimand_level,result_direction,
reviewer_status,reviewer_reason,verified_at,effect_estimate,standard_error,
ci_95,p_value,paper_one_sentence_conclusion,paragraph_function,
cautious_paraphrase,comparison_or_companion_sources,
relation_to_project_results,prohibited_wording
```

写作卡不另建逐篇文件，直接由主张表的上述字段承担：`paper_one_sentence_conclusion`记录论文级一句话结论，`paragraph_function`记录定义/铺垫/支持/对照/限制/方法等段落功能，`cautious_paraphrase`记录可采用的谨慎转述，`comparison_or_companion_sources`记录需并列或对照的来源，`relation_to_project_results`记录与本项目结果的关系，`prohibited_wording`记录不得如何表述。

阅读矩阵、证据账本和主张表共同描述论文并支持写作：矩阵负责论文内容、方法、结果、质量和用途；账本负责来源身份、题录、全文/勘误状态、研究家族和核验链；主张表负责一个主张与一个来源的证据位置、表述上限、写作卡和 Reviewer 状态。三者不能互相替代，但联合后应能从正文主张回到报告、PDF位置和来源状态。

允许的固定值：

- `claim_type`：`definition`、`theory`、`prevalence`、`direct-empirical`、`measurement`、`method`、`context`、`interpretation`。
- `support_status`：`confirmed`、`partial`、`rejected`、`blocked`。
- `claim_ceiling`：`definition`、`descriptive`、`association`、`temporal-prediction`、`within-person-temporal`、`mechanism-candidate`、`causal-effect`。
- `support_carrier_type`：`text`、`table`、`figure`、`supplement`、`multiple`。
- `construct_match`：`exact`、`partial`、`adjacent`、`mismatch`、`unclear`。
- `estimand_level`：`descriptive`、`between-person`、`within-person`、`mixed`、`not-applicable`、`unclear`。
- `result_direction`：`supports`、`null`、`opposite`、`mixed`、`not-tested`。
- `reviewer_status`：`A-only/B-pending`、`agreed`、`conflict`、`adjudicated`。

`partial` 和 `blocked` 不能成为定稿主张的唯一支撑；`rejected` 保留理由。正文措辞不得高于 `claim_ceiling`。`fulltext_location` 至少含 PDF 页码并尽量附章节、段落、表图或补充材料编号。量化主张记录效应估计、SE/95% CI/精确 p 或明确零结果；不适用写 `not-applicable`。

Reviewer B 必须在看不到 Reviewer A 结论和理由时，根据冻结规则、全文和证据位置独立判断；同一 Agent 的第二次提示不算独立复核。A/B 不一致保留冲突并由第三方裁决。未达 `agreed` 或 `adjudicated` 的主张不能作为无标记的定稿主张。

## 7. 质量评价与综合

相关性、方法质量、来源权威性、引用数和新近性是不同维度。期刊分区、引用数、可视化权重或单一总分不能代替设计适配的领域判断。

至少分别判断选择/抽样、测量、时间顺序、混杂、缺失/失访、分析设定、选择性报告和适用性。综合按 `study_id/study_family_id` 而不是报告数计数；同一研究的多报告可互补取证，但只计一个研究。零结果、相反结果、混合结果和不可判定结果均保留。

## 8. 方法选型与关闭规则

任何新增理论、测量或分析方法建议，先回答：

1. 它检测或修复哪个具体失败？
2. 失败或通过后会采取什么不同动作？
3. 它能否改变研究问题、估计对象或结论边界？

答不上来则不新增。不能修复测量构念、时间窗、设计识别或数据结构的复杂方法，应记录为不采用；不得为追求显著性更换主模型，也不得把模拟、探索或结果可见后的敏感性写成盲态确认性分析。

## 9. 模拟审稿与交接

模拟审稿是内部质量控制，不是真实期刊反馈。优先在一个审稿意见文件和一个修改矩阵中累积三轮冻结审查：

1. Reviewer 1：理论贡献、研究问题、可证伪性、构念边界和替代解释。
2. Reviewer 2：检索透明性、研究家族、证据位置、数字、方法质量、估计对象和来源对齐。
3. Reviewer 3：主编/拒稿风险、跨摘要—方法—结果—讨论的一致性、报告规范、开放科学和目标期刊适配。

每个问题有稳定 `issue_id`、证据位置、严重度、处理动作、状态和验证结果。修改后做最终对齐审计；未解决的来源、Reviewer B、方法或期刊要求必须保持 blocker。不得为每个角色机械创建同用途平行报告。

每次交接列明：更新的现有文件、必要新增文件及原因、验证、未解决问题、下一允许动作。项目若规定唯一导航/交接文档，任务结束前必须更新其指定章节。
