# m5a Chrome 설정 (이미지 생성)

## 고정값 (절대 변경 금지)

| 항목 | 값 |
|------|-----|
| user-data-dir | `C:/Users/{WINDOWS_USER}/AppData/Local/Google/Chrome/User Data M5A` (별도 폴더) |
| profile-directory | `Default` (본인 Google 계정으로 로그인) |
| port | `9222` |
| 실행 파일 | `C:\Users\{WINDOWS_USER}\Desktop\클로드\flow-gen-pkg\src\browser.py` (run.py가 자동 호출) |

---

## 실행 방법

run.py 실행 시 `ensure_chrome()`이 자동으로 Chrome 상태를 보장함.
수동으로 열려면:

```powershell
cd C:\Users\{WINDOWS_USER}\Desktop\클로드\flow-gen-pkg\src
python -u browser.py
```

---

## browser.py 동작 (3-Case)

- **Case 1**: CDP 9222 이미 열림 → 아무것도 안 함, 즉시 반환
- **Case 2**: m5a Chrome(User Data M5A) 있는데 CDP 없음 → m5a Chrome만 종료 → 재시작
- **Case 3**: Chrome 없음 → fix_local_state + clean_session + fix_exit_type + launch + 자동 Chrome 시작

---

## 절대 하지 말 것

1. `USER_DATA_DIR`(`User Data M5A`), `PROFILE_DIR`(`Default`), `CDP_PORT`(`9222`) 변경 금지
2. `chrome-cdp-profile` 방식으로 되돌리기 금지 (로그아웃 원인)
3. `Preferences` 파일 JSON 파싱 금지 — 텍스트 replace만 사용
4. `run.py` signal handler (`os._exit(0)`) 제거 금지

---

## m5c와 동시 실행

- m5c: `User Data M5C` + Default + 포트 9223
- m5a: `User Data M5A` + Default + 포트 9222
- 완전히 다른 user-data-dir → 충돌 없음

---

## 초기 로그인

`User Data M5A`는 처음 실행 시 새 Chrome 프로필로 시작됨.
본인 Google 계정으로 1회 로그인 → 이후 세션 자동 유지.
labs.google/fx 에 접속해서 로그인 완료 확인 후 Claude Code 터미널로 복귀하면 됨.

---

## 중지 시

```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
```
Chrome은 절대 닫지 않음.
