---
type: source
domain: marketing-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [C:\Users\Administrator\Desktop\market-research-package\modules\cafe]
---

# src: 네이버 카페 크롤러 모듈

## 위치
`C:\Users\Administrator\Desktop\market-research-package\modules\cafe\`

## 핵심 기능
- 네이버 카페 랭킹 → 대상 카페 선정(나무등급↑) → 자동 가입 → 키워드 검색 기반 게시글 대량 수집(10k+) → 키워드/감정/시술/제품 Counter 분석 → MD 보고서 및 영상 기획 생성.
- Selenium + BS4 + pyautogui + 수동 캡차 루프(answer.txt)로 로그인·가입·크롤링을 한 파이프라인에 묶음.

## 주요 파일
| 파일 | 역할 |
| --- | --- |
| `src/auth/save_cookies.py` | visible 모드 로그인 → `naver_cookies.json` 저장 (이후 세션 재사용) |
| `src/auth/login.py` | 로그인 + 캡차 루프 + 카페 내부 검색(`ArticleSearchList.nhn` iframe) + 키워드 인사이트 리포트 |
| `src/join/join_cafe.py` | 단일 카페 가입 — JS `iframe.contentDocument` 직접 접근 + pyautogui 캡차 크롭 |
| `src/join/batch_join.py` | 7개 카페 일괄 가입, `cafe_join_log.json` 으로 재실행 시 스킵 |
| `src/rankings/collect.py` | 카테고리 4종 × ArticlePaginate 전체 순회 → `cafes_{카테고리}.json` |
| `src/rankings/report.py` | 나무등급 이상 필터 + MD 카페 리스트 |
| `src/posts/collect.py` | 통합검색(`search.naver.com?where=article`) 기반 게시글 대량 수집, CLI 파라미터화 (`--title --seed --queries --target`), 증분 저장 |
| `src/analysis/video_plan.py` | 페르소나 + 퍼포먼스 영상 기획 (8종 광고 요소) |

## 의존성
- Python: `C:\Users\Administrator\AppData\Local\Python\bin\python.exe`
- `selenium`, `webdriver-manager`, `beautifulsoup4`, `pyautogui`, `pillow`
- Chrome binary: `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- ChromeDriver: selenium-manager / webdriver-manager 자동
- 인코딩: `PYTHONIOENCODING=utf-8` 필수
- 외부 의존: 네이버 계정 1개 (`.naver_creds` 또는 env), 사람의 캡차 수동 입력(answer.txt)

## 사용 예
```bash
# 1. 쿠키 저장 (최초 1회)
PYTHONIOENCODING=utf-8 python src/auth/save_cookies.py

# 2. 랭킹 수집 + 후보 필터
PYTHONIOENCODING=utf-8 python src/rankings/collect.py
PYTHONIOENCODING=utf-8 python src/rankings/report.py

# 3. 일괄 가입
PYTHONIOENCODING=utf-8 python src/join/batch_join.py

# 4. 게시글 대량 수집 (시드 키워드 → 자동 쿼리 확장)
PYTHONIOENCODING=utf-8 python src/posts/collect.py \
    --title 기미 --seed 기미 --target 10000

# 5. 영상 기획 분석
PYTHONIOENCODING=utf-8 python src/analysis/video_plan.py
```

## 알려진 이슈
- **계정 plaintext 하드코딩**: auth/login.py, auth/save_cookies.py, join/*.py 에 ID/PW 박혀 있음 → 리팩토링 필요
- **pyautogui 캡차 좌표 하드코딩** (1920x1200 전용)
- **iframe 구조 의존**: 네이버 카페 리뉴얼 시 셀렉터 대거 깨짐. `_archive/scripts/` 에 26개 레거시, `_archive/screenshots/` 98개 디버그 캡처가 증거.
- **UA/프록시 로테이션 없음** — 단일 계정·IP 장기 운영 시 차단 리스크 (확인 필요)
- **캡차 무인 처리 불가** — answer.txt 파일 폴링으로 사람 개입 필수 (10분 타임아웃)
- **크롬 포커스 의존**: clipboard paste, 가입 캡차 크롭이 창 활성 상태 요구
- **법적 회색지대**: 수집된 작성자 닉네임/본문의 상업적 분석 (개인정보·저작권 확인 필요)
- **등급 업/출석 자동화 미구현** (확인 필요)

## 관련 도메인
- [[marketing-automation]]
- [[viral]] (카페는 시딩 채널)
- [[ai-automation]]
