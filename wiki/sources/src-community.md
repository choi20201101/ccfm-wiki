---
aliases: ["커뮤니티 크롤러"]
type: source
domain: marketing-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [C:\Users\Administrator\Desktop\market-research-package\modules\community]
---

# src: 한국 커뮤니티 통합 크롤러 모듈

## 위치
`C:\Users\Administrator\Desktop\market-research-package\modules\community\`

## 대상 사이트 (5종)
| 사이트 | 접근 | 검증된 수집량 | 제목 | 본문 | 댓글 |
| --- | --- | --- | --- | --- | --- |
| 네이트판 | requests + BS4 | 15,000~30,000건 | ✅ | ✅ `#contentArea` 검증 (2026-04-13) | ✅ `dl.cmt_item` 검증 |
| 인스티즈 | requests | 3,000~20,000건 | ✅ | ✅ `#memo_content_1` 검증 | ✅ `table#ajax_table tr.cmt_view` 검증 (likes 미노출) |
| 더쿠 | cloudscraper (CF 우회) | 10,000~30,000건 | ✅ | ✅ `.rd_body .xe_content` 검증 | ⚠️ AJAX 로드 — 정적 요청 불가, 별도 endpoint 호출 필요 |
| 보배드림 | requests | 50~500건 | ✅ | ✅ `div.bodyCont` 검증 (인코딩 자동 교정 추가) | ✅ `#cmt_list li` 검증 |
| 다음카페(쭉빵/여시/소울드레서) | 카카오 search API + 페이지 | 10,000~30,000건 | ✅ + content 200자 | ❌ 로그인벽 (스킵) | ❌ 동일 |

검증 실적: 기미 95,588건 / 탈모 40,643건 / 전체 병합 **119,647건** (제목 기반, 2026-04 이전).

## 수집 필드
**기본(항상 수집)**: `title` / `views` / `comments`(댓글 수 문자열) / `date` / `url` / `community` / `keyword` / `crawled_at`

**FETCH_DETAIL=True 또는 `--with-detail` 시 추가**:
- `body` — 본문 전문 (HTML 태그 제거)
- `comments_detail` — `[{"author": str, "text": str, "likes": int}, ...]`
  - 기존 `comments`(수) 필드는 보존해서 analyzer 하위 호환 유지

## 핵심 기능
- 키워드 하나만 주면 5개 사이트 자동 순회 (`keyword_expander.py`가 업종별로 변형 자동 생성)
- 제목 앞 40자 기준 중복 제거 (`CommunityCollector._add`)
- 10 키워드마다 중간 저장, 에러 150회 초과 시 자동 중단
- Hook 시스템: pre_expand / pre_crawl / post_crawl / post_analyze / on_complete (`hooks.py`)
- `analyzer.py`가 8카테고리 분류·감성 분석·MD 리포트 자동 생성

## 주요 파일
| 파일 | 역할 |
| --- | --- |
| `run.py` | 엔트리포인트 (argparse, `--with-detail` 포함) |
| `config.py` | 환경변수/`.env` 로더, `FETCH_DETAIL` 플래그 |
| `crawler.py` | 5개 사이트 통합 크롤링 (`CommunityCollector`) |
| `detail_fetcher.py` (2026-04-13 신규) | 사이트별 본문/댓글 fetcher 5종 + 디스패처 |
| `analyzer.py` | 정제·8카테고리 분류·감성 분석·MD 리포트 |
| `keyword_expander.py` | 업종 자동 감지 + 카테고리×변형 |
| `hooks.py` | 파이프라인 pre/post Hook |

## 의존성
`requests`, `beautifulsoup4`, `lxml`, `cloudscraper`(더쿠 CF 우회), 카카오 REST API 키

## 사용 예
```bash
py run.py "탈모"                       # 제목만 (기존 워크플로우)
py run.py "탈모" --with-detail         # 본문+댓글까지 (opt-in, ~2배 느림)
py run.py "기미" --community theqoo    # 특정 사이트만
py run.py "여드름" --analyze-only      # 기존 데이터로 분석만
```

## 보안 이슈 (확인됨)
- `config.py:17` 카카오 REST API 키 **평문 fallback** (`KAKAO_API_KEY="8d14...a8f"`) — 별도 작업으로 마스킹/제거 필요. `.env` 사용 시 이 fallback은 덮어씌워짐.

## 알려진 제약
- ToS/robots.txt 회색지대 — 사이트별 rate limit 준수(1.5~3초) 전제로 운영.
- 목록 페이지 셀렉터는 2026-04 기준 검증. UI 개편 시 깨질 수 있음.
- **상세 페이지(본문/댓글) 셀렉터는 가이드 문서(`docs/crawling-guide/`)에 없어 관용 패턴 기반 추정** — 실크롤로 검증 필요 (⚠️ 표시된 5개 사이트 모두).
- 다음카페는 대부분 로그인/앱 전용 → 본문 fetch 거의 항상 실패 (warning 로그, 메인 흐름은 유지).
- 더쿠 검색 API는 CF가 차단 → 게시판 페이지 순회 방식으로만 수집 가능.

## 관련 도메인
- [[marketing-automation]]
- [[viral]] (커뮤니티 데이터 = 바이럴 원료)
