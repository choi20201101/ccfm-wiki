---
type: tacit
category: lesson
confidence: medium
first_observed: 2026-04-12
last_confirmed: 2026-04-13
contradiction: none
---

# 실패 교훈 (Lessons Learned)

## [2026-04-12] LaMa가 항상 OpenCV보다 좋은 건 아니다

**상황:** Gemini 생성 이미지 로고 제거 기술 비교 테스트
**결과:** simple-lama-inpainting < OpenCV TELEA+NS 블렌딩

**이유:**
- LaMa는 넓고 복잡한 텍스처 복원에 최적화 (벽돌, 풀밭 등)
- 극소 마스크(25×31px) + 단순 배경에서는 오버스펙 → 번짐 발생
- pip 패키지(simple-lama-inpainting)는 원본 LaMa의 70~80% 성능

**적용 원칙:**
> 마스크 영역이 이미지 대비 5% 이하 + 주변 배경 단순 → OpenCV 먼저 시도
> LaMa는 복잡 배경 or 넓은 영역(10%+) 제거 시 사용

**관련 소스:** [[src-gemini-logo-remover]]
