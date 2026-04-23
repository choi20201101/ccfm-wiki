---
type: source
domain: content-ai-automation
brand: melable
product: 유쎄라블-2X-볼륨필인-앰플
confidence: high
created: 2026-04-21
updated: 2026-04-21
sources:
  - C:/Users/gguy/Desktop/bolbna/
  - C:/Users/gguy/Desktop/B&A_영상_플레이북/
---

# src-volumefill-video-pipeline (2026-04-21)

## 검색 별칭 — 볼륨필인 영상 · B/A 릴스 · 14일 변화 · 주름 리프팅 · 스킨케어 퍼포먼스 · 볼꺼짐 앰플 · 해골라인 · 3인 릴레이 · 저도 해결했어요 · 아바타 말하는 장면

## 볼륨필인 앰플 Day1→Day14 변화 릴스 공장 — 완성 파이프라인

## 요약
[[src-diet-b2a-v2]] 다이어트 B/A 파이프라인과 [[src-foreign-influencer-guide]] 외국인 인플루언서 자동화를 **통합·심화**한 버전.
볼륨필인 앰플 (유쎄라블 2X) 퍼포먼스 영상 40편 공장 기획 → 8편 + 리믹스 15편 + Trio 10편 = **33편 완성**.
Gemini 2.5 Flash Image edit(nano-banana) + Kling i2v v2.6 master + ElevenLabs multilingual_v2를 fal.ai 프록시 경유.

## v1과 v2의 본질적 차이 — "얼굴형 시드 분리"
[[src-diet-b2a-v2]]은 동일 인물 Before/After 2씬만. 본 파이프라인은 **동일 인물 14일 일자별 변화**로 한 단계 심화.

핵심 기법:
1. **face/** 폴더 원본 얼굴 2장 = **정체성 시드**
2. **bfex_split/before/** 폴더 3장 = **얼굴형(볼꺼짐 패턴) 시드**
3. Gemini edit에 두 종류 시드 + shape-only 프롬프트 → "세상에 없는 인물 × 극적 볼꺼짐" 생성
4. Day1 결과물을 앵커로 Day2~14 순차 생성 — 복장/시간/조명 변화 + 볼륨 선형 회복

## 영상 구조 9종 + Trio 릴레이 — **시네마틱 기승전결 변형**
v1은 단조로웠던 B→A 단일 구조. v2는 **구조를 해시로 배정**해서 같은 자산으로 여러 스토리텔링 가능.

| 구조 | 길이 | 오프닝 기법 |
|---|---|---|
| A_classic | 15s | Day1 셀카 |
| B_shock_open | 15s | **B/A 분할 플래시** (1-2초) |
| C_14first | 15s | **Day14 자신감 먼저 → 플래시백** |
| D_product_open | 15s | **제품 hold 정지 프레임** |
| E_montage_open | 15s | **14일 빠른 몽타주** 후킹 |
| F_5beat | 15s | Day1 → 5비트 하이라이트 (1/4/7/10/14) |
| G_vlog_20s | 20s | **3일 단위 + speaking 2회 인터리브** |
| H_story_20s | 20s | Day14 → 플래시백 → speaking → 긴 몽타주 |
| I_diary_20s | 20s | **일기장 스타일** 3일 단위 + speaking × 2 |
| **Trio 릴레이** | 20s | **3인 동시 등장** "저도 해결!" + triple_split |

### Speaking 클립 기법 (신규)
- Day7 시드 → Kling i2v "mouth slightly opens as if asking a question"
- Day11 시드 → Kling i2v "confidently addresses camera, warm half-smile"
- 아바타 립싱크 없이 **'말하는 듯한 표정만' 2초 컷**으로 vlog 느낌 연출
- 나레이션은 기존 TTS가 이어지며 시청자가 '말하는 장면'으로 인지

## 창의 배리에이션 축 (결정론적 해시 배정)

| 축 | 옵션 수 | 구현 |
|---|---|---|
| 페르소나 | 6 | 독박육아·해골라인·필러대체·동창회·결혼식·체중감량 |
| 장소 | 8 | bathroom/livingroom/bedroom/kitchen/home_office/closet/balcony/reading_nook |
| 시간대 | 3 | evening/morning/afternoon (일자별 주기) |
| 복장 | 30+ | 초반 7 × 중반 7 × 후반 7 × Day14 finale 10 풀 |
| 민족(영문) | 11 | Caucasian/Latina/Japanese/Thai/... |
| TTS 보이스 | 5 | ElevenLabs 순환 |
| CTA 가격 | 10 | 1+1 69% / 48% 할인 / 55ml / 당일출발 |
| CTA 액션 | 12 | 14일 챌린지 / 30일 환불 / 간미연 PICK |

## 이번 세션에서 새로 배운 교훈 (tacit 승격 대상)

### 크리에이티브
- [[creative-patterns]]: **"Day 1에 bfex 얼굴형 시드를 face seed와 별도로 주입하면 극적 볼꺼짐이 재현됨"** — face seed만으로는 Gemini가 볼꺼짐을 약하게 그림. shape reference를 마지막 입력으로 넣고 "ONLY shape guide, NOT identity" 명시해야 효과 극대화.
- [[creative-patterns]]: **"Day 2~6 조기 회복 방지 → prompt에 'ALMOST IDENTICAL to Day 1, barely 5% changed' + bfex 재주입"** — Gemini는 volume_state prompt를 너무 관대하게 해석. Day 2부터 이미 플럼핑되는 문제 해결.
- [[creative-patterns]]: **"아바타 말하는 장면을 립싱크 없이 표정만으로 연출 가능"** — Day7/11 seed에 'mouth slightly opens, asking question' prompt만으로 vlog 느낌. 비용 저렴 ($0.35), OmniHuman 아바타 대비 95% 효과.
- [[creative-patterns]]: **"3인 릴레이 trio 패턴 = '저도 해결했어요!' 공감대 자극"** — 같은 제품·다른 페르소나 3명 = 연령·상황 폭 넓힘. Triple split (360×1920 × 3) 엔딩으로 통합감.
- [[creative-patterns]]: **"구조 9종 × 자산 재활용 = 리믹스 무한대"** — 시드·Kling·TTS 모두 재사용 가능, ffmpeg 합성만 구조 바꿔 신규 영상 ~1분 생성.
- [[creative-patterns]]: **"Day14 복장 10종 풀이 '같은 영상 반복' 느낌 방지"** — 처음엔 고정 burgundy silk blouse → 모든 영상 엔딩 동일 → 풀에서 hash 선택으로 다양화.

### 코딩/자동화
- [[coding-lessons]]: **"fal.ai 프록시가 Kling 직통 API 1003 에러 우회"** — diet v1~v2 시대 교훈 유지 ([[src-diet-b2a-skill]] § 1). 2026-04-21 현재도 fal.ai가 가장 안정.
- [[coding-lessons]]: **"Gemini edit API에 한글 파일명 업로드 시 httpx UnicodeEncodeError"** — Content-Disposition 헤더 ASCII 인코딩. 제품 누끼 등 ASCII 사본 필수 (`product_hold.png` etc.).
- [[coding-lessons]]: **"Windows ffmpeg subtitles 필터 절대경로 콜론 파싱 실패"** — `subtitles=C:/path/subs.ass` 에러. 해결: cwd를 work dir로 변경 후 상대 파일명만 전달. `_run(cmd, cwd=work)` 패턴.
- [[coding-lessons]]: **"Kling i2v negative_prompt에 'cheek plumping in motion, face smoothing during clip' 필수"** — 기본 Kling은 '예쁘게' 비유화. 이 문구 없으면 Day1의 극적 볼꺼짐이 3초 안에 플럼핑됨.
- [[coding-lessons]]: **"PIL에서 한글 텍스트 쓸 때 arialbd.ttf 금지"** — 한글 박스 깨짐. malgunbd.ttf 또는 S-Core Dream만 사용.
- [[coding-lessons]]: **"ElevenLabs multilingual_v2 한국어 숫자 오독 방지 — chunk를 {sub, tts} 분리"** — `"14일"` → TTS `"십사일"` / 자막 `"14일"`. `"1+1"` → TTS `"원플러스원"` / 자막 `"1+1"`. 이중 맵핑 필수.
- [[coding-lessons]]: **"ASS 자막 Persistent 상단 고정 라인은 오히려 산만"** — repcak 스펙 초기에 Persistent bar 도입했으나 사용자 "카피 삭제" 피드백 → 깔끔한 하단 자막만 유지가 더 효과적.
- [[coding-lessons]]: **"atempo 1.0~1.6 캡으로 TTS 자동 목표 길이 맞춤"** — TTS 길이가 영상 길이 초과 시 atempo 필터로 자동 압축. 1.6 초과 시 어색.
- [[coding-lessons]]: **"구조를 set_id 해시로 배정하면 결정론적 다양화"** — 같은 세트 재실행 시 동일 구조 → 재현성. 40편 × 9구조 분포가 해시만으로 자연스럽게 균등.

### 심리/설득
- [[psychology-insights]]: **"Day14 Before/After 좌우 분할이 퍼포먼스 릴스의 감정 포텐셜 피크"** — 단일 셀카보다 B/A split 엔딩이 클릭률·체류시간 최고. BEFORE(빨강)/AFTER(녹색) 컬러 대비 필수.
- [[psychology-insights]]: **"3인 릴레이에서 '저도/저도/저도 해결!' 반복이 의사결정 가속"** — 단일 인물 testimonial보다 3인 연쇄가 '저도 가능하다' 공감 증폭. 나이 폭 30·40·50대 걸치면 효과 극대화.
- [[psychology-insights]]: **"제품 hold 정지 프레임 오프닝이 '약국템' 권위 전달"** — 제품을 모션 리빌 대신 정적 프레임으로 시작하면 '전시된 상품' 느낌. D_product_open / T07_pharmacy_trust 구조의 핵심.

## 통합 파이프라인 구조
```
[00] api.txt           ─ fal/eleven/kling keys
[01] face/             ─ 얼굴 원본 19장
[02] bfex_split/before ─ 얼굴형 참조 3장 (prep_bfex.py로 B/A 합본 분할)
[03] pd/               ─ 제품 누끼 2장 (ASCII 파일명)
[04] prompts/          ─ scripts_ko.json + scripts_en.json + trio_variants.json
[05] setscene.py       ─ 장소/복장/시간대/볼륨상태 결정론 배정
[06] structures.py     ─ 9 구조 템플릿
[07] cta_pool.py       ─ CTA 풀 22종
[08] step1            ─ Day1 시드 (face 2 + bfex 1)
[09] step2            ─ Day2-14 + reveal + apply + hold
[10] step3            ─ TTS atempo fit
[11] step4            ─ Kling 6 클립 (day01/reveal/apply/day14 + speaking_mid/late)
[12] step5            ─ ffmpeg 구조 기반 합성
[13] run_all.py       ─ 세트 1개 전체 오케스트레이터
[14] remix.py         ─ 기존 자산 다른 구조 재합성
[15] trio.py          ─ 3인 릴레이 공통 스토리 (10 variants)
```

## 비용 실측 (1편 = 15~20초)
| 항목 | 비용 |
|---|---|
| Gemini 2.5 flash image × 16~17장 | $0.50 |
| Kling i2v × 4~6 클립 | $1.40~2.10 |
| ElevenLabs TTS (~14s) | $0.10 |
| ffmpeg 합성 | $0 (로컬) |
| **합계** | **~$2.00~2.70/편** |

- 40편 배치: ~$100 (~6시간)
- 리믹스(기존 자산 재사용): $0, ~1분/편

## 적용 도메인 확장
본 패턴은 **모든 짧은 B/A 피부·리프팅 퍼포먼스 영상**에 적용 가능:
1. 볼륨 앰플·크림 (주름·해골라인) — 본 프로젝트
2. 기미·잡티 크림 — 색소 개선 B/A
3. 탈모·헤어 — 정수리 확대 ([[src-talmo-b2a]])
4. 눈가 리프팅 — 다크서클·처짐
5. 여드름·홍조 — 피부톤 개선
6. 다이어트 — 체형+얼굴 볼륨 변화 ([[src-diet-b2a-v2]])

**핵심 반복 가능 패턴**:
- bfex 폴더에 Before 샘플만 바꾸면 도메인 교체
- scripts_ko.json 페르소나만 새로 쓰면 스토리 교체
- structures.py는 그대로 재사용

## 플레이북 위치
- **코드·프롬프트 전체 번들**: `C:\Users\gguy\Desktop\B&A_영상_플레이북\`
- HARNESS.md 포함 — v8 통과 기준 품질 락인 규칙 12섹션

## 관련 페이지
- [[src-diet-b2a-v2]] — 모체 파이프라인
- [[src-talmo-b2a]] — 탈모 도메인 포팅 선례
- [[src-foreign-influencer-guide]] — 외국인 인플루언서 버전 (Avatar v2 Pro 포함)
- [[src-volumefill-pipeline-v2-2026-04-21]] — 정지 이미지 광고 버전
- [[content-ai-automation]]
- [[da-creative]]
- [[video-gen-lessons]] / [[creative-patterns]] / [[coding-lessons]] / [[psychology-insights]]

## 원본 위치
- 프로젝트 루트: `C:\Users\gguy\Desktop\bolbna\`
- 완성 영상: `C:\Users\gguy\Desktop\bolbna_assets\finals\` + `remixes\` + `C:\Users\gguy\Desktop\trio_10편\`
- 플레이북 배포 번들: `C:\Users\gguy\Desktop\B&A_영상_플레이북\`
