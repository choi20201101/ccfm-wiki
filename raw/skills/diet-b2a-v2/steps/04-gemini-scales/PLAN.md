# step-04 · Gemini 체중계 kg 치환 (10장)

## 목적
`cm/01.png` (88.0 원본), `cm/02.png` (44.0 원본)을 Gemini에 업로드해 세트별 kg 값으로 **디스플레이 숫자만** 치환. 외관/배경/로고/디스플레이 테두리 유지.

## 입력
- `cm/01.png`, `cm/02.png`
- `sets/setN/config.json` 의 `kg_before`, `kg_after`

## 출력
- `scales/setN/before.png` (새 kg, 로고 제거됨)
- `scales/setN/after.png`

## 프롬프트
```
Edit this digital scale photo. The CAS brand logo at top, the square screen shape, the 체중 label, the lighting, the perspective, and the borders must all stay EXACTLY the same. 

Change ONLY the large 7-segment digital number on the display to: {kg} kg

Keep the digits in the same 7-segment LCD font, same gray-green tint, same size, same position, same slight reflection. Output a clean photo of the scale with the new number.
```

## 실행
```bash
python gen_scales.py
python gen_scales.py --only set3
```

## 멱등
- 파일 존재 + 사이즈 > 30KB 면 skip
- 로고 제거 자동
