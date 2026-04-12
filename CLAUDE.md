# CCFM Wiki Schema
@"
# CCFM Wiki Schema

## 볼트 목적
CCFM(콘크리트파머스) CEO 최재명의 비즈니스 지식 베이스.
마케팅 구독/유통 구독/브랜드 사업 3개 사업부 운영.
현재 핵심 이슈: M&A Exit(스마일게이트), 조직개편(A→Y/Z), 해외시장(대만/동남아/일본)

## 언어
한국어 기본. 영어 용어는 원문 유지.

## 3층 아키텍처 (카파시 LLM Wiki 패턴)
- raw/ : 원본 소스 (불변, LLM이 읽기만)
- wiki/ : LLM이 관리하는 위키 (LLM이 쓰기)
- CLAUDE.md : 스키마 + 룰 (사람과 LLM이 공동 진화)

## 지식 분류 체계 (형식지 + 암묵지)

### 형식지 (Explicit Knowledge)
문서화된 명시적 지식. raw/에 원본, wiki/에 정리본.
- 규제/법률: TFDA, BPOM, 표시광고법
- 계약/재무: SPA 조건, 네이버 파트너 계약, 수수료 구조
- 프로세스: 쿠팡 입점 절차, TFDA 등록 절차
- 데이터: 매출 추이, ROAS, 광고비

### 암묵지 (Tacit Knowledge)
경험에서 나온 비명시적 지식. 대화/판단/실수에서 추출하여 위키에 명시화.

#### 암묵지 유형과 추출 방법
| 유형 | 예시 | 추출 트리거 | 저장 위치 |
|------|------|-----------|----------|
| 판단 기준 | "네이버 GFA ROAS 150% 이하면 소재 교체" | 의사결정 순간 | wiki/tacit/decision-rules.md |
| 협상 감각 | "스마일게이트 측이 이 조건 넣으면 후순위 지분 희석 의도" | 협상 리뷰 시 | wiki/tacit/negotiation-patterns.md |
| 사람 읽기 | "백영무 부장은 비공식 채널로 먼저 떠봐야 함" | 커뮤니케이션 후 | wiki/tacit/people-dynamics.md |
| 시장 감각 | "대만은 B&A 콘텐츠가 먹히고 일본은 성분 소구" | 시장 분석 시 | wiki/tacit/market-intuition.md |
| 실패 교훈 | "인도네시아 크로스보더 시도 → 배송 7일 → 반품률 40%" | 실패 복기 시 | wiki/tacit/lessons-learned.md |
| 운영 노하우 | "쿠팡 로켓그로스 전환 시 최소 2주 재고 확보" | 운영 판단 시 | wiki/tacit/operational-heuristics.md |
| 크리에이티브 감각 | "릴스 1초컷 + 상단자막이 CTR 2배" | DA 리뷰 시 | wiki/tacit/creative-patterns.md |
| 바이럴 감각 | "댓글 유도형 훅이 공유율 3배" | 바이럴 복기 시 | wiki/tacit/viral-patterns.md |
| 코딩/자동화 교훈 | "LaMa보다 OpenCV가 나은 조건" | 기술 비교 시 | wiki/tacit/coding-lessons.md |
| 심리/설득 원칙 | "B&A에서 Before 어둡게 → 손실회피 자극" | 심리 적용 시 | wiki/tacit/psychology-insights.md |

#### 암묵지 추출 규칙
- 대화 중 "~하면 ~해야 해", "보통 ~하면 ~됨", "경험상~" 패턴 감지 시 자동 추출
- 의사결정 이유를 물었을 때 나오는 답변에서 추출
- 실패/성공 복기에서 패턴 추출
- 추출된 암묵지는 confidence 태그 필수 (경험 횟수 기반)
- 모순되는 암묵지 발견 시 양쪽 병기 + 조건 차이 분석

#### 암묵지 페이지 프런트매터
---
type: tacit
category: decision-rule | negotiation | people | market | lesson | operation | creative | viral | coding | psychology
confidence: high (5회+ 검증) | medium (2-4회) | low (1회, 가설)
first_observed: YYYY-MM-DD
last_confirmed: YYYY-MM-DD
contradiction: none | 충돌하는 암묵지 링크
---

## 페이지 프런트매터 (형식지)
---
type: entity | domain | decision | source | concept
domain: taiwan | sea | japan | ma | org | ai | marketing | brand | vibe-coding | marketing-automation | finance | hr-admin | viral | psychology | content-ai | da-creative
confidence: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
---

## Ingest 워크플로우
1. raw/에 새 소스 저장
2. 소스 읽고 요약 → wiki/sources/src-{slug}.md 생성
3. 관련 엔티티/도메인 페이지 업데이트 (기존 내용에 추가, 덮어쓰기 금지)
4. 모순 발견 시 ⚠️ 표시하고 양쪽 주장 병기
5. 암묵지 패턴 감지 시 wiki/tacit/ 해당 페이지에 추가
6. wiki/index.md 업데이트
7. log.md에 엔트리 추가: ## [YYYY-MM-DD] ingest | 소스제목

## Query 워크플로우
1. wiki/index.md 먼저 읽어서 관련 페이지 파악
2. 관련 페이지 drill down (형식지 + 암묵지 모두 참조)
3. 답변에 [[위키링크]]로 출처 표시
4. 가치 있는 답변은 wiki/에 새 페이지로 저장 제안

## Lint 워크플로우
- 페이지 간 모순 찾기
- 인바운드 링크 없는 고아 페이지 찾기
- 자체 페이지 필요한데 없는 중요 개념
- 누락된 교차 참조
- 낡은 정보 표시
- 암묵지 중 confidence: low가 90일 이상 미검증 시 플래그

## 도메인 구조

### 시장/사업 (Markets & Business)
- taiwan-market : TFDA, 샵라인, 홍콩법인, Merable TW
- sea-tiktok : 동남아 틱톡샵, BPOM, 할랄
- japan-market : Q10 메가세일, X채널
- ma-exit : 스마일게이트 딜, SPA, 네이버 계약 승계

### 조직/경영 (Organization & Management)
- org-restructure : A→Y/Z 모델, AI Cell, 4단계 롤아웃
- finance : 경영/재무/회계, 다법인 세무, 이전가격
- hr-admin : 인사/총무, 보상구조, 조직운영

### 기술/자동화 (Tech & Automation)
- vibe-coding : 바이브코딩, Claude Code 스킬 파이프라인, 프롬프트 엔지니어링
- ai-automation : 스킬 파이프라인(bob/dd/harness/eval/learnings), DA 자동화
- content-ai-automation : 컷편집, 비전분석, Whisper, 자막레이아웃, bob계획서
- marketing-automation : 광고 플랫폼 자동화, 리포트, CRM, 크롤링

### 크리에이티브/마케팅 (Creative & Marketing)
- da-creative : 세이프존, 1초컷, 프롬프트 DB, Gemini/Kling
- viral : 바이럴 메커니즘, 밈 구조, 시딩 전략, 알고리즘

### 인문/심리 (Human & Psychology)
- psychology : 소비자 심리, 설득, 조직심리, 인간 본질, 행동경제학

## 스킬 파이프라인 연결
- 스킬 경로: ~/.claude/skills/user/
- 파이프라인: bob → dd → harness → eval → learnings
- 러닝 결과는 wiki/domains/ai-automation.md에 누적
- 러닝 중 암묵지 패턴 발견 시 wiki/tacit/에도 교차 저장

## 핵심 엔티티
- Merable: 뷰티 브랜드, 대만/일본/동남아 진출
- Rusolve: 탈모 브랜드, 2026 런칭
- 스마일게이트: M&A 인수자 (컨소시엄)
- 백영무: 네이버 채널컨설팅 담당
- 신동협: AI Cell 리더 후보
- 강용길: 제품 컴플라이언스 담당

## 금지 사항
- 재무 수치/밸류에이션 추정 금지
- raw/ 파일 수정 금지
- 확인 안 된 정보에 confidence: high 금지
- 위키 페이지 덮어쓰기 금지 (항상 추가/병합)

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
