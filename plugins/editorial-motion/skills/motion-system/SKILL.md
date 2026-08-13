---
name: motion-system
description: Motion and animation rules for any generated design — HTML artifacts, slides, charts, landing pages, social graphics, UI mockups. Use whenever output will animate, transition, reveal, or move, and whenever building something that currently sits static and would read better with motion. Covers easing curves, the two timing registers (eased settle and hard snap), pacing beats to the copy rather than a clock, entrance timing, staggering, cutting on the velocity peak, anchor-object continuity, arc paths, exits, focal-point dimming, scroll-as-narration, and reduced-motion handling. Not a visual style — pair with editorial-explainer or premium-product-motion for a look.
---

# Motion system

Most generated design fails not because the layout is wrong but because nothing
moves, or everything moves the same way at the same time. This skill fixes the
movement. It is deliberately style-agnostic — it governs *how* things move, not
what they look like.

## Precedence

Where a house standard exists, it wins. For this user that is
`../editorial-explainer/references/house-rules.md`, which carries an established
timing kit, a strict one-ambient-one-accent ceiling and a ban list. **Read it
before applying anything here.** This file supplies the mechanics; the house
rules supply the limits.

Layout and proportion decisions belong to **layout-composition** and should be
made before any motion is designed.

## The two rules that matter most

**Never animate more than one thing at a time unless they are deliberately
staggered.** Simultaneous motion has no focal point, and a frame with no focal
point gives the viewer nothing to look at.

**If it only works moving, it fails.** Every composition must survive as a still
screenshot. Motion is an enhancement to a frame that already works — never the
thing holding it together.

---

## Easing

Linear is wrong for everything except continuous loops (spinners, marquees,
ambient drift). Use these four and nothing else:

```css
--ease-vox:   cubic-bezier(0.10, 0.90, 0.20, 1);/* the reference curve — see below */
--ease-out:   cubic-bezier(0.16, 1, 0.30, 1);   /* entrances — fast, then settle */
--ease-in-out:cubic-bezier(0.83, 0, 0.17, 1);   /* heavy in/out — transitions, cuts */
--ease-spring:cubic-bezier(0.34, 1.56, 0.64, 1);/* slight overshoot — chips, toggles, counters */
--ease-in:    cubic-bezier(0.55, 0, 1, 0.45);   /* exits only */
```

**The reference curve.** A tutorial breakdown showing the actual After Effects
velocity graph (`references/sources.md` §12) has velocity climbing to a ~250%/sec
peak within roughly the first 15% of the duration, then decaying exponentially
across the remaining 85% — a short attack and a very long tail. That is far more
extreme than a stock ease-out, and the long decay is what makes the motion feel
weighted rather than merely quick.

`--ease-vox` approximates it. Use it for hero entrances and anything that should
feel like it has mass. Keep `--ease-out` for ordinary UI-scale motion, where the
extreme curve reads as sluggish on small distances.

`--ease-out` is the default. Reach for it unless you have a reason not to.
`--ease-spring` overshoots ~5%; use it sparingly or the whole page reads bouncy
and cheap. Never apply a spring to something large — overshoot on a full-width
panel looks like a bug.

## Duration

**Use the house timing kit** where one exists — named tokens beat ad-hoc numbers,
because a shared vocabulary is what makes a set of assets read as one family:

| Token | Value | Use for |
|---|---|---|
| Snap | 0.25s | Stickers, pops, anything physical |
| Beat | 0.5s | Word and line reveals |
| Settle | 1.2s | Full text blocks arriving |
| Hold | 1.5s | Dwell before a loop resets |
| Drift | 8–12s | Ambient background movement |

Anything under 100ms reads as a jump-cut. Anything over 1s on a *single* element
reads as sluggish — if you need more time, you need more elements staggered, not
one slower element.

**Loop length:** 3s for a single line, 6s for a stacked tile. Past 8s people
scroll before it resolves.

### The two registers

The kit above is the **eased register** — things travel, and the curve does the
expressive work. The reference set uses a second one constantly, and generated
work almost never does.

**The snap register: no easing at all.** Captions, keyword chips and slam
titles arrive in one or two frames — a hard stamp at full size — hold for as
long as the thought takes, then leave. There is no entrance curve to read,
because the entrance is not the point: the rhythm is carried by *when* things
land and how long they stay.

```css
.stamp { animation: stamp 60ms steps(1, end) both; }   /* effectively instant */
@keyframes stamp { from { opacity: 0 } to { opacity: 1 } }
```

**This is a deliberate exception to "under 100ms reads as a jump-cut".** That
rule governs anything that *travels* — a jump-cut is what you get when a
distance is crossed in no time. An element that never moves has no distance to
cross, so it can arrive instantly. The test is whether the element has a
trajectory: if it does, ease it; if it simply appears in place, stamp it.

Don't mix the two on one element — a stamp that then drifts reads as a bug —
and don't mix them across a set. Pick the register per artifact the same way
you pick one entrance type.

**A stamp needs somewhere to hold.** This register only works with generous
dwell: 0.6–1.2s a beat in the references, with genuinely empty frames between
them. Reveal → hold → clear → about 250ms of nothing → next. That air is
structural; without it a stamped sequence reads as a flicker.

### The stepped finish

The measured recipe (`references/sources.md` §12, §14) posterizes time to
**12fps across the whole composition**, not only on hand-drawn elements, and
lays a subtle chromatic fringe over everything. Stepping is what stops smooth
interpolation reading as computer-generated.

The web equivalent is `steps()` on the ambient moves, at 12 steps per second of
duration:

```css
.stepped { animation: drift 8s steps(96, end) infinite alternate; }  /* 8s × 12 */
```

Reserve it for a piece that is deliberately hand-made in register. Stepping a
UI-scale transition just makes it look dropped-frame.

## Rhythm — pace to the copy, not a clock

Where the beats fall matters more than how any single one is eased, and it is
the decision most often surrendered to a uniform delay.

**Measured across the reference set** (`references/sources.md` §14): twelve of
thirteen clips carry no music bed at all. Every cut, caption swap and graphic
reveal lands on a **voiceover phrase boundary or a stressed word**. The rhythm
engine is language, not a grid.

Nothing in an artifact speaks, but a reader still reads at the pace of the
sentence, so it transfers directly:

- **Time each beat to its own copy**, not to a shared constant. A four-word
  line and a two-clause sentence do not get the same dwell. Allow roughly the
  time it takes to read the line aloud, plus a beat.
- **Put the transition in the pause.** In the strongest reference, the only
  three moments of true silence across sixty seconds are its three biggest
  visual pivots. Change scene where the sentence ends, never mid-clause.
- **Uneven is correct.** A metronomic beat every 3s is the tell that a timeline
  was filled rather than written.

### One hit per piece

Sound in the references is never decoration: every transient *is* a visual
event, and the loudness hierarchy matches the visual hierarchy exactly. A small
text pop gets a small tick; exactly **one whoosh or impact per piece** is
reserved for the single most important moment, and everything else stays quiet.

That is the one-accent rule arriving from the audio side, and it is the useful
form of it for motion: **one move is allowed to be bigger than the others, and
it belongs to the moment that matters.** If two moves are competing for that
job, one of them is decoration.

### Silence is structural

Every reference ends with two to three seconds of dead silence after its final
hit, and leaves real air between beats. The visual equivalents:

- **Let the finale settle.** Nothing new arrives after the payoff — see the
  ending guidance in the editorial-explainer skill.
- **Leave air between beats.** A moment of near-empty frame is not a gap to be
  filled; it is what makes the next arrival land. (Air between *beats* — within
  a single thought, dim the spent line rather than clearing it. See **Exits**.)
- **Stillness is available as an effect.** The references go completely still
  only where stillness is the point — one clip freezes precisely to demonstrate
  "lifeless". Everywhere else, something drifts.

**If you are producing actual video** rather than a silent artifact, all of this
becomes literal: cut on the phrase, design one hit, match foley 1:1 to what
moves, and end quiet.

### Three rules from the audio side the silent form keeps losing

From the sound-design breakdown in `references/sources.md` §15:

- **Restraint is the technique.** The clearest passage in the whole reference
  set is a decision *not* to sound-design: *"I'm actually just going to ignore
  the text and the arrows drawing on. I'm just going to sound design this
  building in the middle."* The motion translation is stronger than one-accent:
  **do not animate the supporting elements at all.** Let them be present.
- **J-cut.** Sound leads picture by ~120ms — *"it helps people's brains prep for
  the scene."* Silent equivalent: a precursor element (plate, rule, shadow,
  underline) arrives ~100–150ms before the thing it introduces.
- **Deliberate desync.** *"The sound effects don't actually have to be perfectly
  lined up with the movement. You can knock them a few frames around."*
  Everything landing on one frame is a tell. Offset related elements by a frame
  or so rather than snapping them to the same instant.

`assets/sfx.js` implements all three literally, for artifacts that can carry
sound. It synthesises the reference's six folders in Web Audio — no sample
library — enforces the one-accent rule and the −20 to −10 dBFS window, and is
**muted by default** behind an explicit toggle. `assets/sfx-test.html` measures
what actually comes out; run it after any edit, since a gain value is not an
output level.

## The ceiling

**One ambient move plus one accent move per composition. That is the maximum.**

- *Ambient* — always on, no visible reset (gradient drift, slow push-in, grain
  flicker, halftone shimmer).
- *Accent* — one beat inside the loop (word-stagger blur-in, line-stack build,
  sticker pop, cutout rise, annotation draw-on).

Exceeding this is the most common way a well-built set turns to noise. Keep the
same easing and stagger across every asset even when the moves differ — that
consistency is what reads as a system.

**Movement never crosses the composition's optical centre** unless it is the
hero element.

## Stagger

Sequence siblings at **60–90ms** apart. Below 50ms they read as simultaneous;
above 120ms the sequence starts to drag.

```css
.item { animation: rise 520ms var(--ease-out) both; }
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 70ms; }
.item:nth-child(3) { animation-delay: 140ms; }
```

For arbitrary counts, set `--i` on each element and compute:
`animation-delay: calc(var(--i) * 70ms);`

Stagger in **reading order**, not DOM order, when they differ.

---

## Cutting the curve

The single most useful technique in the reference set (see
`references/sources.md` §2). It makes a hard transition read as continuous motion.

**The principle:** animate with a *heavy* ease-in-out so the velocity graph is a
tall narrow spike, then change the content at the exact moment the element is
moving fastest. Both sides of the cut are travelling at speed in the same
direction, so the eye reads one continuous movement and stops registering the
transition as a cut.

**Why it works:** at peak velocity the element is motion-blurred and spatially
ambiguous. The viewer's eye is tracking a trajectory, not a shape, so it accepts
whatever arrives next on that trajectory.

Applied to a slide or section change:

```css
@keyframes swap-out { /* first half: accelerate hard, exit at max speed */
  from { transform: translateX(0);      opacity: 1; }
  to   { transform: translateX(-14vw);  opacity: 0; }
}
@keyframes swap-in {  /* second half: enter at max speed, decelerate hard */
  from { transform: translateX(14vw);   opacity: 0; }
  to   { transform: translateX(0);      opacity: 1; }
}
.leaving { animation: swap-out 260ms cubic-bezier(0.55, 0, 1, 1) both; }
.entering{ animation: swap-in  260ms cubic-bezier(0, 0, 0.45, 1) both; }
/* The two halves meet at peak velocity. Fire .entering exactly when
   .leaving ends — no gap, no overlap. Equal durations are essential. */
```

Three things break it, and all three are common mistakes:
- **A gap between the two halves.** Even 30ms of stillness exposes the cut.
- **Mild easing.** A gentle ease has no velocity peak to hide in.
- **Direction change.** Both halves must travel the *same way*. Out-left then
  in-from-left reads as a bounce, not continuity.

### Anchor-object continuity

The cheaper and more robust cousin, used constantly in the references: **keep
one element fixed and change everything else around it.** A circled figure
holds its position while the background swaps beneath it; a giant keyword stays
put while the word under it changes.

Because the anchor never breaks, the eye has nothing to re-acquire, and the
change reads as a new subject rather than a new scene. It also survives what
cutting the curve cannot — a still screenshot, and a reader who is scrolling
rather than watching.

```css
/* everything except .anchor is inside the swapping layer */
.swap      { animation: cut-out 240ms var(--ease-in) both; }
.swap.next { animation: cut-in  240ms var(--ease-out) both; }
.anchor    { /* no animation at all — that is the technique */ }
```

Three conditions. The anchor must be the thing the two states genuinely have in
common, so it is carrying the argument rather than decorating it; it must not
move at all during the swap; and it must be the dominant element, or the change
behind it wins the frame.

---

## Movement paths

**Travel along arcs, not straight lines.** Straight-line translation is the
default in CSS and it is what makes generated motion look mechanical. Curve it:

```css
/* Simplest method: different easing per axis produces a curved path */
@keyframes arc-in {
  from { transform: translate(-40px, 30px); opacity: 0; }
  to   { transform: translate(0, 0);        opacity: 1; }
}
.arc { animation: arc-in 560ms both;
       animation-timing-function: cubic-bezier(0.16,1,0.30,1); }
```

For a true arc, animate a wrapper on X and the child on Y with different curves,
or use `offset-path` where support allows:

```css
.travel {
  offset-path: path("M 0 0 Q 120 -60 240 0");
  animation: move 900ms var(--ease-in-out) both;
}
@keyframes move { from { offset-distance: 0%; } to { offset-distance: 100%; } }
```

## Entrance vocabulary

Pick **one** per design and repeat it. Mixing entrance types across a single
page is the fastest way to look incoherent.

```css
/* Rise — the safe default. Small distance, never more than ~24px. */
@keyframes rise { from { opacity:0; transform: translateY(18px); }
                  to   { opacity:1; transform: none; } }

/* Blur-in — for titles and hero type. Reference §5. */
@keyframes blur-in { from { opacity:0; filter: blur(14px); transform: scale(1.04); }
                     to   { opacity:1; filter: blur(0);    transform: none; } }

/* Grow-from-baseline — bars, meters, anything measured from an axis. */
@keyframes grow { from { transform: scaleY(0); } to { transform: scaleY(1); } }
.bar { transform-origin: bottom; }   /* essential, or it grows from the middle */

/* Wipe — reveals text or images along their reading direction. */
@keyframes wipe { from { clip-path: inset(0 100% 0 0); }
                  to   { clip-path: inset(0 0 0 0); } }
```

Distances stay small. A card sliding 200px looks like it was thrown; 18px looks
like it settled.

## Exits

Generated work animates arrivals and then either cuts or fades. The references
design leaving as carefully as arriving, and three patterns are worth having.

**Erase, don't cut.** An annotation that drew itself on un-draws before the
scene changes — reverse `stroke-dashoffset` over about half the draw-on
duration. Anything built by a wipe can leave the same way, in the same
direction.

**Mirror the entrance.** If characters arrived in random order they leave in
random order; a stack that built bottom-up leaves top-down. That symmetry is
most of what makes a loop read as composed rather than merely restarted.

**Accumulate, then dim — don't clear.** When a second thought follows a first,
the references usually leave the first on screen and drop it to about 30%. The
reader keeps the context and the new line still takes the focus. Clearing is
for a genuine change of subject.

```css
.spent { opacity: .3; filter: saturate(.4);
         transition: opacity 320ms var(--ease-out),
                     filter  320ms var(--ease-out); }
```

Exits run **faster than entrances** — about 60–70% of the duration. A slow exit
is the reader waiting for permission to look at the next thing.

---

## Focal point and dimming

From `references/sources.md` §4 — the named failure mode is a frame with "no
hierarchy, no focal point". The fix is subtractive: **push everything back, then
pull one thing forward.**

```css
.stage.focusing .panel        { opacity: .28; filter: saturate(.5); transform: scale(.98); }
.stage.focusing .panel.active { opacity: 1;   filter: none;         transform: scale(1.03); }
.panel { transition: opacity 420ms var(--ease-out),
                     filter  420ms var(--ease-out),
                     transform 420ms var(--ease-out); }
```

Dim to roughly **25–35% opacity** — deep enough to genuinely recede, shallow
enough that context survives. Scale the active element up only slightly (1.02–1.05);
larger and it detaches from the layout.

The same logic drives **highlighting inside text or data**: instead of colouring
the important part, desaturate everything else and leave the important part at
full strength.

## Scroll as narration

From `references/sources.md` §3. When you have a sequence of comparable panels —
years, steps, regions, options — do not tab between them. Stack them and let
scroll drive the story, with the centred panel active and the rest dimmed.

```js
const io = new IntersectionObserver(
  entries => entries.forEach(e => e.target.classList.toggle('active', e.isIntersecting)),
  { rootMargin: '-42% 0px -42% 0px' }   // narrow band = only one panel active at a time
);
document.querySelectorAll('.panel').forEach(p => io.observe(p));
```

Keep every panel's geometry **identical** — same size, same position, same axes.
Only the data changes. Identical framing is what lets the eye compare; if the
panels shift around, the comparison is lost and it becomes a slideshow.

## Numbers should count

Any figure presented as a headline stat should animate to its value rather than
appear at it. Count over 700–1000ms with `--ease-out` so it decelerates into the
final number, and never re-run it on scroll-back — a stat that recounts every
time it enters the viewport is irritating.

---

## Non-negotiables

**Respect reduced motion.** Always, in every artifact:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Note this preserves the *end state* — content still arrives, it just arrives
immediately. Never hide content behind an animation that reduced-motion cancels.

**Animate only `transform`, `opacity`, `filter` and `clip-path`.** Animating
`width`, `height`, `top`, `left` or `margin` forces layout on every frame and
will judder. If you need a size change, use `scale` with a corrected
`transform-origin`.

**Add `will-change` only to elements actually animating**, and remove it after.
Blanket `will-change` costs memory and can make things slower.

**Set `both` as the fill mode** on entrance animations (`animation: rise 500ms
var(--ease-out) both`) so elements hold their pre-animation state during any
delay instead of flashing at full opacity first.

## Self-check before delivering

- **Does it work as a still screenshot?** If not, nothing else matters.
- Is it legible at 200px wide? Grain and fine texture turn to mud at thumbnail.
- Is there at most one ambient and one accent move?
- Is there exactly one focal point at any given moment?
- Are siblings staggered rather than simultaneous?
- Is every easing curve non-linear — or deliberately in the snap register, with
  the dwell to support it?
- Is each beat timed to its own copy, or is everything on the same delay?
- Is exactly one move the biggest one, and is it on the moment that matters?
- Does anything leave the way it arrived, or does it all just cut?
- Do transitions cut on the velocity peak, or is there a dead gap?
- Does movement stay off the optical centre unless it's the hero?
- Does `prefers-reduced-motion` work?
- Are any layout properties being animated?

---

## Assets

- `assets/motion.css` — the easing set, house timing kit, entrance vocabulary,
  stagger and the reduced-motion block. Paste into any artifact.
- `assets/sfx.js` — procedural sound design for artifacts that can carry it.
  Web Audio, no sample library, muted by default behind an explicit toggle.
  Enforces the one-accent rule, the J-cut lead and the −20 to −10 dBFS window.
- `assets/sfx-test.html` — renders every voice offline and measures the peak
  that actually comes out. Run it after editing `sfx.js`: a gain value is not
  an output level, and the filters attenuate each voice differently.
- `assets/render.py` — renders an animated artifact to MP4, frame by frame, at
  the house 12fps. Needs Chrome and ffmpeg, nothing else.

**It refuses to produce a frozen video, and does so by default** — frozen is the
failure mode you will not notice until someone else watches it. `transform` and
`opacity` animations run on the compositor thread, so the obvious implementation
of a frame-stepper captures the same instant every time and still writes a
plausible-looking file. `render.py` sets each animation's `currentTime`
explicitly for this reason, and the pre-flight probe measures how much the first
and last frames differ rather than merely whether they differ. `--no-check` opts
out, and is only right for a piece that is deliberately static.
