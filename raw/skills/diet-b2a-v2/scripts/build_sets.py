"""Build 5 sets config (model + bg + kg + audio) as sets/setN/config.json."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DANCE_ROOT = ROOT.parent

styles = json.loads((ROOT / "steps/01-styles-prompts/styles.json").read_text(encoding="utf-8"))

# audio reference (from downloads/audio)
AUDIO_V1 = str(DANCE_ROOT / "downloads" / "audio" / "instagram_DUX2DY0EZxW.mp3")
AUDIO_V2 = str(DANCE_ROOT / "downloads" / "audio" / "instagram_DW3BhZxEQLo.mp3")
AUDIO_V3 = str(DANCE_ROOT / "downloads" / "audio" / "instagram_DWnms5UEf-H.mp3")

pair = styles.get("set_pairing", {})
for i, s in enumerate(styles["sets"], 1):
    set_dir = ROOT / "sets" / s["id"]
    set_dir.mkdir(parents=True, exist_ok=True)
    kg = styles["scale_kg"][i - 1]
    # sets 1-5 use 1:1 pairing; sets 6-10 use set_pairing map
    mi = pair.get(s["id"], {}).get("model_idx", i)
    bi = pair.get(s["id"], {}).get("bg_idx", i)
    config = {
        "id": s["id"],
        "index": i,
        "style_name": s["name"],
        "tiktok_tag": s["tiktok_tag"],
        "model_img": str(DANCE_ROOT / "model" / f"{mi}.png"),
        "bg_img": str(ROOT / "bg_png" / f"bg{bi}.png"),
        "kg_before": kg["before"],
        "kg_after": kg["after"],
        "scale_before_template": str(DANCE_ROOT / "cm" / "01.png"),
        "scale_after_template": str(DANCE_ROOT / "cm" / "02.png"),
        "prompts_dir": str(ROOT / "steps" / "01-styles-prompts" / "prompts" / s["id"]),
        "seed_before": str(ROOT / "seeds" / s["id"] / "before.png"),
        "seed_after": str(ROOT / "seeds" / s["id"] / "after.png"),
        "scale_before_out": str(ROOT / "scales" / s["id"] / "before.png"),
        "scale_after_out": str(ROOT / "scales" / s["id"] / "after.png"),
        "raw_dir": str(ROOT / "raw" / s["id"]),
        "output_dir": str(ROOT / "output" / s["id"]),
        "audio": {"v1": AUDIO_V1, "v2": AUDIO_V2, "v3": AUDIO_V3},
        "layout": {
            "cut_v2": 4.85,
            "cut_v3": 4.0,
            "dance_speed": 1.2,
            "after_len_v2": 5.15,
            "after_len_v3": 5.8,
        },
        "copy": {
            "title": s.get("hook_title", f"165cm / {s['name']}"),
            "label_before": "Before",
            "label_after": "After",
            "date_before": "2025년 12월",
            "date_after": "2026년 3월",
        },
        "copy_tw": {
            "title": s.get("hook_title_tw", s.get("hook_title", s["name"])),
            "label_before": "Before",
            "label_after": "After",
            "date_before": "2025年12月",
            "date_after": "2026年3月",
        },
    }
    (set_dir / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", set_dir / "config.json")
