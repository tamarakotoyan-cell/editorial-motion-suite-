#!/usr/bin/env python3
"""Validate the shared Editorial Motion source for Codex and Claude."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "editorial-motion"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?$")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def base_version(value: object) -> str | None:
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        return None
    return value.split("+", 1)[0]


def main() -> int:
    errors: list[str] = []
    claude_path = PLUGIN / ".claude-plugin" / "plugin.json"
    codex_path = PLUGIN / ".codex-plugin" / "plugin.json"
    claude = load_json(claude_path, errors)
    codex = load_json(codex_path, errors)

    if claude.get("name") != "editorial-motion" or codex.get("name") != "editorial-motion":
        errors.append("both host manifests must use plugin name editorial-motion")
    claude_version = base_version(claude.get("version"))
    codex_version = base_version(codex.get("version"))
    if not claude_version or not codex_version:
        errors.append("both host manifests must contain valid semantic versions")
    elif claude_version != codex_version:
        errors.append(f"host manifest versions disagree: Claude {claude_version}, Codex {codex_version}")
    if codex.get("skills") != "./skills/":
        errors.append("Codex manifest must expose the shared ./skills/ directory")

    headings = re.findall(
        r"^## +(\d+\.\d+\.\d+)\b",
        (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8"),
        re.M,
    )
    if not headings or headings[0] != claude_version:
        errors.append("newest changelog entry must match the shared manifest base version")

    skill_dirs = sorted(path for path in (PLUGIN / "skills").iterdir() if path.is_dir())
    for folder in skill_dirs:
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{folder.relative_to(ROOT)} has no SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            errors.append(f"{skill_file.relative_to(ROOT)} has invalid frontmatter")
            continue
        fields = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if not separator:
                errors.append(f"{skill_file.relative_to(ROOT)} has malformed frontmatter")
                continue
            fields[key.strip()] = value.strip()
        unknown = sorted(set(fields) - {"name", "description"})
        if unknown:
            errors.append(f"{skill_file.relative_to(ROOT)} uses non-portable fields: {', '.join(unknown)}")
        if fields.get("name") != folder.name:
            errors.append(f"{skill_file.relative_to(ROOT)} name must match its directory")
        if not fields.get("description"):
            errors.append(f"{skill_file.relative_to(ROOT)} needs a description")

    for path in (PLUGIN / "skills").rglob("*"):
        if path.is_file() and "remotion" in path.read_text(encoding="utf-8", errors="ignore").lower():
            errors.append(f"{path.relative_to(ROOT)} retains a Remotion dependency or instruction")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(skill_dirs)} shared skills, Codex and Claude at {claude_version}, no Remotion coupling")
    return 0


if __name__ == "__main__":
    sys.exit(main())
