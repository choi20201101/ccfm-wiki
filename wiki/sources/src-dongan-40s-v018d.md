# src-dongan-40s-v018d

> **UGC 퍼포먼스 광고 소재 프로덕션 기준 (2026-04-20 최종)**
> 기준 샘플: `C:/Users/Administrator/Desktop/klingout/dongan_v01_v10.mp4` (45.8s, 27MB)
> 앞으로 "UGC 퍼포먼스 소재 만들자" 지시 = **최소 이 수준 이상** 이어야 함.

---

## 1. 영상 스펙 (고정)

| 항목 | 값 |
|---|---|
| 해상도 | 1080×1920 (9:16 세로) |
| 프레임율 | 30fps |
| 코덱 | H.264 (video) + AAC 192k (audio) |
| 길이 | 37~60초 (평균 43~50s) |
| 청크 수 | 13~17 (avatar 1chunk + broll 1~3 sub) |
| SFX 레이어 | 3~5 |
| 플로팅 | 5~8 (cue당 1개 기본, 비교만 2 순차, 최소 1.8s) |
| 자막 청크 | 8~12자 rich 강조 (색·크기·줌 애니) |
| 크로스페이드 | dissolve 0.4s (호흡 연결) |
| 자막 선도 | -0.20s |

## 2. 자산 체인 (필수 순서)

```
scripts_{id}.json (cue + shot_type + slot + sos_tag + source_status + floats)
  ↓ Gemini nano-banana-pro edit (gemini-2.5-flash-image)
faces_styled/{sid}.png  (원본 셀카 + "동안 얼굴 + 40대 니트 카디건" 프롬프트)
  ↓ ElevenLabs /with-timestamps (1콜)
voice.mp3 + alignment.json
  ↓ split_avatar_audio (shot_type=avatar cue 구간만 slice·concat)
avatar_audio.mp3 (≤30s 보장)
  ↓ fal.ai OmniHuman v1.5 (또는 Kling /v1/videos/avatar/image2video + sound_file)
avatar_omni.mp4 (또는 avatar_kling.mp4)
  ↓ slice_avatar_omni (cue 단위 pre-slice)
avatar_slices/cueNN.mp4
  ↓ build_plan_v018d (avatar=1chunk, broll 순환, overlay, 플로팅 매핑)
plan_v018d_{id}.json
  ↓ render_plan_continuous (TTS 1콜 재사용, alignment 타이밍, SFX 자동, 플로팅 overlay, build_ass_rich)
klingout/{id}.mp4
```

## 3. 핵심 규칙 (하네스 강제, 린터 통과 필수)

- **훅 cue.dur_s ≤ 3.0s**, 한글 28자 이내
- **avatar cue = 1 chunk 통합** (립싱크 끊김·반복 방지)
- **broll cue = 1~3 sub-chunk**, cue.sos_tag manifest 파일 **순환** (반복 방지)
- **POSITIVE overlay 먼저, NEGATIVE 두 번째** (긍정 핵심 먼저 잡힘)
- **POSITIVE overlay 가 cue.sos_tag 와 같으면 skip** (반복 방지)
- **긍정 대사 cue + 부정 플로팅 자동 skip** (예: "얇은 금빛 막" cue 에 "일반:겉만" 플로팅 금지)
- **첫 sub-chunk = cue 지정 sos_tag 우선** (사용자 명시 매핑 존중)
- **플로팅 = SOS 영상 / flo 실사만** (검정+노랑 PIL 배너 **완전 금지**)
- **SOS 범위 = `pilot/sos/` + `seven_day/` 전용**
- **voice 다양화 = 캠페인 내 동일 voice ≤2편**

## 4. 자주 쓰는 SOS 키워드 ↔ 태그

| 대사 키워드 | sos_tag |
|---|---|
| 화장대 크림 다 꺼내 | 화장대 위 무명 크림 여러개 |
| 피부과 선생님/원장님 추천 | 의사가 제품 추천하는 장면 |
| 얇은 금빛 막 · 골드필름 | 골드필름 피부 침투 3D |
| 속까지·안쪽·스며 | 골드필름 피부 침투 3D |
| 대부분 겉에만 | 피부 겉만 지나가는 일반크림 컷 |
| 파운데이션 톡톡 떡칠 | 파운데이션 떡칠 화장 |
| 광대 자국 흐려지기·일주일 | 7일 얼굴 변화 타임랩스 |
| 피부과 입점 기념가 | 피부과 진열대 제품 배치 |
| 민낯·립글로스만·선크림만 | 민낯 40대 동안 클로즈업 |
| 도드라지·번지·효과없 | 기미가 번지는 3d |
| 셀카 기록 | 셀카 기록 40대 동안 |

## 5. Voice 페르소나 톤 매핑

- **차분/조용/관조**: Jini, Park Hyun-mi, Eunhye
- **따뜻/가족/대화**: Sumi, Jian.K
- **밝음/감탄/경쾌**: Bomisori, Jian.K
- **전문/직장/신뢰**: Eunha
- 감정이 큰 cue (감탄·놀라움) 에 차분 voice 붙이지 말 것

## 6. 스크립트 스키마

```jsonc
{
  "id": "vNN_name",
  "title": "...",
  "render_mode": "avatar_base|source_only",
  "persona": { "age": 42, "name": "...", "vibe": "..." },
  "voice_name": "Jini", "voice_id": "...",
  "cta_mode": "strong|soft|none",
  "avatar_audio_cue_ids": [1,5,8],
  "cues": [
    {
      "cue": 1, "slot": "hook|pain|context|turn|product|proof|compare|peak|cta",
      "shot_type": "avatar|broll",
      "text": "…", "dur_s": 3.0,
      "sos_tag": "…", "source_status": "existing|new",
      "floats": [{"text":"광대 기미 포착","start_s":0.8,"dur_s":2.0}]
    }
  ]
}
```

## 7. 파이프라인 스크립트 (재현용)

`avatar_10_dongan/scripts/` 에 전부:
- `gemini_face_restyle.py` — 얼굴 재생성
- `gen_tts_10.py` — TTS 1콜
- `split_avatar_audio.py` — avatar cue concat
- `gen_avatar_fal.py` — OmniHuman 병렬
- `slice_avatar_omni.py` — cue pre-slice
- `gen_new_sos_3.py` / `regen_*.py` — 부족 SOS Kling v3 생성
- `build_plan_v018d.py` — 플랜 빌더 (핵심)
- `render_v018d_10.py` — 일괄 렌더
- `vision_qc_v018.py` — Gemini Vision QC

## 8. 품질 기준 (사용자 극찬 포인트)

- **립싱크 연속성** (cue 1chunk → 끊김 없음)
- **플로팅 = SOS 영상 or 실사 매칭** (검정 박스 텍스트 X)
- **제품 라벨 정확** (Gemini seed 에 product.png 레퍼런스)
- **대사 ↔ 장면 정합** (긍정 cue = 긍정 SOS, 부정 cue = 부정 SOS)
- **반복 없음** (sub-chunk 별 다른 파일 순환)
- **호흡 연결** (dissolve 0.4s)
- **Voice 페르소나 맞춤**

## 9. 실패 회피 히스토리

| 시도 | 실패 이유 | 해결 |
|---|---|---|
| Kling 직통 `multi-image2video` avatar | model_name 전부 invalid | **`/v1/videos/avatar/image2video` + `sound_file` base64** |
| fal.ai Kling avatar 경로 | submit OK, result 404 | **fal.ai = OmniHuman 전용** |
| avatar chunk 여러개 | 립싱크 처음부터 반복 | **avatar cue 1 chunk 통합** |
| POSITIVE overlay = cue tag | 파일 반복 | **same tag 면 skip + used_files 추적 순환** |
| 긍정 cue 에 부정 플로팅 | 의미 충돌 | **POS_CUE_KW + NEG_FLOAT_KW 자동 skip** |
| "골드필름" 폴더에 파란 크림 섞임 | 옛 영상 잘못 분류 | **신규 `골드필름 피부 침투 3D` 폴더 Kling v3 재생성** |
| PIL 검정+노랑 배너 | 매칭 실패 시 남발 | **폴백 제거, 플로팅 생략이 정답** |
| Ken Burns 정적 얼굴 | 립싱크 아님 | **OmniHuman 서버 복구 후 진짜 립싱크** |

## 10. 관련

- [[src-foreign-influencer-guide]] — 외국인 인플루언서 33편 (립싱크 뿌리)
- [[AI-Avatar-Automation-Guide]] — 아바타 모델 비교
- 하네스: `klinginter/docs/HARNESS_SOS.md`
- 메모리: `.claude/projects/.../memory/feedback_ugc_v10_spec.md`

*2026-04-20 v10 최종 확정. 이후 UGC 소재 제작 = 이 스펙 최소 기준.*
