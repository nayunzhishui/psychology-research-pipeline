---
name: empirical-data-analysis
description: Local subskill under psychology-research-pipeline for empirical psychology data audit, statistical analysis, and result verification. Chinese-first; use only inside the empirical workflow.
---

# 数据分析分 skill

## 目标

对实证论文数据进行结构审计、统计分析、结果核验和偏离记录，确保结果可追溯、可复核、不过度解释。

## 适用场景

- 用户已有 Excel、CSV、SPSS、PROCESS、AMOS、Mplus、R、Python、JASP 输出或统计表。
- 需要执行或解释描述统计、信度、相关、回归、中介/调节、SEM、实验差异检验等。

## 输入

- 数据文件或统计输出。
- 数据字典、量表计分规则、统计分析计划、缺失值和异常值处理方案。
- 研究问题与假设、变量角色、样本说明。

## 执行步骤

1. 检查数据字典、变量名、反向计分、缺失值、异常值、剔除规则和协变量处理。
2. 对照冻结的统计分析计划，区分验证性分析、次要分析和探索性分析。
3. 执行或解释统计分析，记录软件、版本、语法或操作步骤。
4. 输出 APA 结果文本、表格建议、图表建议和稳健性检查。
5. 核对正文数字、表格、图、p 值、效应量、置信区间和模型拟合指标。
6. 记录所有计划外分析和模型修改。

## 输出文件

- `数据字典_data_dictionary.csv`
- `数据质量审计_data_audit.md`
- `统计分析报告_analysis_report.md`
- `分析偏离记录_analysis_deviation_log.csv`
- `结果表格_results_tables.md`
- `数字核查报告_numeric_audit.md`

## 中文文件命名

所有本地输出必须使用“中文主名_英文兼容名.扩展名”。

## 质量检查

- 是否按冻结分析计划执行？
- 是否记录缺失值、异常值、剔除、反向计分和协变量？
- 统计结果是否含必要效应量和置信区间？
- 探索性分析是否明确标注？
- 正文数字是否与软件输出一致？

## 失败与停止条件

- 没有数据，不得写结果。
- 没有统计输出，不得写 p 值、效应量、置信区间或模型拟合指标。
- 变量含义不清、计分规则不明或反向题无法确认时停止。
- 数据与样本说明不一致时停止。
- 用户要求伪造显著结果或美化统计结论时停止。

## 安全边界

不伪造数据、样本量、描述统计、信效度、模型拟合、p 值、置信区间、效应量或图表。

## 完成条件

生成数据审计、统计分析报告、分析偏离记录、结果表格和数字核查报告，并明确哪些结果可写入论文。