---
aliases: ["Step 02 — Kling 4개 영상 생성"]
---

# Step 02 — Kling 4개 영상 생성

## 목적
이미지 → 영상 변환(Kling image2video v1-6)으로 다음 4개 원본 클립을 얻는다.

| key     | 소스 이미지 | 길이 | 의도                                    |
|---------|-------------|------|-----------------------------------------|
| A3_fat  | before.png  | 10s  | 영상1 좌반 — 1-2-3 손가락 카운트         |
| A3_thin | after.png   | 10s  | 영상1 우반 — 동일 시퀀스 (sync)         |
| B4_fat  | before.png  |  5s  | 영상2·3 전반 — 리듬 타기(팔 다운)        |
| B4_thin | after.png   |  5s  | 영상2·3 후반 — 신나는 K-pop 축하 춤      |

## 실행
```bash
python scripts/kling_client.py --config config/<project>.json
```

## 호출 규약
- 인증: HS256 JWT, payload `{iss: ACCESS_KEY, exp: +1800s, nbf: -5s}`, Secret Key 서명
- Endpoint: `https://api-singapore.klingai.com/v1/videos/image2video` (실패 시 `api.klingai.com` 폴백)
- Body:
  ```json
  {
    "model_name": "kling-v1-6",
    "mode": "std",
    "aspect_ratio": "9:16",
    "duration": "10" | "5",
    "cfg_scale": 0.5,
    "image": "<base64>",
    "prompt": "<prompts/XX.txt>"
  }
  ```
- 폴링: `GET /v1/videos/image2video/{task_id}`, 15초 간격, 최대 25분
- 저장: `output/raw/<key>.mp4`

## 상태 파일 — `output/tasks.json`
```json
{ "A3_fat": { "task_id": "...", "image": "...", "video_url": "..." }, ... }
```
멱등 규칙: 이 파일에 `task_id`가 있고 `raw/<key>.mp4` 가 100KB 이상이면 제출·다운로드 스킵.

## 프롬프트 파일
- [`prompts/v1_before_count.txt`](../prompts/v1_before_count.txt) (A3_fat)
- [`prompts/v1_after_count.txt`](../prompts/v1_after_count.txt)  (A3_thin)
- [`prompts/v23_before_rhythm.txt`](../prompts/v23_before_rhythm.txt) (B4_fat)
- [`prompts/v23_after_dance.txt`](../prompts/v23_after_dance.txt)  (B4_thin)

## 출력
- `output/raw/{A3_fat,A3_thin,B4_fat,B4_thin}.mp4` — 각각 720×1280, 30fps
- `output/tasks.json` 갱신

## 다음 단계
→ [03-overlay-compose](./03-overlay-compose.md)
