#!/usr/bin/env python3
"""中文综述草稿的文风自查。

按 references/review-writing-standard.md 第 5 节的目标值逐项判定，检查段落和句子的长短起伏、
句式和引用的分布，并列出禁用的过渡词和目录句。参照取自《心理科学进展》2024—2026 年 40 篇综述的逐篇统计：
- 全文指标：各篇数值的四分位范围（中间一半篇目所在的区间）；
- 长短起伏：取范例小节的第 10 百分位作提示线，低于它说明比九成范例小节都整齐。按小节而不按整篇算，
  因为单个小节本来就比整篇整齐；段落的切分受 PDF 版面影响，提示线取得更宽；
- 句式与引用：取范例小节的第 90（或第 10）百分位作提示线，只抓比九成范例小节都多（或都少）的写法，
  如句句“一项研究发现”、两两“X 与 Y 相关”。每段引用数按一区期刊综述小节的第 75 百分位提示（第 11.4 节）；
- 论证动作：数一数一区期刊综述常做的几件事（写出证据强弱、替代解释、标明本文的推论），
  全文一处都没有时提示。参照是 7 篇一区期刊叙述综述的逐段统计；
- 项数与穷尽说法：列出“至少 8 项研究”“只有 3 项”“尚无研究”“本文只找到”“唯一的研究”这类说法。
  非系统检索的叙述综述写这些，等于声称检索已经穷尽（第 11.3 节）；系统综述和元分析加 --systematic 跳过；
- 可能重复的句子：不同段落里说法高度重合的句子，用来查同一判断是否说了不止一次（第 11.8 节）。

统计前去掉 YAML 头、Obsidian 注释、标题行、表格行、表题、表注和括号里的引文。只读，不改文件。

用法：
    python scripts/check_review_prose.py 草稿.md [草稿2.md ...]
    python scripts/check_review_prose.py 草稿.md --json
    python scripts/check_review_prose.py 草稿.md --systematic   # 系统综述、元分析：不查项数
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

# 句式与引用：(提示线, "高"或"低", 范例参照, 越线时怎么改)。按范例小节的第 90（或第 10）百分位定线，
# 只在比九成范例小节都多（或都少）时提示。用词指标按去掉引文的正文算，引用指标按带引文的原文段落算。
PATTERN_TARGETS: dict[str, tuple[float, str, str, str]] = {
    "以“一项”开头的句子 %": (3, "高", "范例小节第 90 百分位 0%",
                       "“一项……研究发现”式开头太多：先写结论再引研究，或用“例如，……”“有研究……”、叙述引用"),
    "“越……越……”/万字": (7.3, "高", "范例小节中位数 0，第 90 百分位 7.3",
                      "“越……越……”太多：一节用一两次，其余直接写方向和强度"),
    "“一致”/万字": (17, "高", "范例小节中位数 0，第 90 百分位 17",
                 "“一致”太多：直接写结果的方向和大小，少用“与……一致”概括"),
    "“相关”/万字": (44, "高", "范例小节中位数 11，第 90 百分位 44",
                 "“X 与 Y 相关”太多：先写结论再挑代表研究，批量的系数放进表。"
                 "不要只换成“关系”“关联”，那只会让另一个词超标"),
    "“相关、关系、关联”合计/万字": (64, "高", "范例小节中位数 22，第 90 百分位 64",
                          "两两关系的陈述太多：合并成结论句，把逐项系数放进表"),
    "不引文献的段 %": (14, "低", "范例小节中位数 36%，第 10 百分位 14%",
                  "每段都引文献：提出问题、下判断、做过渡和总结的段可以不引，引用留给交代证据的段"),
    "每段引用数（中位数）": (4, "高", "范例小节中位数 1、第 90 百分位 2.5；一区综述小节中位数 2.5、第 75 百分位 4",
                    "每段引用比四分之三的一区综述小节还密：一个论点挑两三项代表研究，其余放进表或附表，也要顾及参考文献总数"),
}

# 论证动作：一区期刊综述常做、目标期刊范例少做的几件事。只数，不判错；全文一处都没有时提示。
MOVES: dict[str, tuple[str, str, str]] = {
    "写出证据强弱": (
        r"(?:较强|较弱|有限|初步|一致|充分|混合|直接)的(?:证据|支持)|证据(?:较为|比较|十分|仍|尚|还)?(?:充分|有限|不足|薄弱)"
        r"|方向(?:相同|一致|相反)|结果同向|初步(?:的)?支持",
        "一区综述每百段约 22 处（多半用研究项数表达），《心理科学进展》约 4 处",
        "没有交代证据有多强：用设计、信息源和结果是否一致来说，如“自评、访谈评定和临床组比较的结果方向相同”；"
        "非系统检索不写研究项数（第 11.3 节）"),
    "替代解释": (
        r"另一种(?:解释|可能)|替代(?:性)?解释|也可能(?:是|反映|来自|源于)|既可能[^。]{2,40}也可能",
        "一区综述每百段约 1 处，写得好的 4—5 处；《心理科学进展》几乎没有",
        "关键的发现可以写一种替代解释，并说明什么设计能分辨"),
    "标明本文的推论": (
        r"本文(?:认为|推测|提出|主张|据此)",
        "一区综述作者自称每百句约 8 次，《心理科学进展》约 2 次",
        ""),
}
# 项数与穷尽说法：非系统检索的叙述综述不写（第 11.3 节）。指代引到的研究（“上述两项研究”“这些研究”）不算。
NUM = r"(?:[0-9０-９]+|[一两二三四五六七八九十几]+)"
COUNT_CLAIMS: dict[str, str] = {
    "研究项数": r"(?:至少|只有|仅有|共有?|已有|本文(?:只|共)?找到)\s?" + NUM + r"\s?(?:项|篇)"
                r"|[0-9０-９]+\s?(?:项|篇)(?:研究|横断|纵向|前瞻|实验|追踪|报告)",
    "说没有研究": r"(?:尚无|还没有|没有|尚未有|很少有?|少有)(?:直接|专门|系统|任何)?的?(?:研究|证据)"
                 r"|本文(?:还)?没有找到|(?:研究|证据)(?:还|仍)?(?:很少|较少|很缺乏|缺乏)",
    "全称说法": r"唯一[^。，；]{0,15}研究|证据最多|无论(?:用|采用)?哪一?[类种]",
}
COUNT_ADVICE = ("非系统检索不报研究项数，也不说没有研究：只描述引到的研究（“这些研究”“上述两项研究”），"
                "缺口写成“这一问题需要……的研究来回答”（第 11.3 节）")
REFERRING = re.compile(r"(?:上述|这|该|此|前述|以上|上面)\s?$")
REPEAT_MIN_HAN = 15
REPEAT_LINE = 0.6

YEAR = r"(?:19|20)\d{2}[a-z]?"
CITE_GROUP = re.compile(r"[（(][^（）()]*?" + YEAR + r"[^（）()]*[)）]")
ONLY_YEAR = re.compile(r"[（(]\s*" + YEAR + r"\s*[)）]")
NARRATIVE = re.compile(r"(?:[A-Z][A-Za-zÀ-ÿ'\-]+(?: et al\.| 等人?| 和 [A-Z][A-Za-zÀ-ÿ'\-]+| & [A-Z][A-Za-zÀ-ÿ'\-]+)?"
                       r"|[一-鿿]{2,4}(?:等人?)?)\s?[（(]" + YEAR + r"[)）]")

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


def body_lines(raw: str) -> list[tuple[int, str]]:
    """正文行和行号：YAML 头、跨行的 %% 注释换成空行（行号不变），跳过标题、表格和引用块。"""
    def blank(m: re.Match) -> str:
        return "\n" * m.group(0).count("\n")

    raw = re.sub(r"\A---\n.*?\n---\n", blank, raw.replace("\r\n", "\n"), flags=re.S)
    raw = re.sub(r"%%.*?%%", blank, raw, flags=re.S)
    return [(n, line) for n, line in enumerate(raw.splitlines(), 1) if not re.match(r"^\s*(#|\||>)", line)]


def banned_hits(raw: str) -> list[tuple[int, str, str]]:
    hits = []
    for lineno, body in body_lines(raw):
        for phrase, advice in BANNED.items():
            if phrase in body:
                hits.append((lineno, phrase, advice))
    return hits


def count_claims(raw: str) -> list[dict]:
    """项数与穷尽说法。前面是“上述”“这”等指代词的（如“上述两项研究”），是在描述引到的研究，不算。"""
    hits = []
    for lineno, body in body_lines(raw):
        for kind, pattern in COUNT_CLAIMS.items():
            for m in re.finditer(pattern, body):
                if REFERRING.search(body[max(0, m.start() - 4):m.start()]):
                    continue
                hits.append({"行": lineno, "词": m.group(0), "类型": kind})
    return hits


def bigrams(s: str) -> set[str]:
    h = "".join(HAN.findall(s))
    return {h[i:i + 2] for i in range(len(h) - 1)}


def repeats(text: str, line: float = REPEAT_LINE) -> list[dict]:
    """不同段落里说法高度重合的句子。先去掉一成以上句子都有的高频双字（主题词），
    再看较短一句的双字有多少出现在另一句里；达到六成算可能重复。只是提示，要人看。"""
    items = [(pi, s, bigrams(s)) for pi, p in enumerate(paragraphs(text))
             for s in sentences(p) if han(s) >= REPEAT_MIN_HAN]
    df: dict[str, int] = {}
    for _, _, grams in items:
        for g in grams:
            df[g] = df.get(g, 0) + 1
    common = {g for g, n in df.items() if n > max(3, 0.1 * len(items))}
    hits = []
    for i, (pa, sa, ga) in enumerate(items):
        for pb, sb, gb in items[i + 1:]:
            a, b = ga - common, gb - common
            if pa == pb or min(len(a), len(b)) < 6:
                continue
            share = len(a & b) / min(len(a), len(b))
            if share >= line:
                hits.append({"段": [pa + 1, pb + 1], "重合": round(share, 2), "句一": sa, "句二": sb})
    return sorted(hits, key=lambda h: -h["重合"])


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


def raw_paragraphs(raw: str) -> list[str]:
    """带引文的正文段落：去掉 YAML 头、注释和代码块，跳过标题、表格、引用块、表题和表注。"""
    raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
    raw = re.sub(r"%%.*?%%", "", raw, flags=re.S)
    raw = re.sub(r"```.*?```", "", raw, flags=re.S)
    out = []
    for p in re.split(r"\n\s*\n", raw):
        p = p.strip().replace("*", "")
        if han(p) >= PARA_MIN_HAN and not re.match(r"^(#|\||>)", p) and not CAPTION.match(p):
            out.append(p)
    return out


def n_cites(p: str) -> int:
    """一段里引了几项文献：括号引用数年份，叙述引用“某某等人(年份)”各算一项。"""
    groups = [g for g in CITE_GROUP.findall(p) if not ONLY_YEAR.fullmatch(g)]
    return sum(len(re.findall(YEAR, g)) for g in groups) + len(NARRATIVE.findall(p))


def patterns(raw: str, text: str) -> dict[str, float]:
    sents = sentences(text)
    cites = [n_cites(p) for p in raw_paragraphs(raw)]
    return {
        "以“一项”开头的句子 %": 100 * sum(bool(re.match(r"^[^一-鿿]*一项", s)) for s in sents) / len(sents)
        if sents else 0.0,
        "“越……越……”/万字": per(text, r"越[^，。；]{1,14}越"),
        "“一致”/万字": per(text, "一致"),
        "“相关”/万字": per(text, "相关"),
        "“相关、关系、关联”合计/万字": per(text, "相关|关系|关联"),
        "不引文献的段 %": 100 * sum(c == 0 for c in cites) / len(cites) if cites else 0.0,
        "每段引用数（中位数）": median(cites),
        "_段落数": len(cites),
        "_句子数": len(sents),
    }


def judge_pattern(name: str, value: float, p: dict[str, float], n_han: int) -> tuple[str, str]:
    if name in ("不引文献的段 %", "每段引用数（中位数）"):
        enough = p["_段落数"] >= MIN_PARAS
    elif name.startswith("以"):
        enough = p["_句子数"] >= MIN_SENTS
    else:
        enough = n_han >= MIN_HAN
    if not enough:
        return "不判断", "段落、句子或字数太少"
    line, side, _, fix = PATTERN_TARGETS[name]
    over = value > line if side == "高" else value < line
    return ("偏多" if side == "高" else "偏少", fix) if over else ("在范围内", "")


def pattern_rows(p: dict[str, float], n_han: int) -> list[dict]:
    rows = []
    for name, (_, _, ref, _) in PATTERN_TARGETS.items():
        verdict, fix = judge_pattern(name, p[name], p, n_han)
        rows.append({"指标": name, "草稿": round(p[name], 1), "范例参照": ref, "判定": verdict, "怎么改": fix})
    return rows


def moves(text: str, n_paras: int) -> list[dict]:
    """数论证动作。按去掉引文的正文数；不足 6 段不判断。"""
    rows = []
    for name, (pattern, ref, fix) in MOVES.items():
        n = len(re.findall(pattern, text))
        if n_paras < MIN_PARAS:
            verdict, advice = "不判断", "段落太少"
        elif n == 0:
            verdict, advice = ("可以加上", fix) if fix else ("没有", "")
        else:
            verdict, advice = "有", ""
        rows.append({"动作": name, "草稿": n, "参照": ref, "判定": verdict, "怎么改": advice})
    return rows


def report(path: Path, systematic: bool = False) -> dict:
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = clean(raw)
    m = metrics(text)
    rows = []
    for name, value in m.items():
        verdict, fix = judge(name, value)
        low, high = TARGETS[name][:2]
        rows.append({"指标": name, "草稿": round(value, 1), "目标": f"{low:g}—{high:g}", "判定": verdict, "怎么改": fix})
    return {"文件": str(path), "汉字": han(text), "短稿": han(text) < MIN_HAN, "指标": rows,
            "长短起伏": spread_rows(spread(text)),
            "句式与引用": pattern_rows(patterns(raw, text), han(text)),
            "论证动作": moves(text, len(raw_paragraphs(raw))),
            "禁用词": [{"行": n, "词": p, "怎么改": a} for n, p, a in banned_hits(raw)],
            "项数与穷尽说法": None if systematic else count_claims(raw),
            "可能重复的句子": repeats(text)}


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
    out += ["", "句式与引用（只在比九成范例小节都多或都少时提示）：", "",
            "| 指标 | 草稿 | 范例参照 | 判定 | 怎么改 |", "|---|---|---|---|---|"]
    for row in r["句式与引用"]:
        out.append(f"| {row['指标']} | {row['草稿']} | {row['范例参照']} | {row['判定']} | {row['怎么改']} |")
    out += ["", "论证动作（一区期刊综述的做法，只数次数，全文一处都没有时提示）：", "",
            "| 动作 | 草稿（处） | 参照 | 判定 | 怎么改 |", "|---|---|---|---|---|"]
    for row in r["论证动作"]:
        out.append(f"| {row['动作']} | {row['草稿']} | {row['参照']} | {row['判定']} | {row['怎么改']} |")
    out.append("")
    if r["禁用词"]:
        out.append(f"禁用的过渡词和目录句 {len(r['禁用词'])} 处：")
        out += [f"- 第 {h['行']} 行“{h['词']}”：{h['怎么改']}" for h in r["禁用词"]]
    else:
        out.append("没有禁用的过渡词和目录句。")
    claims = r["项数与穷尽说法"]
    if claims is None:
        out.append("系统综述或元分析：没有查项数与穷尽说法。")
    elif claims:
        out.append(f"项数与穷尽说法 {len(claims)} 处（非系统检索的叙述综述不写）：")
        out += [f"- 第 {h['行']} 行“{h['词']}”（{h['类型']}）" for h in claims]
        out.append(f"  怎么改：{COUNT_ADVICE}")
    else:
        out.append("没有项数与穷尽说法。")
    reps = r["可能重复的句子"]
    if reps:
        out.append(f"可能重复的句子 {len(reps)} 对（不同段落里说法高度重合；同一判断全章只说一次，第 11.8 节）：")
        for h in reps[:12]:
            out.append(f"- 第 {h['段'][0]} 段与第 {h['段'][1]} 段（重合 {h['重合']}）：“{h['句一']}”／“{h['句二']}”")
    else:
        out.append("没有说法高度重合的句子。")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="中文综述草稿的文风自查")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--systematic", action="store_true", help="系统综述或元分析：不查项数与穷尽说法")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    results = [report(f, args.systematic) for f in args.files]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render(r) for r in results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
