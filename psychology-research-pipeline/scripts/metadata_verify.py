#!/usr/bin/env python3
"""Compare a candidate citation with normalized Crossref and OpenAlex metadata."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path


def text_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return re.sub(r"[^\w]+", " ", value).strip()


def doi_key(value: str) -> str:
    value = (value or "").strip().casefold()
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)


def author_keys(values: list[str]) -> set[str]:
    return {text_key(value) for value in values if text_key(value)}


def verify(candidate: dict, crossref: dict, openalex: dict) -> dict:
    sources = {"candidate": candidate, "crossref": crossref, "openalex": openalex}
    normalized = {
        name: {
            "doi": doi_key(item.get("doi", "")),
            "title": text_key(item.get("title", "")),
            "year": item.get("year"),
            "authors": sorted(author_keys(item.get("authors", []))),
        }
        for name, item in sources.items()
    }
    conflicts: list[str] = []
    for field in ("doi", "title", "year"):
        values = {item[field] for item in normalized.values() if item[field] not in {None, ""}}
        if len(values) > 1:
            conflicts.append(field)
    author_sets = [set(item["authors"]) for item in normalized.values() if item["authors"]]
    if len(author_sets) > 1 and not set.intersection(*author_sets):
        conflicts.append("authors")
    status = "verified" if not conflicts and all(normalized[name]["doi"] for name in normalized) else "conflict"
    return {
        "schema_version": 1,
        "status": status,
        "eligible_for_verified_ledger": status == "verified",
        "conflict_fields": conflicts,
        "normalized": normalized,
        "sources": sources,
        "guardrail": "A conflict requires manual comparison with the publisher record; no field is silently overwritten.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--crossref", required=True, help="normalized Crossref response JSON")
    parser.add_argument("--openalex", required=True, help="normalized OpenAlex response JSON")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = verify(*[
        json.loads(Path(value).read_text(encoding="utf-8"))
        for value in (args.candidate, args.crossref, args.openalex)
    ])
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
