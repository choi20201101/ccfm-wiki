# [참고 사례] 율이 EP02 50초 광고 — v01~v08 8회 iteration 우여곡절 성공기

**위치 후보**: `wiki/tacit/coding-lessons.md` 새 § 또는 `wiki/domains/performance-ad.md` 또는 `wiki/cases/yuri-ep02-2026-05-03.md`
**confidence**: high (실제 빌드 + 사용자 합격 검증)
**source**: 2026-05-03 Administrator PC, `Desktop/bj/output/율이_레이저전_50s_2026-05-03/` + `Desktop/율이_레이저전_50s_v08_directorpkg.zip`
**status**: ⚠️ **참고용**. 메인 파이프라인 권장 X (`/bj-vlog` 스킬이 8회 학습 결과 반영해서 처음부터 v08 settings로 시작하도록 별도 정리됨)

---

## 한 줄

50초 짜리 BJ 라이브 광고 1편을 만드는데 8번 iteration 돌렸고, 매 iteration마다 다른 종류 함정에 걸려서 고침. 결과는 **합격 (사용자 OK)**. 본 문서는 **무엇을 처음부터 회피해야 하는지** 학습용 사례.

## 빌드 스택 (최종 v08 합격 settings)

| 단계 | 백엔드 | 핵심 settings |
|---|---|---|
| 시드 이미지 | `image_gen.py` (gpt-image-2) | edit mode + master ref + "NO BRAND TEXT, NO LOGOS, NO AD COPY" 강제 |
| TTS | ElevenLabs `1YzIw7PZ7iaD4alelyHY` (Stella) | model `eleven_multilingual_v2`, stability 0.20, style 0.90, speed 1.20 |
| 영상 생성 | `bytedance/seedance-2.0/fast/reference-to-video` | 720p / 16:9 / `generate_audio: false`, master + 컷 시드 2장 ref + TTS audio_urls (모션 힌트) |
| 립싱크 | `fal-ai/sync-lipsync/v3` | 단일 얼굴 영상에만 적용 (다중 얼굴 함정 회피) |
| PIP | ffmpeg overlay | lipsync **후** 정지 PNG 합성 (단, 폰/손 위치 stable해야) |
| 합성 | ffmpeg drawtext + concat | 9:16 1080×1920 + 16:9 영상 중앙(y=656) + 한국어 자막 (Malgun Bold) |

## 8회 iteration 무엇이 매번 깨졌나

| 버전 | 무엇이 깨졌나 | 어떻게 고쳤나 |
|---|---|---|
| **v01** | Seedance v2 endpoint 경로 4번 헛삽질 (`fal-ai/` 접두어 함정), TTS atempo 0.62~1.76 극단으로 잠오는 톤 + 35초 갑자기 빨라짐, C7 시드에 가짜 RubyRN 라벨/광고카피 박힘 | endpoint = `bytedance/seedance-2.0/...` (fal-ai/ X), atempo 컷 dur 재배정, prompt에 NO BRAND TEXT 강제 |
| **v02** | TTS 텍스트 너무 짧아 패딩으로 부자연 | 텍스트 늘려서 raw≈target |
| **v03** | "시꾸들" → ElevenLabs가 "식구들"로 발음, 쉼표 너무 많아 매 쉼표마다 끊어 읽음 | "시꾸들" 전부 제거, 쉼표 최소화 |
| **v04** | atempo 적용 시 음질 손실 | ElevenLabs `speed` 1.15 직접 파라미터 (atempo 후처리 최소화) |
| **v05** | 폰 PIP에 옛 사진 띄웠더니 **lipsync가 정지 사진까지 입을 움직이게 함** (UGC 신뢰도 박살) | PIP 후처리 분리: 빈 폰 시드 → lipsync → ffmpeg overlay 정지 PNG |
| **v06** | ffmpeg overlay 좌표 첫 시도 잘못 (율이 얼굴을 덮음) | 영상 첫 프레임 보고 폰 화면 bbox 정확히 추출 (x=620, y=275, w=265, h=395) |
| **v07** | voice (Anna Kim) 자체가 차분한 아나운서 톤 → BJ 라이브 감정 한계 | voice 교체 — Stella (광고/소셜미디어용 middle-aged 한국어 여성), model multilingual_v2, 텍스트 길이 균일화 |
| **v08** | "진짜" 단어가 모든 컷에 반복돼서 부자연 (사람 그렇게 말 안 함), C7 가짜 제품 흰색 보틀 | 텍스트 자연화 + 컷별 다른 감탄사 (어머/봐봐/근데/헐), C7 빈 손 시드 → ffmpeg overlay 진짜 `pd/rubi.png` |

## 최종 합격 비용 / 시간

| 항목 | 값 |
|---|---|
| 누적 비용 | ~$56 USD (8회 iteration) |
| 처음부터 v08 직행 시 추정 비용 | ~$20 USD |
| 벽시계 작업 시간 | 약 4-5시간 (사용자 검토 포함) |
| 처음부터 v08 직행 시 추정 시간 | 약 30-40분 |

## 함정 5선 (이미 별도 노트 분리됨)

1. **`feedback_fal_seedance_v2_endpoint.md`** — Seedance v2 endpoint `fal-ai/` 접두어 X
2. **`feedback_lipsync_multi_face_trap.md`** — sync-lipsync 다중 얼굴 함정 (PIP 정지 사진까지 sync)
3. **`feedback_ugc_before_after_proof.md`** — UGC 전후비교 인증 디자인 (폰 텍스트 0, 폰 크게)
4. **`feedback_image_gen_backend_priority.md`** — image_gen.py CLI 우선, edit_multi.mjs 다중 ref
5. **`feedback_per_video_unique_subs.md`** — 영상별 스크립트 자체를 다르게 (자막만 바꾸기 X)

## 다음 영상 제작 시 0회 iteration 목표

`/bj-vlog` 스킬이 위 8회 학습을 반영해서 처음부터 v08 settings로 시작하도록 정리됨 (`bj-vlog-pipeline` 스킬 참고). 본 사례는 **왜 그 settings가 박혔는지** 이해를 위한 참고용.

## 인계 패키지 (직원 편집용)

`Desktop/율이_레이저전_50s_v08_directorpkg.zip` (99MB). 구조:
- `01_final/final_50s_v08.mp4` — 송출본
- `02_cuts/CXX_lipsync.mp4` — 7컷 raw
- `03_seeds/`, `04_audio/`, `05_images/` — 모든 소스
- `06_plan/` — 기획 문서 (storyboard, dialog, subtitles)
- `07_project/ae_setup.jsx` — After Effects 자동 셋업
- `07_project/edit_list.csv` — Premiere/DaVinci 호환
- `07_project/ffmpeg_compose.sh` — 재합성 레시피
- `00_README.md` — 직원 가이드 + 함정 5선 요약

## ingest 작업 (gguy PC에서 수행)

```bash
# 1. wiki_pending에서 가져오기
cp Desktop/wiki_pending/yuri-ep02-8iter-success-case-2026-05-03.md \
   ccfm-wiki/wiki/cases/  # 또는 wiki/tacit/coding-lessons.md §[2026-05-03]에 append

# 2. 기존 함정 노트 4개도 같이 ingest
cp Desktop/wiki_pending/ugc-before-after-proof-2026-05-03.md ccfm-wiki/wiki/...
cp Desktop/wiki_pending/lipsync-multi-face-trap-2026-05-03.md ccfm-wiki/wiki/...

# 3. 커밋
git -C ccfm-wiki add .
git -C ccfm-wiki commit -m "cases: 율이 EP02 8회 iteration 성공 사례 + 함정 5선

- yuri-ep02-8iter-success-case-2026-05-03.md (참고용 종합 사례)
- ugc-before-after-proof: UGC 전후비교 인증 디자인
- lipsync-multi-face-trap: PIP 정지 사진 입 움직임 함정

메인 파이프라인은 /bj-vlog 스킬이 처리 (학습 반영)."
git -C ccfm-wiki push

# 4. graphify post-commit hook이 자동 그래프 리빌드
```
