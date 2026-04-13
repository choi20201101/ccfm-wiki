"""Re-generate GRAPH_REPORT.md using the semantic community labels stored on
each node's `community_label` attribute in graph.json.

Why this exists: graphify's `_rebuild_code` (run by the post-commit hook)
regenerates GRAPH_REPORT.md with default "Community N" names, wiping the
human-curated Korean labels. This script restores them from persisted node
attributes so the report is always informative.

Usage:
    python scripts/regen_graph_report.py

If `community_label` is absent on nodes, falls back to COMMUNITY_LABELS below.
Edit that dict when the community structure changes.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx

from graphify import analyze, cluster, detect, report

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
REPORT_PATH = ROOT / "graphify-out" / "GRAPH_REPORT.md"

FALLBACK_LABELS: dict[int, str] = {
    0: "해외 시장 (대만/일본/동남아)",
    1: "AI 자동화 & 스킬 파이프라인",
    2: "M&A Exit & 재무",
    3: "QSCV 문서 추출 코드",
    4: "조직개편 & HR",
    5: "크리에이티브 & 심리 패턴",
    6: "본사 사업/마케팅 (최재명·네이버·GFA)",
    7: "루솔브 퍼포먼스 캔버스 코드",
    8: "로고 제거 기술",
    9: "AI 아바타/영상 툴",
}


def main() -> int:
    if not GRAPH_PATH.exists():
        print(f"[regen] graph.json not found at {GRAPH_PATH}", file=sys.stderr)
        return 1

    with GRAPH_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    G = nx.node_link_graph(
        data,
        directed=data.get("directed", True),
        multigraph=data.get("multigraph", False),
        edges="links",
    )

    communities: dict[int, list[str]] = defaultdict(list)
    persisted_labels: dict[int, str] = {}
    for nid, attrs in G.nodes(data=True):
        cid = attrs.get("community")
        if cid is None:
            continue
        communities[cid].append(nid)
        if "community_label" in attrs and cid not in persisted_labels:
            persisted_labels[cid] = attrs["community_label"]

    communities = {cid: sorted(nodes) for cid, nodes in sorted(communities.items())}
    labels = {cid: persisted_labels.get(cid, FALLBACK_LABELS.get(cid, f"Community {cid}"))
              for cid in communities}

    undirected = G.to_undirected() if G.is_directed() else G
    cohesion = cluster.score_all(undirected, communities)
    god_nodes = analyze.god_nodes(G, top_n=10)
    surprises = analyze.surprising_connections(G, top_n=5)
    detection_result = detect.detect(ROOT)
    token_cost = {"input": 0, "output": 0}

    md = report.generate(
        G=G,
        communities=communities,
        cohesion_scores=cohesion,
        community_labels=labels,
        god_node_list=god_nodes,
        surprise_list=surprises,
        detection_result=detection_result,
        token_cost=token_cost,
        root=".",
    )
    REPORT_PATH.write_text(md, encoding="utf-8")
    print(f"[regen] wrote {REPORT_PATH.relative_to(ROOT)} with {len(labels)} labeled communities")

    for nid, attrs in G.nodes(data=True):
        cid = attrs.get("community")
        if cid is not None and cid in labels:
            attrs["community_label"] = labels[cid]
    with GRAPH_PATH.open("w", encoding="utf-8") as f:
        json.dump(nx.node_link_data(G, edges="links"), f, ensure_ascii=False, indent=2)
    print(f"[regen] persisted community_label on {GRAPH_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
