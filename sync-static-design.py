#!/usr/bin/env python3
"""Vendor the static design system's principle files into the static-design plugin.

The master lives outside this repo, in the pilot folder, because it doubles as a
Claude Design design system (brand.md + principles/ + annotated example sets).
The plugin needs the same prose reachable from each skill by relative path, so
this copies it in with a header marking it generated.

Skills cite `references/NN-name.md`. Editing those copies directly is the
failure this script exists to prevent: the next sync silently overwrites it.

    python3 sync-static-design.py            # vendor + validate
    python3 sync-static-design.py --check    # validate only, no writes
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER = ROOT.parent.parent / "Static design content" / "static-design-system"
SKILLS = ROOT / "plugins" / "static-design" / "skills"

# Which master file lands in which skill's references/, and under what name.
# house-rules-static.md is the ban list under its house name, so the router can
# cite it the same way editorial-motion cites house-rules.md.
VENDOR = [
    ("brand.md",                          "static-design",       "brand.md"),
    ("principles/06-anti-patterns.md",    "static-design",       "house-rules-static.md"),
    ("principles/01-layout.md",           "static-composition",  "01-layout.md"),
    ("principles/03-colour-and-ground.md","static-composition",  "03-colour-and-ground.md"),
    ("principles/02-typography.md",       "static-type-graphics","02-typography.md"),
    ("principles/04-graphics-imagery.md", "static-type-graphics","04-graphics-imagery.md"),
    ("principles/05-series.md",           "static-series",       "05-series.md"),
    ("principles/07-focal-point.md",      "static-composition",  "07-focal-point.md"),
    ("principles/08-layered-editorial.md","static-type-graphics","08-layered-editorial.md"),
]

NOTE = ("<!-- Vendored copy. Master: Static design content/static-design-system/{origin}\n"
        "     Regenerate with sync-static-design.py; do not edit here. -->\n\n")

# Master files cross-reference each other and the examples by relative path.
# Inside a skill's references/ those paths dangle, so rewrite them to prose.
REWRITE = {
    "`../examples/bad/":        "`bad example: ",
    "`../examples/good/":       "`good example: ",
    "`../../principles/":       "`principles/",
    "`../principles/":          "`principles/",
    "`check-static.py`":        "`assets/check-static.py`",
    "`session-output/albo-75-tile.html`": "the 19 Aug 2026 proof tile (albo-75-tile.html, pilot folder)",
    "`halftone.py`":            "`assets/halftone.py`",
}


def rewrite(text):
    for old, new in REWRITE.items():
        text = text.replace(old, new)
    return text


def main():
    check_only = "--check" in sys.argv
    problems, written = [], 0

    if not MASTER.is_dir():
        print(f"FAIL  master folder not found: {MASTER}")
        return 1

    for origin, skill, dest_name in VENDOR:
        src = MASTER / origin
        dest = SKILLS / skill / "references" / dest_name

        if not src.is_file():
            problems.append(f"missing master file: {origin}")
            continue
        if not (SKILLS / skill).is_dir():
            problems.append(f"missing skill folder: {skill}")
            continue

        body = NOTE.format(origin=origin) + rewrite(src.read_text())

        if check_only:
            if not dest.is_file():
                problems.append(f"not vendored yet: {skill}/references/{dest_name}")
            elif dest.read_text() != body:
                problems.append(f"stale, master has changed: {skill}/references/{dest_name}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body)
            written += 1

    # Every skill must cite at least one of the files vendored into it, or the
    # vendoring is dead weight nobody reads.
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        refs = skill_dir / "references"
        if not refs.is_dir():
            continue
        skill_text = (skill_dir / "SKILL.md").read_text()
        for ref in sorted(refs.glob("*.md")):
            if f"references/{ref.name}" not in skill_text:
                problems.append(f"uncited: {skill_dir.name}/references/{ref.name}")

    for p in problems:
        print(f"FAIL  {p}")
    if not check_only:
        print(f"vendored {written} file(s) into plugins/static-design/skills/")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
