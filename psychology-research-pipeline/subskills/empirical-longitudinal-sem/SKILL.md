---
name: empirical-longitudinal-sem
description: Design, generate, and audit a fail-closed longitudinal SEM workflow for empirical psychology, including longitudinal and sex-group measurement invariance, RI-CLPM, power and parameter recovery, missing-data sensitivity, school/class clustering, zero-heavy self-harm outcomes, and independent result verification. Use after research questions, scoring, data linkage, and the primary estimand are frozen. Do not use to select a model after viewing significance, infer causality from observational data, or analyze unfrozen row-level data.
---

# 纵向 SEM 实证分析

把冻结后的纵向心理学问题转换为有顺序、有门禁、可恢复的模型阶梯。默认输出分析计划与代码草案，不声称模型已运行。

## 前置门禁

确认数据哈希、计分规则、波次间隔、样本流、构念、主要估计对象、分析层级、缺失策略、聚类结构、性别变量含义和分析分类均已冻结。任一缺失则返回 `blocked`。

青少年自伤指标只有在工具原文核实排除自杀意图后才能称为 NSSI；否则沿用原始工具名称。行级自伤、学校和可识别信息只留在本地受控 R 环境。

## 执行顺序

1. 用 `scripts/generate_analysis_plan.py` 从冻结规格生成 14 步模型阶梯。
2. 人工批准计划，禁止根据主结果修改主要路径或约束。
3. 依据 `references/model-ladder.md` 执行前置测量和数据 gate。
4. 主分析采用 RI-CLPM；传统 CLPM 仅作说明性比较，不替代个体内估计。
5. 按规格执行性别直接约束检验、缺失、聚类、零值密集和替代估计敏感性。
6. 用 `powRICLPM` 与 `simsem` 报告功效、偏差、覆盖率、收敛率和模型恢复；不得只报告一个功效百分比。
7. 用 `scripts/validate_model_ladder.py` 验证阶梯完整性，再由独立结果核验角色检查输出哈希和异常估计。

## 强制解释规则

- 先检验纵向测量不变性；性别结构路径比较前另检验组间测量可比性。
- “一组显著、另一组不显著”不等于组间差异；必须直接检验相等约束。
- FIML 为主时，`mice` 多重插补与完整案例是敏感性分析，不能混成一个主要估计量。
- 学校/班级聚类已知时，使用聚类稳健修正或多层模型敏感性，并说明聚类数和小样本修正。
- 自伤零值密集时，RI-CLPM 主模型之外增加两部分、广义或贝叶斯敏感性；不得事后替换主模型以追求显著。
- 不收敛、Heywood case、不可接受参数、低覆盖率或高失败率均触发 `blocked`，不得静默删除样本或路径。

## 按需读取

- 阶梯与停止条件：`references/model-ladder.md`
- 测量不变性：`references/measurement-invariance.md`
- 缺失与聚类：`references/missingness-and-clustering.md`
- 功效、恢复与稳健性：`references/power-recovery-and-sensitivity.md`
- 输出和报告契约：`references/reporting-contract.md`
