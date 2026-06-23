# GitHub design provenance

Snapshot: 2026-06-23. Star counts are discovery signals, not quality evidence.

## Repositories reviewed

- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — 33,657 stars at snapshot. Reviewed deep research, academic paper, pipeline, reviewer, handoff, quality-rubric, and Zotero-adapter patterns.
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) — 29,050 stars at snapshot. Reviewed literature-review, citation-management, scientific-writing, peer-review, and progressive-disclosure patterns.

Local installed baselines also reviewed: `academic-research-suite`, `literature-to-zotero`, `Zotero`, `control-chrome`, `computer-use`, `pdf`, and `documents`.

## Patterns adopted

- Separate orchestration from phase expertise.
- Use explicit stage inputs, outputs, handoffs, failure paths, and gates.
- Keep an append-only state/log record and stable identifiers.
- Preserve independent editorial, methodology/statistics, domain, and integrity review roles before synthesis.
- Store detailed standards in references and deterministic checks in scripts.
- Make search, screening, citation, and analysis reproducible rather than narrative-only.

## Patterns deliberately not copied

- Automatic agent spawning: Codex subagents require explicit user delegation in this environment.
- Unbounded Google Scholar scraping: browser automation must respect anti-bot controls and source terms.
- Citation-count or venue prestige as a substitute for evidence quality.
- Rules requiring DOI, volume, or pages for every article: legitimate online-first, preprint, report, and dataset records may lack these fields.
- Real submission or external reviewer communication inside a “simulation” stage.
- Long third-party prose, templates, or scripts. This package uses independently written contracts and only general workflow ideas.

When updating this package, recheck repository license, current structure, last activity, and official reporting standards. Record the accessed commit or date in the maintenance log.
