---
aliases: ["피코세라 핀터레스트 키워드 확장", "pin 파이프라인 3000 키워드"]
type: source
domain: marketing-automation
confidence: high
created: 2026-05-14
updated: 2026-05-14
related:
  - instagram-content-research
  - todayhumor-mining-playbook
  - market-research-playbook
---

# 피코세라 핀터레스트 레퍼런스 키워드 확장 (2026-05-14)

## 요청

> "핀터레스트에 유머 밈 이미지 모을 건데, `pin/items`에 모아둔 것과 중복 안 되는
> 밈·유머 + 광고소재 아이디어 키워드를 3,000개 선정·정리해서 이미지 시각화 MD로 정리하고,
> 핀터레스트에서 실제 이미지도 다운로드(레퍼런스용)."

## 위치 & 파이프라인 관계

워크스페이스: `C:/Users/gguy/Desktop/gpt/projects/picosera/pin/`

**피코세라 레퍼런스 수집 3형제** — 같은 브랜드, 다른 소스:
| 파이프라인 | 소스 | 워크스페이스 |
|---|---|---|
| `pin/` (본 건) | 핀터레스트 (gallery-dl) | `projects/picosera/pin/` |
| `inset/` | 인스타 8계정 (instaloader) | `projects/picosera/inset/` → [[instagram-content-research]] |
| `todayhumor_ideas/` | 오늘의유머 BoB | `projects/picosera/new/todayhumor_ideas/` → [[todayhumor-mining-playbook]] |

`pin` 파이프라인 구조: `config.yaml` → `scrape.py`(gallery-dl) → `items/NNNN/`(image + source.json) → 서브에이전트가 `idea.md` 작성 → `build_index.py` → `index.md`. 기존 43종 검색어로 1,412개 수집된 상태였음.

## 한 일

### 1. 키워드 생성기 — `scripts/gen_keywords.py`
- 40개 카테고리 × 75개 = **정확히 3,000개**, 기존 44종 검색어와 정규화 기준 **중복 0**
- 실축 결합 방식: 큐레이션한 base(의미 축) × 접미사 풀(검색어화) → 전역 dedup → 카테고리당 75개
- 산출: `keywords_3000.md`(하이브리드 — 카테고리 설명 + 압축 테이블), `config_expanded.yaml`(scrape.py용, 3000 queries × n=4)

### 2. 위키 지식을 카테고리·앵글에 반영 (핵심)
- **피코세라 후킹 A~F**, **7대 자극 후킹**, **B/A 12가지 위트 우회**, **위트축 8종**(반전·공감·의외성·과몰입·능청·정성·집착·디스), **100만뷰 후킹 5선**, **8개 한국 밈 IG 계정 스타일**을 카테고리 설계 + 각 키워드의 '피코세라 활용 앵글' 컬럼에 직접 매핑
- 예: A1 반전·역접 밈 → 후킹2 / B1 타인 리액션·3인칭 목격담 → B/A 우회 #1#3 + viral패턴5 / B2 오브젝트·과일 비유 → B/A 우회 #5#7#8

### 3. `scrape.py` 비파괴 확장
- `main()`이 `argv[1]`을 config 경로로 받도록 수정 (없으면 기존 `config.yaml`)
- `python scripts/scrape.py config_expanded.yaml` 로 확장 수집

### 4. 수집 실행
- 2개 키워드 테스트 통과 (한글·영문 모두 정상, `items/` 1413~1418 추가)
- 3,000개 전체 백그라운드 수집 시작 — `scrape.py`는 폴더 있으면 skip → **resumable**, `normalize()`가 `items/` 1413번부터 pin_id dedup append

## 재사용 포인트

- **실축 결합 생성기 패턴**: base(의미) × suffix(검색어화) → dedup → 카테고리 cap. 어떤 브랜드든 base 리스트만 갈아끼우면 N천 개 키워드 결정론 생성. `gen_keywords.py` 재사용 가능.
- **위키 프레임워크 → 키워드 앵글 매핑**: 수집 단계부터 후킹 패턴을 박아두면, 나중에 `idea.md` 분석 서브에이전트가 일관된 앵글로 작업. 수집과 분석의 결합도를 낮춤.
- **scrape config 분리**: 기존 `config.yaml` 보존 + `config_expanded.yaml` 별도. argv 한 줄로 전환.

## 다음 단계

1. 백그라운드 수집 완료 후 `items/` 총량 확인 (1,418 + 신규)
2. `SUBAGENT_PROMPT.md` 템플릿으로 신규 `items/`에 `idea.md` 분산 작성
3. `build_index.py` → `index.md` 활용도순 갱신
