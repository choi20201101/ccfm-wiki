---
aliases: ["step-05 · Kling 40 클립 생성"]
---

# step-05 · Kling 40 클립 생성

## 목적
10세트 × 4 key = **40 클립** 을 Kling image2video로 생성.
- A_before (10s) · A_after (10s) — 영상1 좌우분할용 (세트 고유 동작)
- B_before (5s)  · B_after (5s)  — 영상2·3 전후 하드컷용

## 입력
- `seeds/setN/{before,after}.png` (step-03 산출)
- `steps/01-styles-prompts/prompts/setN/{v1_before,v1_after,v23_before,v23_after}.txt`
- `api.txt` (Kling Access/Secret)

## 출력
- `raw/setN/{A_before,A_after,B_before,B_after}.mp4`
- `raw/tasks.json` (멱등 상태)

## 실행
```bash
python gen_kling.py              # 40 클립 순차 제출
python gen_kling.py --only set3
python gen_kling.py --parallel 4 # 동시 4개 제출
```

## 시간/비용
- std 10s × 20 = 평균 3~6분 × 20 = 60~120분
- std 5s × 20 = 평균 2~3분 × 20 = 40~60분
- 총 2~3시간 (순차) / 30~60분 (병렬)

## 멱등
- `raw/tasks.json` 에 task_id 있고 mp4 파일 > 100KB 면 skip
- 세션 만료 시 자동 JWT 재발급
