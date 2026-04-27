---
aliases: ["USP 퍼포먼스 캔버스 조사", "USP 조사", "랜딩 USP 조사", "퍼포먼스 캔버스 조사"]
type: domain
domain: marketing-research
confidence: high
created: 2026-04-27
updated: 2026-04-27
sources:
  - src-charde-melapeel-usp-2026-04-27
  - market-research-playbook
related:
  - marketing
  - market-research-playbook
  - da-creative
  - content-ai-automation
---

# USP 퍼포먼스 캔버스 조사 플레이북

> **🔥 글로벌 지식**: 사용자가 **"USP 조사해줘 + 링크"** 또는 **"USP 퍼포먼스 캔버스 조사"** 계열 요청을 하면 **바로 이 파일 구조대로** 진행할 것.
> 입력: **랜딩페이지 URL 1개** (+ 선택적으로 담당자가 준 타깃·페인포인트·전환반응 카피 텍스트)
> 출력: **`docs/{제품}_brief.md` 인덱스 + `docs/{제품}/01~07_*.md` 7파일** + `refs/{제품}_landing/`(원본) + `refs/{제품}_landing_ocr/`(리사이즈본)
> 참조 성공 케이스: [[src-charde-melapeel-usp-2026-04-27]]

---

## 0️⃣ 입력 수집 (반드시 확인)

| # | 질문 | 기본값 |
|---|---|---|
| 1 | **랜딩페이지 URL** | (필수) |
| 2 | **제품 코드명/슬러그** (출력 폴더 이름) | URL 끝 product_no 또는 사용자 지정 |
| 3 | **출력 위치** | `~/Desktop/{프로젝트}/docs/{slug}_brief.md` + `~/Desktop/{프로젝트}/refs/{slug}_landing/` |
| 4 | **담당자 사전 자료** (타깃·전환 카피·페인포인트·이미지 가이드) | 있으면 본문에 그대로 포함, 없으면 6번 섹션 비워두고 진행 |
| 5 | **리뷰 위젯 동적 데이터 필요?** | 기본 NO. 필요하면 Playwright 별도 수집 단계 추가 |

> ⚠️ 담당자 자료가 있으면 **자료↔페이지 근거 매핑 섹션(07)이 핵심 가치**가 됨. 없으면 06 섹션은 "미수집" 처리.

---

## 1️⃣ 1단계 — 캔버스 카피·이미지 URL 수집 (WebFetch 1회)

```
WebFetch(url=<랜딩 URL>, prompt=<아래 프롬프트>)
```

**프롬프트 템플릿** (그대로 사용):
```
이 페이지는 ____ 랜딩페이지(퍼포먼스 캔버스). 다음을 모두 추출:
1. 메인 헤드라인/카피
2. 캔버스 요소 - 헤드라인, 서브카피, 후킹문구, CTA, 강조 숫자/통계
3. 상세페이지에 포함된 모든 이미지 URL (img 태그의 src/srcset 전부)
4. 리뷰 위젯 최상단 소구점/페르소나 텍스트
5. 가격, 옵션, 프로모션, 구성
6. 페이지 전체 카피를 순서대로
가능한 모든 raw HTML/텍스트와 이미지 src를 빠짐없이 나열.
```

추가로 정적 HTML도 직접 파싱:
```bash
curl -s -A "Mozilla/5.0" "<URL>" -o /tmp/page.html
grep -oE '<script type="application/ld\+json">[^<]+' /tmp/page.html
```
- JSON-LD `Product`/`AggregateRating`에서 평점·리뷰수·가격 옵션·item_code 추출
- `<iframe>`, `snap_widget`, `crema_widget` 등 비동기 리뷰 위젯 감지

---

## 2️⃣ 2단계 — 상세페이지 이미지 일괄 다운로드

이미지 URL 목록을 받았다면 (보통 카페24 `/web/upload/category/editor/.../page/{ver}/{nn}.{jpg|gif}`), 한 번에 받기:

```bash
mkdir -p ~/Desktop/{proj}/refs/{slug}_landing
cd ~/Desktop/{proj}/refs/{slug}_landing
for f in 01.jpg 02.gif 03.gif ...; do
  curl -s -o "$f" "<base>/{f}"
done
```

> **카페24 패턴 팁**: 폴더 `page/{YYMMDDver}/` 안에 `00_01.jpg`, `01.jpg`, `02.gif`, `04_01.jpg`, `04_02.gif`, `05_all.jpg` 등 번호 분할. 누락된 번호는 일반적으로 없음.

---

## 3️⃣ 3단계 — OCR 친화 리사이즈 (≥2000px → 1500px, GIF는 첫·마지막 프레임 분리)

**왜 필요한가**: subagent의 multimodal Read는 한 컷 2000px 초과 시 거부됨. 첫 시도에서 막히면 시간 낭비. 처음부터 무조건 리사이즈.

`scripts/_resize_for_ocr.py` (재사용 표준):
```python
from pathlib import Path
from PIL import Image, ImageSequence
SRC = Path("refs/{slug}_landing")
DST = Path("refs/{slug}_landing_ocr"); DST.mkdir(exist_ok=True)
MAX = 1500
def shrink(im):
    w, h = im.size
    if max(w, h) <= MAX: return im
    s = MAX / max(w, h)
    return im.resize((int(w*s), int(h*s)), Image.LANCZOS)
for f in sorted(SRC.iterdir()):
    with Image.open(f) as im:
        if f.suffix.lower() == ".gif":
            frames = list(ImageSequence.Iterator(im))
            shrink(frames[0].convert("RGB")).save(DST/(f.stem+"_first.jpg"), "JPEG", quality=80)
            shrink(frames[-1].convert("RGB")).save(DST/(f.stem+"_last.jpg"), "JPEG", quality=80)
        else:
            shrink(im.convert("RGB")).save(DST/(f.stem+".jpg"), "JPEG", quality=82)
```

확인: `du -sh refs/{slug}_landing_ocr` → 보통 3~5MB로 떨어짐.

---

## 4️⃣ 4단계 — Subagent OCR 일괄 (3장씩 병렬, 형식 강제)

`Agent(subagent_type="general-purpose")` 호출. 프롬프트 포인트:
- 폴더 경로 명시
- **3장씩 병렬 Read** (메모리 부담 방지)
- 출력 형식 강제 (아래 템플릿)
- 마지막에 **"카피 핵심 추출(병합)" 섹션 필수**

**출력 강제 템플릿**:
```
### {파일명}
- **유형**: 헤더 / 후킹 / 본문 / 비교(B&A) / 사용법 / 성분/특허 / 임상수치 / 후기 / 옵션·가격 / 산더미컷 / 모델컷 / 라벨
- **카피 (raw)**:
  - 줄바꿈 단위로 그대로
- **시각**: 한 줄 (모델/제품/그래프 묘사)
```

> ⚠️ **의역·요약 금지** 명시. raw 카피 보존이 자산 가치의 핵심.

---

## 5️⃣ 5단계 — 리뷰 위젯 분석 (현재는 메타 + OCR 후기 카드로 대체)

대부분 카페24 쇼핑몰은 SnapReview / 크리마 / 알랭 같은 **비동기 JS 위젯**. 정적 fetch에서는 본문 추출 불가.

| 위젯 | 도메인 | 가능 / 한계 |
|---|---|---|
| SnapReview | snapfit.co.kr / snapvi.co.kr | JSON-LD `aggregateRating`만 정적 추출 가능. 별점 분포·키워드·페르소나 위젯은 Playwright 필요 |
| 크리마(CREMA) | review.cre.ma | iframe src만 정적 추출 |
| 알랭(Alainn) | api.alainn.io | 메타만 |

**대체 전략**: 페이지 내 상세이미지 컷 중 보통 1~2장은 **브랜드 큐레이션 후기 카드**(예: `05_all.jpg`의 "BRAND REAL REVIEW")로 박혀 있음. 이게 사실상 "리뷰 영역 진입 시 최상단 노출" 역할이니 OCR 결과를 5번 섹션 소구점으로 정리.

**페르소나 단서 추론 포인트**:
- 후기 어조에서 연령대 추정
- 모델 셀렉션 (한국/외국인/연령대 분포)
- 평점 분포 (3점대 = 호불호 분명, 4.5+ = 무난한 호평)

---

## 6️⃣ 6단계 — 담당자 자료 통합 (있을 때)

담당자가 준 **타깃·전환반응 카피·이미지 가이드·페인포인트**는 **그대로** 6번 섹션에 박는다 (편집·요약 금지).

표준 4 블록:
1. 타깃 (연령·성별·메인/서브)
2. 전환 반응 요소 — 카피
3. 전환 반응 요소 — 이미지
4. 페인포인트 (보통 3~4축)

> 페인포인트는 **번호 + 한 줄 제목 + 본문** 형태로 받는 게 일반적. 그대로 옮기되, "핵심 축"이 어느 것인지 강조 표시.

---

## 7️⃣ 7단계 — 페이지 ↔ 담당자 매핑표 (가장 큰 가치)

| 담당자 카피/요소 | 페이지 내 즉시 활용 가능한 근거 (컷 번호 + OCR 텍스트) |
|---|---|
| 정량 카피 (예 "31% 개선") | OCR 컷 N에 같은 수치 있음 → 그대로 인용 가능 |
| 페인 #1 ~ #4 | 어느 컷의 어느 텍스트/시각이 매칭되는지 |
| 메인 타깃 (예 여성 40-59) | 어느 컷의 모델·후기 어조가 매칭되는지 |
| 이미지 가이드 (외국인/산더미/B&A) | 페이지 내 해당 컷 번호 |

이 표가 **퍼포먼스 카피 시드를 만들 때 직접 발사대 역할**.

---

## 8️⃣ 출력 구조 (표준)

```
{프로젝트}/
├── docs/
│   ├── {slug}_brief.md            ← 인덱스 (50~60줄, 30초 요약 + 자산 위치)
│   └── {slug}/
│       ├── 01_overview_pricing.md         ~70줄  메타·자산·가격
│       ├── 02_canvas_copy.md              ~50줄  랜딩 헤더 카피·CTA·JSON-LD
│       ├── 03_detail_ocr.md              200~250줄 상세 N컷 OCR
│       ├── 04_copy_assets.md              ~50줄  카피 시드 풀
│       ├── 05_review_widget.md            ~50줄  위젯 메타·소구점·페르소나
│       ├── 06_target_persona.md           ~50줄  담당자 타깃·페인 (있을 때만)
│       └── 07_mapping_followup.md         ~40줄  매핑표 + 후속
└── refs/
    ├── {slug}_landing/                    원본 (jpg/gif)
    └── {slug}_landing_ocr/                ≤1500px 리사이즈본
```

> **인덱스(`{slug}_brief.md`)는 60줄 이내** 엄수. 상세는 모두 서브 폴더로.
> 03(detail_ocr)이 길어지는 건 OK — 컷 수에 비례. 200줄 넘으면 내부에 10개 서브섹션(인트로/페인/임상/후기카드/POINT 1~N/사용법/Q&A·고시)으로 나눔.

---

## 9️⃣ 실행 체크리스트

- [ ] 1. 랜딩 URL 수신 + 출력 폴더·슬러그 결정
- [ ] 2. WebFetch 프롬프트 호출 → 카피·이미지 URL·옵션·JSON-LD 추출
- [ ] 3. `curl` 일괄 다운로드 → `refs/{slug}_landing/`
- [ ] 4. `_resize_for_ocr.py` 실행 → `refs/{slug}_landing_ocr/`
- [ ] 5. Agent OCR 호출 (3장 병렬, 형식 강제)
- [ ] 6. 리뷰 위젯 감지 + 메타/OCR 후기 카드로 5번 섹션 작성
- [ ] 7. 담당자 자료 있으면 6번 섹션 그대로 박기
- [ ] 8. 7번 매핑표 작성 (담당자 자료 ↔ 페이지 근거)
- [ ] 9. 7개 분할 MD + 인덱스 1개 생성
- [ ] 10. 위키 업데이트 — 새 케이스 → `sources/src-{브랜드}-{제품}-usp-{날짜}.md`

---

## 🔁 트리거 패턴

사용자가 다음 표현 중 하나로 부르면 **이 플레이북을 즉시 가동**:
- "USP 조사해줘 [URL]"
- "USP 퍼포먼스 캔버스 조사 [URL]"
- "이 랜딩 USP 정리해줘 [URL]"
- "퍼포먼스 캔버스 조사 [URL]"
- "이 페이지 캔버스 요소 정리해줘 [URL]" (시장조사 플레이북과 헷갈리지 말 것 — 시장조사는 카테고리 단위, USP는 제품 1개 단위)

**시장조사 플레이북([[market-research-playbook]])과 차이**:
| 구분 | 시장조사 플레이북 | USP 퍼포먼스 캔버스 조사 |
|---|---|---|
| 입력 단위 | 카테고리 (주름·탈모·다이어트) | 제품 1개 (랜딩 URL) |
| 데이터 소스 | 네이버·다음·메타광고·유튜브 N채널 | 단일 랜딩 페이지 + 리뷰 위젯 |
| 출력 | 11파일 (시장 트렌드·경쟁사·인사이트) | 7파일 (제품 자체 USP·페인·매핑) |
| 소요 | 30분~수시간 (병렬 크롤) | 5~15분 (단일 페이지) |
| 다음 단계 | 영상기획 / 카테고리 진입 | 카피 시드 → 광고 크리에이티브 생성 |

> 카테고리 조사는 [[market-research-playbook]], **제품 USP 조사는 본 플레이북** 사용.

---

## 🔗 관련 위키

- [[src-charde-melapeel-usp-2026-04-27]] — 첫 케이스 (샤르드 멜라케어 필크림 마스크)
- [[market-research-playbook]] — 카테고리 단위 조사 (대척점)
- [[marketing]] — i-boss 201건 USP·공감·CRM·매체
- [[da-creative]] — 카피 시드를 광고 소재로 변환
- [[content-ai-automation]] — 카피 시드 → 영상기획 연결
- [[creative-patterns]] — 시각 시드(B&A·산더미·외국인 모델) 적용 감각
