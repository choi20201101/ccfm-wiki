from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence


def step1_audio_cut(config):
    tts_input = Path(config['tts_input'])
    tts_cut = Path(config['tts_cut'])
    audio_cfg = config['audio']

    fmt = tts_input.suffix.lstrip('.')  # 'wav' or 'mp3'

    audio = AudioSegment.from_file(tts_input, format=fmt)

    chunks = split_on_silence(
        audio,
        min_silence_len=audio_cfg['min_silence_len'],
        silence_thresh=audio_cfg['silence_thresh'],
        keep_silence=audio_cfg['keep_silence'],
    )

    if not chunks:
        raise ValueError(f"무음 구간 감지 실패 — silence_thresh 조정 필요: {tts_input}")

    combined = sum(chunks, AudioSegment.empty())

    tts_cut.parent.mkdir(parents=True, exist_ok=True)
    combined.export(tts_cut, format=fmt)

    print(f"[STEP1] 완료: {tts_cut.name}  ({len(audio)/1000:.1f}s → {len(combined)/1000:.1f}s)")
