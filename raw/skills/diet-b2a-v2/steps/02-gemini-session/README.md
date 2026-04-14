# step-02 · README

## 실행
```bash
python check_session.py
```
- exit 0 + `session_ok.flag` 생성 → 세션 유효, 다음 스텝 진행 가능
- exit 3 → 사용자가 로그인 필요:
  ```bash
  python C:/Users/gguy/Desktop/MD/gemini-imagegen/login_once.py
  ```
  크롬창이 뜨면 **cjm@ccfm.co.kr** 로 로그인 → Gemini 정상 작동 확인 → 창 닫기.

## 다음 스텝
→ [03-gemini-seeds](../03-gemini-seeds/)
