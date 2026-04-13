"""Shared helpers: config loading, path resolution, ffmpeg runner."""
from __future__ import annotations
import json
import os
import subprocess as sp
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_config(path: str | Path) -> dict:
    p = Path(path)
    if not p.is_absolute():
        p = skill_root() / p
    return json.loads(p.read_text(encoding="utf-8"))


def rel(cfg_path: str) -> Path:
    """Resolve a path relative to skill root."""
    p = Path(cfg_path)
    if p.is_absolute():
        return p
    return skill_root() / p


def out_dir(cfg: dict) -> Path:
    p = rel(cfg.get("output_dir", "output"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def run(cmd: list[str]):
    print(">", cmd[0], "...")
    sp.run(cmd, check=True)


def ffprobe_duration(p: Path) -> float:
    r = sp.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())
