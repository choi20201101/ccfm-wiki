---
source_file: "raw/skills/diet-b2a/ARCHITECTURE.md"
type: "document"
community: "CCFM 미디어본부 고객여정편 chunk002 (영상제작·성과지표·후행액"
tags:
  - graphify/document
  - graphify/EXTRACTED
  - community/CCFM_미디어본부_고객여정편_chunk002_(영상제작·성과지표·후행액
---

# [Hyperedge] diet-b2a pipeline flow (00 validate → 01 overlay/face → 02 Kling → 03 compose → 04 QA → 05 export)

## Connections
- [[Kling AI API (image2video v1-6 std)]] - `calls` [EXTRACTED]
- [[Prompt v1_after_count (영상1 After 1-2-3 카운트)]] - `references` [EXTRACTED]
- [[Prompt v1_before_count (영상1 Before 1-2-3 카운트)]] - `references` [EXTRACTED]
- [[Prompt v23_after_dance (영상2·3 후반 K-pop 축하 춤)]] - `references` [EXTRACTED]
- [[Prompt v23_before_rhythm (영상2·3 전반 팔 다운 리듬)]] - `references` [EXTRACTED]
- [[diet-b2a step-00 input-validate]] - `references` [EXTRACTED]
- [[ffmpeg (filter_complex hstackconcatoverlay)]] - `calls` [EXTRACTED]

#graphify/document #graphify/EXTRACTED #community/CCFM_미디어본부_고객여정편_chunk002_(영상제작·성과지표·후행액