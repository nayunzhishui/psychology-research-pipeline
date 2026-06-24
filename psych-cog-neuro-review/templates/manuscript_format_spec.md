# 正文格式规范 / Manuscript Format Specification

## 1. 格式轨道

本 skill 支持两个默认正文轨道：

1. 中文核心综述轨道
2. 外文 Q1 review 预备稿轨道

可同时生成双轨结构，但必须在 `07_prewrite/review_methods_plan.md` 中说明优先轨道。

## 2. 中文核心综述轨道

### 2.1 推荐结构

```text
中文题目
作者信息（如需要）
中文摘要
关键词
1 引言
2 核心概念与理论基础
3 研究证据与主要发现
4 认知神经机制
5 影响因素与边界条件
6 现有研究不足
7 未来研究方向
8 结论
参考文献
```

### 2.2 写作要求

- 摘要应交代主题、目的、证据范围、主要结论和启示，不写空泛背景。
- 引言末段必须说明本文综述范围和结构。
- 每个一级标题下应有明确论证任务，不使用堆砌式文献罗列。
- 参考文献格式最终按目标期刊要求调整；未确定期刊时先保持一致性。
- 不把英文关键词全部硬译，脑区、范式、量表、数据库名可保留英文原词。

## 3. 外文 Q1 review 预备稿轨道

### 3.1 推荐结构

```text
Title
Abstract
Keywords
1. Introduction
2. Scope and Review Approach
3. Conceptual and Theoretical Background
4. Behavioral Evidence
5. Neural and Physiological Mechanisms
6. Moderators and Boundary Conditions
7. Methodological Limitations and Open Questions
8. Integrative Framework
9. Future Directions
10. Conclusion
References
```

### 3.2 写作要求

- 需要有明确的 contribution statement。
- 每节要围绕问题推进，而不是按文献年份堆叠。
- 机制模型必须区分 direct evidence、indirect evidence、speculative inference。
- 对 neuroimaging/EEG/PSG 结果必须避免 reverse inference。
- 如果不是 systematic review，不要使用 systematic search、PRISMA-compliant review 等表述。

## 4. Word 输出要求

生成 `review_draft.docx` 时尽量包含：

- 标题层级：Title, Heading 1, Heading 2, Normal
- 中文字体优先宋体或等效中文字体；英文字体 Times New Roman 或等效字体
- 表格使用可编辑 Word 表格，不使用截图
- 图题和表题独立编号
- 文内引用与参考文献列表保持一致
- 段落 ID 可保留在隐藏注释或段首标记中；最终投稿版可移除

## 5. 格式检查清单

| 项目 | 中文核心 | Q1 review | 状态 | 备注 |
|---|---|---|---|---|
| 题目是否明确机制或对象 | required | required |  |  |
| 摘要是否有证据范围 | required | required |  |  |
| 是否有综述方法/范围说明 | recommended | required |  |  |
| 是否区分直接证据与推断 | required | required |  |  |
| 是否有机制整合图/表 | recommended | recommended |  |  |
| 是否有局限与未来方向 | required | required |  |  |
| 文内引用与参考文献是否一致 | required | required |  |  |
| 段落—来源矩阵是否完成 | required | required |  |  |