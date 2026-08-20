#!/usr/bin/env python3
"""Treat a cutout for the frame: harden → window → duotone → (halftone).

The raster pipeline in 04-graphics-imagery, as a script, so a treated cutout
can be produced the same way twice. It is what made the two proof assets for
the layered-editorial register (08) — the halftoned subject and the duotoned
ground mass — and it is the step that turns seven photographs shot by seven
people into one sheet.

The four steps, in order, and why each is there
-----------------------------------------------
1. **Harden the alpha.** A soft matte is what makes a cutout look pasted.
   Threshold at 128 (anything half-transparent or more is in, the rest is out),
   then shave one pixel off the edge with a MinFilter so the halo the keyer
   left — a ring of ground-coloured fringe — goes with it.
2. **Contrast window.** Stretch the greys so the subject uses the whole range
   before it is mapped. Auto by default (a 1% clip at each end, measured over
   the subject only, never the transparent surround); or an explicit
   `--window lo,hi` when the auto pick is wrong.
3. **Duotone to the brand map.** Shadow → one brand value, highlight → the
   other, and **the highlight must stay a colour.** A map whose highlight is
   within a few points of white on all three channels is greyscale with a
   rounding error, and reads as a black-and-white photograph sitting on the
   ground rather than an image belonging to it. The script runs 04's test —
   sample the lightest opaque pixel; if it is neutral the duotone did not
   happen — and fails loudly rather than writing a file.
4. **Halftone screen** (subjects only; a ground mass stops at step 3). Dots in
   the shadow colour on the highlight colour, on a rotated lattice, cell about
   7 source pixels — 5–8px at 1080 wide; below 4px it aliases at feed size.
   Dot area is proportional to darkness, so a mid grey is a half-covered cell,
   and the dots are drawn at 4× and downsampled so they are round.

It also prints the **measured subject box**, because placement comes from the
subject's bounding box and never from the file's frame (04): a portrait centred
in its PNG and one sitting in its left third land in different places from
identical CSS.

Usage
-----
    python3 halftone.py subject.png --out subject-halftone.png \\
        --shadow '#1E1E4A' --highlight '#E2491A'            # full pipeline
    python3 halftone.py mass.png --out mass-duotone.png --mode duotone \\
        --shadow '#1E1E4A' --highlight '#E2491A'            # stop before the screen
    python3 halftone.py subject.png --out s.png --cell 6 --angle 30 --window 20,235
    python3 halftone.py --self-test                          # prove the steps still work

Pillow only — no numpy — so it runs wherever the linter runs. Exit codes:
0 written, 1 the lightest-pixel test failed (or a self-test did), 2 bad usage.
"""

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps
except ImportError:                                            # pragma: no cover
    sys.exit("halftone.py needs Pillow:  python3 -m pip install pillow")

# --- thresholds, all from the principle files ------------------------------
ALPHA_THRESHOLD = 128       # 04: harden the alpha — in or out, nothing between
FRINGE_SHAVE = 1            # px eroded off the matte to drop the keyer's halo
CELL_PX = 7                 # 08: cell ≈7px in the source; 5–8px at 1080 wide
SCREEN_ANGLE = 45           # degrees; the classic single-ink screen
SUPERSAMPLE = 4             # dots drawn at 4x, then downsampled: round, not jagged
AUTO_CLIP = 1.0             # % clipped at each end by the auto contrast window
NEUTRAL_CHROMA = 24         # 04's lightest-pixel test: below this (max−min) it is grey
DOT_GAIN = 1.0              # multiply dot radius; >1 lets shadows close to solid


def parse_hex(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise argparse.ArgumentTypeError(f"not a hex colour: {value!r}")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def chroma(rgb):
    """Distance from the neutral axis, 0–255. Cheap stand-in for C* in LCh."""
    return max(rgb[:3]) - min(rgb[:3])


# --- the four steps ---------------------------------------------------------
def harden_alpha(im, threshold=ALPHA_THRESHOLD, shave=FRINGE_SHAVE, key_white=None):
    """A binary matte, eroded by `shave` px. Returns (rgba, matte)."""
    im = im.convert("RGBA")
    if key_white is not None:
        # No alpha to speak of: key on near-white ground. The pipeline's first
        # step is "key on the channel that separates subject from ground" —
        # white is the common case for a supplied cutout that lost its alpha.
        # A pixel is ground only if every channel is near-white, so key on the
        # minimum over the three channels, not on luma.
        r, g, b = im.convert("RGB").split()
        mn = ImageChops.darker(ImageChops.darker(r, g), b)
        matte = mn.point(lambda v: 0 if v >= key_white else 255)
    else:
        matte = im.getchannel("A")
    matte = matte.point(lambda a: 255 if a >= threshold else 0)
    if shave > 0:
        matte = matte.filter(ImageFilter.MinFilter(2 * shave + 1))
    im.putalpha(matte)
    return im, matte


def contrast_window(im, matte, window=None, clip=AUTO_CLIP):
    """Greyscale, stretched. `window=(lo,hi)` maps lo→0 and hi→255; else auto."""
    grey = ImageOps.grayscale(im.convert("RGB"))
    if window:
        lo, hi = window
        span = max(1, hi - lo)
        return grey.point(lambda v: max(0, min(255, round((v - lo) * 255 / span))))
    # Auto — measured over the subject only. Autocontrast over the whole file
    # would let the transparent surround (usually black or white in RGB) set
    # one end of the range and leave the subject flat.
    return ImageOps.autocontrast(grey, cutoff=clip, mask=matte)


def duotone(grey, shadow, highlight):
    return ImageOps.colorize(grey, black=shadow, white=highlight)


def lightest_pixel(rgb, matte):
    """The lightest opaque pixel — the one 04's test samples."""
    best, best_l = None, -1
    px, mp = rgb.load(), matte.load()
    w, h = rgb.size
    for y in range(h):
        for x in range(w):
            if mp[x, y] < 128:
                continue
            p = px[x, y]
            l = 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]
            if l > best_l:
                best, best_l = p[:3], l
    return best


def halftone(grey, matte, shadow, highlight, cell=CELL_PX, angle=SCREEN_ANGLE,
             gain=DOT_GAIN, supersample=SUPERSAMPLE):
    """Dots in the shadow colour on the highlight colour, area ∝ darkness."""
    w, h = grey.size
    S = supersample
    # a cell's darkness is the mean over the cell, not one pixel: box-blur then
    # point-sample at the lattice, which is the same thing and far cheaper
    blurred = grey.filter(ImageFilter.BoxBlur(cell / 2))
    bp = blurred.load()
    out = Image.new("RGB", (w * S, h * S), highlight)
    draw = ImageDraw.Draw(out)
    th = math.radians(angle)
    ct, st = math.cos(th), math.sin(th)
    cx, cy = w / 2, h / 2
    reach = math.hypot(w, h) / 2 + cell
    n = int(reach / cell) + 1
    dots = 0
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = i * cell, j * cell
            x = cx + u * ct - v * st
            y = cy + u * st + v * ct
            if not (0 <= x < w and 0 <= y < h):
                continue
            darkness = 1 - bp[int(x), int(y)] / 255
            if darkness <= 0.01:
                continue
            r = cell * math.sqrt(darkness / math.pi) * gain     # area ∝ darkness
            draw.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=shadow)
            dots += 1
    out = out.resize((w, h), Image.LANCZOS)
    return out, dots


# --- driver -----------------------------------------------------------------
def treat(src, mode, shadow, highlight, cell=CELL_PX, angle=SCREEN_ANGLE,
          threshold=ALPHA_THRESHOLD, shave=FRINGE_SHAVE, window=None,
          key_white=None, gain=DOT_GAIN):
    """Run the pipeline on an Image. Returns (rgba_out, report_dict).

    Raises ValueError when the lightest-pixel test fails: the caller decides
    whether that is fatal (it is, on the command line).
    """
    rgba, matte = harden_alpha(src, threshold, shave, key_white)
    if matte.getbbox() is None:
        raise ValueError("nothing survived the matte — is the alpha real, or "
                         "does this need --key-white?")
    grey = contrast_window(rgba, matte, window)
    duo = duotone(grey, shadow, highlight)
    light = lightest_pixel(duo, matte)
    report = {
        "mode": mode, "size": list(rgba.size),
        "subject_box": list(matte.getbbox()),        # left, top, right, bottom
        "shadow": "#%02X%02X%02X" % shadow, "highlight": "#%02X%02X%02X" % highlight,
        "lightest_pixel": list(light) if light else None,
        "lightest_chroma": chroma(light) if light else None,
        "alpha_values": len(set(matte.getdata())),   # must be 2 after hardening
    }
    if light is None or chroma(light) < NEUTRAL_CHROMA:
        raise ValueError(
            f"lightest opaque pixel is {light} (chroma "
            f"{chroma(light) if light else 0} < {NEUTRAL_CHROMA}) — the duotone did "
            "not happen. The highlight end of the map must remain a colour: push it "
            "to the actual brand value and let the shadow carry a hue (04).")
    if mode == "halftone":
        out, dots = halftone(grey, matte, shadow, highlight, cell, angle, gain)
        report.update({"cell": cell, "angle": angle, "dots": dots})
    else:
        out = duo
    out = out.convert("RGBA")
    out.putalpha(matte)
    return out, report


def _self_test():
    """Prove each step does what the docstring says, on a synthetic cutout.

    A disc with a soft alpha edge and a dark-to-light ramp across it. After
    the pipeline: the matte is binary and one pixel smaller than the soft
    edge; the lightest pixel is the highlight, and it is a colour; the screen
    drew dots; and a neutral highlight is refused.
    """
    w = h = 160
    src = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = src.load()
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - w / 2, y - h / 2)
            a = 255 if d < 60 else max(0, int(255 * (1 - (d - 60) / 12)))   # soft edge 60–72
            v = int(255 * x / (w - 1))                                       # ramp
            px[x, y] = (v, v, v, a)

    ok = True

    def check(cond, msg):
        nonlocal ok
        print(("OK    " if cond else "FAIL  ") + msg)
        ok = ok and cond

    out, rep = treat(src, "halftone", (0x1E, 0x1E, 0x4A), (0xE2, 0x49, 0x1A))
    check(rep["alpha_values"] == 2, "alpha hardened to two values")
    soft_r = 60 + 12 * (1 - 128 / 255)            # where the soft edge crosses 128
    l, t, r, b = rep["subject_box"]
    check((r - l) / 2 < soft_r, f"fringe shaved: matte radius {(r - l) / 2:.1f} < {soft_r:.1f}")
    check(rep["lightest_chroma"] >= NEUTRAL_CHROMA,
          f"lightest pixel {rep['lightest_pixel']} is a colour (chroma {rep['lightest_chroma']})")
    check(rep["dots"] > 100, f"halftone drew {rep['dots']} dots")
    colours = {p[:3] for p in out.getdata() if p[3] == 255}
    check(len(colours) > 2, "screen has both inks and antialiased edges")

    duo, rep2 = treat(src, "duotone", (0x1E, 0x1E, 0x4A), (0xE2, 0x49, 0x1A))
    check("dots" not in rep2, "duotone mode stops before the screen")

    try:
        treat(src, "duotone", (0x12, 0x12, 0x12), (0xF2, 0xF0, 0xEC))
        check(False, "neutral highlight refused")
    except ValueError:
        check(True, "neutral highlight refused (greyscale with a rounding error)")

    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("src", nargs="?", help="cutout PNG (alpha) or a photo with --key-white")
    p.add_argument("--out", help="output PNG")
    p.add_argument("--mode", choices=("halftone", "duotone"), default="halftone",
                   help="halftone for a subject (default); duotone for a ground mass")
    p.add_argument("--shadow", type=parse_hex, help="hex, the shadow end of the map")
    p.add_argument("--highlight", type=parse_hex, help="hex, the highlight end — a colour")
    p.add_argument("--cell", type=float, default=CELL_PX, help=f"dot cell in source px (default {CELL_PX})")
    p.add_argument("--angle", type=float, default=SCREEN_ANGLE, help=f"screen angle (default {SCREEN_ANGLE})")
    p.add_argument("--gain", type=float, default=DOT_GAIN, help="dot radius multiplier")
    p.add_argument("--alpha-threshold", type=int, default=ALPHA_THRESHOLD)
    p.add_argument("--shave", type=int, default=FRINGE_SHAVE, help="px eroded off the matte")
    p.add_argument("--window", help="lo,hi grey levels mapped to 0..255 (default: auto)")
    p.add_argument("--key-white", type=int, metavar="T",
                   help="no alpha: key out pixels whose channels are all >= T")
    p.add_argument("--json", action="store_true", help="print the report as JSON")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        return _self_test()
    if not (a.src and a.out and a.shadow and a.highlight):
        p.print_usage()
        print("need: src --out --shadow --highlight  (or --self-test)")
        return 2
    window = None
    if a.window:
        try:
            lo, hi = (int(v) for v in a.window.split(","))
            window = (lo, hi)
        except ValueError:
            print("--window wants two integers: lo,hi")
            return 2

    src = Image.open(a.src)
    try:
        out, report = treat(src, a.mode, a.shadow, a.highlight, a.cell, a.angle,
                            a.alpha_threshold, a.shave, window, a.key_white, a.gain)
    except ValueError as exc:
        print(f"FAIL  {exc}")
        return 1
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.save(a.out)
    report["out"] = a.out
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        l, t, r, b = report["subject_box"]
        print(f"wrote {a.out}  ({report['size'][0]}×{report['size'][1]}, {a.mode})")
        print(f"subject box  left {l} top {t} right {r} bottom {b}  "
              f"({r - l}×{b - t}) — place from this, not the file's frame")
        print(f"lightest pixel {tuple(report['lightest_pixel'])}  chroma "
              f"{report['lightest_chroma']}  — a colour: the duotone happened")
        if "dots" in report:
            print(f"screen  cell {a.cell}px  angle {a.angle}°  {report['dots']} dots")
    return 0


if __name__ == "__main__":
    sys.exit(main())
