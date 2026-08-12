---
name: premium-product-motion
description: High-end product and UI motion style for generated design — floating widget stacks, soft studio lighting, shallow depth of field, camera-style moves, and mixed-scale kinetic typography. Use for product mockups, app UI showcases, feature reveals, landing-page hero sections, brand or title sequences, and any artifact meant to feel expensive and tactile rather than informational. Pair with motion-system for the underlying timing rules.
---

# Premium product motion

The Apple-adjacent product film look: objects floating in a softly lit neutral
space, a camera that drifts rather than cuts, and typography treated as a
physical object in the scene. Where **editorial-explainer** is trying to make you
understand something, this style is trying to make you *want* something.

Movement rules live in **motion-system**. Frame-by-frame source observations live
in `../motion-system/references/sources.md`.

---

## Precedence and the carve-out

`../editorial-explainer/references/house-rules.md` governs. Read it first — the
ban list, the one-ambient-one-accent ceiling and the house timing kit apply here
unchanged.

This style is built from large radii, three-layer shadows, radial gradients and
blurred blobs, and house rules ban "Drop shadows or glows" and "Decorative
background gradients that mean nothing". Those two bans are about **data** and
about **decoration carrying no meaning**. In this style the light source and the
shadow it casts *are* the subject-matter — they are what makes an element read as
a physical object in a lit room, which is the entire proposition. So:

- **Permitted on objects.** Cards, widgets, device frames, chips, cutouts, the
  studio sweep behind them, and blurred colour blobs behind type. The shadow is
  describing a light source, not dressing up a flat rectangle.
- **Still banned on data.** Bars, lines, dots, areas, slices, stat tiles, axes,
  gridlines, annotation marks, legends and figures take no shadow, no glow, no
  gradient fill and no blurred blob behind them — inside this style exactly as
  outside it.

The line is the mark, not the medium. A chart *housed in* a floating card is
fine: the card is an object and carries the shadow; everything drawn inside it is
flat, and the moment a data mark starts casting its own shadow you are back in
the ban list. If a shadow or gradient is not describing the room's lighting, it
is decoration with no meaning and it goes.

---

## The governing idea

**Everything is an object in a lit room.** Nothing is a flat rectangle on a page.
Elements have thickness, catch light from a consistent direction, cast real
shadows onto what is behind them, and go out of focus when they are not the
subject. If an element could not plausibly exist as a physical card on a table,
it is off-style.

---

## The room

A soft neutral backdrop with a visible light falloff — not a flat grey, and not
a colourful gradient. The reference frames use an off-white to mid-grey vignette
that reads as a photographic studio sweep.

```css
.stage {
  background:
    radial-gradient(120% 90% at 50% 8%, #FAFAFA 0%, #EDEDED 42%, #D8D8D8 100%);
}
/* Dark variant */
.stage--dark {
  background:
    radial-gradient(120% 90% at 50% 8%, #2A2A2E 0%, #1A1A1D 45%, #0E0E10 100%);
}
```

Light comes from **top-centre**, consistently. Every shadow in the scene falls
down and slightly away. Mixed shadow directions are the fastest way to destroy
the illusion.

## Objects

Rounded rectangles with a large, soft radius and layered shadows. One shadow is
never enough — real objects cast a tight contact shadow plus a wide ambient one.

```css
.card {
  border-radius: 28px;
  background: #FFFFFF;
  box-shadow:
    0 1px 2px rgba(0,0,0,.06),      /* contact */
    0 8px 20px rgba(0,0,0,.08),     /* mid */
    0 32px 64px rgba(0,0,0,.12);    /* ambient */
}
```

Radius scales with the object: a small chip takes 12–14px, a widget 24–32px, a
full device frame 44–56px. A uniform radius across wildly different sizes is a
tell that the shapes were not considered individually.

Add a hairline top highlight (`inset 0 1px 0 rgba(255,255,255,.7)`) to suggest a
lit edge. On dark backgrounds, invert it to a subtle rim light.

## Depth of field

The single strongest differentiator from ordinary UI mockups. Elements not at
the focal plane are **genuinely blurred**, not just faded.

```css
.layer          { transition: filter 700ms var(--ease-out),
                              opacity 700ms var(--ease-out); }
.layer--far     { filter: blur(9px)   saturate(.85); opacity: .55; }
.layer--near    { filter: blur(4px);                 opacity: .8;  }
.layer--focus   { filter: none;                      opacity: 1;   }
```

Blur radii of 4–12px read as camera defocus. Above ~16px it stops reading as
optics and starts reading as a frosted overlay.

Pull focus *between* elements as the piece progresses — as one widget sharpens,
the previous one softens. Focus is how you direct attention here, in place of
the dimming used in editorial work.

## Camera moves

The scene moves; the elements mostly hold still relative to each other. This is
the opposite of typical web animation, where elements fly in against a fixed
background.

```css
/* Slow dolly across a stack */
@keyframes dolly {
  from { transform: translate3d(6%, 2%, 0) scale(1.06); }
  to   { transform: translate3d(-6%, -2%, 0) scale(1.02); }
}
.scene { animation: dolly 14s var(--ease-in-out) infinite alternate; }
```

Camera motion is **slow** — 10–20s for a full traverse. Fast camera movement
reads as a slideshow transition, not cinematography. Keep it continuous and
never let it fully stop; a scene that halts feels dead.

Add a light 3D tilt to the whole stage for parallax:

```css
.scene { transform-style: preserve-3d; perspective: 1400px; }
.card--a { transform: translateZ(60px); }
.card--b { transform: translateZ(0); }
.card--c { transform: translateZ(-80px); }
```

Layers at different Z will separate naturally as the camera moves — that
parallax is what sells the depth.

---

## Kinetic typography

Type in this style is composed, not laid out. The reference frames set a single
sentence at **wildly mixed scales within the line** — one or two words enormous,
the connecting words small — so the phrase has a rhythm and an obvious emphasis.

Principles:

- **Scale contrast within one sentence is 4–8×.** The emphasised word dominates;
  articles and prepositions shrink to near-caption size.
- **Mix weight and style, not families.** One typeface, but bold italic against
  light roman. Two families in one composition usually reads as a mistake.
- **Break the baseline.** Words sit at different vertical positions and overlap
  slightly. A tidy centred stack is the wrong look.
- **Thread imagery through the type.** A cut-out subject sits *in front of* one
  word and *behind* another. This single trick does more for depth than any
  shadow, and it is what makes a composition look designed rather than generated.

```html
<div class="kinetic">
  <span class="sm">Everybody</span>
  <span class="lg">figures</span>
  <img class="cutout" src="...">   <!-- z-index between the two spans -->
  <span class="md">it out</span>
</div>
```

- **Soft colour blobs behind the type** — large, heavily blurred circles in one
  accent hue — give the composition depth without competing for attention.

```css
.blob { position:absolute; border-radius:50%; filter: blur(46px); opacity:.75;
        background: var(--accent); }
```

Animate words in with a **stagger of 60–80ms** and a small rise, so the sentence
assembles in reading order rather than appearing at once.

## Micro-interaction detail

Small, specific, physical:

- Progress fills that fill in **segments** rather than one continuous bar.
- Counters that tick to their value with a slight overshoot (`--ease-spring`).
- Toggles and chips that compress ~2% on press before releasing.
- A subtle specular sweep across a surface as it enters, then never again.

These are cheap to build and they are most of the perceived quality.

---

## What breaks the style

- Flat shadows — a single `box-shadow` with one blur value.
- Uniform focus. If everything is sharp it is a mockup, not a scene.
- Shadows falling in different directions.
- Fast camera movement, or a camera that stops dead.
- Evenly-sized typography.
- Saturated multi-hue palettes. This style is near-monochrome plus one accent.
- Bouncy spring easing on large objects — overshoot on a big card reads as a bug.
