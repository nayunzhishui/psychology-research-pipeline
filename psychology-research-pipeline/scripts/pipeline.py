#!/usr/bin/env python3
"""Single public command interface for the empirical psychology pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from pipeline_schema import STAGE_IDS
from audit_panel_data import item_variables, load_frame, relation_terms


SCRIPT_DIR = Path(__file__).resolve().parent
LONGITUDINAL_SEM_SCRIPTS = SCRIPT_DIR.parent / "subskills" / "empirical-longitudinal-sem" / "scripts"


def state_path(run_dir: Path) -> Path:
    return run_dir / "状态记录_state.json"


def load_state(run_dir: Path) -> dict:
    path = state_path(run_dir)
    if not path.is_file():
        raise SystemExit(f"状态记录_state.json missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def status_payload(run_dir: Path) -> dict:
    state = load_state(run_dir)
    completed = len(state.get("completed_stages", []))
    return {
        **state,
        "completion_percent": round(completed / len(STAGE_IDS) * 100, 1),
        "remaining_stages": [stage for stage in STAGE_IDS if stage not in state.get("completed_stages", [])],
    }


def run_child(script: str, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT_DIR / script), *arguments],
        text=True, encoding="utf-8", capture_output=True, env=environment,
    )


def run_longitudinal_sem_child(script: str, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(LONGITUDINAL_SEM_SCRIPTS / script), *arguments],
        text=True, encoding="utf-8", capture_output=True, env=environment,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_paths(run_dir: Path) -> tuple[Path, Path, Path]:
    output_dir = run_dir / "06_数据管理"
    return output_dir, output_dir / "数据质量审计_data_audit.json", output_dir / "数据质量审计_data_audit.md"


def execute_audit(run_dir: Path, data: str, spec: str, private_register: str | None = None) -> dict:
    output_dir, json_path, _ = audit_paths(run_dir)
    child_args = [
        "--data", data, "--spec", spec, "--output-dir", str(output_dir),
    ]
    if private_register:
        child_args.extend(["--private-register", private_register])
    result = run_child("audit_panel_data.py", child_args)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)
    return json.loads(json_path.read_text(encoding="utf-8"))


def command_init(args: argparse.Namespace) -> int:
    child_args = ["--project", args.project, "--title", args.title, "--mode", args.mode]
    if args.run_id:
        child_args.extend(["--run-id", args.run_id])
    if args.resume:
        child_args.append("--resume")
    if args.project_pack:
        child_args.extend(["--project-pack", args.project_pack])
    result = run_child("init_research_run.py", child_args)
    if result.returncode:
        sys.stderr.write(result.stderr or result.stdout)
        return result.returncode
    run_dir = Path(result.stdout.strip()).resolve()
    print(json.dumps(status_payload(run_dir), ensure_ascii=False))
    return 0


def command_migrate(args: argparse.Namespace) -> int:
    init_args = ["--project", args.project, "--title", args.title, "--mode", args.mode]
    if args.run_id:
        init_args.extend(["--run-id", args.run_id])
    initialized = run_child("init_research_run.py", init_args)
    if initialized.returncode:
        sys.stderr.write(initialized.stderr or initialized.stdout)
        return initialized.returncode
    run_dir = Path(initialized.stdout.strip()).resolve()
    result = run_child("migrate_legacy_run.py", [
        "--legacy-run", args.legacy_run, "--run-dir", str(run_dir),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_status(args: argparse.Namespace) -> int:
    print(json.dumps(status_payload(Path(args.run_dir).expanduser().resolve()), ensure_ascii=False))
    return 0


def command_inventory(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = ["--run-dir", str(run_dir)]
    for source in args.source:
        child_args.extend(["--source", source])
    result = run_child("inventory_sources.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_prepare_presearch(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("prepare_presearch.py", [
        "--run-dir", str(run_dir), "--spec", args.spec,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_preflight_environment(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = [
        "--run-dir", str(run_dir), "--helper", args.helper, "--rscript", args.rscript,
    ]
    if args.collection_name:
        child_args.extend(["--collection-name", args.collection_name])
    if args.collection_key:
        child_args.extend(["--collection-key", args.collection_key])
    result = run_child("environment_preflight.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_dispatch_task(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("research_orchestrator.py", [
        "dispatch", "--run-dir", str(run_dir), "--spec", args.spec,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_resume_task(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("research_orchestrator.py", [
        "resume", "--run-dir", str(run_dir), "--task-id", args.task_id, "--result", args.result,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_verify_task(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("research_orchestrator.py", [
        "verify", "--run-dir", str(run_dir), "--task-id", args.task_id,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_gate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("pipeline_gate.py", [
        "--run-dir", str(run_dir), "--stage", args.stage,
        "--advance" if args.advance else "--check",
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_verify_run(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    stages = []
    for stage in STAGE_IDS:
        result = run_child("pipeline_gate.py", ["--run-dir", str(run_dir), "--stage", stage, "--check"])
        stages.append({
            "stage": stage, "status": "ready" if result.returncode == 0 else "blocked",
            "details": [line[2:] for line in result.stdout.splitlines() if line.startswith("- ")],
        })
    blocked = [item["stage"] for item in stages if item["status"] == "blocked"]
    payload = {"status": "ready" if not blocked else "blocked", "blocked_stages": blocked, "stages": stages}
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if not blocked else 3


def command_autopilot(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    advanced = []
    while True:
        state = load_state(run_dir)
        stage = state.get("current_stage")
        if state.get("status") == "complete" or stage is None:
            print(json.dumps({"status": "complete", "advanced_stages": advanced, **status_payload(run_dir)}, ensure_ascii=False))
            return 0
        result = run_child("pipeline_gate.py", ["--run-dir", str(run_dir), "--stage", stage, "--advance"])
        if result.returncode:
            print(json.dumps({
                "status": "blocked", "blocked_stage": stage, "advanced_stages": advanced,
                "details": [line[2:] for line in result.stdout.splitlines() if line.startswith("- ")],
            }, ensure_ascii=False))
            return 3
        advanced.append(stage)


def command_audit_data(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    print(json.dumps(execute_audit(run_dir, args.data, args.spec, args.private_register), ensure_ascii=False))
    return 0


def command_prepare_analysis_data(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("prepare_analysis_data.py", [
        "--data", args.data, "--measurement-map", args.measurement_map,
        "--output-dir", str(run_dir / "06_数据管理"),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_freeze_data(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    data_path = Path(args.data).expanduser().resolve()
    spec_path = Path(args.spec).expanduser().resolve()
    output_dir, audit_json, _ = audit_paths(run_dir)
    report = None
    if args.decisions and audit_json.is_file():
        candidate = json.loads(audit_json.read_text(encoding="utf-8"))
        if candidate.get("sha256") == sha256(data_path) and candidate.get("spec_sha256") == sha256(spec_path):
            report = candidate
    if report is None:
        report = execute_audit(run_dir, args.data, args.spec)

    resolved_flags: list[dict] = []
    decision_log = None
    if report.get("flags") and args.decisions:
        decisions_path = Path(args.decisions).expanduser().resolve()
        decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
        errors = []
        if decisions.get("schema_version") != 1:
            errors.append("decision schema_version must be 1")
        if decisions.get("audit_sha256") != sha256(audit_json):
            errors.append("decision audit_sha256 does not match the current audit")
        by_issue = {item.get("issue_id"): item for item in decisions.get("decisions", []) if item.get("issue_id")}
        by_flag = {item.get("flag"): item for item in decisions.get("decisions", []) if item.get("flag")}
        issues = report.get("issues", [{
            "issue_id": f"legacy-{index}", "message": flag,
            "allowed_resolutions": ["source-verified", "corrected", "excluded"],
        } for index, flag in enumerate(report["flags"], 1)])
        for issue in issues:
            flag = issue["message"]
            item = by_issue.get(issue["issue_id"]) or by_flag.get(flag)
            if not item:
                errors.append(f"unresolved audit flag: {flag}")
                continue
            if item.get("status") != "resolved":
                errors.append(f"audit issue is not resolved: {issue['issue_id']}")
            if item.get("resolution") not in issue.get("allowed_resolutions", []):
                errors.append(
                    f"resolution is not allowed for {issue['issue_id']}: {item.get('resolution')}; "
                    f"allowed={issue.get('allowed_resolutions', [])}"
                )
            for field in ["rationale", "evidence", "approved_by", "decided_at"]:
                if not str(item.get(field, "")).strip():
                    errors.append(f"decision field {field} missing for audit flag: {flag}")
            resolved_flags.append(item)
        known_ids = {issue["issue_id"] for issue in issues}
        known_flags = set(report["flags"])
        unknown_ids = sorted(set(by_issue) - known_ids)
        unknown_flags = sorted(set(by_flag) - known_flags)
        if unknown_ids or unknown_flags:
            errors.append(f"decisions contain issues absent from current audit: ids={unknown_ids}, flags={unknown_flags}")
        if errors:
            print(json.dumps({"status": "blocked", "reason": "invalid or incomplete decisions", "errors": errors}, ensure_ascii=False))
            return 3
        decision_log = output_dir / "数据审计决策记录_data_decisions.md"
        lines = ["# 数据审计决策记录", "", f"- 审计：`{audit_json.name}`", f"- 审计 SHA-256：`{sha256(audit_json)}`", ""]
        for index, item in enumerate(resolved_flags, 1):
            lines.extend([
                f"## 决策 {index}", "", f"- 阻断项：{item['flag']}",
                f"- 处理：{item['resolution']}", f"- 理由：{item['rationale']}",
                f"- 证据定位：{item['evidence']}", f"- 批准者：{item['approved_by']}",
                f"- 日期：{item['decided_at']}", "",
            ])
        decision_log.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    elif report.get("flags"):
        print(json.dumps({
            "status": "blocked", "reason": "unresolved data audit flags",
            "flags": report["flags"], "issues": report.get("issues", []),
        }, ensure_ascii=False))
        return 3

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    variables = set(spec.get("id_by_wave", {}).values()) | set(spec.get("sex_by_wave", {}).values())
    variables |= {item["variable"] for item in spec.get("measures", [])}
    for item_set in spec.get("item_sets", []):
        variables.update(item_variables(item_set))
    for relation in spec.get("score_relations", []):
        variables.add(relation["target"])
        _, coefficients, products = relation_terms(relation)
        variables.update(coefficients)
        variables.update(variable for left, right, _ in products for variable in (left, right))
    frame, _ = load_frame(data_path, sorted(variables))
    frozen_path = output_dir / "冻结分析数据_frozen.csv"
    temp_path = frozen_path.with_suffix(".csv.tmp")
    frame.to_csv(temp_path, index=False, encoding="utf-8-sig")
    os.replace(temp_path, frozen_path)
    manifest = {
        "schema_version": 1, "status": "frozen", "source_data": str(data_path),
        "source_sha256": sha256(data_path), "spec": str(spec_path),
        "spec_sha256": sha256(spec_path), "audit": str(audit_json),
        "audit_sha256": sha256(audit_json), "frozen_data": str(frozen_path),
        "frozen_sha256": sha256(frozen_path), "rows": int(len(frame)),
        "columns": list(frame.columns), "flags": report.get("flags", []),
        "resolved_flags": resolved_flags,
        "decision_log": str(decision_log.resolve()) if decision_log else None,
    }
    manifest_path = output_dir / "冻结清单_freeze_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


def command_generate_analysis(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    output_dir = run_dir / "07_统计分析"
    result = run_child("generate_longitudinal_analysis.py", [
        "--data", args.data, "--spec", args.spec, "--output-dir", str(output_dir),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_plan_longitudinal_sem(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    output = run_dir / "05_方法设计" / "纵向SEM模型阶梯_longitudinal_sem_plan.json"
    result = run_longitudinal_sem_child("generate_analysis_plan.py", [
        "--spec", args.spec, "--output", str(output),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_validate_results(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("validate_analysis_results.py", [
        "--run-dir", str(run_dir), "--input", args.input,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_run_analysis(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("analysis_runner.py", [
        "--manifest", args.manifest, "--rscript", args.rscript,
        "--output-dir", str(run_dir / "07_统计分析"),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_dedupe_evidence(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("evidence_dedupe.py", [
        "--input", args.input, "--output-dir", str(run_dir / "04_文献筛选与小综述"),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_build_evidence_index(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("evidence_ledger.py", [
        "--run-dir", str(run_dir), "--ledger", args.ledger,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_verify_metadata(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    output = run_dir / "03_Zotero与全文获取" / args.output_name
    result = run_child("metadata_verify.py", [
        "--candidate", args.candidate, "--crossref", args.crossref,
        "--openalex", args.openalex, "--output", str(output),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_audit_pdf(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    output = run_dir / "03_Zotero与全文获取" / args.output_name
    child_args = ["--pdf", args.pdf, "--output", str(output)]
    if args.grobid_url:
        child_args.extend(["--grobid-url", args.grobid_url])
    result = run_child("pdf_ingest.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_rank_screening(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    output = run_dir / "04_文献筛选与小综述" / "主动学习排序_queue.json"
    result = run_child("screening_rank_bridge.py", ["--input", args.input, "--output", str(output)])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_export_ro_crate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = ["--run-dir", str(run_dir)]
    for artifact in args.artifact:
        child_args.extend(["--artifact", artifact])
    result = run_child("export_ro_crate.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_plan_search(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("literature_pipeline.py", [
        "plan-search", "--run-dir", str(run_dir), "--spec", args.spec,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_import_evidence(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = ["import-evidence", "--run-dir", str(run_dir), "--search-id", args.search_id]
    for source in args.input:
        child_args.extend(["--input", source])
    result = run_child("literature_pipeline.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_sync_zotero(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = ["--run-dir", str(run_dir), "--helper", args.helper]
    if args.collection_name:
        child_args.extend(["--collection-name", args.collection_name])
    if args.collection_key:
        child_args.extend(["--collection-key", args.collection_key])
    if args.allow_empty:
        child_args.append("--allow-empty")
    result = run_child("zotero_bridge.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_cluster_studies(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("literature_pipeline.py", [
        "cluster-studies", "--run-dir", str(run_dir), "--input", args.input,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_audit_screening(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("screening_audit.py", [
        "--input", args.input, "--output-dir", str(run_dir / "04_文献筛选与小综述"),
        "--reviewers", *args.reviewers, "--adjudicator", args.adjudicator,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_literature_action(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    child_args = [args.command, "--run-dir", str(run_dir)]
    for name in ["input", "requirements", "baseline", "current"]:
        value = getattr(args, name, None)
        if value:
            child_args.extend([f"--{name}", value])
    result = run_child("literature_pipeline.py", child_args)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_render_manuscript(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("render_manuscript.py", [
        "--template", args.template, "--results", args.results, "--claims", args.claims,
        "--references", args.references, "--output-dir", str(run_dir / "09_论文正文"),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_export_publication_files(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("export_publication_files.py", [
        "--run-dir", str(run_dir), "--manuscript", args.manuscript, "--title", args.title,
        *(["--soffice", args.soffice] if args.soffice else []),
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def command_build_submission(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    load_state(run_dir)
    result = run_child("build_submission_package.py", [
        "--run-dir", str(run_dir), "--journal-policy", args.journal_policy,
        "--manuscript", args.manuscript, "--numeric-audit", args.numeric_audit,
        "--claim-audit", args.claim_audit,
    ])
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Psychology research pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize a run")
    init.add_argument("--project", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--mode", choices=["lite", "standard", "strict", "top-journal-prep"], default="standard")
    init.add_argument("--run-id")
    init.add_argument("--resume", action="store_true")
    init.add_argument("--project-pack", help="attach a versioned project-pack directory")
    init.set_defaults(handler=command_init)

    migrate = subparsers.add_parser("migrate", help="migrate recognized artifacts from the legacy ten-stage layout")
    migrate.add_argument("--project", required=True)
    migrate.add_argument("--legacy-run", required=True)
    migrate.add_argument("--title", required=True)
    migrate.add_argument("--mode", choices=["lite", "standard", "strict", "top-journal-prep"], default="standard")
    migrate.add_argument("--run-id")
    migrate.set_defaults(handler=command_migrate)

    status = subparsers.add_parser("status", help="read run status")
    status.add_argument("--run-dir", required=True)
    status.set_defaults(handler=command_status)

    inventory = subparsers.add_parser("inventory", help="hash research sources without previewing sensitive rows")
    inventory.add_argument("--run-dir", required=True)
    inventory.add_argument("--source", action="append", required=True)
    inventory.set_defaults(handler=command_inventory)

    presearch = subparsers.add_parser("prepare-presearch", help="render scope/protocol drafts and audit readiness before searching")
    presearch.add_argument("--run-dir", required=True)
    presearch.add_argument("--spec", required=True, help="structured pre-search protocol JSON")
    presearch.set_defaults(handler=command_prepare_presearch)

    environment = subparsers.add_parser("preflight-environment", help="audit R packages and one exact Zotero collection before searching")
    environment.add_argument("--run-dir", required=True)
    environment.add_argument("--helper", required=True, help="path to the installed Zotero helper")
    environment.add_argument("--rscript", default="Rscript")
    environment.add_argument("--collection-name", help="exact collection name; may come from the attached project pack")
    environment.add_argument("--collection-key", help="exact collection key; may come from the attached project pack")
    environment.set_defaults(handler=command_preflight_environment)

    dispatch_task = subparsers.add_parser("dispatch-task", help="register a hash-bound controlled research-role task")
    dispatch_task.add_argument("--run-dir", required=True)
    dispatch_task.add_argument("--spec", required=True)
    dispatch_task.set_defaults(handler=command_dispatch_task)

    resume_task = subparsers.add_parser("resume-task", help="record one controlled task attempt and enforce bounded retries")
    resume_task.add_argument("--run-dir", required=True)
    resume_task.add_argument("--task-id", required=True)
    resume_task.add_argument("--result", required=True)
    resume_task.set_defaults(handler=command_resume_task)

    verify_task = subparsers.add_parser("verify-task", help="verify controlled task inputs and outputs against recorded hashes")
    verify_task.add_argument("--run-dir", required=True)
    verify_task.add_argument("--task-id", required=True)
    verify_task.set_defaults(handler=command_verify_task)

    gate = subparsers.add_parser("gate", help="check or advance one canonical stage")
    gate.add_argument("--run-dir", required=True)
    gate.add_argument("--stage", choices=STAGE_IDS, required=True)
    gate.add_argument("--advance", action="store_true")
    gate.set_defaults(handler=command_gate)

    verify = subparsers.add_parser("verify-run", help="check all twelve stage contracts")
    verify.add_argument("--run-dir", required=True)
    verify.set_defaults(handler=command_verify_run)

    autopilot = subparsers.add_parser("autopilot", help="advance valid stages and stop at the first evidence gate")
    autopilot.add_argument("--run-dir", required=True)
    autopilot.set_defaults(handler=command_autopilot)

    audit = subparsers.add_parser("audit-data", help="audit SPSS/CSV panel data without row-level disclosure")
    audit.add_argument("--run-dir", required=True)
    audit.add_argument("--data", required=True)
    audit.add_argument("--spec", required=True)
    audit.add_argument("--private-register", help="local ignored JSONL row-issue register")
    audit.set_defaults(handler=command_audit_data)

    prepare_data = subparsers.add_parser("prepare-analysis-data", help="derive privacy-safe rescored analysis data")
    prepare_data.add_argument("--run-dir", required=True)
    prepare_data.add_argument("--data", required=True)
    prepare_data.add_argument("--measurement-map", required=True)
    prepare_data.set_defaults(handler=command_prepare_analysis_data)

    freeze = subparsers.add_parser("freeze-data", help="freeze analysis data only after a clean audit")
    freeze.add_argument("--run-dir", required=True)
    freeze.add_argument("--data", required=True)
    freeze.add_argument("--spec", required=True)
    freeze.add_argument("--decisions", help="JSON decisions resolving every current audit flag")
    freeze.set_defaults(handler=command_freeze_data)

    analysis = subparsers.add_parser("generate-analysis", help="generate auditable R code for longitudinal analysis")
    analysis.add_argument("--run-dir", required=True)
    analysis.add_argument("--data", required=True)
    analysis.add_argument("--spec", required=True)
    analysis.set_defaults(handler=command_generate_analysis)

    sem_plan = subparsers.add_parser("plan-longitudinal-sem", help="generate the fail-closed 14-step longitudinal SEM ladder")
    sem_plan.add_argument("--run-dir", required=True)
    sem_plan.add_argument("--spec", required=True)
    sem_plan.set_defaults(handler=command_plan_longitudinal_sem)

    run_analysis = subparsers.add_parser("run-analysis", help="execute generated R code with hash and output verification")
    run_analysis.add_argument("--run-dir", required=True)
    run_analysis.add_argument("--manifest", required=True)
    run_analysis.add_argument("--rscript", default="Rscript")
    run_analysis.set_defaults(handler=command_run_analysis)

    validate_results = subparsers.add_parser("validate-results", help="validate model output and generate traceable result artifacts")
    validate_results.add_argument("--run-dir", required=True)
    validate_results.add_argument("--input", required=True)
    validate_results.set_defaults(handler=command_validate_results)

    evidence = subparsers.add_parser("dedupe-evidence", help="normalize and deduplicate candidate evidence")
    evidence.add_argument("--run-dir", required=True)
    evidence.add_argument("--input", required=True)
    evidence.set_defaults(handler=command_dedupe_evidence)

    evidence_index = subparsers.add_parser("build-evidence-index", help="build a disposable index from full-text-verified ledger records")
    evidence_index.add_argument("--run-dir", required=True)
    evidence_index.add_argument("--ledger", required=True)
    evidence_index.set_defaults(handler=command_build_evidence_index)

    metadata = subparsers.add_parser("verify-metadata", help="compare candidate metadata against normalized Crossref and OpenAlex records")
    metadata.add_argument("--run-dir", required=True)
    metadata.add_argument("--candidate", required=True)
    metadata.add_argument("--crossref", required=True)
    metadata.add_argument("--openalex", required=True)
    metadata.add_argument("--output-name", default="题录双源核验_metadata_verification.json")
    metadata.set_defaults(handler=command_verify_metadata)

    pdf_audit = subparsers.add_parser("audit-pdf", help="audit PDF integrity and optional GROBID availability")
    pdf_audit.add_argument("--run-dir", required=True)
    pdf_audit.add_argument("--pdf", required=True)
    pdf_audit.add_argument("--grobid-url")
    pdf_audit.add_argument("--output-name", default="全文解析审计_pdf_audit.json")
    pdf_audit.set_defaults(handler=command_audit_pdf)

    rank = subparsers.add_parser("rank-screening", help="import active-learning scores as a ranking-only human queue")
    rank.add_argument("--run-dir", required=True)
    rank.add_argument("--input", required=True)
    rank.set_defaults(handler=command_rank_screening)

    search_plan = subparsers.add_parser("plan-search", help="freeze modular database-specific query families")
    search_plan.add_argument("--run-dir", required=True)
    search_plan.add_argument("--spec", required=True)
    search_plan.set_defaults(handler=command_plan_search)

    evidence_import = subparsers.add_parser("import-evidence", help="normalize heterogeneous evidence exports")
    evidence_import.add_argument("--run-dir", required=True)
    evidence_import.add_argument("--input", action="append", required=True)
    evidence_import.add_argument("--search-id", required=True)
    evidence_import.set_defaults(handler=command_import_evidence)

    zotero_sync = subparsers.add_parser("sync-zotero", help="export one exact Zotero collection, import records, and audit local PDFs")
    zotero_sync.add_argument("--run-dir", required=True)
    zotero_sync.add_argument("--helper", required=True, help="path to the installed Zotero helper")
    zotero_sync.add_argument("--collection-name", help="exact collection name; may come from the attached project pack")
    zotero_sync.add_argument("--collection-key", help="exact Zotero collection key; may come from the attached project pack")
    zotero_sync.add_argument("--allow-empty", action="store_true", help="preflight an empty verified collection without importing evidence")
    zotero_sync.set_defaults(handler=command_sync_zotero)

    study_clusters = subparsers.add_parser("cluster-studies", help="flag possible multi-report study families for review")
    study_clusters.add_argument("--run-dir", required=True)
    study_clusters.add_argument("--input", required=True)
    study_clusters.set_defaults(handler=command_cluster_studies)

    screening = subparsers.add_parser("audit-screening", help="audit dual-reviewer screening, adjudication, PRISMA, and risk-of-bias setup")
    screening.add_argument("--run-dir", required=True)
    screening.add_argument("--input", required=True)
    screening.add_argument("--reviewers", nargs=2, required=True)
    screening.add_argument("--adjudicator", required=True)
    screening.set_defaults(handler=command_audit_screening)

    coverage = subparsers.add_parser("audit-evidence-coverage", help="gate synthesis on explicit evidence slots")
    coverage.add_argument("--run-dir", required=True)
    coverage.add_argument("--input", required=True)
    coverage.add_argument("--requirements", required=True)
    coverage.set_defaults(handler=command_literature_action)

    retrieval = subparsers.add_parser("build-retrieval-queue", help="prioritize authorized full-text acquisition")
    retrieval.add_argument("--run-dir", required=True)
    retrieval.add_argument("--input", required=True)
    retrieval.set_defaults(handler=command_literature_action)

    refresh = subparsers.add_parser("refresh-search", help="compare a search refresh without deleting prior evidence")
    refresh.add_argument("--run-dir", required=True)
    refresh.add_argument("--baseline", required=True)
    refresh.add_argument("--current", required=True)
    refresh.set_defaults(handler=command_literature_action)

    manuscript = subparsers.add_parser("render-manuscript", help="render only verified result and claim placeholders")
    manuscript.add_argument("--run-dir", required=True)
    manuscript.add_argument("--template", required=True)
    manuscript.add_argument("--results", required=True)
    manuscript.add_argument("--claims", required=True)
    manuscript.add_argument("--references", required=True)
    manuscript.set_defaults(handler=command_render_manuscript)

    publication = subparsers.add_parser("export-publication-files", help="build DOCX, PDF, supplement, and publication manifests")
    publication.add_argument("--run-dir", required=True)
    publication.add_argument("--manuscript", required=True)
    publication.add_argument("--title", required=True)
    publication.add_argument("--soffice")
    publication.set_defaults(handler=command_export_publication_files)

    submission = subparsers.add_parser("build-submission", help="build a privacy-safe simulated submission package")
    submission.add_argument("--run-dir", required=True)
    submission.add_argument("--journal-policy", required=True)
    submission.add_argument("--manuscript", required=True)
    submission.add_argument("--numeric-audit", required=True)
    submission.add_argument("--claim-audit", required=True)
    submission.set_defaults(handler=command_build_submission)

    crate = subparsers.add_parser("export-ro-crate", help="export a hash-linked RO-Crate-style research manifest")
    crate.add_argument("--run-dir", required=True)
    crate.add_argument("--artifact", action="append", required=True)
    crate.set_defaults(handler=command_export_ro_crate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
