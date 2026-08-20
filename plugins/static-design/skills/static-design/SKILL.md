---
name: static-design
description: Start here for any static design request — this skill decides which of the static-design skills to load and in what order. Use whenever the work is a social tile, feed post, carousel, Instagram or LinkedIn graphic, story frame, event poster, quote card, stat tile, chart card, infographic, report visual, or any fixed-canvas artifact that will be exported as an image rather than animated. Also use when checking a static piece before it goes out. Dispatches and states precedence; teaches no design rules of its own.
---

# static-design — start here

This skill routes. It decides **which skills to load, in what order, and what overrides
what**; every design decision lives in the skills it names. Load it first, load what it
names, then work.

**Static, not motion.** If the piece animates, this is the wrong plugin — use
`editorial-motion`. If the piece is a fixed canvas exported as PNG or JPG, it is this one.

## Load order

The order is not a preference. Each stage constrains the next, and a decision made out of
order gets made twice.

1. **layout-composition** — first, when the `editorial-motion` plugin is installed. Grid,
   canvas format, proportional derivation, the four type scales. It is format-agnostic and
   is not duplicated here. Without it, `static-composition` carries a compact substitute.
2. **static-composition** — always. Occupancy floor, thirds, frame-breaking, the
   no-container rule, colour roles, contrast floors, texture.
3. **static-type-graphics** — always. Two families, three registers, size floors, the
   overline rule, illustration, photography, cutouts, charts, stat tiles.
4. **static-series** — whenever the piece is more than one frame. Carousels, post sets,
   multi-slide decks. What is held constant and what varies.
5. **type-treatment** — additive, and only when a **selected display string** needs a
   material or reproduction cue: type printed into a surface, a halftone or dry-stamp
   word, a paper label. From `editorial-motion`. It owns the print-process taxonomy and
   the tactile contact stack; this plugin does not restate them.

   ⚠️ It is opt-in by design. Regular typeface styling is the default, and most static
   frames should never load it. Reach for it when a physical cue is editorially useful,
   not to make flat type look interesting — that is the failure it exists to prevent.
6. **format-adaptation** — last, and only when the piece ships to more than one aspect
   ratio. From `editorial-motion`; it re-composes per format and is not a way to crop a
   master.

A bare request — "a tile about rental affordability" — resolves to layout-composition →
static-composition → static-type-graphics. No type-treatment, no format-adaptation.

## Precedence

Where two sources disagree, the higher one wins:

1. **The client's brand.** Colour and typeface come from them. Work is produced for many
   clients; Essential is simply the case where the client is Essential. Role slots and the
   Essential values are in `references/brand.md`.
2. **The house ban list** — `references/house-rules-static.md`. It overrides every style
   skill, including the reference material they cite.
3. **The skill files**, in the load order above.

## Before you build — the five-line plan

Written before the first line of code, every time. Finding, ground, type, layout,
signature. Then critique each line against *"would I have written this for any other
finding?"* Full method in `references/brand.md`.

**Spend the boldness on the signature, never on the palette or the type.**

**Count the assets before the layout line.** The picture structure is decided from what
was supplied, not from what the brief wants: one strong photograph → **A**; one cuttable
subject and a glyph vocabulary → **C** (layered editorial, one cutout); roughly ten
silhouette cutouts → **B**; none → type-led or data-led. Two to seven photographs is
never B — it is the pinboard, and the linter fails it. The table and each wrong choice's
failure mode are in `static-type-graphics`.

**Treat every raster before it goes on the frame.** `assets/halftone.py` runs the
pipeline — harden alpha, contrast window, duotone to one brand map, halftone the subject —
prints the subject box to place from, and refuses a duotone whose highlight came out grey:

```
python3 assets/halftone.py cutout.png --out cutout-halftone.png --shadow '#1E1E4A' --highlight '#E2491A'
python3 assets/halftone.py mass.png --out mass-duotone.png --mode duotone --shadow '#1E1E4A' --highlight '#E2491A'
```

## Stamp the output

Every generated artifact carries the version of the system that made it, in the head:

```html
<meta name="static-design" content="X.Y.Z">
```

Take the number from the plugin manifest, `.claude-plugin/plugin.json`. Without a stamp an
output cannot be attributed to a version, and no change to these skills can be shown to
have helped or hurt. The linter treats a missing or malformed stamp as an error, and a stale one — a
well-formed number that is not the manifest's — as a warning.

## Before delivering

Lint the generated HTML and fix what it reports. This is a required step, not a suggestion:

```
python3 assets/check-static.py artifact.html
```

For a carousel, lint the whole set at once so the template-sameness check can run:

```
python3 assets/check-static.py --set out/
```

It catches the mechanical failures prose gets wrong under load — white or pure-black
grounds, content covering less than 60% of the canvas, containers and shadows, a third type
family, sizes off the scale, text below the size floor, accent inflation, contrast failures,
decorative gradients, more than one persistent brand element, two to seven photographs on
one frame (the pinboard), and two frames in a set with the same shape. **Errors are not
advisory.** A warning may be left in, but only with a reason.

## Then the three questions

Any "no" is a fix, not a ship.

1. At 200px wide, is the finding still legible?
2. Could someone state the point out loud after two seconds?
3. Would this be interchangeable with the last piece after a content swap? **"Yes" is the
   failure.**

Then remove the one element doing the least. Something always comes out.
