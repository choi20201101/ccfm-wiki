# CCFM Wiki Log

## [2026-05-26] ingest | Gemini Omni (Omni Flash) 사용 가이드 — Google Flow 멀티모달 영상 모델
- 소스: 노션 페이지 [Gemini Omni 가이드](https://synonymous-nation-db3.notion.site/Gemini-Omni-367239465f12805b9acdcb50907338a5)
- 로컬 미러: `C:\Users\gguy\Desktop\omni\` (HTML 가이드 + 영상 34개·이미지 27개 + manifest.json, 약 125MB)
- source: `wiki/sources/src-gemini-omni-guide.md` (전체 워크플로 9종 + 프롬프트 + 한계 정리)
- 도메인 업데이트: [[ai-automation]] §Omni 항목 신설, [[da-creative]] §툴/플랫폼에 v2v 1스텝 합성 효과 등록
- 핵심:
  - **포지셔닝**: Seedance = 0→1 생성 / Omni = 기존 영상 수정·변형 + 누끼 1스텝 합성. 분업이 답.
  - **워크플로 9종**: 영상 내 이미지 합성 / 행동·배경·복장·앵글 변경 / 목소리 변경 / 캐릭터 에셋 일관성 / 실무 (착한구두 럭셔리 패션 에디토리얼 5변주 케이스).
  - **CCFM 임팩트**: 기존 [[da-creative]] 2스텝 워크플로(이미지 합성 → I2V) → 1스텝 압축. 캐릭터 에셋으로 B&A 시리즈 일관성 확보.
  - **한계 3종**: 한국어 글씨/제품 글씨 왜곡/스토리보드 해석 — 후처리 또는 더 명확한 프롬프트로 회피.
  - 영상 본 파일은 위키 레포에 푸시 X (125MB, LFS 미사용) → 로컬 미러로만 보관.

## [2026-05-20] ingest | 위너소재 ffmpeg 트랜지션 + ChatGPT 이미지 레퍼런스 질문 답변 정리
- 직원 → 대표 문의 2건: (1) ffmpeg 트랜지션 커스텀 가능 여부 (2) ChatGPT 이미지 레퍼런스 직접 입력 vs 자동 학습
- raw: `raw/inbox/2026-05-20-winnersojae-higgsfield-chatgpt-image-questions.md` (원문 캡처)
- source: `wiki/sources/src-winnersojae-feedback-2026-05-20.md` (위키 기반 답변 정리 + 직원 답신 초안)
- 핵심 메시지:
  - Q1: ffmpeg `xfade` 50종 + `custom` expression + GL Transitions로 충분히 커스텀 가능. 그러나 "빠른 템포에서 편집점 약함"은 트랜지션 문제가 아니라 [[tacit/video-gen-lessons]] §35·§36 의 "씬 길이를 TTS char-level timestamp에 동기화" 미적용 문제일 가능성 큼.
  - Q2: ChatGPT 이미지는 진짜 학습 안 됨. 레퍼런스 직접 입력 유지 + "visual template, not inspiration" 명시 강화 + 다양성은 18축 cid 시드 결정론 풀 회전으로. "진짜 학습" 원하면 Flux LoRA(Higgsfield Brand Kit) 별도 검토.

## [2026-05-14] ingest | GFA-Setting v0.1.x — 멀티 잡 큐 + rwc 캘린더 + 디버그 pause
- 소스: `C:\Users\gguy\Desktop\GFA-Setting` master HEAD (commit 75472ff + 미커밋 작업트리)
- domain: `wiki/domains/gfa-setting-automation.md` 에 §v0.1.x 업데이트 (2026-05-13~14) 신설 — (A) rwc 가상 스크롤 캘린더 대응 + `GFA_DEBUG_PAUSE_ON_ERROR=1` 라이브 디버깅, (B) 멀티 잡 큐 (입력 페이즈 `collect_group_setup_spec` + 실행 페이즈 `execute_group_setup`, `GroupSetupSpec` frozen dataclass, `JOB_COOLDOWN_SECONDS=30`, 잡 단위 격리)
- 플레이북: §"UI 변경 / 셀렉터 깨짐 대응" 에 §0 디버그 pause 모드 추가 + §8.4 rwc 캘린더 사례 추가
- index/HOTSHEET: GFA 카드 v0.1.x 변경 반영 (멀티 잡 큐 / 30초 cooldown / rwc / 디버그 모드)
- 의도: 단일 잡 흐름이 v0.1.0 의 한계였음 — 같은 계정에 콘텐츠/캠페인 다른 잡들이 자주 발생 → 입력 한 번에 끝내고 잡 단위 commit. 첫 GFABrowserError 살린 채 DOM 검사할 수 있어야 셀렉터 깨짐 디버깅 속도가 단축됨.

## [2026-05-14] ingest | 피코세라 1차 하네스 (광고 소재 검수 루브릭) + ad-bdh 스킬
- raw: `raw/skills/picosera-harness/` (rubric-v1.md + SUMMARY.md)
- source: `wiki/sources/src-picosera-harness-v1-2026-05-14.md` — 체크리스트 25항목 + 17규칙 (0~5점)
- domain: `wiki/domains/da-creative.md` "소재 검수 하네스" 섹션 / `wiki/domains/ai-automation.md` "ad-bdh 스킬"
- tacit: `wiki/tacit/creative-patterns.md` "소재 점수 판정 기준" 추가 (confidence: medium)
- index/HOTSHEET: "피코세라 하네스 기준으로 필터링해줘" 트리거 등록
- 의도: 트리거 한 줄로 소재를 1차 루브릭으로 분류·필터링. 기준은 v2로 교체 가능(멀티패스).

## [2026-05-12] ingest | Higgsfield CLI ↔ Claude Code 연동 가능성 + ggttt 식 우회 불가 (3중 교차검증)

- 출처: 사용자 질문 "higgsfield.ai/cli 클로드 연동? ggttt 같은 우회? Seedance 2.0 + 웹 SaaS?"
- **3중 평가 절차**: Claude(Opus 4.7) 초안 → Codex frontier(gpt-5.4 xhigh) cross-check → general-purpose 서브에이전트 가혹 eval
- **핵심 결론**:
  - Q1 연동: ✅ 공식 `@higgsfield/cli` + `npx skills add higgsfield-ai/skills` 또는 공식 MCP (`https://mcp.higgsfield.ai`). 단 npm 패키지 first publish 2026-05-02 (10일 된 베타, 9일에 18 릴리즈) → 프로덕션 의존 위험
  - Q2 ggttt 우회: ❌ 불가. Higgsfield 는 자체 OAuth + 자체 크레딧제, ChatGPT entitlement 재활용 표면 없음. 합법 무료 경로는 가입 보너스 + 월 150cr 무료 티어 (메라블 광고 1편 330cr 못 함)
  - Q3 Seedance 2.0: ✅ 지원. **단 plan 자격 충돌**(본문 "모든 플랜" vs FAQ "Team 전용") + CLI 스키마에 `--seed` 미노출 → `perf-ad-library` 컷별 재현성 워크플로에 치명. 약관상 입력/출력 학습 활용 가능 → 브랜드 자산 PoC 금지
- **수정한 Claude 초안 오류**:
  - MCP 출시일 "2026-04-30 확정" → "2026-04-말~5-08, 공식 1차 못 박기 어려움"
  - "Higgsfield = 어그리게이터 마진" → "OpenAI/Google/ByteDance 파트너 위에 자체 모델 + proprietary reasoning engine"
  - 월 가격 "$20+" → 직접 검증 안 됨, credit-based 만 확실
  - `QalaLabs/claude-higgsfield-mcp` → 실재 미확인. `AKCodez/higgsfield-claude-skills` 만 검증됨
  - "ggttt 우회 절대 불가" → "현재 공개 표면 기준 불가" (단정 톤 약화, 실용 결론 동일)
- **권고**: fal.ai Seedance 직접 호출 유지. Higgsfield 는 신모델 탐색/Marketing Studio/Brand Kit/Virality Predictor 보조 실험만. 첫 액션 = 무료 가입 + 퍼블릭 도메인 이미지로 Seedance 5초 1클립 fal.ai 1:1 비교
- 갱신: [[sources/src-higgsfield-cli-claude-bypass-2026-05-12]] (10개 섹션, 교차검증 결과 포함), [[HOTSHEET]] 트리거 행 추가
- 메타: 본 PC OAuth 환경에서 `gpt-5.5-pro` 거부 확인(ChatGPT 계정 불가). codex 차상위 = frontier(5.4 xhigh) 가 실용 최대치

## [2026-05-12] ingest | todayhumor-mining-playbook — 오늘의유머 → 광고 소재 1:1 변환 파이프라인

- 출처: picosera/new/todayhumor_ideas/ 실전 운영 (2026-05-11~12 진행, 614/1469 시점 중단)
- 위치: wiki/domains/todayhumor-mining-playbook.md
- 핵심: Best of Best 추천 N+ 게시물 → Gemini SDK Vision → 게시물 1개 = 폴더 1개 = 아이디어 1개 (idea.md + src + gen)
- 브랜드 보이스 주입: 후킹 패턴 A~F(시간/비용·생활페인·충동전환·숫자임상·후기인용·페르소나) + 식약처 금지 표현 + 시그니처 표현 추출
- 운영 성과: brand_fit=high 519/614 (84.5%), humor_axis TOP=반전(272), 공감(66), 의외성(61)
- 교훈 cross-ref (tacit/coding-lessons.md 추가):
  - [2026-05-12] Gemini CLI는 자동화 파이프라인에 부적합 → SDK 직호출 (confidence: high)
  - [2026-05-12] Windows Git Bash + nohup/&는 신뢰 X → schtasks `cmd.exe /c` 래퍼 (confidence: high)
  - [2026-05-12] 오늘의유머 리스트 파서 `tr.list_tr_humordata` + `td.subject a` 정답 (confidence: high)
- cross-ref: domains/marketing-automation.md, domains/da-creative.md, HOTSHEET 트리거 추가
- confidence: high (실제 614건 안정 처리, brand_fit high 비율 84.5%)

## [2026-05-11] ingest | wmux/wmux-orchestrator 흡수 (멀티 에이전트 안정화 6패턴)

- 외부 레포: amirlehmam/wmux + wmux-orchestrator (Claude Code 가시성 + dependency-aware wave)
- 본체(Electron UI)는 무시, orchestrator의 6패턴만 흡수
- 6패턴: Shared Contract / allowed_files frontmatter / Auto-fix 권한 화이트리스트 / 3단 권고 시그널 / Wave-DAG 실행 / 환경 감지 + 혼용 금지
- 적용 스킬: dd, dd-executor, eval, multi-llm-orchestrator + commands(parallel, subagent, review)
- 핵심 인사이트: ①Coupling 해결 3가지(병합/wave분리/contract) ②자동수정 권한은 좁고 명시적이어야 ③모드 혼용 금지(가시성과 학습성은 직교축)
- confidence: low (1회, 가설) — 실전 검증 전, Codex CLI quota 한도로 단독 분석
- 추가 위치: wiki/tacit/coding-lessons.md §2026-05-11, wiki/domains/vibe-coding.md (🆕 최근 흡수 섹션)

## [2026-05-05] ingest | Codex grounding protocol — 3-CLI 깡통 응답 방지 시스템

- 출처: 사용자 요청 "코덱스 호출될 때 메모리 인덱스랑 wiki 지식 교훈 기반으로 피드백/리뷰. 깡통 코덱스 의미없으니 강제 설정"
- **문제**: Claude/Codex/Gemini 3-CLI 가 각자 dotfile(`CLAUDE.md`/`AGENTS.md`/`GEMINI.md`) 자동 로드하지만, 메모리/위키를 **읽으라고 강제하는 절차** 없어 LLM이 "기억나는 대로" 답변. 사용자가 거른 함정(`feedback_*.md`) 반복.
- **해결 (3-layer defense in depth)**:
  - **Layer 1 — 헬퍼**: `~/.codex/scripts/context-bootstrap.mjs` (Node.js). prompt → 한국어 조사 trim + stop word 필터 → MEMORY.md/HOTSHEET.md 토큰 매칭 → `<context_grounding>` 블록 출력.
  - **Layer 2 — dotfile MANDATORY PRE-WORK PROTOCOL**: 3개 dotfile 최상단에 marker(`<!-- BEGIN: codex-grounding-protocol v1 -->`) 으로 감싼 4단계 절차(헬퍼 → fallback grep → 매칭 파일 로드 → `📚 참조:` 첫 줄 표시).
  - **Layer 3 — orchestrator.py inject**: `multi-llm-orchestrator/scripts/orchestrator.py` 의 ask/review/fix/debate/consensus 5모드 모두에서 `_grounded(prompt, source)` 헬퍼로 `<context_grounding>` 블록을 prompt 앞에 prepend. 비활성화: env `MLLM_SKIP_GROUNDING=1`.
- **Opus 4.7 review로 즉시 반영된 P0/P1**:
  - P0: `orchestrator.py` 가 forwarding 시 grounding 미주입 → 5모드 모두 깡통이었음. `build_grounding()` 헬퍼 + `_grounded()` 래퍼 추가하고 ask/review/fix/debate r1/consensus r0 patch.
  - P1: 한국어 조사 미분리(`feedback이` → 매칭 실패). `KOR_PARTICLES` regex로 token 끝에서 trim. 의문/명령형 어미("어떻게"/"뭐야"/"해줘"/"만들어줘") stop word 추가.
- **다른 컴퓨터 portability**: 헬퍼는 `$USERPROFILE`/`$HOME` 자동 해석. env `CCFM_WIKI_ROOT`, `CCFM_MEMORY_INDEX` 또는 `~/.codex/AGENTS.local.md` 의 `KEY=...` 1줄로 override. 1줄 install: `git clone <wiki> && cd skills && .\install-codex-grounding.ps1` (marker-based idempotent, 백업 자동).
- 갱신: [[domains/codex-grounding-protocol]] (신규 도메인 페이지), [[HOTSHEET]] 트리거 행 추가, `skills/codex-grounding/` 신규(헬퍼 + 3개 protocol fragment + install ps1), `skills/README.md` 표 추가.

## [2026-05-04] ingest | 루비알엔 v6_hero 액션 광고 4대 함정 — ChatGPT 웹 우회 + cut 캐시 + TTS 리듬 + 광고 QA

- 출처: 2026-05-04 루비알엔 v6_hero (12컷 원펀맨 톤 액션 영웅 광고) 재작업. 1차 빌드 후 사용자 컴플레인 4건 동시 발생 → 풀 재빌드 케이스
- **(A) ChatGPT 웹 자동화로 god-tibo-imagen API 한도 우회** — `playwright launch_persistent_context` + 시스템 Chrome (`channel='chrome'`) + 자동화 감지 우회 인자. 이미지 다운로드는 `page.on('response')` **네트워크 가로채기로만 작동** (DOM `<img>`, conversation API 모두 실패). ChatGPT가 매번 캐릭터 시트(고정 `4883567 bytes`) + 실제 장면 둘 다 생성 → 캐릭터 시트 명시 제외 + ref hash/size 제외 + 2MB 미만 제외 + 남은 것 중 가장 큰 것 = 실제 장면. 한국어 프롬프트로 "캐릭터 시트나 여러 패널 절대 안 됨, 단일 장면 일러스트만" 강하게 명시
- **(B) build_video_v2 cut 캐시 함정** — `make_cut_motion()` 첫 줄 `if exists: return out` 때문에 SCRIPT/SPEED 변경 후 재빌드해도 옛날 cut_XX.mp4 그대로 사용. 재빌드 시 `_work_v{N}/cut_*.mp4` + `03_audio/full_v{N}*` + `03_audio/cues_v{N}*` 반드시 삭제 (디렉토리 통째 rm -rf 는 'busy' 자주 남, 파일 단위로)
- **(C) TTS 리듬 baseline 재확정** — 액션/임팩트 광고는 **SPEED=1.05 + MAX_SIL=0.30** (검증: v6 1.05+0.30 → 23.5s ✓). SPEED 0.8대로 길이 늘리면 무조건 "늘어진다" 컴플레인. 진단법: cue ratio `(end-start)/(raw_end-raw_start)` 1.15 초과면 음성 자체가 늘어진 것
- **(D) 광고 QA 3대 필수 (사용자 명시 피드백)** — ① 제품 누끼 = 실제 제품 (`pd1.png` 직접 ref, `product_master.png` 는 스타일 통일용일뿐 누끼 보존용 아님), ② 한글 텍스트 무결 (이미지 프롬프트에 한국어 텍스트 그리기 요구하면 깨짐 70%+, 자막은 ffmpeg ASS 단계로만), ③ TTS 늘어짐 금지
- 갱신: [[tacit/video-gen-lessons]] §50, [[tacit/chatgpt-web-automation]] §7 (영구 프로필 + 네트워크 가로채기 패턴, CDP 모델과 비교)
- 코드 위치: `pipeline/open_chatgpt.py`, `pipeline/gen_via_chatgpt.py`, `pipeline/dl_via_network.py`, `pipeline/_chrome_profile/`

## [2026-05-03] ingest | 샤르드 cid 3001~6000 18축 자동 광고 시스템 정본 — 자극 카피 7대 후킹

- 출처: 샤르드 CHARDE 멜라케어 필크림 마스크 cid 3001~6000 광고 3000장 운영 (2026-04-30~05-03)
- **18축 cid 시드 결정론** (`_div_rng = random.Random(cid * 31337 + 11)`): 모델 8축 + 권위·증거 2축 + 카피 8축 모두 동일 RNG → 재현성 + 다양성 동시
- **자극 카피 7대 후킹 패턴 (자연 문장체)**: 인용+인지차이 / 역접·반전 / 인과·결과 / 관계·인용추천 / 시간·장면 / 단톡 인증 / 민간요법 vs 본품
- **풀 사이즈 × 0.06 ≈ cap** 공식: 3000장 운영 시 풀 100·cap 6 = sub max repeat 9x (이전 풀 50 → 15x 의 40% 개선)
- **sub_review 30%→100% 강제**: 페르소나 후기 확률 룰 폐기 (70% 빈 카피 폭증 원인)
- **사용자 분류 폴더 보존 룰**: ckpt 등록 cid 카피 무조건 보존 (사용자 노력 보존)
- 신규 페이지: [[sources/src-charde-cid-3001-6000-axis-system-2026-05-03]]
- 갱신: [[tacit/creative-patterns]] §광고 카피 자극 패턴 (자극 7대 후킹 + 풀 사이즈 룰 + 18축 결합 + 보존 룰)

## [2026-04-30] ingest | GFA-Setting max-mode 교차 감사 (Codex 5.5 max + Claude 서브에이전트)

- 두 독립 evaluator 병렬 감사 후 file:line 직접 검증 → 수렴/발산 정리
- **두 감사 모두 수렴(가장 신뢰)**: antd CDP 트러스트 약속 위반, secrets=[] 마스킹 무력화, partial 자동정리 0, naive datetime, 죽은 코드(mappings/models 빌더/prompts/requests 등) 6개 항목
- **Codex 5.5 max 추가 발견(검증됨)**: `browser.py:79` auto_handle_alert(accept=True) 의도외 confirm 자동수락, `ad_sets.py:410-416` 달력 월이동 미지원, operations 내부 _pause 환경변수 무시(.env delay 옵션 무력화), `(x=10,y=10)` 고정좌표 click, 새 그룹명 충돌 사전조회 0, 진단 dump 폼값 평문 저장
- **Claude 서브에이전트 추가 발견(검증됨)**: `materials.py:672` urlMoved 정규식(`/done|/complete`) word-boundary 없음 → `/da/dashboard?type=complete` false-positive, `exceptions.GFAAPIError/GFAUploadError` 정의만 0 사용, `dd/step-01.../output/` 56 git-tracked prototype 잔재
- **거짓 클레임 기각**: 서브에이전트의 "`_assembled/.venv` git tracked" → 루트 `.gitignore:2` `**/.venv/` 매치로 ignored 확인 (`git check-ignore -v` 통과)
- **최종 분류**: 릴리스 차단 5건(antd 트러스트/마스킹/partial 출력/urlMoved 정규식/auto_handle_alert) + v0.2 차단 5건(timezone/_pause 환경변수/fingerprint/그룹명 충돌/달력 월이동) + 백로그 6건(죽은 코드/dd output/셀렉터 중앙화/dump 디렉토리·마스킹/단독 보호 파일/실브라우저 스모크)
- 갱신: [[domains/gfa-setting-automation]] §최종 max-mode 교차 감사

## [2026-04-30] ingest | GFA-Setting 위키 보강 — 코덱스 2차 감사 + UI 깨짐 대응 플레이북

- 코덱스(gpt-5) CLI 2차 감사: 죽은 코드 + 방향성 위험
  - 죽은 코드 (직접 grep 검증): `mappings/` 폴더, `models.py:76,83,133,141` 의 4개 빌더 클래스, `pyproject.toml` 의 `requests/responses` 의존, `dd/step-01.../output/` 중복본 — 모두 src import 0건
  - 방향성: DrissionPage 단일 장애점, 셀렉터 분산(README 중앙화 약속과 불일치), 진단 dump cwd 직쓰기, partial rollback 0, 소재 이미지 전용, 테스트 mock 중심
  - v0.2 우선순위 7개 명문화 (죽은 코드 제거 → 셀렉터 중앙화 → diag 디렉토리화 → orphan 자동 정리 → CLI partial 출력 → secrets 주입 → 단독 보호 파일)
- UI 깨짐 대응 플레이북 8단계 추가:
  - diag dump 5종으로 깨짐 구간 식별 (참조 hydrate / remove images / image modal ok / set name / set url)
  - antd CSS-in-JS hash 클래스 금지, ARIA role + data 속성 + 텍스트 매치 우선
  - hydrate 트리거는 무조건 DP CDP 트러스트 click (이게 root cause 함정)
  - 텍스트 input 은 `ele.input(text, clear=True)` (CDP keyboard)
  - `is_saved` 는 URL `/create/complete` 우선 (selector false negative 회피)
  - N=1 → N=2~3 단계 검증 후 운영 사용
  - 자주 깨지는 4지점: 모달 클래스, 이미지 카드 wrapper, 버튼 텍스트, DatePicker 셀
- 갱신: [[domains/gfa-setting-automation]] 본문 (§코덱스 2차 감사, §UI 변경 대응 플레이북)

## [2026-04-30] ingest | GFA-Setting 스킬 v0.1.0 — 네이버 GFA 광고 세팅 자동화 + 코덱스 감사

- 신규 도메인: [[domains/gfa-setting-automation]] — `gfa-setting <광고계정ID>` 7개 입력값 → N개 광고 그룹+소재 atomic 등록
- 신규 소스: [[sources/src-gfa-setting-skill-2026-04-30]] — v0.1.0 빌드 스냅샷 (bob → dd → harness → 구현 → 코덱스 감사)
- 진입 절차 명문화: git clone Min-Gil-Sang/GFA-Setting → `_assembled` → pip install -e .[dev] → .env → 최초 1회 수동 로그인 → CLI 실행
- 코덱스(gpt-5) CLI 감사 결과 반영:
  - **치명**: README/SKILL antd 안전가정과 코드 불일치 (`ad_sets.py:73,99,133,169,336`, `materials.py:63,89,124,255` dispatchEvent/native setter 잔존)
  - **높음**: CLI partial(orphan group) 출력 누락(`cli.py:111`), `configure_logging(secrets=[])` 마스킹 무력화(`cli.py:60`), `_assembled/.gitignore`/`.pre-commit-config.yaml` 단독 부재
  - **중간**: N>20 차단 느슨, +50분 rollover 타임존 미검증, `_NN` 끝자리 한정
  - **낮음**: 설치 경로 가정, `.browser_profile` 상대경로, mock 중심 테스트의 실브라우저 보장 한계
- 4시간 troubleshooting 교훈 4가지: 이미지 카드 selector(antd CSS-in-JS hash), modal scope 카운트 정규식, 참조 hydrate 부분 실패(DP CDP 트러스트 click), `is_saved` urlMoved 단독 인정
- 교차 링크: [[domains/marketing-automation]] §광고 플랫폼 자동화, [[index]] §🔥 핵심, [[HOTSHEET]] 트리거 표

## [2026-04-30] ingest | 루비알엔 v3 해골 변신 광고 — 7단 파이프라인 7대 교훈 (§43-49)

- 케이스: 유쎄라블 META 광고(50s) → 루비알엔 PDRN 클렌저(29.6s 16컷) 재구성
- 7대 신규 교훈:
  - §43 레퍼런스 영상 분석 (fps=2 프레임 + audio + scenedetect, Gemini+Codex 협업)
  - §44 캐릭터 일관성 2단계 마스터 시트 + edit_b64.mjs (base64 dataURL 패치)
  - §45 실제 제품 사진 reference 필수 (자연어만으론 임의 화장품 그림)
  - §46 GPT-5.5 이미지젠은 한국어 텍스트 정확 (§14 Gemini 예외 케이스)
  - §47 리듬감 SPEED+MAX_SIL 매트릭스 (1.0 / 0.35 = 16컷 30s 균등 분포)
  - §48 후편집 효과 (post_fx_v3.py — 컷별 줌/페이드/플래시 매핑 룰)
  - §49 패키지 폴더 seeds/ 보관 (재생성·바리에이션 작업용)
- 추가 위치: wiki/tacit/video-gen-lessons.md §43-49, wiki/domains/content-ai-automation.md §16
- 산출 패키지: C:\Users\gguy\Desktop\rubiv_v3_skull_pkg\ (110MB, AE 25.0)

## [2026-04-30] ingest | ggttt-imagen CCFM 커스텀 + 모델 강제 룰 정리
- 신규 페이지 [[domains/ggttt-imagen]] 추가 (god-tibo-imagen 우회 이미지 생성, BDH 구조)
- 깃허브 원본 위험 7종 → CCFM 커스텀 가드레일 정리표
  - 모델 미강제 → `gpt-5.5-pro` + `reasoning_effort=max` 강제 (폴백 5.5/high)
  - `CODEX_BASE_URL` 변조 → openai.com 화이트리스트 차단
  - path traversal → cwd escape 거부 + 입력 확장자/50MB 상한
  - 로그 누출 → 60자 이상 자동 truncate
  - `--debug` 덤프 → 사용 금지
- 동일 룰을 imagen / gptim / rubyrn-pipeline 세 글로벌 스킬에 공통 적용
- 핵심 인사이트: **Codex CLI 최신 + 모델/effort 강제** 두 핀만 박으면 어떤 에이전트가 호출해도 거의 동일한 결과 (멱등성)
- index.md "🔥 핵심 지식" 섹션에 노출

## [2026-04-23] graphify | 볼륨필인 영상 파이프라인 + Higgsfield Soul API 그래프 반영
- 신규 소스 2종 untracked → wiki/index.md 소스 섹션에 등록
  - [[sources/src-volumefill-video-pipeline-2026-04-21]] — 볼륨필인 Day1→Day14 릴스 공장 (33편, Trio 10편)
  - [[sources/src-higgsfield-soul-api-2026-04-21]] — Soul Character API 실증 (엔드포인트·flat JSON)
- [[tacit/video-gen-lessons]]: 16 → 34 섹션으로 확장 (§17-34 신규, 2026-04-21/23 추가분 반영)
  - §17-19 얼굴형 시드 분리 · 웻룩 도트 · Kling 스무딩 방지
  - §20-25 Trio 릴레이 · 구조 해시 · CTA 풀 · 숫자 오독 방지
  - §26-34 인페인팅 · shadow/silhouette 금지어 · 17s 표준 구조
- `graphify.watch._rebuild_code` 실행: 450 files · 260,642 words · 256 nodes · 328 edges · 31 communities
- `scripts/regen_graph_report.py` 로 한국어 커뮤니티 라벨 재적용

## [2026-04-22] ingest | Claude Code 스킬/커맨드 인벤토리 스냅샷
- `~/.claude/skills/` 20개 + `~/.claude/commands/` 18개 스냅샷을 [[sources/src-claude-skills-inventory-2026-04-22]]에 기록
- 다른 기기 이전용 백업 패키지: `Desktop/claude-skills-package-20260422.zip` (286KB)
- 파이프라인: bob → dd → harness → eval → learnings (5단 순환)
- index.md §소스 섹션에 링크 추가

## [2026-04-15] update | goglecc — 다이어트 B/A "예쁜 얼굴 + 통통 몸" V15 확정
- 사용자 승인: "만족스러운 결과가 나왔어" (15회 반복 후)
- 최종 파이프라인: Higgsfield Soul (strength 0.85 After + 0.6 Before_raw) + `fal-ai/face-swap`
- [[src-goglecc-seed-curation]] §9 (V15 아키텍처·엔드포인트·프롬프트·비용) + §10 (실패 경로 금지 리스트) 추가
- [[tacit/creative-patterns]]: "예쁜 얼굴+통통 몸" 레시피 (confidence high)
- [[tacit/coding-lessons]] 2건: (1) Gemini preserved-face body 부피 증가 거부 확정, (2) Higgsfield Soul API 실전 스펙(hf-api-key/hf-secret 헤더, /v1/custom-references, /higgsfield-ai/soul/standard)
- 핵심 인사이트: 한 AI 툴로는 목적 달성 불가 → **Higgsfield(몸 생성) + fal face-swap(얼굴 합성)** 파이프라인이 유일 해법
- 비용: ~$0.10/세트, 10세트 ~$1

## [2026-04-13] prune | 통합검색 크롤링(posts/collect.py) 레퍼런스 제거
- 사용자 지시: 통합검색 크롤링 불필요 → 위키에서 삭제
- 영향 파일: wiki/sources/src-cafe-crawler.md, wiki/tacit/coding-lessons.md
- 제거 항목: 파일 테이블 row, CLI 사용 예, 셀렉터 설명, rate limit 값, HITL 캡차 파일 레퍼런스, 크레덴셜 분리 언급

## [2026-04-13] restructure | 도메인 카테고리 확장 (7→14)
- 신규 도메인 7개 생성:
  - vibe-coding (바이브코딩 & 클로드 스킬)
  - marketing-automation (마케팅 자동화 AI)
  - finance (경영/재무/회계)
  - hr-admin (인사/총무)
  - viral (바이럴 지식)
  - psychology (심리학 & 인간의 본질)
  - content-ai-automation (기존, 유지)
- 도메인을 5개 카테고리로 그룹핑: 시장/사업, 조직/경영, 기술/자동화, 크리에이티브/마케팅, 인문/심리
- CLAUDE.md 업데이트: 도메인 구조, 암묵지 category enum, domain enum 확장
- index.md 전면 재작성
- 암묵지 유형 3개 추가: viral-patterns, coding-lessons, psychology-insights

## [2026-04-12] ingest | DA 크리에이티브 암묵지 8건
- 소스: CEO 구두 경험칙
- 생성: wiki/tacit/creative-patterns.md (8건)
- 업데이트: wiki/domains/da-creative.md, wiki/index.md

## [2026-04-12] ingest | Gemini Logo Remover v3.0
- 소스: CEO 직접 개발 + LaMa 비교 테스트 결과
- 생성: raw/reports/gemini-logo-remover-v3.md
- 생성: wiki/sources/src-gemini-logo-remover.md
- 업데이트: wiki/domains/ai-automation.md (로고 제거 섹션 추가)
- 생성: wiki/tacit/lessons-learned.md (LaMa vs OpenCV 교훈)
- 업데이트: wiki/index.md

## [2026-04-13] ingest | 네이버 카페 크롤링 모듈 지식화

## [2026-04-13] ingest | naverapi (네이버 검색광고 + Meta 광고) 모듈 지식화

## [2026-04-16] ingest | talmo 탈모 B/A 파이프라인 (루솔브 런칭용)
- 소스: `C:\Users\gguy\Desktop\talmo\` 전체 트리 (v1 완성: 1세트 검증 통과)
- 생성: wiki/sources/src-talmo-b2a.md (전체 파이프라인 + 교훈 + 스크립트 맵)
- 업데이트: wiki/domains/content-ai-automation.md §14 talmo (신설)
- 업데이트: wiki/tacit/creative-patterns.md (+6 항목 — 정수리위젯/조명대비/전환카드/2박스카피/계절의상/후킹핏)
- 업데이트: wiki/tacit/coding-lessons.md (+5 항목 — Haar 3단방어/Gemini합성표현/phone_look/HAIR_COLOR/cp949)
- 업데이트: wiki/tacit/psychology-insights.md (+4 항목 — 정수리공포/3개월시간축/쓸어올림제스처/조명대비)
- 업데이트: wiki/index.md (sources 목록에 src-talmo-b2a 추가)
- 핵심 결정: burst(고무줄 폭발) 씬 실험 후 폐기 → 3씬 + 헤어플립 엔딩으로 확정

## [2026-04-17] ingest | Multi-LLM Orchestrator v2.0.1 패치
- 소스: `C:\Users\gguy\Desktop\multi-llm-orchestrator-v2` (v1 API → v2 CLI subprocess 전환 + 4종 함정 패치)
- 업데이트: wiki/domains/ai-automation.md (Multi-LLM Orchestrator 섹션 신설)
- 업데이트: wiki/tacit/coding-lessons.md (+3 항목 — Windows .cmd 멀티라인 인자 함정 / CLI 플래그 변경 대응 / exit code+json-output 자동화 계약)
- 핵심 발견: Codex/Gemini 자체 SKILL.md 리뷰로 P0 가드레일 도출 (description 과잉 트리거 제거, 자동화 계약, 첫 실행 실패 차단)
- 영향 스킬: ~/.claude/skills/multi-llm-orchestrator/ + ~/.claude/commands/{askall,ask-all}.md

## [2026-04-20] ingest | 볼륨필인 앰플 광고 소재 자동생성 파이프라인 성공사례
- `wiki/sources/src-volumefill-pipeline-2026-04-20.md` 생성 (전체 케이스 스터디)
- `wiki/domains/da-creative.md` 에 링크·요약 추가
- `wiki/tacit/creative-patterns.md` 에 6개 패턴 추가 (타입 진단형 후킹, B/A 우회 12종, 나이 단정 회피, 시각 템플릿 선언, O 마스킹, 인종 강제)
- `wiki/tacit/coding-lessons.md` 에 6개 교훈 추가 (gpt-image 첫입력 fidelity, 백그라운드 조기종료, bash rm 영구삭제, rate limit 30분캡, Codex 크로스리뷰, 라운드로빈 정렬)
- 결과: 다음 프로젝트 시작 시 `projects/<new>/` 템플릿 복제 + 규칙 MD 6종 제품별 맞춤 → 동일 퀄리티 유지 가능

## [2026-04-20] playbook | 시장조사 파이프라인 플레이북 등록 (주름/유쎄라블 성공 케이스)

### 등록 배경
사용자 요청: "시장조사하는 것 구조 전체를 wiki에 등록해서 최근 성공 사례로 하고, 이거 요청 시장조사 요청하면 이것 형태로 바로 구조화해서 할 수 있게 업데이트"

### 추가 파일
- `wiki/sources/src-market-research-pipeline-2026-04.md` — 주름·유쎄라블 시장조사 전체 케이스 스터디
  - 소비자 발언 17,690건 수집 (다음카페 + 네이트판 + 유튜브)
  - 연관키워드 1,158개 6개월 트렌드 → 저점폭증 32건 발굴
  - 메타 광고 500+ 카피 경쟁사 역설계
  - 영상기획 MD 11파일 (각 <150줄, 쉬운말 치환)
- `wiki/domains/market-research-playbook.md` — **재사용 플레이북 (글로벌 지식)**
  - "시장조사 해줘" 요청 시 즉시 참조하는 runbook
  - 9단계 체크리스트 + 쉬운 말 치환 규칙 + 브랜드 제외 체크
  - Gemini Deep Research API 현황 + 하이브리드 전략 명시

### Gemini Deep Research API 조사 결과
- 2026-04 기준 **공식 API 미제공** (Gemini Advanced 앱 전용 기능)
- 대안: Gemini 2.5 Pro + `google_search` grounding tool (Vertex AI / AI Studio)
- 실무 권장: 앱에서 수동 생성 후 폴더 투입 → Claude가 읽어 통합

### 쉬운 말 치환표 (중요)
- "지방 세포 증식" → "꺼진 자리 깨우기" (⚠️ 살찐다 오해 방지)
- "인텔리전트 미니멀리즘" → "한 병으로 끝"
- 향후 시장조사 시 전문용어 감수에 활용

## [2026-04-21] ingest | 볼륨필인 파이프라인 v2 성공 패턴 심화 확장
- `wiki/sources/src-volumefill-pipeline-v2-2026-04-21.md` 생성 (v2 심화 사례)
- 15개 개선 항목: 컷 10종 · 키워드 120개 · 카피 3박자 · 궁금증 갭 · 자연 어법 · 글로벌 캡 · 동적 금지어 · 11 민족 · 첨부 순서 · O 마스킹 · 뚜껑 자동 · melable 로고 강제 · rate limit 1탭 · JPG 전환 · QC 8축
- 성과: 24시간 200+ 이미지 자동 생성, 사용자 만족 "매우 좋아짐"
- tacit/creative-patterns.md: 7개 패턴 추가
- tacit/coding-lessons.md: 5개 교훈 추가

## [2026-04-28] ingest | 시장조사 4단 심화 신 표준 (루비알엔 광채 클렌저 케이스)
- `wiki/sources/src-rubyrn-glow-deep-research-success-2026-04-28.md` 생성 — 🏆 사용자 승인 표준
- `wiki/sources/src-rubyrn-cleanser-glow-research-2026-04-28.md` (1·2단 부분 자료)
- 새 단계 추가:
  - **3단 영상 1차 분석**: yt-dlp로 자막 srt + 썸네일 jpg → Claude Read로 시각 분석 → 100만뷰+ 5건 후킹 5선 추출
  - **4단 민간 속설/통념**: 60성분+14카테고리 시드로 unique 발화 1,195건 → "통념 얹기" 카피 80선 직변환
- 1차 자료 규모: **약 12,800건** (검색 80kw + 카페 5,377 + 커뮤 7,390 + YT 65 + 영상자막 10 + 썸네일 10)
- 핵심 인사이트:
  - PDRN 흡수 의심 → 클렌저 차별화 무기 ([[viral-patterns]])
  - "자연광 = 진실 판정" 합격선 ([[creative-patterns]])
  - "통념 얹기 vs 깨기" A/B 분기 ([[psychology-insights]])
- 플레이북 [[market-research-playbook]] 업데이트: 9단계 체크리스트 → 4단 20단계로 확장
- 산출 MD: 4단 → 6개 (`canvas/04~06.md` 분리, 총 1,813줄)

## [2026-04-28] ingest | 간호사 신발 시장조사 + 착한구두 시너지 (브랜드 시장 단위 변형 모드)
- sources/src-nurse-shoes-2026-04-28.md 신규 (4단 파이프라인, 11시트 Excel, Toss UI HTML, 시너지 매트릭스)
- domains/market-research-playbook.md §9 (변형 모드: 브랜드 시장 단위 + 자사몰 분석 + 진입 권고) append
- tacit/coding-lessons.md §검색량 역산 공식 + §Toss UI HTML 템플릿 append
- tacit/operational-heuristics.md §브랜드 시너지 3 시나리오 매트릭스 append
- index.md 핵심 지식 섹션 추가
- 핵심 도구: nurse/fetch_brand_trends.py (DataLab+SearchAd 역산), nurse/generate_excel_report.py

## [2026-04-29] ingest | rubyrn 24h 자율 파이프라인 운영 교훈

- 백엔드: Playwright UI → god-tibo-imagen 사설 Codex API (안정성 급상승)
- 버그: PNG-only skip 체크로 watcher 변환 후 같은 cid 중복 생성 (47장 손실 후 발견)
- 운영: ScheduleWakeup 1시간 자가 감시 + autoloop 다중 실행 방지 + usage_limit 자동 대기
- 배포: check_env.py + init_product.py 로 신상품 fork 자동화
- 추가 위치: wiki/tacit/coding-lessons.md (8개 신규 교훈)

## [2026-04-30] ingest | 한국 퍼포먼스 광고 영상 21초 + AE 핸드오프 end-to-end 자동화

- 케이스: 루비알엔 PDRN 앰플 클렌저 광고 v09 (1080x1920, 21.54s)
- 파이프라인: ElevenLabs char-level TTS → ffmpeg atempo 라인별 속도 → 13 segs 합성 → 워드팝 자막(45 word-pops) → AE 25.0 .aep 빌드 → 핸드오프 패키지 18.2MB
- 핵심 함정 11개 정리: amix normalize=1 볼륨 죽음 / ASS 핑크박스+핑크텍스트 투명 / AE 텍스트 sourceRectAtTime 앵커 보정 / AE 버전별 .aep 호환 / 핸드오프는 별도 절대경로 재빌드
- 추가 위치: wiki/tacit/coding-lessons.md ([2026-04-30] 섹션, 11단계 + 10대 교훈)

## [2026-04-30] ingest | 컷편집·자막·TTS 매칭 타이밍 정리 (v09 회고)

- 핵심 발견: **씬 길이 고정(2초씩) ≠ 정답**. TTS 실측 길이 + atempo 차등으로 씬 길이 결정해야 더빙 안 잘림.
- 11개 정리 항목: 단방향 의존 파이프라인 / 라인별 atempo 매트릭스 / char→word→dialogue / 워드팝 / ffprobe 실측 / GAP 0.05 / 씬 종류별 길이 가이드 / 박스-텍스트 색 충돌
- 추가 위치: wiki/tacit/video-gen-lessons.md §35 (10대 규칙 포함)

## [2026-04-30] ingest | 루비알엔 v2 24컷 빌드 + AE 25.0 자동화 7대 보완 교훈

- v09 21초 광고와 별개 트랙(24컷 49.7s) 에서 다시 발견된 7개 함정·기법:
  - §36 컷 길이 = 다음 cue start (NOT 발화 길이) — `-shortest` 가 오디오 자르는 변종 버그
  - §37 자막↔TTS 텍스트 강제 일치 + 숫자 한글 변환 매핑 (`+166%` → "백육십육 퍼센트")
  - §38 silencedetect 트림 (cut/rejoin 금지 — 잔향 끊김)
  - §39 ffmpeg input seek 함정: `-ss` 가 `-i` 뒤면 afade `st` 가 절대 타임스탬프 → 첫 세그먼트 외 묵음 (1시간 디버깅)
  - §40 atempo + cue scale 동시 적용 (mp3만 가속하면 자막 어긋남)
  - §41 AE 자동 빌드 (COM 폴백 → AfterFX.exe -r) + AE 25/26 버전 지정
  - §42 .aep 패키징 (절대경로 import 회피, 환경변수로 빌드 경로 강제)
- 추가 위치: wiki/tacit/video-gen-lessons.md §36-42, wiki/domains/content-ai-automation.md §15
- 산출 패키지: C:\Users\gguy\Desktop\rubiv_v2_revised_pkg\ (64.5MB)

## [2026-04-30] ingest | B&A 표현 타이밍·감정 곡선 (v09 회고 §36)

- 핵심: B&A는 **공감→충격→안도→환희** 4단계 감정 곡선. 컷 길이가 곡선 따라야.
- v09 진단: Day5(1.24s) < Day3(1.55s) 가속 거꾸로 / Day7 광채 1.60s 절정 약함 / CTA 1.30s 못 읽음
- 7대 규칙: Before>Trigger / Day1<3<5<7 가속 / After 길게 / Trigger 첫 0.5초 / CTA 2.5s+ / atempo도 감정 곡선 / 자막 폰트도 곡선
- 추가 위치: wiki/tacit/video-gen-lessons.md §36

## [2026-05-12] ingest | 3팀 영상 자동화 M1~M5 5단 NAS 파이프라인 성공 사례
- raw: `raw/skills/video-automation-m1-m5/` (스킬 6종 + M4 코드 + 입력폼)
- source: `wiki/sources/src-video-automation-m1-m5-2026-05-12.md`
- domain: `wiki/domains/content-ai-automation.md` §14 추가
- tacit: `wiki/tacit/coding-lessons.md` + `wiki/tacit/operational-heuristics.md` 신규 엔트리
- index: 핵심지식에 🏆 항목 등록
- 의도: 다른 PC/Mac에서 NAS 마운트만 하면 동일 파이프라인 재현 가능하도록 박제

## [2026-05-19] ingest | seebio 비오티아 라디오 빌드 — 영상 광고 baseline 등록
- source: `C:\Users\gguy\Desktop\seebio\pd\con1\build\` (사용자 직접 작업)
- domain: `wiki/domains/seebio-radio-pipeline.md` 신규 (8단계 파이프라인 + 베이스라인 사양)
- tacit: `wiki/tacit/video-gen-lessons.md` 에 [2026-05-19] 엔트리 추가
- 의도: 사용자가 "이정도 이하 결과는 절대로 나오게 해선 안됨" 품질 baseline으로 지정. 시댄스+ElevenLabs+AE 파이프라인 재사용 위해 박제.
- 함정 누적: TTS 전면 교체 금지 (lip-sync 깨짐), 보이스 청취 선정 필수, 플로팅 배너 금지 (로고만), AEP 자산 완전 분리, 자막 8~12자 한 줄, 청크간 공백 금지, EBU R128 정규화
