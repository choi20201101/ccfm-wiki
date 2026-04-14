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

## 연관 문서
- [[src-diet-b2a-v2]] — 다이어트 B&A 릴스 v2 (시드 이미지 소비자)
- [[content-ai-automation]] — 콘텐츠 AI 자동화 도메인
- [[tacit/coding-lessons]] — Google 차단 우회 / 실시간 크롤링 교훈
- [[tacit/creative-patterns]] — AI tell 제거 / aesthetic LoRA
