#!/usr/bin/env python3
"""Generate seamlessly tiling grain plates for the editorial-motion skills.

Grain is the last layer in every reference recipe — "grain last", after the
tint, the curves and the texture. It is also the layer generated design most
often omits, which is a large part of why generated output reads as digital.

Two things this fixes that a sourced grain PNG does not:

1. **It tiles.** `type-treatment/assets/example.html` currently carries the
   warning that a grain plate must be applied `cover` rather than tiled because
   "a tiled texture shows its seams as hard bands". Stretching one plate over a
   whole card means the grain scales with the element, so a large card gets soft
   blurry grain and a small one gets harsh grain. A seamless tile is applied at
   a fixed pixel size and stays the same everywhere.

2. **It can move.** Static grain is a tell — real film grain is different on
   every frame. `--frames N` writes N independent plates to cycle through, using
   the same stacked-and-stepped idiom as `.tt-boil` in type.css.

Stdlib only. See _noise.py.

Usage
-----
    python3 make-grain.py --out grain.png
    python3 make-grain.py --frames 3 --out grain.png     # grain-1/2/3.png
    python3 make-grain.py --softness 1.4 --intensity .8 --out coarse.png
    python3 make-grain.py --check-tile
"""

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _noise import fbm, seam_ratio, white_noise, write_png  # noqa: E402


def seam_threshold(size):
    """Return a size-aware tolerance for seam discontinuity ratio checks."""
    if size <= 80:
        return 1.7
    return 1.35


def build_grain(size, rng, softness, intensity):
    """Grain field centred on zero.

    `softness` is grain *size* — the reference recipe calls for 1.4, meaning
    slightly chunkier than one pixel. At 1.0 the plate is pure per-pixel noise;
    above that, progressively more of a mid-frequency value-noise layer is
    blended in, which clumps the grain without blurring it.
    """
    fine = white_noise(size, rng)
    if softness <= 1.0:
        field = fine
    else:
        # Frequency falls as softness rises: 1.4 -> lattice ~183 on a 256 tile,
        # i.e. clumps about 1.4px across.
        freq = max(2, int(size / softness))
        chunky = fbm(size, freq, freq, 2, rng)
        # Normalise: fbm output is roughly half the amplitude of white noise.
        chunky = [c * 2.0 for c in chunky]
        blend = min(1.0, (softness - 1.0) / 1.5)
        field = [f * (1 - blend) + c * blend for f, c in zip(fine, chunky)]

    return [v * intensity for v in field]


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Generate seamlessly tiling grain plates (stdlib only).")
    p.add_argument("--size", type=int, default=256,
                   help="tile edge in px (default 256 — grain is fine detail, "
                        "a small tile is enough)")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--frames", type=int, default=1,
                   help="write N independent plates to cycle for moving grain; "
                        "files are named <out>-1.png ... <out>-N.png")
    p.add_argument("--softness", type=float, default=1.4,
                   help="grain size in px; 1.0 is per-pixel (default 1.4, the "
                        "reference value)")
    p.add_argument("--intensity", type=float, default=1.0,
                   help="amplitude multiplier before the mid-grey offset")
    p.add_argument("--spread", type=float, default=0.42,
                   help="how far full-amplitude grain moves from mid-grey, "
                        "0-1 (default 0.42)")
    p.add_argument("--check-tile", action="store_true")
    p.add_argument("--out", default="grain.png")
    args = p.parse_args(argv)

    if args.size < 32:
        p.error("--size must be at least 32")
    if args.softness <= 0:
        p.error("--softness must be > 0")
    if args.intensity < 0:
        p.error("--intensity must be >= 0")
    if args.frames < 1:
        p.error("--frames must be at least 1")
    if not 0 < args.spread <= 1:
        p.error("--spread must be in (0, 1]")

    def plate(seed):
        rng = random.Random(seed)
        field = build_grain(args.size, rng, max(1.0, args.softness),
                            args.intensity)
        # Mid-grey centred so `mix-blend-mode: overlay` leaves the layer beneath
        # untouched where the grain is neutral, and only modulates around it.
        return [
            max(0, min(255, int(round(128 + v * 255 * args.spread))))
            for v in field
        ]

    if args.check_tile:
        px = plate(args.seed)
        rx, ry = seam_ratio(px, args.size, args.size, 1)
        print(f"seam/neighbour mean delta  x: {rx:.2f}x   y: {ry:.2f}x")
        threshold = seam_threshold(args.size)
        ok = rx < threshold and ry < threshold
        print("seamless" if ok else "NOT SEAMLESS")
        return 0 if ok else 1

    stem = Path(args.out).with_suffix("")
    suffix = Path(args.out).suffix or ".png"
    for i in range(args.frames):
        # Distinct seeds, not offsets of one field: cycling shifted copies of
        # the same noise reads as the grain *sliding*, which is worse than not
        # animating it at all.
        px = plate(args.seed + i * 977)
        path = args.out if args.frames == 1 else f"{stem}-{i + 1}{suffix}"
        written = write_png(path, args.size, args.size, px, 1)
        print(f"{path}  {args.size}x{args.size}  softness {args.softness}  "
              f"{written // 1024} KB")

    if args.frames > 1:
        print(f"\nCycle these with the .tt-boil idiom from type.css: {args.frames} "
              f"stacked layers, steps(1, end), one visible per frame.\n"
              f"Hold each for 1/12s to match the house posterize rate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
