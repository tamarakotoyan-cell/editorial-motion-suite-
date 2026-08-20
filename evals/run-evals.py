#!/usr/bin/env python3
"""Run the golden brief set against the editorial-motion plugin.

`check-artifact.py --self-test` tests the linter. `build-skills.py` tests the
paths. Neither tests the skills. Without this, an edit to `motion-system` cannot
be shown to have improved or degraded anything, and the only evidence a change
helped is that it felt better on the one artifact someone happened to look at.

What one run does, per brief
----------------------------
Drives `claude -p` at the plugin **in the working tree** — `--plugin-dir`, not
the installed copy — so the set tests the code being edited rather than whatever
was last published. Each brief runs in its own empty directory, so the artifact
it writes is unambiguous.

Three things are then checked mechanically:

    load order    the router loads first, and the skills the brief needs load
                  in the order the router mandates. Order is checked as a
                  subsequence of first-load, not as an exact list — a brief that
                  legitimately pulls in imagery-motion should not fail for it.
    exclusivity   editorial-explainer and premium-product-motion are
                  alternatives. Loading both is the failure this catches.
    lint          check-artifact.py --strict on the artifact. Strict here, not
                  in CI: a golden brief is a controlled input, so a warning is a
                  finding rather than noise.

The fourth thing — whether the piece is any good — is not mechanical, and this
script does not pretend otherwise. It writes `rubric.md` with the three-question
check from house-rules.md for a human to fill in.

Usage
-----
    python3 evals/run-evals.py                    # the whole set
    python3 evals/run-evals.py --brief stat-tile  # one, repeatable
    python3 evals/run-evals.py --dry-run          # validate the set, spend nothing

`--dry-run` checks that every skill a brief names exists and that the set is
well-formed. It costs nothing and is what CI runs; a real run costs tokens and
several minutes per brief, so it belongs in the version-bump process, run by a
person, not on every push.

Exit codes: 0 all briefs pass, 1 one or more failed, 2 bad usage or setup.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = ROOT / "evals" / "briefs.json"
LINTER = (ROOT / "plugins" / "editorial-motion" / "skills" / "analog-surface"
          / "assets" / "check-artifact.py")

# Appended to every brief so the runner knows where to look. It says where to
# put the file and nothing about how to design it — the point of the set is to
# see what the skills do when nobody tells them.
OUTPUT_INSTRUCTION = (
    "\n\nSave the finished artifact as artifact.html in the current directory. "
    "Do not open a browser or ask follow-up questions; produce the file."
)

SKILL_MD = re.compile(r"/skills/([\w-]+)/SKILL\.md")


def load_briefs():
    data = json.loads(BRIEFS.read_text(encoding="utf-8"))
    plugin = ROOT / data["plugin"]
    available = {p.name for p in (plugin / "skills").iterdir() if p.is_dir()}
    problems = []
    seen = set()
    for ev in data["evals"]:
        for field in ("id", "name", "prompt", "expected_load_order"):
            if not ev.get(field):
                problems.append(f"brief {ev.get('name', ev.get('id'))}: no {field}")
        if ev["name"] in seen:
            problems.append(f"duplicate brief name {ev['name']}")
        seen.add(ev["name"])
        for skill in ev["expected_load_order"] + ev.get("must_not_load", []):
            if skill not in available:
                problems.append(f"brief {ev['name']}: names unknown skill {skill}")
        if "editorial-motion" not in ev["expected_load_order"]:
            problems.append(f"brief {ev['name']}: does not expect the router")
    return data, plugin, problems


def observed_skills(events):
    """Skill names in order of first load, from the run's tool calls.

    A skill enters context either through the Skill tool or through a Read of
    its SKILL.md, and which one happens is not something a brief should depend
    on, so both count.
    """
    order = []
    for event in events:
        if event.get("type") != "assistant":
            continue
        for block in event.get("message", {}).get("content", []):
            if block.get("type") != "tool_use":
                continue
            name, args = block.get("name", ""), block.get("input", {})
            found = None
            if name == "Skill":
                found = str(args.get("skill", "")).split(":")[-1].strip()
            elif name == "Read":
                m = SKILL_MD.search(str(args.get("file_path", "")))
                found = m.group(1) if m else None
            if found and found not in order:
                order.append(found)
    return order


def is_subsequence(expected, observed):
    """Every expected skill present, in the expected relative order.

    Deliberately not an equality check. A brief that also pulls in
    type-treatment is not wrong for doing so; a brief that decides motion
    before layout is.
    """
    it = iter(observed)
    return all(skill in it for skill in expected)


def run_metrics(events, elapsed):
    """What the run cost, so a change to the skills can be priced.

    Without this the set can say an edit kept the output compliant but not
    whether it took twice as long to get there. A shorter instruction that
    causes five more internal turns is not a saving, and only the pair of
    numbers shows it — so turns and tokens are always reported together.

    `turns` is the model's own iteration inside one non-interactive run, not
    corrective prompts from a person. It is the closest mechanical proxy the
    harness has for "how much rework did this take", and it is the number to
    watch when trimming context.
    """
    result = next((e for e in reversed(events)
                   if e.get("type") == "result"), {})
    usage = result.get("usage") or {}

    def tok(*keys):
        return sum(int(usage.get(k) or 0) for k in keys)

    read = tok("cache_read_input_tokens")
    written = tok("cache_creation_input_tokens")
    return {
        "turns": result.get("num_turns"),
        "input_tokens": tok("input_tokens") + read + written,
        "uncached_input_tokens": tok("input_tokens"),
        "cache_read_tokens": read,
        "output_tokens": tok("output_tokens"),
        "cost_usd": result.get("total_cost_usd"),
        "seconds": round(elapsed, 1),
        "tool_calls": sum(
            1 for e in events if e.get("type") == "assistant"
            for b in e.get("message", {}).get("content", [])
            if b.get("type") == "tool_use"),
    }


def run_brief(brief, plugin, workspace, model, timeout, permission_mode):
    rundir = workspace / brief["name"]
    rundir.mkdir(parents=True)
    workdir = rundir / "work"
    workdir.mkdir()

    cmd = ["claude", "-p", brief["prompt"] + OUTPUT_INSTRUCTION,
           "--plugin-dir", str(plugin),
           "--output-format", "stream-json", "--verbose",
           "--permission-mode", permission_mode,
           "--add-dir", str(workdir)]
    if model:
        cmd += ["--model", model]

    # CLAUDECODE is a guard against nesting an interactive session; a
    # programmatic subprocess is the case it is not guarding against.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    started = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(cmd, cwd=workdir, env=env, timeout=timeout,
                              capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return {"name": brief["name"], "checks": [
            ("completed", False, f"timed out after {timeout}s")]}
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()

    events = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    (rundir / "stream.jsonl").write_text(proc.stdout, encoding="utf-8")

    # A run that never reached the model is a setup problem, not a design
    # failure, and reporting it as five failed checks sends you looking in
    # entirely the wrong place. The nested CLI does not inherit credentials
    # from an enclosing Claude Code session, which is the usual cause.
    for event in events:
        if event.get("error") == "authentication_failed" or (
                event.get("type") == "result" and event.get("is_error")
                and "Not logged in" in str(event.get("result", ""))):
            return {"name": brief["name"], "setup_error":
                    "the claude CLI is not authenticated in this environment. "
                    "Run `claude` once interactively and /login, or set "
                    "ANTHROPIC_API_KEY, then run the set again."}

    order = observed_skills(events)
    metrics = run_metrics(events, elapsed)
    checks = []

    checks.append(("completed", proc.returncode == 0,
                   f"claude exited {proc.returncode}" if proc.returncode
                   else f"{elapsed:.0f}s"))

    checks.append(("router-first", bool(order) and order[0] == "editorial-motion",
                   f"first skill loaded was {order[0]}" if order
                   else "no skill loaded at all"))

    expected = brief["expected_load_order"]
    checks.append(("load-order", is_subsequence(expected, order),
                   f"expected {' -> '.join(expected)}; observed "
                   f"{' -> '.join(order) or 'nothing'}"))

    forbidden = sorted(set(brief.get("must_not_load", [])) & set(order))
    checks.append(("exclusivity", not forbidden,
                   f"loaded {', '.join(forbidden)}" if forbidden
                   else "no excluded skill loaded"))

    artifact = workdir / "artifact.html"
    if not artifact.exists():
        found = sorted(workdir.rglob("*.html"))
        if found:
            artifact = found[0]
    checks.append(("artifact-produced", artifact.exists(),
                   artifact.name if artifact.exists() else "no HTML written"))

    if artifact.exists():
        # Strict here, not in CI: a golden brief is a controlled input, so a
        # warning is a finding rather than noise. The profile is what tells the
        # linter whether a missing source line is fatal — it cannot tell a
        # survey finding from a product mockup on its own.
        lint_cmd = [sys.executable, str(LINTER), str(artifact), "--strict"]
        if brief.get("profile"):
            lint_cmd += ["--profile", brief["profile"]]
        lint = subprocess.run(lint_cmd, capture_output=True, text=True)
        (rundir / "lint.txt").write_text(lint.stdout + lint.stderr,
                                         encoding="utf-8")
        summary = next((l for l in lint.stdout.splitlines() if ":" in l),
                       "no linter output")
        checks.append(("lint-strict", lint.returncode == 0,
                       summary.split(": ", 1)[-1]))
    else:
        checks.append(("lint-strict", False, "nothing to lint"))

    return {"name": brief["name"], "checks": checks, "observed_order": order,
            "seconds": round(elapsed, 1), "metrics": metrics,
            "artifact": str(artifact) if artifact.exists() else None}


def print_cost_table(results):
    """Turns and tokens beside the pass/fail, because trimming context is a
    trade and this is the side of it the checks above cannot see.

    Read the two columns together. Context going down while turns go up is a
    skill file that was carrying its weight; both going down is a real saving.
    """
    priced = [r for r in results if r.get("metrics", {}).get("turns")]
    if not priced:
        return
    print(f"\n{'brief':<24} {'turns':>6} {'tools':>6} {'in':>10} "
          f"{'out':>8} {'secs':>7}  cost")
    for r in priced:
        m = r["metrics"]
        cost = f"${m['cost_usd']:.3f}" if m.get("cost_usd") else "—"
        print(f"{r['name']:<24} {m['turns']:>6} {m['tool_calls']:>6} "
              f"{m['input_tokens']:>10,} {m['output_tokens']:>8,} "
              f"{m['seconds']:>7.1f}  {cost}")
    total_in = sum(r["metrics"]["input_tokens"] for r in priced)
    total_out = sum(r["metrics"]["output_tokens"] for r in priced)
    total_turns = sum(r["metrics"]["turns"] for r in priced)
    print(f"{'TOTAL':<24} {total_turns:>6} {'':>6} {total_in:>10,} "
          f"{total_out:>8,}")
    print("\nCompare these against a baseline run of the same briefs before "
          "changing the skills.\nA shorter instruction that costs more turns "
          "is not a saving.")


def write_rubric(data, results, workspace):
    """The half no script can grade, laid out so a person can fill it in."""
    lines = ["# Human rubric — the three-question check", "",
             f"Source: `{data['rubric_source']}`", "",
             "Mechanical checks are in `results.json`. These are not mechanical.",
             "Any \"no\" is a fix, not a ship.", ""]
    for r in results:
        art = r.get("artifact") or "— no artifact produced —"
        lines += [f"## {r['name']}", "", f"Artifact: `{art}`", ""]
        for q in data["rubric"]:
            lines += [f"- [ ] {q}"]
        lines += ["", "Notes:", "", ""]
    (workspace / "rubric.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--brief", action="append",
                   help="run only this brief by name (repeatable)")
    p.add_argument("--dry-run", action="store_true",
                   help="validate the set without calling claude")
    p.add_argument("--model", help="model id to run the briefs on")
    p.add_argument("--timeout", type=int, default=900,
                   help="seconds per brief (default 900)")
    p.add_argument("--permission-mode", default="acceptEdits")
    p.add_argument("--out", help="workspace directory (default evals/runs/<ts>)")
    args = p.parse_args(argv)

    data, plugin, problems = load_briefs()
    if problems:
        print("the brief set is not well-formed:")
        for problem in problems:
            print("  ✘", problem)
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
        print(f"{len(data['evals'])} briefs, all well-formed; "
              f"every skill named exists in {data['plugin']}")
        for b in data["evals"]:
            print(f"  {b['name']:<24} {' -> '.join(b['expected_load_order'])}")
        return 0

    if not shutil.which("claude"):
        print("the claude CLI is not on PATH — needed to run the briefs")
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    workspace = Path(args.out) if args.out else ROOT / "evals" / "runs" / stamp
    workspace.mkdir(parents=True, exist_ok=True)

    print(f"running {len(briefs)} brief(s) against {plugin}")
    print(f"workspace: {workspace}\n")

    results = []
    for brief in briefs:
        print(f"  {brief['name']} ...", flush=True)
        results.append(run_brief(brief, plugin, workspace, args.model,
                                 args.timeout, args.permission_mode))

    setup = next((r for r in results if "setup_error" in r), None)
    if setup:
        print(f"\ncannot run the set: {setup['setup_error']}")
        return 2

    print()
    failed = 0
    for r in results:
        bad = [c for c in r["checks"] if not c[1]]
        status = "PASS" if not bad else "FAIL"
        failed += bool(bad)
        print(f"{status}  {r['name']}")
        for rule, ok, detail in r["checks"]:
            print(f"        {'ok  ' if ok else 'FAIL'} {rule:<18} {detail}")

    (workspace / "results.json").write_text(
        json.dumps({"timestamp": stamp, "plugin": str(plugin),
                    "results": results}, indent=2), encoding="utf-8")
    write_rubric(data, results, workspace)
    print_cost_table(results)

    print(f"\n{len(results) - failed}/{len(results)} briefs pass the mechanical "
          f"checks.")
    print(f"results.json and rubric.md written to {workspace}")
    print("The rubric is the half that matters and the half no script can "
          "grade — fill it in before shipping a version.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
