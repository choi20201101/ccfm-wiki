---
aliases: ["볼륨필인 B/A 파이프라인 v1 (2026-04-20)"]
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-20
updated: 2026-04-20
sources:
  - C:/Users/gguy/Desktop/gpt/projects/volumefill/
---

# 성공사례: 볼륨필인 앰플 광고 소재 자동생성 파이프라인

> 기간: 2026-04-20 단일 세션 (약 5시간)
> 결과: 사용자 만족도 매우 높음 ("아주좋네~ 훨씬 좋아짐 매우 좋아짐")
> 제품: 메라블 유쎄라블 2X 볼륨필인 앰플 (55ml)

## 🎯 배경

40~55대 여성 타깃 볼륨 앰플 광고 소재를 ChatGPT web UI 자동화로 대량 생산. 123개 best 레퍼런스 기반 롤링 + 다양한 후킹 ideas 반영. 목표는 밤새도록 수백 장 소재 자동 생성.

## 🏗 파이프라인 아키텍처

```
분석 (Gemini) → 카피 생성 (Gemini + 규칙 MD) → 이미지 생성 (ChatGPT Chrome + Playwright) → 리사이즈 → QC
```

### 핵심 컴포넌트
1. **Best Refs 분석** (`scripts/analyze_best_refs.py`) — 123장 레퍼런스 이미지 → Gemini vision → frontmatter MD (main/sub 카피 개수·글자수·위치·폰트·색·효과·레이아웃)
2. **ref_loader** (`scripts/ref_loader.py`) — 123 ref MD 로드 + copy_id 기반 정확 매칭 또는 롤링
3. **카피 생성기** (`scripts/generate_copies_project.py`) — Gemini로 각 ref 구조에 맞는 볼륨필인 카피 생성. 180+ 후킹 아이디어 뱅크·14 페르소나·7 얼굴형 축·금지어 48개 필터
4. **Alt 워커** (`scripts/run_worker_alt.py`) — ChatGPT Chrome 2탭 번갈아 이미지 생성, 1200×1200 리사이즈
5. **Supervisor** (`scripts/supervisor_project.py`) — Chrome·워커 감시, 8분 stall 시 자동 재기동

## 🔑 성공 요인

### GFA(메타 광고) 심의 반려 회피
- 금지어 48개 (탱탱·차오른다·해결·탈출·필러·시술·N일만에·완판·1등…)
- **마스킹 규칙**: 필O·시O·보O스·주O (X 기호는 'ㅅㅂ' 연상 문제로 O로 전환)
- **B/A 직접 비교 금지** → 12가지 위트 우회
  - 타인 리액션 / 혼잣말 코미디 / 3인칭 목격담 / 메타 유머 / 오브젝트 스토리 / 다른 인물 대비 / 캐릭터 비유 / 과일 비유 / 시간 암시 등
- **나이 숫자 단정 금지** ("10년 어려짐" X, "5살 어려보여요" X) → '놀라는 사람'으로 표현

### 다양성 확보
- 페르소나 14개 (독박육아·해골라인·시O 대체·워킹 커리어우먼·자영업·중년 브런치·골프·갱년기·장모님·손자 돌봄·부부 기념일·자기관리)
- 얼굴형 축 7개 (V라인 무너짐·광대 도드라짐·이중턱·팔자주름·부기 동글이·땅콩 해골라인·목턱 경계)
- 민족 11종 가중 (한국 40% · 한백혼혈 16% · 백인 12.5% · 라틴 10% · 흑인 6% · 혼혈·중동·일본·알비노 등)
- 후킹 아이디어 180+ (13 섹션)

### 제품 무결성
- `product_identity.md` 실물 기반 스펙 (메탈릭 퍼플 캡 + 투명 유리 + 연 라벤더 + 5단 라벨)
- pd0/pd1 (뚜껑 O) 모델·히어로 컷 전용, pd2 (뚜껑 X 제형 쏟아짐) 텍스처 컷 전용
- enforce 블록 ⑤ "single source of truth" + negative anchors (no gold cap, no dropper…)

### 레퍼런스 스타일 충실도
- **첨부 순서**: ref 첫 번째 (gpt-image fidelity 편향 활용 — OpenAI 공식문서상 첫 이미지가 더 높은 fidelity로 보존)
- **TOP 배너 + BOTTOM enforce ⑥** 양쪽에서 조임
- "Typography Fidelity Hard Lock" — 자간·행간·폰트 캐릭터·강조 단어·줄바꿈 구조 레퍼런스 템플릿 복제 강제
- 카피·모델·제품만 교체, 그 외 시각 요소 그대로

### 운영 안정성
- Supervisor 야간 무인 운영 (Chrome 죽으면 자동 재기동, 8분 stall 자동 재기동)
- Rate limit 30분 캡 (ChatGPT 17시간 엄살 무시 — 실제 20~30분이면 풀림)
- 체크포인트 file-lock 동기화
- **절대 삭제 금지 규칙** — 소재 누적만

### Codex 크로스 리뷰
- 코드·규칙 MD 수정 시 multi-llm-orchestrator (Codex) 리뷰 후 반영
- 실수 방지 사례: 제품 뚜껑 색을 실물 확인 없이 추측으로 '골드/화이트' 썼다가 실물 확인 후 '메탈릭 퍼플' 정정

## 📁 재사용 자산

```
projects/volumefill/
├── config.json                 ← 제품 컨텍스트 + 정책 설정
├── pd/pd0.png, pd1.png, pd2.png ← 제품 누끼 (뚜껑 O 2장 + 쏟아짐 1장)
├── face/ (38장)                 ← 얼굴 레퍼런스 풀
├── best/ (123장)                ← 베스트 광고 레퍼런스
├── best_refs/ (123 MD)          ← 레퍼런스 구조 분석 결과
├── canvas/                      ← 퍼포먼스 캔버스 3분할 (제품·페르소나·시각화)
├── rejection_rules.md           ← GFA 심의 반려 회피 규칙
├── model_guide.md               ← 모델 연출 가이드 (quiet luxury 감성)
├── product_identity.md          ← 제품 시각 정체성 (실물 기반)
├── product_size.md              ← 크기 표현 가이드 (cm + palm-sized)
└── hook_ideas.md                ← 180+ 후킹 아이디어 뱅크

scripts/
├── analyze_best_refs.py         ← Gemini 비전 분석기
├── ref_loader.py                ← Ref MD 롤링 로더
├── generate_copies_project.py   ← 프로젝트 전용 카피 생성기
├── run_worker_project.py        ← 프로젝트 전용 이미지 워커
├── run_worker_alt.py            ← 탭 번갈아 오케스트레이터
└── supervisor_project.py        ← 야간 감시자
```

## 🚀 신규 프로젝트 복제 방법

1. `python scripts/new_project.py --name <신프로젝트>` 로 scaffold
2. `pd/`, `face/`, `best/` 자산 투입
3. `config.json` product_context 채우기
4. 규칙 MD 6종 (`canvas/`, `rejection_rules.md`, `model_guide.md`, `product_identity.md`, `product_size.md`, `hook_ideas.md`) 제품별 맞춤 작성
5. `analyze_best_refs.py` → `generate_copies_project.py` → `supervisor_project.py` 순서 실행

볼륨필인 프로젝트의 규칙 MD 구조를 **템플릿**으로 복제하고 제품별 내용만 교체해 동일 퀄리티 유지 가능.

## 🔗 관련 위키
- [[content-ai-automation]] — 콘텐츠 AI 자동화 전반
- [[da-creative]] — 퍼포먼스 광고 크리에이티브
- [[creative-patterns]] — 크리에이티브 암묵지
- [[coding-lessons]] — 기술 구현 암묵지
- [[psychology-insights]] — 설득 심리학

## 실수·학습
- bash `rm -f` 는 Windows 휴지통 안 거침 → 소재 누적 원칙 확립
- X 마스킹('시X')은 'ㅅㅂ' 연상 위험 → O 마스킹('시O') 로 전환
- Claude Code 백그라운드 태스크는 조용히 종료되는 이슈 있음 → Supervisor 필수
