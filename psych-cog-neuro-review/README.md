# psych-cog-neuro-review

这是一个面向心理学与认知神经科学文献综述的 Codex skill 文件夹。它用于把“检索—筛选—阅读矩阵—神经机制提取—综述写作—参考文献对应核查”固定成可复用流程。

## 适用范围

- 通用心理学文献综述
- 认知神经科学综述
- REM sleep 与情绪记忆主题
- EEG/ERP、fMRI、行为实验、量表、睡眠实验、多方法整合综述
- 中文核心综述风格或外文 Q1 review 预备稿风格

## 文件结构

```text
psych-cog-neuro-review/
├── SKILL.md
├── README.md
├── subskills/
│   └── source-alignment/
│       └── SKILL.md
├── templates/
│   ├── project_intake.md
│   ├── search_strategy.md
│   ├── database_search_log.csv
│   ├── screening_table.csv
│   ├── literature_matrix.csv
│   ├── neural_mechanism_matrix.csv
│   ├── claim_evidence_map.csv
│   ├── review_outline.md
│   ├── writing_style_rules.md
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
- 覆盖 PubMed、Web of Science、PsycINFO、Scopus、CNKI、Google Scholar、Semantic Scholar、Crossref、Zotero。
- 强制输出检索记录、筛选表、阅读矩阵、神经机制矩阵、证据映射、综述正文、Word 草稿、参考文献核查表。
- 写完综述后，使用子 skill 生成“综述段落—文献原文/结果段落”的对应矩阵。
- 明确限制 AI 式空泛表达、虚假引用、过度因果推断和脑区功能泛化。
