# CCFM Wiki Log

## [2026-04-14] ingest | goglecc — 씨드 이미지 수집·큐레이션 파이프라인
- 원본: `C:/Users/gguy/Desktop/goglecc/` (BDH 구조, bing scraper + negative curation + fal LoRA 준비)
- 신규 소스: [[src-goglecc-seed-curation]]
  - Google 차단 → Bing 우회 (`a.iusc[m].murl`)
  - Negative curation (aa/ 폴더 학습) > Positive (10장 선별)
  - 안 좋은 이미지 정량 시그니처: saturation_std>0.17, aspect≈1.55, width<556, phash Hamming≤12
  - 키워드 bad률 상관: 단일명사 4% vs 합성어 59~91%
- tacit 신규:
  - [[coding-lessons]] 4건: Google 차단/Bing 우회, Negative curation 효율성, 키워드 품질 상관, pHash 블랙리스트
  - [[creative-patterns]] 3건: AI tell 제거 프롬프트 스택, aesthetic LoRA vs subject LoRA, Higgsfield/Nano Banana 철학 차이
- 의의: 다이어트 B&A v2의 씨드 입력 자산을 체계적으로 확보하는 선행 파이프라인. "인플루언서 씨드 가져와줘" 류 요청에 재사용.

## [2026-04-14] ingest | diet-b2a-v2 — 대량생산·다국어 확장 (60영상, Gemini+Kling+ffmpeg bdh)
- 원본: `raw/skills/diet-b2a-v2/` + `diet-b2a-v2-skill.zip` (140KB), 바탕화면 동일본
- 신규 소스: [[src-diet-b2a-v2]] (10세트·2언어 파이프라인, 스텝별 bdh 구조)
- domains 업데이트: [[content-ai-automation]] · [[da-creative]] · [[ai-automation]] (v2 추가)
- tacit 신규 9건:
  - [[creative-patterns]] 3건: before/after 각각 박스 필수, 유행 댄스명 고유명사 박기, 영문 자막 → 한국어 자극 훅
  - [[coding-lessons]] 5건: Gemini Thinking 강제 선택, after 시드에 before 입력 금지, Gemini 거부 우회 3패턴(AI캐릭터/의상완화/safe fallback), OpenCV haarcascade 오검출 패턴, 프롬프트 짧게(40~60s vs 3분+타임아웃)
- 의의: v1 스킬 실전 대량 운영시 나타난 품질/세션/안전 이슈를 체계화. 직원 공유 가능한 압축 패키지.

## [2026-04-13] ingest | diet-b2a 스킬 — 다이어트 B/A 릴스 3종 자동화 (bdh 완주 사례)
- 원본: `raw/skills/diet-b2a/` (트리 전부) + `raw/skills/diet-b2a/diet-b2a-skill.zip` (35KB)
- 스킬 위치: 사용자 바탕화면 `C:\Users\gguy\Desktop\diet-b2a-skill.zip`, 소스는 `C:\Users\gguy\Desktop\dance\diet-b2a-skill\`
- 신규 소스 페이지: [[src-diet-b2a-skill]] (SKILL/PLAN/HOOK/ARCHITECTURE/USAGE 요약 + 관련 페이지 링크)
- 도메인 append: [[content-ai-automation]] §9, [[da-creative]] 레이아웃 레퍼런스, [[ai-automation]] bdh 완주 사례
- 암묵지 신규:
  - [[creative-patterns]] 5건 (하드컷 매칭 포즈, 전반억제→후반폭발, 모자이크 범위, 자막-박스 여백, 1-2-3 시퀀스)
  - [[coding-lessons]] 6건 (cp949 em-dash, Kling 10s>5s 포즈 준수, xfade vs 매칭컷, split=2 loop, 멱등 이중체크, JWT 재발급)
  - [[psychology-insights]] 2건 (억제→해방 릴스 구조, 모자이크 과다 시 몰입 저하)
- index.md Sources 섹션에 링크 추가
- 파이프라인 의의: bob(PLAN.md) → dd(steps/00~05) → harness(RULES.md 10조) 3단 완주한 **첫 프로덕션 스킬** — 향후 B/A 류 콘텐츠 스킬 제작의 레퍼런스
- 재사용 벡터: `config/default.json` 의 5개 슬롯(이미지 4 + 카피 5 + face_box + audio 3 + kling 설정)만 편집하면 새 인물 프로젝트

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
## [2026-04-13] ingest | community 모듈 본문/댓글 수집 추가 + 지식화
- 신규: `market-research-package/modules/community/detail_fetcher.py` (5개 사이트 opt-in fetcher)
- 변경: `crawler.py`(`_enrich_detail` 훅), `config.py`(`FETCH_DETAIL`), `run.py`(`--with-detail`), `README.md`
- 위키: `wiki/sources/src-community.md` 신규, `wiki/tacit/coding-lessons.md` append, `domains/marketing-automation.md`·`viral.md` 링크 추가

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

## [2026-04-13] skills-ingest | 로드된 스킬 전수 조사 → content-ai-automation §8 (영상 자동화 파이프라인 교훈 12개) 추가

## [2026-04-13] ingest | 릴스 zh-TW 번역/더빙 작업 암묵지
- 출처: DW1X3RRk_7Q 세션 (자막 OCR 신뢰 실패 → STT 교정, 번체 번역, ElevenLabs v3 Yun 보이스)
- coding-lessons.md: STT 검증, whisper 모델 크기, ElevenLabs v3 우위, 중국어 네이티브 보이스, atempo fit, malgunbd 폰트
- creative-patterns.md: 세로 자막 위치 20% 상향, 다국어 CTA 노란색 유지

## [2026-04-13] refactor | 다국어 릴스 교훈을 규칙→질문 체크리스트로 재구성
- 사용자 피드백: "영상마다 변수가 달라서 무조건 규칙화 금지, 질문 체크리스트로 저장"
- coding-lessons.md: 자막/STT/ElevenLabs/atempo/폰트 7개 Q 체크리스트로 재작성
- creative-patterns.md: 자막 위치/CTA 컬러/다국어 스타일 3개 Q로 재작성
- decision-rules.md: 메타 원칙("영상 작업은 규칙화 금지, 질문 체크리스트화") 추가
## [2026-04-13] ingest | youtube 모듈 지식화
## [2026-04-13] ingest | instar 모듈 지식화

## [2026-04-14] ingest | Gemini 레퍼런스 기반 프롬프트 포맷 (실사 질감 + safety 우회)
- [[da-creative]] 프롬프트 DB 섹션에 템플릿·예시·운용팁 추가
- [[coding-lessons]] 2026-04-14 엔트리 추가 (confidence: medium)
- 출처: diet-b2a-v2 실전 검증 + 사용자 스크린샷 (20260414_142011.png)
