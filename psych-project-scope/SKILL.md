---
name: psych-project-scope
description: Use this skill to audit a psychology research workspace, define the research scope, identify constructs, variables, waves, datasets, seed literature, feasibility constraints, and research questions. 适用于项目定标、变量与数据可行性判断；不要用于文献下载、数据建模或论文正文写作。 Use this skill when starting or resuming a psychology empirical project, when the topic is broad, or when $psychology-research-pipeline delegates its scope stage. Do not use this skill when the project scope and analysis-ready variable map are already frozen.
---

# Psychology Project Scope / 心理学项目定标

Produce a defensible project brief from available evidence. Do not infer a construct solely from a filename when instruments, variable labels, or data dictionaries are available.

## Workflow

1. Inventory the workspace read-only. Classify files as data, instruments, literature, code, drafts, outputs, or unknown.
2. Extract metadata first: formats, row/column counts, wave markers, variable labels, dates, sample fields, and document headings.
3. Read the minimum content needed to identify constructs, measures, population, waves, and prior analytical choices. Use the installed PDF, documents, spreadsheet, or Zotero skills for their formats.
4. Build a construct-to-variable map. Separate observed evidence, inference, and unknowns.
5. Form one primary research question and at most three secondary questions. Score feasibility, novelty, ethics, data support, and analytical identifiability.
6. Define in-scope and out-of-scope claims, target population, exposure, mediator/moderator, outcome, time horizon, and comparison groups.
7. State the minimum viable design and two credible alternatives. Flag decisions that would materially alter the study.
8. Write `01_scope/project_brief.md` and `01_scope/research_question.md`; record source paths and evidence for every material decision.

## Gates

- Do not pass scope when wave count, participant linkage, core variable scoring, or target outcome is unknown.
- Do not call a measured binary sex variable “gender identity.” Use the instrument's term and explain limitations.
- Treat self-harm and mental-health data as sensitive. Never transmit row-level data to external services.
- Never promise causal conclusions from observational panel data.

## Output contract

Include workspace inventory, study context, evidence table, construct map, candidate questions, selected question with rationale, hypotheses, scope boundaries, feasibility risks, missing information, and next-stage acceptance criteria.

When invoked by the main pipeline, follow `$CODEX_HOME/skills/psychology-research-pipeline/references/stage-contracts.md` and append a decision event to the run log.
