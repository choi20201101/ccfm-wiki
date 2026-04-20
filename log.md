# CCFM Wiki Log

## [2026-04-15] update | goglecc — 다이어트 B/A "예쁜 얼굴 + 통통 몸" V15 확정
- 사용자 승인: "만족스러운 결과가 나왔어" (15회 반복 후)
- 최종 파이프라인: Higgsfield Soul (strength 0.85 After + 0.6 Before_raw) + `fal-ai/face-swap`
- [[src-goglecc-seed-curation]] §9 (V15 아키텍처·엔드포인트·프롬프트·비용) + §10 (실패 경로 금지 리스트) 추가
- [[tacit/creative-patterns]]: "예쁜 얼굴+통통 몸" 레시피 (confidence high)
- [[tacit/coding-lessons]] 2건: (1) Gemini preserved-face body 부피 증가 거부 확정, (2) Higgsfield Soul API 실전 스펙(hf-api-key/hf-secret 헤더, /v1/custom-references, /higgsfield-ai/soul/standard)
- 핵심 인사이트: 한 AI 툴로는 목적 달성 불가 → **Higgsfield(몸 생성) + fal face-swap(얼굴 합성)** 파이프라인이 유일 해법
- 비용: ~$0.10/세트, 10세트 ~$1

## [2026-04-13] prune | 통합검색 크롤링(posts/collect.py) 레퍼런스 제거
- 사용자 지시: 통합검색 크롤링 불필요 → 위키에서 삭제
- 영향 파일: wiki/sources/src-cafe-crawler.md, wiki/tacit/coding-lessons.md
- 제거 항목: 파일 테이블 row, CLI 사용 예, 셀렉터 설명, rate limit 값, HITL 캡차 파일 레퍼런스, 크레덴셜 분리 언급

## [2026-04-13] restructure | 도메인 카테고리 확장 (7→14)
- 신규 도메인 7개 생성:
  - vibe-coding (바이브코딩 & 클로드 스킬)
  - marketing-automation (마케팅 자동화 AI)
  - finance (경영/재무/회계)
  - hr-admin (인사/총무)
  - viral (바이럴 지식)
  - psychology (심리학 & 인간의 본질)
  - content-ai-automation (기존, 유지)
- 도메인을 5개 카테고리로 그룹핑: 시장/사업, 조직/경영, 기술/자동화, 크리에이티브/마케팅, 인문/심리
- CLAUDE.md 업데이트: 도메인 구조, 암묵지 category enum, domain enum 확장
- index.md 전면 재작성
- 암묵지 유형 3개 추가: viral-patterns, coding-lessons, psychology-insights

## [2026-04-12] ingest | DA 크리에이티브 암묵지 8건
- 소스: CEO 구두 경험칙
- 생성: wiki/tacit/creative-patterns.md (8건)
- 업데이트: wiki/domains/da-creative.md, wiki/index.md

## [2026-04-12] ingest | Gemini Logo Remover v3.0
- 소스: CEO 직접 개발 + LaMa 비교 테스트 결과
- 생성: raw/reports/gemini-logo-remover-v3.md
- 생성: wiki/sources/src-gemini-logo-remover.md
- 업데이트: wiki/domains/ai-automation.md (로고 제거 섹션 추가)
- 생성: wiki/tacit/lessons-learned.md (LaMa vs OpenCV 교훈)
- 업데이트: wiki/index.md

## [2026-04-13] ingest | 네이버 카페 크롤링 모듈 지식화

## [2026-04-13] ingest | naverapi (네이버 검색광고 + Meta 광고) 모듈 지식화

## [2026-04-16] ingest | talmo 탈모 B/A 파이프라인 (루솔브 런칭용)
- 소스: `C:\Users\gguy\Desktop\talmo\` 전체 트리 (v1 완성: 1세트 검증 통과)
- 생성: wiki/sources/src-talmo-b2a.md (전체 파이프라인 + 교훈 + 스크립트 맵)
- 업데이트: wiki/domains/content-ai-automation.md §14 talmo (신설)
- 업데이트: wiki/tacit/creative-patterns.md (+6 항목 — 정수리위젯/조명대비/전환카드/2박스카피/계절의상/후킹핏)
- 업데이트: wiki/tacit/coding-lessons.md (+5 항목 — Haar 3단방어/Gemini합성표현/phone_look/HAIR_COLOR/cp949)
- 업데이트: wiki/tacit/psychology-insights.md (+4 항목 — 정수리공포/3개월시간축/쓸어올림제스처/조명대비)
- 업데이트: wiki/index.md (sources 목록에 src-talmo-b2a 추가)
- 핵심 결정: burst(고무줄 폭발) 씬 실험 후 폐기 → 3씬 + 헤어플립 엔딩으로 확정

## [2026-04-17] ingest | Multi-LLM Orchestrator v2.0.1 패치
- 소스: `C:\Users\gguy\Desktop\multi-llm-orchestrator-v2` (v1 API → v2 CLI subprocess 전환 + 4종 함정 패치)
- 업데이트: wiki/domains/ai-automation.md (Multi-LLM Orchestrator 섹션 신설)
- 업데이트: wiki/tacit/coding-lessons.md (+3 항목 — Windows .cmd 멀티라인 인자 함정 / CLI 플래그 변경 대응 / exit code+json-output 자동화 계약)
- 핵심 발견: Codex/Gemini 자체 SKILL.md 리뷰로 P0 가드레일 도출 (description 과잉 트리거 제거, 자동화 계약, 첫 실행 실패 차단)
- 영향 스킬: ~/.claude/skills/multi-llm-orchestrator/ + ~/.claude/commands/{askall,ask-all}.md

## [2026-04-20] ingest | 볼륨필인 앰플 광고 소재 자동생성 파이프라인 성공사례
- `wiki/sources/src-volumefill-pipeline-2026-04-20.md` 생성 (전체 케이스 스터디)
- `wiki/domains/da-creative.md` 에 링크·요약 추가
- `wiki/tacit/creative-patterns.md` 에 6개 패턴 추가 (타입 진단형 후킹, B/A 우회 12종, 나이 단정 회피, 시각 템플릿 선언, O 마스킹, 인종 강제)
- `wiki/tacit/coding-lessons.md` 에 6개 교훈 추가 (gpt-image 첫입력 fidelity, 백그라운드 조기종료, bash rm 영구삭제, rate limit 30분캡, Codex 크로스리뷰, 라운드로빈 정렬)
- 결과: 다음 프로젝트 시작 시 `projects/<new>/` 템플릿 복제 + 규칙 MD 6종 제품별 맞춤 → 동일 퀄리티 유지 가능
