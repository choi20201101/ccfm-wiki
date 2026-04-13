---
type: domain
domain: ai
confidence: low
created: 2026-04-12
updated: 2026-04-12
sources: []
---

# AI 자동화 (AI Automation)

## 개요
스킬 파이프라인(bob/dd/harness/eval/learnings), DA 자동화 관련 도메인.

## 스킬 파이프라인
_내용 추가 예정_

## DA 자동화
_내용 추가 예정_

## 러닝스 누적
_내용 추가 예정_

## 관련 페이지
- [[org-restructure]]
- [[da-creative]]


## Gemini 로고 제거 (2026-04-12 추가)
→ [[src-gemini-logo-remover]] 참조

### 현재 최선 기술
- OpenCV TELEA+NS 인페인팅 50:50 블렌딩
- LaMa(simple-lama-inpainting) 대비 우위 확인
- 품질: 60~70점 / 비교 대상 추가 예정

### 암묵지 추출
- Gemini 로고는 극소 영역(이미지 대비 4~5%)이라 딥러닝보다 OpenCV가 유리
- LaMa가 오히려 나쁜 경우: 마스크 크기 작고 주변 배경 단순할 때
- → [[lessons-learned]] 교차 저장됨

## 최재명 대표 i-boss 인사이트 (2026-04-13 추가)
원본: [[src-iboss-choi-jaemyeong]] · 인덱스: `raw/inbox/2026-04-13-iboss-choi-jaemyeong-201articles.md`

### AI 시대 실행 격차 = 10~100배
- "아는 것 ≠ 쓰는 것 ≠ 성과 내는 것" — 3단 분리가 핵심
- CLI(Claude Code)는 IDE 대비 10배 빠름 — 병렬 실행·파이프라인·스크립팅 가능
- SDD/DDD 도입으로 수정 3~4회 → 1~2회로 감소
- 월 $100~200 토큰을 일주일 내 소진하는 게 실력 지표
- 마케터 AI 활용/미활용 생산성 격차 변곡점: 2026-2027년

### 암묵지 × AI 협업 공식
- "Claude는 IQ 1000짜리 신입" — 도메인 기준을 명시화해야 작동
- "5단계로 보이는 업무가 실제론 30단계" — 숨은 단계가 자동화 70% 벽
- 도메인 전문성 × AI 활용 능력 = 생존 공식

### AI 무중단 스튜디오 (일매출 8천만 사례)
- 나노바나나 · Midjourney · Runway · Veo3 조합
- 모델비·촬영비 없이 300종 A/B, CPC 400→300원
- 용도별 분리: Higgsfield(사실성) · Midjourney(일관성) · Flux(포즈)

### 스킬/에이전트 빌딩
- 프롬프트 → 스킬(재현성) → 에이전트(자율성)로 단계 진화
- bob(설계) → dd(분해) → harness(강제) → eval(평가) → learnings(피드백)
- 산출물 품질은 "강제 규칙(린터·하네스)" 유무가 결정
- → [[wiki/tacit/coding-lessons]] 2026-04-13 엔트리 교차 저장
