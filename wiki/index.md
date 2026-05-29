# CCFM Wiki Index

> 🔥 = 허브(god node) · 🌐 = 교차 도메인 · 📄 = 미작성/스텁
> 최종 정리: 2026-05-29
> ⚡ **빠른 꺼내쓰기**: [[HOTSHEET]] (트리거 → 답 직입식 단축표)
> 🕸️ **그래프**: 691 노드 · 1723 엣지 · 156 커뮤니티 ([[../graphify-out/GRAPH_REPORT|GRAPH_REPORT]])
> 재빌드: `python scripts/build_wiki_graph.py` → `inject_iboss_entities.py` → `regen_graph_report.py`

---

## 🕸️ 그래프 기반 진입점 (Graph Navigation)

> 가장 많이 연결된 노드 = 위키에서 실제로 가장 자주 호출되는 지점. 모르면 여기서 시작.

| Rank | God Node | 연결 | 들어가는 곳 |
|---|---|---|---|
| 1 | i-boss 201건 지식베이스 (최재명) | 224 | [[sources/src-iboss-choi-jaemyeong]] · [[../raw/iboss/INDEX]] |
| 2 | 퍼포먼스 마케팅 | 80 | [[domains/marketing]] |
| 3 | AI 자동화 | 73 | [[domains/ai-automation]] |
| 4 | 운영 노하우 | 53 | [[tacit/operational-heuristics]] |
| 5 | DA 크리에이티브 | 52 | [[domains/da-creative]] |
| 6 | 소비자 심리 | 41 | [[domains/psychology]] |
| 7 | 바이럴 · 콘텐츠 AI | 40 | [[domains/viral]] · [[domains/content-ai-automation]] |

**최대 커뮤니티**: 크리에이티브&심리(121) · 바이브코딩&에이전트(67) · 해외시장(39) · iboss(38) · 본사 사업/마케팅(32) · 조직개편&HR(28)

---

## 🔥 핵심 지식 (Quick Access)

- [[tacit/coding-lessons]] — 자동화·크롤링·헤드리스 실전 차오. 위키 최대 코딩 노하우.
- [[tacit/creative-patterns]] — 1초컷·세이프존·후킹 등 크리에이티브 감각.
- [[tacit/video-gen-lessons]] — Kling/Veo/Omni 영상 생성 교훈.
- [[tacit/operational-heuristics]] — 운영 판단 기준 (god node #4).
- [[domains/gfa-setting-automation]] · [[qscv/media-gfa]] — 네이버 GFA 자동화/세팅.
- [[sources/src-geo-aeo-guide]] — **GEO/AEO 실행 가이드**. 블로그/워드프레스/구글 글 발행 자동화의 기준 프레임 (필수).
- [[domains/psychology]] · [[tacit/psychology-insights]] — 설득·소비자 심리.
- [[수치-단위-착각-방지-규칙]] — 매출 데이터 억 단위 변환 시 법인별 스케일 착각 방지.
- [[../CLAUDE.md]] — 위키 스키마 + 자동 동작 규칙(캡처/암묵지 추출/그래프 되먹임).

---

## 🌐 도메인 (Domains)

**시장/사업** · [[domains/taiwan-market]] · [[domains/japan-market]] · [[domains/sea-tiktok]] · [[domains/ma-exit]]

**조직/경영** · [[domains/org-restructure]] · [[domains/finance]] · [[domains/hr-admin]]

**기술/자동화** · [[domains/ai-automation]] · [[domains/vibe-coding]] · [[domains/content-ai-automation]] · [[domains/marketing-automation]] · [[domains/codex-grounding-protocol]] · [[domains/gfa-setting-automation]] · [[domains/seebio-radio-pipeline]]

**크리에이티브/마케팅** · [[domains/marketing]] · [[domains/da-creative]] · [[domains/viral]] · [[domains/ggttt-imagen]] · [[domains/gptim-ad-creative-batch]] · [[domains/skin-care-13cut-pattern]]

**리서치/플레이북** · [[domains/market-research-playbook]] · [[domains/usp-performance-canvas-research]] · [[domains/competitor-ad-research]] · [[domains/instagram-content-research]] · [[domains/todayhumor-mining-playbook]] · [[domains/grill-me-ccfm]]

**심리** · [[domains/psychology]]

---

## 🧠 암묵지 (Tacit)

[[tacit/decision-rules]] · [[tacit/operational-heuristics]] · [[tacit/people-dynamics]] · [[tacit/market-intuition]] · [[tacit/lessons-learned]] · [[tacit/creative-patterns]] · [[tacit/viral-patterns]] · [[tacit/psychology-insights]] · [[tacit/coding-lessons]] · [[tacit/video-gen-lessons]] · [[tacit/chatgpt-web-automation]] · [[tacit/meta-ad-library-search]] · [[tacit/ugc-before-after-proof]] · [[tacit/lipsync-multi-face-trap]] · [[tacit/ae-aep-default-v25]] · [[tacit/yuri-ep02-bj-vlog-case]]

---

## 📐 QSCV (퍼포먼스 캔버스)

진입: [[qscv/index]] · 사고틀 [[qscv/performance-thinking]] · 캔버스 [[qscv/canvas-rusolve-v1]]
미디어 · [[qscv/media-gfa]] · [[qscv/media-meta]] · [[qscv/media-google]] · [[qscv/media-search-ads]]
여정 · [[qscv/design-customer-journey]] · [[qscv/media-customer-journey]]
부록 · [[qscv/appendix-landing]] · [[qscv/appendix-detail-page]] · [[qscv/appendix-image-planning]] · [[qscv/appendix-video-planning]] · [[qscv/appendix-content-guide]] · [[qscv/appendix-aov]] · [[qscv/appendix-canvas-reupdate]]

---

## 📚 소스 (Sources) — `wiki/sources/` (40+건)

최근/핵심: [[sources/src-geo-aeo-guide]] · [[sources/src-winnersojae-feedback-2026-05-20]] · [[sources/src-iboss-choi-jaemyeong]] · [[sources/src-gemini-omni-guide]] · [[sources/src-nari-chatgpt-image]] · [[sources/src-creative-autogen-framework]] · [[sources/src-foreign-influencer-guide]]
리서치: [[research/2026-05-20_기미크림-퍼포먼스요소]]

---

## 🔧 Lint / 정리 필요 (2026-05-29 진단)

- **고립 파일 다수**: 문서 고아 111개 중 **108개가 `raw/`**(iboss 201건 원문 등). raw는 불변·MOC로 조직되므로 정상 — 건드리지 않음. 가치 있는 신규 raw만 `wiki/sources/`로 요약·링크.
- **그래프 빌드 복원**: 마크다운→그래프 파이프라인(`scripts/build_wiki_graph.py`)을 신규 작성해 커밋. 이전엔 gitignore된 일회성 스크립트라 유실됐었음. 이제 재현 가능.
- **2026-05-29 정리 완료**: `_sync-test.md`(테스트 잔재) 삭제 · `수치-단위-착각-방지-규칙`(고아) → [[domains/finance]]에서 링크 연결.
- **교차참조 보강 후보**: `domains/seebio-radio-pipeline`, `domains/skin-care-13cut-pattern` 등 신규 도메인의 인바운드 링크가 적음 → 관련 tacit/source에서 역링크 추가.
- **graphify 한계**: 설치된 graphify의 `extract()`는 코드(AST) 전용·LLM 미사용. document 노드는 본 빌더가 생성하므로, 새 .md 추가 후엔 위 재빌드 3종을 실행해야 index/그래프가 갱신됨.

---

*Part of the graphify knowledge wiki. 네비게이션은 [[../CLAUDE.md]] 스키마를 따른다.*
