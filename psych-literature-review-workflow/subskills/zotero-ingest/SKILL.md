---
name: review-zotero-ingest
description: Local subskill under psych-literature-review-workflow for safe Zotero ingestion in literature review projects.
---

# Review Zotero Ingest / 综述 Zotero 入库分 skill

本分 skill 用于综述项目的题录、PDF 和全文入库管理。

## 安全边界

不保存账号密码、验证码、cookie、token 或校园认证信息；不绕过付费墙、下载限制或出版社条款；只处理用户有权访问的文献。

## 操作路径

1. 确认 Zotero collection 和本地文献目录。
2. 使用 Chrome + Zotero Connector 保存题录和 PDF。
3. 失败时下载到 `literature/00_待导入Zotero/`，由用户手动导入。
4. 导出 BibTeX/RIS，核对 DOI、题名、作者、年份和 PDF 是否匹配。

## 输出

- `zotero_manifest.csv`
- `pdf_manifest.csv`
- `duplicate_check.csv`
- `acquisition_report.md`