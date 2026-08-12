#!/usr/bin/env python3
"""Check a generated HTML artifact against the mechanically checkable house rules.

Prose rules get skipped under load. A check that fails loudly does not. This
covers the subset of the editorial-motion rules that can be verified from the
source text alone — most from analog-surface, a few from motion-system.

It does NOT judge design. It cannot tell you the composition is weak, the focal
point is wrong or the pacing is off. It catches the specific, repeated,
mechanical failures the reference set names.

Stdlib only. Ancestry is tracked with html.parser rather than guessed with
regexes, so the "image outside a homogenise wrapper" and "fringe on glyphs"
checks are accurate rather than approximate.

Usage
-----
    python3 check-artifact.py artifact.html
    python3 check-artifact.py *.html --strict     # warnings also fail
    python3 check-artifact.py --self-test         # prove the checks still fire

Exit codes: 0 clean, 1 errors found (or warnings under --strict), 2 bad usage.
"""

import argparse
import re
import sys
from html.parser import HTMLParser

# The house curve set, from motion-system/assets/motion.css.
HOUSE_CURVES = {
    (0.10, 0.90, 0.20, 1.0),    # --ease-vox
    (0.16, 1.0, 0.30, 1.0),     # --ease-out
    (0.83, 0.0, 0.17, 1.0),     # --ease-in-out / --ease-io
    (0.34, 1.56, 0.64, 1.0),    # --ease-spring
    (0.55, 0.0, 1.0, 0.45),     # --ease-in
    (0.55, 0.0, 1.0, 1.0),      # .is-leaving  (motion.css cut-out)
    (0.0, 0.0, 0.45, 1.0),      # .is-entering (motion.css cut-in)
}

TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "span", "a", "li",
             "strong", "em", "b", "i", "blockquote", "figcaption", "label"}

WHITE = re.compile(
    r"background(?:-color)?\s*:\s*(?:#fff(?:fff)?|white)\b", re.I)
BLACK = re.compile(
    r"background(?:-color)?\s*:\s*(?:#000(?:000)?|black)\b", re.I)
HAIRLINE = re.compile(
    r"border(?:-top|-bottom|-left|-right)?\s*:\s*1px\s+solid", re.I)
BEZIER = re.compile(r"cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,"
                    r"\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", re.I)
STRENGTH = re.compile(r"--(?:tex|grain)-strength\s*:\s*([\d.]+)", re.I)
# Lookbehind rejects a preceding digit or dot, so `.01ms` / `0.01ms` — the
# reduced-motion idiom — no longer parses as "1ms". That regex bug, plus no
# block exclusion, made the linter flag the house's own accessibility CSS.
SHORT_ANIM = re.compile(
    r"(?:animation|transition)(?:-duration)?\s*:[^;{}]*?(?<![\d.])(\d+)ms", re.I)
REDUCED_BLOCK = re.compile(
    r"@media[^{]*prefers-reduced-motion[^{]*\{", re.I)
MASK_SIZE = re.compile(r"mask-size\s*:\s*(\d+)px", re.I)
TILE = re.compile(r"--tile\s*:\s*(\d+)px", re.I)


class Finding:
    def __init__(self, level, rule, message, line=None):
        self.level, self.rule, self.message, self.line = level, rule, message, line

    def __str__(self):
        where = f":{self.line}" if self.line else ""
        return f"  {self.level.upper():5s} {self.rule}{where} — {self.message}"


def strip_comments(text):
    """Remove CSS and HTML comments, preserving line count.

    Essential: analog.css itself contains the literal text "NEVER #fff" in a
    comment, and the reference boards discuss the rules they demonstrate. A
    checker that flags its own documentation gets switched off.
    """
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    return text


class Ancestry(HTMLParser):
    """Collect elements with their open-tag ancestry and source line."""

    VOID = {"img", "br", "hr", "input", "meta", "link", "source", "area",
            "base", "col", "embed", "param", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.elements = []   # (tag, attrs dict, [(tag, classes)...], line)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        self.elements.append((tag, a, list(self.stack), self.getpos()[0]))
        if tag not in self.VOID:
            self.stack.append((tag, classes))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        self.elements.append((tag, a, list(self.stack), self.getpos()[0]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


IGNORE = re.compile(r"check-artifact-ignore\s*:\s*([^\n>]*)", re.I)
RULE_TOKEN = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")

ALL_RULES = {"no-pure-white", "no-pure-black", "homogenise-imagery",
             "fringe-on-glyphs", "reduced-motion", "roughen-hairlines",
             "house-easing", "texture-strength", "matte-alignment",
             "jump-cut", "unparsed"}


def ignored_rules(text):
    """File-level suppressions, read before comments are stripped.

    A reference board that demonstrates a failure on purpose — a white panel as
    the "before" half of an A/B, an un-homogenised image shown for contrast —
    would otherwise fail its own checks forever, and a linter that always fails
    is a linter people stop reading. The directive is a comment naming the rules
    and, by convention, why:

        <!-- check-artifact-ignore: no-pure-white, homogenise-imagery
             The digital panel IS the counter-example. -->

    Rule names are extracted as tokens rather than split on commas, so a
    trailing `-->` does not get glued onto the last name — which it did, and
    which the self-test caught.
    """
    rules = set()
    for m in IGNORE.finditer(text):
        rules.update(RULE_TOKEN.findall(m.group(1)))
    return rules


def check(text, name="<input>"):
    findings = []
    suppressed = ignored_rules(text)
    clean = strip_comments(text)

    def line_of(match_start):
        return clean[:match_start].count("\n") + 1

    # --- 1. Pure white / black grounds -------------------------------------
    for m in WHITE.finditer(clean):
        findings.append(Finding(
            "error", "no-pure-white",
            "pure white ground. Paper absorbs the colour temperature of the "
            "room; #FDFAF3 is the measured reference value", line_of(m.start())))
    for m in BLACK.finditer(clean):
        findings.append(Finding(
            "error", "no-pure-black",
            "pure black ground. Printed black sits around 12-15% lightness "
            "(#1F1C18)", line_of(m.start())))

    # --- 2/3. Ancestry-dependent checks ------------------------------------
    parser = Ancestry()
    try:
        parser.feed(text)
    except Exception as exc:                       # malformed markup
        findings.append(Finding("warn", "unparsed",
                                f"HTML could not be fully parsed: {exc}"))

    has_homogenise_anywhere = "an-homogenise" in clean
    for tag, attrs, ancestors, line in parser.elements:
        classes = (attrs.get("class") or "").split()

        if tag in ("img", "video"):
            wrapped = any("an-homogenise" in cls for _, cls in ancestors)
            if not wrapped:
                findings.append(Finding(
                    "error" if has_homogenise_anywhere else "warn",
                    "homogenise-imagery",
                    f"<{tag}> is not inside an .an-homogenise wrapper. Every "
                    "raster asset goes through one shared treatment or "
                    "mismatched sources stay mismatched", line))

        if tag in TEXT_TAGS and any(c.startswith("an-ca-") for c in classes):
            findings.append(Finding(
                "warn", "fringe-on-glyphs",
                f"chromatic fringe applied directly to <{tag}>. The filter "
                "recombines channels with `screen`, which washes dark ink out "
                "over light paper — put it on the container", line))

    # --- 4. Reduced motion --------------------------------------------------
    animates = ("@keyframes" in clean
                or re.search(r"animation\s*:", clean) is not None)
    if animates and "prefers-reduced-motion" not in clean:
        findings.append(Finding(
            "error", "reduced-motion",
            "the artifact animates but has no prefers-reduced-motion block"))

    # --- 5. Hairlines -------------------------------------------------------
    # Scope the "is it already treated?" test to the enclosing declaration
    # block. A line-window is too coarse: in compact CSS it reaches into the
    # neighbouring rule, and a masked rule two lines away silently suppresses
    # the finding — which is exactly what the self-test caught.
    for m in HAIRLINE.finditer(clean):
        ln = line_of(m.start())
        open_brace = clean.rfind("{", 0, m.start())
        close_brace = clean.find("}", m.start())
        block = clean[open_brace + 1:close_brace if close_brace != -1 else len(clean)]
        if "mask" not in block and "filter" not in block:
            findings.append(Finding(
                "warn", "roughen-hairlines",
                "1px solid border with no mask or filter nearby. Sharp clean "
                "rules read as computerized; mask with the grain plate "
                "(.an-rule) rather than filtering, which pixelates", ln))

    # --- 6. Easing off the house set ---------------------------------------
    for m in BEZIER.finditer(clean):
        curve = tuple(round(float(g), 2) for g in m.groups())
        if curve not in HOUSE_CURVES:
            findings.append(Finding(
                "warn", "house-easing",
                f"cubic-bezier{curve} is not in the house set. See motion.css",
                line_of(m.start())))

    # --- 7. Texture too strong ---------------------------------------------
    for m in STRENGTH.finditer(clean):
        val = float(m.group(1))
        if val > 0.12:
            findings.append(Finding(
                "warn", "texture-strength",
                f"texture strength {val} is well above the 5% house value. If "
                "the texture is noticeable as texture it is too strong",
                line_of(m.start())))

    # --- 8. mask-size against --tile ---------------------------------------
    tiles = {int(m.group(1)) for m in TILE.finditer(clean)}
    if tiles:
        for m in MASK_SIZE.finditer(clean):
            size = int(m.group(1))
            if size not in tiles:
                findings.append(Finding(
                    "warn", "matte-alignment",
                    f"literal mask-size {size}px does not match any --tile "
                    f"value {sorted(tiles)}. The ink is then masked against a "
                    "different part of the paper than it sits on, and the "
                    "effect silently disappears", line_of(m.start())))

    # --- 9. Sub-100ms travel -----------------------------------------------
    # Scan a copy with @media prefers-reduced-motion blocks blanked: near-zero
    # durations there are the required accessibility idiom, not a jump-cut.
    scan = clean
    for m in list(REDUCED_BLOCK.finditer(clean)):
        depth, i = 1, m.end()
        while i < len(scan) and depth:
            if scan[i] == "{":
                depth += 1
            elif scan[i] == "}":
                depth -= 1
            i += 1
        scan = (scan[:m.start()]
                + re.sub(r"[^\n]", " ", scan[m.start():i])
                + scan[i:])
    for m in SHORT_ANIM.finditer(scan):
        ms = int(m.group(1))
        if ms < 100:
            findings.append(Finding(
                "warn", "jump-cut",
                f"{ms}ms duration. Under 100ms an element that *travels* reads "
                "as a jump-cut; only sub-perceptual UI feedback belongs here",
                scan[:m.start()].count("\n") + 1))

    unknown = suppressed - ALL_RULES
    if unknown:
        findings.append(Finding(
            "warn", "unknown-suppression",
            f"check-artifact-ignore names {sorted(unknown)}, which is not a "
            f"rule this checker emits — a typo suppresses nothing"))
    if suppressed:
        findings = [f for f in findings if f.rule not in suppressed]
    return findings


# ------------------------------------------------------------------ tests ---

GOOD = """<!doctype html><style>
:root{--tile:512px;--tex-strength:.05}
.an-surface{background-color:#FDFAF3;background-size:var(--tile)}
.an-ink{mix-blend-mode:multiply;mask-image:url(m.png);mask-size:512px}
.an-rule{height:1.5px;background:#1F1C18;mask-image:url(g.png)}
.x{animation:rise .5s cubic-bezier(0.16,1,0.30,1) both}
@keyframes rise{from{opacity:0}to{opacity:1}}
.y{animation:cut-out 260ms cubic-bezier(0.55,0,1,1) both}
@media (prefers-reduced-motion:reduce){.x{animation-duration:.01ms !important}
 .y{animation:fast 1ms both}}
</style>
<!-- background:#fff in a comment must not be flagged -->
<div class="an-homogenise"><img src="a.png"></div>
<h1 class="an-ink">EVIDENCE</h1>"""

BAD = """<!doctype html><style>
:root{--tile:512px;--tex-strength:.35}
.card{background:#fff}
.dark{background-color:black}
.hr{border-bottom:1px solid #ccc}
.y{animation:slide 60ms cubic-bezier(0.25,0.1,0.25,1) both}
.an-ink{mask-image:url(m.png);mask-size:256px}
@keyframes slide{from{transform:translateX(20px)}to{transform:none}}
</style>
<div class="an-homogenise"><img src="ok.png"></div>
<img src="loose.png">
<h1 class="an-ca-archival">FRINGE</h1>"""

EXPECTED_BAD = {"no-pure-white", "no-pure-black", "texture-strength",
                "roughen-hairlines", "house-easing", "jump-cut",
                "matte-alignment", "homogenise-imagery", "fringe-on-glyphs",
                "reduced-motion"}


def self_test():
    ok = True

    good = check(GOOD, "GOOD")
    if good:
        ok = False
        print("FAIL: clean input produced findings (false positives):")
        for f in good:
            print(f)
    else:
        print("pass: clean input produces no findings")

    fired = {f.rule for f in check(BAD, "BAD")}
    missing = EXPECTED_BAD - fired
    unexpected = fired - EXPECTED_BAD
    if missing:
        ok = False
        print(f"FAIL: these checks did not fire on known-bad input: "
              f"{sorted(missing)}")
    else:
        print(f"pass: all {len(EXPECTED_BAD)} checks fired on known-bad input")
    if unexpected:
        print(f"note: also fired (not asserted): {sorted(unexpected)}")

    # Suppression must remove exactly the named rules and nothing else.
    directive = ("<!-- check-artifact-ignore: no-pure-white, "
                 "homogenise-imagery -->\n")
    after = {f.rule for f in check(directive + BAD, "BAD+ignore")}
    if {"no-pure-white", "homogenise-imagery"} & after:
        ok = False
        print("FAIL: suppression directive did not remove its named rules")
    elif after != fired - {"no-pure-white", "homogenise-imagery"}:
        ok = False
        print(f"FAIL: suppression changed unrelated findings — {sorted(after)}")
    else:
        print("pass: suppression removes exactly the rules it names")

    print("\nSELF-TEST PASSED" if ok else "\nSELF-TEST FAILED")
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Check generated HTML against the house rules.")
    p.add_argument("files", nargs="*")
    p.add_argument("--strict", action="store_true",
                   help="warnings fail too")
    p.add_argument("--self-test", action="store_true",
                   help="verify the checks still fire, then exit")
    args = p.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.files:
        p.error("give at least one HTML file, or --self-test")

    errors = warns = 0
    for path in args.files:
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            print(f"{path}: cannot read — {exc}")
            return 2
        findings = check(text, path)
        e = sum(1 for f in findings if f.level == "error")
        w = len(findings) - e
        errors += e
        warns += w
        status = "clean" if not findings else f"{e} error(s), {w} warning(s)"
        print(f"{path}: {status}")
        for f in sorted(findings, key=lambda f: (f.level != "error", f.line or 0)):
            print(f)

    if errors or (args.strict and warns):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
