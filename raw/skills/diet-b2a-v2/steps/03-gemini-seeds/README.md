# step-03 · README

## 실행
```bash
python gen_seeds.py              # 전체 5세트
python gen_seeds.py --only set3  # 한 세트만
python gen_seeds.py --force      # 기존 시드 덮어쓰기
```

## 산출물
- `../../seeds/setN/before.png` — 뚱뚱 + 방 어지러움 + 밤
- `../../seeds/setN/after.png`  — 마름 + 방 정리 + 낮
- 두 장 모두 **Gemini ✦ 로고가 자동 제거된** 상태로 저장됨

## 로고 제거 파이프라인
- `scripts/gemini_client.py` 내부에서 생성 직후 `logo_remover.py` 자동 호출
- 하단 좌/우 코너 타원형 마스크 → OpenCV TELEA+NS 블렌딩 → 가우시안 블렌딩
- ~0.5초/장, 90%+ 제거율

## 다음
→ [04-gemini-scales](../04-gemini-scales/)
