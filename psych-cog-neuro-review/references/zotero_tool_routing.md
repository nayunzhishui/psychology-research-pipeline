# Zotero tool routing for review acquisition / Zotero 工具路由

## Purpose

Use this file during `psych-cog-neuro-review` Stage 03 Acquire / 获取与文献库. It adapts the main pipeline's Zotero acquisition rules to the cognitive neuroscience review workflow.

## Route order

Prefer structured scholarly APIs, publisher metadata, database exports, and local Zotero search for discovery and metadata. Use Chrome only when the user's existing logged-in session, institutional access, or Zotero Connector is needed. Use Computer Use only for a desktop action the Zotero helper or connector cannot perform.

Before controlling any tool, load and follow the currently installed tool skill for that tool, such as Zotero, Chrome/browser control, Computer Use, or literature-to-Zotero. The installed tool instructions override duplicated operational detail here.

## Browser / Chrome

- Use the user's existing logged-in state without inspecting cookies, local storage, passwords, or browser profiles.
- Open one verified article page at a time; capture exact URL, source, and access outcome.
- Prefer official publisher pages, DOI landing pages, PubMed/PubMed Central, institutional proxy pages, CNKI/万方/维普 pages, or repository pages that clearly provide authorized access.
- Do not guess PDF URLs or loop through URL variants.
- The user handles login, MFA, CAPTCHA, payment, license acceptance, and ambiguous access rights.
- Downloading authorized files is allowed. Never bypass paywalls, anti-bot controls, robots controls, rate limits, or safety interstitials.

## Zotero

1. Run the available Zotero helper `status --json`.
2. Resolve the exact named collection and record collection key/name in `03_library/zotero_collection_plan.md`.
3. Search for duplicates before download using DOI, PMID, then normalized title + first author + year.
4. Preferred save path: Zotero Connector on the verified article page into the exact collection.
5. Fallback path: export or create RIS/BibTeX from verified metadata, import with Zotero helper, then attach a verified PDF to the parent item when authorized.
6. Verify title, creators, year, DOI, collection, parent item key, attachment child key, and readable full text.

Never create attachment-only items when metadata is available. Additive authorization never permits deleting, merging, renaming, moving, or overwriting existing Zotero records.

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
