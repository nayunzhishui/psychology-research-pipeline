#!/usr/bin/env python3
"""Canonical schema shared by the psychology research pipeline scripts."""

from __future__ import annotations

import json
from pathlib import Path


SCHEMA_VERSION = 2
PLACEHOLDER = "__REQUIRED__"
RUN_ROOT = "实证论文运行"

STAGES = [
    {"id": "00_scope", "dir": "00_项目定标", "required": [
        "项目定标简报_project_brief.md", "研究问题与假设_research_questions_hypotheses.md",
        "构念变量关系表_construct_variable_map.csv"]},
    {"id": "01_protocol", "dir": "01_标准与协议", "required": [
        "实证研究协议_empirical_protocol.md", "报告规范计划_reporting_plan.md",
        "伦理与开放科学_ethics_open_science.md"]},
    {"id": "02_search", "dir": "02_证据检索", "required": [
        "检索式记录_queries.md", "检索记录_search_log.csv", "候选文献表_candidate_records.csv"]},
    {"id": "03_library", "dir": "03_Zotero与全文获取", "required": [
        "Zotero入库清单_zotero_manifest.csv", "PDF全文清单_pdf_manifest.csv",
        "全文获取报告_acquisition_report.md"]},
    {"id": "04_synthesis", "dir": "04_文献筛选与小综述", "required": [
        "文献筛选表_literature_screening.csv", "文献阅读矩阵_literature_matrix.csv",
        "小综述_mini_review.md", "主张证据对应表_claim_evidence_map.csv"]},
    {"id": "05_methods", "dir": "05_方法设计", "required": [
        "方法设计方案_methods_plan.md", "测量工具表_measurement_table.csv",
        "统计分析计划_statistical_analysis_plan.md"]},
    {"id": "06_data", "dir": "06_数据管理", "required": [
        "数据字典_data_dictionary.csv", "数据质量审计_data_audit.md", "数据清理记录_cleaning_log.csv"]},
    {"id": "07_analysis", "dir": "07_统计分析", "required": [
        "统计分析报告_analysis_report.md", "分析偏离记录_analysis_deviation_log.csv",
        "分析清单_analysis_manifest.json", "结果表格_results_tables.md"]},
    {"id": "08_results", "dir": "08_结果与图表", "required": [
        "结果写作稿_results.md", "图表计划_figure_table_plan.md", "稳健性检查_robustness_checks.md"]},
    {"id": "09_manuscript", "dir": "09_论文正文", "required": [
        "论文正文_manuscript.md", "参考文献_references.bib", "APA参考文献_apa_references.md"]},
    {"id": "10_alignment", "dir": "10_对齐审计", "required": [
        "来源对齐表_source_alignment_table.csv", "数字核查报告_numeric_audit.md",
        "主张核查报告_claim_audit.md"]},
    {"id": "11_review", "dir": "11_模拟投稿审稿", "required": [
        "模拟审稿意见_simulated_reviews.md", "修改矩阵_revision_matrix.csv",
        "作者回复草稿_response_to_reviewers.md", "最终审计_final_audit.md"]},
]

STAGE_BY_ID = {stage["id"]: stage for stage in STAGES}
STAGE_IDS = [stage["id"] for stage in STAGES]

CSV_HEADERS = {
    "构念变量关系表_construct_variable_map.csv": ["construct_id", "构念", "变量角色", "波次", "变量名", "工具", "计分", "估计对象", "理论依据", "状态", "备注"],
    "检索记录_search_log.csv": ["search_id", "database", "platform", "query", "filters", "run_at", "result_count", "export_file", "notes"],
    "候选文献表_candidate_records.csv": ["candidate_id", "title", "authors", "year", "doi", "pmid", "source", "abstract", "landing_url", "database", "search_id", "dedup_status"],
    "Zotero入库清单_zotero_manifest.csv": ["candidate_id", "zotero_item_key", "title", "year", "doi", "collection", "attachment_key", "attachment_status", "validation_status", "source_url", "notes"],
    "PDF全文清单_pdf_manifest.csv": ["candidate_id", "file_name", "sha256", "page_count", "signature_valid", "metadata_match", "status", "notes"],
    "文献筛选表_literature_screening.csv": ["candidate_id", "stage", "decision", "reason", "reviewer_basis", "full_text_available", "decided_at"],
    "文献阅读矩阵_literature_matrix.csv": ["study_id", "candidate_id", "citation", "design", "country", "sample", "waves", "intervals", "constructs", "measures", "analysis", "main_findings", "effect_data", "limitations", "quality", "doi", "zotero_item_key", "evidence_location"],
    "主张证据对应表_claim_evidence_map.csv": ["claim_id", "claim_text", "claim_type", "study_ids", "support_level", "contradictions", "verification_status", "manuscript_destination"],
    "测量工具表_measurement_table.csv": ["construct_id", "工具中文名", "工具英文名", "版本", "波次", "题项数", "维度", "计分", "反向题", "有效范围", "缺失规则", "信度", "效度", "中文版来源", "授权状态", "跨波可比", "备注"],
    "数据字典_data_dictionary.csv": ["变量名", "变量中文名", "波次", "变量角色", "数据类型", "取值范围", "缺失值编码", "计分规则", "反向计分", "所属量表", "来源", "备注"],
    "数据清理记录_cleaning_log.csv": ["change_id", "timestamp", "source_file", "record_scope", "variable", "original", "revised", "rule", "reason", "code_location", "review_status"],
    "分析偏离记录_analysis_deviation_log.csv": ["deviation_id", "timestamp", "planned", "actual", "reason", "impact", "exploratory", "manuscript_disclosure", "decision"],
    "来源对齐表_source_alignment_table.csv": ["claim_id", "正文位置", "正文主张", "主张类型", "来源或输出", "证据位置", "支持程度", "是否过度推断", "风险等级", "处理状态", "修改建议"],
    "修改矩阵_revision_matrix.csv": ["comment_id", "severity", "source", "location", "comment", "response", "action", "artifact", "status", "evidence"],
}

MARKDOWN_SECTIONS = {
    "项目定标简报_project_brief.md": ["项目与用途", "数据和样本", "主要研究问题与估计对象", "构念变量映射", "推论边界与排除项", "风险与未决问题"],
    "研究问题与假设_research_questions_hypotheses.md": ["主要研究问题", "主要假设", "次要问题", "探索性问题", "估计对象与允许的主张", "冻结记录"],
    "实证研究协议_empirical_protocol.md": ["研究问题与结局", "样本与纳排", "变量与计分", "分析族", "偏离政策", "冻结记录"],
    "报告规范计划_reporting_plan.md": ["研究分类", "适用规范", "要求到产物映射", "目标期刊待核查项"],
    "伦理与开放科学_ethics_open_science.md": ["已知伦理事实", "未核实事项", "敏感数据保护", "数据代码材料可用性", "预注册与披露"],
    "检索式记录_queries.md": ["概念块", "中英文术语", "数据库检索式", "补充检索", "更新计划"],
    "全文获取报告_acquisition_report.md": ["范围与集合", "获取与核验统计", "失败与阻断", "临时文件和下一步"],
    "小综述_mini_review.md": ["定义与理论框架", "主题证据", "矛盾和零结果", "证据确定性", "精确研究空白"],
    "方法设计方案_methods_plan.md": ["研究设计与推论边界", "样本与流程", "测量与计分", "缺失流失与聚类", "伦理与复现", "分析摘要"],
    "统计分析计划_statistical_analysis_plan.md": ["冻结信息", "主要估计对象", "数据与变量", "主要模型与识别", "估计量与分布", "缺失异常与流失", "测量不变性", "性别与聚类", "协变量与多重检验", "诊断和稳健性", "输出与偏离"],
    "数据质量审计_data_audit.md": ["文件哈希与只读源", "ID重复与波次连接", "变量类型范围与异常编码", "计分公式和跨波可比", "缺失流失与分布", "聚类与隐私", "分析就绪结论与阻断项"],
    "统计分析报告_analysis_report.md": ["环境与输入", "样本和描述", "测量模型", "主要模型", "次要与探索性分析", "诊断与稳健性", "偏离"],
    "结果表格_results_tables.md": ["样本流", "描述统计", "测量模型", "主要模型", "组间检验", "稳健性"],
    "结果写作稿_results.md": ["参与者与流失", "描述与测量", "主要结果", "次要结果", "稳健性", "探索性结果与偏离"],
    "图表计划_figure_table_plan.md": ["正文表", "正文图", "补充材料", "隐私与可访问性"],
    "稳健性检查_robustness_checks.md": ["预设检查", "结果", "与主结论关系", "未解决风险"],
    "论文正文_manuscript.md": ["题目", "摘要", "引言", "方法", "结果", "讨论", "声明", "表图与补充材料"],
    "APA参考文献_apa_references.md": ["核验规则", "参考文献"],
    "数字核查报告_numeric_audit.md": ["样本量", "估计与区间", "p值与拟合", "表图一致性", "异常和处理"],
    "主张核查报告_claim_audit.md": ["核查范围", "unsupported", "overextended", "已处理项", "剩余阻断"],
    "模拟审稿意见_simulated_reviews.md": ["模拟性质声明", "主编初筛", "理论审稿", "方法与统计审稿", "测量审稿", "开放科学审稿", "反对性审稿", "综合决定"],
    "作者回复草稿_response_to_reviewers.md": ["模拟性质声明", "逐条回复", "未采纳意见及理由"],
    "最终审计_final_audit.md": ["目标期刊实时核查", "报告与引用", "方法与数字", "伦理隐私与复现", "未解决问题", "最终状态"],
}


def relative_artifacts(stage: dict) -> list[str]:
    return [f'{stage["dir"]}/{name}' for name in stage["required"]]


def all_artifacts() -> list[str]:
    return [path for stage in STAGES for path in relative_artifacts(stage)]


def template_text(file_name: str) -> str:
    suffix = Path(file_name).suffix.lower()
    if suffix == ".csv":
        return ",".join(CSV_HEADERS[file_name]) + "\n" + ",".join([PLACEHOLDER] * len(CSV_HEADERS[file_name])) + "\n"
    if suffix == ".json":
        return json.dumps({
            "schema_version": SCHEMA_VERSION,
            "data_files": [PLACEHOLDER],
            "file_hashes": {PLACEHOLDER: PLACEHOLDER},
            "software": [PLACEHOLDER],
            "packages": [PLACEHOLDER],
            "code_files": [PLACEHOLDER],
            "random_seed": PLACEHOLDER,
            "analysis_plan": PLACEHOLDER,
            "deviations": [PLACEHOLDER],
            "outputs": [PLACEHOLDER],
        }, ensure_ascii=False, indent=2) + "\n"
    if suffix == ".bib":
        return "% 使用经核验的 Zotero/BibTeX 记录替换占位符。\n" + PLACEHOLDER + "\n"
    sections = MARKDOWN_SECTIONS[file_name]
    title = Path(file_name).stem.split("_")[0]
    return "# " + title + "\n\n" + "\n\n".join(f"## {section}\n\n{PLACEHOLDER}" for section in sections) + "\n"
