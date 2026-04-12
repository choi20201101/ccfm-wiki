---
type: source
domain: ai-automation
confidence: high
created: 2026-04-12
updated: 2026-04-12
sources: [raw/reports/gemini-logo-remover-v3.md]
---

# src-gemini-logo-remover

## 요약
Gemini 생성 이미지의 ✦ 워터마크를 자동 제거하는 Python 스크립트.
OpenCV TELEA+NS 인페인팅 블렌딩 방식. 현재 최선 기술 (60~70점).
LaMa 대비 우위 확인됨. 마스크 정밀도 개선 시 90점 가능.

## 기술 스펙
- 방식: 고정 위치 마스킹 (하단 좌/우 코너 타원형) + 인페인팅
- 알고리즘: TELEA 50% + NS 50% 블렌딩
- 속도: ~0.5초/장
- 지원: PNG/JPG/JPEG/WEBP, RGBA 알파채널 보존, 모든 비율

## 사용법
```bash
pip install opencv-python numpy Pillow
python remove_logo.py image.png                        # 단일
python remove_logo.py ./input/ ./output/               # 배치
```

## 한계 및 개선 포인트
- 마스크가 실제 로고보다 2배 큼 → CORNER_W_RATIO 0.09→0.04 시도 가능
- 복잡 배경에서 티 남
- 코너에 피사체 있는 이미지 주의

## 다음 비교 예정
- [ ] iopaint (진짜 LaMa 모델)
- [ ] 동적 마스크 감지 버전 (색상 기반)

## 관련 페이지
- [[ai-automation]]
- [[da-creative]]
