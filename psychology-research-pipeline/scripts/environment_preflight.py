#!/usr/bin/env python3
"""Audit the local R and Zotero environment before evidence retrieval begins."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from analysis_runner import resolve_rscript


R_PACKAGES = ["readr", "dplyr", "psych", "lavaan", "semTools", "simsem", "jsonlite"]
REPRODUCIBILITY_PACKAGES = ["renv", "targets"]
ANALYSIS_EXTENSION_PACKAGES = [
    "mice", "powRICLPM", "effectsize", "performance", "parameters", "clubSandwich",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_helper(helper: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(helper), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    )


def pack_target(run_dir: Path) -> dict:
    path = run_dir / "00_项目定标" / "课题包_project_pack" / "zotero-target.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def r_audit(rscript_value: str) -> dict:
    executable = resolve_rscript(rscript_value)
    result = {
        "ready": False, "executable": str(executable), "version": None,
        "executable_sha256": None, "packages": [], "reproducibility_packages": [],
        "analysis_extension_packages": [], "full_analysis_ready": False, "errors": [],
    }
    if not executable.is_file():
        result["errors"].append(f"Rscript executable missing: {executable}")
        return result
    version = subprocess.run(
        [str(executable), "--version"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    )
    version_text = (version.stdout or version.stderr).strip()
    if version.returncode:
        result["errors"].append(f"Rscript version check failed: {version_text}")
        return result
    expression = (
        "pkgs <- c(" + ",".join(json.dumps(name) for name in [*R_PACKAGES, *REPRODUCIBILITY_PACKAGES, *ANALYSIS_EXTENSION_PACKAGES]) + "); "
        "v <- vapply(pkgs, function(x) if (requireNamespace(x, quietly=TRUE)) "
        "as.character(utils::packageVersion(x)) else NA_character_, character(1)); "
        "cat(paste(names(v), v, sep='\\t', collapse='\\n'))"
    )
    packages = subprocess.run(
        [str(executable), "-e", expression], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=180,
    )
    versions: dict[str, str] = {}
    for line in packages.stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2:
            versions[parts[0]] = parts[1].strip()
    result.update({
        "version": version_text,
        "executable_sha256": sha256(executable),
        "packages": [
            {"name": name, "version": versions.get(name), "installed": versions.get(name) not in {None, "NA", "<NA>"}}
            for name in R_PACKAGES
        ],
        "reproducibility_packages": [
            {"name": name, "version": versions.get(name), "installed": versions.get(name) not in {None, "NA", "<NA>"}}
            for name in REPRODUCIBILITY_PACKAGES
        ],
        "analysis_extension_packages": [
            {"name": name, "version": versions.get(name), "installed": versions.get(name) not in {None, "NA", "<NA>"}}
            for name in ANALYSIS_EXTENSION_PACKAGES
        ],
    })
    if packages.returncode:
        result["errors"].append((packages.stderr or packages.stdout).strip() or "R package check failed")
    missing = [item["name"] for item in result["packages"] if not item["installed"]]
    if missing:
        result["errors"].append(f"R packages missing: {missing}")
    result["ready"] = not result["errors"]
    result["full_analysis_ready"] = result["ready"] and all(
        item["installed"] for item in [*result["reproducibility_packages"], *result["analysis_extension_packages"]]
    )
    return result


def zotero_audit(run_dir: Path, helper: Path, requested_name: str | None, requested_key: str | None) -> dict:
    target = pack_target(run_dir)
    name = requested_name or target.get("collection_name")
    key = requested_key or target.get("collection_key")
    result = {
        "ready": False, "helper": str(helper), "api_running": False,
        "connector_running": False, "target": {"collection_name": name, "collection_key": key},
        "matched_collection": None, "errors": [],
    }
    if not helper.is_file():
        result["errors"].append(f"Zotero helper missing: {helper}")
        return result
    if not name and not key:
        result["errors"].append("exact Zotero collection name/key is not configured")
        return result
    status_result = run_helper(helper, "status", "--json")
    collections_result = run_helper(helper, "collections", "--json")
    try:
        status = json.loads(status_result.stdout)
        collections = json.loads(collections_result.stdout)
    except json.JSONDecodeError:
        result["errors"].append("Zotero helper returned invalid JSON")
        return result
    result["api_running"] = bool(status.get("api_running"))
    result["connector_running"] = bool(status.get("connector_running"))
    matches = [
        item for item in collections
        if (not name or item.get("name") == name) and (not key or item.get("key") == key)
    ]
    if not result["api_running"]:
        result["errors"].append("Zotero local API is not running")
    if not result["connector_running"]:
        result["errors"].append("Zotero Connector is not running")
    if len(matches) != 1:
        result["errors"].append(f"exact Zotero collection match count is {len(matches)}, expected 1")
    else:
        result["matched_collection"] = matches[0]
    result["ready"] = not result["errors"]
    return result


def write_report(run_dir: Path, payload: dict) -> tuple[Path, Path]:
    output_dir = run_dir / "00_项目定标"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "环境预检_environment_preflight.json"
    md_path = output_dir / "环境预检_environment_preflight.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    package_lines = "\n".join(
        f"- {item['name']}: {item['version'] or 'missing'} ({'通过' if item['installed'] else '缺失'})"
        for item in payload["r"]["packages"]
    ) or "- 尚未取得包信息。"
    extension_lines = "\n".join(
        f"- {item['name']}: {item['version'] or 'missing'} ({'通过' if item['installed'] else '待安装'})"
        for item in [*payload["r"].get("reproducibility_packages", []), *payload["r"].get("analysis_extension_packages", [])]
    ) or "- 尚未取得扩展包信息。"
    errors = payload["errors"]
    md_path.write_text(
        "# 环境预检\n\n"
        f"- 总状态：**{payload['status']}**\n"
        f"- Rscript：`{payload['r']['executable']}`\n"
        f"- R 版本：{payload['r']['version'] or '未识别'}\n"
        f"- Zotero API：{payload['zotero']['api_running']}\n"
        f"- Zotero Connector：{payload['zotero']['connector_running']}\n"
        f"- 精确集合：{payload['zotero']['target']['collection_name']} (`{payload['zotero']['target']['collection_key']}`)\n\n"
        f"## 检索前核心 R 包\n\n{package_lines}\n\n"
        f"## 正式分析扩展包\n\n{extension_lines}\n\n"
        f"- 完整分析环境：{payload['r'].get('full_analysis_ready', False)}\n\n"
        "## 阻断项\n\n" + ("\n".join(f"- {item}" for item in errors) if errors else "- 无。") +
        "\n\n> 此检查只确认技术环境，不代表研究问题、伦理、检索协议或分析计划已获批准。\n",
        encoding="utf-8", newline="\n",
    )
    return json_path, md_path


def preflight(run_dir: Path, helper: Path, rscript: str, collection_name: str | None, collection_key: str | None) -> tuple[dict, int]:
    if not (run_dir / "状态记录_state.json").is_file():
        return {"status": "blocked", "errors": [f"run state missing: {run_dir}"]}, 3
    r = r_audit(rscript)
    zotero = zotero_audit(run_dir, helper, collection_name, collection_key)
    errors = [*r["errors"], *zotero["errors"]]
    payload = {
        "schema_version": 1,
        "status": "ready" if not errors else "blocked",
        "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "python": {"version": sys.version.split()[0], "executable": sys.executable},
        "r": r, "zotero": zotero, "errors": errors,
    }
    json_path, md_path = write_report(run_dir, payload)
    payload.update({"report_json": str(json_path.resolve()), "report_markdown": str(md_path.resolve())})
    return payload, 0 if not errors else 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--helper", required=True)
    parser.add_argument("--rscript", default="Rscript")
    parser.add_argument("--collection-name")
    parser.add_argument("--collection-key")
    args = parser.parse_args()
    payload, code = preflight(
        Path(args.run_dir).resolve(), Path(args.helper).resolve(), args.rscript,
        args.collection_name, args.collection_key,
    )
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
