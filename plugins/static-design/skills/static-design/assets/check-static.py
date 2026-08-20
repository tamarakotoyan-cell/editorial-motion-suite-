#!/usr/bin/env python3
"""Check a static design artifact against the mechanically checkable house rules.

Prose rules get skipped under load. A check that fails loudly does not. This
covers the subset of the static-design rules that can be verified from the
artifact alone. It does NOT judge design — it cannot tell you the composition is
weak or the finding is dull. It catches the specific, repeated, mechanical
failures the rejected reference set names, keyed to the A–M codes in
references/house-rules-static.md.

Two tiers, and the second one is the point
------------------------------------------
The three rules that most reliably separate good static work from rejected —
canvas occupancy, contrast, and template sameness across a carousel — cannot be
measured by reading HTML source. A div's share of the frame depends on layout;
a label's contrast depends on which ancestor's background actually shows
through; two frames having the same shape is a fact about geometry. So:

- **static tier** runs on the source text with no dependency, and catches
  containers, typeface soup, decorative gradients, the overline, the stamp.
- **rendered tier** drives headless Chrome and measures what the page actually
  produces.

Without Chrome the rendered tier is skipped and every skipped check is reported
by name. A linter that silently passes work it did not measure is worse than no
linter, because it is believed.

Usage
-----
    python3 check-static.py artifact.html
    python3 check-static.py --set out/            # a carousel: adds check H
    python3 check-static.py *.html --strict       # warnings also fail
    python3 check-static.py --self-test           # prove the checks still fire
    python3 check-static.py a.html --no-render    # static tier only, on purpose

Exit codes: 0 clean, 1 errors found (or warnings under --strict), 2 bad usage.
"""

import argparse
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN_JSON = HERE.parents[2] / ".claude-plugin" / "plugin.json"

# --- thresholds, all from the principle files -----------------------------
OCCUPANCY_FLOOR = 0.60      # 01-layout: content covers >=60% of the canvas
RADIUS_CEILING = 10         # 01-layout: no radius above 10px
MAX_FAMILIES = 2            # 02-typography
MAX_REGISTERS = 3           # 02-typography
MIN_TEXT_RATIO = 0.0125     # 02-typography: no text below 1.25% of canvas height
                            # 17px on 1350. Was 1.6% (22px), which sat above the
                            # 12-17px every reference caption uses and collapsed
                            # three type registers into two.
CAP_RATIO = 0.70            # cap-height as a fraction of font-size, approx
# 02-typography: 8-12% applies where type IS the picture. On a frame carrying a
# chart, image or mark field, the picture is the picture and the headline sits
# lower — Guardian's chart headlines measure about 3.5% of canvas height. A
# single band would fail their own reference set.
HEADLINE_CAP_MIN = 0.08     # type-led frames
HEADLINE_CAP_MAX = 0.12
PICTURE_CAP_MIN = 0.038     # frames where a picture carries the canvas
PICTURE_SHARE = 0.25        # a picture is one covering >=25% of the canvas
CONTRAST_FLOOR = 4.5        # 03-colour: text vs its field
# WCAG's own large-text threshold: 18pt (24px) bold or 14pt (18.66px)… in
# practice 24px bold / 30px regular and above take a 3:1 floor rather than 4.5.
# Applying 4.5 to a 100px headline is stricter than the standard and would
# reject accent-coloured display type that is genuinely legible.
LARGE_TEXT_FLOOR = 3.0
LARGE_BOLD_PX = 24.0
LARGE_REGULAR_PX = 30.0
DELTA_L_FLOOR = 25.0        # 03-colour: mark vs mark, mark vs field
MARK_MAX_SHARE = 0.15       # above this it is a field, not a mark
SAFE_INSET = 0.111          # 150px on 1350: the profile-grid crop plus the dots
MAX_CHROME = 1              # 05-series: one persistent brand element per frame
# 07-focal-point
CHROMA_ISOLATION = 1.6      # top chroma must clear the runner-up by this factor
CHROMA_MIN = 25             # below this (0-255 max-min) nothing is saturated
MIN_COLOURED = 4            # fewer coloured elements than this and U does not run
TYPE_ZONE_TYPE_LED = 0.28   # union of text boxes / usable canvas
TYPE_ZONE_PICTURE_LED = 0.18
GRAIN_MIN, GRAIN_MAX = 0.04, 0.06
# 04-graphics-imagery routing / 06-V the pinboard. A photographic element is an
# <img>, <picture>, <video>, <canvas>, an SVG <image>, or a raster background.
# A: exactly one. C: one subject plus at most one treated mass. B: roughly ten.
# The band between is the pinboard — photographs arranged politely on a field.
PINBOARD_MIN = 3            # from here up it is neither A nor C...
COLLAGE_MIN = 8             # ...and below here it is not B either
PHOTO_MIN_SHARE = 0.005     # a raster background smaller than this is a texture tile

SEMVER = re.compile(r"\d+\.\d+\.\d+")
STAMP = re.compile(r'<meta\s+name=["\']static-design["\']\s+content=["\']([^"\']+)["\']', re.I)

WHITE_BG = re.compile(r"background(?:-color)?\s*:\s*(?:#fff(?:fff)?\b|white\b|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))", re.I)
BLACK_BG = re.compile(r"background(?:-color)?\s*:\s*(?:#000(?:000)?\b|black\b|rgb\(\s*0\s*,\s*0\s*,\s*0\s*\))", re.I)
RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)", re.I)
SHADOW = re.compile(r"box-shadow\s*:\s*(?!none)([^;}]+)", re.I)
# `inset 0 0 0 1px <colour>` is a hairline, not a shadow: no blur, no offset, no
# depth, and it is what 03-colour prescribes to rescue a mark that cannot clear
# ΔL 25 against the accent. Banning every box-shadow banned the fix as well as
# the failure. A drop shadow has offset or blur; a hairline has neither.
# Authored: `inset 0 0 0 1px #EDE9E2`.  Computed: `rgb(237,233,226) 0px 0px 0px 1px inset`.
# Parse lengths rather than pattern-matching the whole layer, because the colour
# comes first in one form and last in the other, and it contains digits.


def _is_hairline_shadow(value):
    """True when every layer is an inset hairline: no offset, no blur, <=2px spread.

    `inset 0 0 0 1px <colour>` is a hairline, not a shadow, and it is what
    03-colour prescribes to rescue a mark that cannot clear DL 25 against the
    accent. Banning every box-shadow banned the fix along with the failure.
    """
    if not (value or "").strip():
        return False
    for layer in re.split(r",(?![^(]*\))", value):
        if "inset" not in layer.lower():
            return False
        # Strip the colour before reading lengths: it comes first in the
        # computed form and last in the authored one, and rgb() is full of
        # digits. A bare `0` is a valid CSS length, so the unit is optional.
        bare = re.sub(r"\w+\([^)]*\)", " ", layer)
        bare = re.sub(r"#[0-9a-fA-F]{3,8}", " ", bare)
        bare = re.sub(r"\b(?:inset|[a-z]+)\b", " ", bare)
        toks = re.findall(r"-?\d*\.?\d+(?:px)?", bare)
        lens = []
        for t in toks:
            v = float(t[:-2]) if t.endswith("px") else float(t)
            if not t.endswith("px") and v != 0:
                return False          # a non-zero length in some other unit
            lens.append(v)
        if len(lens) not in (3, 4) or any(v != 0 for v in lens[:3]):
            return False
        if len(lens) == 4 and lens[3] > 2:
            return False
    return True
TEXT_SHADOW_GLOW = re.compile(r"text-shadow\s*:[^;}]*\b(\d+(?:\.\d+)?)px\s+(\d+(?:\.\d+)?)px\s+(\d{2,})px", re.I)
GRADIENT = re.compile(r"(linear-gradient|radial-gradient|conic-gradient)\s*\(", re.I)
TILE_SIZE = re.compile(r"background-size\s*:\s*([\d.]+)px", re.I)
# type-treatment's print-process and tactile classes. The taxonomy lives there;
# this linter only enforces the opt-in boundary.
PROCESS_CLASS = re.compile(
    r"\btt-(?:process|clean-print|halftone|stamp|bleed|photocopy|misregister|"
    r"pattern-fill|paper-label|tactile-surface|tactile-ink)\b")
FAMILY = re.compile(r"font-family\s*:\s*([^;}]+)", re.I)
TABULAR = re.compile(r"font-(?:variant-numeric|feature-settings)\s*:[^;}]*(?:tabular-nums|['\"]tnum['\"])", re.I)
GRAIN_OPACITY = re.compile(r"--(?:grain|tex)-strength\s*:\s*([\d.]+)", re.I)
PX_SIZE = re.compile(r"font-size\s*:\s*([\d.]+)px", re.I)

BANNED_TITLES = {"key insights", "data overview", "by the numbers",
                 "at a glance", "the breakdown"}

# Generic families are not a house choice and must not count toward the ceiling.
GENERIC_FAMILIES = {"sans-serif", "serif", "monospace", "system-ui", "cursive",
                    "fantasy", "ui-sans-serif", "ui-serif", "ui-monospace",
                    "-apple-system", "blinkmacsystemfont", "inherit", "initial"}

SERIF_HINTS = ("serif", "georgia", "times", "garamond", "cheltenham", "caslon",
               "baskerville", "playfair", "merriweather", "lora", "cormorant",
               "didot", "bodoni", "freight", "tiempos", "canela")


# --- findings --------------------------------------------------------------
class Report:
    def __init__(self):
        self.items = []      # (level, code, message)
        self.skipped = []

    def error(self, code, message):
        self.items.append(("ERROR", code, message))

    def warn(self, code, message):
        self.items.append(("WARN", code, message))

    def skip(self, name):
        self.skipped.append(name)

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]

    @property
    def warnings(self):
        return [i for i in self.items if i[0] == "WARN"]

    def codes(self):
        return {c for _, c, _ in self.items}


# --- colour maths ----------------------------------------------------------
def _srgb_to_linear(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (_srgb_to_linear(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    a, b = relative_luminance(fg), relative_luminance(bg)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def lstar(rgb):
    """CIE L*, which is what ΔL is measured in — not sRGB luminance.

    ΔL and contrast ratio answer different questions and a palette can pass one
    while failing the other. ΔL says two marks are separable; contrast ratio
    says text can be read. Both are run.
    """
    y = relative_luminance(rgb)
    return 116 * (y ** (1 / 3)) - 16 if y > 0.008856 else 903.3 * y


def parse_rgb(value):
    """Parse a computed colour string. Returns None for transparent."""
    if not value:
        return None
    m = re.match(r"rgba?\(([^)]+)\)", value.strip(), re.I)
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).replace("/", " ").split(",")]
    if len(parts) == 1:
        parts = m.group(1).split()
    try:
        nums = [float(p.rstrip("%")) for p in parts[:4]]
    except ValueError:
        return None
    if len(nums) >= 4 and nums[3] == 0:
        return None
    return tuple(int(round(n)) for n in nums[:3])


# --- static tier -----------------------------------------------------------
class Doc(HTMLParser):
    """Flat, ordered element list. Ancestry tracked rather than guessed.

    check-artifact.py takes the same approach for the same reason: a regex over
    source cannot answer "is this element inside that wrapper", and the overline
    and chrome checks are both questions about position in the tree.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []          # dicts: tag, attrs, depth, text, order
        self._stack = []
        self._order = 0

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "depth": len(self._stack),
                "text": "", "order": self._order, "parent": self._stack[-1] if self._stack else None}
        self._order += 1
        self.nodes.append(node)
        if tag not in ("br", "img", "meta", "link", "hr", "input", "source"):
            self._stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["tag"] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        # Style and script contents are not visible text. Counting them made the
        # mid-dot check fire on a CSS comment documenting a type scale
        # ("24 · 32 · 43 · 57"), which is exactly the kind of false positive that
        # teaches people to ignore a linter.
        if any(n["tag"] in ("style", "script") for n in self._stack):
            return
        if self._stack and data.strip():
            self._stack[-1]["text"] += data


def _selector_before(text, pos, window=240):
    """The selector for the rule block opening at `pos`.

    Sliced, not matched. A leading `([^{}]*)` in the block pattern turns the
    scan quadratic on a file carrying megabytes of base64, which is how this
    linter came to hang on two artifacts in one session.
    """
    head = text[max(0, pos - window):pos]
    return head.rsplit("}", 1)[-1].rsplit(";", 1)[-1].strip()


def static_checks(path, text, report, expected_version):
    doc = Doc()
    doc.feed(text)

    # --- provenance
    m = STAMP.search(text)
    if not m:
        report.error("stamp", 'missing <meta name="static-design" content="X.Y.Z">')
    elif not SEMVER.fullmatch(m.group(1).strip()):
        report.error("stamp", f'malformed version stamp: {m.group(1)!r}')
    elif expected_version and m.group(1).strip() != expected_version:
        report.warn("stamp", f'stale stamp {m.group(1)} (plugin is {expected_version})')

    # --- A: containers
    for raw in RADIUS.findall(text):
        for px in re.findall(r"([\d.]+)px", raw):
            if float(px) > RADIUS_CEILING:
                report.error("A", f"border-radius {px}px exceeds the {RADIUS_CEILING}px "
                                  "ceiling — rounded cards are the loudest tell")
                break
    if any(not _is_hairline_shadow(m) for m in SHADOW.findall(text)):
        report.error("A", "box-shadow present — depth comes from overlap and scale, "
                          "never from shadows")
    for x, y, blur in TEXT_SHADOW_GLOW.findall(text):
        report.error("A", f"text-shadow with {blur}px blur reads as a glow; the only "
                          "permitted text-shadow is the sub-pixel print fringe")

    # --- ground
    body_style = "\n".join(re.findall(r"(?:body|html|\.frame|\.slide|\.canvas)\s*\{([^}]*)\}",
                                      text, re.I))
    if WHITE_BG.search(body_style):
        report.error("ground", "pure white page field — the ground is always tinted")
    if BLACK_BG.search(body_style):
        report.error("ground", "pure black page field — use #1A1A1A or above")

    # --- D: typeface soup
    families = set()
    for decl in FAMILY.findall(text):
        first = decl.split(",")[0].strip().strip("'\"").lower()
        if first and first not in GENERIC_FAMILIES and not first.startswith("var("):
            families.add(first)
    if len(families) > MAX_FAMILIES:
        report.error("D", f"{len(families)} type families ({', '.join(sorted(families))}) "
                          f"— the ceiling is {MAX_FAMILIES}")

    # --- F: decoration standing in for meaning
    #
    # Checked per rule block, not per line, because the two legitimate uses are
    # both identified by a sibling declaration: a type plate (marked `plate`),
    # and a print screen — a gradient tiled at a small background-size, which is
    # a halftone lattice rather than a wash. Texture is required by
    # 03-colour-and-ground; flagging it as decoration would ban the house style.
    for block in re.finditer(r"\{([^{}]*)\}", text):
        body = block.group(1)
        if not GRADIENT.search(body):
            continue
        # `plate` in the block, or in the selector that opens it: `.plate{…}`
        # is how the house tiles mark one, and only the body was being read.
        if "plate" in body.lower() or "plate" in _selector_before(text, block.start()).lower():
            continue
        tile = TILE_SIZE.search(body)
        if tile and float(tile.group(1)) <= 40:
            continue                      # a dot screen, not a background wash
        # A ground is four layers, and structure is one of them: folds, creases
        # and rules, directional and asymmetric. Those are drawn as narrow
        # linear-gradient bands and were being reported as decoration, which
        # banned the layer 03-colour-and-ground requires.
        #
        # Narrow deliberately. GROUND_ROLE is the right test for "is this the
        # surface" and the wrong one here: it matches `.frame`, and a radial
        # wash across `.frame` is the decoration this check exists to catch.
        # Structure is linear and it is named.
        selector = _selector_before(text, block.start())
        if (GROUND_STRUCTURE.search(selector)
                and "linear-gradient" in body.lower()
                and "radial-gradient" not in body.lower()
                and "conic-gradient" not in body.lower()):
            continue
        report.error("F", "decorative gradient \u2014 the only permitted gradients are a type "
                          "plate at a frame edge (mark it `plate`), a print screen "
                          "tiled under 40px, and ground structure on a ground-role "
                          "selector (crease, fold, tooth, paper, field)")
        break

    # --- F: a torn edge is never a polygon
    #
    # A tear is a cut photograph or a turbulence-displaced mask, one seed per
    # fragment. A vector path with a handful of vertices reads as Canva at any
    # size, and it was the failure mode in this system's own first attempt.
    for m in re.finditer(r"clip-path\s*:\s*polygon\(([^)]*)\)", text, re.I):
        if m.group(1).count(",") >= 4:
            report.error("F", "torn edge drawn as a clip-path polygon \u2014 tear with a "
                              "turbulence-displaced mask, or cut the photograph")
            break

    # --- F: padding never on a flex-grow mark
    #
    # With `flex-basis:0` the browser distributes free space by grow factor and
    # then adds each item's padding back, so every mark gains the same constant
    # and length / value stops being one number. Measured on a real chart, a 9%
    # category drew 32% too long. The inset belongs on a child.
    for block in re.finditer(r"\{([^{}]*)\}", text):
        body = block.group(1)
        grows = re.search(r"flex\s*:\s*[^;}]*\s0(?:px)?\s*(?:;|$)", body) or \
                re.search(r"flex-basis\s*:\s*0(?:px)?\s*(?:;|$)", body)
        if not grows:
            continue
        pad = re.search(r"(?<!-)\bpadding(?:-(?:left|right|inline[a-z-]*))?\s*:\s*([^;}]+)", body)
        if pad and not re.fullmatch(r"[\s0px]*", pad.group(1)):
            selector = _selector_before(text, block.start())
            report.error("F", f"padding on a flex-grow mark ({selector}) \u2014 basis-0 items "
                              "get their padding added back after distribution, so every "
                              "mark gains a constant and length / value is no longer "
                              "one number; put the inset on a child")
            break

    # --- banned titles
    for tag, inner in re.findall(r"<(h[1-6])\b[^>]*>(.*?)</\1\s*>", text, re.I | re.S):
        plain = re.sub(r"<[^>]+>", "", inner).strip().lower().rstrip(":.")
        if plain in BANNED_TITLES:
            report.error("F", f'banned title {plain!r} — the title is the finding, '
                              "not a section label")

    # --- D: serif or tabular-nums on a hero figure
    for node in doc.nodes:
        cls = node["attrs"].get("class", "").lower()
        if "hero" in cls or "figure" in cls or "stat" in cls:
            style = node["attrs"].get("style", "").lower()
            scoped = style + " " + _rules_for_class(text, cls)
            if any(h in scoped for h in SERIF_HINTS):
                report.error("D", "serif or display face on a hero figure — hero figures "
                                  "are set in the sans")
            if TABULAR.search(scoped):
                report.error("D", "tabular-nums on a hero figure — equal-width digits read "
                                  "loose at display size")

    # --- overline above a heading (D/F), with the serial running-head exception
    _check_overline(doc, report, text)

    # --- N: mid-dot metadata chains
    #
    # Ported from editorial-motion's check-artifact.py, same threshold and same
    # reasoning. Two mid-dots in one string is a chain; one is a separator and
    # is fine. Static frames are where these breed, because a footer feels like
    # somewhere to put things rather than something to design.
    for node in doc.nodes:
        body = " ".join(node["text"].split())
        if body.count("·") >= 2:
            report.error("N", f'mid-dot metadata chain "{body[:52]}" — use line breaks, '
                              "commas or plain labelled lines; a mid-dot ranks nothing")
            break

    # --- type-process misuse (02-typography's opt-in boundary)
    #
    # type-treatment owns the taxonomy; this only enforces the boundary, which
    # is the part that fails silently. A process class on a global selector
    # treats everything, and a treatment applied to everything is not a
    # treatment.
    # Anchored on the brace, selector sliced backwards. `([^{}]+)\{` can start
    # matching at any offset, so on a file carrying megabytes of base64 the
    # engine backtracks across the whole document for every candidate start —
    # this is what hung the linter on two artifacts in one session, and the
    # hang predates the checks that were blamed for it. Nothing is reported, and
    # the run reads as clean because it never finished.
    for _m in re.finditer(r"\{([^{}]*)\}", text):
        block = _m.group(1)
        selector = _selector_before(text, _m.start())
        sel = selector.strip().lower().split("/*")[0]
        if not PROCESS_CLASS.search(block) and not PROCESS_CLASS.search(sel):
            continue
        if re.search(r"(^|[,\s])(body|html|\*|:root)\b", sel):
            report.error("F", f"type-process class applied through a global selector "
                              f"({sel[:40].strip()}) — processes are per-string features, "
                              "never a property of the type system")
            break
    for node in doc.nodes:
        classes = (node["attrs"].get("class") or "")
        found = PROCESS_CLASS.findall(classes)
        # tt-process is the shared base class and pairs with exactly one process.
        named = [c for c in found if c not in ("tt-process",)]
        if len(named) > 1:
            report.error("F", f"{len(named)} print processes on one string "
                              f"({', '.join(named)}) — one dominant process per string")
            break

    # --- texture strength
    for value in GRAIN_OPACITY.findall(text):
        v = float(value)
        if not (GRAIN_MIN <= v <= GRAIN_MAX):
            report.warn("texture", f"grain strength {v} is outside {GRAIN_MIN}–{GRAIN_MAX}; "
                                   "above that it reads as a broken image")

    return doc


def _rules_for_class(text, class_attr):
    """CSS declarations for any of an element's classes. Approximate by design.

    A full cascade resolver is the rendered tier's job. This only has to be good
    enough to notice a serif declared on the hero figure's own rule.
    """
    out = []
    for cls in class_attr.split():
        for body in re.findall(r"\.%s\b[^{]*\{([^}]*)\}" % re.escape(cls), text, re.I):
            out.append(body)
    return " ".join(out).lower()


def _check_overline(doc, report, text):
    """A caps line directly above a heading is banned — unless it is serial.

    The distinction is mechanical, and stated that way in 02-typography: on one
    frame it is a kicker restating the headline; repeated verbatim across three
    or more consecutive frames it is a chapter marker and earns its place.
    """
    headings = {"h1", "h2", "h3"}
    candidates = []
    for i, node in enumerate(doc.nodes):
        if node["tag"] not in headings:
            continue
        for prev in reversed(doc.nodes[:i]):
            # Same parent only. Without this, the last element of one frame
            # reads as the overline of the next frame's heading, and a mark
            # parked in the footer gets reported as a kicker.
            if prev["parent"] is not node["parent"]:
                continue
            if prev["depth"] > node["depth"] or not prev["text"].strip():
                continue
            body = prev["text"].strip()
            if prev["tag"] in headings:
                break
            letters = [c for c in body if c.isalpha()]
            if letters and len(body) < 60 and all(c.isupper() for c in letters):
                candidates.append(body.rstrip("… .").upper())
            break

    if not candidates:
        return
    # Serial: the same text on three or more frames of this document.
    for body in set(candidates):
        if candidates.count(body) >= 3:
            continue
        report.error("D", f'capitalised overline {body[:40]!r} above a heading — it '
                          "restates the heading and pushes it down the canvas. Permitted "
                          "only as a running head repeated across 3+ consecutive frames")


# --- rendered tier ---------------------------------------------------------
PROBE = r"""
(() => {
  const frames = [...document.querySelectorAll('[data-frame], .frame, .slide')];
  const roots = frames.length ? frames : [document.body];
  // `from` lets a caller ask for the background *behind* an element rather than
  // its own. Text wants its own (a highlight chip is the field its words sit
  // on); a mark wants what is behind it, or every filled element would report
  // itself as its own field and separate from it by exactly zero.
  const effBg = (el, from) => {
    for (let n = from || el; n && n !== document.documentElement.parentNode; n = n.parentElement) {
      const c = getComputedStyle(n).backgroundColor;
      const m = c && c.match(/rgba?\(([^)]+)\)/);
      if (m) { const p = m[1].split(',').map(s => parseFloat(s)); if (p.length < 4 || p[3] > 0.15) return c; }
    }
    return getComputedStyle(document.body).backgroundColor || 'rgb(255,255,255)';
  };
  return roots.map((root, fi) => {
    const rr = root.getBoundingClientRect();
    const out = { index: fi, w: rr.width, h: rr.height, els: [] };
    for (const el of root.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      // Direct text only: a wrapper's textContent would credit its children's
      // colour to the wrapper and report contrast against the wrong field.
      let own = [...el.childNodes].filter(n => n.nodeType === 3)
                    .map(n => n.textContent.trim()).join(' ').trim();
      // aria-hidden text is a mark, not copy. 04-graphics-imagery's ghosted
      // artefact — a much larger, low-contrast copy of the hero behind the
      // composition — is set in type on the house tiles, and read as copy it
      // fails the safe-zone, register and contrast checks by construction.
      // Declared decorative, it is measured as a picture and skipped as text.
      const deco = !!el.closest('[aria-hidden="true"]');
      if (deco) own = '';
      const bgi = cs.backgroundImage && cs.backgroundImage !== 'none' ? cs.backgroundImage : '';
      out.els.push({
        tag: el.tagName.toLowerCase(),
        deco: deco,
        // a raster background: a photograph as CSS, or the linter's own
        // dimension-preserving placeholder for one (see _lighten)
        raster: /url\(["']?(?:data:image\/(?:png|jpe?g|webp|gif|avif)|[^)"']*\.(?:png|jpe?g|webp|gif|avif)\b)/i.test(bgi)
                || /data-raster=/.test(bgi),
        cls: el.className && el.className.baseVal !== undefined ? el.className.baseVal : (el.className || ''),
        x: r.left - rr.left, y: r.top - rr.top, w: r.width, h: r.height,
        text: own.slice(0, 80),
        kids: el.childElementCount,
        pcls: el.parentElement && el.parentElement.className
              && el.parentElement.className.baseVal !== undefined
                ? el.parentElement.className.baseVal
                : ((el.parentElement && el.parentElement.className) || ''),
        // direct children carrying their own opaque fill — what separates a
        // mark field from a wrapper with the same child count
        fills: [...el.children].filter(c => {
          const b = getComputedStyle(c).backgroundColor;
          return b && b !== 'transparent' && !/rgba\(.*,\s*0\)$/.test(b);
        }).length,
        size: parseFloat(cs.fontSize) || 0,
        weight: parseInt(cs.fontWeight, 10) || 400,
        inline: cs.display.startsWith('inline'),
        // getBoundingClientRect is post-transform, so a rotated element reports
        // a larger axis-aligned box than it occupies and two stacked lines on a
        // tilted band appear to collide. The offset chain is pre-transform, so
        // it gives the true layout box. Occupancy still uses the visual rect —
        // a rotated band really does cover that area — but collision and
        // overflow use this. Skipping rotated elements instead (the first fix
        // here) turned a false positive into a false negative and hid a real
        // three-line overflow on a tilted band.
        // offsetLeft/offsetWidth are HTMLElement APIs. An inline <svg>, and
        // everything inside one, has none of them — so w and h came back
        // undefined, JSON dropped the keys entirely, and the overflow check
        // below raised KeyError on the first artifact to carry a leader line.
        // Fall back to the visual rect there; SVG is not rotated by a CSS
        // transform anywhere in the house set, so the two agree.
        lay: (() => {
          if (typeof el.offsetWidth !== 'number' || typeof el.offsetHeight !== 'number')
            return { x: r.left - rr.left, y: r.top - rr.top, w: r.width, h: r.height };
          let x = 0, y = 0, n = el;
          while (n && n !== root && n.offsetParent) {
            x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent;
          }
          return { x: x, y: y, w: el.offsetWidth, h: el.offsetHeight };
        })(),
        family: (cs.fontFamily || '').split(',')[0].replace(/['"]/g, '').trim().toLowerCase(),
        color: cs.color, bg: effBg(el), behind: effBg(el, el.parentElement),
        ownBg: cs.backgroundColor,
        radius: Math.max(...['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius']
                  .map(k => parseFloat(cs[k]) || 0)),
        shadow: cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : '',
        bgImage: bgi
      });
    }
    return out;
  });
})()
"""


GROUND_STRUCTURE = re.compile(
    r"\b(crease|fold|tooth|grain|texture|tex|structure|scuff|bleed-through)\b", re.I)
GROUND_ROLE = re.compile(
    r"\b(canvas|frame|stage|sheet|ground|paper|field|tooth|grain|texture|tex|"
    r"crease|fold|noise|scrim|vignette|backdrop|bleed-through)\b", re.I)


def _is_ground(el, frame):
    """Is this element the surface, or something sitting on it?

    By role, not by area. The old test skipped anything covering more than 92%
    of the canvas, which threw away a full-bleed photograph — the element most
    likely to be carrying the whole frame — and scored a Structure A tile as
    near-empty. 04-graphics requires photo frames to be full-bleed, so the
    guard was failing the house style by construction.

    Own class only. Reading the parent's class would make every fragment
    inside `.canvas` read as ground.
    """
    if el["tag"] in ("img", "svg", "canvas", "picture", "video"):
        return False                      # a picture is never the ground
    if el["text"]:
        return False
    if GROUND_ROLE.search(el.get("cls") or ""):
        return True
    # An unclassed full-bleed wrapper with nothing of its own is still ground.
    w, h = frame["w"] or 1, frame["h"] or 1
    return el["w"] * el["h"] > 0.92 * w * h and not el.get("kids")


def text_zone(frame, grid=120):
    """Union of the text boxes, against the usable canvas.

    07-focal-point: the copy occupies a zone, not a corner. A frame can clear
    the 60% occupancy floor and still have no type zone, because pictures made
    up the difference — which is why this is measured separately rather than
    folded into B.
    """
    w, h = frame["w"], frame["h"]
    if w < 1 or h < 1:
        return 0.0
    cells = set()
    for el in frame["els"]:
        if not el["text"]:
            continue
        x0 = max(0, int(el["x"] / w * grid))
        x1 = min(grid, int((el["x"] + el["w"]) / w * grid) + 1)
        y0 = max(0, int(el["y"] / h * grid))
        y1 = min(grid, int((el["y"] + el["h"]) / h * grid) + 1)
        for gx in range(x0, x1):
            for gy in range(y0, y1):
                cells.add((gx, gy))
    band0 = int(SAFE_INSET * grid)
    band1 = grid - band0
    usable = grid * (band1 - band0)
    if usable < 1:
        return 0.0
    return sum(1 for gx, gy in cells if band0 <= gy < band1) / usable


def _chroma(rgb):
    """Distance from the neutral axis, 0-255. Cheap stand-in for C* in LCh."""
    return max(rgb) - min(rgb)


def occupancy(frame, grid=120):
    """Fraction of the canvas covered, by coarse rasterisation.

    A rectangle-union algorithm would be exact and is not worth it: the rule is
    a 60% floor, and a 120x120 grid resolves that to well under a percent.
    Ground-sized elements are excluded — the field covering the frame is not
    content, and counting it would pass every artifact.

    A cluster — a dot field, a waffle grid, a pictogram — is credited as its
    whole bounding box rather than as its individual marks. Rasterising 100 dots
    counts only the ink and scores a full-frame dot grid at about 40%, which
    would fail the house's own recommended device. The eye reads that field as
    one mass, so the linter does too.
    """
    w, h = frame["w"], frame["h"]
    if w < 1 or h < 1:
        return 0.0
    cells = set()
    for el in frame["els"]:
        if _is_ground(el, frame):
            continue                      # the surface, not something on it
        # An outlined mark is a mark. 03-colour prescribes fill-versus-stroke
        # as one of the resolutions when a fill cannot clear the DL floor, and
        # counting only fills made that resolution invisible here — a drawn
        # category scored zero and dragged the frame under the floor.
        if not (el["text"] or el["tag"] in ("img", "svg", "canvas", "picture", "video")
                or _is_hairline_shadow(el.get("shadow"))
                or el["ownBg"] not in ("", "rgba(0, 0, 0, 0)") or el["bgImage"]
                or el.get("kids", 0) >= 6):
            continue                      # a layout wrapper with nothing in it
        x0 = max(0, int(el["x"] / w * grid))
        x1 = min(grid, int((el["x"] + el["w"]) / w * grid) + 1)
        y0 = max(0, int(el["y"] / h * grid))
        y1 = min(grid, int((el["y"] + el["h"]) / h * grid) + 1)
        for gx in range(x0, x1):
            for gy in range(y0, y1):
                cells.add((gx, gy))

    # Against the *usable* canvas, not the total. With 150px safe zones top and
    # bottom, 11% of a 4:5 tile is a band nothing a reader needs may occupy, so
    # scoring against the full frame quietly asks for 77% of what is actually
    # available in order to report 60%. Cells in the safe band still count for
    # nothing here — bleed art is welcome to cross it, but it cannot be the
    # thing that fills the frame.
    band0 = int(SAFE_INSET * grid)
    band1 = grid - band0
    usable = grid * (band1 - band0)
    if usable < 1:
        return 0.0
    inside = sum(1 for gx, gy in cells if band0 <= gy < band1)
    return inside / usable


SAMENESS_FLOOR = 0.75       # 05-series: the blur test, as a similarity threshold


def frame_signature(frame, grid=16):
    """A frame's shape, independent of its words.

    This is the blur test from 05-series, done mechanically: normalise every
    element's box to a coarse grid. Two frames with near-identical box sets are
    the same frame with different text.

    Position and height only — not width. An auto-width element is as wide as
    its words, so including width would make "The Canopy" and "Top Ryde" look
    like different compositions when they are the same frame. Width is the one
    dimension the words are allowed to change.
    """
    w, h = frame["w"] or 1, frame["h"] or 1
    boxes = set()
    for el in frame["els"]:
        if not (el["text"] or el["tag"] in ("img", "svg", "canvas", "picture")):
            continue
        if el["w"] * el["h"] > 0.92 * w * h:
            continue
        boxes.add((round(el["x"] / w * grid), round(el["y"] / h * grid),
                   round(el["h"] / h * grid)))
    return frozenset(boxes)


def _box(el):
    """Layout box for collision and overflow, falling back to the visual rect.

    A malformed `lay` must degrade to the visual rect rather than raise: this
    check crashing is worse than it being approximate, because a traceback in a
    pre-ship linter reads as "the tool is broken" and the artifact ships anyway.
    """
    lay = el.get("lay")
    if isinstance(lay, dict) and all(k in lay for k in ("x", "y", "w", "h")):
        return lay
    return el


def sameness(a, b):
    """Jaccard overlap of two frame signatures. 1.0 is the identical frame."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def rendered_checks(frames, report, accent=None):
    for frame in frames:
        tag = f"frame {frame['index'] + 1}" if len(frames) > 1 else "frame"
        h = frame["h"] or 1
        els = frame["els"]
        texts = [e for e in els if e["text"] and e["size"] > 0]

        # --- fit: content running outside the frame
        #
        # A fixed canvas has no scrollbar to reveal what fell off the bottom, so
        # overflow is silent — it renders as a headline that stops mid-word. An
        # absolutely-positioned block whose text grew by one line is the usual
        # cause, and nothing else in this file would notice.
        for e in els:
            box = _box(e)
            over_b = (box["y"] + box["h"]) - frame["h"]
            over_r = (box["x"] + box["w"]) - frame["w"]
            if max(over_b, over_r) > 2 and (e["text"] or e.get("kids", 0) >= 6):
                edge = "bottom" if over_b >= over_r else "right"
                report.error("fit", f"{tag}: content runs {max(over_b, over_r):.0f}px "
                                    f"past the {edge} edge: {(e['text'] or 'a mark field')[:32]!r}")
                break

        # --- fit: text blocks colliding
        # Inline elements are excluded: an <em> inside an <h1> overlaps its own
        # parent by definition, and an inline box can spill a pixel or two past
        # the block's border box, so a containment test alone does not settle it.
        blocks = [e for e in texts
                  if e["w"] > 40 and e["h"] > 20 and not e.get("inline")]
        collided = False
        for i, a in enumerate(blocks):
            box_a = _box(a)
            for b in blocks[i + 1:]:
                box_b = _box(b)
                if _contains(box_a, box_b) or _contains(box_b, box_a):
                    continue          # nesting is not a collision
                ox = (min(box_a["x"] + box_a["w"], box_b["x"] + box_b["w"])
                      - max(box_a["x"], box_b["x"]))
                oy = (min(box_a["y"] + box_a["h"], box_b["y"] + box_b["h"])
                      - max(box_a["y"], box_b["y"]))
                if ox > 4 and oy > 4:
                    report.error("fit", f"{tag}: two text blocks overlap by "
                                        f"{ox:.0f}×{oy:.0f}px: {a['text'][:24]!r} and "
                                        f"{b['text'][:24]!r}")
                    collided = True
                    break
            if collided:
                break

        # --- S: safe zones
        #
        # Instagram crops a 4:5 post to a centre square in the profile grid, so
        # the top and bottom 135px of a 1350px canvas are cut; carousel dots
        # overlay the bottom ~60px in feed. Anything a reader needs — a time, an
        # address, a source line — has to survive both. Bleed art may cross it;
        # text may not.
        inset = h * SAFE_INSET
        for e in texts:
            if e["y"] < inset or (e["y"] + e["h"]) > h - inset:
                where = "top" if e["y"] < inset else "bottom"
                report.error("S", f"{tag}: text sits in the {where} {inset:.0f}px safe "
                                  f"zone and will be cropped in the profile grid: "
                                  f"{e['text'][:32]!r}")
                break

        # --- B: dead canvas
        cov = occupancy(frame)
        if cov < OCCUPANCY_FLOOR:
            report.error("B", f"{tag}: content covers {cov:.0%} of the canvas, floor is "
                              f"{OCCUPANCY_FLOOR:.0%} — make the type bigger, don't move it")

        # --- E: size floors and registers
        if texts:
            biggest = max(texts, key=lambda e: e["size"])
            cap = biggest["size"] * CAP_RATIO / h
            has_picture = _has_picture(frame)
            floor = PICTURE_CAP_MIN if has_picture else HEADLINE_CAP_MIN
            if cap < floor:
                kind = "a picture-led" if has_picture else "a type-led"
                report.error("E", f"{tag}: largest type has a cap-height of {cap:.1%} of "
                                  f"canvas height; floor on {kind} frame is {floor:.1%}")
            elif cap > HEADLINE_CAP_MAX and not has_picture and not _is_hero_figure(biggest):
                # The 8–12% band in 02-typography is about headlines. A stat
                # tile's hero figure is meant to be bigger than a headline, so
                # only the floor applies to it.
                report.warn("E", f"{tag}: headline cap-height is {cap:.1%}, above the "
                                 f"{HEADLINE_CAP_MAX:.0%} guide")
            for e in texts:
                if e["size"] / h < MIN_TEXT_RATIO:
                    report.error("E", f"{tag}: text at {e['size']:.0f}px is "
                                      f"{e['size']/h:.2%} of canvas height (floor "
                                      f"{MIN_TEXT_RATIO:.2%}): {e['text'][:32]!r}")
                    break
            # A bare unit set at half the digit size is part of the hero
            # figure, not a register of its own — it is how "28%" is kept inside
            # a narrow block.
            units = {"%", "pp", "pt", "pts", "p", "$", "\u00b0"}
            sizes = sorted({round(e["size"]) for e in texts
                            if e["text"].strip() not in units}, reverse=True)
            registers = _registers(sizes, hero=_is_hero_figure(biggest))
            if len(registers) > MAX_REGISTERS:
                shown = " / ".join("+".join(str(s) for s in g) for g in registers)
                report.error("E", f"{tag}: {len(registers)} type registers "
                                  f"({shown}) \u2014 the ceiling is {MAX_REGISTERS}")

        # --- D: families as actually resolved
        fams = {e["family"] for e in texts
                if e["family"] and e["family"] not in GENERIC_FAMILIES}
        if len(fams) > MAX_FAMILIES:
            report.error("D", f"{tag}: {len(fams)} resolved type families "
                              f"({', '.join(sorted(fams))})")

        # --- I: contrast, smallest text first
        for e in sorted(texts, key=lambda e: e["size"]):
            fg, bg = parse_rgb(e["color"]), parse_rgb(e["bg"])
            if not fg or not bg:
                continue
            ratio = contrast_ratio(fg, bg)
            bold = (e.get("weight") or 400) >= 700
            large = e["size"] >= (LARGE_BOLD_PX if bold else LARGE_REGULAR_PX)
            floor = LARGE_TEXT_FLOOR if large else CONTRAST_FLOOR
            if ratio < floor:
                report.error("I", f"{tag}: text at {ratio:.2f}:1 against its field "
                                  f"(floor {floor}:1 at {e['size']:.0f}px"
                                  f"{' bold' if bold else ''}): {e['text'][:32]!r} — "
                                  "invisible on a phone, faintly readable on the display "
                                  "where it gets signed off")

        # --- I: marks separable from what is behind them
        #
        # Capped at 15% of the canvas. A tonal field is a deliberate, subtle
        # shift in the ground and is not a data mark; checking it against the
        # ground it sits on would report every field in the house style as a
        # failure.
        for e in els:
            if e["text"] or (e["w"] * e["h"]) / (frame["w"] * h) > MARK_MAX_SHARE:
                continue
            mc, behind = parse_rgb(e["ownBg"]), parse_rgb(e.get("behind"))
            if not mc or not behind:
                continue
            gap = abs(lstar(mc) - lstar(behind))
            if gap < DELTA_L_FLOOR:
                report.warn("I", f"{tag}: a mark sits ΔL {gap:.0f} from the field "
                                 f"(floor {DELTA_L_FLOOR:.0f}) — it will evaporate at 200px")
                break

        # --- A: containers, as rendered
        for e in els:
            if e["radius"] <= RADIUS_CEILING or e["ownBg"] in ("", "rgba(0, 0, 0, 0)"):
                continue
            # A circle or a pill is a mark, not a rounded card. `border-radius:50%`
            # on a dot in a waffle field resolves to half its width, and the
            # house's own recommended device would otherwise fail check A.
            if e["radius"] * 2 >= min(e["w"], e["h"]) - 1:
                continue
            report.error("A", f"{tag}: element with {e['radius']:.0f}px radius and a "
                              "fill is a card — put it on the ground")
            break
        if any(e["shadow"] and not _is_hairline_shadow(e["shadow"]) for e in els):
            report.error("A", f"{tag}: box-shadow present")

        # --- G: accent inflation
        if accent:
            target = parse_rgb(accent) or _hex_to_rgb(accent)
            if target:
                # A mark and its own sub-segments are one element class. The
                # accent rule exists to stop a *second thing* taking the accent;
                # a bar and the strip that splits that same bar are one thing.
                #
                # Containment alone does not settle it — the split may be drawn
                # in a separate row, outside the block it decomposes. Tie them
                # by category token instead: `.seg` inside `.grp.g-oppose` and
                # the block `.grp.g-oppose` share `g-oppose`, and two genuinely
                # different uses of the accent share nothing.
                GENERIC = {"", "grp", "seg", "row", "bar", "col", "cell",
                           "item", "block", "mark", "fill", "wrap", "inner"}

                def _tokens(e):
                    own = set((e.get("cls") or "").split())
                    par = set((e.get("pcls") or "").split())
                    return (own | par) - GENERIC

                accented = []
                for e in els:
                    if _is_brand_furniture(e, frame):
                        continue
                    for value in (e["color"], e["ownBg"]):
                        rgb = parse_rgb(value)
                        if rgb and _close(rgb, target):
                            accented.append(e)
                            break

                # union-find over shared category tokens
                groups = []          # list of (token_set, key_set)
                for e in accented:
                    toks = _tokens(e)
                    key = f"{e['tag']}.{(e['cls'] or '').split(' ')[0]}"
                    hit = [g for g in groups if toks & g[0]] if toks else []
                    if hit:
                        merged = (set(), set())
                        for g in hit:
                            merged[0].update(g[0]); merged[1].update(g[1])
                            groups.remove(g)
                        merged[0].update(toks); merged[1].add(key)
                        groups.append(merged)
                    else:
                        groups.append((set(toks), {key}))

                classes = {" / ".join(sorted(g[1])) for g in groups}
                if len(classes) > 1:
                    report.error("G", f"{tag}: accent applied to {len(classes)} element "
                                      f"classes ({', '.join(sorted(classes))}) — an accent "
                                      "everywhere is a second brand colour and points at "
                                      "nothing")

        # --- C: chrome tax
        chrome = [e for e in els
                  if re.search(r"\b(logo|mark|wordmark|handle|pagination|pager|watermark)\b",
                               (e["cls"] or ""), re.I)]
        if len(chrome) > MAX_CHROME:
            report.error("C", f"{tag}: {len(chrome)} persistent brand elements — the "
                              "ceiling is one mark in a fixed corner")

        # --- U: is anything isolated?
        #
        # 07-focal-point: the focal point is a contrast of kind — one element is
        # the only saturated / photographic / dense / textured thing on the
        # frame. Of the five carriers this check can see exactly one, because it
        # reads CSS colour and cannot sample a photograph. So it is a warning
        # with the escape hatch stated in the message: a frame that fails may
        # still have a perfectly good focal point carried by something else.
        # Grouped by colour, not by element. Comparing the top element against
        # the next *lower* value made five identical blocks look isolated —
        # each one cleared the neutral text behind it. And comparing against
        # the next element punished a hero figure whose unit span carries the
        # same colour. The question is whether one colour dominates, so one
        # colour is one entry however many elements wear it.
        by_colour = {}
        for e in els:
            if _is_ground(e, frame) or _is_brand_furniture(e, frame):
                continue
            for value in ((e["color"] if e["text"] else None), e["ownBg"]):
                rgb = parse_rgb(value)
                if rgb:
                    by_colour[rgb] = _chroma(rgb)
        chromas = sorted(by_colour.values(), reverse=True)
        if len(els) >= MIN_COLOURED and len(chromas) >= 2:
            top, runner = chromas[0], chromas[1]
            if top < CHROMA_MIN:
                report.warn("U", f"{tag}: nothing on this frame is saturated (top chroma "
                                 f"{top:.0f}) — if the focal point is carried by register, "
                                 "density, texture or negative space, this check cannot "
                                 "see it; if it isn't, there is no focal point")
            elif top < runner * CHROMA_ISOLATION:
                report.warn("U", f"{tag}: top chroma {top:.0f} against a runner-up of "
                                 f"{runner:.0f} — nothing is isolated by colour. Suppress "
                                 "the field rather than amplifying the subject")

        # --- W: the type zone
        zone = text_zone(frame)
        picture_led = _has_picture(frame)
        floor = TYPE_ZONE_PICTURE_LED if picture_led else TYPE_ZONE_TYPE_LED
        if zone < floor:
            msg = (f"{tag}: copy covers {zone:.0%} of the usable canvas, floor on a "
                   f"{'picture-led' if picture_led else 'type-led'} frame is {floor:.0%} — "
                   "the copy occupies a zone, not a corner")
            (report.warn if picture_led else report.error)("W", msg)

        # --- V: the pinboard
        #
        # 04-graphics-imagery routes on the asset count before design starts:
        # one photograph is A, one cut subject (plus at most one treated mass)
        # is C, roughly ten cutouts is B. Between C's ceiling and B's floor
        # there is no structure — only photographs arranged politely on a
        # field, which is what this system's own collage attempts produced and
        # what the count catches. It cannot see overlap, scale or silhouette,
        # so eight-plus passes the count without being shown to be a B, and a
        # portrait used as a data unit is indistinguishable from a pinboard.
        photos = photo_count(frame)
        if PINBOARD_MIN <= photos < COLLAGE_MIN:
            report.error("V", f"{tag}: {photos} photographic elements — too many for A "
                              "or C, too few for B: the pinboard. One strong photograph "
                              "is A; one cut subject with a glyph vocabulary is C; a "
                              f"collage needs roughly ten cutouts (floor {COLLAGE_MIN})")


def photo_count(frame):
    """Photographic elements visible on the frame — the routing count.

    Tags first (img, video, canvas, SVG image), whatever their size,
    because a lightened render may have shrunk them; then raster backgrounds
    above a small share, so a tiled texture is not mistaken for a picture.
    Decorative (aria-hidden) elements still count: a ghosted second copy of the
    subject is a photograph however faint, and 04's device allows one, which is
    inside C's ceiling.
    """
    area = (frame["w"] or 1) * (frame["h"] or 1)
    n = 0
    for el in frame["els"]:
        # <picture> is not listed: the <img> inside it is the element.
        if el["tag"] in ("img", "video", "canvas", "image"):
            n += 1
        elif el.get("raster") and (el["w"] * el["h"]) / area >= PHOTO_MIN_SHARE:
            n += 1
    return n


BRAND_FURNITURE = re.compile(
    r"\b(dot|dot-mark|brand-dot|logo|wordmark|mark)\b", re.I)
HERO_FIGURE = re.compile(
    r"\b(hero|figure|stat-figure|stat|big-number|num|pct|percent)\b", re.I)
FURNITURE_MAX = 3           # above this a shared class is a data unit, not a mark


def _is_brand_furniture(el, frame=None):
    """The one-off brand mark, not a repeated data unit.

    `span.dot` — the accent full stop that closes a headline — is furniture,
    and the exemption previously missed it: the pattern listed `brand-dot` and
    `dot-mark` but not the bare `dot` the house tiles actually use.

    Adding it needs a guard. A hundred `.dot`s in a waffle field are marks, and
    exempting those would hide exactly the accent inflation check G exists to
    catch. So a class carrying the accent on three or more elements is data.
    """
    if not BRAND_FURNITURE.search(el.get("cls") or ""):
        return False
    if frame is None:
        return True
    cls = el.get("cls") or ""
    same = sum(1 for e in frame["els"] if (e.get("cls") or "") == cls)
    return same < FURNITURE_MAX


def _is_hero_figure(el):
    return bool(HERO_FIGURE.search(el.get("cls") or ""))


REGISTER_RATIO = 1.20       # sizes closer than this are one register


def _registers(sizes, hero=False):
    """Group type sizes, descending, into registers.

    02-typography caps a frame at three registers — display, body, caption —
    not at three distinct pixel values. Two sizes 18% apart are one register
    set slightly differently, and counting each separately fired the ceiling on
    frames the system elsewhere prescribes.

    A hero figure and the display line beneath it are also one register: the
    figure *is* the display, run large. That replaces the old +1 allowance,
    which handed a fourth register to any frame carrying a `.hero` class
    whether or not the extra size belonged to the figure.
    """
    groups = []
    for s in sizes:
        if groups and s * REGISTER_RATIO >= groups[-1][-1]:
            groups[-1].append(s)
        else:
            groups.append([s])
    if hero and len(groups) > 1:
        groups[0].extend(groups.pop(1))
    return groups


def _has_picture(frame):
    """Does something other than type carry this canvas?

    A photograph, illustration, chart or mark field covering a quarter of the
    frame. Its presence lowers the headline floor: on those frames the picture
    is the picture, and a 12%-cap headline would be fighting it.
    """
    area = (frame["w"] or 1) * (frame["h"] or 1)
    for el in frame["els"]:
        share = (el["w"] * el["h"]) / area
        if share < PICTURE_SHARE or _is_ground(el, frame):
            continue
        if el["tag"] in ("img", "svg", "canvas", "picture", "video"):
            return True
        if el.get("kids", 0) >= 6 and not el["text"]:
            return True                   # a dot field or waffle grid
        # A three-block stacked bar is as much a picture as a hundred-dot grid.
        # Count children that carry their own fill: a wrapper holding three
        # paragraphs has none, a bar holding three marks has three.
        if el.get("fills", 0) >= 2 and not el["text"]:
            return True
        if el["bgImage"] and "gradient" not in el["bgImage"].lower():
            return True
    return False


def _hex_to_rgb(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        return None
    try:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _close(a, b, tol=16):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def _contains(outer, inner, pad=2):
    return (outer["x"] - pad <= inner["x"]
            and outer["y"] - pad <= inner["y"]
            and outer["x"] + outer["w"] + pad >= inner["x"] + inner["w"]
            and outer["y"] + outer["h"] + pad >= inner["y"] + inner["h"])


# --- driver ----------------------------------------------------------------
def plugin_version():
    try:
        return json.loads(PLUGIN_JSON.read_text())["version"]
    except Exception:
        return None


RASTER_URI = re.compile(
    r"data:image/(?P<kind>png|jpe?g|webp|gif|avif);base64,(?P<b64>[A-Za-z0-9+/=]{2000,})")
HEAVY_FILE = 1_200_000     # bytes of HTML above which the rasters get swapped


def _raster_dims(kind, b64):
    """Pixel dimensions from the head of a base64 raster, or None.

    Decodes only the head — 64KB is enough for a PNG IHDR, a GIF header, a WebP
    chunk header and any JPEG SOF that is not buried under an oversized EXIF
    thumbnail. Unknown or unparseable falls back to None, and the caller
    substitutes a 1x1.
    """
    import base64
    head = b64[:88_000]
    head = head[:len(head) - len(head) % 4]
    try:
        data = base64.b64decode(head, validate=False)
    except Exception:
        return None
    try:
        if kind == "png" and data[:8] == b"\x89PNG\r\n\x1a\n":
            return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
        if kind == "gif" and data[:4] == b"GIF8":
            return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
        if kind == "webp" and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            tag = data[12:16]
            if tag == b"VP8X":
                return (1 + int.from_bytes(data[24:27], "little"),
                        1 + int.from_bytes(data[27:30], "little"))
            if tag == b"VP8 ":
                return (int.from_bytes(data[26:28], "little") & 0x3FFF,
                        int.from_bytes(data[28:30], "little") & 0x3FFF)
            if tag == b"VP8L":
                bits = int.from_bytes(data[21:25], "little")
                return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
        if kind in ("jpg", "jpeg") and data[:2] == b"\xff\xd8":
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                seg = int.from_bytes(data[i + 2:i + 4], "big")
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    return (int.from_bytes(data[i + 7:i + 9], "big"),
                            int.from_bytes(data[i + 5:i + 7], "big"))
                i += 2 + seg
    except Exception:
        return None
    return None


def _placeholder(match):
    """A same-size stand-in for one embedded raster.

    An SVG with explicit width and height has those intrinsic dimensions, so an
    <img> that took its size from the picture keeps it. The 1x1 PNG this used
    to swap in collapsed any auto-sized image to a pixel, which moved every
    element laid out against it and put a full-bleed photograph under the
    picture-share threshold — so a lightened Structure A frame was measured as
    type-led. `data-raster` marks it so the probe still counts it as a photo.
    """
    dims = _raster_dims(match.group("kind"), match.group("b64")) or (1, 1)
    w, h = max(1, dims[0]), max(1, dims[1])
    return ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
            f"width='{w}' height='{h}' data-raster='{match.group('kind')}'/%3E")


def _lighten(path, tmpdir):
    """Swap embedded rasters for a same-size placeholder before probing.

    Nothing the probe reads is a pixel. It measures boxes, computed styles and
    tag names, so the picture content is dead weight in the render — and a tile
    carrying a few megabytes of base64 keeps headless Chrome busy well past any
    sane timeout. Two artifacts in one session never returned a result at all,
    which is worse than a slow check: nothing is reported, and the run reads as
    clean because it never ran.

    Returns (path_to_load, n_swapped). The swap is announced, not silent — a
    check that quietly changes its input is a check you cannot trust.
    """
    raw = Path(path).read_bytes()
    if len(raw) < HEAVY_FILE:
        return path, 0
    text = raw.decode("utf-8", "replace")
    text, n = RASTER_URI.subn(_placeholder, text)
    if not n:
        return path, 0
    out = Path(tmpdir) / f"lightened-{Path(path).name}"
    out.write_text(text, encoding="utf-8")
    return str(out), n


def render_frames(paths, chrome_path=None, width=1080, height=1350):
    sys.path.insert(0, str(HERE))
    from _chrome import Chrome, find_chrome, ChromeUnavailable  # noqa: E402

    binary = find_chrome(chrome_path)          # raises ChromeUnavailable
    per_file = {}
    tmpdir = tempfile.mkdtemp(prefix="check-static-")
    with Chrome(binary, width, height) as browser:
        for path in paths:
            load_path, swapped = _lighten(path, tmpdir)
            if swapped:
                print(f"NOTE  {Path(path).name}: {swapped} embedded raster(s) replaced "
                      f"with same-size placeholders for the render — geometry, colour "
                      f"and tag checks are unaffected; check U cannot sample them",
                      file=sys.stderr)
            browser.load(load_path)
            declared = browser.evaluate(
                "getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()"
                " || (document.querySelector('[data-accent]')||{dataset:{}}).dataset.accent || ''")
            # Settle entry animations before measuring. An artifact with a
            # `rise` entrance sits at its from-state (translateY(18px)) when the
            # page is probed, and getBoundingClientRect is post-transform — so
            # every animated block reported 18px lower than it actually rests,
            # producing phantom safe-zone and overflow errors. The exported
            # still is the rested frame, so that is what gets measured.
            browser.evaluate(
                "document.getAnimations().forEach(function(a){try{a.finish()}"
                "catch(e){}}); 1")
            per_file[path] = (browser.evaluate(PROBE) or [], declared or None)
    return per_file


def check(paths, strict=False, no_render=False, chrome_path=None, as_set=False):
    version = plugin_version()
    reports = {}
    rendered = {}

    if not no_render:
        try:
            rendered = render_frames(paths, chrome_path)
        except Exception as exc:                # ChromeUnavailable, CDPError
            for path in paths:
                reports.setdefault(path, Report())
            note = str(exc).splitlines()[0]
            for report in reports.values():
                report.warn("render", f"rendered tier skipped ({note})")
                for name in ("B occupancy", "E size floors", "I contrast", "I mark ΔL",
                             "G accent inflation", "C chrome tax", "H template sameness"):
                    report.skip(name)

    all_signatures = []
    for path in paths:
        report = reports.setdefault(path, Report())
        static_checks(path, Path(path).read_text(), report, version)
        if path in rendered:
            frames, accent = rendered[path]
            rendered_checks(frames, report, accent)
            for frame in frames:
                all_signatures.append((path, frame["index"], frame_signature(frame)))

    # --- H: template sameness, across the whole set
    if as_set:
        for i, (path, index, sig) in enumerate(all_signatures):
            for other_path, other_index, other_sig in all_signatures[i + 1:]:
                overlap = sameness(sig, other_sig)
                if overlap >= SAMENESS_FLOOR:
                    where = (f"{Path(other_path).name} frame {other_index + 1}"
                             if other_path != path else f"frame {other_index + 1}")
                    reports[path].error(
                        "H", f"frame {index + 1} is {overlap:.0%} the same shape as "
                             f"{where} — same frame, different words. Hold style "
                             "constant; vary the composition")
    return reports


def print_reports(reports, strict):
    failed = False
    for path, report in reports.items():
        name = Path(path).name
        if not report.items:
            print(f"OK    {name}")
            continue
        for level, code, message in report.items:
            print(f"{level:<5} {name}  [{code}] {message}")
        if report.skipped:
            print(f"      {name}  skipped: {', '.join(report.skipped)}")
        if report.errors or (strict and report.warnings):
            failed = True
    return failed


# --- self-test -------------------------------------------------------------
def self_test(chrome_path=None):
    """Fire every check against fixtures that are wrong on purpose.

    A check that has never failed on purpose is a check nobody has tested. Each
    fixture reconstructs a real rejected example from ../../../examples/bad/ and
    declares the codes it must produce.
    """
    fixtures = HERE / "fixtures"
    expect = {
        "dead-canvas.html": {"B", "C", "F", "N"},
        "drawn-tear.html": {"F"},
        "unfocused.html": {"U", "W"},
        "accent-inflation.html": {"G"},
        "contrast-failure.html": {"A", "D", "I"},
        "pinboard.html": {"V"},
    }
    # Right on purpose. A check that only ever fires has not been shown to
    # stop firing where the system says the thing is allowed: a Structure C
    # frame carries a subject and a treated mass (two photographs, inside C's
    # ceiling) and a ghosted artefact set in type behind the safe line. None of
    # V, S, E or I may fire on it. Everything else it reports is tolerated —
    # the fixture proves the carve-outs, not that it is a good tile.
    quiet = {
        "layered-c.html": {"V", "S", "E", "I"},
    }
    missing = [n for n in list(expect) + list(quiet) if not (fixtures / n).is_file()]
    if missing:
        print(f"FAIL  fixtures missing: {', '.join(missing)}")
        return 1

    paths = [str(fixtures / n) for n in list(expect) + list(quiet)]
    reports = check(paths, as_set=True)
    ok = True
    for name, wanted in expect.items():
        got = reports[str(fixtures / name)].codes()
        missed = wanted - got
        if missed:
            print(f"FAIL  {name}: expected {sorted(wanted)}, missing {sorted(missed)} "
                  f"(got {sorted(got)})")
            ok = False
        else:
            print(f"OK    {name}: fired {sorted(wanted)}")
    for name, banned in quiet.items():
        got = reports[str(fixtures / name)].codes()
        wrong = banned & got
        if wrong:
            print(f"FAIL  {name}: must stay quiet on {sorted(banned)}, fired {sorted(wrong)}")
            ok = False
        else:
            print(f"OK    {name}: quiet on {sorted(banned)} (fired {sorted(got)})")

    # The sameness check needs two frames that match; the two Socceroos-derived
    # fixtures are built to.
    same = any("H" in r.codes() for r in reports.values())
    print(("OK    " if same else "FAIL  ") + "H template sameness fires across the set")
    return 0 if (ok and same) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="*", help="HTML artifacts to check")
    parser.add_argument("--set", dest="as_set", metavar="DIR", nargs="?", const=True,
                        help="treat the inputs (or DIR's *.html) as one carousel, "
                             "enabling the template-sameness check")
    parser.add_argument("--strict", action="store_true", help="warnings also fail")
    parser.add_argument("--no-render", action="store_true",
                        help="static tier only, on purpose")
    parser.add_argument("--chrome", help="path to a Chrome or Chromium binary")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test(args.chrome)

    paths = list(args.paths)
    if isinstance(args.as_set, str):
        paths += sorted(str(p) for p in Path(args.as_set).glob("*.html"))
    if not paths:
        parser.print_usage()
        return 2
    for path in paths:
        if not Path(path).is_file():
            print(f"FAIL  not a file: {path}")
            return 2

    reports = check(paths, strict=args.strict, no_render=args.no_render,
                    chrome_path=args.chrome, as_set=bool(args.as_set))
    failed = print_reports(reports, args.strict)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
