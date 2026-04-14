"""Inject Korean alias nodes for diet-b2a-v2 into the graphify graph.json.

Rationale: graphify LLM extraction doesn't reprocess md heading changes without
a full /graphify --update run. For the diet-b2a-v2 ingest we add a small set of
alias document-nodes manually so Korean queries (다이어트, 비포애프터, 릴스...)
hit the src page.
"""
from __future__ import annotations
import json
from pathlib import Path

GRAPH = Path(__file__).resolve().parent.parent / "graphify-out" / "graph.json"

ALIASES = [
    # long aliases (multiple keywords)
    ("다이어트 비포애프터 릴스 자동 생성 스킬", "diet_b2a_v2_alias_ko_main"),
    ("다이어트 변신 릴스 공장", "diet_b2a_v2_alias_ko_factory"),
    ("비포애프터 영상 자동화", "diet_b2a_v2_alias_ko_b2a_auto"),
    ("체중감량 쇼츠 릴스", "diet_b2a_v2_alias_ko_weightloss"),
    ("Kling Gemini 비포애프터 파이프라인", "diet_b2a_v2_alias_pipeline"),
    ("다국어 다이어트 릴스 (한국어·번체)", "diet_b2a_v2_alias_multilang"),
    ("다이어트 B2A v2", "diet_b2a_v2_alias_short"),
    ("bdh 파이프라인 B/A 스킬", "diet_b2a_v2_alias_bdh"),
    # single-word aliases (for exact one-keyword queries)
    ("다이어트", "diet_b2a_v2_alias_word_diet"),
    ("비포애프터", "diet_b2a_v2_alias_word_b2a"),
    ("릴스", "diet_b2a_v2_alias_word_reels"),
    ("쇼츠", "diet_b2a_v2_alias_word_shorts"),
    ("변신", "diet_b2a_v2_alias_word_transform"),
    ("체중감량", "diet_b2a_v2_alias_word_weightloss"),
    ("감량", "diet_b2a_v2_alias_word_loss"),
    ("B/A", "diet_b2a_v2_alias_word_ba"),
]

SOURCE_FILE = "wiki/sources/src-diet-b2a-v2.md"
COMMUNITY = 3
COMMUNITY_LABEL = "콘텐츠 AI 자동화 (FFmpeg·Whisper·TTS)"

# Also add edges: each alias --rationale_for--> main src node
SRC_NODE_HINTS = [
    "src-diet-b2a-v2",
    "diet-b2a-v2",
]


def main():
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    existing_ids = {n.get("id") for n in g["nodes"]}

    # 1) add alias nodes
    added = 0
    for label, nid in ALIASES:
        if nid in existing_ids:
            continue
        g["nodes"].append({
            "label": label,
            "file_type": "document",
            "source_file": SOURCE_FILE,
            "source_location": None,
            "source_url": None,
            "captured_at": "2026-04-14",
            "author": None,
            "contributor": None,
            "community": COMMUNITY,
            "community_label": COMMUNITY_LABEL,
            "id": nid,
        })
        added += 1

    # 2) find a target src node
    src_target = None
    for n in g["nodes"]:
        if "src-diet-b2a-v2" in str(n.get("source_file", "")) and n.get("id") != "diet_b2a_v2":
            src_target = n.get("id")
            break
    if src_target is None:
        # add a stub main src node if missing
        src_target = "diet_b2a_v2_src"
        if src_target not in existing_ids:
            g["nodes"].append({
                "label": "src-diet-b2a-v2",
                "file_type": "document",
                "source_file": SOURCE_FILE,
                "source_location": None,
                "source_url": None,
                "captured_at": "2026-04-14",
                "author": None,
                "contributor": None,
                "community": COMMUNITY,
                "community_label": COMMUNITY_LABEL,
                "id": src_target,
            })
            added += 1

    # 3) edges (networkx JSON uses "links")
    g.setdefault("links", [])
    edge_added = 0
    for _, nid in ALIASES:
        edge = {
            "source": nid,
            "target": src_target,
            "relation": "alias_for",
            "confidence": 1.0,
            "extraction_source": "manual",
        }
        if edge not in g["links"]:
            g["links"].append(edge)
            edge_added += 1

    GRAPH.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added {added} nodes, {edge_added} edges → {GRAPH}")


if __name__ == "__main__":
    main()
