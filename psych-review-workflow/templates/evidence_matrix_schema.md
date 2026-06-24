# 文献阅读矩阵字段模板

用于 `05_matrix/evidence_matrix.csv`。字段可按综述主题删减，但不得删除稳定 ID、相关性等级、证据位置、质量风险和可用章节。

## 推荐 CSV 表头

```csv
paper_id,study_id,zotero_key,bibtex_key,citation_apa,year,document_type,relevance_level,relevance_reason,quality_domains,quality_concerns,review_role,constructs,population,age_range,country_or_region,sample_size,design,measures,methods_or_analysis,key_findings,effect_or_result_summary,mechanism_claim,limitations,contradictions,relation_to_topic,usable_for_sections,evidence_location,short_quote,claim_id,notes
```

## 字段说明

| 字段 | 含义 | 必填 |
|---|---|---|
| `paper_id` | 稳定文献 ID，优先 DOI/PMID | 是 |
| `study_id` | 同一样本或同一研究的多个报告共享 ID | 建议 |
| `zotero_key` | Zotero parent item key | Zotero 入库后必填 |
| `bibtex_key` | BibTeX citekey | 写作前必填 |
| `citation_apa` | APA 7 参考文献条目草案 | 是 |
| `document_type` | 文献类型，多标签可用 `;` 分隔 | 是 |
| `relevance_level` | 1–4 级相关性 | 是 |
| `relevance_reason` | 相关性理由 | 是 |
| `quality_domains` | 按研究设计评价的质量域 | 是 |
| `quality_concerns` | 方法风险或报告不足 | 是 |
| `review_role` | 在综述中的角色：定义/理论/测量/方法/实证/争议/背景 | 是 |
| `constructs` | 主要构念 | 是 |
| `population` | 样本或人群 | 实证文献必填 |
| `sample_size` | 样本量 | 实证文献必填 |
| `design` | 研究设计 | 是 |
| `measures` | 量表、任务、指标 | 视文献而定 |
| `methods_or_analysis` | 统计方法、实验范式、综述方法 | 是 |
| `key_findings` | 可转述的核心发现 | 是 |
| `effect_or_result_summary` | 效应方向、主要结果、置信区间或定性主题 | 视文献而定 |
| `mechanism_claim` | 文献是否提出机制解释 | 建议 |
| `limitations` | 作者限制 + 阅读者判断 | 是 |
| `contradictions` | 与其他证据的冲突 | 建议 |
| `relation_to_topic` | 与本综述主题的具体关系 | 是 |
| `usable_for_sections` | 可用于哪些章节 | 是 |
| `evidence_location` | 页码、章节、段落、表格或图号 | 是 |
| `short_quote` | 必要短引文，便于核查 | 可选 |
| `claim_id` | 将来对应正文主张 | 写作前必填 |
| `notes` | 其他备注 | 可选 |

## 相关性等级速查

| 等级 | 判断 |
|---|---|
| 4 | 核心文献：直接支撑主题核心定义、机制、测量、方法或主要结论 |
| 3 | 重要相关：支撑某一关键板块，但不是全篇核心 |
| 2 | 背景/边缘：可用于背景或方法参考，不能承担关键论证 |
| 1 | 弱相关/排除：不进入正文证据链，记录原因即可 |

## 质量评价提醒

不要用期刊等级、影响因子或引用量替代方法质量。评价时至少考虑：样本、测量、设计、混杂、缺失、统计/分析、报告透明度、适用性、过度推论风险。
