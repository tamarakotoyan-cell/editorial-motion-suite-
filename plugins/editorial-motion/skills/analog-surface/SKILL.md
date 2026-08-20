---
name: analog-surface
description: Surface treatment for generated design — how to make a ground, a mark or a screenshot read as a physical artefact rather than a rendered rectangle. Use whenever output includes paper, documents, maps, charts on a ground, screenshots, UI captures, archival or stock imagery, hand-drawn annotation, or any composition that currently sits on a flat colour fill. Covers the Surface / Ink / Life pipeline, blending ink into paper fibres with a luma matte, letterpress and ink bleed, roughened hairlines, posterize-time stepping, boil, film grain, screen emulation with scanlines and refresh flicker, footage homogenisation across mismatched sources, focus bands, and chromatic fringe scaled by register. Pair with motion-system for timing and a look skill for composition.
---

# Analog surface

Generated design has one tell that outranks the rest: **every surface is a flat
digital fill, and every mark sits on top of it.** Real artefacts do not work
that way. Ink soaks into paper, edges are irregular, surfaces carry the colour
temperature of the room, and nothing holds perfectly still.

This is not nostalgia. The reference states the commercial case directly:

> "Everything's like that perfect digital imagery. We associate it with like AI
> and that corporate look ... by adding those imperfections, that grit and that
> dust, it basically signals human curation to your viewer."

Imperfection is a **trust signal**. A chart on a printed ground is believed more
than the same chart on a white div — the demonstration is an A/B of identical
text on a white rectangle and on an aged sheet, and only one of them reads as
evidence. For client work, this is the difference between a deck that looks
authored and one that looks generated.

## The three pillars

Do them in this order. The order *is* the method.

| | | |
|---|---|---|
| **Surface** | The ground | Never white, never flat |
| **Ink** | The marks | Blended *into* the surface, not laid on it |
| **Life** | Time | Stepping, boil, flicker — nothing holds still |

## The treatment ladder

Treatment strength is keyed to what the object is pretending to be. One global
setting for everything is the most common mistake.

| Register | Surface | Ink | Life | Fringe |
|---|---|---|---|---|
| Document / paper | paper texture, warm, fibre | multiply + paper matte + bleed | boil | 0.5 |
| Native graphics | tinted ground, no pure white | roughened edges | posterize 12 | 0.8 |
| Screen / UI | scanlines + falloff | — | 24 Hz flicker + posterize 12 | 1.2 |
| Archival footage | shared homogenisation | — | posterize 12 + grain | 2.0 |

## 1. Surface

**Never `#fff`.** The measured reference value is `#FDFAF3` — H 41°, S 6%,
B 99%. The reasoning is physical: *"every room is going to have some sort of
light temperature ... your paper is always going to absorb that temperature."*
An untinted ground reads as synthetic because no real surface is neutral.

Never `#000` either. Printed black sits around 12–15% lightness.

**Texture at 5%.** Recorded four separate times across the reference set:
overlays work at far lower strengths than instinct suggests. If the texture is
noticeable as texture, it is too strong.

**Vignette in CSS, not in the texture.** A centred falloff cannot tile, and in
CSS it adapts to the element rather than to the tile.

**Broken grid.** The strongest single surface move in the Vox-style reference
set (`../motion-system/references/sources.md` §16), and cheap: a background grid
that *erodes* rather than tiles cleanly. Draw the grid at one shade off the
ground, then mask it with the same grain tile the paper uses. The line survives
where the fibre took ink and drops out where it didn't, so it fragments
irregularly — never on a repeating interval.

```css
.grid {
  background-image: linear-gradient(var(--rule) 1px, transparent 1px),
                    linear-gradient(90deg, var(--rule) 1px, transparent 1px);
  background-size: var(--grid-step) var(--grid-step);
  -webkit-mask-image: var(--grain-src);  mask-image: var(--grain-src);
  -webkit-mask-size: 420px;              mask-size: 420px;   /* same tile, same size as the paper */
  opacity: .5;
}
```

⚠️ **This is not a licence for `stroke-dasharray`.** An eroded solid line and a
dashed line look adjacent and mean opposite things — a dash pattern is a chart
convention (projected, excluded, below threshold). Same tile and same size as
the surface, or the grid reads as a separate object floating over the paper.

**Textures are generated, not sourced.** `assets/make-paper.py` and
`assets/make-grain.py` produce seamless tiles with no licensing question and no
network dependency. Where procedural genuinely loses is a hero sheet at full
strength with real crinkles — use a public-domain scan there (Library of
Congress, Smithsonian Open Access, Internet Archive), never a stock texture
library, whose terms almost always forbid redistribution inside a plugin.

## 2. Ink — the pillar most often skipped

This is the one that separates a convincing result from a pasted one, and it is
where generated work almost always fails. **Texture goes over the content in
most generated design. It should go under, with the content blended into it.**

Four mechanisms, all in `assets/analog.css`:

- **Multiply** so the ground reads through the mark. Expect this to look like a
  no-op on near-black ink over near-white paper — it earns its place on coloured
  ink, aged grounds, and overlapping marks.
- **A luma matte taken from the paper itself** so the fibres cut into the mark.
  This is the technique with no equivalent anywhere else in the system. The
  matte must come from the *same generated tile* as the surface, at the *same*
  size — a mismatch masks the ink against paper it is not sitting on, and the
  effect silently disappears.
- **Ink bleed** — porous stock wicks ink outward. Three stacked shadows at zero
  distance, expressed in `em` so they hold at any type size. The reference's
  absolute pixel values were tuned to one comp; below about 100px they read as a
  drop shadow.
- **Ink flecks** — printing-press error, a stroke-only ghost eroded and
  displaced behind the mark.

**Hairlines are a special case.** Rules and 1px strokes must be **masked**, not
filtered: `feDisplacementMap` displaces pixels after rasterisation, so on a thin
stroke it produces pixelation rather than roughness. This was diagnosed once
already — see the underline note in `../motion-system/references/sources.md`. Jitter geometry or
mask with the grain plate for anything under ~3px; filters are for large shapes;
a scanned mark beats both.

### Ink on stock — texturing type you set yourself

Everything above assumes ink you scanned. This is the other case, and it is the
common one: a headline set in the brand's own grotesque that needs to read as
printed rather than rendered.

**It is never a different typeface.** The brand owns the face, the editorial
weight comes from scale contrast, and an exotic display face will not survive an
Express import or a PPTX export anyway. Texture the face you have.

```html
<filter id="tooth" x="-3%" y="-6%" width="106%" height="112%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="1.7"
                     xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

- **Scale the displacement to the type size**, roughly `size ÷ 37` — about 1.7
  at 63px, 2.6 at 112px. A fixed value tuned on a headline reads as a rendering
  fault on a hero figure and as nothing at all on a caption.
- **The ceiling is ~2.6 at display sizes.** Measured against the alternatives:
  at 1.7 the edge erodes and the counters stay open; by 2.6 with coarser noise
  the stems start to wobble and it stops reading as print and starts reading as
  a low-resolution render.
- **It replaces the print fringe on that element — never stacks with it.** One
  surface treatment per string, same as everywhere else in this skill.
- ⛔ **Default: do not texture type at all.** Measured against 17 reference
  frames from NYT, Guardian and Vox — every one of them keeps its type clean at
  full strength, and puts the texture in the **ground** and the **imagery**
  instead. That is where texture reads as a material; on a letterform it reads
  as fur. The instruction that used to sit here — "apply it to the hero figures
  too" — was wrong, and produced exactly that.
- **Texture the field, not the words.** A grained ground under clean type gives
  the whole frame its surface; the type stays legible and the tile stops
  looking filtered. Ground grain goes **under the marks**, over the field: a
  full-frame overlay washes the marks and reads as a dirty gradient.
- **Texturing type is a rare, deliberate exception**, for one string, with a
  stated editorial reason — a headline that is *about* print, a stamped
  overprint. If you cannot say why in one sentence, leave it clean.
- **Add a second, finer noise as an alpha mask** for ink that didn't take —
  speckles knocked out of the glyph. Keep it subtle enough that no counter
  closes.
- ⚠️ **Check at 200px.** This is where an over-scaled displacement turns to mud.
- ⚠️ **Live SVG filters do not survive the Express import as text.** If a piece
  is going to Express as an editable document, send the headline untextured and
  treat it on the way out, or ship it as an image. Decide this as a standing
  rule per output route, not per piece.

## 3. Life

**Posterize time.** 12 fps as standard, 8 for a collage feel, 4 for a
deliberately choppy hero move. In CSS this is `steps()` sized to the duration,
so it is tied to the house timing kit in the motion-system skill's `motion.css`:
beat → `steps(6)`, settle → `steps(14)`, drift → `steps(120)`.

**Grain last**, after tint, curves and texture — and *moving*. Static grain is a
tell; real film grain differs every frame. Three independent plates cycled with
`steps(1, end)`.

**Boil.** Hand-drawn marks keep moving for their whole life; they are never
static after the draw-on. Three genuinely different states cycled, never one
state tweened.

## 4. Screens

Screenshots are never flat rectangles. The reference recipe: horizontal
scanlines at 8px pitch and 5% strength (*"most monitors are horizontal"*), a
radial falloff, and a 24 Hz refresh flicker. Then move a camera across it rather
than cutting — *"it helps you feel like you're participating in the journalism
and discovering things along with the narrator."* The pan is the argument.

**Safety note on the flicker.** The reference value is `wiggle(24, 0.08)` —
±8% exposure. That is fine on a small screen inside a frame and is not fine on
a screen-filling web element. `analog.css` scales it to ±2.5%, keeps it opt-in,
and disables it entirely under `prefers-reduced-motion`. Do not raise it.

## 5. Footage homogenisation — mandatory, not optional

Every raster asset passes through **one shared treatment** so mismatched
sources stop reading as mismatched. Claude assembles imagery from more varied
sources than any editor does, which makes this more important here than in the
original workflow, not less.

The reference is explicit that the choice of effects matters less than the
sameness: *"This matters less about the effects you use. It's just more
consistency across clips."* Force to greyscale or one shared duotone, blur the
edges behind a feathered mask so the centre stays sharp, add fringe and grain.

**A focus band beats a vignette** for placing attention — a linear blur map
leaves a sharp horizontal strip with soft top and bottom, which is what sells
macro depth on a flat composition. Do not stack a focus band and homogenisation
on the same element; both apply a backdrop layer and the masks compose into
"blurred everywhere except a small patch".

## Non-negotiable

- No pure white or pure black grounds.
- No raster asset outside a homogenisation wrapper.
- No hairline roughened with a displacement filter.
- Fringe on containers, not on dark glyphs over light paper — the filter
  recombines channels with `screen` and visibly washes the ink out.
- Reduced motion stops flicker and freezes grain and boil on a *visible* state,
  never a hidden one.

## What this is not

This is a surface treatment, not a look. It supplies no colour system, no type
scale and no composition. Take colour and typeface from the installed brand
system; take grid and proportion from layout-composition; take timing from
motion-system; take structure from a look skill.

And take the *technique*, never the identity. The reference material reverse-
engineers one publisher's house style. Trade dress — their logotype, their
palette as a palette, their chapter-card furniture — stays out. See
`../editorial-explainer/references/house-rules.md`.

## Assets

- `assets/analog.css` — the primitives. Paste alongside `motion.css`.
- `assets/filters.svg` — SVG filter defs. Paste as the first child of `<body>`.
- `assets/example.html` — reference board showing every register, with
  `{{IMG_*}}` placeholders to fill with base64 data URIs.
- `assets/make-paper.py` — seamless paper surfaces and their companion
  ink mattes. Stdlib only; no pip install.
- `assets/make-grain.py` — seamless grain plates, single or animated.
- `assets/_noise.py` — shared noise and PNG primitives for both.
