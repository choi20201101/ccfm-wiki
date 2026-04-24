---
type: source
domain: da-creative
confidence: high
created: 2026-04-20
updated: 2026-04-20
sources: [raw/skills/creative-autogen/, C:/Users/Administrator/Desktop/creative-autogen/, C:/Users/Administrator/Desktop/gptimege/, C:/Users/Administrator/Desktop/nari/]
---

# src-creative-autogen-framework

## 요약

**한 제품 · 1000장 DA 크리에이티브 자동 생산 프레임워크** (2026-04 실증).

ChatGPT 웹 UI (Playwright + CDP 9222) + GPT-Image 로 카피 1개 → 광고 이미지 1장 **1샷** 생성.
**이미지 모델 편집 체인 금지** — 1샷 통합이 fidelity 유지에 유리.

제품 교체 = PRODUCT_CONTEXT 문자열 + refs/ 폴더 내용만 바꾸면 끝. **신규 광고주 투입 ≤ 1시간**.

실증 사례:
1. **루비알엔 피코샷 크림** (메라블, 기미 미백) — 첫 1000장 파이프라인 구축
2. **네리티아 세럼 파운데이션** (PGA 세럼 파데) — 프레임워크 재사용 검증 (정리된 폴더 구조)

## 출력 스펙 (듀얼 aspect)

| 비율 | 용도 | 해상도 | 포맷 |
|------|------|--------|------|
| 1:1 | 인스타·페이스북 피드 | 1200×1200 (또는 1024↑) | JPG (용량 최적화) |
| 1250×560 | 네이버 GFA 메인 배너 | 정확히 1250×560 | PNG |

## 폴더 구조 (재사용 템플릿)

```
<project>/
├── README.md · SETUP.md · PLAN.md · HOOKS.md · CHANGELOG.md
├── scripts/
│   ├── pipeline.py       # PRODUCT_CONTEXT + 프롬프트 빌더 + 데이터 로더
│   ├── run_worker.py     # 워커 (--aspects 1x1 or wide 또는 둘 다)
│   ├── chatgpt_client.py # ChatGPT DOM 조작
│   ├── harness_vocab.py  # 한글 카피 치환·린트
│   ├── launch_chrome.py  # Chrome CDP 기동
│   ├── generate_copies.py# 엑셀 → copies.json
│   ├── modal_watcher.py  # rate-limit 모달 자동 클릭
│   └── supervisor.py     # 워커 감시·재시작
├── templates/            # 카피 공식·컬러·스타일 풀 문서
├── docs/                 # naver_banner_guide, chatgpt-dom-spec 등
├── hooks/                # on_rate_limit.py
├── refs/
│   ├── pd/               # 제품 누끼 (투명 배경 PNG)
│   ├── face/             # 얼굴 레퍼런스 10~12장
│   ├── best/             # 자사 베스트 성과 소재
│   └── best2/            # 범용 벤치마크 광고
├── state/                # checkpoint.json · logs/ · shot_history.jsonl
└── out/
    ├── 1x1/{final,raw}/
    └── main1250x560/{final,raw}/
```

## 창의성 차원 (1000장 중복 방지)

| 차원 | 개수 | 비고 |
|------|-----|------|
| FACE_TRENDS | 7 | **중안부 짧은 동안 얼굴 50% 주류** (2025~2026 한국 뷰티) + 베이비페이스·도자기·여신·단정·시크·생기소녀 |
| MODEL_POSES | 32 | 정적 14 + 동적 10 + UGC 셀피 8 |
| MODEL_EXPRESSIONS | 16 | 미소·수줍음·감탄·놀람·집중·윙크 |
| MODEL_GAZES | 10 | 카메라·허공·거울·제품·창밖·위·아래·감은눈 |
| MODEL_HAIRS | 15 | 생머리·웨이브·단발·업스타일·시스루 앞머리 |
| MODEL_MAKEUPS | 10 | 세미매트·글로시·누드·MLBB·쿨톤 누디 |
| MODEL_OUTFITS | 28 | 베이직·여성·트렌디·럭셔리 |
| LOCATIONS | 18 | 집·카페/외부·뷰티 공간 |
| SHOT_STYLES | 38 | photo 22 + illustration 10 + hybrid 6 |
| COLOR_PALETTES | 24 | 과도한 핑크 편중 방지 |
| ETHNICITY | 9 | 한국인 60% + 다양성 40% (가중 랜덤) |
| ILLUSTRATION_SUBSTYLES | 12 | 웹툰·순정·Pixar·벡터·수채화·지브리·민화 |

**최근 히스토리 회피**: `state/shot_history.jsonl` 에 매 생성 시 기록. 최근 6장 내 같은 SHOT_STYLE 2회 초과 시 풀에서 제외.

## 후처리 (fit_to_exact)

### 1:1
- GPT 원본(보통 2048²) → 중앙 정사각 crop → 1200×1200 LANCZOS → JPG quality 92.

### 1250×560 — 네이버 DA 공식 `Image_M_DA_total_PF.pdf` 준수

```python
SAFE_L, SAFE_R, SAFE_T, SAFE_B = 240, 240, 50, 35   # 텍스트 기준
SAFE_W, SAFE_H = 770, 475                            # 오브젝트는 225px 로 완화 가능

# Layer 1: blur-extend bg (자연스러운 배경 연장)
work = (1250*2, 560*2)
bg = img.resize(cover(src, work)).crop(center).resize((1250, 560))
bg = bg.filter(GaussianBlur(28))
bg = Brightness(bg).enhance(0.92)

# Layer 2: safezone 원본 오버레이
scale = min(SAFE_W / src_w, SAFE_H / src_h)
content = img.resize((int(src_w*scale), int(src_h*scale)))
bg.paste(content, (SAFE_L + (SAFE_W - new_w)//2, SAFE_T + (SAFE_H - new_h)//2))
```

**이 방식 쓰는 이유**: 네이버 공식 반려 사유 = "좌/우 영역을 **이질적 컬러·흰색·빈 여백**으로 채운 경우". 단순 letterbox (solid color) = 반려. blur-extend 로 원본 배경을 자연 연장해야 통과.

## 운영 패턴 (무인 야간)

- `pythonw.exe` + `CREATE_NO_WINDOW=0x08000000` → 콘솔 창 안 뜸
- `supervisor.py`: 30초 감시, 죽으면 15초 내 재시작
- `modal_watcher.py`: rate-limit 모달 자동 "알겠습니다" 클릭
- 체크포인트 per aspect: `completed_1x1`, `completed_wide` 분리
- 장간 대기 90초 × 워커 2개 = **평균 45초/장, 1000장 ≈ 12시간**
- Rate limit 감지 시 메시지에서 "N분 후" 파싱 → 자동 백오프 (한/중/영 3언어 지원)
- **2 워커 기준 실측**: 하루 200~350장 (rate-limit 주기에 따라)

## 하네스 (카피 자동 린트)

`harness_vocab.py::_FORBIDDEN_SUBS` 258+ 패턴:
- 조사 오류 자동 교정 (기미이 → 기미가, 선생님가 → 선생님이)
- 신조어·일본어 잔재 → 자연 한국어 (쿨하다 → 멋있다, 츤데레 → 까칠한 척)
- 성분명 → 친숙어 (PDRN → 피부 재생 성분, 앞타알부틴 → 미백 성분)
- 방송사 로고·허위 의료효능 과장 금지
- 중복 오타 (만에만에 → 만에)
- CREAM_PHRASES 93개 / TROUBLE_PHRASES 61개 / HOOK_PHRASES 65개 / SHORT_BADGES 50개 랜덤 풀

## 1샷 프롬프트 구조 (build_oneshot_prompt)

1. 레퍼런스 99% 충실 복제 지시 (레이아웃·타이포·색감)
2. 슬롯 교체 원칙 (모델·제품·카피만 교체, 배치는 레퍼런스 그대로)
3. 포맷 힌트 (best_ref 파일명 기반)
4. 촬영 스타일 + 컬러 팔레트
5. 제품 누끼 그대로 규칙 (라벨 왜곡 금지)
6. 모델 블록 — 민족 + 얼굴 유형 + 포즈·표정·시선·헤어·메이크업·의상·장소
7. 피부 규칙 (도자기 금지, 실제 질감)
8. 서브카피 1~3개 가중 랜덤 (0.35 / 0.40 / 0.25)
9. aspect 별 출력 규격

## 제품 교체 체크리스트 (1시간)

1. `scripts/pipeline.py::PRODUCT_CONTEXT` 브랜드·성분·USP·타겟 문구 교체
2. `refs/pd/<product>.png` 누끼 투입
3. `refs/face/*` 타겟 분위기 얼굴 10~12장 교체
4. `refs/best/*` 자사 베스트 (있다면), `refs/best2/*` 범용 벤치마크
5. 카피 엑셀 → `python scripts/generate_copies.py --xlsx xxx.xlsx --n 1000`
6. `python scripts/launch_chrome.py` → ChatGPT 수동 1회 로그인
7. 워커 기동: `python scripts/run_worker.py --worker 0 --total 2 --aspects 1x1 &`

## 폐기된 접근 (시행착오)

| 시도 | 이유 |
|------|------|
| 3단계 편집 체인 (모델→제품→카피) | edit 연쇄로 fidelity 붕괴. 1샷 통합으로 전환 |
| 1875×840 생성 후 중앙 1250×560 크롭 | "크롭 예정" 지시가 GPT 구도를 과도 확대 중앙으로 몰아감 |
| 코너-색 단색 letterbox | 네이버 공식 반려 (이질적 컬러·빈 여백) |
| 좌/우 std 비교로 edge-hug 판정 | 모델(복잡) vs 텍스트(단순) 구분 못 함 |
| 한글 카피 GPT 직접 렌더 | 오타·철자 오류 빈발. 생성 후 Gemini OCR QC → Nano Banana Pro 정밀 리터치 권장 |

## 관련 페이지
- [[da-creative]] · [[creative-patterns]] · [[content-ai-automation]]
- [[src-diet-b2a-skill]] (동일 BDH 프레임워크 패턴)
