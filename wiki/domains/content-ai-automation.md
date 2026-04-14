# 콘텐츠 AI 자동화 — 최근 1달 대화 전체 추출 정리

> 추출 기준: 2026-03 ~ 2026-04 (일부 2월 포함)
> 분류: 컷편집, 영상 비전 분석, 음성 Whisper, 자막 레이아웃, bob 구조 계획서
> 목적: 잘된 부분 선별 → 스킬/위키에 영구 반영

---

## 1. 컷편집 (FFmpeg 기반)

### 1-1. 핵심 결론

- **FFmpeg가 컷편집 최선** — 다른 도구(MoviePy, Remotion, Shotstack 등)도 내부적으로 FFmpeg 사용
- `-ss`(시작점) + `-to`(끝점)으로 트림, `concat`으로 이어붙이기
- 트랜지션 없이 컷 단위 붙이기는 FFmpeg가 가장 가볍고 빠름

### 1-2. 트림 + 전환효과 (xfade) 구현

```json
{
  "duration": 4,
  "trim_to": 2,
  "trim_start": 0
}
```

**전환효과 지원 10+ 타입:**
```json
"transitions": [
  {"type": "fadeblack", "duration": 0.15},
  {"type": "wipe_left", "duration": 0.25},
  {"type": "zoom", "duration": 0.2},
  {"type": "dissolve", "duration": 0.2}
]
```

### 1-3. Smart Trim (자동 베스트 구간 선택)

- **auto 모드**: 프레임 퀄리티 분석 → 베스트 구간 자동 선택 (양산용)
- **preview 모드**: 콘택트 시트 생성 → 직접 구간 지정 (정밀 편집)
- **fixed 모드**: trim_start 기반 단순 트림 (기본)

### 1-4. 퍼포먼스 광고 컷 구조 (15초 기준)

```
7씬 × 평균 2.1초 = 15초 광고
┌─2s─┬─2s─┬─3s─┬─2.5s─┬─1.5s─┬─3s─┬─1s─┐
│hook│미러│제품│사용  │텍스처│자신│CTA│
```

### ✅ 잘된 부분
- trim_to + trim_start JSON 스키마 확정
- xfade 전환효과 10+ 타입 + duration 설정
- Smart Trim 3가지 모드 (auto/preview/fixed)
- 1초 컷 리듬 원칙 적용

### 🔄 업데이트 검토 필요
- auto 모드 프레임 퀄리티 분석 알고리즘 정교화
- 퍼포먼스 광고 컷 구조 템플릿을 제품 카테고리별로 분기

---

## 2. 영상 비전 분석 (Gemini Vision / Claude Vision)

### 2-1. 레퍼런스 영상 분석 파이프라인

```
레퍼런스 영상 → yt-dlp 다운로드 → FFmpeg 프레임 추출 (1초 단위) → Gemini Vision 분석 → 로직 JSON
```

### 2-2. 1초 단위 7요소 추출 스키마

| # | 추출 항목 | 좌표 포함 |
|---|----------|----------|
| 1 | 인물/캐릭터 위치+동작 | ✅ bounding box |
| 2 | 배경 | ❌ 텍스트 |
| 3 | 메인 자막 (더빙 싱크) | ✅ 좌표+스타일 |
| 4 | 추가 자막 (강조) | ✅ 좌표+스타일 |
| 5 | 플로팅 이미지/영상 | ✅ 좌표+크기+타이밍 |
| 6 | 화면효과 | ❌ |
| 7 | 효과음 | ❌ 타임스탬프만 |

### 2-3. 이미지 일관성 해결: 템플릿 설정 (STEP 3.5)

모든 장면에 동일 character description 자동 삽입하여 인물/스타일 일관성 확보

### 2-4. 모션 분석: L2 프리셋 매칭 (추천)

정밀 모션 복제(L3) 대신 20~30개 프리셋 라이브러리로 "느낌" 재현

### ✅ 잘된 부분
- 7요소 추출 스키마 확정
- 템플릿 설정(3.5)으로 일관성 해결
- L2 프리셋 매칭이 현실적 타협점

### 🔄 업데이트 검토 필요
- 모션 프리셋 20~30개 구체적 목록 필요
- Gemini vs Claude Vision 성능 비교

---

## 3. 음성 Whisper (STT + 타임스탬프)

### 3-1. 핵심 용도

TTS 생성 → Whisper word-level 타임스탬프 → 자막 싱크 + 이미지 배치

### 3-2. 사용법

| 방법 | 비용 | 추천 |
|------|------|------|
| 로컬 Whisper (Python) | 무료 | 대량 처리 |
| OpenAI Whisper API | $0.006/분 | 소량 |

한국어: **small 이상** 모델 권장, medium이면 최적

### 3-3. TTS 길이 매칭 3단계

1차: ElevenLabs speed 파라미터 (target/generated = ratio)
2차: 오차 ±0.3초 이상 → 재생성
3차: ffmpeg atempo 필터 (0.8x~1.2x)

### 3-4. AE 자막 자동화 7단계

음성분석 → 번역대사생성 → TTS생성 → 길이대조 → ±1초검증 → 배치조절 → AE완성

### ✅ 잘된 부분
- word-level 타임스탬프 활용 패턴 확정
- TTS 길이 매칭 3단계 전략
- 7단계 파이프라인 구조

### 🔄 업데이트 검토 필요
- faster-whisper / WhisperX 비교 필요
- AE ExtendScript 한글 자동 감지 정확도 검증

---

## 4. 자막 레이아웃 + 세이프존 / 데드존

### 4-1. 플랫폼별 데드존 (2026-03 기준)

| 플랫폼 | 상단 | 하단 | 좌 | 우 |
|--------|------|------|---|---|
| 인스타 릴스 | 220px | 320px (광고:420) | 60px | 120px |
| 유튜브 쇼츠 | 380px | 300px (확장:400) | 60px | 120px |
| **유니버설** | **380px** | **420px** | **60px** | **120px** |

### 4-2. 유니버설 세이프존

**900 × 1120 px (x:60~960, y:380~1500)**

### 4-3. 자막 배치 규칙

- 메인 자막: x=540, y=1400, 48px, 흰색+검정외곽
- 강조 자막: x=540, y=500, 64px, 브랜드컬러
- 플로팅: 좌=80~500, 우=500~940, y=500~1300
- 자막 리듬: 8~10자 단위, 어절 단위 분할

### 4-4. 변동 관리

값은 고정 아님. 플랫폼 UI 업데이트 시 재측정 필수. 분기 1회 실측 권장.

### ✅ 잘된 부분
- 유니버설 세이프존 확정
- 자막 리듬 분할 규칙
- 변동 관리 원칙

### 🔄 업데이트 검토 필요
- 틱톡/커머스 데드존 미측정
- 2026-04 기준 IG/YT UI 변경사항 재확인

---

## 5. bob 구조 계획서 (경쟁사 레퍼런스 기반)

### 5-1. DD Plan (10단계)

| Step | 이름 | 핵심 도구 |
|------|------|----------|
| 00 | 프로젝트셋업+입력규격 | - |
| 01 | 레퍼런스 1초단위 분석 | Gemini 2.5 Pro + FFmpeg |
| 02 | 스크립트재작성+TTS | ElevenLabs |
| 03 | 장면이미지생성 | Gemini 크롬자동화 |
| 04 | 장면영상생성 Kling i2v | fal.ai Kling O3 |
| 05 | 플로팅에셋생성 | Safe Zone 내 |
| 06 | 자막생성 리듬분할 | 8~10자, 좌표 |
| 07 | 컷편집 리듬비교분석 | 1초 컷 배열 |
| 08 | 효과음매칭 | sfx-matcher |
| 09 | AE프로젝트조립 | afterfx.exe -r |

### 5-2. 성공 기준

1. 레퍼런스 1개 + 제품 정보 → AE .aep + 소스 폴더 자동 출력
2. 60초 영상 기준 30분 이내
3. AE 타임라인에 모든 소스 배치 완료

### 5-3. AI 평가 루프

완성 영상 → Gemini Vision 평가 (100점) → 70점+ PASS / 미만 시 문제 씬만 재생성 (최대 10회)

### ✅ 잘된 부분
- 10단계 DD Plan + 데이터 흐름도 완성
- 기술 스택 구체적 확정
- AI 평가 + 부분 재생성 루프

### 🔄 업데이트 검토 필요
- sfx-matcher 구체화
- AE JSX 표준화
- Kling O3 vs Seedance vs Veo 3.1 비교

---

## 6. 광고 소재 디자인 시스템 (DA 크리에이티브)

9개 파일 체계: 오버뷰, 공통+1:1, 9:16, 타이포+컬러, 카피패턴, 텍스트이펙트, 레퍼런스, 입출력스키마, 자동로직

핵심: 제품 회피 배치 로직 매트릭스 (제품 위치 8가지 경우별 카피 자동 배치)

Python 함수: `get_copy_layout()`, `get_text_effect()`, `select_highlight_words()`

### ✅ 잘된 부분
- 디자인 시스템 9파일 체계화
- 제품 회피 배치 로직
- Python 함수 바로 붙여넣기 가능

### 🔄 업데이트 검토 필요
- A/B 테스트 결과로 프리셋 최적화
- 카테고리별 분기 (스킨케어 vs 헤어 vs 바디)

---

## 7. 전체 요약 — 업데이트 판단 가이드

### ✅ 바로 반영 가능

| 영역 | 반영 대상 |
|------|----------|
| 컷편집 | trim JSON 스키마, xfade 전환, Smart Trim, 1초컷 리듬 |
| 비전분석 | 7요소 추출, 템플릿설정, L2 프리셋 매칭 |
| Whisper | word-level 패턴, TTS 매칭 3단계 |
| 자막 | 유니버설 세이프존, 5블록, 리듬 분할 |
| bob계획서 | 10단계 DD Plan, AI 평가 루프 |
| DA디자인 | 9파일 시스템, 제품 회피 로직 |

### 🔄 추가 검증 필요

| 영역 | 필요 작업 |
|------|----------|
| 컷편집 | auto 모드 알고리즘 정교화 |
| 비전분석 | 모션 프리셋 목록, Vision 모델 비교 |
| Whisper | faster-whisper 비교, AE 한글 감지 |
| 자막 | 틱톡/커머스 데드존 측정, UI 재확인 |
| bob계획서 | sfx-matcher, AE JSX, Kling 대안 비교 |
| DA디자인 | A/B 테스트, 카테고리별 분기 |

---

## 8. 스킬 파이프라인 교훈 — 영상 자동화 적용 (2026-04-13 추가)

> 로드된 스킬 전수 조사 후, 영상 자동화(10단계 DD Plan)에 바로 먹이는 패턴만 추려냄.
> 원천: `~/.claude/skills/user/` + Vercel/claude-api/harness 계열 스킬.

### 8-1. 파이프라인 구조 = 영상 DD Plan과 1:1 매핑

스킬 파이프라인: **bob → dd → harness → eval → learnings**
영상 자동화 DD Plan: **Spec 작성 → 10 step 분해 → 제약 강제 → AI 평가 70점 → 러닝 반영**

→ 같은 뼈대. 영상 자동화 계획서를 bob-auto-spec으로 시작하면 **레퍼런스 링크 1줄 → Spec 자동 생성 → DD 분해 → dd-executor 순차 실행**까지 사람 개입 없이 연결됨.

### 8-2. harness-auto-rules = 영상 제약의 린터화

지금까지 "합의/문서"였던 제약을 **실행 가능한 린터**로 내림:
- Safe Zone 좌표 (x:60~960, y:380~1500) → 좌표 범위 벗어난 자막 배치 JSON을 사전 거부
- 1초 컷 리듬 → 평균 컷 길이 > 3초면 CI 실패
- trim JSON 스키마 → 필수 키(duration/trim_to) 누락 시 빌드 중단
- 자막 리듬 8~10자 → 어절 분할 규칙 위반 시 리포트

**암묵지 → 형식지 → 실행 강제**의 최종 단계. 반복 실수 봉쇄.

### 8-3. eval-feedback-loop — 평가 루프를 순환형으로

기존 영상 자동화 AI 평가 루프는 **Gemini Vision 70점 → PASS/재생성**에서 멈춤 (직선형).
eval-feedback-loop 도입 시:
- 70점 미만 씬 원인 → **bob Spec**에 반영 (예: "이 제품 카테고리는 L2 프리셋 B계열 우선")
- 반복 감점 패턴 → **harness 규칙**에 반영 (예: "메인 자막 y>1400 금지")
- 즉, 이번 영상이 아니라 **다음 영상 자동화 생산성**이 올라감

### 8-4. eval-regression — 영상 품질 시계열 추적

단건 평가(70점/PASS)로는 "소리 없이 썩는" 회귀 감지 불가.
누적 eval 점수를 프로젝트별로 쌓으면:
- 카테고리별 평균 점수 추이 (스킨케어 vs 헤어)
- 모델 업데이트(Kling O3 → 후속) 전후 품질 변동
- ROAS 하락 이전에 **CTR 선행지표 감지**

### 8-5. learnings-confidence — 세이프존/프리셋 시간 감쇠

4-4 "분기 1회 실측 권장"과 정확히 맞물림:
- 플랫폼 데드존 측정값 → confidence 점수 + 마지막 검증일
- 90일 미검증 → 자동 플래그 → 세션 시작 시 "IG 데드존 재측정 필요" 알림
- 검증된 값만 harness 린터에 반영 (낡은 값으로 린트하면 역효과)

### 8-6. cross-project-sync — Merable → Rusolve 패턴 이식

2026 Rusolve 런칭 시 Merable에서 **검증된 영상 패턴만** 선택적 이식:
- 카테고리 상이(뷰티↔탈모) → 전부 복사는 위험
- confidence: high + eval 누적 70점+ 패턴만 전파 대상
- 이식 후 초기 eval 점수가 기존 Merable 대비 80% 미만이면 **패턴 회귀** 경고

### 8-7. psd-blueprint 철학 = 영상 자동화 일관성의 정답

psd-blueprint: "PSD 파싱 → 에셋+좌표 추출 → **기계적 조립**으로 99%+ 재현"
영상 자동화 2-2 (7요소 추출 + bounding box + 좌표): **완전 동일한 철학**

핵심 교훈:
- AI 생성(=확률적) 단계는 최소화
- 레퍼런스에서 **좌표/스타일/타이밍은 결정론적으로 추출**
- 마지막 조립은 AE JSX 등 기계적 렌더로 — 확률 변수 제거
- "일관성" 문제는 프롬프트로 풀지 말고 **구조화된 데이터 + 기계적 조립**으로 풀어야 함

### 8-8. parallel / subagent — 10단계 중 독립 step 병렬화

현재 DD Plan은 직렬 실행(60초 영상 30분 목표). 독립 step 병렬 가능:
- step 03 이미지 생성
- step 05 플로팅 에셋
- step 08 효과음 매칭

→ parallel 스킬로 3개 서브에이전트 동시 디스패치 시 **30분 → 15분 예상**.
의존성 맵: 01(분석) → 02(TTS) → [03, 05, 08 병렬] → 04(i2v) → 06(자막) → 07(컷편집) → 09(AE)

### 8-9. market-research 5병렬 = 이미 검증된 패턴 재사용

market-research 스킬이 쓰는 **5개 서브에이전트 병렬(cafe/community/instar/naverapi/youtube)** 구조는 영상 자동화의 **경쟁사 레퍼런스 수집**에 그대로 재사용 가능.
→ 레퍼런스 1개 지정 대신 **카테고리+브랜드만 입력 → 5채널 자동 수집 → 최상위 n개 자동 선정**.

### 8-10. code-fusion / multi-llm-orchestrator — AI 평가 교차검증

현재 AI 평가는 Gemini Vision 단일 채점. 편향 가능.
code-fusion 패턴: 같은 영상을 Gemini/GPT/Claude 3종 동시 평가 → 편차 큰 항목만 사람 리뷰.
→ **70점 PASS 기준의 신뢰도 자체를 올림**. 단, API 비용 3배 — 최종 컷 1회만 교차평가 권장.

### 8-11. verify / tdd — step별 중간산출물 증거 검증

"완료 주장 전 증거 필수" 원칙을 영상 DD에 적용:
- step 01 끝 → 추출 JSON의 7요소 전부 채워졌는지 스키마 검증 (빈 필드 있으면 step 02 진입 금지)
- step 02 끝 → Whisper 타임스탬프 word 단위 전부 존재 + 오차 ±1초 이내
- step 09 끝 → AE 프로젝트 무결성 + 렌더 테스트 프레임 1장 실제 생성 확인

→ "끝까지 돌았는데 AE 파일이 안 열린다" 사태 방지.

### 8-12. cleanup — DD step 폴더 GC

영상 1건당 step-00~09 폴더 × 중간 산출물(프레임/TTS/이미지/영상) 누적 → 수십 GB.
cleanup 스킬로 **PASS된 프로젝트 step 폴더는 최종 AE + 소스만 남기고 중간물 자동 삭제** 룰.

### ✅ 바로 반영 가능
- bob-auto-spec → 영상 계획서 Phase 0 자동화
- harness-auto-rules → Safe Zone/리듬/스키마 린터화
- parallel → step 03/05/08 병렬화로 30분 → 15분
- verify → step별 산출물 증거 검증 게이트

### 🔄 설계 논의 필요
- eval-feedback-loop 도입 시 Spec/harness 규칙 자동 수정 권한 범위
- cross-project-sync 이식 임계값 (Rusolve 런칭 시점에 재논의)
- 3-LLM 교차평가 비용 vs 품질 트레이드오프 실측

---

*추출 완료: 2026-04-12 (§1-7)*
*스킬 교훈 추가: 2026-04-13 (§8)*
*대화 소스: 15+ 스레드 + 로드된 스킬 전수 조사*

---

## 9. diet-b2a — 다이어트 Before/After 릴스 자동화 스킬 (2026-04-13)

→ 상세: [[src-diet-b2a-skill]]

### 9-1. 파이프라인 (bdh 완주 케이스)
```
bob PLAN.md  →  dd steps 00~05  →  harness RULES  →  output/영상{1,2,3}.mp4
```
- **4장 이미지 + config 5줄** → 10초 릴스 3본 자동화. 인물/프로젝트 교체 = config 편집만.
- Kling image2video(v1-6, std, 9:16) 4개 클립(A3_fat, A3_thin, B4_fat, B4_thin) + ffmpeg filter_complex 합성.

### 9-2. 3종 영상 구조 (레퍼런스 포맷 복제)
| 영상 | 레이아웃 | 길이 | 전환/동작 |
|---|---|---|---|
| 1 | 좌우 분할 (Before\|After 동시) | ~9.4s | 1-2-3 손가락 카운트 싱크, 하단 타이틀 |
| 2 | 중앙 인물 + 우상단 체중계 | ~10s | 4s 하드컷: 전반 팔 다운 리듬 → 후반 1.2× 축하 춤 루프 |
| 3 | 중앙 인물 + 좌상단 체중계 (거울) | ~10s | 동일 |

### 9-3. ffmpeg 핵심 패턴 (재사용 가능)
```
# 얼굴 모자이크 (720x1280 좌표계)
[in]split=2[a][b];
[a]crop=W:H:X:Y,scale=iw/22:ih/22:flags=neighbor,scale=W:H:flags=neighbor[m];
[b][m]overlay=x=X:y=Y[out]

# 전→후 하드컷 + 후반 1.2× 루프 (5s → 6s 유지)
[0:v]trim=0:4[v0]
[1:v]setpts=PTS/1.2,split=2[a][b]; [a][b]concat=n=2:v=1:a=0,trim=0:6[v1]
[v0][v1]concat=n=2:v=1:a=0
```

### 9-4. 프롬프트 설계 규칙 (Kling 싱크 실전)
- 첫 문장: 의상/체형/배경 고정
- 중간: **초 단위로 포즈 시퀀스 명시** (`0-1s 팔 다운, 1-2s 팔 올려 X자 ...`) — 10초 영상에서만 잘 먹힘
- 금지어는 대문자 (`NO dancing`)
- before/after 쌍은 `EXACT SAME motion synchronized` 문구로 일치성 강제
- em-dash(—) 사용 금지 (cp949 크래시)

### 9-5. 좌표 레이아웃 (1080×1920)
- 영상1: 체중계 (270,370)/(810,370) 310폭, 라벨 y=165, 타이틀 하단
- 영상2: 체중계 (780,430) 400폭 / 날짜 (625,125) 48pt
- 영상3: 체중계 (260,430) 380폭 / 날짜 (105,130) 48pt

### 9-6. 재사용 포인트
- `config/default.json` 5슬롯(이미지 4 + 카피 5 + face_box + audio 3 + kling 설정) 만 수정
- 훅은 [[HOOK]] 30선 라이브러리에서 선택
- 동작 전환은 `prompts/*.txt` 파일 단위 교체 (동적 f-string 치환 금지, 재현성 저해)

### 9-7. 교훈 (tacit으로 승격)
- "전→후 하드컷은 양팔 다운 중립 포즈에서 자르면 끊김이 안 보인다" → [[creative-patterns]]
- "전반 리듬 + 후반 폭발 춤" 구조가 다이어트 변신 해방감에 가장 강함 → [[creative-patterns]] / [[psychology-insights]]
- "얼굴 모자이크 박스는 머리 영역만. 넓히면 어깨·가슴까지 덮여 미관 파괴" → [[creative-patterns]]
- "Kling std 10s가 5s보다 포즈 초 단위 지시 준수율 높음" → [[coding-lessons]]
- "프롬프트에 em-dash 쓰면 Windows cp949에서 state 저장 크래시" → [[coding-lessons]]

*추가: 2026-04-13 (§9 diet-b2a)*
*추출 완료: 2026-04-12*
*대화 소스: 15+ 스레드*

## 관련 소스
- [[src-youtube]] — yt-dlp 대량 수집 + Claude CLI 서브에이전트 4개 병렬 분석 (자막 풀텍스트)
- [[src-instar]] — 인스타 릴스 yt-dlp 익명 추출 + Claude Vision 프롬프트 자동화
- [[src-diet-b2a-v2]] — 대량생산·다국어 B/A 공장 (아래 §10)
- [[src-instarup]] — 인스타 릴스 자동 업로드 파이프라인 (아래 §11, §12)

---

## 10. diet-b2a-v2 — 다이어트 비포애프터 릴스 대량생산·다국어 공장 (2026-04-14)

### 검색 별칭
- 다이어트 영상 자동화
- 비포애프터 릴스 스킬
- 다이어트 변신 쇼츠
- 체중감량 릴스 대량
- B/A 10세트 60영상
- Kling Gemini 파이프라인

→ 상세: [[src-diet-b2a-v2]]

### 10-1. 스케일 확장
- 세트 1 → **10**, 언어 1 → **2 (ko + 번체)**, 영상 3 → **60개** 한 파이프라인.
- 모델 5 × 배경 5 × 춤 10 × kg 랜덤 × 2언어 조합.

### 10-2. 시드 자동화 (Gemini Chrome)
- Playwright persistent context + `.session/` 재사용.
- 매 new_chat 후 **Thinking 모델 강제 선택** (Fast는 지시 무시).
- **체중계 숫자까지 Gemini로 랜덤 치환** (외관·로고·테두리 유지, 숫자만).
- 생성 후 자동 로고 제거: [[src-gemini-logo-remover]] 통합.

### 10-3. 얼굴 모자이크 — **before/after 각각** 박스 (v2 차이점)
- v1은 단일 박스. v2에서 Kling 결과 얼굴 위치가 before/after 서로 다름이 확인되어 `face_boxes.json`을 `{sid: {before:{}, after:{}}}` 구조로 확장.
- OpenCV haarcascade는 30%+ 오검출 → **수동 검토 루프** 필수. 프레임 추출 후 눈으로 확인.

### 10-4. 카피 로컬라이제이션
- 영문 댄스명(NewJeans Super Shy 등) → 한국어 자극 훅(살 뺐더니 친구가 몰라봄ㅋㅋ 등) + 번체 자극 훅(瘦了之後朋友都認不出來) 각 10종 등재.
- 날짜 자막 `2025년 12월 ↔ 2025年12月` 언어별 자동 치환.

### 10-5. Kling 40 클립 배치
- 10s × 20 + 5s × 20 순차 submit. code 1303(parallel limit) → 30/60/120s 백오프.
- `raw/tasks.json` 멱등: task_id 있고 mp4 100KB+ 면 skip.

### 10-6. 이 섹션이 주는 직원 공유 포인트
1. "스킬 한번 만들면 10개 콘텐츠 하루만에" 가능한 수준으로 공정화된 첫 B/A 스킬.
2. 시드·체중계·로고·자막·BGM·모자이크까지 전부 스크립트 파라미터. 사람은 styles.json만 터치.
3. 거부/안전 필터 자동 우회(AI 캐릭터 명시, 의상 완화, safe fallback)로 실전 운영 가능.

### 10-7. 파이프라인 스크립트 인덱스 (graphify 통합)
모두 [[src-diet-b2a-v2]] 하위. 각 파일이 이 도메인의 구성원이며 서로 순차 의존:
- `lib.py` · `gemini_client.py` · `logo_remover.py` · `detect_faces.py` · `build_sets.py` (공용 라이브러리)
- `analyze_bgm.py` → `build_prompts.py` → `check_session.py` → `gen_seeds.py` → `gen_scales.py` → `gen_kling.py` → `compose.py` (스텝 00→06 순차 실행)
- 공용 라이브러리는 스텝 여러 개가 import 함 → graphify 그래프에서 **hub 노드** 로 자리잡음

*추가: 2026-04-14 (§10 diet-b2a-v2, [[src-diet-b2a-v2]])*

---

## 11. Instagram 릴스 자동 업로드 (검증됨, 2026-04-13)

### 11-1. 검증된 업로드 파이프라인

> confidence: high (실제 테스트 업로드 2건 성공 — 계정 `jmtw.12345`, 3MB mp4, 대만시장 번체중문 캡션)

**결론**: 공식 Graph API 대신 `instagrapi` (비공식 Private API, ID/PW 로그인)가 **현실적으로 가장 빠른 구현**. 단, ToS 위반 & 계정 밴 리스크 감수.

### 11-2. 최소 동작 코드 (약 40줄)

```python
from instagrapi import Client
cli = Client()
# 세션 재사용 (재로그인 최소화 — 밴 방어 핵심)
if session_file.exists():
    cli.load_settings(session_file)
    cli.login(username, password)  # 세션 있어도 login 호출 필요
    cli.get_timeline_feed()  # 세션 유효성 검증
else:
    cli.login(username, password)
    cli.dump_settings(session_file)
# 릴스 업로드
media = cli.clip_upload(path=video_path, caption=caption_with_hashtags)
# → media.pk, media.code 반환. URL: instagram.com/reel/{code}/
# 삭제: cli.media_delete(media.pk)
```

### 11-3. 실전 교훈 (테스트에서 검증)

- **로그인 → 업로드 총 소요: 38초** (신규 세션, 3MB 영상 기준). 세션 재사용 시 업로드만 ~28초
- `clip_upload` 내부에서 moviepy로 썸네일 자동 생성 — ffmpeg 바이너리 PATH 필수 아님 (imageio-ffmpeg 번들)
- 캡션에 해시태그 같이 넣음 (별도 필드 없음). 2200자·30해시태그 제한
- 업로드 직후 `media_delete(pk)` 즉시 먹힘 → 테스트 후 정리 용이

### 11-4. 멀티계정 운영 (50~100개) 아키텍처

- **accounts.xlsx 단일 파일**로 계정 관리. 필수 컬럼: username, password. 나머지(account_name, session_file, status, daily_limit, proxy, note)는 빈칸 허용, 첫 실행 시 자동 채움
- account_name 자동 생성: username의 특수문자(`.`, `+` 등) → `_` 치환
- 계정당 고유 `sessions/{account_name}.json` → 재로그인 횟수 최소화
- **밴 방어 파라미터** (검증 전이지만 합리적 기본값):
  - daily_limit 5건/계정 (신규 3건)
  - 업로드 사이 랜덤 60~180초 지터 (고정 간격 금지)
  - 계정별 고유 device_settings 고정 (`cli.set_device()`)
  - proxy 계정별로 분산 강력 권장 (IP 분산)

### 11-5. 예외 처리 패턴

- `LoginRequired`, `ChallengeRequired`, `PleaseWaitFewMinutes` → 해당 계정 status=paused + 알림
- 챌린지/2FA 발생 시 `instarup relogin --account <n>` 대화형으로 해결
- 세션 만료(`get_timeline_feed` 실패) → 자동 재로그인 + 세션 덮어쓰기

### 11-6. 워크플로우 설계 (BDH 스킬로 검증)

```
videos/{account}/pending/   ← 사용자 투입
   ↓ analyze (Claude Code 서브에이전트 병렬, A/B 캡션 생성)
drafts/{account}.xlsx       ← 사람이 엑셀로 검토·승인 (yaml 아닌 엑셀이 훨씬 편함)
   ↓ plan (일정 할당)
schedule/{account}.xlsx     ← 예약 큐
   ↓ run (APScheduler 데몬)
videos/{account}/uploaded/  ← 성공 자동 이동
videos/{account}/failed/    ← 실패 이동 + 로그
```

- **엑셀 > yaml** (50~100 계정 규모에서 검토 UX 차이 큼)
- **검토 게이트 필수** (status=draft → approved 수동 변경)
- **A/B 캡션 자동 제안** + custom_caption 수기 오버라이드 옵션 (감성톤/직관톤 2개)

### 11-7. AI 캡션 생성 비용 절감 패턴

- **anthropic SDK 직접 호출 금지** → Claude Code 서브에이전트(Agent 툴)로 대체
- Python 코드는 ffmpeg로 영상당 5프레임(10/30/50/70/90% 지점) 추출만 담당
- Claude Code 스킬이 서브에이전트 10개 병렬 디스패치 → 프레임 Read → 캡션 생성 → 엑셀 기록
- 이유: (a) API 비용 제거 (구독에 포함), (b) 서브에이전트 병렬성 활용, (c) 아키텍처 단순화

### 11-8. 관련 소스
- [[src-instarup]] — 프로젝트 경로: `C:\Users\Administrator\Desktop\instarup\`
- BDH 스킬로 Spec v5까지 반복 구체화 후 step-00/01 구현 + E2E 업로드 검증 완료

---

## 12. instarup 확장 스펙 — 백엔드·UI·배포 (2026-04-13)

> confidence: high — 실제 구현·테스트 완료 부분 + medium — 배포 계획 부분

### 12-1. 완성된 백엔드 구조 (BDH 파이프라인 결과물)

```
src/instarup/
  accounts.py    # accounts.xlsx R/W (username/password만 필수, 나머지 자동)
  config.py     # config.yaml (upload_delay_min/max, daily_limit, paths, limits)
  state.py      # state/processed.json (account+hash 키, count_today)
  scanner.py    # videos/{account}/{pending,uploaded,failed}/ 상태머신
  uploader.py   # instagrapi Client + 세션 재사용 + _move 폴더 이동
  planner.py    # schedule/{account}.xlsx R/W, due_rows(now)
  scheduler.py  # APScheduler BlockingScheduler + 랜덤 지터(60~180s) + daily_limit
  cli.py        # status / schedule add|list / run / upload-now
```

- **핵심 교훈**: 엑셀을 "컨트롤 패널"로 쓰면 사용자가 대량 편집(50~100행 복붙)을 엑셀로 할 수 있어 UX 압승. 데몬은 60초 폴링으로 엑셀 변경을 자동 반영
- **테스트**: pytest 13/13 통과 (accounts/state/scanner/config)

### 12-2. Streamlit UI 스택 (한국 커뮤니티 표준)

- **streamlit-option-menu** 패키지 사용 — Bootstrap 아이콘 내장, 한글 라벨 자연스러움
- 상단 수평 메뉴 (`orientation="horizontal"`) + 사이드바는 `collapsed` 기본값
- 커스텀 CSS로 MainMenu/footer 숨김, 카드형 UI(그림자+테두리+pill)
- 인스타 브랜드 컬러 `#E1306C` (primary) — `.streamlit/config.toml`에 테마 지정

```python
# 한국 Streamlit 프로젝트에 복붙용 스니펫
from streamlit_option_menu import option_menu
selected = option_menu(
    menu_title=None,
    options=["대시보드", "업로드", "큐", "계정", "로그"],
    icons=["grid-fill", "cloud-upload-fill", "list-task", "person-circle", "terminal"],
    orientation="horizontal",
    styles={
        "nav-link-selected": {"background-color": "#FDF2F6", "color": "#E1306C"},
    },
)
```

- **데몬 제어 패턴**: `subprocess.Popen([sys.executable, "-m", "mod.cli", "run"])` + `st.session_state.daemon_proc` 으로 UI 내 시작/중지 버튼
- **로그 tail**: `log_path.read_text().splitlines()[-200:]` → `st.code(..., language="log")`

### 12-3. Windows 패키징 3-배치 패턴

1. `install.bat` — `py -m pip install -e .` + 템플릿 생성 (최초 1회)
2. `start_ui.bat` — `py -m streamlit run app.py` (브라우저 자동 오픈)
3. `start_daemon.bat` — UI 없이 데몬만 (서버 스타일)

모두 `cd /d "%~dp0"` + `set PYTHONPATH=%~dp0src` 헤더로 src-layout 해결.

### 12-4. Vercel 배포의 현실 (모바일 친화 질문 시 대답 템플릿)

> **Vercel은 이 종류 자동화에 절반만 맞음**. 반드시 설명해야 할 제약:

- ❌ APScheduler 데몬 실행 불가 (서버리스 = 항상 켜진 프로세스 없음)
- ❌ instagrapi 세션 파일 저장 불가 (디스크 휘발성)
- ❌ 긴 업로드 작업 불가 (함수 타임아웃 10~60초)
- ❌ 영상 파일 임시 저장 불가
- ✅ 모바일 UI(Next.js)는 완벽

**권장 2-tier 아키텍처**:
```
Vercel (Next.js mobile UI) ──HTTPS──▶ Backend (always-on)
                                       - FastAPI
                                       - APScheduler daemon
                                       - instagrapi sessions
                                       - 영상 저장소
```

**백엔드 호스팅 옵션 티어표**:
| 옵션 | 비용 | 항상 켜짐 | 난이도 |
|---|---|---|---|
| A. 본인 PC + Cloudflare Tunnel | 무료 | PC 켜진 동안만 | 쉬움 |
| B. Railway | ~$5/월 | ✅ | 쉬움(깃푸시) |
| C. Fly.io 무료 티어 | 무료 | ✅ | 중간 |
| D. Oracle 무료 VPS | 무료 | ✅ | 어려움 |

**Phase 접근법** (대화 시 제안 템플릿):
1. Phase 1: FastAPI로 백엔드 재구성(현 Python 80% 재사용) + Next.js 모바일 UI — 로컬 테스트
2. Phase 2: Vercel(프론트) + Railway/PC터널(백엔드) 배포
3. Phase 3: 인증(단순 비밀번호 or NextAuth)

### 12-5. 재사용 가능한 결정 체크리스트 (IG 자동화 신규 프로젝트 시)

- [ ] 업로드 라이브러리: **instagrapi** (Graph API보다 빠른 구현, ToS 위반 감수)
- [ ] 계정 레지스트리: **accounts.xlsx 단일 파일** (username/password만 필수)
- [ ] 세션 재사용: **`sessions/{account}.json`** dump/load (밴 방어 핵심)
- [ ] 검토 UX: **엑셀 기반** (yaml/JSON 버림 — 50~100건 스케일에서 엑셀 압승)
- [ ] 예약 큐: **schedule/{account}.xlsx** 계정별 분리
- [ ] 폴더 상태머신: **pending → uploaded/failed** (삭제 금지, 이동만)
- [ ] 데몬: **APScheduler BlockingScheduler + IntervalTrigger(60s)**
- [ ] 지터: **랜덤 60~180s** (고정 간격 금지 — 봇 패턴 회피)
- [ ] daily_limit: **신규 3건 / 숙성 5~10건**
- [ ] UI: **Streamlit + streamlit-option-menu** (로컬) / **Next.js** (모바일·원격)
- [ ] AI 캡션: **Claude Code 서브에이전트** (anthropic SDK 직접 호출 금지)
- [ ] Harness: **Level 3** (ruff + mypy strict + pre-commit + 커스텀 훅)

### 12-6. 관련 링크
- [[src-instarup]] — 프로젝트 레퍼런스
- [[content-ai-automation#11. Instagram 릴스 자동 업로드]] — §11 검증된 스니펫
- 지식 체인: BDH(bob+dd+harness) 파이프라인 적용 사례. Spec v1→v5 진화 전체 기록이 `dev/active/insta-autopost/state.md`

*추가: 2026-04-13 (§11 instarup 업로드, §12 백엔드·UI·배포, [[src-instarup]])*

---

## 13. 외국인 인플루언서 리뷰 영상 자동화 (fal.ai·Kling Avatar v2 Pro, 2026-04-13~14)

> confidence: high — 33편 완성본 실제 제작 (메라블 루비알엔 피코샷, 기미 타겟 / 40~60대 여성) · 상세: [[src-foreign-influencer-guide]]

### 13-1. 핵심 스택 선택 (재사용 권장)
- **Kling 직통 API 비활성 (code 1003)** → **fal.ai 프록시로 Avatar v2 Pro / i2v 2.1 Pro / TTS 전부 우회**. 계약 전 API 호출 테스트 1회 의무화.
- 립싱크 = **Kling AI Avatar v2 Pro** (fal), 모션 B-roll = Kling i2v 2.1 Pro, 시드·B&A·B-roll 시드 = Gemini 2.5 Flash Image (제품 라벨 유지 reference), TTS = Kling TTS(EN) + ElevenLabs(KO), 편집 = FFmpeg + ASS.
- 자동 QC = Gemini 2.5 Flash Vision (거울 반사·크림 입가·Q-tip·변형 수지 감지 → 해당 B-roll만 재생성 1회).

### 13-2. 실측 비용·시간 (1편 = 40초)
- **$7.90/편** (Avatar $4.60 + i2v×4 $2.00 + Gemini×7 $0.21 + TTS×11 $1.10). 33편 실측 $340.
- 10~15분/편 (Avatar 2~5분 병목). 29편 순차 5~7h.
- 재렌더(자막만): **1~2분/편** — Avatar 재사용, ffmpeg만 재실행. 비싼 자산은 disk cache로 멱등화.

### 13-3. 포맷 표준 (9:16 세로 1080×1920)
- 길이 30~45초, 구조 **HOOK(0-4) → PAIN(4-10) → PRODUCT(10-20) → PROOF(20-30) → CTA(30-35)**.
- 메인 립싱크 아바타 + PAIN/PRODUCT/APPLY/CTA 씬 **B-roll 4개** 오버레이.
- 한/영 이중 자막 (KO 크게 위, EN 작게 노랑 이탤릭 아래) + 검정 바 520px 상단 2줄 카피.

### 13-4. 할루시네이션 회피 프롬프트 표준
- 메인 시드: `Exactly ONE person, no mirror reflections` **필수**. 거울 셀피 페르소나는 무한반사로 무조건 실패 → 평면 벽 배경 강제.
- i2v negative prompt 공통 세트: `multiple people, mirror reflection, extra arms, deformed face, cream in mouth, eating cream, licking product, jar near mouth, cotton swab, applicator wand, Q-tip near face`.
- **이미지 AI에 한글 baked-in 금지** — 한글은 깨진 글자로 렌더. `Korean text`/`Korean numbers` 같은 qualifier까지 제거. 한국어 카피는 전부 ASS 후처리 자막으로.

### 13-5. FFmpeg filter_complex 재사용 교훈
- `scale=1080:1080,pad=1080:1920:0:520:black,setsar=1` 로 Avatar 1440² → 9:16 (상/하 검정 520px).
- 오버레이 체인 `overlay=0:520:enable='between(t,start,end)'[vN]` 누적 → 마지막에 `ass='subs.ass'[v]` (자막은 항상 최상단, 안 가리게).
- **필터 인덱스 동적 계산 필수**: `n = len(broll_specs); sb_idx = n+1` — 하드코딩 시 입력 개수 변동에 파싱 실패.
- `force_original_aspect_ratio=cover` 값 없음 → `increase` 또는 `decrease`만.

### 13-6. 중년(40~60대) 한국어 자막 규칙
- AI 번역 → 그대로 쓰면 "소프트걸 불가능", "풀스택 미백", "ㅋㅋ", "고고" 등 Z세대 슬랭 혼입 → **수동 교정 필수** (금지어 리스트 운영).
- EN 서브큐는 오디오 **실제 문장을 쉼표/마침표로 분할**, KO는 EN 청크의 의미 번역. 시간 = 씬 duration × (청크 char / 총 char).
- PIP y좌표 540 (상단 카피 아래) — 하단 자막 safe zone(y~1500) 침범 금지.

### 13-7. 배치 운영 체크리스트 (다음 제품 재사용 시)
- [ ] 시드 이미지 1장으로 페르소나 identity 고정 (Gemini reference)
- [ ] 각 단계 파일 존재 시 skip — Avatar $4×N 재생성 방지
- [ ] 백그라운드 배치는 `| head` 금지 (SIGPIPE 사망), `> log.txt 2>&1` redirect
- [ ] subprocess 실패 시 `e.stderr.decode()[-300:]` 반드시 로그
- [ ] 배치 마지막에 `DONE: X/Y` 명시 로그 — 프로세스 exit ≠ 논리 완료
- [ ] 레퍼런스 영상 1:1 복제 불가 (Avatar v2 Pro는 오디오 길이만 맞춤) → 기획 단계에서 "느낌" 모방 + 변주 허용

### 13-8. 관련 소스
- [[src-foreign-influencer-guide]] — 7개 문서 + scripts(personas/creative_scripts/mashups/USP) 전체 원본
- raw 백업: `raw/foreign-influencer-guide/` (README·01 계획·02 훅·03 파이프라인·04 자막·05 레퍼런스·06 실패·07 비용)
- 프로젝트 코드: `C:/Users/Administrator/Desktop/klinginter/src/` (fal_kling/gemini/subtitle/batch_20/batch_mashup/fix_subs_c)

*추가: 2026-04-15 (§13 외국인 인플루언서 Kling Avatar 파이프라인, [[src-foreign-influencer-guide]])*
