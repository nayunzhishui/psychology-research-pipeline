# HTML 文献星图规格

用于 `07_star_map/reference_star_map.html` 和 `07_star_map/star_map_data.json`。

## 目标

把文献阅读矩阵转化为可视化证据网络，帮助用户看到：

- 哪些文献是核心证据；
- 哪些文献负责定义、测量、方法、实证结果或争议；
- 哪些理论、构念和方法连接多个文献群；
- 哪些位置是证据缺口或审稿风险点。

## 数据结构

```json
{
  "topic": "聚焦后的综述主题",
  "nodes": [
    {
      "id": "paper_001",
      "label": "Author et al. (Year)",
      "type": "paper_core",
      "weight": 0.86,
      "relevance_level": 4,
      "document_type": "empirical_longitudinal",
      "apa": "",
      "summary": "",
      "usable_for_sections": ["研究现状", "机制模型"],
      "evidence_locations": ["p. 5, Results", "Table 2"],
      "risks": ["横断外推风险", "测量不变性未检验"]
    }
  ],
  "edges": [
    {
      "source": "topic_seed",
      "target": "paper_001",
      "type": "supports",
      "weight": 0.74,
      "claim_id": "C001"
    }
  ]
}
```

## 节点类型

| 类型 | 含义 |
|---|---|
| `topic_seed` | 综述核心主题 |
| `construct` | 构念、理论概念 |
| `method` | 量表、统计模型、实验范式、神经指标 |
| `paper_core` | 4 级核心文献 |
| `paper_important` | 3 级重要文献 |
| `paper_background` | 2 级背景文献 |
| `gap` | 证据缺口 |
| `controversy` | 争议或矛盾证据 |

## 边类型

| 类型 | 含义 |
|---|---|
| `defines` | 定义或概念来源 |
| `measures` | 测量工具或操作化 |
| `tests` | 实证检验 |
| `reviews` | 综述整合 |
| `supports` | 支持主张 |
| `contradicts` | 反驳或限制主张 |
| `method_for` | 提供研究方法 |
| `cites_or_extends` | 引文链或理论延伸 |

## 权重公式

```text
paper_weight =
  0.30 * relevance_score +
  0.20 * quality_score +
  0.15 * conceptual_coverage +
  0.15 * citation_network_role +
  0.10 * recency_or_update_value +
  0.10 * writing_utility
```

### 评分说明

- `relevance_score`：1–4 级相关性归一化。
- `quality_score`：按研究设计质量域判断，不使用期刊等级代替。
- `conceptual_coverage`：覆盖定义、机制、测量、人群、争议的广度。
- `citation_network_role`：seed paper、桥接文献、被核心文献频繁引用的程度。
- `recency_or_update_value`：近年更新价值；经典理论可手动保留高值。
- `writing_utility`：可直接支撑正文关键段落的程度。

## 激活扩散规则

1. `topic_seed` 初始激活值为 1.00。
2. 激活沿边扩散：`activation_target += activation_source * edge_weight * decay`。
3. 默认 `decay = 0.65`，每增加一跳继续衰减。
4. 多条路径指向同一节点时累加，但上限为 1.00。
5. `contradicts` 边不降低文献价值，而是把节点标记为争议证据，提高审稿风险提示。
6. 扩散结果只代表综述证据连接强度，不代表因果关系、真实影响力或学术质量。

## HTML 功能要求

- 单文件 HTML，可离线打开。
- 包含图例、搜索框、等级筛选、文献类型筛选。
- 点击节点显示：APA 引文、摘要、相关性理由、质量风险、证据位置、可用于章节。
- 能突出显示核心文献、争议节点和缺口节点。
- 不加载外部不可控脚本；若使用 CDN，需提供本地备选或在说明中标注。
