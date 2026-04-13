# Graph Report - .  (2026-04-13)

## Corpus Check
- Large corpus: 319 files · ~202,954 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 124 nodes · 166 edges · 10 communities detected
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_iboss 201건 지식베이스 (최재명)|iboss 201건 지식베이스 (최재명)]]
- [[_COMMUNITY_해외 시장 (대만일본동남아)|해외 시장 (대만/일본/동남아)]]
- [[_COMMUNITY_콘텐츠 AI 자동화 (FFmpeg·Whisper·TTS)|콘텐츠 AI 자동화 (FFmpeg·Whisper·TTS)]]
- [[_COMMUNITY_조직개편 & HR|조직개편 & HR]]
- [[_COMMUNITY_바이브코딩 & 에이전트 스택|바이브코딩 & 에이전트 스택]]
- [[_COMMUNITY_QSCV 문서 추출 코드|QSCV 문서 추출 코드]]
- [[_COMMUNITY_크리에이티브 & 심리 패턴|크리에이티브 & 심리 패턴]]
- [[_COMMUNITY_루솔브 퍼포먼스 캔버스 코드|루솔브 퍼포먼스 캔버스 코드]]
- [[_COMMUNITY_로고 제거 기술|로고 제거 기술]]
- [[_COMMUNITY_그래프 인덱싱 스크립트|그래프 인덱싱 스크립트]]

## God Nodes (most connected - your core abstractions)
1. `DA 크리에이티브` - 12 edges
2. `콘텐츠 AI 자동화` - 11 edges
3. `iboss 201건 인덱스 (2017-2026)` - 10 edges
4. `AI 자동화` - 9 edges
5. `동남아 틱톡샵` - 8 edges
6. `경영/재무/회계` - 8 edges
7. `AI 무중단 스튜디오 일매출 8천만` - 8 edges
8. `대만 시장` - 7 edges
9. `일본 시장` - 6 edges
10. `M&A Exit` - 6 edges

## Surprising Connections (you probably didn't know these)
- `쿠팡` --semantically_similar_to--> `네이버 GFA`  [INFERRED] [semantically similar]
  CLAUDE.md → wiki/domains/marketing-automation.md
- `Merable` --tracked_in--> `경영/재무/회계`  [INFERRED]
  CLAUDE.md → wiki/domains/finance.md
- `Rusolve` --tracked_in--> `경영/재무/회계`  [INFERRED]
  CLAUDE.md → wiki/domains/finance.md
- `스마일게이트` --counterparty--> `M&A Exit`  [EXTRACTED]
  CLAUDE.md → wiki/domains/ma-exit.md
- `네이버` --contract_succession--> `M&A Exit`  [EXTRACTED]
  CLAUDE.md → wiki/domains/ma-exit.md

## Communities

### Community 0 - "iboss 201건 지식베이스 (최재명)"
Cohesion: 0.1
Nodes (25): 누적 광고비 2,500억 집행 경험, 강남 정육점 재구매율 86% 일매출 8억, 유통 구독 사업, 공감 마케팅 7요소, 공감 > 퀄리티 (CPA 10배 차이), 마케팅 구독 사업, 제품>상세>소재>타겟>매체 우선순위, 재구매·CRM > 신규 획득 (+17 more)

### Community 1 - "해외 시장 (대만/일본/동남아)"
Cohesion: 0.12
Nodes (23): 브랜드 사업, Dual Engine Model, 이전가격 (Transfer Pricing), Rusolve 2026 런칭, 경영/재무/회계, 일본 시장, 동남아 틱톡샵, 대만 시장 (+15 more)

### Community 2 - "콘텐츠 AI 자동화 (FFmpeg·Whisper·TTS)"
Cohesion: 0.15
Nodes (17): 1초단위 7요소 추출 스키마, bob 10단계 DD Plan, 유니버설 세이프존 900×1120, 콘텐츠 AI 자동화, 세로영상 제품 하단 1/3 배치, 세이프존 플랫폼마다 재측정 필수, TTS 1.1x 최적 속도, After Effects (AE) (+9 more)

### Community 3 - "조직개편 & HR"
Cohesion: 0.14
Nodes (14): AI Cell, A→Y/Z 조직 모델, 마케팅1팀 (100% AI 파일럿), SPA 계약, 인사/총무, M&A Exit, 조직개편, 네이버 (+6 more)

### Community 4 - "바이브코딩 & 에이전트 스택"
Cohesion: 0.19
Nodes (13): AI 무중단 스튜디오 일매출 8천만, AI 실행 격차 10~100배 (2026-2027 변곡), 암묵지 추출 = AI 협업 엔진, AI 자동화, 바이브코딩, AI 자동화 시리즈 (2025-2026), bob→dd→harness→eval→learnings 파이프라인, AKOOL (AI 모델) (+5 more)

### Community 5 - "QSCV 문서 추출 코드"
Cohesion: 0.39
Nodes (8): chunk_and_write(), extract(), iter_block_items(), main(), paragraph_text(), QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플, slugify(), table_to_md()

### Community 6 - "크리에이티브 & 심리 패턴"
Cohesion: 0.25
Nodes (9): 설득 9요소 (상호성·희소성·권위 등), 제품 회피 배치 로직, 롤링발칸 (월 500~2500 소재 테스트), DA 크리에이티브, 심리학, 바이럴, 1초컷 + 상단자막 = CTR 2배, B&A Before 어둡게 / After 밝게 (+1 more)

### Community 7 - "루솔브 퍼포먼스 캔버스 코드"
Cohesion: 0.5
Nodes (3): kv(), put(), 루솔브 퍼포먼스 캔버스 v1 → xlsx (바탕화면 출력)

### Community 8 - "로고 제거 기술"
Cohesion: 0.6
Nodes (5): 로고 제거에 OpenCV 채택, src-gemini-logo-remover, LaMa가 항상 OpenCV보다 좋진 않다, LaMa / simple-lama-inpainting, OpenCV TELEA+NS

### Community 9 - "그래프 인덱싱 스크립트"
Cohesion: 0.67
Nodes (3): main(), pick_label(), Re-generate GRAPH_REPORT.md using the semantic community labels stored on each n

## Knowledge Gaps
- **46 isolated node(s):** `루솔브 퍼포먼스 캔버스 v1 → xlsx (바탕화면 출력)`, `QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG] 플`, `Re-generate GRAPH_REPORT.md using the semantic community labels stored on each n`, `스마일게이트`, `백영무 (네이버 채널컨설팅)` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components.