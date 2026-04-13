"""Step 01b (optional) — detect face in after.png and save face_box.json.

Uses OpenCV haarcascade. Falls back to config.face_box if unavailable.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from lib import load_config, rel, out_dir


DEFAULT_BOX = dict(x=325, y=405, w=112, h=125)


def try_opencv_detect(img_path: Path) -> dict | None:
    try:
        import cv2  # type: ignore
    except Exception:
        print("[warn] OpenCV not available, skipping auto-detect")
        return None
    img = cv2.imread(str(img_path))
    if img is None:
        return None
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, 1.2, 5)
    if len(faces) == 0:
        return None
    x, y, fw, fh = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)[0]
    sx, sy = 720 / w, 1280 / h
    bx, by = int(x * sx), int(y * sy)
    bw, bh = int(fw * sx * 0.82), int(fh * sy * 0.82)
    return dict(x=bx, y=by, w=bw, h=bh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    fb = cfg.get("face_box", {})
    od = out_dir(cfg)

    box = None
    if fb.get("auto"):
        box = try_opencv_detect(rel(cfg["input"]["after_image"]))
    if box is None:
        box = {k: fb.get(k, DEFAULT_BOX[k]) for k in DEFAULT_BOX}
    (od / "face_box.json").write_text(json.dumps(box, indent=2), encoding="utf-8")
    print("face_box =", box)


if __name__ == "__main__":
    main()
