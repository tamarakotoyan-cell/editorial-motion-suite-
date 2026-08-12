---
name: layout-composition
description: Layout, grid and proportion decisions for any generated design — before placing content, choosing sizes, or writing a type scale. Use whenever a composition needs structure: slides, tiles, posters, reports, dashboards, social graphics, infographics, carousels, landing pages, charts. Covers rule of thirds, modular grids, manuscript grids, root-rectangle proportions, proportional derivation, and the four type scales (Major Second 1.125, Major Third 1.25, Perfect Fourth 1.333, Golden Ratio 1.618). Apply proactively — the person asking usually has not specified a layout, and choosing one deliberately is the job.
---

# Layout and composition

Most weak generated design is a layout failure that got styled. Elements are
centred by default, sized independently of each other, and spaced by whatever
number came to mind. This skill decides **where things go** and **how big they
are relative to each other**, before any styling happens.

Apply it **without being asked**. Someone requesting "a slide about X" has not
chosen a grid, and will not think to. Choosing one deliberately is the work.

---

## Order of decisions

Run these in order. Each one constrains the next.

0. **Where will it be seen, and what must it hold?** → picks the canvas format
1. **What is the content's job?** → picks the grid
2. **Where is the focal point?** → picks the composition
3. **What is the base unit?** → picks spacing and sizing
4. **How much hierarchy is needed?** → picks the type scale

Skipping to step 4 is the most common mistake — a type scale on an unstructured
layout just makes the disorder more legible. Skipping step 0 is the quieter one:
a grid chosen before the canvas is a grid chosen against an unknown aspect ratio.

---

## Choosing the canvas format

Aspect ratio is the first decision, and it is made from two inputs: **where the
piece will be seen** and **what it has to hold**. Not from habit, and not from
whatever the last file was.

| Format | Where it lives | What it holds |
|---|---|---|
| 9:16 (1080×1920) | Stories, Reels, TikTok, Shorts | One statement. A headline plus one mark. Vertical stacks of 2–3 elements, nothing side-by-side |
| 1:1 (1080×1080) | Feed posts, carousels, ad units | One chart or one stat tile with a title and a source line. The safest general-purpose social canvas |
| 4:5 (1080×1350) | Instagram/Facebook feed at maximum height | Same as 1:1 but with room for a longer headline or a taller chart. Prefer it over 1:1 in-feed — it occupies ~25% more screen |
| 16:9 (1920×1080) | Slides, decks, YouTube, screens in a room | Side-by-side comparison, a chart with an annotation column, three-across modules |
| 4:3 (1440×1080) | Documents, older projection, deliberate letterboxing | Denser reading than 16:9; the format when the content is closer to a page than a screen |

Two rules of thumb. **Comparison needs width** — anything asking the eye to put
two things next to each other wants 16:9 or 4:3, and forcing it into 9:16 turns
a comparison into a list. **Sequence suits height** — a build, a countdown or a
stacked argument reads better vertical.

### Letterboxing as a register signal

Letterboxing is usually treated as a failure to fill the frame. Used
deliberately it is a register signal: the bars say *this is not native to the
feed*, and the eye reads that as cinema rather than social.

The worked example is in `../motion-system/references/sources.md` §11 — a 4:3
piece posted into a 9:16 feed. The observation recorded there is that the
letterboxing is the point, and it reads as cinema rather than social.

To use it: pick the inner format for its own reasons (4:3 or 16:9 because the
content is a place, a comparison, or a wide frame), then centre it in the
delivery canvas on a flat ground — near-black, or the field colour. Bars stay
**symmetrical and hard-edged**. Blurred self-extension in the bars (see
**imagery-motion**) is a different device with the opposite intent — it hides the
letterbox rather than declaring it. Do not mix the two in one piece.

Do this once per piece, never per frame. Letterboxing that comes and goes reads
as an export error.

### One piece, several formats

**Re-compose per format. Never scale one master.** A 16:9 slide reduced to fit
9:16 gives you 8px type in a band of empty ground, and a 9:16 tile stretched to
16:9 gives you a column of content marooned in the middle.

Re-composing means the same content, the same palette and the same type scale,
but a grid decision made again for each canvas. This is the same rule as
elements moving **between modules** rather than to arbitrary coordinates — the
modules are what survives the format change, not the pixel positions. Hold
constant: the finding, the accent, the base unit, the type scale ratio. Let vary:
the number of columns, the reading order, which elements are present at all.

Practically:

- Decide the **primary** format first and design it properly. The others are
  derived, not co-equal.
- Drop elements rather than shrinking them. A 9:16 cut of a 16:9 chart usually
  loses the annotation column and keeps the mark.
- Re-run the type scale against the new width. The ratio holds; the base does not
  — 16px base on a 1920px slide is not 16px base on a 1080px tile.
- Check each format at 200px wide independently. Passing in one proves nothing
  about the others.

---

## Choosing a grid

| Content | Grid | Because |
|---|---|---|
| One hero image, one message | Rule of thirds | Needs a focal point, not organisation |
| Repeating components, multi-asset sets | Modular | Needs alignment and repeatability |
| Long-form reading, reports, articles | Manuscript | Needs a stable reading area |
| Geometric, nested, poster-like | Root rectangle | Needs proportional subdivision |

These combine. A report uses a manuscript grid for its body and a modular grid
for its data pages. Pick the primary one first.

### Rule of thirds

Divide the canvas 3 × 3. The four intersections are candidate focal points.

Place primary subjects and visual anchors on **intersections or third-lines**
rather than centring them by default. Preserve negative space around the focal
point — the empty area is doing work, not going to waste.

```css
.thirds { display:grid;
          grid-template-columns:repeat(3,1fr);
          grid-template-rows:repeat(3,1fr); }
/* anchor at the upper-left intersection */
.focal  { grid-column:1 / 3; grid-row:1 / 3; align-self:end; justify-self:end; }
```

Centring is a legitimate choice for symmetrical, ceremonial or single-word
compositions. It should be a decision, not the default that happens when no
decision was made.

**In motion:** move between intersections rather than to arbitrary points. A
subject travelling from one third-line to another reads as a deliberate journey.

### Modular grids

Repeating columns and rows forming consistent modules. This is an
**organisational** system, not a compositional shortcut — it controls alignment,
repetition, component sizing and consistency across a set.

Establish the grid **before** placing content. Align text, images and graphic
elements to shared rows and columns. Hold the same grid across related frames
and assets; deviate only when the deviation has a compositional purpose you
could state out loud.

```css
.modular { display:grid;
           grid-template-columns:repeat(12, 1fr);
           gap:var(--gap); }
.card    { grid-column:span 4; }     /* consistent module widths */
```

**In motion:** elements move **between modules**, not to arbitrary coordinates.
This is what makes a rearrangement read as a system reorganising itself rather
than objects scattering.

### Manuscript grids

One dominant content rectangle inside deliberate margins — the book page. It
controls reading width, margins, text density and long-form consistency.

The principle is not "use one column". It is **a stable reading area that makes
extended content comfortable**.

- Running text near **65 characters** per line.
- Margins generous enough to feel intentional — a cramped manuscript grid is
  just a full-bleed page.
- Do not add columns or decorative elements unless they improve comprehension.

### Root rectangles

Ratios of √2 (1.414), √3 (1.732), √4 (2). **√2 is the one that matters** — it is
the A-series paper proportion, and its defining property is that halving it
preserves the proportion (A4 → A5 → A6).

That makes it the right tool for **nested and scalable** compositions: a panel
subdivides into panels of the same shape, indefinitely.

Use these ratios to establish relationships between canvas regions rather than
introducing arbitrary rectangular dimensions.

---

## Proportional derivation

**Prefer related dimensions to independent ones.** Where a layout has a panel,
its height should influence its width, its padding, its headline size and the
space around it — all traceable to one base value.

```css
:root{
  --u: 8px;                        /* base unit */
  --pad:      calc(var(--u) * 3);  /* 24 */
  --gap:      calc(var(--u) * 4);  /* 32 */
  --section:  calc(var(--u) * 10); /* 80 */
}
```

Le Corbusier's Modulor is the canonical version of this idea — human proportion
tied to Fibonacci and golden-ratio relationships. **Do not implement the
historical Modulor dimensions as a default system.** The transferable principle
is derivation from a coherent relationship, not those specific numbers.

**Guardrail:** human-scale readability and usability outrank mathematical
purity, always. If the proportional system produces 13px body text or a
40-character line, the system is wrong for this canvas — not the reader. Break
the ratio and keep the accessibility.

---

## Type scales

Set a base (commonly 16px) and multiply. Never pick sizes independently —
16 / 19 / 27 / 31 / 42 is the signature of a layout nobody structured.

**More information density → smaller jumps between levels.**

### Major Second — 1.125
`16 · 18 · 20 · 23 · 26 · 29 · 32`

Restrained hierarchy. **Dashboards, interfaces, dense information, data
visualisation, small-format typography.** When many levels must coexist without
any of them shouting.

*(Note: 1.125 is the Major Second. "Double octave" is a different, much larger
ratio at 4:1 — the two terms are not interchangeable.)*

### Major Third — 1.250
`16 · 20 · 25 · 31 · 39 · 49 · 61`

Noticeable but controlled. **The balanced default when no brand scale exists** —
websites, presentations, social graphics, general work.

### Perfect Fourth — 1.333
`16 · 21 · 28 · 38 · 51 · 67`

Pronounced separation. Use when the composition wants **display → heading →
body** as three distinct registers rather than many subtle steps. **Posters,
campaign graphics, editorial graphics, title slides, high-impact motion.**

### Golden Ratio — 1.618
`16 · 26 · 42 · 68 · 110`

Dramatic. Few usable levels — effectively display and body with little in
between. Also applicable to canvas division: **38.2% / 61.8%** instead of
50/50 introduces asymmetry while keeping proportional logic.

**Guardrail:** the golden ratio does **not** automatically make a design better.
It is one compositional tool among several, and its importance is routinely
overstated. Reach for it when you want dramatic asymmetry, not because it is
supposed to be inherently harmonious. Never justify a layout decision on the
grounds that it is golden.

```css
:root{
  --f0: 1rem;                        /* base */
  --f1: calc(var(--f0) * 1.25);
  --f2: calc(var(--f1) * 1.25);
  --f3: calc(var(--f2) * 1.25);      /* swap 1.25 for the chosen ratio */
}
```

---

## Self-check

- Was a grid chosen, or did content just get centred?
- Is the focal point on a third rather than dead centre — and if it is centred,
  was that a decision?
- Do sibling elements align to shared rows and columns?
- Do spacing values derive from one base unit, or were they picked individually?
- Is every type size on the scale?
- Does the scale's density match the content's density?
- Is running text near 65 characters?
- Did any proportional rule push type or spacing below accessible limits? Fix
  the rule, not the reader.
