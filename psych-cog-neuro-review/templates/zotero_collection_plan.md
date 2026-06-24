# Zotero collection plan / Zotero 集合计划

## Basic information

- review_run_id:
- run_mode:
- stage: 03_library
- verified_at:
- operator:

## Target collection

- target_collection_name:
- target_collection_key:
- parent_library: personal / group / unknown
- collection_verified_by: Zotero helper / Zotero Desktop / user confirmation / other
- exact collection match: yes / no / blocker

## Acquisition boundary

- candidate source file: `02_search/candidate_records.csv`
- candidate_id range or list:
- record cap:
- full_text_policy: metadata_only / metadata_plus_authorized_pdf / user_provided_pdf_only
- additive write authorization: yes / no
- allowed actions: create metadata record; attach verified PDF; add to named collection
- prohibited actions: delete; merge; rename; move; overwrite existing records

## Tool availability

- Zotero Desktop available:
- Zotero helper status:
- Zotero Connector available:
- browser access available:
- Computer Use available for Zotero Desktop fallback:
- RIS/BibTeX import fallback available:

## Duplicate policy

Search order:

1. DOI
2. PMID
3. normalized title + first author + year

Duplicate actions:

- existing parent + readable PDF: mark `duplicate-skipped`
- existing parent + missing PDF: attach only verified authorized PDF when requested
- uncertain match: mark `manual_needed`

## PDF validation policy

A file can be marked complete only after checking:

- `.pdf` extension and expected content type
- nonzero plausible size
- `%PDF-` signature
- not an HTML login/error page
- readable first page
- plausible page count
- title/author/DOI agreement

## Blockers and unresolved items

| candidate_id | blocker type | reason | user action needed |
|---|---|---|---|
