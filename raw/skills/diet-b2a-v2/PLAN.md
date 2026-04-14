# PLAN v2 — 15개 다이어트 B/A 릴스 대량 생성

## 목적
diet-b2a-skill의 bdh 파이프라인을 확장해 **5세트 × 3종 영상 = 15개 릴스**를 한 번의 오케스트레이션으로 뽑는다.
각 세트는 서로 다른 모델·배경·춤·체중계 숫자를 사용하여 "다양한 사례"로 보이게 한다.

## 파이프라인 개요
```
[00] BGM 분석   → bgm_report.json   (3곡 BPM/드롭/배정 결정)
[01] 스타일/프롬프트 → styles.json + prompts/set1..5   (5세트 × 4 prompt)
[02] Gemini 세션 → .session/ (로그인 상태 확인/로그인)
[03] Gemini 시드 → seeds/set1..5/{before,after}.png    (모델+배경 합성)
[04] Gemini 체중계 → scales/set1..5/{before,after}.png  (kg 랜덤 치환)
[05] Kling 20 클립 → raw/set1..5/{A_before,A_after,B_before,B_after}.mp4
[06] ffmpeg 합성 → output/set1..5/영상{1,2,3}.mp4
[07] eval/조정 → qa_report + 필요 시 해당 세트 특정 스텝 재실행
```

## 산출 규모
- 시드 이미지 10장, 체중계 이미지 10장 → Gemini
- Kling 클립 20개 (10s × 10개 + 5s × 10개)
- 최종 mp4 15개 (9.4s × 5 + 10s × 10)

## 춤 스타일 (5세트, TikTok/Insta 유행)
1. **set1** — NewJeans "Super Shy" (볼에 손, 수줍음)
2. **set2** — Apple Challenge (머리·가슴 팔 교차, Meduza)
3. **set3** — aespa Supernova Chacha (허리 차차+팔슬라이스)
4. **set4** — Hot To Go (Chappell Roan, 몸글자 H-O-T-G)
5. **set5** — Confident Flex (Bbl Drizzy, 어깨·부채 셋업)

## 배경음 배정 (BPM 분석 반영)
| 영상 | BGM | BPM | 컷 지점 |
|---|---|---|---|
| 영상1 (좌우분할) | DUX (9.4s) | 95 | N/A |
| 영상2 (우측체중계) | DW3 (10s) | **129** | 4.85s (드롭) |
| 영상3 (좌측체중계) | DWnms (9.8s) | 95 | 4.0s (드롭 2.5s는 너무 빨라 후반 길이 부족 → 타협) |

## 성공 기준
- [ ] 15개 mp4 모두 1080×1920 / aac / 9~10초
- [ ] 각 세트 before 체중계 kg > after (논리 검증)
- [ ] 세트별 before/after 시드의 방 상태가 극적으로 다름 (어지러움/밤 ↔ 정돈/낮)
- [ ] 모든 얼굴에 모자이크
- [ ] 영상2·3의 컷 지점이 BPM 드롭과 맞음 (±0.5s)

## 멱등
- 각 스텝은 `state.json`에 완료 플래그. 실패 시 해당 세트·스텝만 재실행.
- Gemini/Kling 둘 다 비용 발생 → 성공 결과 무조건 캐시.

## 디렉토리 지도
```
v2/
├── PLAN.md                     (이 문서)
├── HOOK.md                     (영상·카피 훅 라이브러리)
├── harness/RULES.md            (멱등/품질 가드레일)
├── scripts/                    (공유 라이브러리)
├── steps/
│   ├── 00-bgm-analyze/         PLAN·HOOK·README + 스크립트·리포트
│   ├── 01-styles-prompts/      PLAN·HOOK·README + styles.json + build_prompts.py
│   ├── 02-gemini-session/
│   ├── 03-gemini-seeds/
│   ├── 04-gemini-scales/
│   ├── 05-kling-20clips/
│   ├── 06-compose-15/
│   └── 07-eval-adjust/
├── sets/set1..5/               (각 세트 입력 config + 산출물)
├── seeds/                      (03 산출)
├── scales/                     (04 산출)
├── raw/                        (05 산출)
├── output/                     (06 산출)
└── state.json
```
