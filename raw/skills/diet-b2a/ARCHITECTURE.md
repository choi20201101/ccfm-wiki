# ARCHITECTURE — 내부 기술·포맷

## 데이터 플로우
```
config.json ─┐
input/*.png ─┼─► [00 validate] ─► validation_ok.flag
             │
             ├─► [01 make_overlays]  ─► output/overlays/*.png (5장)
             └─► [01b detect_face]   ─► output/face_box.json

prompts/*.txt + api.txt ─► [02 kling_client]
                               │ JWT HS256
                               │ POST image2video → GET poll
                               ▼
                        output/raw/{A3_fat,A3_thin,B4_fat,B4_thin}.mp4
                               │
                        [03 compose] (ffmpeg filter_complex)
                               │ split → mosaic → scale/crop
                               │ hstack (v1)  or  concat(trim + setpts/1.2 + split×2) (v2·v3)
                               │ overlay(scale, labels, date, title)
                               ▼
                        output/영상{1,2,3}.mp4
                               │
                        [04 qa_check] ─► qa_report.{json,md}
                               │
                        [05 export] ─► thumbs/, captions/, release.zip
```

## 핵심 ffmpeg 필터

### 얼굴 모자이크 (모든 Kling 원본 공통, 720×1280 좌표계)
```
[in]split=2[a][b];
[a]crop=W:H:X:Y,scale=iw/22:ih/22:flags=neighbor,scale=W:H:flags=neighbor[m];
[b][m]overlay=x=X:y=Y[out]
```
- `scale down by 22` → `scale up neighbor` = 픽셀화
- X,Y,W,H 는 `face_box.json` 값

### 영상1 — 좌우 분할 (10s)
```
[0:v]mosaic→scale=-2:1920,crop=540:1920[lv]
[1:v]mosaic→scale=-2:1920,crop=540:1920[rv]
[lv][rv]hstack=2[base]
+ scale_before @ (270,370) + scale_after @ (810,370)
+ label_before @ y=165 + label_after @ y=165
+ title @ bottom center
```

### 영상2 / 영상3 — 하드컷 + 후반 1.2× 루프 (10s)
```
[0:v]mosaic→trim=0:4.0[v0]                         # 전반 리듬 4s
[1:v]mosaic→setpts=PTS/1.2→split=2
 → concat(n=2) → trim=0:6.0[v1]                   # 후반 1.2× × 루프 → 6s
[v0][v1]concat=2[base]                             # 총 10s
+ scale(전) enable='lt(t,4)'
+ scale(후) enable='gte(t,4)'
+ date(전) / date(후) 동일 스위치
```

## 좌표계 이중화
- **원본 Kling 좌표** (720×1280): 얼굴 모자이크, prompt 내부 포즈 해석
- **최종 캔버스** (1080×1920): 체중계 박스, 자막, 라벨 위치

`compose.py` 에서 모자이크는 scale 전에 적용 → 좌표 변환 불필요.

## 상태 관리 (멱등)
### `output/tasks.json`
```jsonc
{
  "A3_fat":  { "task_id": "872...", "image": "...", "video_url": "...", "duration": "10" },
  "A3_thin": { ... },
  "B4_fat":  { ... },
  "B4_thin": { ... }
}
```
- `task_id` 있으면 재제출 안 함
- `raw/<key>.mp4` 100KB+ 있으면 재다운로드 안 함
- `video_url` 은 약 1시간 TTL이라 만료 시 재폴링으로 새 URL 획득

### `output/face_box.json`
```jsonc
{"x": 325, "y": 405, "w": 112, "h": 125}
```

## 프롬프트 설계 규칙
1. **첫 문장**에 인물 묘사 (의상/체형/배경) 고정
2. **중간**에 동작 시퀀스를 초 단위로 명시 (`0-1s, 1-2s, ...`)
3. **마지막**에 카메라/프레이밍 고정어 (`full body front view, fixed camera, vertical 9:16`)
4. 금지어는 `NO dancing`, `NO bouncing` 식으로 대문자 강조
5. before/after 쌍은 "EXACT SAME motion synchronized" 문구로 일치성 강제

## Kling API 노트
- Endpoint 폴백 순서: `api-singapore` → `api.klingai.com` (글로벌)
- JWT 필수 필드: `iss`, `exp`, `nbf` / alg=HS256
- std 모드 5초: 평균 생성 2~3분 / 10초: 3~6분
- 응답 `data.task_status`: submitted → processing → succeed | failed
- 성공 시 `task_result.videos[0].url` 은 CDN 링크 (~1h TTL)

## 외부 의존
- Python 3.10+, `pyjwt`, `requests`, `pillow`, (선택) `opencv-python`
- `ffmpeg`, `ffprobe` (7.0+ 권장)
- 폰트: `C:/Windows/Fonts/malgunbd.ttf` (한글 볼드)
