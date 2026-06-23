---
name: psych-reporting-standards
description: Use this skill to select and operationalize psychology reporting standards, ethics requirements, transparency rules, preregistration needs, journal requirements, and empirical manuscript reporting checklists. 适用于投稿规范、伦理披露和报告标准确认；不要用于实际数据分析或自由写作。 Use this skill when creating a protocol, reporting checklist, preregistration frame, author-guideline plan, or when $psychology-research-pipeline delegates its standards stage. Do not use this skill to invent ethics approval, journal policy, registration, or data-sharing commitments.
---

# Psychology Reporting Standards / 心理学报告规范

Turn standards into project-specific requirements, not a generic list.

## Workflow

1. Read the scope artifacts and classify study design, data source, population, analyses, and intended article type.
2. Read `$CODEX_HOME/skills/psychology-research-pipeline/references/psychology-standards.md`.
3. Verify current official target-journal instructions and applicable checklists when a journal is known. Save access dates and URLs.
4. Build a requirement matrix: requirement, source, applicability, planned manuscript location, evidence artifact, owner, and status.
5. Define ethics, consent, adolescent self-harm safety reporting, privacy, data/code availability, preregistration, AI-use disclosure, conflicts, funding, and authorship fields.
6. Freeze primary RQ, hypotheses, outcome/exposure roles, estimands, analysis families, and deviation policy in `02_protocol/protocol.md`.
7. Write `02_protocol/reporting_plan.md` with the governing standards and acceptance checks for later stages.

## Rules

- Apply design-appropriate standards: APA JARS-Quant and STROBE for observational panel work; PRISMA only for systematic reviews/search reporting; SAGER when sex/gender is analyzed.
- Journal instructions override general formatting rules but never research-integrity requirements.
- Do not invent ethics approval, consent, registration, safety procedures, data availability, or journal policy.
- Mark missing documentation as a blocker or explicit manuscript limitation.
- Do not freeze statistical details that the data structure cannot support; route unresolved feasibility issues back to scope.

## Output

Return standards selected, exclusions with rationale, requirement matrix, protocol, later-stage gates, unresolved evidence, and the official sources checked. In pipeline mode, use the stage-contract schema and append the decision log.
