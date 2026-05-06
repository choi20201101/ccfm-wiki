<!-- BEGIN: codex-grounding-protocol v1 -->
## 🚨 MANDATORY PRE-WORK PROTOCOL (모든 substantive 요청 강제)

> Codex / Claude 와 동일한 grounding 규약. 깡통 답변(개인 메모리·위키 무시) 방지.
> 자동 동기화 출처: `ccfm-wiki/skills/codex-grounding/GEMINI-protocol.md` — 직접 편집 X, install-codex-grounding.ps1 로 갱신.

substantive 요청 (인사·trivial 단일 명령 제외) 을 받으면 **답변·코드 작성 전에 반드시** 다음 절차를 수행한다.

### Step 1. context-bootstrap 헬퍼 호출
```bash
node "~/.codex/scripts/context-bootstrap.mjs" "<원본 사용자 prompt>"
```
출력은 `<context_grounding>` 블록 — memory/wiki 후보 + 매칭 hit count.

### Step 2. fallback (헬퍼 없는 다른 컴퓨터)
```bash
cat ~/.claude/projects/C--Users-<your-username>/memory/MEMORY.md
cat <CCFM_WIKI_ROOT>/wiki/HOTSHEET.md
```
키워드 매칭은 직접 grep.

### Step 3. 매칭된 파일 직접 로드
- memory hits: `memory/<file>.md` 전부 읽기
- wiki hits: `wiki/domains|tacit|sources/<file>.md` 읽기
- hits 많으면 상위 3개만 깊게

### Step 4. 응답 첫 줄 grounding 표시
```
📚 참조: memory/<file>.md, wiki/<path>.md
```
0건이면 `📚 참조: 없음 (인덱스 스캔 완료, 매칭 0건)`

### 절대 금지
- 인덱스 스캔 없이 "기억나는 대로" 답변
- 같은 사용자가 거른 함정(`feedback_*.md`) 무시하고 같은 실수 반복
- `📚 참조:` 줄 없는 substantive 응답

### 다른 컴퓨터 / 환경
- 헬퍼 경로(`~/.codex/scripts/context-bootstrap.mjs`)가 없으면 위 fallback 으로 대체
- 위키 경로 override: env `CCFM_WIKI_ROOT` 또는 `~/.codex/AGENTS.local.md` 의 `CCFM_WIKI_ROOT=...`
- 메모리 경로 override: env `CCFM_MEMORY_INDEX`

설치: `cd ccfm-wiki/skills && .\install-codex-grounding.ps1`
상세 규약 + 다른 컴퓨터 설치 가이드: `ccfm-wiki/wiki/domains/codex-grounding-protocol.md`
<!-- END: codex-grounding-protocol v1 -->
