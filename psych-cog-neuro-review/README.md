# psych-cog-neuro-review

这是一个面向心理学与认知神经科学文献综述的 Codex skill 文件夹。它把“项目定标—协议冻结—检索—文献库获取—筛查—提取—质量评价—证据综合—脱稿前写作计划—正文写作—参考文献对应核查”固定成可复用流程。

该 skill 不是单纯写综述正文，而是复现 `psychology-research-pipeline` 中数据分析与实证论文写作之前的阶段控制思路，并把这些步骤改写为综述写作场景。

## 默认定位

- 默认综述类型：混合型机制综述（mixed mechanism review）。
- 默认运行模式：`standard`。
- 可升级方向：范围综述（scoping review）或系统综述（systematic review）。
- 默认写作风格：中文核心综述风格，同时保留外文 Q1 review 预备稿结构。
- 默认主题扩展包：当主题涉及 REM sleep、emotional memory、fear conditioning、extinction、memory consolidation、reconsolidation、PSG 或睡眠依赖情绪加工时，加载 `topic_packs/rem_emotional_memory/`。

## 运行模式

| 模式 | 适用场景 | 特点 |
|---|---|---|
| `lite` | 课程论文、快速选题、早期综述草图 | 允许跳过完整筛查和正式质量评价，但必须记录跳过原因 |
| `standard` | 研究生综述、中文核心预备稿、普通机制综述 | 默认模式，执行 00–09 全流程，允许单人筛查但必须披露 |
| `strict` | 系统综述、范围综述、外文 Q1 review 预备稿 | 强化检索、筛查、质量评价、PRISMA-style traceability 和段落来源核查 |

## 适用范围

- 通用心理学文献综述
- 认知神经科学综述
- REM sleep 与情绪记忆主题
- EEG/ERP、fMRI、PSG、行为实验、量表、睡眠实验、多方法整合综述
- 中文核心综述风格或外文 Q1 review 预备稿风格
- 叙事综述、理论综述、机制综述、范围综述、系统综述预备流程

## 阶段流程

| 阶段 | 目标 | 主要产出 |
|---|---|---|
| 00 Scope | 项目定标、运行模式、概念边界、工作区盘点 | `review_scope.md`, `concept_map.md` |
| 01 Protocol | 报告规范、综述协议、纳排标准冻结 | `reporting_plan.md`, `review_protocol.md` |
| 02 Search | 中英文检索式与数据库记录 | `search_strategy.md`, `database_search_log.csv`, `candidate_records.csv` |
| 03 Acquire | DOI/PMID/CNKI/万方/维普/Zotero/PDF 状态核查 | `library_acquisition_manifest.csv`, `acquisition_report.md` |
| 04 Screen | 标题摘要与全文筛查、PRISMA flow counts | `screening_table.csv`, `prisma_flow_counts.csv` |
| 05 Extract | 阅读矩阵、神经机制矩阵、质量评价 | `literature_matrix.csv`, `neural_mechanism_matrix.csv`, `quality_appraisal.csv` |
| 06 Synthesize | 脱稿前证据综合、claim-evidence map | `prewriting_synthesis_plan.md`, `claim_evidence_map.csv` |
| 07 Prewrite | 章节论证路径、综述方法段、允许/禁止结论、格式冻结 | `review_methods_plan.md`, `section_argument_plan.md` |
| 08 Manuscript | 综述正文与 Word 草稿 | `review_draft.md`, `review_draft.docx` |
| 09 Audit | 段落—来源对应矩阵与参考文献核查 | `paragraph_source_alignment_matrix.csv`, `reference_consistency_check.csv` |

## 文件结构

```text
psych-cog-neuro-review/
├── SKILL.md
├── README.md
├── references/
│   └── review_stage_contracts.md
├── scripts/
│   └── validate_run.py
├── subskills/
│   └── source-alignment/
│       └── SKILL.md
├── topic_packs/
│   └── rem_emotional_memory/
│       ├── search_terms.md
│       ├── extraction_fields.csv
│       ├── mechanism_framework.md
│       └── common_overclaim_risks.md
├── templates/
│   ├── run_mode_policy.md
│   ├── project_intake.md
│   ├── review_protocol.md
│   ├── search_strategy.md
│   ├── database_search_log.csv
│   ├── candidate_records.csv
│   ├── library_acquisition_manifest.csv
│   ├── screening_table.csv
│   ├── prisma_flow_counts.csv
│   ├── literature_matrix.csv
│   ├── neural_mechanism_matrix.csv
│   ├── quality_appraisal.csv
│   ├── reading_card.md
│   ├── prewriting_synthesis_plan.md
│   ├── evidence_gap_register.csv
│   ├── claim_evidence_map.csv
│   ├── review_methods_plan.md
│   ├── section_argument_plan.md
│   ├── manuscript_format_spec.md
│   ├── review_outline.md
│   ├── writing_style_rules.md
│   ├── stage_handoff.md
│   ├── paragraph_source_alignment_matrix.csv
│   ├── reference_audit.csv
│   └── zotero_tags.md
└── examples/
    └── rem_emotional_memory_prompt.md
```

## 使用方式

把研究主题、边界、数据库、目标风格和可用文件交给 Codex，并要求它调用 `psych-cog-neuro-review`。如果主题是 REM 与情绪记忆，可以直接复制 `examples/rem_emotional_memory_prompt.md`。

## 核心特点

- 中文优先，英文术语保留。
- 中英文文献均纳入。
- 覆盖 PubMed、Web of Science、PsycINFO、Scopus、CNKI、万方、维普、Google Scholar、Semantic Scholar、Crossref、Zotero。
- 默认执行 `standard` 全流程；也可用 `lite` 快速试跑或 `strict` 强化为范围/系统综述预备流程。
- 先完成协议、检索、获取、筛查、提取、质量评价和证据综合，再写综述正文。
- 支持自定义质量评价，并可按研究类型选择 MMAT、JBI、RoB 2、ROBINS-I、SYRCLE、AMSTAR 2。
- 强制输出检索记录、筛选表、阅读矩阵、神经机制矩阵、证据映射、综述正文、Word 草稿、参考文献核查表。
- 写完综述后，使用子 skill 生成“综述段落—文献原文/结果段落”的对应矩阵。
- 明确限制 AI 式空泛表达、虚假引用、过度因果推断和脑区功能泛化。
- 附带 `scripts/validate_run.py`，用于检查阶段文件、CSV 表头和关键 ID 连贯性。