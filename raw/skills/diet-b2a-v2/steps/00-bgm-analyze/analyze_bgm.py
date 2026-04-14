"""Analyze 3 reference BGM tracks: BPM, drop (onset max energy) second, first-chorus heuristic."""
import json
from pathlib import Path

import librosa
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "downloads" / "audio"
OUT = Path(__file__).parent / "bgm_report.json"


def analyze(path: Path) -> dict:
    y, sr = librosa.load(str(path), mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)

    # "drop" = peak onset strength time after 1.5s (avoid intro spike)
    mask = times > 1.5
    if mask.any():
        idx_rel = int(np.argmax(onset_env[mask]))
        drop_time = float(times[mask][idx_rel])
    else:
        drop_time = float(times[int(np.argmax(onset_env))])

    # RMS for loudness curve -> secondary drop candidates
    rms = librosa.feature.rms(y=y)[0]
    rms_time = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

    # Top-3 loudness peaks (separated by 1s)
    peaks = []
    sorted_idx = np.argsort(rms)[::-1]
    for i in sorted_idx:
        t = float(rms_time[i])
        if all(abs(t - p) > 1.0 for p in peaks):
            peaks.append(t)
        if len(peaks) >= 3:
            break

    # Chroma similarity peak (chorus)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    sim = np.correlate(chroma.mean(axis=0), chroma.mean(axis=0), mode="full")
    # not super meaningful here; skip

    return {
        "file": str(path),
        "duration": float(librosa.get_duration(y=y, sr=sr)),
        "bpm": float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo),
        "drop_peak_sec": round(drop_time, 2),
        "top3_rms_peaks_sec": sorted([round(p, 2) for p in peaks]),
        "first_beat_sec": round(float(beats[0]), 2) if len(beats) else None,
        "beat_count": int(len(beats)),
    }


def main():
    report = {}
    for mp3 in sorted(AUDIO_DIR.glob("*.mp3")):
        print(f"== {mp3.name} ==")
        r = analyze(mp3)
        for k, v in r.items():
            print(f"  {k}: {v}")
        report[mp3.stem] = r
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
