"""Compose 30 final videos from raw Kling + scale + overlay + BGM."""
from __future__ import annotations
import argparse
import json
import subprocess as sp
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

V2_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = V2_ROOT / "raw"
SCALES_ROOT = V2_ROOT / "scales"
# OUT_ROOT / OV_ROOT assigned per run via main()
OUT_ROOT = V2_ROOT / "output"
OV_ROOT = V2_ROOT / "overlays_cache"

FONT = "C:/Windows/Fonts/malgunbd.ttf"
TARGET_W, TARGET_H = 1080, 1920

DEFAULT_FACE = {"x": 300, "y": 180, "w": 170, "h": 210}

FACE_BOXES = {}
_fb_file = V2_ROOT / "face_boxes.json"
if _fb_file.exists():
    FACE_BOXES = json.loads(_fb_file.read_text(encoding="utf-8"))


def get_boxes(sid: str):
    """Return (before_box, after_box). Accept both legacy (flat dict per set)
    and v2 {"before":{},"after":{}} structures.
    """
    entry = FACE_BOXES.get(sid)
    if entry is None:
        return DEFAULT_FACE, DEFAULT_FACE
    if "before" in entry and "after" in entry:
        return entry["before"], entry["after"]
    # legacy: same box on both
    return entry, entry


def stroked(text: str, size: int, stroke: int, path: Path):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(FONT, size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox = d0.textbbox((0, 0), text, font=font, stroke_width=stroke)
    w = bbox[2] - bbox[0] + stroke * 2 + 20
    h = bbox[3] - bbox[1] + stroke * 2 + 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).text(
        (-bbox[0] + stroke + 10, -bbox[1] + stroke + 10),
        text, font=font, fill=(255, 255, 255, 255),
        stroke_width=stroke, stroke_fill=(0, 0, 0, 255),
    )
    img.save(path)


def mosaic(label_in, label_out, box):
    fx, fy, fw, fh = box["x"], box["y"], box["w"], box["h"]
    return (
        f"[{label_in}]split=2[{label_in}_a][{label_in}_b];"
        f"[{label_in}_a]crop={fw}:{fh}:{fx}:{fy},"
        f"scale=iw/22:ih/22:flags=neighbor,"
        f"scale={fw}:{fh}:flags=neighbor[{label_in}_m];"
        f"[{label_in}_b][{label_in}_m]overlay=x={fx}:y={fy}[{label_out}]"
    )


def run(cmd):
    print(">", cmd[0])
    sp.run(cmd, check=True)


def build_overlays(sid: str, cfg: dict) -> dict[str, Path]:
    d = OV_ROOT / sid
    d.mkdir(parents=True, exist_ok=True)
    c = cfg["copy"]
    paths = {
        "title": d / "title.png",
        "label_before": d / "label_before.png",
        "label_after": d / "label_after.png",
        "date_before": d / "date_before.png",
        "date_after": d / "date_after.png",
    }
    stroked(c["title"], 72, 6, paths["title"])
    stroked(c["label_before"], 90, 6, paths["label_before"])
    stroked(c["label_after"], 90, 6, paths["label_after"])
    stroked(c["date_before"], 48, 4, paths["date_before"])
    stroked(c["date_after"], 48, 4, paths["date_after"])
    return paths


def compose_v1(sid: str, cfg: dict, ov: dict[str, Path], _box=None):
    raw = RAW_ROOT / sid
    left = raw / "A_before.mp4"
    right = raw / "A_after.mp4"
    sc_b = SCALES_ROOT / sid / "before.png"
    sc_a = SCALES_ROOT / sid / "after.png"
    audio = cfg["audio"]["v1"]
    out = OUT_ROOT / sid / "영상1.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    box_before, box_after = get_boxes(sid)
    fc = (
        mosaic("0:v", "lm", box_before) + ";"
        + mosaic("1:v", "rm", box_after) + ";"
        "[lm]scale=-2:1920,crop=540:1920,setsar=1[lv];"
        "[rm]scale=-2:1920,crop=540:1920,setsar=1[rv];"
        "[lv][rv]hstack=inputs=2[base];"
        "[2:v]scale=310:-1[sc1];"
        "[3:v]scale=310:-1[sc2];"
        "[base][sc1]overlay=x=270-overlay_w/2:y=370-overlay_h/2[b1];"
        "[b1][sc2]overlay=x=810-overlay_w/2:y=370-overlay_h/2[b2];"
        "[b2][4:v]overlay=x=(W-overlay_w)/2:y=H-overlay_h-80[b3];"
        "[b3][5:v]overlay=x=270-overlay_w/2:y=165[b4];"
        "[b4][6:v]overlay=x=810-overlay_w/2:y=165[final]"
    )
    cmd = ["ffmpeg", "-y",
           "-i", str(left), "-i", str(right),
           "-i", str(sc_b), "-i", str(sc_a),
           "-i", str(ov["title"]),
           "-i", str(ov["label_before"]),
           "-i", str(ov["label_after"]),
           "-i", audio,
           "-filter_complex", fc,
           "-map", "[final]", "-map", "7:a",
           "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", str(out)]
    run(cmd)
    print("wrote", out)


def compose_v23(sid: str, cfg: dict, ov: dict[str, Path], mode: str, _box=None):
    raw = RAW_ROOT / sid
    fat = raw / "B_before.mp4"
    thin = raw / "B_after.mp4"
    sc_b = SCALES_ROOT / sid / "before.png"
    sc_a = SCALES_ROOT / sid / "after.png"
    lay = cfg["layout"]
    if mode == "v2":
        CUT = lay["cut_v2"]
        AFTER_LEN = lay["after_len_v2"]
        audio = cfg["audio"]["v2"]
        sc_cx, sc_cy, sc_w = 780, 430, 400
        date_x, date_y = 625, 125
        out = OUT_ROOT / sid / "영상2.mp4"
    else:
        CUT = lay["cut_v3"]
        AFTER_LEN = lay["after_len_v3"]
        audio = cfg["audio"]["v3"]
        sc_cx, sc_cy, sc_w = 260, 430, 380
        date_x, date_y = 105, 130
        out = OUT_ROOT / sid / "영상3.mp4"
    SPEED = lay["dance_speed"]

    box_before, box_after = get_boxes(sid)
    fc = (
        mosaic("0:v", "m0", box_before) + ";"
        + mosaic("1:v", "m1", box_after) + ";"
        f"[m0]trim=0:{CUT},setpts=PTS-STARTPTS,"
        f"scale=-2:{TARGET_H},crop={TARGET_W}:{TARGET_H},setsar=1[v0];"
        f"[m1]setpts=(PTS-STARTPTS)/{SPEED},"
        f"scale=-2:{TARGET_H},crop={TARGET_W}:{TARGET_H},setsar=1,split=2[m1a][m1b];"
        "[m1a][m1b]concat=n=2:v=1:a=0[m1loop];"
        f"[m1loop]trim=0:{AFTER_LEN},setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[base];"
        f"[2:v]scale={sc_w}:-1[sc1];"
        f"[3:v]scale={sc_w}:-1[sc2];"
        f"[base][sc1]overlay=x={sc_cx}-overlay_w/2:y={sc_cy}-overlay_h/2:enable='lt(t,{CUT})'[b1];"
        f"[b1][sc2]overlay=x={sc_cx}-overlay_w/2:y={sc_cy}-overlay_h/2:enable='gte(t,{CUT})'[b2];"
        f"[b2][4:v]overlay=x={date_x}:y={date_y}:enable='lt(t,{CUT})'[b3];"
        f"[b3][5:v]overlay=x={date_x}:y={date_y}:enable='gte(t,{CUT})'[final]"
    )
    cmd = ["ffmpeg", "-y",
           "-i", str(fat), "-i", str(thin),
           "-i", str(sc_b), "-i", str(sc_a),
           "-i", str(ov["date_before"]), "-i", str(ov["date_after"]),
           "-i", audio,
           "-filter_complex", fc,
           "-map", "[final]", "-map", "6:a",
           "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", str(out)]
    run(cmd)
    print("wrote", out)


def main():
    global OUT_ROOT, OV_ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--lang", default="ko", choices=["ko", "tw"])
    args = ap.parse_args()

    if args.lang == "tw":
        OUT_ROOT = V2_ROOT / "output_tw"
        OV_ROOT = V2_ROOT / "overlays_cache_tw"
    else:
        OUT_ROOT = V2_ROOT / "output"
        OV_ROOT = V2_ROOT / "overlays_cache"

    set_dirs = sorted((V2_ROOT / "sets").glob("set*"),
                      key=lambda p: int(p.name.replace("set", "")))
    if args.only:
        set_dirs = [d for d in set_dirs if d.name == args.only]
    for sd in set_dirs:
        sid = sd.name
        cfg = json.loads((sd / "config.json").read_text(encoding="utf-8"))
        if args.lang == "tw" and "copy_tw" in cfg:
            cfg["copy"] = cfg["copy_tw"]
        ov = build_overlays(sid, cfg)
        # Only compose if raw clips exist
        missing = [k for k in ("A_before", "A_after", "B_before", "B_after")
                   if not (RAW_ROOT / sid / f"{k}.mp4").exists()]
        if missing:
            print(f"skip {sid}: missing raw {missing}")
            continue
        print(f"=== {sid} ===")
        compose_v1(sid, cfg, ov)
        compose_v23(sid, cfg, ov, "v2")
        compose_v23(sid, cfg, ov, "v3")
    print("ALL COMPOSED")


if __name__ == "__main__":
    main()
