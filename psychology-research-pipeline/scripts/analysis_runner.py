#!/usr/bin/env python3
"""Execute generated R analysis code and preserve a hash-verified audit trail."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def command_for(executable: Path, arguments: list[str]) -> list[str]:
    if executable.suffix.lower() in {".cmd", ".bat"}:
        return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", str(executable), *arguments]
    return [str(executable), *arguments]


def run(manifest_path: Path, rscript: Path, output_dir: Path) -> dict:
    if not manifest_path.is_file():
        return {"status": "blocked", "errors": [f"analysis code manifest missing: {manifest_path}"]}
    if not rscript.is_file():
        return {"status": "blocked", "errors": [f"Rscript executable missing: {rscript}"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    code_files = [Path(value).resolve() for value in manifest.get("code_files", [])]
    for code_file in code_files:
        if not code_file.is_file():
            errors.append(f"analysis code missing: {code_file}")
        elif manifest.get("code_hashes", {}).get(str(code_file)) != sha256(code_file):
            errors.append(f"analysis code hash mismatch: {code_file}")
    if errors:
        return {"status": "blocked", "errors": errors}

    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir = output_dir / "execution_logs"
    log_dir.mkdir(exist_ok=True)
    version = subprocess.run(
        command_for(rscript, ["--version"]), text=True, encoding="utf-8", errors="replace",
        capture_output=True, cwd=str(output_dir),
    )
    version_text = (version.stdout or version.stderr).strip()
    if version.returncode:
        return {"status": "blocked", "errors": [f"Rscript version check failed: {version_text}"]}

    executions = []
    for code_file in code_files:
        result = subprocess.run(
            command_for(rscript, [str(code_file)]), text=True, encoding="utf-8", errors="replace",
            capture_output=True, cwd=str(code_file.parent),
        )
        log_path = log_dir / f"{code_file.stem}.log"
        log_path.write_text(
            f"exit_code={result.returncode}\n\n[stdout]\n{result.stdout}\n[stderr]\n{result.stderr}",
            encoding="utf-8", newline="\n",
        )
        executions.append({
            "code_file": str(code_file), "code_sha256": sha256(code_file),
            "exit_code": result.returncode, "log": str(log_path.resolve()), "log_sha256": sha256(log_path),
        })
        if result.returncode:
            return {
                "status": "blocked", "errors": [f"R analysis failed: {code_file.name}"],
                "executions": executions,
            }
    expected = [Path(value).resolve() for value in manifest.get("expected_outputs", [])]
    missing = [str(path) for path in expected if not path.is_file() or path.stat().st_size == 0]
    if missing:
        return {"status": "blocked", "errors": [f"expected R outputs missing or empty: {missing}"], "executions": executions}
    payload = {
        "schema_version": 1, "status": "executed", "validation_status": "requires-result-validation",
        "executed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "rscript": str(rscript), "r_version": version_text,
        "code_manifest": str(manifest_path), "code_manifest_sha256": sha256(manifest_path),
        "executions": executions,
        "outputs": [{"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size} for path in expected],
    }
    execution_manifest = output_dir / "分析执行清单_analysis_execution_manifest.json"
    execution_manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    model_output = next((path for path in expected if path.name == "model_output.json"), None)
    return {
        **payload, "execution_manifest": str(execution_manifest.resolve()),
        "model_output": str(model_output) if model_output else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--rscript", default="Rscript")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rscript = Path(args.rscript).expanduser()
    if not rscript.is_absolute():
        import shutil
        located = shutil.which(args.rscript)
        rscript = Path(located) if located else rscript.resolve()
    result = run(Path(args.manifest).resolve(), rscript.resolve(), Path(args.output_dir).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "executed" else 3


if __name__ == "__main__":
    raise SystemExit(main())
