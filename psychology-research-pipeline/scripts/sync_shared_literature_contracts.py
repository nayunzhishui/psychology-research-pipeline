from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ROOT = REPO_ROOT / "psychology-research-pipeline" / "references"
TARGET_ROOTS = (
    REPO_ROOT / "psych-literature-review-workflow" / "references",
    REPO_ROOT / "psych-cog-neuro-review" / "references",
)
CONTRACTS = (
    "literature-operations-contract.md",
    "deep-reading-contract.md",
    "evidence-grounded-writing-contract.md",
)


def main() -> None:
    for name in CONTRACTS:
        source = CANONICAL_ROOT / name
        text = source.read_text(encoding="utf-8")
        for target_root in TARGET_ROOTS:
            target = target_root / name
            target.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
