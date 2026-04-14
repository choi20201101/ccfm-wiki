"""Generate before/after seeds for 5 sets via Gemini + auto logo removal."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

V2_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2_ROOT / "scripts"))
from gemini_client import new_client, generate  # noqa: E402


PROMPT_BEFORE = (
    "AI 가상 캐릭터 이미지 생성: 1번 사진의 가상 캐릭터 스타일을 참고해서, 2번 사진의 방 안에 "
    "세로 9:16 전신샷으로 넣어줘. 캐릭터는 통통한 몸매(둥근 볼, 살짝 나온 배), "
    "오버사이즈 회색 맨투맨+무릎 위 트레이닝 반바지, 양말. 방은 어지러움(이불 흐트러짐, 바닥에 옷 몇 개, 밤 스탠드 조명). "
    "건전한 일상 사진 스타일. 방 구조 유지."
)

# Softer, non-sexualized prompt for after
PROMPT_AFTER = (
    "AI 가상 캐릭터 이미지 생성: 1번=가상 캐릭터 스타일, 2번=방 레퍼런스. "
    "같은 캐릭터의 다이어트 성공 후 모습 — 건강한 날씬한 체형(마른 편), "
    "단정한 흰 반팔 티셔츠 + 청바지 + 운동화, 미소. "
    "방은 깔끔히 정리됨(침대 정돈, 커튼 열림, 낮의 밝은 자연광). "
    "건전한 라이프스타일 사진 톤. 세로 9:16 전신샷."
)

# Softer fallback if the first prompt is refused
PROMPT_BEFORE_SAFE = (
    "AI 가상 캐릭터 전신 일러스트: 세로 9:16, 아늑한 방 안에 서있는 평범한 여성 가상 캐릭터. "
    "통통한 체형, 편안한 오버사이즈 회색 맨투맨 + 무릎 위 츄리닝 반바지. "
    "방 안은 정리 안된 상태(침구 흐트러짐, 옷 몇 개 바닥). 밤 실내 분위기. 건전한 라이프스타일 일러스트."
)
PROMPT_AFTER_SAFE = (
    "AI 가상 캐릭터 전신 일러스트: 세로 9:16, 아늑한 방 안에 서있는 같은 스타일 캐릭터의 건강한 after 버전. "
    "건강하게 마른 체형, 단정한 흰 티셔츠 + 청바지 + 운동화, 밝은 미소. "
    "방 정리되고 낮의 따뜻한 햇살. 건전한 라이프스타일 일러스트."
)

# Error / refusal patterns on Gemini web UI
REFUSAL_PATTERNS = [
    "can't help with",
    "cannot help with",
    "unable to generate",
    "I'm not able to",
    "not able to create",
    "정책에 위배",
    "생성할 수 없",
    "도와드릴 수 없",
    "민감한",
    "선정적",
    "인물 사진",
    "실제 사람",
    "I can't create",
]


def page_text(gen) -> str:
    try:
        return gen.page.evaluate("() => document.body.innerText || ''")
    except Exception:
        return ""


def was_refused(gen) -> bool:
    txt = page_text(gen).lower()
    return any(p.lower() in txt for p in REFUSAL_PATTERNS)


def _try(gen, prompt, uploads, output_name):
    """Attempt a single generation; return path or None."""
    return generate(
        gen, prompt, uploads, output_name=output_name,
        new_chat=True, strip_logo=True,
    )


def _with_fallback(gen, primary_prompt, safe_prompt, uploads, safe_uploads, output_name):
    """Run primary; if no image (refusal), retry with safe prompt and fewer uploads."""
    p = _try(gen, primary_prompt, uploads, output_name)
    if p:
        return p
    gen.log("primary prompt failed; trying safe fallback...")
    time.sleep(3)
    return _try(gen, safe_prompt, safe_uploads, output_name + "_safe")


def run_one(gen, set_id: str, cfg: dict, out_dir: Path, force: bool = False):
    out_before = out_dir / "before.png"
    out_after = out_dir / "after.png"
    out_dir.mkdir(parents=True, exist_ok=True)

    # before
    if out_before.exists() and out_before.stat().st_size > 100_000 and not force:
        print(f"skip {set_id} before (exists)")
    else:
        print(f"== {set_id} before ==")
        p = _with_fallback(
            gen,
            PROMPT_BEFORE.format(kg=cfg["kg_before"]),
            PROMPT_BEFORE_SAFE,
            [cfg["model_img"], cfg["bg_img"]],
            [cfg["bg_img"]],  # safe: no person photo, only room
            output_name=f"{set_id}_before_raw",
        )
        if not p:
            print(f"FAIL {set_id} before")
            return False
        shutil.copy(p, out_before)
        print(f"saved {out_before}")
        time.sleep(3)

    # after
    if out_after.exists() and out_after.stat().st_size > 100_000 and not force:
        print(f"skip {set_id} after (exists)")
    else:
        print(f"== {set_id} after ==")
        p = _with_fallback(
            gen,
            PROMPT_AFTER.format(kg=cfg["kg_after"]),
            PROMPT_AFTER_SAFE,
            [cfg["model_img"], cfg["bg_img"]],
            [cfg["bg_img"]],
            output_name=f"{set_id}_after_raw",
        )
        if not p:
            print(f"FAIL {set_id} after")
            return False
        shutil.copy(p, out_after)
        print(f"saved {out_after}")
        time.sleep(3)

    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run only this set id (e.g. set1)")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    sets_root = V2_ROOT / "sets"
    seeds_root = V2_ROOT / "seeds"
    gen = new_client(output_dir=str(V2_ROOT / "output" / "_gemini_seeds_tmp"), headless=False)
    gen.start_browser()
    try:
        gen.goto_gemini()
        for set_dir in sorted(sets_root.glob("set*")):
            sid = set_dir.name
            if args.only and sid != args.only:
                continue
            cfg = json.loads((set_dir / "config.json").read_text(encoding="utf-8"))
            run_one(gen, sid, cfg, seeds_root / sid, force=args.force)
    finally:
        gen.close_browser()
    print("DONE")


if __name__ == "__main__":
    main()
