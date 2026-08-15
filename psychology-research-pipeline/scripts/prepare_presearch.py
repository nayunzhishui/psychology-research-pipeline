#!/usr/bin/env python3
"""Render auditable scope and protocol drafts before any literature search is run."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from pipeline_schema import CSV_HEADERS


REQUIRED_KEYS = {
    "schema_version", "protocol_id", "title", "purpose", "study", "estimands",
    "research_questions", "hypotheses", "constructs", "analysis_families",
    "inference_boundaries", "reporting", "ethics", "open_science",
    "search_protocol", "unresolved_items", "approval",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def bullets(values: list[str], empty: str = "- 无已记录事项") -> str:
    return "\n".join(f"- {value}" for value in values) if values else empty


def tiered(values: list[dict]) -> str:
    labels = {"primary": "主要", "secondary": "次要", "exploratory": "探索性"}
    return "\n".join(
        f"- **{item['id']}（{labels[item['tier']]}；{item['status']}）**：{item['text']}"
        for item in values
    )


def validate_spec(spec: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_KEYS - set(spec)
    if missing:
        errors.append(f"presearch protocol keys missing: {sorted(missing)}")
        return errors
    if spec.get("schema_version") != 1:
        errors.append("presearch protocol schema_version must be 1")
    if not spec.get("estimands") or not spec.get("research_questions") or not spec.get("constructs"):
        errors.append("estimands, research_questions, and constructs must be non-empty")
    ids = [item.get("id") for item in spec.get("unresolved_items", [])]
    if len(ids) != len(set(ids)):
        errors.append("unresolved item ids must be unique")
    return errors


def blocking_items(spec: dict, stages: set[str] | None = None) -> list[dict]:
    items = [
        item for item in spec["unresolved_items"]
        if item.get("status") != "resolved" and item.get("severity") == "blocking"
    ]
    if stages is not None:
        items = [item for item in items if stages.intersection(item.get("blocking_stages", []))]
    return items


def render_scope(spec: dict, scope_dir: Path) -> None:
    study = spec["study"]
    sample = study["sample"]
    approval = spec["approval"]
    constructs = "\n".join(
        f"- **{item['label']}**（{item['status']}）：{item['role']}；{item['instrument']}；{item['scoring']}"
        for item in spec["constructs"]
    )
    open_items = [item for item in spec["unresolved_items"] if item.get("status") != "resolved"]
    brief = (
        "# 项目定标简报\n\n"
        "## 项目与用途\n\n"
        f"- 题目：{spec['title']}\n- 目标：形成可投稿的心理学实证论文；不承诺发表。\n"
        f"- 设计：{study['design']}。\n- 当前状态：检索前草案；scope={approval['scope_status']}，protocol={approval['protocol_status']}。\n\n"
        "## 数据和样本\n\n"
        f"- 目标人群：{study['population']}\n- 情境：{study['setting']}\n- 波次：{', '.join(study['waves'])}\n"
        f"- 时间：{study['wave_timing']['value']}（{study['wave_timing']['status']}；来源：{study['wave_timing']['source']}）\n"
        f"- 已观察行数：{sample['observed_rows']}；解释：{sample['interpretation']}\n- 招募：{sample['recruitment']}\n\n"
        "## 主要研究问题与估计对象\n\n"
        f"{tiered(spec['research_questions'])}\n\n### 估计对象\n\n{tiered(spec['estimands'])}\n\n"
        "## 构念变量映射\n\n"
        f"{constructs}\n\n"
        "## 推论边界与排除项\n\n"
        f"{bullets(spec['inference_boundaries'])}\n\n"
        "## 风险与未决问题\n\n"
        + "\n".join(
            f"- **{item['id']} / {item['severity']} / {item['category']}**：{item['question']}；所需证据：{item['resolution_evidence']}"
            for item in open_items
        )
        + "\n"
    )
    (scope_dir / "项目定标简报_project_brief.md").write_text(brief, encoding="utf-8", newline="\n")

    hypotheses = (
        "# 研究问题与假设\n\n"
        "## 主要研究问题\n\n"
        f"{tiered([item for item in spec['research_questions'] if item['tier'] == 'primary'])}\n\n"
        "## 主要假设\n\n"
        f"{tiered([item for item in spec['hypotheses'] if item['tier'] == 'primary'])}\n\n"
        "## 次要问题\n\n"
        f"{tiered([item for item in spec['research_questions'] + spec['hypotheses'] if item['tier'] == 'secondary'])}\n\n"
        "## 探索性问题\n\n"
        f"{tiered([item for item in spec['research_questions'] + spec['hypotheses'] if item['tier'] == 'exploratory'])}\n\n"
        "## 估计对象与允许的主张\n\n"
        f"{tiered(spec['estimands'])}\n\n{bullets(spec['inference_boundaries'])}\n\n"
        "## 冻结记录\n\n"
        f"- scope_status：`{approval['scope_status']}`\n- protocol_status：`{approval['protocol_status']}`\n"
        f"- approved_by：`{approval['approved_by']}`\n- approved_at：`{approval['approved_at']}`\n"
        "- 当前内容是检索前草案；只有状态改为 approved/frozen 且阻断项解除后才算冻结。\n"
    )
    (scope_dir / "研究问题与假设_research_questions_hypotheses.md").write_text(
        hypotheses, encoding="utf-8", newline="\n"
    )

    map_path = scope_dir / "构念变量关系表_construct_variable_map.csv"
    headers = CSV_HEADERS[map_path.name]
    with map_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for item in spec["constructs"]:
            for wave, variable in item["variables"].items():
                writer.writerow({
                    "construct_id": item["construct_id"], "构念": item["label"],
                    "变量角色": item["role"], "波次": wave, "变量名": variable,
                    "工具": item["instrument"], "计分": item["scoring"],
                    "估计对象": "; ".join(value["id"] for value in spec["estimands"]),
                    "理论依据": "待证据检索后建立主张—证据映射",
                    "状态": item["status"], "备注": "不得依据主结果反向修改",
                })

    supervisor = (
        "# 导师汇报版简表\n\n"
        f"- **题目**：{spec['title']}\n- **用途**：期刊实证论文。\n- **设计**：{study['design']}。\n"
        f"- **主要估计对象**：{spec['estimands'][0]['text']}\n- **主要模型候选**：{'; '.join(spec['analysis_families']['primary'])}\n"
        f"- **关键优势**：三波原始题项可用于跨时测量检验；区分个体内与个体间关联。\n"
        f"- **关键风险**：{len(blocking_items(spec))}个阻断项尚未解决；NSSI命名、伦理、样本流和波次时间不得猜测。\n"
        f"- **当前决定**：文献检索、模型运行和正式写作均尚未开始。\n"
    )
    (scope_dir / "导师汇报版简表_supervisor_brief.md").write_text(supervisor, encoding="utf-8", newline="\n")
    questions = "# 未决问题清单\n\n" + "\n".join(
        f"- [ ] **{item['id']}（{item['severity']}；阻断 {', '.join(item['blocking_stages']) or '无'}）**："
        f"{item['question']}\n  - 解决证据：{item['resolution_evidence']}"
        for item in open_items
    ) + "\n"
    (scope_dir / "未决问题清单_open_questions.md").write_text(questions, encoding="utf-8", newline="\n")


def render_protocol(spec: dict, protocol_dir: Path) -> None:
    study = spec["study"]
    sample = study["sample"]
    families = spec["analysis_families"]
    approval = spec["approval"]
    protocol = (
        "# 实证研究协议\n\n"
        "## 研究问题与结局\n\n"
        f"{tiered(spec['research_questions'])}\n\n- 主要结局候选：三个波次的自伤/NSSI候选指标；正式命名取决于自杀意图排除证据。\n"
        "- 主要预测与内生构念：父母冲突、抑郁症状和自伤指标的个体内偏离。\n\n"
        "## 样本与纳排\n\n"
        f"- 样本状态：{sample['status']}；{sample['interpretation']}\n- 招募：{sample['recruitment']}\n"
        f"- 纳入：\n{bullets(sample['inclusion'])}\n- 排除：\n{bullets(sample['exclusion'])}\n\n"
        "## 变量与计分\n\n"
        + "\n".join(
            f"- **{item['label']}（{item['status']}）**：变量={item['variables']}；{item['scoring']}；工具={item['instrument']}"
            for item in spec["constructs"]
        )
        + "\n\n## 分析族\n\n"
        f"- 主要：\n{bullets(families['primary'])}\n- 次要：\n{bullets(families['secondary'])}\n"
        f"- 敏感性：\n{bullets(families['sensitivity'])}\n- 探索性：\n{bullets(families['exploratory'])}\n"
        f"- 多重性：{families['multiplicity']}\n\n"
        "## 偏离政策\n\n"
        f"{spec['open_science']['deviation_policy']} 所有偏离记录计划、实际、原因、影响、探索性标记和正文披露位置。\n\n"
        "## 冻结记录\n\n"
        f"- scope_status：`{approval['scope_status']}`\n- protocol_status：`{approval['protocol_status']}`\n"
        f"- approved_by：`{approval['approved_by']}`\n- approved_at：`{approval['approved_at']}`\n"
        "- 协议不得在读取本轮主结果后回填为事前决定。\n"
    )
    (protocol_dir / "实证研究协议_empirical_protocol.md").write_text(protocol, encoding="utf-8", newline="\n")

    reporting = spec["reporting"]
    reporting_text = (
        "# 报告规范计划\n\n"
        f"## 研究分类\n\n{reporting['study_class']}。本研究不是随机试验，也不把实证论文中的小综述宣称为系统综述。\n\n"
        "## 适用规范\n\n"
        f"{bullets(reporting['standards'])}\n\n"
        "## 要求到产物映射\n\n"
        "- APA JARS-Quant：研究问题、样本、测量、分析、效应估计、不确定性、透明性声明。\n"
        "- STROBE：研究设计、场景、参与者、波次、流失、变量、偏倚、统计方法和限制。\n"
        "- SAGER：区分记录的sex与gender，说明编码、缺失、比较方法和局限。\n"
        "- 规范用于报告完整性，不替代方法质量评价。\n\n"
        "## 目标期刊待核查项\n\n"
        f"- 目标期刊：{reporting['target_journal']}。\n- 官网政策状态：{reporting['policy_status']}。\n"
        "- 正式投稿前实时核查文章类型、字数、摘要结构、表图、补充材料、开放数据例外、AI披露和伦理声明。\n"
    )
    (protocol_dir / "报告规范计划_reporting_plan.md").write_text(reporting_text, encoding="utf-8", newline="\n")

    ethics = spec["ethics"]
    science = spec["open_science"]
    ethics_text = (
        "# 伦理与开放科学\n\n"
        "## 已知伦理事实\n\n"
        f"{bullets(ethics['known_facts'])}\n\n"
        "## 未核实事项\n\n"
        f"- 伦理批准：{ethics['approval_status']}；批准号：{ethics['approval_id']}。\n"
        f"- 监护人同意：{ethics['consent_status']}；青少年同意：{ethics['assent_status']}；风险处置：{ethics['risk_protocol_status']}。\n"
        f"{bullets(ethics['unknowns'])}\n- 未核实事项不得改写为肯定性伦理声明。\n\n"
        "## 敏感数据保护\n\n"
        "- 原始标识符、行级自伤反应、学校代码和小单元交叉组合不得进入版本库、公开论文附件或公开数据。\n"
        "- 私密问题登记仅保存伪匿名定位信息，并置于被版本控制排除的目录。\n\n"
        "## 数据代码材料可用性\n\n"
        f"- 数据：{science['data_sharing']}\n- 代码：{science['code_sharing']}\n- 材料：{science['materials_sharing']}\n\n"
        "## 预注册与披露\n\n"
        f"- 预注册/后设协议：{science['preregistration']}\n- 偏离：{science['deviation_policy']}\n"
    )
    (protocol_dir / "伦理与开放科学_ethics_open_science.md").write_text(
        ethics_text, encoding="utf-8", newline="\n"
    )


def render_search_prep(spec: dict, search_dir: Path, spec_path: Path) -> None:
    search = spec["search_protocol"]
    text = (
        "# 检索前方案\n\n"
        "## 数据库与范围\n\n"
        f"- 数据库：{', '.join(search['databases'])}\n- 语言：{', '.join(search['languages'])}\n- 日期范围：{search['date_range']}\n\n"
        "## 纳入标准\n\n"
        f"{bullets(search['include'])}\n\n## 排除标准\n\n{bullets(search['exclude'])}\n\n"
        "## 补充检索\n\n"
        f"{bullets(search['supplemental_methods'])}\n\n## 筛选与审计\n\n- {search['screening_plan']}\n"
        "- 本文件仅准备协议；尚未执行数据库检索、题录导入或文献筛选。\n"
    )
    (search_dir / "检索前方案_presearch_protocol.md").write_text(text, encoding="utf-8", newline="\n")
    target = search_dir / "检索前协议_presearch_protocol.json"
    target.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    provenance = {
        "schema_version": 1,
        "source": str(spec_path.resolve()),
        "source_sha256": sha256(spec_path),
        "rendered_copy": str(target.resolve()),
        "rendered_copy_sha256": sha256(target),
        "rendered_at": now(),
    }
    (search_dir / "检索前协议来源_presearch_provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def readiness_payload(spec: dict, spec_path: Path) -> dict:
    approval = spec["approval"]
    early_blockers = blocking_items(spec, {"00_scope", "01_protocol", "02_search"})
    approval_errors = []
    if approval.get("scope_status") != "approved":
        approval_errors.append("scope_status is not approved")
    if approval.get("protocol_status") != "frozen":
        approval_errors.append("protocol_status is not frozen")
    if approval.get("approved_by") in {"", "unknown"} or approval.get("approved_at") in {"", "unknown"}:
        approval_errors.append("approval identity or timestamp is unknown")
    ethics = spec["ethics"]
    ethics_errors = []
    for key in ["approval_status", "consent_status", "assent_status", "risk_protocol_status"]:
        if ethics.get(key) == "unverified":
            ethics_errors.append(f"ethics.{key} is unverified")
    ready = not early_blockers and not approval_errors and not ethics_errors
    return {
        "schema_version": 1,
        "status": "ready" if ready else "blocked",
        "ready_for_search": ready,
        "prepared_at": now(),
        "protocol_source": str(spec_path.resolve()),
        "protocol_sha256": sha256(spec_path),
        "approval": approval,
        "blocking_items": early_blockers,
        "approval_errors": approval_errors,
        "ethics_errors": ethics_errors,
        "all_open_items": [item for item in spec["unresolved_items"] if item.get("status") != "resolved"],
        "guardrail": "prepared artifacts are drafts; no literature search, import, analysis, or submission occurred",
    }


def write_readiness(payload: dict, protocol_dir: Path) -> None:
    json_path = protocol_dir / "检索前准备审计_presearch_readiness.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# 检索前准备审计", "", f"- 状态：**{payload['status']}**",
        f"- 可开始正式检索：**{payload['ready_for_search']}**",
        f"- 协议哈希：`{payload['protocol_sha256']}`", "",
        "## 阻断项", "",
    ]
    if payload["blocking_items"]:
        lines.extend(
            f"- **{item['id']}**：{item['question']}（阻断 {', '.join(item['blocking_stages'])}）"
            for item in payload["blocking_items"]
        )
    else:
        lines.append("- 无。")
    lines.extend(["", "## 审批与伦理检查", ""])
    lines.extend(f"- {value}" for value in payload["approval_errors"] + payload["ethics_errors"])
    if not payload["approval_errors"] and not payload["ethics_errors"]:
        lines.append("- 已满足。")
    lines.extend(["", "## 边界", "", f"- {payload['guardrail']}", ""])
    (protocol_dir / "检索前准备审计_presearch_readiness.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


def prepare(run_dir: Path, spec_path: Path) -> tuple[dict, int]:
    state_path = run_dir / "状态记录_state.json"
    if not state_path.is_file():
        return {"status": "blocked", "errors": [f"run state missing: {state_path}"]}, 3
    if not spec_path.is_file():
        return {"status": "blocked", "errors": [f"presearch protocol missing: {spec_path}"]}, 3
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "blocked", "errors": [f"invalid presearch protocol JSON: {exc}"]}, 3
    errors = validate_spec(spec)
    if errors:
        return {"status": "blocked", "errors": errors}, 3

    scope_dir = run_dir / "00_项目定标"
    protocol_dir = run_dir / "01_标准与协议"
    search_dir = run_dir / "02_证据检索"
    render_scope(spec, scope_dir)
    render_protocol(spec, protocol_dir)
    render_search_prep(spec, search_dir, spec_path)
    readiness = readiness_payload(spec, spec_path)
    write_readiness(readiness, protocol_dir)
    payload = {
        **readiness,
        "status": "prepared" if readiness["ready_for_search"] else "prepared-blocked",
        "scope_dir": str(scope_dir.resolve()),
        "protocol_dir": str(protocol_dir.resolve()),
        "search_prep_dir": str(search_dir.resolve()),
        "readiness_report": str((protocol_dir / "检索前准备审计_presearch_readiness.json").resolve()),
    }
    return payload, 0 if readiness["ready_for_search"] else 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()
    payload, code = prepare(Path(args.run_dir).resolve(), Path(args.spec).resolve())
    print(json.dumps(payload, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
