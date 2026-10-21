"""初始化 Obsidian 知识库：建文件夹、首页、视图和 .obsidian 设置。

规则见 references/knowledge-vault-contract.md。已存在的文件一律不覆盖；
.obsidian/app.json 只补排除列表，不动用户已有的其他设置。

用法：
  python init_knowledge_vault.py --根目录 <项目根目录> --主题 人格功能 \
      [--排除 旧项目/ --排除 tmp/] [--结局目录 结局]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

NODE_COLORS = {  # 文件夹 -> 关系图颜色（RGB 整数）
    "文献": 0x9E9E9E,
    "概念": 0xF29D38,
    "测量工具": 0x4CAF50,
    "结局": 0xE05A5A,
    "方法": 0x8E6CC9,
    "样本": 0x2BB3B3,
}
CORE_PLUGINS = [
    "file-explorer", "global-search", "switcher", "graph", "backlink",
    "outgoing-link", "tag-pane", "properties", "page-preview", "outline",
    "bookmarks", "bases", "file-recovery", "word-count", "command-palette",
    "editor-status",
]
DEFAULT_IGNORES = ["tmp/", ".git/"]

HOME = """# {topic}知识库

这是“{topic}”这个研究主题的长期知识库。项目文件照旧放在原来的文件夹里，这里只放可以长期复用的知识。

## 从哪里开始

- 想看读过哪些文献：打开 [[视图/文献总览.base|文献总览]]，可以按年份、设计、阅读深度排序。
- 想从一个概念出发联想：打开 `概念/` 里的概念卡，看“关联”和“激活扩散”两节，再打开局部关系图，把深度调到 2–3。
- 想核对一个数字：阅读笔记里的页码都能点开，直接跳到 PDF 的那一页。

## 文件夹

| 文件夹 | 放什么 |
|---|---|
| 文献 | 每篇精读文献一份阅读笔记 |
| 概念 | 构念、理论、现象和关键术语 |
| 测量工具 | 量表、访谈和任务 |
| {outcome} | 结局或研究变量 |
| 方法 | 设计、模型和分析术语 |
| 样本 | 队列、数据集和研究家族 |
| 视图 | 表格视图和脚本生成的边表 |

## 怎么长起来

知识库边读边长，不预先批量建：
- 每精读完一篇，阅读笔记放进 `文献/`；
- 这篇涉及的概念、工具、{outcome}、方法和样本，库里没有的建卡，已有的补上关联和证据；
- 笔记末尾的“提取记录”写明这次改了哪些卡；
- 每读完一批，脚本更新各卡的“激活扩散”一节。

## 节点怎么连

知识库按激活扩散模型组织：概念卡之间写明关联和强度，阅读笔记把用到的概念连起来。`spreading_activation.py` 定期算出每个概念最相关的节点，写进概念卡的“激活扩散”一节。规则见 skill 里的 `knowledge-vault-contract.md`。
"""


def base_file(filters: list[str], combine: str, name: str, columns: list[str]) -> str:
    lines = ["filters:", f"  {combine}:"]
    lines += [f"    - {item}" for item in filters]
    lines += ["views:", "  - type: table", f"    name: {name}", "    order:"]
    lines += [f"      - {column}" for column in columns]
    return "\n".join(lines) + "\n"


def write_if_missing(path: Path, text: str, created: list[str]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    created.append(str(path))


def merge_app_json(path: Path, ignores: list[str], created: list[str]) -> None:
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            print(f"跳过：{path} 不是有效的 JSON，没有改动")
            return
    current = list(data.get("userIgnoreFilters", []))
    for item in ignores:
        if item not in current:
            current.append(item)
    data["userIgnoreFilters"] = current
    data.setdefault("useMarkdownLinks", False)
    data.setdefault("newLinkFormat", "shortest")
    data.setdefault("alwaysUpdateLinks", True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    created.append(f"{path}（已合并排除列表）")


def main() -> None:
    parser = argparse.ArgumentParser(description="初始化 Obsidian 知识库")
    parser.add_argument("--根目录", "--root", dest="root", default=".", help="库的根目录，即项目根目录")
    parser.add_argument("--主题", "--topic", dest="topic", required=True, help="如：人格功能")
    parser.add_argument("--排除", "--ignore", dest="ignores", action="append", default=[],
                        help="不进搜索和关系图的文件夹，相对根目录，可多次给出")
    parser.add_argument("--结局目录", "--outcome-folder", dest="outcome", default="结局",
                        help="结局文件夹的名字，实证论文可用“变量”")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    kb_name = f"{args.topic}知识库"
    kb = root / kb_name
    created: list[str] = []

    folders = ["文献", "概念", "测量工具", args.outcome, "方法", "样本", "视图"]
    for folder in folders:
        (kb / folder).mkdir(parents=True, exist_ok=True)

    write_if_missing(kb / "首页.md", HOME.format(topic=args.topic, outcome=args.outcome), created)
    write_if_missing(
        kb / "视图" / "文献总览.base",
        base_file([f'file.inFolder("{kb_name}/文献")'], "and", "文献总览",
                  ["file.name", "年份", "设计", "人群", "阅读深度", "章节", "等级", "状态"]),
        created,
    )
    node_folders = ["概念", "测量工具", args.outcome, "方法", "样本"]
    write_if_missing(
        kb / "视图" / "节点总览.base",
        base_file([f'file.inFolder("{kb_name}/{folder}")' for folder in node_folders], "or",
                  "节点总览", ["file.name", "类型", "英文名", "上位", "状态"]),
        created,
    )

    obsidian = root / ".obsidian"
    merge_app_json(obsidian / "app.json", DEFAULT_IGNORES + args.ignores, created)
    write_if_missing(
        obsidian / "core-plugins.json",
        json.dumps({name: True for name in CORE_PLUGINS}, ensure_ascii=False, indent=2),
        created,
    )
    colors = dict(NODE_COLORS)
    if args.outcome != "结局":
        colors[args.outcome] = colors.pop("结局")
    graph = {
        "search": f'path:"{kb_name}" -path:"{kb_name}/视图"',
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": True,
        "showOrphans": True,
        "showArrow": False,
        "colorGroups": [
            {"query": f'path:"{kb_name}/{folder}"', "color": {"a": 1, "rgb": rgb}}
            for folder, rgb in colors.items()
        ],
    }
    write_if_missing(obsidian / "graph.json", json.dumps(graph, ensure_ascii=False, indent=2), created)

    print(f"知识库：{kb}")
    for item in created:
        print(f"  新建或更新：{item}")
    if not created:
        print("  没有需要新建的文件")


if __name__ == "__main__":
    main()
