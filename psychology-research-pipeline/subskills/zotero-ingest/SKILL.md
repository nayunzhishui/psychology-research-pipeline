---
name: empirical-zotero-ingest
description: Local subskill under psychology-research-pipeline for safe Chrome/Zotero ingestion in empirical psychology projects.
---

# Empirical Zotero Ingest / 实证论文 Zotero 入库分 skill

本分 skill 只在实证论文工作流内部使用，用于合法保存题录、PDF 和入库日志。

## 安全边界

- 不记录账号、密码、验证码、cookie、token 或校园认证信息。
- 不绕过付费墙、下载限制、MFA、验证码或出版社条款。
- 只使用用户已合法访问的页面、Zotero Connector、题录导出或用户提供的 PDF。

## 操作路径

1. 确认 Zotero collection 名称。
2. Chrome 打开数据库、DOI、PubMed、期刊官网或学校已授权页面。
3. 使用 Zotero Connector 保存题录和 PDF。
4. 失败时下载到 `literature/00_待导入Zotero/`，由用户手动导入。
5. 导出 BibTeX/RIS 并写入 manifest。

## 输出

- `zotero_manifest.csv`
- `pdf_manifest.csv`
- `acquisition_report.md`
- `failed_ingest_queue.csv`