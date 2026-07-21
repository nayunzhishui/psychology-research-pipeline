#!/usr/bin/env python3
"""Deterministic literature discovery, normalization, linkage, and coverage module."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree


EVIDENCE_FIELDS = [
    "candidate_id", "title", "authors", "year", "doi", "pmid", "openalex_id",
    "source_record_id", "source", "abstract", "landing_url", "database", "search_id",
    "publication_type", "evidence_role", "constructs", "design", "cohort_name", "sample_country",
    "sample_size", "recruitment_years", "correction_status", "retraction_status",
    "open_access_status", "fulltext_status", "metadata_verified_at", "metadata_source",
    "raw_export_file", "raw_export_sha256", "dedup_status",
]


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_doi(value: str) -> str:
    value = str(value or "").strip().casefold()
    value = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value)
    return value.rstrip(". ")


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return " ".join(value.split())


def first(value, default=""):
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default


def year_from(value) -> str:
    if isinstance(value, dict):
        parts = value.get("date-parts", [[]])
        return str(first(first(parts, []), ""))
    match = re.search(r"(?:19|20)\d{2}", str(value or ""))
    return match.group(0) if match else ""


def parse_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_ris(path: Path) -> list[dict]:
    records, record = [], {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^([A-Z0-9]{2})\s{0,2}-\s?(.*)$", raw_line)
        if not match:
            continue
        tag, value = match.groups()
        if tag == "ER":
            if record:
                records.append(record)
            record = {}
            continue
        record.setdefault(tag, []).append(value.strip())
    if record:
        records.append(record)
    return [{
        "title": first(item.get("TI") or item.get("T1")),
        "authors": "; ".join(item.get("AU", [])),
        "year": year_from(first(item.get("PY") or item.get("Y1"))),
        "doi": first(item.get("DO")), "abstract": " ".join(item.get("AB", [])),
        "landing_url": first(item.get("UR")), "source_record_id": first(item.get("ID")),
        "publication_type": first(item.get("TY")),
    } for item in records]


def split_bibtex_entries(text: str) -> list[tuple[str, str, str]]:
    entries = []
    cursor = 0
    while True:
        match = re.search(r"@(\w+)\s*\{\s*([^,]+),", text[cursor:], flags=re.I)
        if not match:
            break
        start = cursor + match.end()
        depth, index = 1, start
        while index < len(text) and depth:
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
            index += 1
        entries.append((match.group(1), match.group(2).strip(), text[start:index - 1]))
        cursor = index
    return entries


def parse_bibtex(path: Path) -> list[dict]:
    records = []
    for entry_type, key, body in split_bibtex_entries(path.read_text(encoding="utf-8-sig")):
        fields = {}
        pattern = re.compile(r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|([^,]+))\s*,?", re.S)
        for match in pattern.finditer(body):
            fields[match.group(1).casefold()] = next(value for value in match.groups()[1:] if value is not None).strip()
        records.append({
            "title": fields.get("title", ""), "authors": fields.get("author", "").replace(" and ", "; "),
            "year": year_from(fields.get("year")), "doi": fields.get("doi", ""),
            "abstract": fields.get("abstract", ""), "landing_url": fields.get("url", ""),
            "source_record_id": key, "publication_type": entry_type,
        })
    return records


def xml_text(node, path: str) -> str:
    found = node.find(path)
    return "" if found is None else "".join(found.itertext()).strip()


def parse_pubmed(path: Path) -> list[dict]:
    root = ElementTree.parse(path).getroot()
    records = []
    for article in root.findall(".//PubmedArticle"):
        authors = []
        for author in article.findall(".//Article/AuthorList/Author"):
            name = " ".join(filter(None, [xml_text(author, "ForeName"), xml_text(author, "LastName")]))
            if name:
                authors.append(name)
        ids = {item.attrib.get("IdType", "").casefold(): (item.text or "").strip()
               for item in article.findall(".//PubmedData/ArticleIdList/ArticleId")}
        abstract = " ".join("".join(item.itertext()).strip() for item in article.findall(".//Article/Abstract/AbstractText"))
        records.append({
            "title": xml_text(article, ".//Article/ArticleTitle"), "authors": "; ".join(authors),
            "year": year_from(xml_text(article, ".//JournalIssue/PubDate/Year") or xml_text(article, ".//JournalIssue/PubDate/MedlineDate")),
            "doi": ids.get("doi", ""), "pmid": xml_text(article, ".//MedlineCitation/PMID"),
            "source_record_id": xml_text(article, ".//MedlineCitation/PMID"), "abstract": abstract,
            "landing_url": f"https://pubmed.ncbi.nlm.nih.gov/{xml_text(article, './/MedlineCitation/PMID')}/",
            "publication_type": "; ".join(item.text or "" for item in article.findall(".//PublicationTypeList/PublicationType")),
        })
    return records


def abstract_from_inverted_index(index: dict) -> str:
    positioned = [(position, word) for word, positions in (index or {}).items() for position in positions]
    return " ".join(word for _, word in sorted(positioned))


def parse_json(path: Path) -> tuple[str, list[dict]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict) and isinstance(payload.get("message"), dict) and "items" in payload["message"]:
        records = []
        for item in payload["message"]["items"]:
            authors = [" ".join(filter(None, [author.get("given"), author.get("family")])) for author in item.get("author", [])]
            records.append({
                "title": first(item.get("title")), "authors": "; ".join(authors),
                "year": year_from(item.get("published") or item.get("issued")), "doi": item.get("DOI", ""),
                "source_record_id": item.get("DOI", ""), "abstract": item.get("abstract", ""),
                "landing_url": item.get("URL", ""), "publication_type": item.get("type", ""),
            })
        return "Crossref", records
    if isinstance(payload, dict) and "results" in payload:
        records = []
        for item in payload["results"]:
            records.append({
                "title": item.get("title") or item.get("display_name", ""),
                "authors": "; ".join(authorship.get("author", {}).get("display_name", "") for authorship in item.get("authorships", [])),
                "year": str(item.get("publication_year", "")), "doi": item.get("doi", ""),
                "openalex_id": item.get("id", "").rsplit("/", 1)[-1], "source_record_id": item.get("id", ""),
                "abstract": abstract_from_inverted_index(item.get("abstract_inverted_index", {})),
                "landing_url": (item.get("primary_location") or {}).get("landing_page_url", ""),
                "publication_type": item.get("type", ""),
            })
        return "OpenAlex", records
    records = payload if isinstance(payload, list) else payload.get("records", [])
    return "JSON", [dict(item) for item in records]


def parse_export(path: Path) -> tuple[str, list[dict]]:
    suffix = path.suffix.casefold()
    if suffix == ".csv":
        return "CSV", parse_csv(path)
    if suffix == ".ris":
        return "RIS", parse_ris(path)
    if suffix in {".bib", ".bibtex"}:
        return "BibTeX", parse_bibtex(path)
    if suffix == ".xml":
        return "PubMed", parse_pubmed(path)
    if suffix == ".json":
        return parse_json(path)
    raise ValueError(f"unsupported evidence export format: {path.name}")


def canonical_record(raw: dict, *, source_path: Path, source: str, search_id: str, record_index: int) -> dict:
    doi = normalize_doi(raw.get("doi") or raw.get("DOI", ""))
    pmid = str(raw.get("pmid") or raw.get("PMID", "")).strip()
    openalex_id = str(raw.get("openalex_id", "")).strip().rsplit("/", 1)[-1]
    title = normalize_text(raw.get("title") or raw.get("Title", ""))
    authors = str(raw.get("authors") or raw.get("author", "")).strip()
    year = year_from(raw.get("year", ""))
    identity = f"doi:{doi}" if doi else f"pmid:{pmid}" if pmid else f"openalex:{openalex_id}" if openalex_id else f"meta:{title}|{normalize_text(authors)}|{year}"
    defaults = {field: "" for field in EVIDENCE_FIELDS}
    record_identity = f"{sha256_file(source_path)}|{record_index}|{identity}|{raw.get('source_record_id', '')}"
    defaults.update({
        "candidate_id": "cand-" + sha256_bytes(record_identity.encode("utf-8"))[:16],
        "title": str(raw.get("title") or raw.get("Title", "")).strip(), "authors": authors,
        "year": year, "doi": doi, "pmid": pmid, "openalex_id": openalex_id,
        "source_record_id": str(raw.get("source_record_id", "")).strip(), "source": source,
        "abstract": str(raw.get("abstract", "")).strip(), "landing_url": str(raw.get("landing_url") or raw.get("url", "")).strip(),
        "database": source, "search_id": search_id, "publication_type": str(raw.get("publication_type", "")).strip(),
        "correction_status": "unknown", "retraction_status": "unknown", "open_access_status": "unknown",
        "fulltext_status": "metadata-only", "metadata_verified_at": now(), "metadata_source": source,
        "raw_export_file": str(source_path.resolve()), "raw_export_sha256": sha256_file(source_path), "dedup_status": "unreviewed",
    })
    return defaults


def import_evidence(run_dir: Path, inputs: list[Path], search_id: str) -> dict:
    errors, records, sources = [], [], []
    for path in inputs:
        if not path.is_file():
            errors.append(f"evidence export missing: {path}")
            continue
        try:
            source, raw_records = parse_export(path)
        except (ValueError, json.JSONDecodeError, ElementTree.ParseError) as error:
            errors.append(str(error))
            continue
        sources.append({"path": str(path.resolve()), "format": source, "sha256": sha256_file(path), "records": len(raw_records)})
        records.extend(
            canonical_record(item, source_path=path, source=source, search_id=search_id, record_index=index)
            for index, item in enumerate(raw_records, 1)
        )
    if errors:
        return {"status": "blocked", "errors": errors}
    output_dir = run_dir / "02_证据检索"
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = output_dir / "候选文献表_candidate_records.csv"
    with candidate_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EVIDENCE_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    manifest = {
        "schema_version": 1, "status": "complete", "search_id": search_id, "created_at": now(),
        "source_exports": sources, "imported_records": len(records),
        "candidate_records": str(candidate_path.resolve()), "candidate_records_sha256": sha256_file(candidate_path),
    }
    manifest_path = output_dir / "题录导入清单_evidence_import_manifest.json"
    write_json(manifest_path, manifest)
    return {**manifest, "manifest": str(manifest_path.resolve())}


def first_author(value: str) -> str:
    return normalize_text(re.split(r"[;,]", value or "", maxsplit=1)[0])


def cluster_studies(run_dir: Path, source: Path) -> dict:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    pairs = []
    for left_index, left in enumerate(rows):
        for right in rows[left_index + 1:]:
            reasons = []
            for field in ["cohort_name", "sample_country", "sample_size", "recruitment_years"]:
                left_value, right_value = normalize_text(left.get(field, "")), normalize_text(right.get(field, ""))
                if left_value and left_value == right_value:
                    reasons.append(field)
            if first_author(left.get("authors", "")) and first_author(left.get("authors", "")) == first_author(right.get("authors", "")):
                reasons.append("first_author")
            strong = "cohort_name" in reasons and len(reasons) >= 2
            fallback = all(field in reasons for field in ["sample_country", "sample_size", "recruitment_years"]) and "first_author" in reasons
            if not (strong or fallback):
                continue
            identities = sorted([left.get("candidate_id", ""), right.get("candidate_id", "")])
            pairs.append({
                "family_candidate_id": "family-" + sha256_bytes("|".join(identities).encode("utf-8"))[:12],
                "left_candidate_id": identities[0], "right_candidate_id": identities[1],
                "match_reasons": ";".join(reasons), "review_status": "pending",
                "review_decision": "", "reviewer": "", "reviewed_at": "",
            })
    output_dir = run_dir / "04_文献筛选与小综述"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "同研究多报告候选_study_family_candidates.csv"
    fields = [
        "family_candidate_id", "left_candidate_id", "right_candidate_id", "match_reasons",
        "review_status", "review_decision", "reviewer", "reviewed_at",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(pairs)
    manifest = {
        "schema_version": 1, "status": "complete", "source": str(source.resolve()),
        "source_sha256": sha256_file(source), "candidate_pairs": len(pairs),
        "study_family_candidates": str(output_path.resolve()),
    }
    manifest_path = output_dir / "研究家族识别清单_study_family_manifest.json"
    write_json(manifest_path, manifest)
    return {**manifest, "manifest": str(manifest_path.resolve())}


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def token_set(value: str) -> set[str]:
    return {normalize_text(item) for item in re.split(r"[;,|]", value or "") if normalize_text(item)}


def matches_requirement(row: dict, criteria: dict) -> bool:
    if normalize_text(row.get("retraction_status", "")) in {"retracted", "withdrawn"}:
        return False
    roles = {normalize_text(item) for item in criteria.get("evidence_role", [])}
    if roles and normalize_text(row.get("evidence_role", "")) not in roles:
        return False
    allowed_retraction = {normalize_text(item) for item in criteria.get("retraction_status", [])}
    if allowed_retraction and normalize_text(row.get("retraction_status", "")) not in allowed_retraction:
        return False
    allowed_fulltext = {normalize_text(item) for item in criteria.get("fulltext_status", [])}
    if allowed_fulltext and normalize_text(row.get("fulltext_status", "")) not in allowed_fulltext:
        return False
    constructs = token_set(row.get("constructs", ""))
    if not {normalize_text(item) for item in criteria.get("constructs_all", [])}.issubset(constructs):
        return False
    design = token_set(row.get("design", ""))
    required_design = {normalize_text(item) for item in criteria.get("design_any", [])}
    return not required_design or bool(design & required_design)


def audit_coverage(run_dir: Path, source: Path, requirements_path: Path) -> dict:
    requirements = json.loads(requirements_path.read_text(encoding="utf-8"))
    errors = []
    if requirements.get("schema_version") != 1:
        errors.append("coverage requirements schema_version must be 1")
    slots = requirements.get("requirements", [])
    if not slots:
        errors.append("coverage requirements must contain at least one slot")
    _, rows = read_csv(source)
    matrix, missing_core = [], []
    for slot in slots:
        matched = [row.get("candidate_id", "") for row in rows if matches_requirement(row, slot.get("criteria", {}))]
        minimum = int(slot.get("minimum", 1))
        status = "covered" if len(matched) >= minimum else "gap"
        if status == "gap" and slot.get("core", False):
            missing_core.append(slot.get("slot_id", ""))
        matrix.append({
            "slot_id": slot.get("slot_id", ""), "core": str(bool(slot.get("core", False))).lower(),
            "minimum": minimum, "matched_count": len(matched), "status": status,
            "matched_candidate_ids": ";".join(matched),
        })
    if errors:
        return {"status": "blocked", "errors": errors}
    output_dir = run_dir / "04_文献筛选与小综述"
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = output_dir / "证据覆盖矩阵_evidence_coverage.csv"
    with matrix_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(matrix[0]))
        writer.writeheader()
        writer.writerows(matrix)
    memo_path = output_dir / "证据缺口_gap_memo.md"
    lines = ["# 证据覆盖与缺口", "", f"- 核心缺口数：{len(missing_core)}", ""]
    for item in matrix:
        marker = "已覆盖" if item["status"] == "covered" else "缺口"
        lines.append(f"- `{item['slot_id']}`：{marker}（{item['matched_count']}/{item['minimum']}）")
    if missing_core:
        lines.extend(["", "## 阻断项", "", *[f"- {slot}" for slot in missing_core]])
    memo_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    status = "ready" if not missing_core else "blocked"
    result = {
        "schema_version": 1, "status": status, "source": str(source.resolve()),
        "source_sha256": sha256_file(source), "requirements": str(requirements_path.resolve()),
        "requirements_sha256": sha256_file(requirements_path), "missing_core_slots": missing_core,
        "coverage_matrix": str(matrix_path.resolve()), "gap_memo": str(memo_path.resolve()),
    }
    manifest_path = output_dir / "证据覆盖审计_evidence_coverage_audit.json"
    write_json(manifest_path, result)
    return {**result, "manifest": str(manifest_path.resolve())}


def build_retrieval_queue(run_dir: Path, source: Path) -> dict:
    _, rows = read_csv(source)
    priority = {"direct-empirical": 1, "measurement": 2, "method": 2, "systematic-review": 3, "background": 4}
    queued = []
    for row in rows:
        if normalize_text(row.get("retraction_status", "")) in {"retracted", "withdrawn"}:
            continue
        if normalize_text(row.get("fulltext_status", "")) in {"available", "verified"}:
            continue
        role = normalize_text(row.get("evidence_role", ""))
        queued.append({
            "queue_rank": 0, "priority": priority.get(role, 5), "candidate_id": row.get("candidate_id", ""),
            "title": row.get("title", ""), "doi": normalize_doi(row.get("doi", "")),
            "landing_url": row.get("landing_url", ""), "evidence_role": row.get("evidence_role", ""),
            "retrieval_status": "queued", "access_route": "authorized-manual-or-open-access",
            "verification_required": "true", "notes": "",
        })
    queued.sort(key=lambda item: (item["priority"], normalize_text(item["title"]), item["candidate_id"]))
    for index, item in enumerate(queued, 1):
        item["queue_rank"] = index
    output_dir = run_dir / "03_Zotero与全文获取"
    output_dir.mkdir(parents=True, exist_ok=True)
    queue_path = output_dir / "全文获取队列_retrieval_queue.csv"
    fields = [
        "queue_rank", "priority", "candidate_id", "title", "doi", "landing_url", "evidence_role",
        "retrieval_status", "access_route", "verification_required", "notes",
    ]
    with queue_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(queued)
    manifest = {
        "schema_version": 1, "status": "complete", "source": str(source.resolve()),
        "source_sha256": sha256_file(source), "queued_records": len(queued),
        "retrieval_queue": str(queue_path.resolve()),
    }
    manifest_path = output_dir / "全文获取清单_retrieval_manifest.json"
    write_json(manifest_path, manifest)
    return {**manifest, "manifest": str(manifest_path.resolve())}


def record_identity(row: dict) -> str:
    doi = normalize_doi(row.get("doi", ""))
    if doi:
        return f"doi:{doi}"
    pmid = normalize_text(row.get("pmid", ""))
    if pmid:
        return f"pmid:{pmid}"
    openalex_id = normalize_text(row.get("openalex_id", "").rsplit("/", 1)[-1])
    if openalex_id:
        return f"openalex:{openalex_id}"
    return "meta:" + "|".join([
        normalize_text(row.get("title", "")), first_author(row.get("authors", "")), year_from(row.get("year", "")),
    ])


def comparable_hash(row: dict) -> str:
    ignored = {"candidate_id", "metadata_verified_at", "raw_export_file", "raw_export_sha256"}
    payload = {key: normalize_text(value) for key, value in sorted(row.items()) if key not in ignored}
    return sha256_bytes(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def refresh_search(run_dir: Path, baseline_path: Path, current_path: Path) -> dict:
    fields, baseline_rows = read_csv(baseline_path)
    current_fields, current_rows = read_csv(current_path)
    baseline = {record_identity(row): row for row in baseline_rows}
    current = {record_identity(row): row for row in current_rows}
    changes = []
    for identity in sorted(current.keys() - baseline.keys()):
        changes.append({"change_type": "new", "identity": identity, **current[identity]})
    for identity in sorted(baseline.keys() & current.keys()):
        if comparable_hash(baseline[identity]) != comparable_hash(current[identity]):
            changes.append({"change_type": "metadata-changed", "identity": identity, **current[identity]})
    for identity in sorted(baseline.keys() - current.keys()):
        changes.append({"change_type": "missing-from-refresh", "identity": identity, **baseline[identity]})
    output_dir = run_dir / "02_证据检索"
    output_dir.mkdir(parents=True, exist_ok=True)
    changes_path = output_dir / "检索更新差异_search_refresh_changes.csv"
    output_fields = ["change_type", "identity", *dict.fromkeys(fields + current_fields)]
    with changes_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(changes)
    counts = {
        "new_records": sum(item["change_type"] == "new" for item in changes),
        "changed_records": sum(item["change_type"] == "metadata-changed" for item in changes),
        "missing_from_refresh": sum(item["change_type"] == "missing-from-refresh" for item in changes),
    }
    log = {
        "schema_version": 1, "status": "complete", "created_at": now(),
        "baseline": str(baseline_path.resolve()), "baseline_sha256": sha256_file(baseline_path),
        "current": str(current_path.resolve()), "current_sha256": sha256_file(current_path),
        **counts, "changes": str(changes_path.resolve()),
        "policy": "missing records are retained and flagged; refresh never deletes baseline evidence",
    }
    log_path = output_dir / "检索更新记录_search_refresh_log.json"
    write_json(log_path, log)
    return {**log, "refresh_log": str(log_path.resolve())}


def plan_search(run_dir: Path, spec_path: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    errors = []
    required = {"schema_version", "review_id", "concept_blocks", "query_families", "languages", "search_update_days"}
    if missing := required - set(spec):
        errors.append(f"search-plan fields missing: {sorted(missing)}")
    if spec.get("schema_version") != 1:
        errors.append("search-plan schema_version must be 1")
    blocks = spec.get("concept_blocks", {})
    queries = []
    seen_families = set()
    for family in spec.get("query_families", []):
        family_id = family.get("family_id")
        if not family_id or family_id in seen_families:
            errors.append(f"query family has missing or duplicate family_id: {family_id}")
            continue
        seen_families.add(family_id)
        missing_blocks = [name for name in family.get("blocks", []) if name not in blocks]
        if missing_blocks:
            errors.append(f"query family {family_id} references missing blocks: {missing_blocks}")
        if not family.get("queries"):
            errors.append(f"query family {family_id} has no database-verified queries")
        for database, query in family.get("queries", {}).items():
            normalized = " ".join(str(query).split())
            if not database or not normalized:
                errors.append(f"query family {family_id} contains an empty database query")
                continue
            queries.append({
                "search_id": f"search-{len(queries) + 1:04d}", "family_id": family_id,
                "purpose": family.get("purpose", "unspecified"), "database": database,
                "query": normalized, "query_sha256": sha256_bytes(normalized.encode("utf-8")),
                "blocks": family.get("blocks", []), "syntax_status": "provided-exact-not-live-verified",
            })
    if errors:
        return {"status": "blocked", "errors": errors}
    output_dir = run_dir / "02_证据检索"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1, "status": "ready", "review_id": spec["review_id"],
        "created_at": now(), "spec": str(spec_path.resolve()), "spec_sha256": sha256_file(spec_path),
        "languages": spec["languages"], "search_update_days": spec["search_update_days"],
        "concept_blocks": blocks, "queries": queries,
    }
    plan_path = output_dir / "检索计划_search_plan.json"
    write_json(plan_path, payload)
    lines = [
        "# 检索式记录", "", f"- Review ID：`{spec['review_id']}`",
        f"- 计划 SHA-256：`{sha256_file(plan_path)}`", f"- 更新周期：{spec['search_update_days']} 天", "",
        "## 概念块", "",
    ]
    for name, terms in blocks.items():
        lines.append(f"- **{name}**：{'；'.join(terms)}")
    for query in queries:
        lines.extend([
            "", f"## {query['family_id']} / {query['database']}", "",
            f"- 用途：{query['purpose']}", f"- Search ID：`{query['search_id']}`",
            f"- Query SHA-256：`{query['query_sha256']}`", "", "```text", query["query"], "```",
        ])
    markdown_path = output_dir / "检索式记录_queries.md"
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return {
        "status": "ready", "query_count": len(queries), "search_plan": str(plan_path.resolve()),
        "queries_markdown": str(markdown_path.resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan-search")
    plan.add_argument("--run-dir", required=True)
    plan.add_argument("--spec", required=True)
    ingest = subparsers.add_parser("import-evidence")
    ingest.add_argument("--run-dir", required=True)
    ingest.add_argument("--input", action="append", required=True)
    ingest.add_argument("--search-id", required=True)
    cluster = subparsers.add_parser("cluster-studies")
    cluster.add_argument("--run-dir", required=True)
    cluster.add_argument("--input", required=True)
    coverage = subparsers.add_parser("audit-evidence-coverage")
    coverage.add_argument("--run-dir", required=True)
    coverage.add_argument("--input", required=True)
    coverage.add_argument("--requirements", required=True)
    retrieval = subparsers.add_parser("build-retrieval-queue")
    retrieval.add_argument("--run-dir", required=True)
    retrieval.add_argument("--input", required=True)
    refresh = subparsers.add_parser("refresh-search")
    refresh.add_argument("--run-dir", required=True)
    refresh.add_argument("--baseline", required=True)
    refresh.add_argument("--current", required=True)
    args = parser.parse_args()
    if args.command == "plan-search":
        result = plan_search(Path(args.run_dir).resolve(), Path(args.spec).resolve())
    elif args.command == "import-evidence":
        result = import_evidence(
            Path(args.run_dir).resolve(), [Path(item).resolve() for item in args.input], args.search_id,
        )
    elif args.command == "cluster-studies":
        result = cluster_studies(Path(args.run_dir).resolve(), Path(args.input).resolve())
    elif args.command == "audit-evidence-coverage":
        result = audit_coverage(
            Path(args.run_dir).resolve(), Path(args.input).resolve(), Path(args.requirements).resolve(),
        )
    elif args.command == "build-retrieval-queue":
        result = build_retrieval_queue(Path(args.run_dir).resolve(), Path(args.input).resolve())
    elif args.command == "refresh-search":
        result = refresh_search(
            Path(args.run_dir).resolve(), Path(args.baseline).resolve(), Path(args.current).resolve(),
        )
    else:
        raise AssertionError(args.command)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"ready", "complete"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
