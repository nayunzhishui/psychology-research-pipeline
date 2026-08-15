#!/usr/bin/env python3
"""Typed machine contracts for controlled research tasks and evidence provenance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, validator


DRAFT = "https://json-schema.org/draft/2020-12/schema"
STAGES = Literal[
    "00_scope", "01_protocol", "02_search", "03_library", "04_synthesis",
    "05_methods", "06_data", "07_analysis", "08_results", "09_manuscript",
    "10_alignment", "11_review",
]
ROLES = Literal[
    "evidence", "research-design", "data-measurement", "statistics",
    "result-verification", "manuscript-submission",
]


class ContractModel(BaseModel):
    class Config:
        extra = "forbid"


class ArtifactRef(ContractModel):
    path: str = Field(min_length=1)
    sha256: str = Field(regex=r"^[0-9a-f]{64}$")
    role: Literal["input", "output", "evidence", "code", "log"]
    sensitive: bool = False


class TaskEnvelope(ContractModel):
    schema_version: Literal[1] = 1
    task_id: str = Field(regex=r"^[A-Za-z0-9][A-Za-z0-9._-]{2,79}$")
    run_id: str = Field(min_length=1)
    stage: STAGES
    role: ROLES
    action: str = Field(min_length=3)
    inputs: list[ArtifactRef] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
    max_retries: int = Field(default=2, ge=0, le=5)
    reads_primary_results: bool = False

    @validator("reads_primary_results")
    def restrict_primary_results(cls, value: bool, values: dict) -> bool:
        role = values.get("role")
        if value and role not in {"result-verification", "manuscript-submission"}:
            raise ValueError("this role may not read primary results")
        return value


class DecisionRecord(ContractModel):
    decision_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    basis: str = Field(min_length=1)
    human_approved: bool = False


class RoleResult(ContractModel):
    schema_version: Literal[1] = 1
    task_id: str = Field(regex=r"^[A-Za-z0-9][A-Za-z0-9._-]{2,79}$")
    status: Literal["complete", "blocked", "failed"]
    inputs: list[ArtifactRef] = Field(default_factory=list)
    outputs: list[ArtifactRef] = Field(default_factory=list)
    decisions: list[DecisionRecord] = Field(default_factory=list)
    unresolved_items: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
    stop_reason: str = ""
    error_class: Literal[
        "not-applicable", "tool-transient", "network-transient", "format-repair",
        "missing-source", "human-decision", "ethics-unverified", "method-invalid",
        "sensitive-data-risk", "stage-gate-failed", "significance-driven",
    ] = "not-applicable"
    attempt: int = Field(default=1, ge=1, le=6)
    read_primary_results: bool = False
    analysis_classification: Literal["not-applicable", "confirmatory", "secondary", "exploratory"] = "not-applicable"

    @validator("stop_reason")
    def blocked_or_failed_needs_reason(cls, value: str, values: dict) -> str:
        if values.get("status") in {"blocked", "failed"} and not value.strip():
            raise ValueError("blocked or failed role result requires stop_reason")
        return value


class ToolCapability(ContractModel):
    schema_version: Literal[1] = 1
    tool_id: str = Field(regex=r"^[a-z0-9][a-z0-9._-]{1,79}$")
    kind: Literal["browser", "reference-manager", "statistics", "publishing", "metadata", "filesystem", "other"]
    interface: Literal["cli", "mcp", "local-api", "http-api", "desktop-ui"]
    operations: list[str] = Field(min_items=1)
    write_operations: list[str] = Field(default_factory=list)
    readiness: Literal["ready", "optional", "blocked", "unknown"] = "unknown"
    sensitive_data_allowed: bool = False


class LoopPolicy(ContractModel):
    schema_version: Literal[1] = 1
    max_retries: int = Field(default=2, ge=0, le=5)
    retryable_errors: list[Literal["tool-transient", "network-transient", "format-repair"]] = Field(default_factory=list)
    non_retryable_errors: list[Literal[
        "missing-source", "human-decision", "ethics-unverified", "method-invalid",
        "sensitive-data-risk", "stage-gate-failed",
    ]] = Field(default_factory=list)
    forbid_significance_driven_retry: Literal[True] = True
    require_stop_reason: Literal[True] = True


class EvidenceLedgerRecord(ContractModel):
    schema_version: Literal[1] = 1
    evidence_id: str = Field(regex=r"^EV-[A-Za-z0-9._-]+$")
    candidate_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    doi: str = ""
    zotero_item_key: str = ""
    study_design: str = Field(min_length=1)
    sample: str = Field(min_length=1)
    measures: list[str] = Field(min_items=1)
    waves: str = Field(min_length=1)
    effect_estimate: str = ""
    uncertainty: str = ""
    claim_ids: list[str] = Field(default_factory=list)
    evidence_location: str = Field(min_length=1)
    correction_status: Literal["none-found", "corrected", "retracted", "unverified"] = "unverified"
    verification_status: Literal["pending", "metadata-verified", "fulltext-verified", "claim-verified"] = "pending"


MODELS: dict[str, type[BaseModel]] = {
    "task-envelope.schema.json": TaskEnvelope,
    "role-result.schema.json": RoleResult,
    "tool-capability.schema.json": ToolCapability,
    "loop-policy.schema.json": LoopPolicy,
    "evidence-ledger.schema.json": EvidenceLedgerRecord,
}


def model_schema(model: type[BaseModel]) -> dict:
    if hasattr(model, "model_json_schema"):
        payload = model.model_json_schema()  # type: ignore[attr-defined]
    else:
        payload = model.schema()
    payload["$schema"] = DRAFT
    payload["additionalProperties"] = False
    return payload


def emit_schemas(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for name, model in MODELS.items():
        path = output_dir / name
        path.write_text(json.dumps(model_schema(model), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        outputs.append(str(path.resolve()))
    return {"status": "complete", "outputs": outputs}


def validate_contract(kind: str, source: Path) -> dict:
    model = MODELS[kind]
    payload = json.loads(source.read_text(encoding="utf-8"))
    if hasattr(model, "model_validate"):
        validated = model.model_validate(payload)  # type: ignore[attr-defined]
        normalized = validated.model_dump(mode="json")  # type: ignore[attr-defined]
    else:
        normalized = json.loads(model.parse_obj(payload).json())
    return {"status": "valid", "kind": kind, "normalized": normalized}


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    emit = subparsers.add_parser("emit-schemas")
    emit.add_argument("--output-dir", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--kind", choices=sorted(MODELS), required=True)
    validate.add_argument("--input", required=True)
    args = parser.parse_args()
    if args.command == "emit-schemas":
        result = emit_schemas(Path(args.output_dir).resolve())
    else:
        result = validate_contract(args.kind, Path(args.input).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
