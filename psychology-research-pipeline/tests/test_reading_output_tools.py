"""阅读产出自检和机械整理脚本的回归测试：每一条都对应真实笔记里出过的问题。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_reading_outputs as cro  # noqa: E402
import tidy_reading_notes as trn  # noqa: E402


def test_numerals_keep_tool_names_and_ranges_readable() -> None:
    assert trn.numerals("PHQ-8八题") == "PHQ-8 8 题"  # 不能变成 PHQ-88
    assert trn.numerals("0—4五档") == "0—4，共 5 档"
    assert trn.numerals("四领域") == "4 个领域"
    assert trn.numerals("十二题") == "12 题"
    for unchanged in ("三月", "第三波", "两组", "一次", "三分之一"):
        assert trn.numerals(unchanged) == unchanged


def test_links_and_quotes_are_left_alone() -> None:
    text = "[[Lindfors 2015 五年影响]]和“三个朋友”之外有三个结局"
    assert trn.outside_keep(text, lambda s: trn.spacing(trn.numerals(s))) == \
        "[[Lindfors 2015 五年影响]]和“三个朋友”之外有 3 个结局"


def test_unpile_moves_links_before_period_and_keeps_block_id_space(tmp_path: Path) -> None:
    idx = cro.Index(tmp_path, cro.SKIP_DIRS)
    pdfs = cro.Pdfs(None)
    line = "甲组 305 人。乙组 52 人。[[x.pdf#page=1|第 1 页]][[x.pdf#page=2|第 2 页]] ^f1"
    out = trn.unpile(line, idx, pdfs)
    assert out.endswith("。 ^f1")
    assert "。[[" not in out
    assert "（[[x.pdf#page=1|第 1 页]]、[[x.pdf#page=2|第 2 页]]）。" in out


def test_links_after_a_mid_paragraph_period_move_into_that_sentence(tmp_path: Path) -> None:
    idx = cro.Index(tmp_path, cro.SKIP_DIRS)
    line = "效应显著。[[x.pdf#page=8|第 8 页]]—[[x.pdf#page=9|第 9 页]]作者认为可信。"
    assert trn.unpile(line, idx, cro.Pdfs(None)) == \
        "效应显著（[[x.pdf#page=8|第 8 页]]—[[x.pdf#page=9|第 9 页]]）。作者认为可信。"


def test_glued_block_ids_get_a_space() -> None:
    assert trn.GLUED.sub(lambda m: " ^" + m.group(1), "结果很稳。^f2") == "结果很稳。 ^f2"


def _vault(tmp_path: Path) -> Path:
    kb = tmp_path / "知识库"
    (kb / "文献").mkdir(parents=True)
    (kb / "测量工具").mkdir()
    (kb / "测量工具" / "PHQ-9.md").write_text("---\n类型: 测量工具\n讲义: 简短\n---\n# PHQ-9\n\n## 是什么\n\n" + "抑郁问卷。" * 80 + "\n", encoding="utf-8")
    note = (
        "---\n类型: 文献\n候选编号: A1\n阅读深度: D2\n设计: 横断\n测量工具: [\"[[PHQ-9]]\"]\n---\n"
        "# 某某 2024：抑郁和人格功能相关的边界\n\n"
        "## 为什么读这篇\n\n这篇不能说明因果，也不等于纵向证据，样本类型记 C2。\n\n"
        "## 研究怎么做\n\n共 305 人。[[x.pdf#page=1|第 1 页]][[x.pdf#page=2|第 2 页]]\n\n"
        "## 主要发现\n\n相关 r = .40。^f1\n\n## 我的评价\n\n不能说明因果，也不能说明机制。\n\n## 对我的文章有什么用\n\n- 背景。\n"
    )
    (kb / "文献" / "某某 2024.md").write_text(note, encoding="utf-8")
    return kb


def test_check_note_flags_the_common_problems(tmp_path: Path) -> None:
    _vault(tmp_path)
    idx = cro.Index(tmp_path, cro.SKIP_DIRS)
    row = cro.check_note(tmp_path / "知识库" / "文献" / "某某 2024.md", idx, cro.Pdfs(None), cro.D2_SECTIONS, False, [], [])
    assert "速览框不在开头" in row["问题"]
    assert "标题写的是限制" in row["问题"]
    assert "块编号前缺空格" in row["问题"]
    assert "测量工具没放补课框：PHQ-9" in row["问题"]
    assert row["句外或连着的页码"] >= 1
    assert row["多处限定的段"] == 1  # “我的评价”里的限定不算
    assert "C2" in row["讲解区代号"]


def test_stacked_hedges_count_distinct_words_only() -> None:
    assert cro.stacked_hedges("这可能在一定程度上提示二者相关。") == 1
    assert cro.stacked_hedges("差异可能来自取样，也可能来自测量。") == 0
    assert cro.stacked_hedges("两者不可能同时成立；可能性很低。") == 0
    assert cro.stacked_hedges("初步结果有待重复。或许如此。") == 1


def test_stock_defensive_phrases_are_counted() -> None:
    assert len(cro.STOCK.findall("结果需谨慎解释，有待进一步研究。本节将介绍方法。")) == 3
    assert not cro.STOCK.findall("作者谨慎地选择了样本。")


def test_questions_are_not_counted_as_caveats() -> None:
    assert not cro.CAVEAT.findall("能不能觉察情绪、是不是风险因素，而不是别的")


def test_tidy_refuses_backup_inside_the_vault(tmp_path: Path) -> None:
    _vault(tmp_path)
    env = {**__import__("os").environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "tidy_reading_notes.py"), "--根", str(tmp_path), "--知识库", "知识库",
         "--写入", "--备份目录", str(tmp_path / "备份")],
        capture_output=True, text=True, encoding="utf-8", env=env)
    assert result.returncode != 0
    assert "备份目录不能放在库里面" in (result.stderr + result.stdout)


def test_check_note_flags_moved_caveats_labels_formulas_and_check_wording(tmp_path: Path) -> None:
    kb = tmp_path / "知识库"
    (kb / "文献").mkdir(parents=True)
    note = (
        "---\n类型: 文献\n阅读深度: D2\n设计: 横断\n---\n"
        "# 某某 2025：自评人格功能与抑郁相关\n\n> [!summary] 30 秒看懂\n> 一句话。\n\n"
        "## 为什么读这篇\n\n正文所报 χ²(1) = 3.96 与 p < .001 不匹配，需核原统计。\n\n"
        "## 研究怎么做\n\n**教学示例（非研究个案）**：甲乙两人。t 写成 \\(b/SE\\)。\n\n"
        "### 方法与解释补充\n\n这是相关。\n\n"
        "## 主要发现\n\n相关 r = .40。 ^f1\n\n## 我的评价\n\n需核的地方写在这里不算。\n\n"
        "## 对我的文章有什么用\n\n- 背景。\x0c\n"
    )
    p = kb / "文献" / "某某 2025.md"
    p.write_text(note, encoding="utf-8")
    row = cro.check_note(p, cro.Index(tmp_path, cro.SKIP_DIRS), cro.Pdfs(None), cro.D2_SECTIONS, False, [], [])
    assert "有收集限定句的小节：方法与解释补充" in row["问题"]
    assert "1 处教学示例标签不是" in row["问题"]
    assert "处公式用了" in row["问题"]
    assert "个控制字符" in row["问题"]
    assert row["讲解区内部用语"] == "需核×1"  # “我的评价”里的不算


def test_polynomial_terms_are_not_chinese_counts() -> None:
    assert not cro.CN_NUM.search("另试含三次项的模型")
    assert not cro.CN_NUM.search("取三次方")
    assert cro.CN_NUM.search("评估了三次")


def test_orphan_heading_and_math_patterns_do_not_flag_ordinary_text() -> None:
    assert not cro.ORPHAN_HEAD.search("发现6 补充分析")
    assert not cro.ORPHAN_HEAD.search("补充材料")
    assert not cro.BAD_MATH.search("文献 \\[1\\] 和 \\[2\\]")
    assert cro.BAD_MATH.search("\\[ \\frac{a}{b} \\]")
    assert not cro.CTRL.search("第一行\r\n第二行")


def test_full_method_card_needs_a_formula(tmp_path: Path) -> None:
    (tmp_path / "知识库" / "方法").mkdir(parents=True)
    card = tmp_path / "知识库" / "方法" / "线性回归.md"
    body = "## 是什么\n\n### 直观\n\n" + "回归把结果拆成预测部分和误差。" * 200 + "\n\n## 资料来源\n\n[1] 教材。\n"
    head = "---\n类型: 方法\n讲义: 完整\n---\n# 线性回归\n\n"
    card.write_text(head + body, encoding="utf-8")
    row = cro.check_card(card, cro.Index(tmp_path, cro.SKIP_DIRS), cro.Pdfs(None), cro.Counter(), [])
    assert "方法讲义没有公式" in row["问题"]
    card.write_text(head + body.replace("误差。", "误差：$y = b_0 + b_1 x + e$。", 1), encoding="utf-8")
    row = cro.check_card(card, cro.Index(tmp_path, cro.SKIP_DIRS), cro.Pdfs(None), cro.Counter(), [])
    assert "方法讲义没有公式" not in row["问题"]
