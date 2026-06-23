#!/usr/bin/env python3
"""Initialize a non-destructive psychology research pipeline run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


STAGES = [
    "01_scope",
    "02_protocol",
    "03_search",
    "04_library",
    "05_screening",
    "06_synthesis",
    "07_methods",
    "08_analysis",
    "09_manuscript",
    "10_review",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:36] or "study"


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
    parser.add_argument("--title", required=True, help="Short research title")
    parser.add_argument("--run-id", help="Stable run id; generated when omitted")
    parser.add_argument("--resume", action="store_true", help="Return an existing run without overwriting it")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        parser.error(f"Project root does not exist: {project}")

    run_id = args.run_id or f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{slugify(args.title)}"
    if not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
        parser.error("run-id may contain only letters, digits, dot, underscore, and hyphen")

    run_dir = (project / "research-pipeline" / run_id).resolve()
    expected_parent = (project / "research-pipeline").resolve()
    if expected_parent not in run_dir.parents:
        parser.error("Resolved run directory escaped the project research-pipeline directory")

    if run_dir.exists():
        if args.resume and (run_dir / "state.json").is_file():
            print(run_dir)
            return 0
        parser.error(f"Run already exists; use --resume or another run-id: {run_dir}")

    run_dir.mkdir(parents=True)
    for stage in STAGES:
        (run_dir / stage).mkdir()
    (run_dir / "logs").mkdir()

    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    if not template_root.is_dir():
        raise SystemExit(f"Template directory missing: {template_root}")
    for source in sorted(template_root.rglob("*")):
        if source.is_file():
            relative = source.relative_to(template_root)
            destination = run_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    created_at = now()
    state = {
        "schema_version": 1,
        "run_id": run_id,
        "title": args.title,
        "project_root": str(project),
        "run_dir": str(run_dir),
        "created_at": created_at,
        "updated_at": created_at,
        "status": "active",
        "current_stage": STAGES[0],
        "completed_stages": [],
    }
    atomic_json(run_dir / "state.json", state)

    artifacts = []
    for path in sorted(run_dir.rglob("*")):
        if path.is_file() and path.name not in {"state.json", "manifest.json"}:
            artifacts.append({
                "path": path.relative_to(run_dir).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "status": "template" if "__REQUIRED__" in path.read_text(encoding="utf-8", errors="ignore") else "created",
            })
    atomic_json(run_dir / "manifest.json", {"schema_version": 1, "run_id": run_id, "artifacts": artifacts})

    event = {
        "timestamp": created_at,
        "run_id": run_id,
        "stage": "00_admin",
        "action": "run_initialized",
        "status": "completed",
        "tool": "init_research_run.py",
        "inputs": [str(project)],
        "outputs": [str(run_dir)],
        "decision": "start",
        "reason": "new research pipeline run",
        "error": None,
        "next_gate": STAGES[0],
    }
    (run_dir / "logs" / "events.jsonl").write_text(
        json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
