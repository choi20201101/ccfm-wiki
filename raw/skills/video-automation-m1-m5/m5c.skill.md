---
name: m5c
description: |
  M5a가 생성한 씬별 이미지(씬당 2장)를 받아 Flow 영상 생성 실행.
  이미지 1장당 영상 2개 생성 → 씬당 영상 4개 아웃풋.
  트리거: "/m5c 브랜드명", "m5c 시작", "영상 생성해"
---

# M5c — 영상 생성 스킬

## 설정

config.json(`C:/Users/{WINDOWS_USER}/.claude/skills/m5c/skill/config.json`) Read로 경로 확인.

```
m5_output_dir    = //192.168.0.103/.../M5/output
desktop_work_dir = C:/Users/{WINDOWS_USER}/Desktop/클로드/m5-work
flow_video_dir   = C:/Users/{WINDOWS_USER}/Desktop/클로드/flow-video
python           = {PYTHON_PATH}
```

---

## Step 1. 인풋 확인

### 1-1. 브랜드 폴더 확인

```bash
ls "{desktop_work_dir}/"
```

서브폴더 형식: `YYYYMMDD_브랜드명`.
1개면 자동 선택, 여러 개면 사용자 선택.
선택 폴더명을 `M5_BRAND_NAME`으로 기억.

`DESKTOP_BRAND_DIR = {desktop_work_dir}/{M5_BRAND_NAME}`

### 1-2. 인풋 파일 확인

```bash
ls "{DESKTOP_BRAND_DIR}/images/"
ls "{DESKTOP_BRAND_DIR}/scenes.json"
```

- 이미지 파일명 형식: `s01_1.jpg` `s01_2.jpg` ... (영문+숫자, 한글 금지)
- 이미지 없으면 중단 후 "M5a를 먼저 실행하세요" 안내
- scenes.json 없으면 중단 후 "scenes.json이 없습니다" 안내
- 씬 수, 총 이미지 수 확인 후 보고

### 1-2b. NAS images 동기화 확인 (m5a Step 7 누락 방지)

```bash
ls "{m5_output_dir}/{M5_BRAND_NAME}/images/" 2>/dev/null || echo "NAS images 없음"
```

NAS에 images/ 없거나 파일 수가 로컬보다 적으면 → **자동으로 복사 후 진행** (사용자 확인 불필요):

```bash
mkdir -p "{m5_output_dir}/{M5_BRAND_NAME}/images"
cp -r "{DESKTOP_BRAND_DIR}/images/." "{m5_output_dir}/{M5_BRAND_NAME}/images/"
```

NAS images 파일 수 = 로컬 images 파일 수이면 → 스킵, 그대로 진행.

### 1-3. flow-video 스크립트 존재 확인

```bash
ls "{flow_video_dir}/run.py"
```

없으면 중단.

---

## Step 1.5. 영상 프롬프트 분석 + video_scenes.json 생성

1. `DESKTOP_BRAND_DIR/scenes.json` + `DESKTOP_BRAND_DIR/images/` 읽기
2. 씬별 레퍼런스 이미지 확인:
   - `refs: ["model"]` 또는 `refs: ["concept"]` 또는 `refs: ["model", "product"]` → 해당 씬 이미지 사용
   - `refs: ["product"]` → `제품이미지_{브랜드명}.jpg` 사용
   - `refs: []` → 씬 이미지 그대로 사용
3. 영상 프롬프트 생성 시:
   1. 각 이미지 파일을 Read 툴로 직접 열어서 확인
   2. 이미지에 실제로 보이는 장면 기준으로 작성 — 10~15자 이내, 핵심만
   3. scenes.json 프롬프트는 참고만 — 이미지 내용 우선
   4. 인물 있으면:
      - 실물 인물(실사) → 동작/표정 위주 (예: "제품을 카메라에 내미는 여성")
      - 캐릭터·CGI·애니·컨셉이미지 → 동작/표정 위주 (예: "제품을 들고 엄지척하는 캐릭터")
      - **"말없이" 절대 금지** — Flow 생성 실패 원인
   5. 제품만 있으면 → 제품 배치 위주 (예: "대리석 위 유리병과 열매 클로즈업")
   6. "장면", "모션", "차림", "~하는 장면" 등 불필요한 단어 제거
4. `DESKTOP_BRAND_DIR/video_scenes.json` 저장 후 바로 다음 Step 진행 (확인 불필요)

---

## Step 2. Chrome CDP 연결 확인

```powershell
try { Invoke-WebRequest -Uri "http://127.0.0.1:9223/json/version" -UseBasicParsing -TimeoutSec 3 | Out-Null; Write-Output "연결 성공" } catch { Write-Output "연결 실패" }
```

- **연결 성공** → 그대로 다음 Step 진행. Chrome 절대 건드리지 않음.
- **연결 실패** → 아래 명령 실행 후 결과 기다림 (반드시 완료될 때까지 대기):

```powershell
& "{PYTHON_PATH}" "C:/Users/{WINDOWS_USER}/Desktop/클로드/flow-video/start_chrome.py"
```

실행 후 `Chrome 준비됨` 메시지 확인. 그 다음 CDP 재확인:

```powershell
try { Invoke-WebRequest -Uri "http://127.0.0.1:9223/json/version" -UseBasicParsing -TimeoutSec 3 | Out-Null; Write-Output "연결 성공" } catch { Write-Output "연결 실패" }
```

- **재확인 성공** → 다음 Step 진행
- **재확인 실패** → 즉시 사용자에게 보고하고 중단. Chrome 직접 조작 / Playwright 직접 런치 / 코드 수정 절대 금지.

**핵심 원칙 (반드시 준수):**
- Chrome은 한 번 열면 브랜드가 바뀌어도 절대 닫지 않음
- run.py가 매번 새 Flow 프로젝트를 만드므로 Chrome 재시작 불필요
- Chrome을 직접 kill/종료하는 PowerShell 명령 절대 실행 금지
- Playwright `chromium.launch()` 직접 호출 절대 금지 — 반드시 `connect_over_cdp` 방식만 사용
- 로그인 풀렸을 때: Chrome 열린 상태에서 본인 Google 계정으로 직접 로그인

---

## Step 3. 영상 생성 실행

환경변수 설정 후 run.py 직접 실행 (PowerShell):

```powershell
$env:PYTHONUTF8 = "1"
$env:FLOW_M5C_WORK_DIR = "{DESKTOP_BRAND_DIR}"
cd "{flow_video_dir}"
& "{python}" -u run.py 2>&1 | Tee-Object -FilePath "{DESKTOP_BRAND_DIR}\run.log"
```

> 로그 파일 경로: `{DESKTOP_BRAND_DIR}\run.log`

**새 플로우 (v7):**

| Phase | 내용 |
|-------|------|
| Phase 1 | 전체 씬 이미지 일괄 업로드 (시작 시 1회) — 피커 이미지 업로드 버튼 사용 |
| Phase 2 | 피커 파일명 목록 스크롤 검증 → 누락분만 모든 미디어에서 재업로드 |
| Phase 3 | 씬별 순서대로: 시작프레임 선택(피커) → 프롬프트 → 생성 대기 → 업스케일 → 다운로드 → 파일 검증 |

**아웃풋 파일명:**
```
s01_1_a.mp4   s01_1_b.mp4
s01_2_a.mp4   s01_2_b.mp4
s02_1_a.mp4   ...
```

**실행 중 상시 모니터링 (3가지 반드시 병행):**

### ① 로그 실시간 감시
```powershell
Get-Content "{DESKTOP_BRAND_DIR}\run.log" -Tail 20
```
씬 완료(`[완료] sXX_X`) 또는 타임아웃 시마다 확인.

### ② 브라우저 상태 직접 체크 (파일 저장 없음)
로그에 `신규실패 > 0` 또는 이상 징후 시:
```powershell
& "{PYTHON_PATH}" "C:/Users/{WINDOWS_USER}/Desktop/클로드/flow-video/monitor_once.py"
```
출력 예시:
```
생성중   : 아니오
영상 수  : 3
실패 카드: 1개  ⚠️  개입 필요!
```

### ③ 실패 감지 시 개입 방법
- 생성 중(생성중: 예)이면 → 계속 대기
- 생성 완료 + 실패 카드 있으면 → **같은 프로젝트에서** 재시도:
  - 시작프레임 슬롯에 레퍼런스 다시 선택 → 프롬프트 다시 입력 → 생성
  - 새로고침/새 프로젝트 절대 금지
  - 성공 영상 있으면 그것만 다운로드 후 다음 씬 진행

### ④ 아웃풋 폴더 저장 확인
씬 완료 시마다:
```bash
ls "{DESKTOP_BRAND_DIR}/videos/"
```
파일 누락 또는 0바이트 있으면 해당 씬만 재실행.

---

## Step 4. NAS 업로드 + 완료 보고

완료 확인 후:
```powershell
New-Item -ItemType Directory -Force -Path "{m5_output_dir}/{M5_BRAND_NAME}/videos" | Out-Null
Copy-Item -Recurse -Force "{DESKTOP_BRAND_DIR}\videos\*" "{m5_output_dir}/{M5_BRAND_NAME}/videos/"
```

완료 보고:
```
[M5c 완료] {M5_BRAND_NAME}
씬 수: N개 | 영상: N×4 = N개
로컬: {DESKTOP_BRAND_DIR}/videos/
NAS: {m5_output_dir}/{M5_BRAND_NAME}/videos/
```

---

## 종료

```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
```

Chrome은 절대 닫지 않음 — 다음 브랜드 작업에서 그대로 재사용.

---

## ⚠️ 필수 강제 지침 — 생성 중 코드 수정 절대 금지

**run.py가 백그라운드로 실행 중인 동안:**
- `run.py` / `flow_video/` 내 모든 소스 파일 수정 **절대 금지**
- 문제 발생 시 → 임시 스크립트(`C:/Users/{WINDOWS_USER}/Desktop/클로드/temp_fix.py` 등)를 별도 생성하여 처리
- 코드 수정이 필요하면 **먼저 Python 프로세스를 Stop-Process로 중지 후** 수정

**위반 금지 — 실행 중 소스 수정은 예기치 않은 동작·오류를 유발한다.**

---

## 주의사항

- M5a 완료 전 실행 금지 (images/ + scenes.json 필요)
- Chrome port 9223에서 Flow 워크스페이스 열려있는지 확인 후 실행
- 파일명 한글 사용 금지 — Windows 경로 인코딩 오류 발생
- 종료 시 Python만 닫기 — Chrome은 계속 유지

---

## Harness 규칙 (`harness.py`)

| # | 규칙 |
|---|------|
| 1 | 새 프로젝트 뜰 때까지 대기 + 2초 추가 |
| 2 | 모든 액션 후 스크린샷 확인 |
| 3 | 씬 1개 완전 완료 후 다음 씬 진행 |
| 4 | 실패 시 스크린샷 먼저, 판단은 그 다음 |
| 5 | 모든 액션 사이 3초 텀 |
| 6 | 저장 실패 시 갤러리 복귀 후 재저장 |
| 7 | Phase 1에서 전체 이미지 일괄 업로드. Phase 2에서 피커 파일명 검증 → 누락분만 재업로드 |
| 8 | 씬 완료 후 다음 씬 전 반드시 `모든 미디어` 버튼 클릭 — 동영상 탭에 갇히면 다음 씬 오류 |
| 9 | 새 프로젝트 진입 실패 시 "새 프로젝트" 버튼 최대 3회 재시도 — 클릭 후 반드시 `/project/` URL 대기 |
| 10 | 에러 복구: 실패 시 `go_to_main_tab()` → 한 단계 뒤로 → 재실행 (최대 2회). 코드 재작성 없음. 불량 파일(0바이트 등) → 삭제 → 모든 미디어 → 재다운로드 |

스크린샷 저장 위치: `/tmp/m5c_*.png`

---

## 알려진 이슈 및 해결 (_wait_generation)

| 이슈 | 원인 | 해결 (run.py) |
|------|------|------|
| 스크롤 아래 → 맨 위 카드 언마운트 | `_wait_generation` 루프가 매번 `scrollTop+1`로 아래 이동 → 새 카드(맨 위)가 가상 스크롤 밖으로 빠져 video src / 실패 텍스트 미감지 | 루프마다 `scrollTo(0,0)` 맨 위 복귀로 변경 |
| 오디오 실패 무한대기 (600s) | 오디오 실패 카드가 가상 스크롤 밖 → `text=실패` count 미달 → 600s 대기 | `no_fail_chg_for` 추가 — 실패≥1 + 60s 변화없으면 즉시 조기탈출 |
| 무감지 무한대기 (600s) | 생성 시작 후 pct 사라지고 카드도 0 — 영상/실패/로딩 모두 0인데 600s 대기 | elapsed≥120 + 모두 0이면 즉시 조기탈출(무감지) |
| `pre_fails` 스크롤 밖 누락 | `filter(visible=True)`가 뷰포트 밖 실패 카드 제외 → pre_fails 과소 계산 | 스냅샷에서 `filter(visible=True)` 제거 |
| 성공 1개 후 나머지 실패 미감지 | 실패 카드 스크롤 밖 → count 미달 → 600s 대기 | `no_change_for>=60` 조기탈출 — 성공≥1 + 60s 변화없으면 탈출 |

**실행 시 환경변수 방식 필수 (Windows PowerShell):**
```powershell
$env:PYTHONUTF8 = "1"
$env:FLOW_M5C_WORK_DIR = "C:\Users\{WINDOWS_USER}\Desktop\클로드\m5-work\20260506_브랜드명"
cd "C:\Users\{WINDOWS_USER}\Desktop\클로드\flow-video"
& "{PYTHON_PATH}" -u run.py 2>&1 | Tee-Object -FilePath "C:\Users\{WINDOWS_USER}\Desktop\클로드\m5-work\20260506_브랜드명\run.log"
```
(`python run.py "경로"` 인자 방식 사용 금지 — `scenes.json` 폴백 경로 오류 발생)
