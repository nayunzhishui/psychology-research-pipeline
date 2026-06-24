---
name: psych-cog-neuro-review-zotero-ingest
description: Use this subskill during Stage 03 of psych-cog-neuro-review to import literature metadata into a named Zotero collection, use authenticated browser sessions only when the user already has legal access, trigger Zotero Connector, attach verified PDFs, deduplicate records, and report missing full text. 适用于认知神经科学综述的 Zotero 文献入库、合法全文获取和 PDF 匹配；不要用于绕过付费墙、验证码、数据库限制、cookie 提取或盗版全文获取。
---

# Zotero Ingest for Cognitive Neuroscience Review / Zotero 文献入库子流程

## Purpose

Use this subskill only inside `psych-cog-neuro-review` Stage 03 Acquire / 获取与文献库. It mirrors the repository-level `psych-zotero-ingest` behavior, but writes outputs into the review run folder:

```text
03_library/zotero_manifest.csv
03_library/library_acquisition_manifest.csv
03_library/zotero_collection_plan.md
03_library/acquisition_report.md
```

## Preflight

Before any Zotero or browser action, require and record:

1. candidate IDs from `02_search/candidate_records.csv`;
2. exact target Zotero collection name and, when available, collection key;
3. record cap for this acquisition batch;
4. full-text policy: `metadata_only`, `metadata_plus_authorized_pdf`, or `user_provided_pdf_only`;
5. standing additive write authorization for the named collection;
6. whether Zotero Desktop, Zotero Connector, browser access, and local helper are available.

If any of these are missing, stop Stage 03 and write the blocker to `03_library/acquisition_report.md`. Do not guess the collection.

## Tool routing

Read `references/zotero_tool_routing.md` first.

Preferred route:

1. Use structured metadata sources and local Zotero search first.
2. Use Zotero helper where available: run `status --json`, resolve the exact collection, and search duplicates.
3. Use browser and Zotero Connector only on verified article pages when the user already has legal access.
4. Use Computer Use only for a Zotero Desktop action that helper/connector cannot perform, such as attaching a verified PDF to an existing parent item.

## Process each candidate

For each candidate under the record cap:

1. Search Zotero by DOI, PMID, then normalized title + first author + year.
2. If a matching parent item and readable PDF already exist, record `duplicate-skipped` in `zotero_manifest.csv` and `duplicate_skipped` in `library_acquisition_manifest.csv`.
3. If a matching parent item exists without the requested PDF, acquire only the missing authorized attachment.
4. If no record exists, import metadata into the exact target collection. Prefer Zotero Connector from the verified article page. Fallback to RIS/BibTeX import when connector import is unavailable.
5. Download only authorized scholarly files. Validate each PDF before attachment or before marking it complete.
6. Attach verified PDFs only to the correct parent record. Never create attachment-only items when usable metadata exists.
7. Verify title, creators, year, DOI/PMID/CNKI/Wanfang/VIP identifier where available, collection, parent item key, attachment child key, and readable full text.
8. Write both manifests and update `acquisition_report.md` after each batch.

## PDF validation

Before import or attachment, verify:

- expected content type and `.pdf` extension;
- nonzero plausible size and `%PDF-` signature;
- no HTML login page, error page, or executable disguised as PDF;
- readable first page;
- page count is plausible;
- title/author/DOI agreement with the candidate record.

If validation fails, quarantine the local file, record `failed-validation`, and do not attach it to Zotero.

## Allowed statuses

Use these status values in `zotero_manifest.csv`:

- `complete`
- `metadata-only`
- `duplicate-skipped`
- `access-blocked`
- `failed-validation`
- `manual_needed`
- `user_provided`

Use normalized snake_case values in `library_acquisition_manifest.csv` where needed:

- `readable_pdf`
- `metadata_only`
- `abstract_only`
- `access_blocked`
- `duplicate_skipped`
- `failed_validation`
- `manual_needed`
- `user_provided`

## Hard boundaries

- Do not read, save, enter, or request campus account, database account, publisher account, Zotero account, or browser passwords.
- Do not extract, copy, save, export, or reuse cookies, session storage, local storage, browser profiles, saved passwords, tokens, or authentication artifacts.
- Do not use unauthorized full-text sources, shadow libraries, piracy mirrors, PDF bots, leaked credentials, or non-authorized repository copies.
- Do not bypass CAPTCHA, MFA, IP limits, database download limits, robots controls, publisher restrictions, or paywalls.
- Stop the item and record `manual_needed` when CAPTCHA, secondary authentication, abnormal-download warnings, account-risk warnings, license ambiguity, payment prompts, or access uncertainty appears.
- Do not run unattended high-frequency bulk acquisition. Process bounded batches under the configured record cap.
- Do not commit PDFs, Zotero databases, downloaded full text, browser artifacts, credentials, API keys, tokens, cookies, or temporary downloads to GitHub.

## Output rules

- `zotero_manifest.csv` is the direct Zotero import manifest.
- `library_acquisition_manifest.csv` is the richer review-pipeline manifest used by screening, extraction, and audit.
- `acquisition_report.md` must include counts by status, unresolved records, validation failures, access blockers, and manual actions for the user.
- `zotero_collection_plan.md` must record the exact collection name/key, record cap, full-text policy, helper/connector availability, and date of verification.

Never claim full text is available based only on a landing page or metadata record. Never mark Stage 03 complete until every retained candidate has a traceable status.
