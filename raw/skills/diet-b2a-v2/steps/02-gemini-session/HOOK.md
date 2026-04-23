---
aliases: ["step-02 HOOK — 세션 보호 원칙"]
---

# step-02 HOOK — 세션 보호 원칙

## 왜 세션 관리가 중요한가
- Gemini 재로그인은 사용자가 직접 해야 함 (2FA, 이메일 확인) → 자동화 불가
- 1회 로그인 세션을 오래 재사용할수록 총 비용·시간 절약
- 세션 파일(`.session/*`)을 외부에 노출하면 계정 탈취 위험

## 안전 가이드
- `.session/` 은 `.gitignore` 대상
- `SingletonLock` 파일은 크롬 비정상 종료 시 남음 → 감지하고 자동 삭제
- 로그인 시 크롬창에서 **수동 로그인** 후 창 닫기 (login_once.py가 wait_for_event로 대기)

## 실수 방지
- headless 모드에서 로그인 시도 금지 (Google이 자동화 탐지해 차단)
- `accept_downloads=True` 필수 (다음 스텝에서 이미지 다운로드)
