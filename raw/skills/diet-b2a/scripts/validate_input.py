"""Step 00 — validate inputs and config."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from lib import load_config, rel, out_dir


REQUIRED_COPY = ["title", "label_before", "label_after", "date_before", "date_after"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(args.config)
    errors, warnings = [], []

    for key, path in cfg["input"].items():
        p = rel(path)
        if not p.exists():
            errors.append(f"missing input image: {key}={path}")
        elif p.stat().st_size < 50_000:
            warnings.append(f"image file suspicious size: {p} ({p.stat().st_size} bytes)")

    for k in REQUIRED_COPY:
        v = cfg.get("copy", {}).get(k)
        if not v or not str(v).strip():
            errors.append(f"copy.{k} is required and non-empty")

    fb = cfg.get("face_box", {})
    if not fb.get("auto"):
        for k in ("x", "y", "w", "h"):
            if not isinstance(fb.get(k), int):
                errors.append(f"face_box.{k} must be int (or set face_box.auto=true)")

    keyfile = rel(cfg["kling"]["api_keyfile"])
    if not keyfile.exists():
        errors.append(f"Kling api keyfile missing: {keyfile}")
    else:
        text = keyfile.read_text(encoding="utf-8")
        if "Access Key" not in text or "Secret Key" not in text:
            errors.append("api_keyfile must contain 'Access Key:' and 'Secret Key:' lines")

    for k, p in (cfg.get("audio") or {}).items():
        if p and not rel(p).exists():
            warnings.append(f"audio.{k} missing: {p} (will produce silent video)")

    od = out_dir(cfg)
    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        for w in warnings:
            print(" [warn]", w, file=sys.stderr)
        sys.exit(2)

    (od / "validation_ok.flag").write_text("ok", encoding="utf-8")
    for w in warnings:
        print("[warn]", w)
    print("OK: validation passed ->", od / "validation_ok.flag")


if __name__ == "__main__":
    main()
