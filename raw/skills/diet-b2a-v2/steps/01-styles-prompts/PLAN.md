---
aliases: ["step-01 · 5세트 스타일 & 프롬프트"]
---

# step-01 · 5세트 스타일 & 프롬프트

## 목적
5가지 TikTok/Insta 트렌드 댄스를 정의하고, 각 세트당 Kling 4종 프롬프트(v1_before, v1_after, v23_before, v23_after)를 생성.

## 입력
- `styles.json` (사람이 편집 가능한 세트 정의)

## 실행
```bash
python build_prompts.py
```

## 출력
- `prompts/set1..5/{v1_before,v1_after,v23_before,v23_after}.txt` (총 20개)

## 세트별 댄스
| id | 이름 | 특징 동작 |
|---|---|---|
| set1 | NewJeans Super Shy | 볼 손+부끄러움+작은 스텝 |
| set2 | Apple Challenge | 머리 손/허리 손 교차→팔 X→사이드 |
| set3 | aespa Supernova Chacha | 허리 차차차+팔 슬라이스+샤프 포즈 |
| set4 | Hot To Go (Chappell Roan) | 몸으로 H-O-T-G 글자 만들기 |
| set5 | Confident Flex | 부채질·어깨 흔들+엄지척+헤어플립 |

## 체중계 kg (5세트)
| set | before | after |
|---|---|---|
| 1 | 85.3 | 42.1 |
| 2 | 87.8 | 43.5 |
| 3 | 82.4 | 41.7 |
| 4 | 88.9 | 44.2 |
| 5 | 86.5 | 40.8 |

## 검증
- 20개 txt 파일 모두 존재, 공백 아님
- em-dash(—) 등 금지 문자 없음
- 각 파일에 "EXACT SAME" 또는 "synchronized" 또는 신체 묘사 포함
