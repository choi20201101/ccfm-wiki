# Graph Report - .  (2026-04-13)

## Corpus Check
- Corpus is ~5,657 words - fits in a single context window. You may not need a graph.

## Summary
- 76 nodes · 102 edges · 9 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_AI 자동화 & 스킬 파이프라인|AI 자동화 & 스킬 파이프라인]]
- [[_COMMUNITY_해외 시장 (대만일본동남아)|해외 시장 (대만/일본/동남아)]]
- [[_COMMUNITY_브랜드재무법인|브랜드/재무/법인]]
- [[_COMMUNITY_조직개편 & HR|조직개편 & HR]]
- [[_COMMUNITY_크리에이티브 & 심리 패턴|크리에이티브 & 심리 패턴]]
- [[_COMMUNITY_본사 사업마케팅|본사 사업/마케팅]]
- [[_COMMUNITY_M&A Exit|M&A Exit]]
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
10. `Merable` - 5 edges

## Surprising Connections (you probably didn't know these)
- `네이버 GFA` --semantically_similar_to--> `쿠팡`  [INFERRED] [semantically similar]
  wiki/domains/marketing-automation.md → CLAUDE.md
- `최재명 (CEO)` --authored--> `src-gemini-logo-remover`  [EXTRACTED]
  CLAUDE.md → wiki/sources/src-gemini-logo-remover.md
- `Merable` --expands_to--> `대만 시장`  [EXTRACTED]
  CLAUDE.md → wiki/domains/taiwan-market.md
- `Merable` --expands_to--> `일본 시장`  [EXTRACTED]
  CLAUDE.md → wiki/domains/japan-market.md
- `Merable` --expands_to--> `동남아 틱톡샵`  [EXTRACTED]
  CLAUDE.md → wiki/domains/sea-tiktok.md

## Hyperedges (group relationships)
- **해외시장 동시 전개 (대만/동남아/일본)** — domain_taiwan_market, domain_sea_tiktok, domain_japan_market [EXTRACTED 1.00]
- **M&A Exit-조직개편-재무 3중 연동** — domain_ma_exit, domain_org_restructure, domain_finance [INFERRED 0.85]
- **AI 아바타 파이프라인 스택** — tool_elevenlabs, tool_omnihuman, tool_fal_ai [EXTRACTED 1.00]

## Communities

### Community 0 - "AI 자동화 & 스킬 파이프라인"
Cohesion: 0.16
Nodes (15): 1초단위 7요소 추출 스키마, bob 10단계 DD Plan, 유니버설 세이프존 900×1120, AI 자동화, 콘텐츠 AI 자동화, 바이브코딩, bob→dd→harness→eval→learnings 파이프라인, 세로영상 제품 하단 1/3 배치 (+7 more)

### Community 1 - "해외 시장 (대만/일본/동남아)"
Cohesion: 0.18
Nodes (14): 일본 시장, 동남아 틱톡샵, 대만 시장, Merable TW, 강용길 (컴플라이언스), Q10 메가세일, 샵라인 (Shopline), 틱톡샵 (+6 more)

### Community 2 - "브랜드/재무/법인"
Cohesion: 0.28
Nodes (9): 브랜드 사업, Dual Engine Model, 이전가격 (Transfer Pricing), Rusolve 2026 런칭, 경영/재무/회계, Merable, Merable HK (홍콩법인), Rusolve (+1 more)

### Community 3 - "조직개편 & HR"
Cohesion: 0.25
Nodes (8): AI Cell, A→Y/Z 조직 모델, 마케팅1팀 (100% AI 파일럿), 인사/총무, 조직개편, 한태영 CD, 신동협 (AI Cell 리더 후보), 윤지민 CD

### Community 4 - "크리에이티브 & 심리 패턴"
Cohesion: 0.33
Nodes (7): 제품 회피 배치 로직, DA 크리에이티브, 심리학, 바이럴, 1초컷 + 상단자막 = CTR 2배, B&A Before 어둡게 / After 밝게, 첫 프레임 얼굴 = 리텐션 30%↑

### Community 5 - "본사 사업/마케팅"
Cohesion: 0.29
Nodes (7): 유통 구독 사업, 마케팅 구독 사업, 마케팅 자동화, CCFM 콘크리트파머스, 최재명 (CEO), 쿠팡, 네이버 GFA

### Community 6 - "M&A Exit"
Cohesion: 0.33
Nodes (6): SPA 계약, M&A Exit, 네이버, 스마일게이트, 우영회계법인, 백영무 (네이버 채널컨설팅)

### Community 7 - "로고 제거 기술"
Cohesion: 0.6
Nodes (5): 로고 제거에 OpenCV 채택, src-gemini-logo-remover, LaMa가 항상 OpenCV보다 좋진 않다, LaMa / simple-lama-inpainting, OpenCV TELEA+NS

### Community 8 - "AI 아바타/영상 툴"
Cohesion: 0.6
Nodes (5): Creatify Aurora, fal.ai, Kling i2v / Avatar Pro, OmniHuman v1.5 (ByteDance), Rhubarb Lip Sync

## Knowledge Gaps
- **30 isolated node(s):** `스마일게이트`, `백영무 (네이버 채널컨설팅)`, `신동협 (AI Cell 리더 후보)`, `강용길 (컴플라이언스)`, `한태영 CD` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `콘텐츠 AI 자동화` connect `AI 자동화 & 스킬 파이프라인` to `AI 아바타/영상 툴`, `크리에이티브 & 심리 패턴`, `본사 사업/마케팅`?**
  _High betweenness centrality (0.303) - this node is a cross-community bridge._
- **Why does `바이럴` connect `크리에이티브 & 심리 패턴` to `AI 자동화 & 스킬 파이프라인`, `해외 시장 (대만/일본/동남아)`?**
  _High betweenness centrality (0.283) - this node is a cross-community bridge._
- **Why does `동남아 틱톡샵` connect `해외 시장 (대만/일본/동남아)` to `브랜드/재무/법인`, `크리에이티브 & 심리 패턴`?**
  _High betweenness centrality (0.273) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `경영/재무/회계` (e.g. with `Merable` and `Rusolve`) actually correct?**
  _`경영/재무/회계` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `스마일게이트`, `백영무 (네이버 채널컨설팅)`, `신동협 (AI Cell 리더 후보)` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._