# step-01 · README

## 산출물
- `prompts/set1..5/v1_before.txt` (10s, 좌우분할 before)
- `prompts/set1..5/v1_after.txt`  (10s, 좌우분할 after, synced)
- `prompts/set1..5/v23_before.txt` (5s, 영상2·3 전반 리듬)
- `prompts/set1..5/v23_after.txt`  (5s, 영상2·3 후반 춤)

## 다음 스텝
→ [02-gemini-session](../02-gemini-session/)

## 재실행
`styles.json` 편집 후:
```bash
python build_prompts.py
```
기존 prompts/ 는 덮어쓰기 됨 (재현성 문제 없음).
