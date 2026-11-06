from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_review_prose as crp  # noqa: E402


def test_clean_drops_citations_headings_tables_and_comments() -> None:
    raw = "---\n类型: 草稿\n---\n# 一级标题\n焦虑(Smith, 2020)与睡眠相关（张三, 2021）。%% 主张 2-1 %%\n| 列一 | 列二 |\n"
    text = crp.clean(raw)
    assert "Smith" not in text and "张三" not in text
    assert "一级标题" not in text and "主张" not in text and "列一" not in text
    assert "焦虑与睡眠相关。" in text


def test_report_flags_semicolon_lists_and_banned_transitions(tmp_path: Path) -> None:
    draft = tmp_path / "草稿.md"
    draft.write_text(
        "值得注意的是，甲组的得分较高；乙组的得分较低；丙组未达到显著；丁组均为自评。\n下文将讨论其意义和可能的原因。\n",
        encoding="utf-8",
    )
    result = crp.report(draft)
    rows = {row["指标"]: row for row in result["指标"]}
    assert rows["分号/万字"]["判定"] == "偏高"
    assert result["短稿"] is True
    assert {"值得注意的是", "下文将"} <= {hit["词"] for hit in result["禁用词"]}
    assert "禁用的过渡词和目录句" in crp.render(result)
