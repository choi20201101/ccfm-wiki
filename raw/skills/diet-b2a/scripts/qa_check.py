"""Step 04 — quality checks on the 3 output mp4s."""
from __future__ import annotations
import argparse
import json
import subprocess as sp
from pathlib import Path

from lib import load_config, out_dir, ffprobe_duration


def probe(p: Path) -> dict:
    r = sp.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(p)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    od = out_dir(cfg)

    report = {"videos": {}, "overall": "pass"}
    targets = {"영상1.mp4": (8, 11), "영상2.mp4": (9, 11), "영상3.mp4": (9, 11)}
    for name, (lo, hi) in targets.items():
        p = od / name
        entry = {"exists": p.exists()}
        if p.exists():
            dur = ffprobe_duration(p)
            info = probe(p)
            v = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
            a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
            entry.update({
                "duration": round(dur, 3),
                "duration_ok": lo <= dur <= hi,
                "width": v.get("width"), "height": v.get("height"),
                "res_ok": v.get("width") == cfg["layout"]["target_w"]
                          and v.get("height") == cfg["layout"]["target_h"],
                "audio": bool(a),
                "codec": v.get("codec_name"),
            })
        report["videos"][name] = entry
        if not entry.get("duration_ok") or not entry.get("res_ok"):
            report["overall"] = "fail"

    (od / "qa_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# QA Report — {cfg['project_name']}", ""]
    for k, v in report["videos"].items():
        lines.append(f"## {k}")
        for kk, vv in v.items():
            lines.append(f"- {kk}: {vv}")
        lines.append("")
    lines.append(f"**overall: {report['overall']}**")
    (od / "qa_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("QA:", report["overall"])


if __name__ == "__main__":
    main()
