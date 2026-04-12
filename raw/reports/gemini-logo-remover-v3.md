# [RAW] Gemini Logo Remover v3.0
> 수집일: 2026-04-12
> 출처: CEO 직접 개발 + 테스트 결과
> 상태: 불변 원본

## 코드 원본
- 파일: remove_logo.py (Python 3.8+)
- 의존성: opencv-python, numpy, Pillow

## 핵심 원리
하단 좌/우 코너 고정 마스킹 + OpenCV TELEA+NS 인페인팅 50:50 블렌딩 + 가우시안 경계 블렌딩

## 파라미터
- CORNER_W_RATIO = 0.09 (코너 가로 9%)
- CORNER_H_RATIO = 0.07 (코너 세로 7%)
- INPAINT_RADIUS = 15
- BLUR_KERNEL = 31

## 테스트 결과
- 대상: Gemini 생성 인물 이미지 (572×1024px)
- 실제 로고 크기: 25×31px (이미지 대비 4.4%×3.0%)
- 현재 마스크: 51×71px → 로고보다 2배 큼
- 품질 점수: 60~70점 (CEO 직접 평가)
- 처리 속도: ~0.5초/장

## LaMa 비교 테스트 결과
- simple-lama-inpainting pip 패키지 사용
- 결과: 현재 TELEA+NS 코드보다 낮은 품질
- 이유: 극소 영역(25×31px) + 단순 배경에서 LaMa 오버스펙
