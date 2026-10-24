#!/usr/bin/env python3
"""阅读笔记、知识卡和证据提纲的机械整理。默认只试跑、打印改动；确认后加 --写入 --备份目录 <库外的文件夹>。

只做不改变意思的机械修改，讲法问题（满篇限定、内部用语、电报体）仍要手改：
1. 计数用的中文数字改阿拉伯数字：“三个”→“3 个”，“十二题”→“12 题”，“四领域”→“4 个领域”，
   “0—4五档”→“0—4，共 5 档”；“一”“两”、“第三”这类序数、“三月”这类可能指月份的写法不动；
2. 中文与数字、英文之间加空格；
3. 段尾或句号后的页码拆开，放回它支持的那一句的句号前（那一页 PDF 上能找到这句里的数字，就算支持；
   找不到的留在最后一句），用全角括号括起来；“[[第 3 页]]—[[第 5 页]]”这样的页码范围整体搬动；
4. 块编号前补空格（“……。^f1”→“……。 ^f1”）；
5. 知识卡“关联”的关系名改回规定的十种，缺强度或依据的补上。
双链、引号里的原文、二级以下标题、嵌入行和属性一律不动；知识卡只做第 3–5 项，免得改动讲义里的题目原文。

用法：
  python tidy_reading_notes.py --根 <Obsidian 库根目录> --知识库 <知识库文件夹> [--提纲目录 <证据提纲文件夹>]
  试跑时用 --显示 <文件名的一部分> 看某几篇的改动；--保护 <卡片名> 跳过不想动的卡（可重复）。
"""
from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_reading_outputs import (  # noqa: E402
    LINK, NODE_TYPES, NUM, ONE_PAGE, RELATIONS, SKIP_DIRS, TOOLNAME, Index, Pdfs, number_found,
)

DIGIT = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
DIRECT = "个|篇|项|道|题|名|人|次|年|周|天|岁|波|组|类|页|张|条|所|种|份|处|档|轮|位|例|批|段|级|期|家|层|步|句|字|点|倍"
NEED_GE = "领域|维度|因子|时点|分量|侧面|章节|阶段|问题|条目|指标|模型|类别|亚组|中心|国家|样本|研究|变量|结局|路径"
CN_NUM = re.compile(r"(?<![第一二三四五六七八九十百千万两几])([二三四五六七八九]?十[一二三四五六七八九]?|[三四五六七八九]|百)"
                    r"(?!分之)(" + DIRECT + "|" + NEED_GE + ")")
KEEP = re.compile(r"!?\[\[[^\]]*\]\]|“[^”]*”|「[^」]*」|`[^`]*`")  # 这些里面的文字不动
UNIT = re.compile(r"(" + ONE_PAGE + r")(?:\s*[—–-]\s*(" + ONE_PAGE + r"))?", re.I)
TAIL = re.compile(r"[（(]?\s*((?:" + ONE_PAGE + r"(?:\s*[—–-]\s*" + ONE_PAGE + r")?[\s、，,；;和及]*)+)[）)]?"
                  r"(\s*\^[A-Za-z0-9][\w-]*)?\s*$", re.I)
PAGE_OF = re.compile(r"\[\[([^\]|]+?\.pdf)#page=(\d+)", re.I)
# 段落中间放在句号后面的页码：“……显著。[[第 8 页]]作者认为……”，几乎都是支持前一句的
MID = re.compile(r"([。！？])\s*((?:" + ONE_PAGE + r"(?:\s*[—–-]\s*" + ONE_PAGE + r")?[\s、，,；;和及]*)+)(?=[^\s^\[])", re.I)
GLUED = re.compile(r"(?<=\S)\^([A-Za-z0-9][\w-]*)[ \t]*$", re.M)
REL_MAP = {"区别": "区分", "构念比较": "区分", "相关但不同": "区分", "方法组合": "对照", "方法衔接": "对照",
           "方法相近": "对照", "方法对照": "对照", "方法": "对照", "应用": "测量", "行为旁证": "测量",
           "相关": "共变", "关联": "共变"}


def cn_value(s: str) -> int:
    if s == "百":
        return 100
    if "十" in s:
        a, _, b = s.partition("十")
        return (DIGIT[a] if a else 1) * 10 + (DIGIT[b] if b else 0)
    return DIGIT[s]


def outside_keep(text: str, fn) -> str:
    out, last = [], 0
    for m in KEEP.finditer(text):
        out.append(fn(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(fn(text[last:]))
    return "".join(out)


def numerals(s: str) -> str:
    def rep(m):
        unit = m.group(2)
        need = "个" if re.fullmatch(NEED_GE, unit) else ""
        before = m.string[:m.start()]
        if re.search(r"\d[—–-]\d+(\.\d+)?$", before):
            lead = "，共 "  # “0—4五档”改成“0—4，共 5 档”
        elif re.search(r"[A-Za-z0-9.\-]$", before):
            lead = " "  # 免得“PHQ-8八题”变成“PHQ-88 题”
        else:
            lead = ""
        return f"{lead}{cn_value(m.group(1))} {need}{unit}"
    return CN_NUM.sub(rep, s)


def spacing(s: str) -> str:
    s = re.sub(r"(?<=[一-鿿])(?=[A-Za-z0-9])", " ", s)
    return re.sub(r"(?<=[A-Za-z0-9%])(?=[一-鿿])", " ", s)


def tidy_text(line: str) -> str:
    if re.match(r"^\s*>?\s*!\[\[", line) or line.startswith(("---", "%%")) or re.match(r"^#{2,6} ", line):
        return line  # 二级以下标题可能被别处链接
    return outside_keep(line, lambda s: spacing(numerals(s)))


def unit_pages(unit: re.Match, idx: Index, pdfs: Pdfs) -> list[str]:
    pages = [(m.group(1), int(m.group(2))) for m in PAGE_OF.finditer(unit.group(0))]
    pdf = idx.resolve(pages[0][0])
    texts = pdfs.pages(pdf) if pdf else []
    lo, hi = pages[0][1], pages[-1][1]
    return [texts[i - 1] for i in range(lo, hi + 1) if 1 <= i <= len(texts)]


def unpile(line: str, idx: Index, pdfs: Pdfs) -> str:
    if line.lstrip()[:1] in (">", "|", "!", "-", "#", "*"):
        return line
    line = MID.sub(lambda m: "（" + "、".join(u.group(0) for u in UNIT.finditer(m.group(2))) + "）" + m.group(1), line)
    m = TAIL.search(line)
    if not m:
        return line
    body = line[:m.start()].rstrip()
    links = len(PAGE_OF.findall(m.group(1)))
    after_period = body.endswith(("。", "！", "？"))
    if not body or (links < 2 and not after_period):
        return line
    block_id = " " + m.group(2).strip() if m.group(2) else ""
    sentences = [s for s in re.findall(r"[^。！？]*[。！？]?", body) if s]
    attach: dict[int, list[str]] = {i: [] for i in range(len(sentences))}
    for u in UNIT.finditer(m.group(1)):
        texts = unit_pages(u, idx, pdfs)
        target, best = len(sentences) - 1, 0
        for i, s in enumerate(sentences):
            plain = TOOLNAME.sub(" ", LINK.sub(" ", s))
            nums = [n for n in NUM.findall(plain) if not (n.isdigit() and 1900 <= int(n) <= 2035)]
            # 小数和较大的整数更有区分度，记 2 分；10–29 的整数记 1 分
            score = max((sum((2 if "." in n or int(n) >= 30 else 1) * number_found(n, t)
                             for n in nums if "." in n or int(n) >= 10) for t in texts), default=0)
            if score > best:
                best, target = score, i
        attach[target].append(u.group(0))
    out = []
    for i, s in enumerate(sentences):
        if attach[i]:
            s = re.sub(r"[（(]\s*[）)]$", "", s)
            mark = "（" + "、".join(attach[i]) + "）"
            s = s[:-1] + mark + s[-1] if s.endswith(("。", "！", "？")) else s + mark
        out.append(s)
    return "".join(out) + block_id


def fix_relations(text: str) -> str:
    sec = re.search(r"^## 关联\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not sec:
        return text

    def rep(line: str) -> str:
        mm = re.match(r"^- (\[\[[^\]]+\]\])(.*)$", line)
        if not mm:
            return line
        target, rest = mm.groups()
        if rest.startswith("｜"):
            parts = [x.strip() for x in rest[1:].split("｜")]
            if len(parts) >= 3:
                rel = REL_MAP.get(parts[0], parts[0])
                rel = rel if rel in RELATIONS else "对照"
                strength = parts[1] if parts[1] in {"强", "中", "弱"} else "中"
                return f"- {target}｜{rel}｜{strength}｜{'｜'.join(parts[2:])}"
        why = rest.lstrip("｜：: ").strip()
        rel = "区分" if re.search(r"区分|不同|分开|而非|不是|区别", why) else "对照"
        return f"- {target}｜{rel}｜中｜{why}"

    new = "\n".join(rep(l) for l in sec.group(1).split("\n"))
    return text[:sec.start(1)] + new + text[sec.end(1):]


def split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"\A---\n.*?\n---\n", text, re.S)
    return (m.group(0), text[m.end():]) if m else ("", text)


def tidy_note(text: str, idx: Index, pdfs: Pdfs) -> str:
    head, body = split_frontmatter(text)
    body = "\n".join(tidy_text(unpile(l, idx, pdfs)) for l in body.split("\n"))
    return head + GLUED.sub(lambda m: " ^" + m.group(1), body)


def tidy_card(text: str, idx: Index, pdfs: Pdfs) -> str:
    head, body = split_frontmatter(text)
    body = "\n".join(unpile(l, idx, pdfs) for l in body.split("\n"))
    return head + fix_relations(GLUED.sub(lambda m: " ^" + m.group(1), body))


def tidy_outline(text: str) -> str:
    head, body = split_frontmatter(text)
    return head + "\n".join(tidy_text(l) for l in body.split("\n"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--根", "--root", dest="root", required=True)
    ap.add_argument("--知识库", "--vault", dest="kb", required=True)
    ap.add_argument("--笔记目录", "--notes-dir", dest="notes_dir", default="文献")
    ap.add_argument("--提纲目录", "--outline-dir", dest="outline")
    ap.add_argument("--显示", "--show", dest="show", action="append", default=[])
    ap.add_argument("--保护", "--protect", dest="protect", action="append", default=[])
    ap.add_argument("--缓存", "--cache", dest="cache")
    ap.add_argument("--写入", "--write", dest="write", action="store_true")
    ap.add_argument("--备份目录", "--backup", dest="backup")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    root = Path(a.root).resolve()
    if a.write:
        if not a.backup:
            sys.exit("写入前要用 --备份目录 指定一个放在 Obsidian 库外面的文件夹。")
        backup = Path(a.backup).resolve()
        if backup == root or root in backup.parents:
            sys.exit("备份目录不能放在库里面，否则 Obsidian 会把备份当成重复的笔记。")
    kb = root / a.kb
    idx = Index(root, SKIP_DIRS)
    pdfs = Pdfs(Path(a.cache) if a.cache else None)
    jobs = [(p, "笔记") for p in sorted((kb / a.notes_dir).glob("*.md"))]
    jobs += [(p, "卡片") for p in sorted(kb.rglob("*.md")) if p.parent.name in NODE_TYPES and p.stem not in a.protect]
    if a.outline:
        jobs += [(p, "提纲") for p in sorted(Path(a.outline).glob("*.md"))]
    changed = {"笔记": 0, "卡片": 0, "提纲": 0}
    for p, kind in jobs:
        old = p.read_text(encoding="utf-8")
        new = tidy_note(old, idx, pdfs) if kind == "笔记" else tidy_card(old, idx, pdfs) if kind == "卡片" else tidy_outline(old)
        if new == old:
            continue
        changed[kind] += 1
        if any(s in p.stem for s in a.show):
            print(f"==== {p.name}")
            for d in list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0))[2:80]:
                print(d[:400])
        if a.write:
            dest = backup / p.resolve().relative_to(root)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(p, dest)
            p.write_text(new, encoding="utf-8")
    print("会改的文件：", changed, "（已写入，原文件备份在 " + str(a.backup) + "）" if a.write else "（试跑，没有写入）")


if __name__ == "__main__":
    main()
