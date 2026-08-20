#!/usr/bin/env python3
"""Vendor the static design system's principle files into the static-design plugin.

The master lives outside this repo, in the pilot folder, because it doubles as a
Claude Design design system (brand.md + principles/ + annotated example sets).
The plugin needs the same prose reachable from each skill by relative path, so
this copies it in with a header marking it generated.

Skills cite `references/NN-name.md`. Editing those copies directly is the
failure this script exists to prevent: the next sync silently overwrites it.

    python3 sync-static-design.py             # vendor + validate
    python3 sync-static-design.py --check     # is the vendoring current? needs the master
    python3 sync-static-design.py --validate  # plugin tree only — no master, CI-safe
"""
import re
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
    "`session-output/albo-75-tile.html`": "the 19 Aug 2026 proof tile (albo-75-tile.html, pilot folder)",
}

# The two scripts live in static-design/assets/. Rewriting every mention to
# `assets/NAME` was skill-blind: inside static-composition and
# static-type-graphics there is no assets/ folder, so the path dangled on any
# surface that installs a skill on its own — the exact failure this vendoring
# exists to prevent. Only the owning skill gets a path; everyone else gets prose.
ASSET_OWNER = "static-design"
ASSET_SCRIPTS = ("check-static.py", "halftone.py")


def rewrite(text, skill):
    for old, new in REWRITE.items():
        text = text.replace(old, new)
    for script in ASSET_SCRIPTS:
        text = text.replace(
            f"`{script}`",
            f"`assets/{script}`" if skill == ASSET_OWNER
            else f"the static-design skill's `{script}`")
    return text


def validate_tree():
    """Every path a static-design skill cites must resolve inside that skill.

    Deliberately needs no master: the master lives outside this repo, in the
    pilot folder, so --check cannot run on a CI checkout. This can, and it
    catches the failure that actually ships — a skill installed on its own,
    citing a file that is not in it.
    """
    problems = []
    cite = re.compile(r"`((?:references|assets)/[\w.-]+)`")

    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{skill_dir.name}: no SKILL.md")
            continue
        head = skill_md.read_text(encoding="utf-8")
        if not head.startswith("---"):
            problems.append(f"{skill_dir.name}: SKILL.md has no frontmatter")
        elif "name:" not in head.split("---")[1]:
            problems.append(f"{skill_dir.name}: frontmatter has no name")

        for md in sorted(skill_dir.rglob("*.md")):
            body = md.read_text(encoding="utf-8")
            rel = md.relative_to(SKILLS)
            for escaping in re.findall(r"\.\./[\w./-]+", body):
                problems.append(f"{rel}: escaping path {escaping}")
            for ref in cite.findall(body):
                if not (skill_dir / ref).exists():
                    problems.append(f"{rel}: missing {ref}")
    return problems


def main():
    if "--validate" in sys.argv:
        problems = validate_tree()
        for problem in problems:
            print(f"FAIL  {problem}")
        if problems:
            print(f"{len(problems)} problem(s)")
            return 1
        n = sum(1 for d in SKILLS.iterdir() if d.is_dir())
        print(f"{n} skill(s) validated; every cited path resolves inside its own skill.")
        return 0

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

        body = NOTE.format(origin=origin) + rewrite(src.read_text(), skill)

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
