"""Kling image2video batch for all sets × 4 keys. Resume-safe."""
from __future__ import annotations
import argparse
import base64
import json
import sys
import time
from pathlib import Path

import jwt
import requests


V2_ROOT = Path(__file__).resolve().parents[2]
DANCE_ROOT = V2_ROOT.parent
API_FILE = DANCE_ROOT / "api.txt"
RAW_ROOT = V2_ROOT / "raw"
RAW_ROOT.mkdir(parents=True, exist_ok=True)
STATE = RAW_ROOT / "tasks.json"

ENDPOINTS = [
    "https://api-singapore.klingai.com",
    "https://api.klingai.com",
]

JOBS = [
    # (key, seed, prompt_file, duration)
    ("A_before", "before", "v1_before.txt", "10"),
    ("A_after",  "after",  "v1_after.txt",  "10"),
    ("B_before", "before", "v23_before.txt", "5"),
    ("B_after",  "after",  "v23_after.txt",  "5"),
]


def read_keys():
    ak = sk = None
    for line in API_FILE.read_text(encoding="utf-8").splitlines():
        if "Access Key" in line:
            ak = line.split(":", 1)[1].strip()
        elif "Secret Key" in line:
            sk = line.split(":", 1)[1].strip()
    return ak, sk


def token(ak, sk):
    now = int(time.time())
    return jwt.encode({"iss": ak, "exp": now + 1800, "nbf": now - 5},
                      sk, algorithm="HS256",
                      headers={"alg": "HS256", "typ": "JWT"})


def submit(tok, image_path: Path, prompt: str, duration: str) -> str:
    body = {
        "model_name": "kling-v1-6",
        "image": base64.b64encode(image_path.read_bytes()).decode("ascii"),
        "prompt": prompt,
        "cfg_scale": 0.5,
        "mode": "std",
        "duration": duration,
        "aspect_ratio": "9:16",
    }
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    last = None
    for base in ENDPOINTS:
        try:
            r = requests.post(f"{base}/v1/videos/image2video",
                              headers=headers, json=body, timeout=60)
            data = r.json()
            if data.get("code") == 0:
                return data["data"]["task_id"]
            last = f"{base}: {data}"
        except Exception as e:
            last = f"{base}: {e}"
    raise RuntimeError(f"submit failed: {last}")


def poll(tok, task_id: str, timeout: int = 1500) -> str:
    headers = {"Authorization": f"Bearer {tok}"}
    start = time.time()
    while time.time() - start < timeout:
        for base in ENDPOINTS:
            try:
                r = requests.get(f"{base}/v1/videos/image2video/{task_id}",
                                 headers=headers, timeout=30)
                data = r.json()
            except Exception:
                continue
            if data.get("code") != 0:
                break
            s = data["data"].get("task_status")
            if s == "succeed":
                vs = data["data"].get("task_result", {}).get("videos", [])
                if vs:
                    return vs[0]["url"]
            if s == "failed":
                raise RuntimeError(f"{task_id} failed: {data}")
            break
        time.sleep(15)
    raise TimeoutError(task_id)


def download(url: str, dst: Path):
    r = requests.get(url, stream=True, timeout=300)
    r.raise_for_status()
    with dst.open("wb") as f:
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)


def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="one set id")
    args = ap.parse_args()

    ak, sk = read_keys()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}

    set_dirs = sorted((V2_ROOT / "sets").glob("set*"),
                      key=lambda p: int(p.name.replace("set", "")))
    if args.only:
        set_dirs = [d for d in set_dirs if d.name == args.only]

    # 1) submit everything missing
    for sd in set_dirs:
        sid = sd.name
        cfg = json.loads((sd / "config.json").read_text(encoding="utf-8"))
        prompts_dir = V2_ROOT / "steps" / "01-styles-prompts" / "prompts" / sid
        state.setdefault(sid, {})
        raw_set = RAW_ROOT / sid
        raw_set.mkdir(parents=True, exist_ok=True)
        for key, seed, prompt_file, dur in JOBS:
            info = state[sid].get(key, {})
            out_mp4 = raw_set / f"{key}.mp4"
            if info.get("task_id") and out_mp4.exists() and out_mp4.stat().st_size > 100_000:
                continue
            if info.get("task_id"):
                continue  # already submitted, will be polled below
            seed_path = V2_ROOT / "seeds" / sid / f"{seed}.png"
            prompt = (prompts_dir / prompt_file).read_text(encoding="utf-8").strip()
            tok = token(ak, sk)
            for attempt in range(3):
                try:
                    print(f"submit {sid}/{key} dur={dur}")
                    tid = submit(tok, seed_path, prompt, dur)
                    state[sid][key] = {"task_id": tid, "seed": seed, "dur": dur}
                    save_state(state)
                    print(f"  task_id={tid}")
                    time.sleep(2)
                    break
                except Exception as e:
                    backoff = 30 * (2 ** attempt)
                    print(f"  submit failed ({e}); backoff {backoff}s")
                    time.sleep(backoff)

    # 2) poll + download
    for sd in set_dirs:
        sid = sd.name
        raw_set = RAW_ROOT / sid
        for key, *_ in JOBS:
            info = state[sid].get(key)
            if not info or not info.get("task_id"):
                continue
            out_mp4 = raw_set / f"{key}.mp4"
            if out_mp4.exists() and out_mp4.stat().st_size > 100_000:
                continue
            tok = token(ak, sk)
            print(f"poll {sid}/{key} task={info['task_id']}")
            try:
                url = poll(tok, info["task_id"])
            except Exception as e:
                print(f"  poll error {e}")
                continue
            download(url, out_mp4)
            info["video_url"] = url
            save_state(state)
            print(f"  saved {out_mp4}  {out_mp4.stat().st_size//1024}KB")

    print("ALL KLING DONE")


if __name__ == "__main__":
    main()
