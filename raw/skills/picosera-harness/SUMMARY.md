---
type: raw
captured_at: 2026-05-14
source_path: C:/Users/gguy/Desktop/gpt/projects/picosera/bestofbest/ + ~/.claude/skills/ad-bdh/
---

# 피코세라 1차 하네스 + ad-bdh 스킬 (요약)

## 무엇
피코세라 광고 소재를 점수로 분류하는 검수 하네스 1차 + 그것을 브랜드 무관
재사용 스킬로 일반화한 `ad-bdh`.

## 피코세라 1차 산출물 (`picosera/bestofbest/`)
- `harness/rubric.md` `score.py` `classify_all.py` `patterns.json` — 검수 엔진
- `harness/state/results.jsonl` — 371장 자동 분류 결과
- `_정리_4점5점/` — 4·5점 266장을 소재별 폴더로 정리 (266 폴더)
  - 각 폴더: `00_소재` + `01_레퍼런스` + `02_레퍼런스이미지` + `03_생성프롬프트`
    + (`01b/02b` 보조레퍼런스 9장) + (`05_모델컷` P시그니처 13장) + `README.md`
  - `INDEX.md` `_패턴요약.md` `다른브랜드_적용가이드.md` `_모델풀/`
  - 레퍼런스 3타입: pinterest / 타사베스트(best_refs_aux) / 자사best_ref
  - 교차감사: Codex + Claude Opus 4.7 → 레퍼런스 오연결 0건 확인

## ad-bdh 스킬 (`~/.claude/skills/ad-bdh/`)
BDH 3단: bob(브랜드 셋업 계획서) → dd(수집·빌드·생성·검수 step 분해) → harness(루브릭 강제 + 서브에이전트 검수).
- `templates/rubric.v1.yaml` — 피코세라 기준을 데이터화한 시드 루브릭 (checklist 25 / rules 17)
- `scripts/classify.py` — 루브릭 YAML 읽어 분류하는 데이터 드리븐 엔진 (코드 불변)
- `scripts/score_vision.py` — 루브릭 기반 비전 호출
- `scripts/organize.py` — 폴더계약(00~05)대로 정리 + INDEX + 패턴요약
- `hooks/on_creative_created.py` — 소재 생성 감지 → 검수 큐 적재

## 핵심 설계: 루브릭 = 교체 가능
검수 기준은 코드가 아닌 `rubric.<버전>.yaml` 파일. 조건이 바뀌면:
- v1 → v2 새 파일 추가 (v1 보존), `active_rubrics`에 등록 → `_소재검수/v2/` 분리 저장
- 다른 관점은 별도 프로파일(`rubric.layout.yaml` 등) — 멀티패스
→ 1차 결과를 덮어쓰지 않고 비교 가능.
