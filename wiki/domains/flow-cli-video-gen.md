---
type: domain
domain: ai-automation
confidence: high
created: 2026-06-09
updated: 2026-06-10
sources:
  - C:\Users\Administrator\Desktop\flow\flow-ad-pipeline\README.md
  - C:\Users\Administrator\Desktop\flow\flow-ad-pipeline\USAGE.md
  - C:\Users\Administrator\Desktop\flow\examples\샤라웃-크림 (실증 케이스 v5 — 11컷 재현 플레이북)
  - C:\Users\Administrator\Desktop\sharout_cream_ae (AE 25.0 프로젝트 빌드)
---

# flow-cli-video-gen — Google Flow(Veo) CLI 영상 생성 파이프라인

> **분류**: domains / AI-automation
> **최종 업데이트**: 2026-06-10 (§9 재현 플레이북 + §10 AE 빌드 추가)
> **연관**: [[ggttt-imagen]], [[content-ai-automation]], [[ai-automation]], [[tacit/video-gen-lessons]], [[da-creative]]

## 1. 한 줄 정의

Google **Flow(labs.google/flow, Veo 3.x·Imagen)** 를 비공식 CLI `gflow`(ffroliva/gflow-cli)로
터미널에서 호출해 한국 퍼포먼스 광고(9:16 숏폼)를 **생성→음성체크→컷편집→자막** 까지 자동화.
직원 배포 키트: `C:\Users\Administrator\Desktop\flow\flow-ad-pipeline\`.

## 2. 왜 gflow-cli인가 (레포 조사 결론)

GitHub에서 Flow 호출 오픈소스를 별순 조사한 결과(2026-06-09):

| 방식 | 대표 레포 | 평가 |
|---|---|---|
| CLI 파이프라인 | **ffroliva/gflow-cli** ⭐33 | 1픽. pip 설치, 배치/파이프라인 친화, 유지보수 활발 |
| JSON 파이프 백엔드형 | hurara210/google-flow-cli | 전 명령 `--json`, 단 RPC ID 수동 캡처 |
| 영상 체인/임베드 | eddie-fqh/flow-py | extend-loop, 4K 업스케일, Python 임베드 |
| Chrome 확장형 | trgkyle/veo-automation 등 | 브라우저 점유·DOM 의존 → 탈락 |

> ⚠️ 공통 제약: Flow는 공식 생성 API가 없고 **reCAPTCHA Enterprise** 보호 → 브라우저 완전 0 불가(토큰용 1회 필요). 비공식·ToS 소지 → 본인 Ultra/Pro 구독 계정 단일 세션만.

## 3. 설치·인증 (PC당/계정당 1회)

```powershell
pip install gflow-cli              # + faster-whisper, edge-tts
python -m playwright install chromium
setx PYTHONUTF8 1                  # cp949 인코딩 에러 방지 (필수)
# 새 터미널에서:
$env:PYTHONUTF8=1; gflow auth login --browser chrome
```
- 인증은 **Flow 에디터(프롬프트 박스+프로젝트)가 실제로 뜬 뒤 크롬을 닫아야** verified. 구글 로그인만 하고 닫으면 `google_session_only` 실패.
- 격리 프로필(`AppData\Local\ffroliva\gflow-cli\profile_<계정>`) → 사용자 평소 크롬 안 건드림.

## 4. 명령 체계

```
gflow video t2v "프롬프트"                      # 텍스트→영상
gflow video i2v 시드.png "프롬프트"             # 이미지→영상(시작프레임)
gflow video i2v a.png "..." --end-frame b.png  # 이어붙이기(보간)
gflow video r2v "..." --ref x.png --model omni-flash  # 레퍼런스→영상
gflow image t2i "프롬프트"                      # 이미지(Imagen/Nano)
```
모델: `veo-fast`(기본)/`veo-quality`/`veo-lite` · `omni-flash`(i2v 미지원, r2v·t2v만)
공통: `--aspect 9:16 --duration 8 --out-dir 폴더 --json`

## 5. 박제된 함정 4종 (실증: 샤라웃 크림 광고)

1. **얼굴 또렷 인물 시드는 r2v 차단** — `FINISH_REASON_OUTPUT_PROMINENT_PERSON`. r2v는 인물 재현 → 유명인 필터. **i2v(프레임 애니메이션)·이어붙이기는 통과.** omni는 i2v 미지원이라 얼굴 시드 불가. → 인물은 무조건 i2v.
2. **한국어 음성은 prompt에 한국어 대사 명시해야 나옴** — 대사 안 적으면 Veo가 영어로 애드립("Hi everyone, my favorite pink cream"). 명시하면 네이티브 한국어+입싱크("요즘 이거 하나밖에 안 발라요"). 군중도 "팬들이 한국어로 '대박!' 외친다".
3. **TTS 더빙 금지 = 네이티브 음성으로 편집** — TTS는 립싱크 깨지고 어색. 생성 음성을 faster-whisper로 전사(언어 auto감지로 영어 섞임 확인) → 실제 발화 단어에 자막·컷 동기. → [[tacit/video-gen-lessons]] 와 동일 결.
4. **Veo 워터마크는 delogo로 제거** — 우하단(클립마다 위치 확인). `ffmpeg ... delogo=x:y:w:h`. 본인 구독 산출물 한정.

## 6. 컷편집 (퍼포먼스 호흡)

- 8초 클립을 **≤2초 컷**으로 슬라이스 → 점프컷·줌 변주(정적 스케일 변주가 안정적). 말하는 구간은 음성 끊김 없이 영상만 인터컷(J/L컷).
- 자막: ASS 팝 애니메이션(작게→100%), 핵심어 노랑/핑크. 폰트 `Malgun Gothic`(libass fontsdir).
- 음량: `loudnorm=I=-14:TP=-1.5`.
- 제품 라벨은 Veo가 뭉갬 → **ggttt(gpt-5.4 OAuth)로 실제 누끼를 시드 손에 합성**([[ggttt-imagen]]) 후 i2v 재생성, 또는 별도 제품 히어로 컷.

## 7. 직원 키트 구조

```
flow-ad-pipeline/
├── INSTALL.ps1            설치(ASCII-only: 한글 ps1 BOM 함정 회피)
├── README.md / USAGE.md   빠른시작 + 상세/함정/트러블슈팅
├── config.example.json    씬 생성 설정
├── edit.example.json      컷편집 설정
└── scripts/{generate,transcribe,edit}.py
```
- `generate.py` config 기반 씬 생성(i2v/r2v/t2v) · `transcribe.py` 음성 검증 · `edit.py` 네이티브 음성 컷편집.

## 8. 연관 파이프라인

- 기존 [[sources/src-video-automation-m1-m5-2026-05-12]] (웹폼→Premiere+Flow MP4 5단 NAS)와 결합 가능: gflow 산출물을 NAS `scenes.json` 스키마로 흘려보내기.
- 제품 합성/이미지: [[ggttt-imagen]]. 영상 일반 교훈: [[tacit/video-gen-lessons]].

## 9. 재현 플레이북 — 11컷 퍼포먼스 광고 (샤라웃 크림 v5 실증, 2026-06-10)

> 다른 영상에도 그대로 적용하는 **단계별 레시피**. 실증 스크립트: `C:\Users\Administrator\Desktop\flow\examples\샤라웃-크림\build\_*.py`.
> 핵심 원칙: **① 일관성은 시드에서, ② 음성은 컷 성격별(환호=원본·나레이션=TTS), ③ 자막은 대본 텍스트로**.

**0. 기획 = `scenes.json`** — 11씬, 씬마다 `{ggttt(이미지 prompt), gflow(모션/대사 prompt), speakers, ae_captions}`. 포맷 9:16/30fps. 음성/숫자/할인 자막은 전부 후편집 레이어(영상 번인 0)로 규칙화.

**1. 마스터 얼굴 고정 (인물 광고 필수)** — 인물 일관성은 i2v로는 못 잡는다(시작 프레임만 고정, 모션 중 얼굴 변형). 등장 컷(밴/워킹)에서 연예인 **정면 프레임 1장**을 뽑아 `master_face.png`로 박제(워터마크는 crop으로 제거). 이게 모든 인물 씬의 **단일 ref**.

**2. 시드 (Stage A · ggttt gpt-5.4 OAuth)** — `generate.js --provider auto --size 1024x1536 --image <ref>`(ref 복수 가능):
- 인물 씬 = `master_face` ref + *"첨부와 완전히 동일한 한 사람, identity locked, do NOT change identity"* 초강조.
- 제품 씬 = 실제 누끼 ref(라벨 또렷). · broll = ref 없이 톤만 지정(고급·깔끔).
- **NO_TEXT 강력 차단**: "no text/letters/numbers/captions/UI/watermark" (GPT가 한국 토크쇼 자막·가짜 자격 번인하는 함정 [[tacit/video-gen-lessons]] §54).

**3. i2v (Stage B · gflow veo-fast 8s)** — 시드 → `crop=864:1536` → `gflow video i2v`:
- 모션 prompt = **"얼굴·정체성 고정 + 미세 움직임만 + 무발화(silent, no speech, lips closed)"**.
- 무발화 명시가 ① 얼굴 변형 억제 ② `AUDIO_GENERATION_FILTERED` 실패 회피(발화 동작 시드는 음성 안전필터에 확률적으로 걸려 클립 자체 FAIL → 같은 prompt 재시도하면 통과).

**4. 음성 (Stage C) — 컷 성격별 분리가 핵심:**
- **후킹/환호 on-camera 컷 = 원본 native 그대로** (`loudnorm I=-16:TP=-1.5`). 팬 환호·연예인 멘트의 생생함이 후킹. TTS로 덮으면 죽음.
- **나레이션 VO 컷 = ElevenLabs TTS** (`/v1/text-to-speech/{voice_id}`, `eleven_multilingual_v2`, 화자별 voice). Veo native가 헛소리로 hallucinate하면 **그 컷만 TTS로 교체**.
- **S2S 금지**: speech-to-speech는 목소리만 바꾸고 틀린 단어는 보존 → 헛소리가 예쁜 목소리로 박제됨.

**5. 편집 (fast-cut 60초 호흡)** — 컷 길이 = 해당 음성 길이로 trim. 음성이 영상보다 길면 `setpts`로 ≤30% stretch(**freeze 금지** §42). 전 클립 `delogo=x=600:y=1200:w=115:h=68`(720x1280 우하단 Veo). hard-cut concat.

**6. 자막 = 8~10자 카라오케 (음성 싱크)** — ⚠️ **Whisper 전사 텍스트로 자막 만들지 말 것**(`피디알엔→피디아래니`, `피코토닝→피코토닉` 오타가 박힘). **원본 대본**을 어절 단위 8~10자 청크로 분할 + 컷 시간을 글자수 비례 배분(등속 음성이라 싱크 충분, 단어 경계 유지로 안 잘림). Whisper는 검증 전용. 강조 그래픽(애정템·품절대란·숫자)은 사용자가 명시할 때만 — 남발하면 "시키지 않은 자막"으로 인식.

**7. 검증 게이트** — 완성본 오디오를 faster-whisper로 전사해 **대본 일치** 확인(헛소리 재발 차단) + 프레임 추출로 인물 일관성·워터마크·텍스트깨짐 자가검수. [[../feedback_always_verify_with_subagent]]

## 10. After Effects 프로젝트(.aep) 빌드

편집 가능한 인계본이 필요하면 자막을 **AE 텍스트 레이어**로 올려 .aep 생성:
- 소스 = 자막 없는 컷 세그먼트(`seg_sNN.mp4`, 영상+음성) → **영문 패키지 폴더**(`sharout_cream_ae/footage/`)에 복사(한글경로·footage lock 회피).
- 파이썬이 jsx 생성: `addComp(720,1280,1,total,30)` + 컷 영상 레이어(`startTime`=누적) + 자막 텍스트 레이어(`MalgunGothic-Bold` 60px 흰색+검정stroke, `inPoint/outPoint`=청크 타이밍). **한글은 `\uXXXX` escape**로 박아 인코딩 무관.
- 빌드: `"…/After Effects 2025/Support Files/AfterFX.exe" -r build_aep.jsx` (background). **AE 25.0으로** 빌드(상위→하위 호환 X). `alert()` 금지(자동종료 막힘) → try/catch+로그파일.
- 상세 함정(splash 모달·footage lock·컴포지션 자동open 안됨): [[../feedback_ae_aep_default_v25]] · [[../feedback_ae_headless_splash_modal]]. native→TTS·자막·일관성 함정 종합: [[../feedback_gflow_i2v_native_audio_to_tts]].
