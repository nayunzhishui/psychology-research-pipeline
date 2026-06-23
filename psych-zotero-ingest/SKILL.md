---
name: psych-zotero-ingest
description: Use the installed Chrome, Zotero, literature-to-Zotero, and Computer Use workflows to deduplicate candidates, download authorized papers, validate PDFs, save metadata and attachments to an exact Zotero collection, verify every write, and report exceptions. Use when populating a psychology project library or when $psychology-research-pipeline delegates acquisition.
---

# Psychology Zotero Ingest

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

## Boundaries and output

- Never delete, merge, rename, move, or overwrite existing Zotero records.
- Never create an attachment-only item when usable metadata exists.
- Never claim full text from a landing page or metadata record.
- Quarantine HTML login pages, corrupt PDFs, executables, and mismatches.

Write `04_library/zotero_manifest.csv` and `04_library/acquisition_report.md` with counts and exact exceptions using the main stage contract.
