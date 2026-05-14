---
aliases: ["GFA-Setting", "GFA 광고 세팅 자동화", "네이버 GFA 자동화"]
type: domain
domain: marketing-automation
confidence: medium
created: 2026-04-30
updated: 2026-05-14
sources: [src-gfa-setting-skill-2026-04-30]
---

# GFA-Setting — 네이버 GFA 광고 세팅 자동화 스킬

> 네이버 성과형 디스플레이(GFA) 광고 그룹+소재 atomic 자동 등록 Claude 스킬.
> v0.1.0 (2026-04-30) — N=3 dry-run 성공.
> v0.1.x (2026-05-13~14) — 새 UI(rwc 캘린더) 대응 + 디버그 pause 모드 + 멀티 잡 큐.
> 트리거: `GFA-Setting`, `GFA 세팅`, `GFA 광고 세팅`, `NAS 소재 GFA 업로드`, `네이버 광고 자동 세팅`, `GFA 그룹 생성`, `광고 소재 자동 등록`.

## 1줄 요약 (꺼내쓰기용)

```
gfa-setting <광고계정ID>
```
→ 계정 1회 검증 → **여러 잡(콘텐츠/캠페인/참조/소재) 일괄 입력** → 최종 confirm → 잡 #1 commit → 30초 cooldown → 잡 #2 commit → … → 종료 요약.
한 잡 = 7개 입력값(콘텐츠 경로/캠페인 ID/참조 그룹/베이스 이름/참조 소재/per_ad/랜딩 URL) → N개 광고 그룹+소재.

## v0.1.x 업데이트 (2026-05-13 ~ 2026-05-14)

> 두 개의 후속 패치. v0.1.0 → master HEAD 사이의 운영상 큰 변화 두 가지.

### A. 새 UI(rwc 캘린더) 대응 + 디버그 pause 모드 — 2026-05-13 (commit `75472ff`)

GFA 콘솔의 광고 그룹 시작일시 입력 UI 가 antd DatePicker(readonly input + 클릭 → 캘린더 팝업) **→ rwc(react-window-calendar 류) 가상 스크롤 캘린더 + 별도 form 시간 input 분리 마크업**으로 교체됨. 기존 셀렉터 전부 깨짐.

**변경**:
- `operations/ad_sets.py:set_start_datetime` 전면 재작성 — picker trigger 가 input 이 아니라 **button**으로 바뀐 마크업 대응.
- 신규 헬퍼: `_find_start_datetime_trigger`, `_find_form_time_input`, `_set_time_input_value`, `_scroll_rwc_calendar_to`.
- 새 흐름: **trigger button click → rwc 셀까지 가상 스크롤 → 셀 click → form 시간 입력 → Tab commit**.
- `debug.py` 신규 (`_assembled/src/gfa_setting/debug.py`) — 환경변수 `GFA_DEBUG_PAUSE_ON_ERROR=1` 시 `GFABrowserError` 발생 즉시 `input()` 대기. **사용자가 DevTools 로 DOM 검사 → 셀렉터 새로 따기 → 종료**까지 브라우저가 살아있음. 셀렉터 깨짐 디버깅의 결정적 단축.
- `flows/group_setup.py`, `cli.py`: debug 모드일 때 per-group swallow 대신 즉시 raise 로 전파 (조용히 실패 → 다음 그룹 진행 패턴이 디버깅 시 방해됨).
- 검증: 2026-05-13 새 UI 흐름 dry-run 성공.

**운영 노트**:
- 셀렉터 깨짐 의심 시 `GFA_DEBUG_PAUSE_ON_ERROR=1 gfa-setting <id>` 로 실행. 첫 에러 지점에서 멈추고 DevTools 사용 가능.
- rwc 캘린더는 **가상 스크롤** — 셀이 DOM 에 없으면 스크롤로 먼저 만들어줘야 click 됨. `_scroll_rwc_calendar_to` 가 그 역할.

### B. 멀티 잡 큐 (입력 일괄 → 순차 실행) — 2026-05-14 (working tree, 미커밋)

같은 광고 계정 안에서 **콘텐츠/캠페인/참조 그룹/소재가 서로 다른 여러 잡**을 한 명령으로 입력해 두고 순차 실행. 다른 계정으로 가려면 새 명령.

**흐름**:
1. **계정 1회 검증** (CLI 인자 — 다른 계정은 새 명령)
2. **입력 페이즈** (`_collect_input_phase` in `cli.py`):
   잡 #1 입력 (콘텐츠 경로 → 캠페인 ID 검증 → 그룹 spec 입력 → 통합 확인) → `잡을 더 추가하시겠습니까? [y/N]` → `y` 면 잡 #2 입력 → … → `N` 으로 입력 종료
3. **큐 요약 출력** → `총 N개 잡을 순차 실행합니다. 시작? [Y/n]` (`confirm_run_all`)
4. **실행 페이즈**: 잡 #1 commit → 30초 cooldown → 잡 #2 commit → …
5. **종료 요약**: `성공 X / 실패 Y (총 N잡 실행 시도)`

**아키텍처 변경**:
- `flows/group_setup.py` 의 단일 `run_group_setup_flow` 가 **입력 페이즈(`collect_group_setup_spec`)** + **실행 페이즈(`execute_group_setup`)** 둘로 분리.
- `GroupSetupSpec` (frozen dataclass) — 입력 페이즈 산출물. 한 잡의 모든 입력값(`ctx / reference_group_name / base_name / reference_creative_name / materials_per_ad / landing_url_template / distributed / image_count / group_count`)을 freeze 해 담음.
- **시작일시는 spec 에 포함 X** — 큐가 길어질 수 있어서 `execute_group_setup` 진입 시점에 `now + 50분` 으로 매번 재계산.
- 기존 `run_group_setup_flow` 는 `collect → execute` 의 얇은 wrapper 로 유지 (backward compat).
- `verify_account_with_retry`, `verify_campaign_with_retry` 가 `_` 접두 private → public 으로 승격 (cli 가 직접 호출).
- 신규 prompts (`prompts.py`): `prompt_continue_with_next_job` (기본 N, 무한 입력 방지), `confirm_run_all` (기본 Y, 입력 다 끝났으면 보통 실행).
- `cli.py:42` `JOB_COOLDOWN_SECONDS = 30` — 잡 간 cooldown. 봇 탐지 trade-off, 변경 시 본 페이지의 [§운영 제약](#운영-제약-계정-정지-위험) 참조.

**격리 정책**:
- 입력 페이즈에서 한 잡 입력이 실패(취소·이미지 0장·검증 실패)해도 큐는 멈추지 않고 다음 잡 추가 여부를 묻는다. **실패한 잡만 큐에서 제외**.
- 실행 페이즈에서 한 잡 실행이 실패해도 다음 잡으로 계속. **잡 단위 격리**.
- 전체 잡 실패 + 성공 0 → exit 1. 그 외 정상 종료(exit 0).
- `KeyboardInterrupt` (Ctrl+C) — 깔끔히 빠져나오면서 그 시점까지의 성공/실패 요약 출력.

**`GroupSetupResult` 변경**:
- `cancelled=True` 제거. 입력 페이즈에서 취소/무효는 `collect_group_setup_spec` 가 `None` 반환 → cli 가 큐에서 제외. 실행 페이즈는 항상 created/partial/failed 만 추적.
- 단일 잡 wrapper(`run_group_setup_flow`)는 backward compat 위해 spec=None 시 `GroupSetupResult(cancelled=True)` 그대로 반환.

**테스트** (`_assembled/tests/test_cli.py`):
- `test_cli_happy_path_single_job` — 잡 1개 정상.
- `test_cli_happy_path_multi_job` — 잡 3개 순차 실행.
- `test_cli_account_verify_fails_exits_2` — 계정 검증 실패 → exit 2.
- `test_cli_no_jobs_collected_exits_0` — 입력 페이즈에서 잡 0개 → 정상 종료.
- `test_cli_user_declines_run_all_exits_0` — 최종 confirm 에서 N → 실행 안 함.
- `test_cli_execute_browser_error_exits_1` — 모든 잡 실패 → exit 1.
- `time.sleep` 은 monkeypatch 로 무력화 (cooldown 대기로 테스트 늘어지지 않게).

**.gitignore**: `.claude/settings.local.json` 추가 — PC 별 권한 허용 목록은 sync 하지 않음.

## 저장소 / 진입점

- **GitHub**: https://github.com/Min-Gil-Sang/GFA-Setting
- **로컬 검증 위치**: `C:\Users\gguy\Desktop\GFA-Setting`
- **언어/런타임**: Python 3.11+, DrissionPage(Chrome CDP)
- **CLI 진입점**: `gfa_setting.cli:main` → `gfa-setting <광고계정ID>`

## 어느 컴퓨터에서든 0→1 세팅 (이식 절차)

```bash
# 1) 클론
git clone https://github.com/Min-Gil-Sang/GFA-Setting.git
cd GFA-Setting/_assembled

# 2) 가상환경
python -m venv .venv
.venv\Scripts\activate                # Windows
# source .venv/bin/activate            # macOS/Linux

# 3) 설치 (개발의존 포함)
pip install -e .[dev]

# 4) .env
cp .env.example .env                   # 필요 시 편집
#  ADS_BASE_URL=https://ads.naver.com
#  GFA_BROWSER_PROFILE_DIR=./.browser_profile
#  BROWSER_HEADLESS=false               (봇탐지 회피 — false 유지 권장)
#  ACTION_MIN_DELAY=1.0 / ACTION_MAX_DELAY=3.0

# 5) 최초 1회: 브라우저 띄워서 ads.naver.com 수동 로그인
#    이후 .browser_profile/ 에 쿠키 저장 → 자동 재사용

# 6) 실행
gfa-setting 2380197
```

선결 조건:
- Chrome 브라우저 설치 (DrissionPage CDP)
- ads.naver.com 로그인 가능 계정
- 콘텐츠 폴더 접근 권한 (NAS UNC `\\192.168.0.103\...` 또는 로컬)

## 7개 입력값 (대화형 한국어 프롬프트)

| # | 입력 | 예시 | 비고 |
|---|---|---|---|
| 1 | 콘텐츠 폴더 경로 | `\\NAS\제작콘텐츠\GFA\이미지\2026\4월\피드_세럼파데...` | NAS UNC 또는 로컬 |
| 2 | 캠페인 ID | `1327677` | ADR-012: 직접 입력 (스크레이핑 X) |
| 3 | 참조 광고 그룹 이름 | `260424_여4059_[메뷰여]_AI 소재_260422_im_gfa_260424_01` | 전체 정확 매치 |
| 4 | 새 그룹 베이스 이름 | `test` | → `test_01`, `test_02`, ... |
| 5 | 참조 광고 소재 이름 | `AI 소재_260424_4차_im_gfa_260427_04 10_스퀘어형` | 전체 정확 매치 |
| 6 | 광고당 소재 개수 | `5` (default, max 10) | 봇탐지 회피 상한 |
| 7 | 랜딩 URL 템플릿 | `https://...?utm_content=im_gfa_260430_03` | `_NN` suffix → 그룹 인덱스 자동 치환 (또는 `(고정)` 접미사) |

자동 계산:
- **시작일시** = 실행 시각 + 50분 (날짜 자동 rollover)
- **그룹 개수** = `ceil(image_count / per_ad)` — 상한 N=20 (>10 경고, >20 차단)
- **이미지 분배** = 그룹별 N개씩, 마지막 그룹은 잔여 (중복 없음, 순서 보존)
- **랜딩 URL 치환** = 입력 NN 을 base 로 `(base + group_index - 1)`. 예: `_03` + 4 그룹 → `_03, _04, _05, _06`

## 실행 흐름 (그룹당 ≈23 액션)

```
캠페인 대시보드
  → [+ 새 광고그룹] 클릭
  → [기존 광고 그룹 불러오기] 모달 → 이름 필터 → [확인]
  → 시작일시 picker (오늘+50분)
  → [다음] (그룹 commit, /create/adSet → /create/ad 이동)
  → 참조 소재 모달 [확인]
  → 모두 삭제하기
  → [+ 이미지 추가] 모달 → file input set + 카드 click + 모달 [확인]
  → 광고 소재 이름 + 랜딩 URL 입력
  → [저장] (소재 commit, /create/complete 진입)
```

## 핵심 ADR

- **ADR-011**: REST/OAuth → DrissionPage 브라우저 자동화. OpenAPI 차단 우회.
- **ADR-012**: 캠페인 리스트 스크레이핑 제거 → 캠페인 ID 직접 입력.
- **ADR-013**: 27 파라미터 빌더 → "기존 광고 그룹 불러오기" UI 복제. 매핑표/parsers.py 전부 제거, 사용자 입력 5개로 축소.
- **ADR-014**: 그룹+소재 atomic 등록. 그룹만 commit 되고 소재 실패 → `partial` (orphan group) 추적.

## 운영 제약 (계정 정지 위험)

- **봇 탐지 보수 타이밍**: 액션 간 2~8s, 그룹 사이 8~12s 랜덤 지연. N>10 경고, N>20 차단.
- **antd controlled component**: hydrate 트리거(라디오/[확인])는 **반드시 DP CDP 트러스트 click** (`isTrusted=true`). JS dispatchEvent / native value setter 는 silent partial fail.
- **부분 실패 (orphan group)**: 그룹은 commit 됐는데 소재 단계 실패 시 `partial` 추적. **사용자가 GFA 콘솔에서 수동 삭제**. 자동 재시도 0회 (다음 그룹 진행, 무한루프 방지).
- **세션 분산**: 동일 세션 내 200+ 액션 누적 금지. 대량 dry-run 후 다음 운영은 별도 시간으로.

## 진단 / 트러블슈팅

CLI 실행 디렉토리에 자동 생성되는 dump:
- `diag_form_<label>_<ts>.json` — 폼 상태 5시점 snapshot (참조 hydrate / 이미지 모달 후 / 이름 설정 후 / URL 설정 후)
- `diag_save_failed_<ts>.html` — [저장] 실패 시 페이지 HTML
- `diag_calendar_no_cell_<ts>.html` — 시작일시 캘린더 진입 실패

실패 시 흐름:
1. 진단 dump → 어느 시점에 어떤 필드가 비었는지 추적
2. 로그의 `진단 [...]:` 라인 — 시점별 폼 상태 한 줄 요약
3. 부분 실패 그룹은 GFA 콘솔에서 수동 삭제

E2E 4시간 troubleshooting 핵심 교훈 ([[tacit/coding-lessons]] 후보):
1. **이미지 카드 selector 버그** — `img.closest('label, [role=checkbox]...')` 가 antd CSS-in-JS hash wrapper(`div.css-3hsv0d`) 와 매치 안 됨 → `img.parentElement` (50~400px bbox) + alt 매칭으로 수정.
2. **선택 카운트 정규식 false-match** — modal scope 한정 안 한 `\d+/\d+` 가 페이지 전역의 `0/8021200` 매치 → modal scope + `\d{1,4}/\d{1,5}` 자릿수 제한.
3. **참조 hydrate 부분 실패 (root cause)** — `select_first_radio` + `confirm_modal` 의 `dispatchEvent('click')` 이 React state 부분 sync → 이름만 hydrate, 광고 문구/프로필/이미지 비어있음 → DP CDP 트러스트 click 으로 일괄 교체.
4. **`is_saved` false negative** — URL 이 `/create/complete` 이동했는데도 마크업 selector mismatch 로 saved=False → `urlMoved` 단독으로도 saved 인정.

## ⚠️ 코덱스 감사 결과 (2026-04-30 — v0.1.0 기준 잔존 이슈)

> Codex CLI(gpt-5) 가 전체 코드/스킬 직접 감사. 본 위키 작성자가 파일 직접 열어 검증 완료.

### 치명
- **README/SKILL의 antd 안전가정과 코드 불일치**. 문서는 "모든 click/입력은 DP CDP 트러스트, JS dispatchEvent/native value setter 금지"라고 명시(`README.md:62`, `SKILL.md:53`)했으나, 실제 코드에는 `dispatchEvent` / `Object.getOwnPropertyDescriptor(...HTMLInputElement.prototype, 'value').set` 패턴이 다수 잔존:
  - `_assembled/src/gfa_setting/operations/ad_sets.py:73, 99, 133-140, 169, 336-342`
  - `_assembled/src/gfa_setting/operations/materials.py:63, 89-96, 124-126, 255, 493`
  - **실제 fix 는 hydrate 트리거(라디오/확인 모달) 한정**이고, 다른 click/input 은 여전히 JS 패턴 사용. N=3 dry-run 은 통과했지만 "전부 트러스트화" 라는 문서 주장은 오인 소지.
  - **권장**: 문서를 정확히 ("hydrate 트리거만 트러스트화") 고치거나 코드를 일괄 트러스트화로 마저 정리.

### 높음
- **부분 실패가 CLI 종료 출력에 반영 안 됨**. `GroupSetupResult.partial` 은 누적되지만(`flows/group_setup.py:266, 275`), `cli.py:111` 은 `성공: {created} / 실패: {failed}` 만 출력. **orphan group 이 사용자에게 안 보임** → GFA 콘솔에서 수동 정리 누락 위험. 권장: `partial` 카운트와 그룹 ID 목록도 출력.
- **로그 마스킹 필터가 무력화됨**. `logging_config.py:26-47` 에 secrets 마스킹 필터 구현돼 있지만 `cli.py:60` 이 `configure_logging(level=..., secrets=[])` 로 빈 리스트 전달. 결과: 환경변수의 `GFA_WEB_LOGIN_ID/PW` 가 디버그 로그에 그대로 찍힐 가능성. 권장: settings 의 비밀 후보를 secrets 로 주입.
- **pre-commit / .gitignore 강제 누락**. AGENTS.md §1, §8 은 `.env` 커밋 차단을 강제하지만 `_assembled/.gitignore`, `_assembled/.pre-commit-config.yaml` 미존재. 루트 `.gitignore` 에 의존. 다른 컴퓨터로 옮겨 `_assembled/` 단독 작업 시 보호 안 됨.

### 중간
- **그룹 수 상한이 너무 느슨**. `group_setup.py:183-192` 가 N>10 경고, N>20 차단. 단일 세션 200+ 액션 누적 시 봇탐지 위험. 운영 시 N=5 이하 권장.
- **시작일시 +50분 rollover** — `timedelta` 라 날짜 경계는 정상이지만(`group_setup.py:202-204`), **타임존/서버 시간 기준 검증 없음**. 컴퓨터 시계 오차 시 즉시 상영 시작 또는 과거 시간 거부 가능.
- **`_NN` 치환이 마지막 `_\d{2,3}` 만 매치**(`group_setup.py:123-134`). `_1`, `_0001`, 경로 중간 suffix 는 기대와 다른 결과. 입력 URL 의 NN 위치/자릿수 확인 필요.
- **봇탐지 회피가 균등분포 sleep 뿐**(`browser.py:173-176`, `group_setup.py:298-300`). 사람의 액션 간격은 long-tail 분포에 가까움. 헤드리스 false 기본값(`settings.py:35-37`)은 안전한 선택.

### 낮음
- **이식성 함정**. README/SKILL 의 설치 경로가 `~/.claude/skills/GFA-Setting/_assembled` 로 박혀 있음(`README.md:20`, `SKILL.md:33`). 실제로는 어디서든 동작하지만 문서가 위치를 가정. 본 위키의 "이식 절차" 가 정답.
- **`.browser_profile` 상대경로 기본값**(`settings.py:23-24`, `.env.example:9`). 실행 cwd 마다 새 프로필 생성 가능 → 매번 재로그인. **절대경로 권장** (예: `C:/Users/gguy/.gfa-setting/profile`).
- **테스트 163/163은 실브라우저 보장이 아님**. DrissionPage 는 mock 중심(`tests/test_browser.py`, `tests/conftest.py`, `tests/test_operations_ad_sets.py:3-4`). E2E 는 N=3 1회. UI 변경 시 단위 테스트는 통과해도 실제는 깨질 수 있음.

## 검증 상태

- 단위 테스트: **163/163 통과** (커버리지 85%)
- ruff/mypy strict: **에러 0**
- E2E dry-run (2026-04-30): **N=3 atomic 성공**, 모두 `/create/complete` 진입 (테스트 캠페인 1327677, CCFM-인완-네리티아 계정)
- 상세: 저장소 `_assembled/E2E_TEST_REPORT.md`

## 🔬 최종 max-mode 교차 감사 (2026-04-30) — Codex GPT-5.5 max + Claude 서브에이전트 병렬

> 두 독립 evaluator 가 같은 코드를 별도 컨텍스트에서 감사. 수렴/발산 클레임 직접 file:line 검증 후 정리.

### 두 감사 모두 수렴한 사실 (가장 신뢰도 높음)
1. **antd CDP 트러스트 약속 위반** — README.md:62 / SKILL.md:53 약속과 달리 `ad_sets.py:73,99,133-140,169-171,336-342`, `materials.py:63,89-96,124-126,255` 에 `dispatchEvent` + `Object.getOwnPropertyDescriptor(...HTMLInputElement.prototype, 'value').set` 잔존. **N=3 dry-run 통과는 hydrate 트리거(라디오/[확인])만 트러스트화된 결과**, 다른 click/input 은 antd 마이너 업데이트에 silent partial fail 직격 가능.
2. **로그 마스킹 무력화** — `cli.py:60` `configure_logging(level=..., secrets=[])` 빈 리스트 → settings 에 `gfa_web_login_pw: SecretStr` 정의(`settings.py:31-33`)에도 마스킹 미주입.
3. **partial 자동 정리·재시도 0** — `group_setup.py:264-276,319-322` 가 `partial.append + continue` 만, CLI 출력에서도 빠짐(`cli.py:111`).
4. **시작시각 naive datetime** — `group_setup.py:202-204` `now() + timedelta(minutes=50)` 가 timezone 표기 없음. 시계 drift / 타임존 혼선 시 즉시 상영 또는 과거시간 거부.
5. **죽은 코드 일치** — `mappings/*` (ADR-013 이후 0 import), `models.py:76,83,133,141` 의 `AgeRange/AdSetCreateParams/InterestCode/PurchaseIntentCode`, `prompts.py:83-101` 의 `prompt_group_count/confirm_group_creation` (group 수는 자동 계산이라 호출 0), `pyproject.toml:14,19,28,32` 의 `requests/tenacity/responses/types-requests` 의존성.
6. **테스트 mock 중심** — `test_operations_*` 가 DOM 없는 MagicMock. 163/163 + 85% 커버리지는 **로직 정합 보장이지 GFA UI 깨짐 보장 아님**.

### Codex GPT-5.5 max 가 추가로 발견 (검증됨)
- **`browser.py:79` `set.auto_handle_alert(on_off=True, accept=True)`** — 의도치 않은 confirm/beforeunload(데이터 손실 경고 등)도 **자동 수락**. 사용자 작업 중 실수 가능성 ↑.
- **달력 월 이동 미지원** (`ad_sets.py:410-416`) — 에러 메시지에 박혀있음(`"현재 표시 월이 다를 가능성 — 월 이동 미지원"`). 자정 직전 실행 + 시작=다음달 1일 케이스 (드물지만) 깨짐.
- **operations 내부 `_pause` 가 환경변수 무시** — `.env` 의 `ACTION_MIN/MAX_DELAY` 는 `browser.human_delay()` 한 곳에서만 적용. `ad_sets._pause(3.0,6.0)` (`ad_sets.py:41`), modal close `(5.0,8.0)`, inter-group `(8.0,12.0)` (`group_setup.py:298`) 은 하드코딩 → **사용자가 봇탐지 강화하려고 delay 늘려도 대부분 무시됨**.
- **마우스 경로 시뮬 0 / 고정 좌표** (`ad_sets.py:504-510`) — CDP 보강 click 이 항상 `(x=10, y=10)`. 사람 마우스 트레이스 없음.
- **새 그룹명 충돌 사전조회 0** (`group_setup.py:212-215`) — 같은 base_name 재실행 시 `test_01` 중복 생성 가능. GFA 가 막아주면 실패, 안 막아주면 동명 그룹 누적.
- **진단 dump 에 폼 값 평문 저장** (`materials.py:747-756, 810-813`) — `descriptionText/profileName` 등 실 광고 데이터 dump JSON 에 그대로. 다중 작업자 환경에서 디스크 노출 면 ↑.

### Claude 서브에이전트가 추가로 발견 (검증됨)
- **`urlMoved` 정규식 false-positive 위험** (`materials.py:672`) — `/\\/done|\\/complete/.test(url)` 에 word boundary 없음. URL `/da/dashboard?type=complete` 등 query string 매치 가능 → 실제는 저장 안 됐는데 saved=True. **운영 시 미세 흔적 누락 위험**.
- **`exceptions.GFAAPIError`, `GFAUploadError`** — `exceptions.py:10,39` 정의만, src 내 raise/import 0건. ADR-011 (REST→브라우저) 이후 사어.
- **`dd/step-01-환경셋업_API클라이언트/output/`** — git tracked 56 파일 (대부분 README/dom dump/script prototype 잔재). 디스크 484MB 중 venv/.browser_profile 은 .gitignore 로 차단됨, **순수 git 부담은 작지만 (.git 579KB) prototype 잔재가 그대로 trunk 에 노출**.

### Claude 서브에이전트의 거짓 클레임 (검증 후 기각)
- ❌ "`_assembled/.venv` 가 git tracked, 다른 PC 절대경로 박힘" → **거짓**. 루트 `.gitignore:2` 의 `**/.venv/` 패턴이 매치, `git check-ignore -v _assembled/.venv` 통과. 다른 PC 영향 없음.

### 최종 분류 (두 감사 합산)

**🚨 릴리스 차단 (v0.1.x 패치 권고)**
- antd CDP 트러스트 위반 — 코드 일괄 교체 또는 SKILL/README 표현 완화 (현실에 맞춤)
- 로그 마스킹 secrets 빈 배열 — settings 비밀 후보 자동 주입
- partial(orphan group) CLI 출력 누락
- `urlMoved` 정규식 false-positive — `/\/(done|complete)$/` 또는 정확 비교
- `auto_handle_alert(accept=True)` — 데이터 손실 confirm 만 reject 하도록 분기 또는 옵션화

**⚠️ v0.2 차단 (다음 릴리스 전 필수)**
- 시작시각 timezone-aware (`zoneinfo.ZoneInfo("Asia/Seoul")`) + 시계 drift 검증
- operations `_pause` 가 환경변수 반영 — 봇탐지 강화 옵션 실효화
- fingerprint/마우스 경로 시뮬 (현재 봇탐지 단순 균등 sleep + 고정좌표)
- 새 그룹명 충돌 사전조회 + 자동 suffix bump
- 달력 월 이동 지원 또는 다음달 시작 차단

**📋 백로그**
- 죽은 코드 일괄 제거 (`mappings/`, models 빌더 4종, prompts 미사용 2종, exceptions 2종, requests/tenacity/responses/types-requests)
- `dd/step-01-...output/` 56 파일 → `_archive/` 분리
- 셀렉터 중앙화 (`selectors.py`)
- 진단 dump 디렉토리 옵션화 + 폼 값 마스킹
- `_assembled/.gitignore` + `.pre-commit-config.yaml` 단독 신설 (떼어 갈 때 보호)
- 테스트 일부를 실 브라우저 스모크로 보강

### 종합 결론
v0.1.0 은 happy path (N=3, 정상 GFA UI) 동작 검증됨. 그러나 **문서 약속 vs 코드 정합 (antd 트러스트, 마스킹, partial 표시)** 과 **edge case 견고성 (timezone, urlMoved 정규식, auto-confirm)** 에 5개 릴리스 차단급 균열. 운영은 가능하지만 SKILL.md/README.md 의 안전 약속을 글자 그대로 신뢰하면 안 됨 — 본 §최종 감사 항목을 운영 매뉴얼 일부로 취급.

## ⚠️ 코덱스 2차 감사 — 죽은 코드 + 방향성 위험 (2026-04-30)

### 죽은 코드 (직접 검증 완료, 0 import / 0 호출)
- **`_assembled/src/gfa_setting/mappings/`** (interests.py, purchase_intents.py) — ADR-013 으로 폐기됐는데 파일·클래스 잔존. src 어디서도 import 0건.
- **`_assembled/src/gfa_setting/models.py:76,83,133,141`** — `AgeRange / AdSetCreateParams / InterestCode / PurchaseIntentCode` 클래스. 27 파라미터 빌더 시절 잔재. 다른 src 파일에서 사용 0건.
- **`_assembled/pyproject.toml:14,28`** — `requests`, `responses>=0.25` 의존성. REST API 시절 잔재. `_assembled/src` 에서 `import requests` / `import responses` 0건.
- **`dd/step-01-환경셋업_API클라이언트/output/`, `dd/_assembled/`** — DD 빌드 단계별 산출물 중복본. 운영 코드는 `_assembled/` 만 사용.

### 방향성 위험 (앞으로 발등 찍힐 결정)
- **DrissionPage 단일 장애점** (`browser.py:25,66,75`) — 라이브러리/Chrome 자체 깨지면 전체 다운. fallback 0.
- **셀렉터 분산** (`ad_sets.py:331,393,550`, `materials.py:59,239,550,573`) — README 의 "중앙 관리" 약속과 불일치. GFA UI 한 번 바뀌면 여러 파일 동시 수정 강제.
- **진단 dump 가 cwd 직쓰기** — 운영 누적 시 작업 디렉토리 오염. `diag/` 같은 별도 디렉토리 분리 필요.
- **partial 은 기록만, rollback·retry 0** (`group_setup.py:266,275,284`) — orphan group 매 운영 누적 구조.
- **소재가 이미지 전용** (`materials.py:273,826`) — 영상/문구/프로필 override 추가 시 이 모듈 통째로 리팩터.
- **테스트가 mock 중심** (`test_operations_ad_sets.py:35,40`, `test_operations_materials.py:46,49`) — DOM 없는 MagicMock 으로 검증, UI 변경 감지 불가. **163/163 통과는 로직 정합 보장이지 GFA UI 안 깨짐 보장 아님**.

### v0.2 첫 작업 우선순위 (권장)
1. **죽은 코드 제거** — `mappings/` 폴더 + `models.py` 의 4개 빌더 클래스 + `requests/responses` 의존성 → 패키지 슬림화
2. **셀렉터 중앙화** — `selectors.py` 한 파일로 모음 → UI 변경 시 한 곳만 수정
3. **진단 dump 디렉토리 옵션화** — `GFA_DIAG_DIR=./diag/` 환경변수
4. **orphan group 자동 감지/삭제** — 다음 실행 시 partial 흔적 청소 플로우
5. **CLI 종료 출력에 partial/orphan ID 표시** — 코덱스 1차 감사 [높음] 대응
6. **`configure_logging` secrets 주입** — `cli.py:60` 빈 리스트 → settings 의 비밀 후보 자동 주입
7. **`_assembled/.gitignore` + `.pre-commit-config.yaml` 단독 부재 해결** — `_assembled/` 만 떼어 가도 보호되도록

## 🚨 UI 변경 / 셀렉터 깨짐 대응 플레이북

GFA UI 가 antd 업데이트나 마크업 리팩터로 바뀌면 N=1 dry-run 부터 깨진다. 다음 절차로 잡는다.

### 0. (v0.1.x 권장 1순위) `GFA_DEBUG_PAUSE_ON_ERROR=1` 로 라이브 디버깅
첫 `GFABrowserError` 발생 시 브라우저가 살아있는 채로 `input()` 대기. **DevTools 열어서 깨진 element 의 새 셀렉터 직접 따고** 종료. dump 파일 보기 전 가장 빠른 단축.

```bash
# Windows PowerShell
$env:GFA_DEBUG_PAUSE_ON_ERROR=1; gfa-setting 2380197
# bash
GFA_DEBUG_PAUSE_ON_ERROR=1 gfa-setting 2380197
```

debug 모드일 때 cli·group_setup 의 per-group swallow 가 꺼지고 즉시 raise — 첫 에러 지점이 살아 있는 그 페이지에 그대로 멈춤.

### 1. 어느 단계에서 깨졌는지 빠르게 식별
실행 디렉토리에 자동 생성되는 진단 dump 로 구간 좁히기:

| dump 파일 | 의미 | 이 dump 가 비어있다면 |
|---|---|---|
| `diag_form_01_after_reference_hydrate_<ts>.json` | 참조 그룹/소재 hydrate 직후 폼 상태 | 참조 모달 → [확인] 단계 셀렉터 깨짐. `ad_sets.py:open_reference_modal/apply_name_filter/select_first_radio/confirm_modal` 의심 |
| `diag_form_02_after_remove_images_<ts>.json` | "모두 삭제하기" 클릭 후 | `materials.py:remove_all_reference_images` 의 button 텍스트 매치 깨짐 |
| `diag_form_03_after_image_modal_ok_<ts>.json` | + 이미지 추가 모달 닫은 직후 | `materials.py:open_image_upload_modal / upload_image_files` 의 file input 또는 카드 셀렉터 깨짐 |
| `diag_form_04_after_set_name_<ts>.json` | 광고 소재 이름 set 후 | `materials.py:set_creative_name` input 셀렉터 깨짐 |
| `diag_form_05_after_set_url_<ts>.json` | 랜딩 URL set 후 | `materials.py:set_landing_url` input 셀렉터 깨짐 |
| `diag_save_failed_<ts>.html` | [저장] 실패 시 페이지 HTML | save 버튼 텍스트 변경 또는 antd 검증 실패 |
| `diag_calendar_no_cell_<ts>.html` | 시작일시 캘린더 진입 실패 | DatePicker 셀 셀렉터 깨짐 |

→ **JSON 의 어느 필드가 `null`/빈문자열인지** 가 정확한 깨짐 지점.

### 2. 로그의 "진단 [...]:" 라인 보기
`cli.py` 가 stdout 으로 한 줄 요약 출력. 시점별 폼 상태(name/link/profile/imgCount/inputs/textareas/radios) 를 한 줄로 찍음 — dump JSON 풀로 열기 전 빠른 스캔용.

### 3. 실제 GFA 페이지에서 셀렉터 새로 따기
1. Chrome DevTools 열기 (자동화 중인 그 브라우저 그대로 사용 가능)
2. 깨진 element 우클릭 → Inspect
3. **antd CSS-in-JS 해시 클래스(`.css-3hsv0d` 같은)는 절대 셀렉터로 쓰지 말 것** — 빌드마다 바뀜. 이 함정에 4시간 박힌 적 있음 (E2E_TEST_REPORT §1).
4. 안정한 후보 (우선순위):
   - `[role="dialog"]`, `[role="combobox"]`, `[role="checkbox"]` 등 **ARIA role**
   - `name="..."`, `data-...` 속성
   - 버튼은 **텍스트 매치** (`.includes('확인')`, `.includes('+ 새 광고그룹')`)
   - 이미지 카드는 **`img.parentElement` + alt 매칭** (`materials.py:upload_image_files` 패턴 그대로)
5. modal 내부 element 찾을 때는 **반드시 modal scope 부터 좁힐 것** (`document.querySelector('[role="dialog"]') 안에서`). 페이지 전역 검색은 false-match 함정 (E2E_TEST_REPORT §2 — `0/8021200` 매치 사고).

### 4. hydrate 트리거는 무조건 DP CDP 트러스트 click
참조 그룹/소재 모달의 라디오 선택 + [확인] 클릭은 **반드시 `session.page.ele(...).click()` (DrissionPage CDP, `isTrusted=true`)** 사용. JS `dispatchEvent('click')` 이나 `Object.getOwnPropertyDescriptor(...HTMLInputElement.prototype, 'value').set` 은 React state 부분 sync 되어 **이름만 hydrate, 광고 문구/프로필/이미지 비어있는 silent partial fail** 발생 (E2E_TEST_REPORT §3 — root cause). 이게 가장 자주 박히는 함정.

### 5. 텍스트 input 은 `ele.input(text, clear=True)`
native value setter (`Object.getOwnPropertyDescriptor` 패턴) 는 antd Form store sync 가 부분 실패. CDP keyboard 입력 (`ele.input()`) 이 안전 (E2E_TEST_REPORT §4).

### 6. `is_saved` 검증은 URL 우선
[저장] 후 `/create/complete` 로 URL 이동했으면 saved=True. 페이지 마크업의 `completeActive` selector 매칭은 selector 변경에 취약 — false negative 발생함 (E2E_TEST_REPORT §5).

### 7. 셀렉터 수정 후 검증 순서
1. 단위 테스트 `pytest -k <변경 함수>` 통과 확인 (mock 이라 로직만 보장)
2. **N=1 dry-run** 으로 실 브라우저 1회 — diag dump 5개 모두 정상값 채워졌는지 확인
3. **N=2~3 dry-run** 으로 그룹 사이 transition 검증
4. orphan group 모두 GFA 콘솔에서 수동 삭제 후 운영 사용

### 8. 자주 깨지는 지점 우선순위
1. **antd 모달 .ad-cms-modal 클래스** — 가장 자주 변경됨. `[role="dialog"]` 로 fallback.
2. **이미지 카드 wrapper** — CSS-in-JS hash. `img.parentElement` (50~400px bbox) 로 회피.
3. **버튼 텍스트** — "확인" / "다음" / "저장" / "+ 새 광고그룹" / "기존 광고 그룹 불러오기" / "모두 삭제하기" / "+ 이미지 추가". 한 글자 변경에도 매치 깨짐. 부분 매치 (`.includes`) 권장.
4. **DatePicker 셀** — 캘린더 마크업이 antd minor 업데이트마다 자주 흔들림. **2026-05-13 antd DatePicker → rwc(가상 스크롤 캘린더) + form 시간 input 분리로 통째로 교체된 사례 있음** — picker trigger 가 input 이 아니라 button 으로 변하면 input.placeholder 매치 셀렉터부터 깨짐. 가상 스크롤 셀은 DOM 에 없으면 스크롤 먼저, 그다음 click. `operations/ad_sets.py:_find_start_datetime_trigger / _scroll_rwc_calendar_to / _find_form_time_input / _set_time_input_value` 참고.

## 미해결 / 향후 작업

- 영상 소재 (`.mp4` 등) 미지원 — 이미지 (`.jpg/.jpeg/.png/.gif/.webp`) 만
- 광고 문구 사용자 override 미지원 — 참조 그대로
- 부분 실패 자동 재시도 0회 (다음 그룹 진행)
- 동명 라이브러리 이미지 다중 매치 시 첫 N개 사용 — 라이브러리 정리 권고
- 코덱스 1차 감사 치명/높음 항목 후속 패치 (문서-코드 정합 / partial 출력 / secrets 주입 / 단독 .gitignore·pre-commit)
- 코덱스 2차 감사 v0.2 우선순위 (위 §v0.2 첫 작업 우선순위)

## 관련 페이지

- [[domains/marketing-automation]] — 상위 도메인
- [[domains/ai-automation]] — bob/dd/harness 파이프라인 (이 스킬 빌드 경로)
- [[qscv/media-gfa]] — GFA 매체 운영 기준
- [[tacit/coding-lessons]] — antd controlled component / DP CDP 트러스트 / selector hash 함정 (후보 추가)
- [[sources/src-gfa-setting-skill-2026-04-30]] — v0.1.0 빌드/감사 소스

<!-- AUTO:tags-begin -->
**Tags**: #status/active #domain/marketing-automation #tech/drissionpage #tech/python #platform/naver-gfa #skill/gfa-setting
<!-- AUTO:tags-end -->
