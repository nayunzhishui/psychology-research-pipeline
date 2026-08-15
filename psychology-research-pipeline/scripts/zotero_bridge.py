#!/usr/bin/env python3
"""Bridge one exact Zotero collection into the auditable literature workspace."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from literature_pipeline import import_evidence


TARGET_FILE = "zotero-target.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_helper(helper: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(helper), *arguments], capture_output=True,
        text=True, encoding="utf-8", timeout=60,
    )


def load_pack_target(run_dir: Path) -> dict:
    path = run_dir / "00_项目定标" / "课题包_project_pack" / TARGET_FILE
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_error": f"invalid project-pack Zotero target JSON: {path}"}
    payload["_source"] = str(path.resolve())
    return payload


def resolve_collection(
    helper: Path,
    requested_name: str | None,
    requested_key: str | None,
    pack_target: dict,
) -> tuple[dict | None, dict | None]:
    if pack_target.get("_error"):
        return None, {"status": "blocked", "gate": "zotero-target-invalid", "error": pack_target["_error"]}
    name = requested_name or pack_target.get("collection_name")
    key = requested_key or pack_target.get("collection_key")
    if not name and not key:
        return None, {
            "status": "blocked", "gate": "zotero-collection-required",
            "error": "Specify --collection-name/--collection-key or attach zotero-target.json in the project pack; whole-library export is forbidden.",
        }
    collections_result = run_helper(helper, "collections", "--json")
    if collections_result.returncode:
        return None, {
            "status": "blocked", "gate": "zotero-collections-failed",
            "error": collections_result.stderr.strip() or collections_result.stdout.strip(),
        }
    try:
        collections = json.loads(collections_result.stdout)
    except json.JSONDecodeError:
        return None, {"status": "blocked", "gate": "zotero-collections-invalid-json"}
    matches = [
        item for item in collections
        if (not key or item.get("key") == key) and (not name or item.get("name") == name)
    ]
    if not matches:
        return None, {
            "status": "blocked", "gate": "zotero-collection-not-found",
            "requested_name": name, "requested_key": key,
        }
    if len(matches) > 1:
        return None, {
            "status": "blocked", "gate": "zotero-collection-ambiguous",
            "requested_name": name, "requested_key": key, "matches": matches,
        }
    match = matches[0]
    if pack_target:
        if pack_target.get("collection_name") and match.get("name") != pack_target["collection_name"]:
            return None, {"status": "blocked", "gate": "zotero-target-name-mismatch"}
        if pack_target.get("collection_key") and match.get("key") != pack_target["collection_key"]:
            return None, {"status": "blocked", "gate": "zotero-target-key-mismatch"}
    return match, None


def fetch_collection_bibtex(base_url: str, collection_key: str) -> tuple[str, int]:
    chunks: list[str] = []
    start = 0
    total = 0
    while True:
        query = urlencode({"format": "bibtex", "limit": 100, "start": start})
        url = f"{base_url.rstrip('/')}/api/users/0/collections/{collection_key}/items?{query}"
        request = Request(url, headers={"Zotero-API-Version": "3"})
        with urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace").strip()
            header_total = response.headers.get("Total-Results")
            if header_total is not None:
                total = int(header_total)
            if body:
                chunks.append(body)
        if total == 0 or start + 100 >= total or header_total is None:
            break
        start += 100
    return "\n\n".join(chunks) + ("\n" if chunks else ""), total


def audit_local_pdfs(run_dir: Path, output_dir: Path) -> tuple[Path, int, int]:
    pdfs = sorted((run_dir / "文献").glob("**/*.pdf"))
    manifest = output_dir / "pdf_manifest.csv"
    invalid = 0
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "sha256", "bytes", "header_valid", "status"])
        writer.writeheader()
        for path in pdfs:
            header_valid = path.read_bytes()[:5] == b"%PDF-"
            invalid += int(not header_valid)
            writer.writerow({
                "file": str(path.resolve()), "sha256": sha256(path), "bytes": path.stat().st_size,
                "header_valid": header_valid, "status": "verified-file" if header_valid else "invalid-pdf-header",
            })
    return manifest, len(pdfs), invalid


def sync(
    run_dir: Path,
    helper: Path,
    collection_name: str | None = None,
    collection_key: str | None = None,
    allow_empty: bool = False,
) -> tuple[dict, int]:
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

    pack_target = load_pack_target(run_dir)
    collection, collection_error = resolve_collection(
        helper, collection_name, collection_key, pack_target,
    )
    if collection_error:
        return collection_error, 3
    assert collection is not None

    try:
        bibtex, item_count = fetch_collection_bibtex(
            status.get("base_url", "http://127.0.0.1:23119"), collection["key"],
        )
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        return {
            "status": "blocked", "gate": "zotero-collection-export-failed",
            "collection": collection, "error": str(exc),
        }, 3

    export_dir = run_dir / "文献" / "03_题录导出"
    export_dir.mkdir(parents=True, exist_ok=True)
    bib = export_dir / f"zotero-collection-{collection['key']}.bib"
    bib.write_text(bibtex, encoding="utf-8", newline="\n")

    library_dir = run_dir / "文献" / "01_已导入Zotero"
    library_dir.mkdir(parents=True, exist_ok=True)
    zotero_manifest = library_dir / "zotero_manifest.csv"
    verified_at = datetime.now().astimezone().isoformat(timespec="seconds")
    with zotero_manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "collection_name", "collection_key", "export_file", "sha256", "records",
            "api_running", "connector_running", "verified_at", "target_source",
        ])
        writer.writeheader()
        writer.writerow({
            "collection_name": collection["name"], "collection_key": collection["key"],
            "export_file": str(bib.resolve()), "sha256": sha256(bib), "records": item_count,
            "api_running": status.get("api_running"), "connector_running": status.get("connector_running"),
            "verified_at": verified_at, "target_source": pack_target.get("_source", "command-line"),
        })

    pdf_manifest, pdf_count, invalid_pdf_count = audit_local_pdfs(run_dir, library_dir)
    report_path = library_dir / "acquisition_report.md"
    report_path.write_text(
        "# Zotero 与全文获取审计\n\n"
        f"- 精确集合：{collection['name']} (`{collection['key']}`)\n"
        f"- 集合题录：{item_count}\n- PDF文件：{pdf_count}\n- PDF头异常：{invalid_pdf_count}\n"
        "- 全库导出：禁止。\n"
        "- 权限边界：仅核验本地合法获取文件；未绕过登录、付费墙或验证码。\n",
        encoding="utf-8", newline="\n",
    )

    common = {
        "collection": collection, "bibtex": str(bib.resolve()),
        "zotero_manifest": str(zotero_manifest.resolve()), "pdf_manifest": str(pdf_manifest.resolve()),
        "acquisition_report": str(report_path.resolve()), "pdf_count": pdf_count,
        "invalid_pdf_count": invalid_pdf_count,
    }
    if item_count == 0:
        payload = {
            "status": "ready-empty" if allow_empty else "blocked",
            "gate": "zotero-collection-empty", "imported_records": 0,
            "candidate_records": None, **common,
        }
        return payload, 0 if allow_empty else 3

    imported = import_evidence(run_dir, [bib], f"zotero-collection-{collection['key']}")
    if imported.get("status") == "blocked":
        return imported, 3
    return {
        "status": "complete", "imported_records": imported["imported_records"],
        "candidate_records": imported["candidate_records"], **common,
    }, 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--helper", required=True)
    parser.add_argument("--collection-name")
    parser.add_argument("--collection-key")
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args()
    payload, code = sync(
        Path(args.run_dir).resolve(), Path(args.helper).resolve(),
        args.collection_name, args.collection_key, args.allow_empty,
    )
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
