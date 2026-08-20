<!-- Vendored copy. Master: Static design content/static-design-system/principles/01-layout.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 01 — Layout

Where things go and how much of the frame they occupy. Settled before anything is styled.

Grid theory, canvas selection, proportional derivation and the four type scales live in
the `layout-composition` skill and are not repeated here. This file covers what is
specific to a **fixed static canvas that will be seen at thumbnail size in a feed**.

---

## The occupancy floor

**Content occupies at least 60% of the *usable* canvas.** Measured as the union of the
bounding boxes of every visible element, against the area between the safe zones — not
against the total frame.

The denominator matters more than it looks. On a 1080×1350 tile the 150px safe zones top
and bottom take 22% of the height out of play, so scoring against the whole frame quietly
asks for 77% of what is actually available in order to report 60%. Content that lands in
the safe band is not counted: bleed art is welcome to cross it, but it cannot be the thing
that fills the frame.

The ground is excluded by **role**, not by area — a full-bleed photograph is the element
carrying the frame, not the surface under it, and an area threshold cannot tell the two
apart.

This is the single most reliable separator between the good and bad sets. Six of the ten
rejected examples are text frames using 35–50% of the canvas. None of the seventeen good
ones falls below about 70%.

Empty canvas is only permitted when it is **loaded** — when it is on one side of the
composition and something is anchored against it. Emptiness distributed evenly around a
floating block is not margin, it is an unfinished frame.

The test: could you crop 20% off any edge and lose nothing? Then the frame is 20% too big
for its content, and the fix is to make the content bigger, not to move it around.

### The type zone is measured separately

A frame can clear the 60% floor and still have no type zone, because pictures made up the
difference. **The copy occupies a zone, not a corner** — 28% of the usable canvas on a
type-led frame, 18% where a picture carries it, measured as the union of the text boxes.

The Vox covers give the headline 35–55% as one block of tight caps. A headline parked in a
bottom-left quadrant with the other three quarters loosely filled passes occupancy and
still reads as an afterthought. See `07-focal-point`.

> `bad example: aiherway-label-table.jpg` — content in the top 40%, two-thirds of the
> canvas empty, a caption stranded at the bottom edge to justify the height.
>
> `good example: vox-text-only-slide.png` — the same job done at twice the type size,
> whitespace collected into one block beneath the shortest line so it reads as a margin.

## Anchor to a third, load the other side

Place the primary block against one third-line and put the weight of the composition on
one side. Then let the opposite side carry the emptiness.

Three arrangements cover almost everything:

| Arrangement | Use it for |
|---|---|
| Image upper two-thirds, copy lower third | Covers, illustration-led posts |
| Copy upper third, image lower two-thirds | Second and subsequent slides, so the set alternates |
| Copy left, image breaking the right edge | Frames with a cutout or a shape rather than a scene |

**Centring is legitimate and should be rare.** It is right for a cover, a ceremonial
single statement, or a symmetrical mark-plus-headline lockup — and it should then be the
only centred frame in the set. Centring every frame is how `synthwave-gradient-hero.jpg`
happens.

## Break the frame

At least one element bleeds off at least one edge in most frames. Illustrations,
photographs, cutouts, shapes, charts.

This is what makes a composition read as a window onto something larger rather than a
slide with clip art on it. Guardian's cutouts break all four edges; Vox's chartreuse shape
explodes off the right; NYT's illustrations run to the edge below the headline.

A chart that continues off the right edge is also an invitation to swipe — see `05-series`.

## No containers

Elements sit **directly on the ground**. There is no card, no panel, no bordered box, no
translucent rectangle, no drop shadow, no glow.

The ground is already the container. Adding a second one puts a frame inside a frame and
tells the reader the content was not confident enough to stand on the field.

Permitted, and the complete list:

- A **hairline rule** where a rule does real work — seating objects on a groundline, or
  spanning the marks it covers. **Never above a source line:** that rule separates nothing
  that position, size and tone had not already separated, and it is a generated-design
  signifier. See `06-anti-patterns` **R**.
- A **highlight block** behind one word (see `03-colour-and-ground`).
- A **chip** carrying a direct data label, sitting on the mark it names.
- A **type plate** at a frame edge — a hard-edged band or a bottom-anchored gradient sized
  to the copy, used only when type must sit over a photograph and no dark region exists.

Border radius above 10px is banned outright. Rounded cards are the loudest generated-design
tell in the set.

## Zone the canvas before placing marks

Derive the drawing band from the copy blocks rather than from fractions of the frame
height. Measure the **tallest** headline and the **tallest** footer across the whole set,
not the current one, or the marks will jump between slides.

```js
const PAD = 18;
const bandTop = TOP_INSET + tallestHeadlineHeight + PAD;
const bandBot = H - BOT_INSET - tallestFooterHeight - PAD;
```

Everything that is not copy — chart, illustration, cutout — is sized and centred against
that band. This is what keeps a five-slide set feeling like one object.

## Safe zones

The margin is where the frame ends. The safe zone is where the *platform* ends, and they
are not the same number.

**Nothing a reader needs sits within 150px of the top or bottom edge** of a 1080×1350 tile
— about 11% of canvas height. Two things eat that band:

- **The profile grid crops 4:5 to a centre square.** Anyone arriving at the account sees a
  1080×1080 crop, so the top and bottom 135px are simply gone. A time, an address or a
  source line parked down there does not exist for that reader.
- **Carousel page dots overlay the bottom ~60px** in feed.

Bleed art may cross the safe zone freely — that is what bleeding is for. Text may not, and
the source line is text. It is tempting to call the footer inconsequential and let it sit
below the line; it is the one piece of copy `04-graphics-imagery` calls non-negotiable, and
below the line it does not exist for anyone arriving from the profile grid. Raise it.

This is the same nested-crop logic as multi-format delivery: a frame is always being viewed
inside a smaller frame you did not choose. Derive the footer position from the safe line
rather than the canvas edge:

```css
:root{ --margin:80px; --safe:150px; --foot:264px; } /* safe + mark height + gap */
.mark  { bottom:var(--safe); }
.stack { bottom:var(--foot); }   /* clears the mark, cannot grow into the crop */
```

**Anchor stacks to the bottom, not to a fixed top.** A fixed `top` plus one extra wrapped
line is how copy silently leaves the frame — it happened twice building this system's own
test artifacts, and neither time was visible until the PNG was opened.

## Margins

One margin value, derived from the base unit, held on all four sides of every frame in the
set. Bleeding elements ignore it deliberately; copy never does.

At 1080px wide, 64–80px is the working range. Below 48px the frame reads as cramped at
full size; above 120px the occupancy floor starts to fail.

## Reading order

Every frame has one, and it is created by size, not by numbering.

If a layout needs numbers, arrows or connectors to tell the reader where to look next, the
layout has failed — see `bad example: infographic-radial-8-steps.jpeg`, where eight
steps are arranged around a circle and then joined with arrows to repair the fact that a
wheel has no beginning.

Sequences are vertical or they are separate frames. Never radial, never a grid of
equal-weight panels.

## Self-check

- Does content cover at least 60% of the canvas between the safe zones?
- Are both far corners held, or is the composition floating in the middle?
- Is the empty area on one side, with something anchored against it?
- Is the primary block on a third-line, or was it centred by default?
- Does at least one element break an edge?
- Is anything sitting in a box that the field could have held?
- Is any border radius above 10px, or any shadow present?
- Could you state the reading order without following an arrow?
- Do the margins match every other frame in the set?
