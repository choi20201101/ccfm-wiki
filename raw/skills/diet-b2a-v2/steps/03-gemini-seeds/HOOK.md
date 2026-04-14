# step-03 HOOK — 시드가 영상 품질을 결정한다

## 왜 시드가 핵심인가
- Kling image2video는 **시드 이미지를 거의 그대로 유지**하고 움직임만 추가. 시드가 흐리거나 비현실적이면 영상도 망가짐
- 의상/배경/체형을 영상 생성 시점에 바꾸려 하지 말 것 — 시드에서 이미 확정되어야 함

## "자극적 변신" 훅 3요소
1. **같은 방, 다른 상태** — 공간 동일성 + 정돈 대비가 "시간 경과" 착시를 만듦
2. **같은 포즈, 다른 체형** — 카메라 앵글·구도 유지, 몸만 변해야 B/A의 임팩트
3. **밤 → 낮** — 조명 대비가 감정 "어둠→해방" 은유로 직결

## Gemini 시드 프롬프트 규칙 (전이 가능)
- Photo 1 = 모델, Photo 2 = 레퍼런스(배경 or before) — 역할 먼저 박기
- "Do NOT change the room architecture" 같은 **부정 제약**을 명시해야 방 구조 유지
- after는 "SAME pose in the SAME room as Photo 2" 로 before와 연동 → before 생성 후 after 입력에 before 이미지 추가
- 사이즈 지시 `vertical 9:16 portrait` 는 마지막에

## 실패 대응
- 체형이 충분히 마르지 않으면 → after 프롬프트에 "emphasize very visible waist definition, thigh gap" 추가
- 방이 안 바뀌면 → before/after 프롬프트를 분리 대화창에서 각각 생성
- 얼굴 왜곡 심하면 → 해당 세트만 재생성 (멱등 skip)
