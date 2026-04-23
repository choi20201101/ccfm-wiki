---
aliases: ["인스타 수집"]
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [C:\Users\Administrator\Desktop\market-research-package\modules\instar]
---

# src: 인스타그램 릴스 수집·분석 모듈

## 위치
C:\Users\Administrator\Desktop\market-research-package\modules\instar\

## 핵심 기능
릴스 URL 리스트 → yt-dlp 익명 추출 → 필터(날짜/조회/참여율) → 5축 분석 + Claude Vision 프롬프트 생성. 로그인 불요, cron/외부 자동화에서 직접 호출.

## 수집 필드
| 항목 | 비고 |
| --- | --- |
| channel, view_count, like_count, comment_count | yt-dlp 메타 |
| **description (캡션 텍스트)** | 분석에 사용 |
| **영상 .mp4 + 썸네일 .jpg** | 실제 파일 다운로드 |
| 댓글 본문 | ❌ (count만) |

## 주요 파일
| 파일 | 역할 |
| --- | --- |
| insta_tool/cli.py | CLI 진입점, 명령 그룹화 |
| insta_tool/fetcher.py | yt-dlp 서브프로세스 래퍼 |
| insta_tool/filters.py | by_date / by_views / by_likes / by_comments / by_engagement_rate |
| insta_tool/analyzer.py | 5축 분석, 한/영 자동 감지, 언어별 stopwords |
| insta_tool/vision.py | Claude Vision 프롬프트 생성 (11 장면 카테고리) |
| insta_tool/io_schema.py | REEL_FIELDS / validate_reel / empty_reel envelope 계약 |
| credentials.py | 익명 기본 (값 빈 상태, .gitignore 명시) |

## 의존성
- yt-dlp 2026.x (Python 3.14 + yt-dlp 2026.2.4 검증)
- Claude Vision (외부 호출, 프롬프트만 생성)

## 사용 예
```bash
py -m insta_tool fetch --urls reel_urls.txt
py -m insta_tool pipeline --urls reel_urls.txt --min-views 10000
```

## 표준 JSON envelope
```json
{"meta": {...}, "reels": [...], "failures": [{...}]}
```

## 알려진 제약
- Meta ToS 회색지대 (익명 스크래핑도 위반 소지)
- yt-dlp 차단/계정 밴 리스크 (rate limit 필수)
- Python 3.14.2 + yt-dlp 2026.2.4 버전 고정
- `/api/v1/` 엔드포인트 이미 404 (Playwright 경로 폐기 이력)
- 댓글 본문 미수집 — 캡션과 metric만으로 분석

## 관련 도메인
- [[content-ai-automation]] (Vision 프롬프트 자동화)
- [[da-creative]] (릴스 = 숏폼 광고 레퍼런스)
- [[viral]] (조회/참여율 상위 패턴)
