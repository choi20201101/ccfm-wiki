---
type: source
domain: content-ai-automation
brand: rusolve
confidence: high
created: 2026-04-16
updated: 2026-04-16
sources: [C:\Users\gguy\Desktop\talmo, C:\Users\gguy\Desktop\MD\gemini-imagegen]
---

# src-talmo-b2a

## 검색 별칭 — 탈모 · 비포애프터 · 루솔브 · Rusolve · 헤어숱 · 산후탈모 · B/A 자동화 · B/A 릴스 · 모발 · 헤어 풍성

## 탈모 비포애프터 릴스 자동 생성 스킬 (루솔브 런칭용)

## 루솔브 Rusolve 탈모 B/A 영상 공장

## 출산 후 탈모 변신 영상 자동화

## Kling Gemini 탈모 B/A 파이프라인

이 페이지는 위 키워드로 검색될 때 최상위 매치되어야 함 (graphify BFS 용).

## 요약
[[src-diet-b2a-v2]]의 **탈모 도메인 포팅 + 구조 정제 버전**.
3씬 구조(Before → Card → After), 얼굴 스티커, **정수리 확대 플로팅 위젯**, phone_look 후보정, 자연광 대비 조명으로 탈모 **심리 자극 극대화**.
v2 대비 burst(고무줄 폭발) 씬 **실험 → 폐기**, 헤어플립 엔딩으로 대체.

## 다이어트 v2 대비 차이

| 항목 | diet v2 | talmo |
|---|---|---|
| 도메인 | 체중감량 | 탈모 |
| 씬 구조 | 2씬 (B/A) | **3씬 (B + Card + A)** |
| 엔딩 | 댄스 | **헤어 이마→뒤로 쓸어넘기기** |
| 핵심 위젯 | 체중계 랜덤 kg | **정수리 확대 플로팅 박스** |
| 후보정 | — | **phone_look.py** (블러+그레인+비네팅+JPEG) |
| 조명 전략 | before/after 단조 | **저녁 실내 vs 낮 자연광 명확 대비** |
| 의상 | 프롬프트에 고정 | **4월 20-30도 현재 계절 반영** |
| 얼굴 모자이크 | 세트별 수동 박스 | **Haar + 상단55%제한 + 중간값 이상치 필터 + 고정 크기** |
| 시드 생성 | 기본 합성 방식 | **B안 (배경 "분위기만 참고") 확정** |

## 파이프라인 (bdh + 4단)
```
[00-bgm-pick]       BGM 크롤 + 드롭 지점 분석
[01-prompts]        세트별 before/after 프롬프트 (현재 gen_seeds.py 내장)
[02-gemini-session] Gemini 로그인 세션 확인
[03-gemini-seeds]   before+after 시드 2장 + phone_look 자동 후보정
[04-kling-clips]    Kling image2video 2클립 (before/after)
[05-compose]        ffmpeg 3씬 + 오버레이 (상단카피 + 정수리줌 + 얼굴스티커)
```

## 핵심 기술 스택
- **Gemini Chrome 자동화**: `Desktop/MD/gemini-imagegen` 세션 공유 (Thinking 모델 강제)
- **얼굴 스티커**: `face_cover.py` — Haar + 상단55% + median 이상치 필터 + 고정 크기
- **phone_look**: 가우시안 블러 1.0 + 필름 그레인 10 + 비네팅 0.25 + 따뜻한 색온도 + JPEG q85
- **정수리 확대**: `scalp_zoom.py` — 얼굴 위쪽 정사각 크롭 → 280px 확대 → 흰 테두리 + 라벨
- **Kling**: v1-6 image2video std 5s, 9:16 aspect, fallback 엔드포인트
- **합성**: ffmpeg filter_complex — concat 3 + overlay enable 조건부 오버레이

## 시드 생성 방식 — B안 + phone_look (A/B/C 비교로 확정)

A/B/C 3안 비교 결과:
- **A (모델만 업로드, 배경 텍스트 묘사)**: 자연스러우나 원본 배경 참고 불가
- **B (모델+배경 둘 다 업로드, 배경은 "분위기만 참고")** ⭐ 확정
- **C (프롬프트만 "shot on iPhone" 영문 명시)**: 인물 누락 실패

B안 프롬프트 핵심:
- `"2번 사진의 방 분위기와 색감만 참고 (똑같이 복제하지 말고 비슷한 느낌의 방으로)"`
- `"합성하지 말고 처음부터 하나의 장면으로"`
- `"조명 방향/그림자/원근감 자연스럽게 통일"`

생성 후 phone_look 자동 적용으로 AI 과선명 제거.

## 이번 세션에서 새로 배운 교훈 (tacit으로 승격)

### 크리에이티브 감각
- [[creative-patterns]]: **"정수리 확대 플로팅 위젯이 탈모 B/A 감정 임팩트 증폭"** — 체중계 대응 장치로 설정. 박스 위치 y=380 (상단 카피 2박스 하단)
- [[creative-patterns]]: **"Before 저녁 실내 vs After 낮 자연광 대비가 시간 경과 내러티브 강화"** — diet에서 배운 "환경 변화" 원칙의 조명 버전 심화
- [[creative-patterns]]: **"이퓨모먼트(A few moments later) 전환 카드가 B/A 간극 정당화"** — 3씬 구조의 접착제
- [[creative-patterns]]: **"브랜드명 모자이크 + 노란색 '3개월 뒤' 2박스 분리 = 자막 밀도 최적화"** — 단일 박스 대비 가독성·호기심 유발 둘 다 잡음
- [[creative-patterns]]: **"4월 20-30도 계절 현재 반영 의상이 '요즘 느낌' 신뢰도 결정"** — "베이지 오버사이즈 니트" 같은 모호 표현 대신 계절·기온 숫자 박기
- [[creative-patterns]]: **"After 몸매 드러나는 핏 + 자연광 = 후킹 핵심 조합"** — 크롭/미디 스커트/밀착 니트 등 **과하지 않게**

### 코딩/자동화 교훈
- [[coding-lessons]]: **"Haar cascade는 전신샷에서 티셔츠/복부를 얼굴로 자주 오인"** — v2에서 이미 관찰. talmo에서 **상단 55% 크롭 후 검출**로 해결
- [[coding-lessons]]: **"손/팔 올린 자세에서 Haar가 손을 얼굴로 오인"** — "가장 위쪽" 선택으로는 손이 위에 있어 실패. **median 위치에서 크기 120% 이상 벗어난 검출 필터링** 으로 해결
- [[coding-lessons]]: **"프레임별 얼굴 크기 변동이 스티커 크기 변동 유발"** — 기울어진 머리 등에서 박스 작아짐. **중간값 고정 크기** 사용으로 해결
- [[coding-lessons]]: **"Gemini 'shot on iPhone' 영문 프롬프트는 인물 누락 유발"** — 영문 카메라 지시는 Gemini에서 텍스트/배경 위주 생성으로 편향. 한국어 프롬프트 + **후보정(phone_look.py)으로 질감 부여**가 확실
- [[coding-lessons]]: **"Gemini 'N번 사진 합성해줘' 프롬프트는 인위적 합성감 발생"** — "분위기만 참고, 처음부터 하나의 장면으로" 표현이 자연 통합도 높음 (A/B 비교 검증)
- [[coding-lessons]]: **"Before/After 시드를 완전 별개 프롬프트로 생성하면 머리카락 색 불일치"** — 동일 인물에 조명 차이만 있어야 하므로 **HAIR_COLOR_SPEC 공통 블록** 삽입 필수
- [[coding-lessons]]: **"Windows cp949 인코딩 충돌 회피 위해 Python print em-dash 금지"** — UnicodeEncodeError 방지

### 심리/설득
- [[psychology-insights]]: **"탈모 B/A는 '정수리' 노출이 공포 방아쇠"** — 체중계 대비 더 프라이빗한 부위, 클로즈업 플로팅 박스가 강력한 페인포인트 증폭 장치
- [[psychology-insights]]: **"출산 3개월 전 → 3개월 뒤 카피 프레임이 시간 축 압축 효과 최대"** — 산후 여성 페르소나에서 "가능한 변화"로 인식
- [[psychology-insights]]: **"헤어 쓸어넘기는 손동작은 자신감 회복의 시각 코드"** — 고무줄 폭발보다 자연스럽고 보편적

## 내러티브 구조 결정 (burst 씬 실험 → 폐기)
초안: Before → Card → Burst(고무줄 팡) → After (4씬)
최종: Before → Card → After (3씬 with 헤어플립 엔딩)

**폐기 이유**:
- Kling이 고무줄 끊어지는 물리 모션 어색하게 생성
- 3개월 뒤 내러티브에 "물리적 폭발" 비유 과도
- 헤어플립 동작이 자신감 표현에 더 자연스럽고 보편

burst.png 시드 생성 로직·seed_burst config 키는 **제거 완료** (gen_seeds.py, gen_kling.py, compose.py).

## 스크립트 맵 (talmo 프로젝트 루트: `C:\Users\gguy\Desktop\talmo`)

| 파일 | 스텝 | 역할 |
|---|---|---|
| `scripts/gemini_client.py` | 공용 | Gemini 자동화 래퍼 (Thinking 강제) |
| `scripts/phone_look.py` | 공용 | **AI 이미지 → 핸드폰 촬영 질감 후보정** |
| `scripts/face_cover.py` | 공용 | 얼굴 스티커 합성 (Haar + 상단55% + 이상치 필터 + 고정 크기) |
| `scripts/scalp_zoom.py` | 공용 | **정수리 확대 플로팅 박스 생성** |
| `scripts/make_overlays.py` | 공용 | 상단 카피 2박스 (before/after), 캡션, DM CTA |
| `scripts/prep_refs.py` | 공용 | 레퍼런스 9:16 크롭 + 얼굴 확대 |
| `scripts/logo_remover.py` | 공용 | [[src-gemini-logo-remover]] 통합 |
| `steps/03-gemini-seeds/gen_seeds.py` | 03 | before/after 시드 2장 + phone_look |
| `steps/03-gemini-seeds/gen_face_refs.py` | 03 | **10명 다양한 얼굴 레퍼런스 자동 생성 (배치용)** |
| `steps/03-gemini-seeds/setup_batch.py` | 03 | **set2..setN config.json 자동 생성 (모델×배경 순환)** |
| `steps/04-kling-clips/gen_kling.py` | 04 | Kling 2클립 (before/after) |
| `steps/05-compose/compose.py` | 05 | ffmpeg 3씬 + 4종 오버레이 |
| `run_batch.sh` | 루트 | **10세트 파이프라인 순차 실행 스크립트** |

## 관련 페이지
- [[src-diet-b2a-v2]] (전신 파이프라인 부모)
- [[canvas-rusolve-v1]] (Rusolve 브랜드 캔버스)
- [[src-gemini-logo-remover]] (로고 제거)
- [[content-ai-automation]] §14 talmo (신설)
- [[da-creative]] · [[creative-patterns]] · [[coding-lessons]] · [[psychology-insights]]

## 원본 위치
- `C:\Users\gguy\Desktop\talmo\` 전체 트리 (PLAN.md, HOOK.md, harness/RULES.md, scripts/, steps/)
- Gemini 세션 공유: `C:\Users\gguy\Desktop\MD\gemini-imagegen\.session`
- Kling API: `talmo/api.txt`
