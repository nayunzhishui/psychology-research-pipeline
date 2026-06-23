# 运行模式策略 / Run Mode Policy

## 1. 模式选择

| 模式 | 适用情境 | 必须执行 | 可简化 | 不得声称 |
|---|---|---|---|---|
| `lite` | 早期选题、课程论文、快速文献地图 | 00 Scope, 02 Search sketch, 05 Initial extraction, 06 Initial synthesis, 07 Outline | 可不做完整 PRISMA flow、正式质量评价、全文筛查 | exhaustive search, systematic review, publication-ready |
| `standard` | 研究生综述、中文核心预备稿、机制综述 | 00–09 全阶段 | 可单人筛查；正式质量工具可选但需说明 | dual screening, preregistration, systematic review unless actually done |
| `strict` | 系统综述、范围综述、Q1 review 预备稿 | 00–09 全阶段，正式协议，PRISMA-style 记录，正式质量工具按需使用 | 不建议简化；任何缺口都标为 blocker/deviation | 不可省略关键数据库后仍声称 exhaustive |

## 2. 默认规则

- 未指定时使用 `standard`。
- 默认综述类型为“混合型机制综述”。
- 只有当检索、筛查、质量评价和报告规范满足要求时，才能称为 systematic review 或 scoping review。
- 运行模式一旦写入 `review_protocol.md`，下游阶段不得静默改变。

## 3. 升级与降级

| 变更 | 允许条件 | 必需记录 |
|---|---|---|
| `lite` → `standard` | 用户需要完整综述或可投稿草稿 | 需要补齐被跳过的阶段 |
| `standard` → `strict` | 用户需要系统/范围综述或 Q1 review 级别透明度 | 需要补正式协议、质量工具和更严格筛查 |
| `strict` → `standard` | 数据库权限、时间、全文获取或筛查资源不足 | 记录 blocker、影响范围、不得称系统综述 |
| `standard` → `lite` | 用户只要早期探索材料 | 记录哪些 gate 不再适用 |

## 4. 最小输出

### lite

- `00_scope/review_scope.md`
- `02_search/search_strategy.md`
- `05_extraction/literature_matrix.csv` 初版
- `06_synthesis/prewriting_synthesis_plan.md` 初版
- `07_prewrite/review_outline.md` 或 `section_argument_plan.md`

### standard

- 完整 00–09 目录
- 检索记录、筛查表、阅读矩阵、神经机制矩阵、质量评价表
- claim-evidence map
- Markdown + Word 草稿
- 段落—来源对应矩阵

### strict

- standard 全部产物
- 正式报告规范说明
- PRISMA-style flow counts
- 正式质量评价工具记录
- 更详细的 deviation log
- 不支持结论的 blocker list

## 5. 最终回复必须说明

- 本次使用的 run mode
- 是否有升级或降级
- 哪些阶段完成
- 哪些 gate 未通过
- 哪些结论只能作为 tentative claim
- 是否可以称为 systematic/scoping review；如果不能，必须明确说明不能