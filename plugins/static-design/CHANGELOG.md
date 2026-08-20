# Changelog

## 0.6.0

The third picture structure, and the routing that makes the choice mechanical.
Structure B kept failing for one reason — the ten-cutout precondition was never
met — and the tile that finally carried collage energy did it with **one**
cutout: a halftoned subject among flat glyph satellites, the loud texture held
inside a window or a second treated mass seating the subject. That register is
now in the master as Structure C, and the A/B/C decision is made from the asset
count before design starts.

### Added
- **`principles/08-layered-editorial.md`** — Structure C, both builds (window,
  ground-mass), the seven-layer grammar, texture zoning, the satellite tests,
  the ground-mass tests, the register's ban list, build recipes, and the
  measured read of the two source tiles. Three of its rules are marked
  **[proposal]** because they re-read the master rather than restate it: the
  ground mass as a second photographic *element* that is not a *subject*;
  one texture layer *per zone*; and glyph satellites as objects rather than
  concept icons. Vendored into `static-type-graphics`.
- **The routing table in `04-graphics-imagery`** — one strong photograph → A;
  one cuttable subject + a glyph vocabulary → C; roughly ten cutouts → B;
  two to seven photographs → A or C with one of them, never B; none → type-
  or data-led. Each wrong choice named with its failure mode.
- **Check V — the pinboard.** Counts the photographic elements on a frame
  (`img`, `video`, `canvas`, SVG `image`, raster backgrounds above 0.5% of the
  canvas). Three to seven is an error: too many for A or C, too few for B.
  It cannot see overlap, scale or silhouette, and says so. `06-anti-patterns`
  **V**. `collage-v2.html`, this system's own failed pinboard, now fails —
  it passed every check before.
- **`fixtures/pinboard.html`** wrong on purpose (four photographs on a field);
  **`fixtures/layered-c.html`** right on purpose — a subject and a mass (two
  photographs, inside C's ceiling) and a ghosted artefact in the safe zone,
  on which V, S, E and I must all stay quiet. The self-test now proves a
  carve-out as well as a firing.
- **`assets/halftone.py`** — the raster pipeline as a script: harden alpha
  (threshold 128, MinFilter shave) → contrast window measured over the subject
  only → duotone to the brand map with 04's lightest-pixel test run and failed
  loudly → halftone screen (cell ≈7px source, dots in the shadow ink on the
  highlight, area ∝ darkness, drawn at 4× and downsampled). Prints the
  measured subject box to place from. Pillow only. `--self-test`. Cited from
  the router and `static-type-graphics`.

### Fixed
- **`aria-hidden` text is a mark, not copy.** 04's ghosted artefact — a much
  larger, low-contrast copy of the hero behind the composition — is set in
  type on the house tiles, and read as copy it failed the safe-zone, register
  and contrast checks by construction (three errors on the proof tile, all on
  a decorative `75`). Declared decorative it is measured as a picture. Written
  into `04` beside the device.
- **Lightened renders keep their geometry.** Above 1.2MB the embedded rasters
  are swapped before probing, and the swap used a 1×1 PNG — so any image that
  took its size from the picture collapsed to a pixel, everything laid out
  against it moved, and a full-bleed photograph dropped under the picture-share
  threshold, so a Structure A frame was measured as type-led. The placeholder
  is now an SVG carrying the raster's own width and height, read from the PNG
  / JPEG / GIF / WebP header. The stderr note claimed geometry was unaffected;
  now it is.
- **A type plate is recognised by its selector.** Check F excused a gradient
  only when `plate` appeared inside the rule body; `.plate{…}` — how the house
  tiles mark one — still fired. Selector or body now.

### Changed
- `04-graphics-imagery` — "the two picture structures" is three; self-check
  asks for A, B or C from the asset count and flags two-to-seven photographs.
- `06-anti-patterns` — **V**, the pinboard, locked.
- `static-type-graphics` — the routing table, the pipeline step, and the stale
  1.6% text floor corrected to the settled 1.25%.
- `sync-static-design.py` — vendors `08` into `static-type-graphics`.

### Not settled here — for the owner
- The three **[proposal]** rules in `08`; if the ground-mass reading is
  refused, the proof tile is rebuilt as a window build.
- `brand.md` still says "nothing below 1.6%" and stamps `0.3.0` in its
  example; both stale against settled decisions, left for the owner (as the
  Claude Design pack already noted).
- The proof tile's base reads `n=[TK]`; the earlier tiles on the same finding
  carry *July 2026, n=1,060*. Not resolvable from the files.
- Photo rights on the PM and Parliament House photographs. The treated kit
  stays in the pilot folder and is not vendored into this repo for that reason.

## 0.5.0

Adds the missing principle. Nine reference covers, and eight of them make their
focal point by isolating one property rather than by scale — which is the rule
this system did not have, and the reason frames could pass every check and still
read flat.

### Added
- **`principles/07-focal-point.md`.** The focal point is a contrast of *kind*,
  not of size: one element is the only saturated / photographic / dense /
  textured / lit thing on the frame. Five carriers, one per frame, named before
  building. Includes the correction that matters most in practice — **suppress
  the field rather than amplifying the subject**, because a frame that reads
  flat is rarely fixed by making the intended subject louder.
- **Check U — chroma isolation.** Groups colours (not elements) and warns when
  the top chroma does not clear the runner-up by 1.6x, or when nothing on the
  frame is saturated at all. A warning by construction: it reads CSS colour, so
  it cannot sample a photograph and is blind to four of the five carriers. The
  message says so.
- **Check W — the type zone.** Union of the text boxes against the usable
  canvas: 28% on a type-led frame, 18% where a picture carries it. Error on
  type-led, warning on picture-led. Catches the frame that clears the occupancy
  floor because pictures made up the difference and still has its headline in a
  corner.
- **`fixtures/unfocused.html`**, wrong on purpose in both new ways.
- **Eight reference covers** in `examples/good/`, each annotated with the carrier
  it demonstrates.

### Fixed
- **The linter did not finish on large artifacts, and had not for some time.**
  `([^{}]+)\{` in the type-process check can begin matching at any offset, so on
  a file carrying megabytes of base64 the regex engine backtracks across the
  whole document for every candidate start. Two artifacts in one session never
  returned a result — which is worse than a slow check, because nothing is
  reported and the run reads as clean. Anchored on the brace, selector sliced
  backwards: **never finishes becomes 0.16s**, and the same pattern introduced
  in 0.4.0 was fixed with it.
- **Embedded rasters are swapped for a 1x1 placeholder** above 1.2MB of HTML
  before the page is probed. Nothing the probe reads is a pixel. The swap is
  announced on stderr rather than done silently.

### Changed
- `01-layout` — the type zone, measured separately from occupancy.
- `03-colour-and-ground` — **flat field and worked surface named as two ground
  modes**, decide and commit. The flat field was previously "statement frames
  only, never full-bleed data"; five of the nine covers run one carrying a
  headline and a full-bleed illustration, so the restriction was wrong. What
  holds: a flat field carries no texture.
- `04-graphics-imagery` — the **foreign-register exception**: one element may sit
  in a register foreign to the rest when that difference *is* the focal point,
  and exactly one. Plus **shape as a window**, the more general form of
  type-as-window.
- `06-anti-patterns` — **U, the unfocused frame**; **W, copy in a corner**.

## 0.4.0

The rules the reference set actually obeys, applied — and the linter taught to
tell a full-bleed photograph from the ground it is not sitting on.

### Changed — the four open thresholds, settled
- **Text floor 1.6% -> 1.25% of canvas height** (22px -> 17px on a feed tile).
  22px stood above the entire reference set it was derived from, where captions
  run 12-17px, and it collapsed utility and support into one size. The third
  register is back.
- **Hero-figure floor 1.5x -> 1.2x the display.** The reference tiles run about
  1.1x and read stronger than the house's own 1.57x attempts: air and texture
  make a figure dominate, not point size, and a high floor bought scale by
  spending the space that would have done the job better.
- **Occupancy is measured against the usable canvas**, between the safe zones,
  not against the whole frame. With 150px zones top and bottom the old
  denominator quietly asked for 77% in order to report 60%. Cells inside the
  safe band no longer count toward the numerator either — bleed art may cross
  it, but it cannot be what fills the frame.
- **The register ceiling counts registers, not distinct pixel sizes.** Sizes
  within 20% of each other are one register set slightly differently, and a hero
  figure belongs to display alongside the headline it outranks. This replaces
  the +1 allowance, which handed a fourth register to any frame carrying a
  `.hero` class whether or not the extra size belonged to the figure.

### Fixed in `check-static.py`
- **Occupancy and picture detection excluded the ground by area, not by role.**
  Anything over 92% of the canvas was skipped, so a full-bleed photograph — the
  element most likely to be carrying the entire frame, and required to be
  full-bleed by `04-graphics-imagery` — was thrown away and Structure A tiles
  scored as near-empty. Ground is now identified by role, and a picture is never
  ground.
- **The brand-dot exemption in check G never matched `span.dot`.** The pattern
  listed `brand-dot` and `dot-mark` but not the bare `dot` the house tiles use,
  so the accent full stop closing a headline counted as a second element class.
  Adding it needed a guard: a class carrying the accent on three or more
  elements is a data unit, not furniture, or a waffle field would exempt itself
  from the check G exists to run.
- **Check F reported ground structure as decoration.** Folds, creases and rules
  are one of the four layers `03-colour-and-ground` requires and they are drawn
  as narrow linear-gradient bands. Carved out narrowly — a structure-role
  selector *and* a linear gradient; a radial wash on `.frame` is still the
  decoration this check exists to catch, and the self-test proves it.

### Added to `check-static.py`
- **A torn edge drawn as a `clip-path` polygon now fails.** A tear is a cut
  photograph or a turbulence-displaced mask; a path with vertices reads as Canva
  at any size. Fires as **F**.
- **Padding on a flex-grow mark now fails.** With `flex-basis:0` the browser
  adds each item's padding back after distributing, so every mark gains the same
  constant and length / value stops being one number. Measured on a real chart:
  a 9% category with a 14px inset drew 32% too long while the 63% beside it was
  off by 4% and looked fine. Fires as **F**.
- **`fixtures/drawn-tear.html`**, wrong on purpose in both new ways.

### Principles
- `01-layout` — the permission for **a hairline above a source line is deleted**
  and the pattern is banned outright; occupancy restated against the usable
  canvas with ground excluded by role; safe-zone section states that the source
  line is text and stays above the line. Two-corner anchoring added to the
  self-check.
- `02-typography` — new floors; registers counted rather than sizes.
- `04-graphics-imagery` — **Structure A and Structure B named as an explicit
  choice**, with B's precondition (roughly ten cut elements, or build A) and the
  cut-elements-not-torn-rectangles rule; the mandatory homogenisation pipeline
  for raster assets; duotone rather than greyscale, with the lightest-pixel
  test; placement from the measured subject box; one groundline, torn edges on
  large masses, type-as-window, accent keyline, ghosted artefact, two-corner
  anchoring; torn edges as masks with the mask-repeat and alpha gotchas; one
  register per composition, ground included; padding never on a flex-grow mark.
- `06-anti-patterns` — **R, the hairline above the source line**; **T, the drawn
  tear**.

### Worked example
`example-social-tile.html` rebuilt on a Major Third from base 17 rather than 22,
so utility (17px) and support (26.6px) separate again. Clean under both linters.
Re-rendered to `examples/good/essential-data-tile-dark.png`.

## 0.3.0

Shares its source with editorial-motion 1.10.0 — the same rebuild produced both.

### Fixed in `check-static.py`
- **Crash on any artifact containing inline SVG.** `offsetWidth`/`offsetHeight`
  are HTMLElement APIs; on an `<svg>` they are undefined, JSON dropped the keys,
  and the overflow check raised `KeyError`. A crash in a pre-ship linter reads
  as "the tool is broken" and the artifact ships anyway, so the box lookup now
  degrades to the visual rect as well.
- **Every animated artifact reported phantom safe-zone and overflow errors.**
  The page was probed before entry animations settled, so a block with a `rise`
  entrance measured 18px below where it rests. Animations are now finished
  before measuring.
- **`inset 0 0 0 1px` hairlines were reported as box-shadows.** That hairline is
  what `03-colour-and-ground` prescribes to rescue a mark under the DL floor, so
  check A was banning the fix along with the failure. Both the authored and the
  computed layer orders are now recognised.
- **A three-block stacked bar was not counted as a picture**, so a chart frame
  was held to the type-led headline floor. Picture detection now counts children
  carrying their own fill, not child count alone.
- **The hero-figure rule adds a fourth size by construction**, and a bare unit
  set at half the digit size is part of the figure. Both are now allowed for.
- Accent sub-marks no longer count as a second element class under check G.

### Added to the principles
- Hero figure at 1.5-2x the display size (`02-typography`), and the copy budget
  in which the question line replaces the deck.
- The DL-25 impossibility, its arithmetic and its three resolutions
  (`03-colour-and-ground`).
- The flex-grow idiom, direct labelling by leader, and the span rule and callout
  chip (`04-graphics-imagery`).
- Anti-patterns **O** (the disguised legend), **P** (nested marks sized by
  percentage) and **Q** (the figure that lost to its own headline).
- Branding weight by format (`brand.md`).
- `assets/example-social-tile.html` — a worked 4:5 tile, clean under both
  linters.

## 0.2.0

Harmonised with `editorial-motion` 0.1-cross-platform.

- **Anti-pattern N — mid-dot metadata chains**, adopted unchanged from the
  editorial-motion house rules and enforced by `check-static.py`. It belongs
  here because static frames are where metadata chains breed: a footer feels
  like somewhere to put things rather than something to design. It is also the
  mechanism behind the sloppy footer — a chain reads as one lump, gets set small
  and grey to fit, and lands in the safe zone.
- **The opt-in boundary for type texture**, from type-treatment's print-process
  work. `02-typography` now separates composition-wide ground texture (required)
  from a per-string print process (optional, never global, one per string, never
  on body copy, source lines, chart labels or hero figures). The taxonomy itself
  stays in type-treatment — one home per rule area.
- `static-design` router loads **type-treatment** as an additive skill, with the
  warning that most static frames should never load it.
- `check-static.py` enforces the boundary: a process class reached through a
  global selector, or more than one process on a string, is an error.
- Linter fixes found by using it: style and script contents are no longer read
  as visible text (a CSS comment documenting a type scale was firing rule N),
  and collision and overflow now measure the untransformed layout box, so a
  rotated band neither cries wolf nor hides a real overflow.

## 0.1.0

First release. A router plus three skills for fixed-canvas static design.

- `static-design` — router, precedence, version stamp, lint gate, the three-question check.
- `static-composition` — 60% occupancy floor, anchoring to thirds, frame-breaking, the
  no-container rule, colour as roles with exactly one accent, ΔL and contrast floors,
  gradients, texture. Carries a compact substitute for `layout-composition` when the
  `editorial-motion` plugin is not installed.
- `static-type-graphics` — two families and three registers, cap-height and minimum-size
  floors, the capitalised-overline ban with its serial running-head exception, illustration
  register, full-strength photography, silhouette cutouts, direct chart labelling,
  mark-equals-number, stat tiles.
- `static-series` — the carousel as one continuous object, hold-style-vary-composition,
  continued objects, the frame budget, chrome limits, cover and close.
- `references/house-rules-static.md` — the A–M anti-pattern ban list, each entry tied to
  the rejected example that demonstrates it.
- `assets/check-static.py` — static artifact linter, including `--set` for
  template-sameness across a carousel.

Derived from 17 reference posts (@nytimes, @guardianaustralia, @voxdotcom) and 10 rejected
outputs. Ports the precedence chain, colour-as-roles, contrast floors, form-first charts,
texture recipes, the five-line plan and the three-question check from `editorial-motion`;
drops everything timing-related.

One deliberate divergence from `editorial-motion`: the capitalised overline stays banned
per frame, but the **serial running head** — a caps line repeated verbatim across three or
more consecutive frames — is permitted, because the reference set uses it as a chapter
marker and it earns its place in a carousel.
