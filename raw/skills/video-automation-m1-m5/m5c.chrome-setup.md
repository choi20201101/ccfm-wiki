# m5c Chrome 설정 (영상 생성)

## 고정값 (절대 변경 금지)

| 항목 | 값 |
|------|-----|
| user-data-dir | `C:/Users/{WINDOWS_USER}/AppData/Local/Google/Chrome/User Data M5C` (전용 폴더) |
| profile-directory | `Default` (본인 Google 계정으로 로그인) |
| port | `9223` |
| 실행 파일 | `C:\Users\{WINDOWS_USER}\Desktop\클로드\flow-video\start_chrome.py` |

---

## 실행 방법

```powershell
cd C:\Users\{WINDOWS_USER}\Desktop\클로드\flow-video
python -u start_chrome.py
```

---

## start_chrome.py 동작 (3-Case)

- **Case 1**: CDP 9223 이미 열림 → 아무것도 안 함, 즉시 종료 (Chrome 절대 건드리지 않음)
- **Case 2**: m5c Chrome(User Data M5C) 있는데 CDP 없음 → m5a 보호 후 종료 → 재시작
- **Case 3**: Chrome 없음 → fix_local_state + clean_session + fix_exit_type + launch

---

## 절대 하지 말 것

1. `USER_DATA_DIR`, `PROFILE_DIR`, `CDP_PORT` 값 변경 금지
2. `chrome-cdp-profile` 방식으로 되돌리기 금지 (로그아웃 원인)
3. `Preferences` 파일 JSON 파싱 금지 — 텍스트 replace만 사용
4. `kill_chrome()`에서 m5a Chrome(포트 9222 / User Data M5A) 종료 금지
5. `run.py` signal handler (`os._exit(0)`) 제거 금지

---

## m5a와 동시 실행

- m5a: `User Data M5A` + Default + 포트 9222 (완전히 다른 user-data-dir)
- m5c kill_chrome()은 m5a 프로세스 트리(메인+자식) 전체를 BFS로 수집해서 보호
- 두 Chrome이 독립 실행, 서로 간섭 없음

---

## 중지 시

```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
```
Chrome은 절대 닫지 않음.
