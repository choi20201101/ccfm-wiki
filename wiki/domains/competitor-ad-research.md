---
title: 경쟁사 광고 조사 - 메타 + 구글 풀 파이프라인
domain: ad-research
type: domain
confidence: high
source: sisi 프로젝트 13브랜드 실전 검증 (2026-05-17)
related: [[tacit/meta-ad-library-search]], [[domains/marketing-automation]], [[qscv/canvas-rusolve-v1]], [[domains/market-research-playbook]]
tags: [competitor-research, meta-ad-library, google-ads-transparency, performance-canvas, html-report, ccfm-skill]
---

# 경쟁사 광고 조사 도메인 (메타 + 구글 풀 파이프라인)

## 한 줄 요약

도메인 리스트 → 메타·구글 광고 풀 수집 → YouTube 조회수 정렬 → 퍼포먼스 캔버스 분석 → 인터랙티브 HTML 보고서 → 공유 zip. 실전 검증: 13브랜드 / 40+ 영상 캔버스 분석 / 193MB 패키지.

## 스킬화

스킬: `~/.claude/skills/competitor-ad-research/SKILL.md`
트리거: "경쟁사 광고 조사", "competitor ads", "메타 광고 라이브러리 분석", "구글 ads transparency", "/competitor-ads"

## 파이프라인 (7단계)

```
[1] 도메인 리스트 (txt)
    ↓
[2] 메타 수집 (meta-ads-collector)
    └─ 도메인/영문/한글 3쿼리 합집합, link 필터 X
    ↓
[3] 구글 advertiser 발견 (Playwright)
    └─ 라이브러리 fail → Transparency Center 검색 페이지 직접 렌더링
    ↓
[4] 구글 광고 페이지 → YouTube embed iframe ID 추출
    ↓
[5] yt-dlp 메트릭 (조회수/좋아요/title) + top N 정렬
    ↓
[6] 영상 mp4 다운로드 + ffmpeg 키프레임 4장 (기/승/전/결)
    ↓
[7] Claude 멀티모달 → 퍼포먼스 캔버스 12항목 분석
    ↓
[8] 인터랙티브 HTML 보고서 + out 폴더 zip 패키징
```

## 핵심 발견 (sisi 프로젝트, 13브랜드 검증)

### 1. 한국 D2C 퍼포먼스 광고 운영 패턴
- 광고대행사 운영 브랜드는 **추적용 더미 페이스북 페이지** 사용 (브랜드명 페이지 X)
- 자체 단축 URL (`brand.kr/surl/...`) + utm 파라미터로 채널 추적
- 따라서 Meta Ad Library 검색은 **도메인/링크 기준이 정답**, 페이지명 매칭 X
- 자세한 룰: [[tacit/meta-ad-library-search]]

### 2. 동일 광고대행사 시그니처 (4브랜드 클러스터)
sisi 검증 결과 라셀턴 / 비렌느 / 허밍테라피 / 알파4500 동일 광고대행사 운영 의심:
- YouTube 영상 타이틀 "지금이 제일 싸요" 3브랜드 동일
- 카피 시그니처: 🔒비밀링크🔒, ⚠️긴급공지⚠️, 🤫
- 헤드라인 구조: `[비밀링크🔒] / [%할인] / [상품명]`
- 부정어 신뢰 역설: "효능 논란", "양 조절 잘못"
- 가짜 희소성: "곧 가격 인상", "재고 모니터링", "마지막 N세트"
- 추적 코드 광고 본문 노출 (`MHIMGTOSLSMLSM00000X`)

→ **이 시그니처 = 검증된 D2C 광고 공식** (컨버전율 높아서 여러 브랜드에 동일 적용)

### 3. 광고 시각화 4클러스터
| 클러스터 | 특징 | 대표 브랜드 |
|---|---|---|
| **충격 텍스트 폭격형** | 이미지 X, 빨강·검정 텍스트만 | 라셀턴 |
| **AI 캐릭터 의인화** | 3D 친근 캐릭터 + 임상 매트릭스 | 비렌느 |
| **UGC 셀카 친구형** | 일반인 인플루언서 톤 | 헤어리듬 |
| **스토리텔링 페르소나** | 할머니/이모 캐릭터 + 정성 톤 | 그래니샐러드 |

### 4. AI 생성 콘텐츠 침투
- 메타가 "AI로 생성된 콘텐츠입니다" 자동 라벨 추가
- 한국 D2C 광고 AI 비중 급증 (2026 기준)
- 검증: 비렌느(3D 캐릭터), 허밍테라피(AI 신체), 알파4500(AI 슬림 모델)

### 5. 의료법 회색 영역
허밍테라피·라셀턴 카피 단기 컨버전↑이지만 메타 광고 차단·소비자보호원 신고 위험:
- "ZI흅(지방흡입) 대신 패치" (의료 시술 대체)
- "전문 클리닉 납품 강제 승격" (사실 왜곡)
- "효능 논란" (식약처 점검 트리거)
- 검열 카피 ("미X녹시딜", "ㅇㅇ 녹여주는 것")

## 퍼포먼스 캔버스 12항목 (영상별 분석 형식)

[[qscv/canvas-rusolve-v1]] 기반 + 치알디니 7대 설득 요소:

1. 제품 본질
2. 타깃 페르소나
3. 기 (Hook, 첫 1초)
4. 승 (Build-up)
5. 전 (Climax)
6. 결 (Outro/CTA)
7. **숫자적 근거 시각화** ⭐
8. **사회적 증거 시각화** ⭐
9. **사회적 권위 시각화** ⭐
10. **사회적 통념 활용** ⭐
11. 설득 Levers 조합
12. 핵심 메시지 (1줄)

자세한 패턴 라이브러리: `~/.claude/skills/competitor-ad-research/resources/performance-canvas.md`

## 도구 스택

| 단계 | 도구 | 비고 |
|---|---|---|
| 메타 수집 | meta-ads-collector (PyPI) | curl_cffi TLS 위장, API 키 X |
| 구글 발견 | Playwright + chromium | 라이브러리 fail → 수동 우회 |
| 구글 광고 ID | Google-Ads-Transparency-Scraper | `creative_search_by_advertiser_id` 동작 |
| YouTube 메트릭 | yt-dlp --dump-json | API 키 X |
| 영상 처리 | yt-dlp + ffmpeg | 키프레임 추출 |
| 분석 | Claude multimodal (Read) | 멀티모달 |
| 보고서 | Python (f-string HTML) | Jinja2 X (단순) |

비교 디테일: `~/.claude/skills/competitor-ad-research/resources/tools.md`

## Harness 규칙 (강제)

`resources/harness-rules.md` 10개 룰:
- R1: 메타 link 필터 금지
- R2: 구글 advertiser 발견은 Playwright 필수
- R3: 구글 region "KR" 대문자
- R4: HTML 영상은 로컬 mp4 + `<video>` (iframe X)
- R5: 광고 데이터 즉시 다운로드 (signed URL 만료)
- R6: 한 광고주 다중 제품 → 키프레임 분류
- R7: 조회수 threshold 4만 기본
- R8: 한글 UTF-8 인코딩
- R9: 의료법·표시광고법 리스크 표시
- R10: 카피 dedup (메타 top3)

## 산출물 형식

```
프로젝트 폴더/
├── ads_data/{브랜드}/{meta|google}/...
├── ads_data/_visual_analysis.json (캔버스 분석)
├── 경쟁사광고-인터랙티브보고서.html (메인)
├── 경쟁사광고-분석보고서.md (텍스트)
├── out/ (공유 패키지 폴더, 영상·키프레임만)
└── 경쟁사광고-out.zip (zip 공유용)
```

## 관련 메모리·문서

- 메모리: `feedback_meta_ad_library_search.md`, `project_competitor_ad_analysis.md`
- 위키 (관련): [[tacit/meta-ad-library-search]] (메타 검색 룰), [[qscv/canvas-rusolve-v1]] (캔버스 형식), [[domains/marketing-automation]] (마케팅 자동화)
- 외부 도구 가이드: `Desktop/sisi/광고라이브러리-크롤링-가이드.md`

## 한계 (Honest)

1. **광고비/CTR/타겟팅 비공개** — 광고주만 봄
2. **Google Advertiser Verification 미완료** = Transparency Center에 안 뜸 (한국 D2C 소규모 대다수)
3. **단축 URL 사용 브랜드** = link 매칭 검증 불가, 검색 결과 자체를 신뢰
4. **영문 브랜드명 흔한 단어면 노이즈** — 분석 단계 수동 제거
5. **AI 생성 영상 비중 증가** = 시각 패턴 분석은 가능하지만 실제 효과 측정은 별도

## 다음 확장 (v2 후보)

- 네이버 광고 라이브러리 통합
- 인스타그램 인플루언서 협찬 자동 식별
- 시계열 분석 (월별 광고 트렌드)
- 광고 카피 자동 생성기 (학습 데이터 활용)
- 메타 광고 변형 cluster 분석 (같은 base 영상의 비율/카피 변형 그룹화)
