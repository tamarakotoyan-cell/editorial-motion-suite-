# Source analysis

Frame-by-frame observations from reference material. Each entry records what was
actually seen on screen, not a general impression. Use this when you need to know
*why* a rule in SKILL.md exists.

---

## 1. Vox × The Pudding — "We tracked what happens after TikTok songs go viral"
`youtube.com/watch?v=S1m-KgEpoow` · 22:37 · long-form horizontal

**Colour.** Each scene commits to a single saturated field colour that fills the
whole frame — Vox cobalt (~`#2B57F5`), Vox yellow (~`#F5D920`). The colour changes
at scene boundaries, never within a scene. Content sits in an inset panel with a
visible margin against that field; it is not full-bleed.

**Texture.** A faint graph-paper / blueprint grid overlays the colour field, plus
a constant fine grain over the entire frame. Nothing is a flat digital surface.

**Charts as objects.** The "125 viral artists" moment is a unit chart — 125 discrete
black dots packed into a blob — not a bar chart. Quantity is shown by *counting
things*, and a yellow label chip with black caps text sits directly on top of the
cluster rather than in a legend.

**Props over UI.** Data arrives dressed as real-world objects: a Spotify-branded
paper cheque made out to "Viral artist / $50,000 / memo: Streaming payout"; a
TikTok profile card with follower counts. The chrome is drawn in the scene's own
palette (the cheque is green-on-yellow), so props never look pasted in.

**Live-action interleave.** Overhead desk shots (hands, a notebook on plywood)
cut between graphic sequences. The graphics are not the whole video — they punctuate.

---

## 2. @craftedbycm — "How does Vox make their cuts look so smooth?"
`youtube.com/shorts/KtEgj5hMEUk` · 0:20 · vertical

**The single most transferable technique in the set: "CUTTING THE CURVE".**

Stated method, verbatim from the short's own captions and on-screen build:

1. Animate an object with a **heavy ease in and out** — not a mild ease, a
   pronounced one, so the velocity graph is a tall narrow spike.
2. **Parent the second object** to the first so it inherits that motion.
3. Make a **hard cut at the peak of the velocity curve** — the exact frame where
   the object is moving fastest.

Because both sides of the cut are moving at maximum speed in the same direction,
the eye reads continuous motion and the cut disappears. The short visualises this
as a spike curve with a dashed vertical line at the apex, and two overlapping
clip bars (CLIP 1 / CLIP 2) staggered beneath it.

**Its own styling** (a secondary lesson): near-black canvas, wide-letter-spaced
thin caps title, one cyan accent square, periwinkle clip bars, red pill-shaped
caption chips punching the spoken keyword.

---

## 3. Vox — "America's shift to the right, in data"
`youtube.com/shorts/SMXJ-qx54x4` · 0:59 · vertical

**Vertical small multiples.** Three identical map panels stacked down the frame,
one per election year. Panel geometry is *identical* across all three — only the
data changes. Each panel carries a large serif year label bottom-left and a single
diverging bar beneath the map showing the split.

**Scroll is the narration.** The whole stack translates upward continuously as the
voiceover advances. The panel entering the centre scales up slightly and brightens;
panels leaving the centre dim and shrink. Movement, not cutting, drives the piece.

**Diverging encoding.** Red/blue with lighter tints for narrower margins — so the
map reads as *degree*, not just category. Near-black background throughout.

---

## 4. @craftedbycm — "How Vox makes sure you don't miss key information"
`youtube.com/shorts/XJTCTovyfGM` · 0:30 · vertical

**The failure mode it names**, verbatim from captions: a flat unmodified frame
"gives you nothing. There's no hierarchy, no focal point."

**The fix.** Pull the key element forward and push everything else back:
- On a newspaper scan, the word **FREE** is scaled up enormously while the
  surrounding columns stay at their original tiny scale ("apply the effect and
  lower the scale"). One element is huge, everything else is small and quiet.
- Highlight boxes and dimming are described as overriding whatever the raw frame
  was doing — "these override".

**Arcs, not lines.** The After Effects build shows an element travelling along a
visible curved bezier path around the Vox logotype. Motion paths are deliberately
curved; nothing slides in a straight line.

**Persistent chip.** A red pill-shaped lower-third chip punches the current spoken
keyword ("THESE OVERRIDE", "BUILT", "VIDEOS,") — one or two words at a time, always
in the same screen position.

---

## 5. @ieytch — "Graphs vox type motion graphics"
`youtube.com/shorts/DIb1ICTdJbQ` · 0:15 · vertical

A fan recreation, useful as a distilled recipe of the chart look:

- Near-black canvas; large **serif** title ("Timeline") with a small `2.0` version
  mark offset to its right.
- Thin white gridlines drawn **through** the bars, not behind them — the bars and
  the grid occupy the same plane.
- Bars are white; **exactly one bar is red**. That is the whole colour system.
- Small serif caption block, muted grey, bottom-left, two short lines.
- **Entrance:** bars grow from the baseline with a stagger; the title arrives
  blurred and settles into focus.

(Its axis labels run 30/40/50 top-to-bottom, which is wrong — copy the styling,
not the data handling.)

---

## 6. @stanzmedia — "How to Edit Like Vox — Newspaper Animation"
`youtube.com/shorts/_HU37rX4G1U` · 0:04 · vertical, side-by-side comparison

A newspaper-clipping treatment, built from five stacked ingredients:

1. **Crumpled paper texture** as the base, with a faint dot grid over it.
2. **Serif headline** in the style of a broadsheet, with a smaller condensed deck
   beneath it.
3. **Black-and-white cutout** of the subject, masked out of its background, with a
   **red offset echo shape** sitting just behind and to one side of the cutout.
4. **Yellow highlighter swipe** dragged across the key phrase in the headline —
   the swipe covers only the words that matter, not the whole line.
5. **Small red date chip** in caps above the headline.

The "MY EDIT vs ORIGINAL" framing shows the graded version has more contrast,
stronger cutout separation and the added highlight — the ingredients are what
separate the two.

---

## 7. Vox — "The number of guns in the US is skyrocketing"
`tiktok.com/@vox/video/7239344090628869422` · 1:00 · vertical

**Pictogram bars.** The lead chart builds its bars from a repeated small blue
handgun glyph stacked vertically — roughly twenty per bar at the tallest. The
subject of the data is also the mark used to draw it. Dashed grey gridlines run
across at four levels; the background is plain white, not the dark treatment
used elsewhere.

**Segmented progress bar.** A thin rounded bar pinned to the top of the frame,
split into three coloured runs (yellow / periwinkle / coral) sized to the
sections of the piece. It acts as a chapter indicator for a 60-second video —
cheap structure, and it tells the viewer how much is left.

**Hand-drawn annotation.** On the "FBI background checks on gun sales" line
chart, a rough red ellipse circles the 2012 plateau, with a stacked callout
above it: the year in red, then two short black caps lines naming the events.
The ellipse is visibly irregular — drawn, not a geometric primitive.

**Chart typography.** Heavy condensed serif title, lighter serif subtitle deck
beneath it, muted grey axis labels with only the endpoints of the time axis
labelled (`1999` … `2022`). The value axis carries four ticks and spells the
unit out under the top one (`4 million`).

---

## 8. @refined.motion — kinetic typography piece
`tiktok.com/@refined.motion/video/7517698842301582614` · 0:22 · vertical

The clearest reference in the set for type as composition.

**Mixed scale within one sentence.** A single phrase is set with individual words
at wildly different sizes — one word enormous and bold, connecting words small
and light — so the line has rhythm and an unmistakable emphasis. Roughly 6×
between the largest and smallest word.

**Imagery threaded through type.** A black-and-white cut-out figure is layered
*between* the words: in front of one letterform, behind another. This
interleaving is what makes the composition read as designed depth rather than
text sitting over an image.

**Blurred colour blobs.** Large green circles at heavy blur sit behind and in
front of the composition on an off-white paper ground, providing depth without
competing for attention.

**Later frames** split the canvas hard into a green upper band and a near-black
lower band, with heavily defocused imagery behind, and set white type
alternating bold italic against small light roman.

---

## 9. @refined.motion — "A little widget animation"
`tiktok.com/@refined.motion/video/7521798862521060630` · 0:17 · vertical

**Objects in a lit room.** Rounded UI widgets — a maps card with a route and
turn-by-turn pills, a vehicle charge widget with a segmented orange fill, a
circular dial — float in a soft grey studio sweep with a clear top-centre light
source. Every card carries layered shadows: a tight contact shadow plus a wide
ambient one.

**Shallow depth of field.** Cards away from the focal plane are genuinely
blurred, not merely faded. Focus is pulled between widgets as the piece runs.

**Camera, not elements.** The composition holds together while the camera dollies
slowly across the stack. Layers at different depths separate as it moves, and
that parallax is what sells the space. The move is continuous and never stops.

---

## 10. @denyszhylintutorials — "Top 5 most common tricks from Vox"
`tiktok.com/@denyszhylintutorials/video/7664320200208174356` · 1:02 · vertical

A tutorial cataloguing the Vox toolkit. Observed across the five segments:

1. **Texture as subject.** Heavily magnified physical texture — a microscope-like
   grey field with drifting particles — used as a backdrop. Surfaces are always
   *material*, never flat digital fills.
2. **Volume to convey complexity.** A dense grid of scanned documents tiled
   across a black frame, captioned "extremely complex". Sheer quantity of objects
   does the rhetorical work.
3. **Big number over footage.** A very large white figure with a small
   letter-spaced caps label directly beneath it, over dimmed video. The footage
   is letterboxed into a band with a blurred extension filling the rest of frame.
4. **Chapter cards.** A full-frame crumpled-paper card carrying one huge black
   serif numeral and a small yellow brand roundel in the corner, held briefly
   between sections.
5. **Extreme punch-in.** The camera pushes hard into serif text on a paper
   texture, cropping most of the words off-frame. Named in the video as what
   "creates the signature" look — scale pushed past what feels comfortable.

---

## 11. @emeraldlit_ — "Paprika parade"
`tiktok.com/@emeraldlit_/video/7587423553067306258` · 0:17 · **4:3 (1440×1080)**

Missed in the first pass. Sits in a completely different register from the rest
of the set, and is the only 3D-rendered reference.

**Not vertical.** 4:3 in a feed of 9:16 — the letterboxing is the point, and it
reads as cinema rather than social.

**Rendered environment as atmosphere.** An empty cinema interior: warm sepia and
cream, a blown-out glowing screen as the only light source, visible volumetric
falloff down the walls, rows of seats receding into soft shallow-focus. Dust and
grain in the air. Nothing is graphic — it is a *place*.

**Hard cut to a hero object on void black.** A single 3D-rendered red pepper,
centred on pure black, studio-lit with tight specular highlights and no ground
shadow, so it floats. The cut between the warm atmospheric interior and the
stark isolated object is the whole structure of the piece.

**Slow continuous push-in.** Comparing frames at 7s and 15s, the camera has
dollied measurably closer on the same interior shot — the screen larger, the
seats nearer. One unbroken slow move, never stopping.

The transferable lesson is the **register shift**: an enveloping atmospheric
space cutting to an isolated object against nothing. Two extremes of depth,
alternating, with no middle ground.

---

## Second pass — imagery treatment

Re-read of the captured frames looking specifically at how *images* are handled,
a dimension under-weighted in the first pass.

**Panel within field (Vox, throughout).** Illustration and data almost never
bleed to the frame edge. They sit in an inset rectangle — often near-black —
placed on the saturated colour field, with faint rule lines running behind.
A screen within the screen. Full-bleed is reserved for statement moments.

**Interview footage is letterboxed and punched in.** Talking-head material sits
in a band with black above and below, cropped tight, subject placed off-centre
rather than dead middle.

**Selective colour on photographs (@craftedbycm).** A hand-coloured map holds one
state in saturated blue while every surrounding state falls to grey hatching —
hierarchy built *into* the image rather than layered on top of it.

**Extract and scale (@craftedbycm).** A single word is lifted out of a newspaper
scan and blown up enormously while the surrounding columns stay at their original
tiny size. The scale disparity between fragment and source is the effect; a plain
zoom would destroy it.

**Z-interleaved cutout (@refined.motion).** A cut-out figure sits in front of one
word and behind another, so type and image share one space instead of stacking.

**Letterbox with blurred self-extension (@denyszhylin).** Footage held in a band,
the rest of the frame filled by an enlarged, heavily blurred copy of the same
image.

**Cutout with offset echo (@stanzmedia).** A high-contrast black-and-white cutout
with a flat red copy of its silhouette offset behind it — depth with no shadows.


---

## 12. Local reference set — nine Vox-style tutorial clips
`~/Desktop/AI/Animation Ref/Vox style/` · 9 clips, 29–65s, 576×1024

Creator breakdowns (@creonmotion, @chrismoran__) showing the After Effects
project behind the look. The most technically specific material in the set,
because it shows parameter values rather than results.

**The easing, measured.** One clip pauses on the velocity graph and captions it
"copy this easing". Velocity climbs to a ~250%/sec peak inside roughly the first
15% of the duration, then decays exponentially across the remaining 85%. A short
attack and a very long tail — much more extreme than a stock ease-out. Approx.
`cubic-bezier(0.10, 0.90, 0.20, 1)`.

**Cutting the curve, independently confirmed.** A second creator demonstrates
the same technique with the same diagram — a symmetric velocity spike, CLIP 1
and CLIP 2 overlapping, the cut placed on the apex.

**Hand-drawn annotation is displacement, not draughtsmanship.** A clean ellipse
with **Turbulent Displace** over it — Amount 80, Size 2.0, Complexity 1.0 — is
what produces the "circled by hand" look. Directly equivalent to SVG
`feTurbulence` + `feDisplacementMap`.

**Pictogram with a photographic exception.** A result frame shows ~40 flat black
icon figures with a single figure replaced by a *photographic colour cutout*, a
hand-drawn red brace beneath the group, and a highlighter block on one word of
the caption. Mixing register — flat icon against photograph — is what makes the
one highlighted unit read instantly.

**Paper props are rotated in perspective.** A newspaper page sits on a
graph-paper ground, tilted on a 3D plane rather than lying flat, with the
texture layer explicitly set to **5% opacity**. Very low — confirming that these
overlays work at far lower strengths than instinct suggests.


---

## 13. Local reference set, second pass + @ausunions screen capture
`~/Desktop/AI/Animation Ref/` · clips 4, 6, 8, 9 + ScreenRecording (65s)

**Clip 4 — the negative example.** A deliberate "do not do this" frame:
six text elements scattered at similar sizes — "WHERE DO I LOOK / DISTRACTING /
STATISTIC / overwhelming text". Confirms the focal-point rule from the failure
side. Also note the corrective line's mixed register: italic serif "do not"
against bold yellow caps "DO THIS" in one line.

**Clip 6 — collage cluster + ghost texture.** B&W cutouts (courthouse, gavel,
scales) grouped over a flat blue circle on warm grey — captioned "is just a
flat color". Later, background elements are tint-mapped ("Map White To") to sit
just above the dark ground — "so the contrast stays subtle". Texture at 5%.

**Clip 8 — dolly, don't scale.** "Slowly dolly": a 3D camera moved toward a
still photograph (camera Z −1500) instead of scaling the layer.

**Clip 9 — digital evidence as physical prop.** An nytimes.com article
composited onto a physical newspaper sheet — deckled edges, rotation, vignette.
The web page becomes a printed artefact.

**Screen recording — @ausunions reel.** The user's own capture of the reel the
house timing kit was derived from (see house-rules.md). Confirms in motion:
word-stagger blur-in on serif lines, chromatic-fringe caps type, halftone hand
cutouts, dot-pattern blob backing shapes, grid-textured grounds.

**Underline pixelation, diagnosed.** The demo's filter-based underline read as
pixelated because `feDisplacementMap` displaces pixels after rasterisation and
the fixed-viewBox SVG was stretched across the word. Fix recorded in
editorial-explainer: jitter the geometry for small strokes; filters only for
large shapes; scanned marks best of all.

---

## 14. Full re-analysis of the local set — thirteen clips, picture *and* sound
`~/Desktop/AI/Animation Ref/Vox style/` (9 clips, 29–65s) +
`~/Desktop/AI/Animation Ref/Text animation/` (4 clips, 16–98s)

A second pass over every local file, this time frame-accurate and with the audio
analysed rather than ignored. §12 and §13 recorded parts of the Vox-style folder
from stills; the Text animation folder had never been catalogued.

**Method.** Per clip: scene-cut detection (`select='gt(scene,0.2)'`), contact
sheets at 1.5–3fps across the full duration, 12fps bursts over each significant
transition, plus a full-length spectrogram, waveform and `silencedetect` pass,
with transients correlated back to frame timings. This is the first pass where
sound was examined at all, and it is where most of the new material came from.

### ⚠️ Provenance — narrower than it looks

**None of the nine "Vox style" clips is a Vox video.** All are creator
tutorials *about* Vox: six or more by @chrismoran__ (the @craftedbycm of §2, §4
and the type-treatment file), plus @creonmotion and @denyszhylintutorials. The
type-treatment sources file already flags single-author weighting; it is more
concentrated than recorded there. These are one or two practitioners' reading of
Vox, consistent with each other but not independent confirmation of anything.

Two consequences, both acted on:

1. The findings are **reverse-engineering, not house practice** — treat the
   parameter values as well-observed rather than authoritative.
(Partly answered in §15: Flat Pack FX is an independent author confirming the
core analog claims. Three of those four videos are still the same practitioner.)

2. The clips arrive wrapped in **TikTok tutorial chrome** — caption pills,
   platform end-cards, watermarks, talking-head cutaways, logo stings. That is
   a second layer of borrowed identity, and it is now banned alongside Vox trade
   dress in editorial-explainer.

### Sound — the finding this pass exists for

Consistent across effectively every clip:

**Nothing is cut to music.** Twelve of thirteen carry no music bed at all; the
thirteenth has a ~120 BPM bed buried far under the voiceover. Every cut, caption
swap and graphic reveal lands on a **voiceover phrase boundary or a stressed
word**. Section transitions sit *inside* speech pauses — in the @creonmotion
piece the only three silences ≥0.3s across 61s (5.2s, 28.9s, 54.6s) are exactly
its three largest visual pivots.

**1:1 mapping with a loudness hierarchy.** Sound never decorates. Every
transient is a visual event: a soft pop per word, a tick per glyph on typewriter
reveals, paper foley on paper moves. Visual hierarchy equals loudness hierarchy.
And **exactly one whoosh or impact per piece** is spent on the single most
important moment — almost always the end card. In the template reel the endcard
hit is ~10× the amplitude of any text beat.

**Silence is structural.** Every clip ends with 2–3s of dead air after its final
hit. Between beats there is genuinely empty frame and no sound — the template
reel runs a metronomic ~1.0s cycle of reveal → hold → fade → ~250ms of nothing.

**Why it matters for silent artifacts:** the sound grammar *is* the timing
grammar. Cut-on-phrase becomes pace-to-the-copy; one-hit-per-piece is the
one-accent rule arriving from the audio side; the terminal silence is the
settled finale. Recorded in SKILL.md under *Rhythm*.

### The second timing register

The eased curve of §12 is real but it is not the only register. Captions,
keyword chips and slam titles arrive in **1–4 frames with no easing at all**,
hold 0.6–1.2s, and leave. @bradford_marais' entire caption system is hard
pop-on with zero interpolation; the "Fonts" piece stamps one differently-set
word per spoken word for 45 seconds. The rhythm is carried by placement and
dwell, not by curves — which is why the house "under 100ms is a jump-cut" rule
needed the *travelling vs appearing-in-place* distinction now in SKILL.md.

Related, and easy to miss: **two-stage arrival.** Mid-animation glyphs render
pale/blurred/offset and only reach full ink on landing — arrival state encoded
in colour. Seen on every typewriter reveal in the set.

### Object choreography — how scenes actually change

The @creonmotion micro-documentary (65s) contains **one hard cut**, at the end
card. Everything else is objects entering and leaving a persistent paper stage.
Four devices, now in editorial-explainer:

- **Scale hand-off** — the photographed woman shrinks to become the single unit
  in a 750,000-person pictogram; a rolling yellow ball grows into the circle
  holding the next stat. Objects *become* the next idea.
- **Line leads, content follows** — dashed leaders draw first; the labelled
  object arrives at the endpoint. Later, coins physically travel that same path.
- **Build, then label** — pictogram fills, brace draws, *then* the number types
  on with its highlight. Never the reverse.
- **Anchor-object continuity** — @chrismoran__'s "14" circle holds position
  while the entire background swaps; @joshua.esca holds a giant "NO" while the
  word beneath it changes from "fees" to "courses".

### Exits, which the set designs and generated work does not

Annotations **un-draw themselves** (reversed trim path) before a scene change;
per-character reveals exit in the same random order they entered; finished
sentences **dim to ~30% rather than clearing** as the next clause arrives, so
the whole thought stays readable. The "Fonts" piece builds persistent word
clouds this way for 45s.

### New techniques added to the skills

- **Exclusion blend for emphasis** (@bradford_marais, taught explicitly):
  emphasised word set Bold, ~1.5× size, blend mode Exclusion so it self-inverts
  against the footage — guaranteed contrast with no plate. → type-treatment.
- **2.5D parallax from one still**: fg/mg/bg cutouts, clone-stamped patch behind
  each, Z-spacing (the free "Depth" script, 50mm, spacing ~1000), slow dolly,
  foreground slightly defocused. Demonstrated by removal — "this is bad… an
  iMovie slideshow". → imagery-motion.
- **Posterize Time to 12fps across the whole comp** plus a barely-visible
  chromatic fringe over everything, from @chrismoran__'s literal "Vox Sauce"
  preset (Quick Chromatic Aberration 3 → Posterize Time 12.0 → Exposure → Add
  Grain). The stepping is general, not just for boil. → motion-system,
  editorial-explainer.
- **Semantic face pairing**: where two faces share a line, bold sans carries the
  claim and italic serif carries the aside — held to consistently across every
  clip that mixes them. → type-treatment.
- **Before/after toggle as argument**: three clips prove their point by removing
  the technique — texture off is "a sterile Google Doc", parallax off is "an
  iMovie slideshow", boil off is "lifeless". → editorial-explainer.

### Confirmed, with parameters

Nothing already recorded was contradicted. Newly precise:

- **The easing curve** (§12) re-confirmed from the same graph-editor frame, now
  with the creator's own caption "*COPY THIS EASING*" and the surrounding
  recipe: chromatic aberration, long easing, no solid colours, 12fps.
- **Boil** is Roughen Edges (Border ~7–37, Edge Sharpness ~5.7) *plus* Turbulent
  Displace (Amount 15–80, Size 2–52), with a **time-driven expression on the
  random seed** — the stepping is what reads as hand-drawn.
- **Paper at 5% opacity** (§12) confirmed a second time, alongside the full
  paper-realism recipe: Tint mapping black→dark grey and white→dimmed
  ("so the contrast stays subtle"), highlights pulled ~10% with Curves, warm or
  cool tint to match scene lighting, grain last.
- **Hand-drawn annotation** draws on tip-leading over ~0.3–0.4s and then keeps
  boiling for the rest of its life — it is never a static mark after the draw.

---

## 15. Four long-form YouTube tutorials — picture and sound
Downloaded, contact-sheeted at 1 frame / 5s, parameter panels zoomed, captions
pulled, loudness measured. Analysed 12 Aug 2026.

| Video | Author | Len |
|---|---|---|
| "How VOX breaks the Digital Feel with Motion Graphics" `youtube.com/watch?v=sACZlG7z35Q` | Chris Moran | 12:30 |
| "How to Make Text Feel Real Like NETFLIX Docs" `youtube.com/watch?v=eFm43BURGSE` | Chris Moran | 12:46 |
| "The VOX Sound Design System" `youtube.com/watch?v=UgVgzSZVu-8` | Chris Moran | 12:48 |
| "The Psychological Secret of the 'Vox Look'" `youtube.com/watch?v=E7mSfihvjCQ` | Flat Pack FX | 6:06 |

### Provenance — the first cross-author corroboration in the set

§14 records that the entire local reference set is one or two practitioners.
Three of these four are that *same* Chris Moran (@chrismoran__ / @craftedbycm),
now in long form — better evidence, because he shows parameter panels rather
than results, but not independent.

**Flat Pack FX is a genuinely separate voice**, and it independently confirms:
no pure white, roughen edges on ink, multiply blend, posterize time, texture at
low strength. Marked **[×2]** below where both authors agree. This is the first
independent confirmation the set has had; the §14 warning stands otherwise, and
the ban on trade dress is unchanged.

### The organising principle — Surface / Ink / Life

Flat Pack FX states it outright as "three pillars of authority": **surface**
(the ground, never white, never flat), **ink** (the marks, blended *into* the
surface's fibres), **life** (temporal instability — posterize time, described
there as "16mm film flicker" or "texture boil"). The order is the method.

The argument underneath is the transferable part: *"Everything's like that
perfect digital imagery. We associate it with like AI and that corporate look …
by adding those imperfections, that grit and that dust, it basically signals
human curation."* Imperfection as a **trust signal**, not nostalgia. Demonstrated
with an A/B of identical fabricated legislative text on a white digital
rectangle and on an aged printed sheet. Its own summary: *"Stop animating pixels
and start animating artifacts."* → the analog-surface skill.

### Ink sits IN the surface — the gap this pass found

The most important finding. The AE layer stack, read off Flat Pack FX's timeline
at 4:05:

```
1  LOOK          Normal                        grade / CA / vignette
2  Texture       Normal
3  [Text Holder] Multiply  Luma matte from (2)   <- the ink
4  [Paper 1.jpg] Normal                          <- the surface
```

- **Multiply** on the ink so the ground reads through it. **[×2]**
- **A luma matte from a high-contrast duplicate of the paper**, applied to the
  ink, so the paper's own fibres cut into the mark. *"You really want to bring
  those fibres out."* Nothing equivalent existed anywhere in the skills.
- **Letterpress blotch** (Netflix piece): fractal noise, contrast up, brightness
  down, scaled small, multiplied into the glyphs. Ink is never one flat value.
- **Ink bleed**: Gaussian blur 2.5 + **three drop shadows, distance 0**, softness
  ~3 rising, opacity 50% → 30% → 15%. NOTE: these are pixels tuned to one comp
  size — below ~100px type they read as a drop shadow. Use em-relative.
- **Ink flecks**: duplicate the type behind, fill off, black stroke ~13, then
  Turbulent Displace + Roughen Edges with the border raised until the stroke
  breaks into scattered specks.

### Screen emulation — a complete recipe

Venetian Blinds: **transition completion 5%, rotation 90°** (horizontal — *"most
monitors are horizontal"*), **width 8, feather 1**; Solid Composite black;
chromatic aberration **1.2**; Lumetri vignette; and the detail nobody does — an
exposure expression **`wiggle(24, 0.08)`**, a 24 Hz refresh flicker. Duplicate
the blinds at rotation 180 for a pixel grid.

Rationale for moving a camera across it rather than cutting: *"it helps you feel
like you're participating in the journalism and discovering things along with
the narrator."* The pan is the argument.

### Footage homogenisation

Named concept: every archival source through **one shared treatment** so
mismatched material stops reading as mismatched. Fast box blur radius 6 with an
inverted feathered radial mask (centre sharp, *"guides your eye towards the
middle"*), CC Ball Action grid spacing 0, chromatic aberration 2.0,
`wiggle(24, 0.05)`, Add Grain size 1.4. The governing line: *"This matters less
about the effects you use. It's just more consistency across clips."*

### Sound — the production grammar behind §14's timing rules

§14 derived timing from sound. This is the system that produces it.

**Six folders:** mechanical · tech · tactile · ambience · whooshes · misc.

**Hierarchy, stated as a refusal.** The strongest passage in the set is a
decision *not* to sound-design: *"this is where it's going to be beneficial to
exercise a little bit of restraint. Think about hierarchy … I'm actually just
going to ignore the text and the arrows drawing on. I'm just going to sound
design this building in the middle."* One-accent arriving from the audio side —
but as an instruction to leave secondary elements **silent**. Silent
translation: do not animate the supporting elements at all.

**J-cut.** Sound leads picture: *"it helps people's brains prep for the scene by
hearing the sound a little bit before the visuals come."* → a precursor element
(plate, rule, shadow) leads its object by ~100–150ms.

**Deliberate desync.** *"The sound effects don't actually have to be perfectly
lined up with the movement. You can knock them a few frames around because it
fits within that choppy stop motion feel."* Everything landing on one frame is a
tell.

**Variation by rate-stretch**, not by new asset — the same file stretched, which
shifts pitch and duration together. **Stacking:** a movement is whoosh *plus* the
material (paper rustle) — gesture + substance. **Literal, then better than
literal:** a marker sound for lines drawing on was tried and discarded for
stopwatch ticks.

**Mix levels, stated:** dialogue **−6 dB**, music **−20 dB**, SFX **−10 to −20 dB**,
plus a dynamic-EQ "frequency pocket" ducking music in the vocal band. Measured
integrated loudness across the three Chris Moran videos: −20 to −23 LUFS at
LRA ~11 LU, so the dynamic range is real. (Flat Pack FX is −12.6 LUFS, LRA 3.3 —
a loudness-maximised YouTube mix, not a sound-design exemplar.)

### Focus band from a gradient blur map

A linear gradient shape layer (black → white → black) driving Camera Lens Blur
as a **blur map**, producing a horizontal *band* of focus with soft top and
bottom. Better than a radial vignette for placing attention, and it sells macro
depth on a flat composition. The reference also names the cost — *"this effect
will absolutely blow up your computer"* — and works with it disabled until last.

### Values

- **Paper white `#FDFAF3`** — read off the colour picker, H 41° S 6% B 99%. The
  first exact value for "never pure white". **[×2]** *"Every room is going to
  have some sort of light temperature … your paper is always going to absorb
  that temperature."*
- **Roughen Edges border 2–3** on hairlines and grid rules — the fix for
  *"background lines are a little too sharp and clean … they look pretty
  computerized."* **[×2]**
- **Chromatic aberration scales with intended degradation**, and the scaling is
  the rule, not the number: **0.5** delicate type, **~0.8** general comp,
  **1.2** screens, **2.0** archival. *"I always get excited with this effect and
  dialing it too much can look amateur."* (The 0.8 is a caption reading of "8"
  in context of a pull-back from 1.5.)
- **Posterize Time 4 fps** for a deliberately choppy hero move — far below the
  established 12. 8 for "super collagey".
- **Texture 5%** — confirmed a fourth time.
- **Light-leak texture on `add`** over the whole comp to discolour paper unevenly.
- **Blend-mode rule of thumb:** mid-grey textures → overlay family;
  black-background textures → add/screen family.
- **Flash transition:** self-shot phone footage at minimum shutter speed, moved
  chaotically, used to stitch two similar compositions.

### The treatment ladder — synthesised, not stated

Falls out of all four. Treatment strength is keyed to what the object is
pretending to be; one global setting is the common mistake.

| Register | Surface | Ink | Life | CA |
|---|---|---|---|---|
| Document / paper | paper texture, warm, fibre | multiply + paper matte + bleed | boil | 0.5 |
| Native graphics | tinted ground, no pure white | roughen edges 2–3 | posterize 12 | 0.8 |
| Screen / UI | scanlines + vignette | — | 24 Hz flicker + posterize 12 | 1.2 |
| Archival footage | shared homogenisation | — | posterize 12 + grain 1.4 | 2.0 |

---

## 16. Nuclear Motion — "How to Design Infographics in the Vox Style"

`youtube.com/watch?v=1Lru07jxWkQ`, 7:05, published 16 Sep 2025.
Downloaded at 1080p60, contact-sheeted at 1 frame / 4s, transcript pulled,
palette and bar geometry measured in pixels, step cadence measured by frame
differencing. Analysed 14 Aug 2026.

An After Effects screen recording — roughly 85% software UI. The design content
is a three-frame showcase reel at 0:00–0:16 and the finished build looping at
6:44–7:05. Same genre as the §12/§14 local set and by a fifth author, so it
counts as **independent corroboration** of the picture findings rather than new
territory.

### Corroborated, by measurement rather than by caption

- **Posterize Time 12fps over the whole composition**, applied as one adjustment
  layer carrying the grain as well. Frame differencing on the final loop shows
  content updating every **4–6 frames of a 60fps capture** — ~12 discrete
  updates/sec. This is the first *measured* confirmation of the 12fps figure;
  §12 and §14 had it from captions and panel readings only.
  → Drives: *The stepped finish*, and the `--step-*` tokens in `motion.css`.
- **Roughen Edges on grid rules** (§15) — and here also on the **data marks
  themselves**, which §15 does not cover.
- **Noise for film grain**, same adjustment layer.
- Fractal Noise → Color Key (kill white) → CC Ball Action → Fill: a dot/halftone
  overlay tinted to the ground.

### New — the broken grid

The grid is a solid grid eroded by Roughen Edges, so the rules fragment
irregularly rather than repeating a dash. Visually it is the single strongest
surface move in the piece.
→ Drives: *Broken grid* in `analog-surface`, and the amendment to the gridline
ban in `editorial-explainer` — the ban is on the dash *convention*, not on a
line the surface has eaten.

### New — loop structure, measured

Loop restarts at t=413.83s and t=419.87s → **6.04s**, sitting on `--loop-tile`.
Animation resolves in **~2.1s**; the remaining **~3.9s is a static hold**.
Roughly **1:2 motion-to-hold**.
→ Drives: *Reveal short, hold long*.

### ⛔ Negative finding — the reference's charts do not encode their data

The most important thing in this source, and the reason it must not be treated
as a craft model for charts.

Showcase frame at 0:03, bar lengths measured against stated values:

| Label | Value | Bar | px per % |
|---|---|---|---|
| Unemployment | 43% | 762px | 17.7 |
| Banks that failed | 85% | **283px** | 3.3 |
| Growth of government spending | 72% | 864px | 12.0 |

The **85% bar is the shortest on the chart**, at a third the length of the 43%
bar — and the frame carries a `0%…100%` axis with gridlines asserting a scale
the marks ignore. The finished build at 7:03 is better but still not linear:
520px/62%, 598px/65%, 464px/42% — 8.4, 9.2 and 11.0 px per percent.

The bars were drawn by eye and the numbers typed on afterwards. Neither chart is
wrong in a way a reader could catch.
→ Drives: *The mark must equal the number*, and check 4 in *Before shipping*.

### Negative finding — colour

| Role | Hex | L\* | vs card |
|---|---|---|---|
| Ground (peach) | `#F5DECC` | 89.9 | — |
| Card (paper) | `#F5E5D5` | 91.8 | — |
| Bar (blue) | `#91B9D6` | 73.3 | **ΔL 18.5**, 1.69:1 |
| Deck / source | `#9C9286` | 61.1 | ΔL 30.7, **2.48:1** |
| Highlight | `#F2F649` | 94.0 | — |
| Ink | `#000000` | 0.0 | 17.05:1 |

Two distinct failures, and the pack caught only one of them:

- The **bars fail the existing ΔL ≥25 rule** (18.5). The rule works; the chart
  evaporates at the 200px test exactly as predicted.
- The **source line passes ΔL comfortably (30.7) and is still unreadable at
  2.48:1.** ΔL measures separability, not legibility, and nothing in the pack
  was asking the second question.
  → Drives: the contrast-ratio floor table in *Neutrals must be separable*.

### Negative finding — sequencing

At 6:54 and 7:00 the headline is still typewriting while the bars are already
growing. Two entrances competing for the same two seconds in a frame that
carries one thought.
→ Drives: the new *What breaks it* entry.

### Trade dress — no change needed

Sampled `#F2F649` lemon highlighter behind an italicised word, with blue bars
and a high-contrast display serif. Exactly the combination `editorial-explainer`
already lists as *"recognisably Vox, do not reproduce"*. The existing ban is
correctly calibrated.

### What this source is worth

Take the surface and timing findings; they are measured and they corroborate
four other authors. **Do not take its charts.** The set as a whole is
practitioners demonstrating a *look*, and this entry is the clearest evidence
that look-fidelity and data integrity come apart — the piece is convincingly
Vox-like and its central graphic is false.
