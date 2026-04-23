"""Inject aliases into frontmatter by extracting the first H1 title.

Why: raw/ files (iboss/*.md, skills/*.md, etc.) have English-looking slugs
(e.g., ab-6141-26811) but Korean titles in their H1 heading. Pulling that
H1 into `aliases:` makes Obsidian's Front Matter Title plugin display the
Korean title in explorer, graph, and backlinks.

Usage: python scripts/inject_aliases_from_h1.py

Idempotent — skips files that already have `aliases:` set.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories to process
TARGET_DIRS = [
    ROOT / "raw" / "iboss",
    ROOT / "raw" / "skills",
    ROOT / "raw" / "reports",
    ROOT / "raw" / "inbox",
    ROOT / "raw" / "qscv",
    ROOT / "raw" / "foreign-influencer-guide",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def extract_h1(text: str) -> str | None:
    # Strip frontmatter first so we don't pick up # inside YAML comments
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    h1 = H1_RE.search(body)
    if not h1:
        return None
    title = h1.group(1).strip()
    # Skip meaningless titles
    if not title or len(title) < 2:
        return None
    return title


def inject(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)

    title = extract_h1(text)
    if not title:
        return "no-h1"

    # Escape double quotes in title for YAML
    safe = title.replace('"', '\\"')
    alias_line = f'aliases: ["{safe}"]'

    if m:
        fm_body = m.group(1)
        if re.search(r"^aliases\s*:", fm_body, re.MULTILINE):
            return "skip-already-has-aliases"
        new_fm = f"---\n{alias_line}\n{fm_body}\n---\n"
        new_text = new_fm + text[m.end():]
    else:
        new_fm = f"---\n{alias_line}\n---\n\n"
        new_text = new_fm + text

    path.write_text(new_text, encoding="utf-8")
    return "updated"


def main() -> None:
    stats = {"updated": 0, "skip-already-has-aliases": 0, "no-h1": 0}
    for d in TARGET_DIRS:
        if not d.exists():
            continue
        for path in d.rglob("*.md"):
            result = inject(path)
            stats[result] = stats.get(result, 0) + 1
    print(
        f"updated={stats['updated']} "
        f"already_has={stats['skip-already-has-aliases']} "
        f"no_h1={stats['no-h1']}"
    )


if __name__ == "__main__":
    main()
