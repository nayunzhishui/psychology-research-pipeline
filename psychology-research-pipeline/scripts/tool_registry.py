#!/usr/bin/env python3
"""Validate the explicit research-tool capability registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from contracts import ToolCapability


def validate_item(payload: dict) -> dict:
    if hasattr(ToolCapability, "model_validate"):
        item = ToolCapability.model_validate(payload)  # type: ignore[attr-defined]
        return item.model_dump(mode="json")  # type: ignore[attr-defined]
    return json.loads(ToolCapability.parse_obj(payload).json())


def validate_registry(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise SystemExit("tool registry schema_version must be 1")
    tools = [validate_item(item) for item in payload.get("tools", [])]
    ids = [item["tool_id"] for item in tools]
    if len(ids) != len(set(ids)):
        raise SystemExit("tool registry contains duplicate tool_id values")
    return {"status": "valid", "count": len(tools), "tool_ids": sorted(ids), "tools": tools}


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--registry", required=True)
    args = parser.parse_args()
    print(json.dumps(validate_registry(Path(args.registry).resolve()), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
