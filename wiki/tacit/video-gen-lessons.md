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
