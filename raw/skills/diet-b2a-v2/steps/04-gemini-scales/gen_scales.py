"""Generate per-set scale images with varied kg via Gemini + auto logo removal."""
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


PROMPT = (
    "이 CAS 디지털 체중계 사진에서 LCD 화면 숫자만 '{kg} kg'로 바꿔줘. "
    "나머지(CAS 로고, 사각 화면, 체중 라벨, 테두리, 조명, 각도, 반사)는 모두 원본과 동일하게 유지. "
    "숫자 폰트는 원본의 7-segment LCD 스타일 그대로."
)

PROMPT_SAFE = (
    "CAS 디지털 체중계의 제품 사진 이미지 생성. 정면샷, 회색 LCD 디스플레이에 '{kg} kg' 가 7-segment 숫자로 크게 표시됨. "
    "상단에 CAS 로고, 화면 좌상단에 '체중' 라벨. 깔끔한 흰 체중계, 자연광."
)


def run_one(gen, sid: str, cfg: dict, out_dir: Path, force: bool = False):
    out_dir.mkdir(parents=True, exist_ok=True)
    for tag in ("before", "after"):
        out_path = out_dir / f"{tag}.png"
        if out_path.exists() and out_path.stat().st_size > 30_000 and not force:
            print(f"skip {sid} scale {tag}")
            continue
        kg = cfg[f"kg_{tag}"]
        template = cfg["scale_before_template"] if tag == "before" else cfg["scale_after_template"]
        print(f"== {sid} scale {tag} kg={kg} ==")
        p = generate(
            gen, PROMPT.format(kg=kg), [template],
            output_name=f"{sid}_scale_{tag}_raw",
            new_chat=True, strip_logo=True,
        )
        if not p:
            print("  primary failed; safe fallback...")
            time.sleep(2)
            p = generate(
                gen, PROMPT_SAFE.format(kg=kg), [],
                output_name=f"{sid}_scale_{tag}_safe",
                new_chat=True, strip_logo=True,
            )
        if not p:
            print(f"FAIL {sid} {tag}")
            continue
        shutil.copy(p, out_path)
        print(f"saved {out_path}")
        time.sleep(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="run only this set id")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    sets_root = V2_ROOT / "sets"
    scales_root = V2_ROOT / "scales"
    gen = new_client(output_dir=str(V2_ROOT / "output" / "_gemini_scales_tmp"), headless=False)
    gen.start_browser()
    try:
        gen.goto_gemini()
        for set_dir in sorted(sets_root.glob("set*")):
            sid = set_dir.name
            if args.only and sid != args.only:
                continue
            cfg = json.loads((set_dir / "config.json").read_text(encoding="utf-8"))
            run_one(gen, sid, cfg, scales_root / sid, force=args.force)
    finally:
        gen.close_browser()
    print("ALL SCALES DONE")


if __name__ == "__main__":
    main()
