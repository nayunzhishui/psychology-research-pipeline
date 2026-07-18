#!/usr/bin/env python3
"""Safely migrate recognized text artifacts from the legacy ten-stage layout."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


MAPPING = {
    "01_scope/project_brief.md": "00_项目定标/项目定标简报_project_brief.md",
    "01_scope/research_question.md": "00_项目定标/研究问题与假设_research_questions_hypotheses.md",
    "02_protocol/protocol.md": "01_标准与协议/实证研究协议_empirical_protocol.md",
    "02_protocol/reporting_plan.md": "01_标准与协议/报告规范计划_reporting_plan.md",
    "03_search/search_log.csv": "02_证据检索/检索记录_search_log.csv",
    "03_search/candidates.csv": "02_证据检索/候选文献表_candidate_records.csv",
    "04_library/zotero_manifest.csv": "03_Zotero与全文获取/Zotero入库清单_zotero_manifest.csv",
    "04_library/acquisition_report.md": "03_Zotero与全文获取/全文获取报告_acquisition_report.md",
    "05_screening/screening_log.csv": "04_文献筛选与小综述/文献筛选表_literature_screening.csv",
    "05_screening/evidence_matrix.csv": "04_文献筛选与小综述/文献阅读矩阵_literature_matrix.csv",
    "06_synthesis/mini_review.md": "04_文献筛选与小综述/小综述_mini_review.md",
    "06_synthesis/claim_evidence_map.csv": "04_文献筛选与小综述/主张证据对应表_claim_evidence_map.csv",
    "07_methods/methods_plan.md": "05_方法设计/方法设计方案_methods_plan.md",
    "07_methods/analysis_plan.md": "05_方法设计/统计分析计划_statistical_analysis_plan.md",
    "08_analysis/data_audit.md": "06_数据管理/数据质量审计_data_audit.md",
    "08_analysis/analysis_manifest.json": "07_统计分析/分析清单_analysis_manifest.json",
    "08_analysis/results.md": "08_结果与图表/结果写作稿_results.md",
    "09_manuscript/manuscript.md": "09_论文正文/论文正文_manuscript.md",
    "09_manuscript/references.bib": "09_论文正文/参考文献_references.bib",
    "09_manuscript/citation_audit.md": "10_对齐审计/主张核查报告_claim_audit.md",
    "10_review/reviewer_report.md": "11_模拟投稿审稿/模拟审稿意见_simulated_reviews.md",
    "10_review/revision_matrix.csv": "11_模拟投稿审稿/修改矩阵_revision_matrix.csv",
    "10_review/final_audit.md": "11_模拟投稿审稿/最终审计_final_audit.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def migrate(legacy: Path, run_dir: Path) -> dict:
    migrated = []
    for old_relative, new_relative in MAPPING.items():
        source = legacy / old_relative
        if not source.is_file():
            continue
        destination = run_dir / new_relative
        current = destination.read_text(encoding="utf-8", errors="ignore") if destination.exists() else ""
        if current.strip() and "__REQUIRED__" not in current:
            raise SystemExit(f"refusing to overwrite completed artifact: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        migrated.append({
            "source": old_relative, "destination": new_relative,
            "sha256": sha256(source), "bytes": source.stat().st_size,
        })
    recognized = {str((legacy / relative).resolve()) for relative in MAPPING}
    unmapped = []
    for path in sorted((item for item in legacy.rglob("*") if item.is_file()), key=lambda item: str(item).lower()):
        if str(path.resolve()) not in recognized:
            unmapped.append({"path": path.relative_to(legacy).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size})
    report = {
        "schema_version": 1, "status": "migrated-requires-gates", "legacy_run": str(legacy.resolve()),
        "run_dir": str(run_dir.resolve()), "migrated": migrated, "unmapped_metadata_only": unmapped,
        "warning": "Migration preserves recognized artifacts but does not certify their schemas or content; all twelve gates remain mandatory.",
    }
    report_path = run_dir / "日志" / "旧版迁移报告_legacy_migration.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**report, "report": str(report_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-run", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    legacy = Path(args.legacy_run).resolve()
    run_dir = Path(args.run_dir).resolve()
    if not legacy.is_dir() or not (run_dir / "状态记录_state.json").is_file():
        parser.error("legacy-run and initialized run-dir must exist")
    print(json.dumps(migrate(legacy, run_dir), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
