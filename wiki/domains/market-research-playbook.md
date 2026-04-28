---
aliases: ["시장조사 플레이북"]
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
> 참조 성공사례:
> - [[src-market-research-pipeline-2026-04]] — 1·2단 (주름/유쎄라블)
> - **[[src-rubyrn-glow-deep-research-success-2026-04-28]] — 1~4단 심화 (광채/PDRN, 신 표준)** ⭐
>
> ⭐ **2026-04-28 업데이트**: 본 플레이북은 이제 **4단 심화** 구조. 3단(영상 자막+썸네일) + 4단(민간 속설) 추가됨.
> 시장조사 요청 받으면 묻지 말고 4단까지 진행 — 본 케이스가 사용자 승인 표준.

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

## 3-F. 영상 자막+썸네일 1차 분석 (3단, 2026-04-28 신 표준) ⭐

> 영상 메타·댓글만으로는 **"실제 영상 안에서 한 말"** 못 잡음. yt-dlp + Claude Read 조합이 답.

### 도구
- `yt-dlp` Python 모듈 (이미 설치됨: `python -c "import yt_dlp"` 확인)
- 자체 스크립트: [[src-rubyrn-glow-deep-research-success-2026-04-28]] §A (`deep_video_analysis.py`)

### 실행
```bash
python deep_video_analysis.py
# TARGETS = [(name, url), ...] 리스트만 카테고리에 맞게 수정
# 자동: 자막 srt + 썸네일 jpg + 메타 json
```

### 시각 분석 (Claude Read)
- 다운받은 jpg를 Read 도구로 직접 읽음 → vision으로 텍스트·구도·소품·표정 추출
- OCR 불필요 (한국어 손글씨까지 읽힘)
- 권장: **조회수 TOP 5만 분석** (시간 절약, 다른 후킹 유형 분포 우선)

### 산출
- `scripts/video_deep/subs/*.ko.srt` (자막)
- `scripts/video_deep/thumbs/*.jpg` (썸네일)
- `scripts/video_deep/meta.json` (조회수·duration·like·comment_count)
- → MD: `canvas/05_viral_video_deep_analysis.md`

---

## 3-G. 민간 속설/통념 정제 (4단, 2026-04-28 신 표준) ⭐

### 의도
한국 소비자 머릿속 깊이 박힌 미용 통념 (쌀뜨물=미백, 꿀=보습 등) → **"통념 얹기" 카피**의 직접 인풋.

### 시드 키워드 (60+ 성분 + 14 카테고리)
```python
INGREDIENTS = ['쌀뜨물','우유','달걀','오이','꿀','녹차','토마토','감자','당근','호박',
               '요거트','벌꿀','율무','식초','두부','버섯','인삼','홍삼','녹두','석류',
               '상백피','쑥','막걸리','블루베리','수박','복숭아','자몽','아보카도',
               '다시마','미역','감초','유자','매실','참기름','커피','뽕잎','계피',
               '강황','국화','대추','잣','호두','파인애플','연꽃','연잎','코코넛',
               '오트밀','시금치','약쑥','어성초']

CATEGORIES = ['민간요법','녹차 미백','미백','할머니 미용','꿀팩','토마토 피부',
              '당근 피부','피부 천연','달걀팩','우유팩','감자팩','꿀 피부',
              '바나나팩','꿀템','오이팩','쌀뜨물','찐꿀템','꿀광 만드는법']
```

### 실행
```bash
# 시드 변경 후 재크롤
python -u collect_daum_kakao.py --keywords "{60개 성분}" --months 12
python -u collect_community.py --keywords "{18개 카테고리}" --sites natepann --months 24

# 정제 (정규식 패턴)
python -c "..."  # 본 케이스 참조: scripts/folk_beliefs.json 추출 코드
```

### 카피 직변환 공식
```
[옛 비법 호명] + [그 비법의 한계 인지] + [신제품의 진화 약속]

예: "엄마는 쌀뜨물로, 저는 PDRN 30병으로"
    "감자 갈 시간 30분 → 거품 30초"
    "이영애가 감자팩이었다면, 우리는 PDRN 30병"
```

### 산출
- `scripts/folk_beliefs.json` (성분별 컨텍스트 60+)
- `scripts/folk_belief_phrases.json` (명시 phrase)
- `scripts/folk_titles_by_cat.json` (카테고리별 발화)
- → MD: `canvas/06_folk_beliefs_for_glow.md` (속설 200+ + 카피 80선)

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

## 9️⃣ 실행 체크리스트 (2026-04-28 4단 심화 표준) ⭐

> 사용자 승인 표준 ([[src-rubyrn-glow-deep-research-success-2026-04-28]]).
> 시장조사 요청 받으면 **묻지 말고** 1~4단 모두 진행.

### 1단 — 검색·트렌드
- [ ] 1. 입력 확인 (주제·제품·출력위치·용도)
- [ ] 2. Python/Playwright 환경 체크 + `import yt_dlp` 확인
- [ ] 3. `api.txt` scope 검증 (네이버 검색·카카오·인스타)
- [ ] 4. 시드 키워드 20개 정의 (공백 제거 필수) → `find_by_related_keywords.py` / `keywordstool` 실행
- [ ] 5. YoY 트렌드 추출 (24개월 윈도우, 데이터랩)

### 2단 — 소비자 발화 (라이트 크롤)
- [ ] 6. 다음카페·네이트판·유튜브 병렬 수집
- [ ] 7. 7대 인사이트 매칭 (analyze_insights.py) + 브랜드 추출
- [ ] 8. 메타 광고 라이브러리 크롤 (TOP 브랜드 xlsx 기반)

### 3단 — viral 영상 1차 분석 (NEW) ⭐
- [ ] 9. YouTube 검색 결과 중 조회수 10만+ 영상 10건 선정 (제목 키워드 매칭 필터 필수)
- [ ] 10. `deep_video_analysis.py`로 자막 srt + 썸네일 jpg 일괄 다운로드
- [ ] 11. 썸네일 시각 분석 (Claude Read 도구로 jpg 직접 읽기) — TOP 5만
- [ ] 12. 자막 본문 추출 + 후킹 구조 분해 + 차용 어법 매트릭스

### 4단 — 민간 속설/통념 (NEW) ⭐
- [ ] 13. 60+ 성분 + 14 카테고리 시드로 다음카페·네이트판 재크롤
- [ ] 14. 정규식 정제 (`folk_beliefs.json` 패턴) — unique 발화 1,000+ 목표
- [ ] 15. "통념 얹기" 카피 50선 직변환 + 자막 인서트 [대괄호] 풀
- [ ] 16. 사용자에게 브랜드 제외 컨펌 (유명 브랜드 체크)

### 산출 + 위키
- [ ] 17. **6개 MD** 파일 출력 (01~03 캔버스 + **04 검색·트렌드 / 05 영상 1차 / 06 속설**)
- [ ] 18. 위키 인제스트 (`sources/src-market-research-{주제}-{날짜}.md`)
- [ ] 19. tacit 패턴 신규 발견 시 `viral-patterns` / `psychology-insights` / `creative-patterns` append
- [ ] 20. `wiki/log.md` 엔트리 + git commit + push

---

## 🔗 관련 위키

- [[src-market-research-pipeline-2026-04]] — 이 플레이북의 성공 원본 케이스
- [[usp-performance-canvas-research]] — **대척점** 플레이북 (이쪽은 카테고리 단위, USP는 제품 1개 단위). 제품·랜딩 URL이 주어지면 USP 플레이북으로 라우팅
- [[marketing-automation]] — 상위 도메인
- [[src-naverapi]] — 네이버 API 인증·엔드포인트 상세
- [[src-community]] — 커뮤니티 크롤러 모듈
- [[creative-patterns]] — 카피·소재 감각 적용
- [[psychology-insights]] — 설득 심리학 (7대 인사이트 근거)

---

## 9️⃣ 변형 모드: "브랜드 시장 단위 + 자사몰 분석 + 진입 권고" (2026-04-28 추가)

본 플레이북의 기본형은 *화장품 카테고리 11파일 영상기획 산출*. 하지만 비-화장품 카테고리(패션/가전/푸드 등)에서 **신규 브랜드 진입 의사결정**이 목표일 때는 다른 구조로 변형.

### 9-1. 트리거
- "○○ 시장 분석해줘 / ○○ 브랜드들 어떻게 흐르고 있나"
- "이 카테고리에 진입하면 어떨까"
- "기존 브랜드(○○)에서 신규 라인 런칭하면 시너지 날까"

### 9-2. 4 Phase 파이프라인
```
Phase 1 (병렬 ~6분): 브랜드 50+ 발굴 + 페인포인트 100+건 마이닝
Phase 2 (Python ~3분): 데이터랩 트렌드 + 검색광고 역산 (24개월 시계열)
Phase 3 (병렬 ~10분): 자사몰 12개 6 그룹 분할 분석
Phase 4: 통합 MD + Excel 11시트 + Toss UI HTML
```

### 9-3. Excel 11시트 표준 (영상기획용 11파일과 다름)
| 시트 | 용도 |
|---|---|
| 00. Executive Summary | 카테고리·1위·진입전략 1줄 |
| 01. 타겟 페르소나 | 6 페르소나 (연령/성별/직군/페인/구매채널/가격대/메시지) |
| 02. 페인×솔루션 | TOP20 페인 → 필수기능/차별기능/경쟁사처리/우리메시지 |
| 03. 사회적 증거 | 20 인용 + 출처 (활용 메시지) |
| 04. 권위(Authority) | 인증/협회/임상/병원 + 난이도·비용 |
| 05. 통념(Convention) | 깨야할/활용할 분류 + 메시지 전략 |
| 06. 후킹 카피 풀 | 페르소나×페인×채널 매핑 |
| 07. 경쟁사 매트릭스 | USP/강점/빈자리/우리차별점 |
| 08. 가격 전략 | 5단 가격사다리 + 화이트스페이스 강조 |
| 09. 검색량 트렌드 | TOP30 + 24M 성장률 + 시사점 |
| 10. 진입 액션 플랜 | 0-78주 9단계 |

### 9-4. 도구
- 검색량 역산: `naver-competitor-finder/nurse/fetch_brand_trends.py` ⭐
- Excel 생성: `naver-competitor-finder/nurse/generate_excel_report.py`
- Toss UI HTML: `naver-competitor-finder/nurse/reports/report.html` (참조 샘플)

### 9-5. 시너지 분석 (옵션, 모브랜드 확장 검토 시)
PRO 7 / CON 6 / 3 시나리오 ROAS 비교 매트릭스 — 자세히 [[tacit/operational-heuristics]] §브랜드 시너지 3 시나리오.

### 9-6. 성공 케이스
[[sources/src-nurse-shoes-2026-04-28]] — 간호사 신발 55개 + 착한구두 시너지 분석 (사용자 승인 표준).
