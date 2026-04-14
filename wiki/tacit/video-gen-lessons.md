---
tags: [tacit, video-generation, ai-pipeline, skincare, melable]
confidence: high
source: 메라블 피코샷 크림 30+ 영상 제작 경험 (2026-04-13~14)
---

# AI 영상 자동화 파이프라인 — 실전 교훈

> 30편 제작 / 실패 / 재생성 / 자막 재번역을 통해 얻은 암묵지

## 1. Kling API 1003 에러 — **실제 원인은 시계 drift였음**

### 처음 오해
- `code 1003 "Authorization is not active"`
- 5개 키 × 여러 계정에서 동일 → 계정 권한 문제로 오진

### 실제 원인 (Kling CS 답변으로 확인)
- **JWT `nbf` claim이 서버 시간보다 미래** → 아직 유효하지 않은 토큰으로 거부
- 로컬 Windows 시계가 실제 시간보다 **72초 빠름** (NTP 미동기화)
- `nbf = now - 5/-10/-30/-60` 모두 미래 → 거부
- `nbf = now - 120` ✅ 통과 (2분 버퍼로 drift 흡수)

### 해결
```python
payload = {"iss": ak, "exp": now + 1800, "nbf": now - 120}
#                                              ^^^^^ 필수!
```

### 시계 동기화 (근본 해결)
Windows 관리자 PowerShell:
```
w32tm /config /syncfromflags:manual /manualpeerlist:"time.google.com" /reliable:yes
w32tm /resync
```

### 교훈 (광범위 적용)
- **모든 서명 기반 API (JWT, OAuth, AWS sig, Stripe)** 은 시계 drift에 취약
- 앱 레벨: JWT `nbf = now - 120`, `iat = now - 60` 버퍼
- OS 레벨: NTP 자동 동기화 켜두기
- CI/CD 머신: ntpd/chronyd 데몬 확인 필수

### 우회 (드리프트 고치기 전)
- fal.ai 프록시: Kling 2.6, Avatar v2 Pro, TTS 모두 제공 (자체 서명 안 함)

## 2. 자막 싱크의 진실

### 실패 패턴
- 씬 전체에 KO 한 줄, EN 한 줄 → 씬이 5초 넘으면 뒤쳐짐
- 서브큐로 쪼개면서 EN을 **축약/패러프레이즈** → 더빙 실제 내용과 다름
- 한국어 subs를 글자수 비례 분배 → 단어 경계 안 맞음

### 성공 패턴 (Option B)
1. **EN은 오디오 실제 문장을 쪼갬** (축약 금지)
2. 각 청크는 자연스러운 구두점 경계(쉼표/마침표)에서 분할
3. KO는 해당 EN 청크의 **의미** 번역
4. duration = 씬 전체 × (청크 char수 / 씬 총 char수)
5. 마지막 청크는 남은 시간 다 먹임 (누적 오차 제거)

```python
# pseudocode
for scene, dur in zip(scenes, durations):
    chunks = [("I walk into", "걸어 들어가요"), ("the derm office", "피부과에"), ...]
    total_chars = sum(len(en) for en,_ in chunks)
    t = cum_start
    for i, (en, ko) in enumerate(chunks):
        w = len(en) / total_chars
        d = dur*w if i < len(chunks)-1 else (cum_start+dur) - t
        emit_cue(t, t+d, en, ko)
        t += d
```

## 3. 한국어 자막 — 중년 타겟 번역 원칙

### 금지어 (50~60대 이해 어려움)
- 영어식 조어: 풀스택, 스택, 풀 세트, 인박스, 피드
- 신조어: 소프트걸, Y2K, 덕후, 티 떨구다, 고고, 닷지
- 인터넷 축약: ㅋㅋ, 함, 됨, ㅇㅈ, 노노
- 직역: "페이드" → "옅어지다", "스킨" → "피부"

### 권장
- 표준어 완성형: `~이에요`, `~습니다`
- 숫자는 한국 단위: `60불` → `6만원`
- 브랜드명·성분명은 그대로 (PDRN, 나이아신, 트라넥사믹, 알파아르부틴)
- "가다" 대신 "서두르세요", "가세요"

## 4. 상단 고정 카피 (Top Copy)

- 9:16(1080×1920) 기준 **검정 바 520px 위쪽**에 배치
- 2줄 구조: **빨간색(상단) + 노란색(하단)** Arial Black
- fontsize 86, MarginV 200 / 298 (행간 적절 간격)
- 20~25자/줄, 후킹 메시지 (페인+베네핏)

## 5. B-roll 할루시네이션 방지

### 문제 사례 관측
- "거울 셀피" 시드 → Gemini 무한반사로 **사람 2~3명**
- "화장대에서 크림 바르기" → **Q-tip/솜뭉치 애플리케이터** 생성
- 인물 근접 샷 → 입 근처 크림 통 (먹는 장면처럼 보임)

### 프롬프트 네거티브 (Kling i2v `negative_prompt`)
```
multiple people, duplicate persons, mirror reflection, mirror, 
two people, three people, crowd, extra arms, extra hands, 
deformed face, cream in mouth, eating cream, licking product,
jar near mouth, cotton swab, applicator wand, Q-tip near face
```

### Seed Prompt 규칙
- `exactly ONE person in frame, NO mirror, NO reflections` 강제
- `jar stays at chest level (not near mouth)`
- `fingertip only, no applicator/cotton/wand`
- 배경은 `solid soft-lit interior wall`로 한정 (거울 피할 때)

## 6. 자동 Eval 루프 (Gemini Vision)

프레임 추출 후 gemini-2.5-flash에 JSON 반환 강제:

```
You are a strict video QA reviewer. Check this frame for:
(1) >1 person visible or mirror reflection of person
(2) cream jar near mouth / being eaten/licked
(3) Q-tip/applicator on face
(4) extra/deformed limbs
Reply STRICT JSON: {"issues": ["..."]}
```

- 문제 감지 시 해당 B-roll만 delete + 재생성 (1회 재시도)
- 재시도 후에도 남으면 건너뜀 (품질 vs 비용 트레이드)

## 7. 레퍼런스 분석 — 퍼포먼스 영상 패턴

ex/ 폴더 7개 레퍼런스에서 도출:

### A. 인플루언서 스타일 (자보티바)
- 1인 셀카 1인칭, 호텔방/욕실/차 배경
- 컷 간격 2~3초 (중간 속도)
- 듀얼 자막: 한국어 위 굵게 / 영어 아래 작게 노랑 이탤릭
- 상단 고정 카피 + 하단 듀얼 자막 구조

### B. META/스톡 스타일 (유쎄라블/위프)
- 인플루언서 없음
- 3D 의학 모델(해골, 피부 단면) 또는 일상 스톡 샷
- 큰 한국어 중앙 자막 (흰색 + 검정 외곽 3~4px)
- 컷 간격 0.5~1초 (급속 리듬, 타이포 위주)
- 길이 33~56초, 중앙값 45초

### C. 타이포 중심 (하나둘셋얍)
- 정방 1200×1200 사용 (세로뿐 아니라)
- 20+ 컷, 평균 0.5초
- 숫자 카운트다운 / 연속 페이스

## 8. 씬당 듀레이션 설계

| 구조 | 씬 길이 | 총 길이 | 컷 수 | 추천 톤 |
|---|---|---|---|---|
| 인플루언서 리뷰 | 2.5~5s | 30~45s | 8~12 | HOOK-PAIN-PRODUCT-PROOF-CTA |
| META 스톡 | 1.5~3s | 30~50s | 12~20 | 빠른 컷, 자막 중심 |
| 타이포 | 0.5~1s | 20~40s | 20~40 | 강한 리듬, 숫자 강조 |

## 9. TTS 경로

### 영어 (Kling TTS via fal-ai/kling-video/v1/tts)
- 작동 voice_id: `uk_man2`, `uk_boy1`, `uk_oldman3`, `oversea_male1`,
  `chat1_female_new-3`, `girlfriend_1_speech02`, `ai_shatang`, `ai_kaiya`,
  `tianmeixuemei-v1`, `guanxiaofang-v2`
- **안 되는 건**: `commercial_lady_en_f-v1`, `reader_en_m-v1` — "Voice id not found"
- 영어 여성 톤을 원하면 중국계 보이스 쓰면 영어도 그럭저럭 나옴

### 한국어 (fal-ai/elevenlabs/tts/turbo-v2.5)
- Korean 지원, voice=Rachel 기본 괜찮음
- 비용 비쌈 — 분량 관리 필요

## 10. 비용 경험치 (per 30~45s 완성본)

| 구성요소 | 비용/편 |
|---|---|
| Avatar v2 Pro ~35s | $4.03 |
| Kling i2v 5s × 4 B-roll | $2.00 |
| Gemini 이미지 × 7 (시드+B-roll+B&A) | $0.21 |
| Kling TTS × 8~11 세그먼트 | $1.10 |
| **합계** | **~$7.50** |

30편 = ~$225. 인플루언서 제거(Avatar 빼고 i2v로만) 시 $3~4/편 → $100/30편.

## 11. FFmpeg filter 디버깅

### 터진 패턴
- `drawbox ... enable='between(t,a,b)'` with 복잡 표현식 → 필터 실패 (exit -22)
- 인덱스 하드코딩: `[5:v] [6:v]` assuming 4 brolls, 실제 3 brolls → 입력 어긋남

### 안전 패턴
- `scale + pad + pad` 중첩으로 border/shadow 구현 (drawbox 안 씀)
- 인덱스는 `len(broll_specs)` 동적 계산
- `-shortest` 항상 붙임 (loop image로 인한 무한 확장 방지)

## 12. 자산 재사용 경제학

- Avatar v2 Pro 호출 한 번 ($4) = 풀 오디오 어떤 길이도 한 번에
- 같은 시드로 여러 스크립트 재생성 가능 (identity 유지)
- B-roll은 Gemini 시드 + Kling i2v (각 5s, $0.50)이 재활용 단위
- **후처리 실패 시 자산은 살아있음** → ffmpeg 재실행으로 복구 가능

## 13. 릴레이 믹스업 포맷 (발견)

- 여러 인플루언서가 한 문장 **릴레이** (대화X)
- 각 세그먼트 3~5s, 6~7 세그먼트 = 20~30s 영상
- 서로 다른 시드 6~7개 × 짧은 Avatar 호출
- 이어붙일 때 scale + fps + 오디오 sample rate 통일 필수
- 각 세그먼트 자막은 이어지는 **문장의 조각**이 되어야 함

## 14. **Gemini는 한국어 텍스트를 이미지에 못 그림** (매우 중요)

### 증상
- 씬 프롬프트에 Korean text가 baked-in 되면 거의 항상 **깨진 한글 글자** 출력
- 예: "'속보'" → 이상한 자모 조합, "'300만원'" → 뭉개진 한자 같은 글자
- 심지어 "숫자 98/100 Korean numbers" 같은 Korean qualifier 만으로도 품질 저하

### 규칙
1. **Gemini 프롬프트의 모든 한국어 텍스트 → 영어 대체**
   - "'속보'" → "'BREAKING NEWS'"
   - "'7일'" → "'7 DAYS'"
   - "'300만원'" → "'3 MILLION WON'"
   - "Korean typography" → "English typography"
2. **한국어 카피는 ffmpeg/ASS 후처리로만** — 자막·드로잉 텍스트
3. **2차 정리 필수** — 첫 번째 pass에서 놓친 `Korean text`, `Korean numbers` 같은 qualifier도 제거

### 구현 패턴
```python
# YAML visual 필드 정리 함수
KO = re.compile(r"[\uac00-\ud7a3]+")
def clean_visual(v):
    for old, new in SUBSTITUTIONS: v = v.replace(old, new)
    v = v.replace("Korean text", "bold text")  # qualifier까지 제거
    v = KO.sub("", v)                          # 잔여 한글 제거
    return re.sub(r"\s{2,}", " ", v).strip()
```

### 예외: 제품 라벨
- "melable RubyRN PicoShot" 같은 브랜드 영문은 OK (영자)
- "DAY 1", "DAY 7", "BEFORE", "AFTER" 같은 영문 자막도 OK
- 픽셀 단위로 한글 글자 복잡도 높아 diffusion model이 못 그림

## 15. ffmpeg 필터 흔한 함정

- `force_original_aspect_ratio=cover` ❌ 무효값 → `increase` / `decrease` 만 유효
- `-stream_loop -1 -i short.mp4 -t 2.0` 짧은 소스 루핑 OK (5s 소스 2s 잘라쓰기)
- crop 필터 순서: `scale:increase → crop` (오버스캔 후 잘라내기)

## 16. 안 되면 스킵해야 할 것들

- 거울 셀피 기반 페르소나 (99% 할루시네이션)
- "applying with cotton" / "swab"류 (Kling이 오브젝트 혼란)
- "walking while holding jar" (다리 기형화 빈번)
- "elevator mirror selfie" → 강제로 2명
- 정면보다 측면/3/4 앵글이 얼굴 일관성 더 잘 유지

---

*작성: 2026-04-14. 메라블 피코샷 크림 33편 생성 경험 기반.*
