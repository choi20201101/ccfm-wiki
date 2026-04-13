"""Step 02 — Kling image2video: JWT, submit, poll, download, resume."""
from __future__ import annotations
import argparse
import base64
import json
import time
from pathlib import Path

import jwt
import requests

from lib import load_config, rel, out_dir, skill_root


JOBS = [
    # (key, src_cfg_key, prompt_file, duration_cfg_key)
    ("A3_fat",  "before_image", "v1_before_count.txt",  "duration_v1"),
    ("A3_thin", "after_image",  "v1_after_count.txt",   "duration_v1"),
    ("B4_fat",  "before_image", "v23_before_rhythm.txt","duration_v23"),
    ("B4_thin", "after_image",  "v23_after_dance.txt",  "duration_v23"),
]


def read_keys(path: Path):
    ak = sk = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if "Access Key" in line:
            ak = line.split(":", 1)[1].strip()
        elif "Secret Key" in line:
            sk = line.split(":", 1)[1].strip()
    if not ak or not sk:
        raise RuntimeError("api_keyfile missing keys")
    return ak, sk


def token(ak, sk):
    now = int(time.time())
    return jwt.encode({"iss": ak, "exp": now + 1800, "nbf": now - 5},
                      sk, algorithm="HS256",
                      headers={"alg": "HS256", "typ": "JWT"})


def submit(tok, endpoints, image_path: Path, prompt: str, duration: str,
           model: str, mode: str, aspect: str) -> str:
    body = {
        "model_name": model,
        "image": base64.b64encode(image_path.read_bytes()).decode("ascii"),
        "prompt": prompt,
        "cfg_scale": 0.5,
        "mode": mode,
        "duration": duration,
        "aspect_ratio": aspect,
    }
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    last = None
    for base in endpoints:
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


def poll(tok, endpoints, task_id: str, timeout: int = 1500) -> str:
    headers = {"Authorization": f"Bearer {tok}"}
    start = time.time()
    while time.time() - start < timeout:
        for base in endpoints:
            try:
                r = requests.get(f"{base}/v1/videos/image2video/{task_id}",
                                 headers=headers, timeout=30)
                data = r.json()
            except Exception:
                continue
            if data.get("code") != 0:
                break
            s = data["data"].get("task_status")
            print(f"[poll {task_id}] {s} elapsed={int(time.time()-start)}s")
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
    print("saved", dst, f"{dst.stat().st_size/1024:.0f}KB")


def save_state(state, path: Path):
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)

    od = out_dir(cfg)
    raw = od / "raw"
    raw.mkdir(exist_ok=True)

    ak, sk = read_keys(rel(cfg["kling"]["api_keyfile"]))
    tok = token(ak, sk)
    endpoints = cfg["kling"].get("endpoints") or [
        "https://api-singapore.klingai.com", "https://api.klingai.com"
    ]
    model = cfg["kling"]["model"]
    mode = cfg["kling"]["mode"]
    aspect = cfg["kling"].get("aspect_ratio", "9:16")

    state_file = od / "tasks.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}

    prompts_dir = skill_root() / "prompts"

    for key, src_k, prompt_file, dur_k in JOBS:
        if key in state and state[key].get("task_id"):
            continue
        img = rel(cfg["input"][src_k])
        prompt = (prompts_dir / prompt_file).read_text(encoding="utf-8").strip()
        dur = cfg["kling"][dur_k]
        print(f"== submit {key} ({img.name}) dur={dur} ==")
        tid = submit(tok, endpoints, img, prompt, dur, model, mode, aspect)
        state[key] = {"task_id": tid, "image": str(img), "prompt_file": prompt_file, "duration": dur}
        save_state(state, state_file)
        print("  task_id =", tid)
        time.sleep(2)

    for key, *_ in JOBS:
        dst = raw / f"{key}.mp4"
        if dst.exists() and dst.stat().st_size > 100_000:
            print(f"skip {key}: already have {dst}")
            continue
        tok = token(ak, sk)
        url = poll(tok, endpoints, state[key]["task_id"])
        download(url, dst)
        state[key]["video_url"] = url
        save_state(state, state_file)

    print("ALL DONE")


if __name__ == "__main__":
    main()
