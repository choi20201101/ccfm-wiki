---
aliases: ["인스타그램 콘텐츠 리서치", "IG 게시물 수집", "인스타 벤치마킹"]
type: domain
domain: marketing-automation
confidence: high
created: 2026-05-12
updated: 2026-05-12
sources:
  - src-instagram-content-research-picosera-2026-05-12
---

# 인스타그램 콘텐츠 리서치 (Instagram Content Research Playbook)

> **🔥 글로벌 지식**: 사용자가 "인스타 계정 N개 게시물 좋아요 X개 이상 가져와서 콘텐츠 아이디어로 정리" 류를 요청하면 **반드시 이 파일 구조대로 진행**.
>
> 참조 성공사례: [[src-instagram-content-research-picosera-2026-05-12]] — 피코쎄라 8계정 리서치 (humor__.cok, zzal_zzal_zzal 등)
>
> 핵심 아키텍처: **2-단계 파이프라인** (메타 스크랩 → 미디어 추출) + **카드뉴스 슬라이드 전수 다운로드** + **게시물 폴더당 idea.md 동봉**

---

## 0️⃣ 입력 수집 단계 (건너뛰지 말 것)

사용자에게 반드시 확인:

1. **계정 URL 리스트** (`ink.txt`) — `https://www.instagram.com/<id>/` 한 줄당 하나
2. **좋아요 임계치** (`MIN_LIKES`, 기본 500)
3. **계정당 최대 수집 게시물** (`MAX_POSTS`, 기본 150)
4. **브랜드/맥락** — 추출된 아이디어를 어떤 브랜드 톤으로 재해석할지 (예: 피코쎄라 = 클린/뷰티)

---

## 1️⃣ 환경

```bash
python --version    # 3.11+
pip install instaloader instagrapi requests
# ffmpeg 필수 (영상 장면 추출):  https://www.gyan.dev/ffmpeg/builds/
ffmpeg -version
```

### 1.1 인스타 세션 (선택, 권장)

`instagrapi` 세션 캐시가 있으면 메타 스크랩 속도가 훨씬 안정적.

```text
C:/Users/gguy/Desktop/instarup/state/sessions/<account>.json
```

세션이 **챌린지 걸린 상태**면 사용 불가 → `sess_check.py`로 사전 검증 필수.

### 1.2 IP 차단(429) 대응 — 항상 발생한다

- 익명 `instaloader.Profile.from_username` → 분당 1~3회 호출만 가능
- 30분 차단 → 1시간 차단 → 영구 차단(이 IP에서 며칠) 순으로 증폭
- **해법**: 세션 회전 + 게시물당 3~6분 sleep + 15개마다 10~20분 휴식

---

## 2️⃣ 디렉토리 구조 (산출물)

```
<project>/
├ ink.txt                 # 입력: 계정 URL 리스트
├ data/
│  └ <username>.jsonl     # 메타데이터 (재실행 시 dedup, append-only)
├ analyzed/
│  └ <username>/<code>/
│     ├ slide_01.jpg ... slide_20.jpg   (카드뉴스 슬라이드 전체)
│     ├ frame_001.jpg ... frame_012.jpg (영상 장면 추출)
│     ├ image.jpg                       (단일 이미지)
│     ├ cover.jpg                       (영상 커버)
│     ├ meta.json                       (게시물 메타 + extracted info)
│     └ idea.md                         (1장 이미지 아이디어 카드)
├ ideas/
│  ├ INDEX.md             # TOP 100 인덱스
│  ├ all_ideas.jsonl      # 머신 리더블
│  └ <username>/<code>.md # 평면 복사본
├ report.md               # 1차 카테고리/해시태그 분석
├ top_posts.jsonl         # ≥MIN_LIKES 필터링된 원본
├ FINAL_REPORT.md         # TOP 50 아이디어 종합
└ logs/                   # 모든 stage별 실행 로그
```

**핵심 결정**: 각 게시물의 슬라이드/프레임/메타/아이디어 카드를 **한 폴더**에 묶어둔다.

---

## 3️⃣ 파이프라인 단계

### Stage 1 — 메타 스크랩 (`scrape2.py` / `scrape_anon.py`)

`scrape2.py` (instagrapi, 로그인 세션 사용):
- `cl.user_info_by_username_v1(username)` → uid
- `cl.user_medias_paginated_v1(uid, 33, end_cursor)` 페이지네이션
- 챌린지 발생 시 다른 세션으로 회전

`scrape_anon.py` (instaloader 익명, 폴백):
- `instaloader.Profile.from_username` + `profile.get_posts()`
- 익명 모드는 429 매우 잘 걸림 — 백업용으로만 사용

**저장 필드**: `username, pk, code, url, date, likes, comments, media_type, product_type, view_count, caption, hashtags`

`media_type`: 1=단일이미지, 2=영상, 8=카드뉴스(carousel)
`product_type`: `feed`/`clips`(릴스)/`carousel_container`

### Stage 2 — 1차 분석 (`analyze.py`)

- `data/*.jsonl` 전체 로드 → `MIN_LIKES` 필터 → `top_posts.jsonl` 생성
- 카테고리 자동 태깅 (감정·주제·해시태그)
- `report.md`: TOP 30 게시물, 카테고리별 인사이트, 후킹 카피 TOP 50, 해시태그 TOP 30

### Stage 3 — 미디어 추출 (`extract2.py`)

**핵심**: 익명 `Post.from_shortcode` 사용 — Profile 엔드포인트는 막혀도 Post 엔드포인트는 자주 살아있다.

```python
post = instaloader.Post.from_shortcode(L.context, code)
if post.typename == "GraphSidecar":
    for n in post.get_sidecar_nodes(): ...  # 모든 슬라이드
elif post.is_video:
    video_url = post.video_url             # 영상 파일
else:
    display_url = post.url                 # 단일 이미지
```

영상 장면 추출 (ffmpeg):
```bash
ffmpeg -i video.mp4 -vf "select='gt(scene,0.30)',scale=720:-2" -vsync vfr frame_%03d.jpg
```
scene cut이 없으면 균등 간격 폴백, MAX_FRAMES(기본 12) 초과 시 균등 솎아내기.

**페이스 (차단 방지)**:
- `SLEEP_MIN=180, SLEEP_MAX=360` (게시물당 3~6분)
- 15개마다 10~20분 휴식 (`time.sleep(random.uniform(600, 1200))`)
- 99개 추출 = 약 6~8시간

### Stage 4 — 아이디어 생성 (`ideate.py`)

각 `analyzed/<u>/<code>/meta.json` → `idea.md` 생성:

- **카드뉴스 흐름 분석**: caption 단락 → 슬라이드 N개에 매핑
- **영상 장면 narrative**: frame_count로 클라이맥스 추정
- **1장 이미지 컨셉**: 후킹 카피 + 흐름 압축 → 단일 이미지 변환 지시
- **태깅**: 감정(공감/위로/분노/유머/감동/충격/꿀팁) × 주제(연애/직장/가족/외모/음식/동물/MZ/돈/건강)

게시물 폴더(`analyzed/<u>/<code>/`)에 `idea.md`로 동봉 → 슬라이드 이미지와 함께 한 곳에서 확인.

### Stage 5 — 종합 리포트 (`FINAL_REPORT.md`)

TOP 50 아이디어 (engagement_score = likes + comments × 5 기준 정렬)
- 계정별 통계 테이블
- 종류별 분포 (카드뉴스/영상/단일)
- 각 아이디어: 후킹, 감정·주제 태그, 1장 컨셉, 링크, 폴더 경로

---

## 4️⃣ 오케스트레이션 (`overnight2.py` / `finish.py`)

- `overnight2.py`: 처음부터 끝까지 (스크랩→분석→추출→아이디어→리포트)
- `finish.py`: 스크랩 끝났다고 가정하고 추출→아이디어→리포트만
- 모두 **resumable**: dedup·skip-if-exists. 끊겼다 재실행 OK.
- 백그라운드 실행: `Start-Process python -ArgumentList "-u","overnight2.py" -RedirectStandardOutput "logs/overnight2.log"`

---

## 5️⃣ 함정 (이 프로젝트에서 실제로 발생)

1. **세션이 모두 챌린지** — 4개 부계정 모두 동시에 `ChallengeUnknownStep` 발생. `sess_check.py`로 사전 필터 필수.
2. **익명 Profile 엔드포인트 즉시 429** — 첫 요청부터 30분 락. 5개 계정 스크랩 실패.
3. **Post 엔드포인트는 더 관대** — Profile 막혀도 `Post.from_shortcode`는 403 retry로 작동. Stage 3는 보통 가능.
4. **카드뉴스가 압도적** — 한국 humor 계정 ≥500 좋아요 게시물의 80%+가 carousel. 캡션만으론 부족, 슬라이드 전체 다운로드 필수.
5. **head | pipe 죽이기** — `python script.py | head -20`은 SIGPIPE로 백그라운드 프로세스를 종료시킴. 반드시 `> log.txt 2>&1 &`로 분리.
6. **Windows에서 nohup/&** — 권장 X. `Start-Process ... -WindowStyle Hidden -RedirectStandardOutput` 사용.

---

## 6️⃣ 빠른 시작

```bash
# 1) 환경
pip install instaloader instagrapi requests

# 2) 입력
echo "https://www.instagram.com/humor__.cok/" > ink.txt
echo "https://www.instagram.com/zzal_zzal_zzal/" >> ink.txt

# 3) 풀 파이프라인 (resumable)
python -u overnight2.py > logs/overnight2.log 2>&1 &

# 4) 진행 확인
ls analyzed/*/*/idea.md | wc -l
cat FINAL_REPORT.md
```

---

## 7️⃣ 산출물 검증 체크리스트

- [ ] `data/*.jsonl` — 계정별 메타 라인 수 ≥ TARGET_POSTS × 0.6
- [ ] `top_posts.jsonl` — 좋아요 ≥ MIN_LIKES 라인만
- [ ] `analyzed/<u>/<code>/meta.json` — 모든 ≥MIN_LIKES 게시물에 존재
- [ ] 카드뉴스 폴더에 `slide_01.jpg ~ slide_NN.jpg` (NN = meta.json의 slide_count)
- [ ] 영상 폴더에 `frame_*.jpg` 또는 `cover.jpg`
- [ ] 각 폴더에 `idea.md` 동봉
- [ ] `ideas/INDEX.md`, `FINAL_REPORT.md` 생성됨

---

## 8️⃣ 관련 위키

- [[market-research-playbook]] — 카테고리·시장 단위 조사 (인스타는 채널 단위)
- [[viral]] — 바이럴 콘텐츠 패턴 분석
- [[content-ai-automation]] — 추출된 아이디어를 실제 소재로 변환
- [[ggttt-imagen]] — 1장 이미지 아이디어 → 실제 배너 생성
