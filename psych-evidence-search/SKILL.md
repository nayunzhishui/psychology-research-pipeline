---
name: psych-evidence-search
description: Use this skill to build reproducible psychology literature search strategies, bilingual query blocks, database-specific search strings, metadata exports, search logs, and candidate reference lists. 适用于心理学文献检索和候选题录生成；不要用于全文下载或 Zotero 附件处理。 Use this skill for empirical psychology evidence discovery, search updates, protocol searches, or when $psychology-research-pipeline delegates its search stage. Do not use this skill for unauthorized scraping, CAPTCHA bypass, or claiming a convenience source is exhaustive.
---

# Psychology Evidence Search / 心理学证据检索

Search for coverage and traceability, not an impressive raw count.

## Build the strategy

1. Read the RQ, protocol, population, constructs, temporal design, analysis terms, years, languages, document types, exclusions, and record cap.
2. Decompose into concept blocks. Generate controlled vocabulary, construct names, scale names, abbreviations, spelling variants, developmental terms, design terms, and Chinese/English synonyms.
3. Create a broad sensitivity query and narrower precision queries. Translate syntax per database; do not paste one query everywhere.
4. Pilot each query, inspect relevant and irrelevant hits, then make one logged revision. Preserve all versions.

For longitudinal psychology work, combine substantive constructs with population and, when useful, design terms such as longitudinal, panel, cross-lagged, random-intercept cross-lagged, within-person, cohort, mediation, and measurement invariance. Do not require a method term when it would exclude relevant theory or measurement studies.

## Run and record

- Prefer PsycINFO plus appropriate multidisciplinary/biomedical sources such as Web of Science, Scopus, PubMed, and OpenAlex/Crossref metadata. Add CNKI, Wanfang, or SinoMed for Chinese evidence when access permits.
- Use APIs/connectors for metadata. Use Chrome only when the current browser session or institutional access is required; first read the main pipeline's `references/tool-routing.md` and the installed Chrome skill.
- Respect rate limits, robots, licenses, and anti-bot controls. Never automate CAPTCHA or bypass access restrictions.
- Export complete metadata where possible. Record database, platform, exact query, filters, date/time, count, export path, and notes in `03_search/search_log.csv`.
- Assign `candidate_id`; normalize DOI/PMID/title/authors/year/source/abstract/URL/search provenance into `03_search/candidates.csv`.
- Deduplicate by DOI, then PMID, then normalized title + first author + year. Preserve provenance from every search.
- Use backward and forward citation chasing on verified seed papers as a separately logged search method.

## Gate

Fail when a core construct lacks synonyms, search strings cannot be rerun, exports are missing, database counts are undocumented, duplicates were deleted without provenance, or a convenience source is presented as exhaustive. Report access limitations and database bias explicitly.
