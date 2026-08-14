#!/usr/bin/env python3
"""Render every requested format in an Editorial Motion project."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode


ROOT = Path(__file__).resolve().parent.parent


def load_contract() -> dict:
    path = ROOT / "production-contract.json"
    if not path.is_file():
        raise SystemExit(f"Production contract not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", dest="formats", action="append", help="render only this format; repeat as needed")
    parser.add_argument("--reduced-motion", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-audio", action="store_true")
    args = parser.parse_args()

    contract = load_contract()
    delivery = contract.get("delivery", {})
    available = {item["id"]: item for item in delivery.get("formats", [])}
    selected = args.formats or list(available)
    unknown = sorted(set(selected) - set(available))
    if unknown:
        raise SystemExit(f"Unknown format(s): {', '.join(unknown)}")

    renderer = ROOT / "tools" / "render.py"
    source = ROOT / "src" / "index.html"
    if not renderer.is_file() or not source.is_file():
        raise SystemExit("Project runtime is incomplete; rerun the scaffold preflight")

    duration = delivery.get("duration_seconds")
    fps = delivery.get("fps")
    if not isinstance(duration, (int, float)) or duration <= 0:
        raise SystemExit("delivery.duration_seconds must be positive")
    if not isinstance(fps, int) or fps <= 0:
        raise SystemExit("delivery.fps must be a positive integer")

    slug = contract.get("project", {}).get("slug") or "editorial-motion"
    outputs = []
    for name in selected:
        spec = available[name]
        query = urlencode({"format": name, "motion": "reduced" if args.reduced_motion else "full"})
        target = f"{source.resolve().as_uri()}?{query}"
        suffix = "-reduced" if args.reduced_motion else ""
        output = ROOT / "renders" / f"{slug}-{name}{suffix}.mp4"
        command = [
            sys.executable,
            str(renderer),
            target,
            "--duration", str(duration),
            "--fps", str(fps),
            "--width", str(spec["width"]),
            "--height", str(spec["height"]),
            "--out", str(output),
        ]
        if args.reduced_motion:
            command.append("--no-check")
        if args.no_audio:
            command.append("--no-audio")
        print(shlex.join(command))
        if not args.dry_run:
            output.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(command, check=True, cwd=ROOT)
        outputs.append(output)

    if args.dry_run:
        print(f"Preflight OK: {len(outputs)} render command(s)")
    else:
        print("Rendered:")
        for output in outputs:
            print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
