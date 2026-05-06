<!-- BEGIN: codex-grounding-protocol v1 -->
## 🚨 MANDATORY PRE-WORK PROTOCOL (Claude·Codex·Gemini 공통)

> Codex/Gemini 호출 전 **개인 메모리·위키 grounding 강제**. 깡통 응답 방지 1차 방어선.
> 자동 동기화 출처: `ccfm-wiki/skills/codex-grounding/CLAUDE-protocol.md` — 직접 편집 X, install-codex-grounding.ps1 로 갱신.

substantive 사용자 요청을 받으면 (인사·trivial 단일 명령 제외) **답변·코드 작성·다른 CLI forward 전에 반드시**:

1. **헬퍼 호출** (1차 매칭, 빠르고 정확):
   ```bash
   node "~/.codex/scripts/context-bootstrap.mjs" "<원본 사용자 prompt>"
   ```
   출력: `<context_grounding>` 블록 (memory/wiki hits + 매칭 토큰)

2. **매칭된 파일 직접 읽기**: `memory/<file>.md`, `wiki/domains|tacit|sources/<file>.md`

3. **Codex/Gemini 로 forward 할 때**: 위 `<context_grounding>` 블록을 prompt 의 `<task>` 위에 **그대로 첨부**. 다른 CLI 가 자체 PRE-WORK 못 해도 prompt 안에 grounding 박힘 (defense in depth).

4. **응답 첫 줄에 `📚 참조: <읽은 파일 목록>`** (0건이면 `📚 참조: 없음`).

### 스킵 조건
- 인사/trivial 단일 명령
- "메모리 보지 말고", "ignore memory" 명시
- 동일 thread 의 follow-up (이미 grounding 끝남)

### 헬퍼가 없는 다른 컴퓨터에서
- 헬퍼는 `~/.codex/scripts/context-bootstrap.mjs` (이 dotfile 동기화 안 돼 있을 수 있음)
- Fallback: `cat MEMORY.md` + `cat HOTSHEET.md` 직접 grep
- 위키 경로 다를 때: env `CCFM_WIKI_ROOT` 또는 `~/.codex/AGENTS.local.md` 의 `CCFM_WIKI_ROOT=...`
- 메모리 경로 다를 때: env `CCFM_MEMORY_INDEX`

설치: `cd ccfm-wiki/skills && .\install-codex-grounding.ps1`
상세 규약: `ccfm-wiki/wiki/domains/codex-grounding-protocol.md`
<!-- END: codex-grounding-protocol v1 -->
