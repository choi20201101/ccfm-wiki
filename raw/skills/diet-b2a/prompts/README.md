---
aliases: ["prompts/"]
---

# prompts/

Kling image2video에 보낼 프롬프트 텍스트. `scripts/kling_client.py`가 key별로 이 파일을 읽는다.

| 파일 | key | 영상 | 의도 |
|---|---|---|---|
| `v1_before_count.txt`  | `A3_fat`  | 영상1 Before | 10초 1-2-3 손가락 카운트 |
| `v1_after_count.txt`   | `A3_thin` | 영상1 After  | 10초 동일 싱크 |
| `v23_before_rhythm.txt`| `B4_fat`  | 영상2·3 전반 | 5초 팔 다운 리듬만 |
| `v23_after_dance.txt`  | `B4_thin` | 영상2·3 후반 | 5초 신나는 축하 춤 |

## 새 인물/콘셉트로 커스터마이즈
1. 의상/피부톤/배경 묘사만 교체 (동작 뼈대는 유지)
2. 남자 버전은 `Young Asian man in ...`, 아동은 정책상 금지
3. 프롬프트 끝 `vertical 9:16` 토큰은 반드시 유지
4. em-dash(—) 사용 금지 — Windows cp949에서 크래시 발생
