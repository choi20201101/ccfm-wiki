---
type: domain
domain: content-ai-automation
aliases: ["seebio 라디오 파이프라인", "비오티아 라디오 빌드", "rusolve 광고 파이프라인", "시댄스+ElevenLabs+AE 파이프라인"]
tags: [content-ai-automation, seedance, elevenlabs, after-effects, baseline]
confidence: high
created: 2026-05-19
updated: 2026-05-19
sources: ["C:\\Users\\gguy\\Desktop\\seebio\\pd\\con1\\build\\"]
---

# Seebio 비오티아 라디오 컨셉 빌드 — 영상 광고 baseline

> 사용자(CCFM CEO) 정의 "이정도 이하 결과는 절대로 나오게 해선 안됨" baseline.
> 9 iteration 시행착오 후 2026-05-19 완성. 향후 모든 영상 광고 빌드의 품질 하한선.

## 한 줄 정의
**시댄스 i2v + ElevenLabs S2S + Whisper word-timestamp + TikTok 자막 + ffmpeg 합성 + AE AEP 자산 분리** = 9:16 80~85초 라디오 토크쇼 광고 1편 자동 생성.

## 베이스라인 사양 (절대 하한선)

| 항목 | 사양 | 비고 |
|---|---|---|
| 해상도 | 1080×1920 9:16 | 릴스/틱톡/쇼츠 |
| 런타임 | 80~85초 | 7컷 → 12 sub-segment |
| 화자 일관성 | 컷별 voice_id 핀 + S2S | lip-sync 보존 |
| 음량 정규화 | EBU R128 -16 LUFS | 화자 간 균일 |
| 자막 | TikTok 스타일, 한 줄 8~12자, word timestamp 동기 | 청크간 공백 X |
| 화면 | 방송 로고(좌상단) + 자막(하단) | 플로팅 배너 절대 추가 X |
| AEP | 자산 완전 분리 (컷별 영상 + 로고 + 자막 텍스트 레이어 모두 별도) | [[feedback-aep-layer-separation]] |

## 8단계 파이프라인

| # | 단계 | 도구 | 산출물 |
|---|---|---|---|
| 1 | 마스터 시드 | 기존 PNG 활용 가능 (또는 GPT image gen) | seeds/_master_*.png |
| 2 | (선택) 컷 시드 | 동일 인물 다양한 표정 | seeds/C*.png |
| 3 | 시댄스 i2v | bytedance/seedance-2.0/image-to-video (R10c) | 02_원본영상/video_*.mp4 |
| 4 | Voice 통일 | ElevenLabs eleven_multilingual_sts_v2 (R4) | _v05/*.mp4 |
| 5 | Whisper 검수 | fal-ai/whisper chunk_level=word | logs/whisper_words/*.json |
| 6 | TikTok 자막 | word timestamp + 기획안 원문 alignment | subs/subs.ass |
| 7 | 합성 | ffmpeg (logo + 자막 burn-in) | deliverables/*.mp4 |
| 8 | AEP 패키지 | AE 25.0 헤드리스, 자산 분리 jsx | *.aep + zip |

## 핵심 결정 사항 (회피하면 안 되는 함정)

### 1) TTS 전면 교체 금지 — S2S 우선
- TTS는 시댄스 영상 lip-sync를 망가뜨림. 사용자가 "입모양이랑 하나도 안맞음" 직접 컴플레인.
- ElevenLabs Speech-to-Speech (eleven_multilingual_sts_v2) 사용:
  - 시댄스 audio를 source로 음색만 voice_id로 변환
  - 타이밍/lip-sync 그대로 유지
- 발음 오류는 R5 우선순위: trim > 시댄스 재생성 > TTS surgical splice (단어 1개 부분만)

### 2) 보이스 청취 선정 필수
- ElevenLabs Korean voice 라이브러리에서 후보 4~5개 추출
- 같은 source audio로 S2S 샘플 생성 → 사용자 청취 후 선택
- "공식 라벨이 professional이어도 실제 들으면 어색한 경우 많음" (사용자 경험)

### 3) 플로팅 배너 절대 금지 (방송 로고 제외)
- CG 인서트, 제품 PIP 카드, 화자 라벨 모두 사용자가 명시적으로 거부함
- 화면에는 방송 로고(좌상단) + TikTok 자막(하단)만
- 깔끔한 미니멀 톤이 정답

### 4) AEP 자산 분리 강제
- 최종 mp4 하나만 import한 AEP는 "이거 다 합쳐져있네?" 컴플레인 받음
- 컷별 영상 footage + 로고 PNG + 자막 텍스트 레이어 모두 별도
- 텍스트 레이어 = `comp.layers.addText()` per chunk, font/color/stroke/position 속성 노출
- 편집자가 컷 클릭 → 그 컷만 trim/대체 가능해야 함

### 5) 자막 = 기획안 원문 + Whisper 타이밍
- Whisper transcribe는 가끔 오기 (예: "84.2%" → "83.2%")
- 자막 텍스트는 **YAML expected text**에서 가져오고
- 타이밍만 Whisper word timestamp 활용
- SequenceMatcher로 alignment

### 6) 자막 청크 사이 공백 금지
- 마지막 청크 종료 ~ 다음 청크 시작 사이 0.04초 외에는 빈 공간 없도록
- 각 청크는 다음 청크 시작 직전까지 표시 (무음 구간 메우기)
- 짧은 청크 (<0.55s)는 다음 청크와 자동 병합

## 발음 오류 처리 (시댄스 한국어 약점)

### 자주 깨지는 단어
- 두피 → 두비/두리 (ㅍ 약화)
- 머리카락 → 머리카리 (받침 ㄱ 약화)
- 휑해 → 흰해 (ㅎ 약화)
- 비오티아 샴푸 → 샴푼/샴표
- 84.2% → 83.2% (Whisper 측 오인식)

### 해결 우선순위 (R5)
1. **시댄스 재생성** (랜덤 시드 변화로 발음 개선) — 가장 효과적
2. **Trim** — 잘못된 부분만 silencedetect로 잘라내기
3. **Surgical TTS splice** — 단어 1개 정확한 timestamp 위치에 끼워넣기
4. ~~전체 TTS 교체~~ — lip-sync 망가져서 금지

## 빌드 산출물

```
build/
├── motion_prompts.yaml         (cast, cuts, sub_segments 정의)
├── seeds/                       마스터 시드 + 제품/로고
├── _seedance_in/                blur+grain 처리된 시댄스 입력
├── 02_원본영상_시댄스/           video_*.mp4 (원본 시댄스)
├── _audio_orig/                 시댄스 추출 audio
├── _audio_converted/            S2S 변환 audio
├── _v05/                        시댄스 video + S2S audio mux
├── 03_그래픽_PNG/                logo_alpha + (옵션) CG 인서트
├── subs/subs.ass                TikTok 자막
├── deliverables/biotia_radio_v01.mp4   최종
├── scripts/                     8개 Python 스크립트
├── logs/                        whisper_words, splice 로그
└── 비오티아_샴푸_라디오_브랜드팀전달.zip
```

## 재사용 가능 스크립트

- `common.py` — API 키 로드, YAML 파싱, 경로
- `run_seedance.py` — 5병렬 i2v 생성, R9 blur/grain fallback
- `voice_convert.py` — S2S + EBU R128 normalize + mux
- `whisper_words.py` — fal Whisper word-level chunks
- `build_subs_tiktok.py` — 청크 그룹핑, alignment, 무공백 t1 결정
- `compose.py` — ffmpeg 합성 + 자막 burn-in
- `package_aep.py` — AE 25.0 자산 분리 jsx + zip
- `word_splice.py` — 단어 단위 TTS surgical splice

## 함께 보기
- [[tacit/video-gen-lessons]] — Kling/Gemini 시절 영상 생성 교훈
- [[domains/content-ai-automation]] — 큰 그림 (컷편집/Whisper/자막 일반)
- [[tacit/creative-patterns]] — 광고 소재 시각 패턴
- [[feedback-aep-layer-separation]] (gguy memory) — AEP 분리 강제 규칙
