"""Generate 20 Kling prompt files (5 sets × 4 keys) from styles.json."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
styles = json.loads((ROOT / "styles.json").read_text(encoding="utf-8"))
out_root = ROOT / "prompts"

BODY_BEFORE = (
    "Young Asian woman looking ~85 kg, chubby body, round face, {outfit_before}, "
    "standing in a messy night bedroom (unmade bed, clothes scattered, dim warm lamp light)"
)
BODY_AFTER = (
    "Young Asian slim woman looking ~43 kg, toned abs, slender arms, {outfit_after}, "
    "standing in a tidy sunlit bedroom (neatly made bed, everything organized, bright daylight from window)"
)
TAIL = "full body front view, static fixed camera, vertical 9:16"
NEG = "NO dancing, NO bouncing, NO big arm movements"


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print("wrote", path)


for s in styles["sets"]:
    d = out_root / s["id"]
    ob = styles["outfit_before"]
    oa = styles["outfit_after"]

    # v1_before (A3_fat) 10s synced motion
    write(d / "v1_before.txt",
          f"{BODY_BEFORE.format(outfit_before=ob)}, "
          f"performing this choreography: {s['v1_motion']}. "
          f"Executed gently and a bit self-consciously. {TAIL}.")

    # v1_after (A3_thin) 10s — EXACT SAME motion, synced
    write(d / "v1_after.txt",
          f"{BODY_AFTER.format(outfit_after=oa)}, "
          f"performing the EXACT SAME synchronized choreography as the before version: {s['v1_motion']}. "
          f"Executed with confidence and happy energy. {TAIL}.")

    # v23_before (B4_fat) 5s — rhythm only, arms down
    write(d / "v23_before.txt",
          f"{BODY_BEFORE.format(outfit_before=ob)}, "
          f"{s['v23_before']}. {TAIL}. {NEG}.")

    # v23_after (B4_thin) 5s — full burst into the set's signature dance
    write(d / "v23_after.txt",
          f"{BODY_AFTER.format(outfit_after=oa)}, "
          f"{s['v23_after']}. {TAIL}.")

print("DONE:", out_root)
