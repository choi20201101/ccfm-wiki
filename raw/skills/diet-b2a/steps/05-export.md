# Step 05 — 내보내기 / 업로드 준비

## 목적
QA 통과한 3개 영상을 릴스 업로드 규격으로 패키징.

## 실행
```bash
python scripts/export.py --config config/<project>.json
```

## 처리
1. **썸네일**: 각 영상의 `t=1.0` 지점 프레임 추출 → `output/thumbs/영상{1,2,3}.jpg`
2. **캡션 파일**: `HOOK.md § 3` 템플릿에 `copy.*` 치환 → `output/captions/영상{1,2,3}.txt`
3. **릴스 메타**: 제목, 해시태그, 길이 요약 → `output/meta.json`
4. **압축**: `output/release.zip` 에 3개 mp4 + 3개 썸네일 + 3개 캡션 포함

## 업로드 체크리스트 (사람이 수동)
- [ ] 인스타 릴스 음원 라이브러리에서 유사 트렌드 음원 재매칭 (외부 mp3 직접 업로드 시 노출↓)
- [ ] 썸네일 교체 또는 첫 프레임 유지 선택
- [ ] 캡션에서 플랫폼별 해시태그 조정 (인스타 30개, 틱톡 3~5개)
- [ ] 잠금 오디오·저작권 경고 확인

## 출력
- `output/release.zip`
- `output/thumbs/*.jpg`
- `output/captions/*.txt`
