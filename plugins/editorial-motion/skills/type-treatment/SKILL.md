---
name: type-treatment
description: How type is styled, textured, layered against imagery and animated in generated design — headlines over photos, titles on paper or concrete, kinetic text, hand-lettered captions, numbers that land. Use whenever text sits on top of a photograph, video frame, texture or colour field, whenever a headline needs to feel printed rather than pasted, and whenever text itself is the thing that animates. Covers the four layering registers (on / in / through / among), blend-mode texturing, grain masks and displacement, ink colour sampling, legibility plates, exclusion-blend emphasis, semantic face pairing, per-character reveals, two-stage arrival, fill sweeps, digit rolls and hand-drawn boil. Pair with motion-system for timing, imagery-motion for the picture, layout-composition for where it goes.
---

# Type treatment

Generated design gets type wrong in one specific way: **the text is rendered
separately from the image and laid on top of it.** Every tell follows from that —
the too-clean edge, the flat #000, the drop shadow standing in for integration,
the headline centred over someone's face.

In the reference material type is almost never on top of the picture. It is
printed into the surface, knocked out of it, or woven through it. This skill is
about closing that gap.

Timing comes from **motion-system**. The picture itself comes from
**imagery-motion**. Grid, placement and the type *scale* come from
**layout-composition** — set those before styling a single letter. Colour and
typeface come from the client's brand system, never from here.

## Precedence

The house standard wins where one exists:
`../editorial-explainer/references/house-rules.md`. It carries the timing kit,
the one-ambient-one-accent ceiling and the ban list — including **no serif or
display face on a hero figure** and **no capitalised overline above a heading**,
both of which constrain what follows. Read it first.

---

## The four registers

Before styling anything, decide which relationship the type has to the image.
Picking one and committing is most of the work; the tell is usually that nobody
picked.

| Register | What it means | Reach for it when |
|---|---|---|
| **On** | Type sits above the image on its own plate or scrim | Utility text — captions, sources, credits, chart labels |
| **In** | Type is printed into the surface and takes its grain and form | Titles on paper, concrete, fabric, newsprint — anything material |
| **Through** | The image shows through the letterforms | One or two words, very large, where the picture *is* the subject |
| **Among** | Type interleaves in z with cut-out subjects | A person or object the story is about, composited with a headline |

**On** is the honest default for small text and the wrong answer for a title.
**In** is the highest-value treatment and the rest of this file is mostly about
it. **Among** belongs to `../imagery-motion/SKILL.md` (z-interleaved cutouts) —
build it there, don't rebuild it here.

Mixing registers within one composition is fine and usually correct: a headline
**in** the paper, a caption **on** a small plate. Mixing them on the *same
string* is not.

---

## Register: In — printing type into a surface

Four ingredients. Each one alone is not enough, and the order matters.

### 1. Blend, never fade

**The single rule that fixes most of it.** Dropping a texture's opacity to blend
it is the most common mistake and it is what makes textured work look grey and
dead — it "makes your textures feel dull", in the words of the reference
(`references/sources.md` §1). Opacity averages two layers toward mid-grey.
A blend mode lets the surface's own light and dark drive the result.

The reference stack uses **Overlay** and **Pin Light** for the texture plates
and a texture as a **track matte** on the type. The CSS equivalents:

```css
.plate            { position: relative; isolation: isolate; }  /* contains the blend */
.plate .ink       { color: var(--ink); mix-blend-mode: multiply; }  /* dark ink, light ground */
.plate .ink--rev  { color: var(--paper); mix-blend-mode: screen; }  /* light ink, dark ground */
.plate .grain     { position:absolute; inset:0; background:url(grain.jpg) center/420px;
                    mix-blend-mode: overlay; pointer-events:none; }
```

`isolation: isolate` on the wrapper is not optional — without it the blend
leaks through to whatever is behind the section.

Which mode: **multiply** for dark ink on a light ground, **screen** for light ink
on dark. `overlay` and `soft-light` are for the *texture plate*, not for the
type — run through the type they wash it out to about half strength and you lose
the ink. Never use `opacity` to sink type into a surface.

### 2. Break the edge

The reference short circles two specific places on a giant letterform and names
them as the whole game: where the stroke meets the grain
(`references/sources.md` §2 — "blending text in a texture is all about the
details"). A perfectly clean vector edge over a rough surface is the tell,
because nothing printed on a rough surface has a clean edge.

Mask the type with the surface's own texture so the ground eats into the ink:

```css
.eroded {
  -webkit-mask-image: url(grain.png);  mask-image: url(grain.png);
  -webkit-mask-size: 300px;            mask-size: 300px;
  -webkit-mask-mode: luminance;        mask-mode: luminance;   /* light = keep */
}
```

Keep the erosion **subtle and uneven**. A mask that removes an even 20%
everywhere reads as a faded layer; a mask that bites hard in three places and
not at all elsewhere reads as ink that didn't take. If the mask asset is high
contrast, soften it with `filter: contrast(.6) brightness(1.25)` on a wrapper
before using it, or the type shreds.

### 3. Follow the form

Type on a curved, woven or corrugated surface should bend with it. The reference
adds a displacement map so the type "takes on the form of our texture"
(§1) — this is what turns a flat overlay into something that looks photographed.

```svg
<filter id="surface" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.014" numOctaves="3" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6"
                     xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

**House constraint — this is a hard limit.** `feTurbulence` +
`feDisplacementMap` is only usable on **large shapes**: display type at roughly
72px and above. On body copy and small labels the filter pixelates the stems and
looks like a compression artefact, not a surface. Below that size, get the
irregularity from **jittered geometry** — an SVG path with the points nudged —
or skip it. The best answer of all is a real scanned asset; see *Assets* below.

`scale` of 4–8 reads as a surface. Past ~12 it reads as a heat haze.

If the real surface has a direction — corrugation, fabric weave, wood grain —
give the noise that direction with an anisotropic `baseFrequency`
(`baseFrequency="0.004 0.03"`), or the warp fights the photograph.

### 4. Match the light

The type must share the plate's grain, and it must share its colour range.

**Never pure black, never pure white.** The reference pauses on a colour picker
with the corners struck out — "avoid these sections" (§2). Type printed on a
real surface never reaches #000 or #FFF, because the surface is scattering light
into it. Sample the ink from the image's own dark values and lift it; sample
highlights from its light values and drop them.

```css
:root {
  --ink:   #23201C;   /* not #000 — carries the surface's warmth */
  --paper: #F2EEE6;   /* not #FFF */
}
```

A practical floor: keep the ink about 8–12% off the extreme, and let it carry a
few points of the surface's hue. If the concrete is cool, the ink is cool.

Then run the **grain over everything, type included** — a single grain layer at
the top of the stack, not one per element. Type that is clean while the plate is
grainy is the same failure as a clean edge, one level up.

---

## Register: Through — the image inside the letterforms

Two words maximum, set very large and very heavy. This only works when the
counters and stems are wide enough to show a readable piece of picture — a light
or condensed face turns it to confetti.

```css
.knockout {
  background-image: url(photo.jpg);
  background-size: cover;
  background-position: 50% 38%;      /* aim the interesting part at the letterforms */
  -webkit-background-clip: text; background-clip: text;
  color: transparent;
  font-weight: 800;
  font-size: clamp(56px, 16vw, 200px);
  letter-spacing: -0.02em;
}
```

Two things it needs, and neither is optional:

- **A fallback.** If `background-clip: text` fails, transparent text disappears.
  Guard it: `@supports (background-clip:text) or (-webkit-background-clip:text)`
  and set a solid `color` outside the block.
- **A busy-image check.** Grade the source down first —
  `filter: contrast(1.25) saturate(.8)` on a wrapped copy — or crop to a calm
  region. A high-detail photograph inside letterforms is unreadable at any size.

The inverse — type knocked *out* of a solid plate so the image shows through the
holes — is more robust and often better. Build it with a mask rather than
clipping, so the plate stays opaque:

```css
.stencil { background: var(--accent);
           -webkit-mask-image: var(--text-mask); mask-image: var(--text-mask);
           -webkit-mask-composite: xor; mask-composite: exclude; }
```

---

## Register: On — plates and scrims that aren't lazy

When type genuinely does sit over a picture, the job is contrast without a black
box over the photograph.

**Ranked, best first:**

1. **Put it in the quiet region.** Find the calm area of the image and set the
   type there. Costs nothing and needs no scrim. This is a *layout* decision —
   see below.
2. **Grade the image locally.** A soft directional gradient in the image's own
   dark tone, sitting under the type only:
   `linear-gradient(to top, rgba(20,18,16,.72), transparent 62%)`. Use the
   photograph's dark value, not black.
3. **A real plate.** An opaque shape in the palette that the type sits inside as
   a designed element — a coloured band, a sticker, a torn strip. Honest and
   often the strongest.
4. **Backdrop blur.** `backdrop-filter: blur(14px) saturate(.9)` with a low-alpha
   fill. Works, but reads as product UI rather than editorial. Know that you're
   borrowing a different idiom.
5. **Exclusion blend on the word itself.** The type inverts against whatever is
   behind it, so contrast is guaranteed with no plate at all — it goes white
   over dark passages and dark over light ones, per pixel, as the image moves
   beneath it.

   ```css
   .knock { mix-blend-mode: exclusion; color: #fff; }  /* inverts its ground */
   ```

   Taught in the reference set as the emphasis treatment for a keyword over
   footage. Two limits: it is for **one or two emphasised words**, never a
   paragraph, because the colour is not yours to choose and shifts as the
   backdrop changes; and over a mid-grey region it inverts to mid-grey and
   disappears, so check it against the actual passage it sits on. Needs
   `isolation: isolate` on the wrapper, as every blend here does.

**Not on the list:** a text shadow, a glow, or a 40%-black rectangle over the
whole frame. A drop shadow on type is the same error as a drop shadow on data —
decoration standing in for a decision.

Verify contrast **in the region the type actually occupies**, not against the
image's average. A headline can pass against a mean value and vanish over one
bright cloud.

---

## Type and the layout

Where the type goes is a layout decision made against the *image's* content, not
against an empty rectangle. **layout-composition** owns the grid and the scale;
these are the image-specific rules on top.

- **Read the picture first.** Set type into its negative space. Never centre a
  headline over the subject's face, and never let a line cross the eyes.
- **Anchor to something in the frame.** Align the headline's baseline to a real
  edge in the photograph — a horizon, a table, a doorframe. Type aligned to an
  edge in the image looks placed; type floating in the middle looks dropped.
- **One optical centre.** If the image has a strong focal point, the type is
  secondary and sits off-thirds. If the type is the hero, the image must be
  graded down to atmosphere (see imagery-motion). Two things competing at full
  strength is the "where do I look" failure (§3).
- **Let type break the frame.** Running a word off the edge, or across the seam
  between a photo and a colour field, ties the two together. A headline fully
  contained inside its own margin sits on a separate plane.
- **Mixed scale within one thought.** The reference sets the emphasis word two
  or three steps up from the rest of the line and often in a contrasting style,
  so a single sentence carries its own hierarchy. Use the scale ratio from
  layout-composition — jumping steps arbitrarily is what makes it look random.
- **Pair the faces by role, not by whim.** Where the references mix two faces in
  one line they do it to the same rule every time: **the sans carries the
  claim, the serif carries the aside.** Bold grotesque takes the load-bearing
  word — the number, the verdict, the name — and an italic serif takes the
  qualifier, the irony or the human note. One line, two registers, and the
  reader can tell which is which without being told. Alternating faces for
  variety rather than for meaning is the version that looks random.
  ⚠️ The hero figure stays in the sans regardless — house rules ban a serif or
  display face on it.

**Ban check:** no capitalised overline above a heading (house rule, hard). If a
kicker is needed, set it beside or beneath the headline.

---

## Type in motion

Everything in **motion-system** applies — the easing set, the timing kit, the
one-ambient-one-accent ceiling, `prefers-reduced-motion`. These are the moves
specific to text.

### The rule that governs all of them

**One text animation on screen at a time.** The reference is blunt about it: a
frame with several animating text elements is "distracting", "overwhelming",
"almost like a slot machine", and the viewer's question becomes *where do I
look* (§3). Multiple simultaneous text animations is the single most common way
kinetic type fails.

Everything else on screen holds still while text moves.

### Per-character reveal

The workhorse. Reveal by character with a small offset ramp, not all at once.

```css
.by-char span {
  display: inline-block;
  animation: rise var(--beat) var(--ease-out) both;
  animation-delay: calc(var(--i) * 26ms);
}
```

Per-**character** stagger runs much tighter than the 70ms sibling stagger —
**20–35ms**. At 70ms a nine-letter word takes two thirds of a second to arrive
and reads as a typewriter. Per-**word** stagger stays at the house 0.2s.

Set `--i` in reading order. Wrap each character in a span, and keep the original
string available to screen readers (`aria-label` on the parent, `aria-hidden` on
the spans) — splitting text into spans destroys it for assistive tech otherwise.

### Two-stage arrival

The detail that separates the reference reveals from a plain stagger: an element
mid-animation is rendered **pale, soft and slightly offset**, and only reaches
full ink once it has landed. Arrival state is encoded in colour, not just in
position — so a half-built line visibly reads as half-built.

```css
@keyframes ink-in {
  from { opacity: 0; color: var(--muted); filter: blur(3px);
         transform: translateY(3px); }
  60%  { opacity: 1; color: var(--muted); filter: blur(0);
         transform: none; }
  to   { opacity: 1; color: var(--ink); }
}
.by-char span { animation: ink-in var(--beat) var(--ease-out) both; }
```

Keep the settle to the last third of the duration. It is also the honest way to
show a per-word build: the words already placed sit at full strength while the
newest one is still resolving, so the eye tracks the front edge of the sentence.

### Text exits

Everything in the **Exits** section of motion-system applies, and the text
specifics are: mirror the entrance (characters that arrived in random order
leave in random order), and prefer **accumulate-then-dim** over clearing —
a finished line drops to about 30% rather than vanishing when the next line
starts, so the thought stays whole.

### Fill sweep

The Vox move (§3): the word fills with the brand colour, then **settles to the
ink colour for legibility**. The brand does the arrival; the ink does the
reading. That second half is the part everyone drops, and it is why the
technique looks sophisticated rather than gaudy.

```css
.fill      { position: relative; color: var(--ink); }
.fill::after {
  content: attr(data-text); position: absolute; inset: 0;
  color: var(--brand);
  clip-path: inset(0 100% 0 0);
  animation: fill-sweep var(--beat) var(--ease-vox) both,
             fill-settle 400ms var(--ease-out) 1.1s both;
}
@keyframes fill-sweep  { to { clip-path: inset(0 0 0 0); } }
@keyframes fill-settle { to { opacity: 0; } }
```

Sweep in the reading direction. Hold the brand colour about a beat before it
settles — settling immediately looks like a glitch.

### Digit roll

Numbers arrive by rolling to their value like an odometer, decelerating into
place. Strong, and strictly limited: **the hero figure only.** House rules ban
count-up on anything else, and the reference's slot-machine warning applies here
first — a screen of rolling numbers is unreadable.

```css
.odo      { display:inline-flex; height:1em; overflow:hidden; line-height:1; }
.odo ul   { margin:0; padding:0; list-style:none;
            animation: roll 900ms var(--ease-vox) both; }
@keyframes roll { from { transform: translateY(calc(-9 * 1em)); }
                  to   { transform: translateY(0); } }
```

Stagger the digits 60–80ms left to right so the number *lands* rather than
snapping. Never re-run it when the element scrolls back into view.

### Hand-drawn boil

The wiggle in hand-lettered captions. The reference method is physical and worth
understanding, because it explains why synthetic versions look wrong: the word
is written by hand **three separate times**, the three takes are stacked, and
the edit cycles between them (§4). The irregularity comes from three genuinely
different drawings, not from one drawing being distorted.

Reproduce that structure — three variants cycled — rather than animating a
single wobble:

```css
.boil            { position: relative; display: inline-block; }
.boil > span     { animation: boil-flick .27s steps(1, end) infinite; }
.boil > span + span { position:absolute; left:0; top:0; }
.boil > span:nth-child(2) { animation-delay: .09s; }
.boil > span:nth-child(3) { animation-delay: .18s; }
@keyframes boil-flick { 0%, 33.32% { opacity: 1; } 33.33%, 100% { opacity: 0; } }
```

That is a 3-frame cycle at ~11fps. **8–12fps is the working range** — faster
reads as a flicker fault, slower as a stutter. A continuous smooth wobble is the
giveaway that it was generated; hand-drawn boil is *stepped*, never eased.

Source the three variants, best first: three real scanned drawings; three SVG
paths with hand-nudged points; three `feTurbulence` seeds on large type only
(the size limit from §3 above applies). Never one variant with a smooth
transform loop.

Boil is an **ambient** move under the house ceiling — it never stops. Pair it
with at most one accent.

---

## Assets

**In this skill:**

- `assets/type.css` — drop-in primitives for every technique above. Pair with
  `../motion-system/assets/motion.css`, which supplies the easing and timing
  tokens it references.
- `assets/example.html` — a reference board showing all four registers, the
  boil, the fill sweep and the per-character reveal. A template: replace the
  four `{{IMG_*}}` placeholders with base64 data URIs.

**External:**

- **Scanned marks and lettering** — the user's scribble-overlay and brush-arrow
  packs at `~/Desktop/Tools and Stock/Stock/`. Real pen strokes beat both
  synthetic wobble and filter noise for boil variants, underlines and circles.
  Tint to the accent, clip to size.
- **Paper and surface textures** — the user's paper-overlay set (folded, ruled,
  crumpled). Resize to ≤760px and embed as data URIs; artifact CSP blocks
  external hosts.
- **Fonts** — artifact CSP blocks font CDNs. Archivo falls back to Arial, which
  is Essential's own stated fallback. Say so rather than letting it pass
  silently; never let a display face land on a hero figure regardless.

---

## What breaks it

- Type faded into a texture with `opacity` instead of a blend mode.
- A clean vector edge sitting on a rough surface.
- `#000` on a photograph, or `#FFF` on one.
- Drop shadow, glow or a full-frame black scrim doing the work that placement,
  a local grade or a real plate should do.
- A headline centred over a face.
- Grain on the plate but not on the type.
- `feDisplacementMap` on small text — it pixelates the stems.
- More than one text animation running at once.
- A smooth, eased wobble standing in for hand-drawn boil.
- Digit rolls on figures that are not the hero.
- Per-character stagger set at sibling speed, so a word types itself out.
- A second face alternating for variety rather than carrying a different role.
- Exclusion-blend type over a mid-grey passage, where it inverts to invisible.
- Text that clears when it should have dimmed, resetting the reader's context.
- `background-clip: text` with no fallback — the text is invisible where it fails.
- Text split into spans with no `aria-label` on the parent.

## Before shipping

- Which register is each text element in, and was that chosen?
- Does it survive as a **still screenshot**? (Nothing else matters if not.)
- Is it legible at **200px wide**, or has the grain turned it to mud?
- Is the ink off pure black and off pure white, carrying the surface's hue?
- Does the type share the plate's grain and edge quality?
- Is contrast checked in the region the type occupies, not the image average?
- Is exactly one text animation running at any moment?
- Is there one optical centre — image or type, not both?
- Does `prefers-reduced-motion` leave the text present and readable?
- Is the text still readable by a screen reader after any splitting?
