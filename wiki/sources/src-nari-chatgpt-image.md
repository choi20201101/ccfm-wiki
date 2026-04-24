---
title: 네리티아 ChatGPT 웹 이미지 생성 파이프라인 — 2탭 병렬 워커 표준 패턴
source: C:\Users\Administrator\Desktop\nari (원본 프로젝트)
created: 2026-04-26
confidence: high
tags: [nari, chatgpt, playwright, cdp, 광고자동화, 네리티아, 2탭병렬]
---

# 네리티아 ChatGPT 웹 이미지 생성 파이프라인

## 개요
- **제품**: 네리티아 세럼 파운데이션 (Neritia Serum Foundation, SPF50+ PA++++, 30ml, 그린코스(주) 제조)
- **방식**: Playwright + Chrome.exe CDP 9222 → ChatGPT 웹 UI 이미지 생성 1샷 → PIL 후처리 → 1200×1200 JPG
- **진입점**: `C:\Users\Administrator\Desktop\nari\`
- **CCFM wiki에 없던 원본 지식** → 이 문서로 승격 (사용자 지시 2026-04-26)

## 표준 패턴 — 2탭 병렬 워커 (검증됨 2026-04-26)

### 왜 2탭·1크롬·1계정인가
- ChatGPT 계정 1개 (`ceo@mkm20201101.com`) 를 2개 크롬 인스턴스로 동시 접속 → **세션·rate-limit 충돌**. 프로필(`chrome_profile`, `chrome_profile2`) 분리해도 **같은 계정**이면 경합 발생.
- 2026-04-26 실측: 크롬 2개 분리 시도 → 두번째 크롬 "미로그인" 상태로 워커 fail.
- **결론: 1 크롬 인스턴스 (포트 9222) + 탭 2개** 가 유일한 안정적 병렬.

### id 분배 로직 (`run_worker.py:379`)
```python
my_ids = [i for i in all_ids if (i - 1) % args.total == args.worker]
```
| 탭 | `--worker` | `--total` | 처리 id | 비고 |
|----|-----------|-----------|---------|------|
| 탭1 | 0 | 2 | 홀수 (1, 3, 5, ...) | `acquire_tab(ctx, 0)` 첫 탭 |
| 탭2 | 1 | 2 | 짝수 (2, 4, 6, ...) | `acquire_tab(ctx, 1)` 두번째 탭 |

**"라인 물리 분리" 불가 원인**: `worker=1` 사용하려면 `acquire_tab(ctx, 1)`로 탭2 잡아야 하는데, id 분배가 `(i-1) % total == worker` 라 `total=1, worker=1`이면 매칭 0개. 즉 탭2 전담 워커는 **분배 로직 패치 없이 불가**.

**라인 구분 원칙**: **id 번호대로 결과물 식별** (예: `state/copies.json` 에 `id 1~1000`은 기존 생산 라인, `id 1001~1035`는 시장조사 기반 시드 등). 물리 탭 분리 대신 데이터 분리.

### 표준 실행 스니펫
```bash
ROOT="C:\Users\Administrator\Desktop\nari"
PY="C:\Users\Administrator\AppData\Local\Python\bin\python.exe"

# 1. CDP 살아있는지
curl -s -m 3 http://localhost:9222/json/version

# 2. 없으면 크롬 기동 (프로필 유지면 ChatGPT 자동 로그인)
"$PY" "$ROOT/scripts/launch_chrome.py"

# 3. copies.json 실제 max id
END=$("$PY" -c "import json; d=json.load(open(r'$ROOT/state/copies.json',encoding='utf-8')); print(max(x['id'] for x in d))")

# 4. 2탭 동시 기동 (반드시 background)
"$PY" "$ROOT/scripts/run_worker.py" --worker 0 --total 2 --start 1 --end $END --aspects 1x1 --mode instant --cdp-port 9222 >> "$ROOT/state/logs/worker0_parallel.log" 2>&1 &
"$PY" "$ROOT/scripts/run_worker.py" --worker 1 --total 2 --start 1 --end $END --aspects 1x1 --mode instant --cdp-port 9222 >> "$ROOT/state/logs/worker1_parallel.log" 2>&1 &
```

### `--mode instant` 권장 (2026-04-26)
- ChatGPT UI 업데이트로 `chatgpt_client.py` 의 selector `menu_thinking` / `menu_instant` / `menu_pro` (구 `gpt-5-4-*` / `gpt-5-3`) 가 실제 DOM 과 불일치.
- `--mode thinking` 지정해도 실제 로그: `[thinking-mode] all openers failed — continuing without thinking` → 자동으로 기본(5.5) 모드로 동작.
- 실측: thinking 없이도 품질 충분 + 생성 속도 단축 → **--mode instant 가 표준**.

## 심사 반려 5대 규칙 (브랜드 오염 방지)
`C:\Users\Administrator\Desktop\nari\scripts\pipeline.py:831` `_FORBIDDEN_SUBS` 반영됨.

| 반려 사유 | 구현된 회피 방법 |
|-----------|------------------|
| 신체 매크로 확대 (피부·모공·주름 매크로) | 얼굴 전체/반신 구도만, `refs/face/` 중안부 비율 유지 |
| 1위·KCAI 순위 주장 | `1위 → 주목`, `KCAI → 누적 200만개` 치환 |
| B&A 전후 비교 | `before/after → 사용 효과`, `전/후 → 후` |
| 가슴골 노출 | 모델 프롬프트에서 깊은 V넥·오픈 셔츠 배제 |
| 피부과 입점 / 청담 / 의사·박사 | `피부과 → 관리실`, `청담 → 동네 뷰티샵`, `피부과학연구소 → 자체 임상센터`, 의사·박사·FDA·KCAI·전문의·병원전용 단어 자체 차단 |

## 레퍼런스 폴더 구조
| 경로 | 용도 | GPT 첨부? |
|------|------|-----------|
| `refs/pd/` | 제품 누끼 | ✅ 항상 |
| `refs/face/`, `refs/face/jung/` | 얼굴 레퍼 (중안부 짧은 동안 미인) | ✅ 테마별 |
| `refs/best/*.jpg` | **레이아웃 벤치마크 하드코딩** (pipeline.py:659, 1385 에서 특정 파일명 참조) | ✅ 테마별 |
| `refs/best2/` | 타 카테고리 베스트 70+ | ❌ (현재 미사용) |
| `refs/youtube/` | 유튜브 썸네일 수집 (레이아웃·분위기 참고만) | ❌ (자동 첨부 X) |
| `refs/market/` | 시장조사 산출물 (4050_mood_report·authority_archetypes·cafe/insta summary) | ❌ (참고 문서) |

## 시장조사 기반 시드 확장 워크플로 (2026-04-26 검증)
1. 서브에이전트 병렬 디스패치 (general-purpose) → `refs/market/*.md` 산출물
2. 산출물의 시드 카피를 `copies.json` 끝에 id append (예: 1001~1035)
3. `--end` 값을 새 max id 로 확장해 2탭 워커 재기동
4. 신규 시드도 홀짝 분배로 자동 포함 처리

## 2026-04-26 이후 검증 이력
- 서브에이전트 3종 병렬: Instagram (로그인월로 0건), Cafe (16건 + 인사이트 7블록), 4050Mood (H섹션 시나리오 15), Authority (아키타입 15·신규 cut_type 4종 제안)
- 시드 35개 추가: H시나리오 15 + Cafe 카피앵글 5 + Authority 아키타입 15
- 재기동 후 통합 풀 id 1~1035 2탭 병렬 처리 안정 확인

## 관련 메모리
- `project_nari_pipeline.md` — nari 프로젝트 전체 운영 경로
- `project_nari_runbook.md` — 즉시 세팅 런북 (트리거 발화 기반)
- `feedback_reject_rules.md` — 심사 반려 5건 상세
- `feedback_copy_quality.md` — 카피 품질 기준 (판타지 서사 금지)
- `project_neritia.md` — 세럼 파운데이션 상세 스펙

## 후속 승격 후보
- 시장조사 서브에이전트 프롬프트 템플릿 → `wiki/skills/` 로 승격
- 간접 권위 아키타입 15 → `wiki/tacit/` 로 승격 (다른 뷰티 브랜드 재활용 가능)
