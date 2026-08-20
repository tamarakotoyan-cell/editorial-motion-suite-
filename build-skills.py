#!/usr/bin/env python3
"""Build standalone, self-contained skill folders from the editorial-motion plugin.

The plugin works as a bundle: a router plus nine skills that cite each other by
relative path (`../motion-system/references/sources.md`). Those paths resolve inside the
plugin and dangle anywhere else. Any surface that takes skills one at a time —
Claude Design among them — needs each skill to carry everything it cites.

This vendors the shared reference files into every skill that cites them,
rewrites the paths, then validates that no referenced path is missing. The
plugin stays the single source of truth; dist/ is generated and disposable.

    python3 build-skills.py            # build + validate
    python3 build-skills.py --check    # build into a temp dir + validate; no repo writes
"""
import re, shutil, sys, tempfile, zipfile
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
          "type-treatment", "premium-product-motion", "format-adaptation"]

# Cross-skill citations → the file to vendor in, keyed by the literal path text.
VENDOR = {
    "../motion-system/references/sources.md":
        (SRC / "motion-system" / "references" / "sources.md", "references/sources.md"),
    "../editorial-explainer/references/house-rules.md":
        (SRC / "editorial-explainer" / "references" / "house-rules.md", "references/house-rules.md"),
    # The shared core. These two sit under editorial-explainer for historical
    # reasons — they are cited from the router and belong to no single skill.
    # Moving them to a real core/ is a build change rather than a content one;
    # logged as deferred in decisions.md.
    "../editorial-explainer/references/accessibility.md":
        (SRC / "editorial-explainer" / "references" / "accessibility.md",
         "references/accessibility.md"),
    "../editorial-explainer/references/decisions.md":
        (SRC / "editorial-explainer" / "references" / "decisions.md",
         "references/decisions.md"),
}

# Citations of a whole SKILL.md can't be vendored — a 36KB skill inside another
# skill is noise. Replace the path with the rule's own name.
PROSE = {
    "`../editorial-explainer/SKILL.md`": "the editorial-explainer skill",
    "`../imagery-motion/SKILL.md`": "the imagery-motion skill",
    "`../motion-system/assets/motion.css`": "the motion-system skill's `motion.css`",
    "`../analog-surface/assets/check-artifact.py`":
        "the analog-surface skill's `check-artifact.py`",
}

# A vendored file can have dependencies of its own. house-rules.md names the
# timing tokens but deliberately no longer carries their values — motion.css is
# the single source — so a bundle that gets house-rules.md and not motion.css
# would carry the rule with the numbers missing.
VENDOR_DEPS = {
    "references/house-rules.md":
        [(SRC / "motion-system" / "assets" / "motion.css", "assets/motion.css")],
}

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


def build_skill(name):
    src, out = SRC / name, DIST / name
    if out.exists():
        shutil.rmtree(out)
    # ignore Finder droppings and build caches — a .DS_Store shipped inside
    # analog-surface.zip before this filter existed, and __pycache__ shipped
    # three .pyc files into it after the asset scripts were run in place
    shutil.copytree(src, out, ignore=shutil.ignore_patterns(
        ".DS_Store", "__pycache__", "*.pyc", "*.pyo"))

    skill_md = out / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    vendored = []

    for path_text, (origin, local) in VENDOR.items():
        if path_text not in text:
            continue
        vendored.append(local)
        vendor_file(origin, out / local)
        text = text.replace(path_text, local)
        for dep_origin, dep_local in VENDOR_DEPS.get(local, []):
            # The skill may already own the file — motion-system owns motion.css
            # — in which case there is nothing to bring in.
            if (SRC / name / dep_local).exists():
                continue
            vendored.append(dep_local)
            vendor_file(dep_origin, out / dep_local)

    for old, new in PROSE.items():
        if old in text:
            text = text.replace(old, new)

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


def restamp_examples():
    """Point every shipped example's version stamp at the current manifest.

    A version bump that does not restamp the examples leaves them failing
    check-artifact.py's `version-stamp` rule at error severity — which is the
    CI step that lints the shipped examples, so the build goes red for a reason
    that has nothing to do with design. That is exactly what had happened: four
    examples stamped 1.9.0 against a 1.11.0 manifest.

    Run this as part of a version bump, before committing.

    Keyed on the stamp name, not on where the file sits: editorial-explainer's
    worked example carries a `static-design` stamp, and it belongs to the static
    plugin's version wherever it lives. Both plugins are handled — the static
    side was restamped by hand through 0.6.1 because this only knew about one.
    """
    import json

    changed = 0
    for plugin in ("editorial-motion", "static-design"):
        manifest = ROOT / "plugins" / plugin / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            print(f"  no manifest for {plugin}, skipped")
            continue
        version = json.loads(manifest.read_text(encoding="utf-8"))["version"]
        stamp = re.compile(rf'(name="{re.escape(plugin)}"\s+content=")(\d+\.\d+\.\d+)(")')

        hits = 0
        for html in sorted((ROOT / "plugins").rglob("*.html")):
            text = html.read_text(encoding="utf-8")
            new, n = stamp.subn(rf"\g<1>{version}\g<3>", text)
            if not n:
                continue
            hits += 1
            if new != text:
                html.write_text(new, encoding="utf-8")
                changed += 1
                print(f"  restamped {html.relative_to(ROOT)} -> {version}")
        print(f"{plugin}: {hits} stamped file(s), now all {version}")

    print(f"{changed} file(s) rewritten" if changed else "all stamps already current")
    return 0


def main():
    # --check used to skip validate() entirely — `if check: continue` sat above
    # the call — so the CI step named "every cited path resolves inside its own
    # skill" ran a build that wrote nothing, validated nothing, and exited 0. It
    # had never caught anything. --check now performs the real build into a
    # throwaway directory and validates that, so the only difference from a full
    # run is where the output lands and that no zips are written.
    global DIST
    check = "--check" in sys.argv
    if "--restamp-examples" in sys.argv:
        return restamp_examples()

    scratch = tempfile.mkdtemp(prefix="skills-check-") if check else None
    if check:
        DIST = Path(scratch)
    else:
        if DIST.exists():
            shutil.rmtree(DIST)
        DIST.mkdir()

    try:
        return _build(check)
    finally:
        if scratch:
            shutil.rmtree(scratch, ignore_errors=True)


def _build(check):
    all_problems, rows = [], []
    for name in SKILLS:
        vendored = build_skill(name)
        problems = validate(name)
        all_problems += problems
        if check:
            continue
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
        if all_problems:
            print("PROBLEMS:")
            for problem in all_problems:
                print("  ✘", problem)
            return 1
        print(f"{len(SKILLS)} skill(s) built into a temp dir and validated; "
              f"no writes to the repo.")
        print("All referenced paths resolve inside their own skill.")
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
