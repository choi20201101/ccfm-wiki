# Graph Report - .  (2026-04-13)

## Corpus Check
- Large corpus: 318 files · ~202,076 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 93 nodes · 123 edges · 11 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_AI 자동화 & 스킬 파이프라인|AI 자동화 & 스킬 파이프라인]]
- [[_COMMUNITY_조직개편 & HR|조직개편 & HR]]
- [[_COMMUNITY_해외 시장 (대만일본동남아)|해외 시장 (대만/일본/동남아)]]
- [[_COMMUNITY_QSCV 문서 추출 코드|QSCV 문서 추출 코드]]
- [[_COMMUNITY_M&A Exit & 재무|M&A Exit & 재무]]
- [[_COMMUNITY_크리에이티브 & 심리 패턴|크리에이티브 & 심리 패턴]]
- [[_COMMUNITY_본사 사업마케팅 (최재명·네이버·GFA)|본사 사업/마케팅 (최재명·네이버·GFA)]]
- [[_COMMUNITY_루솔브 퍼포먼스 캔버스 코드|루솔브 퍼포먼스 캔버스 코드]]
- [[_COMMUNITY_로고 제거 기술|로고 제거 기술]]
- [[_COMMUNITY_AI 아바타영상 툴|AI 아바타/영상 툴]]
- [[_COMMUNITY_그래프 인덱싱 스크립트|그래프 인덱싱 스크립트]]

## God Nodes (most connected - your core abstractions)
1. `콘텐츠 AI 자동화` - 11 edges
2. `DA 크리에이티브` - 9 edges
3. `동남아 틱톡샵` - 8 edges
4. `경영/재무/회계` - 8 edges
5. `대만 시장` - 7 edges
6. `일본 시장` - 6 edges
7. `M&A Exit` - 6 edges
8. `조직개편` - 6 edges
9. `AI 자동화` - 6 edges
10. `extract()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `쿠팡` --semantically_similar_to--> `네이버 GFA`  [INFERRED] [semantically similar]
  CLAUDE.md → wiki/domains/marketing-automation.md
- `최재명 (CEO)` --authored--> `src-gemini-logo-remover`  [EXTRACTED]
  CLAUDE.md → wiki/sources/src-gemini-logo-remover.md
- `Merable` --tracked_in--> `경영/재무/회계`  [INFERRED]
  CLAUDE.md → wiki/domains/finance.md
- `Rusolve` --tracked_in--> `경영/재무/회계`  [INFERRED]
  CLAUDE.md → wiki/domains/finance.md
- `스마일게이트` --counterparty--> `M&A Exit`  [EXTRACTED]
  CLAUDE.md → wiki/domains/ma-exit.md

## Communities

### Community 0 - "AI 자동화 & 스킬 파이프라인"
Cohesion: 0.16
Nodes (15): 1초단위 7요소 추출 스키마, bob 10단계 DD Plan, 유니버설 세이프존 900×1120, AI 자동화, 콘텐츠 AI 자동화, 바이브코딩, bob→dd→harness→eval→learnings 파이프라인, 세로영상 제품 하단 1/3 배치 (+7 more)

### Community 1 - "조직개편 & HR"
Cohesion: 0.14
Nodes (14): AI Cell, A→Y/Z 조직 모델, 마케팅1팀 (100% AI 파일럿), SPA 계약, 인사/총무, M&A Exit, 조직개편, 네이버 (+6 more)

### Community 2 - "해외 시장 (대만/일본/동남아)"
Cohesion: 0.18
Nodes (14): 일본 시장, 동남아 틱톡샵, 대만 시장, Merable TW, 강용길 (컴플라이언스), Q10 메가세일, 샵라인 (Shopline), 틱톡샵 (+6 more)

### Community 3 - "QSCV 문서 추출 코드"
Cohesion: 0.39
Nodes (8): chunk_and_write(), extract(), iter_block_items(), main(), paragraph_text(), QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플, slugify(), table_to_md()

### Community 4 - "M&A Exit & 재무"
Cohesion: 0.28
Nodes (9): 브랜드 사업, Dual Engine Model, 이전가격 (Transfer Pricing), Rusolve 2026 런칭, 경영/재무/회계, Merable, Merable HK (홍콩법인), Rusolve (+1 more)

### Community 5 - "크리에이티브 & 심리 패턴"
Cohesion: 0.33
Nodes (7): 제품 회피 배치 로직, DA 크리에이티브, 심리학, 바이럴, 1초컷 + 상단자막 = CTR 2배, B&A Before 어둡게 / After 밝게, 첫 프레임 얼굴 = 리텐션 30%↑

### Community 6 - "본사 사업/마케팅 (최재명·네이버·GFA)"
Cohesion: 0.29
Nodes (7): 유통 구독 사업, 마케팅 구독 사업, 마케팅 자동화, CCFM 콘크리트파머스, 최재명 (CEO), 쿠팡, 네이버 GFA

### Community 7 - "루솔브 퍼포먼스 캔버스 코드"
Cohesion: 0.5
Nodes (3): kv(), put(), 루솔브 퍼포먼스 캔버스 v1 → xlsx (바탕화면 출력)

### Community 8 - "로고 제거 기술"
Cohesion: 0.6
Nodes (5): 로고 제거에 OpenCV 채택, src-gemini-logo-remover, LaMa가 항상 OpenCV보다 좋진 않다, LaMa / simple-lama-inpainting, OpenCV TELEA+NS

### Community 9 - "AI 아바타/영상 툴"
Cohesion: 0.6
Nodes (5): Creatify Aurora, fal.ai, Kling i2v / Avatar Pro, OmniHuman v1.5 (ByteDance), Rhubarb Lip Sync

### Community 10 - "그래프 인덱싱 스크립트"
Cohesion: 0.67
Nodes (1): Re-generate GRAPH_REPORT.md using the semantic community labels stored on each n

## Knowledge Gaps
- **33 isolated node(s):** `루솔브 퍼포먼스 캔버스 v1 → xlsx (바탕화면 출력)`, `QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플`, `Re-generate GRAPH_REPORT.md using the semantic community labels stored on each n`, `스마일게이트`, `백영무 (네이버 채널컨설팅)` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.