#!/usr/bin/env python3
"""Smoke-test the Foundation 0.1 production path without rendering video."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "editorial-motion" / "skills"


def run(*command: object, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run([str(value) for value in command], cwd=cwd, check=True, text=True, capture_output=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="editorial-motion-foundation-") as temporary:
        project = Path(temporary) / "project"
        scaffold = SKILLS / "motion-project-scaffold" / "scripts" / "create_motion_project.py"
        result = run(
            sys.executable,
            scaffold,
            project,
            "--title", "Foundation smoke test",
            "--slug", "foundation-smoke",
            "--duration", "1",
            "--fps", "12",
        )
        if "Preflight OK: 4 render command(s)" not in result.stdout:
            raise SystemExit("scaffold did not complete its four-format preflight")
        duplicate = subprocess.run(
            [
                sys.executable,
                str(scaffold),
                str(project),
                "--title", "Must not overwrite",
                "--slug", "must-not-overwrite",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if duplicate.returncode == 0 or "Refusing to overwrite" not in duplicate.stderr:
            raise SystemExit("scaffold overwrite guard did not fire")

        required = [
            "production-contract.json",
            "storyboard.json",
            "assets.json",
            "src/index.html",
            "src/vendor/motion.css",
            "scripts/render_project.py",
            "tools/render.py",
            "tools/mix_sfx.py",
        ]
        missing = [relative for relative in required if not (project / relative).is_file()]
        if missing:
            raise SystemExit(f"scaffold missing: {', '.join(missing)}")
        if (project / "package.json").exists():
            raise SystemExit("scaffold unexpectedly contains a package.json")

        beat = {
            "id": "beat-1",
            "start_frame": 0,
            "end_frame": 12,
            "function": "hook",
            "screen_copy": "One clear proposition",
            "before": {},
            "after": {},
            "focal_object": "headline",
            "persistent_objects": [],
            "continuity_action": "hold",
            "motion": {},
            "sound": {},
            "reduced_motion": {"substitute": "direct state"},
            "evidence": "not applicable",
            "interpretation": "not applicable",
            "recommendation": "not applicable",
            "approval": "test fixture",
        }
        storyboard = {
            "schema_version": "1.0",
            "fps": 12,
            "duration_frames": 12,
            "takeaway": "One clear proposition",
            "beats": [beat],
        }
        storyboard_path = project / "storyboard.json"
        storyboard_path.write_text(json.dumps(storyboard, indent=2) + "\n", encoding="utf-8")
        validator = SKILLS / "storyboard-and-beat-sheet" / "scripts" / "validate_storyboard.py"
        run(sys.executable, validator, storyboard_path)

        linter = SKILLS / "analog-surface" / "assets" / "check-artifact.py"
        run(sys.executable, linter, project / "src" / "index.html")

    print("OK: scaffold, four-format preflight, storyboard and starter lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
