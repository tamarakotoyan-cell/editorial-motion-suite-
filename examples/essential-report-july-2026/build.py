#!/usr/bin/env python3
"""Build the Essential Report right/wrong direction tile for Instagram.

Portrait 1080x1350. One frame, one fact: the July split, with the change on
June. Every mark is computed from the datum — the hundred dots ARE the
percentages, so `length / value` is constant by construction rather than by
eye.

    python3 build.py                 # writes tile.html and tile.png
    python3 build.py --no-png        # HTML only (skips Chromium)

Edit DATA below and re-run. Nothing else needs touching.

Colour and type come from the Essential design system
(`plugins/editorial-motion/skills/editorial-explainer/references/essential-tokens.md`).
Structure comes from `editorial-explainer`; the ban list in
`references/house-rules.md` overrides both.
"""

from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".fontcache"

# --------------------------------------------------------------------------
# DATA — the only block that changes month to month.
# --------------------------------------------------------------------------
# ⚠️ PLACEHOLDER FIGURES. These are shape-only stand-ins so the layout can be
# checked; they are NOT Essential Report results. Replace every value in this
# block with the published July figures before this goes anywhere near a feed.
DATA = {
    "placeholder": True,  # set False once the real figures are in

    "question": ("Overall, do you think the country is heading in the "
                 "right direction or the wrong direction?"),
    "month": "July",
    "fieldwork": "fieldwork 00–00 July 2026",
    "base": "all respondents (n=0,000)",

    # Percentages as published. They need not sum to exactly 100 — the dot
    # allocation below reconciles rounding and reports it if it had to.
    "july": {"right": 33, "wrong": 52, "unsure": 15},
    "june": {"right": 37, "wrong": 49, "unsure": 14},

    # Which group carries the accent. This is the editorial decision: the
    # accent goes on the mark that proves the finding, and on nothing else.
    "accent": "wrong",

    # What the hero figure IS — the one number the tile exists to deliver.
    #   "level"  the accent group's own share this month
    #   "gap"    how far the leading group sits clear of the other
    #   "change" the accent group's movement on June
    # Everything else is support, and is sized to look like support.
    "hero": "level",

    # Leave these as None to derive them from the numbers, or write them
    # yourself — the takeaway is editorial judgement, not arithmetic.
    "hero_label": None,
    "change_line": None,
}

LABELS = {
    "right": "Right direction",
    "wrong": "Wrong direction",
    "unsure": "Unsure",
}
ORDER = ["right", "wrong", "unsure"]

# --------------------------------------------------------------------------
# Palette — Essential tokens, with the measured separations that justify them.
# --------------------------------------------------------------------------
# L* values against the field, checked with the CIE L* formula:
#   field  #E9E7E5  L* 91.7
#   ink    #4E4E50  L* 33.2   dL 58.5 vs field
#   mid    #9A9490  L* 61.7   dL 30.0 vs field, dL 28.5 vs ink
#   accent #E2491A  L* 53.0   dL 38.8 vs field
#
# The two categorical neutrals clear the >=25 dL floor against each other and
# against the field. The accent cannot also clear 25 against both — at L* 53 it
# sits between them, and no single-accent palette on a light warm ground can
# satisfy all three pairs at once. It is separated by chroma instead, and the
# third category is separated by *form* (open rings, not a fill) so the
# encoding still survives greyscale and colour-blind viewing. Check any edit
# against both, not just against the swatch chips.
#
# Text contrast against the field (>=4.5:1 required):
#   ink    #4E4E50  6.73:1  ok
#   muted  #636366  4.85:1  ok  <- one step darker than the token #6D6D70,
#                                  which measures 4.18:1 and fails
#   accent #E2491A  3.27:1  FAILS — marks only, never text
FIELD = "#E9E7E5"
INK = "#4E4E50"
MUTED = "#636366"
ACCENT = "#E2491A"
MID = "#9A9490"

W, H = 1080, 1350
# 20 x 5 rather than 10 x 10: the band then runs the full text measure, so the
# marks, the headline and the key row all share one left edge. A square hundred
# would have to shrink to about half the measure to fit the portrait canvas and
# would float free of the type.
COLS, ROWS = 20, 5
CELL = 58
DOT_R = 20.5
RING_R = 18.0
RING_W = 5.0

ARCHIVO = "https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;700"
GLYPHS = ("abcdefghijklmnopqrstuvwxyz"
          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
          "0123456789 .,:;'’—–−+%()?“”/=")


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------
def fetch_archivo() -> dict[int, bytes]:
    """Archivo substitutes Berthold Akzidenz Grotesk, which is not
    web-licensable. Cached locally; Arial is the brand's own stated fallback if
    this cannot reach the network."""
    CACHE.mkdir(exist_ok=True)
    weights = {}
    for weight in (300, 400, 700):
        cached = CACHE / f"Archivo-{weight}.ttf"
        if cached.exists():
            weights[weight] = cached.read_bytes()
            continue
        try:
            req = urllib.request.Request(
                f"{ARCHIVO}&display=swap",
                headers={"User-Agent": "Mozilla/5.0"})
            css = urllib.request.urlopen(req, timeout=45).read().decode()
            url = None
            for block in css.split("@font-face"):
                if f"font-weight: {weight};" in block and "url(" in block:
                    url = block.split("url(")[1].split(")")[0]
                    break
            if not url:
                return {}
            data = urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                timeout=45).read()
            cached.write_bytes(data)
            weights[weight] = data
        except Exception as exc:                      # offline, proxy, 403
            print(f"  Archivo {weight} unavailable ({exc}); falling back to Arial",
                  file=sys.stderr)
            return {}
    return weights


def subset(raw: bytes, weight: int) -> bytes:
    """Cut the font down to the glyphs actually used. Optional — without
    fonttools the full face is embedded, which only costs file size."""
    try:
        from fontTools import subset as fts
    except ImportError:
        return raw
    src = CACHE / f"Archivo-{weight}.ttf"
    dst = CACHE / f"Archivo-{weight}.subset.woff2"
    if not dst.exists():
        try:
            fts.main([str(src), f"--text={GLYPHS}", "--flavor=woff2",
                      f"--output-file={dst}", "--layout-features=*"])
        except Exception:
            return raw
    return dst.read_bytes()


def font_css() -> tuple[str, str]:
    faces = fetch_archivo()
    if not faces:
        return "", "Arial, 'Liberation Sans', Helvetica, sans-serif"
    css = []
    for weight, raw in faces.items():
        data = subset(raw, weight)
        fmt = "woff2" if data[:4] == b"wOF2" else "truetype"
        b64 = base64.b64encode(data).decode()
        css.append(
            "@font-face{font-family:Archivo;font-style:normal;"
            f"font-weight:{weight};"
            f"src:url(data:font/{fmt};base64,{b64}) format('{fmt}')}}")
    return "\n".join(css), "Archivo, Arial, 'Liberation Sans', sans-serif"


# --------------------------------------------------------------------------
# Data -> marks
# --------------------------------------------------------------------------
def allocate(pct: dict[str, float]) -> tuple[dict[str, int], bool]:
    """Turn published percentages into exactly 100 dots, one dot = one per
    cent, using largest remainder. Returns whether rounding had to move a dot,
    because that is worth saying on the tile rather than hiding."""
    total = sum(pct.values())
    if abs(total - 100) > 2.5:
        raise SystemExit(f"figures sum to {total}, not ~100 — check DATA")
    scaled = {k: v * 100 / total for k, v in pct.items()}
    dots = {k: int(v) for k, v in scaled.items()}
    short = 100 - sum(dots.values())
    for key in sorted(scaled, key=lambda k: scaled[k] - int(scaled[k]),
                      reverse=True)[:short]:
        dots[key] += 1
    adjusted = any(dots[k] != round(pct[k]) for k in pct)
    return dots, adjusted


def fmt_pct(v: float) -> str:
    return f"{v:g}%"


def hero_markup(figure: str) -> str:
    """Set the per cent sign and any sign glyph down against the digits. At
    270px a full-size `%` takes about a third of the width and the figure stops
    reading as a number at a glance."""
    out = figure
    for glyph in ("%", "+", "−"):
        out = out.replace(glyph, f'<span class="unit">{glyph}</span>')
    return out


def fmt_delta(now: float, then: float) -> str:
    d = round(now - then, 1)
    if d == 0:
        return "no change since June"
    sign = "+" if d > 0 else "−"          # true minus, not a hyphen
    return f"{sign}{abs(d):g} since June"


def derive_hero(data: dict) -> tuple[str, str, str]:
    """The one number the tile delivers, its sentence, and the single line of
    movement — in that order of weight.

    An earlier draft set three values and three deltas at one size, and the
    result carried eight numbers of equal rank and no takeaway. Everything
    except the hero is deliberately demoted here; the other shares still
    appear, small, in the key beneath the marks.
    """
    july, june, accent = data["july"], data["june"], data["accent"]
    mode = data["hero"]
    other = "right" if accent == "wrong" else "wrong"

    if mode == "level":
        figure = fmt_pct(july[accent])
        if accent == "unsure":
            label = "are unsure which direction the country is heading"
        else:
            label = ("say the country is heading in the "
                     f"{LABELS[accent].lower()}")
    elif mode == "gap":
        lead = max(("right", "wrong"), key=lambda k: july[k])
        figure = f"{round(abs(july['wrong'] - july['right']), 1):g}"
        label = (f"points clear — {LABELS[lead].lower()} over "
                 f"{LABELS['right' if lead == 'wrong' else 'wrong'].lower()}")
    elif mode == "change":
        move = round(july[accent] - june[accent], 1)
        figure = f"{'+' if move > 0 else '−'}{abs(move):g}"
        label = (f"point move in {LABELS[accent].lower()} "
                 "in a single month")
    else:
        raise SystemExit(f'unknown hero mode {mode!r}')

    # One movement sentence, carrying both main groups. Three separate delta
    # chips is what made the first version unreadable.
    a_move = round(july[accent] - june[accent], 1)
    o_move = round(july[other] - june[other], 1)

    def phrase(move: float) -> str:
        if move == 0:
            return "unchanged"
        return f"{'up' if move > 0 else 'down'} {abs(move):g}"

    if a_move == 0 and o_move == 0:
        change = f"{data['month']}, unchanged on June."
    elif o_move == 0:
        change = (f"{data['month']}, {phrase(a_move)} points on June. "
                  f"{LABELS[other]} unchanged.")
    else:
        change = (f"{data['month']}, {phrase(a_move)} points on June. "
                  f"{LABELS[other]} {phrase(o_move)}.")

    return figure, data["hero_label"] or label, data["change_line"] or change


def grid_svg(dots: dict[str, int], accent_key: str) -> str:
    """The hundred marks. Filled accent, filled ink, open rings — three
    encodings that stay distinct in greyscale."""
    fills = {}
    for key in ORDER:
        if key == accent_key:
            fills[key] = ("fill", ACCENT)
        elif key == "unsure":
            fills[key] = ("ring", MID)
        else:
            fills[key] = ("fill", INK)
    # If the accent lands on unsure, the remaining two both need a fill; keep
    # one of them as rings so the third encoding is never lost.
    if accent_key == "unsure":
        fills["right"] = ("ring", MID)

    sequence = []
    for key in ORDER:
        sequence.extend([key] * dots[key])

    marks = []
    for i, key in enumerate(sequence):
        cx = (i % COLS) * CELL + CELL / 2
        cy = (i // COLS) * CELL + CELL / 2
        form, colour = fills[key]
        if form == "fill":
            marks.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{DOT_R:g}" '
                         f'fill="{colour}"/>')
        else:
            marks.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{RING_R:g}" '
                         f'fill="none" stroke="{colour}" '
                         f'stroke-width="{RING_W:g}"/>')
    vw, vh = COLS * CELL, ROWS * CELL
    return (f'<svg class="grid" viewBox="0 0 {vw} {vh}" '
            f'width="{vw}" height="{vh}" role="img" '
            f'aria-label="One hundred dots, one dot for each per cent">'
            + "".join(marks) + "</svg>"), fills


def key_row(data: dict, fills: dict) -> str:
    """Names the three colours and gives their shares — small, on one line
    each. This is support, not a second headline: no deltas here, and nothing
    at a size that could compete with the hero figure."""
    cells = []
    for key in ORDER:
        form, colour = fills[key]
        if form == "fill":
            swatch = ('<svg class="sw" viewBox="0 0 24 24" width="14" '
                      f'height="14"><circle cx="12" cy="12" r="11" '
                      f'fill="{colour}"/></svg>')
        else:
            swatch = ('<svg class="sw" viewBox="0 0 24 24" width="14" '
                      f'height="14"><circle cx="12" cy="12" r="9" fill="none" '
                      f'stroke="{colour}" stroke-width="4"/></svg>')
        cells.append(
            f'<p class="k">{swatch}<span class="k-name">{LABELS[key]}</span>'
            f'<span class="k-val">{fmt_pct(data["july"][key])}</span></p>')
    return '<div class="keys">' + "".join(cells) + "</div>"


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
def build_html(data: dict) -> str:
    dots, adjusted = allocate(data["july"])
    figure, hero_label, change = derive_hero(data)
    hero_fig = hero_markup(figure)
    svg, fills = grid_svg(dots, data["accent"])
    keys = key_row(data, fills)
    faces, stack = font_css()

    logo = (HERE.parents[1] / "plugins/editorial-motion/skills/"
            "editorial-explainer/assets/logo-nourl.png")
    logo_b64 = base64.b64encode(logo.read_bytes()).decode()

    note = (" Percentages are rounded, so the dots are allocated to the "
            "nearest whole point." if adjusted else "")
    warning = ('<p class="placeholder">Placeholder figures — not '
               'Essential Report results</p>') if data["placeholder"] else ""

    # Grain at 5%. Above ~10% it stops reading as texture and starts reading as
    # a broken image, and it turns to mud at thumbnail size either way.
    grain = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'"
             "%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' "
             "baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect "
             "width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")

    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="editorial-motion" content="1.10.0">
<title>{LABELS[data['accent']]} — Essential Report, {data['month']}</title>
<!-- check-artifact-ignore: homogenise-imagery
     The only raster asset is the Essential wordmark. .an-homogenise greyscales
     what it wraps, which would strip the brand dot out of the logo; the rule
     is aimed at mismatched photography, and there is none here. -->
<style>
{faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px}}
body{{
  background:{FIELD};
  color:{INK};
  font-family:{stack};
  font-weight:400;
  -webkit-font-smoothing:antialiased;
  display:flex;flex-direction:column;
  padding:84px 84px 72px;
  position:relative;overflow:hidden;
}}
/* Texture, not decoration. One layer. */
body::after{{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:99;
  opacity:.05;mix-blend-mode:overlay;background-image:{grain};
}}

/* Every block but the plot is flex:none. Without it they share the shrink when
   copy runs long, and the source line silently loses its last row — which is
   the one carrying the sample size. The plot absorbs it all instead. */
.hero,.hero-label,.change,.keys,.foot{{flex:none}}

/* The hero carries the accent because it and the accent dots state the same
   fact. At this size it clears the 3:1 large-text floor (measured 3.27:1);
   nothing smaller may be set in it — see the palette note above. */
.hero{{
  font-weight:700;font-size:280px;line-height:.84;letter-spacing:-.035em;
  color:{ACCENT};
}}
.unit{{font-size:.5em;letter-spacing:-.01em}}
.hero-label{{
  margin-top:30px;font-weight:400;font-size:46px;line-height:1.14;
  letter-spacing:-.01em;max-width:19ch;
}}
/* Archivo renders a period as a hard square; the brand full stop is round. */
.dot-mark{{display:inline-block;width:.22em;height:.22em;border-radius:50%;
  background:{ACCENT};margin-left:.07em;vertical-align:baseline}}

/* One movement line, not three delta chips. */
.change{{
  margin-top:26px;font-weight:300;font-size:27px;line-height:1.3;
  color:{MUTED};max-width:30ch;
}}

/* flex-basis auto, not 0 — a basis of 0 gives the plot no shrink weight, so
   the browser takes the overflow out of the copy blocks instead. min-height:0
   lets it shrink past the SVG's intrinsic size when the headline runs long. */
/* The band sits with its key rather than centred in the leftover space: the
   slack collects in one break between the statement and the evidence instead
   of splitting into two gaps that leave the marks floating. */
.plot{{flex:1 1 auto;min-height:0;display:flex;align-items:flex-end;
  justify-content:flex-start;padding:40px 0 34px}}
.grid{{width:100%;height:auto;max-height:100%}}

.keys{{display:flex;gap:30px;margin-top:22px}}
.k{{flex:1;display:flex;align-items:center;gap:10px;font-size:20px;
  line-height:1.2;color:{INK}}}
.sw{{flex:none}}
.k-name{{color:{MUTED}}}
.k-val{{font-weight:700;letter-spacing:-.01em}}

.foot{{margin-top:46px;display:flex;align-items:flex-end;
  justify-content:space-between;gap:40px}}
.src{{font-size:16px;line-height:1.42;color:{MUTED};max-width:44ch}}
.src .q{{display:block;margin-bottom:7px}}
.logo{{width:186px;height:auto;flex:none;mix-blend-mode:multiply;
  opacity:.94}}
.placeholder{{position:absolute;top:0;left:0;right:0;padding:9px 0;
  text-align:center;font-size:17px;font-weight:700;letter-spacing:.04em;
  color:#FFF1EC;background:{ACCENT}}}
</style>
</head>
<body>
{warning}
<p class="hero">{hero_fig}</p>
<h1 class="hero-label">{hero_label}<span class="dot-mark"></span></h1>
<p class="change">{change}</p>

<div class="plot">{svg}</div>

{keys}

<div class="foot">
  <p class="src">
    <span class="q">Q. {data['question']}</span>
    Essential Report, {data['fieldwork']}. Base: {data['base']}.
    Each dot is one per cent.{note}
  </p>
  <img class="logo" alt="Essential"
       src="data:image/png;base64,{logo_b64}">
</div>
</body>
</html>
"""


def find_chrome() -> tuple[str, bool] | tuple[None, None]:
    """Prefer the headless shell.

    Measured on this canvas: `chrome --headless` and `--headless=new` both
    rasterise only the first ~1263px of a 1350px window and leave everything
    below it unpainted, while still writing a full-height PNG. The page
    background fills the gap, so the result looks finished and is quietly
    missing the last line of the source block — the line carrying the sample
    size. The headless shell paints the full height. Verify any change here by
    pixel, not by eye.
    """
    shell = list(Path("/opt/pw-browsers").glob(
        "chromium_headless_shell-*/chrome-linux/headless_shell"))
    if shell:
        return str(sorted(shell)[-1]), True
    full = list(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))
    for path in [str(sorted(full)[-1]) if full else None,
                 shutil.which("chromium"), shutil.which("chromium-browser"),
                 shutil.which("google-chrome")]:
        if path and Path(path).exists():
            return path, False
    return None, None


def render_png(html_path: Path, png_path: Path) -> bool:
    chrome, is_shell = find_chrome()
    if not chrome:
        print("  no Chromium found; skipping PNG", file=sys.stderr)
        return False
    cmd = [chrome]
    if not is_shell:
        cmd.append("--headless")
        print("  warning: headless shell not found — check the bottom of the "
              "PNG for unpainted rows", file=sys.stderr)
    cmd += ["--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={W},{H}",
            f"--screenshot={png_path}", "--virtual-time-budget=4000",
            html_path.as_uri()]
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png_path.exists()


def verify_png(png_path: Path) -> None:
    """Cheap guards against the two failures that survive a glance: a bottom
    band that never got painted, and copy that ran past the canvas."""
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png_path).convert("RGB")
    if im.size != (W, H):
        print(f"  PNG is {im.size}, expected {(W, H)}", file=sys.stderr)
    px = im.load()
    ink = [y for y in range(H) if any(sum(px[x, y]) / 3 < 150
                                     for x in range(0, W, 3))]
    if not ink:
        raise SystemExit("  nothing rendered")
    bottom_gap = H - ink[-1]
    print(f"  last ink row {ink[-1]}, {bottom_gap}px of clear bottom margin")
    if bottom_gap < 24:
        print("  copy is running to the canvas edge — check for a clipped "
              "source line", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--out", default="tile")
    args = ap.parse_args()

    dots, adjusted = allocate(DATA["july"])
    html_path = HERE / f"{args.out}.html"
    html_path.write_text(build_html(DATA), encoding="utf-8")
    print(f"  {html_path.name}  {html_path.stat().st_size/1024:.0f} KB")
    print(f"  dots: {json.dumps(dots)}  sum={sum(dots.values())}"
          f"{'  (rounding reconciled)' if adjusted else ''}")

    if not args.no_png:
        png_path = HERE / f"{args.out}.png"
        if render_png(html_path, png_path):
            print(f"  {png_path.name}  {png_path.stat().st_size/1024:.0f} KB")
            verify_png(png_path)
    if DATA["placeholder"]:
        print("\n  PLACEHOLDER FIGURES ARE STILL IN DATA — do not publish.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
