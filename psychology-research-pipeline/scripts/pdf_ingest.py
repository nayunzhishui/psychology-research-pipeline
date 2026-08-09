#!/usr/bin/env python3
"""Two-level PDF preflight: PyMuPDF integrity first, optional GROBID structure second."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


def audit_pdf(path: Path, grobid_url: str | None = None) -> dict:
    result = {
        "schema_version": 1, "path": str(path.resolve()), "sha256": None,
        "valid_pdf": False, "pages": None, "text_characters": None,
        "fast_parser": None, "grobid_status": "not-requested", "eligible_for_fulltext_verification": False,
        "errors": [],
    }
    if not path.is_file():
        result["errors"].append("PDF missing")
        return result
    result["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not path.read_bytes()[:5] == b"%PDF-":
        result["errors"].append("invalid PDF header")
        return result
    try:
        import fitz  # type: ignore
        with fitz.open(path) as document:
            result.update({
                "valid_pdf": True, "pages": document.page_count,
                "text_characters": sum(len(page.get_text("text")) for page in document),
                "fast_parser": "PyMuPDF",
            })
    except ImportError:
        result.update({"valid_pdf": True, "fast_parser": "header-only"})
        result["errors"].append("PyMuPDF unavailable; page/text audit not completed")
    except Exception as exc:
        result["errors"].append(f"PyMuPDF parse failed: {exc}")
        return result
    if grobid_url:
        request = urllib.request.Request(grobid_url.rstrip("/") + "/api/isalive")
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                result["grobid_status"] = "ready" if response.status == 200 else f"http-{response.status}"
        except Exception as exc:
            result["grobid_status"] = "unavailable"
            result["errors"].append(f"GROBID unavailable: {exc}")
    result["eligible_for_fulltext_verification"] = bool(
        result["valid_pdf"] and result["pages"] and result["text_characters"] and result["text_characters"] > 100
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--grobid-url")
    args = parser.parse_args()
    payload = audit_pdf(Path(args.pdf).resolve(), args.grobid_url)
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["valid_pdf"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
