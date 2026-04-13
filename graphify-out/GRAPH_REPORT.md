# Graph Report - .  (2026-04-13)

## Corpus Check
- Large corpus: 318 files · ~201,999 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 90 nodes · 121 edges · 10 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_해외 시장 (대만일본동남아)|해외 시장 (대만/일본/동남아)]]
- [[_COMMUNITY_AI 자동화 & 스킬 파이프라인|AI 자동화 & 스킬 파이프라인]]
- [[_COMMUNITY_M&A Exit & 재무|M&A Exit & 재무]]
- [[_COMMUNITY_QSCV 문서 추출 코드|QSCV 문서 추출 코드]]
- [[_COMMUNITY_조직개편 & HR|조직개편 & HR]]
- [[_COMMUNITY_크리에이티브 & 심리 패턴|크리에이티브 & 심리 패턴]]
- [[_COMMUNITY_본사 사업마케팅 (최재명·네이버·GFA)|본사 사업/마케팅 (최재명·네이버·GFA)]]
- [[_COMMUNITY_루솔브 퍼포먼스 캔버스 코드|루솔브 퍼포먼스 캔버스 코드]]
- [[_COMMUNITY_로고 제거 기술|로고 제거 기술]]
- [[_COMMUNITY_AI 아바타영상 툴|AI 아바타/영상 툴]]

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

## Hyperedges (group relationships)
- **해외시장 동시 전개 (대만/동남아/일본)** — domain_taiwan_market, domain_sea_tiktok, domain_japan_market [EXTRACTED 1.00]
- **M&A Exit-조직개편-재무 3중 연동** — domain_ma_exit, domain_org_restructure, domain_finance [INFERRED 0.85]
- **AI 아바타 파이프라인 스택** — tool_elevenlabs, tool_omnihuman, tool_fal_ai [EXTRACTED 1.00]

## Communities

### Community 0 - "해외 시장 (대만/일본/동남아)"
Cohesion: 0.14
Nodes (18): 브랜드 사업, Rusolve 2026 런칭, 일본 시장, 동남아 틱톡샵, 대만 시장, Merable, Merable TW, Rusolve (+10 more)

### Community 1 - "AI 자동화 & 스킬 파이프라인"
Cohesion: 0.15
Nodes (16): 1초단위 7요소 추출 스키마, bob 10단계 DD Plan, 유니버설 세이프존 900×1120, AI 자동화, 콘텐츠 AI 자동화, 바이브코딩, bob→dd→harness→eval→learnings 파이프라인, 세로영상 제품 하단 1/3 배치 (+8 more)

### Community 2 - "M&A Exit & 재무"
Cohesion: 0.2
Nodes (11): Dual Engine Model, SPA 계약, 이전가격 (Transfer Pricing), 경영/재무/회계, M&A Exit, Merable HK (홍콩법인), 네이버, 스마일게이트 (+3 more)

### Community 3 - "QSCV 문서 추출 코드"
Cohesion: 0.39
Nodes (8): chunk_and_write(), extract(), iter_block_items(), main(), paragraph_text(), QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플, slugify(), table_to_md()

### Community 4 - "조직개편 & HR"
Cohesion: 0.25
Nodes (8): AI Cell, A→Y/Z 조직 모델, 마케팅1팀 (100% AI 파일럿), 인사/총무, 조직개편, 한태영 CD, 신동협 (AI Cell 리더 후보), 윤지민 CD

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
Cohesion: 0.83
Nodes (4): Creatify Aurora, fal.ai, Kling i2v / Avatar Pro, OmniHuman v1.5 (ByteDance)

## Knowledge Gaps
- **32 isolated node(s):** `루솔브 퍼포먼스 캔버스 v1 → xlsx (바탕화면 출력)`, `QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플`, `스마일게이트`, `백영무 (네이버 채널컨설팅)`, `신동협 (AI Cell 리더 후보)` (+27 more)
  These have ≤1 connection - possible missing edges or undocumented components.