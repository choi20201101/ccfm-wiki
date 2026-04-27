---
type: source
title: 샤르드 멜라케어 필크림 마스크 — USP 퍼포먼스 캔버스 조사 첫 케이스
domain: marketing-research
confidence: high
created: 2026-04-27
updated: 2026-04-27
related:
  - usp-performance-canvas-research
  - marketing
---

# src-charde-melapeel-usp-2026-04-27

[[USP 퍼포먼스 캔버스 조사]] 플레이북의 **최초 적용 케이스**. 본 케이스로 표준 7파일 구조·OCR 리사이즈 단계·담당자 매핑표가 확립됐다.

---

## 입력

- **URL**: https://charde.co.kr/surl/P/241
- **제품**: 샤르드 멜라케어 필크림 마스크 (50ml, 미백·주름개선 2중 기능성)
- **product_no**: 241
- **담당자 자료**: 타깃(여성 40-59 메인) + 전환 반응 카피 + 이미지 가이드 + 페인포인트 4축

---

## 출력 위치

```
~/Desktop/srd/
├── docs/melapeel_brief.md             # 인덱스 56줄
└── docs/melapeel/
    ├── 01_overview_pricing.md         65줄
    ├── 02_canvas_copy.md              42줄
    ├── 03_detail_ocr.md              240줄  (36컷)
    ├── 04_copy_assets.md              42줄
    ├── 05_review_widget.md            47줄
    ├── 06_target_persona.md           50줄
    └── 07_mapping_followup.md         33줄
```

원본/리사이즈본:
- `~/Desktop/srd/refs/melapeel_landing/`     (jpg/gif 36장)
- `~/Desktop/srd/refs/melapeel_landing_ocr/` (≤1500px jpg 53장, 3MB)

---

## 핵심 학습 (이 케이스에서 확립된 규칙)

### L1. 첫 OCR 시도가 "2000px 초과" 에러로 실패 → 무조건 리사이즈 단계 표준화
- 카페24 상세이미지는 보통 1500~2400px 폭. 첫 시도에서 8~9컷 막히고 멈춤.
- **해결**: PIL로 long side ≤1500px JPEG로 다운샘플 + GIF는 first/last 프레임만 분리
- 결과: 53장 3MB → subagent OCR 280초 내 완료

### L2. 리뷰 위젯(SnapReview)은 비동기 JS — 정적 fetch 무용
- `<span class="snap_widget">` + `spm_f_common.js` 비동기 XHR 후 렌더
- 외부 API(`api.snapfit.co.kr`)는 본 환경에서 DNS/방화벽 차단
- **확보 가능 메타**: JSON-LD `aggregateRating` (예: 3.5 / 1,157건)
- **대체 노출 지점**: 페이지 내 `05_all.jpg` "CHARDE REAL REVIEW" 4건 ★★★★★ 카드

### L3. 담당자 자료 ↔ 페이지 매핑표가 결과물의 "발사대"
- 담당자가 강조한 카피 ("31% 개선", "벌써 N통 째", "그냥 뜯어버리세요", "쾌감")는 **페이지 컷에 정확히 같은 수치/표현이 박혀 있음**
- 매핑 없이 페이지만 정리하면 "OCR 받아쓰기"에 그침
- 매핑 있으면 "어느 컷을 카피 시드로 즉시 사용 가능한지" 1대1 발사 가능

### L4. 인덱스 60줄 이내 + 7파일 분할 = 가독성·재사용성 동시 확보
- 처음에 415줄 단일 MD로 작성 → 사용자 피드백 "너무 길다"
- 30초 요약·자산 위치만 인덱스에 남기고 나머지 7개 카테고리 파일로 분리
- 03(detail_ocr.md)만 240줄로 길지만 컷 수에 비례 → 내부 10개 서브섹션으로 탐색 가능

### L5. 자산 폴더 구조: `refs/{slug}_landing/`(원본) + `refs/{slug}_landing_ocr/`(리사이즈본)
- 원본은 보존, OCR용은 재가공 가능
- 다음 케이스에서도 `refs/{다른제품}_landing/` 형식으로 평행 누적 가능

---

## 처리 시간

| 단계 | 소요 |
|---|---|
| WebFetch (캔버스 추출) | ~30초 |
| 상세이미지 36장 curl 다운로드 | ~25초 |
| PIL 리사이즈 (53컷 출력) | ~10초 |
| Subagent OCR (3장 병렬) | ~280초 |
| MD 7파일 작성 | ~60초 |
| **합계** | **~7분** |

---

## 담당자 자료 (요약 인용)

- **메인 타깃**: 여성 40-59 / 서브: 여성 30-39, 남성 30-60(55-59 제외)
- **전환 반응 카피**: "흑자가 딱지처럼 똑…?", "31% 개선", "벌써 N통 째", "그냥 뜯어버리세요", "쾌감", "외국·호주·뉴질랜드"
- **이미지 가이드**: 외국인 모델 우세, 기미 있는 인물의 필오프 떼는 장면, 산더미 컷
- **페인포인트 4축**: ① 짙은 흑자 콤플렉스 ② 시술 후 다운타임 부담 ③ 미백제품 체감 불신 ④ 흡착 배출 시각적 쾌감

---

## 다음 단계 후보

- 매핑표 7번 섹션 → 카피 30~50개 시드뱅크로 확장 → 광고 크리에이티브 생성 ([[da-creative]])
- 페이지 외국인 모델 컷 → `srd/refs/face/influencer_2026/` 시드와 묶어 외국인 광고 소재 생성 라인
- "산더미 컷" 시드 → `srd/refs/best/`에 신규 카테고리 생성

---

## 한계 / 미수집

- SnapReview 동적 본문 (별점 분포, 키워드, 페르소나 위젯) — Playwright 별도 수집 필요
- "200만 개 판매 / 30초마다 1개" 류 정량 대세감 카피 — 사실 근거 미확보
- `srd/refs/face`·`refs/best`는 nari(네리티아) 자산 그대로 복사 → 메인 타깃·필오프 톤과 안 맞는 컷 다수 → 1차 큐레이션 필요
