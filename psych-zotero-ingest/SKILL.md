---
name: psych-zotero-ingest
description: Use this skill to import literature metadata into Zotero, use authenticated browser sessions for legally accessible scholarly PDFs, trigger Zotero Connector, attach verified PDFs, deduplicate records, and report missing full text. 适用于 Zotero 文献入库、合法全文获取和 PDF 匹配；不要用于绕过付费墙、验证码、数据库限制、cookie 提取或盗版全文获取。 Use this skill when populating a psychology project library or when $psychology-research-pipeline delegates acquisition. Do not use this skill for unauthorized access, high-frequency unattended bulk downloading, or modifying existing Zotero records.
---

# Psychology Zotero Ingest / Zotero 文献入库

Run an additive, bounded acquisition workflow. Read `$CODEX_HOME/skills/psychology-research-pipeline/references/tool-routing.md` and follow the current installed tool skills.

## Preflight

1. Require candidate IDs, target Zotero collection, record cap, full-text policy, and standing write authorization. A pipeline acquisition stage supplies additive authorization for matching records in the named collection.
2. Run the Zotero helper `status --json`; resolve the exact collection and record its key/name.
3. Create a task-specific temporary download directory. Never use an ambiguous shared Downloads folder as the manifest.

## Process each candidate

1. Search Zotero by DOI, PMID, then normalized title + first author + year.
2. If a matching parent item and readable PDF exist, record `duplicate-skipped`. If metadata exists without the requested PDF, acquire only the missing attachment.
3. Use Chrome for the verified article page when browser login or Zotero Connector is needed. The user handles login, MFA, CAPTCHA, payment, and access decisions.
4. Download only authorized scholarly files. Validate signature, size, first-page readability, page count, and title/DOI agreement before import.
5. Prefer Zotero Connector into the exact collection. Fallback to RIS/BibTeX import, then use Computer Use in Zotero Desktop to attach the verified PDF to its parent.
6. Verify title, creators, year, DOI, collection, parent key, attachment child key, and readable full text. Only then mark `complete` and remove temporary files.

## Additional hard boundaries

- Do not read, save, enter, or request campus account, database account, or publisher-account passwords.
- Do not extract, copy, save, export, or reuse cookies, session storage, local storage, browser profiles, saved passwords, tokens, or authentication artifacts.
- Do not use unauthorized full-text sources, shadow libraries, piracy mirrors, PDF bots, leaked credentials, or non-authorized repository copies.
- Do not bypass CAPTCHA, MFA, IP limits, database download limits, robots controls, publisher restrictions, or paywalls.
- Stop the item and record `manual_needed` when CAPTCHA, secondary authentication, abnormal-download warnings, account-risk warnings, license ambiguity, payment prompts, or access uncertainty appears.
- Do not run unattended high-frequency bulk acquisition. Process bounded batches under the configured record cap and stop when the cap or warning condition is reached.
- Do not commit PDFs, Zotero databases, downloaded full text, browser artifacts, credentials, API keys, tokens, or cookies to GitHub.

## Boundaries and output

- Never delete, merge, rename, move, or overwrite existing Zotero records.
- Never create an attachment-only item when usable metadata exists.
- Never claim full text from a landing page or metadata record.
- Quarantine HTML login pages, corrupt PDFs, executables, and mismatches.

Write `04_library/zotero_manifest.csv` and `04_library/acquisition_report.md` with counts and exact exceptions using the main stage contract.
