# 检索策略模板 / Search Strategy

## 1. 检索主题

- 中文主题：
- English topic:
- 运行模式：lite / standard / strict
- 核心概念 1：
- 核心概念 2：
- 核心概念 3：
- 目标人群：
- 方法限定：behavioral / EEG / ERP / fMRI / PSG / sleep lab / questionnaire / meta-analysis
- 是否加载 REM 情绪记忆 topic pack：是 / 否

## 2. 英文关键词

### REM/sleep terms

```text
"REM sleep" OR "rapid eye movement sleep" OR dream* OR "sleep architecture" OR "REM density" OR "REM duration" OR "REM latency" OR polysomnography OR PSG OR nap OR "sleep deprivation" OR "sleep restriction"
```

### Emotional memory terms

```text
"emotional memory" OR "affective memory" OR "fear memory" OR "fear conditioning" OR extinction OR "extinction recall" OR "memory consolidation" OR reconsolidation OR "emotional reactivity" OR "emotion regulation"
```

### Cognitive neuroscience terms

```text
EEG OR ERP OR fMRI OR neuroimaging OR "functional connectivity" OR amygdala OR hippocampus OR "prefrontal cortex" OR vmPFC OR dlPFC OR ACC OR insula OR theta OR alpha OR LPP OR P300
```

## 3. 中文关键词

```text
快速眼动睡眠 OR REM睡眠 OR 梦 OR 睡眠结构 OR REM密度 OR REM时长 OR REM潜伏期 OR 多导睡眠图 OR 睡眠剥夺 OR 睡眠限制 OR 小睡
```

```text
情绪记忆 OR 情感记忆 OR 恐惧记忆 OR 恐惧条件反射 OR 恐惧消退 OR 消退回忆 OR 记忆巩固 OR 再巩固 OR 情绪反应 OR 情绪调节
```

```text
脑电 OR 事件相关电位 OR 功能磁共振 OR 神经影像 OR 功能连接 OR 杏仁核 OR 海马 OR 前额叶 OR 前扣带回 OR 岛叶
```

## 4. 推荐英文检索式

### Broad query

```text
("REM sleep" OR "rapid eye movement sleep" OR "sleep deprivation" OR nap OR polysomnography)
AND
("emotional memory" OR "affective memory" OR "fear memory" OR "fear conditioning" OR extinction OR "memory consolidation")
AND
(EEG OR ERP OR fMRI OR neuroimaging OR amygdala OR hippocampus OR "prefrontal cortex" OR "functional connectivity" OR behavior*)
```

### Mechanism-focused query

```text
("REM sleep" OR "rapid eye movement sleep" OR "REM density" OR "REM duration")
AND
(amygdala OR hippocampus OR vmPFC OR "prefrontal cortex" OR theta OR LPP OR P300 OR "functional connectivity")
AND
("emotional memory" OR extinction OR "fear conditioning" OR "memory consolidation")
```

### Review/meta-analysis query

```text
("REM sleep" OR "rapid eye movement sleep")
AND
("emotional memory" OR "fear memory" OR extinction OR "memory consolidation")
AND
(review OR meta-analysis OR systematic OR scoping)
```

## 5. 推荐中文检索式

### 中文宽检索

```text
(快速眼动睡眠 OR REM睡眠 OR 睡眠剥夺 OR 多导睡眠图 OR 小睡)
AND
(情绪记忆 OR 恐惧记忆 OR 恐惧条件反射 OR 恐惧消退 OR 记忆巩固)
```

### 中文机制检索

```text
(快速眼动睡眠 OR REM睡眠 OR REM密度 OR REM时长 OR 多导睡眠图)
AND
(杏仁核 OR 海马 OR 前额叶 OR 脑电 OR 事件相关电位 OR 功能磁共振 OR 功能连接)
AND
(情绪记忆 OR 恐惧记忆 OR 恐惧消退 OR 记忆巩固)
```

## 6. 数据库适配提醒

| 数据库 | 重点 | 注意事项 |
|---|---|---|
| PubMed | MeSH + Title/Abstract | 不要直接使用中文词；记录 MeSH/tiab 版本 |
| Web of Science | Topic search | 记录 Web of Science Core Collection 还是其他集合 |
| PsycINFO | 心理学主题词 | 注意 EBSCO/Ovid 平台语法差异 |
| Scopus | TITLE-ABS-KEY | 记录文献类型过滤 |
| CNKI | 中文主题、篇名、关键词、摘要 | 记录来源类别、学科、发表时间、中文检索字段 |
| 万方 | 中文期刊/学位论文补充 | 记录检索字段和学科过滤 |
| 维普 | 中文期刊补充 | 记录题名/关键词/摘要范围 |
| Google Scholar | 补充发现和引文追踪 | 结果波动大，只记录前 N 条策略 |
| Semantic Scholar | 语义检索与相似文献 | 适合补充，不代表穷尽 |
| Crossref | DOI/元数据核查 | 不作为主题检索主来源 |
| Zotero | 本地文献库 | 记录 collection、tag、搜索字段和导出时间 |

## 7. 数据库记录表

| database | query | date | filters | result_count | exported_records | notes |
|---|---|---|---|---:|---:|---|
| PubMed |  |  |  |  |  |  |
| Web of Science |  |  |  |  |  |  |
| PsycINFO |  |  |  |  |  |  |
| Scopus |  |  |  |  |  |  |
| CNKI |  |  |  |  |  |  |
| 万方 |  |  |  |  |  |  |
| 维普 |  |  |  |  |  |  |
| Google Scholar |  |  |  |  |  |  |
| Semantic Scholar |  |  |  |  |  |  |
| Crossref |  |  |  |  |  |  |
| Zotero |  |  |  |  |  |  |

## 8. 检索规则

- 每次检索必须记录日期、数据库、完整检索式、筛选条件和结果数。
- 不同数据库的语法可以调整，但核心概念组合必须保持可追踪。
- Google Scholar 结果波动较大，只作为补充发现和引文追踪来源。
- CNKI、万方、维普检索需记录中文主题词、篇名/摘要/关键词范围和学科限制。
- Zotero 本地库检索需记录 collection、tag、搜索字段和导出时间。
- strict 模式下，任何未检索数据库必须写入 deviation log。