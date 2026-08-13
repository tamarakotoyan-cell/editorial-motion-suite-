#!/usr/bin/env python3
"""Mix timecoded sound effects into a video with ffmpeg."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


def ffprobe_has_audio(ffprobe: str, video: Path) -> bool:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(video)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return bool(result.stdout.strip())


def number(value: object, field: str, default: float | None = None) -> float:
    if value is None and default is not None:
        return default
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{field} must be a finite number")
    return float(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("cues", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise SystemExit("ffmpeg and ffprobe are required")
    if not args.video.is_file() or not args.cues.is_file():
        parser.error("video and cue JSON must be files")

    config = json.loads(args.cues.read_text())
    cues = config.get("cues", [])
    if not isinstance(cues, list) or not cues:
        parser.error("cue JSON must contain a non-empty cues array")

    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(args.video)]
    filters: list[str] = []
    mix_inputs: list[str] = []
    has_original = ffprobe_has_audio(ffprobe, args.video)

    if has_original:
        original_gain = number(config.get("original_audio_gain_db"), "original_audio_gain_db", 0.0)
        filters.append(f"[0:a]volume={original_gain}dB[original]")
        mix_inputs.append("[original]")

    cue_root = args.cues.resolve().parent
    for index, cue in enumerate(cues, start=1):
        if not isinstance(cue, dict) or not isinstance(cue.get("file"), str):
            parser.error(f"cue {index} requires a file string")
        source = (cue_root / cue["file"]).resolve()
        if not source.is_file():
            parser.error(f"cue {index} file not found: {source}")
        at = number(cue.get("at"), f"cue {index} at")
        trim_start = number(cue.get("trim_start"), f"cue {index} trim_start", 0.0)
        gain = number(cue.get("gain_db"), f"cue {index} gain_db", 0.0)
        fade_in = number(cue.get("fade_in"), f"cue {index} fade_in", 0.01)
        fade_out = number(cue.get("fade_out"), f"cue {index} fade_out", 0.05)
        duration_value = cue.get("duration")
        duration = number(duration_value, f"cue {index} duration") if duration_value is not None else None
        if min(at, trim_start, fade_in, fade_out) < 0 or (duration is not None and duration <= 0):
            parser.error(f"cue {index} contains a negative time or non-positive duration")

        command.extend(["-i", str(source)])
        trim = f"atrim=start={trim_start}"
        if duration is not None:
            trim += f":duration={duration}"
        chain = [trim, "asetpts=PTS-STARTPTS", f"volume={gain}dB"]
        if fade_in > 0:
            chain.append(f"afade=t=in:st=0:d={fade_in}")
        if fade_out > 0 and duration is not None:
            fade_start = max(duration - fade_out, 0)
            chain.append(f"afade=t=out:st={fade_start}:d={min(fade_out, duration)}")
        delay_ms = round(at * 1000)
        chain.append(f"adelay={delay_ms}|{delay_ms}:all=1")
        label = f"cue{index}"
        filters.append(f"[{index}:a]{','.join(chain)}[{label}]")
        mix_inputs.append(f"[{label}]")

    filters.append(
        f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=longest:dropout_transition=0,"
        "alimiter=limit=0.95,apad[mix]"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "0:v:0",
            "-map",
            "[mix]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(args.output),
        ]
    )
    subprocess.run(command, check=True)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
