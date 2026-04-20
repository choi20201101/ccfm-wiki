---
type: domain
domain: marketing-automation
confidence: high
created: 2026-04-20
updated: 2026-04-20
sources:
  - src-market-research-pipeline-2026-04
  - src-naverapi
  - src-community
---

# 시장조사 플레이북 (Market Research Playbook)

> **🔥 글로벌 지식**: 사용자가 "시장조사 해줘" 계열 요청 시 **바로 이 파일 구조대로 진행**할 것.
> 참조 성공사례: [[src-market-research-pipeline-2026-04]]

---

## 0️⃣ 입력 수집 단계 (건너뛰지 말 것)

사용자에게 반드시 확인할 4가지:

1. **조사 주제·카테고리** (예: 주름, 탈모, 다이어트, 기미)
2. **제품 링크 or 제품 캔버스 MD** (pd/01_product_kpi_usp.md 같은 사전자료 있는지)
3. **출력 위치** (기본값: `~/Desktop/{주제}_시장조사/` 하위)
4. **타깃 인사이트 요구**: 영상기획용? 쇼핑몰 상세페이지용? 경쟁사 브랜드 발굴용? 세 용도는 **출력 구조가 다름**

---

## 1️⃣ 설치·환경 확인

```bash
python --version   # 3.11+ 권장
pip list | grep -iE "requests|openpyxl|playwright|docx|cloudscraper|bs4|instagrapi"
```

필수 패키지: `requests openpyxl playwright python-docx cloudscraper beautifulsoup4 instagrapi`

Playwright 브라우저 설치: `playwright install chromium`

---

## 2️⃣ API 키 확인 (api.txt 파싱)

표준 포맷 (`bol/api.txt`):
```
네이버데이터랩API-1
Client ID=...
Client Secret=...

네이버검색광고API
CUSTOMER_ID=...
엑세스라이선스=...
비밀키=...

카카오키
API=...

인스타그램 아이디
ID : ...
pw : ...
```

⚠️ **체크포인트**:
- 네이버 오픈API "검색" scope 활성화 여부 (developers.naver.com/apps)
  - 미활성화 시 `cafearticle` 401 → 카카오·네이트판으로 대체
- 인스타 로그인 실패 시 즉시 사용자에게 알림, 커뮤니티 데이터로 커버

---

## 3️⃣ 수집 파이프라인 (병렬 실행)

### 3-A. 네이버 급등 키워드 (카테고리 기반)
```bash
python scan_surge.py --title {주제} \
  --cats "카테고리1:CID1,카테고리2:CID2" --months 6
```
> ⚠️ 카테고리 TOP500이 주제와 안 맞으면 (예: 스킨케어 TOP500은 오일·향수) 다음 단계로 넘어갈 것.

### 3-B. 시드→연관키워드→6개월 트렌드 (**권장 핵심**)
```bash
python find_by_related_keywords.py
```
- 시드 20개 → 연관키워드 1,000+ → 상위 250 트렌드 → 저점폭증 + 최근피크 필터
- **저장된 JSON으로 재필터링만으로 브랜드 제외 무한 반복 가능** (`refilter_trends.py`)

### 3-C. 소비자 발언 수집 (병렬)
| 채널 | 스크립트 | 소스 |
|------|---------|------|
| 다음카페 | `collect_daum_kakao.py` | 카카오 검색 API |
| 네이트판 | `collect_community.py --sites natepann` | HTML |
| 네이버 카페/블로그 | `collect_naver_search.py` | cafearticle API (scope 필수) |
| 인스타 | `collect_instagram.py` | instagrapi |
| 유튜브 | `collect_youtube.py` | Playwright |

→ 모두 `output/raw/*.jsonl` 로 저장

### 3-D. 7대 인사이트 매칭
```bash
python analyze_insights.py
```
7 카테고리: **통념·근거·권위·배경·장소·물건·원초적 욕망**
→ `output/reports/07_광고소재_인사이트.md` 생성

### 3-E. 메타 광고 라이브러리 경쟁사 분석
```bash
python make_meta_xlsx.py                 # 브랜드/키워드 리스트
python scrape_meta.py --title {주제} --brands-xlsx ~/Desktop/{주제}_신규브랜드_TOP30.xlsx
python collect_text.py --title {주제}    # 카피 텍스트 재수집
python analyze_pattern.py --title {주제} # 훅·CTA·키워드 집계
```

---

## 4️⃣ 표준 출력 구조 (영상기획용 · 11파일)

출력: `{bol_video}/see/00~11.md` (각 <150줄 엄수)

| # | 파일 | 내용 |
|---|------|------|
| 00 | 개요_목차_임원요약 | 3줄 요약 + 쉬운 말 치환표 |
| 01 | 유튜브_트렌드_제목_아키텍처 | 제목 4패턴 + 제품 적용 |
| 02 | 영상_서사_5단계 | 내얘기→다르다→진짜야→와된다→지금사자 |
| 03 | 성분_트렌드_설득근거 | 5대 성분 + 소비자 언어 |
| 04 | 홈케어_vs_시술_포지셔닝 | 돈·근본·걱정제거 3축 |
| 05 | 구매_트리거 | 감각·숫자·권위·손실회피 4방아쇠 |
| 06 | 경쟁사_메타광고_매트릭스 | 브랜드별 집행량·훅·CTA |
| 07 | 저점폭증_시장신호 | 키워드 TOP 15 성장률 |
| 08 | 영상기획_템플릿10종 | 15~60초 대본 10개 |
| 09 | 카피_시드뱅크 | 훅10·본문10·CTA10 |
| 10 | 7대인사이트_연상체인 | 고객말 + 5체인 |
| 11 | 참고자료_출처 | 파일·API·URL 전부 공개 |

---

## 5️⃣ 쉬운 말 치환 규칙 (모든 리포트 공통)

사용자 피드백 누적 결과. 아래 표현은 **무조건 치환**:

| 어려운 말 | 쉬운 말 |
|-----------|---------|
| 지방 세포 증식 | **꺼진 자리 깨우기** (⚠️ 살찐다 오해 방지) |
| 지방층 침투 | 피부 속 깊이 스며들어 |
| 초저분자·나노 입자 | 엄청 작은 알갱이 |
| 세포 간 신호 전달체 | 피부 세포끼리 주고받는 신호 |
| 인텔리전트 미니멀리즘 | 한 병으로 끝 |
| 경제적 승리감 | 돈 아낀 기분 |
| 노화로 인한 사회적 지위 하락 공포 | 늙어 보여서 주눅드는 마음 |
| 부작용 회피 심리 | 멍·붓기 걱정 없애기 |
| 구조적 개선 vs 데일리 유지 | 근본 바꾸기 vs 매일 챙기기 |
| 보록시핀/Voluplus | **보르피린** (한 가지로 통일) |

→ 새 주제에서 유사 전문용어 나올 때마다 이 표 확장.

---

## 6️⃣ 브랜드 제외 체크리스트 (자동 적용)

### 기본 MAJOR (주름·스킨케어 기준)
설화수·아이오페·헤라·라네즈·이니스프리·에뛰드·마몽드·아모레퍼시픽·더후·오휘·빌리프·더페이스샵·에스티로더·랑콤·시슬리·클리니크·바비브라운·샤넬·디올·입생로랑·톰포드·조말론·겔랑·비오템·올레이·니베아·뉴트로지나·세타필·유세린·바이오더마·아벤느·미샤·토니모리·클리오·페리페라·에스쁘아·롬앤·웨이크메이크·닥터지·AHC·바닐라코·스킨푸드·메디힐·에이바이봄·메디필·셀퓨전씨·비타브리드·라로슈포제·이솝·마데카·센텔리안24·수려한·닥터자르트·피지오겔·키엘·일리윤·코스알엑스·로레알·바셀린·도브·미쟝센·톤28·맥스올인원·프라나롬·**시드물**

### 동적 확장 규칙
- 사용자가 "~는 너무 유명해", "~ 뺴야함" 발언 시 **즉시 MAJOR에 추가 + `refilter_trends.py` 재실행**
- API 재호출 비용 0 (저장된 JSON 재필터만)

---

## 7️⃣ 트렌드 필터 표준값

| 필터 유형 | 기준 | 목적 |
|-----------|------|------|
| 저점 → 폭증 (strict) | 6개월 전 = 0, 최근 ≥ 300 | 진짜 신생 (건수 적음) |
| **저점 → 폭증 (실용)** | **저점 < 100, (최근 or 피크) ≥ 300** | **권장 기본값** |
| 최근 3개월 피크 | 후반 평균/전반 평균 > 1.3, 피크 > 500 | 성장 중 경쟁사 |

---

## 8️⃣ Gemini Deep Research 통합 전략

### 현재 (2026-04)
- Deep Research는 **앱 전용 기능**, 별도 API 없음
- 대안: **Gemini 2.5 Pro + `google_search` grounding tool** (Vertex AI / AI Studio)

### 실무 권장 하이브리드
```
[Phase 0] 사용자가 Gemini 앱 Deep Research 수동 실행 → docx/pdf 저장
          → `see/` 폴더에 원본 투입
          → Claude가 읽어 배경·narrative로 활용
[Phase 1~] 본 파이프라인으로 한국 실데이터 수집·분석
[Phase 최종] 두 소스 통합해 영상기획 MD 생성
```

### 에이전트 루프 자작 (API로 Deep Research 유사 기능)
```python
# pseudocode
plan = gemini("주제X 시장조사 계획 수립")
for q in plan.subquestions:
    results = gemini(q, tools=[google_search])
    notes.append(results)
final_report = gemini("다음 노트를 narrative로 합성", notes)
```

### 향후 Deep Research API 출시 시
- `tacit/coding-lessons.md` §"Gemini Deep Research API" 섹션 신설
- `find_by_related_keywords.py` Phase 0에 DR 자동 호출 추가

---

## 9️⃣ 실행 체크리스트 (신규 시장조사 요청 받았을 때)

- [ ] 1. 입력 확인 (주제·제품·출력위치·용도)
- [ ] 2. Python/Playwright 환경 체크
- [ ] 3. `api.txt` scope 검증 (네이버 검색·카카오·인스타)
- [ ] 4. 시드 키워드 20개 정의 → `find_by_related_keywords.py` 실행
- [ ] 5. 다음카페·네이트판·유튜브 병렬 수집 (instagrapi 실패 시 건너뜀)
- [ ] 6. 7대 인사이트 매칭 + 브랜드 추출
- [ ] 7. 메타 광고 라이브러리 크롤 (TOP 브랜드 xlsx 기반)
- [ ] 8. 사용자에게 브랜드 제외 컨펌 (유명 브랜드 체크)
- [ ] 9. 11개 MD 파일 출력 (각 <150줄, 쉬운 말 치환)
- [ ] 10. 위키 업데이트 (새 케이스 → `sources/src-market-research-{주제}-{날짜}.md`)

---

## 🔗 관련 위키

- [[src-market-research-pipeline-2026-04]] — 이 플레이북의 성공 원본 케이스
- [[marketing-automation]] — 상위 도메인
- [[src-naverapi]] — 네이버 API 인증·엔드포인트 상세
- [[src-community]] — 커뮤니티 크롤러 모듈
- [[creative-patterns]] — 카피·소재 감각 적용
- [[psychology-insights]] — 설득 심리학 (7대 인사이트 근거)
