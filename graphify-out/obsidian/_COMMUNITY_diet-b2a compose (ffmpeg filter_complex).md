---
type: community
cohesion: 0.17
members: 25
---

# diet-b2a compose (ffmpeg filter_complex)

**Cohesion:** 0.17 - loosely connected
**Members:** 25 nodes

## Members
- [[BGM librosa analyzer (BPMdrop)]] - code - raw/skills/diet-b2a-v2/steps/00-bgm-analyze/analyze_bgm.py
- [[Diet BeforeAfter video pipeline (skill)]] - document - raw/skills/diet-b2a/scripts/run_all.py
- [[Face mosaic anonymization box]] - document - raw/skills/diet-b2a/scripts/detect_face.py
- [[Gemini logo remover (corner inpaint)]] - code - raw/skills/diet-b2a-v2/scripts/logo_remover.py
- [[Gemini scale (kg) image generator]] - code - raw/skills/diet-b2a-v2/steps/04-gemini-scales/gen_scales.py
- [[Gemini seed image generator (beforeafter)]] - code - raw/skills/diet-b2a-v2/steps/03-gemini-seeds/gen_seeds.py
- [[Gemini session validator (Playwright)]] - code - raw/skills/diet-b2a-v2/steps/02-gemini-session/check_session.py
- [[Gemini web UI imagegen via Playwright session]] - document - raw/skills/diet-b2a-v2/scripts/gemini_client.py
- [[Kling 20-clip batch generator]] - code - raw/skills/diet-b2a-v2/steps/05-kling-20clips/gen_kling.py
- [[Kling image2video API (JWT submitpolldownload)]] - document - raw/skills/diet-b2a/scripts/kling_client.py
- [[Kling prompt builder (5 sets x 4 keys)]] - code - raw/skills/diet-b2a-v2/steps/01-styles-prompts/build_prompts.py
- [[diet-b2a Kling image2video client]] - code - raw/skills/diet-b2a/scripts/kling_client.py
- [[diet-b2a QA check (ffprobe)]] - code - raw/skills/diet-b2a/scripts/qa_check.py
- [[diet-b2a compose (ffmpeg filter_complex)]] - code - raw/skills/diet-b2a/scripts/compose.py
- [[diet-b2a export (thumbnails+captions+zip)]] - code - raw/skills/diet-b2a/scripts/export.py
- [[diet-b2a face detection (OpenCV)]] - code - raw/skills/diet-b2a/scripts/detect_face.py
- [[diet-b2a orchestrator (run_all)]] - code - raw/skills/diet-b2a/scripts/run_all.py
- [[diet-b2a shared lib (configpathrun)]] - code - raw/skills/diet-b2a/scripts/lib.py
- [[diet-b2a stroked-text PNG overlays]] - code - raw/skills/diet-b2a/scripts/make_overlays.py
- [[diet-b2a validate_input]] - code - raw/skills/diet-b2a/scripts/validate_input.py
- [[diet-b2a-v2 Gemini wrapper client]] - code - raw/skills/diet-b2a-v2/scripts/gemini_client.py
- [[diet-b2a-v2 build_sets (5 sets config)]] - code - raw/skills/diet-b2a-v2/scripts/build_sets.py
- [[diet-b2a-v2 compose 30 final videos]] - code - raw/skills/diet-b2a-v2/steps/06-compose-15/compose.py
- [[diet-b2a-v2 per-set face detection]] - code - raw/skills/diet-b2a-v2/scripts/detect_faces.py
- [[ffmpeg mosaic+overlay compose pattern]] - document - raw/skills/diet-b2a/scripts/compose.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/diet-b2a_compose_(ffmpeg_filter_complex)
SORT file.name ASC
```
