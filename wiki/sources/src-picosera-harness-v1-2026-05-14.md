---
aliases: ["피코세라 하네스", "피코세라 검수 루브릭", "피코쎄라 소재 분류 기준", "피코세라 하네스 기준"]
type: source
domain: da-creative
confidence: high
created: 2026-05-14
updated: 2026-05-14
sources: [raw/skills/picosera-harness/, C:/Users/gguy/Desktop/gpt/projects/picosera/bestofbest/, ~/.claude/skills/ad-bdh/]
related:
  - da-creative
  - ai-automation
  - creative-patterns
  - creative-autogen-framework
---

# 피코세라 1차 하네스 — 광고 소재 검수 루브릭

> ⚡ **트리거**: "피코세라 하네스 기준으로 필터링해줘" → 이 페이지의 §2 규칙표대로
> 소재를 0~5점으로 분류·필터링한다. 비전 판단(§1 체크리스트)은 서브에이전트로 격리.

## 무엇 / 왜

피코세라 FF-28(핸드헬드 LED 토닝 디바이스) 광고 소재 371장을 SNS 후킹력 +
사실 정확성 기준으로 0~5점 자동 분류한 **1차 하네스**. 230장 사전 분류에서 기준 추출.
산출물 `picosera/bestofbest/_정리_4점5점/` — 4·5점 266장을 소재별 폴더로 정리.
일반화 스킬 = `ad-bdh` ([[domains/ai-automation]]).

**1차다** — 조건은 바뀐다. 기준이 바뀌면 v2 루브릭을 새로 추가하고 결과는
버전별 폴더에 분리 저장(`_소재검수/v1/`, `/v2/`). v1을 덮어쓰지 않는다.

## 1. 비전 체크리스트 (서브에이전트가 이미지당 채울 항목)

| 키 | 값 | 뜻 |
|---|---|---|
| headline_position | top/center/bottom/none | 헤드라인 위치 |
| headline_weight | ultra-bold/bold/regular/none | 헤드라인 굵기 |
| headline_is_meta_or_witty | bool | 광고 자체를 메타로 비꼬거나 반전·역설 |
| text_density | low/medium/high/wall-of-text | 텍스트 밀도 |
| text_columns | int | 본문 컬럼 수 |
| copy_present | yes/no/illegible | 카피 존재 |
| copy_is_spec_label_only | bool | 카피가 제품명·인증 라벨 수준만 |
| copy_natural_sentence | bool | 자연 문장체(슬로건 아닌 말하는 톤) |
| handwritten_or_ugc_tone | bool | 손글씨·UGC·플랫레이 톤 |
| clinical_73_present | bool | 임상 73.93%/73% 노출 |
| price_anchor_present | bool | 9만원대 / 1/10 가격 노출 |
| speed_anchor_present | bool | 1조분의1초 / 3분 노출 |
| tech_anchor_present | bool | 피부과 4종 토닝 / 피코초 노출 |
| model_count / device_count | int | 인물 / 디바이스 수 |
| product_FF28_correct | yes/no/wrong | 제품 식별 정확도 (wrong=다른 제품) |
| before_after_layout | bool | 비포/애프터 직접 비교 구도 |
| personification | none/cute/grotesque | 의인화 (grotesque=혐오·uncanny) |
| multi_layer_composite | bool | 배지·박스·썸네일 다중 레이어 |
| badge_or_tape_layers | bool | 테이프·스티커·다중 배지 |
| lifestyle_natural_lighting | bool | 라이프스타일 자연광 톤 |
| dl_keyvisual_tone | bool | 3D 렌더·상세페이지 키비주얼 톤 |
| visual_polish | low/medium/high | 비주얼 완성도 |

## 2. 점수 결정 규칙 (우선순위 상→하, 첫 매칭으로 확정)

`anchors_count` = clinical_73 + price + speed + tech 중 true 개수.

| # | 라벨 | 점수 | 조건 |
|---|---|---|---|
| 1 | 문제있음 | **0** | personification=grotesque OR product_FF28_correct=wrong |
| 2 | 글자가많아 | **0** | text_density=wall-of-text OR text_columns≥4 |
| 3 | 카피없음 | **0** | copy_present≠yes OR copy_is_spec_label_only |
| 4 | DL이미지만 | **0** | dl_keyvisual_tone AND NOT clinical_73 |
| 5 | 위트5점 | **5** | headline_is_meta_or_witty AND clinical_73 |
| 6 | 베스트디벨롭5점 | **5** | multi_layer_composite AND (clinical_73 OR price) AND headline_weight=ultra-bold |
| 7 | 캐릭터5점 | **5** | personification=cute AND headline_weight∈{ultra-bold,bold} |
| 8 | 네이티브5점 | **5** | handwritten_or_ugc_tone AND model_count=0 |
| 9 | 텍스트강조4점 | **4** | badge_or_tape_layers AND (clinical_73 OR price) |
| 10 | 분위기톤4점 | **4** | lifestyle_natural_lighting AND text_density∈{low,medium} |
| 11 | 비포에프터4점 | **4** | before_after_layout |
| 12 | 단체컷4점 | **4** | model_count≥2 OR device_count≥2 |
| 13 | 네이티브4점 | **4** | copy_natural_sentence AND text_density≠wall-of-text |
| 14 | 점수3점 | **3** | anchors_count≥2 AND model_count≥1 AND product_FF28_correct=yes |
| 15 | 점수2점 | **2** | anchors_count=1 AND copy_present=yes |
| 16 | 점수1점 | **1** | model_count≥1 AND anchors_count=0 AND product_FF28_correct=yes |
| 17 | fallback | **1** | 위 어느 것에도 안 걸림 (수동 확인) |

**채택선**: 4점 이상 = 채택. 0점 = 탈락(사유별 4종).

## 3. "피코세라 하네스 기준으로 필터링해줘" 실행 절차

1. 대상 소재 폴더 확인.
2. 검수 서브에이전트 디스패치 — 이 페이지 §1 체크리스트를 첨부, 이미지당 JSON 반환.
   (비전 판단을 메인 컨텍스트에 들이지 않는다.)
3. §2 규칙표를 위→아래로 적용, 첫 매칭으로 점수·라벨 확정.
4. 점수/라벨별로 분류 → 4점+ 채택, 0점 탈락. 결과를 `_소재검수/v1/`에 저장.
5. 자동화 경로: `ad-bdh` 스킬 (`scripts/score_vision.py` + `classify.py` + `organize.py`).
   루브릭 정본 = `~/.claude/skills/ad-bdh/templates/rubric.v1.yaml` (이 표의 YAML 데이터화).

## 4. 다른 브랜드 적용

§1 체크리스트의 제품 특화 항목(`product_FF28_correct`, 앵커 4종)만 새 브랜드로 교체,
§2 규칙은 라벨·조건만 손보면 그대로 재사용. → [[domains/ai-automation]] ad-bdh 스킬,
원본 정리 `picosera/bestofbest/_정리_4점5점/다른브랜드_적용가이드.md`.

## 연결
- [[domains/da-creative]] — 크리에이티브 검수 하네스로 등록
- [[domains/ai-automation]] — ad-bdh 스킬 (bob→dd→harness 일반화)
- [[tacit/creative-patterns]] — 5/4/0점 판정 = 크리에이티브 감각의 명시화
- [[sources/src-creative-autogen-framework]] — 소재 생성 프레임워크 (이 하네스가 검수)
- [[sources/src-instagram-content-research-picosera-2026-05-12]] — 피코세라 콘텐츠 소싱
