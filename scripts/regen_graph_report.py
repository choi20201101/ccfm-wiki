"""Re-generate GRAPH_REPORT.md with content-aware community labels.

Why: graphify's `_rebuild_code` (post-commit hook) writes "Community N"
names. Community IDs also shift across rebuilds — so persisting labels by ID
is unreliable. This script labels each community by inspecting its member
node labels and matching against a keyword taxonomy. Works across rebuilds.

Edit LABEL_RULES when adding new communities. Each rule is
`(label, [keywords])`; the community with the most keyword hits wins that
label. Falls back to the top-frequency node label if no rule matches.

Usage: python scripts/regen_graph_report.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

from graphify import analyze, cluster, detect, report

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
REPORT_PATH = ROOT / "graphify-out" / "GRAPH_REPORT.md"

LABEL_RULES: list[tuple[str, list[str]]] = [
    ("해외 시장 (대만/일본/동남아)", ["Merable", "TFDA", "BPOM", "대만", "일본", "동남아", "틱톡샵", "샵라인", "Q10"]),
    ("콘텐츠 AI 자동화 (FFmpeg·Whisper·TTS)", ["FFmpeg", "Whisper", "ElevenLabs", "Rhubarb", "Gemini Vision", "콘텐츠 AI", "TTS", "After Effects", "서브매직"]),
    ("바이브코딩 & 에이전트 스택", ["바이브코딩", "bob", "dd", "harness", "eval", "learnings", "스킬 파이프라인", "DD Plan", "나노바나나", "Veo3", "Midjourney", "Higgsfield", "Seedream", "AKOOL"]),
    ("M&A Exit & 재무", ["M&A", "SPA", "스마일게이트", "이전가격", "Transfer Pricing", "Dual Engine", "HK 법인", "경영/재무"]),
    ("조직개편 & HR", ["AI Cell", "신동협", "A→Y", "조직개편", "인사", "CD", "Day1"]),
    ("크리에이티브 & 심리 패턴", ["DA 크리에이티브", "릴스", "썸네일", "1초컷", "B&A", "CTR"]),
    ("본사 사업/마케팅 (최재명·네이버·GFA)", ["CCFM", "최재명", "네이버 GFA", "마케팅 자동화", "본사", "iboss"]),
    ("로고 제거 기술", ["OpenCV", "LaMa", "gemini-logo", "TELEA", "인페인팅"]),
    ("AI 아바타/영상 툴", ["OmniHuman", "Kling", "Creatify", "Aurora", "fal.ai", "ByteDance"]),
    ("QSCV 문서 추출 코드", ["extract_and_chunk", "slugify", "docx", "chunk_and_write", "QSCV"]),
    ("루솔브 퍼포먼스 캔버스 코드", ["export_canvas_rusolve", "style_section", "Rusolve", "퍼포먼스 캔버스"]),
    ("그래프 인덱싱 스크립트", ["regen_graph_report", "graph.json", "community_label"]),
    ("iboss 201건 지식베이스 (최재명)", ["iboss", "근육돌이", "나노바나나", "롤링발칸", "정육점", "40부작", "USP", "공감", "설득 9요소", "2,500억"]),
]


def pick_label(node_labels: list[str], used: set[str]) -> str:
    joined = " ".join(node_labels)
    best_label, best_score = None, 0
    for label, kws in LABEL_RULES:
        if label in used:
            continue
        score = sum(1 for kw in kws if kw in joined)
        if score > best_score:
            best_label, best_score = label, score
    if best_label and best_score > 0:
        return best_label
    counts = Counter(node_labels)
    top = counts.most_common(1)[0][0] if counts else "Unlabeled"
    return f"기타: {top[:30]}"


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
    comm_node_labels: dict[int, list[str]] = defaultdict(list)
    for nid, attrs in G.nodes(data=True):
        cid = attrs.get("community")
        if cid is None:
            continue
        communities[cid].append(nid)
        comm_node_labels[cid].append(attrs.get("label", nid))

    communities = {cid: sorted(nodes) for cid, nodes in sorted(communities.items())}

    labels: dict[int, str] = {}
    used: set[str] = set()
    sorted_cids = sorted(communities.keys(), key=lambda c: -len(communities[c]))
    for cid in sorted_cids:
        label = pick_label(comm_node_labels[cid], used)
        labels[cid] = label
        used.add(label)

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
    for cid in sorted(labels.keys()):
        print(f"  C{cid} ({len(communities[cid])} nodes): {labels[cid]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
