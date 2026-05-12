---
aliases: ["오늘의유머 광고 소재 마이닝", "오유 마이닝", "humor mining"]
type: playbook
domain: marketing-automation
confidence: high
created: 2026-05-12
updated: 2026-05-12
sources:
  - "C:/Users/gguy/Desktop/gpt/projects/picosera/new/todayhumor_ideas/"
  - "[[domains/marketing-automation]]"
  - "[[domains/da-creative]]"
  - "[[tacit/coding-lessons]]"
related:
  - "[[domains/marketing-automation]]"
  - "[[domains/da-creative]]"
  - "[[concepts/picosera-ad-canvas]]"
---

# 오늘의유머 → 광고 소재 마이닝 플레이북

> 한국 커뮤니티(오늘의유머 Best of Best)의 추천 N+ 게시물에서 위트 코드를 추출 → 자사 브랜드 광고 아이디어(레이아웃 + Imagen 프롬프트 + 카피 5종)로 1:1 변환하는 자동 파이프라인.
> 2026-05-11 피코세라 사례에서 실전 검증 (614/1469 진행 중단 시점, brand_fit=high 519/614 = 84.5%).

## 🚀 빠른 호출 (Trigger)
- "오늘의유머에서 [브랜드] 광고 소재 마이닝해줘"
- "추천 N+ 게시물에서 N개 아이디어 추출"
- "humor mining" / "오유 마이닝" / "커뮤니티 위트 → 광고"

호출 시 곧장 본 페이지의 §실행 절차로 진입. 사전 질문 2개만:
1. 대상 브랜드 + 브랜드 톤 참고 파일 (예: `광고 카피 100선.md`)
2. 목표 아이디어 개수 + 최소 추천수 (기본: 10+)

---

## 파이프라인 개요

```
오늘의유머 Best of Best 리스트
        │
        ▼ (1) crawl_index.py — 추천수 N+ 필터 + 브랜드 하드드롭
posts_index.json (~30개/페이지, 150p → ~2700 후보)
        │
        ▼ (2) run.py — workers=3 병렬, _state.json 재개 가능
generate.py per post:
   ├─ fetch_post() : 본문 + 이미지 URL 추출
   ├─ download_image() : ideas/NNNN_{slug}/src_NN.{jpg,png}
   ├─ call_gemini()    : SDK 직접 호출 (CLI 회피)
   │     └─ Picosera 브랜드 보이스 + 후킹 패턴 A~F 강제 주입
   └─ write_idea()     : ideas/NNNN_{slug}/idea.md
        │
        ▼ (3) status.py / _progress.log
brand_fit 분포 · humor_axis 통계 · 실패 패턴
        │
        ▼ (4) eval/큐레이션 → Imagen 일괄 생성
```

### 산출물 폴더 구조 (게시물 1개 = 폴더 1개 = 아이디어 1개)
```
todayhumor_ideas/
├── INDEX.md
├── RESUME_TOMORROW.md       ← 재개/스케줄 안내
├── posts_index.json         ← 후보 마스터
├── _state.json              ← done/failed/next_idx (재개 가능)
├── _progress.log            ← 실시간 진행 로그
├── _scripts/
│   ├── crawl_index.py
│   ├── generate.py
│   ├── run.py
│   ├── status.py
│   └── resume_tomorrow.bat  ← schtasks용 wrapper
└── ideas/
    ├── 0001_{slug}/         ← idea.md + src_NN.{jpg,png}(+gen_*.png)
    ├── 0002_{slug}/
    └── ...
```

---

## 컴포넌트 디테일

### (1) crawl_index.py — 인덱스 빌더
**셀렉터** (오늘의유머 Best of Best 행 정확 매칭):
```python
for tr in soup.select("tr.list_tr_humordata"):
    sub   = tr.select_one("td.subject a")
    no_a  = tr.select_one("td.no a")
    hits  = tr.select_one("td.hits")    # 조회수
    oknok = tr.select_one("td.oknok")   # 추천수
```
⚠️ **함정 — 한 행에 view.php 앵커가 여러 개** (번호 셀 / 제목 셀 / 댓글 셀). `soup.select('a[href*=view.php]')` 같이 전역 셀렉하면 번호 셀의 숫자 텍스트를 제목으로 잡아버림. 반드시 `td.subject a`로 좁힐 것.

⚠️ **인코딩** — 응답 헤더 charset이 비어 있으면 `r.encoding = r.apparent_encoding or "utf-8"` 보정 필수. 안 하면 한글이 mojibake로 들어와 필터 정규식이 전부 빗나감.

⚠️ **콘솔 출력 mojibake** ≠ JSON 내용 mojibake. JSON은 `ensure_ascii=False`로 UTF-8 저장됨. 검증은 `python -c "import io,sys,json; sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8'); ..."`.

**브랜드 하드드롭 패턴** (피코세라 톤 기준, 다른 브랜드는 조정):
```python
HARD_DROP_PATTERNS = [
    r"김건희|윤석열|이재명|문재인|박근혜|이명박|대통령|국회의원|판사|검사|검찰|민주당|국민의힘|선거|정당|탄핵|법무부|장관",
    r"살인|강간|성폭|성범죄|폭행|추락사|사망|죽음|자살|마약|도박|사기|아동학대|학대|음주운전",
    r"산불|화재|지진|참사|사고로|피습|총격|테러",
    r"혐오|차별|일베|페미|메갈",
    r"성인|야동|섹스|유흥",
]
```
60페이지 기준 약 21% 드롭 → 약 79% 후보 통과 (페이지당 22~28건). 페이지 150 크롤 시 약 2700~2800 후보.

### (2) generate.py — 게시물별 처리
**핵심 함수 4개**:
- `fetch_post(no)` : `#viewContent, .view_content, .viewContent, .smtRefresh, #memoContent` 셀렉터 다중 시도, 본문 div 안의 `<img>`만 추출 (사이드바·관련글 제외)
- `download_image(url, dest)` : Referer/UA 설정 (없으면 403 또는 깨진 이미지)
- `call_gemini(images, title, body)` : ⭐ Gemini SDK 직접 호출 (§Gemini CLI 함정 참조)
- `write_idea(idx, post, slug, srcs, body_md)` : frontmatter + 본문 일관 포맷

**제목 출처 — 리스트 크롤이 정답**:
view 페이지에는 사이드바/관련글 링크가 많아 `h1`/`.subject`/`.view_title` 셀렉터 어느 것을 잡아도 다른 게시물 제목이 섞일 수 있다. 따라서 **list crawl에서 추출한 title을 그대로 사용**하고 view 페이지 title은 무시한다 (`if post.get("title"): full["title"] = post["title"]`).

### (3) run.py — 오케스트레이터
```bash
python _scripts/run.py --target 1000 --workers 3 --max-retries 2
```
- `ThreadPoolExecutor` 3 워커 = 처리 속도 ~7~8개/분 (병목: Gemini API)
- `_state.json` 자동 저장 → 어디서 중단해도 같은 명령으로 재개
- `failed`에 retry 카운트 별도 기록, `max-retries` 초과 시 영구 스킵
- `target` = 누적 done 개수 — 어제 469 + 오늘 1000 더 처리하려면 `--target 1469`

### (4) status.py — 한눈에 통계
```bash
python _scripts/status.py
```
- 총 done / failed
- brand_fit 분포 (high/med/low)
- humor_axis TOP 10
- 최근 실패 5건

---

## ⭐ 프롬프트 엔지니어링 — 가장 중요한 부분

### 브랜드 보이스 주입 (피코세라 케이스)
프롬프트 상단에 다음 3블록을 **하드코딩**:

1. **브랜드 팩트시트** — 운영사·제품·가격·임상 수치·타깃 페르소나·톤
2. **필수 후킹 패턴 A~F** — 카피 5종 작성 시 최소 1개 차용 강제
3. **금지 표현 리스트** — 식약처/표시광고법 위반 자동 회피

피코세라 패턴 A~F:
| 라벨 | 패턴 | 예시 |
|------|------|------|
| **A** | 시간/비용 비교 | "피부과 5회 시술비 vs 9만 9천원, 매일 쓰면 답 나옴" |
| **B** | 생활 페인 직격 | "출산 후 안 빠지는 기미", "마스크 벗으니 톤 두 단계" |
| **C** | 충동/반신반의 → 전환 | "충동구매였는데 환불 못 하게 된 이유" |
| **D** | 숫자 임상 | "1조 분의 1초", "+73.93% 윤기", "84g" |
| **E** | 후기 인용형 | "거울 볼 때마다 옅어진 게 보여요" |
| **F** | 페르소나 직격 | "워킹맘 화장대에 올라온 단 하나" |

각 카피 5종 끝에 `[A]~[F]` 라벨 자동 부여 → 사후 분석/A·B 테스트 쉬움.

### 원본 베스트 카피 반영
프롬프트에 명시:
> "첨부 이미지/본문에서 가장 임팩트 있는 표현(시그니처 문장·대사·반전 포인트·핵심 단어)을 추출해, 그 표현의 구조나 단어를 변주해서 광고 카피로 사용한다. 그래야 원본 유머가 광고에 살아남는다."

또한 `## 원본 장면` 섹션에 `- 시그니처 표현 추출: {{원본에서 임팩트 가장 큰 문장/대사/단어 1~2개 — 그대로 인용}}` 필드 추가 → 카피 생성 시 강제로 참조하게 됨.

### 출력 안정화
- **첫 줄 명령형**: `RESPONSE FORMAT: Output ONLY the markdown template below with EVERY placeholder replaced. NO PREAMBLE. NO POSTAMBLE.`
- **placeholder 형식**: `{{내용 지시}}` (반각 중괄호 2개) — 모델이 hint text를 그대로 출력하는 사고를 줄임
- **golden constraint**: "Do NOT echo placeholder hint text in parentheses or square brackets — replace them entirely"
- 그래도 가끔 placeholder 그대로 남기는 경우 발생 → 후처리 검사 또는 재시도 권장

---

## ⚠️ Gemini CLI vs SDK — 결정적 교훈

**결론: 자동화 파이프라인은 Python SDK (`google.genai`) 직호출이 정답. CLI(`gemini` 명령) 쓰지 말 것.**

### CLI의 함정
1. **에이전트 모드 진입**: CLI는 사용자를 "도우려는" 에이전트로 동작 → 템플릿 무시하고 "이미지를 정리해 드립니다", "파일을 생성하시겠어요?" 같은 채팅 응답을 냄
2. **--approval-mode plan + 강력한 영어 명령형 프롬프트**로 bash 직접 호출에선 됐지만 `subprocess.run([gemini.cmd, ...])`로 호출 시 또 다른 결과
3. **CWD 의존**: 폴더에 `idea.md`가 이미 있으면 "이미 했네" 판단 → 빈/엉뚱한 응답
4. **Windows .cmd shim**: subprocess shell quoting/escape 문제로 동일 prompt가 bash↔python 사이에서 다르게 동작
5. **출력 인코딩**: `--output-format text`로도 mojibake 발생 케이스 있음

### SDK 호출 패턴 (안정)
```python
from google import genai
from google.genai import types

client = genai.Client()  # GEMINI_API_KEY 환경변수
parts = [prompt]
for p in image_paths:
    parts.append(types.Part.from_bytes(
        data=p.read_bytes(),
        mime_type=mimetypes.guess_type(p.name)[0] or "image/jpeg"
    ))
resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=parts,
    config=types.GenerateContentConfig(
        temperature=0.9, top_p=0.92, max_output_tokens=4800
    ),
)
return resp.text.strip()
```
- 모델: `gemini-2.5-flash` (속도/품질 균형)
- max_output_tokens: 4800 (2400은 6섹션 템플릿에 부족 — 중간에 잘림)
- temperature 0.9 / top_p 0.92 (위트 다양성 확보)

→ 일반화: **Vision + 구조화 출력 = SDK 직호출**. 관련 교훈은 [[tacit/coding-lessons]] §Gemini CLI 함정에 cross-post.

---

## 실패 패턴 및 대처

| 실패 reason | 비율 (1473건 중) | 원인 | 대처 |
|-------------|-----------------|------|------|
| `no_images` | ~5% | 텍스트-only 게시물 | **fallback: 본문 80자+ 있으면 텍스트만으로 SDK 호출, `src_body.txt`로 저장** |
| `gemini:empty response` | ~3% | 안전 필터 또는 일시 장애 | retry (max-retries 2). 지속 시 hard-drop 키워드 미스 케이스 의심 |
| `gemini:503 UNAVAILABLE` | <1% | API 일시 장애 | 자동 retry로 흡수 |
| `no_images_no_text` | <1% | 본문이 너무 짧음 | 영구 스킵 |

전체 처리 성공률: **~93%** (60p 인덱스, 469/525 = 89% 첫 패스 + retry 후 회복분 포함).

---

## 운영 노하우 (실전 함정)

### Windows + Git Bash 백그라운드 실행
- ❌ `nohup python ... &` 는 Git Bash에서 자주 즉시 종료 (exit code 2). nohup이 PATH에 없거나 동작 안 함
- ✅ **schtasks 1회 발화로 .bat 실행**:
  ```cmd
  cmd.exe /c "schtasks /Create /TN PicoseraResume /SC ONCE /SD 2026/05/12 /ST 09:00 /TR \"C:\path\to\resume.bat\" /F"
  ```
  Git Bash에서 직접 `schtasks /Create`는 `/F` 등을 path로 해석해 실패 → `cmd.exe /c` 래퍼 필수
- ✅ **수동 실행 시 foreground**가 가장 안정. 5~10분 작업이면 그냥 전경 실행

### 모니터링 — `_progress.log` + Monitor 도구
```bash
tail -F _progress.log | awk '
/OK  #/ { ok++; if (ok % 25 == 0) { print; fflush(); }
          if ($0 ~ /\(1000\/1000\)/) { print "FINAL: " $0; fflush(); exit; } }
/FAIL #|reached target|done\. total/ { print; fflush(); }'
```
- 25개마다 OK + 모든 FAIL + 종료 시그널만 emit → Monitor 알림 노이즈 최소화
- Monitor 1시간 타임아웃 시 재무장 (`-n0`로 신규 라인만)

### 인덱스 확장 전략
- 페이지 1~60: 추천 51~118 (최근, 가장 신선)
- 페이지 61~150: 추천 10~50 (오래된 + 추천 적음, 양으로 보완)
- 더 풍부한 후보 필요 시 페이지 200+ 또는 `humordata` 일반 게시판도 추가 (`table=humordata` 동일 코드 흐름)

### 폴더 매칭 원칙
**1 폴더 = 1 게시물 = 1 아이디어 = 모든 산출물**. 이미지·MD·생성시안 분리하지 말 것. 1000개 스케일에서 폴더 분리는 매칭 어그러짐.

---

## 결과 활용 (다음 단계)

1. **/eval 큐레이션**: `brand_fit=high` & `humor_axis ≠ 반전` 위주(다양성 확보) 상위 100개 골라 광고 운영팀에 전달
2. **Imagen 일괄 생성**: 각 폴더의 `## 이미지 생성 프롬프트` 섹션 추출 → `gen_*.png`로 같은 폴더에 떨어뜨림
3. **A/B 테스트 묶음**: 카피 5종의 라벨([A]~[F])별로 광고 그룹화 → 어떤 후킹 패턴이 CTR 우위인지 학습
4. **위트축 분포 관리**: TOP1 축(반전)이 50%+ 차지하면 다양성 부족 → 프롬프트의 `humor_axis` 후보 단어 셔플 또는 명시적 분산 지시 추가

---

## 핵심 산출물 위치 (피코세라 사례)
- 워크스페이스: `C:/Users/gguy/Desktop/gpt/projects/picosera/new/todayhumor_ideas/`
- 진행 상태: 614/1469 (중단 시점)
- brand_fit: high 519 / med 25 / low 69 (전체 84.5% high)
- humor_axis TOP: 반전(272), 공감(66), 의외성(61), 과몰입(52), 능청(42), 정성(24), 집착(13), 디스(11)

## 재사용 체크리스트 (새 브랜드 적용 시)
- [ ] 브랜드 팩트시트 작성 (운영사·제품·가격·임상·페르소나·톤)
- [ ] 후킹 패턴 A~F 정의 (기존 광고 카피 ≥30개 분석에서 추출)
- [ ] 금지 표현 리스트 (해당 카테고리 표시광고 규제)
- [ ] hard-drop 패턴 조정 (브랜드 카테고리에 맞게 — 예: 뷰티는 정치/사건 드롭, B2B는 가십/연예 드롭)
- [ ] `generate.py`의 `GEMINI_PROMPT_TEMPLATE` 상단 3블록만 교체
- [ ] 파일럿 3~5개로 톤 검증 → 본 가동
