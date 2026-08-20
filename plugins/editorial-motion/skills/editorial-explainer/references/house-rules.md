# House rules — authoritative

> **This file is the only copy.** It lives at
> `plugins/editorial-motion/skills/editorial-explainer/references/house-rules.md`.
> `build-skills.py` vendors it into every skill that cites it, and the design
> system projects receive it by sync. Do not edit a vendored or synced copy —
> the two copies that existed before this note had already drifted in both
> directions, each carrying rules the other lacked, which is exactly the
> failure the timing-kit section below describes and was written to prevent.

Condensed from the user's own reference notes in their vault:
`Reference/Claude Design tells - banned attributes.md` and
`Reference/Prompting Claude Design for motion.md`.

**These override every style skill.** Where the Vox/TikTok reference material and
this file disagree, this file wins. The reference material is inspiration; this
is the house standard, arrived at from real campaign work.

Read the vault notes for the full reasoning — this is a working summary.

---

## The framing that matters most

> Most "AI slop" in a data graphic is a **point-of-view problem**, not a styling
> problem. The chart weights everything equally because nothing decided what the
> finding was.

Fix the finding first and roughly half the visual tells disappear on their own.
This is why **editorial-explainer** opens with "one frame, one fact" — the
governing idea is upstream of every styling rule.

## Ban list

Entries marked 🔒 are enforced by `check-artifact.py` at **error** severity —
the linter fails the artifact, so they do not depend on being recalled from
this document under load. Entries marked 🔓 are checked but only warn: real
findings, overridable with a reason. Everything unmarked lives here and nowhere
else, and depends on being read. Migrating more of them is the standing
direction of travel: a rule that fails a build beats a rule in a paragraph.

**The marks are generated, not remembered.** Run

```
python3 check-artifact.py --rules
```

for the current table, and reconcile this file against it. Three marks in this
document were wrong before that command existed — a 🔒 on a rule the linter
never implemented, and two on rules that only warn. A false 🔒 is worse than no
mark, because it tells you to stop holding the rule in mind. CI now fails if
the two disagree.

**Structural** — wrong decision made before styling started:

- A colour per category when the story is one number
- Dual y-axes
- A value printed on every data point
- Donut or pie with more than 6 segments
- Title is the metric name rather than the finding
- A one-bar bar chart or two-slice pie, where a stat tile was the answer
- Colour assigned by rank, so filtering repaints the survivors
- Nested marks sized with `%`, so sub-segments resolve against their group
  rather than the plot — plausible, invisible, and wrong by roughly 3×
- A value–label list under a chart, standing in for direct labelling
- A hero figure at or below the display size on a frame whose job is a number
- A deck **and** a separate question line on a feed-scale canvas
- Content covering less than 60% of the canvas

**Typographic** — punctuation and small type doing damage out of proportion to
their size:

- **Mid-dot metadata chains** — `Source · Date · Sample`. The mid-dot ranks
  nothing, so three facts of different importance get one weight and one line.
  It is also the mechanism behind the sloppy footer: once metadata is a chain it
  reads as one lump, gets set small and grey to fit, and lands in the crop. One
  mid-dot is a separator; two in a string is a chain. Use line breaks, commas or
  plain labelled lines.
  *Enforced by the static system's `check-static.py`; still prose-only here —
  migrating it is the next linter job.*
- Text below **1.25% of canvas height**, ~17px on a 1080×1350 tile. The floor
  outranks the type scale that produced it — see **layout-composition**.

**Decorative** — styling doing work that meaning should do:

- Gradient fills on bars or marks
- Drop shadows or glows on data
- Heavy or dashed gridlines
- Boxed-in chart cards with no breathing room
- 3D or perspective
- **Serif or display face on the hero figure**
  *Enforced by the static system's `check-static.py`; still prose-only here.*
- **Decorative background gradients that mean nothing.** The common case is a
  full-bleed radial vignette over a flat field. See analog-surface §1: a
  vignette is opt-in, its strength is per register (`--vig-*`), and alpha does
  not carry across fields — a value calibrated on paper reads as nothing on a
  dark ground, which is the signal to drop it, not to raise it.
- Icons or emoji used as data marks
- 🔒 **`tabular-nums` on a large standalone number** — equal-width digits read loose
- 🔒 **Letter-spaced uppercase, and small-caps, on labels.** Data labels, legend
  keys, axis labels, chip text, table column heads, eyebrows and stat-tile
  captions are **sentence case**. Small tracked caps read as product chrome
  rather than as a newsroom graphic, and they are the label register several AI
  assistants use for their own interface — on client work that mis-attributes
  the piece to the tool that made it, which is the opposite of what a house
  style is for. Separate a label from body copy with size, weight and the muted
  neutral; that is what the neutral is for.

  The check is scoped to *positive tracking*, because that is the register at
  fault. Caps set large with negative tracking is a poster or stamp treatment
  that **type-treatment** owns. Headings remain sentence case under their own
  rule, so this is not a licence to set one in caps.
- 🔒 **A pure white or pure black ground.** Not a styling preference: a flat
  `#fff` is the absence of a surface. The default ground is the brand's tinted
  paper; white is an *inset* surface — cards, input fields, table bodies

**Motion** — the animated version of the same problem:

- Every element easing in at once
- Bounce on everything
- Count-up animation on stats that aren't the point
- Motion that only makes sense while playing, so the screenshot fails
- 🔒 **No `prefers-reduced-motion` block.** Motion without an opt-out is an
  accessibility failure, not a style choice — see `accessibility.md`
- 🔓 Travel under 100ms, which reads as a jump cut rather than a move
- 🔓 Easing off the house curve set

🔒 Banned titles: "Key Insights", "Data Overview", "By the Numbers".

🔒 **Every artifact carries the version stamp** that made it. Not a design rule
— an attribution rule, and the reason any change to these skills can be shown
to have helped or hurt.

## What to do instead

- **Form first.** Pick the chart type from the data's job — magnitude, identity,
  polarity, change over time, or a single headline. If the finding is one number,
  it's a stat tile, not a chart.
- **State the finding in one sentence** before designing. If you can't, it isn't
  ready.
- **Emphasis over variety.** One accent on the mark that proves the finding;
  every other mark neutral grey.
- **Thin marks, hairline solid gridlines** one shade off the background, or none.
  Separate fills with a 2px background-coloured gap, not a border.
- **Label selectively** — the endpoint, the extreme, the one series that matters.
- 🔒 **Source and sample size**, small and muted, bottom-aligned. Non-negotiable
  for research work, and an **error** when the linter is run as
  `--profile research` or `--profile editorial`. It is only a warning by
  default because the checker cannot tell a survey finding from a product
  mockup from the HTML alone — so pass the profile; that is what it is for.
  Set it as labelled lines, never a mid-dot chain:

  ```
  Essential Report, March 2026
  Base: all participants (n=1,002)
  ```

## The three-question check

1. At 200px wide, is the finding still legible?
2. As a still screenshot, does it still work?
3. Could someone state the finding out loud after two seconds?

Any "no" is a fix, not a ship.

---

## House timing kit

Shared vocabulary so a set of tiles reads as one family. **Use the token names,
not generic duration bands** — `--snap`, `--beat`, `--settle`, `--hold`,
`--drift`, `--stagger`, and the `--loop-*` lengths.

**The values live in the motion-system skill's `motion.css` and only there.**
This file used to carry a second copy of the table; the copies had already
drifted apart on spring overshoot, which is the argument against keeping them.
Paste `motion.css` in and use the names.

What is a house decision rather than a number:

- Reveals → `--ease-out`. Fast in, gentle landing.
- Ambient → `--ease-in-out`, so the loop point is invisible.
- Stickers → `--ease-spring`, a slight overshoot past final size, then settle.
- Never linear, except gradient drift.
- 🔓 Stagger stays in the house band, 60–90ms. `check-artifact.py` warns when
  `--stagger` sits outside it rather than failing — a client brand with its own
  motion spec is a legitimate reason to leave the band, and there is no way to
  tell that case from carelessness in the CSS. Leaving it needs a reason.

## The ceiling

**One ambient move + one accent move per tile.** That is the maximum. This is
stricter than general motion advice and it is the rule that keeps a set from
turning into noise.

- Same easing and same stagger across every tile, even when the moves differ.
  The consistency is what makes it read as a system.
- Movement never crosses the tile's optical centre unless it's the hero element.
- Check every tile at 200px wide — grain, chromatic split and halftone shimmer
  all turn to mud at thumbnail size.
- **If a tile works as a still, motion is a bonus. If it only works moving, it
  fails the moment someone screenshots it.**

## The signature accent move

**Word-stagger blur-in.** Words appear one at a time, 0.2s apart. Each: opacity
0→100%, blur 8px→0, over 0.4s, ease-out. Hold 1.5s, then the whole line blurs and
fades out together over 0.3s.

The blur is doing the work — a plain fade reads as generic.

Other accent moves available: line-stack build, sticker pop, chromatic pulse
(dark backgrounds only), cutout rise, annotation draw-on. Ambient moves:
gradient drift, slow push-in with return, grain flicker, halftone shimmer.
See the vault note for full specs.
