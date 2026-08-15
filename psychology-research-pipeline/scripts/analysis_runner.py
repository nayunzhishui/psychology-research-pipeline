#!/usr/bin/env python3
"""Execute generated R analysis code and preserve a hash-verified audit trail."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
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


def package_names(manifest: dict, code_files: list[Path]) -> list[str]:
    """Discover the R packages whose installed versions must be recorded."""
    names: set[str] = set()
    for item in manifest.get("packages", []):
        name = item.get("name") if isinstance(item, dict) else item
        if isinstance(name, str) and name.strip():
            names.add(name.strip())
    quoted = re.compile(r"['\"]([^'\"]+)['\"]")
    namespaces = re.compile(r"\b([A-Za-z][A-Za-z0-9.]*)::")
    for code_file in code_files:
        text = code_file.read_text(encoding="utf-8", errors="ignore")
        for block in re.findall(r"required_packages\s*<-\s*c\((.*?)\)", text, re.DOTALL):
            names.update(quoted.findall(block))
        names.update(namespaces.findall(text))
    return sorted(names)


def declared_random_seed(manifest: dict, code_files: list[Path]) -> int | str | None:
    if manifest.get("random_seed") not in {None, ""}:
        return manifest["random_seed"]
    for code_file in code_files:
        match = re.search(r"\bset\.seed\(\s*(\d+)\s*\)", code_file.read_text(encoding="utf-8", errors="ignore"))
        if match:
            return int(match.group(1))
    return None


def installed_package_versions(rscript: Path, names: list[str], cwd: Path) -> tuple[list[dict], list[str]]:
    if not names:
        return [], ["analysis package provenance is empty"]
    expression = (
        "pkgs <- c(" + ",".join(json.dumps(name) for name in names) + "); "
        "v <- vapply(pkgs, function(x) if (requireNamespace(x, quietly=TRUE)) "
        "as.character(utils::packageVersion(x)) else NA_character_, character(1)); "
        "cat(paste(names(v), v, sep='\\t', collapse='\\n'))"
    )
    result = subprocess.run(
        command_for(rscript, ["-e", expression]), text=True, encoding="utf-8", errors="replace",
        capture_output=True, cwd=str(cwd),
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        return [], [f"R package version check failed: {detail or 'no diagnostic output'}"]
    versions: dict[str, str] = {}
    for line in result.stdout.splitlines():
        parts = line.split("\t", 1) if "\t" in line else line.split(None, 1)
        if len(parts) != 2:
            continue
        name, version = parts
        if name in names and version.strip():
            versions[name] = version.strip()
    missing = [name for name in names if versions.get(name) in {None, "NA", "<NA>"}]
    if missing:
        return [], [f"R package versions unavailable: {missing}"]
    return [{"name": name, "version": versions[name]} for name in names], []


def resolve_rscript(value: str) -> Path:
    """Resolve Rscript from an explicit path, PATH, R_HOME, or the Windows R registry."""
    expanded = Path(value).expanduser()
    if expanded.is_file():
        return expanded.resolve()
    located = shutil.which(value)
    if located:
        return Path(located).resolve()

    candidates: list[Path] = []
    r_home = os.environ.get("R_HOME")
    if r_home:
        candidates.extend([Path(r_home) / "bin" / "Rscript.exe", Path(r_home) / "bin" / "x64" / "Rscript.exe"])
    if os.name == "nt":
        try:
            import winreg

            for hive, key_name in [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\R-core\R"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\R-core\R"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\R-core\R"),
            ]:
                try:
                    with winreg.OpenKey(hive, key_name) as key:
                        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
                    root = Path(install_path)
                    candidates.extend([root / "bin" / "Rscript.exe", root / "bin" / "x64" / "Rscript.exe"])
                except OSError:
                    continue
        except ImportError:
            pass
        program_files = os.environ.get("ProgramFiles")
        if program_files:
            candidates.extend(sorted(Path(program_files).glob("R/R-*/bin/Rscript.exe"), reverse=True))

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return expanded.resolve()


def run(manifest_path: Path, rscript: Path, output_dir: Path) -> dict:
    if not manifest_path.is_file():
        return {"status": "blocked", "errors": [f"analysis code manifest missing: {manifest_path}"]}
    if not rscript.is_file():
        return {"status": "blocked", "errors": [f"Rscript executable missing: {rscript}"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    raw_code_files = manifest.get("code_files", [])
    if not raw_code_files:
        errors.append("analysis code manifest contains no code files")
    code_files = [Path(value).expanduser().resolve() for value in raw_code_files]
    for raw_code_file, code_file in zip(raw_code_files, code_files):
        if not code_file.is_file():
            errors.append(f"analysis code missing: {code_file}")
        elif manifest.get("code_hashes", {}).get(str(raw_code_file)) != sha256(code_file):
            errors.append(f"analysis code hash mismatch: {code_file}")
    input_records: list[dict] = []
    declared_inputs = []
    if manifest.get("data"):
        declared_inputs.append((manifest["data"], manifest.get("data_sha256"), "data"))
    if manifest.get("spec"):
        declared_inputs.append((manifest["spec"], manifest.get("spec_sha256"), "analysis-spec"))
    for raw_path in manifest.get("data_files", []):
        declared_inputs.append((raw_path, manifest.get("file_hashes", {}).get(raw_path), "data"))
    for raw_path, expected_hash, role in declared_inputs:
        input_path = Path(raw_path).expanduser().resolve()
        if not input_path.is_file():
            errors.append(f"analysis input missing: {input_path}")
            continue
        actual_hash = sha256(input_path)
        if not expected_hash or expected_hash != actual_hash:
            errors.append(f"analysis input hash mismatch: {input_path}")
        input_records.append({"path": str(input_path), "sha256": actual_hash, "bytes": input_path.stat().st_size, "role": role})
    expected = [Path(value).expanduser().resolve() for value in manifest.get("expected_outputs", [])]
    if not expected:
        errors.append("analysis code manifest contains no expected outputs")
    model_outputs = [path for path in expected if path.name == "model_output.json"]
    if len(model_outputs) != 1:
        errors.append("expected outputs must contain exactly one model_output.json")
    execution_manifest = output_dir / "分析执行清单_analysis_execution_manifest.json"
    if execution_manifest.exists():
        errors.append(f"analysis execution manifest already exists; use a new run directory: {execution_manifest}")
    existing_outputs = [str(path) for path in expected if path.exists()]
    if existing_outputs:
        errors.append(f"expected outputs already exist before execution: {existing_outputs}")
    existing_logs = [str(output_dir / "execution_logs" / f"{path.stem}.log") for path in code_files if (output_dir / "execution_logs" / f"{path.stem}.log").exists()]
    if existing_logs:
        errors.append(f"execution logs already exist before execution: {existing_logs}")
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

    packages, package_errors = installed_package_versions(rscript, package_names(manifest, code_files), output_dir)
    if package_errors:
        return {"status": "blocked", "errors": package_errors}

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
    missing = [str(path) for path in expected if not path.is_file() or path.stat().st_size == 0]
    if missing:
        return {"status": "blocked", "errors": [f"expected R outputs missing or empty: {missing}"], "executions": executions}
    output_records = [
        {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in expected
    ]
    model_output = model_outputs[0]
    payload = {
        "schema_version": 2, "status": "executed", "validation_status": "requires-result-validation",
        "executor": "analysis_runner.py",
        "executed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "rscript": str(rscript), "r_version": version_text,
        "software": [{"name": "R", "version": version_text, "executable": str(rscript), "executable_sha256": sha256(rscript)}],
        "packages": packages,
        "code_manifest": str(manifest_path), "code_manifest_sha256": sha256(manifest_path),
        "inputs": input_records,
        "random_seed": declared_random_seed(manifest, code_files),
        "code_files": [str(path) for path in code_files],
        "code_hashes": {str(path): sha256(path) for path in code_files},
        "executions": executions,
        "outputs": output_records,
        "model_output": str(model_output), "model_output_sha256": sha256(model_output),
    }
    execution_manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        **payload, "execution_manifest": str(execution_manifest.resolve()),
        "execution_manifest_sha256": sha256(execution_manifest),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--rscript", default="Rscript")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    rscript = resolve_rscript(args.rscript)
    result = run(Path(args.manifest).resolve(), rscript, Path(args.output_dir).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "executed" else 3


if __name__ == "__main__":
    raise SystemExit(main())
