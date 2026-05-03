# [실패 사례] sync-lipsync 다중 얼굴 함정 — 정지 사진이 말한다

**제목 후보**: "이렇게 만들면 안 된다 — 폰 PIP + lipsync 동시 적용"
**소속 도메인 후보**: `wiki/tacit/coding-lessons.md` 새 § 또는 `wiki/domains/performance-ad.md` `wiki/domains/ai-automation.md`
**confidence**: high (실패 케이스 직접 검증)
**source**: 2026-05-03 율이 EP02 광고 v05 빌드 실패
**triggered by**: 사용자 검토 — "사진 보여주는 장면에 사진이 더빙이 되어서 입이 움직임 / 이건 망한 거 같네"

---

## 한 줄

`fal-ai/sync-lipsync/v3` (sync.so v1/v2/v3 + wav2lip + musetalk 모두) 는 **영상 안에서 detect된 모든 얼굴**에 입 모양을 합성한다. 폰 PIP에 정지 사진을 띄우면 그 사진까지 말하는 것처럼 됨.

## 실패 시나리오

율이 EP02 v05 (50초 광고 / 7컷):

- **C2 컷 의도**: BJ 율이가 "한 달 전 내 얼굴이야 안 보정"이라며 폰을 카메라에 가까이 들어 옛 얼룩덜룩 사진을 보여줌. UGC 인증 디자인 규칙 완벽 준수 (폰 텍스트 0, 폰 크게, 디테일 보임)
- **시드 결과**: 완벽 — `seeds/C2_v05.png` 봐도 두 얼굴 (현재 율이 + 폰 안 옛 사진) 정확히 분리, 텍스트 없음, raw 디테일
- **Seedance 결과**: 양호 — 율이는 자연스럽게 말함, 폰 안 사진은 정지 (당연)
- **sync-lipsync v3 결과**: ❌ **폰 안 옛 사진까지 입이 움직임** → 두 얼굴이 동시에 같은 음성으로 말하는 그로테스크한 컷
- 시청자 즉시 "AI 합성" 인지 → UGC 인증 신뢰도 0

## Why (구조적 원인)

| 단계 | 모델 동작 |
|---|---|
| 1. face detection | 영상 안 **모든 얼굴 bbox** 검출 |
| 2. mouth region 추출 | 각 얼굴의 입 영역 mask |
| 3. audio-driven synthesis | 단일 audio → **모든 입에 동일 sync 적용** |
| 4. blend | 원본 영상 위에 합성 |

문제는 3단계 — `target_face_id` / `face_mask` / `bbox` 같은 영역 지정 파라미터 **없음**. fal sync-lipsync schema 확인. 모든 얼굴이 같은 음성에 sync됨.

## 어떤 모델도 같은 함정

- `fal-ai/sync-lipsync/v1` ❌
- `fal-ai/sync-lipsync/v2` ❌
- `fal-ai/sync-lipsync/v3` ❌ (검증 케이스)
- `fal-ai/wav2lip` ❌ (구조상 동일)
- `fal-ai/musetalk` ❌ (구조상 동일)
- `fal-ai/heygen/v3/lipsync/*` 미확인 (가능성 동일)
- `bytedance/omnihuman/v1.5` 회피 가능성 있음 (single-person 가정 모델)

## 해결책 (권장 순서)

### A. PIP 후처리 분리 (권장, 검증된 안전책)

```
[시드] 폰 화면을 빈 검정/회색으로 → [Seedance] 율이만 말함
  → [lipsync v3] 율이 1명만 detect → 안전
  → [ffmpeg overlay] 정지 PNG (옛 사진) 합성 → lipsync 후라 안 움직임
```

ffmpeg 의사코드:
```bash
ffmpeg -i lipsynced.mp4 -i past_photo.png \
  -filter_complex "[1:v]scale=400:-1[ph];[0:v][ph]overlay=480:340:enable='between(t,0,7)'" \
  out.mp4
```

폰 화면 좌표는 시드 단계에서 일정하게 잡고 motion tracking 필요시 OpenCV/AE.

### B. 컷 분할 (단순/빠름)

- 컷 A: 율이 토킹 (폰 X) → lipsync 적용
- 컷 B: 폰 화면 클로즈업 정지 (율이 음성만 voice-over) → lipsync 미적용

50s 합산 깨고 시간 재배정. 단순/빠름.

### C. 폰 PIP 자체 폐기

영수증·매장 사진·다 쓴 통 등 얼굴이 안 들어가는 인증으로 대체. 가장 안전하지만 본인 사진 효과 잃음.

## 다음 빌드 체크리스트

폰 PIP 또는 다중 얼굴이 한 컷 안에 등장할 때:

- [ ] **lipsync 적용 전** "이 컷에 detect 가능한 얼굴이 1개인가?" 자문
- [ ] 2개 이상이면 → 위 A/B/C 중 하나 적용
- [ ] 시드 단계에서 폰 화면을 비워두고 후처리 PNG overlay 권장
- [ ] 또는 폰 컷·토킹 컷 분할

## 연계 노트

- `ugc-before-after-proof-2026-05-03.md` — UGC 전후비교 디자인 룰 (이 함정과 묶어서 적용)
- 시리즈 ccfm-wiki §"AI 광고 자동화 함정 모음"에 추가 권장

## ingest 작업

`Desktop/wiki_pending/lipsync-multi-face-trap-2026-05-03.md` → 다른 PC에서 ccfm-wiki로:
```bash
cp Desktop/wiki_pending/lipsync-multi-face-trap-2026-05-03.md \
   ccfm-wiki/wiki/tacit/coding-lessons.md  # §lipsync-함정 append
git -C ccfm-wiki add . && git commit -m "tacit: lipsync 다중 얼굴 함정 (UGC 폰 PIP 실패 사례)"
```
