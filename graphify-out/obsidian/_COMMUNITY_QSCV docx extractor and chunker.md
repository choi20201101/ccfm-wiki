---
type: community
cohesion: 1.00
members: 2
---

# QSCV docx extractor and chunker

**Cohesion:** 1.00 - tightly connected
**Members:** 2 nodes

## Members
- [[Inject H1 title into frontmatter aliases]] - code - scripts/inject_aliases_from_h1.py
- [[QSCV docx extractor and chunker]] - code - raw/qscv/_extract_and_chunk.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/QSCV_docx_extractor_and_chunker
SORT file.name ASC
```
