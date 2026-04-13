# Step 00 — 입력 검증

## 목적
사용자가 제공한 4장의 이미지 + config.json이 스킬이 요구하는 최소 조건을 만족하는지 검사. 실패하면 이후 단계 전부 무의미하므로 여기서 결정적으로 reject.

## 입력
- `config/<project>.json`
- 위 JSON이 가리키는 4장의 PNG

## 실행
```bash
python scripts/validate_input.py --config config/<project>.json
```

## 검증 규칙
| 항목 | 기준 | 실패 시 |
|---|---|---|
| 4개 이미지 파일 존재 | fs check | abort |
| 인물 이미지 비율 | 9:16 ± 20% 권장 | warn + autocrop 예고 |
| 체중계 이미지 | 세로 ≤ 2.2× 가로(정사각 근처) | abort |
| 최소 해상도 | 인물 ≥ 1000px 세로, 체중계 ≥ 800px 변 | abort |
| `copy` 블록 | 필수 5개 키 존재, 빈 문자열 금지 | abort |
| `face_box` | x,y,w,h 정수 or `"auto": true` | abort |
| 오디오 3개 파일 존재 | optional(없으면 무음) | warn |
| Kling API 키 | `api.txt` 존재, `Access Key`/`Secret Key` 라인 | abort |

## 출력
- 성공: `output/validation_ok.flag` 빈 파일 생성
- 실패: stderr에 명확한 원인 + exit code 2

## 다음 단계
→ [01-asset-prep](./01-asset-prep.md)
