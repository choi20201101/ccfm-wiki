import json
import unicodedata
from pathlib import Path


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def load_config(base_dir: Path) -> dict:
    return json.loads((base_dir / "config.json").read_text(encoding="utf-8"))


SFX_THEMES = ["공포", "네이티브", "정보성"]


def detect_theme(folder: Path):
    """프로젝트 폴더의 *_기획안.md 에서 SFX 테마 자동 감지

    우선순위:
    1) 명시적 테마 라인 (**테마**: 공포, **SFX 테마**: 네이티브 등)
    2) "광고 유형" 섹션 + 다음 2줄
    3) 전체 텍스트 중 최다 출현 테마
    """
    md_files = [f for f in folder.iterdir()
                if f.suffix == ".md" and "기획안" in _nfc(f.name)]
    if not md_files:
        return None
    text  = md_files[0].read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1순위: 명시적 테마 라인
    for line in lines:
        low = line.replace(" ", "").replace("*", "").lower()
        if any(k in low for k in ("테마:", "sfx테마:", "sfx_theme:")):
            for theme in SFX_THEMES:
                if theme in line:
                    return theme

    # 2순위: "광고 유형" 섹션 (해당 라인 + 다음 2줄)
    for i, line in enumerate(lines):
        if "광고 유형" in line:
            block = " ".join(lines[i:i+3])
            for theme in SFX_THEMES:
                if theme in block:
                    return theme

    # 3순위: 전체 텍스트 중 최다 출현 테마
    counts = {t: text.count(t) for t in SFX_THEMES}
    if max(counts.values()) > 0:
        return max(counts, key=counts.get)

    return None


def load_marker(path: Path) -> dict:
    """M4마커.json 또는 scenes.json → 정규화된 {scenes: [...]} 반환

    - 05_브랜드_M3_M4마커.json: {brand, scenes: [{effects: [{sfx_id, trigger_sec}], ...}]}
    - scenes.json: [{sfx: ["SFX_027", "bgm_start"], start_sec, ...}]
    """
    data = json.loads(path.read_text(encoding="utf-8"))

    # scenes.json (배열 직접 형태) → 표준 형태로 정규화
    if isinstance(data, list):
        scenes = []
        for scene in data:
            sfx_list = scene.get("sfx", [])
            effects = [
                {"sfx_id": s, "trigger_sec": scene.get("start_sec", 0.0)}
                for s in sfx_list
                if isinstance(s, str) and s.startswith("SFX_")
            ]
            scenes.append({**scene, "effects": effects})
        return {"scenes": scenes}

    return data


def build_paths(base_dir: Path, config: dict, date: str, brand: str,
                tts_input: Path, marker_file: Path) -> dict:
    """볼륨 구조: input/YYYYMMDD_브랜드/, output/YYYYMMDD_브랜드/"""
    input_root  = base_dir / config["paths"]["input_folder"].strip("./")
    output_root = base_dir / config["paths"]["output_folder"].strip("./")
    proj_name   = f"{date}_{brand}"
    proj_input  = input_root / proj_name
    output_dir  = output_root / proj_name
    tts_ext     = tts_input.suffix.lstrip(".")

    return {
        "input_dir":        proj_input,
        "output_dir":       output_dir,
        "tts_input":        tts_input,
        "tts_cut":          output_dir / f"{proj_name}_tts_cut.{tts_ext}",
        "marker_json":      marker_file,
        "subtitle_chunks":  output_dir / f"{proj_name}_subtitle_chunks.json",
        "subtitle_srt":     output_dir / f"{proj_name}_subtitle_ko.srt",
        "timeline_xml":     output_dir / f"{proj_name}_timeline.xml",
        "sfx_input":        base_dir / config["paths"]["sfx_folder"].strip("./"),
        "sfx_output":       output_dir / "sfx",
    }
