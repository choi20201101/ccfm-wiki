---
type: source
domain: content-ai-automation
confidence: high
created: 2026-05-20
updated: 2026-05-20
sources:
  - raw/inbox/2026-05-20-winnersojae-higgsfield-chatgpt-image-questions.md
related:
  - [[domains/content-ai-automation]]
  - [[domains/da-creative]]
  - [[tacit/video-gen-lessons]]
  - [[tacit/creative-patterns]]
  - [[tacit/chatgpt-web-automation]]
  - [[tacit/coding-lessons]]
  - [[sources/src-higgsfield-cli-claude-bypass-2026-05-12]]
  - [[sources/src-higgsfield-soul-api-2026-04-21]]
---

# 위너소재 — 힉스필드 + 챗GPT 이미지 자동화 직원 피드백 정리

**계기**: 2026-05-20 직원이 힉스필드(Higgsfield) 영상 자동화 + ChatGPT 이미지 2.0 배너/캐러셀 자동화 진행 중 두 가지 질문 — (1) ffmpeg 트랜지션 커스텀 가능 여부 (2) 레퍼런스 직접 입력 vs 자동 학습 방향.

원문: [[raw/inbox/2026-05-20-winnersojae-higgsfield-chatgpt-image-questions]]

---

## Q1. ffmpeg 트랜지션 — **얼마든지 커스텀 가능. 다만 진짜 문제는 트랜지션이 아니라 "편집점이 보이스에 안 붙어 있는 것"**

### 결론
**ffmpeg에서 트랜지션은 충분히 풍부하게 정의 가능**. 그러나 직원이 말한 "빠른 템포에서 편집점·트랜지션이 약하다"는 증상은 **트랜지션 이펙트의 문제가 아니라 "씬 길이를 TTS/오디오 cue에 동기화하지 못한 것"**일 확률이 매우 높음. 이게 [[tacit/video-gen-lessons]] §35·§36 의 단일 최대 교훈.

### 1) ffmpeg가 기본 제공하는 트랜지션 — 10+ 타입

[[domains/content-ai-automation]] §1-2 에 이미 운영 중인 JSON 스키마:

```json
"transitions": [
  {"type": "fadeblack", "duration": 0.15},
  {"type": "wipe_left", "duration": 0.25},
  {"type": "zoom", "duration": 0.2},
  {"type": "dissolve", "duration": 0.2}
]
```

`xfade` 필터가 노출하는 효과: `fade / fadeblack / fadewhite / wipeleft·right·up·down / slideleft·right·up·down / dissolve / pixelize / radial / smoothleft·right·up·down / circleopen·close / vertopen·close / horzopen·close / diagtl·tr·bl·br / hlslice / hrslice / vuslice / vdslice / hblur / fadegrays / squeezev·h / zoomin / circlecrop / rectcrop / distance / hlwind / hrwind / vuwind / vdwind / coverleft·right·up·down / revealleft·right·up·down` 등 50종 가까이. **직원이 알고 있는 것보다 풀이 훨씬 큼**.

### 2) 진짜 커스텀 — `xfade=transition=custom:expr='...'`

`xfade` 필터에는 `custom` 모드가 있어 **GLSL 비슷한 표현식으로 픽셀 단위 블렌드 식을 직접 정의** 가능:

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "xfade=transition=custom:duration=0.3:offset=1.7:\
   expr='if(gte(P,0.5),B,A)'" out.mp4
```

- `P` = 0~1 progress
- `A` / `B` = 두 비디오의 픽셀
- `X`,`Y` = 좌표, `W`,`H` = 해상도
- 사인파·랜덤·마스크·줄무늬·diagonal cut 등 무엇이든 식으로 표현

### 3) GL Transitions 라이브러리 (200+ 효과)

ffmpeg 빌드를 `--enable-libplacebo` 또는 GL transition shader 빌드로 컴파일하면 **gl-transitions.com 에 있는 200+ shader (Doorway, Heart, GlitchMemories, Burn 등)** 를 그대로 사용 가능. 핸드 코딩보다 빠름.

### 4) ⚠️ 그러나 — **빠른 템포에서 진짜 안 잡히는 건 트랜지션이 아니라 "편집점"**

[[tacit/video-gen-lessons]] §35·§36 핵심 교훈:

> **씬 길이를 미리 박아두면 안 됨. TTS 보이스가 끝나는 시점에 컷이 바뀌어야 한다.**

- §35.1 "씬 = 2초 고정" 절대 금지 — TTS가 씬 경계를 넘김 → "더빙 끝나기 전에 다음 씬으로 넘어감"
- §36 컷 길이 = 다음 cue start 까지 (TTS 발화 길이 아님) — 호흡 갭 0.1~0.5s × 23개 ≈ 5.5s 누락되면 영상이 오디오보다 짧아짐
- 정석 파이프라인: **대본 → ElevenLabs `with-timestamps` → ffprobe 실측 → 라인별 atempo 차등 (1.07~1.23) → cue 기반 가변 컷 길이**
- 워드팝 자막: char-level timestamp → 단어 경계로 묶기 → 한 화면 1단어, 시작 -0.05s 일찍 등장, 다음 단어 시작 = 현재 단어 끝

### 5) ⚠️ 그 위에 — **xfade가 항상 정답이 아님**

[[tacit/coding-lessons]] 2026-04-13 메모:
> "ffmpeg xfade(0.3s)는 흐리게 섞이기만 함. 양쪽 클립의 **같은 포즈 프레임 지점에서 concat 하드컷** 하면 '몸만 변한' 효과가 더 자연스럽다."

빠른 템포에서는 오히려 **하드컷 + 짧은 fadeblack(0.05~0.10s) 펀치**가 더 잘 먹힘. xfade를 화려하게 깐다고 빠르게 보이는 게 아님.

### 6) 직원에게 줄 행동 가이드 (우선순위)

1. **트랜지션 커스텀보다 먼저 — 컷 타이밍을 TTS char-level timestamp에 붙여라.** ElevenLabs `with-timestamps` 엔드포인트 + ffprobe 실측. [[tacit/video-gen-lessons]] §35.2 단방향 파이프라인 그대로 적용.
2. **워드팝 자막 (한 화면 1단어, 220pt+)**. 빠른 템포의 "쳐주는 느낌"은 트랜지션이 아니라 워드팝과 cut on beat가 만듦. [[tacit/video-gen-lessons]] §35.5.
3. **xfade는 0.10~0.20s로 짧게**. 0.30s 이상이면 흐리게만 보임. 빠른 템포에선 `fadeblack 0.05~0.10s` 또는 하드컷이 더 펀치 있음.
4. **그래도 부족하면** xfade `custom` expression 또는 GL transitions 도입. 단, 이 단계는 1~3이 다 잡힌 다음에.
5. **테스트 영상 받아서 위 4단계 중 어디가 빠졌는지 진단** 후 회신 권장.

---

## Q2. ChatGPT 이미지 2.0 레퍼런스 — **"직접 입력 vs 자동 학습" 양자택일이 아님. 두 가지를 다른 레이어로 같이 운영.**

### 결론
- **레이아웃·브랜드 디자인 톤** = 직원이 매번 직접 넣어주는 게 정답 (ChatGPT 이미지 자동화에서 가장 안정적)
- **다양성** = 레퍼런스를 늘리거나 LoRA 학습으로 분리해서 해결
- "스스로 학습" = ChatGPT 이미지에는 사실상 없음. 다양성은 **레퍼런스 풀 회전 + 18축 cid 시드 결정론**으로 만든다.

### 1) ChatGPT 이미지의 실제 동작 — "학습"이 아니라 "참고"

[[tacit/chatgpt-web-automation]] §1·§5·§7 에서 운영 검증한 사실:

- ChatGPT 이미지는 **세션 단위로 첨부 레퍼런스를 "참고"** 함. 진짜 학습(weight update)은 안 됨.
- **첨부한 베스트 레퍼런스의 카피 텍스트를 그대로 복사하려는 충동**이 강함 → "베스트는 시각·구도·인물·컬러 참고용. 텍스트는 모두 무시" 명시 필수
- **캐릭터 시트 부산물** 매번 같이 만듦 (영웅 캐릭터 4-패널, 4883567 bytes 고정) — 다운로드 로직에서 필터링 필수
- 레퍼런스 그대로 픽셀 복사되는 함정 — `alt="생성된 이미지"` vs `alt="업로드한 이미지"` 분리 안 하면 첨부본이 final 폴더에 그대로 떨어짐

### 2) 레퍼런스를 "영감"이 아니라 "시각 템플릿"으로 명시

[[tacit/creative-patterns]] [2026-04-20] 핵심 룰:

> gpt-image는 레퍼런스 이미지 첨부만으로는 타이포·레이아웃을 제대로 안 따라감. 프롬프트 **TOP과 BOTTOM 양쪽에 "visual template, not inspiration"** 강조하고, **카피·모델·제품만 교체·그 외 시각 요소는 그대로**라고 명시하면 재현력 향상.

→ 직원이 "레퍼런스 직접 입력"을 계속 하는 건 옳음. 다만 **프롬프트 양쪽에 명시 강도를 높이는 것**이 핵심 개선 포인트.

### 3) 다양성은 "스스로 학습"이 아니라 **풀 회전 + 시드 결정론**으로

[[tacit/creative-patterns]] [2026-05-03] 18축 cid 시드 결정론 시스템 (샤르드 CHARDE 3000장 운영 검증):

- **18축 = 모델 8축 + 권위·증거 2축 + 카피 8축**
- 각 축마다 풀 25~33개 → cid * 31337 + 11 해시로 결정론 회전
- 같은 cid 재실행 시 같은 결과 (재현성) + cid별 회전 (다양성)
- 풀 사이즈 50→100 으로 늘리면 평균 60회 반복 → 30회 / max 9x (40% 개선)
- cap 권장값 = `풀 사이즈 × 0.06` (3000장 기준)

**위너소재 적용 시:**
- 자사 배너 디자인 5~10종 → "레이아웃 풀"
- 소구점 30~50개 → "카피 풀"
- 모델/배경/색감 → 각 풀
- 캐러셀 1장당 cid 부여 → 시드 회전으로 다양성 자동 확보

### 4) "스스로 학습"을 굳이 하고 싶다면 — aesthetic LoRA

[[tacit/creative-patterns]] 2026 초 메모 ([[sources/src-goglecc-seed-curation]] 기반):

- ChatGPT는 학습 불가. 학습 원하면 **Flux LoRA** (Higgsfield Brand Kit 또는 fal.ai 직접 학습) 사용
- **같은 무드, 다른 사람/장소 30~50장**으로 학습 → 모델이 "내용"은 못 외우고 **질감·조명·그레인·색감·프레이밍**만 학습
- Nano Banana 같은 reference-based 호출은 **배경까지 복제** → "베낀 티" 강함
- 콘텐츠 다양성 필수: 같은 장소/인물 사진은 학습 셋에 1~2장만 (pHash 클러스터로 자동 배제)

→ "스스로 학습"의 진짜 형태. 단, 구축 비용·러닝 커브 있음.

### 5) 카드 캐러셀 특수 고려 — **첫 컷은 layout 가장 강제, 끝 컷은 CTA 강제**

배너 단일 이미지와 달리 캐러셀은 **시리즈 일관성**이 필수.

- 첫 컷(hook): 레이아웃 가장 강하게 박음. 베스트 레퍼런스 1장 + "visual template" 강제.
- 중간 컷(증거·USP): 같은 색감/타이포만 유지, 구도는 자유.
- 끝 컷(CTA): 가격·혜택 위치를 마스터 좌표로 고정. ffmpeg/PIL 후처리로 카피를 직접 그리는 것도 옵션 — [[tacit/video-gen-lessons]] §14 "Gemini는 한국어 텍스트를 이미지에 못 그림" 교훈은 ChatGPT에도 부분 적용.

### 6) 직원에게 줄 행동 가이드 (우선순위)

1. **레퍼런스 직접 입력은 유지** — 자동화 시점에 안정성이 가장 높음.
2. **프롬프트 TOP·BOTTOM 양쪽에 "visual template, not inspiration" + "카피·모델·제품만 교체"** 명시 (재현력 향상).
3. **다양성은 "스스로 학습"이 아니라 풀 회전으로 해결** — 레퍼런스 풀 5~10종, 카피 풀 30~50개, cid 시드 결정론. [[tacit/creative-patterns]] 18축 시스템 참고.
4. **베스트 카피 텍스트 복사 차단** — 프롬프트 상단에 "베스트는 시각 참고. 텍스트는 모두 무시" + 광고주 반려 어휘 "절대 그리지 마" 섹션.
5. **다운로드 로직 점검** — 캐릭터 시트 부산물 / 첨부 이미지 픽셀 복사 함정 [[tacit/chatgpt-web-automation]] §1·§5 확인.
6. **장기 다양성** 원하면 그때 Flux LoRA (Higgsfield Brand Kit) 검토. 단, 구축 비용 고려.

---

## 직원에게 보낼 답신 초안

> 잘 진행 중이네요. 두 가지 다 답 정리해서 드릴게요.
>
> **1) 힉스필드 빠른 템포 — ffmpeg 트랜지션 커스텀 가능합니다. 다만 진짜 문제는 트랜지션이 아닐 가능성이 큽니다.**
>
> ffmpeg `xfade` 필터는 50종 가까운 기본 트랜지션 + `custom` expression 모드(GLSL 비슷한 픽셀 식 직접 정의)를 지원합니다. GL Transitions 라이브러리(200+ shader)도 연결 가능합니다.
>
> 그런데 "빠른 템포에서 편집점·트랜지션이 약하다"는 증상은 우리 30+편 영상 만들면서 발견한 가장 큰 함정이랑 정확히 일치해요. **씬 길이를 미리 박아두면 보이스가 씬을 넘어가서 끊기는 느낌**이 납니다. 정답은:
> - TTS는 ElevenLabs `with-timestamps` 엔드포인트로 받기 (char-level 타임스탬프)
> - ffprobe로 실측 길이 측정 (API 응답 신뢰 X)
> - 라인별 atempo 차등 (1.07~1.23) — 후킹·CTA는 천천히, 정보 라인은 빠르게
> - 컷 길이 = 다음 cue start 까지 (TTS 발화 길이 X)
> - 자막은 워드팝 (한 화면 1단어, 220pt+, 시작 -0.05s 일찍 등장)
>
> 그 다음에 xfade는 0.10~0.20s로 짧게. 더 빠른 템포 원하면 `fadeblack 0.05s` 또는 같은 포즈 매칭 하드컷이 오히려 더 펀치 있습니다. 위키 [[tacit/video-gen-lessons]] §35·§36 에 풀 파이프라인 있으니 참고.
>
> 테스트 영상 공유해주시면 어디 단계가 빠졌는지 같이 봅시다.
>
> **2) 챗GPT 이미지 레퍼런스 — 직접 입력 유지가 정답. 다양성은 "스스로 학습"이 아니라 풀 회전으로 만듭니다.**
>
> ChatGPT 이미지는 사실 진짜 학습(weight update)을 안 합니다. 세션 단위로 첨부 레퍼런스를 "참고"만 합니다. 그래서 자동화에선 **레퍼런스 직접 입력이 가장 안정적**이에요.
>
> 다만 두 가지 개선 포인트:
>
> a) **프롬프트 TOP·BOTTOM 양쪽에 "visual template, not inspiration" + "카피·모델·제품만 교체, 나머지 시각 요소는 그대로"** 명시. 우리 운영 데이터로 재현력 크게 향상.
>
> b) **다양성은 "풀 회전 + cid 시드 결정론"으로** — 우리가 샤르드 CHARDE 3000장 운영하면서 정리한 18축 시스템 그대로 적용 가능합니다:
> - 자사 배너 레이아웃 5~10종 풀
> - 소구점/카피 30~50개 풀
> - 모델·배경·색감 각각 풀
> - 캐러셀 1장당 cid 부여 → 시드 해시로 회전
>
> 풀 사이즈 100 + cap 6 정도면 같은 패턴 max 9회 반복 안에 들어옵니다.
>
> "진짜 학습"을 원하면 Flux LoRA (Higgsfield Brand Kit 또는 fal.ai)로 같은 무드 30~50장 학습하는 방식이 있는데, 구축 비용·러닝 커브 있으니 풀 회전부터 검증 후 검토합시다.
>
> 위키 [[tacit/chatgpt-web-automation]] [[tacit/creative-patterns]] 에 운영 디테일 다 있으니 참고하세요.

---

## 사용자(대표)가 추가로 결정해야 할 것

- 테스트 영상 공유받을 채널 (Slack? Drive?)
- 위너소재 전용 18축 시스템 구축 우선순위 (지금 vs 검증 후)
- Higgsfield Brand Kit / LoRA 학습 진입 여부 — [[sources/src-higgsfield-cli-claude-bypass-2026-05-12]] 의 "보조 실험 레이어" 권고 참고
