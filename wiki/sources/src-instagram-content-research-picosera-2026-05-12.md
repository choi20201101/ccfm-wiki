---
aliases: ["피코쎄라 인스타 리서치", "IG 8계정 콘텐츠 조사"]
type: source
domain: marketing-automation
confidence: high
created: 2026-05-12
updated: 2026-05-12
related:
  - instagram-content-research
  - market-research-playbook
---

# 피코쎄라 인스타 콘텐츠 리서치 (2026-05-11 ~ 12)

## 요청

> "ink.txt 인스타 링크 8개 → 좋아요 ≥500 게시물 가져와서 피코쎄라 콘텐츠 아이디어로 정리, 1000개 이상 조사. 카드뉴스는 슬라이드 전체 받아서 흐름·내용 분석 후 1장 이미지로, 영상은 컷별로 추출해서 이미지 아이디어로 변환."

대상 8계정:
- `humor__.cok`, `zzal_zzal_zzal`, `haldo_daily`, `think_pocket.official`
- `windows.98b`, `power_biolife`, `but___ter_`, `zam_zam_me`

## 실제 결과

- 메타 수집: **336개** (목표 1200개의 28%) — 3개 계정만 성공
- ≥500 좋아요: **99개**
- 미디어+아이디어 추출 완료: **47개** (목표 99의 47%)
- 5개 계정 IP 차단으로 스크랩 실패

| 계정 | 수집 | 좋아요≥500 | 비고 |
|---|---|---|---|
| @humor__.cok | 156 | 64 | 정상 |
| @zzal_zzal_zzal | 156 | 30+ | 정상 (10만+ 좋아요 게시물 포함) |
| @haldo_daily | 24 | 일부 | 도중 차단 |
| 나머지 5계정 | 0 | - | Profile 엔드포인트 429 |

## 시행착오 (다음 회 차단 피하려면)

1. **로그인 세션 미리 점검** — `instarup/state/sessions/*.json` 4개 중 2개만 살아있었고 한 시간 후 0개로 줄어듦
2. **첫 요청부터 429** — 이 IP에서 이전 instaloader 활동 누적되어 있었음. 새 IP/VPN 필요
3. **세션 회전 로직 부재** — `overnight.py`(v1)는 세션 회전 안 함, `overnight2.py`(v2)는 익명만 사용
4. **익명 instaloader Profile** — 너무 빠르게 막힘. Post 엔드포인트만 안정적
5. **카드뉴스 비중 압도적** — ≥500 좋아요 99개 중 80%+가 carousel (5~20 슬라이드)

## 산출물 위치

```
C:\Users\gguy\Desktop\gpt\projects\picosera\inset\
├ FINAL_REPORT.md          # TOP 47 아이디어
├ analyzed/<u>/<code>/     # 슬라이드+frame+idea.md 한 폴더
├ ideas/INDEX.md           # 인덱스
└ data/*.jsonl             # 원본 메타
```

## 성공 아이디어 패턴 (47개 중 상위)

- **@zzal_zzal_zzal/C9PO1m4pvKQ** ♥116,836 — "산책 거부하는 강아지" (단일 이미지 + 짧은 캡션 + 공감 해시태그)
- **@zzal_zzal_zzal/C_NsKalp9LM** ♥101,682 — "샘 해밍턴이 아들 혼내는 사진" (밈 짤 + 캡션 한 줄)
- **@humor__.cok/DOsTWZrEoJ4** ♥15,463 — 영상 클립 + 공감 후킹

**공통 패턴**: 짧은 1~2줄 한국어 후킹 + 강한 시각 + 해시태그 1~3개. 카드뉴스 시리즈는 ♥1k~5k 대 형성, 단일 짤이 폭발(>10만).

## 다음 회 권장

1. IP 회복까지 24~48시간 대기 후 5개 미수집 계정 재시도
2. 또는 별도 IP (VPN/모바일 핫스팟) 사용
3. 또는 유료 서비스 (Apify Instagram Scraper, ~$5/1000 posts)
4. `overnight2.py`의 scrape stage `SLEEP_MIN=540, SLEEP_MAX=660` (10분/post)으로 더 보수적으로 재실행

## 재현 가능한 코드

`projects/picosera/inset/` 의 모든 .py 파일이 재사용 가능. 자세한 사용법은 [[instagram-content-research]].
