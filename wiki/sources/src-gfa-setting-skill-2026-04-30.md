---
type: source
domain: marketing-automation
confidence: high
created: 2026-04-30
updated: 2026-04-30
sources: ["github:Min-Gil-Sang/GFA-Setting", "C:/Users/gguy/Desktop/GFA-Setting"]
---

# src — GFA-Setting v0.1.0 (2026-04-30)

네이버 GFA 광고 그룹+소재 atomic 자동 등록 Claude 스킬의 v0.1.0 릴리스 소스 스냅샷.

## 빌드 경로

bob (Spec) → dd (6 step 분해) → harness (가드레일) → 구현 → eval (코덱스 감사) → wiki

```
dd/step-00 설계_및_가드레일       (bob + harness)
dd/step-01 환경셋업_API클라이언트  → ADR-011 피봇 후 브라우저 클라이언트로 성격 변경
dd/step-02 계정_캠페인_플로우      (cli.py + 캠페인 ID 직접 입력)
dd/step-03 광고그룹_생성로직        (참조 그룹 UI 복제)
dd/step-04 소재_DrissionPage_자동화 (이미지 업로드)
dd/step-05 스킬_통합_및_검증       (E2E + SKILL.md)
```

## 핵심 ADR

| ADR | 결정 | 효과 |
|---|---|---|
| 011 | REST/OAuth → DrissionPage 브라우저 자동화 | OpenAPI 차단 우회 |
| 012 | 캠페인 리스트 스크레이핑 → 직접 입력 | 스크레이핑 코드 전체 제거 |
| 013 | 27 파라미터 빌더 → 기존 그룹 UI 복제 | 매핑표/parsers.py 전부 제거, 사용자 입력 5개로 축소 |
| 014 | 그룹+소재 atomic 등록 + partial 추적 | orphan group 처리 룰 명문화 |

## E2E 검증 (2026-04-30)

| 그룹 | 이미지 | adSetNo | URL suffix |
|---|---|---|---|
| `길상_테스트_01` | 2장 | 4263467 | `vi_gfa_260429_01` |
| `길상_테스트_02` | 2장 | 4263502 | `vi_gfa_260429_02` |
| `길상_테스트_03` | 1장 | 4263536 | `vi_gfa_260429_03` |

3 그룹 모두 `/create/complete` 진입. 단일 세션 약 200+ 액션 누적 (3 그룹 + troubleshooting dry-run 4-5회).

## 코덱스 감사 결과 (2026-04-30)

직접 검증 완료된 잔존 이슈 — 자세한 항목은 [[domains/gfa-setting-automation]] §코덱스 감사 결과 참조.

- **치명**: README/SKILL의 antd 안전가정과 코드 불일치 (dispatchEvent / native value setter 다수 잔존, hydrate 트리거만 트러스트화됨)
- **높음**: CLI 종료 출력에서 partial(orphan group) 누락, `cli.py:60` `configure_logging(secrets=[])` 마스킹 무력화, `_assembled/.gitignore`/`.pre-commit-config.yaml` 단독 부재
- **중간**: N>20 차단은 너무 느슨, 시작일시 타임존 검증 없음, `_NN` 치환은 끝 자리 한정
- **낮음**: 설치 경로 `~/.claude/skills/...` 가정, `.browser_profile` 상대경로 기본값, mock 중심 테스트의 실브라우저 보장 한계

## 4시간 troubleshooting 교훈 (해결 순)

1. **이미지 카드 selector 버그** — antd CSS-in-JS hash wrapper(`div.css-3hsv0d`) 매치 실패 → `img.parentElement` + alt 매칭
2. **선택 카운트 정규식 false-match** — 페이지 전역 `0/8021200` 매치 → modal scope + 자릿수 제한
3. **참조 hydrate 부분 실패 (root cause)** — `dispatchEvent('click')` React state 부분 sync → DP CDP 트러스트 click 일괄 교체
4. **`is_saved` false negative** — `/create/complete` 이동 후에도 marker selector mismatch → urlMoved 단독 인정

## 저장소

- GitHub: https://github.com/Min-Gil-Sang/GFA-Setting
- 로컬 검증: `C:\Users\gguy\Desktop\GFA-Setting`
- 메인 코드: `_assembled/src/gfa_setting/`
- 테스트: `_assembled/tests/` (163/163, 커버리지 85%)
- E2E 보고서: `_assembled/E2E_TEST_REPORT.md`

## 관련

- [[domains/gfa-setting-automation]] — 메인 도메인 페이지
- [[domains/marketing-automation]] — 상위 도메인
- [[domains/ai-automation]] — 빌드 파이프라인 (bob/dd/harness/eval)
- [[qscv/media-gfa]] — GFA 매체 운영 기준

<!-- AUTO:tags-begin -->
**Tags**: #status/released #domain/marketing-automation #tech/drissionpage #tech/python #platform/naver-gfa #skill/gfa-setting
<!-- AUTO:tags-end -->
