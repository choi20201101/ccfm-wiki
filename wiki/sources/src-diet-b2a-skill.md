---
aliases: ["다이어트 B/A 스킬 v1"]
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [raw/skills/diet-b2a/, raw/skills/diet-b2a/diet-b2a-skill.zip]
---

# src-diet-b2a-skill

## 요약
다이어트 Before/After 자극 릴스 **3종 자동 생성 스킬**.
Kling AI(image2video v1-6 std) + ffmpeg filter_complex + Pillow 기반.
4장 이미지(인물 전/후 + 체중계 전/후) + 5줄 카피만 주면 10초 릴스 3개 산출.
bdh 파이프라인(bob → dd → harness)으로 구조화되어 다른 인물/컨셉으로 config만 바꿔 재사용.

## 산출물 3종
| 영상 | 레이아웃 | 길이 | 핵심 |
|---|---|---|---|
| 영상1 | 좌우 분할 Before/After 동시 | ~9.4s | 둘 다 **1-2-3 손가락 카운트** 싱크, 하단 타이틀 |
| 영상2 | 우상단 체중계 + 시간축 하드컷 | ~10s | 전반 4s 리듬 → 후반 6s **1.2× 신나는 춤 + 루프** |
| 영상3 | 좌상단 체중계 (영상2 거울) | ~10s | 동일 구조 |

## 기술 스펙
- **Kling API** v1-6, std, 9:16, HS256 JWT 인증
- **ffmpeg filter_complex**:
  - 얼굴 모자이크: `crop→scale÷22 neighbor→scale back neighbor→overlay`
  - 영상1: `split→mosaic→scale=-2:1920,crop=540:1920→hstack`
  - 영상2·3: `trim=0:4 + setpts/1.2→split=2→concat→trim=0:6` (후반 1.2× 루프)
- **Pillow**: 맑은 고딕 Bold + stroke 6~4 자막 PNG
- **멱등**: `tasks.json` + 파일 존재 체크로 재실행 시 이어하기

## 파이프라인 (bdh)
```
bob    → PLAN.md          (스펙/좌표/의도 single source of truth)
dd     → steps/00~05/*.md  (validate → overlays → kling → compose → qa → export)
harness → RULES.md         (멱등/cp949금지/얼굴모자이크강제/좌표한계 10개 규칙)
```

## 실행
```bash
python scripts/run_all.py --config <project>/config.json
```
config 5줄만 수정하면 새 인물로 재생성. Kling 4 클립 평균 7~12분 대기.

## 핵심 발견 (프로젝트에서 얻은 암묵지, 상세는 tacit/ 참조)
- **전→후 "하드컷"은 동일 중립 포즈(양팔 다운)에서 자르면 끊김이 안 보인다**
- **전반부는 리듬만, 후반부는 신나는 춤** 구조가 "변신 해방감" 자극에 가장 강함
- **얼굴 모자이크 박스 = 전체 body의 ~10%**만 덮을 때 자연스러움. 넓히면 어깨/가슴까지 먹힘
- **Kling std 5s 대비 10s는 포즈 시퀀스 초 단위 지정이 더 잘 먹힘** ("0-2s 포즈A, 2-4s 포즈B ...")
- **자막 폰트는 체중계 박스와 Y픽셀 겹치면 안 됨** → 48pt + stroke 4로 박스 위 여백 65px 이상
- **em-dash(—) Windows cp949에서 크래시** → ASCII 콜론(:)으로 대체

## 프롬프트 4개 (prompts/)
- `v1_before_count.txt` / `v1_after_count.txt`: 1-2-3 카운트 싱크
- `v23_before_rhythm.txt` / `v23_after_dance.txt`: 리듬 → 축하 춤

## 재사용 벡터
- 남자/다른 연령 인물로 프롬프트 첫 문장만 교체
- 날짜 자막을 "D-0 / D+90", "시작 / 3개월 후" 등으로 교체 (`copy.date_*`)
- 훅 카피는 [[HOOK]]의 30선에서 선택

## 관련 페이지
- [[content-ai-automation]]
- [[da-creative]]
- [[ai-automation]]
- [[viral]]
- [[creative-patterns]] · [[coding-lessons]] · [[psychology-insights]]

## 원본 위치
- `raw/skills/diet-b2a/` (전체 트리)
- `raw/skills/diet-b2a/diet-b2a-skill.zip` (35KB 아카이브)
- 사용자 바탕화면: `C:\Users\gguy\Desktop\diet-b2a-skill.zip`
