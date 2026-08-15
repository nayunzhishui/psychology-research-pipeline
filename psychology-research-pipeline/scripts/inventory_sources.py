#!/usr/bin/env python3
"""Create a metadata-only, privacy-safe inventory of supplied research sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


DATA_SUFFIXES = {".sav", ".dta", ".sas7bdat", ".xlsx", ".xls", ".csv", ".parquet", ".feather"}
LITERATURE_SUFFIXES = {".pdf", ".ris", ".bib", ".enw", ".nbib"}
CODE_SUFFIXES = {".r", ".rmd", ".qmd", ".py", ".do", ".sps", ".ipynb"}
DOCUMENT_SUFFIXES = {".md", ".txt", ".docx", ".doc", ".odt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def category(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in DATA_SUFFIXES:
        return "participant-data"
    if suffix in LITERATURE_SUFFIXES:
        return "literature"
    if suffix in CODE_SUFFIXES:
        return "analysis-code"
    if suffix in DOCUMENT_SUFFIXES:
        return "research-document"
    return "other"


def inventory(run_dir: Path, sources: list[Path]) -> dict:
    files: list[Path] = []
    errors = []
    for source in sources:
        if not source.exists():
            errors.append(f"source missing: {source}")
        elif source.is_symlink():
            errors.append(f"symlink source not followed: {source}")
        elif source.is_file():
            files.append(source)
        else:
            files.extend(path for path in source.rglob("*") if path.is_file() and not path.is_symlink())
    run_resolved = run_dir.resolve()
    unique = []
    for path in sorted({path.resolve() for path in files}, key=lambda item: str(item).lower()):
        if path == run_resolved or run_resolved in path.parents:
            continue
        unique.append(path)
    if errors:
        return {"status": "blocked", "errors": errors}
    entries = [{
        "name": path.name, "path": str(path), "suffix": path.suffix.lower(),
        "bytes": path.stat().st_size, "modified_at": datetime.fromtimestamp(path.stat().st_mtime).astimezone().isoformat(timespec="seconds"),
        "sha256": sha256(path), "category": category(path),
        "content_previewed": False, "privacy": "metadata-only",
    } for path in unique]
    output_dir = run_dir / "00_项目定标"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1, "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "sources": [str(path) for path in sources], "file_count": len(entries), "files": entries,
        "privacy": "No file contents, participant IDs, or row-level values are stored in this inventory.",
    }
    json_path = output_dir / "资料盘点_source_inventory.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {name: sum(item["category"] == name for item in entries) for name in ["participant-data", "literature", "analysis-code", "research-document", "other"]}
    lines = [
        "# 资料盘点", "", "> 仅记录文件元数据和哈希；未读取或输出参与者行级内容。", "",
        f"- 文件总数：{len(entries)}", *[f"- {name}：{count}" for name, count in counts.items()], "",
        "## 文件", "", "| 文件 | 类别 | 大小(byte) | SHA-256 |", "|---|---|---:|---|",
    ]
    lines.extend(f"| {item['name']} | {item['category']} | {item['bytes']} | `{item['sha256']}` |" for item in entries)
    md_path = output_dir / "资料盘点_source_inventory.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return {
        "status": "ready", "file_count": len(entries), "categories": counts,
        "inventory_json": str(json_path.resolve()), "inventory_markdown": str(md_path.resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--source", action="append", required=True)
    args = parser.parse_args()
    result = inventory(Path(args.run_dir).resolve(), [Path(value).resolve() for value in args.source])
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "ready" else 3


if __name__ == "__main__":
    raise SystemExit(main())
