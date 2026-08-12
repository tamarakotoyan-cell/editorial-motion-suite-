# Source analysis — type treatment

Observations from reference material, recorded as what was actually seen and
heard on screen. Use this when you need to know *why* a rule in SKILL.md exists.

**Method and its limits.** Each short was played in the browser pane with frames
captured as screenshots and the auto-caption track read off the DOM during
playback. YouTube's timed-text endpoint is token-gated and returned empty, and
frame-accurate seeking stalls on the Shorts player, so narration was sampled
across several playback passes rather than transcribed continuously. **The
captions below are partial** — gaps between quoted lines are real. Quoted text
is verbatim from the auto-captions or from words burned into the frame;
everything else is description of what was visible. Where a reading is inferred
rather than seen, it says so.

---

## 1. @craftedbycm — "Texturing your animations is your secret sauce"
`youtube.com/shorts/sKqA13yzfcQ` · 40.9s · 9:16 · 83k likes

The most directly useful of the four. A title-card build in After Effects.

**The thesis, verbatim:** *"Texturing is the secret sauce of animation. Most
people just slap [a texture on] and use opacity. And what I found is it makes
your textures feel [dull]."*

On-screen at that moment: the word **OPACITY** set in a heavy condensed sans,
charcoal, on a green textured field, with **DULL &** below it in a marker-style
hand face and **FEEL LESS** in a yellow pill sticker. The lettering of "OPACITY"
itself has visibly eroded, dry-brush edges — the frame demonstrates the
technique it is describing.

**The layer stack, read directly off the AE timeline.** Blend modes visible in
the Mode column, top to bottom: `Overlay`, `Overlay`, `Pin Light`, `Pin Light`,
then `Normal` rows below. One row shows a Track Matte set to **`11. TEXTURE`**.
So: texture plates composited with Overlay and Pin Light, plus a texture used as
a matte on the type layer. Opacity is not the mechanism anywhere in the stack.

**Choosing the texture.** *"…for my meal. For this title card, I'm going to
choose this faded newspaper…"* — the surrounding metaphor (sampled mid-sentence)
is choosing a texture the way you'd choose a wine for a meal. The point stands
without the metaphor: the texture is chosen to suit the piece, not applied
generically.

**Displacement.** *"…make it feel even more tactile, let's add a
displacement…"* and, at the end, *"…make it take on the form of our texture. And
there you have it."* The Effects menu is visible with `Displacement Map` and its
`Use For Horizontal` / `Use For Vertical` channel selectors, applied against a
layer named `TEXTURE 3`. A yellow sticker reads **A DISPLACEMENT**.

**The finished card.** A charcoal letterform (a giant `T`) on a saturated orange
field, the letter carrying a black dry-brush/newsprint texture inside it. The
type is not sitting on the orange — the orange field, the type and the grain all
share one surface.

→ Drives: *Blend, never fade*; *Follow the form*; the mode choices in
`Register: In`.

---

## 2. @craftedbycm — "Why Your Text Looks Fake on Textures (and How to Fix It)"
`youtube.com/shorts/pZhxPbM63Ko` · 35.4s · 9:16 · 13k likes

**The thesis, burned into the opening frame:** *"Blending text in a texture is
all about the details."* Rendered as `is all about the` in a black serif with
**`details`** below it in a red serif italic, over a coarse light-grey
concrete/paper wall. Behind that copy, an enormous charcoal letterform fills the
frame — and its edges are visibly absorbing the wall's aggregate.

**What "the details" means, shown rather than said.** Two thin red circles are
drawn onto the frame, each ringing a specific point on the giant letterform:
the inner notch of a stroke junction, and a stroke terminal. Both are places
where the letterform's edge meets the surface grain. The circles are the whole
argument — the technique lives at the edge, not in the fill.

**Colour selection.** A long hold on a colour picker panel (`Select Color`, with
an eyedropper). Hand-lettered white text across the gradient field reads
**"AVOID THESE SECTIONS"**, with two curved arrows drawn from that label toward
the extremes of the field — one sweeping up toward the near-white corner, one
down toward the black/fully-dark edge.

⚠️ *Inferred:* the arrows point at the pure-white and pure-black extremes, so
the rule is read as "don't take your ink from the extremes — sample from the
surface's own range." A later frame shows a hex value beginning `#0…` against
white, but it was not legible enough to record. The rule in SKILL.md is stated
at the level the frames support (stay off #000/#FFF, carry the surface's hue);
the specific hex is not claimed.

**Structure.** A `HOW TO` card with three numbered steps, each marked with an
`fx` badge — i.e. three effects applied in sequence. Cutaway stickers punctuate
the talking head: **THIS BREAKS** (blue pill), **THIS MA…** (blue pill),
**DISPLACEMENT MAP** (a black `fx` chip). A late frame shows heavy black grain
laid over the letterform.

So the three-step spine is consistent with §1: matte/mask the type with the
texture → displacement map → grain over the whole frame.

→ Drives: *Break the edge*; *Match the light*; the "never pure black, never pure
white" rule.

---

## 3. @craftedbycm — "Vox text animations always feel so sophisticated"
`youtube.com/shorts/OOry5FgjXEU` · 30.8s · 9:16 · 12k likes

**Tool:** *"…sophisticated and you can make them in seconds. We're going to use
the text animator tool in After Effects."* Text animators are per-character
property animation driven by a range selector with an offset ramp — the direct
CSS analogue is a per-character stagger, which is why SKILL.md specifies a much
tighter interval than the sibling stagger.

**Fill animation.** A card reading **FILL ANIMATION** in heavy charcoal caps on a
pale graph-paper ground, Vox's yellow logo sticker beneath it. Narration:
*"…for their brand color and then fades the charcoal for legibility."* The
sequence is: the type fills with the brand colour, then resolves to charcoal so
it can actually be read. Two stages, and the second is the one that makes it
work.

**Number roll.** A frame holding **`$600,000`** in heavy charcoal on a pale
vertical-textured ground, with the trailing digits caught mid-roll — visibly
smeared through a vertical odometer transition while the leading digits have
already landed. A red sticker reads **STYLE MOVES.**

**The warning, and it is the strongest statement in the set.** *"…almost like a
slot machine. Also, don't have multiple text animations going on at one time.
That way, your viewer…"* The frame illustrating it is a dark textured field
carrying six text elements animating simultaneously, all motion-blurred:
**WHERE DO I LOOK** (top right), **DISTRACTING** (left), *do not* **DO THIS**
(centre, mixed italic serif in white + heavy yellow caps), **STATISTIC**, and
*overwhelming text* in italic serif at the bottom. A red sticker reads
**YOUR VIEWER**.

Note the "do not DO THIS" line is itself a demonstration of mixed-scale,
mixed-style emphasis within a single phrase — two faces, two weights, two
colours, one thought.

→ Drives: *One text animation on screen at a time*; *Per-character reveal*;
*Fill sweep*; *Digit roll*; *Mixed scale within one thought*.

---

## 4. @NickAndersonCreative — "HOW TO make wiggly, handwritten text"
`youtube.com/shorts/3G-LxxgwPa4` · 40.9s · 9:16 · 177k likes

A practical build for hand-lettered captions, done entirely in the edit — no
motion-graphics tool.

**The method, from the captions:** *"…simple steps number one grab some blue
construction paper…"* → write the word by hand, filmed against blue → *"…Final
Cut Pro or the editor of your choice…"* → *"…and stack them on top of each other
crop out each of the words and Center…"* → *"…and apply it to each clip it
should automatically remove the blue…"* (a keyer; the Transform/**Tracker**
panel is visible) → *"…and copy and paste a bunch of times until you like the
length."*

**What the frames show.** A viewer holding the word `Wiggle` written **three
times** in white marker on blue paper, stacked vertically as three separate
clips on three timeline tracks (all `DSC00871`). A later frame shows the blue
keyed out on two of the three, the third still blue — mid-process. The final
frame is a single white hand-lettered `Wiggle` on black.

**The mechanism, and why it matters.** The wiggle is *three genuinely separate
drawings* cycled, not one drawing being distorted. Each take differs in stroke
weight, letter spacing and baseline because a hand cannot repeat itself. That is
the source of the irregularity, and it is why a smooth procedural wobble reads
as fake — a real boil is stepped between discrete drawings and never
interpolates.

⚠️ *Inferred:* the exact frame rate of the cycle is not stated and the timeline
zoom was not readable enough to count frames. SKILL.md specifies 8–12fps as the
working range from standard hand-drawn boil practice, not from a measurement in
this video.

→ Drives: *Hand-drawn boil*, including the ordering of variant sources and the
insistence on `steps()` over easing.

---

## Cross-cutting

Three of the four are by the same author (@craftedbycm / TikTok @chrismoran__),
who also appears in the motion-system reference set — so their weight in this
file is one point of view repeated, not three independent confirmations. §4 is a different author working in a different tool,
and is the only genuinely independent source here.

All four treat **texture as the default state of a surface**, never as an
optional overlay, which is consistent with the "surfaces are always material; a
flat digital fill is the tell" finding already recorded in imagery-motion.

Not covered by any of these sources, and therefore taken from house rules rather
than the videos: the size threshold for `feDisplacementMap`, the ban on
capitalised overlines, the 200px legibility check, and the works-as-a-still
requirement.
