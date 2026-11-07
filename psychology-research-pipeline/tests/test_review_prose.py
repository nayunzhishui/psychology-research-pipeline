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


def pattern_verdicts(text: str, tmp_path: Path) -> dict[str, str]:
    draft = tmp_path / "草稿.md"
    draft.write_text(text, encoding="utf-8")
    return {row["指标"]: row["判定"] for row in crp.report(draft)["句式与引用"]}


def test_n_cites_counts_parenthetical_and_narrative_citations() -> None:
    p = "焦虑升高(Smith, 2020; Lee & Kim, 2021)。Clark 等人(2018)发现了同样的结果。张三等(2019)认为两者有别。"
    assert crp.n_cites(p) == 4


def test_patterns_flag_study_openers_pairwise_correlations_and_citation_piles(tmp_path: Path) -> None:
    study = "一项针对大学生的研究发现，焦虑与抑郁的得分显著相关。"
    cited = ("一项针对大学生的研究发现，焦虑与抑郁的得分显著相关"
             "(Smith, 2020; Lee, 2021; Wang, 2022; Chen, 2023; Zhao, 2024)。")
    verdicts = pattern_verdicts("\n\n".join([cited + study * 7] * 8), tmp_path)
    assert verdicts["以“一项”开头的句子 %"] == "偏多"
    assert verdicts["“相关”/万字"] == "偏多"
    assert verdicts["“相关、关系、关联”合计/万字"] == "偏多"
    assert verdicts["不引文献的段 %"] == "偏少"
    assert verdicts["每段引用数（中位数）"] == "偏多"


def test_patterns_accept_selective_citations_and_uncited_judgements(tmp_path: Path) -> None:
    cited = "甲组的平均分明显高于乙组(Smith, 2020)，二者的差异在统计上显著。"
    paras = [LONG * 2 + MID * 2 if i in (0, 3, 8) else cited + LONG * 2 + MID for i in range(9)]
    verdicts = pattern_verdicts("\n\n".join(paras), tmp_path)
    assert set(verdicts.values()) == {"在范围内"}, verdicts


def test_patterns_do_not_judge_short_drafts(tmp_path: Path) -> None:
    verdicts = pattern_verdicts(MID * 3, tmp_path)
    assert set(verdicts.values()) == {"不判断"}


def move_verdicts(text: str, tmp_path: Path) -> dict[str, str]:
    draft = tmp_path / "草稿.md"
    draft.write_text(text, encoding="utf-8")
    return {row["动作"]: row["判定"] for row in crp.report(draft)["论证动作"]}


def test_moves_suggest_evidence_strength_and_alternatives_when_absent(tmp_path: Path) -> None:
    verdicts = move_verdicts("\n\n".join([LONG + MID] * 7), tmp_path)
    assert verdicts["写出证据强弱"] == "可以加上"
    assert verdicts["替代解释"] == "可以加上"
    assert verdicts["标明本文的推论"] == "没有"


def test_moves_count_graded_evidence_alternatives_and_stance(tmp_path: Path) -> None:
    paras = [LONG + MID] * 6 + ["自评、访谈和他评的结果方向相同，甲组都高于乙组。"
                                "另一种解释是两组的测量时点不同。本文认为，这一差异主要来自基线。"]
    verdicts = move_verdicts("\n\n".join(paras), tmp_path)
    assert set(verdicts.values()) == {"有"}, verdicts
    assert move_verdicts(MID * 3, tmp_path)["替代解释"] == "不判断"


def test_moves_no_longer_count_study_numbers_as_evidence_strength(tmp_path: Path) -> None:
    paras = [LONG + MID] * 6 + ["至少 5 项研究发现甲组高于乙组。"]
    assert move_verdicts("\n\n".join(paras), tmp_path)["写出证据强弱"] == "可以加上"


def test_count_claims_flag_study_counts_and_claims_of_absence(tmp_path: Path) -> None:
    draft = tmp_path / "草稿.md"
    draft.write_text("至少 8 项研究发现甲组更高。本文只找到 2 项。尚无研究检验这一点。\n\n"
                     "这是唯一用父母报告的研究，证据最多的是内化问题。\n%%\n至少 3 项（注释里的不算）\n%%\n",
                     encoding="utf-8")
    kinds = [h["类型"] for h in crp.report(draft)["项数与穷尽说法"]]
    assert kinds.count("研究项数") == 2 and kinds.count("说没有研究") == 1 and kinds.count("全称说法") == 2, kinds


def test_count_claims_accept_references_to_cited_studies_and_research_needs(tmp_path: Path) -> None:
    draft = tmp_path / "草稿.md"
    draft.write_text("上述两项研究都发现甲组更高，这 2 项研究的样本不同。这一问题需要纵向研究来回答。\n", encoding="utf-8")
    assert crp.report(draft)["项数与穷尽说法"] == []
    assert crp.report(draft, systematic=True)["项数与穷尽说法"] is None


def test_repeats_flag_the_same_judgement_in_two_paragraphs(tmp_path: Path) -> None:
    claim = "人格功能损害与总体困扰和内化问题的同向变化最为一致，外化问题的结果较少。"
    others = ["甲组在随访中的平均分高于乙组，差异在三个时点上都保持稳定。",
              "睡眠时长与次日的情绪评分没有明显的联系，只在周末略有不同。",
              "父母报告的照料负担随孩子年龄增长而下降，男孩下降得更快。",
              "访谈评分与自评问卷的一致性在临床样本中高于社区样本。"]
    text = "\n\n".join([claim + others[0], others[1] + others[2], others[3] + claim])
    hits = crp.repeats(text)
    assert len(hits) == 1 and hits[0]["段"] == [1, 3], hits
    assert crp.repeats("\n\n".join([others[0] + others[1], others[2] + others[3]])) == []
