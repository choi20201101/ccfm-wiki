# ccfm-wiki / skills

위키 동기화를 통해 모든 컴퓨터에서 동일한 Claude 스킬을 쓰기 위한 원본 보관소.
git clone → `install-*.ps1` 한 번 실행 → Claude Code + Desktop 양쪽에서 즉시 작동.

---

## 등록된 스킬

| 스킬 | 트리거 키워드 | 설치 스크립트 |
|------|--------------|---------------|
| [grill-me-ccfm](grill-me-ccfm/) | `grill해줘`, `꼼꼼하게 캐물어`, `방향 잡아줘`, `하지 말아야 할 거 정리`, 신규 시장·조직개편 등 되돌리기 어려운 결정 (강제 발동) | `install-grill-me-ccfm.ps1` |
| [codex-grounding](codex-grounding/) | (자동 발동) Claude/Codex/Gemini 호출 시 개인 메모리 + 위키 인덱스 grounding 강제 → 깡통 응답 방지 | `install-codex-grounding.ps1` |
| [feedfm](feedfm/) | `/feedfm`, `퍼포먼스 캔버스 피드백`, `진단 피드백 만들어`, `응시자 피드백 문서` → 진단 답안+점수 → 다크테마(검정·흰·핑크) 1페이지 피드백 HTML+PDF (캔버스 채점 루브릭) | `install-feedfm.ps1` |

---

## 새 컴퓨터 부트스트랩 (최초 1회)

```powershell
# 1. 위키 clone (이미 있으면 git pull)
cd $env:USERPROFILE
git clone <ccfm-wiki repo URL> ccfm-wiki   # 또는 기존 위치 사용

# 2. 스킬 설치 (복사 모드 — 안전, 권한 불필요)
cd ccfm-wiki\skills
.\install-grill-me-ccfm.ps1

# 또는 심볼릭 링크 모드 — git pull 시 스킬도 자동 갱신 (관리자 권한)
.\install-grill-me-ccfm.ps1 -Symlink
```

설치 후 Claude Code 또는 Desktop 재시작 → 시스템 스킬 카탈로그에 `grill-me-ccfm` 자동 등록.

---

## 작동 방식

1. **원본**: `ccfm-wiki/skills/<skill-name>/` (이 repo, git 동기화)
2. **활성 위치**: `~/.claude/skills/<skill-name>/` (Claude가 자동 로드)
3. **동기화 모드**:
   - **복사 (기본)**: install 스크립트가 매번 덮어쓴다. 위키 update 후 install 재실행.
   - **심볼릭 링크**: install 시 한 번 링크. `git pull` 만으로 스킬도 갱신.

---

## 새 스킬 추가 절차

1. `ccfm-wiki/skills/<new-skill>/SKILL.md` + 보조 파일 작성
2. `ccfm-wiki/skills/install-<new-skill>.ps1` 작성 (`install-grill-me-ccfm.ps1` 복제 후 경로 수정)
3. 이 README 표에 한 줄 추가
4. `wiki/HOTSHEET.md` 와 `wiki/index.md` 에 트리거 매핑 추가
5. `git commit && git push`
6. 다른 PC: `git pull && .\skills\install-<new-skill>.ps1`

---

## 트러블슈팅

### Claude Desktop 에서 인식 안 됨
- Desktop 종료 후 재실행 (스킬 폴더는 시작 시 1회 스캔)
- `~/.claude/skills/<skill-name>/SKILL.md` 가 실제로 존재하는지 확인
- SKILL.md 의 frontmatter 가 valid YAML 인지 확인

### `python` 명령이 안 움직임 (Windows)
- `python` 은 Microsoft Store 스텁일 가능성 높음
- 실제 경로: `C:\Users\<user>\AppData\Local\Python\bin\python.exe`
- 스킬 내부에서는 절대경로 또는 `py -3` 권장

### 심볼릭 링크 생성 실패
- "관리자 권한 필요" 에러 → 관리자 PowerShell 에서 재실행
- 또는 Windows 설정 → 개발자용 → "개발자 모드" 켜기
- 둘 다 어려우면 그냥 복사 모드 사용 (위키 변경 시 install 재실행)
