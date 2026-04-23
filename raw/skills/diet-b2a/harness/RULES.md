---
aliases: ["Harness Rules — 멱등성 & 품질 가드레일"]
---

# Harness Rules — 멱등성 & 품질 가드레일

> 이 파일은 스킬이 어떤 모델/에이전트/사용자 손에서 실행되든 **같은 입력 → 같은 출력** 이 되도록 강제하는 규칙. 스크립트는 이 규칙을 어길 수 없게 짜고, 어겼다면 실패한다.

---

## R1. 멱등 (idempotency)
| 단계 | 멱등 조건 |
|---|---|
| step-00 | `validation_ok.flag` 있으면 skip |
| step-01 | 각 `overlays/*.png` 가 존재하고 stat > 0 이면 skip |
| step-02 | `tasks.json` 에 key의 `task_id` 있고 `raw/<key>.mp4` 가 100KB+ 이면 skip |
| step-03 | `output/영상N.mp4` 존재하고 ffprobe duration 8~11s 이면 skip (--force 로 덮어쓰기) |
| step-04 | `qa_report.json` 있고 해시 일치하면 skip |
| step-05 | `release.zip` 있고 안의 mp4 sha 일치하면 skip |

## R2. 경로 & 파일명 규약
- 모든 경로는 스킬 루트 기준 상대 경로
- 파일명에 공백, 한글, 특수문자 금지 (출력 파일명만 한글 허용: `영상1.mp4` 등)
- 중간 산출물은 `output/` 하위에만 쓰기 (절대 스킬 루트나 시스템 경로에 쓰지 않음)

## R3. 인코딩
- 모든 텍스트 파일: UTF-8 (Windows cp949 금지)
- Python `write_text()` 반드시 `encoding="utf-8"` 명시
- 프롬프트에 em-dash(U+2014), 스마트 따옴표 금지 — 로컬 인코딩 크래시 유발

## R4. 얼굴 모자이크 강제
- 합성 파이프라인의 모든 비디오는 `mosaic_clip_filter` 를 **먼저** 통과해야 함
- 바이패스 금지. face_box 미확정 시 step-01에서 abort
- 모자이크 미적용 감지 (step-04 QA의 엣지 에너지 체크) → fail

## R5. 프롬프트 잠금
- `prompts/*.txt` 는 파일 단위로 교체만 허용
- 스크립트에서 동적 f-string 치환 금지 (재현성 저해)
- 새 컨셉은 **별도 파일**을 만들고 config에서 key-file 매핑으로 선택

## R6. Kling API 호출 안전판
- JWT exp ≤ 1800s (30분)
- 폴링 간격 15s 고정, 총 대기 ≤ 25분
- 에러 응답 시 다음 endpoint로 폴백 (list 기반)
- 429/5xx → 지수 백오프 30s → 60s → 120s, 최대 3회

## R7. 레이아웃 하드 한계
- 캔버스: 1080 × 1920 고정
- 체중계 박스는 화면 밖으로 5px 이상 나가면 안 됨 (compose.py에서 어서트)
- 자막은 체중계 박스와 Y축 픽셀 중첩 금지 (QA에서 BBox overlap 체크)
- 영상1 하단 타이틀: 하단 마진 ≥ 60px

## R8. 의상/배경 등 관념 고정
- 스킬은 "의상 다름 → 변신으로 보이게" 효과에 의존. before/after 이미지 의상이 거의 동일하면 프롬프트에 의상 구분 힌트를 주거나, 사용자에게 교체 권장 경고
- QA에서 before/after 평균 색상차가 임계값 이하면 warn

## R9. 저작권 & 음원
- `audio/*.mp3` 는 **레퍼런스 가이드 트랙**일 뿐, 최종 업로드는 플랫폼 공식 라이브러리 음원으로 교체하라는 메시지를 `captions/*.txt` 상단에 자동 삽입
- 외부 URL 직접 첨부 금지

## R10. AI 생성 인물 라벨
- 실존 인물 사진 사용 금지(법적/윤리적). config에 `"ai_generated_person": true` 플래그가 없으면 step-00 에서 warn
- `examples/` 의 샘플은 모두 AI 생성 이미지여야 한다 (README 고지)
