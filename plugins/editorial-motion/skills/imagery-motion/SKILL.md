---
name: imagery-motion
description: Photographic and footage treatment for generated design — how to compose, grade, mask, layer and move images rather than dropping them in as rectangles. Use whenever a design includes a photo, screenshot, video, cutout, document scan, or any raster asset, and whenever a composition of charts and type needs an image to carry a beat. Covers selective colour, extract-and-scale, letterbox with blurred self-extension, z-interleaved cutouts, focus pulls, offset echoes, duotone grading, punch-ins, 2.5D parallax from a single still, tiled document grids and video walls. Pair with motion-system for timing and layout-composition for placement.
---

# Imagery motion

The most common gap in generated design is that images are treated as
**rectangles that appear**. In the reference material they are almost never that:
they are masked, graded, cut out, layered between type, pushed out of focus,
punched into past comfort, or tiled into a wall. The image is a performer, not a
slot filler.

This skill covers what to do with a raster asset. Timing comes from
**motion-system**, placement from **layout-composition**, palette from the brand
system.

## The governing idea

**An image should be doing one of three jobs**, and you should know which:

1. **Evidence** — this is the thing being discussed (a document, a screenshot, a
   record). Treat it as a *prop*: real texture, real edges, held in the frame.
2. **Subject** — a person or object the story is about. Treat it as a *cutout*:
   separated from its background and composited with type.
3. **Atmosphere** — texture, ground, mood. Treat it as *defocused*: blurred,
   graded down, never competing.

An image doing none of these is decoration and should be cut. An image trying to
do two at once is why a composition feels muddy.

---

## Direct attention inside the image

The single biggest lift, and the technique most consistently missed. A raw
photograph gives the viewer no hierarchy — the fix is to build hierarchy *into
the image itself*.

### Selective colour

Keep the focal region in full colour; push everything else to desaturated,
hatched or line-art. In the reference, a hand-coloured map holds one state in
saturated blue while every surrounding state falls away to grey hatching.

```css
.sel        { position:relative; isolation:isolate; }
.sel img    { display:block; filter:saturate(.12) contrast(1.15) brightness(1.05); }
.sel .focus { position:absolute; inset:0;
              background:url(...) center/cover;
              clip-path: ellipse(18% 22% at 62% 44%);   /* the region that matters */
              filter:saturate(1.15); }
```

Animate the `clip-path` open over ~700ms so the colour *arrives* on the focal
region rather than being there from the start.

### Extract and scale

Pull the detail out of the image and blow it up, while the source stays where it
is. In the reference, a single word is lifted from a newspaper scan and scaled
enormously as the surrounding columns stay at their original tiny size.

This is compositing, not zooming — the point is the **scale disparity between
the detail and its source**, which a plain zoom destroys.

```css
.extract{ position:absolute;
          background:url(scan.jpg);
          background-size: 1400% auto;          /* huge, so we see one fragment */
          background-position: 34% 61%;          /* the fragment we want */
          transform: scale(.6); transform-origin: center;
          animation: lift 700ms var(--ease-out) both; }
@keyframes lift{ from{ transform:scale(.6); opacity:0 }
                 to  { transform:scale(1);  opacity:1 } }
```

Draw a thin connector or a faint outline back to the source location so the
reader knows where the fragment came from.

### Dim the rest

The general form: everything drops to ~28% and desaturates, one region stays
full. Same mechanic as the focal-point rule in **motion-system**, applied inside
a single image rather than across panels.

---

## Framing and the camera

### Punch-in past comfort

Scale into an image far enough that content crops off-frame. The reference
tutorial names this as what creates the signature look — the discomfort is the
point. A timid 105% zoom reads as an accident; 180% with words running off both
edges reads as a decision.

```css
@keyframes punch{ from{ transform:scale(1.0) } to{ transform:scale(1.8) } }
.punch{ animation:punch 6s var(--ease-io) both; transform-origin:38% 46%; }
```

Set `transform-origin` on the thing that matters, not the centre. Slow —
4–8s. A fast punch-in is a jump-scare.

### Letterbox with blurred self-extension

Footage sits in a band; the rest of the frame is filled by an enlarged, heavily
blurred copy of the same image. Standard for putting landscape footage in a
vertical frame without pillarboxing to black.

```html
<div class="lb">
  <div class="lb-bg" style="background-image:url(shot.jpg)"></div>
  <img class="lb-fg" src="shot.jpg" alt="">
</div>
```
```css
.lb     { position:relative; overflow:hidden; display:grid; place-items:center; }
.lb-bg  { position:absolute; inset:-10%; background-size:cover; background-position:center;
          filter:blur(38px) saturate(.7) brightness(.55); transform:scale(1.15); }
.lb-fg  { position:relative; width:100%; }
```

Blur hard — 30–48px. A lightly blurred backdrop reads as a rendering fault
rather than an intentional field.

### Focus pull

Genuine blur between depth layers, transitioning as attention moves. Not opacity
— optical defocus.

```css
.layer      { transition: filter 700ms var(--ease-out); }
.layer--far { filter: blur(9px) saturate(.85); }
.layer--near{ filter: none; }
```

4–12px reads as camera defocus. Past ~16px it becomes a frosted overlay.

### Slow drift

Any image held on screen more than ~3s should move a little — scale 100% → 103%
over 4–6s, ease-in-out, reversing. A completely still image reads as a stalled
video. Keep it under the threshold of notice.

---

## Compositing

### Z-interleaved cutouts

**The technique that most separates designed from generated.** A cut-out subject
sits *in front of* one word and *behind* another, so the type and the image
occupy the same space rather than stacking.

```html
<div class="weave">
  <span class="w-back">figures</span>
  <img class="w-mid" src="subject.png" alt="">
  <span class="w-front">out</span>
</div>
```
```css
.weave   { position:relative; }
.w-back  { position:relative; z-index:1; }
.w-mid   { position:absolute; z-index:2; }
.w-front { position:relative; z-index:3; }
```

Requires a real cutout with alpha. Without one, this collapses into a rectangle
sitting on top of text and looks worse than no attempt.

### Torn panels — the highest-value treatment on a paper ground

If the piece has a paper texture, **cut the photograph into the paper** rather
than laying it over the top. This is the single treatment that most changes how
a data piece reads, and it is what the newspaper references are all doing: the
image and the document are one object.

Four ingredients, all needed:

1. **A torn edge**, not a rectangle. An irregular `clip-path` polygon with
   ~36 points, jagging 0–5% in and out along every side.
2. **Duotone to the palette** — greyscale the photo, then a solid accent layer
   in `mix-blend-mode: color`. Raw colour photography sitting on a branded
   ground always fights it.
3. **An offset echo** — a flat accent-coloured copy of the same torn shape,
   translated ~10px behind. Depth with no drop shadow.
4. **A slight rotation**, 1–2°. Nothing pasted onto a page lands square.

```css
:root{ --tear: polygon(1% 3%, 9% 0%, 18% 4%, /* …~36 points… */ 0% 12%); }

.torn .echo{ position:absolute; inset:0; background:var(--accent);
             clip-path:var(--tear); transform:translate(11px,10px); }
.torn .pic { position:absolute; inset:0; clip-path:var(--tear);
             overflow:hidden; isolation:isolate; }
.torn .pic img   { filter:grayscale(1) contrast(1.3); }
.torn .pic::after{ content:""; position:absolute; inset:0;
                   background:var(--accent); mix-blend-mode:color; opacity:.5; }
.torn{ transform:rotate(-1.5deg); }
```

`isolation: isolate` on the clipped wrapper is what stops the blend leaking
into the page behind it.

Enter by scaling from ~0.93 with the rotation already applied, so the panel
settles onto the page rather than sliding in.

**Where it goes:** above the paper ground, below the marks and copy. And it
should be **inset with margins** — a torn panel that bleeds off the frame edge
loses the torn edge, which is the entire point.

The related newspaper devices from the same references, all cheap and all
worth having: a small **date chip** in the accent, a **highlighter block**
behind only the words that matter, and a small serif **credit line** beneath
the panel.

Place the date chip **beside the headline, or in the panel's corner, or on the
credit line** — never stacked above the title. (The reference puts it above; the
house ban on a capitalised overline above a heading overrides that — see
`../editorial-explainer/SKILL.md`.) A date is qualifying detail, so it belongs
beside or after the heading, not in front of it.

### Offset echo

A flat, accent-coloured copy of the subject's silhouette, offset a few pixels
behind it. Depth with no shadows, and it ties the image to the palette.

```css
.echo{ position:relative; }
.echo::before{ content:""; position:absolute; inset:0;
  background:var(--accent);
  -webkit-mask:url(subject.png) center/contain no-repeat;
          mask:url(subject.png) center/contain no-repeat;
  transform:translate(10px, 8px); z-index:-1; }
```

Offset 6–14px, always the same direction across a set.

### Duotone / high-contrast grading

This is the recipe, not the policy. **Whether every raster asset must share one
treatment is analog-surface's rule** — §5, Footage homogenisation, where it is
mandatory. What follows is how to grade one, once that decision is made.

Cutouts read best pushed to high-contrast black and white, then optionally
tinted. Raw colour photography inside a designed frame usually fights the
palette.

```css
.duo{ filter: grayscale(1) contrast(1.35) brightness(1.05); }
.duo-tint{ position:relative; isolation:isolate; }
.duo-tint::after{ content:""; position:absolute; inset:0;
  background:var(--accent); mix-blend-mode:color; opacity:.55; }
```

The comparison in one reference showed the graded version reading better purely
through contrast and cutout separation — no extra elements.

For a **pre-rendered** treatment — a cutout that will be embedded as a PNG rather
than filtered live — the static-design plugin's `halftone.py` runs the
whole pipeline repeatably: harden the alpha (threshold 128, one-pixel shave),
contrast window over the subject only, duotone to two brand values with the
lightest-pixel test (the highlight must remain a colour, or it fails), then an
optional halftone screen at about 7px cell. It prints the subject box to place
from. Same map for every asset in the composition.

Routing, in one line, shared with the static system: one strong photograph is
**Structure A** (it carries the frame); one cuttable subject plus a glyph
vocabulary is **Structure C** (layered editorial — one halftoned cutout, flat
glyph satellites, texture zoned); roughly ten silhouette cutouts is
**Structure B** (dense collage). Two to seven photographs on one frame is the
pinboard — `check-static.py` fails it (V); `check-artifact.py` does not, so hold
the count yourself.

### Masked reveal

Images arrive by being *uncovered*, not by fading. Wipe along the image's own
reading direction.

```css
@keyframes uncover{ from{ clip-path: inset(0 0 100% 0) } to{ clip-path: inset(0 0 0 0) } }
.uncover{ animation: uncover 800ms var(--ease-out) both; }
```

Pair with a slight counter-scale (image starts at 1.06, settles to 1.0) so the
picture appears to settle rather than slide.

---

### Ghost texture — near-ground tint mapping

To fill a ground with content-relevant imagery *without* competing: map the
image's white point to a value just above the ground colour, so cutouts and
documents sit as barely-there texture. Named on screen in the reference as
keeping "the contrast stays subtle".

```css
.ghost{ filter:grayscale(1); opacity:.07; }          /* on a dark ground  */
.ghost-light{ filter:grayscale(1) invert(.92); opacity:.09; }  /* light ground */
```

5–10% is the working range — the reference sets its texture layer at 5%. The
subject matter should relate to the story (newspapers behind a media piece,
columns behind a courts piece); at this opacity it registers as atmosphere,
not information.

### Collage cluster on a flat backing shape

Group two or three B&W cutout objects (building, gavel, scales) over **one flat
colour shape** — a circle or blob in the accent or a muted tone — on the warm
ground. The backing shape is what makes disparate cutouts read as one
illustration rather than scattered clippings. The reference states it plainly:
the backing "is just a flat color".

Order: ground → flat shape → cutouts overlapping the shape's edge. Cutouts
should break the shape's silhouette — fully contained reads as a sticker.

### Dolly, don't scale

The reference moves a 3D camera toward the still ("slowly dolly", Z −1500)
rather than scaling the image. With layered planes this yields true parallax;
even on a flat image, perspective foreshortening feels different from a zoom:

```css
.scene{ perspective:1200px; }
.scene img{ animation: dolly 9s var(--ease-vox) both; }
@keyframes dolly{ from{ transform:translateZ(0) } to{ transform:translateZ(260px) } }
```

Separate the subject and background into two planes at different Z and the
dolly produces genuine parallax between them.

### 2.5D parallax from a single still

The full form of that idea, and the one technique the references treat as the
difference between a photograph that lives on screen and one that sits there.
A reference clip demonstrates it by *removing* it and calling the result an
iMovie slideshow.

Cut the image into **three planes — foreground, midground, background** — patch
the holes left behind each cutout (clone/heal, or a generative fill), space them
in Z, and move the camera rather than the image:

```css
.par        { perspective: 900px; transform-style: preserve-3d; overflow: hidden; }
.par > *    { position: absolute; inset: -6%;   /* overscan, or edges swing in */
              background-size: cover; }
.par .bg    { transform: translateZ(-260px) scale(1.35); }
.par .mid   { transform: translateZ(-90px)  scale(1.12); }
.par .fg    { transform: translateZ(60px)   scale(0.94); filter: blur(1.5px); }
.par.run > *{ animation: cam 9s var(--ease-in-out) infinite alternate; }
@keyframes cam { to { translate: -3% 0; } }
```

Four things make or break it:

- **Patch behind the cutouts.** The hole is what gives it away — as the camera
  moves, an unpatched background tears open behind the subject.
- **Counter-scale each plane** (`scale` rises as Z falls) so the planes still
  frame the same picture at rest. Without it the composition reflows.
- **Defocus the foreground slightly.** 1–3px. Real lenses cannot hold near and
  far at once, and this is the cheapest part of the illusion.
- **Move slowly and never stop** — 8–12s a traverse, the drift rules above.

⚠️ It needs an image with genuine depth separation. On a flat image — a crowd
at one distance, a document, a head-on portrait — there is nothing to separate
and the planes shear against each other. Use a punch-in instead.

### Digital evidence as physical prop

A web article shown as evidence is **printed onto paper** — screenshot
composited onto a sheet with soft deckled edges, slight rotation, vignette
ground — rather than shown as a browser window. The document reads as an
artefact with weight, and it inherits every paper technique above (tears,
creases, punch-ins). Screenshot-in-a-browser-frame is the generic move;
screenshot-as-clipping is the editorial one.

## Volume as an argument

### Tiled document grids

To convey scale or complexity, show **many** — a dense grid of scanned pages
filling the frame. The rhetorical work is done by quantity, and it lands harder
than any adjective.

```css
.tiles{ display:grid; grid-template-columns:repeat(auto-fill,minmax(90px,1fr)); gap:6px; }
.tiles > *{ animation: rise 420ms var(--ease-out) both;
            animation-delay: calc(var(--i) * 26ms); }   /* fast stagger — a cascade */
```

Stagger tight (20–30ms). At 70ms a 40-tile grid takes three seconds to build.

### Video walls

Many tiles playing at once behind a composited figure or headline, tiles at
reduced opacity so the foreground stays legible. Used in the reference behind a
very large number.

### Texture as subject

Magnified physical material — paper fibre, grain, particulate — as a full-frame
ground. Surfaces in this idiom are always *material*. A flat digital fill is the
tell.

---

## Depth registers

The most cinematic reference in the set alternates between two extremes of depth
and never sits between them:

- **Enveloping space** — a rendered or photographed *place*, warm-graded, lit
  from one dominant source, with visible falloff and shallow focus at the back
  of the room. Atmosphere, not information.
- **Isolated object on void** — a single subject on pure black, studio-lit with
  tight speculars and no ground shadow, so it floats.

Cutting between the two is the structure. A composition that lives permanently
in the middle distance — objects on a mid-grey backdrop, evenly lit — is the
flattest place to be.

```css
/* enveloping */
.room{ background: radial-gradient(120% 80% at 50% 22%, #F6ECD8, #C9BCA4 55%, #5A5044);
       filter: saturate(.9); }
/* void */
.void{ background:#000; }
.void .hero{ filter: drop-shadow(0 0 60px rgba(255,255,255,.06)); }
```

**Slow, unbroken camera.** In that reference the push-in never stops across the
whole shot — measurably closer at 15s than at 7s, with no pause. A camera that
halts makes a scene read as dead. See the drift and punch-in patterns above.

## Panel within field

A structural device running through the long-form reference: illustration and
data almost never bleed to the frame edge. They sit in an **inset rectangle** —
often near-black — placed on a saturated colour field, with faint rule lines
running behind it. A screen within the screen.

```css
.field { background: var(--field); padding: clamp(24px, 6vw, 72px); }
.field .panel { background: #111; }        /* the inset screen */
```

Reserve full-bleed for statement moments. Constant full-bleed removes the
contrast that makes a statement frame feel like one.

Interview and talking-head footage follows the same logic: **letterboxed into a
band**, cropped tight, subject placed off-centre rather than dead middle.

## Evidence handling

Screenshots, scans and recordings are the most common images in research and
comms work, and the most commonly mishandled.

- **Keep the artefacts.** Paper texture, fold lines, screen bezels, slight
  rotation. A perfectly flat, perfectly square scan reads as a mockup.
- **Crop hard.** Show the fragment that matters, not the whole page.
- **Annotate rather than caption.** Circle, underline or mark on the document —
  see the hand-drawn annotation pattern in **editorial-explainer**.
- **Never fabricate a document that purports to be real.** Synthetic props must
  be visibly constructed, and any placeholder marked as such.
- **Interleave live action.** Overhead shots of hands, objects and desks between
  graphic sequences give a piece rhythm. All-graphics reads as a slideshow.

---

## Asset sources

- **Icons:** flaticon.com/hand-drawn-icons — hand-drawn style matches the
  annotation vocabulary (scribbles, arrows, roughened marks). Check the licence:
  free tier requires attribution; the team's paid seat may not. ⚠️ Icons remain
  banned *as data marks* (house rules) — use them as props and annotation, not
  as chart elements.
- **Scanned marks:** the user's local scribble-overlay and brush-arrow packs
  (`~/Desktop/Tools and Stock/Stock/`) — real pen strokes; beat synthetic
  wobble for circles, underlines and arrows. Tint to the accent, clip to size.
- **Paper:** the user's paper-overlay set (folded, ruled, crumpled), resized to
  ≤760px and embedded as data URIs.

## What breaks it

- Images as plain rectangles that fade in.
- Parallax planes with the holes behind them left unpatched, or applied to an
  image with no real depth to separate.
- A raw photograph with no internal hierarchy.
- Timid punch-ins, or a still image held with no drift.
- Lightly-blurred backdrops — reads as a fault, not a field.
- Rectangular "cutouts" — the whole technique needs real alpha.
- Full-colour photography fighting a brand palette.
- Drop shadows standing in for depth where a focus pull or an offset echo is the
  actual answer.
- Decorative imagery doing none of evidence, subject or atmosphere.

## Before shipping

- Does every image have a stated job — evidence, subject, or atmosphere?
- Is there hierarchy *inside* each image, or is it uniformly weighted?
- Does anything move, and does it survive as a still frame?
- At 200px wide, does the treatment still read, or has it turned to mud?
- Are cutouts genuinely cut out?
- Is any synthetic prop clearly marked as illustrative?
