# 资源索引

按需读取，避免一次加载全部资源：

| 任务 | 必读资源 |
|---|---|
| 初始化、推进和 gate | `references/stage-contracts.md`、`scripts/pipeline_schema.py` |
| 本课题定标与数据审计 | `project-packs/interparental-conflict-depression-nssi/` |
| 三波 RI-CLPM、自伤、性别差异 | `references/longitudinal-panel-nssi.md` |
| APA JARS、STROBE、SAGER | `references/psychology-standards.md` |
| 文献获取与 Chrome/Zotero | `references/tool-routing.md`、`scripts/zotero_bridge.py` |
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

运行时唯一产物契约由 `scripts/pipeline_schema.py` 生成。顶层 `templates/` 不得作为另一套运行目录来源。
