---
aliases: ["영상 생성 교훈", "Kling·Gemini 실전 이슈"]
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

## 17. Day별 변화 시드 생성 — **얼굴형 시드 분리 패턴** (2026-04-21 볼륨필인 추가)

### 문제
동일 인물 Day1~Day14 변화 영상에서 face seed만 사용하면:
- Day1의 볼꺼짐이 Gemini 기본 경향(얼굴 부드럽게)으로 약하게 그려짐
- Day2부터 이미 플럼핑되어 조기 회복 (사용자 피드백 "볼꺼짐 없이 그냥 바뀜")

### 해결 — 시드를 2종류로 분리
1. **face/** = 얼굴 정체성 시드 (원본 셀카 2장)
2. **bfex_split/before/** = 얼굴형(고민 상태) 시드 1장 — 사용자가 제공한 참조 이미지의 Before 부분만 크롭
3. Gemini edit에 3장 입력 + 프롬프트에 "FIRST TWO = identity blend, LAST = ONLY shape guide for cheek hollow depth"

### 효과
- 측면 프로필 bfex(세로 그림자 진함) 사용 시 가장 극적
- 사용자 "이정도 극적인 느낌" 기준 달성

### 프롬프트 필수 문구
```
"SEVERE dramatic volume loss: vertical shadow groove from cheekbone to jaw,
 pronounced nasolabial folds, drooping mouth corners, skull-like cheekbones,
 looks 5-10 years older than actual age"
```

### Day 2~6 조기 회복 방지 (핵심)
```
"CRITICAL FOR EARLY DAYS (2-6): her face volume and hollow cheek depth should
 look ALMOST IDENTICAL to Day 1 reference — DO NOT plump, DO NOT fill hollow,
 DO NOT smooth nasolabial folds"
```
+ Day 2-6 generation에 bfex shape reference 재주입.

## 18. Apply 씬 — **그래픽 도트 금지**, 촉촉 웻룩만

### 실패 (v6-v7)
- "5-7 purple ampoule dots on cheek like rejuran spots" → Gemini가 **스티커·이모지** 같은 그래픽 도트 생성
- 사용자 피드백 "그래픽 이미지 올린거처럼 됨 ㅋㅋ"

### 성공 (v8)
도트 개념 완전 제거. 대신:
```
"On sunken left cheek, the ampoule has JUST been applied and is visible ONLY as
 a GLOSSY DEWY WET PATCH of skin — freshly moisturized-looking with subtle
 specular highlight. NO purple color, NO pigment. Recognizable only by its
 slightly wetter/shinier look. Skin pores visible THROUGH the sheen.
 Fingertip mid-tap on this wet area.
 ABSOLUTELY NO graphic dots, NO cartoon droplets, NO painted shapes."
```
→ 실제 세럼 바른 직후 피부 광택처럼 자연스러움.

## 19. Kling i2v — 모션 중 얼굴 스무딩 방지

### 문제
Day1 시드는 볼꺼짐 극적이지만, Kling i2v 5초 모션 중 얼굴이 '예뻐지며' 플럼핑.

### 해결 negative_prompt
```
cheek plumping in motion, face smoothing during clip, volume appearing,
hollow filling in, beautification filter, skin smoothing, face younger,
wrinkles removed, cheeks filling up, hollow disappearing, skull line disappearing mid-clip
```

Day1 prompt에도 명시:
```
"CRITICAL: preserve DEEPLY sunken cheeks and vertical shadow groove throughout
 the entire clip — do NOT smooth, plump, or beautify her face.
 Keep the skull-line silhouette every single frame."
```

## 20. Speaking 클립 기법 — 립싱크 없이 vlog 느낌

### 목적
사용자 요청: "1~3일차 보여주고 아바타가 말하는 장면 점점 좋아지나요? 하면서"

### 구현 — **아바타 립싱크 없이 표정만**
- Day7 시드 → Kling i2v "mouth slightly opens as if asking a question, curious engaged expression, slight head tilt"
- Day11 시드 → Kling i2v "opens mouth as if emphasizing a word, nods once, warm knowing half-smile"

### 효과
- 2초짜리 클립 × 2회 인터리브로 vlog 느낌 성공
- OmniHuman/Aurora 아바타 ($0.14~0.16/s) 없이 Kling i2v ($0.05/s)만으로 해결
- 나레이션은 기존 TTS가 이어지지만 시청자는 '말하는 장면'으로 인지

## 21. 3인 릴레이 Trio 패턴 — "저도 해결했어요!"

### 구조
- 3명(30대/40대/50대) Day1 각 2초 = 6초 페인 릴레이
- 공통 제품 reveal (1명 대표) + apply (1명 대표)
- 3명 Day14 각 2초 "저도/저도/저도 해결" 릴레이
- **triple_split 엔딩** — 3분할 좌우 (360×1920 × 3) Day14 스틸 + 하단 "저도/저도/해결!" PIL 배너
- CTA 2초

### 효과
- 단일 testimonial보다 공감 자극 2배
- 연령 폭 30·40·50대 전부 커버 → 타겟층 넓힘
- TTS만 바꿔 10 variants 생성 가능 (전연령/필러거부/가격비교/주변반응/일자별변화/보르피린성분/약국권위/이벤트준비/다이어트후)

### 주의
- triple_split PIL 배너는 **malgunbd.ttf** (한글 지원) 필수. arialbd.ttf 쓰면 □□□ 박스.
- triple_split 구간(15-18s) 자막은 Hook 스타일(MarginV 620 상단)으로 올려 PIL 배너와 분리

## 22. 구조 해시 배정 — **같은 자산, 다양한 스토리**

### 패턴
```python
def pick_structure(set_id: str) -> str:
    return STRUCTURE_NAMES[hash(set_id + "struct") % len(STRUCTURE_NAMES)]
```
set_id에 따라 결정론적으로 9개 구조 중 하나 배정 → 재현성 + 자연스러운 분포.

### 9개 구조 (15s × 6 + 20s × 3)
- A_classic / B_shock_open / C_14first / D_product_open / E_montage_open / F_5beat (15s)
- G_vlog_20s (speaking × 2) / H_story_20s / I_diary_20s (20s)

### 리믹스
기존 시드·클립·TTS 재사용하고 compose 단계에서만 다른 구조 적용 → **1분/편** 추가 생성 가능. 비용 $0.

## 23. Day14 복장 풀 다양화 — **피로도 방지**

### 문제
초기 OUTFIT_14가 고정된 리스트 → 모든 영상 Day14 엔딩이 **같은 burgundy silk blouse**.
사용자 피드백 "마지막 복장이 완전 똑같아서".

### 해결
`setscene.outfit_for(set_id, day)` — 일자별 풀에서 set_id 해시로 선택.
Day14 finale pool 10종: cream silk / burgundy / powder-blue / terracotta / camel turtleneck / deep forest / beige trench / dusty pink / navy blazer / ivory cashmere.

### 교훈
**광고 40편 기획 시 '엔딩 복장'도 배리에이션 축**. 스토리·씬 구성만큼 시각적 피로도 결정자.

## 24. CTA 청크 풀 — **"14일 챌린지 참여" 반복 방지**

### 문제
모든 스크립트 마지막 2청크가 "1+1 할인" + "14일 챌린지 참여"로 동일 → 광고 피로도.

### 해결
```python
CTA_PRICE = [...10종...]   # 1+1 69% / 48% 할인 / 55ml / 당일출발 / ...
CTA_ACTION = [...12종...]  # 14일 챌린지 / 30일 환불 / 3만 포인트 / 간미연템 / ...

def pick_cta(set_id):
    return [CTA_PRICE[hash(set_id+"cta1") % 10],
            CTA_ACTION[hash(set_id+"cta2") % 12]]
```
각 세트마다 10×12=120 조합 중 1개. 40편에 동일 CTA 조합 반복될 확률 거의 없음.

## 25. TTS/자막 분리 — **숫자 오독 방지** (핵심 기법)

### 문제
ElevenLabs multilingual_v2가 한국어 숫자 오독:
- "14일" → "열네일" (X)
- "1+1" → "원 플러스 원" (읽긴 읽지만 어색)
- "5살" → "오살" (X)

### 해결 — chunk를 dict로 분리
```python
# scripts_ko.json
{"sub": "14일 후엔", "tts": "십사일 후엔"}
{"sub": "1+1 할인", "tts": "원플러스원 할인"}
{"sub": "5살 어려", "tts": "다섯살 어려"}
```
`chunk_util.py`의 `chunk_tts()` / `chunk_sub()` 헬퍼로 각각 추출.
자막은 눈에 예쁜 표기, 오디오는 자연스러운 발음. 둘 다 최적.

---

*작성: 2026-04-14. 메라블 피코샷 크림 33편 생성 경험 기반.*
*확장: 2026-04-21 볼륨필인 앰플 33편 + Trio 10편 경험 (§17-25).*

## 26. 참조 이미지 모자이크 제거 인페인팅 (2026-04-23 추가)

### 문제
사용자가 개인정보 보호 모자이크(블러) 씌워진 얼굴 참조 이미지를 제공할 때, bfex shape guide로 쓰면 Gemini가 **모자이크 아트팩트까지 복사**함. 결과물의 눈이 블러 처리되어 나옴.

### 해결 — Gemini edit으로 인페인팅
```
"Keep EVERYTHING exactly the same — same face shape, cheekbones, skin, hair, clothing, background, pose, lighting.
ONLY replace the blurred eye region with natural clear Korean eyes.
[eye characteristics: double/monolid, dark brown iris, natural lashes, tired under-eye].
The rest of the face must NOT change."
```

결과물을 `skull_unmask.png` 같은 ASCII 명명으로 저장 → 이후 파이프라인에서 bfex 참조로 사용.

### 이점
- 원본의 **실제 구조 정보(해골형/볼꺼짐/주름)는 그대로 유지**
- 눈 영역만 자연스러운 새 눈으로 교체
- 전체 재생성보다 훨씬 원본 충실도 높음

## 27. "shadow/hollow/dark" 키워드가 Gemini 그래픽 패치 유발 (금지)

### 문제 관측 (볼륨필인 샘플 v4~v8 반복 실패)
프롬프트에 `"deep shadow on cheeks"`, `"dark hollows"`, `"shadowed mid-cheek"` 등 명시 시:
→ Gemini가 **검은 타원 패치**를 볼에 그림 (makeup contour 같은 그래픽)
→ 사용자 피드백: "그래픽 이미지 올린거처럼 됨"

### 해결 — 금지 단어 & 대체 용어
❌ 금지: shadow, hollow, dark, shadowed, shadow pools, painted shadow

✅ 대체:
- "inverted triangle face outline"
- "cheekbones protruding as visible bone ridges"
- "mid-cheek indented inward"
- "sculpted angular face structure"
- "natural bone prominence"
- "physics-correct lighting on bone structure"

### 추가 네거티브 프롬프트
```
"no painted shadow patches on cheeks, no makeup contour, no graphic overlays"
```

### 왜 일어나는가 (추정)
Gemini 2.5 Flash Image는 "shadow"라는 단어를 Photoshop/makeup overlay로 해석하는 경향. "bone structure"로 쓰면 natural physics lighting으로 렌더.

## 28. Before/After 동일 장소 + 옷만 변경 원칙

### 사용자 피드백 (2026-04-23)
"해결된 얼굴과 같은 장소에서 찍는 느낌으로 해줘 옷만 변경되도록"
"14일동안 변화할 수 있는 느낌으로"

### 이전 실패 패턴
Day1과 Day14의 장소·가구·커튼·조명이 다름 → 서로 다른 날·다른 셋업 느낌 → 변화의 연속성 낮음.

### 성공 패턴
- **같은 공간** (same bedroom dresser, same curtains, same mirror, same camera angle)
- **같은 헤어스타일** (Day1~Day14 공통 "low messy bun" or "half-up ponytail" — 14일 만에 머리 바꾸는 건 부자연스러움)
- **옷만 변경** (Day1 홈웨어 → Day14 spring blouse 등, 일자별 outfit pool 로테이션)

### 효과
- 같은 거울 앞에서 매일 찍은 **일상 브이로그** 느낌
- 변화 자체에 시선 집중 (배경 노이즈 제거)
- 진정성·신뢰도 상승

### 프롬프트 패턴
```
"SAME location, SAME curtains, SAME furniture, SAME camera angle as reference.
SAME hair style (low messy bun).
ONLY outfit and face volume changes between before/after."
```

### 시즌 맞추기
봄(4월)이면 turtleneck/cashmere 금지, spring blouse·cotton tee·linen shirt 등 light-weight fabric만.

## 29. 헤어·메이크업 드리프트 방지 (부수 발견)

14일 progression에서 Day14가 갑자기 메이크업한 얼굴이 되면 "다른 사람" 느낌.

### 규칙
- Day1~Day6: "no makeup, natural bare skin" (고민 스테이트)
- Day7~Day10: "subtle tinted lip, minimal blush" (회복 중)
- Day11~Day14: "natural K-beauty makeup (soft blush, tinted lip)" (회복 완료)

메이크업을 점진적으로 추가 → Day14 변신이 자연스러움 (확 달라진게 아니라 **점점 밝아진 본인**).

---

*확장: 2026-04-23 볼륨필인 Day1 인페인팅 성공 사례 기반 (§26-29).*

## 30. "silhouette/outline" 키워드 = Gemini가 검은 선 드로잉 유발 (금지)

### 문제 관측 (2026-04-23 14일 progression Day13)
프롬프트에 `"copy the rounded/soft/egg-shape face silhouette from reference"` 사용 →
Gemini가 얼굴 턱 라인을 따라 **검은 선을 실제로 드로잉**. 사용자 피드백: "Day13 얼굴에 검정색 선이 들어가있는데?"

### 해결 — 금지 단어 & 대체 용어
❌ 금지: silhouette, outline, face line, edge line, shape line

✅ 대체:
- "cheek volume"
- "cheek fullness / plumpness"
- "bone curvature"
- "natural face anatomy"
- "how plump her cheeks should look"

### 네거티브 프롬프트
```
"no drawn edges, no graphic lines, no visible outline drawn on face"
```

### 종합 금지 키워드 리스트 (§27 + §30)
이제 Gemini Image Edit 프롬프트에서 절대 금지:
- shadow / dark / hollow
- silhouette / outline / face line
- 모두 그래픽 패치 또는 검은 선으로 렌더링됨

## 31. Day14 옷 변경 강제 패턴 (2026-04-23)

### 문제
Day1을 앵커로 Day14 생성 시 Gemini가 **Day1과 같은 옷을 유지**하는 경우 발생. 사용자 피드백: "B 영상 마지막 에프터랑 비포랑 얼굴이 같음 이상함" (얼굴뿐 아니라 옷도 같음).

### 해결 — 명시적 negation
Day14 prompt에 구체적 차이 + 명시적 부정:
```
"OUTFIT CHANGED to: a fresh cream silk blouse with a delicate small bow tie at the neckline
 (spring-weight, NOT a white T-shirt, NOT the same as Day 1)."
```

`NOT ...` 구문으로 직접 부정하면 Gemini가 따름.

## 32. 피부 세포 3D 애니메이션 기법 (B/A 비주얼 임팩트)

### 구조
1. **cells_shrunken.png** — 쭈글쭈글 세포 클러스터 (Gemini text-to-image)
   - 프롬프트: "3D medical visualization of dehydrated shriveled skin cells, raisin-like wrinkled surface, gray-purple"
2. **cells_plump.png** — 탱탱 세포 클러스터 (Gemini text-to-image)
   - 프롬프트: "3D medical visualization of healthy plump skin cells, round juicy pink-lavender grapes, glossy hydrated"
3. **cells_morph.mp4** — Kling i2v 쭈글 → 탱탱 (5초)
   - 입력: cells_shrunken.png
   - 프롬프트: "cells rapidly PLUMP UP AND FILL OUT, swelling into round juicy grape-like cells, subtle light burst"

### 영상 내 활용
나레이션 "세포가 파바박 차올라요"와 **cell_morph 클립 싱크** → 강한 시각적 임팩트. B/A 설득력 2배.

### 비용
- Gemini text-to-image × 2장: ~$0.08
- Kling i2v 5s × 1: $0.35
- 총 ~$0.45로 고급 의학 애니메이션 효과 재현

## 33. Dramatic Product Reveal Kling 기법

### 목적
제품 씬을 단순 정적 홀드 대신 **럭셔리 CM 같은 dramatic reveal**로 연출.

### 레시피
1. **product_dramatic.png** 시드 생성 (Gemini edit):
   - 입력: product_hold.png (원본 제품 누끼)
   - 프롬프트 핵심:
     - "hero product shot, slightly tilted, floating in ethereal luxury atmosphere"
     - "soft rim lighting, subtle light burst behind cap, sparkle particles floating"
     - "pastel gradient bokeh background (pink-lavender)"
     - "Chanel/Dior-level luxury commercial quality"
     - "product label UNCHANGED from reference"
2. **Kling i2v 회전 모션**:
   - 프롬프트: "product rotates gently and tilts toward camera, catching rim light, sparkle particles floating"

### 효과
"볼륨필인 앰플을 만나면" 나레이션 타이밍에 제품이 빛나며 회전 → "이 제품이 답이구나" 강한 각인.

## 34. 14일 progression 성공 영상 표준 구조 (17s locked in)

### 레퍼런스 구조 (2026-04-23 확정)
```
0-2.5s   Day1 Kling (해골형 모션)           + "피부 세포 쭈글쭈글 탄력이 죽어"
2.5-4.5s 제품 dramatic Kling (회전 + 스파클) + "볼륨필인 앰플을 만나면"
4.5-7.5s 세포 파바박 Kling (쭈글 → 탱탱)    + "세포가 파바박 차올라요"
7.5-13s  14일 몽타주 (14 stills 크로스페이드) + "푹꺼진 볼 해골형 얼굴이 14일 만에 이렇게 변화"
13-15s   Day14 Kling (탱글 미소 모션)
15-17s   Before/After 좌우 분할 + CTA
```

### 검증된 나레이션 리듬
총 8 청크 × 14초 타깃 (atempo 자동 조정):
1. "피부 세포가 쭈글쭈글"
2. "탄력이 죽어가요"
3. "볼륨필인 앰플을 만나면"  ← 제품 등장 큐
4. "세포가 파바박 차올라요"   ← 세포 morph 큐
5. "푹꺼진 볼"                 ← 14일 몽타주 시작
6. "해골형 얼굴이"
7. "14일 만에"  (TTS "십사일")
8. "이렇게 변화합니다"

### 복제 가능성
이 17초 구조는 **주름·기미·리프팅·여드름·탈모·다이어트** 모든 B/A 카테고리에 그대로 이식 가능:
- Day1 해골형 → 주름 제품이면 "주름 가득한 얼굴"로 교체
- cells_morph → 탈모 제품이면 "모낭 활성화" 애니메이션
- Day1-14 progression → 카테고리별 14일 변화 시드 풀 교체
- 나레이션 청크만 카테고리에 맞게 rewrite

### 핵심 교훈
**비주얼 4요소 모두 필요** — 인물 비포·제품 dramatic·과학 애니메이션·14일 몽타주. 1개라도 빠지면 설득력 급감.

---

*확장: 2026-04-23 볼륨필인 3인 × 세포 애니 × 14일 몽타주 성공 사례 (§30-34).*

---

## 35. 컷편집·자막·TTS 매칭 — 21초 광고 v09 정리 (2026-04-30)

> 18-21초 vertical 광고 만들 때 가장 자주 깨지는 부분: **씬 길이를 고정값으로 박지 않고 보이스에 맞춰 자르는 것**. 그리고 **자막은 보이스 char-level 타임스탬프 위에 1단어씩 얹는 것**.

### 35.1 절대 금지 — "씬 = 2초 고정"
- 처음에 SCENES = `[(0,2), (2,4), (4,6)...]` 식으로 박아두고 TTS만 따로 만들면 **8/13 라인이 씬 경계 넘김** (총 5.86s 오버플로). "더빙 끝나기 전에 다음 씬으로 넘어감" 발생.
- 해결: **TTS 길이 → 씬 길이** 단방향 의존. 씬은 보이스가 결정한다.

### 35.2 정석 파이프라인 (단방향 의존)
```
대본(13 라인)
  ↓ ElevenLabs with-timestamps
tts/SXX.mp3 + tts/SXX.json (char timestamps)
  ↓ ffprobe로 실제 길이 측정
SXX_dur (실측 — API 응답 길이 ≠ 실제 mp3 길이)
  ↓ atempo 라인별 (1.07~1.23) 라인이 너무 길면 압축
tts_v8/SXX.mp3 + 비례 조정된 timestamps
  ↓ 누적 + GAP=0.05s
timeline = [(SXX, st, et, dur), ...]
  ↓ 비주얼 segs를 (et - st) 길이로 렌더 (씬 = TTS 길이 + GAP)
seg_NN.mp4 (각 씬마다 길이 다름)
  ↓ concat
silent.mp4
  ↓ 워드팝 자막 (단어별 timestamp)
subs.ass
  ↓ ffmpeg subtitles + amix audio
final.mp4
```
**핵심: 씬 길이는 TTS 길이로 결정. 절대 역방향 안 됨.**

### 35.3 라인별 속도 매트릭스 (코덱스 합의 결과)
씬이 너무 길어 광고 18초 안에 안 들어오면, **라인별로 atempo 차등 적용**해서 압축:
- 후킹/CTA 같이 임팩트 필요 → atempo 1.00~1.07 (천천히)
- 정보 전달 라인 → atempo 1.10~1.20 (빠르게)
- 긴급/숫자 강조 → atempo 1.20~1.23 (최대 압축)

루비알엔 v09 실측:
| 라인 | 내용 | atempo | 결과 길이 |
|------|------|--------|-----------|
| S01 후킹 | 1.14 | 2.28s |
| S02-S03 도입 | 1.00 | 1.30+1.35s |
| S04 후기 | 1.13 | 1.78s |
| S05 30→1 수치 | 1.20 | 2.09s |
| S06 1일차 | 1.00 | 0.74s |
| S07-S08 3,5일차 | 1.18, 1.10 | 1.55+1.24s |
| S09 7일차 광채 | 1.07 | 1.60s |
| S10 +166% | 1.23 | 2.19s |
| S11 핑크광 | 1.00 | 1.25s |
| S12 가격 | 1.20 | 2.21s |
| S13 CTA | 1.00 | 1.30s |
| **총합** | | | **21.54s** |

균일 1.00 (총 25.4s) → 라인별 차등 (21.54s). 광고 플랫폼 21초 제한 안에 들어옴.

### 35.4 자막 = char-level → word-level → dialogue-per-word
- ElevenLabs `with-timestamps` 응답의 `alignment.characters` + `character_start_times_seconds`/`_end_times_seconds`을 받아 **공백 경계로 단어 묶기**.
- 각 단어가 별개의 `Dialogue:` 줄. 시작 = `scene_st + word.st - 0.05` (살짝 일찍 등장), 끝 = 다음 단어 시작 (틈 없음).
- 마지막 단어만 `+ 0.30s` 여유.

```python
def split_words_with_times(align):
    words = []; cur = ""; cur_st = None
    for ch, st, et in zip(align["characters"],
                          align["character_start_times_seconds"],
                          align["character_end_times_seconds"]):
        if ch.strip() == "":
            if cur: words.append((cur_st, et, cur)); cur=""; cur_st=None
        else:
            if cur_st is None: cur_st = st
            cur += ch; cur_end = et
    if cur: words.append((cur_st, cur_end, cur))
    return words
```

### 35.5 워드팝 = 무조건 안 잘림
- TikTok/Reels 스타일 큰 폰트(180-260pt) 쓰면서도 한 화면 1단어만 표시 → **가로 오버플로 절대 발생 안 함**.
- 등장 애니: `\fscx40\fscy40\t(0,140,\fscx112\fscy112)\t(140,260,\fscx100\fscy100)\fad(50,80)` (40% → 112% 바운스 → 100% 안착, 50ms 페이드인 80ms 페이드아웃).
- 한 줄에 여러 단어를 큰 폰트로 띄우면 가로폭 1080 넘어 잘림. **무조건 1단어**.

### 35.6 atempo 시 timestamps도 같이 압축
TTS json 그대로 두고 mp3만 atempo하면 자막 동기화 깨짐. **반드시 char timestamp도 비례 조정**:
```python
data["alignment"]["character_start_times_seconds"] = [t / sp for t in starts]
data["alignment"]["character_end_times_seconds"]   = [t / sp for t in ends]
```

### 35.7 ffprobe로 실측 길이 사용 — TTS API 응답 신뢰 금지
- ElevenLabs API 응답의 `character_end_times_seconds[-1]`이 실제 mp3 길이와 미세하게 다름 (codec 인코딩 오차).
- 무조건 ffprobe `-show_entries format=duration`으로 실측 후 timeline 계산.
```python
r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                    "-of","default=noprint_wrappers=1:nokey=1", str(mp3)],
                   capture_output=True, text=True)
dur = float(r.stdout.strip())
```

### 35.8 GAP — 씬 사이 0.05s 호흡
- TTS 끝나자마자 다음 씬이 0.00s에 시작하면 너무 답답.
- GAP = 0.05s (50ms) 추가 → 씬 전환 자연스럽고 보이스는 끊기지 않음.
- GAP=0.10 이상 두면 광고 21초 제한 빠듯하므로 0.05 권장.

### 35.9 씬 종류별 길이 가이드 (실측)
| 씬 종류 | 권장 길이 | 이유 |
|---------|-----------|------|
| 후킹 | 1.8~2.5s | 너무 짧으면 못 읽음, 길면 스크롤됨 |
| 정보 전달 | 1.0~1.5s | TTS 길이만큼만 |
| 일차 진행 (Day1, 3, 5, 7) | 0.8~1.2s | 빠른 컷 |
| 광채 폭발 / 임팩트 | 1.5~1.8s | 임팩트 살릴 시간 |
| 스탯 (+166% 등) | 2.0~2.5s | 숫자 인지 시간 |
| 가격 | 2.0~2.3s | 숫자 + CTA 인지 |
| 최종 CTA | 1.2~1.5s | "구매하세요" 짧고 굵게 |

### 35.10 마지막 카피 박스 — 색 충돌 체크
- BoxPink 스타일에 핑크 accent 텍스트 입히면 **글자 안 보이고 빈 박스만 뜸**. 사용자가 "마지막 핑크박스만 보임"이라고 함 = 정확히 이 버그.
- ASS BorderStyle 3 + BackColour = 박스. 위에 PrimaryColour나 `\1c` accent 색이 박스 색과 같으면 투명.
- 핑크 박스 위 = 흰 텍스트 (None accent), 노란 박스 위 = 검정 텍스트, 검정 박스 위 = 흰/핑크/노랑.

### 35.11 핵심 정리 — 컷편집 타이밍 10대 규칙
1. **씬 길이는 TTS 길이가 결정** — 2초 고정 절대 금지.
2. **TTS는 `with-timestamps` 엔드포인트** — char-level 타임스탬프 받아둬야 자막 동기화 가능.
3. **ffprobe로 실측 길이** — API 응답 신뢰 금지.
4. **라인별 atempo 차등** — 광고 길이 제한 맞추되 임팩트 라인은 천천히.
5. **atempo 적용 시 timestamps도 비례 압축** — 안 하면 자막 어긋남.
6. **GAP 0.05s** — 씬 사이 호흡, 더 길게 두면 안 됨.
7. **자막 = 1단어씩** — 큰 폰트(220pt+) 쓰면서도 안 잘림.
8. **단어 시작 -0.05s 일찍 등장** — 보이스보다 살짝 먼저 보여야 자연스러움.
9. **다음 단어 시작 = 현재 단어 끝** — 틈 없는 연속 표시.
10. **박스 색 vs 텍스트 색 충돌 체크** — accent 매핑 시 배경/박스 색과 다른 색 강제.

- confidence: high
- source: 2026-04-30 rubi_v09 광고 (1080x1920 21.54s, 13 라인 TTS, 45 워드팝, atempo 차등 적용 후 광고 21초 제한 통과)

---

## 36. 컷 길이 = 다음 cue start 까지 (NOT TTS 발화 길이) (2026-04-30, 루비알엔 v2 24컷)

§35.1 의 자매 교훈. 24컷 빌드에서 별개로 터진 같은 패밀리 버그.

### 증상
24컷 영상 빌드 시 마지막 5.5초 TTS(S22~S24) 통째로 잘림. 영상 48.7s, 오디오 54.1s. mux의 `-shortest` 가 영상 길이로 오디오 트림.

### 원인
컷 mp4 길이를 `cue['end'] - cue['start']` (= TTS 순수 발화) 로 잡음 → 발화 사이 자연스러운 호흡(0.1~0.5s × 23개 ≈ 5.5s)이 비디오 트랙에 안 잡혀 비디오가 오디오보다 짧아짐.

### 해결
```python
for idx, c in enumerate(cues):
    nxt = cues[idx+1]['start'] if idx+1 < len(cues) else total
    dur = max(0.6, nxt - c['start'])
```
컷이 다음 cue 시작까지 늘어나면서 자동으로 음성 총 길이와 일치.

### §35.1 과의 차이
§35.1: 씬 길이를 미리 박아두면 발화가 씬을 넘어감 (overflow).
§36: 씬 길이를 발화 정확 길이로 잡으면 호흡 갭이 누락되어 underflow + `-shortest` 잘림.
**둘 다 정답: cue start 기반 가변 길이.**

## 37. 자막↔TTS 텍스트 강제 일치 + 숫자 한글화 (2026-04-30, 루비알엔)

### 증상
자막 "1+2 세트 55%" 위에 음성 "원 플러스 투 세트, 오십오 퍼센트 할인" 이 깔림. 시청자가 자막을 보면서 음성을 들으면 단어 매칭 실패 → 인지 부조화 → 신뢰도 하락.

### 룰
**자막 텍스트와 TTS 발화 단어 1:1 일치 강제.** 의역·축약·확장 금지.

### 숫자/기호 → 한글 변환 (TTS 입력용)
| 자막 표기 | TTS 입력 |
|----------|---------|
| `+166%` | "백육십육 퍼센트" |
| `+107%` | "백칠 퍼센트" |
| `-91%` | "구십일 퍼센트" |
| `25,000건` | "이만 오천 건" |
| `1+2` | "원 플러스 투" 또는 "일 더하기 이" |
| `30초` | "삼십 초" |
| `30일` | "삼십 일" |
| `PDRN` | "피디알엔" |

ElevenLabs multilingual_v2 가 한글 발음을 정확히 읽으려면 한글로 입력 필수. 영문/숫자 그대로 두면 영어식 또는 어색한 발음.

## 38. 묵음 압축은 silencedetect 트림, cut/rejoin 금지 (2026-04-30, 루비알엔)

### 실패한 방식
TTS를 라인별로 잘라서 0.18s gap 으로 다시 이어붙임 → 잘린 부분의 잔향(reverb tail)이 끊겨 "뚝뚝" 끊어지는 음성. 사용자 피드백: "음성이 뚝뚝 끊어지는 느낌".

### 성공한 방식
`ffmpeg silencedetect=n=-38dB:d=0.22` 로 묵음 구간만 검출 → `max_sil` 초과분만 트림 → 음성 신호는 절대 건드리지 않음. 발화 prosody 100% 보존.

```python
for (sst, sen) in silences:
    if (sen - sst) <= max_sil:
        continue  # 짧은 호흡은 그대로
    plan.append({'kind':'audio','a':cursor,'b':sst})
    plan.append({'kind':'silence','a':sst,'b':sen,'new_dur':max_sil})
    cursor = sen
```

`max_sil=0.18` 이 너무 공격적이면 0.25 / 0.30 으로 완화. -38dB threshold 는 Adam 보이스 기준 안정적.

## 39. ffmpeg input seek 함정 — afade 가 절대 타임스탬프로 동작 (2026-04-30, 루비알엔)

### 증상 (디버깅에 1시간 소비)
silence_compress 결과 mp3 에서 **첫 세그먼트만 정상**, 나머지 세그먼트 23개 모두 `-91dB` 묵음. 라인 1만 들리고 라인 2~24가 통째로 사라짐. 자막은 정상이라 사용자가 "어떻게 하고 계세요 음성 안 나옴" 으로 인지.

### 원인
세그먼트 추출 명령:
```bash
ffmpeg -i in.mp3 -ss 2.419 -to 3.857 -af "afade=t=out:st=1.430:d=0.008" out.wav
```
`-ss/-to` 가 `-i` **뒤**에 있어도 input seek 로 동작하지만, **타임스탬프는 입력 절대값을 유지**. afade 필터가 보는 시간은 0이 아닌 2.419s 부터. `st=1.430` 은 입력 t=1.430s 의미 → 추출 구간(2.419~3.857) 내내 fade-out 발동 → 묵음 출력. 첫 세그먼트만 a=0 이라 우연히 작동.

### 해결 (둘 중 하나)
1. `-ss/-to` 를 `-i` **앞**으로 이동 → seek 후 타임스탬프 0 부터.
2. 또는 `asetpts=PTS-STARTPTS` 필터 추가해서 명시적 리셋.

```python
subprocess.run(['ffmpeg','-y',
    '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', in_mp3,    # ← input 앞
    '-af', 'asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005,'
           f'afade=t=out:st={(b-a)-0.008:.3f}:d=0.008',
    '-c:a','pcm_s16le','-ar','44100','-ac','2', out_wav],
    check=True)
```

### 검증 패턴
세그먼트 추출 직후 `ffmpeg -i seg.wav -af volumedetect -f null -` 로 mean_volume 확인. -91dB 면 무조건 추출 명령 의심. 또는 `silencedetect -n -50dB -d 0.05` 로 전 구간 묵음인지 체크.

## 40. atempo + cue scale 동시 적용 — 영상 페이스 가속 (2026-04-30, 루비알엔)

자막/TTS 가 늘어진다는 피드백 시 (사용자: "자막 속도감이 너무 늦어서 10% 빠르게"):
```python
SPEED = 1.10
subprocess.run(['ffmpeg','-i', tts_mp3,
                '-filter:a', f'atempo={SPEED:.3f}',
                '-c:a','libmp3lame','-b:a','192k', tts_fast],
               check=True)
for c in cues:
    c['start'] /= SPEED
    c['end']   /= SPEED
```
음성과 자막 동기화 유지하면서 전체 페이스만 압축. atempo 0.5~2.0 범위 무손실, 그 이상은 체이닝(`atempo=1.5,atempo=1.5` = 2.25). §35.3 의 라인별 차등 atempo 와 보완 관계.

**핵심: mp3 만 atempo 하고 cue 시간은 그대로 두면 자막 어긋남.** 반드시 동시 적용.

## 41. AE .aep 자동 빌드 — Adobe 는 Python API 가 없다 (2026-04-30, 루비알엔)

### 표준 방식
1. `win32com.client.Dispatch('AfterFX.Application').DoScript(jsx_text)` — COM 등록 안 되어 있으면 실패 빈도 높음. AE 26 에서 빈번히 `-2147221005 잘못된 클래스 문자열` 발생.
2. 폴백: `subprocess.Popen([AfterFX.exe, '-r', jsx_path])` — AE 실행 + ExtendScript 자동 실행 + 완료 시 alert dialog. Python 측은 .aep 파일 생성 폴링.

### 버전 지정 (AE 25 = 2025, AE 26 = 2026)
설치된 AE 바이너리 경로 우선순위로 제어:
```python
AE_EXES = [
    r'C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe',
    r'C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe',
]
exe = next(p for p in AE_EXES if os.path.exists(p))
```
.aep 는 forward-incompatible. 25.0 으로 저장하려면 25.0 바이너리로 실행 필수. ExtendScript 의 `app.project.save()` 는 현재 실행 중인 AE 버전 포맷으로만 저장.

### Font 호환
PostScript 이름 (공백 제거) 사용: `Pretendard-Bold`, `NotoSansKR-Black`. AE 가 못 찾으면 "유효하지 않은 문자가 포함되어 있습니다" 에러. setFontSafe(td, candidates) 헬퍼로 fallback 처리:
```js
function setFontSafe(td, candidates, layerName) {
  for (var i=0; i<candidates.length; i++) {
    try { td.font = candidates[i]; return true; } catch(e) {}
  }
  return false;
}
```

### sourceRectAtTime 자동 fit
긴 자막(예: "누렇게 뜬 얼굴" 158pt) 이 화면 폭 1080 넘으면 잘림. width 측정 후 fontSize 동적 축소:
```js
var fitR = TAG.sourceRectAtTime(cs+0.01, false);
if (fitR.width > 980) {
  var newSize = Math.floor(SIZE * 980 / fitR.width);
  td.fontSize = newSize;  // 158 → 122
}
```

### Comp 길이 안전망
`comp.duration = total + 1/FPS` 로 1프레임 여유. workAreaDuration 은 try/catch (out-of-range 에러 빈번).

## 42. .aep 패키징 — 절대경로 import 회피 (2026-04-30, 루비알엔)

### 문제
.aep 는 import 자산 경로를 **절대경로로 베이킹**. 다른 PC 로 .aep 만 보내면 "missing media" 폭탄. 자산을 다른 폴더로 옮겨도 마찬가지.

### 해결: 환경변수로 빌드 경로 강제 + 미리 자산 복사
```bash
AEP_CUTS_DIR="C:/.../pkg/cuts" \
AEP_AUDIO_PATH="C:/.../pkg/audio/full.mp3" \
AEP_OUT_DIR="C:/.../pkg/final" \
python build_aep.py
```
build_aep.py 내부:
```python
cuts_dir   = os.environ.get('AEP_CUTS_DIR', WORK)
audio_path = os.environ.get('AEP_AUDIO_PATH', default_audio)
out_dir    = os.environ.get('AEP_OUT_DIR', FINAL)
```

### 패키지 폴더 구조 (배포 단위)
```
rubiv_v2_revised_pkg/
├ cuts/    cut_00.mp4 ~ cut_23.mp4    (24개 컷)
├ audio/   full_v2_revised.mp3        (TTS+압축본)
│          full_v2_revised_raw.mp3    (원본)
│          sfx_track.mp3
└ final/   rubiv_v2_revised.aep       (← 이 폴더 기준 절대경로 import)
           rubiv_v2_revised.jsx       (재실행용)
           rubiv_v2_revised.mp4       (완성본)
           subs.ass, cues.json, script.json, _ae_build.log
```
.aep 가 그 폴더 내부 경로로만 import 하므로 폴더째 다른 PC 로 이동해도 그대로 열림. 단, 받는 쪽도 동일한 절대경로(`C:\Users\...\rubiv_v2_revised_pkg\`)에 두어야 함. 더 견고한 방법은 AE 의 "Collect Files" 또는 .aepx 텍스트 포맷 후처리.

- confidence: high
- source: 2026-04-30 루비알엔 v2 24컷 빌드 (49.7s 영상, AE 25.0 .aep 자동화, 패키지 64.5MB)

---

*확장: 2026-04-30 루비알엔 24컷 v2 빌드 — 컷·자막·TTS·페이스·AE·패키징 7대 보완 교훈 (§36-42).*

---

## 36. B&A(Before/After) 타이밍 — 감정 곡선 위에 컷을 얹기 (2026-04-30)

> v09에서 일차 진행(Day1→3→5→7)이 그냥 정보 나열처럼 흘러가는 문제. B&A는 **공감 → 충격 → 안도 → 환희**의 감정 곡선이고, 컷 길이가 그 곡선을 따라야 한다.

### 36.1 B&A 4단계 감정 곡선
```
Before (공감/고통)    → 길게 머물기 (인지·체화 시간)
Trigger (제품/변화)   → 빠르게 (충격·전환 임팩트)
Progress (일차 진행)  → 점진적 가속 (희망 누적)
After (환희/광채)     → 다시 길게 (체감·소비)
```

### 36.2 길이 분배 원칙 (21초 광고 기준)
| 단계 | 권장 길이 | 비율 | 이유 |
|------|-----------|------|------|
| Before (고통/문제) | 2.5~3.5s | 15-17% | 시청자가 자기 얼굴 떠올릴 시간 필요 |
| Trigger (제품 등장) | 1.5~2.0s | 8-10% | 충격 한 번. 너무 길면 임팩트 죽음 |
| Day1 | 0.6~0.8s | 3-4% | 변화 미미 — 짧게 |
| Day3 | 1.0~1.3s | 5-7% | 변화 보이기 시작 — 살짝 늘림 |
| Day5 | 1.2~1.5s | 6-8% | 확연한 변화 — 더 늘림 |
| Day7 (광채) | 1.5~2.0s | 8-10% | 절정 — 임팩트 강하게 |
| After/스탯 | 2.0~2.5s | 10-12% | 숫자 인지 + 환희 체감 |
| CTA | 2.5~3.0s | 12-14% | 가격 + 행동 유도 |

**리듬 키포인트:**
- Day1 < Day3 < Day5 < Day7 — **점진적 가속**(점점 길어짐). 균일하면 지루.
- Before > Trigger — Before 길게, Trigger 짧고 강하게.
- After > Day7 — 절정 후 음미 시간.

### 36.3 v09 실측 — 어디서 리듬 깨졌나
| 씬 | 길이 | 원래 의도 | 실제 효과 | 진단 |
|----|------|-----------|-----------|------|
| S04 후기 (Before) | 1.78s | 공감 | 너무 짧음 | ❌ 2.5s+ 필요 |
| S05 30→1 (Trigger) | 2.09s | 충격 | 적절 | ✅ |
| S06 Day1 | 0.74s | 시작 | 적절 | ✅ |
| S07 Day3 | 1.55s | 변화 | 적절 | ✅ |
| S08 Day5 | 1.24s | 확연 | **Day3보다 짧음** | ❌ Day3 < Day5 가속 깨짐 |
| S09 Day7 (광채) | 1.60s | 절정 | 약함 | ❌ 1.8-2.0s 필요 |
| S10 +166% (After) | 2.19s | 환희 | 적절 | ✅ |
| S13 CTA | 1.30s | 마무리 | 너무 짧음 | ❌ 2.5s+ 필요 |

**문제 패턴:** Day5(1.24) < Day3(1.55) — 가속이 거꾸로. Day7(1.60)이 Day5와 비슷 — 절정 못 살림.

### 36.4 B&A 점진적 가속 공식
일차 진행 N개 컷의 길이를 다음 공식으로:
```
dur(i) = base × (1 + 0.25 × i)    # base=0.6s
Day1=0.60, Day3=0.75, Day5=0.90, Day7=1.05  ← 가속 (× 0.25)
```
또는 절정에 임팩트 더 주려면:
```
Day1=0.6, Day3=0.9, Day5=1.2, Day7=1.8  ← 절정 1.5배 점프
```
**원칙: 절정(Day7/After)에서 길이 점프**. 균일 1.0s씩 4컷 = 정보 나열, 임팩트 0.

### 36.5 Trigger(전환점) 컷의 마법 — 0.5초 룰
- "제품 등장"이나 "morph 변화" 같은 전환점은 **풀 길이의 첫 0.5초가 절대적**.
- 0~0.3s: 큰 임팩트 시각요소 (제품 줌인 / 빛 폭발 / 30개→1개 모핑 시작)
- 0.3~0.5s: 전환 텍스트 한 단어 (`"단" 1병으로!"`)
- 이후: 정보 소비 시간

전환점 컷은 **워드팝 자막 시작도 동시에**. 보이스보다 먼저 비주얼이 터져야 시청자 시선 잡힘.

### 36.6 After(환희) 컷의 호흡
- 광채/완성 컷은 **줌인 + 펄스**로 시각적 호흡 만듦.
- Day7 광채 = `zoom 0.96 → 1.02` (느린 줌인) + 후광 `pulse 0.95 → 1.05` (호흡감).
- 정적 이미지면 시청자 1초만에 스킵. 미세 모션이 시선 잡아둠.

### 36.7 CTA 컷의 길이 — 절대 짧게 X
- "단돈 19,800원!" 같은 가격 CTA 1.3초 → **읽기도 전에 끝남**.
- 최소 2.5초. 권장 3.0초.
  - 0~0.5s: 가격 등장 (워드팝)
  - 0.5~1.5s: 가격 인지 + 긴급성 텍스트 ("오늘만!")
  - 1.5~2.5s: 행동 유도 ("👉 지금 구매")
  - 2.5~3.0s: 머무는 시간 (시청자 결정)

### 36.8 음향과 컷 매칭
- Before/문제 라인 → **낮은 톤 / 조용한 BGM** (atempo 1.00, 천천히)
- Trigger 라인 → **임팩트 사운드 (whoosh/sparkle)** + atempo 1.00 (충격 살리려면 천천히)
- Day1~7 라인 → **BGM 점진 빌드업** (atempo 점진 가속 1.10→1.18)
- After 라인 → **밝은 톤** (atempo 1.07~1.20, 환희감)
- CTA → **BGM hit + 종소리** (atempo 1.00, 또박또박)

atempo 매트릭스도 감정 곡선에 맞춰야 함. 균일하게 빠르게 X. **Trigger와 CTA만 atempo 1.00 보호**.

### 36.9 B&A 표현 안티패턴 ❌
1. **Before 0.5초** — 공감 시간 부족. 시청자가 "뭔 얘기야" 하고 스킵.
2. **모든 일차 균일 1초** — 정보 나열. 가속 못 만듦.
3. **Trigger 3초+** — 임팩트 죽음. 한 번에 빠르게 폭발해야.
4. **After 1초** — 절정 음미 시간 없음. 환희 못 느낌.
5. **CTA 1.5초** — 못 읽음. 구매 결정 시간 없음.
6. **모든 컷 atempo 1.20** — 보이스 가쁨. 임팩트 라인까지 빨라져 죽음.
7. **자막 일정한 폰트 크기** — Day7 광채 = 같은 사이즈면 절정감 0. 절정만 1.3배 키워야.

### 36.10 핵심 정리 — B&A 타이밍 7대 규칙
1. **Before > Trigger** — Before 길게(2.5s+), Trigger 짧고 강하게(1.5-2.0s).
2. **Day1 < Day3 < Day5 < Day7** — 점진적 가속. 절정에서 1.5배 점프.
3. **After 길게** — 환희 음미 시간 2.0s+.
4. **Trigger 첫 0.5초가 절대적** — 큰 비주얼 + 워드팝 동시 폭발.
5. **CTA는 2.5s+** — 가격 인지 + 행동 결정 시간 필수.
6. **atempo도 감정 곡선 따라 차등** — Trigger·CTA만 1.00 보호.
7. **자막 폰트 크기도 곡선** — 절정(Day7/CTA) = 1.3배 키워 시각 임팩트.

- confidence: high
- source: 2026-04-30 v09 회고 — Day5(1.24s) < Day3(1.55s) 가속 깨짐 / Day7 광채 1.60s 절정 약함 / CTA 1.30s 너무 짧음 진단

---

## 43. 레퍼런스 영상 분석 → 재구성 파이프라인 (2026-04-30, 루비알엔 v3 해골 변신)

기존 광고를 자기 제품으로 재구성할 때 표준 분석 흐름.

### 43.1 영상 → 분석 가능 자산 분해
```bash
# 1) 프레임 100장 (2fps) — Gemini Vision 입력용
ffmpeg -i ref.mp4 -vf "fps=2,scale=540:960" -qscale:v 3 frames/f_%03d.jpg
# 2) 오디오 (16kHz mono) — STT 용
ffmpeg -i ref.mp4 -vn -ac 1 -ar 16000 -b:a 128k audio.mp3
# 3) scene cut 자동 감지
ffmpeg -i ref.mp4 -filter:v "select='gt(scene,0.30)',showinfo" -f null - 2>&1 | grep pts_time
```
50초 영상 → 100장 프레임(~5MB) + 1MB 오디오 + 13개 cut 타임스탬프. 각 산출물 모두 5MB 이하라 Gemini 첨부 안전.

### 43.2 멀티 LLM 협업 분담
- **Gemini Vision** (`gemini -p` 또는 Python SDK): 씬별 비주얼/자막/모션 분석. 영상 직접 첨부.
- **Codex (gpt-5.5 high)**: 분석 결과 → 새 제품 USP에 맞춘 서사 재구성·카피 작성. Codex 한도 걸리면 Gemini 로 fallback.

### 43.3 산출물 표준
- `transcript.json` — 더빙 전사 (start/end/text/tone/breath_after)
- `scenes_breakdown.json` — N개 씬별 분석
- `sync_table.md` — 자막↔더빙 동기화 표
- `patterns.md` — 컷·색감·음악 패턴
- `기획서_full.md` (300줄 이하) + `plan/00_hub.md` 인덱스 + `01_story.md` ~ `08_build.md` (각 100줄 이하 hub-and-spoke 패턴)

## 44. 캐릭터 일관성 — 2단계 마스터 시트 전략 (2026-04-30, 루비알엔 v3)

캐릭터(해골/마스코트) 가 여러 컷에 등장할 때 일관성 확보 표준.

### 44.1 Stage A — 마스터 시트 1회 생성
ACT 1 상태(예: 누런 해골) + ACT 3 상태(핑크 광채 해골) 마스터 1장씩 먼저 만들고 사용자 컨펌.
```bash
node scripts/generate.mjs "<full visual prompt for yellow master>"
# → out/yellow_master.png
```

### 44.2 Stage B — 모든 씬을 마스터 reference 로 생성
god-tibo-imagen 의 edit 기능 사용. 단 원본 `edit.mjs` 는 **로컬 파일 절대경로를 그대로 보내서 400 에러** ("Invalid 'image_url'. Expected a valid URL").

**해결: data:URL base64 변환 패치본 `edit_b64.mjs`:**
```js
const buf = await readFile(inputAbs);
const dataUrl = `data:image/${mime};base64,${buf.toString('base64')}`;
await provider.generateImage({ prompt, model, images: [dataUrl], outputPath });
```
이러면 ChatGPT Codex 백엔드가 reference 를 정상 인식.

### 44.3 Multi-image edit (캐릭터 + 제품 합성)
S14 같이 "캐릭터가 제품을 들고 있는" 컷은 reference 2장 동시. `edit_multi.mjs`:
```js
const dataUrls = refs.map(r => `data:image/${mime};base64,${b64}`);
provider.generateImage({ prompt, model, images: dataUrls, outputPath });
```
호출: `node edit_multi.mjs <out> "프롬프트" <pink_master.png> <pd1.png>`

### 44.4 In-place 후보정 (덮어쓰기 edit)
1차 결과 텍스처가 매끈하면 같은 이미지를 reference + 새 프롬프트로 호출하면 그 자리에 덮어씀.
효과적인 키워드:
- yellow 거친: `얼룩덜룩 mottled blotchy uneven yellow patches with darker brown spots, NOT plastic smooth`
- pink 자연: `dewy pearlescent rose-pink mottling, natural sheen, real luminous skin texture, NOT plastic-smooth glossy white`

### 44.5 캐릭터 무관 컷 분류
모든 컷 캐릭터 일관성 강제할 필요 없음. 별도 fresh 생성:
- 인포그래픽 (PDRN 진피)
- 스마트폰 mockup (리뷰)
- 도장 (환불 보장)
- 마크로 손바닥 (앰플)
→ generate.mjs 로 fresh, reference 불필요.

## 45. 실제 제품 사진 reference 필수 (2026-04-30, 루비알엔 v3)

### 증상
"RubyRN ampoule cleanser bottle (frosted magenta-pink glass...)" 식으로 자연어로만 설명하면 GPT 가 임의의 화장품 병을 그림. 사용자: **"루비알엔 제품이 아님"**.

### 해결
실제 제품 누끼 사진 (`pd/pd1.png`) 을 reference 로 첨부 + "Use this exact RubyRN bottle (red-pink liquid, white label 'x melable' logo, 'RubyRN Ampoule Cleanser' text, 'PDRN+Vitamin C / Glutathione+Niacinamide' subtext, 150ml)" 프롬프트.

### 적용 컷
- 제품 hero (S04)
- 손바닥에 짜는 컷 (S05) — 제품 부분 노출 필요
- 캐릭터가 제품 들고 있는 컷 (S14) — multi-image (캐릭터 마스터 + 제품)

### 검증 패턴
1차 생성 후 결과 mp4/png 직접 보면서 "라벨 텍스트 = 실제 제품과 일치하는지" 확인. 다르면 즉시 재생성.

## 46. GPT-5.5 image gen 은 한국어 텍스트 정확히 그림 (2026-04-30)

기존 §14 ("Gemini는 한국어 텍스트를 이미지에 못 그림") 의 예외 케이스. GPT-5.5 (god-tibo-imagen 백엔드) 는 한국어 도장/타이포 한 번에 정확히 생성.

### 검증 케이스
프롬프트: `한국어 도장 이미지: 마젠타 핑크 색상의 둥근 도장, 도장 안에 굵은 한국어 글씨로 '30일 환불 보장' 명확하고 정확하게 렌더링`
→ 1번 생성에 한글 정확, 잉크 튐 효과 자연. ([[wiki/sources/src-rubiv-v3-skull-2026-04-30]])

### 룰
- Gemini imagen → 영문 강제 (§14 그대로 유효)
- GPT-5.5 (god-tibo-imagen) → 한국어 OK, 단 프롬프트도 한국어로 명확히
- 두 백엔드 모두 동시에 갖고 있으면 텍스트 들어가는 컷은 GPT-5.5 로 보낼 것

## 47. 리듬감 — SPEED + MAX_SIL 조합 표 (2026-04-30, 루비알엔 v3)

§35.3 라인별 차등 atempo 의 단순화 버전. 균등 페이스가 필요할 때.

### 검증 매트릭스 (16컷 30s 기준)

| 페이스 의도 | SPEED | MAX_SIL | 결과 |
|------------|-------|---------|------|
| 너무 빠름 (앞부분 루즈, 뒷부분 가속) | 1.05 | 0.20 | 26.8s, ACT 3 1.5s/컷 (헐떡) |
| **균등 자연 페이스** ✅ | 1.00 | 0.35 | 29.6s, ACT 3 2.0s/컷 (인지 가능) |
| 여유로운 페이스 | 0.95 | 0.45 | 35s+, 광고 길이 초과 우려 |

### 검증된 컷 길이 분포 (균등 페이스)
- ACT 0/1 (HOOK/PAIN): 0.9~2.0s
- ACT 2 mid (TRANSFORM): 2.0~2.85s
- ACT 3 PROOF: 1.85~2.10s
- CTA: 1.5s

### 사용자 신호 → 조정 방향
- "앞은 느린데 뒤가 갑자기 빠름" → SPEED 낮추고 MAX_SIL 높임
- "전체적으로 늘어짐" → SPEED 1.05~1.10
- "긴급함이 필요" → SPEED 1.05 + 라인별 차등 (§35.3)

## 48. 후편집 효과 (post_fx) — 줌·페이드·플래시 (2026-04-30, 루비알엔 v3)

빌드 완료 mp4 에 **컷별** 시네마틱 효과 추가 후처리 스크립트 패턴.

### 48.1 줌 (시간 가변 스케일 + 센터 크롭)
```python
zexpr = f'{s_start}+({s_end}-{s_start})*t/{dur:.3f}'
vf = (
  f"scale=w='{W}*({zexpr})':h='{H}*({zexpr})':eval=frame,"
  f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,setsar=1"
)
```
- 줌인: `s_start=1.0, s_end=1.06`
- 줌아웃 settle: `s_start=1.05, s_end=1.0`
- 강도 1.04~1.10 권장 (그 이상이면 화질 손상 시각적으로 보임)

### 48.2 페이드
```
fade=t=in:st=0:d=0.3
fade=t=out:st={DUR-0.4}:d=0.4
```

### 48.3 셔터 플래시 (셀카·카메라 컷)
```
eq=brightness='if(between(t,0.38,0.44),0.6,0)'
```
0.06s 짧은 brightness 펄스로 카메라 플래시 모방.

### 48.4 매핑 룰 (검증된 패턴)
| 역할 | 효과 |
|------|------|
| HOOK / PAIN / PROOF (감정 강조) | 줌인 1.04~1.10 |
| 제품 등장 / CTA | 줌아웃 settle 1.05→1.0 |
| 거품 reveal / TRANSFORM 시작 | 줌아웃 1.08→1.0 |
| REVEAL (광채 등장) | 줌인 1.0→1.10 + 페이드인 0.15s |
| 마지막 CTA | 줌아웃 + 페이드아웃 0.4s |
| 인포그래픽 / 마크로 / stamp | 정적 (효과 없음) |
| 셀카 / 카메라 컷 | 플래시 추가 |

### 48.5 워크플로 분리
- 1단계: build_video_v2.py 로 컷별 mp4 (효과 없음) + audio + subs 생성
- 2단계: post_fx_*.py 로 cut_NN.mp4 → cut_fx_NN.mp4 (효과 적용) → concat → audio mux + subs burn → final_fx.mp4

이렇게 분리하면 효과만 다르게 여러 버전 (A/B 테스트) 빠르게 만들 수 있음.

## 49. 패키지 폴더 구조 — seeds 까지 보관 (2026-04-30, 루비알엔 v3)

§42 (.aep 패키징) 확장. 후속 재생성·바리에이션 작업 위해 시드 PNG 도 패키지에 보관.

### 표준 구조
```
Desktop/rubiv_v3_skull_pkg/  (~110MB)
├ cuts/    16개 cut_NN.mp4 (각 1~3s, 컷 raw)
├ audio/   full.mp3 (TTS+silence_compress) + raw + sfx_track
├ final/   .aep (AE 25.0) + .jsx + 완성 mp4 (원본) + final_fx.mp4 (효과 적용)
│          + subs.ass + cues.json + script.json + _ae_build.log
└ seeds/   16 시드 PNG + 마스터 v1 (yellow/pink) + 마스터 v2 (mottled/dewy)
```

### seeds/ 보관 이유
- 시드 PNG 가 있으면 모션만 다시 (Kling i2v 만 재실행) 가능
- 마스터 v1/v2 가 있으면 캐릭터 추가 컷 (예: 광고 시리즈 2탄) 일관성 유지
- 비용: PNG 16~20장 ~30MB. 이 정도 늘어도 OK.

### 작업 모드
1. 신규 변형 만들 때: `seeds/` 의 마스터 reference + edit_b64.mjs 로 새 컷 생성
2. 모션만 다시: `seeds/SXX.png` → `gen_motion_v3.py` (Kling i2v) → 새 mp4
3. 효과만 다시: `cuts/cut_NN.mp4` → `post_fx_*.py` 로 새 후처리

- confidence: high
- source: 2026-04-30 루비알엔 v3 해골 변신 광고 빌드 (29.6s 16컷, AE 25.0, 패키지 110MB)


## §39 — 시드 캐릭터 일관성 파이프라인 (slime_v03 메이플 슬라임)

광고 영상 캐릭터(슬라임/마스코트)를 GPT 이미지 + Kling i2v 파이프라인으로 일관성 유지하면서 12씬 생성하는 워크플로우.

### 4단계 파이프라인
1. **시드 캐릭터 1장** (codex/ggttt + gpt-5.4)
   - 프롬프트에 "MapleStory chibi humanoid proportions" + "Haribo gummy 일체형" 명시
   - 곰귀/안테나/볼터치/흰얼굴 명시적 제외 (negative)
   - 9:16 portrait, 흰 배경

2. **12씬 정적 이미지** (`edit_b64.mjs` 또는 `edit_multi.mjs`)
   - 브랜드 제품 등장 씬은 무조건 `edit_multi.mjs` (시드+제품 ref) → §37
   - 그 외 씬은 `edit_b64.mjs` (시드 1장 ref)
   - 각 씬마다 배경/감정/포즈/입자/조명 텍스트로 다양화

3. **Kling i2v 5초 클립 12개** (fal.ai)
   - 엔드포인트: `fal-ai/kling-video/v2.6/master` → fallback `v2.5-turbo/pro`
   - aspect_ratio="9:16", duration="5", cfg_scale=0.5
   - 모션 prompt에 브랜드명 포함 시 content policy 거부 → 색/형태로 우회

4. **편집 합성**
   - Kling 5초 클립 → TTS 길이만큼 trim (`-t {dur}`)
   - DAY 라벨 / CTA 박스 / 자막 burn (ASS subtitles, MarginV ≈ 280으로 하단 배치)
   - 12 segs concat → silent.mp4 → audio mix (alimiter limit=0.95) → final

### 일관성 유지 핵심
- **시드 PNG는 절대 재생성 X** — 한 번 만들고 모든 씬에 동일 ref로 사용
- **각 씬 prompt 시작에 "Keep EXACT same character from reference"** 강조
- 캐릭터 디테일(코랄 톤, 통짜 젤리, 큰 애니눈, 메이플 비율)을 매 prompt에 반복

### 비용 (12씬 광고 1편)
- 코덱스 13장 (시드 1 + 씬 12) ≈ 무료 (ChatGPT 세션)
- Kling i2v 12 × $0.49 ≈ $5.9
- 총 ~$6 / 30분 작업

### 결과물 폴더링 (바탕화면)
```
slime_v03_handoff/         ⭐ 메인 (AE + Footage + Final mp4)
slime_v03_seed/            시드 PNG + prompt.txt
slime_v03_scenes/          12 정적 AI 씬 PNG
slime_v03_clips_kling/     Kling 5초 클립 원본
slime_v03_handoff_static/  정적 zoom-only 백업
slime_v03/                 소스 프로젝트
```

- confidence: high
- source: 2026-04-30 slime_v03 광고 영상 (22.2s, 12씬, 메이플 슬라임 캐릭터, 멜라블 RubyRN 클렌저)


## §40 — Kling i2v content policy 회피 (브랜드명 + 부정 키워드)

Kling i2v는 input 이미지에 브랜드 라벨이 보여도 OK이지만, **prompt 텍스트**에 브랜드명/특정 단어 들어가면 content policy 거부.

### 거부 트리거 (실측)
- 브랜드명: "melable", "RubyRN" (직접 명시 시 거부)
- 특정 부정 키워드: "deformed face", "extra limbs" 등 일부 negative_prompt 단어가 strict 거부 (모델 버전마다 다름)

### 우회 패턴
```python
# 거부 (✗)
prompt = "The melable RubyRN cleanser bottle gently rotates..."

# 통과 (✓)
prompt = "The pink cleanser bottle with white label gently rotates..."
```

### Negative prompt 안전 키워드
- ✅ "deformed face, multiple characters, low quality"
- ⚠️ "extra limbs, missing fingers" — 일부 모델에서 거부

### 권장 워크플로우
1. 정적 이미지(코덱스 GPT) prompt에는 브랜드명 명시 OK
2. Kling i2v 모션 prompt에는 색/형태로만 표현 ("pink bottle", "round container")
3. 거부 발생 시 prompt 단순화 + negative_prompt 축약 (deformed face, low quality 정도만)

- confidence: high
- source: 2026-04-30 slime_v03 S05/S07 Kling 1차 거부 → 브랜드명 빼고 재시도 성공


## §41 — Seedance 2.0 / Veo3 / Sora2 보이스 일관성 (다중 컷 시나리오)

**문제**: i2v 모델로 5초씩 여러 컷을 뽑을 때 동일 화자 보이스 유지 불가.

### 현재(2026-05) 업계 공통 한계
Seedance 2.0의 audio param은 `generate_audio: bool` 하나뿐. Veo3, Sora2도 동일.
- ❌ `voice_id`, `voice_reference`, `speaker_seed` — 모두 미지원
- 같은 프롬프트 두 번 호출 → 다른 사람 목소리 (랜덤 화자)
- 프롬프트에 "30대 차분한 남성" 명시해도 카테고리만 맞을 뿐 음색·억양·발음 습관은 매번 다름 (30~50% 일관성)

### 해결책 4지선다 + 권장도

| 방법 | 일관성 | 자연스러움 | 한계 | 권장 |
|---|---|---|---|---|
| A. 한 generation에 15초 다 담기 (natural cuts) | 100% | ★★★★★ | 15초 천장, 시작 이미지 1장 고정 | 단발성 ≤15s |
| B. Lip-sync 후처리 (sync-labs/veed/latentsync) | 95% (영) / 80~90% (한) | ★★★ | 입 픽셀 재합성, 양순음 P/B/M 어색, 측면샷 X | 원본 음성 자체가 없을 때만 |
| **C. Voice Conversion 후처리 (RVC/ElevenLabs Voice Changer)** | **95~100%** | **★★★★★** | 원본 톤·감정·속도가 그대로 이식됨 | **★ 1순위** |
| D. 영상 무음 + TTS 풀 합성 + lip-sync | 100% | ★★★ | 입모양·감정 모두 어색 가능 | 시리즈 캐릭터 풀 양산 |

### Voice Conversion이 베스트인 이유
입모양을 손대지 않고 음성만 바꿈 → 영상 변형 0, 자연스러움 최상.
원본 영상의 호흡·타이밍·감정 모두 보존.

### 권장 워크플로 (방법 C)
```
[1] Seedance 2.0 i2v (generate_audio=true 그대로 둠)
       ↓ 영상 + 랜덤 보이스
[2] ffmpeg로 음성만 추출 (.wav)
       ↓
[3] RVC / ElevenLabs Voice Changer 로 동일 target voice 변환
       ↓ 일관 보이스 음성
[4] ffmpeg로 영상에 새 오디오 합치기 (-c:v copy → 영상 손실 0)
       ↓ 최종
```

### 도구 우선순위 (한국어 기준)
1. **ElevenLabs Voice Changer** — 상용 1티어, voice_id 라이브러리 영구 재사용. ~$0.05/컷
2. **RVC (Retrieval-based VC)** — 오픈소스, 로컬 GPU 무료. Huggingface에 한국어 voice 모델 다수
3. Seed-VC — 30초 reference로 zero-shot
4. OpenVoice v2 — MIT 라이선스, 무료 상업용
5. fal-ai/playht/voice-conversion — API 통합형

### 비용 (30초 광고 = 5초×6컷)
| 방법 | Seedance | TTS/VC | Lip-sync | 합계 |
|---|---|---|---|---|
| A. 한 방 15s | $0.6 | - | - | $0.6 (15s 한정) |
| B. Lip-sync | $1.2 | $0.1 | $0.9~1.5 | $2.2~2.8 |
| **C. Voice Conversion (ElevenLabs)** | $1.2 | $0.30 | - | **$1.5** |
| C-무료 (RVC 로컬) | $1.2 | $0 | - | **$1.2** |

### 의사결정 트리
```
영상 ≤ 15초 + 단발성?
  YES → A (한 방 15s)
  NO ↓
원본 영상 톤·감정 살리고 싶음?
  YES → C (Voice Conversion) ★
  NO  → B (Lip-sync)
```

### Seedance 프롬프트 팁 (방법 C 전제)
- 정면샷: `front-facing, mouth clearly visible, looking at camera`
- 톤 지정: `calm tone` / `energetic` (방법 C에서 톤이 그대로 이식되므로 이 단계가 결정적)
- 클로즈업 회피: 상반신샷 위주가 자막·후처리 모두 자연스러움

- confidence: high
- source: 2026-05-02 fal.ai Seedance 2.0 image-to-video 모델 페이지 직접 확인 + 광고 영상 합성 실측


## §42 — 광고 영상 후처리 합성 표준 (원본 음성 + ASS 자막 + 16:9)

**언제 적용**: 두 개 이상의 i2v 결과물(또는 같은 화자 컷들)을 합쳐 광고/릴스로 만들 때.

### 절대 규칙 4개

1. **원본 음성을 우선 시도** — TTS 합성은 마지막 수단. 한국어 무료 TTS(edge-tts SunHi/JiMin 등)는 광고 톤에서 기계음 명확. 원본이 있고 화자가 같으면 원본 그대로가 자연스러움 100%.

2. **freeze 화면 금지** — TTS가 영상보다 길어서 마지막 프레임 `tpad=stop_mode=clone`으로 패딩하면 광고로서 치명적 어색. TTS 길이를 영상에 맞춰 줄이거나, 영상을 다시 뽑거나, 그냥 원본 음성을 써라.

3. **자막 timestamp는 STT word-level에서** — TTS 음성의 word boundary를 신뢰하지 마라. edge-tts ko-KR voice는 WordBoundary 이벤트 자체를 안 내보낸다. 대신 faster-whisper로 음성을 STT 돌려 word timestamp를 받아라 (TTS 음성도 깨끗해서 STT 품질 매우 좋음). 다만 원본 음성이 있으면 그걸로 STT가 베스트.

4. **ASS 자막은 phrase 단위로 청크 묶기** — 단어 1개씩 휙휙 바꾸면 못 읽는다. 1.0~1.8초 / 18자 이내로 phrase 묶어서 fade in/out + pop-in 애니메이션.

### 검증된 ASS 스타일 (1920×1080, 한국어)
```
Style: Tok, Malgun Gothic, 88, &H00FFFFFF, &H000000FF, &H00000000, &H64000000, 1, 0, 0, 0, 100, 100, 0, 0, 1, 6, 3, 2, 80, 80, 200, 1
```
- 흰 글자 + 검정 outline 6px + shadow 3px → 어떤 배경에서도 가독성
- 하단 중앙 (MarginV=200)
- per-line override: `{\fad(80,80)\fscx85\fscy85\t(0,140,\fscx100\fscy100)}` (페이드 + pop-in)

### 청크 분할 알고리즘 (검증된 디폴트)
```python
MAX_CHUNK_SEC = 1.8
MAX_CHARS = 18
TAIL_PAD = 0.35   # 끝을 살짝 늘려 가독성 ↑ (다음 청크 시작 전까지만)
```
- 시간 또는 글자 수 둘 중 하나 초과하면 새 청크
- 청크 끝점을 +0.35초 늘리되 다음 청크 시작 −0.02초까지만

### ffmpeg 합성 단일 커맨드 (16:9 1080p)
```
ffmpeg -y -i src.mp4 \
  -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,\
                   pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,\
                   subtitles=clip.ass[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 24 \
  -c:a aac -b:a 192k \
  out.mp4
```
- `subtitles` 필터 path는 **상대경로** 권장 (윈도우 콜론 escape 함정 회피). cwd 로 work 폴더 이동 후 실행.
- `fontsdir` 옵션은 윈도우에서 `C:` 콜론 파싱 충돌 → 제거. 시스템 fontconfig가 Malgun Gothic 자동 인식.

### 컷별 합성 후 concat
```
ffmpeg -y -f concat -safe 0 -i list.txt -c copy final.mp4
```
- 컷별 mp4가 모두 동일 codec/해상도/fps이면 `-c copy`로 무손실 concat. 재인코딩 X.

### 스킵하면 망가지는 5가지
1. ❌ TTS 사용 → 기계음 광고
2. ❌ TTS 음성 STT로 timestamp 추정 → 자막 부정확
3. ❌ 영상보다 긴 TTS에 freeze 패딩 → 정지 화면 광고
4. ❌ 단어 1개씩 자막 → 못 읽음
5. ❌ `subtitles` 필터에 절대경로 + `fontsdir` 옵션 → 윈도우에서 파싱 에러

### 폴더 구조 표준 (재사용 패턴)
```
v_output/
├── final_16x9_v2.mp4
├── README.md
├── preview_v2_01~04.jpg
├── 원본음성_들어보세요/      ← 화자 비교 검수용
├── work/                    ← 중간 산출물
│   ├── clipNN_stt.json
│   ├── clipNN_v2.ass
│   └── clipNN_v2_final.mp4
└── scripts/
    ├── stt.py
    └── v2_compose.py        ← 자막+합성+concat 한 방
```

### 처리 시간 / 비용
- faster-whisper small int8 (CPU): 15초 영상 STT 약 5초
- ffmpeg 합성 + concat: 30초 영상당 약 10초
- 전체: 30초 광고 1편 ~2분 (모델 다운 제외), 비용 $0

- confidence: high
- source: 2026-05-02 bj/v 영상 2개 (루비아렌 광고 컷) 합성 작업. v1(TTS+freeze) 실패 → v2(원본음성+정확STT+freeze제거) 성공
- related: §3 자막 싱크의 진실, §41 Seedance 보이스 일관성

---

## §50 — 루비알엔 v6_hero 액션 광고 (2026-05-04) — 4대 함정과 처방

40초 목표 원펀맨 톤 액션 영웅 광고 (12컷, "루비알엔 맨" vs "얼룩 괴물" 진심펀치). 1차 빌드 후 사용자 피드백 4건이 동시에 떨어져 풀 재작업한 케이스. 다음 액션 광고에 그대로 통하는 처방 정리.

### A. ChatGPT 웹 자동화로 god-tibo-imagen 한도 우회 (네트워크 가로채기 패턴)

**상황:** S06/S07/S11 제품 컷 재생성 필요한데 god-tibo-imagen API 가 `usage_limit_reached` (prolite plan, 24h 후 리셋). 사용자: "GPT 이미지 크롬 플레이라이트로 해서 생성하면 됨, 크롬 창 띄우면 로그인해줄게."

**해결 — 영구 프로필 + 네트워크 가로채기 조합 (CDP 9222 안 씀):**

1. `playwright.chromium.launch_persistent_context()` 로 영구 프로필 (`pipeline/_chrome_profile/`) 사용. 사용자가 한 번만 로그인하면 이후 자동.
2. **시스템 Chrome 필수** — `channel='chrome'` 안 쓰면 번들 chromium 흰화면 멈춤. 자동화 감지 우회 인자 필수:
   ```python
   args=['--start-maximized', '--disable-blink-features=AutomationControlled']
   ignore_default_args=['--enable-automation']
   ```
3. **이미지 다운로드는 `page.on('response')` 네트워크 가로채기로만 가능.** 시도해서 실패한 방식:
   - DOM `<img>` 셀렉터 (alt 등): ChatGPT가 생성 이미지를 `<img>` 태그로 렌더하지 않음 (canvas / picture / blob form)
   - `/backend-api/conversation/{id}` API: `Conversation not found` 반환 (auth/format issue)
   - 사이드바 클릭/lightbox: pointer events intercepted 빈발
4. **ChatGPT 가 매 생성마다 캐릭터 시트 + 실제 장면 둘 다 만든다.** 캐릭터 시트는 항상 `4883567 bytes` 고정 사이즈 (4MB 이상)로 가장 크게 응답되므로 단순 "largest" 정렬은 무조건 캐릭터 시트를 가져옴. 필터링:
   - `CHARSHEET_SIZE = 4883567` 명시 제외
   - `< 2MB` 제외 (보통 ref 썸네일)
   - ref 파일 hash/size 제외 (hero, pd1)
   - 남은 것 중 가장 큰 것 = 실제 장면

5. **stop 버튼 사라짐 = 완료 신호:**
   ```python
   page.locator('button[data-testid="stop-button"], button[aria-label*="중지"]').count() == 0
   ```
   사라진 후 +8초 안정화 대기 필수 (이미지 src 동기화).

6. 프롬프트는 한국어로 강하게 명시: **"캐릭터 시트나 여러 패널 절대 안 됨. 오직 하나의 장면 일러스트만. 전체 화면을 가득 채우는 한 장의 큰 일러스트. 작은 패널 분할 금지. 텍스트/라벨/사이드바/도표 금지"** — 약하게 쓰면 무시당함.

검증: v6_hero S06/S07/S11 3컷 모두 melable RubyRN 라벨 정확히 보존하며 액션 포즈 생성 성공. 컷당 사이클 ~5분.

코드 위치: `pipeline/open_chatgpt.py` (세션 띄우기), `pipeline/gen_via_chatgpt.py` (생성+네트워크캡처), `pipeline/dl_via_network.py` (다운만).

→ 별도 페이지: [[tacit/chatgpt-web-automation]] 의 §6 으로 보강됨.

### B. build_video_v2 cut 캐시 함정 — 30분 디버깅 손실

`build_video_v2.py:292` 의 `make_cut_motion()` 첫 줄: `if os.path.exists(out): return out`. SCRIPT/SCENE/SPEED 변경 후 재빌드해도 옛날 `cut_XX.mp4` 그대로 사용됨.

**증상:** v6 SPEED 1.10 으로 빌드했는데 영상 길이가 옛날과 동일 (43.4s). cut_XX.mp4 timestamp 보니 4일 전. cue JSON 은 새로 생성됐는데 컷 mp4 만 캐시된 상태.

**처방 — 재빌드 시 반드시 삭제 (디렉토리 통째로 rm -rf 는 'Device or resource busy' 자주 남, 파일 단위로):**
```bash
cd pipeline/_work_v{N}_*/
rm -f cut_*.mp4 video_only.mp4 video_fx.mp4 sfx_track.mp3 \
      full_audio*.mp3 sil_seg_*.wav sil_concat.txt subs.ass concat.txt
rm -rf fx_cuts
cd ..
rm -f 03_audio/full_v{N}*.mp3 03_audio/_alignment_v{N}*.json 03_audio/cues_v{N}*.json
```

근본 fix: `make_cut_motion` 에 `cue['start']` + `cue['end']` 해시를 outname 에 박아두면 자동 무효화. 시간 없으면 매뉴얼 삭제 운영.

### C. TTS 늘어짐 진단 — SPEED 와 MAX_SIL 누가 범인?

사용자: "TTS가 너무 늘어지고 느림. 좀더 리듬감 있게."  
→ 진단: 문장 길이가 짧아서 패딩으로 늘어진 것인지, 음성 자체가 느린 것인지 cue JSON 으로 분리.

```python
# cue JSON 에서 컷별 ratio 계산
ratio = (cue['end'] - cue['start']) / (cue['raw_end'] - cue['raw_start'])
# ratio = 1.0 → 음성 그대로
# ratio > 1.2 → SPEED 가 너무 낮음 (atempo < 0.85)
# ratio ≈ 1.0 + sum(silence) > raw_dur → MAX_SIL 이 너무 큼
```

v6_hero 사례:
- 1차: SPEED=0.82 + MAX_SIL=0.85 → 43.4s (ratio 1.21+) → "늘어진다" 컴플레인
- 2차: SPEED=1.10 + MAX_SIL=0.30 → 21.5s → "너무 빠르다, 5%만 모션 잘 보이게"
- 3차: **SPEED=1.05 + MAX_SIL=0.30 → 23.5s → 사용자 OK** ("오 잘됐다")

**액션 광고 baseline = SPEED=1.05 + MAX_SIL=0.30** 으로 시작. 호흡 강조 컷 있으면 라인별 SPEED 차등 (§35.3).

문장이 짧아서 길이 부족하면 컷 추가 / BGM intro·outro 로 채울 것. SPEED 0.8 대로 떨어뜨려 강제 늘리면 무조건 "늘어진다" 컴플레인.

### D. 광고 QA — 빌드 전후 매번 검수해야 할 3가지

사용자 명시 피드백 (2026-05-04): "**제품 일관성, 한글이 영어/이상한 언어로 나오는거, TTS 늘어짐 — 절대로 안 되게.**"

| QA 항목 | 검수 방법 | 대표 실패 |
|---|---|---|
| 제품 누끼 = 실제 제품 | 빌드 후 제품 컷 sample frame → "melable", "RubyRN Ampoule Cleanser" 라벨 식별 가능? | v6 처음에 product_master 를 빨강 오라로 재해석한 것 들고 있었음 → "다른 제품으로 합성됐다" 컴플레인 |
| 텍스트 한글 무결 | ASS 자막 + 이미지 내 텍스트 모두. 영어/일본어/깨진 한글 0건 | 이미지 프롬프트에 "Korean text bubble '~'" 넣으면 GPT 가 잘못된 한글/일본어 그리기 쉬움 |
| TTS 페이스 | cue ratio < 1.15 + 사용자 시청 | SPEED 너무 낮으면 호흡 늘어짐 |

**제품 일관성 — 핵심 룰:** 제품 등장 컷 (hero가 들고있는 컷, 짜는 컷, victory 컷) 은 반드시 `pd1.png` 를 직접 ref로 사용. `product_master.png` 는 **스타일 통일용일 뿐 누끼 보존용 아님** (이미 generative 변형이 들어가 있음). edit_multi.mjs 호출 시 (hero_master + pd1) 조합.

**한글 깨짐 회피:** 이미지 프롬프트에 한국어 텍스트 그리기 요구하면 GPT가 깨뜨릴 확률 70%+. 제품 라벨 한글은 pd1.png ref 픽셀 보존, 자막은 ffmpeg ASS 합성 단계에서만. 프롬프트 끝에 "텍스트/라벨/사이드바/도표 금지" 명시.

- confidence: high (4건 모두 단일 세션 내 발견 + 사용자 직접 검증)
- source: 2026-05-04 루비알엔 v6_hero 액션 광고 재작업 (43s → 23.5s, S06/S07/S11 제품컷 재생성)
- related: §47 SPEED+MAX_SIL 표, §45 실제 제품 사진 reference 필수, [[tacit/chatgpt-web-automation]]


## §51 — 시댄스/AI 영상기 native audio "환각 발화" 트랩 (2026-05-08)

> 시댄스(Seedance) 같은 native-audio video gen 모델은 **의도한 한국어 대사 + garbage 발화** (메타 설명·중국어/잡음·랜덤 한국어 prefix) 를 같이 생성한다. 이것을 raw 그대로 자르고 붙이면 "이상한 단어/장면이 다 들어가 있는" 결과물이 됨.

### 사용자 컴플레인 원문
> "엥 입이 일그러지도록 립싱크하는게 아니라 그냥 시댄스로 자연스럽게 뽑힌 영상으로 합쳐야하는데? 잘못됨"
> "존댓말.. 이런거 들어가있고 중국어같은 알수없는 말하는 구간 까지 다합쳣어"
> "진짜 뒤지기 싫음녀 제대로 좀 처 알아들어"

→ **3번 wrong build 후 transcribe 도입해서 해결**. 이 트랩에 시간 30분+ 손실.

### 관찰된 garbage 패턴 (10컷 중 3컷에서 발견)

| 컷 | garbage 위치 | 실제 음성 |
|----|-------------|-----------|
| C1 | 시작 0–1.5s | "**존댓말**, 오늘은 요즘 화제가 되고…" (메타 발화 prefix) |
| C2 | 시작 0–3.7s | "**잠정 2척이 된다요. 송도환이라서**, 혹시 루비알엔이라고…" (랜덤 잡담 prefix) |
| C9 | 시작 0–2.4s | "**그제한 감독을 온록 스테인 사연합니다**, 14일 얼룩 챌린지도…" (가장 긴 garbage prefix) |

C8/C10 같이 끝부분에도 짧은 잡음·무음이 붙는 경우 있음. **시작·끝 양쪽 모두 검사 필수.**

### 함정 — 하지 말 것

1. **silencedetect만 믿고 자르기 ❌** — garbage도 음성이라 silence가 아님. silencedetect는 trailing silence(끝 무음)만 잡지 prefix garbage는 못 잡음.
2. **Gemini Vision으로 mouth-close 분석 ❌** — 입은 garbage 발화 동안에도 움직이고 있음. 시각만으론 의도/garbage 구분 불가.
3. **TTS를 raw video 위에 덮어씌우기 ❌** — 사용자 말: "왜 자꾸 이상한 TTS 음성을 입힌건데?" — native 발화의 자연스러움이 망가지고 입 모양도 안 맞음.
4. **Lipsync API로 입 모양 재합성 ❌** — 사용자 말: "입이 일그러지도록 립싱크하는게 아니라" — 입이 부자연스럽게 변형됨.
5. **video 길이 = audio 길이 가정 ❌** — Seedance는 7s/9s 같은 fixed-length 출력에 garbage로 padding 함.

### 정답 절차 — Whisper transcribe + 의도 대사 매칭

```
1. ffmpeg -vn -acodec libmp3lame로 각 컷 오디오 추출
2. faster-whisper (small도 충분, medium/large는 download 오래걸림) word-level transcribe
   - 모델: WhisperModel("small", device="cpu", compute_type="int8")
   - language="ko", word_timestamps=True
3. 의도 대사(motion_prompts.yaml의 Korean dialog)와 transcript 단어 비교
4. 의도 첫 단어의 start time = clip_start (- 0.1s lead pad)
5. 의도 마지막 단어의 end time = clip_end (+ 0.15s tail breath)
6. ffmpeg -ss/-to로 정밀 trim → concat
```

### 매칭 알고리즘 함정

- Whisper는 phonetic substitution이 흔함:
  - 피디알엔에 → "피디아렌의"
  - 글루타치온까지 → "글루크라 논까지"
  - 클렌저 → "클랜더"
  - 루비알엔 → "루비아렌"
  - 멜라블 → "멜랍을"
  - 세정 → "세경"
  - 얼룩 → "온록"
- `target in cum` 같은 strict substring matching은 q=0 자주 나옴 → **SequenceMatcher 또는 word-level 매칭** 필요.
- **실용해법**: transcripts.json을 먼저 저장 → 사람이 word 배열 보고 의도 첫·마지막 단어를 직접 골라 cut_overrides.json 작성. 알고리즘 매칭 실패해도 진행 가능.

### 코드 스켈레톤

```python
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio_path, language="ko", word_timestamps=True)
words = [{"w": w.word, "s": w.start, "e": w.end}
         for seg in segs if seg.words for w in seg.words]
# words 출력 후 사람이 보고 의도 첫·마지막 단어를 골라 cut window 결정
```

### 표준 파이프라인 (BJ/박사대화 톤 광고)

```
[02_원본영상_시댄스/*.mp4]
  → 오디오 추출 (mp3)
  → faster-whisper word-level transcribe → transcripts.json
  → 의도 대사와 word 비교 → cut_overrides.json (사람 큐레이션)
  → ffmpeg trim (-ss intended_start - 0.1, -to intended_end + 0.15)
  → 1920×1080 + tv_frame.png overlay
  → concat → 자막 burn → 최종 mp4
```

**속도/비용**: faster-whisper small CPU = 컷당 5–15초, 10컷 ≈ 1–3분. 시간 가치 대비 매우 cheap.

### 파일·폴더 표준 (재현용)

| 파일 | 용도 |
|------|------|
| `transcripts.json` | 컷별 word-level 받아쓰기 (Whisper 출력) |
| `intended_dialog.json` | motion_prompts.yaml에서 추출한 의도 한국어 대사 |
| `cut_overrides_v##.json` | `{cid: {intended_start, intended_end, note}}` — 사람이 큐레이션한 cut 시점 |
| `timings_v##.json` | 빌드 후 실제 사용된 cut 시간들 (검증용) |

### 사용자 핸드오프 패키지 표준 폴더링

```
박사대화_..._v05_PACKAGE/
├── 01_최종영상/         # 자막 포함/없음 mp4
├── 02_AE프로젝트/       # .aep (AE 2025)
├── 03_컷별영상_av/      # 1080p+frame 처리된 av 컷 (AE 입력)
├── 04_원본소스_시댄스/  # raw 시댄스 (재컷용)
├── 05_그래픽_자막/      # tv_frame.png + .ass
├── 06_분석데이터/       # transcripts/cut_overrides/timings JSON
└── README.md            # 사용법 + 컷 시점 표
```

`.aep`는 **패키지 내부 절대 경로로 빌드** (build_ae_*.py에서 PKG 변수 분리). 패키지 옮기면 AE에서 풋티지 relink 필요 — README에 명시.

### 메모리·메타 교훈

- **AI 영상기 출력 = "주석이 섞인 raw"**. 의도 대사만 살리는 후처리 필수.
- **Native audio**의 자연스러움은 lipsync/TTS 더빙으로 절대 못 따라옴 → 자르기로 garbage 제거가 정답.
- **사용자가 "잘 자르고 붙이면 되는데"** 라고 짧게 말하면, 그건 "Whisper transcribe → 의도 대사 매칭 → 정밀 cut" 절차를 의미한다. 단순 "전체 길이 사용"이나 "silencedetect"로 가면 다시 컴플레인 받음.

- confidence: high (단일 세션 4번 wrong build → transcribe 도입 후 1발 OK + 사용자 "오 이거 잘했다" 명시 칭찬)
- source: 2026-05-08 박사대화_루비알엔클렌저_70s v01→v05 재제작
- related: §42 후처리 표준, §41 Voice Conversion vs TTS 비교, [[tacit/lipsync-multi-face-trap]]
