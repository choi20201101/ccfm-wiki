"""Inject Korean aliases into wiki page frontmatter.

Why: English slugs like `src-volumefill-video-pipeline-2026-04-21` are hard to
scan in Obsidian's graph/file list. Adding `aliases:` in frontmatter makes
Obsidian display the Korean name while keeping the slug (no file rename,
no link breakage, no git/script impact).

Usage: python scripts/inject_korean_aliases.py

Idempotent — skips files that already have `aliases:` set. Adds frontmatter
to files that don't have it.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

ALIAS_MAP: dict[str, list[str]] = {
    # tacit
    "tacit/coding-lessons": ["코딩 교훈", "자동화 시행착오"],
    "tacit/creative-patterns": ["크리에이티브 패턴", "영상·이미지 감각"],
    "tacit/decision-rules": ["판단 기준", "의사결정 룰"],
    "tacit/lessons-learned": ["실패 교훈", "회고 레슨"],
    "tacit/market-intuition": ["시장 감각"],
    "tacit/operational-heuristics": ["운영 노하우"],
    "tacit/people-dynamics": ["사람 읽기", "커뮤니케이션 신호"],
    "tacit/psychology-insights": ["심리·설득 원칙"],
    "tacit/video-gen-lessons": ["영상 생성 교훈", "Kling·Gemini 실전 이슈"],
    "tacit/viral-patterns": ["바이럴 감각", "밈·공유 패턴"],

    # domains
    "domains/ai-automation": ["AI 자동화", "스킬 파이프라인"],
    "domains/content-ai-automation": ["콘텐츠 AI 자동화", "컷편집~업로드"],
    "domains/da-creative": ["DA 크리에이티브"],
    "domains/finance": ["재무", "경영·재무·회계"],
    "domains/hr-admin": ["인사·총무"],
    "domains/japan-market": ["일본 시장"],
    "domains/ma-exit": ["M&A Exit", "스마일게이트 딜"],
    "domains/market-research-playbook": ["시장조사 플레이북"],
    "domains/marketing-automation": ["마케팅 자동화"],
    "domains/marketing": ["퍼포먼스 마케팅", "i-boss 본사"],
    "domains/org-restructure": ["조직개편", "A→Y/Z 모델"],
    "domains/psychology": ["소비자 심리", "행동경제학"],
    "domains/sea-tiktok": ["동남아 틱톡샵", "BPOM·할랄"],
    "domains/taiwan-market": ["대만 시장", "TFDA"],
    "domains/vibe-coding": ["바이브코딩"],
    "domains/viral": ["바이럴 메커니즘"],

    # sources
    "sources/src-cafe-crawler": ["네이버 카페 크롤러"],
    "sources/src-claude-skills-inventory-2026-04-22": ["Claude 스킬·커맨드 인벤토리 (2026-04-22)"],
    "sources/src-community": ["커뮤니티 크롤러"],
    "sources/src-diet-b2a-skill": ["다이어트 B/A 스킬 v1"],
    "sources/src-diet-b2a-v2": ["다이어트 B/A v2 대량생산"],
    "sources/src-foreign-influencer-guide": ["외국인 인플루언서 가이드"],
    "sources/src-gemini-logo-remover": ["Gemini 로고 제거"],
    "sources/src-goglecc-seed-curation": ["goglecc 씨드 이미지 큐레이션"],
    "sources/src-higgsfield-soul-api-2026-04-21": ["Higgsfield Soul API (2026-04-21)"],
    "sources/src-iboss-choi-jaemyeong": ["i-boss 201건 (최재명)"],
    "sources/src-instar": ["인스타 수집"],
    "sources/src-instarup": ["IG 자동 업로드"],
    "sources/src-market-research-pipeline-2026-04": ["시장조사 파이프라인 (주름·유쎄라블)"],
    "sources/src-naverapi": ["네이버 검색광고 API"],
    "sources/src-skincare-ba-pipeline-2026-04-23": ["스킨케어 B/A 17초 파이프라인 (2026-04-23)"],
    "sources/src-talmo-b2a": ["탈모 루솔브 B/A 릴스"],
    "sources/src-volumefill-pipeline-2026-04-20": ["볼륨필인 B/A 파이프라인 v1 (2026-04-20)"],
    "sources/src-volumefill-pipeline-v2-2026-04-21": ["볼륨필인 파이프라인 v2 심화 (2026-04-21)"],
    "sources/src-volumefill-video-pipeline-2026-04-21": ["볼륨필인 Day1→14 영상 공장 (2026-04-21)"],
    "sources/src-youtube": ["유튜브 수집"],

    # qscv
    "qscv/appendix-aov": ["[QSCV] 객단가"],
    "qscv/appendix-canvas-reupdate": ["[QSCV] 캔버스 재기획"],
    "qscv/appendix-content-guide": ["[QSCV] 콘텐츠 기획"],
    "qscv/appendix-detail-page": ["[QSCV] 상세페이지"],
    "qscv/appendix-image-planning": ["[QSCV] 이미지 기획"],
    "qscv/appendix-landing": ["[QSCV] 랜딩"],
    "qscv/appendix-video-planning": ["[QSCV] 영상 기획"],
    "qscv/canvas-rusolve-v1": ["[QSCV] 루솔브 캔버스 v1"],
    "qscv/design-customer-journey": ["[QSCV] 디자인본부 고객여정"],
    "qscv/index": ["[QSCV] 인덱스"],
    "qscv/media-customer-journey": ["[QSCV] 미디어본부 고객여정"],
    "qscv/media-gfa": ["[QSCV] GFA"],
    "qscv/media-google": ["[QSCV] Google"],
    "qscv/media-meta": ["[QSCV] META"],
    "qscv/media-search-ads": ["[QSCV] 검색광고"],
    "qscv/performance-thinking": ["[QSCV] 퍼포먼스 사고 확장"],

    # top-level
    "AI-Avatar-Automation-Guide": ["AI 아바타 자동화 가이드"],
}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def yaml_aliases_block(aliases: list[str]) -> str:
    quoted = ", ".join(f'"{a}"' for a in aliases)
    return f"aliases: [{quoted}]"


def inject(path: Path, aliases: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    alias_line = yaml_aliases_block(aliases)

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
    changed = 0
    skipped = 0
    missing = 0
    for slug, aliases in ALIAS_MAP.items():
        path = WIKI / f"{slug}.md"
        if not path.exists():
            print(f"MISSING: {path}")
            missing += 1
            continue
        result = inject(path, aliases)
        if result == "updated":
            changed += 1
            print(f"UPDATED: {slug} → {aliases}")
        else:
            skipped += 1
    print(f"\nDone. updated={changed} skipped={skipped} missing={missing}")


if __name__ == "__main__":
    main()
