#!/usr/bin/env python3
"""Render the shipped starter twice and verify deterministic video output."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "editorial-motion" / "skills"
WIDTH = 320
HEIGHT = 180
FPS = 12
DURATION = 1
MIN_FRAME_PSNR = 45.0


def run(*command: object, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    command_line = [str(value) for value in command]
    result = subprocess.run(
        command_line, cwd=cwd, text=True, capture_output=True
    )
    if result.returncode:
        detail = "\n".join(
            value.strip() for value in (result.stdout, result.stderr) if value.strip()
        )
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(command_line)}"
            + (f"\n{detail}" if detail else "")
        )
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def frame_fingerprints(ffmpeg: str, media: Path) -> list[str]:
    result = run(
        ffmpeg,
        "-v",
        "error",
        "-i",
        media,
        "-map",
        "0:v:0",
        "-f",
        "framemd5",
        "-",
    )
    return [line for line in result.stdout.splitlines() if line and not line.startswith("#")]


def psnr(ffmpeg: str, first: Path, second: Path) -> tuple[float, float]:
    result = run(
        ffmpeg,
        "-i",
        first,
        "-i",
        second,
        "-lavfi",
        "psnr",
        "-f",
        "null",
        "-",
    )
    summary = next(
        (line for line in reversed(result.stderr.splitlines()) if "PSNR" in line),
        "",
    )
    values = {}
    for token in summary.split():
        field, separator, value = token.partition(":")
        if separator and field in {"average", "min"}:
            values[field] = 99.0 if value == "inf" else float(value)
    if set(values) != {"average", "min"}:
        raise SystemExit(f"could not parse ffmpeg PSNR summary: {summary or 'no output'}")
    return values["average"], values["min"]


def probe(ffprobe: str, media: Path) -> dict:
    result = run(
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,nb_frames",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        media,
    )
    return json.loads(result.stdout)


def main() -> int:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise SystemExit("ffmpeg and ffprobe are required for the render regression")

    with tempfile.TemporaryDirectory(prefix="editorial-motion-render-") as temporary:
        temporary_root = Path(temporary)
        project = temporary_root / "project"
        scaffold = SKILLS / "motion-project-scaffold" / "scripts" / "create_motion_project.py"
        run(
            sys.executable,
            scaffold,
            project,
            "--title",
            "Deterministic render regression",
            "--slug",
            "render-regression",
            "--duration",
            str(DURATION),
            "--fps",
            str(FPS),
            "--formats",
            "landscape",
        )

        renderer = project / "tools" / "render.py"
        source = project / "src" / "index.html"
        outputs = [
            temporary_root / "warmup.mp4",
            temporary_root / "first.mp4",
            temporary_root / "second.mp4",
        ]
        for output in outputs:
            run(
                sys.executable,
                renderer,
                source,
                "--duration",
                str(DURATION),
                "--fps",
                str(FPS),
                "--width",
                str(WIDTH),
                "--height",
                str(HEIGHT),
                "--out",
                output,
                "--no-audio",
            )

        comparands = outputs[1:]
        frames = [frame_fingerprints(ffmpeg, path) for path in comparands]
        schedules = [
            [line.rsplit(",", 1)[0].rstrip() for line in render]
            for render in frames
        ]
        if schedules[0] != schedules[1]:
            raise SystemExit(
                "render frame schedules do not match: "
                f"counts {len(schedules[0])} and {len(schedules[1])}"
            )

        if frames[0] == frames[1]:
            average_psnr = minimum_psnr = 99.0
        else:
            average_psnr, minimum_psnr = psnr(ffmpeg, *comparands)
            if minimum_psnr < MIN_FRAME_PSNR:
                raise SystemExit(
                    "rendered frames differ visibly: "
                    f"minimum PSNR {minimum_psnr:.2f}dB, "
                    f"required {MIN_FRAME_PSNR:.2f}dB"
                )

        hashes = [sha256(path) for path in comparands]

        metadata = probe(ffprobe, comparands[0])
        video = next(
            (stream for stream in metadata.get("streams", []) if stream.get("codec_type") == "video"),
            None,
        )
        expected = {
            "codec_name": "h264",
            "width": WIDTH,
            "height": HEIGHT,
            "pix_fmt": "yuv420p",
            "r_frame_rate": f"{FPS}/1",
            "nb_frames": str(FPS * DURATION),
        }
        if video is None:
            raise SystemExit("render has no video stream")
        wrong = {
            field: {"expected": value, "actual": video.get(field)}
            for field, value in expected.items()
            if video.get(field) != value
        }
        duration = float(metadata.get("format", {}).get("duration", 0))
        if abs(duration - DURATION) > 0.001:
            wrong["duration"] = {"expected": DURATION, "actual": duration}
        if wrong:
            raise SystemExit("render metadata mismatch: " + json.dumps(wrong, sort_keys=True))

    print(
        f"OK: two visually deterministic {DURATION}s H.264 renders, "
        f"{WIDTH}x{HEIGHT} at {FPS}fps; PSNR min {minimum_psnr:.2f}dB, "
        f"average {average_psnr:.2f}dB; container sha256 {hashes[0]} and "
        f"{hashes[1]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
