---
type: raw
captured_at: 2026-05-14
source_path: C:/Users/gguy/Desktop/gpt/projects/picosera/bestofbest/harness/rubric.md
---

# 피코세라 광고 소재 점수 루브릭 v1 (원본)

> 추출 원본: 230장 사전 분류 (19개 폴더). 비전 평가는 eval 서브에이전트로 격리 수행.
> 제품: 페이스팩토리 피코세라 FF-28 (핸드헬드 LED 토닝 디바이스).
> 1차 검수로 371장 분류 완료 → `bestofbest/_정리_4점5점/` 산출.

## 0. 평가 체크리스트 (Vision JSON 반환 스키마)

headline_position(top/center/bottom/none), headline_weight(ultra-bold/bold/regular/none),
headline_screen_ratio_pct(0~100), headline_is_meta_or_witty(bool), text_density(low/medium/high/wall-of-text),
text_columns(int), copy_present(yes/no/illegible), copy_is_spec_label_only(bool), copy_natural_sentence(bool),
handwritten_or_ugc_tone(bool), clinical_73_present(bool — 73.93%/73%), price_anchor_present(bool — 9만원대/1/10),
speed_anchor_present(bool — 1조분의1초/3분), tech_anchor_present(bool — 피부과 4종/피코초),
model_count(int), device_count(int), product_FF28_correct(yes/no/wrong), before_after_layout(bool),
personification(none/cute/grotesque), multi_layer_composite(bool), badge_or_tape_layers(bool),
lifestyle_natural_lighting(bool), dl_keyvisual_tone(bool), visual_polish(low/medium/high), main_signal_one_line(str)

## 1. 점수 결정 규칙 (우선순위 상→하, 첫 매칭으로 확정)

| 순위 | 라벨 | 점수 | 조건 (must all true) |
|---|---|---|---|
| 1 | 문제있음 | 0 | personification=="grotesque" OR product_FF28_correct=="wrong" |
| 2 | 글자가많아 | 0 | text_density=="wall-of-text" OR text_columns>=4 |
| 3 | 아쉬운거카피없어서 | 0 | copy_present!="yes" OR copy_is_spec_label_only==true |
| 4 | 카피이상한거+DL이미지만 | 0 | dl_keyvisual_tone==true AND clinical_73_present==false |
| 5 | 위트5점 | 5 | headline_is_meta_or_witty==true AND clinical_73_present==true |
| 6 | 베스트디벨롭5점 | 5 | multi_layer_composite==true AND (clinical_73 OR price_anchor) AND headline_weight=="ultra-bold" |
| 7 | 캐릭터5점 | 5 | personification=="cute" AND headline_weight in [ultra-bold,bold] |
| 8 | 네이티브5점 | 5 | handwritten_or_ugc_tone==true AND model_count==0 |
| 9 | 텍스트강조4점 | 4 | badge_or_tape_layers==true AND (clinical_73 OR price_anchor) |
| 10 | 분위기톤4점 | 4 | lifestyle_natural_lighting==true AND text_density in [low,medium] |
| 11 | 비포에프터4점 | 4 | before_after_layout==true |
| 12 | 단체컷4점 | 4 | model_count>=2 OR device_count>=2 |
| 13 | 네이티브4점 | 4 | copy_natural_sentence==true AND text_density!="wall-of-text" |
| 14 | 점수3점 | 3 | anchors_count>=2 AND model_count>=1 AND product_FF28_correct=="yes" |
| 15 | 점수2점 | 2 | anchors_count==1 AND copy_present=="yes" |
| 16 | 점수1점 | 1 | model_count>=1 AND anchors_count==0 AND product_FF28_correct=="yes" |
| 17 | 점수1점(fallback) | 1 | 위 어느 것에도 안 걸리면 1점 (수동 확인 대상) |

anchors_count = clinical_73 + price + speed + tech 중 true 개수.

## 2. 비전 평가 분리 룰
- Vision 호출은 메인 컨텍스트에서 직접 Read 금지. score.py가 Gemini API 직호출 + 스키마 강제 JSON.
- 각 호출 독립 워커. temperature=0.1 (재실행 결정론).
- JSON parse 실패는 state/failed.jsonl 보존, 점수 미부여.

## 일반화 (ad-bdh 스킬)
이 루브릭은 `~/.claude/skills/ad-bdh/templates/rubric.v1.yaml` 로 데이터화됨.
checklist/anchors/rules 3블록 YAML — 코드 수정 없이 기준 교체 가능 (v2, 프로파일 추가).
