---
name: cog-neuro-zotero-ingest
description: Local subskill under psych-cog-neuro-review for safe Zotero ingestion in cognitive neuroscience review projects. Chinese-first; use only inside the cognitive neuroscience review workflow.
---

# Zotero 入库分 skill

## 目标

把认知神经科学综述候选文献合法、安全、可追溯地导入 Zotero，并核验题录和全文状态。

## 适用场景

- 需要使用 Chrome + Zotero Connector 保存题录和 PDF。
- 需要核验 DOI、PMID、题名、作者、年份、PDF 和目标 collection。

## 输入

候选文献表、DOI/PMID、数据库页面、期刊官网页面、Zotero collection、用户已合法访问的 PDF。

## 执行步骤

1. 确认 Zotero collection 和本地文献目录。
2. 使用 Zotero Connector 保存题录和 PDF。
3. 核验题录与 PDF 是否匹配。
4. 标记缺失全文、重复题录、题录不完整和需用户手动处理项。
5. 导出 BibTeX/RIS/CSV，并生成入库清单。

## 输出文件

- `Zotero入库清单_zotero_manifest.csv`
- `PDF全文清单_pdf_manifest.csv`
- `重复文献检查_duplicate_check.csv`
- `全文获取报告_acquisition_report.md`
- `全文获取失败清单_failed_ingest_queue.csv`

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
- 大量题录缺失 DOI/PMID 时需先清洗题录。

## 安全边界

不保存账号密码、验证码、cookie、token 或密钥；不绕过付费墙、MFA、验证码、数据库条款或下载限制；不使用盗版来源。

## 完成条件

形成 Zotero 入库清单、PDF 全文清单、重复检查和失败队列，说明哪些文献可进入全文阅读。