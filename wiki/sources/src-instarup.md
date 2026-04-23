---
aliases: ["IG 자동 업로드"]
name: src-instarup
type: source
project: instarup
created: 2026-04-13
confidence: high
---

# src-instarup — Instagram 릴스 멀티계정 자동 업로드 프로젝트

## 개요
로컬 PC에서 50~100개 인스타그램 계정에 릴스 영상을 배치 업로드하는 시스템. BDH 파이프라인(bob+dd+harness)으로 Spec v5까지 설계 + step-01까지 구현 + E2E 업로드 2건 실제 검증 완료.

경로: `C:\Users\Administrator\Desktop\instarup\`

## 검증된 사실 (실제 테스트 결과)

### 2026-04-13 업로드 성공 2건 — 계정 jmtw.12345
1. `media.pk=3874384363297837322` / code=DXElA0RshEK (한글 테스트 캡션)
2. `media.pk=3874385348590108927` / code=DXElPJ5sQD_ (번체중문 대만시장 캡션)

- 영상: 3MB mp4 (KakaoTalk 내보내기)
- 신규 로그인→업로드 총 38초
- `media_delete(pk)`로 즉시 삭제 가능 확인
- 세션 재사용 시 로그인 스킵 → 업로드 시간만 소요

## 기술 스택 (확정)
- Python 3.11+ / instagrapi 2.3+ / openpyxl / APScheduler / ffmpeg-python
- AI는 Claude Code 서브에이전트 (anthropic SDK 사용 X)

## 핵심 결정사항
1. **instagrapi 선택** — Graph API 대신 (ID/PW 로그인, ToS 위반, 밴 리스크 감수)
2. **accounts.xlsx 최소 입력** — username/password만, 나머지 자동
3. **엑셀 기반 검토** — yaml 버림. 50~100계정 규모에 엑셀이 훨씬 편함
4. **A/B 캡션 자동 제안** + 수기 오버라이드
5. **폴더 상태머신** — pending → uploaded/failed 자동 이동
6. **Harness Level 3** — ruff + mypy strict + pre-commit + 커스텀 훅(anthropic 임포트 금지, 시크릿 커밋 차단, 스키마 drift 방지)

## 파생 지식 (다른 프로젝트에서 재사용 가능)
- 콘텐츠 AI 자동화 도메인의 [[content-ai-automation#10. Instagram 릴스 자동 업로드]]에 패턴 기록
- instagrapi 세션 재사용 스니펫 — 모든 IG 봇 프로젝트에 공통
- BDH 파이프라인 적용 사례 — 요구사항 5번 변경에도 Spec 관리 가능(v1→v5)

## 완성된 컴포넌트 (2026-04-13 세션 종료 시점)

### Python 백엔드 (9개 모듈, 13 테스트 통과)
- accounts / config / state / scanner / uploader / planner / scheduler / cli

### Streamlit UI (app.py)
- 5개 탭 한글 메뉴: 대시보드 · 영상 업로드 · 예약 큐 · 계정 관리 · 로그
- streamlit-option-menu 수평 네비, 인스타 핑크(#E1306C) 테마
- 사이드바 제거, 헤더에 데몬 시작/중지 버튼 통합
- 드래그앤드롭 영상 업로드 + 즉시/예약 선택

### Windows 패키징
- install.bat / start_ui.bat / start_daemon.bat / README.md

### 검증된 E2E
- 실 계정 jmtw.12345 업로드 2건 성공 (삭제→재업로드 확인)

## 미완성 (의도적 유예)
- step-02: frames.py (ffmpeg 프레임 추출) — Claude Code 스킬과 쌍
- step-06: .claude/skills/instarup-analyze/ — A/B 캡션 서브에이전트 병렬
- step-07: 모의 Graph API E2E 테스트 (instagrapi 전환으로 요구 변경)
- Vercel + Next.js 모바일 UI — Phase 2 계획 단계

## 열린 질문
- 50계정 동시 운영 시 실제 밴율 — proxy 없이 실측 필요
- daily_limit 5의 적정성 — 계정 숙성도별 실측 필요
- 챌린지 자동 해결 — 현재 수동(`instarup relogin`), 자동화 어려움

## 관련 위키
- [[content-ai-automation]] §10 — 검증된 업로드 파이프라인
- [[marketing-automation]] — 상위 맥락
- [[taiwan-market]] — 대만시장 콘텐츠 맥락 (번체중문 캡션)
