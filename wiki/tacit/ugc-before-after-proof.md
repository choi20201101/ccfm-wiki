# UGC 인증 디자인 — 전후 비교 사진 컷 규칙

**소속 도메인 후보**: `wiki/tacit/coding-lessons.md` (새 §) 또는 `wiki/domains/performance-ad.md` 또는 `wiki/domains/ad-creative.md`
**confidence**: high (사용자 직접 명시 + 8회 iteration 검증)
**source**: 2026-05-03 율이 EP02 광고 빌드 (Administrator PC, `Desktop/bj/output/율이_레이저전_50s_2026-05-03/`)
**triggered by**: 사용자 피드백 v04 검토 — "휴대폰에 글씨 있을 필요 없이 그냥 더 가까이 크게 보여주고 얼룩덜룩한 얼굴 보여지는 게 맞음"

---

## 핵심 규칙

UGC·인플루언서·BJ 라이브 광고에서 **본인 전후 비교 사진을 띄우는 컷**은 다음을 따른다.

| 항목 | ❌ 광고스러운 (피해야 함) | ✅ UGC 인증 톤 (정답) |
|---|---|---|
| 폰 화면 위 텍스트 | "1달 전" / "Before" / "After" 라벨, 광고 카피 | **0건** — 사진만 |
| 폰 크기 | 작게 (한 손에 들어옴) | **카메라에 가까이, 화면을 가득 채울 정도로** |
| 옛날 사진 가시성 | 작아서 디테일 안 보임 | **얼룩덜룩한 톤·푸석함이 명확히 보일 정도로 클로즈업** |
| 구도 | 인물 + 폰 균형 | **폰이 화면의 50%+, 인물 얼굴은 폰 옆 일부** |
| 톤 | "광고합니다" | "야 이거 봐봐 진짜야" 인증 |

## Why

광고스러운 라벨 → 시청자가 즉시 "광고 ≠ 진짜 후기"로 분류. UGC 인증의 신뢰도는 **"광고가 아닌 척" 흉내**에서 나옴. 라이브 BJ가 폰을 카메라에 들이대면서 "이거 봐 한 달 전이야 안 보정"이라고 말하는 게 가장 자연스러운 인증 형식.

## 시드 prompt 템플릿 (gpt-image-2 / nano-banana-pro 공통)

```
The same person from reference, holding a smartphone close to the camera so
that the phone screen FILLS most of the frame. The phone screen shows ONLY
a clear close-up selfie photo of her past dull/blotchy/yellowish skin —
NO text labels, NO Korean text, NO "1달 전" / "Before" / date stamps,
NO graphic overlays, NO ad copy. Just the raw past photo, big enough that
the dull skin texture is clearly visible. Her current bright glowing face
is partially visible beside the phone. UGC livestream proof aesthetic.
```

## 검증 체크리스트

시드 생성 후:
- [ ] 폰 화면에 한국어/영어 텍스트 0건
- [ ] 폰이 프레임 폭의 50% 이상 차지
- [ ] 옛날 사진이 얼룩덜룩 디테일이 보일 만큼 충분히 큼
- [ ] 광고 카피·라벨·날짜 스탬프 0건

## 동일 패턴이 적용되는 다른 인증 형식

- **영수증 인증** (가격·구매처): 영수증을 카메라에 가까이, 텍스트 그대로 보이게. 모자이크 X
- **약국 매장 인증** (사회증거): 매장 간판을 폰으로 찍은 raw 사진
- **사용 흔적 인증** (소진된 통): 다 쓴 통을 카메라에 가까이, 라벨 자연 노출

**공통 원칙**: 카메라 가까이 + raw 노출 + 텍스트/라벨/꾸밈 0.

## 연계 노트

- BJ 영상 = 정면 토킹헤드 강제 — 동일 철학(꾸미지 않은 라이브 인증)
- 자막은 영상 위 ASS 트랙으로만 박고 화면 안 텍스트는 raw 그대로

## ingest 작업

이 파일을 ccfm-wiki에 옮기는 절차 (gguy PC에서 수행):
```bash
cp "Desktop/wiki_pending/ugc-before-after-proof-2026-05-03.md" \
   "ccfm-wiki/wiki/tacit/coding-lessons.md" 의 §UGC-인증-디자인 섹션 append
# 또는 도메인 파일 신규 생성
git -C ccfm-wiki add . && git commit -m "tacit: UGC 전후비교 인증 디자인 규칙"
# graphify post-commit hook이 자동 그래프 리빌드
```
