# Higgsfield Soul Character API — 실증 호출 레퍼런스

**확인일**: 2026-04-21
**프로젝트 컨텍스트**: `C:\Users\gguy\Desktop\by\` (볼륨필인 앰플 "나됐어요!" 반전 테스티모니얼 파이프라인)
**관련 문서**: `src-volumefill-video-pipeline-2026-04-21.md`

## 요약

Higgsfield의 공식 Python SDK(`higgsfield-client`)와 docs에서 명시한 `/v1/text2image/soul` 엔드포인트는 **일반 고객 API 키로는 "Unavailable model"(400) 반환**. 실제 동작하는 Soul 이미지 생성 엔드포인트는 **`/higgsfield-ai/soul/character`** (docs 하단에 별도 표기).

SDK readme의 예시 body 포맷(`{params: {prompt, width_and_height, quality, batch_size, style_id}}`) 역시 이 엔드포인트에서는 적용 안 됨 — **flat JSON** 사용.

## 엔드포인트 매트릭스

| 동작 | Method | Path |
|---|---|---|
| Soul Character 이미지 생성 | POST | `/higgsfield-ai/soul/character` |
| 요청 상태 조회 | GET  | `/requests/{request_id}/status` |
| 요청 취소 | POST | `/requests/{request_id}/cancel` |
| Soul 스타일 목록 (106개) | GET  | `/v1/text2image/soul-styles` |
| Soul ID(커스텀 캐릭터) 생성 | POST | `/v1/custom-references` |
| Soul ID 목록 | GET  | `/v1/custom-references/list` |
| Soul ID 상세 | GET  | `/v1/custom-references/{reference_id}` |
| Soul ID 삭제 | DELETE | `/v1/custom-references/{reference_id}` |

Base URL: `https://platform.higgsfield.ai`

## 인증

단일 헤더:
```
Authorization: Key <API_KEY_ID>:<API_KEY_SECRET>
Content-Type: application/json
```
- 리터럴 문자열 `Key ` 접두, 그 뒤에 `id:secret` 콜론 결합.
- Python SDK는 env `HF_KEY=id:secret` 또는 분리 env `HF_API_KEY` + `HF_API_SECRET` 읽음.
- 공식 SDK는 대안이지만 엔드포인트 경로는 수동 지정 필요 (SDK readme는 `bytedance/seedream/v4/text-to-image`만 예시로 다룸).

## 요청 본문 (Character)

**flat JSON** — `params: {...}` 래퍼 없음.

```json
{
  "prompt": "string (required)",
  "width_and_height": "1152x2048",
  "quality": "1080p",
  "batch_size": 1,
  "style_id": "<UUID>",
  "seed": 42
}
```

### 필드 상세
- `prompt` — 유일한 필수 필드. 없으면 `422 {"type":"missing","loc":["body","prompt"]}`.
- `width_and_height` — literal enum. 허용 값:
  - `1152x2048` (9:16) ← 세로 셀피/릴스 표준
  - `2048x1152` (16:9)
  - `2048x1536`, `1536x2048`, `1344x2016`, `2016x1344`
  - `960x1696`, `1696x960`, `1152x1536`, `1088x1632`, `1632x1088`
  - `1120x1680`, `1680x1120`
  - `1536x1536`, `1536x1152`, `2048x2048`
- `quality` — `"720p"` | `"1080p"` (기본 서버값, 미지정 허용).
- `batch_size` — 정수 `1` 또는 `4`.
- `style_id` — `/v1/text2image/soul-styles`에서 조회 가능한 UUID.
- `seed` — 정수, **`>= 1`** (−1 금지 — `greater_than_equal` 에러).

### 제한
- **동시 요청 ≤ 4건**. 초과 시: `400 {"detail":"Maximum number of concurrent requests (4) has been reached"}`
- 일반 생성 소요: 30~50초 (1080p, batch_size=1 기준).

## 응답

### 제출
```json
{
  "status": "queued",
  "request_id": "<uuid>",
  "status_url": "https://platform.higgsfield.ai/requests/<uuid>/status",
  "cancel_url": "https://platform.higgsfield.ai/requests/<uuid>/cancel"
}
```

### 상태 폴링
- 진행: `{"status": "queued" | "in_progress"}`
- 완료: 
  ```json
  {
    "status": "completed",
    "request_id": "...",
    "images": [{"url": "https://d3u0tzju9qaucj.cloudfront.net/<bucket>/<file>.png"}]
  }
  ```
- 실패 상태: `failed` | `nsfw` | `canceled` → 상세 필드는 케이스별 상이.

### 이미지 URL
CloudFront 프리사인드 URL. 수명 확인 안 됐으나 최소 수 시간은 유효 (관찰치). 즉시 `GET` + 로컬 저장 권장.

## 스타일 id 목록 (소개, 총 106개 중 셀카/릴스 테스티모니얼용 선별)

| Name | UUID | 용도 |
|---|---|---|
| **Realistic** | `1cb4b936-77bf-4f9a-9039-f3d349a4cdbe` | 필터 없이 피부 결·모공까지 살리는 초사실. **AI 질감 최소화 1순위**. |
| **DigitalCam** | `ca4e6ad3-3e93-4e03-81a0-d1722d2c128b` | 2007 하드 플래시 디카 룩. 바이럴 릴스 진짜감. |
| **Library** | `6fb3e1f5-d721-4523-ac38-9902f2b2b850` | 따뜻한 실내 자연광 — 집 셀피에 자연스러움. |
| **Spotlight** | `40ff999c-f576-443c-b5b3-c7d1391a666e` | 파파라치 플래시 고대비. |
| **Quiet luxury** | `ff1ad8a2-94e7-4e70-a12f-e992ca9a0d36` | 프리미엄 셀피. |
| Creatures | `b3c8075a-cb4c-42de-b8b3-7099dd2df672` | 스타일 기본값 — 이 프로젝트엔 부적합. |
| Medieval | `1fc861ed-5923-41a6-9963-b9f04681dddd` | 중세/캐주얼 코디 룩. |
| Giant People | `a5f63c3b-70eb-4979-af5e-98c7ee1e18e8` | — |
| Subway | `d2e8ba04-9935-4dee-8bc4-39ac789746fc` | 외부 로케 필요 시. |

전체 목록은 `GET /v1/text2image/soul-styles`로 실시간 조회. `description` 필드에 서브 스타일 가이드 포함 (예: Realistic = *"No filters, just flawless clarity. Light, pores, fabric—everything exactly as it is, but better"*).

## 실증 로그 (API 키 `0e76855e-…-41f1`)

| 경로 | 결과 |
|---|---|
| `POST /bytedance/seedream/v4/text-to-image` | 200 OK, request_id 발급 (참고 — 다른 모델) |
| `POST /v1/text2image/soul` (params wrapper, 모든 필드) | **400 "Unavailable model"** (키 tier 밖) |
| `POST /higgsfield-ai/soul/character` (flat body, prompt만) | **200 OK**, 48초 후 completed |
| `GET /v1/text2image/soul-styles` | 200 OK, 106개 style 객체 반환 |
| 5번째 동시 제출 | 400 "Maximum number of concurrent requests (4) has been reached" |

## Python 구현 패턴

```python
import httpx, time

BASE = "https://platform.higgsfield.ai"
H = {"Authorization": f"Key {api_id}:{api_secret}", "Content-Type": "application/json"}

def soul_character(prompt, style_id=None, size="1152x2048", quality="1080p"):
    body = {"prompt": prompt, "width_and_height": size, "quality": quality, "batch_size": 1}
    if style_id: body["style_id"] = style_id
    with httpx.Client(timeout=90) as c:
        r = c.post(f"{BASE}/higgsfield-ai/soul/character", headers=H, json=body)
        r.raise_for_status()
        rid = r.json()["request_id"]
        while True:
            s = c.get(f"{BASE}/requests/{rid}/status", headers=H).json()
            if s["status"] == "completed":
                return s["images"][0]["url"]
            if s["status"] in ("failed", "nsfw", "canceled"):
                raise RuntimeError(s)
            time.sleep(3)
```

## 실무 팁

- **AI 질감 최소화**: `Realistic` 스타일 + 프롬프트에 "iPhone front camera selfie, natural skin texture, visible pores, unretouched, slight JPEG compression, authentic tired look" 권장.
- **9:16 셀피**: `width_and_height="1152x2048"` 고정.
- **정체성 유지 필요 시**: 먼저 `POST /v1/custom-references`로 Soul ID 생성 → `reference_id`를 이후 생성에 적용 (현재 Character 엔드포인트에서 파라미터명은 미검증).
- **배치 처리 시 동시 4건 상한 주의**: Python `asyncio.Semaphore(4)` 또는 순차 4개 묶음 권장.
- **SDK vs raw httpx**: SDK readme가 엔드포인트를 혼동시키므로, 현 시점 raw `httpx` 호출이 더 투명하고 디버깅 쉬움.

## 관련 파일

- 구현: `C:\Users\gguy\Desktop\by\scripts\hfutil.py`
- 키 파일: `C:\Users\gguy\Desktop\by\api.txt` (`API Key ID=...`, `API Key Secret=...` 라벨 정규식 파싱)
- 핸드오프: `C:\Users\gguy\Desktop\by\HANDOFF.md`
- 프로젝트 메모리: `C:\Users\gguy\.claude\projects\C--Users-gguy-Desktop-by\memory\ref_higgsfield_soul_api.md`
