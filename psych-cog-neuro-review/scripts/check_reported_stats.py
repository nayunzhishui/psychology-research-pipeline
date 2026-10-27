#!/usr/bin/env python3
"""验算论文报告的统计量：用原文给的数重算，看和报告的是否对得上。

页码核对只能说明数字抄对了，这个脚本看的是原文自己算不算得通（reading-note-style.md 6.1）。
报告值都经过四舍五入：脚本按每个数的小数位数算出舍入范围，差别落在范围里的算“相符”。
只用标准库；p 值按正态、t、χ²、F 分布精确计算，四格表另算费舍尔精确检验。

数值照原文写，保留原来的小数位数（写 1.0 不写 1）；p 可以写成 "<.001"。用法：
  python check_reported_stats.py 系数 --估计 -.26 --标准误 .47 --自由度 83 --报告t -5.5 --报告p "<.001"
  python check_reported_stats.py 区间 --估计 2.21 --下限 1.0 --上限 4.7 --比值 --报告p .42
  python check_reported_stats.py 卡方 --值 3.96 --自由度 1 --报告p "<.001"
  python check_reported_stats.py F --值 14.90 --自由度 5 --分母自由度 198 --报告p "<.001"
  python check_reported_stats.py 四格 7 9 2 18 --报告卡方 4.47      （第一组有、无，第二组有、无）
  python check_reported_stats.py 两组 --均值 3.88 4.75 --标准差 1.10 0.92 --人数 20 25 --报告t 2.90
  python check_reported_stats.py 相关 --r .32 --人数 115 --报告p .001
  python check_reported_stats.py 比例 --分子 25 --分母 40 --报告 62.5
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys


# ---------- 分布 ----------

def _betacf(a: float, b: float, x: float) -> float:
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 500):
        m2 = 2 * m
        for aa in (m * (b - m) * x / ((qam + m2) * (a + m2)), -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))):
            d = 1.0 + aa * d
            d = 1.0 / (d if abs(d) > tiny else tiny)
            c = 1.0 + aa / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
        if abs(d * c - 1.0) < 1e-15:
            break
    return h


def betai(a: float, b: float, x: float) -> float:
    """正则化不完全贝塔函数 I_x(a, b)。"""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def gammaq(a: float, x: float) -> float:
    """正则化上不完全伽马函数 Q(a, x)。"""
    if x <= 0:
        return 1.0
    log_front = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1:
        ap, total, term = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1
            term *= x / ap
            total += term
            if abs(term) < abs(total) * 1e-16:
                break
        return max(0.0, 1.0 - total * math.exp(log_front))
    tiny = 1e-300
    b = x + 1 - a
    c, d = 1.0 / tiny, 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = b + an / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        if abs(d * c - 1.0) < 1e-16:
            break
    return math.exp(log_front) * h


def p_z(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


def p_t(t: float, df: float | None) -> float:
    if df is None:
        return p_z(t)
    return betai(df / 2, 0.5, df / (df + t * t))


def p_chi2(x: float, df: float) -> float:
    return gammaq(df / 2, x / 2)


def p_f(f: float, df1: float, df2: float) -> float:
    if f <= 0:
        return 1.0
    return betai(df2 / 2, df1 / 2, df2 / (df2 + df1 * f))


def z_crit(level: float) -> float:
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p_z(mid) > 1 - level:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2

    def logp(x: int) -> float:
        return (math.lgamma(r1 + 1) - math.lgamma(x + 1) - math.lgamma(r1 - x + 1)
                + math.lgamma(r2 + 1) - math.lgamma(c1 - x + 1) - math.lgamma(r2 - c1 + x + 1)
                - math.lgamma(n + 1) + math.lgamma(c1 + 1) + math.lgamma(n - c1 + 1))
    observed = logp(a)
    total = sum(math.exp(logp(x)) for x in range(max(0, c1 - r2), min(r1, c1) + 1)
                if logp(x) <= observed + 1e-7)
    return min(1.0, total)


# ---------- 读数和舍入 ----------

def num(s: str) -> float:
    return float(str(s).strip().replace("−", "-").replace("–", "-").replace("＋", "+"))


def half(s: str) -> float:
    """报告值的舍入半宽：.47 → .005，1.0 → .05，12 → .5。"""
    s = str(s).strip().lstrip("<>=≤≥ ")
    return 0.5 * 10 ** -len(s.split(".")[1]) if "." in s else 0.5


def around(s: str) -> tuple[float, float]:
    v, h = num(s), half(s)
    return v - h, v + h


def parse_p(s: str) -> tuple[str, float, float]:
    s = str(s).strip().lower().replace("p", "").replace(" ", "")
    op = "="
    if s[:1] in "<≤":
        op, s = "<", s[1:]
    elif s[:1] in ">≥":
        op, s = ">", s[1:]
    s = s.lstrip("=")
    return op, num(s), half(s)


def corners(f, *intervals):
    vals = [f(*xs) for xs in itertools.product(*intervals)]
    return min(vals), max(vals)


def fmt(x: float, digits: int = 3) -> str:
    s = f"{x:.{digits}f}"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) and abs(x) < 1 else s


def fmt_p(p: float) -> str:
    """p 不到 .001 时给两位有效数字，验算时要看到具体大小（如原文写 .0002）。"""
    if p >= 0.001:
        return fmt(p)
    if p < 1e-6:
        return "< .000001"
    digits = -math.floor(math.log10(p)) + 1  # 两位有效数字需要的小数位数
    return f"{p:.{digits}f}".replace("0.", ".", 1)


def p_eq(p: float) -> str:
    return f"p < .001（约 {fmt_p(p)}）" if p < 0.001 else f"p = {fmt(p)}"


class Report:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.bad = 0

    def say(self, s: str) -> None:
        self.lines.append(s)

    def value(self, name: str, lo: float, hi: float, reported: str | None, absolute: bool = False) -> None:
        if reported is None:
            return
        r = num(reported)
        if absolute:
            r = abs(r)
            lo, hi = (min(abs(lo), abs(hi)), max(abs(lo), abs(hi))) if lo * hi > 0 else (0.0, max(abs(lo), abs(hi)))
        h = half(reported)
        ok = lo <= r + h and r - h <= hi
        msg = f"报告的 {name} = {reported}：" + ("相符" if ok else "不相符")
        mid = (lo + hi) / 2
        if not ok and mid and r:
            ratio = abs(r / mid)
            if 8.5 < ratio < 11.5 or 8.5 < 1 / ratio < 11.5:
                msg += "（相差约 10 倍，像是小数点错位或少了一个 0）"
            elif r * mid < 0:
                msg += "（符号相反）"
        self.bad += not ok
        self.say(msg)

    def p(self, lo: float, hi: float, reported: str | None) -> None:
        if reported is None:
            return
        op, v, h = parse_p(reported)
        if op == "<":
            ok = lo < v
        elif op == ">":
            ok = hi > v
        else:
            ok = lo <= v + h and v - h <= hi
        shown = ("p " + op + " " if op != "=" else "p = ") + reported.strip().lstrip("pP<>=≤≥ ")
        span = f"约为 {fmt_p(lo)}" if fmt_p(lo) == fmt_p(hi) else f"在 {fmt_p(lo)} 到 {fmt_p(hi)} 之间"
        msg = f"报告的 {shown}：" + ("相符" if ok else f"不相符（按报告的数算，p {span}）")
        mid = (lo + hi) / 2
        if not ok and op == "=" and mid > 0 and (8.5 < v / mid < 11.5 or 8.5 < mid / v < 11.5):
            msg += "；相差约 10 倍，像是少了或多了一个 0"
        self.bad += not ok
        self.say(msg)

    def done(self) -> str:
        self.say("结论：" + ("报告的数彼此相符" if not self.bad else f"有 {self.bad} 处不相符，写进笔记时写明怎么算的"))
        return "\n".join(self.lines)


def p_span(stat_lo: float, stat_hi: float, pfun) -> tuple[float, float]:
    """统计量有舍入范围时，p 的范围（p 随 |统计量| 增大而减小）。"""
    if stat_lo <= 0 <= stat_hi:
        return pfun(max(abs(stat_lo), abs(stat_hi))), 1.0
    a, b = sorted((abs(stat_lo), abs(stat_hi)))
    return pfun(b), pfun(a)


# ---------- 各种验算 ----------

def coef(a) -> str:
    rep = Report()
    df = int(a.df) if a.df else None
    t = num(a.est) / num(a.se)
    lo, hi = corners(lambda b, s: b / s, around(a.est), [max(x, 1e-12) for x in around(a.se)])
    name = "t" if df else "z"
    rep.say(f"系数：估计 {a.est}，标准误 {a.se}" + (f"，自由度 {df}" if df else "（没给自由度，按正态分布算 z）"))
    rep.say(f"  {name} = 估计 / 标准误 = {fmt(t, 2)}（舍入范围 {fmt(lo, 2)} 到 {fmt(hi, 2)}）")
    plo, phi = p_span(lo, hi, lambda x: p_t(x, df))
    rep.say(f"  双侧 {p_eq(p_t(t, df))}")
    rep.value(name, lo, hi, a.t)
    rep.p(plo, phi, a.p)
    return rep.done()


def interval(a) -> str:
    rep = Report()
    level = num(a.level)
    zc = z_crit(level)
    g = math.log if a.ratio else (lambda x: x)
    floor = 1e-9 if a.ratio else -math.inf
    lo_i, hi_i = [max(x, floor) for x in around(a.lo)], [max(x, floor) for x in around(a.hi)]
    se = (g(num(a.hi)) - g(num(a.lo))) / (2 * zc)
    scale = "对数尺度" if a.ratio else "原尺度"
    rep.say(f"区间：估计 {a.est}，{fmt(level * 100, 0)}% 区间 [{a.lo}, {a.hi}]（{scale}）")
    rep.say(f"  标准误 = (上限 − 下限) / {2 * zc:.2f} = {fmt(se, 3)}")
    centre = (math.exp((g(num(a.lo)) + g(num(a.hi))) / 2) if a.ratio else (num(a.lo) + num(a.hi)) / 2)
    if a.est is None:
        z = g(centre) / se
        rep.say(f"  没给估计值，用区间中点 {fmt(centre, 3)}：z = {fmt(z, 2)}，双侧 {p_eq(p_z(z))}")
        return rep.done()
    clo, chi = corners(lambda l, u: math.exp((g(l) + g(u)) / 2) if a.ratio else (l + u) / 2, lo_i, hi_i)
    elo, ehi = around(a.est)
    if ehi < clo or elo > chi:
        rep.say(f"  估计值不在区间正中（区间中点 {fmt(centre, 3)}）：区间可能不是按正态近似算的，或某个数有误")
    if a.est is not None:
        z = g(num(a.est)) / se
        est_i = [max(x, floor) for x in around(a.est)]
        zlo, zhi = corners(lambda e, l, u: g(e) / ((g(u) - g(l)) / (2 * zc)), est_i, lo_i, hi_i)
        rep.say(f"  z = {fmt(z, 2)}，双侧 {p_eq(p_z(z))}（按舍入范围，p 在 {fmt_p(p_span(zlo, zhi, p_z)[0])} 到 {fmt_p(p_span(zlo, zhi, p_z)[1])} 之间）")
        rep.p(*p_span(zlo, zhi, p_z), a.p)
    return rep.done()


def chi2(a) -> str:
    rep = Report()
    df = int(a.df)
    lo, hi = around(a.value)
    rep.say(f"卡方：χ²({df}) = {a.value}，{p_eq(p_chi2(num(a.value), df))}")
    rep.p(p_chi2(max(hi, 0), df), p_chi2(max(lo, 0), df), a.p)
    return rep.done()


def ftest(a) -> str:
    rep = Report()
    d1, d2 = int(a.df), int(a.df2)
    lo, hi = around(a.value)
    rep.say(f"F 检验：F({d1}, {d2}) = {a.value}，{p_eq(p_f(num(a.value), d1, d2))}")
    rep.p(p_f(max(hi, 0), d1, d2), p_f(max(lo, 0), d1, d2), a.p)
    return rep.done()


def table(a) -> str:
    rep = Report()
    x1, n1, x2, n2 = a.cells[0], a.cells[0] + a.cells[1], a.cells[2], a.cells[2] + a.cells[3]
    aa, bb, cc, dd = a.cells
    n = aa + bb + cc + dd
    denom = (aa + bb) * (cc + dd) * (aa + cc) * (bb + dd)
    rep.say(f"四格表：第一组 {x1}/{n1}（{100 * x1 / n1:.1f}%），第二组 {x2}/{n2}（{100 * x2 / n2:.1f}%）")
    if denom == 0:
        rep.say("  有一行或一列全是 0，算不了卡方")
        return rep.done()
    pearson = n * (aa * dd - bb * cc) ** 2 / denom
    yates = n * max(0.0, abs(aa * dd - bb * cc) - n / 2) ** 2 / denom
    rep.say(f"  不校正 χ²(1) = {pearson:.2f}，{p_eq(p_chi2(pearson, 1))}")
    rep.say(f"  连续性校正 χ²(1) = {yates:.2f}，{p_eq(p_chi2(yates, 1))}")
    rep.say(f"  费舍尔精确检验，双侧 {p_eq(fisher_two_sided(aa, bb, cc, dd))}")
    cells = [x + 0.5 for x in a.cells] if 0 in a.cells else [float(x) for x in a.cells]
    oratio = cells[0] * cells[3] / (cells[1] * cells[2])
    se = math.sqrt(sum(1 / x for x in cells))
    note = "（有 0 格，每格加 .5）" if 0 in a.cells else ""
    rep.say(f"  OR = {oratio:.2f}，95% 区间 [{math.exp(math.log(oratio) - 1.96 * se):.2f}, "
            f"{math.exp(math.log(oratio) + 1.96 * se):.2f}]{note}")
    if a.chi2 is not None:
        lo, hi = around(a.chi2)
        hits = [k for k, v in (("不校正", pearson), ("连续性校正", yates)) if lo <= v <= hi]
        if hits:
            rep.say(f"报告的 χ² = {a.chi2}：与{hits[0]}的卡方相符")
        else:
            rep.bad += 1
            rep.say(f"报告的 χ² = {a.chi2}：与两种卡方都不相符，组人数或事件数可能和表里的不一样")
    return rep.done()


def groups(a) -> str:
    rep = Report()
    (m1, m2), (s1, s2), (n1, n2) = a.means, a.sds, a.ns
    df = n1 + n2 - 2

    def pooled(x1, x2, y1, y2):
        return math.sqrt(((n1 - 1) * y1 ** 2 + (n2 - 1) * y2 ** 2) / df)

    def tval(x1, x2, y1, y2):
        return (x1 - x2) / (pooled(x1, x2, y1, y2) * math.sqrt(1 / n1 + 1 / n2))

    def dval(x1, x2, y1, y2):
        return (x1 - x2) / pooled(x1, x2, y1, y2)
    ranges = (around(m1), around(m2), [max(v, 1e-9) for v in around(s1)], [max(v, 1e-9) for v in around(s2)])
    args = (num(m1), num(m2), num(s1), num(s2))
    t, d = tval(*args), dval(*args)
    tlo, thi = corners(tval, *ranges)
    dlo, dhi = corners(dval, *ranges)
    sw = math.sqrt(num(s1) ** 2 / n1 + num(s2) ** 2 / n2)
    dfw = sw ** 4 / ((num(s1) ** 2 / n1) ** 2 / (n1 - 1) + (num(s2) ** 2 / n2) ** 2 / (n2 - 1))
    tw = (num(m1) - num(m2)) / sw
    rep.say(f"两组：{m1}（SD {s1}，n = {n1}）对 {m2}（SD {s2}，n = {n2}）")
    rep.say(f"  合并方差 t({df}) = {fmt(t, 2)}（舍入范围 {fmt(tlo, 2)} 到 {fmt(thi, 2)}），双侧 {p_eq(p_t(t, df))}")
    rep.say(f"  不假定方差相等（Welch）t({dfw:.1f}) = {fmt(tw, 2)}，双侧 {p_eq(p_t(tw, dfw))}")
    rep.say(f"  d = {fmt(d, 2)}（舍入范围 {fmt(dlo, 2)} 到 {fmt(dhi, 2)}），校正后的 g = {fmt(d * (1 - 3 / (4 * df - 1)), 2)}")
    rep.value("t（取绝对值比较）", tlo, thi, a.t, absolute=True)
    rep.value("d（取绝对值比较）", dlo, dhi, a.d, absolute=True)
    rep.p(*p_span(tlo, thi, lambda x: p_t(x, df)), a.p)
    return rep.done()


def corr(a) -> str:
    rep = Report()
    n = a.n
    df = n - 2

    def tval(r):
        r = max(min(r, 0.999999), -0.999999)
        return r * math.sqrt(df) / math.sqrt(1 - r * r)
    lo, hi = corners(tval, around(a.r))
    t = tval(num(a.r))
    rep.say(f"相关：r = {a.r}，n = {n}；t({df}) = {fmt(t, 2)}，双侧 {p_eq(p_t(t, df))}")
    rep.value("t", lo, hi, a.t)
    rep.p(*p_span(lo, hi, lambda x: p_t(x, df)), a.p)
    return rep.done()


def proportion(a) -> str:
    rep = Report()
    pct = 100 * a.k / a.n
    rep.say(f"比例：{a.k} / {a.n} = {pct:.2f}%")
    if a.reported is not None:
        lo, hi = around(a.reported)
        ok = lo <= pct <= hi
        rep.bad += not ok
        msg = f"报告的 {a.reported}%：" + ("相符" if ok else "不相符")
        if not ok:
            fits = [k for k in range(a.n + 1) if lo <= 100 * k / a.n <= hi]
            msg += f"；分母是 {a.n} 时，能得到这个百分比的分子是 {'、'.join(map(str, fits[:5]))}" if fits else f"；分母是 {a.n} 时，没有哪个整数分子能得到这个百分比"
        rep.say(msg)
    return rep.done()


def main(argv: list[str] | None = None) -> str:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="kind", required=True)

    c = sub.add_parser("系数", aliases=["coef"], help="系数、标准误 → t 和 p")
    c.add_argument("--估计", "--est", dest="est", required=True)
    c.add_argument("--标准误", "--se", dest="se", required=True)
    c.add_argument("--自由度", "--df", dest="df")
    c.add_argument("--报告t", "--reported-t", dest="t")
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=coef)

    c = sub.add_parser("区间", aliases=["ci"], help="估计值和置信区间 → 标准误、z 和 p")
    c.add_argument("--估计", "--est", dest="est")
    c.add_argument("--下限", "--lower", dest="lo", required=True)
    c.add_argument("--上限", "--upper", dest="hi", required=True)
    c.add_argument("--比值", "--ratio", dest="ratio", action="store_true", help="OR、RR、HR 这类比值，在对数尺度上算")
    c.add_argument("--水平", "--level", dest="level", default="0.95")
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=interval)

    c = sub.add_parser("卡方", aliases=["chi2"], help="χ² 和自由度 → p")
    c.add_argument("--值", "--value", dest="value", required=True)
    c.add_argument("--自由度", "--df", dest="df", required=True)
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=chi2)

    c = sub.add_parser("F", help="F 和两个自由度 → p")
    c.add_argument("--值", "--value", dest="value", required=True)
    c.add_argument("--自由度", "--df", dest="df", required=True)
    c.add_argument("--分母自由度", "--df2", dest="df2", required=True)
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=ftest)

    c = sub.add_parser("四格", aliases=["2x2"], help="四格表人数 → 两种卡方、费舍尔检验和 OR")
    c.add_argument("cells", type=int, nargs=4, metavar="人数", help="第一组有、第一组无、第二组有、第二组无")
    c.add_argument("--报告卡方", "--reported-chi2", dest="chi2")
    c.set_defaults(fun=table)

    c = sub.add_parser("两组", aliases=["groups"], help="两组均值、标准差和人数 → t、p 和 d")
    c.add_argument("--均值", "--means", dest="means", nargs=2, required=True)
    c.add_argument("--标准差", "--sds", dest="sds", nargs=2, required=True)
    c.add_argument("--人数", "--ns", dest="ns", nargs=2, type=int, required=True)
    c.add_argument("--报告t", "--reported-t", dest="t")
    c.add_argument("--报告d", "--reported-d", dest="d")
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=groups)

    c = sub.add_parser("相关", aliases=["r"], help="相关系数和人数 → t 和 p")
    c.add_argument("--r", dest="r", required=True)
    c.add_argument("--人数", "--n", dest="n", type=int, required=True)
    c.add_argument("--报告t", "--reported-t", dest="t")
    c.add_argument("--报告p", "--reported-p", dest="p")
    c.set_defaults(fun=corr)

    c = sub.add_parser("比例", aliases=["pct"], help="人数和分母 → 百分比")
    c.add_argument("--分子", "--k", dest="k", type=int, required=True)
    c.add_argument("--分母", "--n", dest="n", type=int, required=True)
    c.add_argument("--报告", "--reported", dest="reported")
    c.set_defaults(fun=proportion)

    a = ap.parse_args(argv)
    return a.fun(a)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(main())
