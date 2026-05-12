---
type: source
domain: content-ai-automation
confidence: high
created: 2026-05-12
updated: 2026-05-12
sources:
  - raw/skills/video-automation-m1-m5/
---

# 🏆 3팀 영상 자동화 M1~M5 — 5단 NAS 파이프라인 성공 사례 (2026-05-12)

> **무엇**: 영상 직원이 운영중인 5단계 영상 광고 자동화 파이프라인.
> 웹 입력 1번 → NAS 5단 → Premiere XMEML + Flow MP4 까지 자동.
> **재현 가치**: 어떤 PC/Mac에서도 NAS 마운트 + 스킬 4개 설치로 즉시 가동.

원본 스냅샷: [[raw/skills/video-automation-m1-m5/]]

---

## 0. 한 줄 요약

| 모듈 | 입력 | 출력 | 핵심 도구 |
|---|---|---|---|
| **M1** 입력 패키지 | 웹폼(브랜드명/Q1/Q2/이미지) | 브랜드자산.md + 영상분석.md + user_input.md | Bash + WebSearch fallback |
| **M2** 기획안 생성 | M1 3종 | 04_기획안.md + scenes.json | LLM (plan_rules + prompt_rules) |
| **M3** 패키징 | M2 산출물 + 제품이미지 | M3/M4/M5 input 동시 분배 | 한글↔영문 매핑 + 파일명 표준화 |
| **M4** 자동 편집 | scenes.json + TTS | XMEML 타임라인 + SRT 자막 + 컷 mp3 | pydub + Whisper + XMEML |
| **M5a/c** 이미지/영상 | scenes.json + ref | 씬×2 이미지 / 씬×4 mp4 | Flow CDP 9222/9223 |

전체 길이: 입력 5분 → 출력 ~30분~수시간 (Whisper/Flow 단계가 병목).

---

## 1. 핵심 아키텍처 패턴

### 1-1. NAS는 큐, Desktop은 작업대 (Down → Local → Up + done 이동)
- 모든 단계가 동일한 4-stroke: **NAS 입력 → Desktop 복사 → 작업 → NAS 출력 + done 이동**
- 중간 작업 전부 로컬에서, NAS 접근은 다운(Step 3)+업(Step 7~9) 두 번뿐
- 동일 폴더 재처리 방지: done/ 폴더로 이동 (M1, M2, M3, M4 전부 같은 패턴)
- 새 파일은 cp+rm (SMB mv 오류 회피 — 모든 스킬에 명시)

### 1-2. 폴더명 = 프로젝트 ID
- 표준: `YYYYMMDD_브랜드[_제품][_N]` (예: `20260427_자보티바_1`)
- 8자리 날짜로 파싱 → 나머지가 브랜드/제품
- 동일 브랜드 다중 매칭은 `_1`, `_2` suffix로 구분
- M2~M5 모든 단계가 이 ID로 폴더를 찾음 → 단계 간 결합도 0

### 1-3. scenes.json이 단일 진실 (Single Source of Truth)
- M2가 만들고 M3/M4/M5 모두 같은 파일 사용
- 필드 스키마 고정: `id / scene_id(s01) / role / start_sec / end_sec / script / prompt / refs / sfx / slot_indices`
- 한글 scene_id 금지 (Windows 인코딩 안전성)

### 1-4. ref 크로스체크 + slot_indices = 명시적 LLM 결정
- M5a가 인물/제품 이미지를 Read 툴로 직접 본 뒤 씬별 slot 배정
- 결정 결과를 scenes.json에 `slot_indices` 필드로 기록 → run.py가 그대로 실행
- "어떻게 매핑할지"는 LLM, "어떻게 생성할지"는 코드 — **판단/실행 분리**

### 1-5. Chrome CDP 9222/9223 영구 세션
- M5a는 9222, M5c는 9223 → 같은 PC에서 충돌 없이 병행
- Chrome 한 번 열면 브랜드 바뀌어도 절대 종료 안 함
- `chromium.launch()` 절대 금지, `connect_over_cdp`만 사용
- 로그인 풀리면 사람이 직접 재로그인 (자동화 금지)

---

## 2. 단계별 입출력 계약

### M1 (입력 패키지)
- **트리거**: 웹폼 제출 → `/m1v2` 실행
- **입력**: `Desktop/클로드/m1-inputs/{브랜드_날짜}/m1_text_*.txt` + `m1_img_*`
- **처리**:
  1. NAS `브랜드 분석 MD/`에서 브랜드 에셋 검색
  2. 없으면 WebSearch로 자동 생성 + NAS에도 저장 (다음에 재사용)
  3. NAS `영상 분석 MD/`에서 동일 브랜드 제외하고 랜덤 1개 픽
- **출력**: `M1/output/{YYYYMMDD_브랜드_N}/01_~~_brand_asset.md` + `02_~~_영상분석.md` + `03_~~_user_input.md` + 컨셉이미지

### M2 (기획안 생성)
- **입력**: M1 3종 파일
- **규칙 외부화**: `references/plan_rules.md`, `references/prompt_rules.md` 먼저 Read
- **CONCEPT_TYPE 판별**: 컨셉이미지 있음+비실사 → "컨셉" / 그 외 → "실사"
- **3순회 품질체크**: 1순회 Fail 목록화 → 2순회 재작성 → 3순회 흐름+CTA
- **출력**: `04_기획안.md` + `scenes.json`. **02번(영상분석)은 M3로 넘기지 않음** — 아이디어 추출용으로만.

### M3 (패키징 + 분배)
- **한글↔영문 매핑 테이블** (제품이미지 폴더 검색용):
  | 한글 | 영문 |
  |---|---|
  | 모미차 | momicha |
  | 나잇사렌 | nightsaren |
  | 로쌩 | lossang |
  | 메디티엔 | meditn |
  | 레피넬 | refinelle |
  | 엔케이365 | NK365 |
  | 프리우먼 | freewoman |
- 1차 한글 검색 → 결과 없으면 영문 패턴으로 재검색 (fallback)
- 파일명 표준화: `컨셉이미지.ext`, `제품이미지_{브랜드}_{제품}_N.ext`
- **3곳 동시 분배**: M3/output(전체 보관) + M4/input(TTS용) + M5/input(이미지생성용)

### M4 (자동 편집, **유일하게 Python 모듈 실제 코드**)
- 운영 위치: NAS 직접 실행 (`BASE_DIR = Path(__file__).parent`로 Mac/Win 양쪽 동일)
- STEP1: pydub 무음 컷편집 (min_silence_len=150ms, thresh=-35dB, keep=50ms)
- STEP2: Whisper small (Mac mps / Win cpu 자동 fallback) → SRT + chunks.json
- STEP3: **XMEML** 생성 (`.fcpxml` 아님 — Premiere가 fcpxml 임포트 불가). 자막 forecolor, 정수 프레임(FPS=30), SFX A3 단일트랙 일렬배치
- **마커 JSON 두 포맷 자동 정규화**: 구버전(래퍼) vs scenes.json(배열) — `utils.load_marker()`가 통일
- **SFX 테마 자동 감지**: 기획안.md → 명시 테마 라인 → 광고 유형 섹션 → 최다 키워드
- **한글 경로**: macOS NFD, Windows NFC → `unicodedata.normalize("NFC", ...)`로 통일

### M5a (이미지 생성)
- Flow CDP 9222, `User Data M5A` 프로필
- IMAGE_TYPE: `"컨셉"` (비실사) / `"모델"` (실사 또는 모델이미지)
- 제품이미지 분류: `외관컷` + `제형컷` 둘 다 있으면 **반드시 둘 다 ref 사용**
- 씬당 2장 출력 (`s01_1.jpg`, `s01_2.jpg`)
- **사용자 확인 게이트**: ref 크로스체크 결과 출력 후 "이대로 진행할까요?" 대기

### M5c (영상 생성)
- Flow CDP 9223
- **Phase 1/2/3 패턴**: 전체 이미지 일괄 업로드(1회) → 피커 파일명 검증 + 누락분만 재업로드 → 씬별 시작프레임+프롬프트+업스케일+다운로드
- 영상 프롬프트 10~15자, **"말없이" 금지** (Flow 생성 실패 키워드)
- 씬당 4 mp4 (`s01_1_a.mp4 / s01_1_b.mp4 / s01_2_a.mp4 / s01_2_b.mp4`)
- 모니터링 3종 병행: 로그 tail + monitor_once.py + 아웃풋 폴더 ls

---

## 3. 다른 곳에서 재현하는 법

### 3-1. 사전 준비 (PC당 1회)
```
1. NAS 마운트: \\192.168.0.103\01_마케팅사업부_직원\{NAS_USER}\3팀 영상 자동화
2. Python 3.10+ (python.org 공식 설치본 — Store stub 회피)
3. ffmpeg (winget install Gyan.FFmpeg 또는 brew install ffmpeg)
4. pip install pydub openai-whisper
5. Flow용 Chrome: User Data M5A (9222) + User Data M5C (9223) 두 프로필 분리 생성
6. 스킬 4종 ~/.claude/skills/user/ 에 설치 (m1v2 / m2 / m3 / m4 / m5a / m5c)
7. 스킬 내 {WINDOWS_USER}, {NAS_USER}, {PYTHON_PATH} 치환
```

### 3-2. 운영 흐름 (브랜드 1개당)
```
웹폼 제출
  → /m1v2            (1분)
  → /m2 브랜드명     (3-5분, LLM)
  → /m3 브랜드명     (1분)
  → /m4 브랜드명     (5-15분, Whisper 모델 다운로드 첫 1회 460MB)
  → /m5a 브랜드명    (씬 수 × 약 2분)
  → /m5c 브랜드명    (씬 수 × 약 5-10분)
  → Premiere에서 timeline.xml import
```

### 3-3. 새 브랜드 추가 시
- `M3` 스킬의 한글↔영문 매핑 테이블에 추가
- NAS `M3/제품이미지/` 폴더에 `{브랜드}_{제품}_N.jpg` 형식으로 업로드
- 브랜드 자산 MD는 자동 생성 또는 수동 추가 (`M1/input/브랜드 분석 MD/`)

---

## 4. 왜 잘 됐나 (재현 가능한 설계 원칙)

1. **5개 단계로 쪼개서 각 단계 실패해도 그 자리에서 재실행 가능** — 파일이 단계 간 인터페이스
2. **NAS 큐 패턴** — 단계 간 의존성을 폴더 존재 여부로 표현 (코드 호출 없음)
3. **scenes.json 단일 스키마** — 4개 모듈이 같은 파일 보고 합의된 동작
4. **한글 경로 / SMB / NFC-NFD를 정면 처리** — 회피 아닌 정규화로 통일
5. **LLM 판단을 명시 필드로 고정 (slot_indices)** — 비결정성을 데이터로 박제
6. **Chrome 세션 영속화** — 로그인 비용을 0으로 분할 상각
7. **사용자 확인 게이트** — 시간 비싼 작업(M5a/c) 전에 ref 크로스체크 + 사용자 OK 필수
8. **fallback 체인** — 브랜드 에셋 없음 → WebSearch / 한글 매칭 없음 → 영문 / mps 실패 → cpu

---

## 5. 함정 (이미 해결됨, 다른 PC에서도 같은 함정 만남)

| 함정 | 해결 |
|---|---|
| SMB에서 `mv` 실패 | 항상 `cp -r` + `rm -rf` |
| 한글 파일 `glob` 실패 (macOS NFD) | `iterdir()` + `unicodedata.normalize("NFC", ...)` |
| Premiere가 `.fcpxml` 임포트 불가 | XMEML(`.xml`)로 출력 |
| 자막 색상 무시 | `forecolor` 사용 (`fontcolor` 아님) |
| Whisper mps Windows 불가 | `step2_whisper_sub.py`에서 cpu 자동 fallback |
| Flow `chromium.launch()`로 띄우면 세션 분리 | `connect_over_cdp` 강제 |
| Flow "말없이" 프롬프트 → 생성 실패 | 동작/표정 키워드만, 10-15자 |
| `run.py` 실행 중 코드 수정 → 예측 불가 오류 | Stop-Process 후에만 수정. 급하면 `temp_fix.py` 별도 파일 |
| Whisper `_wait_generation` 무한대기 5종 | 가상스크롤 맨위 복귀 + 60s 변화없으면 조기탈출 + 120s 무감지 탈출 |

---

## 6. 한계 + 개선 후보

- M2 LLM 호출이 사람의 LLM 세션을 직접 점유 (API 자동화 X) — 야간 배치 불가
- M5a/c Flow가 비공식 → Google 측 UI 변경 시 셀렉터 갱신 필요
- 단계 간 큐를 NAS 폴더로 관리 → 동시성/멱등성 보증은 사람 책임
- 개선 후보: scenes.json 스키마 버전 필드 추가, M2~M5에 `--dry-run`, M3 한글↔영문 매핑을 외부 JSON으로 분리

---

## 7. 관련 위키

- 도메인: [[domains/content-ai-automation]] §컷편집/STT/자막
- 영상생성 함정 모음: [[tacit/video-gen-lessons]]
- ChatGPT 웹 자동화 (M5c 패턴 참고): [[tacit/chatgpt-web-automation]]
- 코딩 교훈 §M1~M5: [[tacit/coding-lessons]]
- 운영 휴리스틱: [[tacit/operational-heuristics]] §NAS 큐 패턴
