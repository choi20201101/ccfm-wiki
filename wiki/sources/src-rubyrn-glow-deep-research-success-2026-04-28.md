---
type: source
domain: marketing-automation
confidence: high
created: 2026-04-28
updated: 2026-04-28
sources:
  - C:/Users/gguy/Desktop/naver-competitor-finder/canvas/04_glow_keyword_research.md
  - C:/Users/gguy/Desktop/naver-competitor-finder/canvas/05_viral_video_deep_analysis.md
  - C:/Users/gguy/Desktop/naver-competitor-finder/canvas/06_folk_beliefs_for_glow.md
  - C:/Users/gguy/Desktop/bol/output/raw/
  - C:/Users/gguy/Desktop/naver-competitor-finder/scripts/video_deep/
---

# 🏆 성공사례: 루비알엔 광채 클렌저 시장조사 4단 심화 (2026-04-28)

> 단일 세션 (3시간) 안에 검색 → 발화 → 영상 자막+썸네일 → 민간 속설 4단계 모두 1차 자료로 수집 완료.
> 사용자 승인: "이 정도 이상으로 시장조사 바로 될 수 있게 해줘" (재현성 표준 지정)

---

## 🎯 도달 표준 (앞으로 모든 시장조사가 이 이상이어야 함)

### 4단 심화 구조 (직선형 → 입체형)

```
1단 [검색·트렌드]    : API 키워드 +YoY 추세
2단 [소비자 발화]    : 다음카페 + 네이트판 + YouTube 댓글 (수천 건 raw)
3단 [영상 1차 분석]  : 자막 srt + 썸네일 jpg 직접 다운로드 → 멘트·텍스트·구도 추출
4단 [민간 속설/통념] : 한국 머릿속 깊은 미용 통념 (성분·행동·셀럽 어법)
```

기존 [[market-research-playbook]]은 1단·2단까지만 표준이었음.
**3단·4단을 새 표준으로 추가** → 앞으로 "시장조사" 요청 받으면 4단까지 자동 진행.

---

## 📊 본 케이스 1차 자료 규모 (참조 기준)

| 단계 | 데이터 | 규모 |
|------|--------|------|
| 1단 검색 | 검색광고 keywordstool + 데이터랩 24개월 | **80 키워드** + YoY |
| 2단 카페 | 다음카페 (Kakao API) | **5,377건** |
| 2단 커뮤 | 네이트판 (HTML, 시드 18개) | **7,390건** |
| 2단 영상 메타 | YouTube Playwright (제목+조회수+상위댓글) | **65건** (100만+ 5건) |
| **3단 자막** | yt-dlp `--writesubtitles --writeautomaticsub` | **10건 srt** |
| **3단 썸네일** | requests로 thumbnail jpg | **10건 jpg + Read 시각 분석** |
| **4단 속설** | 같은 데이터 X 정제 | unique 발화 **1,195건** + 카피 직변환 80선 |
| **합계 raw** | — | **약 12,800건 1차 자료** |

---

## 🛠 새로 추가된 도구 / 스크립트

### A. `deep_video_analysis.py` — 자막+썸네일 일괄 다운로드
경로: `naver-competitor-finder/scripts/deep_video_analysis.py`

```python
# 핵심 ydl_opts
ydl_opts = {
    'skip_download': True,          # 영상 본체 다운 안 함 (저장공간·시간 절약)
    'writesubtitles': True,         # 수동 자막
    'writeautomaticsub': True,      # 자동 자막 (CC)
    'subtitleslangs': ['ko','ko-KR','a.ko'],
    'subtitlesformat': 'srt/vtt/best',
    'outtmpl': '...subs/{name}.%(ext)s',
}
# + thumbnail URL을 requests로 별도 다운로드
```

**소요 시간**: 10건 영상 약 60초. **거의 무비용 (yt-dlp + requests).**

### B. 썸네일 시각 분석 (Claude Read 도구로 jpg 직접 읽기)
- yt-dlp가 jpg 저장 → Claude의 Read 도구가 이미지 multimodal로 읽음
- 텍스트(헤드라인·서브카피·CTA)·색상·구도·소품·표정 모두 추출 가능
- **OCR 불필요** (Claude vision이 한국어 손글씨까지 읽음)

### C. 속설 추출 정규식 패턴 (`scripts/folk_beliefs.json`)
```python
INGREDIENTS = ['쌀뜨물','우유','달걀','오이','꿀','녹차','토마토','감자',
               '당근','호박','요거트','벌꿀','율무','식초','두부','버섯',
               '인삼','홍삼','녹두','석류','상백피','쑥','막걸리',...]  # 60+
LANGUAGE = ['미백','광채','맑','꿀광','기미','잡티','톤업','뽀얗','보습','진정',...]
# 패턴 A: [성분] (조사) [language]
# 패턴 B: [성분]팩
# 패턴 C: [성분] (조사) 세안/마사지/먹/바르
```

---

## 🔑 본 케이스가 발견한 핵심 인사이트 (재사용 가능)

### 1. PDRN 통념 의심 → 차별화 무기
> 댓글 [좋아요 104]: "PDRN이라도 그냥 손으로 바르면 입자가 커서 그런지 겉도는 느낌"

소비자는 **PDRN 검색 +27% 폭증**과 동시에 **"흡수 안 되는 듯한 의심"**을 가짐.
→ 클렌저/마스크/토너 카테고리는 **"앰플은 겉돌지만, 거품/제형으로 풀어 쓰면 다르다"** 메시지로 정면 돌파 가능.

### 2. "자연광 = 진실 판정" 합격선
> 댓글 [좋아요 814]: "**화장은 무조건 자연광이야**"

**모든 광고 비주얼은 자연광 모티프 명시 필수** (창가 햇살 / 모닝 라이트 / no-flash candid).
→ wiki/tacit/creative-patterns.md §"Before 어두움 + After 자연광"과 동일 결.

### 3. "통념 깨기"보다 "통념 얹기"가 광고 반려율 낮음
- A형 (얹기): "엄마는 쌀뜨물로, 저는 PDRN 30병으로"
- B형 (깨기): "꿀팩 끈적이는 거 말고, 거품에 풀어 쓰는 4중 성분"
- **A형이 광고 심의 통과 잘 되고 거부감 적음** (효능 단정 없이 사회증거 강화)

### 4. 100만뷰 후킹 공식 5선 (실측 검증)
1. ⚠️ "제발 그거 쓰지마" + 5개 자가진단표 (뭔몽 149만)
2. "쌩얼도 예뻐지는 / 내돈내산 파데프리" (현징이 146만)
3. "대부분 잘 모르는 / 찐 꿀팁" (림온 137만)
4. "포기하려던 그때" 좌절 서사 (피부결 59만)
5. "광고❌ 모두 다 광고 없이 찐이야" (최종시안 38만)

→ 모두 [[viral-patterns]]에 append됨.

### 5. 자막 인서트 [대괄호] 표현 풀 (B/A 우회)
```
[3통째 다시 사는 클렌저]
[비싼 값하는 효과 직빵템]
[광고 진짜 없음]
[찐이야... 시꾸들]
[최약체 피부... 흑흑]
[피부 뒤집어지는 시기 TOP3]
```
→ 최종시안 38만뷰의 자막 인서트 패턴, GFA B/A 반려 회피 + 시청자 공감 동시.

---

## 🧰 재현 명령 (다른 카테고리에서 그대로 사용)

```bash
# 환경
cd C:/Users/gguy/Desktop/bol/scripts

# 1단 — 검색 트렌드
python -u research_glow.py  # (시드 변경)

# 2단 — 다음카페 + 네이트판
python -u collect_daum_kakao.py --keywords "{시드 60개 콤마구분}" --months 12
python -u collect_community.py --keywords "{시드 18개}" --sites natepann --months 24

# 2단 — YouTube 검색결과 + 상위댓글
python -u collect_youtube.py --keywords "{시드 13개}" --max 50 --months 12 --detail-top 5

# 3단 — viral 영상 자막+썸네일 (yt-dlp)
python deep_video_analysis.py  # TARGETS 리스트만 카테고리 맞게 수정

# 3단 — 썸네일 시각 분석 (Claude Read 도구로 jpg 읽기)
# → MD 작성 시 Read tool로 각 thumb 직접 호출

# 4단 — 속설 정제
python -c "..." # folk_beliefs.json 추출 (이 파일 §C 참조)
```

---

## 📋 표준 출력 (이제부터 시장조사 산출물 = 6개 MD)

기존 11개 영상기획 MD에 더해 본 케이스 출력:

| # | MD | 내용 |
|---|----|----|
| 01 | `01_product_kpi_usp.md` | KPI / USP / 신뢰장치 |
| 02 | `02_persona_copy.md` | 페르소나 / 카피 / 우회 풀 |
| 03 | `03_visual_lp_reviews.md` | 비주얼 / LP / 리뷰 |
| **04** | **`04_glow_keyword_research.md`** | **검색·트렌드 거시 분석 (1단)** |
| **05** | **`05_viral_video_deep_analysis.md`** | **viral 영상 자막+썸네일 1차 분석 (3단)** |
| **06** | **`06_folk_beliefs_for_glow.md`** | **민간 속설/통념 풀 (4단)** |

→ 04 한 개 → 04+05+06 세 개로 분리하면 IDE 가독성·유지보수 모두 우위.

---

## 🚦 시간 가이드

| 단계 | 예상 시간 | 비고 |
|------|----------|------|
| 1단 검색 | 5분 | 키 있으면 즉시 |
| 2단 카페+커뮤니티 | 5~15분 | API rate limit 대기 |
| 2단 YouTube Playwright | 10~20분 | 13키워드 × 5탑상세 |
| 3단 자막+썸네일 | 1분 | 10영상 × 6초 |
| 3단 시각 분석 (Read) | 5분 | Claude vision 다중호출 |
| 4단 속설 정제 | 3분 | 정규식 1패스 |
| MD 작성 | 30~60분 | 4~6개 파일 |
| **총** | **약 1.5~2시간** | (사용자 컨펌 시간 제외) |

---

## ⚠️ 주의사항·한정조건

### Playwright YouTube 노이즈
- "노란기 없애기" 같은 모호 키워드 → "아이폰17 초기 불량" 같은 무관 영상 섞임
- 후처리: 제목 키워드 매칭 필터 필수 (관련성 토큰 1개 이상)

### yt-dlp 자막 한계
- 자동 자막은 띄어쓰기·조사 오류 자주 (예: "정정밀히" → "찐이야")
- 한국어 어법 추정으로 보정 필요 (특히 의성어·신조어)

### 썸네일 시각 분석
- Claude Read는 한 번에 1 이미지 권장 — 10장이면 10번 호출
- 대량이면 "주요 5장만" 원칙 (조회수 상위 + 톤·후킹 유형 다른 것 우선)

### 다음카페 검색광고 이슈 재발 방지
- `keywordstool`에 공백 키워드 ❌ → 시드 정의 단계에서 공백 제거 자동화
- (이번 케이스에서 1차 시드 13개 모두 400 반려 → 공백 제거 후 재시도)

---

## 🔗 관련 위키

- [[market-research-playbook]] — 본 케이스로 **3단·4단 추가 업데이트 필요**
- [[src-market-research-pipeline-2026-04]] — 1·2단 표준 (주름·유쎄라블 케이스)
- [[src-rubyrn-cleanser-glow-research-2026-04-28]] — 본 케이스 1·2단 부분
- [[viral-patterns]] — 100만뷰 후킹 5선 추가됨
- [[psychology-insights]] — "통념 얹기 vs 깨기" 분기 추가됨
- [[creative-patterns]] — 자막 인서트 [대괄호] 패턴 (최종시안 38만뷰)
- [[usp-performance-canvas-research]] — 04~06 분리 구조 통합 가능

## 📌 다음 시장조사 요청 시 자동 동작

`/시장조사 [주제]` 또는 "**X 시장조사 해줘**" 받으면:
1. **묻지 말고** 1단~4단 모두 진행 (본 케이스가 표준)
2. 산출물은 `canvas/04~06.md` 3개 파일 분리 (단, 사용자가 다른 디렉토리 지정 시 우선)
3. 위키 자동 인제스트 (sources/ + tacit/ append)
4. `wiki/log.md` 엔트리: `## [YYYY-MM-DD] ingest | {주제} 시장조사 4단 심화`
