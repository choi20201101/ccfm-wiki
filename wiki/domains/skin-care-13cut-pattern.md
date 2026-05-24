---
aliases: ["스킨 변화 13컷", "skin transformation ad", "Day1-30 progression"]
type: domain
category: creative
confidence: high
first_observed: 2026-05-24
last_confirmed: 2026-05-24
contradiction: none
---

# 스킨 변화 13컷 광고 패턴 (Skin Transformation 13-cut)

> **검증 케이스**: TW 32편 + JP 35편 = 67편 양산 (2026-05-24)
> **연관**: [[gptim-ad-creative-batch]], [[da-creative]], [[creative-patterns]], [[japan-market]], [[taiwan-market]]

## 1. 한 줄 정의

ChatGPT/FAL gpt-image-2로 만든 인물 frame 18장 라이브러리에서 **13컷만 골라 25초 1인=1영상으로 양산**. Before-Authority-Receive-Apply-Day1-Apply-Day7-Apply-Day14-Day30-Split-CTA 흐름. JP/TW 2언어 동시.

## 2. 왜 만들었나

- 일반 18컷 순차 양산은 변화 모호 ("바르기 컷이 이미 좋은 피부로 나옴" 사용자 피드백)
- 인물별 1영상 (variant 4종 X) — 중복 인물 노출 줄임, 100명=100영상
- Day cut(피부 점진 변화) 사이에 **사용(apply) 컷을 끼워** "시간 경과 + 지속 사용" 시각화
- 잠금화면 plate를 시간대별 다른 캡쳐로 띄워 "사회증거 측정 시점" 객관화

## 3. 핵심 13컷 매핑 (총 25초)

| pos | scene | timing | 의도 | 색상 자막 |
|---|---|---|---|---|
| 0 | sc01_hook       | 0.0~2.0 (2.0s) | BEFORE 강조 (여드름 잔뜩) | LineRed |
| 1 | sc04_authority  | 2.0~3.5 (1.5s) | 약사/피부과 권위 | LineYellow |
| 2 | sc05_receive    | 3.5~5.5 (2.0s) | 제품 받기 + 호기심 훅 | LineYellow |
| 3 | sc07_dispense   | 5.5~7.0 (1.5s) | 제형 (한 방울) | LineBlue |
| 4 | sc08_rub        | 7.0~8.5 (1.5s) | 손바닥 비비기 | LineBlue |
| 5 | sc12_day01      | 8.5~10.5 (2.0s) | **Day1 + 잠금화면 3/1** | LineRed |
| 6 | sc10_apply_b    | 10.5~12.0 (1.5s) | 바르기 (Day 사이 끼움) | LineBlue |
| 7 | sc13_day07      | 12.0~14.0 (2.0s) | **Day7 + 잠금화면 3/8** | LineYellow |
| 8 | sc11_apply_c    | 14.0~15.5 (1.5s) | 바르기 | LineBlue |
| 9 | sc14_day14      | 15.5~17.5 (2.0s) | **Day14 + 잠금화면 3/15 (저녁)** | LinePink |
| 10 | sc15_day30      | 17.5~20.0 (2.5s) | **Day30 + 잠금화면 3/30 (밤)** | LinePink |
| 11 | sc17_split      | 20.0~22.5 (2.5s) | Before vs After | LineGreen |
| 12 | sc18_cta        | 22.5~25.0 (2.5s) | CTA (master_after.png 풀스크린) | CTABox |

## 4. 자막 룰

### 4-1. 톤 (Performance Ads, 한국 인사이트 → TW 중문/JP 일문 의역)

- **마음의 소리** 톤 ("아 또 뒤집어졌어" / "어? 좀 잔잔해졌네")
- **2단어 짧게**가 아니라 **한 호흡 4-8자 문장**
- 매 컷 한 줄, 짧게 치고 빠짐

### 4-2. 색상 5구간

| 구간 | 색 | 의도 | 컷 |
|---|---|---|---|
| Before | **빨강** (TopRed/LineRed) | 페인 강조 | sc01, sc12 (Day1) |
| 호기심 훅 | **노랑** (TopYellow/LineYellow) | 권위·신뢰 | sc04, sc05, sc13 (Day7) |
| 사용중 | **파랑** (LineBlue) | 수분감·약국 톤 | sc07, sc08, sc10, sc11 |
| After 결과 | **핑크** (TopPink/LinePink) | 성과 강조 | sc14, sc15 (Day30) |
| 사회증거 | **초록** (LineGreen) | 후기·자랑 | sc17 split, sc18 cta |

### 4-3. 일자 라벨 = 실제 날짜 통합

- Day labels 표기는 "Day N (M/D)" 통합 형식
  - TW: "1日 3/1", "7日 3/8", "14日 3/15", "30日 3/30"
  - JP: "1日目 3/1", "7日目 3/8", "14日 3/15", "30日 3/30"
- 잠금화면 plate가 같은 날짜로 떠서 reinforcement

### 4-4. 위치 (얼굴 안 가리도록)

- Top 헤드라인: `Alignment 2` (bottom center), `MarginV 200` (하단 200px 위) → 화면 약 1720 지점 = 옷/어깨 영역
- Line word pop: `Alignment 2`, `MarginV 380` → 화면 1540 지점
- Top과 Line 간격 180px → 동시 노출 시 안 겹침

## 5. 잠금화면 plate (시간 도장)

### 5-1. 디자인

- **가로 16:9** floating plate (1280x720 source → 600x340 overlay)
- 검은 배경 + Helvetica/Yu Gothic Thin 큰 시계 "09:42" + 그 아래 작은 날짜
- 우측 상단 배터리/시그널 아이콘 (사실감)
- iOS/Samsung 로고 절대 금지 (상표권)

### 5-2. 시리즈 5장 (시간 다양화 필수)

- 모두 9시대로만 만들면 부자연 → 다양한 시간대 분포:
  - 3/1 일요일 **09:42** (아침)
  - 3/8 일요일 **14:23** (한낮)
  - 3/15 일요일 **19:08** (저녁)
  - 3/22 일요일 **11:35** (오전)
  - 3/30 월요일 **22:47** (밤)
- 배터리 % 도 변주 (87, 62, 47, 89, 31)
- **연도 표기 필수**: "2026年3月1日 日曜日" / "2026年3月1日 週日" (월일만 X)

### 5-3. 영상 합성 위치

- 가로 중앙 (`overlay=(W-w)/2:80`), 상단 y=80
- 컷별 enable 시점:
  - sc12 (Day1): 8.5~10.5s → plate 3/1
  - sc13 (Day7): 12.0~14.0s → plate 3/8
  - sc14 (Day14): 15.5~17.5s → plate 3/15
  - sc15 (Day30): 17.5~20.0s → plate 3/30

## 6. 시간대 조명 (frame 자체에 반영)

### 6-1. 잠금화면 시간과 frame 조명 일치 필수

- sc12 (09:42 아침) → 자연 모닝 라이트
- sc13 (14:23 한낮) → 밝은 미드데이
- sc14 (19:08 저녁) → **블루아워 (해 진 후 어두운 푸른)** — golden hour 아님
- sc15 (22:47 밤) → **PITCH BLACK + 따뜻한 램프** 한쪽만 illuminate

### 6-2. relight 방식

- 기존 master_after 영향으로 만든 frame을 **본인 frame을 ref input**으로 다시 FAL gpt-image-2/edit 호출
- prompt 패턴: `"DRAMATIC LIGHTING CHANGE - keep person/face/outfit/pose same, ONLY change lighting to [time-of-day description with DARK/BRIGHT/etc strong modifier]"`
- prompt 약하면 ref 톤 따라가서 결과 약함 → **DRAMATIC·MUST·NOT 같은 강조어 필수**
- 출력 → `{scene}_v2.png`로 저장 (원본 보존)

### 6-3. 조건부 plate overlay

- `sc14_v2 + sc15_v2` 둘 다 있는 인물만 잠금화면 plate 4장 모두 overlay
- 없는 인물 → plate 생략, 자막의 날짜 라벨만 (정보는 유지)
- 이유: relight 안 된 인물에 plate를 띄우면 "한낮 컷에 저녁 시계" 부조화

## 7. frame 라이브러리 구조 (재사용 핵심)

```
frames_skin_v7/{slot}/                  (TW 인물)
  sc01_hook.png ~ sc18_cta.png          (18장 원본)
  sc12_day01_v2.png ~ sc15_day30_v2.png (relight된 시간대 조명본, 선택)
frames_skin_v7_jp/{slot}/               (JP 인물)
ads_skin_v7/{slot}_after.png            (TW master after — sc18 CTA용 + ref)
ads_skin_v7_jp/{slot}_after.png         (JP master)
output/lockscreen/                      (잠금화면 plate)
  lockscreen_tw_2026_03_NN.png          (TW 중국어 날짜)
  lockscreen_jp_2026_03_NN.png          (JP 일본어 날짜)
```

새 광고 만들 때 frame 라이브러리만 채우면 같은 13컷 패턴으로 양산 가능.

## 8. compose 스크립트 (핵심 결정 사항)

- **PowerShell + ffmpeg** 2단계: concat silent.mp4 → subtitles+overlay filter chain final.mp4
- **VARIANT_ORDER 1개**만 (`A_classic` sequential 0..12) — variant 4종 만들지 말기 (중복 인물 노출 불필요)
- **filter_complex 일관성**: lockscreen 있든 없든 `filter_complex` 패턴 사용 (`-vf` 혼용하면 인용·경로 오류)
- **work dir Force**: `New-Item -ItemType Directory -Path $workDir -Force -ErrorAction SilentlyContinue`

## 9. 안 되는 것 (피해야 할 함정)

- 18컷 순차 양산 → 변화 모호 (사용자 "갑자기 좋아짐" 피드백)
- 같은 인물 4 variant 양산 → 중복 인물 인지로 광고 효율 저하
- master_after를 sc01-11 ref로 쓰면 BEFORE도 깨끗한 피부로 나옴 → master_before/master_mid 별도 생성 권장 (TODO: 다음 검증)
- 자막 0.6~0.9초/cut → 너무 빨라 못 읽음 (1.5~2.0초/cut 권장)
- 잠금화면 시간이 모두 9시대 → 부자연 (4개 시간대 분포 필수)
- Top 자막 `Alignment 8 + MarginV 130` → 얼굴 가림 → `Alignment 2 + MarginV 200` 하단으로
- lockscreen plate 300x170 작게 → 안 보임 → 600x340 (2배) 가로 중앙
- ffmpeg overlay `W-320:30` 우측 상단 → 좁아서 안 보임 → `(W-w)/2:80` 가로 중앙
- 저녁/밤 relight prompt 약하면 한낮처럼 보임 → "DRAMATIC", "PITCH BLACK", "no daytime brightness" 강조 필수
- PowerShell `$CUTS` 주석에 `—` (em-dash) 같은 unicode 글자 → parser 에러 → ASCII만 사용

## 10. 실행 파이프라인 요약 (재현용)

1. 인물 reference 사진 100장 준비 → `face/` 또는 별도
2. 인물별 master_after.png 생성 (FAL gpt-image-2 t2i, MASTER_TEMPLATE prompt)
3. 인물별 sc01-18 18장 frame 생성 (master ref + SCENE_TEMPLATES, supervisor + 4 batch)
4. (선택) relight_day_cuts.py로 sc12-15 시간대 조명 _v2.png 생성
5. gen_subs_v3.py + _jp.py → ASS 자막 (13컷 timing + 5색 + 날짜 통합)
6. gen_lockscreen_fal.py → 잠금화면 plate 5장 × 2언어
7. compose_v4.ps1 + _jp.ps1 → 인물별 1영상 25초 mp4
8. final_skin_v4/ + _jp/ 에 최종 결과

## 변경 이력

- 2026-05-24: 초안 — TW 32 + JP 35 = 67 영상 양산 검증 완료
