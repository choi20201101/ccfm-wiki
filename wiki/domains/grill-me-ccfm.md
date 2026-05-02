---
aliases: ["grill", "캐물어 스킬", "방향성 grill"]
type: domain
domain: vibe-coding
confidence: high
created: 2026-05-02
updated: 2026-05-02
sources:
  - ~/.claude/skills/grill-me-ccfm/SKILL.md
  - ccfm-wiki/skills/grill-me-ccfm/  (글로벌 동기화 원본)
  - Matt Pocock 원본 grill-me 스킬
related:
  - "[[vibe-coding]]"
  - "[[ai-automation]]"
  - "[[ma-exit]]"
  - "[[content-ai-automation]]"
  - "[[taiwan-market]]"
---

# grill-me-ccfm — 결정 분기 끈질기게 캐묻기 스킬

> "콘텐츠는 '뭘 보여줄지'보다 '뭘 안 보여줄지'가 더 중요하다.
> 코드는 '뭘 만들지'보다 '뭘 안 만들지'가 더 중요하다.
> 큰 결정은 '되돌릴 수 있나'를 먼저 물어야 한다."

Matt Pocock의 grill-me 스킬을 CCFM 맥락(코딩 + 콘텐츠 + 전략 + 개인)으로 확장한 버전. **bob 스킬 앞단** 또는 **단독**으로 동작.

---

## 핵심 차별점 — 기존 스킬과의 경계

| 스킬 | 역할 | 입력 | 출력 |
|------|------|------|------|
| **grill-me-ccfm** | 모호한 요청에서 **방향성 + Don't List** 합의 | 한 줄 요청 | `grill-result.yaml` (Direction + Don't List) |
| bob-auto-spec | 모호한 한 줄 → bob Spec **초안** 자동 생성 | 한 줄 요청 | Spec 초안 (Goal/Scope/Constraints) |
| bob | SDD/DDD/Context Engineering 8-Phase 오케스트레이션 | (Spec 또는 grill-result) | 4대 문서 + 구현 |
| harness-auto-rules | Spec/eval에서 **린터 규칙** 자동 생성 | Spec, eval 결과 | 린터 룰 파일 |

**중첩 회피 원칙**:
- 입력이 **명확**하고 **되돌릴 수 있으면** → bob-auto-spec → bob
- 입력이 **모호**하거나 **되돌리기 어려우면** (M&A, 출산, 신규시장, 콘텐츠 규제) → **grill-me-ccfm 먼저** → 그 다음 bob
- grill-me-ccfm 의 산출물(`grill-result.yaml`)은 bob-auto-spec 의 입력이 될 수 있음 (보완 관계, 충돌 X)

---

## 발동 조건

### 자동 (Ambiguity Score ≥ 5)
`scripts/ambiguity_scorer.py` 가 사용자 입력을 점수화:

| 신호 | 점수 |
|------|------|
| 입력 < 20자 | +5 |
| 입력 < 50자 | +3 |
| 모호한 표현 (대충/알아서/적당히) | +3 |
| 결정 분기 ≥ 5개 (또는·vs·?·고민·어떤) | +2 |
| CCFM 핵심 컨텍스트 누락 (brand·channel·market 중 2개+) | +2 |
| 콘텐츠 모드인데 Don't List/규제 미언급 | +2 |
| 명시적 grill 키워드 | +5 |

### 수동
"grill해줘", "꼼꼼하게 캐물어", "방향 잡아줘", "하지 말아야 할 거 정리"

### 강제 발동 (점수 무시, 999점)
- 전략 되돌리기 어려움: M&A, 매각, 인수, 클로징, 조직개편, 인사이동, 해고
- 신규 진출: 신제품 출시, 신규 시장, 대만/동남아/해외 진출
- 개인 되돌리기 어려움: 출산, 산후, 육아, 신생아

---

## 4모드

| 모드 | 1순위 질문군 | 핵심 산출 |
|------|------------|----------|
| **coding** | 환경(gguy/Administrator/lost2)·레포·기존 스킬 재사용 | 일회성 vs 반복, 멱등성, 실패 복구 |
| **content** ⭐ | 브랜드·제품·채널·시장·목표·타겟·톤 | **Don't List** (시장×제품 자동 규제 체크) |
| **strategy** | Reversibility·Stakeholders·Trade-offs | ADR (`14-decisions/`) |
| **personal** | D-day·가용성·의료진 권고 | Logistics |

### Content 모드 자동 규제 체크 (대만 화장품 예시)
- 의사·약사·약국 등장 금지
- 효능 단정형 카피 금지 (TFDA)
- Before/After 비교 컷 금지
- 한자 간체 금지 (반드시 번체)

→ 시장+제품군 조합으로 4~6개 Don't List 자동 제시 → 합의 → `grill-result.yaml.dont_list[]` 에 기록.

---

## 운영 8원칙

**Matt 원본 4원칙 (절대 변경 금지)**
1. 한 번에 하나씩 질문 (묶음 질문 금지)
2. 각 질문에 추천 답변 제시 ("내 추천은 A, 이유는...")
3. 결정 트리 분기를 의존성 순서로 해소
4. 사용자 "ok 됐어" 할 때까지 끈질기게

**CCFM 추가 4원칙**
5. 격식 없는 한국어 (존댓말 X, 반말 X, 자연체)
6. 모드 자동 식별 (coding/content/strategy/personal) 첫 줄 명시
7. 금기사항(Don't List)과 방향성(Direction) **분리 추적**
8. 체크인 의무 (10분 또는 8개 질문마다 "지금까지 정리할까?" 자동 제안)

---

## 핸드오프 산출물

### `grill-result.yaml` (스키마: [grill-result.schema.yaml](../../skills/grill-me-ccfm/schema/grill-result.schema.yaml))
필수: `version, mode, topic, session_at, duration_min, question_count, direction, ambiguity_remaining, next_step`
- `ambiguity_remaining: []` 비어있어야 다음 단계 진입 OK
- `next_step: bob | dd | direct_execution | hold`

### ADR 자동 저장 (옵션)
`adr.save_to_wiki: true` 면 `wiki/14-decisions/{date}-{topic}.md` 에 ADR 형식으로 저장. 같은 결정 두 번 grill 안 하도록.

---

## 종료 신호 (즉시 grill 중단)

- "ok 충분해" / "됐어 만들자" / "그만"
- "이제 bob 가자" / "코드 짜줘" / "영상 만들어줘"
- "컨텍스트 충분" / "더 물을 거 없으면 정리해줘"

---

## 멀티 LLM 모드 (Claude + GPT-5.5 / Gemini)

이 스킬은 CLI 중립이라 동일한 SKILL.md를 세 CLI가 모두 따른다.

### 단일 모델
| CLI | 모델 | 호출 |
|-----|------|------|
| Claude Code/Desktop | Opus/Sonnet | `grill해줘 — <topic>` (네이티브) |
| Codex CLI | **GPT-5.5** (frontier 프로필) | `codex --profile frontier "grill-me-ccfm: <topic>"` |
| Codex CLI | GPT-5.4 (codex 기본) | `codex "grill-me-ccfm: <topic>"` |
| Gemini CLI | gemini-2.5-flash | `gemini "grill-me-ccfm: <topic>"` |

세 CLI 모두 동일한 `grill-result.yaml` 스키마로 산출 → 다음 단계(bob/dd/직접실행) 변경 없음.

### 병렬 (Claude + GPT-5.5 동시 grill, 차이만 사용자 선택)
큰 결정(M&A·신제품·콘텐츠 규제) 권장:

```bash
# Claude Code 안에서 디스패치
claude "/mllm-debate grill: <topic> — Claude vs Codex(GPT-5.5) 14문항 비교"

# 또는 PowerShell 병렬 호출
$topic = "메라블 루비알엔 앰플클렌저 대만 인스타 릴스"
Start-Job { codex --profile frontier "grill-me-ccfm: $using:topic" }
claude "grill-me-ccfm: $topic"
```

### 사용 기준
| 케이스 | 모드 |
|--------|------|
| 일상 모호함 (점수 5~7) | Claude 단일 |
| 콘텐츠 규제·시장 진출 (점수 ≥ 8) | Claude + GPT-5.5 병렬 |
| 법/회계/계약 검토 | 3중 (`/mllm-consensus`) |

### 안티패턴
- ❌ 두 모델 답변 단순 평균 — 차이가 정보의 핵심
- ❌ 톤 강제 통일 — Claude 부드러움 / GPT-5.5 직설은 신호로 보존
- ❌ 모든 grill 멀티 LLM — 토큰 낭비. 강제 발동(M&A·출산 등) 또는 점수 ≥ 8만

---

## 글로벌 설치 (모든 컴퓨터)

원본은 위키 동기화 (`ccfm-wiki/skills/grill-me-ccfm/`).

```powershell
# 새 PC 부트스트랩
cd $env:USERPROFILE\ccfm-wiki\skills
.\install-grill-me-ccfm.ps1            # 복사 모드 (안전)
.\install-grill-me-ccfm.ps1 -Symlink   # 심볼릭 링크 (git pull 시 자동 갱신, 관리자 권한)
```

설치 위치: `~/.claude/skills/grill-me-ccfm/` → Claude Code + Desktop 양쪽이 시작 시 자동 로드.

---

## 안티 패턴 (하면 안 되는 것)

1. ❌ 묶음 질문 ("어느 브랜드고 어느 채널이고 어느 시장이야?")
2. ❌ 추천 답변 없이 질문 ("어떻게 할래?")
3. ❌ 사용자 입력 없이 임의로 결정 트리 채우기
4. ❌ Don't List 를 Direction 에 섞어 쓰기
5. ❌ 종료 신호 무시
6. ❌ 영문/존댓말 답변 (CCFM 톤 아님)

---

## 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-05-02 | 초기 풀세트 (Matt 원본 + CCFM 4원칙 + 4모드 + 자동 게이트). Windows cp949 인코딩 버그 수정 (UTF-8 강제 출력). |
| - | 2026-05-02 | 위키 동기화 + 글로벌 부트스트랩 스크립트 추가 |
