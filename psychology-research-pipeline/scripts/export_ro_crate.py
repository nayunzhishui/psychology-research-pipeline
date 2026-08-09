#!/usr/bin/env python3
"""Export a compact RO-Crate-style provenance graph for a research run."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(run_dir: Path, artifacts: list[Path]) -> dict:
    resolved: list[Path] = []
    for artifact in artifacts:
        path = artifact.resolve()
        try:
            path.relative_to(run_dir)
        except ValueError as exc:
            raise SystemExit(f"artifact is outside run directory: {path}") from exc
        if not path.is_file():
            raise SystemExit(f"artifact missing: {path}")
        resolved.append(path)
    graph = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "about": {"@id": "./"}},
        {
            "@id": "./", "@type": "Dataset", "name": run_dir.name,
            "dateModified": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "hasPart": [{"@id": path.relative_to(run_dir).as_posix()} for path in resolved],
        },
    ]
    graph.extend({
        "@id": path.relative_to(run_dir).as_posix(), "@type": "File",
        "sha256": sha256(path), "contentSize": path.stat().st_size,
    } for path in resolved)
    payload = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": graph,
    }
    output = run_dir / "ro-crate-metadata.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "complete", "metadata": str(output.resolve()), "sha256": sha256(output), "artifacts": len(resolved)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--artifact", action="append", required=True)
    args = parser.parse_args()
    print(json.dumps(build(Path(args.run_dir).resolve(), [Path(item) for item in args.artifact]), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
