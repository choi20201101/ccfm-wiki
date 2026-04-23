---
aliases: ["[QSCV] 인덱스"]
type: domain
domain: qscv
confidence: high
created: 2026-04-13
updated: 2026-04-13
baseline: 2025-07
sources: [raw/qscv/]
---

# QSCV — CCFM 마케팅 서비스 품질 표준

## 개요
QSCV는 CCFM(콘크리트파머스) 마케팅사업부·디자인본부·미디어본부의 **서비스 품질(Quality / Service / Consistency / Value)** 표준 문서 체계. 신규 광고주 배정부터 광고 라이브, 성과 리뷰, 재기획까지 전 고객여정에서 "어떤 마케터가 담당하든 동일한 품질이 나오게" 하는 매뉴얼.

- **베이스라인**: 2025년 7월 기준 (원본 문서는 2025-04~ 생성됨)
- **업데이트 정책**: 이 베이스라인 위에 사용자가 중요한 내용 계속 추가
- **원본 위치**: [`raw/qscv/`](../../raw/qscv/) — 14개 docx 추출본 + 200줄 단위 청크 47개

## 맵 (14개 문서)

### A. 본부별 고객여정 매뉴얼
| # | 문서 | 페이지 | 원본 |
|---|------|--------|------|
| A1 | 디자인본부 고객여정편 | [[design-customer-journey]] | raw/qscv/CCFM_디자인본부_Q_고객여정편_250424.md |
| A2 | 미디어본부(영상) 고객여정편 | [[media-customer-journey]] | raw/qscv/CCFM_미디어본부_Q_고객여정편_250428.md |

### B. 매체 매뉴얼 (마케팅사업부)
| # | 문서 | 페이지 | 원본 |
|---|------|--------|------|
| B1 | META | [[media-meta]] | raw/qscv/CCFM_마케팅사업부_Q_매체_매뉴얼_META_250430.md |
| B2 | Google | [[media-google]] | raw/qscv/CCFM_마케팅사업부_Q_매체_매뉴얼_Google_250430.md |
| B3 | GFA (네이버 성과형 DA) | [[media-gfa]] | raw/qscv/CCFM_마케팅사업부_Q_매체_매뉴얼_GFA_250430.md |
| B4 | 검색광고 | [[media-search-ads]] | raw/qscv/CCFM_마케팅사업부_Q_매체_매뉴얼_검색광고_250430.md |

### C. 퍼포먼스 사고 프레임
| # | 문서 | 페이지 | 원본 |
|---|------|--------|------|
| C1 | 퍼포먼스 사고 확장 가이드 | [[performance-thinking]] | raw/qscv/CCFM_마케팅사업부_Q_퍼포먼스_사고_확장_가이드.md |

### E. 브랜드별 캔버스 (Live Drafts)
| # | 브랜드 | 버전 | 상태 | 페이지 |
|---|--------|------|------|--------|
| E1 | Rusolve (탈모) | v1 | hypothesis-baseline (데이터 집행 전) | [[canvas-rusolve-v1]] |

### D. Appendix — 점검/기획 체크리스트
| # | 문서 | 페이지 | 원본 |
|---|------|--------|------|
| D1 | 객단가 점검 체크리스트 | [[appendix-aov]] | raw/qscv/객단가_점검_체크리스트_Appendix.md |
| D2 | 랜딩페이지 점검 체크리스트 | [[appendix-landing]] | raw/qscv/랜딩페이지_점검_체크리스트_Appendix.md |
| D3 | 상세페이지 점검 체크리스트 | [[appendix-detail-page]] | raw/qscv/상세페이지_점검_체크리스트_Appendix.md |
| D4 | 영상 필수 기획 항목 | [[appendix-video-planning]] | raw/qscv/영상_필수_기획_항목_Appendix.md |
| D5 | 이미지 필수 기획 항목 | [[appendix-image-planning]] | raw/qscv/이미지_필수_기획_항목_Appendix.md |
| D6 | 콘텐츠 기획 가이드 | [[appendix-content-guide]] | raw/qscv/콘텐츠_기획_가이드_Appendix.md |
| D7 | 퍼포먼스 캔버스 업데이트 및 재기획 | [[appendix-canvas-reupdate]] | raw/qscv/퍼포먼스_캔버스_업데이트_및_재기획_Appendix.md |

## QSCV 레이어 구조
```
[고객여정 레이어]    A1 (디자이너)   A2 (영상디자이너)
        ↓
[매체 실행 레이어]   B1 META   B2 Google   B3 GFA   B4 검색광고
        ↓
[사고 프레임]        C1 퍼포먼스 사고 확장 가이드 (마인드셋 + 캔버스)
        ↓
[실행 체크리스트]    D1~D7 (기획·점검 Appendix)
```

## 업데이트 방식
- **원본 보존**: `raw/qscv/*.md` 는 덮어쓰기 금지. 원본 docx에서 재추출 시에만 갱신.
- **청크 참조**: 각 페이지에서 상세 내용은 `raw/qscv/chunks/*__chunkNNN.md` 로 링크.
- **증분 업데이트**: 사용자가 추가 지시하면 해당 페이지에 append + log.md에 엔트리 기록.
- **암묵지 승격**: 매뉴얼 외 판단 기준(ex. "GFA CPC 얼마에서 소재 교체") 나오면 `wiki/tacit/`로 교차 저장.

## 청크 청크 인덱스 (47개)
| 원본 | 라인수 | 청크 |
|------|-------|------|
| 디자인본부 고객여정편 | 598 | 3 |
| 미디어본부 고객여정편 | 329 | 2 |
| META | 1024 | 6 |
| Google | 1497 | 8 |
| GFA | 1290 | 7 |
| 검색광고 | 1046 | 6 |
| 퍼포먼스 사고 확장 | 1417 | 8 |
| 객단가 Appendix | 148 | 1 |
| 랜딩페이지 Appendix | 120 | 1 |
| 상세페이지 Appendix | 189 | 1 |
| 영상 기획 Appendix | 45 | 1 |
| 이미지 기획 Appendix | 30 | 1 |
| 콘텐츠 기획 Appendix | 56 | 1 |
| 캔버스 재기획 Appendix | 46 | 1 |
| **합계** | **7835** | **47** |

## 관련 암묵지
추출되어 `wiki/tacit/`에 축적될 가능성 있는 영역:
- `tacit/decision-rules.md` — "ROAS X% 이하면 소재 교체" 같은 매체별 판단선
- `tacit/creative-patterns.md` — USP→Pain Point→CTA 구조에서 먹히는 패턴
- `tacit/operational-heuristics.md` — 신입 디자이너 room 수, NAS 세팅 루틴
