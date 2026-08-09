# 资源索引

按需读取，避免一次加载全部资源：

| 任务 | 必读资源 |
|---|---|
| 初始化、推进和 gate | `references/stage-contracts.md`、`scripts/pipeline_schema.py` |
| 五层科研架构、角色契约与有界 Loop | `references/research-system-architecture.md`、`references/controlled-research-roles.md`、`scripts/research_orchestrator.py` |
| 证据账本与可重建 RAG 索引 | `references/evidence-ledger-and-retrieval.md`、`scripts/evidence_ledger.py`、`schemas/evidence-ledger.schema.json` |
| 工具权限与能力清单 | `references/tool-capabilities.json`、`scripts/tool_registry.py`、`schemas/tool-capability.schema.json` |
| R 可复现环境、双源题录、PDF 与投稿构建 | `references/reproducibility-and-publishing.md`、`scripts/bootstrap_r_environment.R`、`templates/_targets.R`、`templates/manuscript.qmd` |
| Crossref/OpenAlex 双源核验 | `scripts/metadata_verify.py` |
| PyMuPDF/GROBID 两级 PDF 审计 | `scripts/pdf_ingest.py` |
| ASReview 排序边界 | `scripts/screening_rank_bridge.py` |
| RO-Crate 式哈希关系导出 | `scripts/export_ro_crate.py` |
| 检索前定标、协议草案和准备度审计 | `scripts/prepare_presearch.py`、`schemas/presearch-protocol.schema.json` |
| 本课题定标与数据审计 | `project-packs/interparental-conflict-depression-nssi/` |
| 三波 RI-CLPM、自伤、性别差异 | `references/longitudinal-panel-nssi.md` |
| 完整纵向 SEM 模型阶梯与恢复模拟 | `subskills/empirical-longitudinal-sem/` |
| APA JARS、STROBE、SAGER | `references/psychology-standards.md` |
| 检索前环境与 Chrome/Zotero | `scripts/environment_preflight.py`、`references/tool-routing.md`、`scripts/zotero_bridge.py`、`schemas/zotero-target.schema.json` |
| 自动生成运行目录 | `scripts/init_research_run.py` |
| 阶段验收 | `scripts/pipeline_gate.py` |
| SPSS/CSV 面板结构审计 | `scripts/audit_panel_data.py` |
| 原始题项重算与隐私安全分析数据 | `scripts/prepare_analysis_data.py` |
| 统一命令入口与全阶段推进 | `scripts/pipeline.py` |
| 旧十阶段运行安全迁移 | `scripts/migrate_legacy_run.py` |
| 资料元数据盘点 | `scripts/inventory_sources.py` |
| 文献规范化去重 | `scripts/evidence_dedupe.py` |
| 双人筛选、裁决、PRISMA与偏倚风险 | `scripts/screening_audit.py` |
| RI-CLPM、测量不变性与敏感性代码 | `scripts/generate_longitudinal_analysis.py` |
| 哈希校验与真实 R 执行 | `scripts/analysis_runner.py` |
| 模型输出一致性与结果产物 | `scripts/validate_analysis_results.py` |
| 已验证数字/主张渲染正文 | `scripts/render_manuscript.py` |
| DOCX/PDF、补充材料与表图投稿清单 | `scripts/export_publication_files.py` |
| 期刊政策核查与隐私安全预投稿包 | `scripts/build_submission_package.py` |
| JSON 机器契约 | `schemas/` |
| 冻结策略案例与回归评测 | `tests/frozen_cases/`、`scripts/run_frozen_evals.py`、`rubrics/promptfoo-research-policy.yaml`、`rubrics/inspect_research_policy_eval.py` |

运行时唯一产物契约由 `scripts/pipeline_schema.py` 生成。顶层 `templates/` 不得作为另一套运行目录来源。
