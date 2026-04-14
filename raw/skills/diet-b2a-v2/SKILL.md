---
name: diet-b2a-v2
description: |
  다이어트 Before/After 릴스를 10세트 × 3포맷 × 2언어 = 60개 자동 생성하는 스킬.
  Gemini Chrome 자동화 + Kling image2video + ffmpeg 합성을 하나의 bdh 파이프라인으로 묶었다.
  트리거: 'B/A 릴스 대량', 'diet reels 10세트', 'kling+gemini 자동화', 'b2a tw', '다이어트 변신 자동', 'diet bulk'.
triggers:
  - 다이어트 대량 생성
  - b2a 10세트
  - 변신 릴스 대량
  - diet bulk
  - b/a 다국어
  - kling gemini pipeline
version: 2.0.0
author: dance/v2
pipeline: bdh (bob → dd 10 steps → harness)
depends_on:
  - diet-b2a (v1 core)
  - gemini-imagegen (MD/gemini-imagegen 의 .session 및 gemini_auto.py)
  - gemini-logo-remover (OpenCV TELEA+NS)
---

# diet-b2a-v2

자세한 사용법: [`README.md`](./README.md) · 사양: [`PLAN.md`](./PLAN.md) · 훅: [`HOOK.md`](./HOOK.md)

## 이 스킬은 언제 트리거하는가
- 사용자가 "다이어트 변신 영상 대량으로 만들어줘" 요청 시
- "다국어 릴스 배포"가 필요할 때 (한국/대만 시장 동시 공략)
- 10세트 이상의 서로 다른 모델·춤·체중 조합이 필요한 프로젝트

## 입력 최소 요건
- `model/1..N.png` — AI 생성 인물 이미지 (N ≥ 세트 수, 기본 5)
- `bg/*.{png,jpg,avif}` — 자취방 배경 이미지
- `cm/01.png`, `cm/02.png` — 체중계 템플릿 2장
- `api.txt` — Kling Access/Secret
- Gemini 로그인된 `.session` (C:/Users/gguy/Desktop/MD/gemini-imagegen/.session)

## 스킬 산출
- `output/setN/영상{1,2,3}.mp4` (한국어 30개)
- `output_tw/setN/영상{1,2,3}.mp4` (대만어 30개)
- 각 영상 1080×1920 / 9~10초 / aac
