---
aliases: ["Step 01 — 에셋 준비 (오버레이 PNG 생성 + 얼굴 박스 확정)"]
---

# Step 01 — 에셋 준비 (오버레이 PNG 생성 + 얼굴 박스 확정)

## 목적
합성 단계에서 재사용할 자막 PNG 5장과 얼굴 모자이크 좌표를 결정한다. 이 단계 출력은 Kling 결과와 독립이라 병렬 가능.

## 입력
- `config.json`의 `copy` / `face_box` 블록
- (선택) 인물 이미지 → 얼굴 자동 검출

## 실행
```bash
python scripts/make_overlays.py --config config/<project>.json
python scripts/detect_face.py   --config config/<project>.json   # face_box.auto=true일 때만
```

## 처리
### 1.1 자막 오버레이 (Pillow, 투명 PNG)
| 파일 | 내용 | 폰트 | 크기 |
|---|---|---|---|
| `output/overlays/title.png`       | `copy.title` | 맑은 고딕 Bold | 72pt, stroke 6 |
| `output/overlays/label_before.png`| `copy.label_before` | 〃 | 90pt, stroke 6 |
| `output/overlays/label_after.png` | `copy.label_after`  | 〃 | 90pt, stroke 6 |
| `output/overlays/date_before.png` | `copy.date_before`  | 〃 | 48pt, stroke 4 |
| `output/overlays/date_after.png`  | `copy.date_after`   | 〃 | 48pt, stroke 4 |

모든 텍스트: 흰색 채움 + 검정 스트로크, 배경 투명.

### 1.2 얼굴 박스 확정
- `face_box.auto == true` 일 때: OpenCV Haar `haarcascade_frontalface_default.xml` 로 **after.png** 에서 검출.
- 검출 실패 시 기본값 `(325, 405, 112, 125)` 사용(원본 720×1280 좌표계).
- 검출 박스는 20% 축소 후 저장 — Kling 결과 얼굴은 보통 해당 영역 내.

## 출력
- `output/overlays/*.png` 5장
- `output/face_box.json` (x,y,w,h + source)

## 다음 단계
→ [02-kling-generate](./02-kling-generate.md)
