---
name: diet-b2a
description: |
  다이어트 Before/After 자극 릴스 3종(좌우분할·우측체중계·좌측체중계)을 Kling AI로 자동 생성하는 스킬.
  인물 전·후 이미지 2장 + 체중계 전·후 이미지 2장만 있으면 범용적으로 10초 릴스 3개를 뽑는다.
  트리거: '다이어트 비포애프터', 'before after', '체중계 릴스', 'diet reels', 'b2a', 'Kling 비포애프터', 'diet transformation video'.
triggers:
  - 다이어트 비포애프터
  - 비포애프터 영상
  - b2a
  - before after reels
  - kling 다이어트
  - diet transformation
version: 1.0.0
author: dance/diet-b2a
engine: Kling API (image2video, v1-6, std) + ffmpeg + Pillow
pipeline: bdh (bob spec → dd step 분해 → harness 멱등 강제)
---

# diet-b2a: 다이어트 Before/After 릴스 자동 생성 스킬

## 언제 트리거하나
- 사용자가 "다이어트 전후 영상 만들어줘", "비포애프터 릴스", "체중계 영상 자동 생성" 등 다이어트 변신 콘텐츠를 요청할 때.
- 인풋 4장(전·후 인물 + 전·후 체중계)이 주어졌을 때.

## 스킬이 만드는 3종 최종물
| 출력 | 레이아웃 | 길이 | 특징 |
|---|---|---|---|
| `output/영상1.mp4` | 좌우 Before/After 동시 분할 + 하단 타이틀 | ~9.4s | 둘 다 1-2-3 손가락 카운트 (동기화) |
| `output/영상2.mp4` | 우측상단 체중계 박스 + 날짜 자막 + 하드컷 | ~10s | 전반 4s 리듬 → 후반 6s 1.2× 신나는 춤 |
| `output/영상3.mp4` | 좌측상단 체중계 박스 (영상2 거울) | ~10s | 동일 구조, 거울 레이아웃 |

## 3단 파이프라인 (bdh)
1. **bob** — `PLAN.md`에서 전체 사양/의도/카피/좌표 스펙 확정
2. **dd** — `steps/00~05/*.md`로 분해된 각 단계가 다음 단계의 입력을 결정적으로 만든다
3. **harness** — `harness/RULES.md`의 가드레일(얼굴 모자이크 강제, 해상도 1080×1920, 좌표 하드 범위 등)이 린터처럼 동작

## 진입 동작 (skill invoked)
`scripts/run_all.py --config config/default.json` 를 실행하기 전에:
1. `PLAN.md` 읽고 의도·카피·좌표 파악
2. `config/<project>.json` 로드 → 입력 4장 경로, 날짜 문자열, 키/체형 라벨, 얼굴 박스 확인
3. steps 0→5 순차 진행 (각 step 문서에 출력 아티팩트와 검증 체크)
4. 최종 `output/영상{1,2,3}.mp4` 생성

## 참조 문서
- [`PLAN.md`](./PLAN.md) — 전체 스펙
- [`HOOK.md`](./HOOK.md) — 훅 카피(자막/CTA) 템플릿
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — 내부 기술/포맷
- [`USAGE.md`](./USAGE.md) — 실행 방법 및 입력 규약
- [`steps/*.md`](./steps/) — dd 단계별 상세
- [`harness/RULES.md`](./harness/RULES.md) — 멱등성/품질 가드레일
