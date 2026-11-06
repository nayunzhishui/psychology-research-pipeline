#!/usr/bin/env python3
"""中文综述草稿的文风自查。

按 references/review-writing-standard.md 第 5 节的目标值逐项判定，检查段落和句子的长短起伏，
并列出禁用的过渡词和目录句。参照取自《心理科学进展》2024—2026 年 40 篇综述的逐篇统计：
- 全文指标：各篇数值的四分位范围（中间一半篇目所在的区间）；
- 长短起伏：取范例小节的第 10 百分位作提示线，低于它说明比九成范例小节都整齐。按小节而不按整篇算，
  因为单个小节本来就比整篇整齐；段落的切分受 PDF 版面影响，提示线取得更宽。

统计前去掉 YAML 头、Obsidian 注释、标题行、表格行、表题、表注和括号里的引文。只读，不改文件。

用法：
    python scripts/check_review_prose.py 草稿.md [草稿2.md ...]
    python scripts/check_review_prose.py 草稿.md --json
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

HAN = re.compile(r"[一-鿿]")
MIN_HAN = 1500
MIN_PARAS = 6
MIN_SENTS = 20
PARA_MIN_HAN = 20
CONNECTIVE = re.compile(r"^(此外|同时|因此|从而|因而|然而|但是|但|尽管|虽然)")
CAPTION = re.compile(r"^(表|图)\s*[0-9０-９A-Za-zＸ]|^注[：:]")

# 指标：(目标下限, 目标上限, 偏低时怎么改, 偏高时怎么改)
TARGETS: dict[str, tuple[float, float, str, str]] = {
    "每句汉字（中位数）": (43, 52, "句子偏短：补回主语、样本、测法和比较对象，两到四个分句一句", "句子偏长：拆成两句"),
    "每个分句汉字（中位数）": (14, 17, "分句压缩成了名词堆：补回必要的修饰", "分句太长：在逻辑停顿处断开"),
    "“的”/百字": (3.9, 4.5, "电报体：还原完整的偏正结构", "“的”字堆叠：精简修饰语"),
    "分号/万字": (11, 26, "", "用分号串条目：改写成完整的句子，三项以上的并列放进表"),
    "冒号/万字": (10, 19, "", "标签句偏多：改成陈述句"),
    "以连接词开头的句子 %": (9, 14, "句间缺衔接：按逻辑关系补“此外、因此、然而、尽管”", "连接词偏多：删掉不承担逻辑关系的"),
    "“其”/万字": (20, 41, "指代偏口语：用“其”代替“它/它们”", ""),
    "“它/它们/他们”/万字": (0, 9, "", "改用“其”或重复名词"),
    "“进行”/万字": (12, 28, "可适度用“对……进行……”，不硬加", "“进行”偏多：直接用动词"),
    "英文术语括注/万字": (12, 29, "核心术语第一次出现时括注英文", ""),
    "缩写/万字": (0, 119, "", "缩写偏多：概念用中文，工具才用缩写"),
    "括号举例“(如……)”/万字": (2.5, 8.3, "简短的例子可放进括号“(如……)”", ""),
    "“均、皆、亦”/万字": (0, 13, "", "压缩体：少用“均”"),
    "口语词/万字": (0, 6, "", "删掉口语词，“比如”换成“例如”"),
    "“为……提供”/万字": (3.5, 9.4, "很少交代用处：段末或节末写清这组证据说明了什么", ""),
}

# 长短起伏：(提示线, 范例参照, 低于提示线时怎么改)。只有下限：太整齐才提示，不要求为错开而错开。
SPREAD_TARGETS: dict[str, tuple[float, str, str]] = {
    "段长变异系数": (0.35, "范例小节约 0.4—0.6，随切段口径而变",
                 "段落长短太整齐：只下判断、做过渡或交代例外的段写短，汇总多项研究的段写长；字数区间不是每段的目标"),
    "每段句数的极差": (2, "范例小节中位数 3—5",
                  "每段句数几乎一样：判断或过渡一两句即可，汇总证据的段可以五六句"),
    "句长变异系数": (0.38, "范例小节 0.48（四分位 0.42—0.55）",
                 "句子长短太整齐：交代设计、结果和比较的句子可以长到六七十字，判断和过渡句可以短"),
    "长于 60 字的句子 %": (14, "范例小节 29%（四分位 20%—39%）",
                     "长句太少：不必把长句都拆开，一句可以交代清楚样本、测法和结果"),
}

BANNED: dict[str, str] = {
    "值得注意的是": "删掉过渡词，直接说事（反防御写作第 20 条）",
    "需要指出的是": "删掉过渡词，直接说事（第 20 条）",
    "综上所述": "改为“综上”，并只用在章末小结（第 20 条）",
    "总的来说": "删掉，结尾落在具体判断上（第 20 条）",
    "本节将": "目录句：改写成这一节要回答的问题（第 19 条）",
    "本部分将": "目录句：改写成这一部分要回答的问题（第 19 条）",
    "下文将": "目录句：用上一段的结论引出下一段的问题（第 19 条）",
    "如前所述": "直接写内容（第 19 条）",
    "具有一定的": "说具体是什么、有多大",
    "有待进一步研究": "写成一项具体的研究：什么样本、什么设计、回答什么问题",
    "具有重要意义": "写具体的用处",
    "笔者": "用“本文”或“本研究”",
}


def clean(text: str) -> str:
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"%%.*?%%", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^\s*(#|\|).*$", "", text, flags=re.M)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\([^()]*?(?:19|20)\d{2}[a-z]?[^()]*\)", "", text)
    text = re.sub(r"（[^（）]*?(?:19|20)\d{2}[a-z]?[^（）]*）", "", text)
    text = text.replace("*", "")
    return re.sub(r"^\s*(?:(?:表|图)\s*[0-9０-９A-Za-zＸ]|注[：:]).*$", "", text, flags=re.M)


def han(s: str) -> int:
    return len(HAN.findall(s))


def per(text: str, pattern: str, unit: float = 10000) -> float:
    n = han(text)
    return len(re.findall(pattern, text)) / n * unit if n else 0.0


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def quartiles(values: list[float]) -> tuple[float, float]:
    if len(values) < 2:
        return (values[0], values[0]) if values else (0.0, 0.0)
    q = statistics.quantiles(values, n=4)
    return q[0], q[2]


def cv(values: list[float]) -> float:
    m = statistics.mean(values) if values else 0.0
    return statistics.pstdev(values) / m if m else 0.0


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[。？！?!]", text) if han(s) >= 6]


def paragraphs(text: str) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text)]
    return [p for p in paras if han(p) >= PARA_MIN_HAN and not CAPTION.match(p)]


def metrics(text: str) -> dict[str, float]:
    sents = sentences(text)
    clauses = [c for c in re.split(r"[。？！?!，,；;：:]", text) if han(c) >= 2]
    return {
        "每句汉字（中位数）": median([han(s) for s in sents]),
        "每个分句汉字（中位数）": median([han(c) for c in clauses]),
        "“的”/百字": per(text, "的", 100),
        "分号/万字": per(text, "[；;]"),
        "冒号/万字": per(text, "[：:]"),
        "以连接词开头的句子 %": 100 * sum(bool(CONNECTIVE.match(s)) for s in sents) / len(sents) if sents else 0.0,
        "“其”/万字": per(text, "其"),
        "“它/它们/他们”/万字": per(text, "它们|它|他们"),
        "“进行”/万字": per(text, "进行"),
        "英文术语括注/万字": per(text, r"[（(]\s*[A-Za-z][A-Za-z\- ]{3,}"),
        "缩写/万字": per(text, r"(?<![A-Za-z])[A-Z]{2,6}(?![A-Za-z])"),
        "括号举例“(如……)”/万字": per(text, r"[（(]\s*(?:如|例如)"),
        "“均、皆、亦”/万字": per(text, "均|皆|亦"),
        "口语词/万字": per(text, "其实|所以|就是|这个|那么|比如"),
        "“为……提供”/万字": per(text, r"为[^。，,]{1,30}提供"),
    }


def spread(text: str) -> dict[str, float]:
    """段落和句子的长短起伏。段落按空行切分，表题、表注和不足 20 字的行不算段落。"""
    paras = paragraphs(text)
    plen = [han(p) for p in paras]
    pnum = [len(sentences(p)) for p in paras]
    slen = [han(s) for s in sentences(text)]
    pq, sq = quartiles(plen), quartiles(slen)
    return {
        "段落数": len(paras),
        "段长中位数": median(plen),
        "段长下四分位": pq[0],
        "段长上四分位": pq[1],
        "段长变异系数": cv(plen),
        "短于 100 字的段 %": 100 * sum(x < 100 for x in plen) / len(plen) if plen else 0.0,
        "长于 190 字的段 %": 100 * sum(x > 190 for x in plen) / len(plen) if plen else 0.0,
        "每段最少句数": min(pnum) if pnum else 0,
        "每段最多句数": max(pnum) if pnum else 0,
        "每段句数的极差": (max(pnum) - min(pnum)) if pnum else 0,
        "句子数": len(slen),
        "句长下四分位": sq[0],
        "句长上四分位": sq[1],
        "句长变异系数": cv(slen),
        "长于 60 字的句子 %": 100 * sum(x > 60 for x in slen) / len(slen) if slen else 0.0,
    }


def banned_hits(raw: str) -> list[tuple[int, str, str]]:
    hits = []
    for lineno, line in enumerate(raw.splitlines(), 1):
        body = re.sub(r"%%.*?%%", "", line)
        for phrase, advice in BANNED.items():
            if phrase in body:
                hits.append((lineno, phrase, advice))
    return hits


def judge(name: str, value: float) -> tuple[str, str]:
    low, high, low_fix, high_fix = TARGETS[name]
    if value < low and low_fix:
        return "偏低", low_fix
    if value > high and high_fix:
        return "偏高", high_fix
    return "在范围内", ""


def judge_spread(name: str, value: float, s: dict[str, float]) -> tuple[str, str]:
    enough = s["段落数"] >= MIN_PARAS if name in ("段长变异系数", "每段句数的极差") else s["句子数"] >= MIN_SENTS
    if not enough:
        return "不判断", "段落或句子太少"
    line, _, fix = SPREAD_TARGETS[name]
    return ("太整齐", fix) if value < line else ("有起伏", "")


def spread_rows(s: dict[str, float]) -> list[dict]:
    def row(name, value, ref, verdict="", fix=""):
        return {"指标": name, "草稿": value, "范例参照": ref, "判定": verdict, "怎么改": fix}

    rows = [
        row("段落数", int(s["段落数"]), "范例小节中位数 9 段"),
        row("段长中位数（四分位）", f"{s['段长中位数']:.0f}（{s['段长下四分位']:.0f}—{s['段长上四分位']:.0f}）",
            "范例小节约 105—130；只算完整段落约 150"),
        row("短于 100 字的段", f"{s['短于 100 字的段 %']:.0f}%", "范例小节约 33%—50%"),
        row("长于 190 字的段", f"{s['长于 190 字的段 %']:.0f}%", "范例小节约 20%—33%"),
        row("每段句数", f"{s['每段最少句数']:.0f}—{s['每段最多句数']:.0f}", "每段中位数 3 句，多的到 8—10 句"),
        row("句长四分位", f"{s['句长下四分位']:.0f}—{s['句长上四分位']:.0f}", "整篇 35—68"),
    ]
    for name in SPREAD_TARGETS:
        verdict, fix = judge_spread(name, s[name], s)
        value = round(s[name], 2) if "变异系数" in name else round(s[name], 1)
        rows.append(row(name, value, SPREAD_TARGETS[name][1], verdict, fix))
    return rows


def report(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    text = clean(raw)
    m = metrics(text)
    rows = []
    for name, value in m.items():
        verdict, fix = judge(name, value)
        low, high = TARGETS[name][:2]
        rows.append({"指标": name, "草稿": round(value, 1), "目标": f"{low:g}—{high:g}", "判定": verdict, "怎么改": fix})
    return {"文件": str(path), "汉字": han(text), "短稿": han(text) < MIN_HAN, "指标": rows,
            "长短起伏": spread_rows(spread(text)),
            "禁用词": [{"行": n, "词": p, "怎么改": a} for n, p, a in banned_hits(raw)]}


def render(r: dict) -> str:
    out = [f"## {r['文件']}", f"正文汉字 {r['汉字']}（去掉引文、标题、表格、表题和表注）。"]
    if r["短稿"]:
        out.append(f"草稿不足 {MIN_HAN} 汉字，比例指标不稳定，主要看禁用词。")
    out += ["", "| 指标 | 草稿 | 目标（范例四分位） | 判定 | 怎么改 |", "|---|---|---|---|---|"]
    for row in r["指标"]:
        out.append(f"| {row['指标']} | {row['草稿']} | {row['目标']} | {row['判定']} | {row['怎么改']} |")
    out += ["", "长短起伏（只在比九成范例小节都整齐时提示）：", "",
            "| 指标 | 草稿 | 范例参照 | 判定 | 怎么改 |", "|---|---|---|---|---|"]
    for row in r["长短起伏"]:
        out.append(f"| {row['指标']} | {row['草稿']} | {row['范例参照']} | {row['判定']} | {row['怎么改']} |")
    out.append("")
    if r["禁用词"]:
        out.append(f"禁用的过渡词和目录句 {len(r['禁用词'])} 处：")
        out += [f"- 第 {h['行']} 行“{h['词']}”：{h['怎么改']}" for h in r["禁用词"]]
    else:
        out.append("没有禁用的过渡词和目录句。")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="中文综述草稿的文风自查")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    results = [report(f) for f in args.files]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render(r) for r in results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
