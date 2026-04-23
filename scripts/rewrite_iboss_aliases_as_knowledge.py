"""Rewrite iboss file aliases from article titles to knowledge-based titles.

Why: The original i-boss article titles ("페이스북으로 본 SNS마케팅의 포인트 1탄")
are uninformative in Obsidian's graph view — they don't convey what knowledge
the article contains. Each iboss file has a `## 핵심 인사이트` section with
bullets shaped as `- {핵심 개념}: {설명}`. The `{핵심 개념}` part IS the
knowledge label, so we concatenate the top 2 to form a scannable title.

Result example:
  Before: "페이스북으로 본 SNS마케팅의 포인트 1탄"
  After:  "[viral] 콘텐츠가 핵심 · 6가지 공유 법칙"

Usage: python scripts/rewrite_iboss_aliases_as_knowledge.py

Non-destructive — only touches files under raw/iboss/ab-*.md. Replaces
existing `aliases:` line. Skips INDEX.md and moc/*.md (already knowledge-
oriented).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IBOSS = ROOT / "raw" / "iboss"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
CATEGORY_RE = re.compile(r"^category:\s*(\S+)", re.MULTILINE)
INSIGHT_SECTION_RE = re.compile(
    r"^##\s*핵심\s*인사이트\s*\n((?:.*\n)+?)(?=^##\s|^<!--|\Z)",
    re.MULTILINE,
)
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$", re.MULTILINE)
MAX_LABEL_LEN = 22  # per concept (keep title scannable in graph view)


def extract_concept(bullet: str) -> str | None:
    """Extract the knowledge label from a bullet. Prefer pre-colon part."""
    # Strip leading quote marks / bold markers
    s = bullet.strip().strip('"').strip("*").strip()

    # Prefer `concept: description` pattern
    if ":" in s:
        head = s.split(":", 1)[0].strip()
    elif "-" in s and len(s.split("-", 1)[0]) < 30:
        head = s.split("-", 1)[0].strip()
    else:
        # No clear delimiter — take the first clause up to a sentence end
        head = re.split(r"[.!?。—]", s, maxsplit=1)[0].strip()

    # Clean up markdown bold/italic and stray quotes/brackets
    head = re.sub(r"[*_`\"'\[\]]", "", head).strip()
    # Drop trailing punctuation
    head = head.rstrip("·,· ")

    if not head or len(head) < 2:
        return None
    if len(head) > MAX_LABEL_LEN:
        head = head[:MAX_LABEL_LEN].rstrip() + "…"
    return head


def build_knowledge_title(text: str) -> str | None:
    fm_match = FRONTMATTER_RE.match(text)
    body = text[fm_match.end():] if fm_match else text
    category = None
    if fm_match:
        c = CATEGORY_RE.search(fm_match.group(1))
        if c:
            category = c.group(1).strip()

    sec = INSIGHT_SECTION_RE.search(body)
    if not sec:
        return None
    bullets = BULLET_RE.findall(sec.group(1))
    concepts: list[str] = []
    seen: set[str] = set()
    for b in bullets:
        c = extract_concept(b)
        if c and c not in seen:
            concepts.append(c)
            seen.add(c)
        if len(concepts) == 2:
            break
    if not concepts:
        return None

    title = " · ".join(concepts)
    if category:
        title = f"[{category}] {title}"
    return title


def rewrite(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return "no-frontmatter"

    title = build_knowledge_title(text)
    if not title:
        return "no-insights"

    safe = title.replace('"', '\\"')
    new_alias_line = f'aliases: ["{safe}"]'

    fm_body = fm_match.group(1)
    if re.search(r"^aliases\s*:.*$", fm_body, re.MULTILINE):
        new_fm_body = re.sub(
            r"^aliases\s*:.*$", new_alias_line, fm_body, count=1, flags=re.MULTILINE
        )
    else:
        new_fm_body = f"{new_alias_line}\n{fm_body}"

    new_text = f"---\n{new_fm_body}\n---\n" + text[fm_match.end():]
    if new_text == text:
        return "unchanged"
    path.write_text(new_text, encoding="utf-8")
    return "updated"


def main() -> None:
    stats = {"updated": 0, "unchanged": 0, "no-insights": 0, "no-frontmatter": 0}
    sample: list[tuple[str, str]] = []
    for path in sorted(IBOSS.glob("ab-*.md")):
        result = rewrite(path)
        stats[result] = stats.get(result, 0) + 1
        if result == "updated" and len(sample) < 5:
            new_text = path.read_text(encoding="utf-8")
            m = re.search(r'aliases:\s*\["([^"]+)"\]', new_text)
            if m:
                sample.append((path.name, m.group(1)))

    print("=== stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print("\n=== first 5 rewrites ===")
    for name, alias in sample:
        print(f"  {name} → {alias}")


if __name__ == "__main__":
    main()
