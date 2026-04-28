# Graph Report - .  (2026-04-28)

## Corpus Check
- Large corpus: 475 files · ~287,509 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 181 nodes · 220 edges · 31 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_iboss 201건 지식베이스 (최재명)|iboss 201건 지식베이스 (최재명)]]
- [[_COMMUNITY_AI 아바타영상 툴|AI 아바타/영상 툴]]
- [[_COMMUNITY_기타 gen_seeds.py|기타: gen_seeds.py]]
- [[_COMMUNITY_바이브코딩 & 에이전트 스택|바이브코딩 & 에이전트 스택]]
- [[_COMMUNITY_QSCV 문서 추출 코드|QSCV 문서 추출 코드]]
- [[_COMMUNITY_기타 kling_client.py|기타: kling_client.py]]
- [[_COMMUNITY_기타 lib.py|기타: lib.py]]
- [[_COMMUNITY_기타 detect_faces.py|기타: detect_faces.py]]
- [[_COMMUNITY_기타 gen_kling.py|기타: gen_kling.py]]
- [[_COMMUNITY_기타 gemini_client.py|기타: gemini_client.py]]
- [[_COMMUNITY_로고 제거 기술|로고 제거 기술]]
- [[_COMMUNITY_본사 사업마케팅 (최재명·네이버·GFA)|본사 사업/마케팅 (최재명·네이버·GFA)]]
- [[_COMMUNITY_기타 inject_aliases_from_h1.py|기타: inject_aliases_from_h1.py]]
- [[_COMMUNITY_기타 inject_iboss_entities.py|기타: inject_iboss_entities.py]]
- [[_COMMUNITY_기타 inject_korean_aliases.py|기타: inject_korean_aliases.py]]
- [[_COMMUNITY_기타 detect_face.py|기타: detect_face.py]]
- [[_COMMUNITY_기타 make_overlays.py|기타: make_overlays.py]]
- [[_COMMUNITY_기타 qa_check.py|기타: qa_check.py]]
- [[_COMMUNITY_기타 analyze_bgm.py|기타: analyze_bgm.py]]
- [[_COMMUNITY_기타 gen_scales.py|기타: gen_scales.py]]
- [[_COMMUNITY_그래프 인덱싱 스크립트|그래프 인덱싱 스크립트]]
- [[_COMMUNITY_기타 export.py|기타: export.py]]
- [[_COMMUNITY_기타 run_all.py|기타: run_all.py]]
- [[_COMMUNITY_기타 validate_input.py|기타: validate_input.py]]
- [[_COMMUNITY_기타 build_prompts.py|기타: build_prompts.py]]
- [[_COMMUNITY_기타 check_session.py|기타: check_session.py]]
- [[_COMMUNITY_기타 inject_diet_b2a_v2_aliases.py|기타: inject_diet_b2a_v2_aliases.py]]
- [[_COMMUNITY_기타 build_sets.py|기타: build_sets.py]]
- [[_COMMUNITY_기타 Run full graphify pipeline on|기타: Run full graphify pipeline on ]]
- [[_COMMUNITY_기타 롤링발칸 (월 500~2500 소재 테스트)|기타: 롤링발칸 (월 500~2500 소재 테스트)]]
- [[_COMMUNITY_기타 설득 9요소 (상호성·희소성·권위 등)|기타: 설득 9요소 (상호성·희소성·권위 등)]]

## God Nodes (most connected - your core abstractions)
1. `iboss 201건 인덱스 (2017-2026)` - 9 edges
2. `main()` - 7 edges
3. `main()` - 7 edges
4. `main()` - 7 edges
5. `AI 무중단 스튜디오 일매출 8천만` - 7 edges
6. `mosaic()` - 6 edges
7. `extract()` - 5 edges
8. `_detect_in_clip()` - 5 edges
9. `compose_v1()` - 5 edges
10. `compose_v23()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `i-boss 게시판 (근육돌이)` --indexes--> `iboss 201건 인덱스 (2017-2026)`  [EXTRACTED]
  wiki/sources/src-iboss-choi-jaemyeong.md → raw/iboss/INDEX.md
- `메타 광고 (페이스북·인스타)` --documented_in--> `iboss 201건 인덱스 (2017-2026)`  [EXTRACTED]
  wiki/sources/src-iboss-choi-jaemyeong.md → raw/iboss/INDEX.md
- `video1()` --calls--> `mosaic()`  [EXTRACTED]
  raw\skills\diet-b2a\scripts\compose.py → raw\skills\diet-b2a-v2\steps\06-compose-15\compose.py
- `video_23()` --calls--> `mosaic()`  [EXTRACTED]
  raw\skills\diet-b2a\scripts\compose.py → raw\skills\diet-b2a-v2\steps\06-compose-15\compose.py
- `main()` --calls--> `video1()`  [EXTRACTED]
  raw\skills\diet-b2a-v2\steps\06-compose-15\compose.py → raw\skills\diet-b2a\scripts\compose.py

## Communities

### Community 0 - "iboss 201건 지식베이스 (최재명)"
Cohesion: 0.13
Nodes (18): 누적 광고비 2,500억 집행 경험, 강남 정육점 재구매율 86% 일매출 8억, 공감 마케팅 7요소, 공감 > 퀄리티 (CPA 10배 차이), 제품>상세>소재>타겟>매체 우선순위, 재구매·CRM > 신규 획득, USP = 욕구 (기능 아님), iboss 201건 인덱스 (2017-2026) (+10 more)

### Community 1 - "AI 아바타/영상 툴"
Cohesion: 0.32
Nodes (12): build_overlays(), compose_v1(), compose_v23(), get_boxes(), main(), mosaic(), Compose 30 final videos from raw Kling + scale + overlay + BGM., Return (before_box, after_box). Accept both legacy (flat dict per set)     and (+4 more)

### Community 2 - "기타: gen_seeds.py"
Cohesion: 0.29
Nodes (9): main(), page_text(), Generate before/after seeds for 5 sets via Gemini + auto logo removal., Attempt a single generation; return path or None., Run primary; if no image (refusal), retry with safe prompt and fewer uploads., run_one(), _try(), was_refused() (+1 more)

### Community 3 - "바이브코딩 & 에이전트 스택"
Cohesion: 0.2
Nodes (10): AI 무중단 스튜디오 일매출 8천만, AI 실행 격차 10~100배 (2026-2027 변곡), 암묵지 추출 = AI 협업 엔진, AI 자동화 시리즈 (2025-2026), AKOOL (AI 모델), Higgsfield (사실적 인물), Midjourney 7, 나노바나나 (Gemini Image Pro) (+2 more)

### Community 4 - "QSCV 문서 추출 코드"
Cohesion: 0.39
Nodes (8): chunk_and_write(), extract(), iter_block_items(), main(), paragraph_text(), QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG], slugify(), table_to_md()

### Community 5 - "기타: kling_client.py"
Cohesion: 0.39
Nodes (8): download(), main(), poll(), Step 02 — Kling image2video: JWT, submit, poll, download, resume., read_keys(), save_state(), submit(), token()

### Community 6 - "기타: lib.py"
Cohesion: 0.33
Nodes (8): ffprobe_duration(), load_config(), out_dir(), Shared helpers: config loading, path resolution, ffmpeg runner., Resolve a path relative to skill root., rel(), run(), skill_root()

### Community 7 - "기타: detect_faces.py"
Cohesion: 0.33
Nodes (8): detect_for_set(), _detect_in_clip(), _extract_frame(), main(), _pick_best_face(), Detect faces in each set's seed images, store per-set mosaic box.  The seed be, Sample multiple frames, pick the largest/median face box., Detect faces SEPARATELY for before and after clips.     CRITICAL: Kling generat

### Community 8 - "기타: gen_kling.py"
Cohesion: 0.39
Nodes (8): download(), main(), poll(), Kling image2video batch for all sets × 4 keys. Resume-safe., read_keys(), save_state(), submit(), token()

### Community 9 - "기타: gemini_client.py"
Cohesion: 0.32
Nodes (6): clean_logo(), generate(), Thin wrapper around gemini-imagegen/gemini_auto.GeminiImageGen. Always applies, In-place replace the image with logo-stripped version., Click the top model-picker and choose '2.5 Pro' / Thinking mode.     Gemini web, select_thinking_model()

### Community 10 - "로고 제거 기술"
Cohesion: 0.43
Nodes (6): batch_process(), make_corner_masks(), process_image(), 하단 좌/우 코너에 타원형 마스크 생성, 양쪽 하단 코너를 인페인팅하여 로고 제거      1. TELEA 알고리즘: 빠른 행진 기반 (텍스처에 강함)     2. NS 알고리즘:, remove_logo()

### Community 11 - "본사 사업/마케팅 (최재명·네이버·GFA)"
Cohesion: 0.43
Nodes (6): build_knowledge_title(), extract_concept(), main(), Rewrite iboss file aliases from article titles to knowledge-based titles.  Why, Extract the knowledge label from a bullet. Prefer pre-colon part., rewrite()

### Community 12 - "기타: inject_aliases_from_h1.py"
Cohesion: 0.6
Nodes (4): extract_h1(), inject(), main(), Inject aliases into frontmatter by extracting the first H1 title.  Why: raw/ f

### Community 13 - "기타: inject_iboss_entities.py"
Cohesion: 0.6
Nodes (4): main(), make_edge(), make_node(), Inject iboss (최재명 i-boss 201건) entities into the knowledge graph.  Why: graphi

### Community 14 - "기타: inject_korean_aliases.py"
Cohesion: 0.6
Nodes (4): inject(), main(), Inject Korean aliases into wiki page frontmatter.  Why: English slugs like `sr, yaml_aliases_block()

### Community 15 - "기타: detect_face.py"
Cohesion: 0.67
Nodes (3): main(), Step 01b (optional) — detect face in after.png and save face_box.json.  Uses O, try_opencv_detect()

### Community 16 - "기타: make_overlays.py"
Cohesion: 0.67
Nodes (3): main(), Step 01 — generate stroked text PNG overlays from config.copy., stroked()

### Community 17 - "기타: qa_check.py"
Cohesion: 0.67
Nodes (3): main(), probe(), Step 04 — quality checks on the 3 output mp4s.

### Community 18 - "기타: analyze_bgm.py"
Cohesion: 0.67
Nodes (3): analyze(), main(), Analyze 3 reference BGM tracks: BPM, drop (onset max energy) second, first-choru

### Community 19 - "기타: gen_scales.py"
Cohesion: 0.67
Nodes (3): main(), Generate per-set scale images with varied kg via Gemini + auto logo removal., run_one()

### Community 20 - "그래프 인덱싱 스크립트"
Cohesion: 0.67
Nodes (3): main(), pick_label(), Re-generate GRAPH_REPORT.md with content-aware community labels.  Why: graphif

### Community 21 - "기타: export.py"
Cohesion: 0.67
Nodes (1): Step 05 — thumbnails + captions + zip.

### Community 22 - "기타: run_all.py"
Cohesion: 0.67
Nodes (1): Orchestrator — run steps 00→05 idempotently.

### Community 23 - "기타: validate_input.py"
Cohesion: 0.67
Nodes (1): Step 00 — validate inputs and config.

### Community 24 - "기타: build_prompts.py"
Cohesion: 0.67
Nodes (1): Generate 20 Kling prompt files (5 sets × 4 keys) from styles.json.

### Community 25 - "기타: check_session.py"
Cohesion: 0.67
Nodes (1): Verify Gemini session is still valid. Non-headless to allow user to see state.

### Community 26 - "기타: inject_diet_b2a_v2_aliases.py"
Cohesion: 0.67
Nodes (1): Inject Korean alias nodes for diet-b2a-v2 into the graphify graph.json.  Ratio

### Community 27 - "기타: build_sets.py"
Cohesion: 1.0
Nodes (1): Build 5 sets config (model + bg + kg + audio) as sets/setN/config.json.

### Community 28 - "기타: Run full graphify pipeline on "
Cohesion: 1.0
Nodes (1): Run full graphify pipeline on the wiki folder. UTF-8 safe.

### Community 29 - "기타: 롤링발칸 (월 500~2500 소재 테스트)"
Cohesion: 1.0
Nodes (1): 롤링발칸 (월 500~2500 소재 테스트)

### Community 30 - "기타: 설득 9요소 (상호성·희소성·권위 등)"
Cohesion: 1.0
Nodes (1): 설득 9요소 (상호성·희소성·권위 등)

## Knowledge Gaps
- **54 isolated node(s):** `QSCV docx → raw/qscv/ 원본 md + chunk/ 200줄 청크 분할 - 표 셀도 텍스트로 추출 - 이미지/도형은 [IMG]`, `Step 01b (optional) — detect face in after.png and save face_box.json.  Uses O`, `Step 05 — thumbnails + captions + zip.`, `Step 02 — Kling image2video: JWT, submit, poll, download, resume.`, `Shared helpers: config loading, path resolution, ffmpeg runner.` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `기타: build_sets.py`** (2 nodes): `Build 5 sets config (model + bg + kg + audio) as sets/setN/config.json.`, `build_sets.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `기타: Run full graphify pipeline on `** (1 nodes): `Run full graphify pipeline on the wiki folder. UTF-8 safe.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `기타: 롤링발칸 (월 500~2500 소재 테스트)`** (1 nodes): `롤링발칸 (월 500~2500 소재 테스트)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `기타: 설득 9요소 (상호성·희소성·권위 등)`** (1 nodes): `설득 9요소 (상호성·희소성·권위 등)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.