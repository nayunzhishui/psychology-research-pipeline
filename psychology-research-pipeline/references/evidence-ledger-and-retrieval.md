# 证据账本与检索索引

## 三层存储

1. **不可变原始来源**：数据库原始导出、Zotero 题录、合法 PDF、问卷与伦理材料；只追加，不由摘要覆盖。
2. **结构化证据账本**：一条研究证据一个 `EvidenceLedgerRecord`，记录 DOI、设计、样本、测量、波次、效应与不确定性、主张编号、页码/表格位置、勘误状态和核验状态。
3. **可重建索引**：仅收录 `fulltext-verified` 或 `claim-verified` 记录，存放在运行目录 `.cache/`，可随时从账本重建。

执行：

```powershell
python scripts/pipeline.py build-evidence-index --run-dir <运行目录> --ledger <证据账本.jsonl>
```

## RAG 权限

RAG 可定位候选段落、量表出处、模型描述并生成待核验摘要；不得决定纳排、主要假设、NSSI 定义、因果主张、统计数字或文献是否支持某个主张。任何进入正文的数字或强主张都必须回到原始全文位置和证据账本复核。

ASReview 等主动学习工具只排序待筛选记录；最终纳排必须由人工确认，并保留审阅者、理由和裁决。
