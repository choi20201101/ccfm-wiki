---
name: grill-me-ccfm
description: |
  사용자의 계획·디자인·콘텐츠 방향성을 결정 트리 분기마다 끈질기게 캐물어
  암묵 가정을 드러내고, "할 것"과 "하지 말아야 할 것"을 명시적으로 합의하는 스킬.
  코딩 작업뿐 아니라 콘텐츠 기획(영상/이미지/카피), 조직·사업 같은 전략 결정,
  건강·생활 같은 개인 영역까지 활용 가능.
  bob 스킬 앞단에서 자동 발동되거나, 사용자가 "grill", "캐물어", "꼼꼼하게",
  "방향 잡아줘", "하지 말아야 할 거 정리" 등을 언급할 때 트리거.
trigger_keywords:
  - grill
  - 캐물어
  - 꼼꼼하게
  - 확실히 정리
  - 방향성 잡아줘
  - 하지 말아야 할 거
  - 컨셉 잡기 전에
  - 본격적으로 만들기 전
  - bob 들어가기 전
modes:
  - coding       # 코드/스킬/자동화 설계
  - content      # 영상/이미지/카피 등 크리에이티브
  - strategy     # 조직/사업/계약 결정
  - personal     # 건강/생활/일상
---

# grill-me-ccfm

> Matt Pocock의 grill-me 원본을 CCFM 맥락에 맞게 확장한 버전.
> 원본 핵심: "Interview the user relentlessly until decision tree is resolved."
> 확장 포인트: 콘텐츠 모드, 한국어/격식없는톤, CCFM 도메인 우선 질문, ADR 자동 저장.

---

## 🎯 발동 조건

### 자동 발동
`ambiguity_scorer.py` 가 점수 5점 이상 매기면 bob이 자동 호출.

### 수동 발동
사용자가 다음 중 하나라도 말하면 즉시 시작:
- "grill해줘" / "꼼꼼하게 캐물어"
- "이거 만들기 전에 방향 잡자"
- "하지 말아야 할 거 먼저 정리"
- "컨셉 grill"

### 강제 발동 (점수 무시)
다음 키워드는 무조건 grill 진입 (되돌리기 어려운 결정):
- 신제품 출시 / 신규 시장 / 해외 진출
- 조직개편 / 인사이동
- 사용자가 본인 키워드 추가 가능 (`scripts/ambiguity_scorer.py` HARD_TRIGGERS)

---

## 📐 운영 원칙 (Matt 원본 4원칙 + CCFM 4원칙)

### 원본 4원칙 (절대 변경 금지)
1. **한 번에 하나씩 질문** — 묶음 질문 금지
2. **각 질문에 추천 답변 제시** — "제 추천은 A입니다, 이유는..."
3. **결정 트리 분기를 하나씩 해소** — 의존성 순서대로
4. **공유 이해 도달까지 끈질기게** — 사용자가 "ok 됐어"라 할 때까지

### CCFM 추가 4원칙
5. **격식 없는 한국어** — 존댓말 X, 반말 X, "~할까요?" 같은 자연체
6. **모드 자동 식별** — coding/content/strategy/personal 중 추정 후 첫 줄에 명시
7. **금기사항(Don't List) 별도 추적** — "할 것"과 "안 할 것"을 분리 수집
8. **체크인 의무** — 10분 / 8개 질문 경과 시 "지금까지 정리할까?" 자동 제안

---

## 🎬 모드별 질문 템플릿

### 🖥️ Coding 모드

**1순위 (Context)**
- 어느 환경? (Windows gguy / Administrator / lost2 / WSL Ubuntu)
- 어느 레포? (ccfm / ccfm-wiki / 신규)
- 기존 스킬 재사용? (bob/dd/harness/eval/learnings)

**2순위 (Decision Tree)**
- 일회성 vs 반복?
- 사람 개입 지점은?
- 실패 복구 전략?
- 멱등성 필요?

**3순위 (Constraints)**
- 데드라인?
- 토큰/비용 제약?
- 누가 유지보수?

---

### 🎨 Content 모드 ← 🆕 사용자 요청 반영

**핵심 철학:**
> "콘텐츠는 '뭘 보여줄지'보다 '뭘 안 보여줄지'가 더 중요하다.
> 특히 CCFM은 화장품/의료/식품 광고 규제가 빡빡하므로 Don't List가 곧 컴플라이언스."

**1순위 (방향성 — Direction)**
- 어느 브랜드? (Merable / Rusolve / 부위부위 / 클라이언트 ID)
- 어느 제품? (제품명 정확히)
- 어느 채널/플랫폼? (인스타 릴스 / 유튜브 쇼츠 / 메타 DA / 네이버 / 틱톡)
- 어느 시장? (한국 / 대만 / 동남아) ← 시장에 따라 규제 다름
- 캠페인 목표? (인지 / 전환 / 리텐션)
- 타겟? (연령/성별/관심사/페르소나)
- 톤앤매너? (전문가 / 친근 / 유머 / 감성)

**2순위 (금기사항 — Don't List) ⭐ 최중요**
모드 진입 시 **자동으로 시장×제품×채널 조합 규제 체크**:

| 시장 | 제품군 | 자동 체크 항목 |
|------|--------|---------------|
| 한국 | 화장품 | 의약품 오인 표현, 효능 단정, 비교 광고, 사용 전후 |
| 한국 | 식품/건기식 | 질병 치료/예방 표현, "최고/유일" 표현 |
| 대만 | 화장품 | 의사/약사/약국 등장, 의료 행위 연상, 효능 단정 |
| 대만 | 모든 제품 | 중국어 간체 사용 (반드시 번체) |
| 동남아 | 화장품 | 할랄 미인증 시 무슬림 타겟 광고 |
| 모든 곳 | 모든 제품 | 경쟁사 비방, 인증 허위 표시, 통계 출처 없는 인용 |

**질문 예시:**
> "이 영상에 의사 캐릭터 등장 시킬 거야? (대만 송출이면 무조건 NO)"
> "Before/After 비교 컷 넣을 거야? (한국 화장품법 위반 가능)"
> "효능을 단정형으로 표현? 아니면 사용감 위주?"

**3순위 (구현 디테일)**
- 분량/길이 (15초 / 30초 / 60초)
- 자막 스타일 (상단고정 / 하단고정 / 음성싱크)
- 세이프존 (플랫폼별 자동 적용)
- 1초 컷 리듬 적용 여부
- 음악/TTS/무음
- 제품 누끼 위치
- 레퍼런스 영상 분석 결과 반영 여부

**4순위 (산출물 형식)**
- 콘티 only? / 스크립트만? / 실제 생성까지?
- 어떤 도구? (Kling / Seedance / fal.ai / Gemini)
- 몇 개 안 만들 거? (A/B 테스트용 변형 수)

---

### 💼 Strategy 모드

**1순위 (Stake & Reversibility)**
- 되돌릴 수 있는 결정? (Hard to reverse면 grill 강도↑)
- 시간 제약? 외부 일정 의존성?
- 의사결정자 본인 vs 위임?

**2순위 (Stakeholders)**
- 누구한테 영향? (직원 / 클라이언트 / 파트너)
- 외부 검토 필요? (회계·법무·컴플라이언스)

**3순위 (Trade-offs)**
- 단기 vs 장기?
- 비용 vs 속도 vs 품질?
- 명시적 옵션 ≥ 2개 비교

---

### 👤 Personal 모드 (건강/생활)

**1순위 (Context)**
- D-day 또는 마감?
- 본인/가족 가용성?
- 전문가 권고 있음?

**2순위 (Reversibility & Risk)**
- 되돌릴 수 있음? 안전·건강 영향?
- 전문가 상담 필요한 영역?

**3순위 (Logistics)**
- 예산?
- 공간/시간 제약?

---

## ⏱️ 체크인 프로토콜

매 10분 또는 8개 질문 경과 시 **자동 일시정지**:

```
[CHECK-IN]
지금까지 수집한 내용:
✅ 결정된 것: [...]
❓ 아직 미정: [...]
🚫 Don't List: [...]

선택해줘:
(a) 계속 grill (남은 질문 N개)
(b) 지금까지로 충분 → 정리하고 bob/실행 단계로
(c) 특정 분기만 더 파고 가기
```

---

## 📤 핸드오프 산출물

grill 종료 시 **자동 생성**:

### 파일 1: `grill-result.yaml` (bob/실행 단계가 읽음)
```yaml
mode: content
topic: "메라블 루비알엔 앰플클렌저 대만 인스타 릴스"
session_at: 2026-05-02T15:30:00+09:00
duration_min: 22

direction:
  brand: Merable
  product: "루비알엔 앰플클렌저"
  channel: "Instagram Reels"
  market: TW
  goal: "인지+전환"
  target: "20대 후반~30대 중반 여성, 클렌저 고관여층"
  tone: "전문가스러운데 친근"

dont_list:  # ⭐ 이게 핵심 산출물
  - id: D1
    rule: "의사/약사/약국 등장 금지"
    source: "대만 화장품 광고 규제"
    severity: critical
  - id: D2
    rule: "효능 단정형 카피 금지 (예: '여드름이 사라집니다')"
    source: "TFDA 가이드라인"
    severity: critical
  - id: D3
    rule: "Before/After 비교 컷 금지"
    source: "대만+한국 공통 화장품법"
    severity: high
  - id: D4
    rule: "한자 간체 사용 금지 (반드시 번체)"
    source: "대만 시장"
    severity: critical

implementation:
  duration_sec: 30
  cut_rhythm: "1초 컷"
  subtitle_style: "상단고정 + 음성싱크 하단"
  safe_zone: "900x1120 (대만 인스타)"
  tools:
    image_gen: "Gemini"
    video_gen: "Kling 3.0"
    edit: "FFmpeg"
    tts: "ElevenLabs (대만식 만다린)"

deliverables:
  - "콘티 1안 (텍스트)"
  - "실제 영상 3변형 (A/B/C)"

context_hints:
  - "컴플라이언스 사전 검수 필수"
  - "외부 일정 (예: 송출 마감) 전 완료 필요"

ambiguity_remaining: []  # 비어있어야 다음 단계 진입 OK
next_step: "bob"  # 또는 "direct_execution"
```

### 파일 2: `decisions/{date}-{topic}.md` (ccfm-wiki/14-decisions/)
ADR 스타일 기록. 같은 결정 두 번 grill 안 하도록.

```markdown
# 2026-05-02 메라블 대만 인스타 릴스 방향성

## Status
Decided

## Context
[grill 세션 요약]

## Decision
[채택된 방향]

## Don't List
[D1~D4]

## Consequences
[영향]

## Related
- 관련 ADR / 도메인 페이지
- 컴플라이언스 검수 담당
```

---

## 🚪 종료 신호 (즉시 grill 중단)

사용자가 다음 중 하나 말하면 **현재 분기 마무리 후 즉시 종료**:
- "ok 충분해" / "됐어 만들자" / "그만"
- "이제 bob 가자" / "코드 짜줘" / "영상 만들어줘"
- "컨텍스트 충분" / "더 물을 거 없으면 정리해줘"

---

## ⚠️ 안티 패턴 (하면 안 되는 것)

1. ❌ 묶음 질문 ("어느 브랜드고 어느 채널이고 어느 시장이야?")
2. ❌ 추천 답변 없이 질문 ("어떻게 할래?")
3. ❌ 사용자 입력 없이 임의로 결정 트리 채우기
4. ❌ Don't List를 Direction에 섞어 쓰기 (반드시 분리)
5. ❌ 종료 신호 무시하고 추가 질문 강행
6. ❌ 영문/존댓말로 답하기 (CCFM 톤 아님)

---

## 🔗 다른 스킬과의 관계

```
[유저 입력]
   ↓
[ambiguity_scorer.py] ── 점수 ≥ 5 ──→ [grill-me-ccfm]
   ↓ 점수 < 5                              ↓
   ↓                                  grill-result.yaml 생성
   ↓                                       ↓
   └────────── 합류 ─────────────────────┘
   ↓
[bob] ← grill-result.yaml 자동 로드
   ↓
[dd] → [harness] → [eval] → [learnings]
```

---

## 🤝 멀티 LLM 모드 (Claude + GPT-5.5 / Gemini)

이 스킬은 **CLI-중립**이다. SKILL.md를 따르는 모든 에이전트가 동일하게 작동:
- **Claude Code / Desktop**: `~/.claude/skills/grill-me-ccfm/` 자동 로드
- **Codex CLI (GPT-5.4 / GPT-5.5)**: `~/.codex/AGENTS.md` 카탈로그 → SKILL.md 읽어 동일 절차 수행
- **Gemini CLI**: `~/.gemini/GEMINI.md` 동기화 (3-CLI 컨텍스트 브릿지)

### 단일 모델 grill

| 명령 | 사용 모델 | 비고 |
|------|---------|------|
| Claude Code 안에서 "grill해줘 — <topic>" | Claude Opus/Sonnet | 기본. 한국어 톤 가장 자연스러움 |
| `codex --profile frontier "grill해줘 — <topic>"` | GPT-5.5 (frontier 프로필) | 영문 reasoning 강함, 결정 트리 깊이 우수 |
| `codex --profile codex "grill해줘 — <topic>"` | GPT-5.4 | 기본 OAuth 안정성 우선 |
| `gemini "grill해줘 — <topic>"` | gemini-2.5-flash | 빠른 1차 진단용 |

세 CLI 모두 **동일한 grill-result.yaml 스키마**로 산출물 통일됨. 어느 모델로 시작해도 다음 단계(bob/dd/직접실행)는 변경 없음.

### 병렬 grill (Claude + GPT-5.5 동시)

같은 주제를 두 모델이 따로 grill 후 **차이점만 사용자에게 제시** → 사용자가 선택. 큰 결정(신제품·해외 진출·콘텐츠 규제 등)에 권장.

```bash
# multi-llm-orchestrator 의 debate 모드 활용
claude "/mllm-debate grill: <topic> — Claude 와 Codex(GPT-5.5) 가 각자 14개 질문 만들고 차이점 비교"

# 또는 직접 두 CLI 병렬 호출 (PowerShell)
$topic = "메라블 루비알엔 앰플클렌저 대만 인스타 릴스"
Start-Job { codex --profile frontier "grill-me-ccfm: $using:topic" } | Out-Null
claude "grill-me-ccfm: $topic"
# 두 결과 grill-result.yaml 을 사용자가 비교 후 머지
```

**사용 기준**:
- 일상 작업·단순 모호함 → Claude 단일 (빠르고 토큰 비용 낮음)
- 콘텐츠 규제·시장 진출·대형 결정 → 병렬 (Don't List 누락 방지)
- 법/회계/계약 검토 → Claude + GPT-5.5 + Gemini 3중 (`/mllm-consensus`)

### 멀티 LLM 모드의 핵심 안티패턴

1. ❌ 두 모델 답변 단순 평균/합치기 — 차이점이 정보의 핵심. 차이는 사용자에게 노출하고 본인이 선택.
2. ❌ 모델별 톤 강제 통일 — Claude 의 부드러운 한국어 톤과 GPT-5.5 의 직설적 영문→한국어 톤은 보존. 톤 차이 자체가 신호.
3. ❌ 모든 grill 을 멀티 LLM 으로 — 토큰 낭비. 점수 ≥ 8 또는 강제 발동 케이스에만.

---

## 📝 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-05-02 | 초기 버전 (Matt 원본 + CCFM 4원칙 + Content 모드) |
| v1.1 | 2026-05-02 | Windows cp949 인코딩 버그 수정(UTF-8 출력 강제), 글로벌 동기화 (`ccfm-wiki/skills/`), Codex/GPT-5.5 멀티 LLM 모드 추가 |
