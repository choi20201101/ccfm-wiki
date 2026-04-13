"""
QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할
- 표 셀도 텍스트로 추출
- 이미지/도형은 [IMG] 플레이스홀더로 표시 (alt text 있으면 포함)
"""
import os
import re
import json
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

SRC = Path(r"C:\Users\gguy\Desktop\QSCV")
DST_RAW = Path(r"C:\Users\gguy\ccfm-wiki\raw\qscv")
DST_CHUNK = Path(r"C:\Users\gguy\ccfm-wiki\raw\qscv\chunks")
DST_RAW.mkdir(parents=True, exist_ok=True)
DST_CHUNK.mkdir(parents=True, exist_ok=True)

CHUNK_LINES = 200

def slugify(name: str) -> str:
    base = re.sub(r"\.docx$", "", name, flags=re.I)
    base = base.replace(" ", "_")
    base = re.sub(r"[\\/:*?\"<>|]", "", base)
    return base

def iter_block_items(parent):
    """문단 + 표를 문서 순서대로 반환"""
    from docx.document import Document as _Document
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def paragraph_text(p):
    # 이미지 감지
    has_img = False
    for run in p.runs:
        if run.element.findall(".//" + qn("w:drawing")):
            has_img = True
            break
    txt = p.text.strip()
    style = (p.style.name or "").lower() if p.style else ""
    prefix = ""
    if "heading 1" in style: prefix = "# "
    elif "heading 2" in style: prefix = "## "
    elif "heading 3" in style: prefix = "### "
    elif "heading 4" in style: prefix = "#### "
    elif "heading" in style: prefix = "##### "
    elif "list" in style: prefix = "- "
    out = []
    if has_img:
        out.append("[IMG]")
    if txt:
        out.append(prefix + txt)
    return "\n".join(out)

def table_to_md(t):
    rows = []
    for row in t.rows:
        cells = [c.text.strip().replace("\n", " / ").replace("|", "\\|") for c in row.cells]
        rows.append("| " + " | ".join(cells) + " |")
    if len(rows) >= 1:
        # header separator
        col = rows[0].count("|") - 1
        sep = "|" + "|".join(["---"] * col) + "|"
        rows.insert(1, sep)
    return "\n".join(rows)

def extract(path: Path) -> str:
    doc = Document(str(path))
    out_lines = []
    for block in iter_block_items(doc):
        from docx.text.paragraph import Paragraph
        from docx.table import Table
        if isinstance(block, Paragraph):
            t = paragraph_text(block)
            if t:
                out_lines.append(t)
        elif isinstance(block, Table):
            out_lines.append("")
            out_lines.append(table_to_md(block))
            out_lines.append("")
    return "\n".join(out_lines)

def chunk_and_write(slug: str, content: str):
    lines = content.split("\n")
    total = len(lines)
    n_chunks = (total + CHUNK_LINES - 1) // CHUNK_LINES
    manifest = {
        "slug": slug,
        "total_lines": total,
        "chunk_size": CHUNK_LINES,
        "n_chunks": n_chunks,
        "chunks": []
    }
    for i in range(n_chunks):
        start = i * CHUNK_LINES
        end = min(start + CHUNK_LINES, total)
        part = "\n".join(lines[start:end])
        chunk_name = f"{slug}__chunk{i+1:03d}.md"
        chunk_path = DST_CHUNK / chunk_name
        header = f"<!-- source: {slug}.docx | chunk {i+1}/{n_chunks} | lines {start+1}-{end}/{total} -->\n\n"
        chunk_path.write_text(header + part, encoding="utf-8")
        manifest["chunks"].append({
            "idx": i+1,
            "file": f"chunks/{chunk_name}",
            "lines": [start+1, end]
        })
    return manifest

def main():
    summary = []
    for f in sorted(SRC.glob("*.docx")):
        slug = slugify(f.name)
        print(f"[*] {f.name} → {slug}")
        try:
            content = extract(f)
        except Exception as e:
            print(f"    ERROR: {e}")
            continue
        # raw full file
        full_path = DST_RAW / f"{slug}.md"
        header = (
            f"---\n"
            f"type: raw\n"
            f"source_file: {f.name}\n"
            f"domain: qscv\n"
            f"captured_at: 2026-04-13\n"
            f"baseline: 2025-07\n"
            f"---\n\n"
            f"# {slug}\n\n"
        )
        full_path.write_text(header + content, encoding="utf-8")
        manifest = chunk_and_write(slug, content)
        summary.append({
            "source": f.name,
            "slug": slug,
            "total_lines": manifest["total_lines"],
            "n_chunks": manifest["n_chunks"],
        })
        print(f"    lines={manifest['total_lines']} chunks={manifest['n_chunks']}")
    (DST_RAW / "_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
