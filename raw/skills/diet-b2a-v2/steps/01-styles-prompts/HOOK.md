# step-01 HOOK — 프롬프트가 춤을 만든다

## Kling에 "춤"을 제대로 시키는 법 (이 프로젝트에서 검증된 패턴)

### 1. 초 단위로 쪼개기
- ❌ "K-pop 춤 추고 있다"
- ✅ "0-2.5s H 포즈, 2.5-5s O 포즈, 5-7.5s T 포즈, 7.5-10s G 포즈"
- 이유: Kling 모션 매끄러움은 "대강" 보다 "분 단위 지시"가 훨씬 잘 먹힘

### 2. 유행 댄스 이름 박기
- "Apple dance", "Hot To Go challenge", "NewJeans style" 같은 고유명사를 프롬프트에 직접 포함
- Kling v1-6은 영어 고유 댄스명에 학습된 패턴이 어느 정도 있어 이름을 박으면 유사 동작 재현율 상승

### 3. 시작·끝 포즈 잠그기
- 하드컷 전환을 위해선 before 끝 포즈 = after 시작 포즈가 필수
- 예: "ends with arms at sides in neutral standing pose" + "starts with arms at sides in neutral then immediately..."

### 4. 억제어를 대문자로
- Kling은 소문자 금지어를 자주 무시. "NO dancing, NO arm raising" 식으로 대문자 강조

### 5. 의상·체형 선차별
- 첫 문장에 의상·체형 고정. 나중 문장에서 동작 → 동작이 의상을 "바꿔버리는" 것 방지

## 이 step에서 의도한 창의적 포인트
- **set 마다 댄스 장르 완전 분리** → 같은 "다이어트 B/A" 포맷이어도 피드에 떴을 때 서로 다른 릴스처럼 보이게
- **v1_motion 은 before/after 공통** → 몸매 차이만 보여지는 효과
- **v23_before 는 절제된 정적, v23_after 는 폭발** → 스킬의 핵심 감정 임팩트(억제→해방) 유지

## 금지
- 프롬프트에 em-dash(—), 스마트 따옴표, 이모지 포함 금지 (cp949 크래시)
- 동일 세트 안에서 v1_before/v1_after 동작 불일치 금지
