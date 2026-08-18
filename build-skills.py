#!/usr/bin/env python3
"""Build standalone, self-contained skill folders from the editorial-motion plugin.

The plugin works as a bundle: a router plus thirteen skills that cite each other by
relative path (`../motion-system/references/sources.md`). Those paths resolve inside the
plugin and dangle anywhere else. Any surface that takes skills one at a time —
Claude Design among them — needs each skill to carry everything it cites.

This vendors the shared reference files into every skill that cites them,
rewrites the paths, then validates that no referenced path is missing. The
plugin stays the single source of truth; dist/ is generated and disposable.

    python3 build-skills.py            # build + validate
    python3 build-skills.py --check    # validate only, no writes
"""
import re, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "plugins" / "editorial-motion" / "skills"
# DIST must stay OUTSIDE the marketplace directory. Build output placed inside
# it puts a second SKILL.md carrying the same `name:` into the tree Claude Code
# scans, and the plugin stops loading — silently, with the CLI still reporting
# it installed and enabled.
# ROOT.parent, not ROOT: the builder now lives inside the marketplace repo, and
# dist output must stay outside the tree Claude Code scans (see comment above).
DIST = ROOT.parent / "editorial-motion-dist"
SKILLS = ["editorial-motion", "layout-composition", "motion-system",
          "design-motion-sound",
          "analog-surface", "editorial-explainer", "imagery-motion",
          "type-treatment", "premium-product-motion", "format-adaptation",
          "motion-project-scaffold", "storyboard-and-beat-sheet",
          "programmatic-motion-renderer", "render-and-delivery-qa"]

# Cross-skill citations → the file to vendor in, keyed by the literal path text.
VENDOR = {
    "../motion-system/references/sources.md":
        (SRC / "motion-system" / "references" / "sources.md", "references/sources.md"),
    "../editorial-explainer/references/house-rules.md":
        (SRC / "editorial-explainer" / "references" / "house-rules.md", "references/house-rules.md"),
}

# Citations of a whole SKILL.md can't be vendored — a 36KB skill inside another
# skill is noise. Replace the path with the rule's own name.
PROSE = {
    "`../editorial-explainer/SKILL.md`": "the editorial-explainer skill",
    "`../imagery-motion/SKILL.md`": "the imagery-motion skill",
    "`../motion-system/assets/motion.css`": "the motion-system skill's `motion.css`",
    "`../analog-surface/assets/check-artifact.py`":
        "the analog-surface skill's `check-artifact.py`",
    "`../programmatic-motion-renderer/assets/render.py`":
        "the programmatic-motion-renderer skill's `render.py`",
}

# A vendored file can have dependencies of its own. house-rules.md names the
# timing tokens but deliberately no longer carries their values — motion.css is
# the single source — so a bundle that gets house-rules.md and not motion.css
# would carry the rule with the numbers missing.
VENDOR_DEPS = {
    "references/house-rules.md":
        [(SRC / "motion-system" / "assets" / "motion.css", "assets/motion.css")],
}

# The scaffold uses sibling skills when installed as a plugin. Its standalone
# zip has no siblings, so the build carries the same runtime under the skill's
# assets/runtime directory. The generated project stays identical either way.
SCAFFOLD_RUNTIME = [
    (SRC / "programmatic-motion-renderer" / "assets" / "render.py",
     "assets/runtime/render.py"),
    (SRC / "motion-system" / "assets" / "motion.css", "assets/runtime/motion.css"),
    (SRC / "motion-system" / "assets" / "sfx.js", "assets/runtime/sfx.js"),
    (SRC / "design-motion-sound" / "scripts" / "mix_sfx.py", "assets/runtime/mix_sfx.py"),
]

VENDOR_NOTE = ("<!-- Vendored copy. Master: plugins/editorial-motion/skills/{origin}\n"
               "     Regenerate with build-skills.py; do not edit here. -->\n\n")

# Same note, for a file where an HTML comment would be a syntax error.
VENDOR_NOTE_CSS = ("/* Vendored copy. Master: plugins/editorial-motion/skills/{origin}\n"
                   "   Regenerate with build-skills.py; do not edit here. */\n\n")


def vendor_file(origin, dest):
    note = VENDOR_NOTE_CSS if dest.suffix == ".css" else VENDOR_NOTE
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(note.format(origin=origin.relative_to(SRC)) +
                    origin.read_text(encoding="utf-8"), encoding="utf-8")


def build_skill(name, check=False):
    src, out = SRC / name, DIST / name
    if not check:
        if out.exists():
            shutil.rmtree(out)
        # ignore Finder droppings and build caches — a .DS_Store shipped inside
        # analog-surface.zip before this filter existed, and __pycache__ shipped
        # three .pyc files into it after the asset scripts were run in place
        shutil.copytree(src, out, ignore=shutil.ignore_patterns(
            ".DS_Store", "__pycache__", "*.pyc", "*.pyo"))

    target = src if check else out
    skill_md = target / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    vendored = []

    for path_text, (origin, local) in VENDOR.items():
        if path_text not in text:
            continue
        vendored.append(local)
        if not check:
            vendor_file(origin, out / local)
            text = text.replace(path_text, local)
        for dep_origin, dep_local in VENDOR_DEPS.get(local, []):
            # The skill may already own the file — motion-system owns motion.css
            # — in which case there is nothing to bring in.
            if (SRC / name / dep_local).exists():
                continue
            vendored.append(dep_local)
            if not check:
                vendor_file(dep_origin, out / dep_local)

    for old, new in PROSE.items():
        if old in text and not check:
            text = text.replace(old, new)

    if name == "motion-project-scaffold":
        for origin, local in SCAFFOLD_RUNTIME:
            vendored.append(local)
            if not check:
                destination = out / local
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(origin, destination)

    if not check:
        skill_md.write_text(text, encoding="utf-8")

    return vendored


def validate(name):
    """Every references/ and assets/ path a skill mentions must exist in it."""
    folder = DIST / name
    problems = []
    for md in folder.rglob("*.md"):
        body = md.read_text(encoding="utf-8")
        if "../" in body:
            for m in re.findall(r"\.\./[\w./-]+", body):
                problems.append(f"{md.relative_to(DIST)}: escaping path {m}")
        for ref in re.findall(r"`((?:references|assets)/[\w.-]+)`", body):
            if not (folder / ref).exists():
                problems.append(f"{md.relative_to(DIST)}: missing {ref}")
    if not (folder / "SKILL.md").exists():
        problems.append(f"{name}: no SKILL.md")
    else:
        head = (folder / "SKILL.md").read_text(encoding="utf-8")
        if not head.startswith("---"):
            problems.append(f"{name}: SKILL.md has no frontmatter")
        elif "name:" not in head.split("---")[1]:
            problems.append(f"{name}: frontmatter has no name")
    return problems


def main():
    check = "--check" in sys.argv
    if not check:
        if DIST.exists():
            shutil.rmtree(DIST)
        DIST.mkdir()

    all_problems, rows = [], []
    for name in SKILLS:
        vendored = build_skill(name, check=check)
        if check:
            continue
        problems = validate(name)
        all_problems += problems
        files = sorted(p for p in (DIST / name).rglob("*") if p.is_file())
        size = sum(p.stat().st_size for p in files)
        zp = DIST / f"{name}.zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(p, str(Path(name) / p.relative_to(DIST / name)))
        rows.append((name, len(files), f"{size/1024:.0f}KB",
                     f"{zp.stat().st_size/1024:.0f}KB",
                     ",".join(v.split("/")[-1] for v in vendored) or "—"))

    if check:
        print("check mode: no writes")
        return 0

    w = max(len(r[0]) for r in rows)
    print(f"{'skill'.ljust(w)}  files  raw     zip     vendored")
    for r in rows:
        print(f"{r[0].ljust(w)}  {str(r[1]).rjust(5)}  {r[2].ljust(6)}  {r[3].ljust(6)}  {r[4]}")

    if all_problems:
        print("\nPROBLEMS:")
        for p in all_problems:
            print("  ✘", p)
        return 1
    print("\nAll referenced paths resolve inside their own skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
