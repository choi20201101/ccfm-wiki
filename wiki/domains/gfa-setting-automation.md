---
aliases: ["GFA-Setting", "GFA 광고 세팅 자동화", "네이버 GFA 자동화"]
type: domain
domain: marketing-automation
confidence: medium
created: 2026-04-30
updated: 2026-04-30
sources: [src-gfa-setting-skill-2026-04-30]
---

# GFA-Setting — 네이버 GFA 광고 세팅 자동화 스킬

> 네이버 성과형 디스플레이(GFA) 광고 그룹+소재 atomic 자동 등록 Claude 스킬.
> v0.1.0 (2026-04-30) — N=3 dry-run 성공.
> 트리거: `GFA-Setting`, `GFA 세팅`, `GFA 광고 세팅`, `NAS 소재 GFA 업로드`, `네이버 광고 자동 세팅`, `GFA 그룹 생성`, `광고 소재 자동 등록`.

## 1줄 요약 (꺼내쓰기용)

```
gfa-setting <광고계정ID>
```
→ 7개 입력값(콘텐츠 경로/캠페인 ID/참조 그룹/베이스 이름/참조 소재/per_ad/랜딩 URL) 받아서 N개 광고 그룹+소재를 한 번에 생성.

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

## 미해결 / 향후 작업

- 영상 소재 (`.mp4` 등) 미지원 — 이미지 (`.jpg/.jpeg/.png/.gif/.webp`) 만
- 광고 문구 사용자 override 미지원 — 참조 그대로
- 부분 실패 자동 재시도 0회 (다음 그룹 진행)
- 동명 라이브러리 이미지 다중 매치 시 첫 N개 사용 — 라이브러리 정리 권고
- 코덱스 감사 치명/높음 항목 후속 패치 (문서-코드 정합 / partial 출력 / secrets 주입 / 단독 .gitignore·pre-commit)

## 관련 페이지

- [[domains/marketing-automation]] — 상위 도메인
- [[domains/ai-automation]] — bob/dd/harness 파이프라인 (이 스킬 빌드 경로)
- [[qscv/media-gfa]] — GFA 매체 운영 기준
- [[tacit/coding-lessons]] — antd controlled component / DP CDP 트러스트 / selector hash 함정 (후보 추가)
- [[sources/src-gfa-setting-skill-2026-04-30]] — v0.1.0 빌드/감사 소스

<!-- AUTO:tags-begin -->
**Tags**: #status/active #domain/marketing-automation #tech/drissionpage #tech/python #platform/naver-gfa #skill/gfa-setting
<!-- AUTO:tags-end -->
