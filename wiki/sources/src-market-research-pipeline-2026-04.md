---
aliases: ["시장조사 파이프라인 (주름·유쎄라블)"]
type: source
domain: marketing-automation
confidence: high
created: 2026-04-20
updated: 2026-04-20
sources:
  - C:/Users/gguy/Desktop/bol/
  - C:/Users/gguy/Desktop/bol_video/see/
  - C:/Users/gguy/Desktop/MD/네이버 급상승 경쟁사 찾는 스킬/naver-competitor-finder/
---

# 성공사례: 주름·리프팅 시장조사 → 영상기획 리포트 파이프라인

> 기간: 2026-04-20 단일 세션
> 제품: 메라블 유쎄라블 2X 볼륨필인 앰플
> 산출물: 영상기획용 MD 11파일 + 브랜드 발굴 엑셀 + 메타광고 경쟁사 분석
> 사용자 만족도: 높음 (쉬운 말 치환·150줄 분할·보르피린 표현 오해 방지 등 디테일 수용)

---

## 🎯 배경

고객사(메라블) 볼륨필인 앰플 영상 기획을 위한 시장조사.
**"경쟁사 발굴 + 급상승 키워드 + 소비자 말 수집 + 경쟁 광고 역설계 + 제품 접목"** 5단계.

## 🏗 파이프라인 아키텍처

```
시드 키워드 → 연관키워드 1,158 → 6개월 트렌드 → 저점폭증 필터 (브랜드 30개)
    ↓
다음카페(Kakao API) 7,338 + 네이트판 HTML 10,257 + YouTube(Playwright) 95
    ↓
7대 인사이트 매칭 (통념·근거·권위·배경·장소·물건·욕망)
    ↓
메타 광고 라이브러리 Playwright 크롤 (25브랜드 500+ 카피)
    ↓
광고 패턴 분석 (훅·CTA·키워드·영상길이)
    ↓
제품 캔버스(pd/01~03.md) 교차 → 영상기획 MD 11파일 (각 <150줄)
```

---

## 📊 활용 API·채널

| API/채널 | 용도 | 엔드포인트 |
|---------|------|-----------|
| 네이버 검색광고 keywordstool | 월간 검색량 + 연관키워드 | api.searchad.naver.com/keywordstool |
| 데이터랩 쇼핑인사이트 | 카테고리 TOP500 급등 | datalab.naver.com/shoppingInsight |
| 데이터랩 통합검색 트렌드 | 6개월 검색 트렌드 | openapi.naver.com/v1/datalab/search |
| 카카오 검색 API | 다음카페 글 수집 | dapi.kakao.com/v2/search/cafe |
| 네이트판 HTML | 게시글 크롤 (UTF-8, EUC-KR 아님 주의) | pann.nate.com/search/talk |
| Meta Ads Library | 경쟁 광고 영상·이미지·카피 | facebook.com/ads/library (Playwright) |
| YouTube | 검색 결과·댓글 (API 대신 Playwright) | youtube.com/results |

---

## 🔑 성공 요인

### 1. 시드→확장 키워드 전략 (카테고리 CID 의존 탈피)
- 최초 시도: 스킨케어/마스크팩 카테고리 CID로 신규 브랜드 발굴 → 0건
- 전환: `keywordstool`에 **시드 21개로 연관키워드 1,158 추출** → 상위 250개 **6개월 트렌드 검증**
- 결과: **저점→폭증 32건 + 신호 키워드 15개 확정**

### 2. 저점→폭증 필터 3단 구조
| 구조 | 기준 | 결과 건수 |
|------|------|----------|
| 엄격 (원본 skill) | 6개월 전 0 → 최근 300+ | 0건 (너무 타이트) |
| 중간 | 저점 < 30, 피크 > 300 | 1~5건 |
| 실용 | **저점 < 100, (최근 or 피크) > 200** | 수십 건 (권장) |

→ **플레이북 표준값: 저점 < 100, 피크 > 200, 성장률 > 30%**

### 3. 인코딩·HTML 구조 함정
- 네이트판: EUC-KR 아님, **UTF-8**로 바로 파싱
- 네이버 shopping insight 카테고리 하위 CID 추측 불가 (50001xxx 범위 거의 실패)
- 인스티즈·더쿠·보배드림: HTML 구조 자주 변경되어 셀렉터 깨짐 → 네이트판만 유지

### 4. 브랜드 제외 리스트 운영
- 대형 브랜드(설화수·메디큐브 등) + **사용자가 "너무 유명하다"고 지목한 브랜드**(이솝·톤28·시드물·프라나롬·도브 등) 즉시 제외
- **재실행 비용 0**: `refilter_trends.py`로 저장된 JSON 재필터링 (API 재호출 불필요)

### 5. 이미지 API 없이 실데이터 수집
- 인스타그램 API 로그인 실패(jobdongsan/IP블랙리스트) → **커뮤니티 데이터로 충분히 대체**
- 네이버 오픈API scope 미활성화 → **카카오 API + 네이트판 크롤**로 보완
- 유튜브 API 키 없이 **Playwright 백그라운드 Chromium**으로 성공

### 6. 메타광고 라이브러리 역설계 (가장 강력)
- 25 키워드/브랜드 → 활성 광고 **10개** 집행 브랜드 발견
- **최강 경쟁사 = 메디큐브 (콜라겐 139건)**, 차앤박 (PDRN 280건)
- **"볼륨필인"·"바르는 필러" 키워드는 유쎄라블(동안연구소) 단독** → 선점 영역 확인
- 500+ 카피에서 **질문형 훅 120건**, **"더 알아보기" CTA 220회** 등 표준 문법 추출

### 7. 표현 감수 루프 (사용자 피드백 즉시 반영)
- "지방 세포 증식" → 살찐다 오해 → **"꺼진 자리 깨우기"** 로 즉시 전환
- "인텔리전트 미니멀리즘" → **"한 병으로 끝"**
- "경제적 승리감" → **"돈 아낀 기분"**
- 7대 인사이트 매칭용 **쉬운 말 치환표** 를 임원요약에 명시

### 8. 리포트 구조 (150줄 쪼개기)
- 원본 docx를 기준으로 **11개 MD 파일**로 분할
- 각 파일 **<150줄** 고정 → Claude Code 한 번에 읽기 좋고 IDE 내비게이션 편함
- 순서: 개요 → 트렌드 → 서사5단계 → 성분 → 포지셔닝 → 트리거 → 경쟁사 → 시장신호 → 템플릿10 → 카피뱅크 → 인사이트·체인 → 참고자료

---

## 🔑 Gemini Deep Research API 관련 (조사 결과)

> 사용자 요청: "제미나이 딥리서치 API 호출로도 되지?"

### 공식 현황 (2026-04 기준)
- **Gemini Advanced 앱**의 "Deep Research" 버튼은 **API로 직접 노출 안 됨** (소비자 제품 기능)
- 비슷한 결과를 내는 API 대안 3가지:
  1. **Gemini 2.5 Pro + `google_search` grounding tool** — 단발성 웹 연동 질의 (Vertex AI / AI Studio)
  2. **URL context 도구** — 지정 URL들 읽어서 요약
  3. **에이전트 루프 자작** — 기획→검색→합성 multi-step orchestration

### 품질 차이
- 소비자 앱 Deep Research: 전용 프롬프트 오케스트레이션 + 수분간 reasoning → 풍부한 서사 보고서
- API 직접: 단발 호출은 얕음, **에이전트 루프로 reasoning 단계 추가**하면 근접 가능

### 권장: 하이브리드 전략
- **Gemini Deep Research (앱/수동)**: 글로벌/업계 narrative 배경 리포트 (워드 파일로 수동 저장 후 인풋)
- **본 파이프라인 (API)**: 한국 시장 실데이터 (네이버/카카오/메타/커뮤니티)
- 최종 통합: 두 소스를 merge해 영상기획 MD 생성

→ **동일 퀄리티로 Gemini DR 보고서 API 자동화는 현재 불가**. 앱에서 수동 생성 후 폴더 투입 방식 권장.

### 만약 Deep Research API 나오면
- 위키에 `tacit/coding-lessons.md` §"Gemini Deep Research API" 섹션 신설 예정
- 파이프라인 Phase 0에 "Gemini DR 호출 → 배경 narrative 수급" 자동화 가능

---

## 📁 재사용 자산

### 작업 결과물
```
bol/                                          (원본 작업 루트)
├── api.txt                                   네이버/카카오/인스타 키
├── scripts/
│   ├── config.py                            API 키 로더 (데이터랩·카카오·인스타)
│   ├── collect_naver_search.py              cafearticle + blog (scope 필요)
│   ├── collect_daum_kakao.py                다음카페 (1000건/키워드 상한)
│   ├── collect_community.py                 네이트판·인스티즈·더쿠·보배
│   ├── collect_instagram.py                 instagrapi 해시태그
│   ├── collect_youtube.py                   Playwright 검색+댓글
│   ├── analyze_insights.py                  7대 카테고리 매칭
│   ├── extract_brands.py                    수집 텍스트 브랜드 추출
│   ├── find_surge_from_zero.py              급등JSON + 6개월 트렌드 필터
│   ├── find_by_related_keywords.py          시드→연관→6개월 트렌드 (핵심)
│   ├── refilter_trends.py                   저장된 JSON 재필터 (API 재호출 X)
│   └── make_meta_xlsx.py                    메타크롤용 xlsx 생성
└── output/
    ├── raw/*.jsonl                          수집 원천 (17,690건)
    └── reports/07~11.md                     단계별 분석 MD

bol_video/see/                                (영상 기획용 최종 산출)
└── 00~11.md                                 11개 <150줄 구조화 MD

MD/네이버 급상승 경쟁사 찾는 스킬/naver-competitor-finder/
└── scripts/                                 scan_surge + scrape_meta + analyze_pattern
```

---

## 📊 최종 지표

- 수집 raw: **17,690건** (다음 7,338 + 네이트 10,257 + 유튜브 95)
- 연관키워드 트렌드 분석: **1,158개** (상위 250 6개월 조회)
- 저점→폭증 발굴: **32건** (대형 브랜드 제외 후)
- 메타광고 분석: **500+ 카피** (25 키워드/브랜드 중 10개 활성 집행)
- 영상기획 MD: **11파일 1,387줄** (평균 126줄)
- 총 세션 시간: 약 3시간 (수집 파이프라인 실행 포함)

---

## 🔗 관련 위키

- [[market-research-playbook]] — **재사용 플레이북 (다음 시장조사 시 바로 참조)**
- [[marketing-automation]] — 광고·크롤링 자동화 도메인
- [[src-naverapi]] — 네이버 API 가이드
- [[src-community]] — 커뮤니티 크롤러
- [[src-cafe-crawler]] — 네이버 카페 크롤러 (이번엔 사용 안 함)
- [[creative-patterns]] — 카피·소재 감각
- [[src-volumefill-pipeline-2026-04-20]] — 후속 이미지 소재 생성 파이프라인

## 실수·학습

- **네이버 openapi "검색" scope 미활성화**: 앱 scope 확인 필수. Search 스코프 없으면 cafearticle 401 → 카카오·네이트판으로 대체
- **카테고리 CID 추측 실패**: 50001xxx 범위 대부분 헤어/바디 카테고리. 하위 스킨케어 CID 하드코딩 대신 시드→연관키워드 전략 사용
- **"지방 세포 증식" 표현**: 살찐다 오해 유발 → 프로덕트 담당 반드시 표현 감수
- **인스타 로그인 실패**: 계정 IP 블랙리스트 가능. 백업 수집 채널(커뮤니티·유튜브) 병행 전제
- **Playwright + 배경 태스크 stdout 버퍼링**: `python -u`로 unbuffered 출력 필수
- **브랜드 제외 리스트**: 사용자가 "너무 유명하다" 지목하는 브랜드 즉시 MAJOR에 추가하는 패턴화 필요
