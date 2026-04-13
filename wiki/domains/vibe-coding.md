---
type: domain
domain: vibe-coding
confidence: medium
created: 2026-04-13
updated: 2026-04-13
sources:
  - 협업 메뉴얼/바이브코딩_AI협업_지침_v2.0.md (v2.0, 2026-02-24)
  - ~/.claude/skills/bob/SKILL.md (8-Phase 반영본)
  - 협업 메뉴얼/바이브 코딩시행착오 케이스 CCFM.pdf
---

# 바이브코딩 & 클로드 스킬 (Vibe Coding & Claude Skills)

## 개요

CCFM의 AI 협업 개발 표준. SDD(Spec Driven Development) + DDD(Domain Driven Design) + 컨텍스트 엔지니어링을 통합한 "바이브 코딩" 방법론.

핵심 슬로건:
- "AI에게 추측하게 하지 말고, 명시적으로 알려줘라."
- "AI는 그냥 쓰면 50점, 시스템을 만들어주면 95점짜리 에이스가 된다."
- "주문서(Spec) 없는 코딩은, 설계도 없는 건축과 같다."

## AI 실수 5대 원인 ↔ 해법 매트릭스

| 원인 | 증상 | 해법 |
|---|---|---|
| 방향 부재 | 엉뚱한 기능 구현 | **SDD** — Spec 먼저 |
| 맥락 부족 | 잘못된 패턴/경로 추측 | **DDD** — 비즈니스 언어 = 코드명 |
| 지침 무시(금붕어 기억력) | 매뉴얼 안 읽음 | **Hook + skill-rules.json** — 자동 활성화 |
| 검증 부재 | 깨진 코드 방치 | **자동 QC** — 완료 직후 build-check |
| 컨텍스트 롯(Context Rot) | 앞 규칙 망각, 같은 실수 반복 | **컨텍스트 엔지니어링** — 대화 < 문서, 30~40% 유지 |

## 8-Phase 파이프라인 (bob 스킬 기준)

원본 v2.0은 7-Phase, 현재 bob 스킬은 컨텍스트 엔지니어링(Phase 0.5)과 Harness(Phase 7)를 추가한 **8-Phase** 확장판을 사용한다.

```
Phase 0   SDD — Spec 작성 (최우선, 건너뛰기 금지)
Phase 0.5 컨텍스트 엔지니어링 — Context Rot 방지
Phase 1   CLAUDE.md — 프로젝트 기억 계층 (5~15KB)
Phase 2   Skills — SKILL.md + resources/ Progressive Disclosure
Phase 3   skill-rules.json — 3중 트리거(키워드/의도/파일경로) 자동 활성화
Phase 4   Agents + 외부 기억(plan/context/tasks/state 4대 문서)
Phase 5   Hooks — skill-activation / post-tool-tracker / build-check
Phase 6   /insight — 마찰 분석 기반 지속 개선 (2~4주 주기)
Phase 7   Harness — 린터·pre-commit·구조 테스트로 모델 무관 결과 강제
Phase 8   코드 작성 시작
```

Phase 0~7 인프라 구축에 30분~1시간 투자 → 이후 수십 시간 디버깅 비용 절약. 이게 안 되면 바이브 코딩은 50점짜리 실험에서 끝난다.

## Phase별 핵심 규칙 (요약)

### Phase 0 — SDD Spec
- 기술 스택은 **버전까지** 명시 ("React" 아님, "React 19 + Next.js 15 App Router")
- 경로는 **복붙 가능하게** ("`backend.main:app`")
- 패턴은 **코드 예시**와 함께
- 검증은 **실행 가능한 명령어**로 ("`pytest backend/tests/ -v`")
- 단계는 **Small Chunks**로 (Phase별 산출물 + 검증 방법 표)

### Phase 1 — CLAUDE.md
- 프로젝트 구조(트리) / 기술 스택 / 실행 명령어 / 아키텍처 패턴 / **흔한 실수 경고** / 작업 프로세스 / 배포
- 실수하기 쉬운 포인트는 반드시 명시적 경고 ("모듈 경로는 `backend.main:app`이지 `app.main:app`이 아님")

### Phase 3 — skill-rules.json
- `suggest` vs `block` 구분. 보안/프레임워크 호환성/브랜드 가이드는 **block**.
- 한국어 + 영어 키워드 양쪽 포함.
- `pathPatterns`가 실제 프로젝트 구조와 일치해야 활성화됨.

### Phase 4 — 에이전트 필수 세트
- planner / plan-reviewer / code-architecture-reviewer / auto-error-resolver / documentation-architect
- 외부 기억 4대 문서: `dev/active/[task]/` 아래 `[task]-plan.md`, `[task]-context.md`, `[task]-tasks.md`, `[task]-state.md`(bob 확장)
- state.md는 확정 결정/변경된 결정을 자동 감지해 누적 ("~로 결정/확정" → 추가, "~는 아니다/버리자" → 변경 로그).

### Phase 5 — Hook 운영 주의
- Stop 훅은 실패 시 작업 종료 자체를 블록함 → **수동 테스트 후** 등록. 소형 프로젝트는 생략 가능.
- skill-activation(작업 전), post-tool-tracker(파일 수정 직후), build-check(완료 시) 3종이 기본.

### Phase 7 — Harness
- 린터·구조 테스트·pre-commit으로 "어떤 AI를 쓰든 동일한 결과물" 강제(멱등성).
- Spec의 "필수/금지"를 CLAUDE.md 규칙으로 자동 추출하는 harness-auto-rules와 연결.

## DDD 관통 원칙 (모든 Phase에 적용)

- **3파일 세트**: `domain/[도메인명]/` 아래 `model.py` / `repository.py` / `service.py`.
- **첫 도메인은 반드시 수동 작성** — AI에게 완벽한 패턴을 보여주는 학습용 기준.
- **비즈니스 언어 = 코드명** — 현업 용어를 그대로 함수/파일명에 반영(추측 의존도↓).
- **도메인 간 격리** — A가 B의 repository를 직접 호출하지 않는다.
- **패턴 복제 지시** — "유저 도메인 패턴 그대로 결제 도메인 만들어"가 가장 정확한 프롬프트.

## bob 확장 파이프라인 (순환형)

```
bob → dd → dd-executor → harness → eval
 ↑                                   │
 └── eval-feedback-loop ←────────────┘
```

- `bob-auto-spec`: 한 줄 요청 → Spec 초안 (Phase 0 자동화)
- `dd` / `dd-executor`: 계획서를 step 폴더로 분해 → 순차/병렬 실행 조율
- `harness-auto-rules`: Spec의 "필수/금지" → CLAUDE.md 규칙으로 자동 추출
- `eval-feedback-loop`: eval 실패 패턴 → bob Spec 수정 제안으로 역류 (직선 파이프라인을 순환형으로 완성)
- `eval-regression`: 품질 추이 시계열 + 회귀 감지
- `learnings-confidence`: 피드백에 0.3~0.9 신뢰도 + 시간 감쇠 + 프로젝트 격리
- `cross-project-sync`: 3개 이상 프로젝트에서 검증된 패턴만 글로벌 승격

## /insight 피드백 루프

- 2~4주 사용 후 `/insight`로 **마찰 패턴**(예: "코드 작성 전 Spec 확인 안 함") 추출
- 구체적 수치(세션 횟수 등)는 **부정확할 수 있음** — 경향성만 신뢰
- 추출된 마찰 패턴은 skill-rules.json 또는 에이전트 규칙으로 반영

## 환경 설정 (CCFM 공용)

- Windows (gguy / Administrator) + WSL Ubuntu 혼용
- PowerShell / Git Bash
- Desktop Commander MCP는 경로 제한 — Windows 경로는 정방향 슬래시 필요
- WSL ↔ Windows 경로 변환 (`/mnt/c/` ↔ `C:\`)
- 한글/이모지 콘솔 출력: `PYTHONIOENCODING=utf-8` + `chcp 65001` 기본 장착

## 멀티 IDE 호환 매핑

| Claude Code | Cursor | Codex CLI | Antigravity |
|---|---|---|---|
| `CLAUDE.md` | `.cursor/rules/*.mdc` | `AGENTS.md` | `.agent/rules/*.md` |
| `.claude/skills/` | `.cursor/rules/` | AGENTS.md 섹션 | `.agent/skills/` |
| `.claude/agents/` | N/A | N/A | N/A |
| `CLAUDE.local.md` | Settings > Rules | `AGENTS.override.md` | `~/.gemini/GEMINI.md` |

## v1.0 → v2.0 핵심 변경 (2026-02-24)

- **최우선 단계**: Phase 1(CLAUDE.md) → **Phase 0(SDD Spec)**
- **DDD 위치**: Phase 2 Skills 내부 → **별도 관통 원칙으로 격상**
- **기억 장치**: 언급만 → **3대 문서 의무화**(bob 확장 후 4대 문서)
- **품질 검증**: Hook 기반 → **Hook + 셀프 체크 리마인더 + 교차 검증**
- **지속 개선**: 없음 → **/insight 피드백 루프 추가**

## 시행착오·주의 패턴 (CCFM 실측)

Phase 0~5를 건너뛰고 코딩했을 때 반복 관찰된 실패:

- Phase 0 생략 → AI가 추측에 의존, 재작업 반복 (1시간 Spec 투자가 수십 시간 디버깅 절약)
- CLAUDE.md 부재 → AI가 같은 질문을 반복 + 방향 상실
- skill-rules.json 미설정 → 스킬이 자동 활성화되지 않음("금붕어 기억력")
- 에이전트 미분업 → 한 AI가 계획/검증/코딩/디버깅을 다 하며 맥락 누적 오류
- Hook 없음 → AI의 "다 했습니다"가 실제로는 깨진 코드
- /insight 루프 부재 → 같은 실수가 반복

추가 시행착오는 [[coding-lessons]] (wiki/tacit/coding-lessons.md) 의 "Desktop/MD 멀티 프로젝트 시행착오 모음" 섹션 참조.

## 관련 페이지

- [[ai-automation]] — 스킬 파이프라인 운영·학습 누적
- [[content-ai-automation]] — 컷편집/비전/자막 자동화 실전
- [[marketing-automation]] — 광고 플랫폼 자동화(GFA/Meta/네이버)
- [[coding-lessons]] — 크로스 프로젝트 시행착오 회고 (tacit)
- [[creative-patterns]] — PSD/DA 크리에이티브 조립 패턴 (tacit)

## 관련 스킬(로컬)

`~/.claude/skills/` 아래:
- bob / bob-auto-spec — Phase 0~8 주문서 및 셋업
- dd / dd-executor — 계획 분해·실행
- harness / harness-auto-rules — 환경 강제, 규칙 자동화
- eval / eval-feedback-loop / eval-regression — 품질 평가·역류·회귀
- learnings-engine / learnings-wrapup / learnings-confidence / cross-project-sync — 학습 누적·전파
