---
aliases: ["마케팅 자동화"]
type: domain
domain: marketing-automation
confidence: low
created: 2026-04-13
updated: 2026-05-29
sources: [wiki/sources/src-geo-aeo-guide.md]
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

### 네이버 블로그 SEO 자동화 (naverpost)
- [[domains/naverpost-seo-pipeline]] — **키워드→SERP→점수→RAG초안(Claude)→이미지(god-tibo-imagen)→에디터 자동채움→사람 검토 발행** 반자동 파이프라인. 캡차·최종 발행은 사람, 일 5개 한도. 경로 `C:\Users\gguy\Desktop\naverpost` (재구축 스펙+`docs/` 동봉). GEO/AEO 프레임(아래)과 연결 — 자동화는 롱테일 발행 효율, 인용 품질은 사람 검토·실사진.

## 커뮤니티 → 광고 소재 마이닝
- [[domains/todayhumor-mining-playbook]] — **오늘의유머 위트 코드 → 광고 아이디어 1:1 변환 파이프라인** (2026-05-12 피코세라 사례 검증, brand_fit=high 84.5%). crawl_index → run.py(workers=3) → SDK 직호출. 게시물 1개 = 폴더 1개 = 아이디어 1개. 트리거 "오유 마이닝" / "humor mining".

## GEO / AEO (생성형·답변 엔진 최적화) 🌐
> 전체 실행 가이드: **[[sources/src-geo-aeo-guide]]** (2026-05 현장 미팅 기반). 블로그/워드프레스/구글 글 **발행 자동화의 기준 프레임**.

- **원리** — LLM은 학습(RAG) 1차 → 웹서치 보완 + 출처. 봇 크롤 = 인용·학습. 한 번 인용되면 다음엔 안 가져갈 수도. → "AI가 굳이 노출시켜줄 이유 = **명확하게 좋은 정보**"를 역순 설계.
- **세팅** — 스키마·데이터 구조를 **오늘의집처럼**(커머스 1순위) + **도메인 지수 누적**(나이·링크·지속운영, 시작 빠를수록 유리) + 크롤 버블 열기 + 이미지 신중 선정(비전 모델이 이미지 내용까지 읽음).
- **콘텐츠** — **실제 사람 글 + 실제 사진** 필수(자동화 글은 AI 글로 걸러져 인용 안 됨). 자동화는 롱테일 커버리지·발행 효율까지만 → **이원화**.
- **키워드** — 단어가 아닌 **문장형 롱테일 대량(100만 규모)**. 메인 키워드는 경쟁·전환 약함. 키워드별 콘텐츠 월 단위 자동 발행. **한국 구글 GEO/SEO는 아직 초기·경쟁 낮아 작성만 잘하면 잘 올라감**(진입 적기). ⚠️ 단 "노출 보장"은 아님 — 경쟁 붙으면 결국 **신뢰도·도메인 싸움**.
- **플랫폼** — Gemini=구글 SEO 영향 최대(웹서치 의존↓·캐시 길다), Perplexity=웹서치 의존↑(빠른 반영). 스마트스토어는 막혀서 **스키마 완비 클론/허브 사이트로 우회 → UTM 추적 → 스토어로 넘김**.
- **측정** — ⚠️ **API·스크린 모드**로 측정(개인화 때문에 본인 PC로는 본인 사이트 안 뜸). GA로 LLM 유입·키워드 추적. ⚠️ 봇 유입량 ≠ 좋은 노출. 노출 키워드 리포트 → 다음 주제 도출 루프.
- **리스크** — ⚠️ 구글은 어뷰징 시 **도메인 영구 사망**(복구 불가) → 정확하게 쓰는 게 빠르고 안전. 어뷰징 한계는 버려도 되는 테스트 사이트로만 확인.

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
