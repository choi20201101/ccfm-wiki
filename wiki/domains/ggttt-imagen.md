---
type: domain
domain: ai-automation
confidence: high
created: 2026-04-30
updated: 2026-04-30
sources:
  - C:\Users\gguy\Desktop\ggttt\README.md
  - C:\Users\gguy\Desktop\ggttt\harness\AGENTS.md
  - C:\Users\gguy\.claude\skills\imagen\SKILL.md
  - C:\Users\gguy\.claude\skills\gptim\SKILL.md
  - C:\Users\gguy\.claude\skills\rubyrn-pipeline\SKILL.md
---

# ggttt-imagen — GPT 우회 이미지 생성 (CCFM 커스텀)

> **분류**: domains / AI-automation
> **최종 업데이트**: 2026-04-30
> **연관**: [[gptim-ad-creative-batch]], [[ai-automation]], [[da-creative]], [[vibe-coding]]

## 1. 한 줄 정의

`god-tibo-imagen` (ChatGPT 비공식 백엔드) 을 한국어 자연어로 호출하는 Claude Code 스킬 + 실행 환경.
경로: `C:\Users\gguy\Desktop\ggttt`. 깃허브 원본을 **그대로 쓰지 않고** 보안·재현성 룰을 덧씌운 CCFM 커스텀.

## 2. 왜 커스텀했나

| 깃허브 원본 위험 | CCFM 커스텀 대응 |
|---|---|
| 모델·effort 미강제 → 호출마다 결과 다름 | `gpt-5.5-pro` + `reasoning_effort=max` 강제 (멱등성) |
| `CODEX_BASE_URL` 임의 변조 가능 → 토큰 탈취 가능 | openai.com 도메인 화이트리스트, 외 즉시 거부 |
| 출력 경로 검증 없음 → path traversal | cwd escape 차단 |
| 입력 이미지 검증 없음 | 확장자(.png/.jpg/.jpeg/.webp/.gif) + 50MB 상한 |
| 진행 로그에 프롬프트·에러 원문 저장 | 60자 이상 문자열 자동 truncate |
| `--debug` 덤프에 인증정보 포함 | 사용 금지, 가드레일 명시 |

## 3. 거의 동일한 결과를 보장하는 두 핀

> 사용자 표현 그대로: **"코덱스 CLI 최신 + gpt-5.5(pro) + reasoning max" 두 핀만 박으면 어떤 에이전트가 돌려도 거의 동일한 결과가 나온다**.

1. **Codex CLI 최신**: `codex --version` → 구버전이면 `npm i -g @openai/codex@latest` (수동).
2. **모델·effort 강제**:
   - `CODEX_IMAGEGEN_MODEL=gpt-5.5-pro`
   - `CODEX_REASONING_EFFORT=max`
   - 백엔드 거부 시 `gpt-5.5` + `high` 폴백

이 두 가지를 모든 스크립트(`scripts/generate.mjs`, `edit.mjs`, `batch.mjs`)에서 자동 적용.

## 4. 디렉토리 구조 (BDH)

```
ggttt/
├── .claude/skills/imagen/SKILL.md   ← 스킬 정의
├── bob/SPEC.md                      ← 의도
├── dd/step-00-precheck/             ← 환경 점검
├── dd/step-01-generate/             ← 신규 생성
├── dd/step-02-edit/                 ← 입력 이미지 편집
├── dd/step-03-batch/                ← 배치
├── harness/AGENTS.md                ← 강제 규칙 (R1~R11)
├── scripts/                         ← 커스텀 실행 스크립트
└── out/                             ← 결과물 (.gitignore)
```

## 5. 연관 글로벌 스킬 (모두 같은 강제 룰 적용)

| 스킬 | 역할 |
|---|---|
| [[ai-automation\|imagen]] (`~/.claude/skills/imagen/SKILL.md`) | 단일 이미지 생성·편집 |
| [[gptim-ad-creative-batch\|gptim]] (`~/.claude/skills/gptim/SKILL.md`) | 광고 소재 N장 배치 (6질문 인터뷰) |
| `rubyrn-pipeline` (`~/.claude/skills/rubyrn-pipeline/SKILL.md`) | 24h 자율 광고 소재 생성 파이프라인 |

세 스킬 모두 2026-04-30 자로 동일한 보안·모델 강제 룰을 공유.

## 6. 보안·정책 주의사항

- `~/.codex/auth.json` 토큰은 **계정 권한 그 자체** — 외부 전송/백업 금지.
- ChatGPT 정책 위반 시 계정 정지 위험. 본인 한도 안에서만 사용.
- `--debug`/`--debug-dir` 사용 금지 (요청·응답 SSE 원문에 인증정보 포함).
- `gti` CLI 직접 호출 금지 (커스텀 스크립트의 강제 룰 우회됨).

## 7. 배치 운영 노하우

- 동일 ChatGPT 계정 → 1세션 순차 호출만 (병렬 금지)
- 1장당 평균 140초, 80장 ≈ 3시간
- 매 호출 사이 1.5초 sleep (페이싱)
- 401 → 즉시 종료 + `codex login` 안내
- 429 → 8s 대기 후 1회 재시도

## 8. 참고

- 깃허브 원본: https://github.com/NomaDamas/god-tibo-imagen
- 동작 원리: `~/.codex/auth.json` 의 ChatGPT 세션 → `codex/responses` SSE → PNG 추출
- **공식 API 가 아니다** — 백엔드 변경 시 깨짐
