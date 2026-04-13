"""Step 05 — thumbnails + captions + zip."""
from __future__ import annotations
import argparse
import subprocess as sp
import zipfile
from pathlib import Path

from lib import load_config, out_dir

CAPTION_TEMPLATE = """{title}

{date_before} → {date_after}

기간 동안 한 것:
1. (식단 원칙 1줄)
2. (운동 원칙 1줄)
3. (습관 원칙 1줄)

궁금한 거 댓글 👇
#다이어트 #비포애프터 #릴스 #변신 #shorts

※ 릴스 업로드 시 플랫폼 공식 음원 라이브러리에서 유사 트렌드 음원을 재매칭하는 것을 권장합니다.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    od = out_dir(cfg)
    thumbs = od / "thumbs"
    caps = od / "captions"
    thumbs.mkdir(exist_ok=True)
    caps.mkdir(exist_ok=True)

    for name in ("영상1.mp4", "영상2.mp4", "영상3.mp4"):
        p = od / name
        if not p.exists():
            continue
        t = thumbs / (p.stem + ".jpg")
        sp.run(["ffmpeg", "-y", "-loglevel", "error",
                "-ss", "1.0", "-i", str(p),
                "-frames:v", "1", "-q:v", "3", str(t)], check=True)
        c = caps / (p.stem + ".txt")
        c.write_text(CAPTION_TEMPLATE.format(**cfg["copy"]), encoding="utf-8")

    zpath = od / "release.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("영상1.mp4", "영상2.mp4", "영상3.mp4"):
            if (od / name).exists():
                z.write(od / name, name)
        for t in thumbs.glob("*.jpg"):
            z.write(t, f"thumbs/{t.name}")
        for c in caps.glob("*.txt"):
            z.write(c, f"captions/{c.name}")
    print("wrote", zpath)


if __name__ == "__main__":
    main()
