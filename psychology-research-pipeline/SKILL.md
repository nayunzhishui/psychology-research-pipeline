---
name: psychology-research-pipeline
description: End-to-end, Chinese-first workflow for auditable empirical psychology papers. Use for cross-sectional, longitudinal, experimental, intervention, psychometric, developmental, clinical, or health psychology projects that require scoping, evidence search, measurement design, data audit, statistical analysis, APA-compatible writing, claim-source alignment, and simulated submission review. Especially use when the user has SPSS/CSV/Excel data, repeated-measures panels, SEM or RI-CLPM questions, sensitive adolescent data, or needs a submission-ready evidence package. Do not use for literature-review-only projects, fabricated data or citations, bypassing access controls, or real journal submission.
---

# 心理学实证论文工作流

在本 skill 内完成从项目定标到模拟投稿审查的可审计流程。默认中文沟通；数据库检索式、量表名、变量名、统计模型、软件输出、APA 引文和文件扩展名保留必要英文。

## 核心规则

- 先冻结问题、估计对象、变量、计分和分析计划，再查看主结果。
- 区分主要、次要和探索性分析；所有偏离均进入偏离记录。
- 不伪造文献、量表来源、伦理信息、数据、统计量或期刊反馈。
- 不从观察性关联推出因果；不以“一组显著、另一组不显著”证明组间差异。
- 不覆盖旧运行；修订使用新版本并记录原因。
- 涉及青少年自伤时，限制行级数据、学校标识和小单元组合的暴露。
- 遇到关键阻断条件，生成 `停止原因与补救清单_stop_reason_and_fix.md`，不得生成“可投稿”结论。

## 启动

从已有材料提取并确认：研究设计、用途、核心构念、样本、波次、数据状态、分析软件、文献获取方式、目标期刊和输出格式。未确认项作为 `assumption` 写入 `日志/决策记录_decisions.md`。

所有自动化只通过统一入口 `scripts/pipeline.py` 调用；兼容脚本只供测试和内部转发。首次运行并盘点资料：

```powershell
python scripts/pipeline.py init --project <项目目录> --title <题目> --mode strict
python scripts/pipeline.py inventory --run-dir <运行目录> --source <资料目录>
```

通用工作流不得硬编码单一课题。特定研究通过 `--project-pack <课题包目录>` 附加版本化 profile、数据审计规格和分析规格；初始化时复制并哈希到运行目录。旧版十阶段运行仅通过 `pipeline.py migrate` 迁移已识别文本产物；未映射文件只记哈希、不复制，迁移后仍必须通过十二阶段 gate。

模式：

- `lite`：定标、种子证据、变量模型和方法草案。
- `standard`：完成全部阶段并形成普通投稿预备包。
- `strict`：增加冻结协议、数据/代码审计、来源对齐和强制 gate。
- `top-journal-prep`：在 strict 基础上增加反对性审稿和不可投稿风险清单；不承诺发表。

## 唯一目录契约

运行目录固定为 `实证论文运行/<run-id>/`：

```text
状态记录_state.json
文件清单_manifest.json
日志/决策记录_decisions.md
日志/事件记录_events.jsonl
文献/
00_项目定标/
01_标准与协议/
02_证据检索/
03_Zotero与全文获取/
04_文献筛选与小综述/
05_方法设计/
06_数据管理/
07_统计分析/
08_结果与图表/
09_论文正文/
10_对齐审计/
11_模拟投稿审稿/
```

脚本、stage contract、模板和 gate 必须使用这一契约；禁止创建另一套英文阶段目录。

## 阶段执行

1. **00 项目定标**：定义主要研究问题、估计对象、推论边界、构念—变量映射和不可做事项。
2. **01 标准与协议**：冻结假设、结局、纳排、伦理、开放科学、偏离政策和适用报告规范。
3. **02 证据检索**：记录精确检索式、平台、日期、结果数和候选记录。
4. **03 Zotero与全文获取**：合法入库、去重、核验题录和可读 PDF；失败保留明确状态。
5. **04 筛选与小综述**：区分相关性与质量，提取证据位置，保留矛盾与零结果，建立主张—证据映射。
6. **05 方法设计**：冻结样本、量表计分、缺失、估计量、协变量、聚类、乘法性、稳健性和模型比较。
7. **06 数据管理**：核验 ID、波次连接、重复、范围、异常编码、反向计分、缺失、流失、分布和隐私风险。
8. **07 统计分析**：只按冻结计划运行；保存代码、软件版本、随机种子、输入哈希、输出和偏离。
9. **08 结果与图表**：报告估计值、不确定性、效应量、拟合、诊断、稳健性和探索性标记。
10. **09 论文正文**：按目标期刊和 APA JARS 组织题目、摘要、引言、方法、结果、讨论、声明与参考文献。
11. **10 对齐审计**：逐项核对正文主张、引用、代码、数字、表图和方法。
12. **11 模拟投稿审稿**：实时核查期刊官网；模拟主编、理论、方法、统计、测量、开放科学和反对性审稿。

## 自动化命令

按阶段生成、验证和推进；任何命令返回 `blocked` 时停止，不得绕过：

```powershell
python scripts/pipeline.py audit-data --run-dir <运行目录> --data <sav或csv> --spec <审计规格json> [--private-register <本地私密jsonl>]
python scripts/pipeline.py freeze-data --run-dir <运行目录> --data <数据> --spec <规格> [--decisions <逐项决策json>]
python scripts/pipeline.py plan-search --run-dir <运行目录> --spec <search-plan.json>
python scripts/pipeline.py import-evidence --run-dir <运行目录> --search-id <search-id> --input <导出文件> [--input <导出文件> ...]
python scripts/pipeline.py dedupe-evidence --run-dir <运行目录> --input <候选文献csv>
python scripts/pipeline.py cluster-studies --run-dir <运行目录> --input <去重后csv>
python scripts/pipeline.py audit-evidence-coverage --run-dir <运行目录> --input <已标注证据csv> --requirements <coverage.json>
python scripts/pipeline.py build-retrieval-queue --run-dir <运行目录> --input <已标注证据csv>
python scripts/pipeline.py refresh-search --run-dir <运行目录> --baseline <旧候选csv> --current <新候选csv>
python scripts/pipeline.py generate-analysis --run-dir <运行目录> --data <冻结数据> --spec <分析规格json>
python scripts/pipeline.py run-analysis --run-dir <运行目录> --manifest <代码清单json> [--rscript <Rscript路径>]
python scripts/pipeline.py validate-results --run-dir <运行目录> --input <模型输出json>
python scripts/pipeline.py render-manuscript --run-dir <运行目录> --template <正文模板> --results <已验证结果json> --claims <主张表csv> --references <bib>
python scripts/pipeline.py build-submission --run-dir <运行目录> --journal-policy <实时核查json> --manuscript <正文> --numeric-audit <数字审计json> --claim-audit <主张审计md>
```

`generate-analysis` 生成测量不变性、RI-CLPM、直接组间约束检验、零值密集两部分敏感性和模拟检验力 R 代码，但不把“已生成”写成“已执行”。`run-analysis` 核验代码哈希、真实调用 R、保存逐脚本日志并检查预期输出；仍须经 `validate-results` 才能进入正文。`freeze-data` 对每个结构化 issue 要求与当前审计哈希绑定的允许处置；ID 错配和计分错误不得用“分析适配”绕过。

私密问题登记必须位于 `.private/` 或其他不会提交的位置，只保存伪匿名标识与定位信息；不得进入文件清单、论文或投稿包。期刊政策必须来自声明的官方域名，并保存核查日期、页面快照与 SHA-256。

检查单阶段或自动推进所有已满足阶段：

```powershell
python scripts/pipeline.py gate --run-dir <运行目录> --stage <stage-id>
python scripts/pipeline.py gate --run-dir <运行目录> --stage <stage-id> --advance
python scripts/pipeline.py verify-run --run-dir <运行目录>
python scripts/pipeline.py autopilot --run-dir <运行目录>
```

`autopilot` 只自动推进已通过证据 gate 的阶段；缺资料、关键判断未确认或占位符未清除时安全停止。它不会生成研究事实、伦理信息、统计结果或期刊反馈。

## 按需读取

- 阶段输入、输出、字段与 gate：读取 `references/stage-contracts.md`。
- 纵向面板、RI-CLPM、自伤和性别差异：读取 `references/longitudinal-panel-nssi.md`。
- 报告规范选择：读取 `references/psychology-standards.md`。
- 文献与 Zotero 工具路线：读取 `references/tool-routing.md`。
- 文献自动化命令、题录字段、去重和覆盖 gate：读取 `references/literature-automation.md`。
- 特定课题变量、数据规格与风险：仅在该课题运行时读取相应 `project-packs/<id>/`。
- JSON 机器契约：按输入类型读取 `schemas/` 中对应 schema。
- 运行模板由 `scripts/pipeline_schema.py` 生成；顶层 `templates/` 仅提供可复用工作表，不定义运行目录。

## 强制停止条件

- ID、波次连接或量表计分规则无法确认。
- 没有数据却要求写结果，或没有输出却要求写统计量。
- 核心变量跨波不可比且无法修复。
- 关键自伤变量存在无法解释的负值、极端值或编码混合。
- 没有全文却要求页码级强引用。
- 没有伦理材料却要求声称伦理合规。
- 没有来源对齐或期刊官网核查却要求“可投稿”。

## 完成条件

仅在用户要求的阶段通过 gate、关键数字可追溯、未解决风险明确列出后结束。返回运行目录、完成阶段、改动文件、主要结果、验证、偏离和 blocker；不得把模拟审稿表述为真实期刊反馈。
