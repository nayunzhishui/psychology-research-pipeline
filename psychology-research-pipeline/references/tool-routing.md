# Tool routing for literature acquisition

## Contents

1. Route order
2. Chrome
3. Zotero
4. Computer Use
5. PDF validation
6. Failure handling

## Route order

Prefer structured scholarly APIs, publisher metadata, and purpose-built connectors for discovery and metadata. Use Chrome only when the user's existing session, institutional access, or Zotero Connector is needed. Use Computer Use only for a desktop action the Zotero helper/connector cannot perform.

Before controlling a tool, load and follow its installed skill: `control-chrome`, `Zotero`, `computer-use`, and `literature-to-zotero`. Their current instructions override duplicated operational detail here.

## Chrome

- Use the user's existing logged-in state without inspecting cookies, local storage, passwords, or profiles.
- Search one focused query at a time; capture exact query, filters, date, count, and source.
- Prefer visible article pages and official download links. Do not guess download URLs or loop through URL variants.
- The user handles login, MFA, CAPTCHA, payment, license acceptance, and ambiguous access rights.
- Downloading authorized files is allowed. Never bypass paywalls, anti-bot controls, or safety interstitials.
- Finalize browser tabs according to the Chrome skill; retain only a user-facing handoff or deliverable tab.

## Zotero

1. Run the bundled helper `status --json`.
2. Resolve the exact named collection; never substitute the currently selected collection silently.
3. Search for duplicates before download using DOI, PMID, then normalized title + first author + year.
4. Preferred save path: Zotero Connector on the verified article page into the exact collection.
5. Fallback: export RIS/BibTeX, import with the Zotero helper, then use Computer Use to attach the verified PDF to the parent item.
6. Verify title, creators, year, DOI, collection, parent item key, attachment child key, and readable full text.

Never create attachment-only items when metadata is available. Additive authorization never permits delete, merge, rename, move, or overwrite of existing records.

## Computer Use

- Use only the installed Computer Use runtime; never replace it with PowerShell SendKeys or terminal automation.
- Discover Zotero with `list_apps`, select a returned window, inspect it, then act on that exact window.
- Prefer keyboard navigation for native menus. Verify focus and the resulting attachment before continuing.
- Do not automate authentication dialogs, security settings, terminal apps, password managers, or the Codex app.
- Apply the Computer Use confirmation policy for uploads, external communication, deletion, permissions, and other side effects.

## PDF validation

Before import, verify:

- expected content type and `.pdf` extension;
- nonzero plausible size and `%PDF-` signature;
- no executable or HTML login page disguised as PDF;
- readable first page;
- title/author/DOI agreement with the candidate record;
- page count and no obvious corruption.

Quarantine mismatches and log `failed-validation`. Do not delete the temporary file until Zotero shows a readable attachment. Never claim full text exists based only on metadata or a web landing page.

## Failure handling

Record `metadata-only`, `duplicate-skipped`, `access-blocked`, or `failed-validation` with exact reason. Continue with other authorized candidates unless the failure invalidates the search scope. Never lower validation standards to improve completion counts.
