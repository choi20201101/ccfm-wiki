"""Step 03 — ffmpeg filter_complex compose: mosaic + overlays + audio → 3 mp4s."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from lib import load_config, rel, out_dir, run

FF = "ffmpeg"


def mosaic(label_in, label_out, box):
    return (
        f"[{label_in}]split=2[{label_in}_a][{label_in}_b];"
        f"[{label_in}_a]crop={box['w']}:{box['h']}:{box['x']}:{box['y']},"
        f"scale=iw/22:ih/22:flags=neighbor,"
        f"scale={box['w']}:{box['h']}:flags=neighbor[{label_in}_m];"
        f"[{label_in}_b][{label_in}_m]overlay=x={box['x']}:y={box['y']}[{label_out}]"
    )


def video1(cfg, box, od: Path):
    L = cfg["layout"]["v1"]
    W, H = cfg["layout"]["target_w"], cfg["layout"]["target_h"]
    raw = od / "raw"
    ov = od / "overlays"
    left = raw / "A3_fat.mp4"
    right = raw / "A3_thin.mp4"
    sc_b = rel(cfg["input"]["scale_before_image"])
    sc_a = rel(cfg["input"]["scale_after_image"])
    audio = rel(cfg["audio"]["v1"]) if cfg.get("audio", {}).get("v1") else None
    out = od / "영상1.mp4"

    cx_l = L["scale_center_left"][0]
    cy = L["scale_center_left"][1]
    cx_r = L["scale_center_right"][0]
    sc_w = L["scale_width"]
    ly = L["label_y"]

    # A3 is already 10s, no speed change.
    fc = (
        mosaic("0:v", "lm", box) + ";"
        + mosaic("1:v", "rm", box) + ";"
        f"[lm]scale=-2:{H},crop={W//2}:{H},setsar=1[lv];"
        f"[rm]scale=-2:{H},crop={W//2}:{H},setsar=1[rv];"
        "[lv][rv]hstack=inputs=2[base];"
        f"[2:v]scale={sc_w}:-1[sc1];"
        f"[3:v]scale={sc_w}:-1[sc2];"
        f"[base][sc1]overlay=x={cx_l}-overlay_w/2:y={cy}-overlay_h/2[b1];"
        f"[b1][sc2]overlay=x={cx_r}-overlay_w/2:y={cy}-overlay_h/2[b2];"
        f"[b2][4:v]overlay=x=(W-overlay_w)/2:y=H-overlay_h-{L['title_bottom_pad']}[b3];"
        f"[b3][5:v]overlay=x={cx_l}-overlay_w/2:y={ly}[b4];"
        f"[b4][6:v]overlay=x={cx_r}-overlay_w/2:y={ly}[final]"
    )
    cmd = [FF, "-y",
           "-i", str(left), "-i", str(right),
           "-i", str(sc_b), "-i", str(sc_a),
           "-i", str(ov / "title.png"),
           "-i", str(ov / "label_before.png"),
           "-i", str(ov / "label_after.png")]
    if audio:
        cmd += ["-i", str(audio)]
    cmd += ["-filter_complex", fc, "-map", "[final]"]
    if audio:
        cmd += ["-map", "7:a"]
    cmd += ["-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", str(out)]
    run(cmd)


def video_23(cfg, box, od: Path, mode: str):
    W, H = cfg["layout"]["target_w"], cfg["layout"]["target_h"]
    CUT = cfg["layout"]["cut_seconds"]
    AFTER_LEN = cfg["layout"]["after_len_seconds"]
    SPEED = cfg["layout"]["dance_speed"]

    raw = od / "raw"
    ov = od / "overlays"
    fat = raw / "B4_fat.mp4"
    thin = raw / "B4_thin.mp4"
    sc_b = rel(cfg["input"]["scale_before_image"])
    sc_a = rel(cfg["input"]["scale_after_image"])
    date_b = ov / "date_before.png"
    date_a = ov / "date_after.png"

    if mode == "v2":
        L = cfg["layout"]["v2"]
        audio_k = "v2"
        out = od / "영상2.mp4"
    else:
        L = cfg["layout"]["v3"]
        audio_k = "v3"
        out = od / "영상3.mp4"

    sc_cx, sc_cy = L["scale_center"]
    sc_w = L["scale_width"]
    dx, dy = L["date_xy"]
    audio = rel(cfg["audio"][audio_k]) if cfg.get("audio", {}).get(audio_k) else None

    fc = (
        mosaic("0:v", "m0", box) + ";"
        + mosaic("1:v", "m1", box) + ";"
        f"[m0]trim=0:{CUT},setpts=PTS-STARTPTS,"
        f"scale=-2:{H},crop={W}:{H},setsar=1[v0];"
        f"[m1]setpts=(PTS-STARTPTS)/{SPEED},"
        f"scale=-2:{H},crop={W}:{H},setsar=1,split=2[m1a][m1b];"
        "[m1a][m1b]concat=n=2:v=1:a=0[m1loop];"
        f"[m1loop]trim=0:{AFTER_LEN},setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[base];"
        f"[2:v]scale={sc_w}:-1[sc1];"
        f"[3:v]scale={sc_w}:-1[sc2];"
        f"[base][sc1]overlay=x={sc_cx}-overlay_w/2:y={sc_cy}-overlay_h/2:enable='lt(t,{CUT})'[b1];"
        f"[b1][sc2]overlay=x={sc_cx}-overlay_w/2:y={sc_cy}-overlay_h/2:enable='gte(t,{CUT})'[b2];"
        f"[b2][4:v]overlay=x={dx}:y={dy}:enable='lt(t,{CUT})'[b3];"
        f"[b3][5:v]overlay=x={dx}:y={dy}:enable='gte(t,{CUT})'[final]"
    )
    cmd = [FF, "-y",
           "-i", str(fat), "-i", str(thin),
           "-i", str(sc_b), "-i", str(sc_a),
           "-i", str(date_b), "-i", str(date_a)]
    if audio:
        cmd += ["-i", str(audio)]
    cmd += ["-filter_complex", fc, "-map", "[final]"]
    if audio:
        cmd += ["-map", "6:a"]
    cmd += ["-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", str(out)]
    run(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    od = out_dir(cfg)
    fb_path = od / "face_box.json"
    if fb_path.exists():
        box = json.loads(fb_path.read_text(encoding="utf-8"))
    else:
        fb = cfg["face_box"]
        box = {k: fb[k] for k in ("x", "y", "w", "h")}
    video1(cfg, box, od)
    video_23(cfg, box, od, "v2")
    video_23(cfg, box, od, "v3")


if __name__ == "__main__":
    main()
