# 心理学实证论文内部分 skill

本目录中的分 skill 只属于 `psychology-research-pipeline`。当主工作流被调用后，Codex 可以在本目录内按任务阶段使用分 skill；不得把这些分 skill 当作顶层独立入口，也不得调用其他主 skill。

## 语言与文件命名

- 自然语言说明默认使用中文。
- 仅在路径名、YAML 键、数据库名、软件名、统计模型名、变量名、APA/DOI/Zotero/CSV/XLSX/HTML/Markdown 等必要位置保留英文。
- 本地运行生成的文件夹名和文件名默认使用中文，具体遵循本主 skill 文件夹下的 `中文文件命名规范.md`。
- 若某个分 skill 中仍保留英文产物名示例，实际生成时应按中文文件命名规范转换。

## 推荐顺序

1. `project-scope`：选题、研究问题、假设、变量模型。
2. `evidence-search`：理论、方法、量表和实证依据检索。
3. `zotero-ingest`：Chrome + Zotero Connector 入库和 PDF/题录核验。
4. `literature-screen`：实证论文所需文献分类、筛选、小综述和证据矩阵。
5. `methods-design`：样本、量表、任务、伦理、开放科学和分析计划。
6. `data-analysis`：数据审计、统计分析、结果解释和偏离记录。
7. `reporting-standards`：STROBE、CONSORT/SPIRIT、测量研究、开放科学报告规范。
8. `manuscript-write`：APA 实证论文写作。
9. `source-alignment`：正文主张、参考文献、统计数字、表图和方法描述对齐。
10. `submission-review`：模拟投稿审稿和修改矩阵。

## 独立性

本主 skill 文件夹内部已经包含完成实证论文项目所需的分 skill。运行时不依赖仓库其他顶层目录。