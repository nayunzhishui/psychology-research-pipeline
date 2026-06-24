---
name: psych-review-workflow
description: Legacy auxiliary Chinese-first psychology review workflow. This file is kept for backward compatibility with older projects and for reusable review-writing rubrics, but it is not one of the three primary workflows. For new standalone literature reviews, use `psych-literature-review-workflow`. For empirical psychology papers, use `psychology-research-pipeline`. For cognitive-neuroscience or experimental-neural mechanism projects, use `psych-cog-neuro-review`. Do not use this legacy workflow to override newer skill constraints, fabricate sources, bypass access restrictions, save credentials, run unattended mass downloading, submit real manuscripts, or write claims unsupported by evidence.
---

# Psychology Review Workflow / 旧版心理学综述辅助工作流

本文件保留为**旧版辅助/历史兼容 skill**。它不是当前仓库的三个主 skill 之一，不应与新的通用综述工作流抢主入口。

当前三个主 skill 为：

1. `psychology-research-pipeline`：心理学实证论文工作流。
2. `psych-cog-neuro-review`：认知神经科学工作流。
3. `psych-literature-review-workflow`：新的通用综述工作流。

## 1. 何时使用本旧版辅助 skill

仅在以下情况使用：

- 旧项目已经明确依赖 `psych-review-workflow` 的目录或文件命名。
- 需要复用本文件中的相关性等级、质量评价、筛选矩阵或写作检查表。
- 用户明确要求继续沿用旧版综述流程。

新项目默认不要调用本文件。若任务是新的综述写作，应使用 `psych-literature-review-workflow`；若任务是实证论文，应使用 `psychology-research-pipeline`；若任务涉及认知神经科学、实验范式、EEG/ERP、fMRI、PSG、眼动或生理指标，应使用 `psych-cog-neuro-review`。

## 2. 继承约束

当本文件与新主 skill 冲突时，优先级如下：

1. 用户在当前任务中明确确认的要求。
2. 对应主 skill 的规则。
3. 本旧版辅助 skill 的规则。

尤其不得覆盖以下新版约束：中文优先、合法获取文献、Chrome + Zotero Connector 边界、两阶段聚焦、1–4 级相关性、文献矩阵、HTML 星图、APA 第 7 版、正文—来源对齐、模拟投稿必须标注模拟性质。

## 3. 可复用的文献相关性等级

相关性等级表示“对当前综述主题的使用价值”，不等于学术质量。

| 等级 | 名称 | 判定标准 | 阅读处理 |
|---|---|---|---|
| 4 | 核心文献 | 直接对应综述核心构念、目标人群/情境和关键理论、测量、方法或结果；若不引用会明显削弱综述 | 全文精读，进入矩阵和星图核心层 |
| 3 | 重要相关 | 至少直接支持一个核心板块，如概念界定、机制、测量、方法或主要实证证据 | 阅读摘要、方法、结果、讨论；必要时全文精读 |
| 2 | 背景相关 | 与主题有交集，但人群、变量、方法或理论边界不完全匹配 | 摘要和关键段落阅读，通常只作背景或边界说明 |
| 1 | 边缘相关 | 只提供一般背景、相邻概念或排除理由 | 记录后通常不纳入正文核心引用 |

辅助评分可包括：方法质量、样本适配度、理论贡献、证据强度、引用价值、与其他文献连接度。

## 4. 可复用的质量评价工具

根据文献类型选择评价标准，不要对所有文献使用同一模板：

- 系统综述/元分析：PRISMA、AMSTAR 2。
- 范围综述：PRISMA-ScR、JBI scoping review guidance。
- 叙述综述/理论综述：SANRA 或透明化叙述综述标准。
- 横断/观察性研究：STROBE。
- 随机对照/干预研究：CONSORT。
- 量表/测量文章：COSMIN。
- 质性研究：COREQ、CASP。
- 混合方法：MMAT。

质量评价必须和主题相关性分开记录。高质量但不贴题的文献不能自动进入核心论证；贴题但质量弱的文献必须降权或标注局限。

## 5. 可复用的输出模板

### 导师汇报版简表

```csv
候选方向,核心问题,文献基础,创新点,风险,推荐等级,下一步建议
```

### 阅读矩阵核心字段

```csv
stable_id,文献类型,相关性等级,方法质量,样本适配度,理论贡献,证据强度,引用价值,核心构念,人群/样本,研究设计,测量/任务,统计方法,主要发现,局限,可引用位置,适合写入章节,是否需要复核
```

### 正文—来源对齐表

```csv
综述页码,综述段落,综述原句,支撑文献,文献页码,文献章节/段落/表图,原文证据短摘录,证据类型,支持强度,是否需要复核
```

## 6. 数据库边界

默认数据库沿用新版主 skill 的范围：PubMed、PsycINFO、Web of Science、Crossref、Google Scholar（辅助）、CNKI、期刊官网、Zotero 本地库。

不要默认加入 Scopus、APA PsycNet、Semantic Scholar、OpenAlex、SinoMed、万方或维普。用户明确要求时才作为附加数据库，并记录理由、检索式、结果数和局限。

## 7. 安全边界

- 不伪造文献、DOI、页码、PDF、样本、统计结果、审稿意见或期刊反馈。
- 不绕过数据库权限、验证码、MFA、付费墙、下载限制或出版社条款。
- 不保存账号、密码、验证码、cookie、token、密钥或浏览器身份凭据。
- 不使用盗版论文站、影子图书馆、PDF bot 或泄露账号。
- 不无人值守高速批量下载。
- 不把 Zotero 数据库、PDF、浏览器凭据或受限全文提交到 GitHub。
- 不真实投稿、支付费用或联系编辑，除非用户另行明确授权并在操作时确认。

## 8. 维护说明

本文件后续只作为辅助材料维护。若要新增综述写作能力，优先更新 `psych-literature-review-workflow`；若要新增实证研究能力，优先更新 `psychology-research-pipeline`；若要新增认知神经科学、实验范式或脑机制能力，优先更新 `psych-cog-neuro-review`。
