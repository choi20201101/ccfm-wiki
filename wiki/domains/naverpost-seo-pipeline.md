---
type: domain
domain: marketing-automation
confidence: high
created: 2026-05-29
updated: 2026-05-29
sources:
  - C:\Users\gguy\Desktop\naverpost\
  - C:\Users\gguy\Desktop\naverpost\docs\
---

# naverpost — 네이버 블로그 SEO 반자동화 파이프라인 (재구축 스펙)

> **분류**: domains / marketing-automation
> **연관**: [[marketing-automation]] · [[ggttt-imagen]] · [[ai-automation]] · [[sources/src-geo-aeo-guide]]
> **목적**: 나중에 "네이버 블로그 글 자동화 다시 하자"가 되면 **이 페이지 + 프로젝트 `docs/`만 보고 재구축**할 수 있게 정리한 스펙/인수인계.
> **프로젝트 경로**: `C:\Users\gguy\Desktop\naverpost` (배포는 폴더째 zip 2분할, 아래 §9).

## 1. 한 줄 정의
키워드 발굴 → SERP 분석 → SEO 점수 → CCFM 자료 RAG 초안(Claude) → 이미지 생성(god-tibo-imagen) →
네이버 에디터 자동 채움 → **사람 검토 후 발행**까지 잇는 CCFM 네이버 블로그 SEO **반자동** 도구.

## 2. 핵심 원칙 (재구축 시 절대 깨지 말 것)
- **반자동**: 글·이미지·에디터 채움은 자동, **최종 발행 검토/클릭과 캡차 풀이는 사람**.
- **캡차/봇감지 자동 우회 금지** = 네이버 ToS 위반·계정 정지 직행. (AI 자동 캡차풀이는 4.7 빌드에 있던 걸 **제거**함)
- **하루 5개 한도** (계정 보호).
- 참고: GEO/AEO 가이드([[sources/src-geo-aeo-guide]])상 **자동화 AI글은 인용에서 걸러질 수 있음** → 사람 검토·실사진 보강이 품질의 핵심. 자동화는 롱테일 커버리지·발행 효율까지.

## 3. 전체 파이프라인
```
① 키워드 발굴   네이버 검색광고 API: 시드→연관확장 + 검색량
② SERP 분석     블로그탭 상위 5개 실제 스크랩(노후/분량/제목매칭/밀도)
③ SEO 점수      상위글 패턴으로 0~100 (compIdx=파워링크 경쟁도는 제외)
④ RAG 초안      CCFM 자료 BM25 검색 → Claude CLI로 글+이미지슬롯(4~5)
⑤ 이미지 생성   god-tibo-imagen으로 슬롯마다 PNG ([[ggttt-imagen]])
⑥ 에디터 채움   Playwright로 제목·본문(마크다운 정리)·이미지 입력
⑦ 검토 후 발행  사람이 확인→발행(또는 예약). 캡차 뜨면 사람이 직접 풀고 "풀었어요"
```

## 4. 모듈 ↔ 파일 지도 (`src/naverpost/`)
| 단계 | 파일 | 비고 |
|---|---|---|
| 오케스트레이션 | `pipeline.py`, `cli.py` | CLI: `ingest/analyze/run/fill/serve/schedule` |
| 설정 | `config.py`, `config.toml`, `.env` | 가중치·한도·시드·시크릿 |
| ① 키워드 | `searchad/{client,keywords_tool}.py` | 검색광고 API HMAC 서명 |
| ② SERP | `serp/{browser,blog_tab,post_fetcher}.py` | Playwright 스크랩 |
| ③ 점수 | `scoring/opportunity.py` | compIdx 제외 (블로그 SEO와 무관) |
| ④ RAG | `rag/{ingest,retriever,reranker}.py` | BM25 + codex 재순위 |
| ④ 초안 | `draft/{generator,prompt}.py` | Claude CLI `claude -p` |
| ⑤ 이미지 | `image_gen/__init__.py` + `/image_gen/` (node) | god-tibo-imagen 0.3.0 |
| ⑥ 에디터 | `naver_editor/{filler,login}.py` | 제목·본문·이미지 입력, 로그인 |
| 캡차 | `bot_check/__init__.py` | 봇감지→사람 해결 대기 |
| 예약 | `schedule/__init__.py`, `scheduler/register.py` | APScheduler + Win Task |
| 백엔드 | `api/main.py`, `api/routes/*.py` | FastAPI (:8000) |
| 프론트 | `web/src/` | Next.js 16 대시보드 (:3000) |

데이터: `data/drafts/*.md`(초안) · `data/drafts/images/*.png` · `data/ccfm_docs/`(RAG 원본) · `data/ccfm_index.json` · `data/serp_cache/` · `data/{schedules,published_count}.json`.

## 5. 기술 스택
Python 3.13 + Playwright(Chromium) + FastAPI/uvicorn(:8000) + Next.js 16(:3000), Windows.
글=**Claude CLI**(구독 인증 재사용), 이미지=**god-tibo-imagen**(Codex 인증 재사용), 검색=네이버 검색광고 API + rank_bm25.

## 6. 이미지 생성 (요지 — 상세는 [[ggttt-imagen]])
- `image_gen/scripts/generate-blog-images.mjs` + `image_gen/node_modules/god-tibo-imagen`(**0.3.0, 공개 npm**) + Python 래퍼.
- 인증: `codex login` → `~/.codex/auth.json` (공유 키 없음, PC별 1회). 1장 ~140초.
- 초안의 `![alt](images/날짜-키워드-슬롯.png)` 슬롯 → spec 추출 → node 호출 → `data/drafts/images/`.

## 7. 계정 안전 규칙 (코드 계약)
- 캡차 = **사람이 브라우저 창에서 직접 풀고 대시보드 "✅ 풀었어요" 클릭** → 백엔드가 화면 넘어간 것 확인 후 진행. 시스템은 답을 타이핑하지 않음.
- 자동 캡차풀이/스텔스/UA 위장 **추가 금지**. 발행은 일 5개 가드레일.
- 로그인 1회 후 세션 유지 → 캡차 빈도↓. 비번 변경 시 ⚙️설정에서 저장비번 갱신.

## 8. 현재 구현 상태 (2026-05-29)
- ✅ **되는 것**: 키워드·SERP·점수·RAG·Claude 초안·이미지 생성·에디터 자동 채움(본문 마크다운 정리 + 이미지 5장 첨부, 라이브 검증)·캡차 사람해결 모델.
- 🚧 **진행 중**: ⚡완전 자동발행의 **발행 패널 처리**(게시판/카테고리 선택 + 최종 발행 클릭). 패널 여는 버튼은 `[data-click-area="tpb.publish"]`로 확정. 임시로 **"검토 후 발행"(사람 클릭)은 동작**. ※ 게시판 선택 자동화는 사용자가 **보류 지시**(재개는 지시 있을 때만).
- ⚠️ **알려진 이슈(4.7 초기 빌드 감사 86건 중 미수정)**: 발행 성공 미검증 카운터 증가 / 일일한도 blog_id 불일치 / 스케줄러 타임존(Asia/Seoul vs naive) / 검색광고 캐시 대소문자→직접지정 키워드 0개 / 초안 글자수·금지어 자동검증 없음 / `web/analyze/page.tsx` 기존 TS 에러 2건 / 캡차 오탐("공지사항").

## 9. 설치·실행·배포
- **수동 설치**(install.bat 의존 X): `docs/02-설치-수동.md` — Python·Node·Claude/Codex CLI → `python -m venv .venv` → `pip install -e .` → `playwright install chromium` → `cd web && npm install` → `cd image_gen && npm install` → `.env` → `claude login`/`codex login`.
- **실행**: `start.bat`(또는 `python -m naverpost.cli serve`) → http://localhost:3000. **코드 수정 시 백엔드 재시작 필수**(자동 리로드 없음).
- **배포**: 폴더째 전달. `.venv`는 비휴대성(경로 박힘) → 받는 PC에서 재생성. Chromium도 폴더 밖(AppData) → `playwright install` 필요. 용량 1.8GB라 zip 2분할(part1=소스+.venv+data+docs, part2=web/node_modules+.playwright_profile, 각 <1GB). `.playwright_profile`엔 네이버 세션 포함 → 다른 계정이면 삭제 후 첫 로그인.

## 10. 재구축 핵심 결정 (있는 그대로)
- 점수에서 **compIdx 제외** — 파워링크 입찰 경쟁도일 뿐 블로그 SEO와 무관. 경쟁도는 실제 SERP 상위글 분석으로만.
- 에디터 본문은 **마크다운→플레인 변환 후 타이핑** — 네이버 SmartEditor가 `~~`→취소선, `---`→구분선으로 자동변환하기 때문. 버튼 클릭은 `:has-text` 부분일치 금지(‘취소’가 ‘취소선’ 버튼 오클릭) → 안정 셀렉터/정확일치 사용.
- 글·이미지 인증은 **사용자 CLI 구독 재사용**(API 키 비용 없음): Claude=`claude login`, 이미지=`codex login`.
- 상세 단계 문서는 프로젝트 동봉 `docs/`(README+01~09)에 있음 — zip에 같이 감.

## 11. 참고
- 프로젝트 인수인계 문서: `naverpost/docs/` (수동설치·실행·사용법·아키텍처·ggttt·계정안전·문제해결·현재상태)
- 이미지 엔진 상세: [[ggttt-imagen]] · 발행 자동화 상위 프레임: [[marketing-automation]]의 GEO/AEO + [[sources/src-geo-aeo-guide]]

<!-- AUTO:tags-begin -->
**Tags**: #status/active #domain/marketing-automation #tech/playwright #tech/naver-api #tech/claude-cli #project/naverpost
<!-- AUTO:tags-end -->
