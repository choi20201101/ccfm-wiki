# CCFM Wiki Index

> 🔥 = 활발 (커밋 4+) · 📘 = 참조용 (커밋 2-3) · 💤 = 미작성 스텁
> 최종 정리: 2026-04-29
> 🚀 **빠른 꺼내쓰기**: [[HOTSHEET]] (트리거 → 진입점 단축표)

---

## 🔥 핵심 지식 (Quick Access)

가장 자주 쓰이고 지속 업데이트되는 지식. 작업 시 여기서 시작.

### 코딩/자동화 교훈 — [[tacit/coding-lessons]] (67KB, 15커밋)
위키 최대 파일. 실전 시행착오 전부 축적.
- §1 네이버 카페 크롤링/가입 자동화 — 쿠키, 셀렉터, 캡차, 회피 전략
- §2 재사용 가능한 크롤링 패턴 — OCR 캡차, iframe 우회, 안티패턴 체크리스트
- §3 네이버 검색광고 API + Meta 광고 분석 — 인증, 키워드 휴리스틱, 스크래핑
- §4 Desktop/MD 멀티 프로젝트 시행착오 — Gemini, PSD, Meta, TTS, 바이브코딩 전반
- §5 i-boss 201건 AI 자동화 교훈 — 프롬프트 설계, 5 Why, AI 도입 로드맵
- §6 다국어 릴스 자막/더빙 체크리스트 — STT 모델, TTS 모델, 폰트, 길이 매칭
- §7 Google Images 씨드용 원본 다운로더 (2026-04-27) — non-headless+stealth+Referer, 사이드패널 원본 추출
- §8 키워드 기반 YouTube/Instagram 썸네일 수집 (2026-04-29) — yt-dlp `sp=` 날짜필터, instaloader 폐기/DrissionPage 우회, 인터리브 다운로드

### 크리에이티브 패턴 — [[tacit/creative-patterns]] (16KB, 10커밋)
영상/이미지/레이아웃 실전 감각.
- 영상 편집: 1초컷+상단자막=CTR 2배, 첫프레임 얼굴=리텐션 30%↑, TTS 1.1x
- 이미지: B&A 보정 (Before 어둡게/After 밝게)
- 세이프존: 세로 영상 제품 하단 1/3, 플랫폼마다 재측정
- AI 생성: AI tell 제거 프롬프트, Reference 누수→aesthetic LoRA, Gemini 직호출 기본값
- B/A 레시피: 예쁜 얼굴+통통 몸 생성 확정 포맷
- i-boss 추출: 퍼포먼스 영상 7단 황금률, B&A 3가지 우회, 후킹 6기법, GFA 황금구도
- 다국어 자막 스타일 Q&A, 얼굴 모자이크 규칙, 댄스명 프롬프트 규칙

### 콘텐츠 AI 자동화 — [[domains/content-ai-automation]] (35KB, 8커밋)
컷편집~업로드까지 전체 파이프라인.
- §1 컷편집 (FFmpeg) — 트림, xfade 전환, Smart Trim, 퍼포먼스 광고 7씬 구조
- §2 영상 비전 분석 (Gemini/Claude Vision) — 1초 단위 7요소, 템플릿, 모션 L2 프리셋
- §3 Whisper STT — 타임스탬프, TTS 길이 매칭 3단계, AE 자막 7단계
- §4 자막 레이아웃 + 세이프존 — 플랫폼별 데드존, 유니버설 세이프존
- §5 bob 구조 계획서 — DD Plan 10단계, AI 평가 루프
- §6 DA 크리에이티브 디자인 시스템
- §8 스킬 파이프라인 교훈 — harness, eval, learnings 영상 적용
- §9 diet-b2a 릴스 자동화 — bdh 완주 케이스, 3종 영상, ffmpeg 재사용 패턴
- §10 diet-b2a-v2 대량생산 — Gemini 시드, 10세트×3×2언어=60영상
- §11-12 IG릴스 자동업로드 (instarup)
- §13 외국인 인플루언서 리뷰 33편 (fal.ai+Kling Avatar v2 Pro)

### DA 크리에이티브 — [[domains/da-creative]] (6KB, 5커밋)
- API 선택 원칙 (Gemini 직호출 기본값, 2026-04-14 확정)
- Gemini 레퍼런스 기반 한국어 프롬프트 포맷
- diet-b2a 레이아웃 레퍼런스 (캔버스, 오버레이, 자막 폰트, 모자이크, 데드존)

### 영상 생성 교훈 — [[tacit/video-gen-lessons]] (27KB, 34 섹션)
Kling/Gemini/ffmpeg 실전 이슈 전체 집합.
- §1 Kling 1003 에러 = 시계 drift · §2 자막 싱크 성공 패턴
- §3 중년 타겟 번역 원칙 · §4 상단 고정 카피 · §5 B-roll 할루시네이션 방지
- §6 Gemini Vision 자동 Eval · §7 퍼포먼스 영상 3가지 스타일
- §8 씬당 듀레이션 · §9 TTS 경로 · §10 비용 경험치
- §11 FFmpeg filter 디버깅 · §14 Gemini 한국어 텍스트 이미지 불가
- §15 ffmpeg 필터 함정 · §16 안 되면 스킵할 것들
- **§17-19 볼륨필인 Day별 변화** — 얼굴형 시드 분리, 그래픽 도트 금지 웻룩, Kling 얼굴 스무딩 방지 (2026-04-21)
- **§20-25 Trio 릴레이 · 구조 해시 · CTA 풀 · 숫자 오독 방지** (2026-04-21)
- **§26-34 참조 이미지 인페인팅 · 금지 키워드(shadow/silhouette) · Day14 옷 변경 · 3D 세포 애니 · Kling reveal · 17s 표준 구조** (2026-04-23)
- **§41 Seedance 2.0 / Veo3 / Sora2 보이스 일관성** (2026-05-02) — 4지선다 비교, Voice Conversion(RVC/ElevenLabs)이 1순위, lip-sync는 2순위, 의사결정 트리·비용 표
- **§42 광고 영상 후처리 합성 표준** (2026-05-02) — 원본음성 + ASS 자막 burn-in + 16:9 1080p, freeze 화면 금지·청크 1.8s/18자·subtitles 필터 윈도우 함정. Reference: `Desktop/bj/v_output/scripts/v2_compose.py`

### 마케팅 자동화 — [[domains/marketing-automation]] (4커밋)
- 네이버 카페 크롤러, 네이버 API, 인스타 수집, 유튜브, 커뮤니티 크롤링

### 🔥 grill-me-ccfm — 결정 분기 캐묻기 스킬 (NEW 2026-05-02)
**"grill해줘" / "방향 잡아줘" / "하지 말아야 할 거" / 신규 시장·조직개편 등 되돌리기 어려운 결정 입력 시 자동 발동.**
- bob 앞단 자동 게이트 (`scripts/ambiguity_scorer.py` 점수 ≥ 5)
- 4모드: coding / content / strategy / personal
- Content 모드: 시장×제품 조합 자동 규제 체크 → Don't List 자동 제시 (대만 화장품 예: 의사 등장·효능 단정·B/A 비교·간체 사용 금지)
- 산출물: `grill-result.yaml` (Direction + Don't List 분리 추적) → bob/dd/직접실행으로 핸드오프
- 글로벌 동기화: `ccfm-wiki/skills/grill-me-ccfm/` 원본 → 새 PC에서 `install-grill-me-ccfm.ps1` 한 줄로 `~/.claude/skills/` 설치 (Code + Desktop 공통)
- 기존 스킬과 경계: bob-auto-spec(Spec 초안) ≠ grill-me-ccfm(방향성+Don't List). 보완 관계.

### 🔥 GFA 광고 세팅 자동화 — [[domains/gfa-setting-automation]] (NEW 2026-04-30)
**"GFA 세팅" / "GFA 광고 세팅" / "NAS 소재 GFA 업로드" 요청 시 진입.**
- `gfa-setting <광고계정ID>` → 7개 입력값 → N개 광고 그룹+소재 atomic 등록
- DrissionPage 브라우저 자동화 (네이버 OpenAPI 차단 우회), 참조 그룹 UI 복제로 27 파라미터 빌더 제거
- v0.1.0: 단위 163/163 + ruff/mypy strict 0 + N=3 E2E 성공 (CCFM-인완-네리티아)
- 코덱스 감사 결과 잔존 이슈 명문화 (antd 안전가정 문서-코드 불일치, partial 출력 누락, secrets 마스킹 무력화)
- 어느 컴퓨터에서든: `git clone Min-Gil-Sang/GFA-Setting` → `_assembled` → `pip install -e .[dev]` → `cp .env.example .env` → 최초 1회 수동 로그인 → `gfa-setting <ID>`

### 🔥 시장조사 플레이북 — [[domains/market-research-playbook]] (NEW 2026-04-20)
**"시장조사 해줘" 요청 시 바로 이 구조로 진행할 것.**
- 시드키워드 → 연관 1,158개 → 6개월 트렌드 → 저점폭증 필터
- 다음카페(Kakao) + 네이트판 + 유튜브 + 메타광고 라이브러리 병렬 수집
- 7대 인사이트(통념·근거·권위·배경·장소·물건·욕망) 매칭
- 영상기획용 11개 MD 자동 생성 (각 <150줄, 쉬운말 치환표 내장)
- Gemini Deep Research: 공식 API 없음 → 하이브리드 전략 명시
- 성공 케이스: [[sources/src-market-research-pipeline-2026-04]] (주름·유쎄라블)

### 🔥 GPT 광고 소재 배치 생성 — [[domains/gptim-ad-creative-batch]] (NEW 2026-04-28)
**"/gptim" / "광고 소재 N장 만들어줘" 요청 시 이 스킬로 진행.**
- ChatGPT 비공식 백엔드(god-tibo-imagen) 활용, API 키 없이 ~/.codex/auth.json 재사용
- 6질문 입력 → 매트릭스 → 스모크 5장 → 풀배치 (1장당 ~140초)
- 시드 폴더 4종(face/pd/best/canvas) + 금지 카피/반려 사유 학습
- 한국 GFA/카카오/네이버 매체 심의 룰 사전 차단
- 검증 케이스: 메라블 루비알엔 앰플클렌저 100장 배치

### 🔥 ggttt-imagen — GPT 우회 이미지 생성 (CCFM 커스텀) — [[domains/ggttt-imagen]] (NEW 2026-04-30)
**"이미지 만들어줘" / "imagen" / "그림 그려줘" 요청 시 진입.**
- `god-tibo-imagen` 깃허브 원본을 그대로 안 쓰고 보안·재현성 룰을 덧씌운 CCFM 커스텀
- 두 핀: **(1) Codex CLI 최신** + **(2) `gpt-5.5-pro` + `reasoning_effort=max` 강제** → 어떤 에이전트가 돌려도 거의 동일 결과
- 보안 가드: `CODEX_BASE_URL` openai.com 화이트리스트, path traversal 차단, 입력 50MB 상한, 로그 60자 truncate, `--debug` 금지
- 같은 룰이 imagen / gptim / rubyrn-pipeline 세 스킬에 공통 적용

### 🔥 USP 퍼포먼스 캔버스 조사 — [[domains/usp-performance-canvas-research]] (NEW 2026-04-27)
**"USP 조사해줘 [URL]" / "퍼포먼스 캔버스 조사 [URL]" 요청 시 바로 이 구조로 진행할 것.**
- 단일 랜딩페이지 URL → 7파일 분할 MD + 인덱스 (5~15분)
- 1단계 WebFetch (캔버스 카피·이미지 URL·JSON-LD) → 2단계 curl 일괄 다운로드
- 3단계 PIL 리사이즈 ≤1500px (subagent 2000px 거부 회피) → 4단계 Agent OCR (3장 병렬·형식 강제)
- 5단계 리뷰 위젯 메타+OCR 후기카드로 대체 (SnapReview/CREMA 등 비동기 위젯 한계)
- 6·7단계 담당자 사전 자료 통합 + 페이지↔담당자 매핑표 (퍼포먼스 카피 시드 발사대)
- **시장조사 플레이북과 차이**: 카테고리 단위 vs 제품 1개 단위
- 성공 케이스: [[sources/src-charde-melapeel-usp-2026-04-27]] (샤르드 멜라케어 필크림 마스크)

---

## 📘 참조 지식 (Reference)

내용 있고 필요할 때 찾아보는 지식.

### 도메인
- [[domains/marketing]] — 퍼포먼스 마케팅 i-boss 201건 (USP·공감·CRM·매체)
- [[domains/vibe-coding]] — 바이브코딩 v2.0 (SDD+DDD, 8-Phase, 스킬 파이프라인)
- [[domains/ai-automation]] — AI 스킬 파이프라인 (bob/dd/harness/eval/learnings)
- [[domains/psychology]] — 소비자 심리, 설득, 조직심리, 행동경제학
- [[domains/viral]] — 바이럴: 밈 구조, 시딩 전략, 알고리즘
- [[domains/usp-performance-canvas-research]] — 🎯 USP 퍼포먼스 캔버스 조사 (랜딩 URL → 7파일, 트리거: "USP 조사해줘 [URL]")
- [[domains/market-research-playbook]] — 🔥 시장조사 (카테고리 단위 11파일, 트리거: "시장조사 해줘")

### 암묵지
- [[tacit/decision-rules]] — 판단 기준 (ROAS, 예산, 지표 해석, 시장·제품, AI 판단)
- [[tacit/psychology-insights]] — 심리/설득 원칙 (6KB)
- [[tacit/lessons-learned]] — 실패 교훈 (인도네시아 크로스보더, 로고 제거 등)
- [[tacit/market-intuition]] — 시장 감각 (대만 B&A, 일본 성분, 할랄)
- [[tacit/operational-heuristics]] — 운영 노하우 (쿠팡 재고, 시즌 타이밍)
- [[tacit/people-dynamics]] — 사람 읽기 (커뮤니케이션, 협상 신호)
- [[tacit/viral-patterns]] — 바이럴 감각 (댓글 유도, 공유 메커니즘)
- [[tacit/chatgpt-web-automation]] — 🆕 **ChatGPT 웹 UI 자동화 운영 룰** (playwright CDP, 셀렉터 자가진단, alt 텍스트가 가장 안정, 다운로드 동기화 함정, 2026-04-27)

### 소스
- [[sources/src-iboss-choi-jaemyeong]] — i-boss 201건 (2017~2026) · 글별 상세: [[raw/iboss/INDEX]]
- [[sources/src-goglecc-seed-curation]] — 씨드 이미지 수집·큐레이션 (Bing+Flux LoRA)
- [[sources/src-diet-b2a-v2]] — B/A v2 대량생산 (60영상)
- [[sources/src-talmo-b2a]] — **탈모 루솔브 B/A 릴스** (3씬 + 정수리줌 + phone_look, 2026-04-16)
- [[sources/src-foreign-influencer-guide]] — 외국인 인플루언서 33편 (fal.ai+Kling)
- [[sources/src-diet-b2a-skill]] — B/A v1 스킬 (Kling+ffmpeg)
- [[sources/src-instarup]] — IG 자동 업로드 (instagrapi+APScheduler)
- [[sources/src-community]] · [[sources/src-instar]] · [[sources/src-youtube]] — 크롤러 모듈
- [[sources/src-cafe-crawler]] · [[sources/src-naverapi]] — 네이버 크롤러/API
- [[sources/src-market-research-pipeline-2026-04]] — **주름/유쎄라블 시장조사 → 영상기획 11파일** (2026-04-20)
- [[sources/src-charde-melapeel-usp-2026-04-27]] — **샤르드 멜라케어 필크림 마스크 USP 캔버스 조사 7파일** (2026-04-27, USP 플레이북 첫 케이스)
- [[sources/src-rubyrn-cleanser-glow-research-2026-04-28]] — **루비알엔 앰플클렌저 광채/톤업 시장조사** (네이버 API + Daum/네이트판/YouTube 크롤, PDRN 흡수 의심 인사이트, 2026-04-28)
- [[sources/src-rubyrn-glow-deep-research-success-2026-04-28]] — 🏆 **시장조사 4단 심화 신 표준** (1·2단 + 영상 자막+썸네일 + 민간 속설, 사용자 승인 표준, 2026-04-28)
- [[sources/src-performance-video-pipeline-v18-2026-04-28]] — 🆕 **퍼포먼스 영상 v18 검증** (메라블 루비알엔 앰플클렌저, 페르소나 1명 × 3 angle 동시 양산, 24초 세로, 2026-04-28)
- [[sources/src-nurse-shoes-2026-04-28]] — 🆕 **브랜드 시장 단위 변형 모드** (간호사 신발 55개 + 자사몰 12개 + 착한구두 시너지 3 시나리오, 검색량 역산 + Excel 11시트 + Toss UI HTML, 2026-04-28)
- [[sources/src-gemini-logo-remover]] — Gemini 로고 제거 (OpenCV TELEA+NS, 60~70점)
- [[sources/src-claude-skills-inventory-2026-04-22]] — **Claude Code 스킬/커맨드 인벤토리** (20 스킬 + 18 커맨드 스냅샷, 2026-04-22)
- [[sources/src-volumefill-pipeline-2026-04-20]] — 볼륨필인 앰플 B/A 광고 소재 자동생성 파이프라인 (2026-04-20)
- [[sources/src-volumefill-pipeline-v2-2026-04-21]] — 볼륨필인 파이프라인 v2 심화 (컷10종·카피3박자·QC 8축, 2026-04-21)
- [[sources/src-volumefill-video-pipeline-2026-04-21]] — **볼륨필인 Day1→Day14 영상 릴스 공장** (얼굴형 시드 분리·Trio·33편, 2026-04-21)
- [[sources/src-higgsfield-soul-api-2026-04-21]] — Higgsfield Soul Character API 실증 호출 레퍼런스 (엔드포인트·인증·flat JSON, 2026-04-21)

### QSCV — 서비스 품질 매뉴얼 (2025-07 베이스라인)
- [[qscv/index|qscv]] — 14개 문서 / 47 청크
  - 고객여정: [[qscv/design-customer-journey|디자인본부]] · [[qscv/media-customer-journey|미디어본부]]
  - 매체: [[qscv/media-meta|META]] · [[qscv/media-google|Google]] · [[qscv/media-gfa|GFA]] · [[qscv/media-search-ads|검색광고]]
  - 사고 프레임: [[qscv/performance-thinking|퍼포먼스 사고 확장 가이드]]
  - Appendix: [[qscv/appendix-aov|객단가]] · [[qscv/appendix-landing|랜딩]] · [[qscv/appendix-detail-page|상세페이지]] · [[qscv/appendix-video-planning|영상기획]] · [[qscv/appendix-image-planning|이미지기획]] · [[qscv/appendix-content-guide|콘텐츠기획]] · [[qscv/appendix-canvas-reupdate|캔버스재기획]]
  - 캔버스: [[qscv/canvas-rusolve-v1]] — 루솔브 탈모 캔버스 v1

### 기타
- [[AI-Avatar-Automation-Guide]] — AI 아바타 자동화 가이드 (OmniHuman, Kling, Aurora, Rhubarb)
- [[수치-단위-착각-방지-규칙]] — 수치/단위 혼동 방지 규칙

---

## 💤 미작성 (Stub — 내용 추가 예정)

### 도메인 스텁
- [[domains/taiwan-market]] — 대만: TFDA, 샵라인, Merable TW ⬜
- [[domains/sea-tiktok]] — 동남아: 틱톡샵, BPOM, 할랄 ⬜
- [[domains/japan-market]] — 일본: Q10, X채널 ⬜
- [[domains/ma-exit]] — M&A: Exit 도메인, SPA ⬜
- [[domains/org-restructure]] — 조직개편: A→Y/Z, AI Cell ⬜
- [[domains/finance]] — 재무/회계: 다법인 세무, 이전가격 ⬜
- [[domains/hr-admin]] — 인사/총무: 보상구조, 채용 ⬜

### 암묵지 미생성
- wiki/tacit/negotiation-patterns.md — 협상 감각 (파일 미생성) ⬜

---

## 엔티티 (Entities)
_아직 없음_

## 의사결정 (Decisions)
_아직 없음_
