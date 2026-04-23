---
aliases: ["PLAN — 다이어트 Before/After 릴스 3종 자동 생성"]
---

# PLAN — 다이어트 Before/After 릴스 3종 자동 생성

> bob 스펙 · SDD(Spec-Driven Development) 기반. 이 문서는 스킬이 무엇을 만들어야 하는지의 **단일 진실(single source of truth)** 이다.

---

## 1. 목적 (Why)
- 릴스/쇼츠 플랫폼에서 **다이어트 변신 전후** 를 가장 자극적으로 보여주는 3종 포맷을 한 번에 뽑는다.
- 인물과 체중계 이미지만 교체하면 누구의 사례로도 **동일 품질**로 재생산 가능해야 한다.
- 사용자는 Kling API 계정과 4장의 PNG만 준비하면 된다.

## 2. 산출물 (What)
### 2.1 3종 최종 영상
| ID | 해상도 | 길이 | 레이아웃 | 전환 | 자막 |
|---|---|---|---|---|---|
| 영상1 | 1080×1920 | 9.4s | 좌우 분할 (Before/After 동시) | 없음 | 하단: `{키} / {체형}` + 각 측 상단 `Before`/`After` |
| 영상2 | 1080×1920 | 10.0s | 인물 중앙 + 우상단 체중계 박스 | 4.0s 지점 하드컷 | 체중계 박스 위: `{이전월}` → `{이후월}` |
| 영상3 | 1080×1920 | 9.8s | 인물 중앙 + 좌상단 체중계 박스(영상2 거울) | 4.0s 지점 하드컷 | 동일 |

### 2.2 산출 플로우
```
input/
  ├─ before.png          (인물 전, 뚱뚱)
  ├─ after.png           (인물 후, 마름)
  ├─ scale_before.png    (체중계 전)
  └─ scale_after.png     (체중계 후)
  + config.json           (날짜/키/체형/얼굴박스)
        │
        ▼
[00] 입력 검증 → [01] 오버레이(PNG) 생성
        │
        ▼
[02] Kling 4개 영상 생성 (A3_fat, A3_thin, B4_fat, B4_thin)
        │
        ▼
[03] 얼굴 모자이크 + 체중계 오버레이 + 날짜 자막 합성
        │
        ▼
[04] 배경음 믹스 → output/영상{1,2,3}.mp4
```

## 3. 입력 규약 (Interface)
### 3.1 `config.json` 스키마 (요약, 정식은 `config/schema.json`)
```json
{
  "project_name": "gguy_sample",
  "input": {
    "before_image": "examples/gguy_sample/before.png",
    "after_image":  "examples/gguy_sample/after.png",
    "scale_before_image": "examples/gguy_sample/scale_before.png",
    "scale_after_image":  "examples/gguy_sample/scale_after.png"
  },
  "copy": {
    "title":  "160cm / 골격 스트레이트",
    "label_before": "Before",
    "label_after":  "After",
    "date_before":  "2025년 12월",
    "date_after":   "2026년 3월"
  },
  "face_box": { "x": 325, "y": 405, "w": 112, "h": 125, "auto": true },
  "audio": {
    "v1": "audio/track1.mp3",
    "v2": "audio/track2.mp3",
    "v3": "audio/track3.mp3"
  },
  "kling": {
    "model": "kling-v1-6",
    "mode":  "std",
    "aspect_ratio": "9:16",
    "duration_v1": "10",
    "duration_v23": "5"
  }
}
```

### 3.2 이미지 요구사항
- 인물: 전신, 세로 9:16 선호, 얼굴 잘리지 않음
- 체중계: 정면, 숫자가 선명한 정사각형 ≈ 2000×2000
- 해상도 부족 시 자동 업스케일/크롭 (scripts/compose.py 내부)

## 4. 고정 좌표 스펙 (1080×1920 캔버스)
### 영상1 (좌우분할, 각 540×1920)
| 요소 | 위치 | 크기 |
|---|---|---|
| Before 체중계 | 중심 (270, 370) | 310×계산 |
| After 체중계  | 중심 (810, 370) | 310×계산 |
| Before 라벨   | 좌반 상단 y=165 | — |
| After 라벨    | 우반 상단 y=165 | — |
| 하단 타이틀   | 가로 중앙, y=H-높이-80 | — |
| 모자이크 박스 (각 원본 720×1280 기준) | (325,405) | 112×125 |

### 영상2 (우측 체중계)
- 체중계 박스 중심 (780, 430), 폭 400
- 날짜 자막 (625, 125), 48pt, 박스 상단 위쪽 여백
- 하드컷 지점: **4.0s** (전반 리듬 → 후반 1.2× 춤 loop 6s = 총 10s)

### 영상3 (좌측 체중계, 영상2 거울)
- 체중계 박스 중심 (260, 430), 폭 380
- 날짜 자막 (105, 130), 48pt
- 나머지는 영상2와 동일 로직

## 5. 춤 의도 스펙 (핵심 창작 규칙)
| 구간 | 동작 | 이유 |
|---|---|---|
| 영상1 좌반(Before) | 가벼운 검지 포인팅 → 2손가락 → 3손가락 (10초) | 음악 1-2-3 카운트 인트로와 동기화 |
| 영상1 우반(After)  | 좌반과 동일 시퀀스 (mirrored sync) | Before/After 대비를 몸매만으로 강조 |
| 영상2·3 전반 0-4s  | **팔 내린 채 미세 리듬 타기만** (춤 금지) | 인트로 구간 — 신나는 훅 전 긴장감 |
| 영상2·3 후반 4-10s | **양팔 들고 신나는 K-pop 축하 춤**, 1.2× 빠르게 + 루프 | 드롭 구간 — 다이어트 성공의 "해방감" |

## 6. 성공 기준 (Definition of Done)
- [ ] 3개 mp4가 `output/` 에 생성된다
- [ ] 각 영상에서 얼굴이 모자이크로 가려진다
- [ ] 영상2/3의 4초 컷 지점에서 양팔 아래 포즈가 매칭된다
- [ ] 자막이 체중계 박스 위 여백에 겹치지 않는다
- [ ] 해상도 1080×1920, fps ≥ 30, 오디오 aac, 각 영상 길이 9~10초 범위
- [ ] `scripts/run_all.py --config <new_project.json>` 만으로 다른 인물로 재생성 가능

## 7. 비범위 (Out of scope)
- 인물 얼굴 교체/디에이징
- 체중계 숫자 자동 편집 (이미지로 받음)
- 사운드 편집(BPM 보정, 이퀄라이징)
- 인스타 업로드 자동화

## 8. 기술 스택 요약
- **Kling AI v1-6 std**: image2video, 9:16, 5s/10s
- **ffmpeg**: hstack, concat, trim, setpts, split+loop, overlay, crop pixelate
- **Pillow**: 스트로크 자막 PNG 생성
- **(선택)** OpenCV haarcascade: 얼굴 박스 자동 검출
