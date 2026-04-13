# CCFM Wiki Log

## [2026-04-13] plan | 루솔브 퍼포먼스 캔버스 v1 초안 (데이터 전 가설 베이스라인)
- 산출물: `wiki/qscv/canvas-rusolve-v1.md` (Part 7 캔버스 프레임 준용)
- 입력: 없음 (집행 전) — 전 항목 가설, USP·임상·근거는 ⏳ 수집 대기
- 구조: 본질 / 고객정의 / 경쟁·시장 / 근거 / 설득(심리) / 메시지·비주얼 / 실행플랜 / 리스크 / v2 재기획 트리거
- 페르소나 가설 2종(박준호 33 남 / 김예린 35 여), 한줄카피 A/B/C 후보
- A/B 매트릭스: USP(성분/루틴/가격) × 메시지(손실회피/자존감/근거)
- 리스크 식별: 표시광고법·의료기기 심의
- 다음 액션: 키워드/썸트렌드/경쟁사 VOC AI 리서치 → v2

## [2026-04-13] ingest | i-boss 201건 글별 상세 요약 수집 완료 (2차)
- 1차 구조화(카테고리·tacit·도메인)에서 부재했던 **글별 개별 요약**을 전량 수집
- 방식: 8개 서브에이전트 병렬 디스패치 (각 ~25건), WebFetch 201회 전량 성공 (실패 0)
- 신규: `raw/iboss/ab-6141-{번호}.md` × 201건 (프런트매터: article_id·date·category + 핵심 인사이트 5~10개)
- 신규: `raw/iboss/INDEX.md` — 카테고리·연도 분포 + 연도별 글 목록(최신순)
- 카테고리 재집계: marketing 54 · operation 43 · ai-automation 34 · psychology 22 · creative 15 · viral 14 · lesson 10 · decision-rule 7
- 연도 재집계: 2017-19(17) · 2020-21(21) · 2022(37) · 2023(33) · 2024(39) · 2025-26(54)
- 효과: "2024-07 글 요지?" 같은 글 단위 질의 가능. on-demand WebFetch 불필요

## [2026-04-13] ingest | 최재명 대표 i-boss 201건 구조화
- 소스: `Desktop/iboss.txt` (201개 URL, 2017-05-22 ~ 2026-04-12) — i-boss.co.kr ab-6141 (근육돌이 게시판)
- 집행 경험 누적: 광고비 2,500억+, 팀 100명+
- 신규 생성: `raw/inbox/2026-04-13-iboss-choi-jaemyeong-201articles.md` (불변 인덱스)
- 신규 생성: `wiki/sources/src-iboss-choi-jaemyeong.md` (소스 메타)
- 신규 생성: `wiki/domains/marketing.md` (퍼포먼스 마케팅 도메인 — 부재 상태였음)
- append: `wiki/domains/ai-automation.md` · `psychology.md` · `viral.md` (iboss 섹션)
- 암묵지 9개 파일 신규/append: decision-rules, psychology-insights, viral-patterns, market-intuition, operational-heuristics, people-dynamics, creative-patterns, lessons-learned, coding-lessons
- 업데이트: `wiki/index.md` — marketing 도메인 + src-iboss 소스 링크
- 핵심 사상 10개 추출: 제품>콘텐츠>타겟>매체 / 공감>퀄리티 / 대량테스트+롤링발칸 / USP=욕구 / 무의식+통념+권위 / 재구매>신규 / AI실행격차10~100배 / 암묵지+문제정의 / 측정·복기 / 기본기>트렌드

## [2026-04-13] ingest | Desktop/MD 시행착오 + 바이브코딩 v2.0 반영
- 소스: `C:/Users/gguy/Desktop/MD/` 다수(gemini-imagegen / PSDSKILL·PSD Replace / 메타 세팅 자동화 / TTS·다이어트 릴스 / 바이브코딩_AI협업_지침_v2.0.md)
- 업데이트: wiki/tacit/coding-lessons.md — "Desktop/MD 멀티 프로젝트 시행착오 모음" append (Gemini, PSD, Meta, TTS, Diet, 바이브코딩, 크로스 프로젝트 공통, TODO 7섹션)
- 업데이트: wiki/domains/vibe-coding.md — 스켈레톤 → v2.0 지침 반영본(5대 원인↔해법, 8-Phase, Phase별 규칙, DDD 관통, bob 순환형, /insight, 시행착오)
- 업데이트: wiki/tacit/lessons-learned.md — last_confirmed 2026-04-13
- 성격: 성공 결과가 아닌 **실패·우회·재시도·재현 불가 케이스**만 필터링해 지식화

## [2026-04-13] restructure | 도메인 카테고리 확장 (7→14)
- 신규 도메인 7개 생성:
  - vibe-coding (바이브코딩 & 클로드 스킬)
  - marketing-automation (마케팅 자동화 AI)
  - finance (경영/재무/회계)
  - hr-admin (인사/총무)
  - viral (바이럴 지식)
  - psychology (심리학 & 인간의 본질)
  - content-ai-automation (기존, 유지)
- 도메인을 5개 카테고리로 그룹핑: 시장/사업, 조직/경영, 기술/자동화, 크리에이티브/마케팅, 인문/심리
- CLAUDE.md 업데이트: 도메인 구조, 암묵지 category enum, domain enum 확장
- index.md 전면 재작성
- 암묵지 유형 3개 추가: viral-patterns, coding-lessons, psychology-insights

## [2026-04-12] ingest | DA 크리에이티브 암묵지 8건
- 소스: CEO 구두 경험칙
- 생성: wiki/tacit/creative-patterns.md (8건)
- 업데이트: wiki/domains/da-creative.md, wiki/index.md

## [2026-04-12] ingest | Gemini Logo Remover v3.0
- 소스: CEO 직접 개발 + LaMa 비교 테스트 결과
- 생성: raw/reports/gemini-logo-remover-v3.md
- 생성: wiki/sources/src-gemini-logo-remover.md
- 업데이트: wiki/domains/ai-automation.md (로고 제거 섹션 추가)
- 생성: wiki/tacit/lessons-learned.md (LaMa vs OpenCV 교훈)
- 업데이트: wiki/index.md

## [2026-04-13] ingest | 네이버 카페 크롤링 모듈 지식화

## [2026-04-13] ingest | naverapi (네이버 검색광고 + Meta 광고) 모듈 지식화

## [2026-04-13] ingest | QSCV 마케팅 서비스 품질 매뉴얼 14종 구조화
- 소스: C:\Users\gguy\Desktop\QSCV\*.docx (2025-04~ 생성, 2025-07 베이스라인)
- 추출: raw/qscv/*.md (14개) + raw/qscv/chunks/*__chunkNNN.md (47개, 200줄 단위)
- 생성: wiki/qscv/ (index + 14페이지)
  - 본부별 고객여정: design-customer-journey / media-customer-journey
  - 매체 매뉴얼: media-meta / media-google / media-gfa / media-search-ads
  - 사고 프레임: performance-thinking
  - Appendix 7종: aov / landing / detail-page / video-planning / image-planning / content-guide / canvas-reupdate
- 업데이트: wiki/index.md 에 QSCV 섹션 추가
- 향후: 사용자가 베이스라인 위에 실무 변경·암묵지 증분 업데이트
