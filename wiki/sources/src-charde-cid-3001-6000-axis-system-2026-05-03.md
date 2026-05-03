---
type: source
domain: da-creative
confidence: high
created: 2026-05-03
updated: 2026-05-03
sources:
  - C:\Users\Administrator\Desktop\srd\scripts\pipeline.py
  - C:\Users\Administrator\Desktop\srd\scripts\_seed_copies.py
  - C:\Users\Administrator\Desktop\srd\state\copies.json
related:
  - "[[creative-patterns]]"
  - "[[da-creative]]"
  - "[[src-charde-melapeel-usp-2026-04-27]]"
---

# 샤르드 CHARDE cid 3001~6000 — 18축 자동 광고 소재 시스템 정본

## 1. 개요

CHARDE 멜라케어 필크림 마스크 (식약처 미백·주름 2중 기능성, HyWhite·SPOTSHOT™ 5단계, 임상 31.38%/34.53%/100%) 광고 이미지 cid 3001~6000 = **3000장 unique 광고 컷**.

ChatGPT GPT-5.4 image generation 웹 자동화 (Playwright + Chrome CDP 9222 + 2탭 병렬 워커) 로 1장당 30초~3분, 분당 ~0.5장 페이스. 약 3.6일 운영.

## 2. 18축 cid 시드 결정론 시스템 (2026-04-30 ~ 2026-05-03 진화)

| 그룹 | 축 | 풀 사이즈 | 도입 일자 | Why |
|---|---|---|---|---|
| 모델 4축 | HAIR / FACE / SKIN / BG_AMBIENCE | 33+31+25+30 | 2026-05-01 | "다 비슷한 모델" 차단 |
| 모델 5축 | + ETHNICITY (백인35/한국25/흑인9/라틴9/일본9/기타12) | 33 | 2026-05-02 | 전부 한국인 인지 차단 |
| 모델 6축 | + OUTFIT_LUXURY (트위드/캐시미어/실크 30종) | 30 | 2026-05-02 | 얼굴 20대 + 복장 4050 명품 무드 대비 |
| 모델 7축 | + GROUP_SIZE (1~5명, 5명 다인종 마스크 떼기) | 15 | 2026-05-02 | 그룹 사이즈·바이럴 후킹 |
| 모델 8축 | + POSE_ATTITUDE (표정 9 / 자세 11 / 손짓 10) | 30 | 2026-05-03 | 정면 반신 만족 미소 단조 차단 |
| 권위·증거 2축 | AUTHORITY_BG (방송/매거진/약국매대/메디컬랩) + PROOF_VISUAL (단톡·인스타·블로그·영수증·매대) | 25+30 | 2026-05-03 | 청담 박사 식상 회피 + 사회증거 시각화 |
| 카피 폼 5축 | LAYOUT / TYPO / FRAME / ACCENT / PALETTE | 25+35+25+18+8 | 2026-05-02 | 카피 폼 거의 동일 차단 |
| 카피 색감 1축 | HEADLINE_COLOR (네온그린·코랄핑크·페일라일락·머스타드·올리브·터쿼이즈·로즈골드 등) | 35 | 2026-05-03 | 검정·노랑·빨강 단조 차단 |
| 카피 화법 1축 | COPY_VOICE (1줄리뷰형/타인반응인용/질문형후킹/명령형단호/가격직격/의태어/단톡채팅체/예능자막체 등) | 20 | 2026-05-03 | 점잖은 슬로건 단조 차단 |
| 카피 자연 문장 1축 | sub_seeds + sub_review_seeds 자연 문장체 | 100+100 / 페인 | 2026-05-03 | 사용자 "겹침없이 중복없이" 디렉션 |

**모든 18축 동일 RNG 시드:** `_div_rng = random.Random(cid * 31337 + 11)` — cid별 결정론 + 재현성 + 다양성 동시 보장.

## 3. 페인포인트 4축 (CHARDE 정본)

| pain_id | 명칭 | 무드 | 비중 |
|---|---|---|---|
| 1 | 시술비 부담 (가성비) | 시술명 직격 + 가격 비교 + 가성비 충격 | 30% |
| 2 | 회복 기간 부담 (다운타임 0) | 자기 전 5분 + 다음 날 출근 + 직장인 1픽 | 25% |
| 3 | 미백 제품 체감 불신 (임상 권위) | 임상 31% + 광고 안 믿다→인정 + 갱년기·민간요법 vs 본품 | 20% |
| 4 | 떼는 결과 시각 쾌감 (바이럴) | 발라서 40분 + 양손 와르르 + 동창·딸·헤어쌤 반응 | 25% |

각 페인별 SHOT_STYLE 풀 (PAIN_THEMES) + sub_seeds 100 + sub_review_seeds 100 (자연 문장체) 매핑.

## 4. 카피 자극 7대 후킹 패턴 (자연 문장체)

| # | 패턴 | 예시 |
|---|---|---|
| 1 | 인용 + 인지 차이 | "친구가 '시술 받았어?' 묻길래 본품 한 통이라 답함" |
| 2 | 역접·반전 ("~인 줄 알았는데") | "갱년기라 어쩔 수 없다 생각했는데 1통 후 30대로 본다" |
| 3 | 인과·결과 | "프락셀 50만 끊고 본품 한 통, 자기 전 5분이라 진짜 편함" |
| 4 | 관계·인용 추천 | "엄마 친구가 '관리실 가지 마' 화내길래 본품 한 통" |
| 5 | 시간·장면 묘사 | "퇴근 후 8시 30분 화장대 5분이면 끝나는 루틴" |
| 6 | 단톡 인증·바이럴 | "단톡방에 사진 올렸더니 다 1통씩 시작" |
| 7 | 민간요법 vs 본품 | "쌀뜨물 30년 한 동기, 본품 1통 4주 후 동안이라 듣기" |

자세한 룰은 [[creative-patterns#광고-카피-자극-패턴-stimulating-hook-patterns]] 참조.

## 5. 결과 메트릭 (cid 3001~6000)

### Before (2026-05-02 기준 — 7축 + 카피 풀 50)
- sub unique: 402 / 3000 (TOP 15가 13~15회 반복)
- sub_review EMPTY: 70% (rnd.random() < 0.3 룰)
- sub max repeat: 15x

### After (2026-05-03 — 18축 + 카피 풀 100 + cap 6 + sub_review 100%)
- sub unique: **796 / 2409 (신규 재시드 영역)** (2배 개선)
- sub_review EMPTY: **0%** (신규 재시드 영역)
- sub max repeat: **9x** (40% 개선)
- 보존 cid 591장 (사용자 폴더 분류 + 이미 그린 jpg) 카피 그대로 유지

## 6. 핵심 코드 위치

- 풀 정의: `pipeline.py` line 75~576 (PAIN_AXIS), line 580~ (LAYOUT/TYPO/FRAME/ACCENT/COLOR/HAIR/FACE/ETHNICITY/OUTFIT/GROUP/POSE/AUTHORITY/PROOF/HEADLINE_COLOR/COPY_VOICE)
- 자연 문장 풀 확장: `pipeline.py` line 576+ (`_NATURAL_SUB_PAIN_X` + `_NATURAL_REVIEW_PAIN_X` extend)
- cid 시드 회전: `pipeline.py` `build_oneshot_prompt` line 2295~ (`_div_rng = random.Random(cid * 31337 + 11)`)
- 카피 시드: `_seed_copies.py` (200회 retry + 3-tuple unique + cap 6 + sub_review 100% 강제)

## 7. 사용자 디렉션 누적 (2026-04-27 ~ 2026-05-03)

| 일자 | 핵심 디렉션 |
|---|---|
| 2026-04-30 | 신컨셉 v3 3000장·8x6 색배경 매트릭스·메인1·서브1~3 |
| 2026-05-01 | 점잖은 과거형 폐기·1줄 리뷰체·강조어·의태어·가격직격 |
| 2026-05-01 | 모델 다양화 4축 (HAIR/FACE/SKIN/BG) 강제 |
| 2026-05-02 | 5축 ETHNICITY (인종 다양화) |
| 2026-05-02 | 6축 OUTFIT (얼굴 20대 + 복장 4050 명품) |
| 2026-05-02 | 7축 GROUP_SIZE + 카피폼 다양화 (TYPO/FRAME/HEAD/ACC) |
| 2026-05-03 | 8축 POSE + 권위배경·화법·색감 변주 |
| 2026-05-03 | "겹침없이 중복없이 사람이 잘 읽을 수 있는 문장 구성" — 자연 문장 풀 100 + cap 6 + sub_review 100% |

## 8. 일반화 가능 교훈

1. **18축 동시 결정론 시드** (`cid * 31337 + 11`) — 한 RNG 로 모든 풀 회전 = 카피·시각 동시 다양화 (한쪽만 다양화 시 다른 쪽 단조 위험)
2. **풀 사이즈 × 0.06 = cap** 공식 — 3000장 운영 시 풀 100·cap 6 안전선
3. **sub_review 30%→100% 강제** — 페르소나 후기는 모든 cid 필수 (확률 룰은 빈 카피 폭증 원인)
4. **자연 문장체 7대 후킹** — 압축 슬로건체 폐기, 인용·역접·인과·관계·시간·바이럴·민간요법 7축
5. **사용자 분류 폴더 보존 룰** — ckpt 등록 cid 카피 무조건 보존 (사용자 노력 보존)

## 🔗 연결

- [[creative-patterns]] — 자극 카피 7대 후킹 패턴 + 18축 시스템 (이 사례에서 추출한 일반화 패턴)
- [[da-creative]] — DA 크리에이티브 도메인 (적용 영역)
- [[src-charde-melapeel-usp-2026-04-27]] — 샤르드 USP 캔버스 (제품 정본)
- [[usp-performance-canvas-research]] — 8요소 USP 캔버스 (영상기획·이미지카피·페인포인트·무의식키워드·후킹·페르소나·사회증거·파생키워드)
