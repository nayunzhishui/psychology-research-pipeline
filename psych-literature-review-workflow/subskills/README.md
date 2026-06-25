# 通用综述内部分 skill

本目录中的分 skill 只属于 `psych-literature-review-workflow`。当新的通用综述工作流被调用后，Codex 可以在本目录内按阶段使用分 skill；不得把这些分 skill 当作顶层独立入口，也不得调用其他主 skill。

## 语言与文件命名

- 自然语言说明默认使用中文。
- 仅在路径名、YAML 键、数据库名、量表名、理论名、APA/DOI/Zotero/CSV/XLSX/HTML/Markdown/BibTeX/RIS 等必要位置保留英文。
- 本地运行生成的文件夹名和文件名默认使用中文，具体遵循本主 skill 文件夹下的 `中文文件命名规范.md`。
- 若某个分 skill 中仍保留英文产物名示例，实际生成时应按中文文件命名规范转换。

## 推荐顺序

1. `review-scope`：宽方向探索和综述聚焦。
2. `evidence-search`：正式综述检索和饱和停止日志。
3. `zotero-ingest`：Chrome + Zotero Connector 入库。
4. `literature-screen`：分类、纳排和 1–4 级相关性评级。
5. `literature-matrix`：全文阅读矩阵和证据提取。
6. `star-map`：基于阅读矩阵和激活扩散权重制作 HTML 文献星图。
7. `source-alignment`：正文—参考文献—原文证据对齐。
8. `manuscript-write`：APA 综述正文写作。
9. `submission-review`：中文/英文期刊模拟审稿。
10. `mini-review`：早期小综述或课程小综述。
11. `old-review-workflow`：旧版综述流程迁移和兼容。

## 独立性

本主 skill 文件夹内部已经包含完成通用心理学综述所需的分 skill。运行时不依赖仓库其他顶层目录。