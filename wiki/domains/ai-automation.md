---
aliases: ["AI 자동화", "스킬 파이프라인"]
type: domain
domain: ai
confidence: low
created: 2026-04-12
updated: 2026-04-27
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

### 저장소 (GitHub)
- **Repo**: https://github.com/choi20201101/multi-llm-orchestrator
- 새 기기 셋업 (3분):
  ```bash
  git clone https://github.com/choi20201101/multi-llm-orchestrator.git \
    ~/.claude/skills/multi-llm-orchestrator
  cp ~/.claude/skills/multi-llm-orchestrator/commands/ask-all.md ~/.claude/commands/
  cp ~/.claude/skills/multi-llm-orchestrator/commands/ask-all.md ~/.claude/commands/askall.md
  npm install -g @openai/codex @google/gemini-cli @anthropic-ai/claude-code
  codex login && claude login && gemini   # gemini 는 첫 실행으로 로그인 자동 트리거
  python ~/.claude/skills/multi-llm-orchestrator/scripts/cli_bridge.py
  ```
  자세한 셋업/트러블슈팅은 repo 의 README.md 참조.

### 위치 / 구조 (gguy 데스크탑 기준)
- 설치본: `~/.claude/skills/multi-llm-orchestrator/`
- 소스 미러: `C:/Users/gguy/Desktop/multi-llm-orchestrator-v2/` (= GitHub repo 의 origin)
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

## AI CLI 인증 모드 표준 (2026-04-26 추가)

mllm/Codex/Claude CLI를 호출할 때 **API 키 종량제가 아닌 구독·OAuth 인증을 우선**으로 한다. 같은 모델·같은 품질에 비용 0원 또는 정액제.

### 표준 인증 매트릭스

| CLI | 인증 | 결제 | 한도 | 자격 파일 |
|---|---|---|---|---|
| `codex` (GPT-5.x) | ChatGPT 구독 OAuth | Pro Lite 월 $150 정액 | 구독 한도 내 무제한 | `~/.codex/auth.json` (`auth_mode: chatgpt`) |
| `gemini` (2.5 Pro) | Google 계정 OAuth | **무료** | 60 req/min, 1,000 req/day | `~/.gemini/oauth_creds.json` |
| `claude` | Claude Code 구독 OAuth | Pro/Max 정액 | 구독 한도 내 | Claude 자체 관리 |

확신도: high (실측, 2026-04-26 ceo@mkm20201101.com 계정에서 검증)

### 신규 컴퓨터 세팅 절차

**Codex (ChatGPT 구독):**
```bash
codex login
# → 브라우저 OAuth → ~/.codex/auth.json 생성 (auth_mode: chatgpt)
```

**Gemini (구글 OAuth, 무료):**
```powershell
# 1) 기존 API 키 환경변수 제거 (이게 있으면 OAuth 메뉴 안 뜸)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', $null, 'User')
# 2) 새 터미널 열고
gemini
# → 메뉴에서 "Login with Google" 선택
# → 브라우저 OAuth → ~/.gemini/oauth_creds.json 생성
```

**Claude:**
```bash
claude login   # 또는 Claude Code 첫 실행 시 자동 안내
```

### 검증

```bash
# Codex
cat ~/.codex/auth.json | grep auth_mode   # "chatgpt" 이어야 함

# Gemini
ls ~/.gemini/oauth_creds.json             # 존재해야 함
gemini -p "auth method?"                   # OAuth 인증 확인 응답
```

### 운영 규칙

- **mllm-* 스킬, multi-llm-orchestrator는 코드 변경 없음** — 그냥 CLI 호출이라 env 없으면 자동으로 OAuth로 fallback
- **`GEMINI_API_KEY` 환경변수가 설정돼 있으면 무조건 API 키 모드**가 됨. OAuth로 가려면 반드시 unset 필요
- **헤비 워크로드(mllm-consensus N라운드)에서 rate limit 자주 걸리면** Gemini만 임시로 API 키 모드 복귀 검토 — 단, 비용 다시 발생
- OAuth 토큰은 가끔 만료 → `gemini`/`codex` 단독 실행 한 번으로 재로그인

### 다른 컴퓨터/Claude Desktop 앱에서

- 같은 컴퓨터의 다른 터미널·Claude Desktop 앱: User scope env가 깨끗하면 자동으로 OAuth 사용 (별도 작업 불필요)
- 다른 컴퓨터: 위 "신규 컴퓨터 세팅 절차" 반복. OAuth 자격은 컴퓨터별로 발급되는 게 정상 (`oauth_creds.json` 공유 비추천 — 보안 리스크)

### OAuth 영구성 (2026-04-26 보강)

- **재인증 불필요**: `~/.gemini/oauth_creds.json`, `~/.codex/auth.json`은 refresh_token 기반으로 영구. 새 터미널·새 세션 열어도 자동 갱신
- access_token은 1시간 만료지만 CLI가 자동 refresh
- 보통 6개월~1년 또는 명시적 로그아웃·계정 비밀번호 변경 시까지 유효
- "새 터미널마다 다시 로그인해야 하나?" 질문에 대한 정답: **아니요**. 단, 환경변수 주입 함정(아래)을 점검할 것

### OAuth 무력화 함정 4곳 (2026-04-26 추가, confidence: high)

OAuth 자격이 있어도 환경변수에 API 키가 깔리면 CLI는 OAuth보다 API 키를 우선 사용해서 종량제 모드로 fallback. 이게 일어나는 4곳을 모두 점검해야 진짜 OAuth 모드가 보장됨:

1. **Claude Code `~/.claude/settings.json`의 `env` 블록** ⚠️ 가장 흔한 함정
   - Claude Code가 새 bash 세션 spawn할 때마다 이 블록의 키들을 자동 주입
   - 점검: `grep -nE "(GEMINI_API_KEY|OPENAI_API_KEY)" ~/.claude/settings.json`
   - 정리: `env` 블록 통째 제거하거나 두 키만 삭제

2. **Windows User scope 환경변수 (HKCU\Environment)**
   - `setx`나 시스템 속성으로 영구 등록된 API 키
   - 점검 (PowerShell): `[Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")`
   - 삭제: `[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $null, "User")`

3. **Shell profile (`~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.zshrc`)**
   - `export GEMINI_API_KEY=...` 한 줄 박혀있을 수 있음
   - 점검: `grep -nE "(GEMINI|OPENAI|ANTHROPIC)_API_KEY" ~/.bashrc ~/.bash_profile ~/.profile ~/.zshrc 2>/dev/null`

4. **Claude Desktop `%APPDATA%\Claude\claude_desktop_config.json`**
   - MCP 서버 정의에 `env` 블록 추가하면 Desktop 앱이 그 환경변수로 MCP 자식 프로세스를 spawn
   - **추가하지 말 것** — Desktop 앱 자체는 별도 OAuth, MCP 서버는 자체 인증 사용해야 함
   - 점검: `cat "$APPDATA/Claude/claude_desktop_config.json" | grep -A2 env`

### 진단 한 줄 명령 (Bash, Windows)

```bash
echo "=== ENV ==="; for k in OPENAI_API_KEY GEMINI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY; do v=${!k}; [ -n "$v" ] && echo "$k=SET" || echo "$k=unset"; done
echo "=== Claude Code settings ==="; grep -nE "(GEMINI|OPENAI|ANTHROPIC)_API_KEY" ~/.claude/settings.json 2>/dev/null || echo "  clean"
echo "=== Shell profiles ==="; grep -nE "(GEMINI|OPENAI|ANTHROPIC)_API_KEY" ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null || echo "  clean"
echo "=== HKCU (PowerShell 별도) ==="; powershell -Command '[Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User"); [Environment]::GetEnvironmentVariable("GEMINI_API_KEY","User")' 2>/dev/null
echo "=== Claude Desktop ==="; grep -nE "(GEMINI|OPENAI|ANTHROPIC)_API_KEY" "$APPDATA/Claude/claude_desktop_config.json" 2>/dev/null || echo "  clean"
echo "=== OAuth 자격 ==="; ls -la ~/.gemini/oauth_creds.json ~/.codex/auth.json 2>&1
```

### Gemini 모델별 OAuth 한도 차등 (2026-04-26 실측)

같은 OAuth 계정이라도 모델마다 무료 한도 다름. Preview 모델은 매우 빡빡:

| 모델 | OAuth 무료 한도 | 권장 용도 |
|---|---|---|
| `gemini-2.5-flash` | 넉넉 (대량 OK) | mllm 1차 답변, 대량 평가 |
| `gemini-2.5-pro` | 중간 | 정밀 분석 |
| `gemini-3.1-pro-preview` | **매우 빡빡** (몇 회만 호출해도 429) | 실험·1회성만 |

→ orchestrator/mllm-* 스킬 기본은 `gemini-2.5-flash` 권장. Preview는 fallback chain에 포함하되 1순위 X. 429 (`RetryableQuotaError: You have exhausted your capacity`) 발생 시 Flash로 자동 fallback 로직 추천.

### 회고: 이 표준이 어떻게 발견됐나
- 2026-04-26 사용자가 "코덱스랑 제미나이 셋이서 평가" 요청 → orchestrator 호출 시 Gemini 429 실패
- 원인 추적: `GEMINI_API_KEY`/`OPENAI_API_KEY` 환경변수가 설정돼 있어 API 키 모드로 fallback. OAuth 자격 파일은 둘 다 정상 존재
- 진짜 출처: `~/.claude/settings.json`의 `env` 블록이 매 Claude Code 세션마다 API 키 주입 (HKCU도 OPENAI_API_KEY 영구 등록)
- 조치: settings.json `env` 블록 제거 + HKCU OPENAI_API_KEY 삭제 → 다음 세션부터 OAuth 자동 사용
- 교훈: OAuth 자격 존재 ≠ OAuth 사용 보장. 환경변수 4곳을 모두 점검해야 함

## 3-CLI 컨텍스트 브릿지 (2026-04-26 추가)

세 CLI(Claude / Codex / Gemini)가 각자 별도 자동 로드 파일을 읽기 때문에, 사용자 핵심 컨텍스트(메모리, 한국어 선호, AI CLI 인증 표준, 스킬 카탈로그)를 세 파일에 동기화해두면 어느 CLI 를 호출해도 동일한 컨텍스트로 동작한다. 멀티 LLM 토론·교차 검증 시 일관성 핵심.

확신도: high (실측, 2026-04-26 검증 — codex/gemini 둘 다 자동 로드 + 사용자 정보 정확히 응답)

### 자동 로드 파일 (CLI 별)
| CLI | 자동 로드 경로 | 비고 |
|---|---|---|
| Claude (Claude Code) | `~/.claude/CLAUDE.md` | 글로벌 + 프로젝트별 `CLAUDE.md` 함께 로드 |
| Codex | `~/.codex/AGENTS.md` | 프로젝트 디렉토리에 `AGENTS.md` 있으면 추가 로드 |
| Gemini | `~/.gemini/GEMINI.md` | 현재 디렉토리부터 위로 walk 하며 `GEMINI.md` 추가 로드 |

### 동기화해야 할 코어 섹션
세 파일 모두 다음을 포함해야 함:
1. **사용자 정보 / 응답 규칙** (언어, 이메일, 일자 기준)
2. **개인화 메모리 파일 경로** (Claude memory, MEMORY.md, 위키 entry)
3. **AI CLI 인증 모드 표준** (위 매트릭스)
4. **스킬 카탈로그** (트리거 키워드 + SKILL.md 경로)
5. **위키 작성 규약** (덮어쓰기 금지 등)
6. **메모리 자동 기록 규칙**
7. **형제 파일 참조** (다른 두 CLI 의 자동 로드 경로 명시)

### 신규 컴퓨터 / 신규 CLI 추가 시 절차
1. 해당 CLI 의 자동 로드 경로 확인 (CLI 문서 또는 `<cli> -p "어떤 컨텍스트 파일을 자동 로드하나"`)
2. Claude `CLAUDE.md` 의 코어 섹션을 베이스로 해당 CLI 형식에 맞게 변환
3. 형제 파일 섹션에 새 CLI 경로 추가
4. 검증: `<cli> -p "사용자 이메일과 응답 언어가 뭐로 적혀 있어?"` → 정확히 답하면 OK

### 운영 규칙
- 한 파일만 수정하면 다른 두 파일 동기화 누락 → 멀티 LLM 결과 불일치. 사용자 핵심 정보 변경 시 세 파일 동시 갱신
- 스킬 카탈로그는 `~/.claude/skills/` 추가/삭제 시마다 세 파일 동시 갱신
- 추가 비용 0원 (각 CLI 가 토큰 사용에 미미한 영향 — 보통 2~5KB 추가 컨텍스트)

<!-- AUTO:domain-crosslinks-begin -->
## 🔗 관련 도메인

- [[domains/content-ai-automation|🎬 콘텐츠 AI 자동화]]
- [[domains/vibe-coding|💻 바이브 코딩]]
- [[domains/org-restructure|🏢 조직개편 (A→Y/Z)]]
- [[domains/marketing-automation|⚙️ 마케팅 자동화]]

## 📊 소스
- [[wiki/sources/src-iboss-choi-jaemyeong|i-boss 201건]] 카테고리별 MOC:
  - [[raw/iboss/moc/ai-automation|🤖 AI 자동화]]
<!-- AUTO:domain-crosslinks-end -->

<!-- AUTO:tags-begin -->
**Tags**: #status/active #domain/ai-automation #region/kr #source/iboss
<!-- AUTO:tags-end -->
