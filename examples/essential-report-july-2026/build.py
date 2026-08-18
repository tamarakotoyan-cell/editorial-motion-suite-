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
    #
    # The hero figure, the emphasis block and the leading mass of the dot
    # field all report this group, so every element pushes the same number.
    # The arrow no longer tracks it — see descent_arrow.
    "accent": "wrong",

    # What the hero figure IS — the one number the tile exists to deliver.
    #   "level"  the accent group's own share this month
    #   "gap"    how far the leading group sits clear of the other
    #   "change" the accent group's movement on June
    # Everything else is support, and is sized to look like support.
    "hero": "level",

    # Leave these as None to derive them from the numbers, or write them
    # yourself — the takeaway is editorial judgement, not arithmetic.
    "hero_label": None,   # what the figure counts, in the poll's own terms
    "takeaway": None,     # what it means, in plain terms — see derive_hero
    "change_line": None,  # how it moved

    # The words the emphasis block sits behind. Defaults to the accent group's
    # own name, so the highlighted phrase and the accent marks say the same
    # thing. Only ever a phrase, never the whole line.
    "highlight": None,
}

LABELS = {
    "right": "Right direction",
    "wrong": "Wrong direction",
    "unsure": "Unsure",
}
ORDER = ["right", "wrong", "unsure"]


def band_order(accent: str) -> list[str]:
    """Accent group first, then the other filled group, with unsure last as
    the residual. Leading with the accent puts the mass the tile is about at
    the top of the field, where reading starts."""
    rest = [k for k in ORDER if k not in (accent, "unsure")]
    return [accent] + rest + (["unsure"] if accent != "unsure" else [])

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
# A wide band rather than a square hundred: it runs the full text measure, so
# the marks, the copy and the key all share one left edge. It gets the full
# mid-canvas because the arrow sits beside the hero figure rather than below
# it — an earlier version paid for the arrow out of the band's height while
# 500 x 400px of canvas sat empty next to a three-glyph number.
COLS, ROWS = 10, 10
CELL = 45
DOT_R = 16.0
RING_R = 14.0
RING_W = 4.0

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


def emphasise(text: str, phrase: str | None) -> str:
    """Put the emphasis block behind the words that matter, and only those.

    The house device is a block of colour covering the key phrase, never the
    whole line — a full-width band is a highlighter pen, which reads as
    decoration. box-decoration-break keeps the block intact when the phrase
    wraps, or the second line loses its ground.
    """
    if not phrase or phrase not in text:
        return text
    head, _, tail = text.partition(phrase)
    return f'{head}<span class="hl">{phrase}</span>{tail}'


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


def derive_hero(data: dict) -> tuple[str, str, str, str]:
    """Four rungs, in descending weight: the figure, what it counts, what it
    means, and how it moved.

    An earlier draft set three values and three deltas at one size, and the
    result carried eight numbers of equal rank and no takeaway. Everything
    except the hero is deliberately demoted here; the other shares still
    appear, small, in the key beneath the marks.

    The third rung is the one that stops the tile being a number with no
    reading. "52% say wrong direction" is a poll result; "more Australians are
    feeling negative than positive about the country's future" is what it
    tells you, and it is the sentence a reader repeats. It is a gloss on the
    question rather than a second measurement, so it is derived only as far as
    which side leads — override `takeaway` whenever the month needs a
    different reading.
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
        change = (f"{data['month']}, {phrase(a_move)} points on June, "
                  f"with {LABELS[other].lower()} unchanged on "
                  f"{fmt_pct(july[other])}.")
    else:
        change = (f"{data['month']}, {phrase(a_move)} points on June, "
                  f"with {LABELS[other].lower()} {phrase(o_move)} to "
                  f"{fmt_pct(july[other])}.")

    # What the result means, rather than what it counts.
    if july["wrong"] > july["right"]:
        takeaway = ("More Australians are feeling negative than positive "
                    "about the country’s future.")
    elif july["right"] > july["wrong"]:
        takeaway = ("More Australians are feeling positive than negative "
                    "about the country’s future.")
    else:
        takeaway = "Australians are split on the country’s future."

    return (figure,
            data["hero_label"] or label,
            data["takeaway"] or takeaway,
            data["change_line"] or change)


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
    for key in band_order(accent_key):
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


def descent_arrow(box_w: float = 340.0, box_h: float = 400.0) -> str:
    """A descending arrow — an illustration of mood, not a plotted series.

    WARNING: this carries no data. An earlier version drew the real monthly
    readings and the arrow's shape was theirs; at the client's direction it is
    now a designed shape that always points down, standing for "the future is
    going down the drain" rather than for any measured decline.

    Two things keep that from becoming a lie, and both matter if this is ever
    edited:

    * **No labels, no endpoints, no axis.** Nothing here can be read off. An
      unlabelled arrow states a mood; the moment a value is attached to either
      end it becomes a chart, and this chart would be wrong — the accent group
      is rising, not falling.
    * **It sits in the right-hand column with the interpretive line, not
      beside the hero figure.** Hard against the number it would assert that
      the number is falling, which is the opposite of true.

    To make the arrow mean something again, restore the data-driven version
    from git history rather than adding labels to this one.
    """
    # Normalised waypoints: a stepped decline, each recovery smaller than the
    # fall before it. Fixed by hand rather than randomised, so the shape is
    # identical across rebuilds.
    shape = [(0.00, 0.05), (0.17, 0.21), (0.30, 0.12), (0.45, 0.38),
             (0.57, 0.28), (0.72, 0.58), (0.83, 0.49), (1.00, 0.88)]
    STROKE, HEAD_L, HEAD_W = 26.0, 60.0, 41.0

    pts = [(x * box_w, y * box_h) for x, y in shape]
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** .5 or 1.0
    ux, uy = dx / length, dy / length
    tip = (x1 + ux * HEAD_L, y1 + uy * HEAD_L)
    base = (tip[0] - ux * HEAD_L, tip[1] - uy * HEAD_L)
    px_, py_ = -uy, ux
    wing_a = (base[0] + px_ * HEAD_W, base[1] + py_ * HEAD_W)
    wing_b = (base[0] - px_ * HEAD_W, base[1] - py_ * HEAD_W)

    line = pts[:-1] + [(base[0] + ux * 2, base[1] + uy * 2)]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in line)
    head = (f"{tip[0]:.1f},{tip[1]:.1f} {wing_a[0]:.1f},{wing_a[1]:.1f} "
            f"{wing_b[0]:.1f},{wing_b[1]:.1f}")

    # viewBox from what is actually drawn, so the head cannot clip.
    xs = [x for x, _ in line] + [tip[0], wing_a[0], wing_b[0]]
    ys = [y for _, y in line] + [tip[1], wing_a[1], wing_b[1]]
    pad = STROKE / 2 + 2
    vx, vy = min(xs) - pad, min(ys) - pad
    vw, vh = max(xs) - vx + pad, max(ys) - vy + pad

    return (
        f'<svg class="arrow-mark" viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" '
        f'role="img" aria-hidden="true">'
        f'<polyline points="{path}" fill="none" stroke="{ACCENT}" '
        f'stroke-width="{STROKE:g}" stroke-linejoin="miter" '
        f'stroke-linecap="butt"/>'
        f'<polygon points="{head}" fill="{ACCENT}"/></svg>')


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
    figure, hero_label, takeaway, change = derive_hero(data)
    hero_fig = hero_markup(figure)
    phrase = data["highlight"] or LABELS[data["accent"]].lower()
    hero_label = emphasise(hero_label, phrase)
    svg, fills = grid_svg(dots, data["accent"])
    keys = key_row(data, fills)
    arrow = descent_arrow()
    faces, stack = font_css()

    logo = (HERE.parents[1] / "plugins/editorial-motion/skills/"
            "editorial-explainer/assets/logo-nourl.png")
    logo_b64 = base64.b64encode(logo.read_bytes()).decode()

    # Two texture layers doing different jobs: laid paper for structure at
    # large scale, fine grain so the surface is not flat at small scale.
    # Generated by analog-surface/assets/make-paper.py, seamlessly tiling.
    paper = CACHE / "paper-overlay.png"
    paper_b64 = base64.b64encode(paper.read_bytes()).decode() if paper.exists() else ""

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

/* ---- layout-composition: the grid is chosen before anything is placed ----
   Canvas 4:5 (1080x1350) — Instagram feed at maximum height, per the format
   table. Grid: 12-column modular for alignment, rule of thirds for the focal
   point. Base unit 8px, which is also the brand's spacing rhythm; every gap
   below derives from it rather than being picked individually.

   Two rails, not one. An earlier version ran the figure, the label, the
   reading, the marks and the source all off the same left margin — five
   elements on one line, which reads as a list rather than a composition.
   Now the left column carries the evidence (figure, label, marks) and the
   right column carries the reading (arrow, interpretation, key). --------- */
:root{{
  --u: 8px;
  --gap: calc(var(--u) * 3);            /* 24 — column gutter        */
  --row: calc(var(--u) * 4);            /* 32 — row rhythm           */
  --band: calc(var(--u) * 6);           /* 48 — major section break  */

  /* Perfect Fourth, 1.333, base 18. Display -> heading -> body as three
     distinct registers, which is what a campaign graphic wants. Every size
     on the tile is a step on this scale and nothing is picked freehand. */
  --f0: 18px;                           /* source line               */
  --f1: 24px;                           /* key entries               */
  --f2: 32px;                           /* the reading               */
  --f3: 43px;                           /* what the figure counts    */
  --f9: 319px;                          /* the figure                */
}}

html,body{{width:{W}px;height:{H}px}}
body{{
  background:{FIELD};
  color:{INK};
  font-family:{stack};
  font-weight:400;
  -webkit-font-smoothing:antialiased;
  padding:calc(var(--u) * 10) calc(var(--u) * 10.5) calc(var(--u) * 8);
  position:relative;overflow:hidden;

  display:grid;
  grid-template-columns:repeat(12, 1fr);
  column-gap:var(--gap);
  grid-template-rows:auto auto 1fr auto;
  align-content:start;
}}

/* Paper sits above the colour field and below every mark and letterform —
   over the top it would darken whichever glyphs a fibre happened to cross.
   Overlay blend, not multiply: the tile is greyscale centred on mid-grey, so
   multiplying it darkens the whole field by half and the paper reads as dirt. */
body::before{{
  content:"";position:absolute;inset:0;pointer-events:none;z-index:0;
  opacity:.13;mix-blend-mode:overlay;
  background-image:url(data:image/png;base64,{paper_b64});
  background-size:384px 384px;
}}
body>*{{position:relative;z-index:1}}
/* Grain over everything, fine scale. */
body::after{{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:99;
  opacity:.05;mix-blend-mode:overlay;background-image:{grain};
}}

/* ---- placement -------------------------------------------------------- */
/* The focal point sits on the upper-left third, not jammed into the corner
   and not centred by default. */
.hero      {{grid-column:1 / 9;  grid-row:1; align-self:start}}
.arrow     {{grid-column:9 / 13; grid-row:1 / 3; align-self:start;
             justify-self:end; padding-top:var(--row)}}
.hero-label{{grid-column:1 / 9;  grid-row:2; margin-top:var(--row)}}
.takeaway  {{grid-column:5 / 13; grid-row:3; margin-top:var(--band);
             align-self:start}}
.plot      {{grid-column:1 / 13; grid-row:4; margin-top:var(--band);
             display:flex;align-items:center;gap:calc(var(--gap) * 2)}}
.foot      {{grid-column:1 / 13; grid-row:5; margin-top:var(--band);
             display:flex;align-items:flex-end;
             justify-content:space-between;gap:var(--band)}}

/* ---- type ------------------------------------------------------------- */
.hero{{
  font-weight:700;font-size:var(--f9);line-height:.82;
  letter-spacing:-.035em;color:{ACCENT};
}}
.unit{{font-size:.5em;letter-spacing:-.01em}}

.hero-label{{
  font-weight:400;font-size:var(--f3);line-height:1.2;
  letter-spacing:-.01em;
}}
/* The emphasis block covers the words that matter and no more — a full-width
   band is a highlighter pen. clone keeps it whole when the phrase wraps. */
.hl{{
  background:{ACCENT};color:#FDFAF3;
  padding:.06em .14em .1em;margin:0 -.02em;
  -webkit-box-decoration-break:clone;box-decoration-break:clone;
}}
/* Archivo renders a period as a hard square; the brand full stop is round. */
.dot-mark{{display:inline-block;width:.22em;height:.22em;border-radius:50%;
  background:{ACCENT};margin-left:.16em;vertical-align:baseline}}

.takeaway{{font-weight:400;font-size:var(--f2);line-height:1.28}}

.arrow-mark{{display:block;width:100%;height:auto;max-height:100%}}

/* ---- marks ------------------------------------------------------------ */
.grid{{flex:none;height:auto;width:52%}}
.keys{{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;
  gap:var(--band)}}
.k{{display:flex;align-items:center;gap:calc(var(--u) * 1.5);
  font-size:var(--f1);line-height:1.2;color:{INK}}}
.sw{{flex:none}}
.k-name{{color:{MUTED}}}
.k-val{{font-weight:700;letter-spacing:-.01em}}

/* ---- attribution ------------------------------------------------------ */
.src{{font-size:var(--f0);line-height:1.4;color:{MUTED};max-width:42ch}}
.src .q{{display:block;margin-bottom:calc(var(--u) * .875)}}
.logo{{width:196px;height:auto;flex:none;mix-blend-mode:multiply;opacity:.94}}
.placeholder{{position:absolute;top:0;left:0;right:0;padding:9px 0;
  text-align:center;font-size:17px;font-weight:700;letter-spacing:.04em;
  color:#FFF1EC;background:{ACCENT}}}
</style>
</head>
<body>
{warning}
<p class="hero">{hero_fig}</p>
<div class="arrow">{arrow}</div>
<h1 class="hero-label">{hero_label}<span class="dot-mark"></span></h1>
<p class="takeaway">{takeaway}</p>

<div class="plot">{svg}{keys}</div>

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
