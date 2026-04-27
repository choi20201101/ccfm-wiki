---
source: srd 샤르드 멜라케어 광고 소재 자동 생성 운영 (2026-04-27)
confidence: high
linked: [[domains/ai-automation]] [[domains/da-creative]]
---

# ChatGPT 웹 UI 자동화 (playwright CDP) — 운영 lessons

ChatGPT 웹 인터페이스를 playwright CDP(Chrome 9222·9223 디버그 포트)로 자동 조작해 광고 소재를 1통당 1~3분에 1장씩 무한 생성하는 파이프라인. 2026년 4월 운영 중 발견한 셀렉터 변동성·다운로드 동기화 함정 정리.

## 1. UI 셀렉터는 매주 깨진다 — 자가 진단 스크립트가 1순위

ChatGPT는 데일리·위클리로 DOM 속성을 변경한다. 셀렉터를 코드에 박아두면 이번주에 잘 돌던 게 다음주에 0장 생성. 운영자는 **"실제 페이지에 가서 dump해 새 셀렉터를 직접 찾는" 진단 스크립트**를 항상 준비.

### 깨진 사례 — 2026-04-27 단일 세션 안에서 발견된 변경 3건

| 변경 전 | 변경 후 | 영향 |
|---|---|---|
| `[data-message-author-role="assistant"] img[src*="backend-api/estuary/content"]` | 해당 attribute 제거됨 → 매칭 0개 | 다운로드 함수가 빈 list 반환 → "dl fail" |
| `model-switcher-gpt-5-4-thinking` | `model-switcher-gpt-5-5-thinking` | thinking 모드 진입 실패 → 일반 GPT 응답 |
| `model-switcher-gpt-5-4-pro` | `model-switcher-gpt-5-5-pro` | Pro 모드 진입 실패 |

### 해결 — alt 텍스트가 가장 안정적

생성된 이미지 식별은 **`img[alt="생성된 이미지"]` (한국어) / `img[alt="Generated image"]` (영어)** 가 가장 오래 살아남는다. ChatGPT가 role/data-attribute는 자주 바꾸지만 사용자에게 보이는 alt 텍스트는 i18n 리소스라 변경 빈도 낮음.

```python
# chatgpt_client.py — 권장 셀렉터
SEL["generated_img"] = 'img[alt="생성된 이미지"], img[alt="Generated image"]'
```

### 진단 스크립트 패턴

CDP 포트 9222에 connect → 페이지의 모든 img/menuitem dump → 새 셀렉터 추출. 5분 안에 어떤 셀렉터가 깨졌는지 확정 가능.

```python
# scripts/_diagnose_menus.py — plus 버튼 + 모델 picker 메뉴 dump
items = page.evaluate("""() => {
    const wrapper = document.querySelector('[data-radix-popper-content-wrapper]') || document.querySelector('[role="menu"]');
    return Array.from(wrapper.querySelectorAll('[role="menuitem"], [role="menuitemradio"]')).map(it => ({
        role: it.getAttribute('role'), text: it.innerText, testid: it.getAttribute('data-testid'),
        state: it.getAttribute('aria-checked')
    }));
}""")
```

운영자는 셀렉터 깨질 때마다 이 스크립트 한번 돌리면 새 셀렉터 5분 안에 확정.

## 2. 다운로드 동기화 — "이미지 만들어졌는데 폴더 빈 채로" 함정

### 원인

ChatGPT 응답의 stop 버튼은 **텍스트 응답이 끝난 시점**에 사라진다. 그러나 이미지 생성 작업은 stop 후에도 백그라운드로 1~3분 더 진행. `wait_until_stopped` 통과 직후 이미지 카운트는 0이고, 짧은 timeout(120초)으로 `wait_image_thumbnail`을 호출하면 이미지 도착 전에 raise → 다음 cid → 새 채팅. 사용자 시점에서는 "분명 채팅에 이미지가 떠있는데 폴더는 비어있음".

### 운영 룰 (2026-04-27 사용자 합의)

> **다운 안 되면 새 채팅 띄우지 X**. 같은 채팅에서 5회 retry. 그래도 X면 cid skip (재시도 X, 새 채팅 X).

```python
# 5회 retry — 같은 채팅 안에서만
for retry in range(5):
    pngs = client.download_new_images(...)
    if pngs: break
    time.sleep(15)
# 마지막 fallback — baseline=0으로 페이지 전체 generated_img 시도
if not pngs:
    pngs = client.download_new_images(..., baseline=0)
# 그래도 X면 raise → main loop가 cid skip (new_conversation 호출 X)
```

main loop의 attempt 분기에서 `"dl fail"` 메시지는 **즉시 cid skip** — 새 채팅 시작하면 안 만들어진 이미지를 더 잃는다.

### 첨부 vs 생성 이미지 분리는 무조건 alt 또는 role 한정

`img[src*="backend-api/estuary/content"]` 만으로는 사용자 첨부 이미지(face·제품 누끼)가 같이 매칭됨. 같은 src prefix를 사용하므로. 분리 기준:
- 첨부: `alt="업로드한 이미지"` 또는 `[data-message-author-role="user"]` 안쪽
- 생성: `alt="생성된 이미지"` 또는 `alt="Generated image"`

이 분리를 안 하면 **첨부한 베스트 레퍼런스가 final 폴더에 픽셀 그대로 복사됨** (= ChatGPT가 생성 안 한 결과를 "성공"으로 기록). 2026-04-27 0001~0009 결과가 모두 이 함정.

## 3. 좀비 워커 — 한 chrome에 여러 명령이 중첩되면 새 채팅이 미친듯이 떠오름

`run_worker.py`를 background로 띄우다가 죽었다고 생각하고 또 띄우면, 이전 인스턴스가 살아있어서 한 chrome 탭(9222)에 두 워커가 동시에 명령. 결과: "이미지 생성 중인데 새 채팅 또 시작됨" → 사용자 분노.

### 운영 체크 — 워커 재시작 전 항상 PID 점검

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object {$_.CommandLine -like "*run_worker*"} |
  Select-Object ProcessId, @{N='Cmd';E={$_.CommandLine.Substring(60,80)}}
```

탭당 워커 1개만 살아있어야 한다. 이상이면 `Stop-Process -Id X -Force`.

`taskkill /F /PID …`은 git bash에서 `/F`를 경로로 오인해 실패한다 — PowerShell `Stop-Process`로 죽이는 게 안전.

## 4. 일관성 함정 — 메모리 룰만 믿지 말고 코드도 확인

CLAUDE.md / 메모리에 "셀렉터는 alt='생성된 이미지'를 쓴다"고 적혀 있어도 실제 코드(`chatgpt_client.py SEL[...]`)와 다를 수 있다. 메모리는 어떤 시점의 약속, 코드는 현재 상태. 매 운영 시작 시 두 가지 일치 여부 grep으로 확인.

```bash
grep -n "generated_img\|menu_thinking\|menu_pro" chatgpt_client.py
```

## 5. 광고 도메인 운영 메모

샤르드 멜라케어 광고 자동 생성 컨텍스트에서:
- ChatGPT가 **첨부 베스트 이미지의 카피 텍스트를 그대로 복사하는** 경향이 강함. prompt에 "베스트는 시각·구도·인물·컬러 참고용. 텍스트는 모두 무시" 명시 필수.
- 광고주 반려 어휘(박피팩·뜯어내·흑자·시꺼먼·B/A)는 **이미지 안에 그려지면 안 됨** — prompt 상단에 "다음 단어를 이미지에 절대 그리지 마세요" 섹션을 두고 명시. ChatGPT가 베스트의 카피를 모방하려는 충동 차단.
- 카피 룰 "메인 1 + 서브 2~3개" 는 **반복·강조 없이는 무시당함**. prompt에 3번 이상 다른 표현으로 못박는다.

## 6. 디버깅 동선 — 막히면 진단 스크립트로

증상별 진단 명령:
- "이미지 안 만들어짐" → `_diagnose_menus.py 9222` (image-mode·model 셀렉터)
- "이미지는 있는데 다운 안 됨" → `_diagnose_chat_url.py <url> 9222` (alt 매칭·src 추출)
- "베스트가 그대로 복사됨" → `_diagnose_chat_url.py` 로 USER vs ASSISTANT 이미지 분리 확인
- "워커가 미친듯이 새 채팅 띄움" → PID 점검 (좀비 동시 실행)

`_save_all_open_chats.py` — 모든 chrome 탭의 ChatGPT 채팅에서 생성 이미지를 자동 다운(파이프라인이 놓쳤을 때 복구).

---

## 출처·날짜

- 2026-04-27 srd 샤르드 멜라케어 필크림 마스크 광고 100장 자동 생성 운영 1차
- 발견자: 운영자 + Claude Opus 4.7 (1M context)
- 코드 경로: `C:\Users\Administrator\Desktop\srd\scripts\chatgpt_client.py`, `run_worker.py`
