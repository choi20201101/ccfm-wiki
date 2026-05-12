---
aliases: ["마케팅 자동화"]
type: domain
domain: marketing-automation
confidence: low
created: 2026-04-13
updated: 2026-04-13
sources: []
---

# 마케팅 자동화 AI (Marketing AI Automation)

## 개요
네이버 GFA/SA, Meta, Google 광고 자동화. 리포트 자동화, 입찰 최적화, 크리에이티브 A/B 테스트 자동화.

## 광고 플랫폼 자동화

### 네이버 GFA 세팅 자동화 (스킬)
- [[domains/gfa-setting-automation]] — **GFA-Setting v0.1.0** (2026-04-30 N=3 dry-run 성공). NAS 폴더 이미지 → N개 광고 그룹+소재 atomic 등록.
- 진입점: `gfa-setting <광고계정ID>`. 7개 입력값(콘텐츠 경로/캠페인 ID/참조 그룹·소재/베이스 이름/per_ad/랜딩 URL) 받아 자동 진행.
- 구현: DrissionPage 브라우저 자동화 (ADR-011). 참조 그룹 UI 복제로 27 파라미터 빌더 회피 (ADR-013).
- 코덱스 감사 잔존 이슈(2026-04-30): antd 안전가정 문서-코드 불일치(치명), CLI partial 누락(높음), 마스킹 secrets=[](높음). 상세는 도메인 페이지.

### 기타
- Meta Marketing API
- Google Ads 자동화
- 쿠팡 무단판매자 모니터링 (Playwright)

## 커뮤니티 → 광고 소재 마이닝
- [[domains/todayhumor-mining-playbook]] — **오늘의유머 위트 코드 → 광고 아이디어 1:1 변환 파이프라인** (2026-05-12 피코세라 사례 검증, brand_fit=high 84.5%). crawl_index → run.py(workers=3) → SDK 직호출. 게시물 1개 = 폴더 1개 = 아이디어 1개. 트리거 "오유 마이닝" / "humor mining".

## 리포트/대시보드
_내용 추가 예정_
- 구글시트 + n8n 자동화
- ROAS/CPA 자동 알림
- 클라이언트 리포트 자동 생성

## CRM/퍼널 자동화
_내용 추가 예정_

## 리뷰/크롤링
_내용 추가 예정_
- 경쟁사 리뷰 분석
- 키워드 트래킹
- 인스타 DM 시딩 파이프라인

## 관련 페이지
- [[ai-automation]]
- [[da-creative]]
- [[content-ai-automation]]

### 조사 플레이북 (트리거 기반 자동 가동)
- [[market-research-playbook]] — "시장조사 해줘" → 카테고리 단위 11파일 출력
- [[usp-performance-canvas-research]] — "USP 조사해줘 [URL]" → 제품 1개 단위 7파일 출력

### 크롤링 도구
- [[src-cafe-crawler]] — 네이버 카페 로그인/가입/크롤링 자동화 (Selenium + iframe JS 접근 + 수동 캡차 루프, 키워드 확장으로 10k+ 게시글 수집 & 키워드/감정 집계 리포트)
- [[src-naverapi]] — 네이버 검색광고 API + Meta 광고 경쟁사 분석 파이프라인
- [[src-community]] — 5개 한국 커뮤니티 통합 크롤러 (제목+본문+댓글, 10만건 검증)

<!-- AUTO:domain-crosslinks-begin -->
## 🔗 관련 도메인

- [[domains/marketing|📣 마케팅]]
- [[domains/ai-automation|🤖 AI 자동화]]
- [[domains/vibe-coding|💻 바이브 코딩]]

## 📊 소스
- [[wiki/sources/src-iboss-choi-jaemyeong|i-boss 201건]] 카테고리별 MOC:
<!-- AUTO:domain-crosslinks-end -->

<!-- AUTO:tags-begin -->
**Tags**: #status/active #domain/marketing #tech/naver-api #tech/crawling
<!-- AUTO:tags-end -->
