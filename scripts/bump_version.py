#!/usr/bin/env python3
"""Move the Editorial Motion release version through every place that carries it.

The plugin version is written down in three kinds of place: two host manifests,
the changelog's newest heading, and a `<meta name="editorial-motion">` stamp in
every shipped HTML artifact and in the router skill that tells agents to emit
one. CI already fails when the manifests and the changelog disagree, and
`check-artifact.py` already fails an artifact whose stamp does not match the
manifest — so a bump done by hand fails late, one check at a time, after the
first few files are already edited. This does all of them in one pass, and
`--check` reports the drift without touching anything.

Two of the files it scans document the *shape* of a stamp rather than carrying
one: the changelog and the renderer contract both print a literal
`content="X.Y.Z"`. Rewriting those turns instructional text into a version
number, so any captured value that is not a semantic version is left alone —
in both modes.

    python3 scripts/bump_version.py 1.11.0     # rewrite everything
    python3 scripts/bump_version.py --check    # report drift, change nothing
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "editorial-motion"
CLAUDE_MANIFEST = PLUGIN / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
CHANGELOG = PLUGIN / "CHANGELOG.md"

# Matches validate_cross_host.py, so the two agree on what a version looks like
# when they read one.
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?$")
# What may be bumped *to* is narrower. A changelog heading is `## X.Y.Z — DATE`
# and CI reads the version out of it with a plain three-number pattern, so a
# prerelease or build-metadata suffix would leave this script and CI disagreeing
# about the same release.
RELEASE = re.compile(r"^\d+\.\d+\.\d+$")

# Targeted, so the manifests keep their own formatting. Round-tripping them
# through json.dumps would reformat files nobody asked to reformat.
MANIFEST_VERSION = re.compile(r'^(\s*"version"\s*:\s*")([^"]*)(")', re.M)

# The one documented stamp shape. The value is captured separately because it
# is the thing that has to be tested against SEMVER before it is touched.
STAMP = re.compile(r'(<meta\s+name="editorial-motion"\s+content=")([^"]*)(")')

# `## 1.10.0 — 2026-08-14`
HEADING = re.compile(r"^## +(\d+\.\d+\.\d+)\b", re.M)

TODO = "TODO"
STAMPED_SUFFIXES = (".html", ".md")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def base_version(value: str) -> str | None:
    """The shared release version, with any local build metadata dropped.

    Codex installs may append a cachebuster after `+`; the release contract
    says that does not change the shared version, so neither does this.
    """
    if not SEMVER.fullmatch(value):
        return None
    return value.split("+", 1)[0]


def manifest_version(path: Path) -> str | None:
    match = MANIFEST_VERSION.search(path.read_text(encoding="utf-8"))
    return base_version(match.group(2)) if match else None


def stamped_files() -> list[Path]:
    return sorted(
        path for path in PLUGIN.rglob("*")
        if path.is_file() and path.suffix in STAMPED_SUFFIXES
        and STAMP.search(path.read_text(encoding="utf-8"))
    )


def newest_entry(text: str) -> tuple[str | None, str]:
    """The newest changelog heading's version, and that entry's whole body."""
    headings = list(re.finditer(r"^## +.*$", text, re.M))
    if not headings:
        return None, ""
    start = headings[0].start()
    end = headings[1].start() if len(headings) > 1 else len(text)
    body = text[start:end]
    version = HEADING.search(body)
    return (version.group(1) if version else None), body


def stamps_in(path: Path) -> list[str]:
    return [match.group(2) for match in STAMP.finditer(path.read_text(encoding="utf-8"))]


def check() -> int:
    problems: list[str] = []
    # A TODO left in the newest entry is a real failure, but rerunning the bump
    # will not clear it — only writing the entry will. Track the two apart so
    # the fix line is only offered when it is actually the fix.
    drifted = False

    claude = manifest_version(CLAUDE_MANIFEST)
    if not claude:
        fail(f"{CLAUDE_MANIFEST.relative_to(ROOT)}: no valid semantic version")
        return 1

    # The Claude manifest is the reference: it is the file check-artifact.py
    # walks up to find when it verifies an artifact's stamp.
    codex = manifest_version(CODEX_MANIFEST)
    if codex != claude:
        problems.append(
            f"{CODEX_MANIFEST.relative_to(ROOT)}: {codex or 'no valid version'}, expected {claude}")
        drifted = True

    changelog = CHANGELOG.read_text(encoding="utf-8")
    newest, body = newest_entry(changelog)
    if newest != claude:
        problems.append(
            f"{CHANGELOG.relative_to(ROOT)}: newest entry is "
            f"{newest or 'missing'}, expected {claude}")
        drifted = True
    elif TODO in body:
        problems.append(
            f"{CHANGELOG.relative_to(ROOT)}: the {newest} entry still contains "
            f"{TODO} — write it before shipping")

    stamps = {path: stamps_in(path) for path in stamped_files()}
    for path, values in stamps.items():
        # A non-semver value is documentation showing the shape of a stamp, not
        # a stamp. It never drifts, so it never disagrees.
        stale = sorted({value for value in values
                        if SEMVER.fullmatch(value) and value != claude})
        if stale:
            problems.append(
                f"{path.relative_to(ROOT)}: stamped {', '.join(stale)}, expected {claude}")
            drifted = True

    if problems:
        for problem in problems:
            fail(problem)
        if drifted:
            print(f"fix: python3 scripts/bump_version.py {claude}", file=sys.stderr)
        return 1

    values = [value for group in stamps.values() for value in group]
    real = sum(1 for value in values if SEMVER.fullmatch(value))
    literal = len(values) - real
    print(f"OK: manifests, changelog and {real} artifact stamps at {claude}"
          + (f"; {literal} documentation placeholders left alone" if literal else ""))
    return 0


def bump(version: str) -> int:
    today = datetime.date.today().isoformat()
    changed: list[str] = []
    wrote_skeleton = False

    for path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
        text = path.read_text(encoding="utf-8")
        updated, count = MANIFEST_VERSION.subn(rf'\g<1>{version}\g<3>', text, count=1)
        if not count:
            fail(f"{path.relative_to(ROOT)}: no version field to rewrite")
            return 1
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    changelog = CHANGELOG.read_text(encoding="utf-8")
    if not re.search(rf"^## +{re.escape(version)}\b", changelog, re.M):
        skeleton = (f"## {version} — {today}\n\n"
                    f"{TODO}: one line on what this release is for.\n\n"
                    f"**Changed**\n\n"
                    f"- {TODO}\n\n")
        first = re.search(r"^## ", changelog, re.M)
        at = first.start() if first else len(changelog)
        CHANGELOG.write_text(changelog[:at] + skeleton + changelog[at:], encoding="utf-8")
        changed.append(f"{CHANGELOG.relative_to(ROOT)} (new {version} skeleton)")
        wrote_skeleton = True

    for path in stamped_files():
        text = path.read_text(encoding="utf-8")
        # Same rule as check: only a value that is already a semantic version
        # is a stamp. `content="X.Y.Z"` is prose about stamps and stays prose.
        updated = STAMP.sub(
            lambda m: m.group(1) + version + m.group(3)
            if SEMVER.fullmatch(m.group(2)) else m.group(0),
            text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    if not changed:
        print(f"already at {version}; nothing to rewrite")
        return 0
    print(f"bumped to {version}:")
    for entry in changed:
        print(f"  {entry}")
    if wrote_skeleton:
        print(f"\nWrite the {version} changelog entry over its {TODO} markers, "
              f"then: python3 scripts/bump_version.py --check")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump or verify the Editorial Motion release version.")
    parser.add_argument("version", nargs="?",
                        help="the new release version, e.g. 1.11.0")
    parser.add_argument("--check", action="store_true",
                        help="report drift and change nothing")
    args = parser.parse_args()

    if args.check and args.version:
        parser.error("--check reports drift; it does not take a version")
    if not args.check and not args.version:
        parser.error("give a version to bump to, or --check")
    if args.version and not RELEASE.fullmatch(args.version):
        detail = (" — the changelog heading carries a plain release version"
                  if SEMVER.fullmatch(args.version) else "")
        parser.error(f"not a release version: {args.version}{detail}")

    return check() if args.check else bump(args.version)


if __name__ == "__main__":
    sys.exit(main())
