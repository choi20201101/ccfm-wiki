---
type: source
slug: nari-2tab-parallel
confidence: high
created: 2026-04-24
updated: 2026-04-24
project: nari (네리티아 세럼 파운데이션)
---

# 네리티아 2탭 병렬 워커 성공 사례 (2026-04-24 검증)

## 개요
1 Chrome 인스턴스 · 2 ChatGPT 탭으로 광고 이미지 병렬 생성. 사용자 요구 "크롬 하나만 작동하는데 두개로 해서 생산속도 높여줘" 에 대응한 구조.

## 왜 1 Chrome + 2 Tab 인가
- 1 Chrome 2 Profile (포트 9222/9223) 방식도 구현돼 있음 (`launch_chrome2.py`) 이지만, 사용자는 창 관리 부담 이유로 거부
- 같은 ChatGPT 계정이면 **계정 단위 image-gen cap** 이 묶이기 때문에 2 프로필 분리해도 속도 증가 미미 → 탭 방식이 자원 효율 우위

## 핵심 구현: `acquire_tab`

```python
# scripts/run_worker.py
def acquire_tab(ctx, worker_idx: int):
    cg = [p for p in ctx.pages if "chatgpt.com" in p.url]
    while len(cg) < worker_idx + 1:
        p = ctx.new_page()
        p.goto("https://chatgpt.com/", wait_until="domcontentloaded")
        time.sleep(2)
        cg.append(p)
    page = cg[worker_idx]
    try: page.bring_to_front()
    except: pass
    return page
```
- `worker 0` 은 첫 탭, `worker 1` 은 두 번째 탭 (없으면 생성)
- id 분배: `my_ids = [i for i in range(start, end+1) if (i-1) % total == worker]`
  - w0=홀수 id, w1=짝수 id

## 기동 명령

```bash
ROOT="C:\Users\Administrator\Desktop\nari"
PY="C:\Users\Administrator\AppData\Local\Python\bin\python.exe"

# 1) Chrome CDP 9222
"$PY" "$ROOT/scripts/launch_chrome.py"   # 첫 실행시 ChatGPT 수동 로그인

# 2) 워커 2개 동시 백그라운드
"$PY" "$ROOT/scripts/run_worker.py" --worker 0 --total 2 --start 1 --end 1000 \
    --aspects 1x1 --mode thinking --cdp-port 9222 \
    >> "$ROOT/state/logs/worker0_parallel.log" 2>&1 &

"$PY" "$ROOT/scripts/run_worker.py" --worker 1 --total 2 --start 1 --end 1000 \
    --aspects 1x1 --mode thinking --cdp-port 9222 \
    >> "$ROOT/state/logs/worker1_parallel.log" 2>&1 &
```

## 검증 결과
- 2026-04-23 22:41 ~ 2026-04-24 07:22 (8시간 40분) 40장 생성, 크래시 0
- 평균 13.4분/장 — **bottleneck은 ChatGPT 계정 image-gen cap**, 코드 아님
- rate-limit 발생 시 5회 exponential backoff (60→120→180→240→300s, 명시 모달이면 900s)

## 제약
- ChatGPT 계정 1개 cap 이 상한 → 2탭 병렬이어도 총 처리량은 단일 탭 × 1.3~1.5배 수준 (완전 2배 아님)
- 탭 하나가 rate-limit 모달에 걸려 있는 동안 다른 탭은 정상 동작 → 대기 시간 흡수 효과가 병렬 이점의 핵심

## 재개 런북
사용자가 "네리티아 소재 만들자" 트리거 시 위 `기동 명령` 3줄만 실행. 나머지는 `state/copies.json`, `state/checkpoint.json` 이 알아서 이어받음.

## 관련
- [[da-creative]] — 1000장 DA 자동 생산 프레임워크
- [[src-creative-autogen-framework]]
- [[feedback-reject-rules]] (메모리) — 심사 반려 5건 규칙
