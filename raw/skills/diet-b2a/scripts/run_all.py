"""Orchestrator — run steps 00→05 idempotently."""
from __future__ import annotations
import argparse
import subprocess as sp
import sys
from pathlib import Path


STEPS = [
    ("00 validate",  "validate_input.py"),
    ("01 overlays",  "make_overlays.py"),
    ("01b face_box", "detect_face.py"),
    ("02 kling",     "kling_client.py"),
    ("03 compose",   "compose.py"),
    ("04 qa",        "qa_check.py"),
    ("05 export",    "export.py"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--from", dest="start", default="00", help="start step (e.g. 03)")
    args = ap.parse_args()

    here = Path(__file__).parent
    for label, script in STEPS:
        step_num = label.split()[0]
        if step_num < args.start:
            print(f"== skip {label} ==")
            continue
        print(f"\n========== {label} ==========")
        r = sp.run([sys.executable, str(here / script), "--config", args.config])
        if r.returncode != 0:
            print(f"FAILED at {label} (exit {r.returncode})")
            sys.exit(r.returncode)
    print("\nALL STEPS DONE")


if __name__ == "__main__":
    main()
