#!/usr/bin/env python3
"""对核心文献做后向和前向引文追踪：从 OpenAlex 取参考文献和施引文献，导出成候选题录，登记检索记录和种子表。

规则见 references/literature-operations-contract.md 4.1。后向是种子引用了谁：先取种子的参考文献列表，再逐条按 ID
取题录和摘要（按 ID 取单篇不花额度）。前向是谁引用了种子：用 cites 过滤分页取，每页 200 条，花 1 个额度。

用法：
  python citation_tracking.py --种子表 引文追踪种子表.csv --输出目录 <原始导出目录>
      [--候选表 候选文献表.csv] [--检索记录 检索记录.csv] [--方向 双向|后向|前向] [--只追 <候选编号>]... [--重追]
  不用种子表时直接给 DOI（可重复）：--doi 10.1080/00223891.2024.2365325 --编号 CAND-0263

种子表的列见 templates/引文追踪种子表模板_citation_seeds.csv，也认中文表头（候选编号、DOI、轮次、前向限定词……）。
默认只追还没追过的方向，--重追 时全部重来。种子的 forward_terms（前向限定词）不为空时，前向只取题名或摘要里有
这些词的施引文献，适合被引上千次的经典文献。

输出都在 --输出目录：
  - 每个种子每个方向一份原始 JSON，只写新文件，不覆盖旧的；
  - 引文追踪结果_<时间>.csv：全部结果，标出是否已在候选表里；
  - 引文追踪新增_<时间>.csv：候选表里没有的，同一篇被几个种子追到时合成一行、排在前面，供筛选和导入候选表。
给了 --检索记录 时每个种子每个方向追加一行（也认中文表头：检索编号、命中数、查重后新增……）；给了 --种子表 时回填追踪状态。

额度：OpenAlex 匿名调用按网络出口每天有额度。剩余额度不高于 --保留额度（默认 20）时停下，已完成的照常写出，
没做完的方向在种子表里标“待续”，下次接着跑；这时退出码是 2。有 API key 的放在环境变量 OPENALEX_API_KEY 里，
脚本不把它写进任何文件，也不发送邮箱或其他个人信息。种子没有 DOI 也没有 OpenAlex 编号的标“缺标识”，
改用 PDF 参考文献表人工追踪。
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openalex.org"
UA = "psych-skill-citation-tracking/1.0"
SELECT = ("id,doi,title,display_name,publication_year,authorships,primary_location,ids,type,cited_by_count,"
          "is_retracted,abstract_inverted_index")
# 同一含义的列可能用英文键名（本 skill 的模板）或中文表头（项目自己的表），按顺序找第一个存在的
COLS = {
    "candidate_id": ("candidate_id", "候选编号", "种子编号"),
    "doi": ("doi", "DOI"),
    "pmid": ("pmid", "PMID"),
    "openalex_id": ("openalex_id", "OpenAlex编号", "OpenAlex"),
    "title": ("title", "题名", "标题"),
    "year": ("year", "年份"),
    "round": ("round", "轮次"),
    "forward_terms": ("forward_terms", "前向限定词"),
}
SEED_OUT = {  # 回填种子表的列：英文键名，中文表头
    "openalex_id": ("openalex_id", "OpenAlex编号"),
    "B_status": ("backward_status", "后向状态"),
    "B_search_id": ("backward_search_id", "后向检索编号"),
    "B_count": ("backward_count", "后向条数"),
    "B_new": ("backward_new", "后向新增"),
    "F_status": ("forward_status", "前向状态"),
    "F_search_id": ("forward_search_id", "前向检索编号"),
    "F_index": ("forward_index", "前向索引"),
    "F_count": ("forward_count", "前向条数"),
    "F_new": ("forward_new", "前向新增"),
    "tracked_at": ("tracked_at", "追踪日期"),
}
LOG = {  # 检索记录的列
    "search_id": ("search_id", "检索编号"),
    "database": ("database", "数据库"),
    "platform": ("platform", "平台"),
    "query": ("query", "检索式"),
    "filters": ("filters", "限定条件"),
    "run_at": ("run_at", "检索时间", "执行时间"),
    "result_count": ("result_count", "命中数", "结果数"),
    "export_file": ("export_file", "导出文件"),
    "new_after_dedup": ("new_after_dedup", "查重后新增"),
    "status": ("status", "状态"),
    "notes": ("notes", "备注"),
}
LOG_HEADER = ["search_id", "database", "platform", "query", "filters", "run_at", "result_count", "export_file", "notes"]
DIRECTIONS = {"双向": ("B", "F"), "后向": ("B",), "前向": ("F",)}
WORD = {"B": "后向", "F": "前向"}
RESULT_COLS = ["search_id", "direction", "seed_candidate_id", "openalex_id", "doi", "pmid", "title", "first_author",
               "authors", "year", "journal", "type", "cited_by_count", "is_retracted", "already_seen",
               "seen_candidate_id", "abstract"]
NEW_COLS = ["seed_hits", "search_ids", "seed_candidate_ids", "openalex_id", "doi", "pmid", "title", "first_author",
            "authors", "year", "journal", "type", "cited_by_count", "is_retracted", "abstract"]


class OutOfCredit(Exception):
    """OpenAlex 今天的额度快用完了，或已经用完。"""


def pick(row: dict, key: str) -> str:
    for name in COLS[key]:
        value = str(row.get(name) or "").strip()
        if value:
            return value
    return ""


def column(fields: list[str], names: tuple[str, ...]) -> str | None:
    return next((n for n in names if n in fields), None)


def norm_doi(value: str) -> str:
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", (value or "").strip().lower())


def short_id(value: str) -> str:
    return (value or "").strip().rstrip("/").rsplit("/", 1)[-1]


def norm_title(value: str) -> str:
    return re.sub(r"[\W_]+", "", (value or "").lower())[:80]


def abstract(inverted: dict | None) -> str:
    """OpenAlex 的摘要是“词 → 位置”的倒排索引，按位置拼回原文。"""
    if not inverted:
        return ""
    words = {pos: word for word, positions in inverted.items() for pos in positions}
    return " ".join(words[i] for i in sorted(words))


def identities(rec: dict) -> list[str]:
    """查重用的身份，顺序同文献操作合同：DOI → PMID 等稳定编号 → 规范题名 + 年份。"""
    out = []
    doi = norm_doi(str(rec.get("doi") or ""))
    if doi:
        out.append("doi:" + doi)
    pmid = short_id(str(rec.get("pmid") or ""))
    if pmid:
        out.append("pmid:" + pmid)
    oid = short_id(str(rec.get("openalex_id") or "")).upper()
    if oid:
        out.append("openalex:" + oid)
    year = re.search(r"\d{4}", str(rec.get("year") or ""))
    title = norm_title(str(rec.get("title") or ""))
    if title and year:
        out.append(f"meta:{title}|{year.group()}")
    return out


class OpenAlex:
    def __init__(self, reserve: int = 20, pause: float = 0.15):
        self.key = os.environ.get("OPENALEX_API_KEY", "").strip()
        self.reserve, self.pause = reserve, pause
        self.remaining: int | None = None

    def get(self, path: str, params: dict | None = None, costly: bool = False):
        if costly and self.remaining is not None and self.remaining <= self.reserve:
            raise OutOfCredit(f"剩余额度 {self.remaining}，不高于保留额度 {self.reserve}")
        query = dict(params or {})
        if self.key:
            query["api_key"] = self.key
        url = f"{API}/{path}" + ("?" + urllib.parse.urlencode(query) if query else "")
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=40) as resp:
                    left = resp.headers.get("X-RateLimit-Remaining", "")
                    if left.isdigit():
                        self.remaining = int(left)
                    data = json.load(resp)
                time.sleep(self.pause)
                return data
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    return None
                wait = (exc.headers.get("Retry-After", "") if exc.headers else "") or ""
                if exc.code == 429:
                    if wait.isdigit() and int(wait) <= 60 and attempt < 3:
                        time.sleep(int(wait) + 1)
                        continue
                    raise OutOfCredit("OpenAlex 返回 429：今天的额度用完了，或请求太快") from None
                if exc.code >= 500 and attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"OpenAlex 返回 HTTP {exc.code}") from None  # 不带网址，免得把 key 打出来
            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"连不上 OpenAlex：{getattr(exc, 'reason', exc)}") from None
        return None


def resolve(api, seed: dict) -> dict | None:
    fields = SELECT + ",referenced_works"
    oid, doi = short_id(pick(seed, "openalex_id")), norm_doi(pick(seed, "doi"))
    if oid:
        return api.get(f"works/{oid}", {"select": fields})
    if doi:
        return api.get(f"works/doi:{urllib.parse.quote(doi, safe='/:;()')}", {"select": fields})
    return None


def backward(api, work: dict) -> tuple[list[dict], int, str]:
    refs = [short_id(r) for r in work.get("referenced_works") or []]
    found, missed = [], 0
    for ref in refs:
        try:
            got = api.get(f"works/{ref}", {"select": SELECT})
        except RuntimeError:  # 个别条目取不到就跳过，记下条数；额度用完（OutOfCredit）照常往上抛
            got = None
        if got:
            found.append(got)
        else:
            missed += 1
    note = "种子在 OpenAlex 的参考文献列表（referenced_works），逐条取题录和摘要"
    return found, len(refs), note + (f"；{missed} 条没取到" if missed else "")


def forward(api, work: dict, terms: str, limit: int) -> tuple[list[dict], int, str]:
    flt = f"cites:{short_id(work['id'])}"
    if terms:
        flt += ",title_and_abstract.search:" + terms.replace(",", " ")
    found, cursor, total = [], "*", 0
    while cursor and len(found) < limit:
        page = api.get("works", {"filter": flt, "per-page": 200, "cursor": cursor, "select": SELECT}, costly=True)
        if not page:
            break
        meta = page.get("meta") or {}
        total = meta.get("count") or total
        found += page.get("results") or []
        cursor = meta.get("next_cursor")
    note = f"filter={flt}" + (f"；只取前 {limit} 条" if total > limit else "")
    return found[:limit], total, note


def record(work: dict) -> dict:
    authors = [((a.get("author") or {}).get("display_name") or "") for a in work.get("authorships") or []]
    source = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    return {
        "openalex_id": short_id(work.get("id") or ""),
        "doi": norm_doi(work.get("doi") or ""),
        "pmid": short_id(str((work.get("ids") or {}).get("pmid") or "")),
        "title": work.get("title") or work.get("display_name") or "",
        "first_author": authors[0] if authors else "",
        "authors": "; ".join(a for a in authors if a),
        "year": work.get("publication_year") or "",
        "journal": source,
        "type": work.get("type") or "",
        "cited_by_count": work.get("cited_by_count", ""),
        "is_retracted": "是" if work.get("is_retracted") else "",
        "abstract": abstract(work.get("abstract_inverted_index")),
    }


def load_seen(path: str | None) -> dict[str, str]:
    seen: dict[str, str] = {}
    if path:
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                rec = {k: pick(row, k) for k in ("doi", "pmid", "openalex_id", "title", "year")}
                for key in identities(rec):
                    seen.setdefault(key, pick(row, "candidate_id") or "已见")
    return seen


def search_id(direction: str, cid: str, rnd: str) -> str:
    return f"CIT-{direction}-{cid}" + (f"-r{rnd}" if rnd not in ("", "1") else "")


def new_path(folder: Path, stem: str, suffix: str) -> Path:
    path, n = folder / f"{stem}{suffix}", 1
    while path.exists():
        n += 1
        path = folder / f"{stem}_{n}{suffix}"
    return path


def write_csv(path: Path, cols: list[str], rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def append_log(path: Path, entries: list[dict]) -> None:
    if not entries:
        return
    exists = path.exists() and path.stat().st_size > 0
    if exists:
        with open(path, encoding="utf-8-sig", newline="") as f:
            fields = next(csv.reader(f))
        if not path.read_bytes().endswith(b"\n"):
            with open(path, "ab") as f:
                f.write(b"\r\n")
    else:
        fields = LOG_HEADER
    with open(path, "a" if exists else "w", encoding="utf-8" if exists else "utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(fields)
        for entry in entries:
            row = {column(fields, LOG[k]): v for k, v in entry.items() if column(fields, LOG[k])}
            w.writerow([row.get(c, "") for c in fields])


def set_seed(row: dict, fields: list[str], key: str, value) -> None:
    names = SEED_OUT[key]
    name = column(fields, names)
    if name is None:
        name = names[0] if "candidate_id" in fields else names[1]
        fields.append(name)
    row[name] = value


def seed_status(row: dict, fields: list[str], direction: str) -> str:
    name = column(fields, SEED_OUT[f"{direction}_status"])
    return str(row.get(name) or "").strip() if name else ""


def main(argv: list[str] | None = None, api=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--种子表", "--seeds", dest="seeds")
    ap.add_argument("--doi", action="append", default=[])
    ap.add_argument("--编号", "--id", dest="ids", action="append", default=[])
    ap.add_argument("--输出目录", "--outdir", dest="outdir", required=True)
    ap.add_argument("--候选表", "--candidates", dest="candidates")
    ap.add_argument("--检索记录", "--search-log", dest="log")
    ap.add_argument("--方向", "--direction", dest="direction", choices=tuple(DIRECTIONS), default="双向")
    ap.add_argument("--只追", "--only", dest="only", action="append", default=[])
    ap.add_argument("--重追", "--again", dest="again", action="store_true")
    ap.add_argument("--前向上限", "--forward-limit", dest="limit", type=int, default=2000)
    ap.add_argument("--保留额度", "--reserve", dest="reserve", type=int, default=20)
    args = ap.parse_args(argv)
    if not args.seeds and not args.doi:
        ap.error("要给 --种子表，或者至少一个 --doi")

    fields: list[str] = []
    if args.seeds:
        with open(args.seeds, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fields, seeds = list(reader.fieldnames or []), list(reader)
    else:
        seeds = [{"candidate_id": (args.ids[i] if i < len(args.ids) else f"DOI-{i + 1}"), "doi": d}
                 for i, d in enumerate(args.doi)]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    api = api or OpenAlex(args.reserve)
    seen = load_seen(args.candidates)
    now = datetime.datetime.now()
    stamp = now.strftime("%Y%m%d%H%M")
    results, log_rows, lines = [], [], []
    tally = {"已做": 0, "待续": 0, "失败": 0, "缺标识": 0}
    stopped = ""

    for seed in seeds:
        cid = pick(seed, "candidate_id") or pick(seed, "doi")
        if args.only and cid not in args.only:
            continue
        todo = [d for d in DIRECTIONS[args.direction] if args.again or seed_status(seed, fields, d) != "已做"]
        if not todo:
            continue
        if stopped:
            for d in todo:
                set_seed(seed, fields, f"{d}_status", "待续")
                tally["待续"] += 1
            continue
        try:
            work = resolve(api, seed)
        except OutOfCredit as exc:
            stopped = str(exc)
            work = None
        except RuntimeError as exc:
            for d in todo:
                set_seed(seed, fields, f"{d}_status", f"失败：{exc}")
                tally["失败"] += 1
            continue
        if work is None:
            reason = "待续" if stopped else ("缺标识" if not (pick(seed, "doi") or pick(seed, "openalex_id"))
                                             else "失败：OpenAlex 里找不到这篇")
            for d in todo:
                set_seed(seed, fields, f"{d}_status", reason)
                tally["待续" if stopped else ("缺标识" if reason == "缺标识" else "失败")] += 1
            continue
        if fields or args.seeds:
            set_seed(seed, fields, "openalex_id", short_id(work["id"]))
        rnd = pick(seed, "round")
        title = work.get("title") or work.get("display_name") or ""
        summary = []
        for d in todo:
            sid = search_id(d, cid, rnd)
            try:
                if d == "B":
                    works, count, flt = backward(api, work)
                else:
                    works, count, flt = forward(api, work, pick(seed, "forward_terms"), args.limit)
            except OutOfCredit as exc:
                stopped = str(exc)
                set_seed(seed, fields, f"{d}_status", "待续")
                tally["待续"] += 1
                continue
            except RuntimeError as exc:
                set_seed(seed, fields, f"{d}_status", f"失败：{exc}")
                tally["失败"] += 1
                continue
            raw = new_path(outdir, f"{sid}_{now:%Y%m%d%H%M%S}", ".json")
            raw.write_text(json.dumps({
                "seed_candidate_id": cid, "seed_openalex_id": short_id(work["id"]), "seed_doi": norm_doi(work.get("doi") or ""),
                "direction": WORD[d], "index": "OpenAlex", "filter": flt, "run_at": now.isoformat(timespec="seconds"),
                "count_reported": count, "results": works}, ensure_ascii=False, indent=1), encoding="utf-8")
            rows = []
            for w in works:
                rec = record(w)
                hit = next((seen[k] for k in identities(rec) if k in seen), "")
                rows.append({"search_id": sid, "direction": WORD[d], "seed_candidate_id": cid, **rec,
                             "already_seen": "是" if hit else "", "seen_candidate_id": hit})
            new = sum(1 for r in rows if not r["already_seen"])
            results += rows
            reported = (f"OpenAlex 记录参考文献 {count} 条，取到 {len(works)} 条" if d == "B"
                        else f"OpenAlex 报告施引文献 {count} 条，取到 {len(works)} 条")
            log_rows.append({"search_id": sid, "database": f"引文追踪（{WORD[d]}）",
                             "platform": "OpenAlex API（citation_tracking.py）",
                             "query": f"种子 {cid}：{title}；DOI {norm_doi(work.get('doi') or '') or '无'}",
                             "filters": flt, "run_at": now.strftime("%Y-%m-%d %H:%M"), "result_count": len(works),
                             "export_file": str(raw.resolve()), "new_after_dedup": new, "status": "已完成",
                             "notes": f"{reported}；与候选表比对新增 {new} 条"})
            for key, value in (("status", "已做"), ("search_id", sid), ("count", len(works)), ("new", new)):
                set_seed(seed, fields, f"{d}_{key}", value)
            if d == "F":
                set_seed(seed, fields, "F_index", "OpenAlex")
            set_seed(seed, fields, "tracked_at", now.strftime("%Y-%m-%d"))
            tally["已做"] += 1
            summary.append(f"{WORD[d]} {len(works)} 条（新增 {new}）")
        if summary:
            lines.append(f"  {cid} " + "，".join(summary))

    merged: dict[str, dict] = {}
    for r in results:
        if r["already_seen"]:
            continue
        key = (identities(r) or [r["openalex_id"]])[0]
        m = merged.setdefault(key, {**{c: r.get(c, "") for c in NEW_COLS}, "_ids": [], "_seeds": []})
        m["_ids"].append(r["search_id"])
        if r["seed_candidate_id"] not in m["_seeds"]:
            m["_seeds"].append(r["seed_candidate_id"])
    new_rows = []
    for m in merged.values():
        m["search_ids"], m["seed_candidate_ids"] = "；".join(m.pop("_ids")), "；".join(m["_seeds"])
        m["seed_hits"] = len(m.pop("_seeds"))
        new_rows.append(m)
    new_rows.sort(key=lambda r: (-r["seed_hits"], -int(r["year"] or 0)))

    if results:
        all_path = new_path(outdir, f"引文追踪结果_{stamp}", ".csv")
        new_csv = new_path(outdir, f"引文追踪新增_{stamp}", ".csv")
        write_csv(all_path, RESULT_COLS, results)
        write_csv(new_csv, NEW_COLS, new_rows)
    if args.log:
        append_log(Path(args.log), log_rows)
    if args.seeds:
        with open(args.seeds, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(seeds)

    print(f"完成 {tally['已做']} 个方向；待续 {tally['待续']}，失败 {tally['失败']}，缺标识 {tally['缺标识']}")
    print("\n".join(lines) if lines else "  没有要追的种子（都已追过；要重来加 --重追）")
    if results:
        print(f"全部结果：{all_path}")
        print(f"候选表里没有的：{new_csv}（{len(new_rows)} 条，被几个种子同时追到的排在前面）")
    if getattr(api, "remaining", None) is not None:
        print(f"OpenAlex 剩余额度：{api.remaining}")
    if stopped:
        print(f"中途停下：{stopped}。没做完的已标“待续”，额度恢复后再运行一次。")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
