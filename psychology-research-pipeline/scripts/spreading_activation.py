"""激活扩散：按概念卡里写明的关联和阅读笔记里的共现，算出每个节点最相关的节点。

规则见 references/knowledge-vault-contract.md 第 4 节：
- 写明的关联：强 0.9、中 0.6、弱 0.3；
- 文献共现：两个节点被 n 篇阅读笔记同时链接，强度 = 1 - 0.7**n；
- 两者合并：1 - (1 - 写明) * (1 - 共现)；
- 从每个节点出发最多走三步，每多一步乘衰减 0.7，多条路径按“至少一条成功”合并。

结果写回每张概念卡的“## 激活扩散”一节（只改标记之间的内容），
并输出 视图/概念网络边表.csv。权重只用于联想和找文献，不是统计量。

用法：
  python spreading_activation.py --知识库 <知识库文件夹> [--步数 3] [--衰减 0.7] [--前 10]
"""
from __future__ import annotations

import argparse
import csv
import re
import urllib.parse
from collections import defaultdict
from itertools import combinations
from pathlib import Path

NODE_DIRS = ("概念", "测量工具", "结局", "变量", "方法", "样本")
PAPER_DIR = "文献"
DECLARED = {"强": 0.9, "中": 0.6, "弱": 0.3}
LINK = re.compile(r"\[\[([^\]|#^]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
ASSOC = re.compile(
    r"^\s*-\s*\[\[([^\]|#^]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]\s*｜\s*([^｜]+?)\s*｜\s*(强|中|弱)\s*(?:｜\s*(.*))?$"
)
START = "%% 以下由 spreading_activation.py 生成，勿手改 %%"
END = "%% 生成结束 %%"


def section(text: str, heading: str) -> str:
    """取出某个二级标题下的内容，到下一个二级标题为止。"""
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, flags=re.M)
    if not match:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"^##\s+", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def find_vault_root(path: Path) -> Path | None:
    for parent in [path, *path.parents]:
        if (parent / ".obsidian").is_dir():
            return parent
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="计算知识库的激活扩散")
    parser.add_argument("--知识库", "--vault", dest="kb", required=True, help="<主题>知识库 文件夹")
    parser.add_argument("--步数", "--steps", dest="steps", type=int, default=3)
    parser.add_argument("--衰减", "--decay", dest="decay", type=float, default=0.7)
    parser.add_argument("--前", "--top", dest="top", type=int, default=10)
    parser.add_argument("--阈值", "--min", dest="minimum", type=float, default=0.05)
    args = parser.parse_args()

    kb = Path(args.kb).resolve()
    nodes: dict[str, Path] = {}
    for folder in NODE_DIRS:
        for path in sorted((kb / folder).glob("*.md")) if (kb / folder).is_dir() else []:
            nodes[path.stem] = path
    if not nodes:
        print("没有找到概念卡，未做任何改动")
        return
    lookup = {name.casefold(): name for name in nodes}

    declared: dict[frozenset, tuple[float, str]] = {}
    for name, path in nodes.items():
        for line in section(path.read_text(encoding="utf-8"), "关联").splitlines():
            match = ASSOC.match(line)
            if not match:
                continue
            target = lookup.get(match.group(1).strip().casefold())
            if not target or target == name:
                continue
            key = frozenset((name, target))
            weight = DECLARED[match.group(3)]
            if key not in declared or weight > declared[key][0]:
                declared[key] = (weight, match.group(2).strip())

    together: dict[frozenset, int] = defaultdict(int)
    paper_dir = kb / PAPER_DIR
    for path in sorted(paper_dir.rglob("*.md")) if paper_dir.is_dir() else []:
        linked = {lookup[m.strip().casefold()] for m in LINK.findall(path.read_text(encoding="utf-8"))
                  if m.strip().casefold() in lookup}
        for a, b in combinations(sorted(linked), 2):
            together[frozenset((a, b))] += 1

    weights: dict[frozenset, float] = {}
    for key in set(declared) | set(together):
        d = declared.get(key, (0.0, ""))[0]
        c = 1 - 0.7 ** together.get(key, 0)
        weights[key] = 1 - (1 - d) * (1 - c)
    graph: dict[str, dict[str, float]] = defaultdict(dict)
    for key, weight in weights.items():
        a, b = tuple(key)
        graph[a][b] = weight
        graph[b][a] = weight

    vault_root = find_vault_root(kb)
    vault_name = vault_root.name if vault_root else None

    def node_link(name: str) -> str:
        if not vault_name:
            return name
        rel = nodes[name].relative_to(vault_root).with_suffix("").as_posix()
        query = urllib.parse.urlencode({"vault": vault_name, "file": rel}, quote_via=urllib.parse.quote)
        return f"[{name}](obsidian://open?{query})"

    for source, path in nodes.items():
        miss: dict[str, float] = defaultdict(lambda: 1.0)
        best: dict[str, tuple[float, list[str]]] = {}

        def walk(current: str, strength: float, trail: list[str]) -> None:
            if len(trail) > args.steps:
                return
            for nxt, weight in graph.get(current, {}).items():
                if nxt in trail:
                    continue
                value = strength * weight * (args.decay if len(trail) > 1 else 1.0)
                if value < 0.01:
                    continue
                miss[nxt] *= 1 - value
                if nxt not in best or value > best[nxt][0]:
                    best[nxt] = (value, trail[1:])
                walk(nxt, value, trail + [nxt])

        walk(source, 1.0, [source])
        ranked = sorted(((1 - miss[n], n) for n in miss if n != source), reverse=True)
        ranked = [(value, name) for value, name in ranked if value >= args.minimum][: args.top]

        if ranked:
            rows = ["| 节点 | 激活值 | 最强路径 |", "|---|---|---|"]
            for value, name in ranked:
                via = best[name][1]
                route = "直接相连" if not via else "经 " + " → ".join(via)
                rows.append(f"| {node_link(name)} | {value:.2f} | {route} |")
            body = "\n".join(rows)
        else:
            body = "（暂无关联：在“关联”一节写明关联，或等阅读笔记链接到这个节点）"
        block = f"{START}\n{body}\n{END}"

        text = path.read_text(encoding="utf-8")
        if START in text and END in text:
            head, tail = text.split(START, 1)
            text = head + block + tail.split(END, 1)[1]
        elif re.search(r"^##\s+激活扩散\s*$", text, flags=re.M):
            text = re.sub(r"(^##\s+激活扩散\s*$)", lambda m: m.group(1) + "\n" + block, text, count=1, flags=re.M)
        else:
            text = text.rstrip("\n") + "\n\n## 激活扩散\n" + block + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")

    out = kb / "视图" / "概念网络边表.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["节点甲", "节点乙", "写明关系", "写明强度", "共现文献数", "合并强度"])
        for key, weight in sorted(weights.items(), key=lambda item: -item[1]):
            a, b = sorted(key)
            d_weight, relation = declared.get(key, (0.0, ""))
            writer.writerow([a, b, relation, f"{d_weight:.1f}" if d_weight else "", together.get(key, 0), f"{weight:.2f}"])

    print(f"节点 {len(nodes)} 个，关联 {len(weights)} 条（写明 {len(declared)}，文献共现 {len(together)}）")
    print(f"已更新概念卡的“激活扩散”一节；边表：{out}")


if __name__ == "__main__":
    main()
