---
name: empirical-evidence-search
description: Local subskill under psychology-research-pipeline for empirical psychology evidence search. Chinese-first; use only inside the empirical workflow.
---

# 证据检索分 skill

## 目标

为实证论文的理论依据、变量模型、量表选择、方法设计和引言写作提供可追溯证据。

## 适用场景

- 需要检索核心理论、综述/元分析、量表/方法文章和直接相关实证研究。
- 需要建立种子文献表、候选文献表和检索记录。
- 需要为后续文献筛选、方法设计和写作提供证据基础。

## 输入

- 项目定标结果、变量模型、关键词、中英文术语。
- 用户可访问的数据库、Zotero collection、已有文献或 DOI/PMID。
- 开始前完整读取 `../../references/literature-operations-contract.md`，并盘点现有候选主表、检索计划、检索日志、证据缺口和历轮原始导出。

## 执行步骤

1. 将人群、构念、结局、设计、测量、方法和调节变量拆为概念块；禁止把全部概念压成一个“大而全”检索式。
2. 按证据任务建立多个 query family：直接变量关系、联合模型、综述/元分析、测量、方法和引文追踪。每个数据库保存其精确语法，不用跨库复制后冒充已验证。
3. 结合阅读矩阵、证据账本、缺口和上轮日志原位更新 `search-plan.json`；每个主题写触发证据、精准问题、数据库专用语法、预期槽和停止条件。运行 `plan-search` 只表示冻结计划。
4. 默认用已合法登录的内置浏览器检索并导出；页面不兼容时回退到用户授权的外置浏览器。Connector 只补单篇，不能替代批量原始导出。
5. 原始 CSV、RIS、BibTeX、PubMed XML、Crossref JSON 或 OpenAlex JSON 保持只读；登记平台、日期、过滤器、结果数、导出路径和必要哈希。
6. 将本轮全部结果追加到唯一候选主表；先按 DOI、PMID/稳定 ID、规范题名+首作者+年份与历轮全部已见题录求差集，再让真正新增题录进入筛选。不能只对 Zotero 或 PDF 查重。
7. 记录级去重后单独识别同研究多报告；保留报告，只建立 `study_id/study_family_id` 候选关系，不自动合并。
8. 标注证据用途、构念、设计、撤稿/更正和全文状态；运行覆盖审计。核心 slot 缺口转为下一轮精准问题，而非机械重跑旧检索式。

## 默认数据库

核心检索按课题权限选择 PubMed、PsycINFO、Web of Science、CNKI 和期刊官网。Crossref 用于 DOI/出版元数据核验，OpenAlex 用于开放的引文发现与补链，Google Scholar 仅作辅助发现；三者均不得替代核心数据库的可复现检索。Scopus、APA PsycNet、SinoMed、万方或维普仅在用户有权限或课题需要时加入并记录理由。

## 输出文件

- `检索式记录_queries.md`
- `检索计划_search_plan.json`
- `检索记录_search_log.csv`
- `候选文献表_candidate_records.csv`
- `题录导入清单_evidence_import_manifest.json`
- `种子文献表_seed_papers.csv`
- `文献去重清单_evidence_dedupe_manifest.json`
- `同研究多报告候选_study_family_candidates.csv`
- `证据覆盖矩阵_evidence_coverage.csv`
- `证据缺口_gap_memo.md`
- `全文获取队列_retrieval_queue.csv`
- `缺PDF下载队列_freepaper.csv`（仅在父条目与附件状态核验后原位重建）

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 检索式是否覆盖构念、变量、人群、方法和测量？
- 是否记录数据库、日期、检索式和结果数？
- 每个原始导出是否保存路径、格式、记录数和 SHA-256？
- 是否区分综述、理论、方法、量表和实证文献？
- 是否明确哪些文献只能作背景、哪些可支撑核心假设？
- 是否检查撤稿/更正，且没有把同一研究的不同报告当作重复记录删除？
- 核心证据 slot 是否全部达到预设最低数？

## 失败与停止条件

- 没有检索记录时不得进入正式写作。
- 核心证据覆盖审计为 `blocked` 时不得进入小综述或正式写作。
- 没有量表来源文献时不得声称“采用某量表”。
- 没有全文时不得做页码级强引用。
- 原始导出缺失而无法建立历轮已见基线时，披露重复风险并阻断“已完成历轮排除”的声明。

## 安全边界

不绕过付费墙、MFA、验证码或出版社条款；不使用盗版论文站；不伪造 DOI、PMID、题录或引用。

## 完成条件

形成带原始导出哈希的可追溯检索记录、规范化候选表、去重与多报告审计、证据覆盖矩阵和全文获取队列；核心 slot 无缺口，或明确阻断与补检索方案。
