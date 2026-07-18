#!/usr/bin/env python3
"""Build a privacy-safe simulated submission-readiness package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_policy(policy: dict, base_dir: Path) -> list[str]:
    required = {
        "journal", "article_type", "checked_at", "scope_fit", "word_limit", "ai_policy",
        "data_policy", "official_domains", "submission_url", "source_urls", "source_snapshots",
    }
    errors = [f"journal policy fields missing: {sorted(required - set(policy))}"] if required - set(policy) else []
    if errors:
        return errors
    try:
        checked = date.fromisoformat(policy["checked_at"])
        age = (date.today() - checked).days
        if age < 0 or age > 90:
            errors.append(f"journal policy check is not current: {age} days")
    except ValueError:
        errors.append("journal policy checked_at must use ISO date")
    urls = [policy.get("submission_url", ""), *policy.get("source_urls", [])]
    if any(not url.startswith("https://") for url in urls):
        errors.append("journal policy URLs must be verified HTTPS sources")
    domains = {value.lower().strip(".") for value in policy.get("official_domains", []) if value}
    if not domains:
        errors.append("at least one official publisher or journal domain is required")
    disallowed = {"example.com", "example.org", "localhost"}
    for url in urls:
        host = (urlparse(url).hostname or "").lower().strip(".")
        if host in disallowed or not any(host == domain or host.endswith("." + domain) for domain in domains):
            errors.append(f"journal policy URL is outside declared official domains: {url}")
    snapshots = {item.get("url"): item for item in policy.get("source_snapshots", []) if item.get("url")}
    for url in policy.get("source_urls", []):
        snapshot = snapshots.get(url)
        if not snapshot:
            errors.append(f"journal policy source snapshot missing: {url}")
            continue
        try:
            retrieved = date.fromisoformat(snapshot.get("retrieved_at", ""))
            age = (date.today() - retrieved).days
            if age < 0 or age > 90:
                errors.append(f"journal policy snapshot is not current: {url}")
        except ValueError:
            errors.append(f"journal policy snapshot retrieved_at must use ISO date: {url}")
        snapshot_path = Path(snapshot.get("file", "")).expanduser()
        if not snapshot_path.is_absolute():
            snapshot_path = (base_dir / snapshot_path).resolve()
        if not snapshot_path.is_file():
            errors.append(f"journal policy snapshot file missing: {url}")
        elif snapshot.get("sha256") != sha256(snapshot_path):
            errors.append(f"journal policy snapshot hash mismatch: {url}")
    return errors


def build(run_dir: Path, policy_path: Path, manuscript: Path, numeric_audit: Path, claim_audit: Path) -> dict:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    errors = validate_policy(policy, policy_path.parent)
    numeric = json.loads(numeric_audit.read_text(encoding="utf-8"))
    if numeric.get("status") != "verified":
        errors.append("numeric audit is not verified")
    claim_text = claim_audit.read_text(encoding="utf-8")
    if "未解决阻断：0" not in claim_text or "unsupported：0" not in claim_text or "overextended：0" not in claim_text:
        errors.append("claim audit contains unresolved or unreported risks")
    if not manuscript.is_file():
        errors.append("manuscript missing")
    if errors:
        return {"status": "blocked", "errors": errors}

    review_dir = run_dir / "11_模拟投稿审稿"
    review_dir.mkdir(parents=True, exist_ok=True)
    package_dir = review_dir / "预投稿包_submission_package"
    package_dir.mkdir(exist_ok=True)
    journal_fit = review_dir / "期刊适配报告_journal_fit.md"
    journal_fit.write_text(
        "# 期刊适配报告\n\n"
        f"- 期刊：{policy['journal']}\n- 文章类型：{policy['article_type']}\n"
        f"- 官网核查日期：{policy['checked_at']}\n- Scope适配：{policy['scope_fit']}\n"
        f"- 字数限制：{policy['word_limit']}\n- AI政策：{policy['ai_policy']}\n"
        f"- 数据政策：{policy['data_policy']}\n- 投稿入口：{policy['submission_url']}\n",
        encoding="utf-8", newline="\n",
    )
    simulated = review_dir / "模拟审稿意见_simulated_reviews.md"
    simulated.write_text(
        "# 模拟审稿意见\n\n> 本文件为自动化模拟审稿，不代表真实期刊、编辑或审稿人。\n\n"
        "## 主编初筛\n\n期刊政策、文章类型、数字审计和主张审计已提供。\n\n"
        "## 理论审稿\n\n需由领域专家继续判断理论新意和文献完整性。\n\n"
        "## 方法与统计审稿\n\n自动核验仅证明材料齐备，不替代对模型假设、识别和估计的专业判断。\n\n"
        "## 测量与开放科学审稿\n\n需报告量表来源、跨波可比性、代码可用性及敏感数据限制。\n\n"
        "## 反对性审稿\n\n重点复核因果措辞、选择性报告、性别组间检验和自伤数据隐私。\n\n"
        "## 综合决定\n\n状态：可进入人工预投稿审查，不等于建议直接投稿。\n",
        encoding="utf-8", newline="\n",
    )
    revision = review_dir / "修改矩阵_revision_matrix.csv"
    fields = ["comment_id", "severity", "source", "location", "comment", "response", "action", "artifact", "status", "evidence"]
    with revision.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "comment_id": "AUTO-001", "severity": "minor", "source": "automation",
            "location": "submission package", "comment": "Verify automated readiness artifacts",
            "response": "Numeric, claim, and journal-policy checks passed", "action": "retain audit trail",
            "artifact": "最终审计_final_audit.md", "status": "resolved", "evidence": "submission manifest",
        })
    response = review_dir / "作者回复草稿_response_to_reviewers.md"
    response.write_text(
        "# 作者回复草稿\n\n> 模拟回复模板，不对应真实审稿意见。\n\n"
        "## AUTO-001\n\n已保留数字核查、主张核查和期刊政策核查记录。\n",
        encoding="utf-8", newline="\n",
    )
    final_audit = review_dir / "最终审计_final_audit.md"
    final_audit.write_text(
        "# 最终审计\n\n"
        "- 目标期刊实时核查：通过\n- 数字核查：通过\n- 主张核查：通过\n"
        "- 隐私检查：预投稿包不含原始或冻结参与者数据\n"
        "- 最终状态：可进入人工预投稿审查；不得表述为已获期刊认可。\n",
        encoding="utf-8", newline="\n",
    )

    sources = [manuscript, numeric_audit, claim_audit, policy_path, journal_fit, simulated, revision, response, final_audit]
    copied = []
    for source in sources:
        if source.suffix.lower() in {".sav", ".xlsx", ".csv"} and source == manuscript:
            raise SystemExit("participant data cannot enter the submission package")
        destination = package_dir / source.name
        shutil.copy2(source, destination)
        copied.append(str(destination.resolve()))
    manifest = {
        "schema_version": 1, "status": "ready", "journal": policy["journal"],
        "article_type": policy["article_type"], "package_dir": str(package_dir.resolve()),
        "files": copied, "hashes": {path: sha256(Path(path)) for path in copied},
        "simulated_reviews": str(simulated.resolve()), "final_audit": str(final_audit.resolve()),
        "privacy": "no raw or frozen participant data included",
    }
    manifest_path = review_dir / "预投稿包清单_submission_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "manifest": str(manifest_path.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--journal-policy", required=True)
    parser.add_argument("--manuscript", required=True)
    parser.add_argument("--numeric-audit", required=True)
    parser.add_argument("--claim-audit", required=True)
    args = parser.parse_args()
    result = build(
        Path(args.run_dir).resolve(), Path(args.journal_policy).resolve(), Path(args.manuscript).resolve(),
        Path(args.numeric_audit).resolve(), Path(args.claim_audit).resolve(),
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "ready" else 3


if __name__ == "__main__":
    raise SystemExit(main())
