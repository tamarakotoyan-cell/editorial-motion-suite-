---
name: static-type-graphics
description: Typography and imagery for fixed-canvas static design — how big the words are, how many typefaces, and what goes on the frame besides them. Use whenever setting type on a social tile, poster, carousel frame or chart card, and whenever a static piece includes an illustration, photograph, cutout, collage, chart or stat tile. Covers two families and three registers, cap-height and minimum-size floors, the capitalised-overline ban and its serial running-head exception, illustration register, full-strength photography, silhouette cutouts, direct chart labelling and mark-equals-number. Pair with static-composition for where it all goes.
---

# Static typography and imagery

The words and the pictures. Composition and colour are settled first by
**static-composition**.

Full detail:

- `references/02-typography.md` — families, registers, size floors, scale, case, the
  overline rule, type as the image.
- `references/04-graphics-imagery.md` — illustration, photography, cutouts, the three
  picture structures and the A/B/C routing table, the raster pipeline, charts, stat
  tiles, source lines.
- `references/08-layered-editorial.md` — Structure C: one cut subject, glyph satellites,
  zoned texture; the window build and the ground-mass build; the layer grammar.

---

## Typography

Static work is read at two sizes: thumbnail, and full frame after someone has decided to
stop. Everything below follows from that.

**Two families maximum, three registers maximum.** One family carries the voice, one
carries the utility. The registers are display (the finding), support (the deck or quote
body) and utility (attribution, source, axis labels, chips). A fourth register is nearly
always a utility line that wanted to be different from the other utility line — make them
the same.

Three valid splits, one per client, held:

- **Serif display + sans utility** — authority. Best when the subject is serious.
- **Single family, weight-differentiated** — the most robust choice when the brand has one
  good face and no second.
- **Heavy sans display + serif support** — conversational. Best when the illustration is
  doing the work.

**Size floors, and they are the point:**

- Headline cap-height runs **8–12% of canvas height**. On 1080×1350 that is a 140–200px
  font size for most faces.
- **No text below 1.25% of canvas height** — about 17px on the same tile. The source line,
  the attribution and the axis labels all sit above it.

The consequence is deliberate: there is not room for much copy. A frame holds a headline, a
supporting sentence and an attribution. If it needs more, it is two frames.

**Scale:** every size on one ratio, declared once. Perfect Fourth (1.333) by default;
Golden Ratio (1.618) for type-only frames; Major Third (1.25) for chart frames. Sizes like
`16 / 19 / 27 / 31 / 42` are the signature of a frame nobody structured.

**Case and alignment:** sentence case, left-aligned. All-caps display is permitted where
the brand's voice is caps — but then for every headline in the set, never one frame in
five. Centred type belongs to the cover. Display leading 0.95–1.05; tracking slightly tight
at display size; never letter-spaced.

⚠️ **Never a serif or display face on a hero figure**, and never `tabular-nums` on one.

### ⛔ The overline rule

No capitalised letterspaced kicker above a single frame's headline. It restates the
headline and pushes it down the canvas. It appears in four of the ten rejected examples.

**The one exception — the serial running head.** A short caps line repeated verbatim across
three or more consecutive frames of one carousel is a chapter marker, not a kicker, and is
permitted. The distinction is mechanical and the linter applies it that way: on one frame
it is a banned kicker; verbatim on three or more consecutive frames, and not restating the
headline beneath it, it is a running head.

Uppercase letterspaced type remains fine for axis labels, chips and attributions.

### Type as the image

When there is nothing to show, the words are the picture — set at display size, filling the
frame. Type-only frames carry the **highest** occupancy requirement, not the lowest. The
failure mode is the same passage at half the size with the remainder abandoned.

## Imagery

**Pick one graphic register per post and hold it:** illustrated, photographic, collaged, or
data-led. Mixing registers is what makes an infographic read as a clip-art assembly.

**Illustration.** One illustrator, one palette of four to six colours, one line weight,
fixed at the cover. Visible texture — stipple, grain, halftone, pencil; flat vector is the
generated-design tell. On the field, not in a box. Breaking an edge.

Icons standing in for concepts — a lightbulb for ideas, a rocket for growth — are
decoration doing meaning's job and are banned. The exception is a pictogram used as a
**unit in a count**, where the icon is the data.

**Photography — full strength or not at all.** Full-bleed, undimmed, hard-cropped, held as
its own frame. Place the type where the photograph is already dark; only where no dark
region exists, add a hard-edged type plate at a frame edge.

⛔ Never a photograph at 40–60% opacity behind the content as wallpaper. Too present to be
neutral ground, too suppressed to be evidence — all it does is lower contrast on everything
in front of it. Alternate registers instead, each at full strength.

**Cutouts** are the highest-risk element in static work. Cut on the silhouette, never a
rectangle through a subject. Vary the scale — uniform-scale cutouts read as a sticker
sheet. Build depth with overlap, never shadows. Keep copy clear of them. Crop at the canvas
edge deliberately or not at all.

### Name the picture structure before you start — from the asset count

Decidable before design, and stated in the five-line plan's layout line:

| You have | Build |
|---|---|
| One strong supplied photograph, and the story *is* evidence | **A** — one photograph carries the frame, full-bleed, type in its dark region |
| One cuttable subject plus a glyph vocabulary the story owns | **C** — layered editorial: one halftoned cutout, 3–6 flat glyph satellites, loud texture inside a window or a second treated mass seating the subject (`references/08-layered-editorial.md`) |
| Roughly ten silhouette cutouts in one register | **B** — dense collage |
| Two to seven photographic elements | **A or C, using one.** Built as B it is the pinboard — photographs arranged politely — and the linter fails it (**V**) |
| None of the above | Type-led or data-led |

Each wrong choice has a named failure in `references/04-graphics-imagery.md`. B without
ten cutouts is the one this system kept producing; C is what dissolves it, because it
needs exactly one.

**Every raster goes through the pipeline** — harden the alpha, contrast window, duotone to
one brand map (the highlight stays a colour), halftone the subject — and the repeatable
way to do that is the static-design skill's `assets/halftone.py`, which also prints the
subject box to place from and fails if the duotone came out grey.

## Charts and figures

**Form first.** Pick the chart type from the data's job — magnitude, identity, polarity,
change over time, or a single headline. **If the finding is one number, it is a stat tile,
not a chart.**

- The title is **the finding**, not the metric name.
- **Direct labelling, never a legend** — the series name in a chip on the mark itself.
- Hairline gridlines one shade off the ground, or none.
- **No chart container.** Full width, at article-headline scale.
- Label selectively: the endpoint, the extreme, the one series that matters.

**⛔ The mark must equal the number.** Every mark in one chart shares a single scale —
length ÷ value constant across the series. Compute geometry from the datum; never draw
marks that look about right and type the numbers on afterwards.

```html
<div class="bar" style="--v: 62"></div>
<style>.bar{ width: calc(var(--v) * 1% * var(--plot-scale)); }</style>
```

Corollaries: no axis without a scale — an axis is a promise about how to read the marks;
and a value label is not a substitute for a correct mark.

**Count rather than measure.** Under roughly 200, draw one mark per unit. Default to one
dot = one per cent so a share is countable against a denominator that is on screen. Never
show a share with no denominator. Emphasise in place rather than extracting a group.

**Stat tiles:** one number at display size in the sans, a short label beneath, the source
line at the foot. Banned: a one-bar bar chart, a two-slice pie, a row of three
equally-weighted figures where one was the point.

**Source and sample size** are non-negotiable for research work — small, muted,
bottom-aligned, above the 1.25% size floor. Re-state the base whenever it changes.

## Self-check

- Two families or fewer, three registers or fewer, every size on the ratio?
- Headline cap-height 8–12%? Smallest text at least 1.25%?
- Hero figure in the sans, without `tabular-nums`?
- Any caps overline above a single frame's headline?
- One graphic register, held across the post? Structure A, B or C named from the asset
  count — and if C, exactly one photographic subject?
- Does the illustration carry texture and break an edge? Any concept icons?
- Any photograph dimmed behind content? Any cutout cut on a rectangle or overlapping copy?
- Is the chart title the finding? Are series labelled on the marks?
- Does length ÷ value hold constant? Is there a denominator for every share?
- Source and sample size present and legible?
