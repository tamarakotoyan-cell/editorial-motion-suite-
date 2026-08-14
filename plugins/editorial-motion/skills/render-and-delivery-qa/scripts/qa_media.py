#!/usr/bin/env python3
"""Write a deterministic ffprobe and checksum report for a rendered media file."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("media", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.media.is_file():
        raise SystemExit(f"Media not found: {args.media}")
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise SystemExit("ffprobe is required")
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(args.media)],
        check=True,
        capture_output=True,
        text=True,
    )
    probe = json.loads(result.stdout)
    report = {
        "file": str(args.media.resolve()),
        "size_bytes": args.media.stat().st_size,
        "sha256": sha256(args.media),
        "probe": probe,
        "human_review": "awaiting_human_review",
    }
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(args.output.resolve())
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
