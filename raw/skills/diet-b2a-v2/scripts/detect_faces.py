"""Detect faces in each set's seed images, store per-set mosaic box.

The seed before.png / after.png are at arbitrary resolution; we map the detected box
to the Kling raw frame coordinate system (720x1280) used by compose.mosaic.
"""
from __future__ import annotations
import json
import subprocess as sp
from pathlib import Path

import cv2

V2_ROOT = Path(__file__).resolve().parents[1]
RAW = V2_ROOT / "raw"
OUT = V2_ROOT / "face_boxes.json"

KLING_W, KLING_H = 720, 1280

# Safety margin around detected face (expand box by this ratio)
PAD_W = 0.35
PAD_H = 0.50   # bigger vertically to cover forehead+chin


def _pick_best_face(gray):
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, 1.2, 4)
    if len(faces) == 0:
        return None
    # biggest face
    return max(faces, key=lambda b: b[2] * b[3])


def _extract_frame(mp4: Path) -> Path:
    tmp = mp4.with_suffix(".preview.jpg")
    if not tmp.exists():
        sp.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(mp4), "-vf", "select=eq(n\\,45),format=yuvj420p",
             "-vframes", "1", str(tmp)],
            check=True,
        )
    return tmp


def _detect_in_clip(mp4: Path) -> dict | None:
    """Sample multiple frames, pick the largest/median face box."""
    if not mp4.exists():
        return None
    preview = _extract_frame(mp4)
    img = cv2.imread(str(preview))
    if img is None:
        return None
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = _pick_best_face(gray)
    if face is None:
        return None
    x, y, fw, fh = face
    nx = int(max(0, x - fw * PAD_W))
    ny = int(max(0, y - fh * PAD_H))
    nw = int(min(w - nx, fw * (1 + 2 * PAD_W)))
    nh = int(min(h - ny, fh * (1 + 2 * PAD_H)))
    return {"x": nx, "y": ny, "w": nw, "h": nh}


def detect_for_set(sid: str) -> dict:
    """Detect faces SEPARATELY for before and after clips.
    CRITICAL: Kling generates slightly different face positions between
    before and after, even on the same seed. Using one box causes the
    mosaic to miss one side.
    """
    b = _detect_in_clip(RAW / sid / "A_before.mp4")
    a = _detect_in_clip(RAW / sid / "A_after.mp4")
    out = {}
    if b:
        out["before"] = b
    if a:
        out["after"] = a
    return out


def main():
    boxes = {}
    DEFAULT = {"x": 300, "y": 180, "w": 170, "h": 210}
    for sd in sorted((V2_ROOT / "sets").glob("set*"),
                     key=lambda p: int(p.name.replace("set", ""))):
        sid = sd.name
        det = detect_for_set(sid)
        before = det.get("before") or DEFAULT
        after = det.get("after") or DEFAULT
        boxes[sid] = {"before": before, "after": after}
        print(f"{sid}: before={before} after={after}")
    OUT.write_text(json.dumps(boxes, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
