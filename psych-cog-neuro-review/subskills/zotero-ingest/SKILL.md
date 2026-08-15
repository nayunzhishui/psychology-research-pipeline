---
name: cog-neuro-zotero-ingest
description: Local subskill under psych-cog-neuro-review for safe Zotero ingestion in cognitive neuroscience review projects. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# Zotero 入库分 skill

## 目标

把认知神经科学综述候选文献合法、安全、可追溯地导入 Zotero，并核验题录和全文状态。

## 适用场景

- 需要批量导入筛选保留的父条目、核验附件、交付缺 PDF 队列或完成下载后挂载。
- 需要核验 DOI、PMID、题名、作者、年份、PDF 和目标 collection。

## 输入

候选文献表、父条目清单、DOI/PMID、数据库原始导出、Zotero collection、附件状态、本批队列和用户已合法访问的 PDF。开始前完整读取 `../../references/literature-operations-contract.md`。

## 执行步骤

1. 精确核验目标 collection 名称/key，对候选主表、父条目清单和 Zotero 目标集合三方查重。
2. 对筛选保留的新增记录，优先用数据库 RIS/BibTeX/CSV 批量导入父条目且不带附件；Connector 仅补单篇。
3. 核验 `candidate_id`、父条目 key、题名、作者、年份、DOI/PMID 和集合；超时后先实时查询，不能盲目重试。
4. 按附件状态原位重建当前缺 PDF 队列；尚未实际下载的队列不进入失败清单。
5. 用户下载后按 DOI，或规范题名+首位作者+年份唯一映射，验证 PDF 文件头、页数和首页身份。
6. 用异步 Zotero JavaScript 将有效正文 PDF 挂到既有父条目，逐条返回 imported/skipped/failed；不新建父条目或猜测多义匹配。
7. 只读核验附件可打开后更新现有 Zotero/PDF 清单、队列和唯一实际下载失败清单。

## 输出文件

- `Zotero入库清单_zotero_manifest.csv`
- `PDF全文清单_pdf_manifest.csv`
- `重复文献检查_duplicate_check.csv`
- `全文获取报告_acquisition_report.md`
- `缺PDF下载队列_freepaper.csv`
- `未能正常下载PDF清单.csv`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 题录是否完整？
- PDF 是否与题录匹配？
- DOI/PMID 是否可核验？
- 失败项是否进入队列？

## 失败与停止条件

- 无合法访问权限时停止全文获取。
- PDF 与题录不匹配时不得进入阅读矩阵。
- 父条目或 PDF 映射不唯一、文件损坏/错文、状态未知时停止该条并保留原因。

## 安全边界

不保存账号密码、验证码、cookie、token 或密钥；不绕过付费墙、MFA、验证码、数据库条款或下载限制；不使用盗版来源。

## 完成条件

形成 Zotero 入库清单、PDF 全文清单、重复检查和失败队列，说明哪些文献可进入全文阅读。
