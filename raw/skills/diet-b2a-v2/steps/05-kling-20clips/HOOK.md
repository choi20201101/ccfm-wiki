---
aliases: ["step-05 HOOK — 40클립 대량 생성 전략"]
---

# step-05 HOOK — 40클립 대량 생성 전략

## 동시성 규칙
- Kling API는 동시 제출 제한이 있음 (계정당 2~5). 초과 시 429
- 전략: 전부 submit 먼저 → 그 다음 모든 task polling → 완료된 것 순차 다운로드
- submit 2초 간격 sleep 으로 리밋 회피

## 장애 대응
- submit 5xx: 30/60/120s 백오프, 최대 3회
- poll 실패: 엔드포인트 fallback (singapore ↔ global)
- 생성 실패(failed): 해당 key 만 재제출 권장 (자동 1회 재시도)

## 비용 보호
- submit 전 "이미 생성된" 체크 (task_id + 파일 존재)
- tasks.json 은 submit 즉시 flush → 크래시 재실행 시 재제출 방지
