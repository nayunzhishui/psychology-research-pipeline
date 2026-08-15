---
name: empirical-zotero-ingest
description: Local subskill under psychology-research-pipeline for safe Chrome/Zotero ingestion in empirical psychology projects.
---

# Empirical Zotero Ingest / 实证论文 Zotero 入库分 skill

本分 skill 只在实证论文工作流内部使用，用于合法保存父条目、核验附件状态并完成下载后挂载。开始前完整读取 `../../references/literature-operations-contract.md`。

## 安全边界

- 不记录账号、密码、验证码、cookie、token 或校园认证信息。
- 不绕过付费墙、下载限制、MFA、验证码或出版社条款。
- 只使用用户已合法访问的页面、数据库题录导出、Zotero 接口或用户提供的 PDF。

## 操作路径

1. 精确核验目标 library/collection 名称和 key；禁止把全库当作项目集合。
2. 对候选主表、父条目清单和目标集合三方查重；状态不明时先查 Zotero，不能直接重试。
3. 对筛选保留的新增记录，优先从数据库原始 RIS/BibTeX/CSV 批量导入父条目，默认不带附件；Connector 仅补单篇。
4. 核验 `candidate_id`、父条目 key、题名、作者、年份、DOI 和集合；逐条记录 imported、duplicate-skipped、failed-validation 或 unknown。
5. 只在附件状态核验后原位重建当前缺 PDF 队列；尚未下载的队列不能列入下载失败清单。
6. 用户完成下载后按 DOI，或规范题名+首位作者+年份唯一映射；验证 PDF 文件头、页数和首页身份。
7. 向用户提供异步 Zotero JavaScript：按父条目 key 获取既有父条目、跳过已有可读 PDF、用 `importFromFile` 挂载，并返回 imported/skipped/failed 明细。不得新建父条目或猜测多义匹配。
8. 根据脚本返回值只读核验附件可打开，再更新现有 Zotero/PDF 清单、当前队列和唯一实际下载失败清单；不删除用户下载文件。

## 输出

- `Zotero入库清单_zotero_manifest.csv`
- `父条目入库清单_zotero_parent_manifest.csv`（项目已有时更新）
- `PDF全文清单_pdf_manifest.csv`
- `缺PDF下载队列_freepaper.csv`
- `未能正常下载PDF清单.csv`（只统计实际尝试批次）
- `全文获取报告_acquisition_report.md`

## 停止条件

- 目标集合、父条目身份或 PDF 映射不唯一时停止该条，不猜测。
- 浏览器/脚本超时而结果未知时先实时核验，不生成重试副本。
- PDF 是 HTML、补充材料、损坏或错文时不得挂载为正文。
