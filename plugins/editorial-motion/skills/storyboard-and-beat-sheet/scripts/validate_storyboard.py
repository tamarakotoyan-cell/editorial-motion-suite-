#!/usr/bin/env python3
"""Validate the timing and required fields of a renderer-neutral storyboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "id",
    "start_frame",
    "end_frame",
    "function",
    "screen_copy",
    "before",
    "after",
    "focal_object",
    "persistent_objects",
    "continuity_action",
    "motion",
    "sound",
    "reduced_motion",
    "evidence",
    "interpretation",
    "recommendation",
    "approval",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--allow-gaps", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.storyboard.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    fps = data.get("fps")
    duration = data.get("duration_frames")
    beats = data.get("beats")
    if not isinstance(fps, int) or fps <= 0:
        errors.append("fps must be a positive integer")
    if not isinstance(duration, int) or duration <= 0:
        errors.append("duration_frames must be a positive integer")
    if not isinstance(beats, list) or not beats:
        errors.append("beats must be a non-empty list")
        beats = []

    cursor = 0
    seen: set[str] = set()
    for index, beat in enumerate(beats):
        label = f"beat[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED - set(beat))
        if missing:
            errors.append(f"{label} missing: {', '.join(missing)}")
        beat_id = beat.get("id")
        if beat_id in seen:
            errors.append(f"duplicate beat id: {beat_id}")
        if isinstance(beat_id, str):
            seen.add(beat_id)
        start = beat.get("start_frame")
        end = beat.get("end_frame")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            errors.append(f"{label} has invalid frame range")
            continue
        if start < cursor:
            errors.append(f"{label} overlaps the preceding beat")
        if start > cursor and not args.allow_gaps:
            errors.append(f"gap before {label}: frames {cursor}-{start - 1}")
        cursor = end
        if not beat.get("screen_copy"):
            errors.append(f"{label} has no screen_copy")
        reduced = beat.get("reduced_motion")
        if not isinstance(reduced, dict) or not reduced.get("substitute"):
            errors.append(f"{label} needs a reduced_motion substitute")

    if beats and cursor != duration:
        errors.append(f"last beat ends at {cursor}, expected {duration}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(beats)} beats, {duration} frames at {fps} fps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
