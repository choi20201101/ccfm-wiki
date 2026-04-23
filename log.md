# CCFM Wiki Log

## [2026-04-23] graphify | 볼륨필인 영상 파이프라인 + Higgsfield Soul API 그래프 반영
- 신규 소스 2종 untracked → wiki/index.md 소스 섹션에 등록
  - [[sources/src-volumefill-video-pipeline-2026-04-21]] — 볼륨필인 Day1→Day14 릴스 공장 (33편, Trio 10편)
  - [[sources/src-higgsfield-soul-api-2026-04-21]] — Soul Character API 실증 (엔드포인트·flat JSON)
- [[tacit/video-gen-lessons]]: 16 → 34 섹션으로 확장 (§17-34 신규, 2026-04-21/23 추가분 반영)
  - §17-19 얼굴형 시드 분리 · 웻룩 도트 · Kling 스무딩 방지
  - §20-25 Trio 릴레이 · 구조 해시 · CTA 풀 · 숫자 오독 방지
  - §26-34 인페인팅 · shadow/silhouette 금지어 · 17s 표준 구조
- `graphify.watch._rebuild_code` 실행: 450 files · 260,642 words · 256 nodes · 328 edges · 31 communities
- `scripts/regen_graph_report.py` 로 한국어 커뮤니티 라벨 재적용

## [2026-04-22] ingest | Claude Code 스킬/커맨드 인벤토리 스냅샷
- `~/.claude/skills/` 20개 + `~/.claude/commands/` 18개 스냅샷을 [[sources/src-claude-skills-inventory-2026-04-22]]에 기록
- 다른 기기 이전용 백업 패키지: `Desktop/claude-skills-package-20260422.zip` (286KB)
- 파이프라인: bob → dd → harness → eval → learnings (5단 순환)
- index.md §소스 섹션에 링크 추가

## [2026-04-15] update | goglecc — 다이어트 B/A "예쁜 얼굴 + 통통 몸" V15 확정
- 사용자 승인: "만족스러운 결과가 나왔어" (15회 반복 후)
- 최종 파이프라인: Higgsfield Soul (strength 0.85 After + 0.6 Before_raw) + `fal-ai/face-swap`
- [[src-goglecc-seed-curation]] §9 (V15 아키텍처·엔드포인트·프롬프트·비용) + §10 (실패 경로 금지 리스트) 추가
- [[tacit/creative-patterns]]: "예쁜 얼굴+통통 몸" 레시피 (confidence high)
- [[tacit/coding-lessons]] 2건: (1) Gemini preserved-face body 부피 증가 거부 확정, (2) Higgsfield Soul API 실전 스펙(hf-api-key/hf-secret 헤더, /v1/custom-references, /higgsfield-ai/soul/standard)
- 핵심 인사이트: 한 AI 툴로는 목적 달성 불가 → **Higgsfield(몸 생성) + fal face-swap(얼굴 합성)** 파이프라인이 유일 해법
- 비용: ~$0.10/세트, 10세트 ~$1

## [2026-04-13] prune | 통합검색 크롤링(posts/collect.py) 레퍼런스 제거
- 사용자 지시: 통합검색 크롤링 불필요 → 위키에서 삭제
- 영향 파일: wiki/sources/src-cafe-crawler.md, wiki/tacit/coding-lessons.md
- 제거 항목: 파일 테이블 row, CLI 사용 예, 셀렉터 설명, rate limit 값, HITL 캡차 파일 레퍼런스, 크레덴셜 분리 언급

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

## [2026-04-16] ingest | talmo 탈모 B/A 파이프라인 (루솔브 런칭용)
- 소스: `C:\Users\gguy\Desktop\talmo\` 전체 트리 (v1 완성: 1세트 검증 통과)
- 생성: wiki/sources/src-talmo-b2a.md (전체 파이프라인 + 교훈 + 스크립트 맵)
- 업데이트: wiki/domains/content-ai-automation.md §14 talmo (신설)
- 업데이트: wiki/tacit/creative-patterns.md (+6 항목 — 정수리위젯/조명대비/전환카드/2박스카피/계절의상/후킹핏)
- 업데이트: wiki/tacit/coding-lessons.md (+5 항목 — Haar 3단방어/Gemini합성표현/phone_look/HAIR_COLOR/cp949)
- 업데이트: wiki/tacit/psychology-insights.md (+4 항목 — 정수리공포/3개월시간축/쓸어올림제스처/조명대비)
- 업데이트: wiki/index.md (sources 목록에 src-talmo-b2a 추가)
- 핵심 결정: burst(고무줄 폭발) 씬 실험 후 폐기 → 3씬 + 헤어플립 엔딩으로 확정

## [2026-04-17] ingest | Multi-LLM Orchestrator v2.0.1 패치
- 소스: `C:\Users\gguy\Desktop\multi-llm-orchestrator-v2` (v1 API → v2 CLI subprocess 전환 + 4종 함정 패치)
- 업데이트: wiki/domains/ai-automation.md (Multi-LLM Orchestrator 섹션 신설)
- 업데이트: wiki/tacit/coding-lessons.md (+3 항목 — Windows .cmd 멀티라인 인자 함정 / CLI 플래그 변경 대응 / exit code+json-output 자동화 계약)
- 핵심 발견: Codex/Gemini 자체 SKILL.md 리뷰로 P0 가드레일 도출 (description 과잉 트리거 제거, 자동화 계약, 첫 실행 실패 차단)
- 영향 스킬: ~/.claude/skills/multi-llm-orchestrator/ + ~/.claude/commands/{askall,ask-all}.md

## [2026-04-20] ingest | 볼륨필인 앰플 광고 소재 자동생성 파이프라인 성공사례
- `wiki/sources/src-volumefill-pipeline-2026-04-20.md` 생성 (전체 케이스 스터디)
- `wiki/domains/da-creative.md` 에 링크·요약 추가
- `wiki/tacit/creative-patterns.md` 에 6개 패턴 추가 (타입 진단형 후킹, B/A 우회 12종, 나이 단정 회피, 시각 템플릿 선언, O 마스킹, 인종 강제)
- `wiki/tacit/coding-lessons.md` 에 6개 교훈 추가 (gpt-image 첫입력 fidelity, 백그라운드 조기종료, bash rm 영구삭제, rate limit 30분캡, Codex 크로스리뷰, 라운드로빈 정렬)
- 결과: 다음 프로젝트 시작 시 `projects/<new>/` 템플릿 복제 + 규칙 MD 6종 제품별 맞춤 → 동일 퀄리티 유지 가능

## [2026-04-20] playbook | 시장조사 파이프라인 플레이북 등록 (주름/유쎄라블 성공 케이스)

### 등록 배경
사용자 요청: "시장조사하는 것 구조 전체를 wiki에 등록해서 최근 성공 사례로 하고, 이거 요청 시장조사 요청하면 이것 형태로 바로 구조화해서 할 수 있게 업데이트"

### 추가 파일
- `wiki/sources/src-market-research-pipeline-2026-04.md` — 주름·유쎄라블 시장조사 전체 케이스 스터디
  - 소비자 발언 17,690건 수집 (다음카페 + 네이트판 + 유튜브)
  - 연관키워드 1,158개 6개월 트렌드 → 저점폭증 32건 발굴
  - 메타 광고 500+ 카피 경쟁사 역설계
  - 영상기획 MD 11파일 (각 <150줄, 쉬운말 치환)
- `wiki/domains/market-research-playbook.md` — **재사용 플레이북 (글로벌 지식)**
  - "시장조사 해줘" 요청 시 즉시 참조하는 runbook
  - 9단계 체크리스트 + 쉬운 말 치환 규칙 + 브랜드 제외 체크
  - Gemini Deep Research API 현황 + 하이브리드 전략 명시

### Gemini Deep Research API 조사 결과
- 2026-04 기준 **공식 API 미제공** (Gemini Advanced 앱 전용 기능)
- 대안: Gemini 2.5 Pro + `google_search` grounding tool (Vertex AI / AI Studio)
- 실무 권장: 앱에서 수동 생성 후 폴더 투입 → Claude가 읽어 통합

### 쉬운 말 치환표 (중요)
- "지방 세포 증식" → "꺼진 자리 깨우기" (⚠️ 살찐다 오해 방지)
- "인텔리전트 미니멀리즘" → "한 병으로 끝"
- 향후 시장조사 시 전문용어 감수에 활용

## [2026-04-21] ingest | 볼륨필인 파이프라인 v2 성공 패턴 심화 확장
- `wiki/sources/src-volumefill-pipeline-v2-2026-04-21.md` 생성 (v2 심화 사례)
- 15개 개선 항목: 컷 10종 · 키워드 120개 · 카피 3박자 · 궁금증 갭 · 자연 어법 · 글로벌 캡 · 동적 금지어 · 11 민족 · 첨부 순서 · O 마스킹 · 뚜껑 자동 · melable 로고 강제 · rate limit 1탭 · JPG 전환 · QC 8축
- 성과: 24시간 200+ 이미지 자동 생성, 사용자 만족 "매우 좋아짐"
- tacit/creative-patterns.md: 7개 패턴 추가
- tacit/coding-lessons.md: 5개 교훈 추가
