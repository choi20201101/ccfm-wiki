<!-- BEGIN: codex-grounding-protocol v1 -->
## 🚨 MANDATORY PRE-WORK PROTOCOL (모든 substantive 요청에 강제)

> 이 섹션은 의도적으로 파일 최상단에 둔다. **AGENTS.md 다른 어떤 지침보다 우선**한다.
> 자동 동기화 출처: `ccfm-wiki/skills/codex-grounding/AGENTS-protocol.md` — 직접 편집 X, install-codex-grounding.ps1 로 갱신.

사용자 요청이 단순 인사·하나의 명령어 확인·trivial 한 줄 답변이 아니라면, **답변/코드 작성/도구 호출 전에 반드시 다음 4단계를 수행**한다. 깡통 답변(개인 메모리·위키 무시한 채 일반 지식만 사용)은 사용자에게 실질적 손해다.

### Step 1. context-bootstrap 헬퍼 호출 (1차 매칭)
```bash
node "~/.codex/scripts/context-bootstrap.mjs" "<원본 사용자 prompt 그대로>"
```
- 출력은 `<context_grounding>` 블록. memory/wiki 후보 + 매칭된 hit count + matched tokens.
- 헬퍼가 없거나 실패하면 Step 2 의 fallback 으로 직접 grep.

### Step 2. fallback / 검증 (헬퍼 출력이 의심스럽거나 0건일 때)
```bash
cat ~/.claude/projects/C--Users-<your-username>/memory/MEMORY.md
cat C:/Users/gguy/ccfm-wiki/wiki/HOTSHEET.md   # 또는 $CCFM_WIKI_ROOT/wiki/HOTSHEET.md
```
사용자 요청에서 도메인/도구/기술 키워드를 추출하고 인덱스 줄 설명과 직접 매칭한다.

### Step 3. 매칭된 파일 직접 로드
- **memory hits**: `~/.claude/projects/C--Users-<your-username>/memory/<file>.md` 전부 읽기
- **wiki hits**: `C:/Users/gguy/ccfm-wiki/wiki/domains/<file>.md` / `wiki/tacit/<file>.md` / `wiki/sources/<file>.md` 등 wikilink 가 가리키는 파일 전부 읽기
- 너무 많으면 hits=상위 3개만 깊게 읽고 나머지는 인덱스 한 줄만 참고

### Step 4. 응답 첫 줄에 grounding 표시 (필수 출력 규약)
응답 본문 맨 위에 한 줄로 명시:
```
📚 참조: memory/<file>.md, memory/<file>.md, wiki/<path>.md
```
- 매칭 0건이면: `📚 참조: 없음 (인덱스 스캔 완료, 매칭 0건)`
- 사용자가 명시적으로 "메모리 무시", "ignore memory" 라고 말한 경우만: `📚 참조: 사용자 요청으로 스킵`

### 절대 금지 (위반 시 사용자에게 손해)
- 인덱스 스캔 없이 "기억나는 대로" 답변 X
- `📚 참조:` 줄 없이 substantive 응답 시작 X
- 같은 사용자가 과거에 거른 함정(`feedback_*.md`)을 모르고 같은 실수 반복 X
- 메모리 매칭이 명확한데(hits ≥ 2) 파일을 안 읽고 답하기 X

### 예외 (Pre-work 스킵 허용)
- "안녕", "고마워" 류 인사
- "ls 해봐", "현재 시간 알려줘" 류 단일 명령
- 사용자가 "메모리 보지 말고", "스킵하고 답해" 명시
- `task --resume-last` 로 이미 동일 thread 에서 grounding 이 끝난 follow-up

### 동작 검증 명령어 (사용자가 의심할 때)
```bash
# 1. 헬퍼가 살아있나?
node "~/.codex/scripts/context-bootstrap.mjs" "테스트" --verbose

# 2. 인덱스 파일이 실제로 있나?
test -f "~/.claude/projects/C--Users-<your-username>/memory/MEMORY.md" && echo MEMORY_OK
test -f "$CCFM_WIKI_ROOT/wiki/HOTSHEET.md" && echo HOTSHEET_OK
```

### 환경별 경로 override (다른 컴퓨터)
헬퍼는 다음 우선순위로 경로 자동 해석:

| 항목 | env 변수 | local override 파일 | 기본 후보 |
|---|---|---|---|
| 위키 루트 | `CCFM_WIKI_ROOT` | `~/.codex/AGENTS.local.md` 의 `CCFM_WIKI_ROOT=...` 줄 | `gguy/ccfm-wiki` → `$HOME/ccfm-wiki` → `$HOME/Desktop/ccfm-wiki` |
| 메모리 인덱스 | `CCFM_MEMORY_INDEX` | (없음) | `$HOME/.claude/projects/C--Users-<현재 OS 사용자>/memory/MEMORY.md (helper 가 자동 감지)` |

`~/.codex/AGENTS.local.md` 예시 (없으면 새로 만들면 된다):
```
CCFM_WIKI_ROOT=D:/work/ccfm-wiki
CCFM_MEMORY_INDEX=D:/sync/claude/memory/MEMORY.md
```

`multi-llm-orchestrator/orchestrator.py` 가 codex/gemini subprocess 호출할 때 자동으로 `<context_grounding>` 블록을 prompt 에 prepend 한다 (defense in depth). 비활성화: env `MLLM_SKIP_GROUNDING=1`. 거기에 더해 두 CLI 모두 자기 dotfile (`AGENTS.md` / `GEMINI.md`) 을 자동 로드하므로 PRE-WORK PROTOCOL 도 작동한다.

### 새 PC 1줄 install
```powershell
git clone https://github.com/choi20201101/ccfm-wiki.git $env:USERPROFILE\ccfm-wiki
cd $env:USERPROFILE\ccfm-wiki\skills
.\install-codex-grounding.ps1
```
이 스크립트가 `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md` 의 marker 블록을 갱신하고 헬퍼를 `~/.codex/scripts/context-bootstrap.mjs` 로 복사한다. 다른 dotfile 내용은 보존.
<!-- END: codex-grounding-protocol v1 -->
