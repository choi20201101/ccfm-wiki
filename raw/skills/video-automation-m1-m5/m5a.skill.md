---
name: m5a
description: |
  M5/input의 scenes.json + 이미지 파일을 읽어
  ref 크로스체크 → 씬별 폴더 생성 → run.py 실행 → 이미지 생성.
  프롬프트 생성 단계 없음. scenes.json의 prompt 필드를 그대로 사용.
  트리거: "/m5a 브랜드명", "m5a 시작", "이미지 생성해"
---

# M5a — 이미지 생성 스킬

## 설정

config.json(`C:/Users/{WINDOWS_USER}/.claude/skills/m5a/config.json`) Read로 경로 확인.

```
m5_input_dir     = //192.168.0.103/.../M5/input
m5_output_dir    = //192.168.0.103/.../M5/output
desktop_work_dir = C:/Users/{WINDOWS_USER}/Desktop/클로드/m5-work
flow_gen_dir     = C:/Users/{WINDOWS_USER}/Desktop/클로드/flow-gen-pkg
python           = {PYTHON_PATH}
```

---

## Step 1. 인풋 폴더 확인

```bash
ls "{m5_input_dir}/"
```

서브폴더 형식: `YYYYMMDD_브랜드명`.
1개면 자동 선택, 여러 개면 사용자 선택, 없으면 준비 요청.
선택 폴더명을 `M5_BRAND_NAME`으로 기억.

---

## Step 2. NAS → Desktop 복사

```bash
DESKTOP_BRAND_DIR="{desktop_work_dir}/{M5_BRAND_NAME}"
mkdir -p "{DESKTOP_BRAND_DIR}"
cp -r "{m5_input_dir}/{M5_BRAND_NAME}/." "{DESKTOP_BRAND_DIR}/"
ls "{DESKTOP_BRAND_DIR}/"
```

이후 모든 파일 탐색은 `DESKTOP_BRAND_DIR` 기준.

---

## Step 3. 파일 목록 확인 + 제품이미지 분류

```bash
ls "{DESKTOP_BRAND_DIR}/"
```

필수 파일:
- `scenes.json` ✓
- `제품이미지_{브랜드명}.*` 1개 이상 ✓

선택 파일:
- `컨셉이미지.*` (있을 경우)
- `모델이미지.*` (있을 경우)

제품이미지 전체 목록 확인 후, **각 파일을 Read 툴로 직접 시각 확인**:

```
제품이미지_{브랜드명}.jpg     → 제품_1
제품이미지_{브랜드명}_2.jpg   → 제품_2 (있을 경우)
제품이미지_{브랜드명}_3.jpg   → 제품_3 (있을 경우)
```

각 제품이미지를 보고 아래 기준으로 분류 후 기억:

| 분류 | 설명 |
|------|------|
| `외관컷` | 포장·용기·병·스틱팩·박스 등 제품 외형 |
| `제형컷` | 음료·액상·분말·알약·원료 등 내용물/섭취 형태 |

> 이미지가 1개뿐이면 분류 생략 (항상 제품_1 사용).

---

## Step 4. BASE_REF 결정

컨셉이미지가 있으면 Read 툴로 직접 확인.

| 조건 | IMAGE_TYPE | 인물 ref 파일 |
|------|-----------|-------------|
| 컨셉이미지 없음 | `"모델"` | 모델이미지.* |
| 컨셉이미지 비실사 (캐릭터·CGI·일러스트) | `"컨셉"` | 컨셉이미지.* |
| 컨셉이미지 실사 + 얼굴 잘 보임 | `"모델"` | 컨셉이미지.* (모델이미지 대신 사용) |
| 컨셉이미지 실사 + 얼굴 없거나 흐림 | `"모델"` | 모델이미지.* |

> `"컨셉_실사"` 타입 없음. 실사 컨셉이미지는 무조건 `"모델"` 타입으로 처리.
> 차이는 ref 파일 소스만 다름 (컨셉이미지 vs 모델이미지).

IMAGE_TYPE = "모델" 인데 인물 ref 파일이 없으면 중단:
```
인물 ref 파일이 없습니다. M3를 다시 실행해주세요.
```

BASE_REF_FILE = 위 표에서 결정된 인물 ref 파일 경로. 이후 모든 단계에서 고정.

---

## Step 5. scenes.json 읽기 + ref 크로스체크

`scenes.json` Read 툴로 읽기.

각 씬의 `refs` 배열 + `prompt` 텍스트를 함께 보고 실제 파일 매핑 결정.

### ref 파일 매핑 규칙

| refs 값 | 사용 파일 | 저장명 |
|--------|--------|-------|
| `"concept"` | BASE_REF_FILE | ref1.jpg |
| `"model"` | BASE_REF_FILE | ref1.jpg |
| `"product"` | 제품이미지 선택 (아래 규칙) | ref1.jpg 또는 ref2.jpg |
| model/concept + product | BASE_REF_FILE → ref1, 제품이미지 → ref2 | ref1.jpg + ref2.jpg |
| `[]` | 없음 | — |

### 제품이미지 여러 개일 때 선택 규칙

Step 3에서 분류한 이미지 타입을 기반으로 결정.

**핵심 원칙: 존재하는 제품이미지는 모두 ref로 사용**
- `외관컷`만 있으면 → 외관컷 1개 사용 (slot 1)
- `제형컷`만 있으면 → 제형컷 1개 사용 (slot 1)
- `외관컷` + `제형컷` **둘 다 있으면 → 반드시 둘 다 사용** (slot 1 + slot 2)
  - 박스 + 포, 용기 + 제형액, 알약병 + 알약 등 모든 경우 동일하게 적용
  - 어떤 씬이든 제품 ref가 있으면 존재하는 제품이미지 전부 포함

**결정된 slot_indices를 scenes.json에 기록** (run.py 실행 전):

각 씬의 결정 결과를 scenes.json `slot_indices` 필드에 씀:
```python
# slot 0 = 인물(concept/model), slot 1 = 제품_1(외관), slot 2 = 제품_2(제형)
# 예: refs=["concept","product"], 외관컷+제형컷 둘 다 있음 → slot_indices=[0, 1, 2]
# 예: refs=["concept","product"], 외관컷만 있음 → slot_indices=[0, 1]
# 예: refs=["product"], 외관컷+제형컷 둘 다 있음 → slot_indices=[1, 2]
# 예: refs=["product"], 외관컷만 있음 → slot_indices=[1]
```

```bash
# Python으로 scenes.json 업데이트 (Write 툴 대신 python 사용)
python -c "
import json; path='{DESKTOP_BRAND_DIR}/scenes.json'
scenes=json.load(open(path,encoding='utf-8'))
# 아래 updates 딕셔너리는 Claude가 위 분석 결과로 채움
updates = {
  's01': [0],
  's02': [0],
  ...
}
for s in scenes:
    if s['scene_id'] in updates:
        s['slot_indices'] = updates[s['scene_id']]
json.dump(scenes, open(path,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
"
```

또는 Write 툴로 scenes.json 전체 재작성.

### 크로스체크 완료 보고 (진행 전 반드시 출력)

```
=== ref 크로스체크 결과 ===
IMAGE_TYPE: 모델
BASE_REF: 컨셉이미지.jpg

s01 → ref1: 컨셉이미지.jpg
s02 → ref1: 컨셉이미지.jpg
s03 → ref1: 컨셉이미지.jpg / ref2: 제품이미지_자보티바_2.jpg (알약컷)
s04 → ref1: 제품이미지_자보티바.jpg (메인)
s05 → ref1: 컨셉이미지.jpg
s06 → ref1: 제품이미지_자보티바.jpg (메인)
s07 → ref1: 컨셉이미지.jpg / ref2: 제품이미지_자보티바.jpg
s08 → ref1: 컨셉이미지.jpg / ref2: 제품이미지_자보티바_2.jpg (알약컷)
========================
이대로 진행할까요?
```

사용자 확인 후 진행. 수정 요청 있으면 해당 씬만 변경 후 재출력.

---

## ⚠️ 필수 강제 지침 — 생성 중 코드 수정 절대 금지

**run.py가 백그라운드로 실행 중인 동안:**
- `run.py` / `flow-gen-pkg/` 내 모든 소스 파일 수정 **절대 금지**
- 문제 발생 시 → 임시 스크립트(`C:/Users/{WINDOWS_USER}/Desktop/클로드/temp_fix.py` 등)를 별도 생성하여 처리
- 코드 수정이 필요하면 **먼저 Python 프로세스를 Stop-Process로 중지 후** 수정

**위반 금지 — 실행 중 소스 수정은 예기치 않은 동작·오류를 유발한다.**

---

## Step 6. run.py 실행

```powershell
try { Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/version" -UseBasicParsing -TimeoutSec 3 | Out-Null; Write-Output "연결 성공" } catch { Write-Output "연결 실패" }
```

Chrome CDP 연결 확인. 실패 시 **직접 실행**:

```powershell
cd "C:/Users/{WINDOWS_USER}/Desktop/클로드/flow-gen-pkg/src"
& "{PYTHON_PATH}" -u browser.py
```

`browser.py`는 `User Data M5A`를 재사용하므로 m5c Chrome(포트 9223)에 영향 없음. 절대 다른 방식으로 Chrome을 열지 말 것.

```bash
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export FLOW_M5_CAMPAIGN="{M5_BRAND_NAME}"
export FLOW_M5_OUTPUT_DIR="{DESKTOP_BRAND_DIR}/images"
export FLOW_M5_REF_DIR="{DESKTOP_BRAND_DIR}"
export FLOW_M5_IMAGE_TYPE="{IMAGE_TYPE}"
export FLOW_M5_WORK_DIR="{DESKTOP_BRAND_DIR}"
mkdir -p "{DESKTOP_BRAND_DIR}/images"
cd "{flow_gen_dir}" && "{python}" -u run.py
```

IMAGE_TYPE 값:
- 인물 ref가 모델이미지 → `"모델"`
- 인물 ref가 컨셉이미지 → `"컨셉"`

아웃풋 파일명: `s01_1.jpg` `s01_2.jpg` `s02_1.jpg` ...
총 아웃풋: 씬 수 × 2장

---

## Step 7. NAS 업로드 + 완료 보고

```bash
mkdir -p "{m5_output_dir}/{M5_BRAND_NAME}/images"
cp -r "{DESKTOP_BRAND_DIR}/images/." "{m5_output_dir}/{M5_BRAND_NAME}/images/"
```

완료 보고:
```
[M5a 완료] {M5_BRAND_NAME}
IMAGE_TYPE: [컨셉 / 모델]
BASE_REF: [파일명]
총 씬: N개
이미지: N×2 = N장
로컬: {DESKTOP_BRAND_DIR}/images/
NAS: {m5_output_dir}/{M5_BRAND_NAME}/images/

다음: /m5c {브랜드명}
```
