---
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-21
updated: 2026-04-21
sources:
  - C:/Users/gguy/Desktop/gpt/projects/volumefill/
  - wiki/sources/src-volumefill-pipeline-2026-04-20.md (v1)
---

# 볼륨필인 파이프라인 v2 — 성공 패턴 심화 확장 (2026-04-21)

> v1([[src-volumefill-pipeline-2026-04-20]]) 이후 24시간 내 사용자 피드백을 반영해
> 실전 qc 통과율·창의성·다양성을 크게 끌어올린 심화 버전. 결과물 퀄리티 매우 높음.

## 🎯 v1 → v2 핵심 개선점

### 1. 컷 변주 10종 체계화 (모델 컷)
**비율 기반 가중 로테이션** — 한 가지 구도 반복 방지. 각 컷마다 별도 프롬프트 블록.

| 컷 타입 | 비율 | 설명 |
|---|---|---|
| holding | 18% | 모델 1명 제품 들고 있기 (뚜껑 O) |
| palm_pour | 9% | 손바닥에 제형 덜기 (뚜껑 X) |
| applying_hand | 9% | 손등·손목에 바르기 |
| applying_face | 9% | 얼굴에 바르기 클로즈업 |
| procedure_style | 9% | 시술풍 집중 홈케어 |
| multi_model_holding | 9% | 2~3명 다함께 들기 (시선집중↑) |
| multi_model_lifestyle | 9% | 2~3명 일상 루틴 |
| **character_juxtaposition** | 18% | **해골·땅콩·건자두 캐릭터 병치 (B/A 우회)** |
| **dried_squid_5stage** | 9% | **마른오징어 5단계 변신 유머 (SNS 스탑)** |
| **annotation_pointer** | 18% | **보라 점선·화살표 튜토리얼 마킹** |

### 2. 연상 키워드 뱅크 120개 (hook_ideas.md 섹션 N)
4050대 한국 중년 여성이 "아 얼굴 푹 들어간 거구나" 바로 연상하는 키워드 대량 수집:
- **사물 30개**: 해골 · 건포도 · 건자두 · 건어물 · 바람빠진풍선 · 꺼진쿠션 · 시든상추 · 구겨진신문지 · 꽁꽁짜낸치약 …
- **음식 22개**: 땅콩 · 대추 · 호두껍질 · 귤껍질 · 먹다남은사과심 · 북어 · 김빠진맥주 …
- **얼굴형 직관 12개**: 땅콩형 · 해골라인 · 아귀형 · 계란껍데기깨진 것 …
- **장소 16개**: 가뭄 논 · 물빠진 수영장 · 텅빈 창고 · 거미줄샹들리에 · 꺼진 벽난로 …
- **캐릭터 12개**: 좀비 · 해골이모지 · 구운고등어 · 빼빼로막대 …
- **감각 12개**: 볼 누르면 쑥 들어감 · 블러셔 올려도 생기 없음 · 큰 마스크 벗으니 가죽만 …
- **상황/트리거 16개**: 동창회 앞 · 상견례 전 · 독박육아 3년 · 갱년기 시작 …

### 3. 카피 품질 규칙 — 밍밍 금지 + 구체성 3박자
사용자 피드백 "문득 보니 피부가 괜찮아요" 너무 약함 → **[상황/행위] + [구체 부위] + [의성어·감탄·반응]** 공식.

❌ 약함: "문득 보니 피부가 괜찮아요"
✅ 강함: "**문득 거울 보니 볼 꺼짐 엇 하고 놀랐어요**"

의성어 풀: 어? / 엇 / 오? / 응? / 어머 / 헉 / 어라 / 헐 / 음?

### 4. 궁금증 유발 (Curiosity Gap) 패턴
말줄임표로 독자 클릭 유도. 전체 카피의 30% 이하 비율.

- "친구들이 해골 같다고 놀려서 발랐는데..."
- "50대인데 동창회 갔더니 다들 언제 만난 사이냐고..."
- "평생 콜라겐만 바르다가 이거 한 번 바르고..."

### 5. 자연스러운 한국어 어법
번역투·딱딱한 명사 나열 금지. 연결 어미 활용.

❌ "약국 입점 앰플 꾸준히 써보니"
✅ "꾸준히 쓰니까 역시 약국앰플" / "한 달 쓰고 나니 왜 약국에 있는지 이해됨"

### 6. 글로벌 카피 캡 (인증마크 남발 방지)
ref 가 10~20개라도 최종은 엄격히 캡:
- 메인 카피 ≤ **3개**
- 서브 카피 ≤ **4개**
- 배지·인증마크 ≤ **2개**

사용자 피드백 "AI_볼륨필인_0190 인증마크 20개 가까이" → 즉시 캡 추가.

### 7. 레퍼런스 원본 카피 동적 금지 목록
ref_loader가 각 ref MD에서 **원본 카피 텍스트 자동 추출** → 워커 프롬프트에 "이 문구 절대 사용 금지" 동적 주입.

예: 치약 광고 ref → "❌ 무시무시한 치약입니다 / 모태누렁니도 백지처럼…" 7개 문구를 프롬프트에 명시.

### 8. 11종 민족 가중 분포
한국 40% / 한·백 혼혈 16% / 백인 12.5% / 라틴 10% / 흑인 6% / 중동 4.5% / 한·흑 혼혈 4% / 남미 3% / 동남아 2% / 일본 1.5% / 알비노 0.5%.

### 9. 첨부 순서 최적화 (Codex 리뷰 반영)
- 제품 drift 우선: **pd0 첫 첨부** (single source of truth · OpenAI 문서: 첫 이미지 fidelity 최고)
- 순서: 제품 누끼 → 레퍼런스 → (컷별 2차 제품) → 로고 → 얼굴

### 10. 의료 시술 마스킹 O → O 통일
- "시X" 는 'ㅅㅂ' 연상 위험 → **"시O"** 로 전환
- 필O · 시O · 보O스 · 주O

### 11. 뚜껑 유무 기반 pd 자동 선택
- holding / multi_model_holding → **pd0/pd1 (뚜껑 O)**
- palm_pour / applying_* / procedure / dried_squid / texture_flow → **pd2 (뚜껑 X 제형 쏟아짐)**

### 12. 타사 로고·브랜드명 → melable 강제 치환
ref 의 타사 로고 위치에 **melable 로고 (첨부 3번)** 로 자동 치환.
melable 로고 = "검정 x 마크 + melable 고딕 볼드".

### 13. Rate Limit 안정화
- ChatGPT "17시간 대기" 엄살 → 실제 20~30분이면 풀림
- 워커 backoff 30분 캡
- 1탭 운영 (2탭은 너무 빨라 rate limit 반복 트리거)
- gap 30초 → **45초** 상향

### 14. JPG 포맷 전환
- 다운로드: PNG (ChatGPT 기본)
- 저장: **1200×1200 JPG (quality 92)**
- 파일명: `AI_볼륨필인_XXXX.jpg`
- 임시 PNG 자동 삭제

### 15. QC 파이프라인 8축 체크
Gemini 2.5 flash vision + gemini-2.5-flash-image 자동 수정.

| 체크 | 종류 |
|---|---|
| competitor_logo | hard fail |
| medical_doctor | hard fail |
| celeb_lookalike | hard fail |
| **category_mismatch** | hard fail (치약/샴푸 등 다른 카테고리 감지) |
| **reference_copy_bleed** | hard fail (레퍼런스 카피 잔존) |
| product_drift | soft/hard |
| korean_typo | soft |
| banned_words | soft |

fail 이면 자동 수정 + 원본 backup (`out/final_original/`), 실패 시 `out/qc_failed/` 분류.

## 📊 운영 성과

- **24시간 내 200+ 이미지 자동 생성**
- 사용자 만족도: "아주좋네 훨씬 좋아짐 매우 좋아짐"
- QC 자동 수정률 ~20% (200 중 ~40장 자동 교정)
- Rate limit backoff 반복되지만 30분 캡 + 1탭으로 안정 운영

## 🔗 관련 위키
- [[src-volumefill-pipeline-2026-04-20]] — v1 (초기 파이프라인)
- [[content-ai-automation]]
- [[da-creative]]
- [[creative-patterns]] / [[coding-lessons]] — 암묵지

## 📁 핵심 파일 (v2 기준)

```
projects/volumefill/
├── config.json               ← product_context · copy_policy
├── pd/ pd0/1/2.png           ← 뚜껑 O 2장 + 뚜껑 X 1장
├── face/ (38장)              ← 얼굴 레퍼런스 풀 확장
├── best/ (123장) + best_refs/(123 MD) ← 레퍼런스 구조 분석
├── canvas/ 01·02·03.md       ← 퍼포먼스 캔버스
├── rejection_rules.md        ← GFA 회피 + 마스킹 + B/A 우회 12종
├── model_guide.md            ← quiet luxury + 11종 민족
├── product_identity.md       ← 실물 기반 제품 스펙
├── product_size.md           ← 6종 크기 표현 블록
├── hook_ideas.md             ← 180+ 후킹 + 120 연상키워드 + 스타일 20
├── logo/images.png           ← melable 로고
└── state/                    ← copies.json · checkpoint · qc_log · logs

scripts/
├── analyze_best_refs.py      ← Gemini 비전 분석
├── ref_loader.py             ← 롤링 + 동적 금지어 추출
├── generate_copies_project.py← 14 페르소나 + 180+ 후킹 + 위트
├── run_worker_project.py     ← 10종 컷 + 11 민족 + 8축 캡 + 로고 주입
├── run_worker_alt.py         ← 1/2탭 오케스트레이터
├── supervisor_project.py     ← Chrome+워커 감시
└── qc_gemini_pipeline.py     ← Gemini QC + 자동 수정
```

## 🚀 신규 프로젝트 적용 체크리스트

1. scaffold (`new_project.py`)
2. 자산 준비: pd 누끼 (뚜껑 O + X), face 20~40장, best 레퍼런스 100+
3. 규칙 MD 6종 제품별 맞춤 작성 — **본 v2 구조를 템플릿으로**
4. logo/ 자사 로고 배치
5. 분석기 실행 → 카피 생성 → supervisor + QC 파이프라인 기동
6. 1탭 · 45초 gap 으로 시작 (rate limit 안정)
