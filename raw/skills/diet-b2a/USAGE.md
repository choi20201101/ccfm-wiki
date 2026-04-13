# USAGE — 실행 방법

## 0. 사전 준비
```bash
pip install pyjwt requests pillow
# 선택(얼굴 자동 검출):
pip install opencv-python
```
- `ffmpeg`, `ffprobe` PATH에 있어야 함
- Windows 한글 폰트: `C:/Windows/Fonts/malgunbd.ttf` 기본 사용

## 1. 프로젝트 폴더 구성
```
<workdir>/
├── api.txt                              # Kling Access/Secret Key
├── diet-b2a-skill/                      # 본 스킬(이 디렉토리)
├── audio/                               # 선택 배경음 (없으면 무음)
│   ├── track1.mp3
│   ├── track2.mp3
│   └── track3.mp3
└── my_project/
    ├── before.png                       # 인물 전 (AI 생성)
    ├── after.png                        # 인물 후 (AI 생성)
    ├── scale_before.png                 # 체중계 전
    ├── scale_after.png                  # 체중계 후
    └── config.json                      # 아래 템플릿 복사
```

## 2. config.json 작성
`diet-b2a-skill/config/default.json` 을 복사하고 5가지 슬롯만 바꾸면 됨:

| 키 | 의미 |
|---|---|
| `project_name` | 구분용 이름 |
| `input.*_image` | 4장 PNG 경로 (config 기준 상대 경로) |
| `copy.title/label_*/date_*` | 자막 한글 카피 5개 |
| `face_box` | 수동 좌표 or `"auto": true` |
| `audio.v{1,2,3}` | 3개 배경음 경로(선택) |

## 3. 실행 — 원샷
```bash
cd diet-b2a-skill
python scripts/run_all.py --config ../my_project/config.json
```
오케스트레이터가 00 → 05 순차 실행. 중간에 끊겨도 다시 돌리면 마지막 완료 지점부터 재개(멱등).

## 4. 실행 — 단계별
```bash
python scripts/validate_input.py --config ../my_project/config.json
python scripts/make_overlays.py  --config ../my_project/config.json
python scripts/detect_face.py    --config ../my_project/config.json
python scripts/kling_client.py   --config ../my_project/config.json
python scripts/compose.py        --config ../my_project/config.json
python scripts/qa_check.py       --config ../my_project/config.json
python scripts/export.py         --config ../my_project/config.json
```

특정 단계부터만:
```bash
python scripts/run_all.py --config ... --from 03
```

## 5. 결과물 위치
```
<output_dir>/
├── 영상1.mp4
├── 영상2.mp4
├── 영상3.mp4
├── thumbs/영상{1,2,3}.jpg
├── captions/영상{1,2,3}.txt
├── qa_report.{json,md}
└── release.zip         ← 업로드용 일괄 패키지
```

## 6. 변형 레시피
### 다른 인물로 교체
1. `input/*.png` 4장만 갈아끼움
2. `copy` 블록 업데이트 (날짜, 체중)
3. `run_all.py` 재실행 → Kling 재호출 (비용 발생) + 재합성

### 의상/동작 변경
- `prompts/*.txt` 를 편집 (새 파일 만들고 `kling_client.py`의 `JOBS` 매핑 변경 권장)
- 캐시 날리기: `output/tasks.json` 에서 해당 key 삭제 후 재실행

### 톤/감정 변경
- `HOOK.md` 의 훅 라이브러리에서 원하는 카피 선택 → `config.copy.title` 교체

### 길이 조절
- `config.layout.cut_seconds` / `after_len_seconds` 수정
- 영상1 길이는 `kling.duration_v1` ("5" 또는 "10")

## 7. 비용/시간 가이드
| 단계 | 소요 |
|---|---|
| Kling std 5s | 평균 2~3분 |
| Kling std 10s | 평균 3~6분 |
| 4개 클립 병렬 제출 후 대기 | 총 7~12분 |
| ffmpeg 합성 3개 | 10~40초 |

std 기준 4 클립 = 대략 한국어 콘텐츠 3본 = 몇 달러 선 (Kling 과금 기준 참고).

## 8. 트러블슈팅
| 증상 | 원인/해결 |
|---|---|
| `cp949 can't encode ...` | 프롬프트/config에 em-dash(—) 들어감. 빼고 재실행 |
| Kling `code: 1201 Task not found` | task_id 오타 or 7일 경과. `output/tasks.json` 해당 key 삭제 후 재제출 |
| 얼굴 모자이크가 얼굴을 벗어남 | `config.face_box` 수동 조정 또는 `"auto": true` + opencv 설치 |
| 영상2/3에서 전→후 전환이 끊겨 보임 | `prompts/v23_*.txt` 에 "ends with arms at sides"/"starts with arms at sides" 조건이 남아있는지 확인 |
| 자막이 체중계를 가림 | `config.layout.v{2,3}.date_xy` 조정, 체중계 박스 위쪽 여백 확인 |
