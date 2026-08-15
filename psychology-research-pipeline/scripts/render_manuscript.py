#!/usr/bin/env python3
"""Render a manuscript only from verified result and claim placeholders."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


RESULT_PATTERN = re.compile(r"\{\{result\.([A-Za-z0-9_.-]+)(?:\|([^}]+))?\}\}")
CLAIM_PATTERN = re.compile(r"\{\{claim\.([A-Za-z0-9_.-]+)\}\}")
UNRESOLVED_PATTERN = re.compile(r"\{\{[^}]+\}\}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nested_value(payload: dict, path: str):
    value = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(path)
        value = value[part]
    return value


def format_value(value, format_spec: str | None) -> str:
    if format_spec:
        return format(value, format_spec)
    if isinstance(value, float):
        return format(value, ".10g")
    if isinstance(value, (int, str)):
        return str(value)
    raise ValueError(f"result placeholder must resolve to a scalar, got {type(value).__name__}")


def bib_keys(text: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"@[A-Za-z]+\s*\{\s*([^,]+),", text)}


def load_claims(path: Path, reference_keys: set[str]) -> tuple[dict[str, dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = set(reader.fieldnames or [])
    required = {"claim_id", "claim_text", "source_type", "source_ids", "evidence_location", "verification_status"}
    errors = [f"claims missing columns: {sorted(required - fields)}"] if required - fields else []
    claims = {}
    for row_number, row in enumerate(rows, start=2):
        claim_id = row.get("claim_id", "").strip()
        if not claim_id:
            errors.append(f"claim id missing at row {row_number}")
            continue
        if claim_id in claims:
            errors.append(f"duplicate claim id: {claim_id}")
        status = row.get("verification_status", "").strip().lower()
        if status not in {"verified", "direct", "qualified"}:
            errors.append(f"unverified claim: {claim_id}")
        if not row.get("evidence_location", "").strip():
            errors.append(f"evidence location missing: {claim_id}")
        if row.get("source_type", "").strip().lower() == "literature":
            for key in filter(None, re.split(r"[;,\s]+", row.get("source_ids", ""))):
                if key not in reference_keys:
                    errors.append(f"claim {claim_id} cites missing BibTeX key: {key}")
        claims[claim_id] = row
    return claims, errors


def render(template: Path, results_path: Path, claims_path: Path, references_path: Path, output_dir: Path) -> dict:
    template_text = template.read_text(encoding="utf-8")
    results = json.loads(results_path.read_text(encoding="utf-8"))
    references_text = references_path.read_text(encoding="utf-8")
    references = bib_keys(references_text)
    claims, errors = load_claims(claims_path, references)
    numeric_audit = []

    def replace_result(match: re.Match[str]) -> str:
        key, format_spec = match.group(1), match.group(2)
        try:
            value = nested_value(results, key)
            rendered = format_value(value, format_spec)
        except (KeyError, ValueError) as exc:
            errors.append(f"result {key}: {exc}")
            return match.group(0)
        numeric_audit.append({"result_key": key, "raw_value": value, "rendered_value": rendered})
        return rendered

    rendered = RESULT_PATTERN.sub(replace_result, template_text)

    def replace_claim(match: re.Match[str]) -> str:
        claim_id = match.group(1)
        if claim_id not in claims:
            errors.append(f"claim placeholder missing from claim map: {claim_id}")
            return match.group(0)
        return claims[claim_id]["claim_text"]

    rendered = CLAIM_PATTERN.sub(replace_claim, rendered)
    unresolved = UNRESOLVED_PATTERN.findall(rendered)
    if unresolved:
        errors.append(f"unresolved placeholders: {sorted(set(unresolved))}")
    if errors:
        return {"status": "blocked", "errors": errors}

    output_dir.mkdir(parents=True, exist_ok=True)
    manuscript_path = output_dir / "论文正文_manuscript.md"
    manuscript_path.write_text(rendered.rstrip() + "\n", encoding="utf-8", newline="\n")
    references_output = output_dir / "参考文献_references.bib"
    references_output.write_text(references_text, encoding="utf-8", newline="\n")
    numeric_path = output_dir.parent / "10_对齐审计" / "数字核查_numeric_audit.json"
    numeric_path.parent.mkdir(exist_ok=True)
    numeric_payload = {
        "schema_version": 1, "status": "verified", "results_source": str(results_path.resolve()),
        "results_sha256": sha256(results_path), "manuscript": str(manuscript_path.resolve()),
        "items": numeric_audit,
    }
    numeric_path.write_text(json.dumps(numeric_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    claim_audit_path = numeric_path.parent / "主张核查报告_claim_audit.md"
    claim_audit_path.write_text(
        "# 主张核查报告\n\n"
        f"- 已渲染并核验主张：{len(claims)}\n"
        f"- 已核验数字占位符：{len(numeric_audit)}\n"
        "- unsupported：0\n- overextended：0\n- 未解决阻断：0\n",
        encoding="utf-8", newline="\n",
    )
    manifest = {
        "schema_version": 1, "status": "ready", "manuscript": str(manuscript_path.resolve()),
        "manuscript_sha256": sha256(manuscript_path), "references": str(references_output.resolve()),
        "numeric_audit": str(numeric_path.resolve()), "claim_audit": str(claim_audit_path.resolve()),
        "result_placeholders": len(numeric_audit), "verified_claims": len(claims),
    }
    manifest_path = output_dir / "论文渲染清单_manuscript_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--claims", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = render(
        Path(args.template).resolve(), Path(args.results).resolve(), Path(args.claims).resolve(),
        Path(args.references).resolve(), Path(args.output_dir).resolve(),
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "ready" else 3


if __name__ == "__main__":
    raise SystemExit(main())
