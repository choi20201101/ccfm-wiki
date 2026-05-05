---
type: domain
status: 🔥
last_updated: 2026-05-05
related: [[ai-automation]], [[index]], [[HOTSHEET]]
---

# Codex Grounding Protocol

> 모든 CLI(Claude/Codex/Gemini)가 호출될 때 **개인 메모리 인덱스 + CCFM 위키**를 자동 grounding 하도록 강제하는 시스템. "깡통 응답"(개인 컨텍스트 무시한 채 일반 지식만 사용) 방지.

## Why

세 CLI(`claude` / `codex` / `gemini`)가 각자 독립된 dotfile(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`)을 자동 로드한다. 각 dotfile에 메모리/위키 경로는 명시돼 있었지만, **읽으라고 강제하는 절차**가 없어서 LLM이 "기억나는 대로" 답하는 경우가 잦았다. 결과:

- 사용자가 과거에 거른 함정(`feedback_*.md`)을 모르고 같은 실수 반복
- 비즈니스 컨텍스트(대만/일본 시장 등) 누락
- mllm 호출 시 다른 CLI가 grounding 없이 raw question 만 받음 → 5모드 모두 깡통

## What

3-layer defense in depth:

```
Layer 1. dotfile MANDATORY PRE-WORK PROTOCOL
   ↓ (LLM self-discipline)
Layer 2. orchestrator.py grounding prepend
   ↓ (forwarding 코드 강제 inject)
Layer 3. context-bootstrap.mjs 헬퍼
   ↓ (실제 매칭 엔진)
   = MEMORY.md + HOTSHEET.md 토큰 매칭 → <context_grounding> 블록
```

각 CLI가 substantive 요청을 받으면:
1. `node ~/.codex/scripts/context-bootstrap.mjs "<prompt>"` 호출 (또는 직접 grep fallback)
2. `<context_grounding>` 블록의 hit 파일들 직접 읽기
3. 응답 첫 줄에 `📚 참조: <파일 목록>` 명시 (0건이면 "없음")

multi-llm-orchestrator는 추가로 codex/gemini subprocess 호출 시 위 블록을 prompt에 prepend (CLI 자체 dotfile 따르지 않더라도 prompt에 grounding이 박힘).

## 컴포넌트

| 컴포넌트 | 위치 | 역할 |
|---|---|---|
| `context-bootstrap.mjs` | `~/.codex/scripts/` | 헬퍼. prompt → 토큰화 → MEMORY/HOTSHEET 매칭 → `<context_grounding>` 블록 |
| `AGENTS.md` PRE-WORK 섹션 | `~/.codex/AGENTS.md` (marker `codex-grounding-protocol v1`) | Codex CLI 자동 로드 instruction |
| `CLAUDE.md` PRE-WORK 섹션 | `~/.claude/CLAUDE.md` (marker) | Claude Code instruction |
| `GEMINI.md` PRE-WORK 섹션 | `~/.gemini/GEMINI.md` (marker) | Gemini CLI instruction |
| `orchestrator.py` `build_grounding()` | `~/.claude/skills/multi-llm-orchestrator/scripts/orchestrator.py` | mllm 5모드(ask/review/fix/debate/consensus) prompt 자동 grounding |
| `install-codex-grounding.ps1` | `ccfm-wiki/skills/` | 위 4개 dotfile + 헬퍼 idempotent 설치 |

## 토큰 매칭 알고리즘

`context-bootstrap.mjs:tokenize()` 동작:

1. 한글/영문/숫자만 추출 (구두점 제거, 소문자화)
2. **한국어 조사 후행 trim**: `에서|에게|이라고|이라|라고|이고|이며|이다|로서|로써|으로|에|을|를|이|가|은|는|의|와|과|도|만|까지|부터` 등
3. **stop word 필터**: 일반어("이거", "그런", "있다") + 의문/명령형 어미("어떻게", "뭐야", "해줘", "만들어줘") + 영어 일반어
4. 길이 < 2 토큰 제거 (한글 2자+, 영문 2자+ — `BJ`, `AE`, `UI` 약어 보존)
5. 중복 제거

매칭:
- MEMORY.md bullet: `- [Title](file.md) — desc` 파싱 → 한 줄에 토큰 N개 포함되면 hits=N
- HOTSHEET.md table: `| trigger | target | note |` 행 파싱 → 동일 매칭
- 상위 6개 (hits 내림차순)만 출력

## 환경별 경로 override

| 항목 | env 변수 | local override 파일 | 기본 후보 |
|---|---|---|---|
| 위키 루트 | `CCFM_WIKI_ROOT` | `~/.codex/AGENTS.local.md` 의 `CCFM_WIKI_ROOT=...` | `gguy/ccfm-wiki` → `$HOME/ccfm-wiki` → `$HOME/Desktop/ccfm-wiki` |
| 메모리 인덱스 | `CCFM_MEMORY_INDEX` | (없음) | `$HOME/.claude/projects/C--Users-Administrator/memory/MEMORY.md` |

비활성화: `MLLM_SKIP_GROUNDING=1` (orchestrator.py 그라운딩만 끔. dotfile 자체 PRE-WORK는 LLM이 따름)

## 새 PC 부트스트랩

```powershell
# 1. wiki clone
git clone https://github.com/choi20201101/ccfm-wiki.git $env:USERPROFILE\ccfm-wiki

# 2. install (marker-based idempotent)
cd $env:USERPROFILE\ccfm-wiki\skills
.\install-codex-grounding.ps1

# 3. 위키/메모리 경로가 다르면 override 등록
@"
CCFM_WIKI_ROOT=$env:USERPROFILE\ccfm-wiki
CCFM_MEMORY_INDEX=$env:USERPROFILE\.claude\projects\C--Users-Administrator\memory\MEMORY.md
"@ | Out-File -Encoding utf8 $env:USERPROFILE\.codex\AGENTS.local.md

# 4. 검증
node $env:USERPROFILE\.codex\scripts\context-bootstrap.mjs "BJ 광고 영상" --verbose
```

## 검증 명령

```bash
# 헬퍼 동작
node ~/.codex/scripts/context-bootstrap.mjs "테스트 프롬프트" --verbose

# 인덱스 파일 존재
test -f "$HOME/.claude/projects/C--Users-Administrator/memory/MEMORY.md" && echo MEMORY_OK
test -f "$CCFM_WIKI_ROOT/wiki/HOTSHEET.md" && echo HOTSHEET_OK

# orchestrator grounding 적용 확인 (mllm-orchestrator 호출 시 첫 라운드 stdout 에 <context_grounding> 보여야 함)
python ~/.claude/skills/multi-llm-orchestrator/scripts/orchestrator.py ask "네이버 키워드 순위 도구"
```

## 한계 (자기 평가)

1. **LLM bypass**: instruction은 무시될 수 있다. 진짜 강제는 wrapper subprocess 가로채기 뿐. 현재는 dotfile + orchestrator inject 2중 방어.
2. **stop word 미흡**: "쓰는거야" 같은 동사 어미는 통과 (큰 문제는 아님 — 매칭 가치 낮은 토큰일 뿐)
3. **HOTSHEET 외 위키 미스캔**: `wiki/index.md` god nodes는 매칭 대상 아님. CCFM 비즈니스 도메인 트리거가 HOTSHEET에 없으면 0건. → HOTSHEET를 풍부하게 유지하는 게 운영 책임.
4. **Windows 의존**: install 스크립트는 PowerShell. macOS/Linux 사용자 추가되면 `install-codex-grounding.sh` 필요.

## 변경 이력

| 날짜 | 변경 | 비고 |
|---|---|---|
| 2026-05-05 | v1 초기 구축 | Opus 4.7 review로 P0 (mllm 우회) + P1 (조사 trim) 즉시 반영 |

## 관련

- [[ai-automation]] — 3-CLI 컨텍스트 브릿지 (CLAUDE.md/AGENTS.md/GEMINI.md 동기화)
- [[HOTSHEET]] — 트리거 → 진입점 단축표 (이 시스템의 매칭 대상)
- [[index]] — 위키 메인 인덱스
