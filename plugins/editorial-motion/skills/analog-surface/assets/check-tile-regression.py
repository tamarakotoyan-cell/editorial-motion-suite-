#!/usr/bin/env python3
"""Regression guard for --check-tile seam continuity false-positives.

This is intentionally tiny and non-invasive: it samples a handful of seeded
inputs and fails if any case exceeds an explicit max-fail threshold.
"""

import argparse
import importlib.util
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _noise import seam_ratio  # noqa: E402


def load_module(path):
    name = f"analog_tool_{path.stem}_{abs(hash(path)) % 1000000}"
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_check_tile(script, args, seeds):
    """Run CLI --check-tile and return number of non-zero exit codes."""
    fails = 0
    first_fail = None
    for seed in seeds:
        cmd = [sys.executable, str(script), *args, "--seed", str(seed), "--check-tile"]
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            fails += 1
            if first_fail is None:
                first_fail = (
                    seed,
                    proc.stdout.strip(),
                    proc.stderr.strip(),
                    proc.returncode,
                )
    return fails, first_fail


def make_paper_breakcase(module, variant="stock", size=64):
    rng = random.Random(11)
    detail = module.build_detail(variant, size, rng, 1.0, 1.0, 1.0)
    pixels = []
    for d in detail:
        v = int(round(128 + d * 127))
        v = max(0, min(255, v))
        pixels.extend((v, v, v))

    # Introduce a clear synthetic X-axis discontinuity at x=0.
    broken = pixels[:]
    for y in range(size):
        for c in range(3):
            idx0 = (y * size + 0) * 3 + c
            idx1 = (y * size + 1) * 3 + c
            broken[idx0] = 0
            broken[idx1] = 0

    ratio_x, ratio_y = seam_ratio(broken, size, size, 3)
    return ratio_x, ratio_y, module.seam_threshold(size)


def make_grain_breakcase(module, size=64):
    rng = random.Random(23)
    field = module.build_grain(size, rng, 1.4, 1.0)
    pixels = [max(0, min(255, int(round(128 + v * 255 * 0.42)))) for v in field]

    broken = pixels[:]
    for y in range(size):
        idx0 = y * size
        idx1 = y * size + 1
        broken[idx0] = 0
        broken[idx1] = 0

    ratio_x, ratio_y = seam_ratio(broken, size, size, 1)
    return ratio_x, ratio_y, module.seam_threshold(size)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Run a tiny regression sweep over check-tile thresholds."
    )
    p.add_argument("--seeds", type=int, default=12,
                   help="number of seeds to sample from each case (default 12)")
    p.add_argument("--strict", action="store_true",
                   help="run with the stricter max-fail thresholds")
    args = p.parse_args(argv)

    paper = ROOT / "make-paper.py"
    grain = ROOT / "make-grain.py"

    # Hand-tuned cases for quick signal:
    paper_cases = [
        ("stock", 64, args.seeds, 0),
        ("stock", 80, args.seeds, 0 if args.strict else 1),
        ("laid", 64, args.seeds, 0),
        ("laid", 80, args.seeds, 0),
        ("newsprint", 64, args.seeds, 0),
        ("crumpled", 64, args.seeds, 0),
    ]

    # Grain is the likely highest-noise path; still expected to remain stable at
    # these seeds/sizes once thresholding is fixed.
    grain_cases = [
        (32, args.seeds, 0),
        (48, args.seeds, 0),
        (64, args.seeds, 0),
        (80, args.seeds, 0),
    ]

    seeds = list(range(1, args.seeds + 1))
    failed = False
    total_cases = 0
    total_failures = 0

    print("paper --check-tile sweep")
    for variant, size, _, max_fails in paper_cases:
        total_cases += 1
        fails, first_fail = run_check_tile(
            paper,
            ["--variant", variant, "--size", str(size)],
            seeds,
        )
        total_failures += fails
        status = "PASS" if fails <= max_fails else "FAIL"
        if fails > max_fails:
            failed = True
        print(f"{status}  {variant:9s} size={size:3d}  fails={fails}/{len(seeds)}  max={max_fails}")
        if first_fail and fails > max_fails:
            seed, out, err, code = first_fail
            print(f"  first fail seed {seed}, exit {code}")
            if out:
                print(f"  stdout: {out}")
            if err:
                print(f"  stderr: {err}")

    print("grain --check-tile sweep")
    for size, _, max_fails in grain_cases:
        total_cases += 1
        fails, first_fail = run_check_tile(
            grain,
            ["--size", str(size)],
            seeds,
        )
        total_failures += fails
        status = "PASS" if fails <= max_fails else "FAIL"
        if fails > max_fails:
            failed = True
        print(f"{status}  grain      size={size:3d}  fails={fails}/{len(seeds)}  max={max_fails}")
        if first_fail and fails > max_fails:
            seed, out, err, code = first_fail
            print(f"  first fail seed {seed}, exit {code}")
            if out:
                print(f"  stdout: {out}")
            if err:
                print(f"  stderr: {err}")

    print("synthetic seam-break checks")
    paper_module = load_module(paper)
    grain_module = load_module(grain)
    px_rx, px_ry, px_thr = make_paper_breakcase(paper_module)
    gr_rx, gr_ry, gr_thr = make_grain_breakcase(grain_module)
    paper_break = (px_rx >= px_thr) or (px_ry >= px_thr)
    grain_break = (gr_rx >= gr_thr) or (gr_ry >= gr_thr)

    print(f"{'PASS' if paper_break else 'FAIL'} paper seam break  "
          f"rx={px_rx:.3f} ry={px_ry:.3f} threshold={px_thr:.2f}")
    print(f"{'PASS' if grain_break else 'FAIL'} grain seam break  "
          f"rx={gr_rx:.3f} ry={gr_ry:.3f} threshold={gr_thr:.2f}")

    if not paper_break or not grain_break:
        failed = True

    print(f"summary: {total_failures} seed-check failures across {len(paper_cases)+len(grain_cases)} cases")
    if failed:
        print("status: FAIL")
        return 1
    print("status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
