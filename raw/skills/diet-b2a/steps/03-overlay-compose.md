# Step 03 — 얼굴 모자이크 + 체중계 오버레이 + 자막 합성

## 목적
Kling 원본 4개와 자막 PNG 5개, 체중계 이미지 2개를 ffmpeg filter_complex 한 번에 합쳐서 3종 최종 mp4를 생성한다.

## 입력
- `output/raw/*.mp4` (Kling 4개)
- `output/overlays/*.png` (자막 5개)
- `input.scale_before_image`, `input.scale_after_image` (체중계 PNG 2개)
- `face_box.json`
- `audio.v{1,2,3}` (선택)

## 실행
```bash
python scripts/compose.py --config config/<project>.json
```

## 필터 파이프라인 요약
### 얼굴 모자이크 (모든 클립 공통, 720×1280 좌표계)
```
[in]split=2[a][b];
[a]crop=W:H:X:Y,scale=iw/22:ih/22:flags=neighbor,scale=W:H:flags=neighbor[m];
[b][m]overlay=x=X:y=Y[out]
```

### 영상1 — 좌우 분할
1. A3_fat / A3_thin 각각 모자이크
2. 각각 `scale=-2:1920,crop=540:1920` (중앙 크롭)
3. 하스택 2개 → 1080×1920
4. 좌측 체중계 @(270,370), 우측 체중계 @(810,370)
5. `Before` @(270,165), `After` @(810,165)
6. 하단 타이틀 @(가운데, H-h-80)
7. 오디오: config.audio.v1

### 영상2 / 영상3 — 시간축 하드컷 + 1.2× 루프
1. B4_fat 모자이크 → `trim=0:4` (전반 리듬)
2. B4_thin 모자이크 → `setpts=PTS/1.2`, split=2 후 concat 2번 → `trim=0:6` (후반 6초)
3. 두 세그먼트 concat → 10초
4. 체중계 박스 오버레이 (enable lt/gte `t<4`/`t>=4`)
5. 날짜 자막 (체중계 위쪽 여백)
6. 오디오: config.audio.v2 / v3, `-shortest`

### 좌표 테이블 (최종 1080×1920 캔버스)
| 요소 | 영상2 | 영상3 |
|---|---|---|
| 체중계 중심 (x,y) | (780, 430) | (260, 430) |
| 체중계 폭        | 400         | 380          |
| 날짜 자막 (x,y)  | (625, 125)  | (105, 130)  |

## 출력
- `output/영상1.mp4` (~9.4s)
- `output/영상2.mp4` (~10s)
- `output/영상3.mp4` (~9.8s)

## 다음 단계
→ [04-qa.md](./04-qa.md)
