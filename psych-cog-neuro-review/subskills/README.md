# Cognitive Neuroscience Workflow Subskills / 认知神经科学内部分 skill

本目录中的分 skill 只属于 `psych-cog-neuro-review`。当认知神经科学工作流被调用后，Codex 可以在本目录内按阶段使用分 skill；不得把这些分 skill 当作顶层独立入口，也不得调用其他主 skill。

## 推荐顺序

1. `cog-neuro-scope`：任务定标，判断综述、实验设计、实证论文或数据分析。
2. `evidence-search`：认知神经科学理论、范式、指标和实证证据检索。
3. `zotero-ingest`：Zotero 入库和 PDF/题录核验。
4. `literature-screen`：认知神经科学文献分类和评级。
5. `paradigm-design`：实验范式、刺激材料和任务流程设计。
6. `neuro-methods-design`：EEG/ERP、fMRI、PSG、眼动、生理指标方法设计。
7. `neuro-data-analysis`：预处理和分析计划。
8. `mechanism-synthesis`：行为—神经/生理机制整合。
9. `source-alignment`：机制主张与原文证据对齐。
10. `manuscript-write`：认知神经科学综述或实证论文写作。
11. `submission-review`：模拟投稿审稿。

## 独立性

本主 skill 文件夹内部已经包含完成认知神经科学综述、实验设计和实证项目所需的分 skill。运行时不依赖仓库其他顶层目录。