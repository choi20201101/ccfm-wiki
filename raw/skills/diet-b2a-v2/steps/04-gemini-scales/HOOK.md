# step-04 HOOK — 체중계 숫자를 "진짜"처럼 바꾸는 법

## 왜 숫자 변주가 중요한가
- 여러 영상에 같은 88.0→44.0 이 반복되면 알고리즘이 "동일 템플릿"으로 분류해 확산 억제
- 체중 숫자는 세트마다 달라야 **10명의 다른 변신기** 로 보임

## 프롬프트 원칙
- "외관·브랜드·화면·테두리 동일, 숫자만" 강제 (Gemini가 전체를 다시 그리려는 경향 제어)
- 7-segment LCD 폰트 질감을 "same 7-segment digital font" 로 명시

## 소프트 폴백
- Gemini가 체중계를 "그냥 체중계 재생성"으로 해석해 숫자 위치/폰트가 흐트러질 때:
  - 1차: 원본 + "change ONLY the digits"
  - 2차: 원본 없이 "Create a CAS digital scale photo showing {kg} kg on the screen"
  - 3차: 사람 손으로 숫자 치환 (OpenCV 7-seg 오버레이) — 이 스킬에서는 구현 X, Kling 합성 전 수동 검사 권장
