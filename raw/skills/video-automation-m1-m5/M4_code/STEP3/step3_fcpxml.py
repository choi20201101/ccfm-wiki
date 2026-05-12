import json
import shutil
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent, tostring

from utils import load_marker

FPS = 30  # XMEML은 프레임 단위 (정수)


def _audio_duration(path: Path) -> float:
    from pydub import AudioSegment
    audio = AudioSegment.from_file(path, format=path.suffix.lstrip("."))
    return len(audio) / 1000.0


def _frames(seconds: float) -> int:
    return round(seconds * FPS)


import re


def _list_theme_sfx(theme_dir: Path) -> list:
    """테마 폴더 내 SFX 파일을 번호 prefix 순으로 반환

    매칭: "1 .뾰로롱.mp3", "11. 멜로디.mp3", "2. 띠딩2.mp3", "01_공포_xxx.mp3" 등
    숫자로 시작하고 점/언더스코어/공백이 따라오면 OK.
    """
    if not theme_dir.exists():
        return []
    files = []
    for f in theme_dir.iterdir():
        if f.suffix.lower() not in (".wav", ".mp3", ".aiff"):
            continue
        m = re.match(r"^\s*(\d+)[\s._]", f.name)
        if m:
            files.append((int(m.group(1)), f))
    return [f for _, f in sorted(files)]


def _rate_elem(parent):
    rate = SubElement(parent, "rate")
    SubElement(rate, "ntsc").text = "FALSE"
    SubElement(rate, "timebase").text = str(FPS)


def _file_elem(parent, fid: str, path: Path, dur_frames: int, channels: int):
    f = SubElement(parent, "file", id=fid)
    SubElement(f, "name").text = path.name
    SubElement(f, "pathurl").text = path.resolve().as_uri()
    _rate_elem(f)
    SubElement(f, "duration").text = str(dur_frames)
    media = SubElement(f, "media")
    audio = SubElement(media, "audio")
    sc = SubElement(audio, "samplecharacteristics")
    SubElement(sc, "depth").text = "16"
    SubElement(sc, "samplerate").text = "44100"
    SubElement(audio, "channelcount").text = str(channels)


def _clipitem(track, cid: str, name: str, dur_f: int,
              start_f: int, end_f: int, file_ref: str,
              track_index: int, first_ref: bool = False,
              path: Path = None, channels: int = 2):
    ci = SubElement(track, "clipitem", id=cid)
    SubElement(ci, "name").text = name
    SubElement(ci, "duration").text = str(dur_f)
    _rate_elem(ci)
    SubElement(ci, "start").text = str(start_f)
    SubElement(ci, "end").text = str(end_f)
    SubElement(ci, "in").text = "0"
    SubElement(ci, "out").text = str(dur_f)
    if first_ref and path:
        _file_elem(ci, file_ref, path, dur_f, channels)
    else:
        SubElement(ci, "file", id=file_ref)
    st = SubElement(ci, "sourcetrack")
    SubElement(st, "mediatype").text = "audio"
    SubElement(st, "trackindex").text = str(track_index)


def _param_elem(parent, pid: str, name: str, value: str):
    p = SubElement(parent, "parameter")
    SubElement(p, "parameterid").text = pid
    SubElement(p, "name").text = name
    SubElement(p, "value").text = value


def _color_param_elem(parent, pid: str, name: str, r: float, g: float, b: float, a: float = 1.0):
    p = SubElement(parent, "parameter")
    SubElement(p, "parameterid").text = pid
    SubElement(p, "name").text = name
    val = SubElement(p, "value")
    arr = SubElement(val, "array")
    SubElement(arr, "datatype").text = "double"
    for v in (r, g, b, a):
        SubElement(arr, "arrayvalue").text = str(v)


def step3_fcpxml(config):
    tts_cut     = Path(config["tts_cut"])
    marker_json = Path(config["marker_json"])
    xml_path    = Path(config["timeline_xml"])
    sfx_input   = Path(config["sfx_input"])
    sfx_output  = Path(config["sfx_output"])
    sfx_theme   = config.get("sfx_theme", "")
    sub_cfg     = config.get("subtitle", {})

    chunks_path = Path(config["subtitle_chunks"])
    chunks    = json.loads(chunks_path.read_text(encoding="utf-8"))
    marker    = load_marker(marker_json)
    total_dur = _audio_duration(tts_cut)
    total_f   = _frames(total_dur)

    # 테마 폴더 SFX 파일 (번호순)
    theme_files = []
    if sfx_theme:
        theme_in_dir  = sfx_input / sfx_theme
        theme_files   = _list_theme_sfx(theme_in_dir)
        if theme_files:
            # 출력 폴더로 테마 SFX 복사
            theme_out_dir = sfx_output / sfx_theme
            if theme_out_dir.exists():
                shutil.rmtree(theme_out_dir)
            theme_out_dir.mkdir(parents=True, exist_ok=True)
            copied = []
            for f in theme_files:
                dst = theme_out_dir / f.name
                shutil.copy2(f, dst)
                copied.append(dst)
            theme_files = copied

    # SFX 이벤트 수집 (모든 씬 effects, trigger_sec 순)
    raw_events = []
    for scene in marker["scenes"]:
        for effect in scene.get("effects", []):
            raw_events.append({
                "trigger": effect["trigger_sec"],
                "id":      effect["sfx_id"],
            })
    raw_events.sort(key=lambda e: e["trigger"])

    # 흐름 순서대로 테마 파일에 매핑 (이벤트가 더 많으면 초과분은 무시)
    sfx_events = []
    for i, ev in enumerate(raw_events):
        if i >= len(theme_files):
            break
        sfx_events.append({
            "file":    theme_files[i],
            "trigger": ev["trigger"],
            "id":      ev["id"],
        })

    # ── XMEML 빌드 ──────────────────────────────────────
    root = Element("xmeml", version="4")
    seq  = SubElement(root, "sequence", id="sequence-1")
    SubElement(seq, "name").text = tts_cut.stem
    SubElement(seq, "duration").text = str(total_f)
    _rate_elem(seq)

    media = SubElement(seq, "media")

    # 빈 비디오 트랙 (Premiere 시퀀스 생성 필요)
    video = SubElement(media, "video")
    fmt   = SubElement(video, "format")
    sc    = SubElement(SubElement(fmt, "samplecharacteristics"), "width")
    sc.text = "1080"  # 재사용 방지 - 직접 설정
    # 깔끔하게 다시 구성
    media.remove(video)
    video = SubElement(media, "video")
    vfmt  = SubElement(video, "format")
    vsc   = SubElement(vfmt, "samplecharacteristics")
    SubElement(vsc, "width").text = "1080"
    SubElement(vsc, "height").text = "1920"
    SubElement(vsc, "pixelaspectratio").text = "square"
    _rate_elem(vsc)
    vtrack = SubElement(video, "track")

    # V1 — 자막 텍스트 (generatoritem)
    for i, chunk in enumerate(chunks):
        dur_f   = _frames(chunk["end"] - chunk["start"])
        start_f = _frames(chunk["start"])
        gi = SubElement(vtrack, "generatoritem", id=f"generatoritem-{i+1}")
        SubElement(gi, "name").text = chunk["text"]
        SubElement(gi, "duration").text = str(dur_f)
        _rate_elem(gi)
        SubElement(gi, "start").text = str(start_f)
        SubElement(gi, "end").text = str(start_f + dur_f)
        SubElement(gi, "in").text = "0"
        SubElement(gi, "out").text = str(dur_f)
        effect = SubElement(gi, "effect")
        SubElement(effect, "name").text = "Text"
        SubElement(effect, "effectid").text = "Text"
        SubElement(effect, "effectcategory").text = "Text"
        SubElement(effect, "effecttype").text = "generator"
        SubElement(effect, "mediatype").text = "video"
        _param_elem(effect, "str",       "Text",       chunk["text"])
        _param_elem(effect, "fontname",  "Font Name",  "Pretendard-Bold")
        _param_elem(effect, "fontstyle", "Font Style", "Bold")
        _param_elem(effect, "fontsize",  "Font Size",  str(round(sub_cfg.get("size", 55) * 12 / 41)))
        _color_param_elem(effect, "forecolor", "Font Color", 1.0, 1.0, 1.0, 1.0)
        _param_elem(effect, "origin",    "Origin",     "537.9 982")
        _param_elem(effect, "alignment", "Alignment",  "2")

    SubElement(vtrack, "enabled").text = "TRUE"
    SubElement(vtrack, "locked").text = "FALSE"

    # 오디오 섹션
    audio_sec = SubElement(media, "audio")
    SubElement(audio_sec, "numOutputChannels").text = "2"
    afmt = SubElement(audio_sec, "format")
    asc  = SubElement(afmt, "samplecharacteristics")
    SubElement(asc, "depth").text = "16"
    SubElement(asc, "samplerate").text = "44100"

    # A1 — 보이스 트랙 L (track index 1)
    track_l = SubElement(audio_sec, "track")
    _clipitem(track_l, "clipitem-1", tts_cut.stem, total_f,
              0, total_f, "file-1", 1,
              first_ref=True, path=tts_cut, channels=2)
    SubElement(track_l, "enabled").text = "TRUE"
    SubElement(track_l, "locked").text = "FALSE"

    # A2 — 보이스 트랙 R (track index 2, 같은 파일 참조)
    track_r = SubElement(audio_sec, "track")
    _clipitem(track_r, "clipitem-2", tts_cut.stem, total_f,
              0, total_f, "file-1", 2)
    SubElement(track_r, "enabled").text = "TRUE"
    SubElement(track_r, "locked").text = "FALSE"

    # A3 — 효과음 단일 트랙 (시간순 배치, 겹치면 이전 끝에 이어붙임)
    if sfx_events:
        sfx_track = SubElement(audio_sec, "track")
        prev_end = 0
        for i, ev in enumerate(sfx_events):
            sfx_dur = _audio_duration(ev["file"])
            sfx_f   = _frames(sfx_dur)
            trig_f  = max(_frames(ev["trigger"]), prev_end)
            end_f   = trig_f + sfx_f
            fid     = f"file-{3 + i}"
            cid     = f"clipitem-{3 + i}"
            _clipitem(sfx_track, cid, ev["file"].stem, sfx_f,
                      trig_f, end_f, fid, 1,
                      first_ref=True, path=ev["file"], channels=1)
            prev_end = end_f
        SubElement(sfx_track, "enabled").text = "TRUE"
        SubElement(sfx_track, "locked").text = "FALSE"

    # 저장
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    indent(ElementTree(root), space="  ")
    xml_body = tostring(root, encoding="unicode")
    xml_path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n' + xml_body,
        encoding="utf-8",
    )

    print(f"[STEP3] 완료: {xml_path.name}  (A1/A2 보이스, SFX {len(sfx_events)}개)")
