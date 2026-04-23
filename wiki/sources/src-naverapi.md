---
aliases: ["네이버 검색광고 API"]
type: source
domain: marketing-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [C:\Users\Administrator\Desktop\market-research-package\modules\naverapi]
---

# src: 네이버 검색광고 API + Meta 광고 분석 모듈

## 위치
`C:\Users\Administrator\Desktop\market-research-package\modules\naverapi\`

## 핵심 기능
- 네이버 검색광고 API(`/keywordstool`) + 데이터랩 API(`/v1/datalab/search`) + 쇼핑인사이트로 **연관키워드·월간검색량·시즌성·급등 키워드** 수집
- 카테고리 500위에서 `0->급등` 신규 브랜드 키워드 추출 → `{title}_신규브랜드_TOP30.xlsx` 자동 생성
- Meta Ads Library 를 Playwright 로 크롤링해 경쟁사 광고 영상/이미지/카피 수집
- 광고 텍스트 패턴 분석(키워드 빈도·훅 6분류·CTA·영상 길이) → 마크다운 경쟁사 분석 보고서 자동 생성
- 카테고리별 시즌 트렌드 Word 보고서(차트 포함) 생성

## 주요 파일
| 파일 | 역할 |
| --- | --- |
| `market_scanner.py` | 통합 시장조사 엔트리(`--mode category|seed|brands|full`). API 키 로드, 서버 시간 보정, 급등 키워드 / 신규 브랜드 TOP30 엑셀 생성 |
| `eval_deep_analysis.py` | 심층 키워드 10차 반복 검토 + 1~6개월 누적 비교 + 월별 상세 트렌드 → Word 보고서 |
| `beauty_device_seasonal_report.py` | 뷰티 디바이스 계절별 트렌드 Word 보고서(파이썬 docx + 차트) |
| `meta_ads_scraper.py` | TOP30 엑셀 → 브랜드명 정제(접미사 제거·prefix 병합) → Meta Ads Library 크롤링 → 영상/이미지 원본 다운로드 + `_ads.json` 기록 |
| `meta_text_collector.py` | 이미 수집한 폴더를 돌며 광고 카드 텍스트만 재파싱해 `ad_texts` 보완 |
| `ad_pattern_analyzer.py` | 광고 카드 raw 텍스트 → 구조화 → 키워드 빈도/훅/CTA/영상길이 집계 → `{title}_메타광고_경쟁사_분석보고서.md` |
| `hooks/run_meta_pipeline.sh` | 3-step 파이프라인 일괄 실행 훅 |
| `API-키워드-검색량-조회-가이드.md` | 검색광고 API + 데이터랩 API 인증/엔드포인트/파라미터/응답 스키마 가이드 |
| `META_경쟁사분석_워크플로우.md` | 5 STEP 경쟁사 분석 파이프라인 문서 |

## 가이드 문서
- `API-키워드-검색량-조회-가이드.md`: 네이버 검색광고 API(HMAC-SHA256)와 데이터랩 API(Client ID/Secret) 두 엔드포인트 + 절대 검색수 역산 공식 정리.
- `META_경쟁사분석_워크플로우.md`: 네이버 TOP30 → 브랜드 정제 → Meta Ads Library 크롤링 → 텍스트 재수집 → 패턴 분석 → 보고서 5단계 파이프라인.

## 산출 리포트
- `기미_키워드_심층분석.md` — 기미/미백 시장 키워드 급등·시즌 분석
- `탈모_키워드_심층분석.md`, `탈모_급등키워드_보고서.md`, `탈모_0to급등_전체.md` — 탈모 시장 키워드 급등/신규 진입 키워드
- `탈모_메타광고_경쟁사_분석보고서.md` — 17개 신규 브랜드 중 10개 메타 광고 집행, 집행량 랭킹·공통 키워드 TOP30·훅 6분류·브랜드별 상세
- Word 보고서: `reports/` 디렉토리 (뷰티 디바이스 계절별 트렌드)

## 의존성 / 환경변수
- Python 패키지: `requests`, `openpyxl`, `playwright` (`playwright install chromium` 필요), `python-docx` (Word 보고서용)
- API 키 파일: `api.txt` (모듈 루트 `market-research-package/` 상위). 라인 포맷:
  - `CUSTOMER_ID = ...`
  - `엑세스라이선스 = ...` (검색광고 API KEY)
  - `비밀키 = ...` (검색광고 API SECRET)
  - `Client ID = ...` / `Client Secret = ...` (데이터랩, 여러 개 로테이션)
- 필수 환경변수: `PYTHONIOENCODING=utf-8` (Windows 한글)

## 사용 예
```bash
cd market-research-package/modules/naverapi

# 통합 시장조사 (카테고리 급등 + 신규 브랜드 TOP30)
python market_scanner.py --mode full --title 탈모 \
  --cats "탈모케어:50000304,두피케어:50000303,샴푸:50000297,건강식품:50000023"

# 시드 키워드 심층분석
python market_scanner.py --mode seed --title 기미 \
  --seeds "기미,기미크림,기미제거,미백,색소침착"

# 메타 경쟁사 분석 파이프라인 (3-step 자동화)
bash hooks/run_meta_pipeline.sh 탈모 탈모_신규브랜드_TOP30.xlsx
```

## 알려진 이슈
- 로컬 시계가 네이버 서버와 ~60초 이상 어긋나면 `Invalid Timestamp` → 서버 시간 보정(`TD`) 로직 필수.
- 데이터랩 API Client ID 일일 한도 도달 시 키 풀 로테이션(`dl_counts >= 950` → 다음 키).
- Meta Ads Library fbcdn 영상 URL 토큰 만료 빠름 → 크롤링 직후 즉시 다운로드해야 0바이트 회피.
- 로그인 모달/DOM 구조 변경 시 스크래퍼 셀렉터 점검 필요.
- 가이드 md 에 실제 API 키가 평문 커밋되어 있음 — **유출 리스크, 별도 볼트 이동 권장** (확인 필요).
- 카테고리 인기검색어 TOP500 API는 미제공 — 연관키워드 수집 후 검색량 정렬로 대체.
- Meta Ads Library 대량 크롤링은 Meta ToS 회색지대 (확인 필요).

## 관련 도메인
- [[marketing-automation]]
- [[da-creative]] (광고 분석은 크리에이티브 인사이트로 이어짐)
- [[content-ai-automation]]

## 관련 암묵지
- [[coding-lessons]] — "네이버 검색광고 API + Meta 광고 분석 패턴" 섹션 (HMAC 서명, 브랜드 병합 규칙, Playwright 영상 캡처 3단 루트)
