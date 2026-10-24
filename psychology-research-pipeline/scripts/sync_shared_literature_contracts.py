"""把三个主 skill 共用的合同和脚本，从 psychology-research-pipeline 同步到另外两个 skill。

要改共用合同或共用脚本时，只改 psychology-research-pipeline 里的那一份，再运行本脚本。
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL = REPO_ROOT / "psychology-research-pipeline"
TARGETS = (
    REPO_ROOT / "psych-literature-review-workflow",
    REPO_ROOT / "psych-cog-neuro-review",
)
CONTRACTS = (
    "literature-operations-contract.md",
    "deep-reading-contract.md",
    "evidence-grounded-writing-contract.md",
    "evidence-figure-contract.md",
    "reading-note-style.md",
    "knowledge-vault-contract.md",
    # 写作示范和取值表模板：三个 skill 的阅读产出用同一套标准
    "reading-note-example-d1.md",
    "reading-note-example-d2.md",
    "writing-before-after.md",
    "matrix-vocabulary-template.json",
)
SHARED_SCRIPTS = (
    "init_knowledge_vault.py",
    "spreading_activation.py",
    "format_reading_matrix.py",
    "export_evidence_outline.py",
    "check_reading_outputs.py",
    "tidy_reading_notes.py",
)


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8").replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def main() -> None:
    for name in CONTRACTS:
        source = CANONICAL / "references" / name
        copy(source, source)  # 正本也统一成 LF，三份逐字一致
        for target in TARGETS:
            copy(source, target / "references" / name)
    for name in SHARED_SCRIPTS:
        source = CANONICAL / "scripts" / name
        copy(source, source)
        for target in TARGETS:
            copy(source, target / "scripts" / name)
    print(f"已同步 {len(CONTRACTS)} 份合同和 {len(SHARED_SCRIPTS)} 个脚本到 {len(TARGETS)} 个 skill")


if __name__ == "__main__":
    main()
