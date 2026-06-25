# 认知神经科学内部分 skill

本目录中的分 skill 只属于 `psych-cog-neuro-review`。当认知神经科学综述工作流被调用后，Codex 可以在本目录内按阶段使用分 skill；不得把这些分 skill 当作顶层独立入口，也不得调用其他主 skill。

## 语言与文件命名

- 自然语言说明默认使用中文。
- 仅在路径名、YAML 键、数据库名、软件名、实验范式名、脑区/网络/成分名、APA/DOI/Zotero/CSV/XLSX/HTML/Markdown/BibTeX/RIS 等必要位置保留英文。
- 本地运行生成的文件夹名和文件名必须优先使用“中文主名_英文兼容名.扩展名”，具体遵循本主 skill 文件夹下的 `中文文件命名规范.md`。
- 若某个分 skill 中仍保留英文产物名示例，实际生成时应按中文文件命名规范转换。

## 推荐顺序

1. `cog-neuro-scope`：方向与任务定标，明确综述问题和机制边界。
2. `evidence-search`：认知神经科学理论、范式、指标和实证证据检索。
3. `zotero-ingest`：Zotero 入库和 PDF/题录核验。
4. `literature-screen`：认知神经科学文献分类和评级。
5. `paradigm-design`：实验范式提取、比较和质量评价。
6. `neuro-methods-design`：EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理等方法评价。
7. `neuro-data-analysis`：预处理与分析方案提取和透明性评价。
8. `mechanism-synthesis`：行为—神经/生理机制整合。
9. `source-alignment`：机制主张与原文证据对齐。
10. `manuscript-write`：认知神经科学综述正文写作。
11. `submission-review`：顶刊预备强度的模拟综述审稿。

## 统一结构要求

核心分 skill 应包含：目标、适用场景、输入、执行步骤、输出文件、中文文件命名、质量检查、失败与停止条件、安全边界、完成条件。

## 权威规范

本 workflow 应把 EEG/ERP、fMRI、PSG、眼动、NIRS、心理生理、行为任务、预处理透明性、开放科学、预注册、数据共享、APA 第 7 版、来源对齐与机制引用风险审计转化为可执行检查表。

## 顶刊预备原则

本 workflow 可以执行顶刊预备审查强度，但不得承诺发表结果。任何关键检索、筛选、机制矩阵、方法信息、预处理信息、来源对齐或投稿要求缺失时，必须停止并生成补救清单。

## 独立性

本主 skill 文件夹内部已经包含完成认知神经科学综述所需的分 skill。运行时不依赖仓库其他顶层目录。