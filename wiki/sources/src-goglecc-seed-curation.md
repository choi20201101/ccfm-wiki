---
type: source
domain: content-ai-automation
confidence: medium
created: 2026-04-14
updated: 2026-04-14
sources:
  - C:/Users/gguy/Desktop/goglecc (이미지 수집 + negative curation + LoRA 파이프라인)
---

# goglecc — 인플루언서 씨드 이미지 수집·큐레이션 파이프라인

> **용도**: "인플루언서/모델 씨드 이미지 수집해줘"류 요청이 올 때 쓸 수 있는 검증된 파이프라인.
> **목표**: 광고 소재용 AI 생성에 넣을 **AI tell이 없는 자연스러운 레퍼런스** 확보.

## 1. 수집 소스 선택 (Google ❌ / Bing ✅)

### Google Images는 headless Playwright에서 막힘
- `google.com/search?udm=2` 접근 시 **reCAPTCHA "비정상 트래픽 감지"** 페이지로 리다이렉트
- `<img>` 0개 반환, `img.YQ4gaf` 같은 selector 무의미
- IP 단위 봇 탐지 (2026-04-14 goglecc에서 재확인)

### Bing으로 우회
- URL: `https://www.bing.com/images/search?q={kw}&form=HDRSC2`
- 핵심 selector: `a.iusc[m]` — `m` 속성이 JSON, **`murl` 키가 원본 URL**
- 스크롤 1회당 ~35장, 4~5스크롤로 100장 URL 확보
- 다운로드 성공률 45%~100% (키워드 의도 명확성에 따라)

## 2. 키워드 표현이 품질 편차의 주 원인

goglecc round_01 (2026-04-14) 7개 키워드 결과:

| 키워드 | 수집 | bad률 | 비고 |
|--------|------|------|------|
| 여자연예인 | 93 | **4%** | 명확, 깔끔 |
| 예쁜여자 | 95 | **4%** | 명확, 깔끔 |
| 몸매가 예쁜 젋은 인플루언서 | 82 | 9% | 긴 표현도 OK |
| 자연스러운 자취방 배경 | 45 | 62% | "자연스러운"이 모호 |
| 여자동안 | 87 | **91%** | "동안" → 어린이 사진 유입 |
| 인플루언서여성 | 100 | **59%** | 일반명사 조합 → AI 이미지/스톡 범람 |
| 동안인플루언서 | **1** | skip | Bing 검색 결과 자체 없음 |

**교훈**: 명확한 단일 명사("여자연예인") > 어색한 합성어("인플루언서여성", "여자동안"). 검색어는 실제 네이티브 구어 표현으로 쓸 것.

## 3. Negative Curation이 Positive보다 효율적

- **Positive (좋은 10장 선별)**: 선택지 많음, 기준 모호, 사용자 피로 큼
- **Negative (안 좋은 것만 aa/로 모음)**: "제외할 패턴"이 **정량 지표로 뚜렷**
- 사용자 피드백: *"안 좋은 걸 빼는 게 더 났네"* (2026-04-14)

### 안 좋은 이미지의 정량 시그니처
- `saturation_std > 0.17` → AI 일러스트/그래픽 가능성
- `aspect_ratio ≈ 1.55` (16:9 근처) → 유튜브/영상 썸네일
- `aspect_ratio ≈ 1.55` + 저해상도 → 콜라주/블로그 스크린샷
- `width < 556` or `height < 400` → 스톡 사이트 썸네일
- `edge_density > 0.12` → 텍스트 오버레이 (배너/밈)
- **pHash Hamming distance ≤ 12** → 블랙리스트와 매우 유사

## 4. 파이프라인 구조 (bdh 준수)

```
수집(Bing)
  → meta_extractor.py   # 이미지별 JSON sidecar (해상도/종횡비/HSV/phash/edge)
  → (사용자 큐레이션: aa/ 폴더로 이동)
  → analyze.py          # aa/ 학습 → criteria.yaml 증분 갱신
  → filters.py --apply  # _filtered_out/으로 자동 분류
  → prepare_lora_dataset.py  # 살아남은 이미지 + 캡션 zip
  → fal_train_lora.py        # fal.ai flux-lora-fast-training (~$2, 3~5분)
  → generate_diet_sets.py    # LoRA URL + 프롬프트 → 10세트 생성
```

라운드 누적 구조: `curation/round_XX/{collected,picks,aa}/` + 글로벌 `curation/criteria.yaml` (version 필드 증가).

## 5. Seed 이미지 → AI 생성 연결 시 주의

### AI tell 제거 (가장 어려운 부분)
- 너무 매끈한 피부, 좌우대칭, 완벽한 보케, 과보정 조명 = AI tell
- 반대 프롬프트: `skin pores, slight film grain, casual snapshot, no retouching, shot on iPhone, slightly underexposed, candid`
- 네거티브: `smooth skin, plastic, cgi, 3d render, hyperreal, airbrushed, overprocessed`
- **Flux 모델 guidance scale 2.5~3.0** (높을수록 AI 느낌 강해짐)

### Reference 누수 문제
- 단순 reference-based 호출(Nano Banana 등)은 **배경까지 복제** → "레퍼런스 베낀 느낌"
- 해법: **subject LoRA가 아니라 aesthetic LoRA** 학습
  - 같은 무드, 다른 사람/장소 30~50장 → 질감·조명·그레인만 학습, 콘텐츠는 못 외움
  - Civitai의 "iPhone candid", "film grain" LoRA들이 이 방식

### 콘텐츠 다양성 필수
- 같은 장소/인물 사진은 LoRA 학습 셋에 1~2장만
- pHash 클러스터로 자동 배제 가능
- 편향 셋으로 학습하면 그 인물/배경까지 외워 reference 누수 재발

## 6. 재사용 체크리스트 ("씨드 이미지 가져와줘" 요청 올 때)

- [ ] 키워드 3~7개 — 명확 단일명사 위주
- [ ] Bing으로 수집 (Google 절대 X)
- [ ] 키워드당 100장 시도, 실수율 10~40% 정상
- [ ] 수집 후 사용자에게 `aa/`로 안 좋은 것 모아달라고 요청
- [ ] meta → analyze → filter로 자동 1차 정제
- [ ] 라운드 2~3회 돌려 살아남은 이미지 50~100장 확보
- [ ] LoRA 학습 전 **콘텐츠 중복 배제** 점검 (같은 인물/장소 편중 X)
- [ ] fal.ai flux-lora-fast-training, is_style=True 설정

## 7. 생성 API 비교 (2026-04-14 검증)

같은 레퍼런스 + 같은 한국어 프롬프트로 A/B 테스트:

| 항목 | **Gemini API 직호출** (`gemini-2.5-flash-image`, `google-genai` SDK) | fal-ai/nano-banana/edit | Flux+LoRA (v3 튜닝) |
|------|------|------|------|
| 실사 질감 | ✅ 챗과 동일 수준 | △ 약간 AI sheen | ❌ AI tell 명확 |
| 얼굴 보존 (ref → 출력) | ✅ 얼굴/특징 유지 | ❌ **얼굴 완전 다르게 바뀌는 사례 다수** | — (학습 기반이라 N/A) |
| 배경 자연스러움 | ✅ 실제 방 느낌 | △ 렌더 느낌 섞임 | △ |
| 비용 | 이미지당 ~$0.039 | ~$0.03~0.05 | 학습 $2 + 장당 ~$0.05 |
| 프롬프트 언어 | **한국어 + 구어 + 풍부한 촬영 컨텍스트**가 최적 | 영어/한국어 혼용 | 영어 |

**결론: 인플루언서 레퍼런스 기반 실사 생성은 Gemini API 직호출이 기본값.**

- fal은 Nano Banana를 프록시하지만 얼굴 보존·실사감 둘 다 품질 저하 발생 (원인 불명, fal 측 래핑·파라미터 차이 추정)
- Flux+LoRA는 스타일 학습엔 쓸만하지만 AI 특유 sheen을 완전히 없애지 못함 (XLabs Realism LoRA 0.75 + guidance 1.8 + 후처리 그레인 스택으로도 한계)
- **프롬프트는 한국어 + "친구가 찍어준 캔디드 스냅, 보정 없음, 피부 모공 그대로, AI처럼 보이지 않게"** 같은 자연스러운 촬영 묘사가 챗 수준 품질 뽑아냄

## 8. 재사용 체크리스트 업데이트 (2026-04-14)
- [ ] 생성은 **Gemini API 직호출** 우선 (`google-genai`, `gemini-2.5-flash-image`)
- [ ] `key.txt`에 `제미나이=AIz...` 라벨로 저장, 라벨 파서로 로드
- [ ] 레퍼런스 이미지는 이 파이프라인(Bing→negative curation)의 생존본에서 로테이션
- [ ] 프롬프트는 **한국어**, 촬영 맥락 풍부하게, 직설 영어 금지 (safety 거부 + 렌더 느낌)
- [ ] fal/Flux LoRA는 fallback 또는 다른 용도 (스타일 변환 등)로만 사용

## 9. 다이어트 B/A 생성 최종 파이프라인 (V15, 2026-04-15 확정)

15회 반복 끝에 확정된 **"예쁜 얼굴 + 진짜 통통 몸"** 조합 해법.
사용자가 "만족스러운 결과" 확인.

### 아키텍처 (세트당 3 API 호출)
```
1. AFTER  = Higgsfield Soul (pretty SoulID, strength 0.85) → K-pop 예쁜 슬림 얼굴
2. BEFORE_raw = Higgsfield Soul (pretty SoulID, strength 0.6) → moderate 통통 몸 + 평범 얼굴
3. BEFORE = fal-ai/face-swap(source=AFTER, target=BEFORE_raw) → 예쁜 얼굴 + 통통 몸
```

### 왜 이 구조로 갔는가 (15회 반복 결과)
- **Higgsfield strength 0.85 단독** → 얼굴 예쁨 ✓ / 배만 임산부형 돌출 ❌
- **Higgsfield strength 0.5 단독** → 몸 리얼 통통 ✓ / 얼굴 평범 ❌
- **After-first + Gemini fatten** → Gemini가 preserved-identity body 살찌움 **완강히 거부** (safety)
- **Before-first + Gemini slim** → Gemini 슬림화는 OK지만 얼굴이 generic
- **v15 face-swap** → 두 이미지의 강점만 합성 ✓

### Higgsfield Soul 엔드포인트 (2026-04-15 검증)
- **Base URL**: `https://platform.higgsfield.ai`
- **Auth headers**: `hf-api-key: {KEY_ID}` + `hf-secret: {KEY_SECRET}` (Authorization 헤더 아님)
- **SoulID 생성**: `POST /v1/custom-references` → body: `{name, input_images: [{type:"image_url", image_url:"..."}]}` → 폴링 `GET /v1/custom-references/{id}`
- **SoulID 학습셋**: 10~20장 **같은 유형의 얼굴**. "같은 사람"이 아니어도 "같은 아름다움 범주"면 충분 (우리는 K-pop 연예인 10명으로 훈련 → "K-pop idol 톤" 학습)
- **이미지 생성**: `POST /higgsfield-ai/soul/standard` → `{prompt, aspect_ratio, resolution:"1080p", custom_reference_id, custom_reference_strength}` → 폴링 `GET /requests/{id}/status`
- **strength 튜닝**: 0.85 = 얼굴 보존 강함 / 0.5~0.6 = 체형 변화 자유

### fal-ai/face-swap 호출 포맷 (2026-04-15 검증)
```python
fal_client.run("fal-ai/face-swap", arguments={
    "base_image_url": target_url,  # 몸 (얼굴이 들어갈 대상)
    "swap_image_url": source_url,  # 덮어씌울 예쁜 얼굴
})
```
- **주의**: 필드명이 `source_image_url/target_image_url` 아님 → `base_image_url/swap_image_url`
- **비용**: ~$0.03/호출
- **대안 엔드포인트**: `easel-ai/advanced-face-swap` — `gender_0`, `workflow_type:"target_hair"` 추가 필요

### 프롬프트 핵심
**AFTER (예쁜 슬림)**:
```
pretty young 20s Korean woman with beautiful K-pop idol face,
lean athletic body with toned abs, fitted black sports bra and
high-waist black leggings. iPhone candid snapshot. visible skin pores.
```

**BEFORE_raw (moderate 70kg 통통)**:
```
A 20s Korean woman with a mildly chubby body — around 70kg, BMI 26
(NOT obese): slightly fuller cheeks, faint double chin, soft rounded belly
creating subtle muffin top, fuller thighs. Grey cotton t-shirt fully
covering chest/torso down to waistband (NOT pulled up, no chest exposed).
```
**체중 수준 명시가 핵심** — "overweight" 만 넣으면 AI가 임산부 체형으로 해석. "70kg, BMI 26" 구체 수치로 moderate 유지.

### 비용/세트
- Higgsfield 2 calls: ~$0.06 (0.025 × 2 standard 1080p)
- fal face-swap: ~$0.03
- **합계: ~$0.10/세트** → 10세트 ~$1

### 양산 시 절감 경로
- fal face-swap → **로컬 InsightFace inswapper_128.onnx** (onnxruntime) 교체
- 1000세트 기준 $30 절감
- 단 로컬 셋업 필요 (Windows wheel 설치 이슈 있음, ONNX 직접 로드 권장)

## 10. 확정된 실패 경로 (다시 시도 금지)

| 시도 | 결과 | 이유 |
|------|------|------|
| Gemini로 preserved-face 인물 **살찌우기** | 실패 | Safety policy 하드 리밋. 40kg, 체인 3pass, 한국어/영어, "과거 사진" 프레이밍, 국소(배만) 변경 모두 무효 |
| Gemini multi-image blending (얼굴+몸) | 실패 | 얼굴만 preserve하고 body는 자체 생성 (slim) |
| Higgsfield img2img로 "얼굴 유지 + 몸 변경" | 실패 | strength 0.5 기준 얼굴 거의 새로 생성, 0.2 이하는 변화 미미 |
| LoRA(Flux aesthetic) + 후처리 그레인 스택 | 부분 성공 | AI sheen 완전 제거 불가 — 구조적 한계 |
| fal-ai/nano-banana/edit (Gemini 프록시) | 실패 | 직호출 대비 얼굴 보존 저하 |

## 연관 문서
- [[src-diet-b2a-v2]] — 다이어트 B&A 릴스 v2 (시드 이미지 소비자)
- [[content-ai-automation]] — 콘텐츠 AI 자동화 도메인
- [[tacit/coding-lessons]] — Google 차단 우회 / 실시간 크롤링 교훈
- [[tacit/creative-patterns]] — AI tell 제거 / aesthetic LoRA
