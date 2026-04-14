# step-06 · 30 영상 ffmpeg 합성

## 목적
세트별 raw mp4 4개 + 체중계 2장 + 자막 PNG 5장 + BGM 3곡 → **세트당 영상1/2/3 총 3개** = 전체 **30 영상**.

## 입력
- `raw/setN/{A_before,A_after,B_before,B_after}.mp4`
- `scales/setN/{before,after}.png`
- `steps/01-styles-prompts/prompts/setN/...` (참고만)
- `sets/setN/config.json` (레이아웃·BGM·컷지점)

## 출력
- `output/setN/영상1.mp4` (좌우분할)
- `output/setN/영상2.mp4` (우측체중계, DW3 배경음)
- `output/setN/영상3.mp4` (좌측체중계, DWnms 배경음)

## 실행
```bash
python compose.py
python compose.py --only set3
```

## 레이아웃 (diet-b2a-skill 검증 값 재사용)
- 영상1: A_before|A_after 좌우 hstack, 체중계 좌우, 라벨, 하단 타이틀
- 영상2: B_before(0-4.85s) → B_after(1.2× 루프) 하드컷, 우상단 체중계, 우상단 날짜
- 영상3: 영상2 거울 레이아웃, 좌상단 체중계, 좌상단 날짜
