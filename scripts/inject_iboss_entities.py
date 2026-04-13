"""Inject iboss (최재명 i-boss 201건) entities into the knowledge graph.

Why: graphify's code-only rebuild ignores document semantics, so the 201
iboss article summaries contribute nothing to the graph beyond one CEO node.
This script adds curated entities (series, tools, concepts, cases) that
represent the iboss corpus so it shows up in god-nodes, communities, and
cross-domain edges.

Idempotent: skips nodes/edges already present. Re-runs Leiden clustering
after injection so new nodes get community IDs. Run after `_rebuild_code`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx

from graphify import cluster

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
SRC_FILE = "wiki/sources/src-iboss-choi-jaemyeong.md"
INDEX_FILE = "raw/iboss/INDEX.md"

NODES: list[dict] = [
    # Source + index
    {"id": "source_iboss_wiki", "label": "i-boss 게시판 (근육돌이)", "source_file": SRC_FILE},
    {"id": "iboss_index_201", "label": "iboss 201건 인덱스 (2017-2026)", "source_file": INDEX_FILE},
    # Series
    {"id": "iboss_series_40부작", "label": "마케팅 핵심 이해 40부작 (2022)", "source_file": INDEX_FILE},
    {"id": "iboss_series_100억_10부작", "label": "100억 쇼핑몰 10부작 (2023)", "source_file": INDEX_FILE},
    {"id": "iboss_series_구글애즈_60억", "label": "구글애즈 60억 10부작 (2023)", "source_file": INDEX_FILE},
    {"id": "iboss_series_정육점", "label": "강남 정육점 인사이트 (2024)", "source_file": INDEX_FILE},
    {"id": "iboss_series_공감콘텐츠", "label": "공감 콘텐츠 5부작 (2017-2020)", "source_file": INDEX_FILE},
    {"id": "iboss_series_스토어팜", "label": "스토어팜 억대 매출 8부작 (2018-2019)", "source_file": INDEX_FILE},
    {"id": "iboss_series_ai_automation", "label": "AI 자동화 시리즈 (2025-2026)", "source_file": INDEX_FILE},
    # Tools (AI creative stack)
    {"id": "tool_nanobanana", "label": "나노바나나 (Gemini Image Pro)", "source_file": SRC_FILE},
    {"id": "tool_veo3", "label": "Veo3", "source_file": SRC_FILE},
    {"id": "tool_midjourney", "label": "Midjourney 7", "source_file": SRC_FILE},
    {"id": "tool_higgsfield", "label": "Higgsfield (사실적 인물)", "source_file": SRC_FILE},
    {"id": "tool_seedream", "label": "Seedream 4.0", "source_file": SRC_FILE},
    {"id": "tool_akool", "label": "AKOOL (AI 모델)", "source_file": SRC_FILE},
    # Core concepts (frameworks repeated 201건 across)
    {"id": "concept_usp_desire", "label": "USP = 욕구 (기능 아님)", "source_file": SRC_FILE},
    {"id": "concept_empathy_7", "label": "공감 마케팅 7요소", "source_file": SRC_FILE},
    {"id": "concept_rolling_balkan", "label": "롤링발칸 (월 500~2500 소재 테스트)", "source_file": SRC_FILE},
    {"id": "concept_persuasion_9", "label": "설득 9요소 (상호성·희소성·권위 등)", "source_file": SRC_FILE},
    {"id": "concept_priority_5step", "label": "제품>상세>소재>타겟>매체 우선순위", "source_file": SRC_FILE},
    {"id": "concept_empathy_over_quality", "label": "공감 > 퀄리티 (CPA 10배 차이)", "source_file": SRC_FILE},
    {"id": "concept_repurchase_over_newacq", "label": "재구매·CRM > 신규 획득", "source_file": SRC_FILE},
    {"id": "concept_ai_execution_gap", "label": "AI 실행 격차 10~100배 (2026-2027 변곡)", "source_file": SRC_FILE},
    {"id": "concept_tacit_ai_collab", "label": "암묵지 추출 = AI 협업 엔진", "source_file": SRC_FILE},
    # Landmark cases
    {"id": "case_jeongyukjeom_rebuy", "label": "강남 정육점 재구매율 86% 일매출 8억", "source_file": SRC_FILE},
    {"id": "case_ai_studio_8000", "label": "AI 무중단 스튜디오 일매출 8천만", "source_file": SRC_FILE},
    {"id": "case_ad_spend_2500", "label": "누적 광고비 2,500억 집행 경험", "source_file": SRC_FILE},
    # Platform (already exists: platform_naver_gfa, entity_naver)
    {"id": "platform_google_ads", "label": "구글애즈 (PMax·Discovery·Video)", "source_file": SRC_FILE},
    {"id": "platform_meta_ads", "label": "메타 광고 (페이스북·인스타)", "source_file": SRC_FILE},
    {"id": "platform_shortform", "label": "숏폼 (틱톡·릴스·쇼츠)", "source_file": SRC_FILE},
]

EDGES: list[tuple[str, str, str]] = [
    # Authorship & provenance
    ("person_choi_jaemyung", "source_iboss_wiki", "authored"),
    ("source_iboss_wiki", "iboss_index_201", "indexes"),
    # Index → series (contains)
    ("iboss_index_201", "iboss_series_40부작", "contains"),
    ("iboss_index_201", "iboss_series_100억_10부작", "contains"),
    ("iboss_index_201", "iboss_series_구글애즈_60억", "contains"),
    ("iboss_index_201", "iboss_series_정육점", "contains"),
    ("iboss_index_201", "iboss_series_공감콘텐츠", "contains"),
    ("iboss_index_201", "iboss_series_스토어팜", "contains"),
    ("iboss_index_201", "iboss_series_ai_automation", "contains"),
    # Series → concepts/cases they articulate
    ("iboss_series_40부작", "concept_priority_5step", "articulates"),
    ("iboss_series_40부작", "concept_usp_desire", "articulates"),
    ("iboss_series_100억_10부작", "concept_repurchase_over_newacq", "articulates"),
    ("iboss_series_100억_10부작", "concept_priority_5step", "articulates"),
    ("iboss_series_구글애즈_60억", "platform_google_ads", "covers"),
    ("iboss_series_구글애즈_60억", "case_ad_spend_2500", "evidences"),
    ("iboss_series_정육점", "case_jeongyukjeom_rebuy", "documents"),
    ("iboss_series_정육점", "concept_repurchase_over_newacq", "articulates"),
    ("iboss_series_공감콘텐츠", "concept_empathy_over_quality", "articulates"),
    ("iboss_series_공감콘텐츠", "concept_empathy_7", "defines"),
    ("iboss_series_ai_automation", "concept_ai_execution_gap", "articulates"),
    ("iboss_series_ai_automation", "concept_tacit_ai_collab", "articulates"),
    ("iboss_series_ai_automation", "case_ai_studio_8000", "documents"),
    # Tools used in AI case
    ("case_ai_studio_8000", "tool_nanobanana", "uses"),
    ("case_ai_studio_8000", "tool_veo3", "uses"),
    ("case_ai_studio_8000", "tool_midjourney", "uses"),
    ("case_ai_studio_8000", "tool_higgsfield", "uses"),
    ("case_ai_studio_8000", "tool_seedream", "uses"),
    ("case_ai_studio_8000", "tool_akool", "uses"),
    # Concept → domain cross-links (where existing domain nodes exist)
    ("concept_usp_desire", "domain_da_creative", "applies_to"),
    ("concept_empathy_over_quality", "domain_da_creative", "applies_to"),
    ("concept_persuasion_9", "domain_psychology", "applies_to"),
    ("concept_rolling_balkan", "domain_da_creative", "applies_to"),
    ("concept_repurchase_over_newacq", "domain_marketing_automation", "applies_to"),
    ("concept_ai_execution_gap", "domain_ai_automation", "applies_to"),
    ("concept_tacit_ai_collab", "domain_ai_automation", "applies_to"),
    # Platform linkages
    ("platform_google_ads", "iboss_series_구글애즈_60억", "documented_in"),
    ("platform_naver_gfa", "iboss_index_201", "documented_in"),
    ("platform_meta_ads", "iboss_index_201", "documented_in"),
    ("platform_shortform", "iboss_series_정육점", "amplifies"),
    # Cases → domain
    ("case_jeongyukjeom_rebuy", "domain_marketing_automation", "example_for"),
    ("case_ai_studio_8000", "domain_ai_automation", "example_for"),
    ("case_ad_spend_2500", "source_iboss_wiki", "credibility_for"),
]


def make_node(spec: dict) -> dict:
    return {
        "label": spec["label"],
        "file_type": "document",
        "source_file": spec.get("source_file", SRC_FILE),
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-04-13",
        "author": "최재명 (근육돌이)",
        "contributor": None,
        "community": None,
        "id": spec["id"],
    }


def make_edge(src: str, tgt: str, relation: str) -> dict:
    return {
        "relation": relation,
        "confidence": "EXTRACTED",
        "source_file": SRC_FILE,
        "source_location": None,
        "weight": 1.0,
        "_src": src,
        "_tgt": tgt,
        "confidence_score": 1.0,
        "source": src,
        "target": tgt,
    }


def main() -> int:
    with GRAPH_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {n["id"] for n in data["nodes"]}
    existing_edges = {(e["source"], e["target"], e.get("relation")) for e in data["links"]}

    added_n = 0
    for spec in NODES:
        if spec["id"] not in existing_ids:
            data["nodes"].append(make_node(spec))
            added_n += 1

    added_e = 0
    skipped_e = 0
    all_ids = {n["id"] for n in data["nodes"]}
    for src, tgt, rel in EDGES:
        if src not in all_ids or tgt not in all_ids:
            skipped_e += 1
            continue
        if (src, tgt, rel) in existing_edges:
            continue
        data["links"].append(make_edge(src, tgt, rel))
        added_e += 1

    print(f"[inject_iboss] +{added_n} nodes, +{added_e} edges (skipped {skipped_e} w/ missing endpoint)")

    G = nx.node_link_graph(
        data,
        directed=data.get("directed", True),
        multigraph=data.get("multigraph", False),
        edges="links",
    )
    undirected = G.to_undirected() if G.is_directed() else G
    communities = cluster.cluster(undirected)
    for cid, nids in communities.items():
        for nid in nids:
            if nid in G.nodes:
                G.nodes[nid]["community"] = cid

    out = nx.node_link_data(G, edges="links")
    out["directed"] = data.get("directed", True)
    out["multigraph"] = data.get("multigraph", False)
    out["graph"] = data.get("graph", {})
    out["hyperedges"] = data.get("hyperedges", [])
    with GRAPH_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[inject_iboss] re-clustered into {len(communities)} communities, saved graph.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
