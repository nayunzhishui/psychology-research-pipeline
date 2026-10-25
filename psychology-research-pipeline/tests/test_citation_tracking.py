"""引文追踪脚本的回归测试：不联网，用假的 OpenAlex 返回值。"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import citation_tracking as ct  # noqa: E402

SKILLS = ("psychology-research-pipeline", "psych-literature-review-workflow", "psych-cog-neuro-review")


def work(wid: str, title: str, year: int, doi: str, refs: tuple[str, ...] = ()) -> dict:
    return {"id": f"https://openalex.org/{wid}", "doi": f"https://doi.org/{doi}", "title": title,
            "publication_year": year, "authorships": [{"author": {"display_name": "Ann Lee"}}],
            "primary_location": {"source": {"display_name": "J Test"}}, "ids": {}, "type": "article",
            "cited_by_count": 3, "abstract_inverted_index": {"world": [1], "hello": [0]},
            "referenced_works": [f"https://openalex.org/{r}" for r in refs]}


class FakeAPI:
    remaining = 500

    def __init__(self) -> None:
        self.db = {"W1": work("W1", "Seed paper", 2020, "10.1/seed", refs=("W2", "W3")),
                   "W2": work("W2", "Old reference", 2010, "10.1/old"),
                   "W3": work("W3", "New reference", 2015, "10.1/new")}

    def get(self, path: str, params: dict | None = None, costly: bool = False):
        if path.startswith("works/doi:"):
            return self.db["W1"]
        if path.startswith("works/W"):
            return self.db.get(path.split("/")[1])
        assert path == "works" and costly
        assert params["filter"] == "cites:W1"
        return {"meta": {"count": 1, "next_cursor": None}, "results": [work("W9", "Citing paper", 2024, "10.1/cite")]}


class BrokeAPI(FakeAPI):
    def get(self, path: str, params: dict | None = None, costly: bool = False):
        if costly:
            raise ct.OutOfCredit("额度用完")
        return super().get(path, params, costly)


def rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def make_files(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    seeds = tmp_path / "种子表.csv"
    seeds.write_text("候选编号,DOI,轮次\nCAND-1,10.1/seed,1\n", encoding="utf-8-sig")
    cands = tmp_path / "候选文献表.csv"
    cands.write_text("候选编号,题名,年份,DOI\nCAND-1,Seed paper,2020,10.1/seed\nCAND-2,Old reference,2010,10.1/OLD\n",
                     encoding="utf-8-sig")
    log = tmp_path / "检索日志.csv"
    log.write_text("检索编号,数据库,平台,检索式,限定条件,检索时间,命中数,导出文件,查重后新增,状态,备注\r\n", encoding="utf-8-sig")
    return seeds, cands, log, tmp_path / "导出"


def test_abstract_and_doi_are_normalized() -> None:
    assert ct.abstract({"world": [1], "hello": [0]}) == "hello world"
    assert ct.norm_doi("https://doi.org/10.1/ABC") == "10.1/abc"
    assert ct.search_id("B", "CAND-1", "2") == "CIT-B-CAND-1-r2"
    assert ct.search_id("F", "CAND-1", "1") == "CIT-F-CAND-1"


def test_tracking_marks_seen_logs_and_fills_a_chinese_seed_table(tmp_path: Path) -> None:
    seeds, cands, log, out = make_files(tmp_path)
    argv = ["--种子表", str(seeds), "--输出目录", str(out), "--候选表", str(cands), "--检索记录", str(log)]
    assert ct.main(argv, api=FakeAPI()) == 0
    new = rows(next(out.glob("引文追踪新增_*.csv")))
    assert {r["doi"] for r in new} == {"10.1/new", "10.1/cite"}  # 10.1/old 已在候选表里，大小写不同也认得出
    logged = rows(log)
    assert [r["检索编号"] for r in logged] == ["CIT-B-CAND-1", "CIT-F-CAND-1"]
    assert logged[0]["数据库"] == "引文追踪（后向）" and logged[0]["命中数"] == "2" and logged[0]["查重后新增"] == "1"
    seed = rows(seeds)[0]
    assert seed["后向状态"] == "已做" and seed["前向状态"] == "已做" and seed["OpenAlex编号"] == "W1"
    assert len(list(out.glob("CIT-*.json"))) == 2
    # 再跑一次：两个方向都追过了，不重复登记
    assert ct.main(argv, api=FakeAPI()) == 0
    assert len(rows(log)) == 2


def test_running_out_of_credit_marks_the_rest_pending(tmp_path: Path) -> None:
    seeds, _, _, out = make_files(tmp_path)
    assert ct.main(["--种子表", str(seeds), "--输出目录", str(out)], api=BrokeAPI()) == 2
    seed = rows(seeds)[0]
    assert seed["后向状态"] == "已做"  # 后向按 ID 取单篇，不花额度
    assert seed["前向状态"] == "待续"


def test_script_and_templates_are_shared_by_all_three_skills() -> None:
    root = SCRIPTS.parents[1]
    texts = [(root / s / "scripts" / "citation_tracking.py").read_text(encoding="utf-8") for s in SKILLS]
    assert texts[0] == texts[1] == texts[2]
    for s in SKILLS:
        for name in ("引文追踪种子表模板_citation_seeds.csv", "结构改良记录模板_structure_findings.csv"):
            assert (root / s / "templates" / name).exists(), (s, name)
