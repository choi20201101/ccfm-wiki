# M4 모듈 — Claude Code 컨텍스트

## 이 프로젝트는

M3 기획안(JSON) + TTS 오디오 + SFX 라이브러리를 입력받아
Premiere Pro에서 바로 임포트 가능한 XMEML 타임라인을 자동 생성하는 모듈이다.

전체 개요: `MD/M4_모듈개요.md`
전체 계획: `MD/M4_계획서.md`

---

## 운영 경로

**최종 운영 위치**: `/Volumes/01_마케팅사업부_직원/{NAS_USER}/3팀 영상 자동화/M4/`
**개발 위치**: `/Users/nuri/Desktop/클로드/M4/`

코드는 `BASE_DIR = Path(__file__).parent` 상대경로 기반이라 두 위치 모두 동일하게 동작.

---

## 폴더 구조

```
M4/
├── CLAUDE.md
├── config.json
├── m4_run.py
├── utils.py
├── STEP1/
│   ├── __init__.py
│   ├── STEP1_오디오컷편집.md
│   └── step1_audio_cut.py
├── STEP2/
│   ├── __init__.py
│   ├── STEP2_자막자동화.md
│   └── step2_whisper_sub.py
├── STEP3/
│   ├── __init__.py
│   ├── STEP3_FCPXML빌드.md
│   └── step3_fcpxml.py
├── MD/
│   ├── M4_모듈개요.md
│   └── M4_계획서.md
├── input/
│   ├── YYYYMMDD_브랜드[_N]/
│   │   ├── 05_브랜드_M3_M4마커.json   (또는 scenes.json)
│   │   └── YYYYMMDD_브랜드_tts.mp3   (또는 .wav, *tts* 패턴 매치)
│   └── sfx/
└── output/
    └── YYYYMMDD_브랜드[_N]/
        ├── *_tts_cut.mp3
        ├── *_subtitle_chunks.json
        ├── *_subtitle_ko.srt
        ├── *_timeline.xml
        └── sfx/
```

---

## 스텝별 설계 문서 경로

작업 전 반드시 해당 스텝 MD를 읽고 구현한다.

| 스텝 | 설계 문서 | 구현 파일 |
|------|----------|----------|
| STEP1 | `STEP1/STEP1_오디오컷편집.md` | `STEP1/step1_audio_cut.py` |
| STEP2 | `STEP2/STEP2_자막자동화.md` | `STEP2/step2_whisper_sub.py` |
| STEP3 | `STEP3/STEP3_FCPXML빌드.md` | `STEP3/step3_fcpxml.py` |
| 통합 | `MD/M4_계획서.md` | `m4_run.py` |

---

## 핵심 규칙

- API 사용 금지 — 모든 처리는 로컬에서 실행
- 외부 라이브러리: `pydub`, `openai-whisper` (import명: `whisper`), `ffmpeg`
- STEP3 파일 경로: 반드시 `Path.as_uri()` 사용 (한글 경로 URL 인코딩)
- STEP3 타임코드: **정수 프레임** 사용 (`round(seconds * 30)`, FPS=30) — rational 형식 아님
- STEP3 포맷: **XMEML** (`<xmeml version="4">`) — FCPXML 아님, Premiere가 `.fcpxml` 임포트 불가
- STEP3 자막 색상: `forecolor` 파라미터 사용 (`fontcolor`는 Premiere가 무시)
- STEP3 SFX 트랙: A3 단일 트랙에 시간순 배치, 이전 SFX 끝나는 시점에 다음 SFX 시작 (겹치면 자동 push)
- 마커 JSON 로드: 반드시 `utils.load_marker()` 경유 — 두 포맷 자동 정규화
- 한글 파일명 글로브: macOS NFD 이슈로 `Path.glob("*한글*")` 작동 안 함 → `iterdir()` + `_nfc()` 사용
- 각 STEP 폴더에 `__init__.py` 필요
- 스텝간 데이터는 파일로 주고받음 (함수 반환값 사용 안 함)

---

## 마커 JSON 두 포맷 (자동 정규화)

`utils.load_marker(path)`가 두 포맷 모두 `{scenes: [{effects: [...], ...}]}` 표준형으로 변환.

**A) `05_브랜드_M3_M4마커.json`** (구버전, 래퍼 객체)
```json
{
  "brand": "...",
  "scenes": [
    {"effects": [{"sfx_id": "SFX_027", "trigger_sec": 0.0}], "script": "...", ...}
  ]
}
```

**B) `scenes.json`** (신버전, 배열 직접)
```json
[
  {"sfx": ["SFX_027", "bgm_start"], "script": "...", "start_sec": 0.0, ...}
]
```
- `sfx` 배열 중 `SFX_*` 시작 항목만 효과음으로 인식 (bgm_* 등은 무시)
- `trigger_sec`은 씬의 `start_sec` 값으로 자동 채움

---

## SFX 테마 자동 감지 + 매칭

**테마 감지** (`utils.detect_theme(folder)`)
프로젝트 폴더의 `*기획안*.md` 파일을 스캔. 우선순위:
1. **명시적 테마 라인**: `**테마**: 공포`, `**SFX 테마**: 네이티브` 등
2. **광고 유형 섹션**: 라인 + 다음 2줄에서 `공포`/`네이티브`/`정보성` 키워드
3. **전체 텍스트 최다 출현 키워드**

**SFX 폴더 구조**
```
input/sfx/
├── 공포/   01_xxx.mp3, 02_xxx.mp3, ...
├── 네이티브/
└── 정보성/
```

**파일 매칭** (`STEP3._list_theme_sfx()`)
- 정규식: `^\s*(\d+)[\s._]` — 숫자 prefix + 점/언더스코어/공백 구분자
- 매칭 가능: `1 .뾰로롱.mp3`, `11. 멜로디.mp3`, `01_공포_xxx.mp3`
- 숫자 prefix 없는 파일은 무시됨

**SFX 이벤트 → 파일 매핑**
- 마커의 모든 SFX 이벤트를 `trigger_sec` 시간순 정렬
- 1번째 이벤트 → 01_*, 2번째 → 02_*, ... 순서로 1:1 매핑
- 이벤트 > 파일: 초과분 무시
- 이벤트 < 파일: 남는 파일 미사용

**타임라인 배치**
- 모든 SFX는 A3 단일 트랙에 일렬 배치
- 시작 시점 = `max(trigger_sec, 이전 SFX 끝)`
- 이전 SFX와 겹치면 자동으로 뒤로 밀림 (겹침 방지)

---

## 폴더 / 파일명 규칙

```
인풋 폴더: YYYYMMDD_브랜드/                  (예: 20260427_자보티바_1)
인풋 마커: 05_브랜드_M3_M4마커.json           또는 scenes.json
인풋 TTS:  *tts*.mp3 / *tts*.wav            (패턴 매치, 명명 유연)

아웃 폴더: output/YYYYMMDD_브랜드/
아웃 파일: YYYYMMDD_브랜드_tts_cut.mp3 (또는 .wav)
          YYYYMMDD_브랜드_subtitle_chunks.json
          YYYYMMDD_브랜드_subtitle_ko.srt
          YYYYMMDD_브랜드_timeline.xml       (XMEML 포맷, .fcpxml 아님)
```

`done/`, `sfx/` 폴더는 자동 스킵.

---

## 실행 방법

```bash
# M4 폴더에서 실행 (개발 또는 볼륨 위치)
cd "/Volumes/01_마케팅사업부_직원/{NAS_USER}/3팀 영상 자동화/M4"

# 최초 1회 설치
pip install pydub openai-whisper
brew install ffmpeg

# 기본 실행 (감지된 1번 프로젝트 처리)
python3 m4_run.py

# 복수 프로젝트 중 특정 번호 실행
python3 m4_run.py --index 2
```

---

## 주의사항

- Whisper 첫 실행 시 모델 다운로드 발생 (small 기준 460MB), 멈춘 것처럼 보여도 정상
- Apple Silicon 맥은 `device="mps"` 설정 시 Whisper 속도 향상 (실패 시 cpu 자동 재시도)
- input/ 자동 스캔으로 날짜·브랜드 파악, config.json 수동 수정 불필요
- macOS Korean 파일명: NFD/NFC 차이로 glob 실패 가능 → `unicodedata.normalize("NFC", fname)` 필수
- Premiere 임포트: `.xml` 파일을 File → Import로 가져오기 (저장된 `.prproj` 열기 아님)
- 자막 스타일 확정값: fontname=Pretendard-Bold / fontstyle=Bold / fontsize=16(~55pt) / forecolor 배열(1.0×4) / origin=540 960
- TTS 파일이 없는 프로젝트는 감지 목록에서 제외됨 (마커만 있고 TTS 미확보 상태)
