import json
import whisper
from pathlib import Path

from utils import load_marker


def _format_srt_time(seconds: float) -> str:
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _extract_scene_words(marker_json: Path) -> list:
    """씬별 단어 리스트 반환: [ ["뚱보균이","내",...], ["이거","나",...], ... ]"""
    data = load_marker(marker_json)
    return [scene["script"].split() for scene in data["scenes"]]


def _chunk_by_scene(scene_word_timings: list, max_chars: int) -> list:
    """씬 경계에서 무조건 끊고, 씬 내에서 max_chars 기준 추가 청킹"""
    chunks = []
    for scene_words in scene_word_timings:
        current_words, current_start = [], None

        for wt in scene_words:
            candidate = " ".join(w["text"] for w in current_words + [wt])
            if current_words and len(candidate) > max_chars:
                chunks.append({
                    "index": len(chunks),
                    "text":  " ".join(w["text"] for w in current_words),
                    "start": current_start,
                    "end":   current_words[-1]["end"],
                })
                current_words  = [wt]
                current_start  = wt["start"]
            else:
                if not current_words:
                    current_start = wt["start"]
                current_words.append(wt)

        # 씬 끝에서 무조건 flush
        if current_words:
            chunks.append({
                "index": len(chunks),
                "text":  " ".join(w["text"] for w in current_words),
                "start": current_start,
                "end":   current_words[-1]["end"],
            })

    return chunks


def _save_srt(chunks: list, srt_path: Path) -> None:
    lines = []
    for chunk in chunks:
        lines += [
            str(chunk["index"] + 1),
            f"{_format_srt_time(chunk['start'])} --> {_format_srt_time(chunk['end'])}",
            chunk["text"],
            "",
        ]
    srt_path.write_text("\n".join(lines), encoding="utf-8")


def step2_whisper_sub(config):
    tts_cut     = Path(config["tts_cut"])
    marker_json = Path(config["marker_json"])
    chunks_path = Path(config["subtitle_chunks"])
    srt_path    = Path(config["subtitle_srt"])
    whisper_cfg = config["whisper"]
    max_chars   = config["subtitle"]["max_chars"]

    # Whisper 전사
    device = whisper_cfg.get("device", "cpu")
    try:
        model  = whisper.load_model(whisper_cfg["model"], device=device)
        result = model.transcribe(str(tts_cut), language=whisper_cfg["language"], word_timestamps=True)
    except (NotImplementedError, RuntimeError):
        print(f"[STEP2] {device} 미지원 — cpu로 재시도")
        model  = whisper.load_model(whisper_cfg["model"], device="cpu")
        result = model.transcribe(str(tts_cut), language=whisper_cfg["language"], word_timestamps=True)

    whisper_words = [
        {"start": w["start"], "end": w["end"]}
        for seg in result["segments"]
        for w in seg.get("words", [])
    ]

    # 씬별 단어 리스트
    scene_words = _extract_scene_words(marker_json)
    all_m3_words = [w for scene in scene_words for w in scene]

    # Whisper 타임스탬프 + M3 텍스트 매핑 (flat)
    if len(all_m3_words) == len(whisper_words):
        flat_timings = [
            {"text": m3, "start": wh["start"], "end": wh["end"]}
            for m3, wh in zip(all_m3_words, whisper_words)
        ]
    else:
        print(f"[STEP2] 경고: M3 단어 수({len(all_m3_words)}) ≠ Whisper 단어 수({len(whisper_words)}) — 비례 분배 fallback")
        total_chars = sum(len(w) for w in all_m3_words)
        total_time  = whisper_words[-1]["end"] if whisper_words else 0.0
        elapsed, flat_timings = 0.0, []
        for w in all_m3_words:
            duration = total_time * (len(w) / total_chars)
            flat_timings.append({"text": w, "start": elapsed, "end": elapsed + duration})
            elapsed += duration

    # flat_timings → 씬별로 재분배
    scene_word_timings, i = [], 0
    for scene in scene_words:
        scene_word_timings.append(flat_timings[i:i + len(scene)])
        i += len(scene)

    chunks = _chunk_by_scene(scene_word_timings, max_chars)

    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    chunks_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    _save_srt(chunks, srt_path)

    print(f"[STEP2] 완료: {len(chunks)}개 자막 청크 → {chunks_path.name}, {srt_path.name}")
