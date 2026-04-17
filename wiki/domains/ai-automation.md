---
type: domain
domain: ai
confidence: low
created: 2026-04-12
updated: 2026-04-12
sources: []
---

# AI 자동화 (AI Automation)

## 개요
스킬 파이프라인(bob/dd/harness/eval/learnings), DA 자동화 관련 도메인.

## 스킬 파이프라인
_내용 추가 예정_

## DA 자동화
_내용 추가 예정_

## 러닝스 누적
_내용 추가 예정_

## 관련 페이지
- [[org-restructure]]
- [[da-creative]]


## Gemini 로고 제거 (2026-04-12 추가)
→ [[src-gemini-logo-remover]] 참조

### 현재 최선 기술
- OpenCV TELEA+NS 인페인팅 50:50 블렌딩
- LaMa(simple-lama-inpainting) 대비 우위 확인
- 품질: 60~70점 / 비교 대상 추가 예정

### 암묵지 추출
- Gemini 로고는 극소 영역(이미지 대비 4~5%)이라 딥러닝보다 OpenCV가 유리
- LaMa가 오히려 나쁜 경우: 마스크 크기 작고 주변 배경 단순할 때
- → [[lessons-learned]] 교차 저장됨

## 최재명 대표 i-boss 인사이트 (2026-04-13 추가)
원본: [[src-iboss-choi-jaemyeong]] · 인덱스: `raw/inbox/2026-04-13-iboss-choi-jaemyeong-201articles.md`

### AI 시대 실행 격차 = 10~100배
- "아는 것 ≠ 쓰는 것 ≠ 성과 내는 것" — 3단 분리가 핵심
- CLI(Claude Code)는 IDE 대비 10배 빠름 — 병렬 실행·파이프라인·스크립팅 가능
- SDD/DDD 도입으로 수정 3~4회 → 1~2회로 감소
- 월 $100~200 토큰을 일주일 내 소진하는 게 실력 지표
- 마케터 AI 활용/미활용 생산성 격차 변곡점: 2026-2027년

### 암묵지 × AI 협업 공식
- "Claude는 IQ 1000짜리 신입" — 도메인 기준을 명시화해야 작동
- "5단계로 보이는 업무가 실제론 30단계" — 숨은 단계가 자동화 70% 벽
- 도메인 전문성 × AI 활용 능력 = 생존 공식

### AI 무중단 스튜디오 (일매출 8천만 사례)
- 나노바나나 · Midjourney · Runway · Veo3 조합
- 모델비·촬영비 없이 300종 A/B, CPC 400→300원
- 용도별 분리: Higgsfield(사실성) · Midjourney(일관성) · Flux(포즈)

### 스킬/에이전트 빌딩
- 프롬프트 → 스킬(재현성) → 에이전트(자율성)로 단계 진화
- bob(설계) → dd(분해) → harness(강제) → eval(평가) → learnings(피드백)
- 산출물 품질은 "강제 규칙(린터·하네스)" 유무가 결정
- → [[wiki/tacit/coding-lessons]] 2026-04-13 엔트리 교차 저장

### bdh 완주 사례: diet-b2a (2026-04-13)
- [[src-diet-b2a-skill]] — bob(PLAN.md) → dd(steps/00~05) → harness(RULES.md 10개) 완주한 첫 프로덕션 스킬
- Kling image2video + ffmpeg filter_complex 조합으로 **이미지 4장 + config 5줄 → 10초 릴스 3본** 자동화
- 재사용 벡터: config 5슬롯만 편집 → 새 인물/프로젝트. 중간 실패 시 멱등 재개.
- 교훈 누적: [[creative-patterns]] (전→후 하드컷 매칭 포즈), [[coding-lessons]] (cp949 em-dash 이슈, Kling 10s > 5s 포즈 준수율), [[psychology-insights]] (전반 억제 → 후반 폭발 해방감)


## Multi-LLM Orchestrator v2.0.1 (2026-04-17 추가)

### 위치 / 구조
- 설치본: `~/.claude/skills/multi-llm-orchestrator/`
- 소스 미러: `C:/Users/gguy/Desktop/multi-llm-orchestrator-v2/`
- 스크립트: `scripts/cli_bridge.py` (CLI 래퍼) + `scripts/orchestrator.py` (5모드 명령)
- 슬래시 커맨드: `/ask-all`, `/askall` (그 외 `mllm-review/fix/debate/consensus`)

### 5모드
| 모드 | 동작 | 모델 간 상호 참조 |
|------|------|-------|
| ask | 병렬 답변 + (선택) 교차검증 + 종합 | parallel/cross/full |
| review | 파일 코드 리뷰 (patch 미생성) | 없음 |
| fix | 멀티 수정안 → Merger 모델 통합 (원본 자동 덮어쓰기 X) | Merger 단계만 |
| debate | A/B 3R 반박 + Judge 판정 | 있음 (쟁점 노출) |
| consensus | N R 상호 참조 → 합의안 | 있음 (수렴) |

### 인증
CLI 로그인(`codex login`/`gemini` 첫 실행/`claude login`) 또는 환경변수(`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`) — **둘 중 하나만**. 우선순위: 로그인 세션 > 환경변수.

### v2.0.1 (2026-04-17) 패치 4종 — 실측 디버그 산물
1. Codex `--skip-git-check` → `--skip-git-repo-check` (CLI 자체 변경)
2. Windows `.cmd` shim FileNotFoundError → `shutil.which()` 절대경로 해석
3. `cp949` UnicodeEncodeError → 모듈 시작 시 `sys.stdout.reconfigure("utf-8")` 강제
4. **Gemini "Hello! I'm ready..." 함정** → Windows `.cmd` 가 멀티라인(`\n`) 인자를 명령 구분자로 오해 → 인터랙티브 폴백. 해결: Gemini만 `transport: "stdin"` + `args_template` 끝에 `"-p", ""` (자세히는 [[tacit/coding-lessons]] 2026-04-17 항목)

### 자동화 인터페이스
- Exit code: 0/1/2/3/4/5/6/130 (스크립트 실행 결과 후속 동작 분기)
- `--json-output PATH`: 메타데이터 JSON emit (모델별 success/elapsed/raw 경로)
- `--quiet`: CI 로그 노이즈 감소

### 다른 스킬과의 위치
- `eval` 스킬의 상위 버전으로 사용 가능 (평가자 1명 → 진짜 다른 모델 2~3명)
- `bob → dd → harness → eval(=mllm) → learnings` 파이프라인의 eval 단계

### 관련 페이지
- [[tacit/coding-lessons]] 2026-04-17 항목 3개 (Windows .cmd shim, CLI 플래그 변경, 자동화 인터페이스)
