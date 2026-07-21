#!/usr/bin/env python3
"""Bridge Zotero Desktop exports into the auditable literature workspace."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from literature_pipeline import import_evidence


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_helper(helper: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(helper), *arguments], capture_output=True,
        text=True, encoding="utf-8", timeout=60,
    )


def sync(run_dir: Path, helper: Path) -> tuple[dict, int]:
    if not helper.is_file():
        return {"status": "blocked", "gate": "zotero-helper-missing", "helper": str(helper)}, 3
    status_result = run_helper(helper, "status", "--json")
    if status_result.returncode:
        return {"status": "blocked", "gate": "zotero-status-failed", "error": status_result.stderr.strip()}, 3
    try:
        status = json.loads(status_result.stdout)
    except json.JSONDecodeError:
        return {"status": "blocked", "gate": "zotero-status-invalid-json"}, 3
    if not status.get("api_running"):
        return {"status": "blocked", "gate": "zotero-local-api-not-running", "zotero_status": status}, 3

    export_dir = run_dir / "文献" / "03_题录导出"
    export_dir.mkdir(parents=True, exist_ok=True)
    bib = export_dir / "zotero-library.bib"
    export_result = run_helper(helper, "export-bibtex", "--out", str(bib))
    if export_result.returncode or not bib.is_file():
        return {"status": "blocked", "gate": "zotero-export-failed", "error": export_result.stderr.strip()}, 3
    imported = import_evidence(run_dir, [bib], "zotero-library")
    if imported.get("status") == "blocked":
        return imported, 3

    library_dir = run_dir / "文献" / "01_已导入Zotero"
    library_dir.mkdir(parents=True, exist_ok=True)
    zotero_manifest = library_dir / "zotero_manifest.csv"
    with zotero_manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["export_file", "sha256", "records", "api_running", "connector_running", "verified_at"])
        writer.writeheader()
        writer.writerow({
            "export_file": str(bib.resolve()), "sha256": sha256(bib),
            "records": imported["imported_records"], "api_running": status.get("api_running"),
            "connector_running": status.get("connector_running"),
            "verified_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        })

    pdfs = sorted((run_dir / "文献").glob("**/*.pdf"))
    pdf_manifest = library_dir / "pdf_manifest.csv"
    with pdf_manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "sha256", "bytes", "header_valid", "status"])
        writer.writeheader()
        for path in pdfs:
            header_valid = path.read_bytes()[:5] == b"%PDF-"
            writer.writerow({
                "file": str(path.resolve()), "sha256": sha256(path), "bytes": path.stat().st_size,
                "header_valid": header_valid, "status": "verified-file" if header_valid else "invalid-pdf-header",
            })
    report_path = library_dir / "acquisition_report.md"
    invalid_pdf_count = sum(path.read_bytes()[:5] != b"%PDF-" for path in pdfs)
    report_path.write_text(
        "# Zotero 与全文获取审计\n\n"
        f"- Zotero题录：{imported['imported_records']}\n"
        f"- PDF文件：{len(pdfs)}\n"
        f"- PDF头异常：{invalid_pdf_count}\n"
        "- 权限边界：仅核验本地合法获取文件；未绕过登录、付费墙或验证码。\n",
        encoding="utf-8", newline="\n",
    )
    payload = {
        "status": "complete", "imported_records": imported["imported_records"],
        "candidate_records": imported["candidate_records"], "bibtex": str(bib.resolve()),
        "zotero_manifest": str(zotero_manifest.resolve()), "pdf_manifest": str(pdf_manifest.resolve()),
        "acquisition_report": str(report_path.resolve()), "pdf_count": len(pdfs),
        "invalid_pdf_count": invalid_pdf_count,
    }
    return payload, 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--helper", required=True)
    args = parser.parse_args()
    payload, code = sync(Path(args.run_dir).resolve(), Path(args.helper).resolve())
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
