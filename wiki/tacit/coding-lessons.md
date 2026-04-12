---
type: tacit
category: coding
confidence: medium
first_observed: 2026-04-13
last_confirmed: 2026-04-13
---

# 코딩/자동화 교훈

## [2026-04-13] 네이버 카페 크롤링/가입 자동화 패턴

### 로그인 유지
- **쿠키 재사용 전략**: `save_cookies.py`로 visible 모드에서 1회 로그인 후 `naver_cookies.json`(기본 경로: `C:\Users\Administrator\Desktop\mindmap\cafe\naver_cookies.json`)에 `driver.get_cookies()` 결과 저장. 이후 세션은 이 파일로 쿠키 주입해 headless 재사용.
- `nid.naver.com/nidlogin.login` 접근 후 `cafe.naver.com`도 한 번 방문해 cafe 도메인 쿠키까지 포함시킴 (도메인 다르면 쿠키 별도 필요).
- **계정 스토리지**: `.naver_creds`(형식 `id:pw`, gitignore됨) 또는 환경변수 `NAVER_ID`/`NAVER_PW`. 일부 레거시 파일에는 계정이 하드코딩되어 있음 (login.py, join_cafe.py, save_cookies.py).
- **봇 감지 우회**:
  - `--disable-blink-features=AutomationControlled`
  - `excludeSwitches: ["enable-automation"]`
  - CDP `Page.addScriptToEvaluateOnNewDocument`로 `navigator.webdriver = undefined` 주입
  - 아이디/비번 입력은 `send_keys` 대신 **Windows clip 명령어 → Ctrl+V 붙여넣기** (키 입력 타이밍 기반 탐지 우회)
  - 붙여넣기 후 `input`/`change` 이벤트 JS로 dispatch (React/Vue reactive 우회)
- **캡차**: 자동 OCR 없음. `ss_captcha.png` 스크린샷 저장 → `answer.txt` 파일 폴링(2초 간격, 10분) → 사람이 답 쓰면 읽어서 입력. 최대 5회 재시도.

### 자동 가입 & 등급 업
- **등급 업 자동화 코드는 없음** (확인 필요 — 출석/활동 자동화 스크립트는 모듈에 미구현).
- **가입 자동화**(`join/join_cafe.py`, `batch_join.py`):
  - 카페 홈(`cafe.naver.com/{slug}`) 접근 → `a._rosRestrict` 선택자로 가입 버튼 감지. 없으면 이미 가입된 것으로 간주.
  - 네이버 카페 가입폼이 **iframe 내부**에 있어 Selenium `switch_to.frame` 만으론 불안정 → JS로 `iframe.contentDocument` 직접 순회하며 `#cafeNicknameInput`/`#captcha`/`#check_join_agree_once` 탐색해서 실제 폼 iframe 인덱스 확보.
  - 닉네임은 랜덤(`조사원{1000-9999}`), 약관 체크박스는 label이 가려져 있어 `execute_script("arguments[0].click();")` 로 강제 클릭.
  - 가입 질문(textarea) 있으면 고정 문구 "네 동의합니다. 안쓰겠습니다." 자동 입력.
  - 가입하기 버튼 클릭 직후 10회 루프로 `switch_to.alert` 폴링 → confirm 다이얼로그 자동 accept.
  - 가입 결과는 `cafe_join_log.json`에 slug별로 기록(`joined`/`already_joined`/`no_button`/`failed`)해서 재실행 시 스킵.

### 가입 캡차 처리 (특이 패턴)
- 가입폼 캡차는 로그인 캡차와 달리 **iframe 내부에서 `default_content` 전환 후 pyautogui 전체 화면 스크린샷** → 좌표 `(700,780,950,930)` 크롭 → `(750,450)` 리사이즈 → `captcha_{slug}.png` 저장 → answer.txt 대기 → iframe 재전환해 입력. (좌표는 1920x1200 창 기준, 해상도 바뀌면 재조정 필요)

### 크롤링 회피 전략
- **요청 간격 랜덤**: 페이지네이션 간 `time.sleep(1.0~1.5)`, 본문 읽기 간 `time.sleep(1.5~2.0)`, 카페 간 `time.sleep(random.randint(3,6))`.
- **UA rotation / 프록시 로테이션 없음** (확인 필요 — 단일 셀레니움 드라이버, 단일 IP).
- **중간 저장**: 5쿼리마다 JSON 덤프, 본문 50개마다 덤프 → 차단/크래시 시 증분 복구.
- **무한 빈 응답 방지**: 연속 3페이지 신규 0건이면 해당 쿼리 중단(`empty >= 3`).
- **쿼리 확장**: 시드 키워드 1개로부터 7카테고리(기본/시술/제품/후기비용/병원/연령/고민) × 접미사 매트릭스로 수십개 쿼리 자동 생성 → 동일 카페 반복 히트 줄이고 다양성 확보.

### 크롤링 타겟 & 셀렉터
- **카페 랭킹**: `https://section.cafe.naver.com/ca-fe/home/rankings` 에서 4개 카테고리(생활/패션·미용/건강·다이어트/가족·육아) × 전체 탭 × `ArticlePaginate` 페이지네이션. JS로 `ul.tab_list button.btn_tab` 텍스트 매칭해 탭 클릭. "나무등급 이상"만 크롤링 후보로 필터.
- **카페 내부 검색**: `cafe.naver.com/{cafe_id}?iframe_url=/ArticleSearchList.nhn%3Fsearch.query%3D{encoded}%26search.page%3D{n}%26search.sortBy%3Ddate` URL 패턴. `iframe[name='cafe_main']`로 전환 후 BS4 파싱.
- **게시글 리스트 셀렉터**(3단계 폴백): `.article-board tbody tr` → `#main-area table tbody tr` → `.board-list tbody tr`.
- **통합 검색 크롤링**(`posts/collect.py`): `search.naver.com/search.naver?where=article&query=...&start={1,11,21,...}&sort=0&nso=so:dd,p:all` — 10건씩 start 증가, 최대 1000건까지 페이지네이션.
- **본문/댓글 셀렉터**: `div.article_viewer` / `div.ArticleContentBox` / `.se-main-container` 중 최초 매칭. 댓글은 `li.CommentItem` 또는 `.comment_list li` (각 10~15개 제한).
- **상태 감지 문자열**: 페이지 텍스트 앞 500자에 `'멤버가 아닙니다'` → `need_join`, `'페이지를 찾을 수 없습니다'` → `not_found`, `'검색결과가 없습니다'` → `no_results`.

### 데이터 스키마
- **게시글**: `cafe_id`, `cafe_name`, `title`, `article_id`, `url`, `views`, `date`, `author`, `comment_count`, `preview`(검색결과 요약), `content`(본문 최대 3000자), `comments`(최대 10~15개, 각 200~300자), `query`(어떤 쿼리에서 발견됐는지).
- **저장 포맷**: `data/posts/posts_{title}.json` (배열, UTF-8, indent=2). 증분 수집 — `title` 기준 중복 제거 후 append.
- **카페 랭킹**: `data/rankings/cafes_{카테고리}.json`. 실제 디렉터리는 현재 비어 있으나 README 기준 카테고리별 150개.

### 리포트 생성 관점
- `analyze()` 함수에서 고정 키워드 사전 기반 Counter 집계: concerns(고민/증상), treatments(시술/치료), products(제품/성분), emotions(감정), questions(질문 패턴 — 추천/효과/가격/후기/병원), cafes(카페 분포).
- **감성분석 모델 없음** — 감정 단어 사전 매칭 방식(`스트레스/고민/만족/후회/실망` 등).
- 리포트는 MD 테이블로 상위 15개씩 덤프, 샘플 게시글 100개 표로 첨부.
- `analysis/video_plan.py` 는 페르소나 + 퍼포먼스 영상 기획을 생성 (세부 내부 확인 필요).

### 함정/제약
- **비밀번호 하드코딩**: `auth/login.py`, `auth/save_cookies.py`, `join/join_cafe.py`, `join/batch_join.py` 에 `mkm202601 / wnstjr66^^` 가 plaintext로 박혀 있음 → 유출 위험. `posts/collect.py`만 `.naver_creds`로 분리됨. **리팩토링 필요**.
- **계정 차단 트리거**: 가입/로그인 시 반복 캡차 실패, 짧은 간격 반복 가입, 동일 IP 다계정. batch_join은 카페 7개 순차 가입 — 하루에 몰아서 하면 차단 가능(확인 필요).
- **가입 실패 사유**: `a._rosRestrict` 없을 때, iframe 구조 변경, 캡차 답 오류, 알럿 타이밍 놓침, 가입 질문 답 거절.
- **수집 실패 카페 유형**: 멤버 전용 게시판(`need_join`), 등급 제한 게시판(준회원 차단), 삭제된 카페(`not_found`). 사전 가입 없으면 `search_in_cafe()`가 스킵.
- **iframe 종속성**: 네이버 카페는 SPA + 중첩 iframe → selenium 업데이트/네이버 리뉴얼에 매우 취약. 실제로 `_archive/scripts/` 에 26개 레거시 버전, `_archive/screenshots/` 에 98개 디버그 캡처가 쌓여 있음.
- **pyautogui 좌표 의존**: 캡차 크롭 좌표(700,780,950,930)는 1920x1200 창 전용. 창 크기 달라지면 캡차 인식 실패.
- **법적 회색지대**: 가입 후 개인정보(닉네임/게시글 작성자)를 JSON에 저장·분석. 상업적 이용 시 개인정보보호법/저작권 이슈 (확인 필요).
- **크롬 포커스 필수**: 클립보드 붙여넣기·캡차 크롭 시 크롬 창이 활성/최상단이어야 함 → 무인 서버에서 다른 창 뜨면 실패.

**출처:** C:\Users\Administrator\Desktop\market-research-package\modules\cafe\

## [2026-04-13] 재사용 가능한 크롤링·화면 자동화 패턴

cafe 모듈 실제 코드에서 추출한 "다른 프로젝트에서 바로 써먹을 수 있는" 패턴 모음.
각 항목은 **왜 → 언제 재사용 → 구현 포인트** 3단 구성.

### A. 캡차 Human-in-the-Loop (파일 폴링 IPC)
- **왜 이렇게 했는가**: 네이버 캡차는 OCR 정확도 낮고, 2Captcha 같은 외부 서비스는 비용·ToS·레이턴시 문제. 반자동 운영자 1인이 옆에서 답만 입력하는 구조가 가장 안정적.
- **어떤 상황에 재사용 가능한가**: 반자동 크롤러, 개인 운영 스크래퍼, QA/리서치 툴. 대용량·무인 서버 운영에는 **부적합**.
- **구체 구현 포인트** (cafe `auth/login.py` `wait_for_answer()`, `posts/collect.py` `wait_answer()`):
  - 브라우저 상태를 `driver.save_screenshot("ss_captcha.png")` 로 덤프
  - 답변 입력 파일 `answer.txt` 경로를 고정
  - **기존 `answer.txt` 가 있으면 먼저 삭제** 해서 이전 답이 오인 사용되는 것 방지
  - `for _ in range(300): time.sleep(2)` → **10분 타임아웃, 2초 폴링** (cafe 기본값)
  - 답 수신 시 즉시 파일 삭제 → 다음 캡차 라운드에 오염 없음
  - 운영자는 스크린샷 확인 → 답을 `answer.txt` 에 쓰기만 하면 됨 (에디터 저장 한 번)
- **제약**: 무인 서버 불가, 운영자 화면 접근 필요, 창 포커스 유지 전제.

### B. 다중 중첩 iframe 우회 (JS contentDocument 순회로 인덱스 역추적)
- **왜 이렇게 했는가**: 네이버 카페는 SPA + 다중 중첩 iframe. Selenium `switch_to.frame(index)` 로 들어가려 해도 **타겟 셀렉터가 몇 번째 iframe 안에 있는지 런타임마다 다름**. 하드코딩 인덱스는 리뉴얼 즉시 깨짐.
- **어떤 상황에 재사용 가능한가**: iframe 기반 레거시 UI, 네이버/다음 카페·블로그 가입폼, 일부 은행/공공기관 포털, 광고 플랫폼 대시보드 내 위젯.
- **구체 구현 포인트** (cafe `join/join_cafe.py` `join_via_js()` 실제 스니펫):
  1. `driver.execute_script` 로 브라우저 쪽에서 모든 `<iframe>` 순회
  2. 각 iframe의 `contentDocument || contentWindow.document` 접근 (same-origin 이어야 동작; cross-origin 이면 `try/catch` 로 조용히 스킵)
  3. 타겟 셀렉터(예: `#cafeNicknameInput`, `#captcha`, `#check_join_agree_once`)가 있는 iframe 의 **index** 를 리턴
  4. Python 쪽에서 `driver.switch_to.frame(frames[iframe_idx])` 로 전환 후 Selenium 네이티브 API 로 조작
- **실제 코드 주석/시그니처 원문 (그대로 인용)**:
  - 파일 헤더 주석: `"""카페 가입 - JS contentDocument로 iframe 내부 직접 접근 + pyautogui 좌표 클릭 폴백"""`
  - 함수 시그니처: `def join_via_js(d, slug, name):` / 내부 주석 `"""JS contentDocument로 iframe 내부 직접 조작"""`
  - JS 블록 요지:
    ```js
    var iframes = document.querySelectorAll('iframe');
    for (var i = 0; i < iframes.length; i++) {
      try {
        var doc = iframes[i].contentDocument || iframes[i].contentWindow.document;
        if (doc.querySelector('#cafeNicknameInput')) return { iframe_index: i, ... };
      } catch(e) {}  // cross-origin 은 무시
    }
    ```
- **보조 패턴**: 전환 후에도 약관 체크박스가 `label` 에 가려져 Selenium click 이 안 먹으면 `driver.execute_script("arguments[0].click();", cb)` 로 우회 (cafe 에서 실제로 쓰임).

### C. 레거시 시행착오 코드 26개 유지 — 삭제하지 말고 아카이브
- **왜 이렇게 했는가**: 카페 가입 iframe 구조 알아내기까지 26개 버전을 거쳤고, 스크린샷 98장이 그 과정의 디버그 로그. iframe 셀렉터·인덱스·캡차 좌표는 외부 사이트가 리뉴얼될 때마다 **회귀**. 이전 시도의 흔적이 있으면 "어떤 접근을 이미 시도했다가 왜 실패했는가" 를 재학습 없이 확인 가능.
- **어떤 상황에 재사용 가능한가**: 안정화 안 된 외부 사이트 대응 프로젝트 전반 (네이버·다음·쿠팡·틱톡샵 UI 자동화). 사이트가 자주 리뉴얼되고 내부 담당자가 적을수록 효과 큼.
- **구체 구현 포인트**:
  - `_archive/scripts/` 디렉토리에 **버전별 스크립트 보존** (파일명 접미사로 시도 번호)
  - `_archive/screenshots/` 에 각 시도의 실패 스크린샷 보존
  - README 에 "구 버전 스크립트 N개 있음" 명시해서 후임이 이 존재를 알 수 있도록
- **교훈**: "돌아가는 코드만 남기고 나머지 날리기" 는 안정된 내부 도메인에서만 통한다. **외부 의존 자동화는 실패 이력이 자산**.

### D. 안티패턴 체크리스트 (이 모듈에서 실제로 발견된 "배포 불가" 신호)
- **하드코딩된 크레덴셜**: `auth/login.py`, `auth/save_cookies.py`, `join/join_cafe.py`, `join/batch_join.py` 4개 파일에 `mkm202601 / wnstjr66^^` plaintext. `posts/collect.py` 만 `.naver_creds` 로 분리되어 있음 → **부분 리팩터가 제일 위험**, 일관성 없음이 유출 경로가 됨.
- **픽셀 좌표 의존**: `pyautogui.screenshot().crop((700, 780, 950, 930))` 는 **1920x1200 크롬 창 전용**. 해상도/창 크기 다르면 캡차 이미지 영역 완전히 벗어남. 대안: iframe 내부 캡차 `<img>` 요소의 `getBoundingClientRect()` 를 JS 로 얻어 좌표 계산.
- **단일 계정·단일 IP 장기 운영**: batch_join 이 카페 7개를 순차 가입. 하루에 몰아서 하면 계정·IP 동시 플래그. 프록시 로테이션/계정 풀 없음.
- **창 포커스 필수**: 클립보드 `Ctrl+V` 붙여넣기와 `pyautogui` 크롭은 **크롬 창이 활성/최상단이어야** 동작. 서버에서 다른 창이 뜨거나 RDP 세션 잠기면 즉시 실패.
- **"작동은 하지만 배포 불가"의 정확한 정의**: 위 4개 중 **하나라도 해당**되면 1인 반자동 운영 한정, 팀 배포·무인 서버·고객 대행 중 **어디에도 못 올린다**. 리팩터링 체크리스트로 그대로 사용 가능.

### E. Rate limit / sleep 패턴 (cafe 모듈 실측값)
- **로그인 직후**: `time.sleep(3~4)` (리다이렉트 + 캡차 감지 여유)
- **페이지 이동 후 파싱 전**: `time.sleep(2 ~ 2.5)` (iframe 로딩)
- **가입 버튼 클릭 후 폼 로드 대기**: `time.sleep(5 ~ 8)`
- **게시글 목록 페이지네이션 간격**: `time.sleep(1)` — cafe 내부 검색
- **통합검색 페이지네이션**: `time.sleep(1.2)` — deprecated 되었지만 값은 기록 가치 있음
- **본문 읽기 간 간격**: `time.sleep(1.5)` (로그인된 세션 내)
- **카페 간 대기**: `time.sleep(random.randint(3, 6))` (batch_join)
- **User-Agent 로테이션**: **없음** (Chrome 기본 UA 그대로) — `--disable-blink-features=AutomationControlled` 와 `excludeSwitches=["enable-automation"]`, `navigator.webdriver=undefined` CDP 인젝션 3개 조합으로 봇 감지 우회
- **프록시**: **없음** (단일 IP)
- **재사용 시 기준값**: 네이버 계열은 위 값으로 수 시간 돌아감. 더 공격적 사이트(쿠팡·배민 등)는 여기에 ×2 ~ ×3 해서 시작 권장 (확인 필요).

### F. 출력 저장 스키마
- **디렉토리 구조** (재사용 권장):
  ```
  module/
    src/          # 실행 코드 (역할별 하위 폴더: auth/ posts/ join/ analysis/ rankings/)
    data/         # 수집 원천 JSON (raw/ 와 정제본 분리)
      raw/        # 원본 HTML
      posts/      # posts_{title}.json 네이밍
      rankings/   # cafes_{카테고리}.json
    reports/      # MD 리포트 (사람이 읽는 결과물)
    _archive/     # 구 버전 스크립트 + 디버그 스크린샷
  ```
- **JSON 레코드 스키마** (게시글, cafe 실측):
  - 필수: `title`, `url`, `cafe_id` 또는 `cafe_name`
  - 선택: `article_id`, `views`, `date`, `author`, `comment_count`, `content`(3000자 cap), `comments`(상위 10~15개, 각 200~300자 cap), `query`, `preview`(300자 cap)
  - **증분 수집 패턴**: 실행 시마다 `existing = json.load(out_path)` → `seen = {p['title'] for p in existing}` → 새 것만 append → 5쿼리마다 중간 저장. **제목 기준 dedup** 은 단순하지만 다른 카페에 같은 제목이 있으면 오탐 가능 (확인 필요 — `(cafe_id, article_id)` 튜플 키가 더 안전).
- **리포트 포맷**: MD 테이블 기반. 상위 15개 키워드 덤프 × 카테고리별 섹션 + 샘플 게시글 100개 표. 그대로 공통 스키마로 차용 가능.

**재사용 체크리스트**: 새 사이트 자동화 시작할 때 A→B→D→E→F 순으로 먼저 설계하면 초기 시행착오 대부분 스킵됨. C 는 운영 돌리면서 자연스럽게 쌓임.

**출처:** `C:\Users\Administrator\Desktop\market-research-package\modules\cafe\` (2026-04-13 기준 `src/auth/login.py`, `src/posts/collect.py` → deprecated, `src/join/join_cafe.py`, `src/join/batch_join.py`)
