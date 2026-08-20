---
name: static-composition
description: Composition, ground and colour for fixed-canvas static design — where content sits on the frame, how much of the frame it fills, what colour the field is, and how many colours do what. Use whenever building a social tile, feed post, carousel frame, poster, quote card, stat tile or chart card. Covers the 60% occupancy floor, anchoring to thirds, breaking the frame, the no-container rule, colour as roles with exactly one accent, contrast floors, gradients and texture. Pair with static-type-graphics for the words and the pictures.
---

# Static composition, ground and colour

Where things go, how much of the frame they fill, and what colour the field is. Settled
before anything is styled.

Grid theory, canvas selection and the four type scales belong to **layout-composition**
from the `editorial-motion` plugin and happen first. If that plugin is not installed, the
compact substitute at the bottom of this file covers the minimum.

Full detail:

- `references/01-layout.md` — occupancy, thirds, frame-breaking, containers, zoning,
  margins, reading order.
- `references/03-colour-and-ground.md` — role slots, grounds, the accent rule, emphasis
  devices, contrast floors, categorical colour, gradients, texture.
- `references/07-focal-point.md` — the focal point as a contrast of kind, the
  five carriers, and the type zone. Read it before choosing values: a frame can
  pass every other rule here and still read flat.

---

## The four rules that carry most of it

**1. Content covers at least 60% of the canvas.** Measured as the union of visible element
bounding boxes against total canvas area. This is the single most reliable separator
between good and rejected static work: six of ten rejected examples sit at 35–50%; none of
seventeen reference examples falls below ~70%.

Empty canvas is permitted only when it is **loaded** — on one side, with something anchored
against it. Emptiness distributed evenly around a floating block is an unfinished frame.

The test: could you crop 20% off any edge and lose nothing? Then the content is too small,
and the fix is to make it bigger, not to move it around.

**2. Anchor to a third and load the other side.** Three arrangements cover nearly
everything: image upper two-thirds with copy below; copy upper third with image below; copy
left with a shape or cutout breaking the right edge. Centring is right for a cover, a
ceremonial single statement, or a symmetrical lockup — and should then be the only centred
frame in the set.

**3. Break the frame.** At least one element bleeds off at least one edge in most frames.
This is what makes a composition read as a window onto something larger rather than a slide
with clip art on it.

**4. No containers.** Elements sit directly on the ground. No card, no panel, no bordered
box, no translucent rectangle, no drop shadow, no glow, no border radius above 10px. The
ground is already the container.

The complete list of permitted enclosures: a **hairline rule** doing real work; a
**highlight block** behind one word; a **chip** carrying a direct data label on the mark it
names; a **type plate** at a frame edge where type must sit over a photograph with no dark
region.

## Colour as roles

Fill from the client's brand. Do not invent a palette.

| Role | Job | Count |
|---|---|---|
| `ground` | The field everything sits on | 1 per frame |
| `ink` | Headlines, primary marks | 1 |
| `muted` | Attribution, source, axis labels | 1 |
| `accent` | The one thing that proves the point | **exactly 1** |
| `secondary` | The opposing side, diverging data only | 0–1 |

**Minimum viable brand: one typeface in the right register, one colour that connects,
everything else neutral.** Past that, extra brand assets stop adding recognition and start
making the work look like a guidelines document.

**The ground is never white.** Pure `#FFFFFF` and `#000000` are both banned as page fields.
Use a warm or cool off-white, a near-black at `#1A1A1A` or above, a desaturated story tint,
or a saturated brand field with content inset against it.

**One accent, one element class.** One bar accented among neutral bars; one word
highlighted; one saturated line among grey lines. The moment a second element class takes
the accent, the frame loses its focal point. If two things matter equally, they are two
frames.

**One emphasis device per frame** — a highlight block behind a single word, or a colour
change on one phrase, or one accent mark in an otherwise neutral illustration. Not three
colours inside one sentence.

## Contrast — run both measures

| | Measure | Floor |
|---|---|---|
| Mark vs mark, mark vs field | ΔL | ≥ 25 |
| Any text vs its field | contrast ratio | ≥ 4.5:1 |

ΔL separates marks; it does not make text readable. A muted grey source line on cream can
sit at ΔL 30 and 2.5:1 — separable, unreadable. Check the *smallest* text, not the largest,
and check marks against the field before checking them against each other.

This failure is invisible on the large bright display where it gets signed off.

## Gradients and texture

Gradients are banned with one exception: **a type plate at a frame edge**, sized to the copy
block, used when type must sit over a photograph that has no dark region. Not a full-frame
dim, not a background wash, not a fill on a button or a data mark.

Texture is required. One layer, not three. Grain at **4–6%** — at 10% it reads as a broken
image. Paper scans go under the marks and copy and above the colour field, at 18–30%
opacity, multiply on light grounds and soft-light on dark. Check at 200px: grain turns to
mud at thumbnail size.

## Compact substitute for layout-composition

Use only when the `editorial-motion` plugin is unavailable.

**Canvas:** 4:5 at 1080×1350 is the default for feed and carousel — ~25% more screen than
1:1. Use 1:1 for ad units and grid-sensitive sets, 9:16 for stories (one statement only),
16:9 for slides. Comparison needs width; sequence suits height. Re-compose per format;
never scale one master.

**Grid:** one hero image and one message → rule of thirds. Repeating components → modular,
12 columns. Long-form reading → manuscript, ~65 characters. Establish it before placing
content.

**Spacing:** derive everything from one base unit rather than picking values independently.

```css
:root{ --u:8px; --pad:calc(var(--u)*3); --gap:calc(var(--u)*4); --section:calc(var(--u)*10); }
```

**Type scale:** one ratio, declared once. Perfect Fourth (1.333) is the static default;
Golden Ratio (1.618) for type-only frames; Major Third (1.25) for chart frames. Human-scale
readability outranks mathematical purity — if the system produces 13px body text, break the
ratio.

## Self-check

- Does content cover at least 60% of the canvas?
- Is the empty area on one side, with something anchored against it?
- Is the primary block on a third-line, or was it centred by default?
- Does at least one element break an edge?
- Is anything in a box the field could have held? Any radius above 10px, any shadow?
- Is the ground tinted rather than white or pure black?
- Is the accent on exactly one element class, with exactly one emphasis device?
- Does the smallest text clear 4.5:1? Does every mark clear ΔL 25 against the field?
- Is there a gradient that is not a type plate?
- Exactly one texture layer, grain at 4–6%?
