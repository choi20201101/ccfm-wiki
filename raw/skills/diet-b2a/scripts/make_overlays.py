"""Step 01 — generate stroked text PNG overlays from config.copy."""
from __future__ import annotations
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from lib import load_config, out_dir

FONT = "C:/Windows/Fonts/malgunbd.ttf"


def stroked(text: str, size: int, stroke: int, out_path: Path):
    font = ImageFont.truetype(FONT, size)
    dummy = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    w = bbox[2] - bbox[0] + stroke * 2 + 20
    h = bbox[3] - bbox[1] + stroke * 2 + 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(img)
    dd.text(
        (-bbox[0] + stroke + 10, -bbox[1] + stroke + 10),
        text, font=font, fill=(255, 255, 255, 255),
        stroke_width=stroke, stroke_fill=(0, 0, 0, 255),
    )
    img.save(out_path)
    print("wrote", out_path, img.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    od = out_dir(cfg) / "overlays"
    od.mkdir(parents=True, exist_ok=True)
    copy = cfg["copy"]

    stroked(copy["title"],        72, 6, od / "title.png")
    stroked(copy["label_before"], 90, 6, od / "label_before.png")
    stroked(copy["label_after"],  90, 6, od / "label_after.png")
    stroked(copy["date_before"],  48, 4, od / "date_before.png")
    stroked(copy["date_after"],   48, 4, od / "date_after.png")


if __name__ == "__main__":
    main()
