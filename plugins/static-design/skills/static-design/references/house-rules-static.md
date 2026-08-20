<!-- Vendored copy. Master: Static design content/static-design-system/principles/06-anti-patterns.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 06 — Anti-patterns

The established norms of bad static design, derived from the ten rejected examples in
`bad example: `. Each code names a failure, the example that shows it, why it fails, and
the correct move.

Entries marked 🔒 are enforced by `assets/check-static.py`. The rest depend on being recalled, and
migrating more of them into the linter is the direction of travel: a rule that fails a build
beats a rule in a paragraph.

On a surface with no linter — Claude Design, chat — 🔒 does not mean *handled*, it means
*this one is mechanical, so check it first and state the number*. Occupancy, the safe zones,
the type floor, contrast and the element count are all readable off the design without
running anything.

---

## The diagnosis, before the list

> Most bad static design is a **point-of-view problem, not a styling problem.** The frame
> weights everything equally because nothing decided what the frame was for.

Fix that and roughly half the visual tells below disappear on their own. The rest are
habits.

---

## A — Containers 🔒

**Cards, panels, bordered boxes, translucent rectangles on a field, drop shadows, glows,
border radius above 10px.**

*Seen in:* `throwback-stat-cards.png` (two translucent rounded panels),
`infographic-six-panel.jpg` (every element in a rounded bordered box),
`aiherway-inline-editing.jpg` (a box inside a box).

*Why it fails:* the ground is already the container. A second one puts a frame inside a
frame and signals that the content was not confident enough to sit on the field.

*Instead:* put the element on the ground. Where separation is genuinely needed, use a
hairline rule or a 2px gap in the ground colour — never a border.

## B — Dead canvas 🔒

**Content occupying less than 60% of the frame, with the remainder empty and unloaded;
content marooned in a middle band with dead space above and below.**

*Seen in:* `aiherway-label-table.jpg` (~40%), `aiherway-dark-quote.jpg` (~45%),
`throwback-stat-cards.png` (empty top and bottom fifths), all three Socceroos tiles (dead
bottom quarter).

*Why it fails:* it reads as a template that the content failed to fill. At thumbnail size
the frame looks like it is loading.

*Instead:* make the type bigger. Six of the ten rejected examples would be fixed by
doubling the display size and nothing else. If the content genuinely will not fill the
frame, the frame is the wrong format.

## C — Chrome tax 🔒

**More than one persistent brand element per frame.**

*Seen in:* the three `aiherway-*` slides — logo lockup, a second lockup line, a handle and
a pagination counter, on frames carrying two pieces of content.

*Why it fails:* furniture competes with content for the same attention, and loses nothing
by being removed.

*Instead:* one mark, one fixed corner, ~3% of canvas width. The serial running head is the
only permitted addition (see `02-typography`).

## D — Typeface soup 🔒

**More than two families; a decorative serif italic dropped in for flavour; a serif or
display face on a hero figure.**

*Seen in:* `throwback-stat-cards.png` (four families, serif hero figures),
`socceroos-top-ryde.jpg` (a serif italic "Piazza" inside a geometric-sans system),
`infographic-radial-8-steps.jpeg` (serif, sans and italic mixed per block).

*Why it fails:* each additional family is a register the reader has to interpret, and
nothing in the content asked for it. A serif hero figure reads loose and old-fashioned at
display size.

*Instead:* two families, three registers, hero figures in the sans.

## E — Unstructured scale 🔒

**Sizes off any ratio; more than three registers; text below 1.25% of canvas height.**

*Seen in:* `infographic-six-panel.jpg` (8+ sizes), `aiherway-label-table.jpg` (six type
treatments), `infographic-radial-8-steps.jpeg` (illegible at thumbnail).

*Why it fails:* a scale is what makes hierarchy legible without being read. Independent
sizes make disorder more visible, not less.

*Instead:* declare one ratio — Perfect Fourth by default — and put every size on it.

## F — Decoration standing in for meaning 🔒

**Decorative gradients, glows, oversized quote glyphs, ornamental asterisks, concept icon
sets, numbered circles, 3D or isometric chrome, dashed connectors between panels.**

*Seen in:* `synthwave-gradient-hero.jpg` (purple gradient, glow bloom, sparkle emoji),
`aiherway-dark-quote.jpg` (giant quote glyph above an already-quoted passage),
`infographic-six-panel.jpg` (numbered circles, tick/cross icons, 3D blocks, ornamental
asterisk), `infographic-radial-8-steps.jpeg` (a decorative numeral holding the optical
centre).

*Why it fails:* each device asks for attention and returns nothing. Together they are what
"AI slop" describes.

*Instead:* the only permitted gradient is a type plate at a frame edge. Emphasis comes from
size and one accent. If a graphic element cannot be given a job in one sentence, delete it.

## G — Accent inflation 🔒

**The accent colour applied to more than one element class; a colour assigned per section,
per rank or per position.**

*Seen in:* `socceroos-canopy.jpg` and `socceroos-top-ryde.jpg` (yellow on rule, pill,
headline, bullets, address, footer, mark — seven classes), `infographic-six-panel.jpg` (a
hue per panel).

*Why it fails:* an accent everywhere is a second brand colour and points at nothing. Colour
assigned by position repaints when the content reorders, which proves it was carrying no
meaning.

*Instead:* one accent, one element class, one emphasis device per frame.

## H — Template sameness 🔒

**Consecutive frames in one set that are identical but for the words.**

*Seen in:* `aiherway-inline-editing.jpg` / `aiherway-label-table.jpg` /
`aiherway-dark-quote.jpg` (slides 5, 6, 7 of 12); `socceroos-canopy.jpg` /
`socceroos-top-ryde.jpg`.

*Why it fails:* a set exists to build an argument across frames. Identical frames make the
swipe pointless.

*Instead:* hold ground, type, margin, mark and accent constant; vary the composition on
every frame. Blur the set — no two frames may share a shape. See `05-series`.

## I — Contrast failure 🔒

**Text below 4.5:1 against its field. Marks below ΔL 25 against each other or the field.**

*Seen in:* `throwback-stat-cards.png` — the top-right label and the entire footer row are
effectively invisible, at roughly 1.5:1.

*Why it fails:* it is invisible on the large bright display where it gets signed off, and
unreadable on the phone where it gets seen.

*Instead:* run both measures, and check the *smallest* text rather than the largest. ΔL
separates marks; it does not make text readable.

## N — Mid-dot metadata chains 🔒

**Footnotes or metadata strung together with mid-dots — `Source · Date · Sample`.**

Shared with the editorial-motion house rules, where it is stated but **not** yet enforced —
`check-artifact.py` has no mid-dot check, so a motion artifact can still ship one. This
file is the enforced copy. Static frames are where metadata chains breed anyway, because a
footer feels like somewhere to put things rather than something to design.

*Why it fails:* the mid-dot is a separator that ranks nothing. Three facts of different
importance get one visual weight and one line, so the reader has to parse a string instead
of reading a hierarchy. It is the typographic form of anti-pattern **J** — a list standing
in for information design.

*It is also the mechanism behind the sloppy footer.* Once metadata is a chain, it reads as
one undifferentiated lump, gets set small and grey to fit, and lands in the safe zone. Three
anti-patterns arriving together, all from one punctuation choice.

*Instead:* line breaks, commas, or plain labelled lines. If two facts matter, give them two
lines. If one matters more, size it that way. If a fact matters enough to be on the frame at
all, it is content — see **S**.

## S — Safe-zone violation 🔒

**Text within 150px of the top or bottom edge of a 4:5 tile.**

*Why it fails:* the profile grid crops 4:5 to a centre square and carousel dots overlay the
bottom edge, so anything down there is invisible to a large share of readers. It is the
failure that looks fine in the file and disappears in the feed.

*The tell it produces:* essential information demoted to a footer. A time, an address or a
source line set small, in muted grey, on the last baseline — treated as furniture because
it was placed where furniture goes.

*Instead:* derive the footer position from the safe line, not the canvas edge, and anchor
content stacks to the bottom so they cannot grow into the crop. If a fact matters, it
belongs in the content at reading size — not in the margin.

## fit — Overflow and collision 🔒

**Content running past a frame edge; two text blocks overlapping.**

*Not seen in the rejected set* — it is the failure that generated static work produces
under its own steam, and it was caught building this system's own test artifacts twice.

*Why it fails:* a fixed canvas has no scrollbar to reveal what fell off the bottom, so
overflow is silent. It renders as a headline that stops mid-word. An absolutely-positioned
block whose text grew by one line is the usual cause, and nothing else on this list would
notice.

*Instead:* measure the tallest state, not the current one. Run the linter before looking,
and look after running it — the two catch different things.

## O — The disguised legend

**A stacked list of value–label pairs sitting under a chart, standing in for direct
labelling.**

*Not in the rejected set* — it is what generated work produces when it obeys "never a
legend" without knowing what replaces one. Caught building this system's own data tiles.

*Why it fails:* it is a legend with the swatches removed. The reader still has to map
marks left-to-right onto text top-to-bottom and hold the mapping while reading. It looks
tidy and orderly, which is exactly why it survives review — the failure is invisible until
someone tries to answer a question from the frame.

*Instead:* label inside the mark where it fits, and run a hairline leader from the mark to
the label where it does not. See `04-graphics-imagery`.

## P — Nested marks sized by percentage

**Sub-segments inside a grouped mark sized with `%` or `calc(var(--v) * 1%)`, so they
resolve against their group rather than the plot.**

*Why it fails:* it is anti-pattern **fit** for data — silent, plausible and invisible in
review. The sub-segments divide correctly relative to each other and land at a fraction of
their true length against every other mark on the frame. Nothing looks broken. Caught twice
on the same chart: once in HTML, once rebuilt in Canva.

*Instead:* `flex: var(--v) 1 0` with `min-width: 0`, and gaps subtracted before
distribution. Then verify on the rendered file, not the source: pixel width ÷ value is one
number across every mark.

## Q — The figure that lost to its own headline

**A hero figure set at or below the display size on a frame whose job is the number.**

*Why it fails:* scale is what tells the reader which element is the content. A percentage
set smaller than the sentence introducing it turns a data frame into a text frame with an
illustration, and the reader reads the words instead of the number. It is the most common
reason a technically-correct chart tile feels weaker than a worse one beside it.

*Instead:* 1.2–2× the display size, unit at half the digit size where width is tight. See
`02-typography`.

## J — List-as-layout

**Bullets, label/value tables or numbered rows substituting for information design.**

*Seen in:* both Socceroos venue tiles (four bullets carrying the entire frame),
`aiherway-label-table.jpg` (a three-row SITTING / BLOCKING / BECAUSE table).

*Why it fails:* a list ranks nothing and emphasises nothing. It transfers the work of
deciding what matters onto the reader.

*Instead:* decide which item is the point and set it at display size. The others become a
single supporting sentence, or a second frame. A three-row table is usually one sentence.

## K — Cutout crimes

**Rectangular crops through a subject; cutouts overlapping copy; subjects cropped at the
canvas edge without compositional intent; uniform-scale cutouts.**

*Seen in:* `socceroos-cover-cutout.jpg` — the scarf cut square mid-fabric, the subject cut
off mid-torso at the frame edge, and the scarf overlapping the CTA pill.

*Why it fails:* a visible rectangular cut announces that the image was pasted rather than
composed, and an overlap with copy makes both illegible.

*Instead:* cut on the silhouette, vary the scale, keep copy clear, and break the frame edge
deliberately. See `good example: nyt-cutout-collage.png`.

## L — No reading order

**Radial or orbital layouts; grids of equal-weight panels; sequences that need arrows or
numbers to be followed.**

*Seen in:* `infographic-radial-8-steps.jpeg` (eight steps around a circle, joined with
arrows), `infographic-six-panel.jpg` (six equal panels, numbered because the layout does
not imply order).

*Why it fails:* if the layout needed numbering, the layout failed. A wheel has no beginning.

*Instead:* sequences are vertical, or they are separate frames. Size creates order.

## M — Centred by default 🔒

**Every element on the vertical centreline with no compositional reason; a single
left-aligned column with an empty column beside it.**

*Seen in:* `synthwave-gradient-hero.jpg` (centred stack), both Socceroos venue tiles (one
narrow left column, one empty right column).

*Why it fails:* centring is a choice with a specific effect — ceremony, symmetry, a single
statement. Applied by default it flattens every frame to the same shape.

*Instead:* anchor to a third and load the opposite side. Reserve centring for the cover.

## R — The hairline above the source line

**A rule drawn across the foot of the frame to separate the source line from the content.**

*Why it fails:* it is a generated-design signifier, and a strict ban. The source line is
already separated — by position, by size, by tone. The rule adds a second separation to a
distinction the reader had made without help, and what it actually announces is that the
layout did not trust its own hierarchy. It is the footer equivalent of a card: a container
drawn around something the ground was holding perfectly well.

The near misses fail the same way — a rule under the headline, a rule between a chart and
its caption, a rule down the gutter.

*Instead:* nothing. Set the source line small and muted, above the safe line, and let the
space do the work. A hairline is legitimate only where it does a job no other element is
doing: seating objects on a groundline, or a span rule across the marks it covers.

## T — The drawn tear 🔒

**A torn or ragged edge built as a vector path — `clip-path: polygon(...)`, a hand-drawn
`<path>`, a zig-zag, a "rough edges" filter preset.**

*Why it fails:* a real tear has structure at two scales at once — the long wander of the
fibre and the fray along it. A polygon has vertices, and the eye counts them. Six or ten
straight runs between corners reads as a shape pretending to be paper, which is worse than
a clean rectangle: it is a clean rectangle that has been caught trying.

*Instead:* a tear is a **cut photograph** or a **turbulence-displaced mask** — long
wavelength across the tear, short down it, one seed per fragment, so the picture inside
stays undistorted. See `04-graphics-imagery`. Fires as **F**.

## U — The unfocused frame 🔒

**Nothing on the frame differs from everything else in any one property. Five saturated
colours; four photographs at the same density; every element equally worked.**

*Why it fails:* the eye has nowhere to land, so it reads the frame as a texture rather
than as a statement. This is the failure behind most frames that pass every other rule and
still feel flat — and it is almost never fixed by making the intended subject louder,
because the thing drowning it is still there.

*Instead:* name the carrier — saturation, register, density, texture or negative space —
and **suppress the field rather than amplifying the subject**. See `07-focal-point`.

*What the check sees:* CSS colour only, grouped by colour rather than by element. It
cannot sample a photograph and it is blind to four of the five carriers, so it is a
**warning**: a frame that fails it may have a good focal point the check cannot reach.

## V — The pinboard 🔒

**Three to seven photographic elements on one frame — too many for A or C, far too few for
B — arranged on a field.**

Three, not two: Structure C's ground-mass build puts exactly two on a frame — the halftoned
subject and the smooth-duotoned mass that seats it — and that is prescribed, not banned
(`08-layered-editorial`). The check counts from three for that reason.

*Seen in:* this system's own `collage.html` / `collage-v2.html` — four rectangular photo
crops behind ragged masks: 1.6× scale disparity where the references run 5×, no overlap, no
occlusion, nothing breaking an edge, neither far corner held.

*Why it fails:* Structure B depends on scale disparity and occlusion that only arrive with
roughly ten cut elements. Below that the frame cannot reach either, and what arrives is
photographs arranged politely — a pinboard. It reads tidy, which is why it survives review,
and it is the failure the maximalist tiles kept producing because the assets did not exist.
Faking the missing density with vector shapes, halftone fields and scattered discs is
precisely what reads as Canva.

*Instead:* count the assets before designing. One strong photograph → **A**. One cuttable
subject and a glyph vocabulary → **C** (`08-layered-editorial`), which reaches collage energy
with one cutout. Roughly ten cutouts → **B**. See the routing table in `04-graphics-imagery`.

*What the check sees:* it counts `<img>`, `<picture>`, `<video>`, `<canvas>` and raster
`background-image`s that are visible on the frame. It cannot tell a portrait used as a data
unit from a pinboard, and it cannot see overlap or scale — so a frame with eight or more
elements passes the count and has still not been shown to be a B.

## W — Copy in a corner 🔒

**A headline parked in one quadrant with the rest of the canvas loosely filled.**

*Why it fails:* it passes the occupancy floor because pictures made up the difference, and
still reads as an afterthought. The Vox covers give the headline 35–55% of the canvas as
one block.

*Instead:* the copy occupies a **zone** — 28% of the usable canvas on a type-led frame,
18% where a picture carries it. Error on type-led frames, warning on picture-led ones,
where the picture is legitimately doing the work.

---

## What the linter cannot see

Two blind spots, both real, both worth knowing before trusting a clean run:

- **Contrast is checked against the DOM ancestor, not against what visually sits behind.**
  An absolutely-positioned label that overlaps a band earlier in the document reports its
  contrast against the page ground, and passes. Caught this way once: a muted mark sitting
  on a cream band, measured against the dark green behind it.
- **It does not judge design.** It cannot tell you the composition is weak, the finding is
  dull, or the frame is a competent arrangement of house devices. A clean run means nothing
  is mechanically broken — it does not mean the piece is good.

Run the linter before looking, and look after running it. They catch different things, and
neither substitutes for the other.

## The three-question check

Any "no" is a fix, not a ship.

1. At 200px wide, is the finding still legible?
2. Could someone state the point out loud after two seconds?
3. Would this frame be interchangeable with the last piece after a content swap?

Question 3 is inverted: **"yes" is the failure.** The palette and type are supposed to be
interchangeable — that is what makes a family. The composition and the device are not.

## Then remove one thing

Before shipping, take out the element doing the least. Texture, grain, torn edge, rule,
chip, plate, pagination — each is defensible alone and the sum is noise.

If removing it costs nothing, it was decoration. If the frame gets worse, put it back and
remove the next-least thing instead. Something always comes out.
