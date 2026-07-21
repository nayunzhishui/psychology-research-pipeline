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

## 执行步骤

1. 将人群、构念、结局、设计、测量、方法和调节变量拆为概念块；禁止把全部概念压成一个“大而全”检索式。
2. 按证据任务建立多个 query family：直接变量关系、联合模型、综述/元分析、测量、方法和引文追踪。每个数据库保存其精确语法，不用跨库复制后冒充已验证。
3. 冻结 `search-plan.json` 并运行 `plan-search`；保存检索式和 SHA-256。实际检索后记录平台、日期、过滤器、结果数和原始导出文件。
4. 原始 CSV、RIS、BibTeX、PubMed XML、Crossref JSON 或 OpenAlex JSON 保持只读；运行 `import-evidence` 统一题录并记录每个导出文件哈希。
5. 先做 DOI、PMID、OpenAlex ID、题名+首作者+年份的记录去重，再单独运行同研究多报告识别；后者只生成待人工复核候选，不自动合并。
6. 标注证据用途、构念、设计、撤稿/更正、全文状态和证据位置。直接实证、测量、方法、综述和背景证据不得混为同一层级。
7. 运行证据覆盖审计；任何核心 slot 未满足时阻断小综述和正式写作，输出精准补检索问题。
8. 用全文获取队列排序合法获取任务；检索更新只追加新记录并标记变化，不删除旧证据。

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
- 数据库权限或 Zotero 导入失败时，生成 `全文获取失败清单_failed_ingest_queue.csv`。

## 安全边界

不绕过付费墙、MFA、验证码或出版社条款；不使用盗版论文站；不伪造 DOI、PMID、题录或引用。

## 完成条件

形成带原始导出哈希的可追溯检索记录、规范化候选表、去重与多报告审计、证据覆盖矩阵和全文获取队列；核心 slot 无缺口，或明确阻断与补检索方案。
