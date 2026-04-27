# CCFM Wiki Index

> 🔥 = 활발 (커밋 4+) · 📘 = 참조용 (커밋 2-3) · 💤 = 미작성 스텁
> 최종 정리: 2026-04-16

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

### 마케팅 자동화 — [[domains/marketing-automation]] (4커밋)
- 네이버 카페 크롤러, 네이버 API, 인스타 수집, 유튜브, 커뮤니티 크롤링

### 🔥 시장조사 플레이북 — [[domains/market-research-playbook]] (NEW 2026-04-20)
**"시장조사 해줘" 요청 시 바로 이 구조로 진행할 것.**
- 시드키워드 → 연관 1,158개 → 6개월 트렌드 → 저점폭증 필터
- 다음카페(Kakao) + 네이트판 + 유튜브 + 메타광고 라이브러리 병렬 수집
- 7대 인사이트(통념·근거·권위·배경·장소·물건·욕망) 매칭
- 영상기획용 11개 MD 자동 생성 (각 <150줄, 쉬운말 치환표 내장)
- Gemini Deep Research: 공식 API 없음 → 하이브리드 전략 명시
- 성공 케이스: [[sources/src-market-research-pipeline-2026-04]] (주름·유쎄라블)

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

### 암묵지
- [[tacit/decision-rules]] — 판단 기준 (ROAS, 예산, 지표 해석, 시장·제품, AI 판단)
- [[tacit/psychology-insights]] — 심리/설득 원칙 (6KB)
- [[tacit/lessons-learned]] — 실패 교훈 (인도네시아 크로스보더, 로고 제거 등)
- [[tacit/market-intuition]] — 시장 감각 (대만 B&A, 일본 성분, 할랄)
- [[tacit/operational-heuristics]] — 운영 노하우 (쿠팡 재고, 시즌 타이밍)
- [[tacit/people-dynamics]] — 사람 읽기 (커뮤니케이션, 협상 신호)
- [[tacit/viral-patterns]] — 바이럴 감각 (댓글 유도, 공유 메커니즘)

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
- [[domains/ma-exit]] — M&A: 스마일게이트 딜, SPA ⬜
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
