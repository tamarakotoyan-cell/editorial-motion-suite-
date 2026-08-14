---
name: editorial-explainer
description: Data-journalism structure and craft for generated design — charts, data stories, infographics, explainer slides, report visuals, social data tiles, and any artifact whose job is to make a number or a finding land. Supplies composition, chart form, texture, annotation and editorial device; takes colour and typeface from the installed brand system rather than defining its own. Pair with motion-system for movement and layout-composition for grid and proportion.
---

# Editorial explainer

The craft of broadcast and newspaper data journalism: confident, textured, one
idea per frame. It is the opposite of the default generated-artifact aesthetic —
soft gradients, rounded cards, evenly-weighted everything — which spreads
attention evenly instead of spending it all in one place.

**This skill supplies structure, not identity.** Colour and type come from the
brand system. What follows is composition, chart form, texture, annotation and
editorial device — the parts that are craft rather than someone's trade dress.

## Precedence

1. **The client's brand**, whoever the client is. Colour and typeface come from
   them. Work is produced for many clients — Essential's own system is simply
   the case where the client is Essential. See
   `references/brand-integration.md`, and `references/essential-tokens.md` for
   that one case.
2. **The house ban list** — `references/house-rules.md`. Where the reference
   material and the ban list disagree, **the ban list wins**.
3. This file.

### Take the brand lightly

**Minimum viable brand: one typeface in the right register, one colour that
connects. Everything else neutral.** That is nearly all of it.

Past that point, extra brand assets stop adding recognition and start making the
work look like a guidelines document. Leave the rest of the palette, the brand
patterns and motifs, the repeated logos, and any sub-brand colours that don't
belong to this job.

The test: someone who knows the client should recognise the work as theirs;
someone who doesn't should just see a clear, well-made graphic. If a brand
element is present and you can't say what job it does in *this* frame, remove it.

Layout and proportion decisions belong to **layout-composition** and happen
first. Movement belongs to **motion-system**.

### Before you build

Write the five-line plan — finding, colour, type, layout, **signature** — and
critique it against "would I have written this for any other finding?" before
opening a file. `references/design-method.md` has the method, adapted from
Anthropic's `frontend-design` skill: where to spend boldness when the palette
and typeface are not yours to invent, how to name the one move the piece will
be remembered by, and how to check that the house style has not quietly become
a template.

### Before you ship

`references/ending.md` covers how a piece ends — the part this skill used to
stop short of. Measured ending grammar from the reference set, how to keep the
payoff from playing behind a panel, how to stop the finale paying for other
beats' layout reservations, how long the dead tail may run, and how to freeze
a frame for inspection without diagnosing a bug that is not there.

---

## Craft versus trade dress

The reference material for this skill is largely Vox and Vox-adjacent (see
`../motion-system/references/sources.md`). Much of what makes it good is general
data-journalism craft, some of it predating Vox by a century. Some of it is
Vox's identity. **Take the first, never the second.**

**Craft — transferable, use freely**

- One idea per frame
- Exactly one accent; everything else neutral
- Direct labelling instead of legends
- Unit and dot charts (ISOTYPE, Vienna, 1920s — long predates anyone)
- Small multiples with identical geometry (Tufte)
- Hand-drawn annotation over a chart (universal across NYT, FT, Reuters, Pudding)
- Texture and grain instead of flat digital surfaces
- A large figure with a small caps label beneath
- Emphasis by dimming everything else
- Scroll-driven narration
- Section structure and chapter breaks
- Presenting data as the document it came from

**Trade dress — recognisably Vox, do not reproduce**

- Their cobalt-and-lemon pairing, or any close variant of it
- A yellow circular roundel mark
- Their high-contrast display serif as the signature voice
- Yellow highlighter as a *brand* device rather than an emphasis tool
- Their specific chapter-card format

The test: if someone could name the publication from a still frame, it has gone
too far. The aim is work that looks like it came from a serious newsroom —
not from *that* newsroom.

### The other trade dress: tutorial chrome

Most of the reference set is not Vox. It is **creator tutorials about Vox**,
filmed for TikTok (see `../motion-system/references/sources.md` §14). They
arrive wrapped in a second layer of borrowed identity that is easy to absorb by
accident, because it is the most visually prominent thing in the frame:

- Red or black **caption pills** carrying two or three words at a time
- A **platform end-card** — logo, handle, search-bar pill, RGB-split glitch
- **Watermarks and handles** parked in a corner
- The **logo sting then silence** outro
- **Talking-head cutaways** and screen-recordings of the software

None of it is editorial craft. It is the packaging of a format whose job is to
sell a tutorial, and in client work it reads as a TikTok pastiche rather than as
a newsroom graphic. Take the technique out of these references; leave the
wrapper. A caption pill in particular is a *subtitle*, not a design device —
if the words matter, they are the headline.

---

## The governing idea

**One frame, one fact.** Every screen states exactly one thing. If a chart needs
two sentences to explain, it is two frames.

From the house rules, and it is upstream of everything else here: most AI slop in
a data graphic is a **point-of-view problem, not a styling problem** — the chart
weights everything equally because nothing decided what the finding was. State
the finding in one sentence before designing. If you can't, it isn't ready.

---

## Colour, as roles

Do not define a palette. Define **roles**, and fill them from the client's brand
— taking only the accent and, if they have them, the ink and surface neutrals:

| Role | Job | Count |
|---|---|---|
| `ground` | The surface everything sits on | 1 |
| `ink` | Primary text and marks | 1 |
| `muted` | Axis labels, captions, secondary text | 1 |
| `accent` | The mark that proves the finding | **exactly 1** |
| `secondary` | The opposing side in diverging data only | 0–1 |

**The accent rule is the whole system.** One bar in the accent among neutral
bars; one line saturated among grey lines. The moment a second element takes the
accent, the frame loses its focal point. If two things genuinely matter equally,
they are two frames.

### Neutrals must be separable, not just neutral

The commonest encoding failure is two "greys" that are the same colour at
different alpha — say white at 34% and at 72% on a dark ground. Both read as
*greyish*, and a viewer cannot reliably say which category is which.

Separate categorical neutrals on **two axes at once**, and make them opaque:

| Role | On a dark ground | On a light ground |
|---|---|---|
| accent | the brand accent | the brand accent |
| substantive opposing group | near-white / bone | near-black ink |
| neutral / unsure middle | mid warm grey | light warm grey |

That gives high-chroma, high-luminance and mid-luminance — three steps
distinguishable at a glance and in greyscale.

Rules:

- **Separate on luminance, and check the number.** Hue alone is not enough —
  two colours can differ in hue and still collapse into each other in print, in
  greyscale, or for a colour-blind viewer. Hold **every pair of mark colours
  ≥25 L apart, and every mark ≥25 L from its own field.** Write the L values
  into a comment beside the tokens so the next edit cannot quietly break it.
- **The field counts as one of the colours.** A mid-grey mark on a light warm
  field is the pairing that fails most often — it passes against the other marks
  and disappears against the ground. Check marks against the field first.
- **Re-check on every field change.** A palette that separates on a light field
  will not automatically separate on a dark or saturated one. Give each field
  its own mark set rather than reusing one across all of them.
- **A hairline outline on legend swatches** costs nothing and rescues the light
  swatch on a light ground.
- **Opaque fills, not alpha ramps of one colour.** Reserve alpha for
  *de-emphasis* (pushing a group back), never for *category*.
- **Two categorical neutrals is the ceiling.** A third is not separable without
  reaching for hue, and a second hue breaks the accent rule.
- **Fix the meaning and keep it.** Decide what accent, bone and grey each mean,
  and hold it across every state. A colour that changes meaning between scenes
  destroys the continuity a persistent-mark system exists to create.
- **Name the colours on screen.** A legend with filled swatches beside the
  figure — this is the one place a legend earns its keep, because the categories
  are carried by colour alone.
- Check in greyscale, and at 200px.

**ΔL separates marks; it does not make text readable.** The two measures answer
different questions and a palette can pass one while failing the other. Run both:

| | Measure | Floor |
|---|---|---|
| Mark vs mark, mark vs field | **ΔL** | ≥25 |
| Deck, source line, axis labels, captions vs their field | **contrast ratio** | ≥4.5:1 |
| Any text below ~14px or set in a light weight | **contrast ratio** | ≥4.5:1, and reconsider the size |

Measured on the reference set (`../motion-system/references/sources.md` §16):
a Vox-style build whose source line is a warm grey on cream sits at **ΔL 30.7 —
comfortably past the mark floor — and 2.48:1, which is unreadable.** ΔL rewards
it for being separable from the paper; nobody was asking whether it was
*separable*, they were asking whether it could be read. Vintage and muted
palettes fail here routinely and the failure is invisible on a large bright
display, which is where it gets signed off.

(The same build's bars sit at ΔL 18.5 against their card — a straight failure of
the ≥25 rule above, and the reason the chart evaporates at 200px.)

Semantic colour (good / warning / critical) is separate from the accent and does
not count against it.

Where the brand offers several accents, pick **one per artifact** and hold it
across the whole set. Rotating accents between tiles destroys the family.

**Two grounds work.** A near-black ground for charts, where a colour field would
compete with data. A saturated brand-colour field for statement frames, with
content inset against it rather than full-bleed. Choose one per artifact.

## Typography, as roles

Take the faces from the brand system. Assign them:

- **Display** — the finding, the section title. Large, tight leading (~1.02),
  never letter-spaced.
- **Body / deck** — supporting sentence. Near 65 characters per line.
- **Utility** — axis labels, captions, chip text. Small, uppercase,
  letter-spaced ~.08em, muted.
- **Hero figure** — the utility or body sans, set very large. ⚠️ Never a serif or
  display face on the hero figure.

**The editorial feel comes from scale contrast and restraint, not from borrowing
a display serif.** Reach for a Perfect Fourth (1.333) scale via
**layout-composition** so display, heading and body read as three distinct
registers. A brand's own sans, set with a dramatic size jump and disciplined
spacing, reads more editorial than a borrowed serif ever will — and it stays
yours.

### ⛔ Never put a capitalised overline above a heading

No small uppercase letter-spaced kicker, eyebrow or overline sitting above the
title. It is one of the most recognisable generated-design tells, it duplicates
information the heading already carries, and it pushes the actual heading down
the page.

This holds even when the brand system defines overline tokens — their existence
is not an instruction to stack one above every heading.

**Instead:** let the heading carry it, and put any qualifying detail in the
sub-line *below*. If a label genuinely must appear, place it beside or after the
content, never stacked above the title.

```html
<!-- no -->
<p class="kicker">KEY FINDINGS</p>
<h2>Support fell nine points</h2>

<!-- yes -->
<h2>Support fell nine points</h2>
<p class="sub">Across all age groups, sharpest among renters.</p>
```

Uppercase letter-spaced type is still fine for axis labels, chip text and table
column heads — the ban is specifically the overline-above-a-heading pattern.

Headings themselves are **sentence case**, not title case and not caps.

## Texture

Flat digital surfaces are the tell of generated design. Every reference frame
carried at least one texture layer.

```css
.grain::after{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:99;
  opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

Grain at **4–6%**. At 10% it stops reading as texture and starts reading as a
broken image. ⚠️ Check at 200px — grain turns to mud at thumbnail size.

**Print fringe.** The measured recipe adds a barely-visible chromatic offset
over the whole composition — the reference describes it as "easy to go
unnoticed", which is the correct strength. It reads as misregistered printing
and it is most of why the references never look like vector art.

```css
.fringe { text-shadow: -0.6px 0 0 rgba(255,0,80,.28),
                        0.6px 0 0 rgba(0,190,255,.28); }
```

Sub-pixel offsets only, on display type and hairline edges. ⚠️ Never on body
copy, never on data marks, and check it at 200px — at thumbnail size an offset
that read as print texture reads as a rendering fault.

### Paper textures go under the content, not over it

Scanned paper — folded, ruled, crumpled — is the strongest ground texture
available, and the fastest way to ruin a layout. **Layer it above the colour
field but below the marks and all copy.**

A paper scan sitting *over* the content with a multiply blend darkens every
letterform a crease happens to cross. That is unpredictable per-render, it
attacks exactly the type you most need read, and it cannot be fixed by nudging
the copy because the creases run the full height of the sheet.

```css
.paper       { position:absolute; inset:0; z-index:2;  /* field is 1 */
               background-size:cover; pointer-events:none }
.paper-light { mix-blend-mode: multiply }    /* creases darken a light field */
.paper-dark  { mix-blend-mode: soft-light }  /* creases lift a dark field    */
/* marks sit at z-index 5, copy at 12 — both above the paper */
```

- **Blend by field.** Multiply on light grounds; a white scan multiplied over a
  dark ground does nothing, so use soft-light or overlay there instead.
- **Opacity 18–30%.** Enough to read as material, low enough that the field's
  luminance barely moves — re-check your ≥25 L mark separation after adding it.
- **One texture per act**, changing at the same boundaries as the field. Ruled
  paper suits a record or a trend; crumpled suits a conclusion.
- **Full-frame photographs cover the paper**, not the reverse. Order the layers
  field → paper → photo so a photo beat is clean.
- Keep the fine grain layer as well. Paper gives structure at large scale; grain
  keeps the surface from looking flat at small scale. They do different jobs.

Other options: a faint rule grid over a colour field; a paper or woven fibre
ground for document-style frames. One texture layer, not three.

---

## Chart patterns

**Form first.** Pick the chart type from the data's job — magnitude, identity,
polarity, change over time, or a single headline. If the finding is one number,
it is a stat tile, not a chart.

**Count rather than measure.** Under roughly 200, draw one mark per unit. A
cluster of 120 dots reads as *a hundred and twenty things*; a bar of height 120
reads as an abstraction.

### ⛔ The mark must equal the number

Every mark in one chart shares a single scale: **length ÷ value is constant
across the series.** Compute the geometry from the datum — never draw marks that
look about right and type the numbers on afterwards.

```html
<!-- the datum is the only source of length -->
<div class="bar" style="--v: 62"></div>
<style>.bar { width: calc(var(--v) * 1% * var(--plot-scale)); }</style>
```

This is not a pedantic check. It is the failure mode of the reference material
itself: a measured Vox-style tutorial
(`../motion-system/references/sources.md` §16) ships a bar chart in which the
**85% bar is the shortest on the chart**, a third the length of the 43% bar, and
a finished build whose three bars run at 8.4, 9.2 and 11.0 px per percent. Both
look plausible at a glance. Both are wrong, and neither is wrong in a way a
reader can catch.

**Corollary: no axis without a scale.** Drawing a `0…100%` axis under marks that
do not obey it is worse than drawing no axis, because the axis is a promise
about how to read the marks. Either the ticks derive from the same scale as the
geometry, or there are no ticks.

**Corollary: a value label is not a substitute for a correct mark.** If the
number has to be read to know the magnitude, the chart is doing nothing that a
sentence would not do better.

### Marks persist — the central technique

**The most common failure is animating the *arrival* of data instead of the data
itself.** Bars grow, text fades, the chart is done. Then the next scene wipes it
and draws different marks. That reads as a slide deck with transitions, not as
motion graphics, and it is the single biggest gap between generated output and
the reference material.

What the references actually do: **the same marks stay on screen and rearrange.**
A cluster of dots becomes a sorted grid, becomes an isolated subgroup, becomes
columns, becomes a block. Nothing is destroyed and redrawn. The chart is not the
destination — it is one *state* in a continuous system.

Why it works: object permanence turns a sequence of charts into a single
argument. When a dot moves from the "all respondents" cloud into the "36% say
risk" group, the viewer *sees* the subsetting happen. Fade one chart out and
another in, and they have to take your word for it.

**Build it as a particle system, not as chart elements.**

```js
// One population, many layouts. Layouts return a target per index.
const N = 336;                       // 1 dot ≈ 3 respondents — state the ratio
const layouts = { cloud, waffle, isolate, trend, block };

// Per dot: lerp position, radius, alpha and colour toward the target,
// with a per-dot stagger so the set sweeps rather than snapping.
const p = clamp((time - stateStart - dot.delay) / TRANSITION, 0, 1);
const e = 1 - Math.pow(1 - p, 3);                     // ease-out cubic
dot.x = lerp(from.x, to.x, e);
```

Rules that make it read well:

- **Transition 1.2–1.5s** with **0.4–0.6s** of total stagger spread across the
  population. Faster and it snaps; slower and it drifts.
- **Bow the paths.** Add a small sine-based offset perpendicular to travel so
  dots arc. Straight-line lerp is the mechanical tell.
- **Sort the stagger** so the eye reads a sweep — by index, by group, or by
  destination — never randomly.
- **Interpolate colour too.** A dot joining the accent group should *become*
  accent over the move, not switch instantly on arrival.
- **Pick the unit so every state sums to a visible whole.** Default to
  **one dot = one per cent** — a hundred dots in a 10×10 grid. Then "63%" is
  literally 63 dots counted against a denominator that is on screen. A unit like
  "one dot ≈ three people" forces rounding in every state and leaves shares
  floating with nothing to read them against.
- **Never show a share as a blob with no denominator.** If a state shows the
  63% and scatters the other 37 into the void, the figure has nothing to be a
  share *of*. Show all response options; the remainder is part of the fact.
- **Isolating one group destroys the denominator.** Pulling 36 dots into a
  floating square leaves a shape that is 36 of nothing — the hundred you built
  is gone, and the square carries no reading. Two ways out, both better:
  **keep the grid and change emphasis** (the group brightens in place, the rest
  drop to ~40%), so you also see *where* in the hundred they sit; or
  **compare the two groups directly**, which is usually the real finding.
- **Compare with a shared width so height carries the count.** Two stacks the
  same number of dots wide — 22 becomes four rows, 36 becomes six — makes the
  gap a visible size difference you can count. Stacks of differing widths turn
  the comparison into an area judgement, which nobody makes accurately. Keep
  the untouched remainder greyed and on screen so the total still reads 100.
- **State the unit on screen**, and re-state the base whenever it changes.

### Objects transform — the general form of persistence

**Marks persist** is the chart-scale case of something the references apply to
every element on screen. The strongest reference in the set runs sixty seconds
with a *single* hard cut: nothing is destroyed and replaced, so the piece reads
as one continuous argument rather than a sequence of slides.

Four devices carry it, and all four are cheap:

**Scale hand-off.** An element shrinks or grows to *become* a component of the
next idea. A photographed figure scales down to become the single unit in a
pictogram of 750,000; a rolling dot grows into the circle that holds the next
stat. The viewer follows one object across a change of subject, which is what
makes the second idea feel earned by the first.

**Line leads, content follows.** A connector — a dashed leader, a rule, an
arrow — draws itself *first*, and the thing it labels arrives at its endpoint
once it gets there. The path is built before it is populated, so the eye is
already looking at the right place. Later, things travel that path: in the
reference, coins roll along the same dotted connector that linked the two
objects.

**Build, then label.** The quantity is drawn before the number is typed. A
pictogram fills, a brace draws under it, *then* "750,000" arrives with its
highlight. Reversing this — number first, marks assembling under it — throws
away the only moment where the reader is counting.

**One element survives each change.** The anchor-object pattern in
motion-system, applied at the scale of the whole piece: something is always
held over from the previous state.

```js
// State changes move and restyle existing elements. Nothing is removed.
// If a state needs an element the previous one lacked, it enters — but
// nothing the two states share is ever destroyed and rebuilt.
const nextIds = new Set(next.map(el => el.id));
const carried = prev.filter(el => nextIds.has(el.id));   // must not be empty
```

The discipline this imposes is useful in itself: if two consecutive frames share
*no* element, they are probably two separate pieces, and the join between them
is the weakest point in the argument.

### Cut between graphics and photography — never layer one under the other

The commonest way a data piece ends up looking like generic social content:
photographs sitting behind the graphics at 40–60% opacity, permanently, as
wallpaper. The reference material almost never does this.

What it does instead is **alternate**:

```
[colour field · data inset]  →  CUT  →  [photograph, full frame]  →  CUT  →  [colour field · data]
```

- **Graphic beats** sit on a saturated colour field with the data in an **inset
  panel** — margins visible on all sides, never full bleed. A faint rule grid
  runs over the field.
- **Photo beats** are **full frame and undimmed**, held 2–3s as their own
  moment, with a hard crop, a slow punch-in, and a small caption chip. The
  photograph is evidence making its own point, not atmosphere.
- **The field colour changes only at beat boundaries** — one hue per scene.

Why it matters: a permanently-dimmed photo is doing neither job. It is too
present to be neutral ground and too suppressed to be evidence, so it just
lowers contrast on the data. Giving it its own beat lets it be at full strength,
and lets the data have a clean field.

A photo beat also earns the cut. Alternating registers — flat graphic, then
photographic — is most of what gives these pieces their rhythm.

### Zone the canvas — measure, don't guess

Marks drawn to fractions of the frame height (`y = H * 0.40`) will sooner or
later sit on top of the legend, because copy blocks change height with their
content and the tallest state is not the one you designed against.

**Derive the drawing band from the copy blocks themselves:**

```js
const PAD = 18;
const topH = headlineBlock.getBoundingClientRect().height;   // tallest headline
const botH = legendBlock.getBoundingClientRect().height;     // tallest legend
const bandTop = TOP_INSET + topH + PAD;
const bandBot = H - BOT_INSET - botH - PAD;
const bandMid = bandTop + (bandBot - bandTop) / 2;

// the grid must fit the band on BOTH axes
const gap = Math.min((bandBot - bandTop) / 10.6, (W - 64) / 10.6);
```

Every layout — grid, cloud, isolated block — centres on `bandMid` and is sized
from `gap`, so all of them inherit the same guarantee. Re-run on resize, and
once more on a short timeout after first paint so webfont metrics have settled.

Measure against the **tallest** copy block, not the current one, or the band
will breathe between states and the marks will jump.

**Measure every block, not a representative one.** Reading the height off a
single element by id looks like it satisfies the rule and does not — the sampled
beat is rarely the tallest, and any beat with more copy then overlaps the marks.
Query them all and take the maximum. Blocks hidden with `opacity` are still laid
out, so they measure correctly even when invisible:

```js
const hOf = sel => Math.max(0, ...[...document.querySelectorAll(sel)]
                                   .map(el => el.getBoundingClientRect().height));
const topH = hOf('.blk.top');     // every headline block
const botH = hOf('.blk.bot');     // every legend block
```

Hiding with `display:none` instead would break this — the elements would measure
zero and the band would size itself from nothing.

**Decoration inside a heading must not join the text flow.** An underline or
highlight added as a block-level child changes the heading's height, which then
feeds the band maths and shifts the marks. Scope it to the word and take it out
of flow:

```css
.uw { position: relative; display: inline-block; }   /* wraps the word */
.ul { position: absolute; left: 0; width: 100%; bottom: -11px; }
```

**Reserve a row for anything that appears mid-band.** A read-out that only shows
during one beat — a year label, a running figure, a callout — still needs its
own permanent slot in the layout maths, subtracted from the band in *every*
state. Positioning it "just above the marks" works until the marks move.

```js
const WAVE_H = 64;                       // reserved in every beat
const readoutTop = TOP_INSET + topH + PAD;
const bandTop    = readoutTop + WAVE_H;  // marks start below it, always
```

**Draw labels that annotate marks onto the same surface as the marks.** A DOM
chip positioned against canvas geometry has to be re-derived on every resize and
re-measured whenever the data changes — and it drifts, overlaps, or lands in a
gap too narrow to hold it. Draw the label in the canvas from the same variables
that place the marks and it cannot come apart:

```js
if (state.pos === 'compare') {
  const topL = baseY - (Math.ceil(22/cw) - 1) * cg - cg * .31;   // same maths
  ctx.textAlign = 'center';
  ctx.fillText('22', leftX + (cw - 1) * cg / 2, topL - cg * 0.62);
}
```

**A floating callout is usually a copy problem in disguise.** "14 points clear"
hovering over two stacks reads as arbitrary; the same fact in the headline —
*"Risk beats opportunity by fourteen points"* — reads as the point of the frame.
Label the marks with their own values, and let the sentence carry the comparison.

**Keep marks and full-frame imagery out of the same frame.** When a photo beat
and a data beat are adjacent, hide the canvas across a window slightly *wider*
than the panel's visible period — 0.2–0.3s of margin either side. Timings that
meet exactly on paper still collide for a frame or two once easing, fade-out and
the next state's stagger overlap.

**Verify the timeline with arithmetic, not by eye.** For every state, compute
`change lands = state start + stagger + transition` and check it falls *inside*
the window of the read-out or copy that announces it. A change that lands after
its label has faded reads as "the dots aren't there" — and one that lands after
a hide window starts is never rendered at all. A five-line script that prints
`state | lands | window | INSIDE/FAIL` catches this in seconds; watching the
loop does not, because the eye forgives what it expects to see.

**Scale the transition to the size of the change.** The ceremonial pacing
(1.2s + 0.5s stagger) is for states that rearrange the whole population. A
state that recolours one or two marks must use a fast override (~0.45s,
minimal stagger) or it will never land inside its beat. Give each timeline
state optional per-state `tr`/`st` overrides rather than one global constant.

**Budget the finale first.** The last frame is usually the densest — headline,
legend, source — and it is the one the loop wrap truncates. Work backwards from
the loop end: the final state needs its transition complete with **2s+ of
settled hold**, and its copy needs 3s+ on screen. If the arithmetic doesn't
fit, trim a middle beat, never the finale.

Two things that hold makes precise, both in `references/ending.md`. **Settled
is not frozen** — across the reference set, the last second of a designed
ending carries about as much motion as mid-clip, so the hold keeps its ambient
move and only the stretch where *nothing at all* changes is capped, at 0.8s.
And the final state must start **after** whatever covers the marks has
cleared, not when the beat nominally begins: start it during a panel and the
fastest part of the payoff plays behind the panel.

**A canvas animation loop must be crash-proof.** An uncaught exception inside
a `requestAnimationFrame` callback ends the chain silently and permanently —
CSS animations keep playing, so the piece looks *mostly* alive while the data
layer is dead. This shipped once: an unsized host (an artifact iframe before
layout) made `build()` produce negative radii, the first `ctx.arc()` threw, and
the loop died — "the last two time periods aren't there." Three guards, all
required:

```js
if (r.width < 100 || r.height < 100) { geomOK = false; return; }  // refuse bad geometry
ctx.arc(x, y, Math.max(.1, radius), 0, 6.2832);                    // clamp anyway
try { /* draw */ } catch (e) { geomOK = false; }                   // loop survives
requestAnimationFrame(frame);                                      // ALWAYS reached
```

And observe the **element**, not the window: iframe hosts resize the stage
without firing `window.resize` — use a `ResizeObserver` on the stage.

**A safety floor must never override the no-overlap guarantee.** Flooring the
drawing band at a fraction of frame height (`max(space, H*0.18)`) forces the
marks into the legend whenever wrapped copy leaves less real space than the
floor. Floor only against degeneracy (`max(space, 24)`) and let the marks
shrink — small dots are acceptable; overlap never is.

**Test by driving the frame clock, not by watching.** Expose a debug hook
(`window.__dbg = {drive: t => frame(t*1000), reset, grid, canvas}`) and a test
can step the loop deterministically, then *count the rendered marks by reading
pixels* at each state. Pixel-counting caught a dead render that three rounds of
timeline arithmetic missed. Keep the hook in production builds — it is inert
and makes every future regression testable.

**Close every timed element before its beat ends.** An element whose keyframes
hold `opacity: 1` to `100%` will persist into every later beat — and land on a
field it was never coloured for, where it either vanishes or clashes. Scope each
read-out inside its own beat window and give it an explicit fade-out before the
boundary. Check the last beat specifically: it is where stragglers accumulate.

### Two traps in a persistent-mark system

**1. Index order silently implies meaning.** If dots are sorted by group for one
question and you then slice "the first 63" for a different question, that block
is composed of whole earlier groups — the animation asserts a relationship
between two questions that does not exist. Assign colour from an explicit
per-state mapping, never from a positional slice that happens to look right.

**2. Different surveys have different bases.** Carrying the same marks across
questions is only honest when the unit is a *percentage point*, not a person.
With one dot = one per cent, a move from an n=1,002 question to an n=1,041
question is legitimate — but label the change on screen ("Different question ·
n=1,041") so continuity of marks is not read as continuity of sample.
- **Hold each state 3–5s.** The move is not the point; the arrangement is.
- Canvas, not DOM. Several hundred animated nodes will judder as elements.

**A five-state argument**, which is the shape most polling data wants:

| State | What it shows |
|---|---|
| Cloud | The whole sample, unsorted — establishes the population |
| Sorted grid | The full breakdown, coloured by group |
| Isolate | One group holds; the rest recede to low alpha |
| Re-form | The same units become a different chart (trend columns) |
| Block | Converge on the headline figure |

Reduced motion: hold the most informative single state — usually the sorted
grid — and skip the transitions entirely.

### Charts must move

A chart that pops into existence fully formed wastes the one moment the reader
is actually looking at it. Give both chart types an entrance and one ambient
beat — within the one-accent-one-ambient ceiling:

| | Accent move (once, on entry) | Ambient move (looping, subtle) |
|---|---|---|
| **Bars, vertical** | Grow from the baseline, staggered ~58ms, then value chips lift in above each bar, then the annotation draws on | A soft blurred glow behind the accent bar breathing 0→32% over 2.4s |
| **Bars, horizontal** | Grow from the left edge, staggered ~58ms, labels already in place above each bar, values arriving after the bar lands | As above |
| **Units** | Dots cascade in reading order ~9ms apart while the total counts up beside them | One ring expanding and fading out of the highlighted unit every ~2.6s |

Rules that keep this honest:

- **Ambient motion never touches the data.** Pulse a glow, a ring or an outline —
  never the bar's height, the dot's size or anything encoding a value. A mark
  that changes size is a mark that is lying.
- `transform-origin: bottom` on vertical bars, `left` on horizontal ones, or
  they grow from the middle.
- ⚠️ **A textured bar must be revealed, not scaled.** `scaleX`/`scaleY`
  stretches everything inside the mark, so a grain, halftone or roughened fill
  starts compressed and relaxes over the entrance — the bar reads as rubber, and
  its texture stops matching the surface it sits on. The measured reference does
  exactly this (`../motion-system/references/sources.md` §16: anchor point to
  the left edge, Scale X 0→100%, over bars carrying Roughen Edges and a dot
  fill). Reveal instead, so the texture holds its true density:

  ```css
  /* horizontal bar; the fill never moves, the window opens over it */
  .bar { clip-path: inset(0 100% 0 0); animation: draw var(--beat) var(--ease-out) both; }
  @keyframes draw { to { clip-path: inset(0 0 0 0); } }
  ```

  Animating `width` works too and is cheaper to reason about; it just costs
  layout. Reserve `scaleX` for flat fills.
- Let the sequence **replay when the chart re-enters the viewport**. A one-shot
  entrance is dead the second time someone scrolls past.
- Value chips arrive *after* their bar lands (delay ≈ stagger + ~620ms), not
  alongside it.
- Everything must still read correctly frozen — check the still frame.

⚠️ **Pictogram bars conflict with the house ban** on icons as data marks. The
carve-out, if you want one, is narrow: the glyph must *be* the counted unit
(ISOTYPE), not an icon decorating a mark it has no relationship to. Default to
the ban.

**Gridlines.** ⚠️ Solid hairlines only — **a dash *pattern* is banned** — one
shade off the ground, or none at all. Draw them *through* the marks so grid and
data share one plane. Separate adjacent fills with a 2px ground-coloured gap,
never a border.

The ban is on the *convention*: `stroke-dasharray` is a chart signal that means
something (projected, excluded, below threshold), and spending it on decoration
throws the signal away. **A solid hairline eroded by the surface is not a dashed
line, and is encouraged** — it is the same ink failing on the same paper as
everything else in the frame. Erode it with the composition's own grain mask,
never with a dash array. The recipe is *Broken grid* in the **analog-surface**
skill.

**Label selectively.** The endpoint, the extreme, the one series that matters.
Label directly on the mark; no legends. On a time axis, label only the two
endpoints. Every additional tick is noise.

**Hand-drawn annotation.** The strongest single device, and general newsroom
craft rather than anyone's trade dress. Circle the important part with a
deliberately irregular path in the accent, with a short callout above.

⚠️ **Position it from the measured mark, never from hardcoded offsets.** An
annotation nudged into place with `right: 2%; top: 5%` will drift off its target
the moment the data, the container width or the font changes — and a circle that
isn't actually on the peak is worse than no circle, because it points at nothing.

Measure the mark, then place the annotation on it:

```js
const cr = chart.getBoundingClientRect();
const br = hotBar.getBoundingClientRect();
const cx = br.left - cr.left + br.width / 2;   // centre of the mark
const cy = br.top  - cr.top;                   // the peak itself
// centre the ellipse a little below the tip so it encircles the peak
annot.style.left = (cx - size / 2) + 'px';
annot.style.top  = (cy + size * 0.18 - size / 2) + 'px';
```

Re-run on resize. Reserve real headroom above the plot (`padding-top`) and cap
the value axis above the tallest bar, so the annotation and its callout have
somewhere to live. Give the callout **at least ~28px of air** below the copy
above it — a callout crowding the sub-line reads as a collision, not a label.

```html
<path d="M 74 26 C 30 30 14 74 44 104 C 78 136 138 118 140 76 C 142 40 116 22 74 26"
      fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>
```

Animate with `stroke-dasharray`/`stroke-dashoffset` so it draws on, as if
annotated live. Keep the wobble — a clean `<ellipse>` defeats the point.

**Don't hand-author the wobble — and pick the method by stroke size.**
A tutorial breakdown (`../motion-system/references/sources.md` §12) shows the
reference look is a clean ellipse with *Turbulent Displace* over it (Amount 80,
Size 2, Complexity 1). But the two web equivalents behave very differently:

- **Large shapes (ellipses, braces, arrows over a chart): SVG filter.**
  `feTurbulence` + `feDisplacementMap` at `scale` 4–8. At this size the pixel
  displacement reads as pen wobble.
- **Small strokes (underlines, ticks, anything under ~20px tall): jitter the
  geometry, never filter it.** Displacement maps push *pixels* after
  rasterisation, so a thin stroke aliases and reads as pixelated — and if the
  SVG is drawn in a fixed viewBox stretched to fit (`preserveAspectRatio:
  none`), the displaced pixels stretch too and it gets worse. This failed in
  practice exactly this way.

The geometry method — build the wobble into the path points at final pixel
size, then let the browser draw one crisp vector stroke:

```js
const n = Math.max(14, Math.round(width / 9));      // a point every ~9px
for (let i = 0; i <= n; i++) {
  const x = 2 + (width - 4) * i / n;
  const base = h * .55 + Math.sin(i / n * Math.PI * 2.1) * 2.2;  // gentle arches
  pts.push([x, base + (seededRandom() - .5) * 2.6]);             // jitter
}
// join with quadratic curves through midpoints; stroke-dasharray from
// getTotalLength() for the ink-on
```

Seed the randomness so the line is stable across rebuilds. Regenerate at the
element's real rendered width on resize — never stretch a fixed drawing.

**Best of all: use real scanned marks when they exist.** A scribble-overlay
pack of actual pen strokes beats both synthetic methods; tint to the accent
and clip to size.

**Boiling.** Stepping the turbulence `seed` (or swapping between 2–3 jitter
seeds) a few times a second makes the line shimmer like hand-drawn animation.
Sparingly — it counts as your one ambient move.

**Do not spell a recognisable shape with the marks unless you have a real
vector asset for it.** A coastline, a building, a logo — approximated from a
hand-authored polygon and sampled into ~100 dots — reads as a blob, and stroking
the same bad polygon behind the dots just draws attention to it. This failed
twice in practice before being cut.

The decision rule: **real traced outline available → dots fill it, outline
stroked behind. No asset → don't attempt the shape.** Open with an even scatter
instead — golden-angle phyllotaxis distributes N points uniformly with no
clumping and no shape to get wrong:

```js
const golden = 2.399963;
const rad = spread * Math.sqrt((i + .5) / N);
const ang = i * golden;
pos = { x: cx + Math.cos(ang) * rad, y: cy + Math.sin(ang) * rad * .94 };
```

A scatter settling into a sorted grid is a strong opening on its own — the
population assembling into evidence — and it never embarrasses you.

**Small multiples.** Identical geometry, only the data changing. Identical
framing is what lets the eye compare; panels that shift around become a
slideshow.

## Editorial devices

**Emphasis mark.** A block of colour behind the key phrase — covering only the
words that matter, never the whole line. Wipe it on left-to-right over ~380ms,
then let the text sit. Use the brand's own emphasis colour; a yellow highlighter
specifically is Vox's signature, not a generic device.

**Before/after toggle.** Three separate references make their case by showing
the same composition with one variable removed — texture off ("a sterile Google
Doc"), depth off ("an iMovie slideshow"), movement off ("lifeless"). Identical
framing, one thing changed, held just long enough to register. It is the most
persuasive device in the set for a finding of the form *X made the difference*,
and it costs nothing but a second state.

It doubles as a self-check: strip your own signature move and see whether the
frame still says anything. If the before and after look much the same, the move
was decoration.

**Section breaks.** A full-frame card carrying one large numeral and a short
label, on a contrasting ground. Gives a long piece structure. Build it from the
brand's own marks — not a coloured roundel.

**Segmented progress bar.** A thin bar divided into one segment per section,
filling as the piece advances. Cheap, and it tells the reader how much is left.

**Document framing.** Present data as the object it came from — a form, a
receipt, a filing, a page. Draw it in the artifact's own palette so it belongs
to the frame rather than looking pasted in.

**Cutout with offset echo.** A subject cut from its background with a flat
accent-coloured copy of its silhouette offset behind it. Depth without shadows.

**Large figure over image.** A big number with a small caps label beneath, over a
dimmed photograph. Count it up on entrance — and only ever the hero figure.

---

## What breaks it

- More than one accent element in a frame.
- Flat surfaces with no texture.
- Evenly-weighted typography.
- Rounded cards with soft drop shadows — this uses hard edges and flat fills.
- Decorative gradients. Colour is either a flat field or it encodes data.
- Legends.
- More than one idea per frame.
- **A capitalised overline above a heading.** Never.
- Title Case or ALL CAPS headings — sentence case.
- **Scenes that destroy their marks and redraw new ones.** Marks persist — and
  so should everything else the two states have in common.
- A number typed on before the quantity that proves it has been drawn.
- **Marks that don't encode their values** — a bar whose length was chosen by
  eye, a series with no constant px-per-unit, an axis the geometry ignores.
- **A headline still typing itself while the chart underneath is already
  growing.** The frame carries one thought; give it one entrance at a time.
  Headline lands → beat → data draws → values arrive.
- Body text that passes ΔL but fails 4.5:1.
- Caption pills, platform end-cards, watermarks or any of the tutorial chrome
  the references arrive wrapped in.
- Entrance animation standing in for motion graphics — the data must *move*,
  not merely arrive.
- A chart that arrives fully formed and then sits still.
- An annotation positioned by hardcoded offsets rather than measurement.
- Anything in `references/house-rules.md`, which overrides this file.
- Anything under **trade dress** above.

## Before shipping

1. At **200px wide**, is the finding still legible?
2. As a **still screenshot**, does it still work?
3. Could someone **state the finding out loud** after two seconds?
4. **Divide each mark's length by its value. Is it the same number every time?**
   If the marks were computed from the data this is free; if it isn't the same
   number, the chart is decoration with numbers on it.
5. **Contrast ratio on every text role ≥4.5:1**, checked against the field it
   actually sits on — not against the page ground it sits near.
4. Could someone **name the publication it was copied from**? If yes, pull back.

Any "no" on 1–3, or "yes" on 4, is a fix rather than a ship.
