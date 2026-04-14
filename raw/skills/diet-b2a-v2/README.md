# diet-b2a-v2 — 다이어트 Before/After 대량 생산 스킬 (10세트 × 3포맷 = 30영상, 다국어)

> v1(diet-b2a) → v2 확장. **Gemini 시드 자동 생성 + 체중계 숫자 랜덤 치환 + 얼굴 자동 모자이크 + 한국어/대만어(번체) 자막 + 60영상 동시 배포**.

## 핵심 차이 (v1 → v2)
| 항목 | v1 | v2 |
|---|---|---|
| 세트 수 | 1 (사용자 이미지 준비 필요) | **10** (모델 5 × 배경 5) |
| 시드 이미지 | 사용자가 제공 | **Gemini Chrome 자동 생성** (before/after 10쌍) |
| 체중계 | 고정 이미지 2장 | **세트별 kg 랜덤** (Gemini 숫자 치환) |
| 로고 제거 | — | **OpenCV TELEA+NS 자동 적용** |
| 얼굴 모자이크 | 고정 박스 | **세트별 자동 검출 박스** (OpenCV Haar) |
| 춤 스타일 | 1종 | **10종** (TikTok/Insta 트렌드) |
| 자막 언어 | 한국어 | **한국어 + 대만어(번체)** = 60영상 |
| 오케스트레이터 | run_all.py | **스텝별 bdh 구조** (10단계) |

## 30초 실행
```bash
# 0. 로그인 (1회)
python C:/Users/gguy/Desktop/MD/gemini-imagegen/login_once.py

# 1. 세션 검증
python steps/02-gemini-session/check_session.py

# 2. 전체 실행 (약 3~4시간)
python steps/01-styles-prompts/build_prompts.py
python scripts/build_sets.py
python steps/03-gemini-seeds/gen_seeds.py        # Gemini 시드 20장
python steps/04-gemini-scales/gen_scales.py      # Gemini 체중계 20장
python scripts/detect_faces.py                    # 얼굴 박스 자동 검출
python steps/05-kling-20clips/gen_kling.py        # Kling 40 클립
python steps/06-compose-15/compose.py             # 한국어 30영상
python steps/06-compose-15/compose.py --lang tw   # 대만어 30영상
```

## 파이프라인 (bdh)
```
[00] BGM 분석 → BPM/드롭 시점
[01] 스타일·프롬프트 (10 × 4 = 40 prompt 파일)
[02] Gemini 세션 보장
[03] Gemini 시드 (20장, before/after × 10세트)
[04] Gemini 체중계 (20장, kg 랜덤)
[05] Kling 40 클립 (10s × 20 + 5s × 20)
[06] ffmpeg 합성 30영상 × 2언어 = 60
[07] eval + 조정
```

## 문서 지도
- `PLAN.md` — 사양/산출/성공기준
- `HOOK.md` — 훅 카피 라이브러리 (언어별)
- `harness/RULES.md` — 멱등·안전 규칙
- `steps/*/PLAN.md + HOOK.md + README.md` — 스텝별 문서
- `scripts/` — 공용 라이브러리
- `prompts/styles.json` — 10종 춤 정의 + 훅 카피 (ko/tw)

## 라이선스/윤리
- **AI 생성 인물만 사용**
- Kling/Gemini 사용약관 준수 (정책 위배 프롬프트 자동 소프트 폴백 내장)
- 실존 인물 사진 금지
