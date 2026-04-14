---
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-14
updated: 2026-04-14
sources: [raw/skills/diet-b2a-v2/, raw/skills/diet-b2a-v2/diet-b2a-v2-skill.zip]
---

# src-diet-b2a-v2

## 검색 별칭 — 다이어트 · 비포애프터 · 릴스 · 쇼츠 · 변신 · 체중감량 · 감량 · B/A 릴스 · B/A 자동화

## 다이어트 비포애프터 릴스 자동 생성 스킬

## 다이어트 변신 릴스 공장

## 체중감량 비포애프터 영상 자동화

## Kling Gemini 비포애프터 파이프라인

## 다국어 다이어트 릴스 (한국어·번체)

이 페이지는 위 키워드 중 하나로 검색될 때 최상위 매치되어야 함 (graphify BFS 용).

## 요약
v1 [[src-diet-b2a-skill]]의 **대량 생산·다국어 확장판**. 
Gemini Chrome 자동화로 시드 이미지·체중계 숫자까지 자동 생성하고, Kling 40 클립 + ffmpeg 합성으로 **10세트 × 3포맷 × 2언어 = 60 영상** 을 한 파이프라인으로 뽑는다.

## 확장 포인트
| 항목 | v1 | v2 |
|---|---|---|
| 세트 수 | 1 | **10** |
| 시드 이미지 | 사용자 제공 | **Gemini 자동 생성** (before/after × 10) |
| 체중계 | 고정 kg | **Gemini 숫자 랜덤 치환** |
| 로고 제거 | — | **OpenCV TELEA+NS 자동** |
| 얼굴 모자이크 | 고정 박스 | **세트별 before/after 각각 수동 튜닝 박스** |
| 춤 스타일 | 1종 | **10종** (NewJeans/Apple/Supernova/HotToGo/BblDrizzy/Jiggle/ITZY/OhNanana/Runway/BodyRoll) |
| 자막 언어 | 한국어 | **한국어 + 번체 중국어** |
| 스텝 구조 | 5 | **8 (bdh)** |

## 핵심 기술 스택
- **Gemini Chrome 자동화**: `Desktop/MD/gemini-imagegen/gemini_auto.py` + `.session/` 재사용. Thinking 모델 강제 선택(`select_thinking_model`) 추가.
- **로고 리무버**: [[src-gemini-logo-remover]] 통합 (하단 좌/우 코너 타원 마스크 + TELEA+NS 블렌딩).
- **얼굴 검출**: `haarcascade_frontalface_default.xml` + padding. **검출 실패·오검출이 많아 수동 교정 필수** (아래 § 교훈).
- **Kling 배치**: 40 클립 순차 제출, 1303(parallel limit) 시 30/60/120s 백오프.
- **합성**: ffmpeg filter_complex — mosaic(before), mosaic(after), hstack / trim+split=2+concat 루프.

## 파이프라인 (bdh)
```
[00] BGM 분석 → BPM/드롭
[01] 10 세트 스타일·프롬프트 (40 파일)
[02] Gemini 세션 (login_once.py 수동)
[03] Gemini 시드 20장 (before/after × 10)
[04] Gemini 체중계 20장 (kg 랜덤)
[05] Kling 40 클립 (10s × 20 + 5s × 20)
[06] ffmpeg 합성 30영상 × 2언어 = 60
[07] eval + 박스 재튜닝
```

## 이번 세션에서 새로 배운 교훈 (tacit으로 승격)
- [[creative-patterns]]: **"얼굴 모자이크는 before/after 각각 박스 잡아야 한다"** — 같은 시드에서 Kling이 뽑는 before/after 카메라 거리·얼굴 높이가 달라 단일 박스로는 한쪽이 벗어남.
- [[coding-lessons]]: **"OpenCV haarcascade는 세로 이미지 전신샷에서 턱/복부를 얼굴로 오인하는 경우가 흔함"** — y 값이 y>400 이면 거의 오검출. 수동 교정이 최종 품질 결정자.
- [[coding-lessons]]: **"Gemini 빠른 모드는 이미지 생성 지시를 자주 무시"** — Thinking 모델 강제 선택 필요. 매 new_chat 후 재선택.
- [[coding-lessons]]: **"Gemini after 시드 생성 시 before 시드를 입력에 포함하면 그대로 복제"** — before 대신 원 배경(bg)을 재사용해야 "극적 대비" 프롬프트가 작동.
- [[psychology-insights]]: **"극적 환경 변화(어지러움·밤 → 정돈·낮) + 의상 변화가 다이어트 B/A의 감정 임팩트 핵심"** — 체형만 바뀌면 약함.
- [[creative-patterns]]: **"10종 춤 스타일로 세트 분리 → 같은 템플릿이 알고리즘에 '반복 콘텐츠'로 분류되는 것을 회피"** — 틱톡 바이럴 댄스명을 프롬프트에 직접 박기.

## 카피 라이브러리 (영문 댄스명 → 한국어 자극 훅)
영문은 자막에서 이상. 10종 한국어 훅 확정:
1. 살 뺐더니 친구가 몰라봄ㅋㅋ
2. 세달만에 옷장 싹 갈아치움
3. 체중계가 더 놀란 거 같음
4. 거울 보고 내가 더 놀람
5. 이 언니 원래 이렇지 않았음
6. 소개팅 취소당하고 결심한 결과
7. 45kg 뺀 거 저도 못 믿음
8. 다이어트 N회차 드디어 성공
9. 살이 어디로 증발함?
10. 보정 아니고 실제 모습입니다

번체 중국어 버전도 `styles.json.sets[*].hook_title_tw` 에 등재.

## 스크립트 맵 (전부 [[content-ai-automation]] §10 diet-b2a-v2 파이프라인에 속함)
| 파일 | 스텝 | 역할 |
|---|---|---|
| `scripts/lib.py` | 공용 | config 로드, 경로 해석, ffmpeg runner |
| `scripts/gemini_client.py` | 공용 | Playwright Gemini 자동화 + Thinking 모델 선택 + 로고 제거 |
| `scripts/logo_remover.py` | 공용 | [[src-gemini-logo-remover]] OpenCV TELEA+NS 인페인팅 |
| `scripts/detect_faces.py` | 공용 | OpenCV haarcascade 얼굴 검출 (before/after 각각) |
| `scripts/build_sets.py` | 공용 | 10 세트 config.json 생성 |
| `steps/00-bgm-analyze/analyze_bgm.py` | 00 | librosa BPM/드롭 분석 |
| `steps/01-styles-prompts/build_prompts.py` | 01 | 10 세트 × 4 prompt 파일 생성 |
| `steps/02-gemini-session/check_session.py` | 02 | Gemini 로그인 세션 검증 |
| `steps/03-gemini-seeds/gen_seeds.py` | 03 | before/after 시드 20장 + safe fallback |
| `steps/04-gemini-scales/gen_scales.py` | 04 | 체중계 kg 랜덤 치환 20장 |
| `steps/05-kling-20clips/gen_kling.py` | 05 | Kling 40 클립 submit+poll+download |
| `steps/06-compose-15/compose.py` | 06 | ffmpeg filter_complex 합성 (ko/tw 2언어) |

이 전체는 하나의 파이프라인이고, 각 스크립트는 [[ai-automation]] 의 **bdh(bob→dd→harness) 완주** 사례로 서로 직접 의존한다. graphify가 개별 스크립트를 단독 community로 떼지 않도록 이 목록으로 명시 연결.

## 관련 페이지
- [[src-diet-b2a-skill]] (v1)
- [[src-gemini-logo-remover]]
- [[content-ai-automation]]
- [[da-creative]]
- [[ai-automation]]
- [[creative-patterns]] · [[coding-lessons]] · [[psychology-insights]]

## 원본 위치
- `raw/skills/diet-b2a-v2/` 전체 트리
- `raw/skills/diet-b2a-v2/diet-b2a-v2-skill.zip` (140KB)
- 사용자 바탕화면: `C:\Users\gguy\Desktop\diet-b2a-v2-skill.zip`
