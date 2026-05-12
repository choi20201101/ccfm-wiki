import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from utils import load_config, build_paths, detect_theme
from STEP1.step1_audio_cut import step1_audio_cut
from STEP2.step2_whisper_sub import step2_whisper_sub
from STEP3.step3_fcpxml import step3_fcpxml

BASE_DIR = Path(__file__).parent

SKIP_FOLDERS = {"done", "sfx"}


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _find_marker(folder: Path):
    """*M4마커*.json 또는 scenes.json 탐색"""
    for f in folder.glob("*.json"):
        if "M4마커" in _nfc(f.name):
            return f
    scenes = folder / "scenes.json"
    if scenes.exists():
        return scenes
    return None


def _find_tts(folder: Path):
    # 1순위: tts 키워드 포함 파일
    for ext in ("wav", "mp3"):
        for f in folder.iterdir():
            if f.suffix.lower() == f".{ext}" and "tts" in f.name.lower():
                return f
    # 2순위: 프로젝트 폴더명과 같은 오디오 파일 (예: 20260427_자보티바_1.mp3)
    for ext in ("wav", "mp3"):
        f = folder / f"{folder.name}.{ext}"
        if f.exists():
            return f
    # 3순위: 폴더 내 첫 번째 오디오 파일
    for ext in ("wav", "mp3"):
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() == f".{ext}":
                return f
    return None


def detect_projects(input_dir: Path):
    """input/YYYYMMDD_브랜드[_N]/ 자동 감지"""
    projects = []
    if not input_dir.exists():
        return projects

    for folder in sorted(input_dir.iterdir()):
        if not folder.is_dir() or folder.name in SKIP_FOLDERS:
            continue
        m = re.match(r"(\d{8})_(.+)$", folder.name)
        if not m:
            continue
        date, brand = m.group(1), m.group(2)

        marker_file = _find_marker(folder)
        if not marker_file:
            continue

        tts_file = _find_tts(folder)
        if not tts_file:
            continue

        projects.append({
            "date":   date,
            "brand":  brand,
            "tts":    tts_file,
            "marker": marker_file,
            "theme":  detect_theme(folder),
            "folder": folder,
        })
    return projects


def main():
    parser = argparse.ArgumentParser(description="M4 자동 편집 파이프라인")
    parser.add_argument("--index", type=int, default=1,
                        help="처리할 프로젝트 번호 (기본: 1)")
    parser.add_argument("--theme", type=str, default=None,
                        help="SFX 테마 강제 지정 (공포/네이티브/정보성). 자동 감지 무시")
    parser.add_argument("--all", action="store_true",
                        help="감지된 모든 프로젝트 순차 처리")
    args = parser.parse_args()

    base_config = load_config(BASE_DIR)
    input_dir   = BASE_DIR / base_config["paths"]["input_folder"].strip("./")

    projects = detect_projects(input_dir)
    if not projects:
        print(f"[M4] {input_dir}/ 에서 처리 가능한 프로젝트를 찾지 못했습니다.")
        print("     YYYYMMDD_브랜드/ 폴더에 마커 JSON + TTS 파일이 모두 있어야 합니다.")
        sys.exit(1)

    print(f"[M4] 감지된 프로젝트: {len(projects)}개")
    for i, p in enumerate(projects, 1):
        theme_str = f"테마={p['theme']}" if p['theme'] else "테마=미감지"
        print(f"  [{i}] {p['date']}_{p['brand']}  ({p['tts'].suffix.lstrip('.').upper()}, {p['marker'].name}, {theme_str})")

    if args.all:
        targets = projects
    else:
        idx = args.index - 1
        if not (0 <= idx < len(projects)):
            print(f"[M4] --index {args.index} 는 범위를 벗어났습니다. (1~{len(projects)})")
            sys.exit(1)
        targets = [projects[idx]]

    for n, proj in enumerate(targets, 1):
        print(f"\n[M4] ▶ 처리 시작 ({n}/{len(targets)}): {proj['date']}_{proj['brand']}")

        paths  = build_paths(BASE_DIR, base_config,
                             proj["date"], proj["brand"],
                             proj["tts"], proj["marker"])
        final_theme = args.theme or proj["theme"] or ""
        if args.theme:
            print(f"[M4] 테마 override: {args.theme}")
        config = {**base_config, **{k: str(v) for k, v in paths.items()},
                  "sfx_theme": final_theme}

        print("[M4] STEP1 — 무음 컷편집")
        step1_audio_cut(config)

        print("[M4] STEP2 — 자막 타이밍 추출")
        step2_whisper_sub(config)

        print("[M4] STEP3 — XMEML 빌드")
        step3_fcpxml(config)

        out_dir = paths["output_dir"]
        print(f"[M4] ✓ 완료 → {out_dir.relative_to(BASE_DIR)}/")
        print(f"       {paths['tts_cut'].name}")
        print(f"       {paths['subtitle_chunks'].name}")
        print(f"       {paths['subtitle_srt'].name}")
        print(f"       {paths['timeline_xml'].name}")

        done_dir = input_dir / "done"
        done_dir.mkdir(exist_ok=True)
        src = proj["folder"]
        dst = done_dir / src.name
        if dst.exists():
            from datetime import datetime
            dst = done_dir / f"{src.name}__{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(src), str(dst))
        print(f"[M4] → input/done/{dst.name}/ 로 이동")


if __name__ == "__main__":
    main()
