#!/usr/bin/env python3
"""Does the static-design plugin route A / B / C correctly from the asset count?

The B-iii eval from the 19 Aug 2026 brief. 04-graphics-imagery says the picture
structure is decidable before design starts, from what has been supplied; this
asks the plugin for its five-line plan on each brief in `static-routing.json`
and reads the structure off the layout line. No artifact is built — the
question is the decision, not the tile — so a run is cheap.

    python3 evals/run-static-routing.py --dry-run     # validate the set, spend nothing
    python3 evals/run-static-routing.py               # the whole set
    python3 evals/run-static-routing.py --brief four-photos-pinboard

Drives `claude -p` at the plugin in the working tree (`--plugin-dir`). Each
brief is answered with the five-line plan and one line `Structure: <A|B|C|
type-led|data-led>`; the runner parses that line, falling back to the first
"Structure A/B/C" or "type-led"/"data-led" mention in the reply.

Exit codes: 0 all briefs route as expected, 1 one or more did not, 2 setup.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = ROOT / "evals" / "static-routing.json"

INSTRUCTION = (
    "\n\nDo not build the tile. Reply with the five-line plan only (finding, ground, "
    "type, layout, signature), then one final line in exactly this form: "
    "`Structure: A` / `Structure: B` / `Structure: C` / `Structure: type-led` / "
    "`Structure: data-led`. Do not ask follow-up questions."
)

VALID = {"A", "B", "C", "TYPE", "DATA"}
STRUCTURE_LINE = re.compile(r"^\s*[`*]*structure[`*]*\s*:\s*[`*]*\s*([A-Za-z-]+)", re.I | re.M)
MENTION = re.compile(r"\bstructure\s+([ABC])\b|\b(type-led|data-led)\b", re.I)


def normalise(token):
    t = token.strip().upper().rstrip(".")
    if t in ("A", "B", "C"):
        return t
    if t.startswith("TYPE"):
        return "TYPE"
    if t.startswith("DATA"):
        return "DATA"
    return None


def load():
    data = json.loads(BRIEFS.read_text(encoding="utf-8"))
    problems, seen = [], set()
    for ev in data["evals"]:
        for field in ("id", "name", "prompt", "assets", "expected_structure"):
            if field not in ev:
                problems.append(f"brief {ev.get('name', ev.get('id'))}: no {field}")
        if ev["name"] in seen:
            problems.append(f"duplicate brief name {ev['name']}")
        seen.add(ev["name"])
        for s in ev.get("expected_structure", []) + ev.get("must_not_be", []):
            if s not in VALID:
                problems.append(f"brief {ev['name']}: unknown structure {s!r}")
        if set(ev.get("expected_structure", [])) & set(ev.get("must_not_be", [])):
            problems.append(f"brief {ev['name']}: expected and must_not_be overlap")
    plugin = ROOT / data["plugin"]
    if not (plugin / ".claude-plugin" / "plugin.json").is_file():
        problems.append(f"plugin not found at {plugin}")
    return data, plugin, problems


def decide(reply):
    m = STRUCTURE_LINE.search(reply)
    if m:
        s = normalise(m.group(1))
        if s:
            return s, "structure line"
    for m in MENTION.finditer(reply):
        s = normalise(m.group(1) or m.group(2))
        if s:
            return s, "first mention"
    return None, "no structure named"


def run_brief(brief, plugin, workspace, model, timeout):
    rundir = workspace / brief["name"]
    rundir.mkdir(parents=True)
    cmd = ["claude", "-p", brief["prompt"] + INSTRUCTION,
           "--plugin-dir", str(plugin), "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        proc = subprocess.run(cmd, cwd=rundir, env=env, timeout=timeout,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return {"name": brief["name"], "ok": False, "got": None,
                "detail": f"timed out after {timeout}s"}
    (rundir / "stdout.json").write_text(proc.stdout, encoding="utf-8")
    reply = ""
    try:
        payload = json.loads(proc.stdout)
        reply = payload.get("result") or ""
        if payload.get("is_error") and "Not logged in" in reply:
            return {"name": brief["name"], "setup_error":
                    "the claude CLI is not authenticated in this environment"}
    except json.JSONDecodeError:
        reply = proc.stdout
    (rundir / "reply.md").write_text(reply, encoding="utf-8")
    got, how = decide(reply)
    ok = got in brief["expected_structure"] and got not in brief.get("must_not_be", [])
    return {"name": brief["name"], "ok": ok, "got": got, "how": how,
            "expected": brief["expected_structure"],
            "must_not_be": brief.get("must_not_be", []),
            "detail": f"got {got or 'nothing'} ({how}); expected "
                      f"{'/'.join(brief['expected_structure'])}"}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--brief", action="append")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--model")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--out")
    args = p.parse_args(argv)

    data, plugin, problems = load()
    if problems:
        print("the brief set is not well-formed:")
        for pr in problems:
            print("  ✘", pr)
        return 2
    briefs = data["evals"]
    if args.brief:
        wanted = set(args.brief)
        briefs = [b for b in briefs if b["name"] in wanted]
        unknown = wanted - {b["name"] for b in data["evals"]}
        if unknown:
            print(f"no such brief: {', '.join(sorted(unknown))}")
            return 2
    if args.dry_run:
        print(f"{len(data['evals'])} routing briefs, all well-formed; plugin at {data['plugin']}")
        for b in data["evals"]:
            a = b["assets"]
            print(f"  {b['name']:<28} photos {a['photographs']}  cutouts {a['cutouts']}  "
                  f"glyphs {a['glyphs']}  → {'/'.join(b['expected_structure'])}"
                  + (f"  (never {'/'.join(b['must_not_be'])})" if b.get("must_not_be") else ""))
        return 0
    if not shutil.which("claude"):
        print("the claude CLI is not on PATH — needed to run the briefs")
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    workspace = Path(args.out) if args.out else ROOT / "evals" / "runs" / f"routing-{stamp}"
    workspace.mkdir(parents=True, exist_ok=True)
    print(f"running {len(briefs)} routing brief(s) against {plugin}\nworkspace: {workspace}\n")
    results = []
    for b in briefs:
        print(f"  {b['name']} ...", flush=True)
        results.append(run_brief(b, plugin, workspace, args.model, args.timeout))
    setup = next((r for r in results if "setup_error" in r), None)
    if setup:
        print(f"\ncannot run the set: {setup['setup_error']}")
        return 2
    failed = 0
    print()
    for r in results:
        failed += not r["ok"]
        print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['name']:<28} {r['detail']}")
    (workspace / "results.json").write_text(json.dumps(
        {"timestamp": stamp, "plugin": str(plugin), "results": results}, indent=2),
        encoding="utf-8")
    print(f"\n{len(results) - failed}/{len(results)} briefs route as expected. "
          f"results.json in {workspace}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
