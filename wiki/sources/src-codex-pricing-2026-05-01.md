---
aliases: ["Codex CLI 한도", "ChatGPT ProLite 한도"]
type: source
category: ai-automation
confidence: high
first_observed: 2026-05-01
last_confirmed: 2026-05-01
sources:
  - https://developers.openai.com/codex/pricing (OpenAI 공식)
  - https://chatgpt.com/codex/pricing/ (OpenAI 공식, 일부 region 403)
  - https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
  - https://community.openai.com/t/understanding-the-new-codex-limit-system-after-the-april-9-update/1378768
  - https://www.knightli.com/en/2026/04/15/codex-usage-limits-five-hour-weekly-credits/
  - https://allthings.how/codex-token-and-rate-limits-explained-for-chatgpt-plans/
  - 실측: ceo@mkm20201101.com Codex CLI v0.125.0 (2026-05-01 10:51 KST)
---

# Codex CLI 한도 체계 (2026-05 시점)

ChatGPT 구독 OAuth로 Codex CLI 호출 시 적용되는 두 종류 한도. 검색 결과 종합 + 실측.

## 플랜별 5h 롤링 한도 (메시지 기준)

| 플랜 | GPT-5.5 / 5h | GPT-5.4 / 5h | GPT-5.3-Codex | Code Reviews |
|---|---|---|---|---|
| Plus ($20) | — | 5.4-mini 1200–7000 | 600–3000 local + 200–1200 cloud | 400–1000 |
| **Pro $100 (Pro 5x) = JWT `prolite`** | 80–400 | 100–500 | 600–3000 local + 200–1200 cloud | 400–1000 |
| Pro $200 (Pro 20x) | 300–1600 | 400–2000 | (5x 대비 5배) | (5x 대비 5배) |

**부스트**: 2026-05-31까지 한시적 ×2 부스트 적용. 위 표 수치 그대로 두 배.

## 주간 캡 (Weekly Cap)

- 별도 존재. **공식 수치 미공개**.
- 모델 풀이 통합된 듯 (실측: gpt-5.5 차단 시 gpt-5.4도 동일 시각에 차단).
- 5h 윈도우보다 먼저 터지는 경우 흔함 (특히 reasoning 시간 길 때).

## 비용 드라이버

- **메시지 수가 아니라 agent reasoning 시간**.
- `reasoning effort` 기본값:
  - codex CLI: `xhigh` (가장 비쌈)
  - 권장: 평상시 `medium`, 정밀 작업만 `high`/`xhigh`
- agentic 한 번 run이 5h 풀의 20%+ 먹을 수 있음.

## 막혔는지 진단하는 법

`ERROR: You've hit your usage limit ... try again at <date>` 메시지 받으면:
- `<date>`가 **지금 + 5h 이내** → 5h 롤링 캡
- `<date>`가 **지금 + 1일 이상** → 주간 캡

세션 중에는 codex 내부 명령 `/status` 로 남은 한도 확인 가능.

## ProLite 명칭 미스매치

- JWT (`chatgpt_plan_type`): `prolite`
- OpenAI 공식 가격 페이지: "Pro $100/month" 또는 "Pro 5x"
- 동일 등급. "Pro Lite"라는 별도 SKU는 없음.

## 관련

- [[wiki/domains/ai-automation#Codex CLI 한도 체계]]
- [[wiki/domains/ai-automation#AI CLI 인증 모드 표준]]

**Tags**: #status/active #domain/ai-automation #source/openai-official #confidence/high
