---
type: source
domain: marketing-automation
confidence: high
created: 2026-04-28
updated: 2026-04-28
sources:
  - C:\Users\gguy\Desktop\naver-competitor-finder\nurse\
---

# 간호사 신발 시장조사 + 착한구두 시너지 — 케이스 스터디 (2026-04-28)

> "naverapi-focused" 시장조사 변종 + 토스 UI 시각 리포트 + 퍼포먼스 마케팅 시너지 분석 — **재사용 표준** (시장조사 플레이북의 "비-화장품 카테고리, 브랜드 시장 단위" 변형 케이스).

---

## 0. 케이스 메타

| 항목 | 값 |
|---|---|
| 카테고리 | 패션잡화 > 여성신발 > 기능화 > 유니폼화 (간호사 신발) |
| 시드 브랜드 | 널핏 / 너스키니 |
| 데이터 기간 | 2024.01 ~ 2026.03 (네이버 데이터랩 + 검색광고 API) |
| 발굴 브랜드 | 55개 |
| 자사몰 심층 분석 | 12개 (병렬 6 에이전트) |
| 페인포인트 분석 | 108건 |
| 산출 파일 | MD 9 + Excel 11시트 + Toss UI HTML 2 |
| 워크폴더 | `C:\Users\gguy\Desktop\naver-competitor-finder\nurse\` |

---

## 1. 4단계 파이프라인 (재사용 표준)

기존 시장조사 플레이북([[domains/market-research-playbook]])이 "화장품 카테고리 11파일 영상기획 산출"이라면, 본 케이스는 **"브랜드 시장 단위 + 자사몰 분석 + 퍼포먼스 마케팅 진입 권고"** 변형.

```
Phase 1 (병렬, ~6분)
├─ Agent A: 브랜드 50+ 발굴 (WebSearch + WebFetch 다채널)
└─ Agent B: 페인포인트 100+건 마이닝 (카페/블라인드/매거진/자사몰후기)

Phase 2 (Python 스크립트, ~3분)
└─ fetch_brand_trends.py — 브랜드별 데이터랩 트렌드(상대비율) + 검색광고 API(절대량) + 역산

Phase 3 (병렬, ~10분)
└─ 6개 자사몰 분석 에이전트 (브랜드 1-3개씩 배분)
    각 에이전트가 슬로건/USP/베스트3/페인→솔루션/사회증거/약점 추출

Phase 4 (직접 작성)
├─ 통합 MD 리포트 (00_FINAL_market_research.md)
├─ Excel 11시트 (페르소나/페인×솔루션/사회증거/권위/통념/카피/경쟁사/가격/검색량/액션)
├─ Toss UI HTML #1 (시장조사 시각 보고서)
├─ Toss UI HTML #2 (시너지 분석, 옵션)
└─ 시너지 분석 MD (3 시나리오 ROAS 비교, 퍼포먼스 마케팅 관점)
```

**시간 총합**: ~25-30분 (병렬 활용 시).

---

## 2. 핵심 재사용 패턴

### 2.1 검색량 역산 공식 ⭐
**문제**: 데이터랩 API는 *상대비율*만 주고, 검색광고 API는 *현재월 절대량*만 줌. 과거 24개월 절대 검색량을 알고 싶다.

**해결**: 현재월 절대량 × (해당월 비율 / 현재월 비율) = 추정 절대량

```python
def reverse_calc_monthly(trend_ratios, current_total):
    """현재월 절대량 + 월별 상대비율 → 월별 추정 절대량."""
    if not trend_ratios or not current_total:
        return {}
    months = sorted(trend_ratios.keys())
    ref = months[-1]  # 가장 최근월 = 검색광고 API 측정월
    ref_ratio = trend_ratios.get(ref, 0)
    if ref_ratio == 0:
        return {}
    return {m: round((trend_ratios.get(m, 0) / ref_ratio) * current_total)
            for m in months}
```

**한계**: ±20% 오차. brand명이 일반명사와 겹치면 noise 큼 (예: "에스티핏=압박스타킹").

### 2.2 데이터랩 일반 검색 API 사용
*쇼핑인사이트*(CID 필요)가 아닌 *일반 검색 트렌드* 사용 — 브랜드 검색 행동에 더 적합.

```python
body = {
    "startDate": "2024-01-01", "endDate": "2026-03-31",
    "timeUnit": "month",
    "keywordGroups": [{"groupName": "널핏", "keywords": ["널핏","Nurfit","널싱화"]}]
}
requests.post("https://openapi.naver.com/v1/datalab/search",
              headers=auth.datalab_headers(), json=body)
```

키워드 그룹은 5개까지, 그룹당 키워드 5개까지. 다중 동의어 묶어서 노이즈 줄임.

### 2.3 병렬 자사몰 분석 디스패치
브랜드 12개를 6개 에이전트에 묶어서 동시 디스패치 (단독 1:1보다 토큰 절감 ~50%).

```
Agent 1: 단독 핵심 1개 (널핏)
Agent 2: 단독 핵심 1개 (너스키니)
Agent 3: 단독 핵심 1개 (뽀너스)
Agent 4: Group A 3개 (너스피아 + 너스뷰티 + 콤포스타)
Agent 5: Group B 3개 (베리슈 + 빅마트 + 페이퍼플레인)
Agent 6: Group C 3개 (우포스 + 슈올즈 + 클로브)
```

**보고 규칙**: 각 에이전트는 *(1) TOP모델+가격 (2) USP 1줄 (3) 파일경로*만 반환. 본문 텍스트 반환 금지 → 컨텍스트 보호.

### 2.4 Excel 11시트 표준 구조 (퍼포먼스 마케팅 진입용)
화장품 영상기획 11파일과 다른 *브랜드 진입 의사결정용* 구조:

| 시트 | 내용 |
|---|---|
| 00. Executive Summary | 카테고리·1위·진입전략 1줄 |
| 01. 타겟 페르소나 | 6 페르소나 × (연령/성별/직군/페인/구매채널/가격대/메시지) |
| 02. 페인×솔루션 | TOP20 페인 → 필수기능/차별기능/경쟁사처리/우리메시지 |
| 03. 사회적 증거 | 20 인용+출처 |
| 04. 권위(Authority) | KFDA/APMA/임상/병원/협회/공공 + 난이도·비용 |
| 05. 통념(Convention) | 깨야할/활용할 분류 |
| 06. 후킹 카피 풀 | 페르소나×페인×채널 매핑 |
| 07. 경쟁사 매트릭스 | USP/강점/빈자리/우리차별점 |
| 08. 가격 전략 | 5단 가격사다리 + 화이트스페이스 강조 |
| 09. 검색량 트렌드 | TOP30 + 24M 성장률 + 시사점 |
| 10. 진입 액션 플랜 | 0-78주 9단계 (임상→인증→개발→브랜드→사전판매→출시→B2B→확장→KPI) |

생성기: `nurse/generate_excel_report.py` (openpyxl, 토스 컬러 적용).

### 2.5 Toss UI HTML 시각 리포트 ⭐
[[domains/da-creative]]의 dig 스킬 (huashu-design-kr) 가이드 직접 적용:
- `<html lang="ko">` + Pretendard Variable
- 컬러 팔레트: `#3182F6` primary / `#191F28` text / `#1AC069` success / `#F04452` error / `#F59E0B` warn
- 타이포: `word-break: keep-all`, `letter-spacing: -0.02em`, `line-height: 1.6`
- 컴포넌트: sticky header(backdrop blur), eyebrow + hero, KPI 4-strip, 12-20px rounded card

**섹션 표준**: HERO → CATEGORY → PAIN POINTS → SEARCH TREND → PERSONA → BRAND DEEP DIVE → WHITESPACE → AUTHORITY → CONVENTION → HOOKING COPY → ACTION PLAN.

### 2.6 시너지 분석 3 시나리오 매트릭스 (퍼포먼스 마케팅 관점)
기존 브랜드(예: 착한구두)에 신규 라인 런칭 가부 판단 시 사용.

| 시나리오 | 가격대 | CAC | ROAS | BEP | 12M 매출 | 흑자 가능성 |
|---|---:|---:|---:|---:|---:|---:|
| A. 메인 라인 직접 출시 | ±20% | -50% | 2.5~3.0x | 4-6개월 | 8억 | 80% |
| **B. 서브브랜드** ★ | 3단 사다리 | -40% | 2.0~2.5x | 12-14개월 | 18억 | 65% |
| C. 완전 신규(자회사) | 프리미엄 | 100% | 1.2~1.5x | 24개월+ | 12억 | 15% |

**판정 기준**: 모브랜드 가격대(M)와 신규 카테고리 권장가(N)의 차이가 1.5x 이상이면 시나리오 B 강력 추천. 같으면 A, 3x 이상이면 C.

### 2.7 PRO/CON 시너지 매트릭스 (체크리스트)
**PRO 7대 축**:
1. 타깃 연령/성별 일치도
2. 핵심 가치(슬로건) 매칭도
3. 기존 라인 중 신 카테고리 페인과 직결되는 SKU 유무
4. 다채널 인프라
5. SNS 팔로워
6. 가격대 호환 (페르소나 일부)
7. 운영 인프라(MD/물류/CS) 공유 → CAC 절감폭

**CON 6대 축**:
1. 브랜드 정체성 충돌(패션 vs 의료, 푸드 vs 헬스 등)
2. 가격 매트리프 미스매치
3. 카테고리 권위 자산 부재(인증/임상/협회)
4. 성별 라인 부재(남성/여성)
5. 신규 카테고리 커뮤니티 인지도
6. 핵심 타깃 페르소나 미스매치

---

## 3. 도구 카탈로그 (재사용 가능)

### 3.1 `fetch_brand_trends.py`
- **위치**: `naver-competitor-finder/nurse/fetch_brand_trends.py`
- **입력**: `data/brands.json` (브랜드 + search_keywords 배열)
- **출력**: `data/datalab_trends.json`, `data/searchad_volumes.json`, `data/brand_volume_timeseries.json`, `reports/03_search_volume_trend.md`
- **의존**: `naver-competitor-finder/scripts/config.py`의 `NaverAuth` (HMAC-SHA256 서명 + DataLab Client ID 라운드로빈)
- **속도**: 55 브랜드 ~3분

### 3.2 `generate_excel_report.py`
- **위치**: `naver-competitor-finder/nurse/generate_excel_report.py`
- **출력**: 11시트 xlsx (위 2.4 표 참조)
- **의존**: openpyxl 3.x
- **스타일**: 토스 컬러 적용, header `#1F4E78`, sub `#D9E1F2`, highlight `#FFF2CC`, warn `#FCE4D6`

### 3.3 Toss UI HTML 템플릿 (단일 페이지)
- **참조 샘플**: `naver-competitor-finder/nurse/reports/report.html`
- **시너지 변형**: `naver-competitor-finder/nurse/reports/report_synergy.html`
- **CSS 토큰** 핵심 변수만 복사하면 다른 케이스에 즉시 적용 가능 (CSS-in-HTML, 외부 의존 0)

---

## 4. 본 케이스 핵심 발견 (도메인 지식)

### 4.1 한국 간호사 신발 시장 구조
- **D2C 코어 11개 + 글로벌 16개 + 외래/관리직 7개 + 유니폼몰 부속 6개 + 종합/PB/협업 15개 = 55개**
- **D2C 1위**: 널핏(Nurfit) — 24M +196.5% / 10,450/월 / 가격 65,400원 (한국 D2C 상한)
- **회복화 1위**: 우포스 +61% / 41,770/월 / 한국 자사몰+무신사 입점
- **의료기기 인증 1위**: 슈올즈 KFDA 2등급 / +109.6%
- **클로브(미국)**: #1 Healthcare Pro Shoes 직구 22만원 — 한국 진출 안 함

### 4.2 화이트스페이스 (12-18만원 한국형 프리미엄)
- 널핏 65,400원이 한국 D2C 상한, 호카·클로브·단스코는 22만원대 직구 → **8만~14만원 가격 공백**.
- 추가 빈자리: 남성 간호사 라인, 수술실 미끄럼방지 D2C, B2B 병원 단체구매, 한국형 리커버리.

### 4.3 1번 페인 = 12시간 후 발통증 + 종아리 부종 + 발냄새 (3종 세트)
- 의학적으로 족저근막염·하지정맥류 직전 단계 만성 직업병.
- 솔루션 5박자: 아치서포트 + 발볼 옵션(EE/EEE) + 록커솔 + 150g 이하 + 통기·항균.

### 4.4 착한구두 시너지 결론
- (주)45스페이스 운영, 슬로건 "편하다 그리고 착하다", 가격 25,900~45,900원.
- 시너지 시나리오 B(서브브랜드) 권장 — KFDA + 임상 200명 + 서브 인스타 분리 3개는 절대 양보 불가.
- 12M 매출 추정: A 8억 / **B 18억** / C 12억.

---

## 5. 다음 진입자가 받아갈 체크리스트

새로운 카테고리·시장 분석 시작할 때 본 케이스 그대로 따라하기:

1. ☐ 시드 브랜드 2-3개 + 카테고리명 확정
2. ☐ `nurse/` 같은 워크폴더 생성 (`{reports,data,raw,assets}` 4개 서브폴더)
3. ☐ Phase 1 병렬 디스패치 — 브랜드 발굴 + 페인포인트 마이닝 (각 에이전트에 산출 파일 경로 명시)
4. ☐ Phase 2 — `fetch_brand_trends.py` 변형해서 실행 (data/brands.json 입력)
5. ☐ Phase 3 — 상승세 브랜드 6 그룹으로 병렬 분석 (단독 핵심 3 + 그룹 3)
6. ☐ Phase 4 — 통합 MD → Excel 11시트 → Toss UI HTML 단계로 작성
7. ☐ (옵션) 모브랜드와 시너지 분석 — PRO 7 / CON 6 / 3 시나리오 ROAS 비교
8. ☐ 위키화 — 본 페이지를 새 케이스용 source로 복제

---

## 6. 학습된 암묵지 (이 케이스에서 추출)

→ [[tacit/coding-lessons]] §검색량 역산 / §토스 UI 리포트 템플릿
→ [[tacit/operational-heuristics]] §브랜드 시너지 3 시나리오 매트릭스
→ [[tacit/creative-patterns]] §시각 리포트 11섹션 표준
