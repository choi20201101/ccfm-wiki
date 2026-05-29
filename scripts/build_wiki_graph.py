"""Build the knowledge graph from wiki/ + raw/ markdown (frontmatter + wikilinks).

Why: graphify's installed `extract()` is code-only (AST). It produces ZERO nodes
for markdown, so the rich "document" layer of this vault was historically built by
a one-off `.run_pipeline.py` that got gitignored and lost. This script restores that
pipeline as a committed, reproducible builder:

  document nodes  <- every .md under wiki/ and raw/ (label = alias|H1|stem)
  links_to edges  <- [[wikilinks]] + frontmatter `related:` entries
  cites edges     <- frontmatter `sources:` entries
  code subgraph   <- merged in via graphify's own AST extractor (unchanged)

It then runs the standard graphify assembly (build -> cluster -> report -> export),
producing graphify-out/graph.json + GRAPH_REPORT.md in the exact same schema as
`graphify.watch._rebuild_code`. Idempotent: a full rebuild from source each run.

Run order (mirrors .git/hooks/post-commit, but document-aware):
    python scripts/build_wiki_graph.py
    python scripts/inject_iboss_entities.py      # curated entities not in markdown
    python scripts/regen_graph_report.py         # content-based community labels
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from graphify.detect import detect
from graphify.extract import extract
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["wiki", "raw"]
OUT = ROOT / "graphify-out"

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def slug_id(rel_no_ext: str) -> str:
    """wiki/_sync-test  ->  wiki_sync-test  (matches the existing node id scheme)."""
    s = rel_no_ext.replace("\\", "/")
    s = re.sub(r"[/.\s]+", "_", s)          # path seps, dots, spaces -> underscore
    s = re.sub(r"_+", "_", s).strip("_")     # collapse repeats, trim
    return s


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Lightweight YAML-ish parser, no deps.

    Handles the shapes this vault uses: inline lists (aliases: ["a","b"]),
    block lists (key:\n  - item), and scalars (key: value).
    """
    fm: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            body = text[end + 4:]
            cur_key = None
            for raw in block.splitlines():
                line = raw.rstrip()
                if not line.strip():
                    continue
                m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
                if m:
                    cur_key, val = m.group(1), m.group(2).strip()
                    if val == "" or val == "[]":
                        fm[cur_key] = []
                    elif val.startswith("["):
                        items = re.findall(r'"([^"]*)"|\'([^\']*)\'|([^,\[\]\s][^,\[\]]*)', val)
                        fm[cur_key] = [a or b or c for a, b, c in items if (a or b or c).strip()]
                    else:
                        fm[cur_key] = val.strip().strip('"\'')
                elif re.match(r"^\s*-\s+", line) and cur_key is not None:
                    item = re.sub(r"^\s*-\s+", "", line).strip().strip('"\'')
                    if not isinstance(fm.get(cur_key), list):
                        fm[cur_key] = []
                    fm[cur_key].append(item)
    return fm, body


def clean_link(target: str) -> str:
    """[[path/to/page|alias]] or [[page#heading]] -> 'path/to/page'."""
    t = target.split("|", 1)[0]
    t = t.split("#", 1)[0]
    return t.strip()


def collect_md() -> list[Path]:
    files: list[Path] = []
    for d in SCAN_DIRS:
        base = ROOT / d
        if base.exists():
            files.extend(p for p in base.rglob("*.md") if p.is_file())
    return files


def main() -> int:
    md_files = collect_md()
    if not md_files:
        print("[build_wiki_graph] no markdown found", file=sys.stderr)
        return 1

    nodes: list[dict] = []
    edges: list[dict] = []
    resolve: dict[str, str] = {}   # candidate (lowercased) -> node id
    raw_links: list[tuple[str, str, str]] = []  # (src_id, target_str, source_file)

    def register(candidate: str, node_id: str) -> None:
        key = candidate.strip().lower()
        if key and key not in resolve:      # first registration wins (exact paths added first)
            resolve[key] = node_id

    # ---- pass 1: nodes + resolution index ----------------------------------
    parsed: list[tuple[Path, str, dict, str]] = []
    for path in md_files:
        rel = path.relative_to(ROOT).as_posix()
        rel_no_ext = rel[:-3] if rel.endswith(".md") else rel
        nid = slug_id(rel_no_ext)
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)

        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        h1 = H1_RE.search(body)
        label = (aliases[0] if aliases else (h1.group(1) if h1 else path.stem)).strip()

        nodes.append({
            "id": nid,
            "label": label,
            "file_type": "document",
            "source_file": rel,
            "source_location": "L1",
            "_folder": rel.split("/", 1)[0],
        })

        # resolution candidates: full rel, rel-without-top-dir (vault-root), stem, aliases, label
        register(rel_no_ext, nid)
        if "/" in rel_no_ext:
            register(rel_no_ext.split("/", 1)[1], nid)   # wiki-vault-root relative
        register(path.stem, nid)
        for a in aliases:
            register(a, nid)
        register(label, nid)
        parsed.append((path, nid, fm, body))

    # ---- pass 2: edges from wikilinks + frontmatter ------------------------
    for path, nid, fm, body in parsed:
        rel = path.relative_to(ROOT).as_posix()
        seen_targets: set[str] = set()
        for raw in fm.get("related", []) if isinstance(fm.get("related"), list) else []:
            for m in WIKILINK_RE.findall(str(raw)):
                seen_targets.add(clean_link(m))
        for m in WIKILINK_RE.findall(body):
            seen_targets.add(clean_link(m))
        for tgt in seen_targets:
            raw_links.append((nid, tgt, rel))
        for src in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
            src_no_ext = re.sub(r"\.md$", "", str(src).strip())
            tgt_id = resolve.get(src_no_ext.lower()) or resolve.get(Path(src_no_ext).name.lower())
            if tgt_id and tgt_id != nid:
                edges.append({"source": nid, "target": tgt_id, "relation": "cites",
                              "confidence": "EXTRACTED", "weight": 1.0,
                              "source_file": rel, "source_location": "L1"})

    for src_id, tgt_str, src_file in raw_links:
        tgt_id = resolve.get(tgt_str.lower()) or resolve.get(Path(tgt_str).name.lower())
        if tgt_id and tgt_id != src_id:
            edges.append({"source": src_id, "target": tgt_id, "relation": "links_to",
                          "confidence": "EXTRACTED", "weight": 1.0,
                          "source_file": src_file, "source_location": "L1"})

    doc_nodes, doc_edges = len(nodes), len(edges)

    # ---- pass 3: merge code subgraph (graphify AST, unchanged) -------------
    detected = detect(ROOT)
    code_files = [Path(f) for f in detected["files"]["code"]]
    if code_files:
        code_res = extract(code_files)
        nodes.extend(code_res.get("nodes", []))
        edges.extend(code_res.get("edges", []))

    # ---- assemble exactly like graphify.watch._rebuild_code ----------------
    extraction = {"nodes": nodes, "edges": edges, "input_tokens": 0, "output_tokens": 0}
    detection = {
        "files": {"code": [str(f) for f in code_files],
                  "document": [p.relative_to(ROOT).as_posix() for p in md_files],
                  "paper": [], "image": []},
        "total_files": len(md_files) + len(code_files),
        "total_words": detected.get("total_words", 0),
    }

    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    labels = {cid: "Community " + str(cid) for cid in communities}
    questions = suggest_questions(G, communities, labels)

    OUT.mkdir(exist_ok=True)
    report = generate(G, communities, cohesion, labels, gods, surprises, detection,
                      {"input": 0, "output": 0}, str(ROOT), suggested_questions=questions)
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    to_json(G, communities, str(OUT / "graph.json"))

    print(f"[build_wiki_graph] docs: {doc_nodes} nodes / {doc_edges} edges (markdown)")
    print(f"[build_wiki_graph] +code: {len(code_files)} files")
    print(f"[build_wiki_graph] TOTAL: {G.number_of_nodes()} nodes, "
          f"{G.number_of_edges()} edges, {len(communities)} communities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
