#!/usr/bin/env python3
"""Initialize a non-destructive, schema-v2 psychology research run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path

from pipeline_schema import RUN_ROOT, SCHEMA_VERSION, STAGES, all_artifacts, template_text


LITERATURE_DIRS = [
    "00_待导入Zotero", "01_已导入Zotero", "02_全文PDF",
    "03_题录导出", "04_阅读矩阵", "05_论文引用",
]


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKC", value.strip())
    value = re.sub(r"[^\w\u3400-\u9fff]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"[-_]{2,}", "-", value).strip("-_")
    return value[:48] or "study"


def safe_run_id(value: str) -> bool:
    return bool(value) and value not in {".", ".."} and not any(char in value for char in '<>:"/\\|?*')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Existing project root")
    parser.add_argument("--title", required=True, help="Research title")
    parser.add_argument("--mode", choices=["lite", "standard", "strict", "top-journal-prep"], default="standard")
    parser.add_argument("--run-id", help="Stable run id; generated when omitted")
    parser.add_argument("--resume", action="store_true", help="Return an existing run without overwriting it")
    parser.add_argument("--project-pack", help="Versioned project-pack directory with pack.json")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        parser.error(f"Project root does not exist: {project}")

    pack_root = None
    pack_manifest = None
    pack = None
    pack_sources: list[tuple[Path, str]] = []
    if args.project_pack:
        pack_root = Path(args.project_pack).expanduser().resolve()
        pack_manifest = pack_root / "pack.json"
        if not pack_manifest.is_file():
            parser.error(f"project pack manifest missing: {pack_manifest}")
        pack = json.loads(pack_manifest.read_text(encoding="utf-8"))
        required = {"schema_version", "id", "title", "profile", "data_audit_spec", "analysis_spec"}
        if pack.get("schema_version") != 1 or required - set(pack):
            parser.error(f"invalid project pack; missing fields: {sorted(required - set(pack))}")
        for source_name, output_name in [
            ("pack.json", "pack.json"), (pack["profile"], "project-profile.md"),
            *([(pack["presearch_protocol"], "presearch-protocol.json")] if pack.get("presearch_protocol") else []),
            *([(pack["zotero_target"], "zotero-target.json")] if pack.get("zotero_target") else []),
            (pack["data_audit_spec"], "data-audit-spec.json"),
            *([(pack["measurement_map"], "measurement-map.json")] if pack.get("measurement_map") else []),
            (pack["analysis_spec"], "analysis-spec.example.json"),
            *([(pack["search_plan"], "search-plan.json")] if pack.get("search_plan") else []),
            *([(pack["evidence_coverage"], "evidence-coverage.json")] if pack.get("evidence_coverage") else []),
        ]:
            source = (pack_root / source_name).resolve()
            if pack_root not in source.parents or not source.is_file():
                parser.error(f"project pack file is missing or escaped the pack: {source_name}")
            pack_sources.append((source, output_name))

    run_id = args.run_id or f"{datetime.now().astimezone():%Y%m%d_%H%M%S}_{slugify(args.title)}"
    if not safe_run_id(run_id):
        parser.error("run-id contains an unsafe path character")

    run_root = (project / RUN_ROOT).resolve()
    run_dir = (run_root / run_id).resolve()
    if run_root not in run_dir.parents:
        parser.error(f"Resolved run directory escaped {RUN_ROOT}")

    state_path = run_dir / "状态记录_state.json"
    if run_dir.exists():
        if args.resume and state_path.is_file():
            print(run_dir)
            return 0
        parser.error(f"Run already exists; use --resume or another run-id: {run_dir}")

    run_dir.mkdir(parents=True)
    for stage in STAGES:
        (run_dir / stage["dir"]).mkdir()
    (run_dir / "日志").mkdir()
    for name in LITERATURE_DIRS:
        (run_dir / "文献" / name).mkdir(parents=True, exist_ok=True)

    for relative in all_artifacts():
        path = run_dir / relative
        path.write_text(template_text(path.name), encoding="utf-8", newline="\n")

    project_pack = None
    if pack_root and pack_manifest and pack:
        pack_output = run_dir / "00_项目定标" / "课题包_project_pack"
        pack_output.mkdir()
        copied = []
        for source, output_name in pack_sources:
            destination = pack_output / output_name
            shutil.copy2(source, destination)
            copied.append({"name": output_name, "sha256": sha256(destination)})
        project_pack = {
            "id": pack["id"], "title": pack["title"], "source": str(pack_root),
            "manifest_sha256": sha256(pack_manifest), "files": copied,
        }

    created_at = now()
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "title": args.title,
        "mode": args.mode,
        "project_root": str(project),
        "run_dir": str(run_dir),
        "created_at": created_at,
        "updated_at": created_at,
        "status": "active",
        "current_stage": STAGES[0]["id"],
        "completed_stages": [],
        "blocked_stages": [],
        "project_pack": project_pack,
    }
    atomic_json(state_path, state)

    decisions = (
        "# 决策记录\n\n"
        f"- {created_at} | 初始化 | mode={args.mode} | title={args.title}\n"
        "- 未确认事项必须标为 assumption；冻结后修改必须记录原因和影响。\n"
    )
    (run_dir / "日志" / "决策记录_decisions.md").write_text(decisions, encoding="utf-8", newline="\n")

    event = {
        "timestamp": created_at, "run_id": run_id, "stage": "00_admin",
        "action": "run_initialized", "status": "completed", "tool": "init_research_run.py",
        "inputs": [str(project)], "outputs": [str(run_dir)], "decision": "start",
        "reason": f"new {args.mode} research pipeline run", "error": None,
        "next_gate": STAGES[0]["id"],
    }
    (run_dir / "日志" / "事件记录_events.jsonl").write_text(
        json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )

    artifacts = []
    for path in sorted(run_dir.rglob("*")):
        if path.is_file() and path.name not in {"状态记录_state.json", "文件清单_manifest.json"}:
            artifacts.append({
                "path": path.relative_to(run_dir).as_posix(),
                "sha256": sha256(path), "bytes": path.stat().st_size,
                "status": "template" if "__REQUIRED__" in path.read_text(encoding="utf-8", errors="ignore") else "created",
                "stage": next((stage["id"] for stage in STAGES if stage["dir"] in path.parts), "00_admin"),
            })
    atomic_json(run_dir / "文件清单_manifest.json", {
        "schema_version": SCHEMA_VERSION, "run_id": run_id, "artifacts": artifacts,
    })
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
