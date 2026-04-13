# diet-b2a — 다이어트 Before/After 릴스 자동화 스킬

Kling AI + ffmpeg + Pillow로 **다이어트 변신 3종 릴스**(좌우분할 / 우측 체중계 하드컷 / 좌측 체중계 하드컷)를 한 번에 생성.

## 30초 요약
1. `config.json` 에 4장 이미지 경로 + 5줄 카피만 기입
2. `python scripts/run_all.py --config <path>`
3. `output/영상{1,2,3}.mp4` + `release.zip` 획득

## 파이프라인 (bdh)
```
bob   → PLAN.md            스펙/의도 단일 진실
dd    → steps/00~05/*.md   단계별 결정적 분해
harness → harness/RULES.md 멱등·품질 가드레일
```

## 문서 지도
| 문서 | 역할 |
|---|---|
| [SKILL.md](SKILL.md) | 스킬 진입점 (트리거/메타) |
| [PLAN.md](PLAN.md) | 스펙·목표·좌표·성공 기준 |
| [HOOK.md](HOOK.md) | 자극 카피 훅 라이브러리 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 내부 기술·필터·상태 |
| [USAGE.md](USAGE.md) | 실행 방법·트러블슈팅 |
| [steps/*.md](steps/) | dd 단계별 README |
| [harness/RULES.md](harness/RULES.md) | 멱등·품질 규칙 |

## 재사용 포인트
- `prompts/*.txt` 만 갈아끼우면 동작/톤 변경
- `config/default.json` 복사 후 5개 슬롯 수정하면 새 인물 프로젝트
- `scripts/run_all.py` 로 원샷 생성, 중간 실패 시 자동 재개

## 라이선스/윤리
- **AI 생성 인물 이미지**만 사용 (실존 인물 사진 금지)
- 레퍼런스 mp3는 개발 가이드용. 업로드 시 플랫폼 공식 음원 재매칭 권장
