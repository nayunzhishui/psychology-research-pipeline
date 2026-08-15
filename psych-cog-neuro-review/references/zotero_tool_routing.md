# Zotero tool routing for review acquisition / Zotero 工具路由

## Purpose

Use this file during `psych-cog-neuro-review` Stage 03 Acquire / 获取与文献库. It adapts the main pipeline's Zotero acquisition rules to the cognitive neuroscience review workflow.

## Route order

先完整读取 `literature-operations-contract.md`。默认路径是在用户已完成合法机构登录的内置浏览器中检索并从数据库导出结构化题录；页面不兼容时回退到用户明确授权的外置浏览器。Connector 只补单篇，不能替代批量原始导出、历轮全部已见主表或检索日志。Computer Use 仅用于 Zotero 助手或脚本无法完成的桌面动作。

Before controlling any tool, load and follow the currently installed tool skill for that tool, such as Zotero, Chrome/browser control, Computer Use, or literature-to-Zotero. The installed tool instructions override duplicated operational detail here.

## Browser / Chrome

- Use the user's existing logged-in state without inspecting cookies, local storage, passwords, or browser profiles.
- 检索阶段可在数据库结果页执行有界批量操作并导出 RIS/BibTeX/CSV；PDF 获取和单篇核验仍逐条记录访问结果。
- Prefer official publisher pages, DOI landing pages, PubMed/PubMed Central, institutional proxy pages, CNKI/万方/维普 pages, or repository pages that clearly provide authorized access.
- Do not guess PDF URLs or loop through URL variants.
- The user handles login, MFA, CAPTCHA, payment, license acceptance, and ambiguous access rights.
- Downloading authorized files is allowed. Never bypass paywalls, anti-bot controls, robots controls, rate limits, or safety interstitials.

## Zotero

1. Run the available Zotero helper `status --json`.
2. Resolve the exact named collection and record collection key/name in `03_library/zotero_collection_plan.md`.
3. 导入前对历轮候选主表、父条目清单和目标集合三方查重；优先 DOI、PMID，再用规范题名 + 首位作者 + 年份。
4. 优先将筛选保留的数据库 RIS/BibTeX/CSV 批量导入为无附件父条目；Connector 仅用于单篇且无法结构化导出的页面。
5. 导入后核验题名、作者、年份、DOI、集合、父条目 key 与附件 key；超时后先实时查询，不盲目重试。
6. 根据附件状态原位重建缺 PDF 队列；用户下载后验证并用异步 Zotero JavaScript 挂到既有父条目，不新建父条目。

Never create attachment-only items when metadata is available. Additive authorization never permits deleting, merging, renaming, moving, or overwriting existing Zotero records. 尚未实际下载的队列不能进入下载失败清单；只有验证通过且唯一挂载的正文 PDF 才能从失败清单移除。

## Computer Use

- Use only the installed Computer Use runtime; never replace it with PowerShell SendKeys or terminal automation.
- Discover Zotero with the available app/window listing, select a returned window, inspect it, and act on that exact window.
- Prefer keyboard navigation for native menus. Verify focus and resulting attachment before continuing.
- Do not automate authentication dialogs, security settings, terminal apps, password managers, browser credential prompts, or the Codex app.
- Apply the Computer Use confirmation policy for uploads, external communication, deletion, permissions, and other side effects.

## PDF validation

Before import or attachment, verify:

- expected content type and `.pdf` extension;
- nonzero plausible size and `%PDF-` signature;
- no executable or HTML login page disguised as PDF;
- readable first page;
- title/author/DOI agreement with the candidate record;
- plausible page count and no obvious corruption.

Quarantine mismatches and log `failed-validation`. Do not delete the temporary file until Zotero shows a readable attachment. Never claim full text exists based only on metadata or a web landing page.

## Failure handling

Record one of these statuses in `03_library/zotero_manifest.csv` and explain the reason in `03_library/acquisition_report.md`:

- `complete`
- `metadata-only`
- `duplicate-skipped`
- `access-blocked`
- `failed-validation`
- `manual_needed`
- `user_provided`

Continue with other authorized candidates unless the failure invalidates the search scope or triggers a safety/access warning. Never lower validation standards to improve completion counts.
