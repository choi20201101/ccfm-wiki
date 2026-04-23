---
aliases: ["스킨케어 B/A 17초 파이프라인 (2026-04-23)"]
type: source
domain: content-ai-automation
brand: melable
product: 유쎄라블-2X-볼륨필인-앰플
confidence: high
created: 2026-04-23
updated: 2026-04-23
sources:
  - C:/Users/gguy/Desktop/bolbna/
  - C:/Users/gguy/Desktop/세포영상_3편_3인/
  - C:/Users/gguy/Desktop/14일변화_3인/
---

# src-skincare-ba-pipeline (2026-04-23)

## 검색 별칭 — 피부 B/A · 리프팅 영상 · 주름 영상 · 14일 변화 · 세포 애니 · 3인 여성 · 해골형 복원 · dramatic product reveal · 얼굴형 변화 영상 · 봄 스킨케어 · 볼꺼짐 해결

## 스킨케어 Before/After 14일 변화 영상 — 17초 표준 레시피 (재현 완료)

## 요약
[[src-volumefill-video-pipeline-2026-04-21]] 의 **실전 검증·재현 가능 최종판**. 볼륨필인 앰플 14일 변화를 3인 여성으로 3편 생성 성공. 17초 표준 구조로 락인 → 주름·기미·리프팅·탈모·다이어트 모든 B/A 카테고리 이식 가능.

## 17초 표준 구조 (복사해서 바로 사용)
```
0-2.5s   Day1 Kling (해골형/주름/기미 모션)     + "[페인] [구체 증상]"
2.5-4.5s 제품 Dramatic Reveal (Kling 회전+스파클) + "볼륨필인 앰플을 만나면" (제품명 교체)
4.5-7.5s 3D 세포 morph Kling (쭈글→탱탱)        + "세포가 파바박 차올라요" (원리 교체)
7.5-13s  14일 몽타주 (14 stills crossfade ~0.4s) + "[페인] [증상]이 14일 만에 이렇게 변화"
13-15s   Day14 Kling (탱글 미소 모션)
15-17s   Before/After 좌우 분할 + CTA
```

## 3인 × 배경 다양화
각 영상마다 다른 인물 + 다른 장소:
- **A**: bedroom dresser with curtains (여성 40대)
- **B**: bathroom white subway tile (여성 40대)
- **C**: reading nook with monstera plant (여성 40대)

- set_id 해시로 face seed + 장소 배정
- 같은 14일 progression 로직, 다른 비주얼 → 광고 피로도 회피

## 재현 레시피 (어떤 제품·카테고리든 동일)

### 자산 준비
```
face/ (19장+)           얼굴 원본 시드
bfex_split/before/      고민 상태 참조 (skull_unmask.png 같은 clean 버전)
bfex_split/after/       회복 상태 참조 (resolved_ref.png)
pd/product_hold.png     제품 누끼 (뚜껑 O)
pd/product_apply.png    제품 누끼 (드롭퍼)
```

### 핵심 규칙 (HARNESS)
1. **참조 모자이크는 먼저 인페인팅** ([[video-gen-lessons]] §26) — eye 영역만 clean 교체
2. **금지 키워드 엄수** ([[video-gen-lessons]] §27, §30)
   - ❌ shadow, dark, hollow, silhouette, outline
   - ✅ volume, fullness, bone curvature, plumpness
3. **같은 장소·같은 헤어·옷만 변경** ([[video-gen-lessons]] §28) — 14일 브이로그 느낌
4. **Day14 옷 명시적 변경** ([[video-gen-lessons]] §31) — "NOT a T-shirt, NOT same as Day 1"
5. **Day7+부터 after reference 주입** — shape guide로 점진 회복 강제

### 5단계 실행
```bash
# 1. 3D 세포 애니 시드 생성 ($0.08)
python -m scripts.gen_cell_product_assets

# 2. 3인 여성 × 14일 progression (42장 시드, ~$12)
python -m scripts.gen_14days_3women

# 3. 3편 영상 Kling + 합성 (Kling 6 클립, ~$2 / 영상당)
python -m scripts.gen_3vids_3women
```

## 비용·시간 (2026-04-23 실측)
| 항목 | 비용 | 시간 |
|---|---|---|
| 3D 세포 시드 × 2 + 제품 dramatic × 1 | $0.15 | 1분 |
| 3인 × 14일 시드 (42장 Gemini edit) | $1.70 | 8분 |
| Kling i2v 6 클립 × 3인 = 18 (세포·제품은 공유 2개 재사용) | $2.10 | 15분 |
| ElevenLabs TTS × 3 | $0.30 | 30초 |
| ffmpeg 합성 × 3 | $0 | 2분 |
| **합계** | **~$4.25** | **~27분** |

## 카테고리 이식 가이드

### 주름·리프팅
- Day1 참조: 깊은 팔자주름 + 눈가 주름 얼굴
- cells_shrunken: "dehydrated collagen fibers broken"
- 나레이션: "주름이 깊어졌어요 → 콜라겐이 끊어져서 → [제품]이 다시 연결 → 14일 만에 피부가 팽팽"

### 기미·잡티
- Day1 참조: 광대 위 색소침착 얼굴
- cells_morph: "melanin clusters dispersing/fading"
- 나레이션: "기미가 가득했어요 → 멜라닌 과다 → 녹여서 → 14일 만에 맑은 피부"

### 탈모
- Day1 참조: 정수리 휑한 샷
- cells_morph: "dormant hair follicles activating, new sprouts emerging"
- 14일 몽타주: 정수리 모발 volume 증가

### 여드름
- Day1 참조: 염증성 여드름
- cells_morph: "pore clogged → pore cleansed and healing"
- 14일 몽타주: 피부톤 개선

### 다이어트
- Day1 참조: 땅콩형 얼굴 + 몸매 샷
- cells_morph: (얼굴 볼륨 회복)
- 14일 몽타주: 얼굴형 갸름해짐

모든 카테고리 공통: **17s 구조 + 비주얼 4요소 유지**.

## 이번 세션에서 새로 배운 교훈 (tacit 승격)

### [[video-gen-lessons]] §30
"silhouette/outline" 키워드 → Gemini 검은 선 드로잉 유발 금지

### [[video-gen-lessons]] §31
Day14 옷 변경 강제 — `"NOT a T-shirt, NOT same as Day 1"` 명시적 negation

### [[video-gen-lessons]] §32
3D 세포 애니 기법 — Gemini t2i + Kling morph ($0.45 / 클립)

### [[video-gen-lessons]] §33
Dramatic Product Reveal — Chanel/Dior 급 럭셔리 CM 프롬프트 템플릿

### [[video-gen-lessons]] §34
17초 표준 구조 — 비주얼 4요소 (인물·제품·과학·몽타주) 모두 필요

## 플레이북 위치
- 코드·프롬프트 전체: `C:\Users\gguy\Desktop\bolbna\scripts\`
- 최종 산출물: `C:\Users\gguy\Desktop\세포영상_3편_3인\`
- 14일 시드 풀: `C:\Users\gguy\Desktop\14일변화_3인\Woman_{A,B,C}\Day01~14.png`
- 교훈 MD: `C:\Users\gguy\Desktop\bolbna\memory\feedback_*.md`
- HARNESS: `C:\Users\gguy\Desktop\bolbna\HARNESS.md`

## 관련 페이지
- [[src-volumefill-video-pipeline-2026-04-21]] (모체 파이프라인)
- [[src-diet-b2a-v2]] (초기 B/A 구조)
- [[src-talmo-b2a]] (탈모 이식 선례)
- [[content-ai-automation]]
- [[video-gen-lessons]] §26~34 — 이번 세션 학습

## 원본 위치
- 프로젝트 루트: `C:\Users\gguy\Desktop\bolbna\`
- 완성 영상: `C:\Users\gguy\Desktop\세포영상_3편_3인\A_침실_17s.mp4`, `B_욕실_17s.mp4`, `C_식물코너_17s.mp4`
- 14일 변화 스틸: `C:\Users\gguy\Desktop\14일변화_3인\Woman_A/B/C\Day01~14.png` (총 42장)
- clean 참조: `bolbna/bfex_split/before/skull_unmask.png` + `bolbna/bfex_split/after/resolved_ref.png`
