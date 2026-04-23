---
aliases: ["외국인 인플루언서 가이드"]
---

# src-foreign-influencer-guide

> 외국인 인플루언서 리뷰 영상 자동화 (메라블 루비알엔 피코샷 크림 / 기미 타겟) — 33편 완성. 제작일 2026-04-13 ~ 04-14.

- **원본**: `C:/Users/Administrator/Desktop/외국인인플루언서_자동화_가이드/` (raw 백업: [[raw/foreign-influencer-guide/README]])
- **프로젝트 루트**: `C:/Users/Administrator/Desktop/klinginter/`
- **산출물**: `Desktop/out/v001_final_v4.mp4 ~ v029_final_v4.mp4` (28편 단독) + `m001~m005_mashup.mp4` (5편 릴레이)
- **규격**: 9:16 세로 1080×1920, 30~45초, H.264+AAC, 한/영 이중 자막 + 상단 2줄 카피

## 1. 파이프라인 (fal.ai 경유)
1. 스크립트 YAML → 페르소나 매핑
2. Gemini 2.5 Flash Image (nano-banana): 메인 시드 + B&A 3종 + B-roll 시드 4개 (제품 라벨 유지)
3. Kling TTS × 11 씬 → 오디오 concat
4. **Kling AI Avatar v2 Pro** (fal.ai) 풀 립싱크 40초 → **병목, 2~5분/편**
5. Kling i2v 2.1 Pro B-roll × 4 병렬
6. Gemini 2.5 Flash Vision 자동 QC (거울 반사, 크림 입가, Q-tip 등 이슈 감지 → 재생성 1회)
7. FFmpeg filter_complex: pad 9:16 + overlay + ASS 자막 burn

## 2. 비용·시간 실측 (1편 = 40초)
| 항목 | 비용 |
|---|---|
| Avatar v2 Pro (40s) | **$4.60** |
| Kling i2v B-roll × 4 | $2.00 |
| Gemini 이미지 × 7 | $0.21 |
| Kling TTS × 11 | $1.10 |
| **합계** | **~$7.90/편** |

- 시간 평균 10~15분/편 (Avatar가 병목). 29편 순차 5~7h, 병렬 3편 ~2h
- 33편 실측 총 비용 ~$340 (자동 QC 재시도 20% 포함)
- 재렌더(자막만): 편당 1~2분 (Avatar 재사용, ffmpeg만)

## 3. Kling 직통 API는 비활성 (중요)
- 5개 Access Key × 복수 계정 모두 `code 1003 "Authorization is not active"` — 리소스 패키지 살아있어도 API 접근 권한 별도
- **해결: fal.ai가 Kling Avatar/i2v/TTS 전부 프록시** 제공, 안정적
- Kling 직통 원복하려면 CS에 `activate API access` 티켓 (24~48h)
- 교훈: **계약 전 API 호출 테스트 1회 의무화**

## 4. TTS voice 풀 (검증됨)
- EN 남: `uk_man2`, `uk_boy1`, `uk_oldman3`, `oversea_male1`
- EN 여/중성: `chat1_female_new-3`, `girlfriend_1_speech02`, `ai_shatang`, `ai_kaiya`, `tianmeixuemei-v1`, `guanxiaofang-v2`
- KO: ElevenLabs `Rachel` 기본
- ❌ 존재 안 함: `commercial_lady_en_f-v1`, `reader_en_m-v1`

## 5. 페르소나 축 (29명)
```yaml
gender: [male, female, gay_male, lesbian, trans_femme, trans_masc, non_binary]
ethnicity: [백인, 흑인, 한국계, 동남아, 라틴, 중동, 혼혈-흑백, 혼혈-아시아-백인]
age_range: [20대 초/후, 30대 초/후]
vibe: [에너제틱뷰티, 시크에디터, GRWM, 스킨케어덕후, Y2K아이돌, 샤이ASMR, 헬스브로, 소프트에스테틱, 드래그퀸]
setting: [화장대, 욕실거울, 차운전석, 호텔침대, 카페창가, 공원, 해변, 엘리베이터, 루프탑, 뉴욕길거리, 도쿄시부야, 파리발코니]
```
- 구조: HOOK(0-4s) → PAIN(4-10s) → PRODUCT(10-20s) → PROOF(20-30s) → CTA(30-35s)
- 각 영상 = 메인 립싱크 아바타 + B-roll 4개 (PAIN/PRODUCT/APPLY/CTA)

## 6. FFmpeg filter_complex 핵심
```bash
# 1440×1440 Avatar → 1080×1920 (상/하 검정 520px bar)
scale=1080:1080,pad=1080:1920:0:520:black,setsar=1

# B-roll overlay 체인 (시간대별 enable)
[0:v][broll1]overlay=0:520:enable='between(t,7.71,11.94)'[v1]
...
[vN]ass='subs.ass'[v]   # ASS 자막은 항상 최상단 (가리지 않게)
```
- **동적 인덱스 필수**: `n = len(broll_specs); sb_idx = n+1` — 하드코딩하면 입력 개수 바뀔 때 파싱 실패
- `scale` 의 `force_original_aspect_ratio=cover` **값 없음** → `increase` 또는 `decrease`만 사용

## 7. 할루시네이션 회피 프롬프트 패턴
### 메인 시드
```
Photorealistic vertical 9:16 selfie. {persona}.
Holding this exact pink 'melable RubyRN PicoShot' jar (reference),
keep label identical. Front-facing, mouth slightly open.
Exactly ONE person, no mirror reflections.
```
### i2v negative prompt (공통 표준)
```
multiple people, duplicate persons, mirror reflection, mirror,
extra arms, extra hands, deformed face,
cream in mouth, eating cream, licking product, jar near mouth,
cotton swab, applicator wand, Q-tip near face
```

## 8. 자동 QC (Gemini Vision)
```python
# 씬별 1프레임 캡처 → gemini-2.5-flash
"Check: (1) multiple people / mirror reflections, (2) cream near mouth,
(3) Q-tip on face, (4) deformed limbs. Reply JSON: {issues: [...]}"
```
- 이슈 있으면 해당 B-roll만 삭제 + 재생성 1회 재시도 → 전체 재생성 비용 방지

## 9. 스케일링 전망
- 100편: ~$605 · ~22h (단일 머신)
- 1000편: ~$6,050 · 5대 병렬 시 ~2일
- 비용 절감 수단: Ken Burns(zoompan)로 일부 i2v 대체 ($2/편), std vs pro 모드, 긴 TTS 1회 호출

## 10. 재사용 자산 인덱스
- `config/personas.yaml` — 페르소나 풀
- `config/creative_scripts.yaml` — 29개 창의 스크립트 (v002~v030)
- `products/melable_picoshot/seeds/` — 시드 이미지 (제품 라벨 유지 reference)
- `src/fal_kling.py`, `src/gemini.py`, `src/subtitle.py`, `src/batch_20.py`, `src/batch_mashup.py`, `src/fix_subs_c.py`

## 관련 지식
- [[content-ai-automation]] §13 — 본 도메인 통합본
- [[src-diet-b2a-v2]] — 같은 Kling + Gemini 조합의 다른 파이프라인 (셀피 립싱크 대신 모션 B/A)
- [[src-instarup]] — 업로드 단계 결합 후보 (본 파이프라인 산출물을 instarup으로 업로드)

*추가: 2026-04-15 (원본: Desktop/외국인인플루언서_자동화_가이드/)*
