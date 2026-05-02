# bob 스킬 진입부 Patch 가이드

> grill-me-ccfm과 연동하기 위한 bob 스킬 수정 사항.
> bob/SKILL.md 의 도입부 섹션에 아래 블록을 추가/교체.

---

## 📍 적용 위치

bob/SKILL.md 파일에서 **"## 진입 절차"** 또는 그에 준하는 첫 동작 섹션 시작부.

---

## 🔧 추가할 블록

```markdown
## 🚪 진입 절차 (v2.1 — grill-me-ccfm 연동)

### Step 0: grill-result.yaml 우선 확인 (NEW)

bob 진입 시 **첫 동작**으로 다음을 체크한다:

1. 현재 작업 디렉토리에 `grill-result.yaml` 존재? → **있으면 무조건 먼저 로드**
2. ccfm-wiki/14-decisions/ 에 같은 topic 의 ADR 존재? → 참조용으로 함께 로드
3. grill-result.yaml의 `next_step` 필드가 `bob` 인지 확인

```python
# 의사코드
if exists("./grill-result.yaml"):
    grill = load_yaml("./grill-result.yaml")
    if grill["ambiguity_remaining"]:
        return "❌ ambiguity_remaining 비어있지 않음. grill-me-ccfm 다시 실행 필요"
    if grill["next_step"] != "bob":
        return f"❌ next_step={grill['next_step']}, bob 아님"
    
    # 정상: bob의 SDD/DDD 산출물 생성 시 grill 결과를 1차 입력으로 사용
    spec_inputs = grill_to_spec_inputs(grill)
else:
    # 기존 bob 동작
    spec_inputs = collect_from_user()
```

### Step 0.5: Ambiguity 자체 측정 (NEW)

`grill-result.yaml` 이 없을 때만 실행:

1. `ambiguity_scorer.py` 호출 (또는 동일 로직 인라인)
2. 점수 ≥ 5: 사용자에게 "grill-me-ccfm 먼저 돌리는 게 좋을 것 같은데, 진행할까?" 제안
3. 점수 < 5: 기존 bob 진입 그대로
4. 사용자가 "그냥 가자" 명시하면 점수 무시 (사용자 우선)

### Step 1 이후: 기존 bob 절차 유지

(기존 SDD → DDD → Context Engineering 산출물 생성 그대로)

단, **grill 결과가 있으면 다음 매핑을 자동 적용**:

| grill-result.yaml 필드 | bob Spec 매핑 |
|------------------------|--------------|
| `direction.brand/product/market` | Spec.Context.도메인 |
| `direction.goal/target` | Spec.Goal |
| `dont_list[]` | Spec.Constraints (강제 제약) |
| `implementation.*` | Spec.Implementation Notes |
| `context_hints[]` | Spec.External Dependencies |
| `deliverables[]` | Spec.Deliverables |

### Step N: 종료 시 grill 세션 보존

bob 작업 완료 후:
1. 사용된 `grill-result.yaml` 을 `ccfm-wiki/14-decisions/` 로 이동
2. 파일명: `{YYYY-MM-DD}-{topic-slug}.md` (ADR 형식 자동 변환)
3. 같은 주제 재발생 시 검색 가능하도록
```

---

## 🚫 변경하지 말 것

- bob의 SDD/DDD/Context Engineering 핵심 로직은 그대로
- grill 없이 단독 실행도 계속 가능해야 함 (하위 호환)
- 사용자가 "grill 건너뛰고 그냥 bob" 명시 시 무조건 따름

---

## ✅ 검증 방법

### 테스트 1: grill 결과 있는 경우
```powershell
cd C:\temp\test-bob
echo "mode: coding`ntopic: 'test'`nambiguity_remaining: []`nnext_step: bob" > grill-result.yaml
# bob 실행 → grill-result.yaml 읽고 Spec 자동 채우는지 확인
```

### 테스트 2: grill 결과 없고 모호한 입력
```
입력: "자동화 만들어줘"
기대: ambiguity_scorer 점수 ≥ 5 → grill 제안
```

### 테스트 3: grill 결과 없고 명확한 입력
```
입력: "ccfm-wiki 레포 README.md 에 '2026-05 업데이트' 섹션 추가, gguy 계정 PowerShell"
기대: 점수 < 5 → 기존 bob 진입
```

---

## 📝 변경 이력

| bob 버전 | grill 연동 | 비고 |
|---------|-----------|------|
| v2.0 (기존) | ❌ | 단독 동작 |
| v2.1 (이 patch 적용 후) | ✅ | grill-result.yaml 자동 인식 |
