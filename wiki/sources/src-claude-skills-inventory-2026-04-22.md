---
aliases: ["Claude 스킬·커맨드 인벤토리 (2026-04-22)"]
type: source
domain: vibe-coding
confidence: high
created: 2026-04-22
updated: 2026-04-22
sources:
  - ~/.claude/skills/ (스냅샷)
  - ~/.claude/commands/ (스냅샷)
snapshot_date: 2026-04-22
---

# Claude Code 스킬/커맨드 인벤토리 스냅샷 — 2026-04-22

CEO 최재명 로컬 머신(`C:\Users\gguy\.claude\`)에 설치된 Claude Code 스킬·슬래시커맨드 전수 목록. 다른 기기 이전 및 히스토리 보존 목적.

**원본 경로**
- 스킬: `~/.claude/skills/` (20개)
- 커맨드: `~/.claude/commands/` (18개 + `resources/`)
- Codex 지침: `~/.codex/AGENTS.md`

**백업 패키지** (USB/클라우드 이전용)
- `C:\Users\gguy\Desktop\claude-skills-package-20260422.zip` (286KB)

---

## 1. 스킬 목록 (20개)

### 파이프라인 핵심 — bob/dd/harness/eval/learnings
| 스킬 | 용도 | 최근 수정 |
|---|---|---|
| **bob** | 바이브 코딩 AI 협업 시스템 (SDD + DDD v2.0 + Context Engineering). Phase 0~8 파이프라인의 시작점 | 2026-04-10 |
| **bob-auto-spec** | 한 줄 프롬프트 → bob Spec 자동 생성. Phase 0 진입장벽 하향 | 2026-04-10 |
| **dd** | 계획서/Spec → step 폴더로 분해 (Divide & Deliver). 실행은 하지 않고 분해까지만 | 2026-04-10 |
| **dd-executor** | dd가 분해한 step 폴더를 순서대로 실행·조율하는 오케스트레이터 | 2026-04-10 |
| **harness** | 린터·pre-commit·구조 테스트로 모델 무관 결과(멱등성) 강제 | 2026-04-21 |
| **harness-auto-rules** | bob Spec + eval 결과에서 harness 린터 규칙 자동 생성 | 2026-04-10 |
| **eval** | Generator-Evaluator 독립 평가 (GAN 영감). 멀티 에이전트 품질 검증 | 2026-04-10 |
| **eval-feedback-loop** | eval 결과를 bob Spec·harness 규칙에 역류시키는 순환 피드백 루프 | 2026-04-10 |
| **eval-regression** | eval 시계열 추적·회귀 감지·품질 트렌드 분석 | 2026-04-10 |
| **learnings-engine** | 스킬 피드백 자동 수집·분류·랩업 시스템 | 2026-04-10 |
| **learnings-confidence** | learnings에 신뢰도 점수·시간 감쇠·프로젝트 격리 추가 | 2026-04-10 |
| **learnings-wrapup** | 세션 종료 전 피드백을 스킬 MD에 영구 반영 (학습 루프 마감) | 2026-04-10 |
| **cross-project-sync** | 프로젝트 간 검증된 패턴·규칙·learnings 동기화 | 2026-04-10 |

### 멀티 LLM 협업
| 스킬 | 용도 | 최근 수정 |
|---|---|---|
| **multi-llm-orchestrator** | Codex/Gemini/Claude CLI subprocess 병렬 호출 (ask/review/fix/debate/consensus 5모드) | 2026-04-17 |
| **code-fusion** | 에러 코드를 3개 LLM에 동시 수정 요청 → 최선 추출 통합 | 2026-03-10 |

### 실무 자동화
| 스킬 | 용도 | 최근 수정 |
|---|---|---|
| **1on1** | 원온원 미팅 녹음+화자분리(최대 6명) → Notion 면담기록 DB 자동 저장 | 2026-04-17 |
| **market-research** | 고객사 링크 1개 → 5개 서브에이전트 병렬 → Word 시장조사 리포트 1개 | 2026-04-10 |
| **psd-blueprint** | PSD 파싱 → 에셋+좌표 추출 → 99%+ 동일 이미지 기계 재현 (Photoshop COM 연동) | 2026-03-26 |
| **cleanup** | 작업 완료 후 중복 폴더/빈 폴더/임시 파일 자동 탐지·정리 | 2026-04-06 |

---

## 2. 슬래시 커맨드 목록 (18개)

### 워크플로우
| 커맨드 | 용도 |
|---|---|
| `/bob` | bob 스킬 직접 호출 (설계·Spec) |
| `/bdh` | BDH — bob + dd + harness 3단 파이프라인 원샷 |
| `/tdd` | RED-GREEN-REFACTOR 강제 사이클 |
| `/subagent` | 서브에이전트 디스패치 + 2단계 리뷰 (스펙 준수 → 코드 품질) |
| `/parallel` | 2개 이상 독립 태스크 병렬 에이전트 디스패치 |
| `/debug` | 체계적 디버깅 — 근본 원인 분석 없이 수정 금지 |
| `/verify` | 완료 전 검증 — 증거 없는 완료 주장 금지 |
| `/review` | 코드 리뷰 (서브에이전트 디스패치 + 기술 검증) |
| `/newc` | 코드 충돌/레거시 정리 |

### 멀티 LLM
| 커맨드 | 용도 |
|---|---|
| `/askall`, `/ask-all` | Codex/Gemini/Claude 병렬 질문 + 교차검증 + 종합 (v2.0 CLI 기반) |
| `/harness-build` | 하네스·계획서 컨텍스트 공유 Codex(초안) + Claude(테스트) 협업 빌드 |
| `/harness-audit` | Codex + Claude 서브에이전트 병렬 감사 → 통합 수정 지시 |

### 운영 모드
| 커맨드 | 용도 |
|---|---|
| `/safe-mode` | 위험 작업 자동 차단 |
| `/freeze-mode` | 지정 경로만 수정 허용 |
| `/free-mode` | 모든 제한 해제 |

### 문서/위키
| 커맨드 | 용도 |
|---|---|
| `/mds` | 프로젝트 md/계획서/hook 전체 최신 코드 기준 재작성 (150줄 제한, 초과 시 phase 분할) |
| `/wiki` | CCFM Wiki 작업 모드 (이 위키) |

---

## 3. 파이프라인 연결도

```
단독 실행 가능:
  /bob → Spec 생성
  /dd → step 분해
  /harness → 환경 강제
  /eval → 품질 평가
  /learnings-* → 피드백 순환

원샷 3단:
  /bdh = bob + dd + harness

풀 파이프라인 5단 (선형 → 순환):
  bob → dd → harness → eval → learnings
                ↑                  ↓
                └── feedback-loop ─┘
```

## 4. 관련 위키

- [[vibe-coding]] — 8-Phase 파이프라인, SDD/DDD 방법론
- [[ai-automation]] — 스킬 파이프라인 러닝 누적
- [[content-ai-automation]] — 컷편집/비전분석 자동화

## 5. 이전/설치 메모

새 기기 설치 순서:
1. zip 해제 → `skills/`, `commands/`, `codex/AGENTS.md` 확인
2. `cp -r skills/. ~/.claude/skills/`
3. `cp -r commands/. ~/.claude/commands/`
4. `cp codex/AGENTS.md ~/.codex/AGENTS.md`
5. Claude Code 재시작

**수동 이전 필요** (민감/환경 의존):
- `~/.claude/settings.json` (API 키·권한)
- `~/.codex/auth.json`, `~/.codex/config.toml`
- 플러그인은 새 기기에서 재설치
- auto-memory (`~/.claude/projects/.../memory/MEMORY.md`)
