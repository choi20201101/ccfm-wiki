# CCFM Wiki Log

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
