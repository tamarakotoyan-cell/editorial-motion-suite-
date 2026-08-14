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


def run(*command: object, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(value) for value in command],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
        outputs = [temporary_root / "first.mp4", temporary_root / "second.mp4"]
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

        hashes = [sha256(path) for path in outputs]
        if hashes[0] != hashes[1]:
            raise SystemExit(
                "render is not deterministic: "
                f"first {hashes[0]}, second {hashes[1]}"
            )

        metadata = probe(ffprobe, outputs[0])
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
        f"OK: two identical {DURATION}s H.264 renders, {WIDTH}x{HEIGHT} at "
        f"{FPS}fps, sha256 {hashes[0]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
