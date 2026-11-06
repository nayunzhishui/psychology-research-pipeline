from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_review_prose as crp  # noqa: E402

MID = "甲组的平均分明显高于乙组，二者的差异在统计上显著。"
SHORT = "两组结果基本一致。"
LONG = ("在控制年龄、性别和基线得分以后，甲组在随访期间的平均分仍然明显高于乙组，"
        "而且这一差异在三个测量时点上都保持稳定，没有随时间缩小的迹象，这与前人的结果相符。")


def spread_verdicts(text: str, tmp_path: Path) -> dict[str, str]:
    draft = tmp_path / "草稿.md"
    draft.write_text(text, encoding="utf-8")
    return {row["指标"]: row["判定"] for row in crp.report(draft)["长短起伏"]}


def test_clean_drops_citations_headings_tables_and_comments() -> None:
    raw = "---\n类型: 草稿\n---\n# 一级标题\n焦虑(Smith, 2020)与睡眠相关（张三, 2021）。%% 主张 2-1 %%\n| 列一 | 列二 |\n"
    text = crp.clean(raw)
    assert "Smith" not in text and "张三" not in text
    assert "一级标题" not in text and "主张" not in text and "列一" not in text
    assert "焦虑与睡眠相关。" in text


def test_clean_drops_table_captions_and_notes() -> None:
    raw = "**表 1　样本特征**\n\n| 组别 | 人数 |\n|---|---|\n\n注：数值为均值。\n\n正文句子照常保留。\n"
    text = crp.clean(raw)
    assert "样本特征" not in text and "数值为均值" not in text
    assert "正文句子照常保留。" in text


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


def test_spread_flags_paragraphs_and_sentences_that_are_too_uniform(tmp_path: Path) -> None:
    text = "\n\n".join([MID * 4] * 8)
    verdicts = spread_verdicts(text, tmp_path)
    for name in ("段长变异系数", "每段句数的极差", "句长变异系数", "长于 60 字的句子 %"):
        assert verdicts[name] == "太整齐", name


def test_spread_accepts_lengths_that_follow_the_task(tmp_path: Path) -> None:
    paras = [MID, LONG + SHORT, MID * 2 + LONG * 2 + SHORT * 2, SHORT + MID,
             LONG * 3 + MID * 2, MID + SHORT * 2, LONG + MID + SHORT * 2]
    verdicts = spread_verdicts("\n\n".join(paras), tmp_path)
    for name in ("段长变异系数", "每段句数的极差", "句长变异系数", "长于 60 字的句子 %"):
        assert verdicts[name] == "有起伏", name


def test_spread_does_not_judge_short_drafts(tmp_path: Path) -> None:
    verdicts = spread_verdicts(MID * 3 + "\n\n" + MID * 3, tmp_path)
    assert verdicts["段长变异系数"] == "不判断"
    assert verdicts["句长变异系数"] == "不判断"
