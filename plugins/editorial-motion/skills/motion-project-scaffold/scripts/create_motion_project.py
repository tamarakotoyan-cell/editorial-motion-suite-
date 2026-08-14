#!/usr/bin/env python3
"""Create a non-destructive, dependency-free Editorial Motion project."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


FORMATS = {
    "vertical": {"id": "vertical", "width": 1080, "height": 1920},
    "portrait": {"id": "portrait", "width": 1080, "height": 1350},
    "landscape": {"id": "landscape", "width": 1920, "height": 1080},
    "square": {"id": "square", "width": 1080, "height": 1080},
}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--duration", type=float, default=20)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--formats", default="vertical,portrait,landscape,square")
    args = parser.parse_args()

    project_dir = args.project_dir.expanduser().resolve()
    if project_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing path: {project_dir}")
    if args.duration <= 0 or args.fps <= 0 or args.fps > 60:
        raise SystemExit("Duration must be positive and fps must be between 1 and 60")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise SystemExit("Slug must use lowercase letters, numbers and single hyphens")

    format_names = [value.strip() for value in args.formats.split(",") if value.strip()]
    if not format_names:
        raise SystemExit("At least one delivery format is required")
    if len(format_names) != len(set(format_names)):
        raise SystemExit("Delivery formats must not be repeated")
    unknown = sorted(set(format_names) - set(FORMATS))
    if unknown:
        raise SystemExit(f"Unknown formats: {', '.join(unknown)}")

    skill_root = Path(__file__).resolve().parent.parent
    skills_root = skill_root.parent
    template = skill_root / "assets" / "html-starter"
    if not template.is_dir():
        raise SystemExit(f"Starter template missing: {template}")
    shutil.copytree(template, project_dir)
    for directory in ("public/assets", "renders", "qa", "tools", "src/vendor"):
        (project_dir / directory).mkdir(parents=True, exist_ok=True)

    local_runtime = skill_root / "assets" / "runtime"
    plugin_runtime = {
        "render.py": skills_root / "motion-system" / "assets" / "render.py",
        "motion.css": skills_root / "motion-system" / "assets" / "motion.css",
        "sfx.js": skills_root / "motion-system" / "assets" / "sfx.js",
        "mix_sfx.py": skills_root / "design-motion-sound" / "scripts" / "mix_sfx.py",
    }
    destinations = {
        "render.py": project_dir / "tools" / "render.py",
        "motion.css": project_dir / "src" / "vendor" / "motion.css",
        "sfx.js": project_dir / "src" / "vendor" / "sfx.js",
        "mix_sfx.py": project_dir / "tools" / "mix_sfx.py",
    }
    runtime_files = {
        (local_runtime / name if (local_runtime / name).is_file() else plugin_source): destinations[name]
        for name, plugin_source in plugin_runtime.items()
    }
    missing = [str(source) for source in runtime_files if not source.is_file()]
    if missing:
        shutil.rmtree(project_dir)
        raise SystemExit("Plugin runtime is incomplete:\n" + "\n".join(missing))
    for source, destination in runtime_files.items():
        shutil.copy2(source, destination)

    duration_frames = round(args.duration * args.fps)
    if duration_frames < 1:
        shutil.rmtree(project_dir)
        raise SystemExit("Duration and fps produce fewer than one frame")
    contract = {
        "project": {"slug": args.slug, "title": args.title, "purpose": "", "audience": ""},
        "takeaway": "",
        "source_copy": "",
        "claims": [],
        "delivery": {
            "duration_seconds": args.duration,
            "duration_frames": duration_frames,
            "fps": args.fps,
            "formats": [FORMATS[name] for name in format_names],
            "codec": "h264",
            "audio": "optional",
            "captions": "caption-safe",
            "reduced_motion": True,
        },
        "brand": {
            "source": "",
            "logo": "",
            "font": "",
            "fallback_font": "Arial, sans-serif",
            "colours": {"ground": "#F2EFE7", "ink": "#171714", "muted": "#625F58", "accent": "#E2491A"},
            "forbidden": [],
        },
        "review_gates": {"claims": "required", "storyboard": "required", "brand": "required", "final": "required"},
    }
    storyboard = {
        "schema_version": "1.0",
        "fps": args.fps,
        "duration_frames": duration_frames,
        "takeaway": "",
        "beats": [],
    }
    assets = {"schema_version": "1.0", "assets": []}
    write_json(project_dir / "production-contract.json", contract)
    write_json(project_dir / "storyboard.json", storyboard)
    write_json(project_dir / "assets.json", assets)
    preflight = [sys.executable, str(project_dir / "scripts" / "render_project.py"), "--dry-run"]
    subprocess.run(preflight, check=True, cwd=project_dir)
    print(f"Created: {project_dir}")
    print(f"Preflight: {shlex_join(preflight)}")
    return 0


def shlex_join(command: list[str]) -> str:
    """Backport-safe command display without adding a runtime dependency."""
    import shlex

    return shlex.join(command)


if __name__ == "__main__":
    raise SystemExit(main())
