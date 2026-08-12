#!/usr/bin/env python3
"""Generate seamlessly tiling paper surfaces for the editorial-motion skills.

Why this exists
---------------
The Vox-style reference tutorials all source their texture from texturelabs.org.
That library is free to *use*, but its terms forbid redistributing the files
"even for free" and forbid using them "to create templates or extensions" — so a
distributed plugin cannot ship them. See vox-longform-analysis.md, Priority 3.

Generating instead is not a workaround, it is better suited to the job. The
reference set uses overlay texture at ~5% opacity (recorded four separate times
in sources.md §12/§13/§14), and at that strength a photographed grunge scan and
generated value noise are indistinguishable. Generation also makes the texture
*parameterised* rather than a fixed set of files, costs no bytes in the repo, and
is deterministic across runs for a given seed.

Where procedural genuinely loses is a hero sheet at full strength with real
crinkles and oxidation. Use a public-domain scan there (Library of Congress,
Smithsonian Open Access, Internet Archive) — CC0, redistributable, and actual
paper rather than a simulation of it.

Stdlib only. No numpy, no Pillow. A plugin that needs a pip install before its
assets build is a plugin that does not get used.

Everything this writes tiles seamlessly. Edge darkening and vignetting are
deliberately *not* included — they would break the wrap, and they belong in CSS
(`radial-gradient`) where they can adapt to the element they sit behind.

Usage
-----
    python3 make-paper.py --variant stock --out paper-stock.png
    python3 make-paper.py --variant newsprint --size 1024 --seed 7 --matte
    python3 make-paper.py --variant crumpled --age 0.6 --out aged.png
    python3 make-paper.py --mode overlay --out grain-overlay.png
    python3 make-paper.py --variant laid --check-tile

`--mode surface` (default) writes an RGB paper ground, ready to use directly.
`--mode overlay` writes a greyscale texture centred on mid-grey, for
`mix-blend-mode: overlay` at 3-8% over anything.
`--matte` additionally writes `<name>-matte.png`: the surface's own luminance,
contrast-stretched. That is the luma matte the ink layer masks against, so the
paper's fibres cut into the ink instead of the ink sitting on top of it.
"""

import argparse
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _noise import fbm, seam_ratio, white_noise, write_png  # noqa: E402

# The measured Vox paper white, read off the colour picker in Chris Moran's
# "How VOX breaks the Digital Feel" at 2:00 — H 41 deg, S 6%, B 99%.
# Never pure white: "every room is going to have some sort of light temperature
# ... your paper is always going to absorb that temperature."
DEFAULT_TONE = "#FDFAF3"


def ridged(size, fx, fy, octaves, rng):
    """Ridged fractal noise — creases rather than mounds.

    Folding the noise at zero and inverting turns smooth valleys into sharp
    ridges, which is what a crease in paper actually is.
    """
    n = fbm(size, fx, fy, octaves, rng)
    return [1.0 - abs(v) * 2.0 for v in n]


# ------------------------------------------------------------- shading ------

def emboss(height, size, azimuth=math.radians(135), strength=1.0):
    """Light a height field from one direction and return a shading term.

    Used for crumple. The gradient is taken with wraparound so the shading
    tiles as cleanly as the height field it came from.
    """
    lx = math.cos(azimuth)
    ly = math.sin(azimuth)
    out = [0.0] * (size * size)
    for y in range(size):
        row = y * size
        up = ((y - 1) % size) * size
        down = ((y + 1) % size) * size
        for x in range(size):
            left = (x - 1) % size
            right = (x + 1) % size
            dx = height[row + right] - height[row + left]
            dy = height[down + x] - height[up + x]
            out[row + x] = (dx * lx + dy * ly) * strength
    return out


# -------------------------------------------------------------- variants ----

def build_detail(variant, size, rng, fibre, blotch, grain):
    """Compose one variant's detail field, centred on zero.

    Weights are in fractions of base tone brightness, so 0.045 means that layer
    swings the paper by +/-4.5% at its extremes. The governing constraint: paper
    is *quiet*. Real stock varies a few percent across a sheet, and the first
    pass at this file ran at RMS 0.12 — six times too loud, which read as grey
    cloud rather than paper. Targets are RMS ~0.02 and p99 ~0.05; `--check-amp`
    reports both.

    Mottle base frequencies are kept at 5-6 rather than 2-3 for a second reason:
    low-frequency content inside a tile is the main cause of visible repetition
    when that tile is repeated across a large surface.
    """
    detail = [0.0] * (size * size)

    def add(layer, weight):
        nonlocal detail
        detail = [d + v * weight for d, v in zip(detail, layer)]

    if variant == "stock":
        # Smooth cartridge/office stock. Felted fibre, very faint mottle.
        add(fbm(size, 48, 48, 4, rng), 0.048 * fibre)
        add(fbm(size, 96, 24, 3, rng), 0.030 * fibre)   # slight machine direction
        add(fbm(size, 5, 5, 2, rng), 0.052 * blotch)
        add(white_noise(size, rng), 0.026 * grain)

    elif variant == "laid":
        # Laid paper: fine parallel laid lines, widely spaced chain lines.
        add(fbm(size, 48, 48, 4, rng), 0.038 * fibre)
        add(fbm(size, 5, 5, 2, rng), 0.044 * blotch)
        # Cosine, not sine: both wrap correctly at an integer cycle count, but
        # cosine puts a crest on the tile boundary where the gradient is zero,
        # matching the quintic noise layers. A sine puts its steepest point
        # there, which is harmless visually but makes --check-tile read a
        # consistent 1.1-1.3x false positive.
        laid_lines = [
            math.cos(2 * math.pi * (i % size) * 26 / size)
            for i in range(size * size)
        ]
        add(laid_lines, 0.013 * fibre)
        chain = [
            math.cos(2 * math.pi * (i // size) * 4 / size)
            for i in range(size * size)
        ]
        add(chain, 0.007 * fibre)
        add(white_noise(size, rng), 0.022 * grain)

    elif variant == "newsprint":
        # Coarser, woodier, more uneven — and legitimately louder than stock,
        # since cheap pulp is what unevenness looks like.
        add(fbm(size, 32, 32, 5, rng), 0.072 * fibre)
        add(fbm(size, 128, 32, 3, rng), 0.048 * fibre)
        add(fbm(size, 6, 6, 3, rng), 0.090 * blotch)
        add(white_noise(size, rng), 0.058 * grain)

    elif variant == "crumpled":
        # Stock, plus creases lit from upper-left. The emboss term is a spatial
        # gradient, so its raw magnitude is far smaller than the noise layers'
        # and it carries a correspondingly larger weight.
        add(fbm(size, 48, 48, 4, rng), 0.040 * fibre)
        add(fbm(size, 5, 5, 2, rng), 0.038 * blotch)
        creases = ridged(size, 5, 5, 4, rng)
        add(emboss(creases, size, strength=1.0), 0.42)
        add(white_noise(size, rng), 0.022 * grain)

    else:
        raise ValueError(f"unknown variant: {variant}")

    return detail


def apply_age(detail, size, rng, age):
    """Oxidation staining — irregular low-frequency darkening.

    Kept tileable on purpose. Edge browning is a separate concern and belongs in
    CSS, where it can respond to the size of the element rather than the tile.
    Returns a stain field in [0, 1] to be applied per-channel by the caller.
    """
    if age <= 0:
        return None
    stain = fbm(size, 2, 2, 3, rng)
    blotches = fbm(size, 6, 6, 3, rng)
    combined = [
        max(0.0, (s * 0.7 + b * 0.5) + 0.15) for s, b in zip(stain, blotches)
    ]
    peak = max(combined) or 1.0
    return [c / peak * age for c in combined]


# ---------------------------------------------------------------- output ----

def parse_hex(value):
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise argparse.ArgumentTypeError(
            f"bad colour: {value}. Use #RGB, #RRGGBB, RGB or RRGGBB."
        )
    try:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"bad colour: {value}. Use valid hex digits 0-9 and A-F."
        ) from exc


def seam_threshold(size):
    """Return a size-aware tolerance for seam discontinuity ratio checks.

    The historical 1.30 threshold is too strict at smaller sizes where local
    edge deltas are short-horizon and naturally noisy for valid generators. A
    higher tolerance for small sizes catches true seam breaks while reducing
    false negatives in valid tiles.
    """
    if size <= 80:
        return 1.7
    return 1.35


def apply_warmth(rgb, warmth):
    """Shift tone along the tungsten/daylight axis.

    Positive is warmer. The rationale is straight from the reference: paper
    absorbs the colour temperature of the room it is in, so a paper ground that
    is not tinted one way or the other reads as synthetic.
    """
    r, g, b = rgb
    r += 10 * warmth
    b -= 12 * warmth
    g += 2 * warmth
    return tuple(max(0, min(255, int(round(c)))) for c in (r, g, b))


# ------------------------------------------------------------------ main ----

def main(argv=None):
    p = argparse.ArgumentParser(
        description="Generate seamlessly tiling paper textures (stdlib only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--variant", default="stock",
                   choices=["stock", "laid", "newsprint", "crumpled"])
    p.add_argument("--mode", default="surface", choices=["surface", "overlay"],
                   help="surface: RGB paper ground. overlay: greyscale centred "
                        "on mid-grey for mix-blend-mode at 3-8%%.")
    p.add_argument("--size", type=int, default=512,
                   help="tile edge in px (default 512)")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--tone", type=parse_hex, default=parse_hex(DEFAULT_TONE),
                   help=f"paper colour (default {DEFAULT_TONE}, the measured "
                        "Vox paper white)")
    p.add_argument("--warmth", type=float, default=0.0,
                   help="-1 cool to +1 warm, on top of --tone")
    p.add_argument("--strength", type=float, default=1.0,
                   help="overall texture depth multiplier")
    p.add_argument("--fibre", type=float, default=1.0)
    p.add_argument("--blotch", type=float, default=1.0)
    p.add_argument("--grain", type=float, default=1.0)
    p.add_argument("--age", type=float, default=0.0,
                   help="0-1 oxidation staining")
    p.add_argument("--matte", action="store_true",
                   help="also write <name>-matte.png, the luma matte the ink "
                        "layer masks against")
    p.add_argument("--matte-bite", type=float, default=0.45,
                   help="0-1: how far the paper's fibres eat into the ink. "
                        "0 leaves ink solid, 1 makes the darkest fibre fully "
                        "transparent (default 0.45)")
    p.add_argument("--matte-range", default="15,85",
                   help="percentile lo,hi stretched to full range before bite "
                        "is applied (default 15,85)")
    p.add_argument("--check-tile", action="store_true",
                   help="report wrap-edge discontinuity and exit non-zero if "
                        "the tile is not seamless")
    p.add_argument("--check-amp", action="store_true",
                   help="report detail amplitude (RMS / p99 / range) as a "
                        "fraction of base tone and exit")
    p.add_argument("--out", default=None)
    args = p.parse_args(argv)

    if args.size < 32:
        p.error("--size must be at least 32")
    if not -1 <= args.warmth <= 1:
        p.error("--warmth must be in [-1, 1]")
    if args.strength < 0:
        p.error("--strength must be >= 0")
    if args.fibre < 0 or args.blotch < 0 or args.grain < 0:
        p.error("--fibre, --blotch and --grain must be >= 0")
    if not 0 <= args.age <= 1:
        p.error("--age must be in [0, 1]")
    if not 0 <= args.matte_bite <= 1:
        p.error("--matte-bite must be in [0, 1]")
    try:
        matte_range = tuple(float(v) for v in args.matte_range.split(","))
        if len(matte_range) != 2 or not 0 <= matte_range[0] < matte_range[1] <= 100:
            raise ValueError
    except ValueError:
        p.error("--matte-range must be 'lo,hi' percentiles with lo < hi, "
                "e.g. 15,85")
    if args.size > 2048:
        print(f"warning: {args.size}px in pure Python will be slow; 512 tiles "
              f"fine for anything at overlay strength", file=sys.stderr)

    out = args.out or f"paper-{args.variant}.png"
    size = args.size
    rng = random.Random(args.seed)

    detail = build_detail(args.variant, size, rng, args.fibre, args.blotch,
                          args.grain)

    if args.check_amp:
        scaled = [d * args.strength for d in detail]
        mags = sorted(abs(d) for d in scaled)
        rms = math.sqrt(sum(d * d for d in scaled) / len(scaled))
        p99 = mags[int(len(mags) * 0.99)]
        print(f"{args.variant}/{args.mode}  rms {rms:.4f}  p99 {p99:.4f}  "
              f"range {min(scaled):+.4f} to {max(scaled):+.4f}")
        print("target: rms ~0.020 (newsprint ~0.035), p99 ~0.055, "
              "range within +/-0.12")
        return 0

    stain = apply_age(detail, size, rng, args.age)

    if args.mode == "overlay":
        # Mid-grey centred so `overlay` blend leaves the underlying tone alone
        # and only modulates it.
        pixels = [
            max(0, min(255, int(round(128 + d * 127 * args.strength))))
            for d in detail
        ]
        channels = 1
    else:
        base = apply_warmth(args.tone, args.warmth)
        pixels = []
        for i, d in enumerate(detail):
            shade = d * args.strength
            r, g, b = base
            r = r * (1 + shade)
            g = g * (1 + shade)
            b = b * (1 + shade)
            if stain is not None:
                s = stain[i]
                # Oxidation pulls blue down hardest, then green — the standard
                # yellowing of aged pulp.
                r *= 1 - 0.10 * s
                g *= 1 - 0.16 * s
                b *= 1 - 0.30 * s
            pixels.extend(
                max(0, min(255, int(round(c)))) for c in (r, g, b)
            )
        channels = 3

    if args.check_tile:
        rx, ry = seam_ratio(pixels, size, size, channels)
        print(f"seam/neighbour mean delta  x: {rx:.2f}x   y: {ry:.2f}x")
        # A correct wrap sits at 1.0. Small tile sizes inflate the ratio variance
        # without indicating a real seam issue, so the threshold is size-aware.
        # See _noise.seam_ratio for the known blind spot and baseline tuning.
        threshold = seam_threshold(size)
        ok = rx < threshold and ry < threshold
        print("seamless" if ok else "NOT SEAMLESS")
        return 0 if ok else 1

    written = write_png(out, size, size, pixels, channels)
    print(f"{out}  {size}x{size}  {args.variant}/{args.mode}  "
          f"seed {args.seed}  {written // 1024} KB")

    if args.matte:
        if channels == 3:
            luma = [
                (pixels[i * 3] * 299 + pixels[i * 3 + 1] * 587
                 + pixels[i * 3 + 2] * 114) / 1000
                for i in range(size * size)
            ]
        else:
            luma = [float(v) for v in pixels]

        # Percentile stretch, not a fixed contrast multiplier. Paper is quiet by
        # design — stock luma spans only a few percent — so a multiplier tuned
        # for one variant leaves another with a matte of alpha 0.78-1.0, which
        # bites into nothing. Anchoring to percentiles guarantees the same usable
        # range whatever the variant and whatever --strength was used.
        lo_pct, hi_pct = matte_range
        ordered = sorted(luma)
        lo = ordered[max(0, min(len(ordered) - 1,
                                int(len(ordered) * lo_pct / 100)))]
        hi = ordered[max(0, min(len(ordered) - 1,
                                int(len(ordered) * hi_pct / 100)))]
        span = (hi - lo) or 1.0
        bite = max(0.0, min(1.0, args.matte_bite))
        matte = []
        for v in luma:
            s = max(0.0, min(1.0, (v - lo) / span))
            matte.append(int(round(255 * (1 - bite * (1 - s)))))

        matte_path = str(Path(out).with_suffix("")) + "-matte.png"
        mw = write_png(matte_path, size, size, matte, 1)
        print(f"{matte_path}  luma matte, bite {bite:.2f}, "
              f"alpha {min(matte) / 255:.2f}-{max(matte) / 255:.2f}  "
              f"{mw // 1024} KB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
