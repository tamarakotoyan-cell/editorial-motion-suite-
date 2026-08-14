# House rules — authoritative

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

Entries marked 🔒 are enforced by `check-artifact.py` — the linter fails the
artifact, so they do not depend on being recalled from this document under load.
The rest still do. Migrating more of them is the standing direction of travel:
a rule that fails a build beats a rule in a paragraph.

**Structural** — wrong decision made before styling started:

- A colour per category when the story is one number
- Dual y-axes
- A value printed on every data point
- Donut or pie with more than 6 segments
- Title is the metric name rather than the finding
- A one-bar bar chart or two-slice pie, where a stat tile was the answer
- Colour assigned by rank, so filtering repaints the survivors

**Decorative** — styling doing work that meaning should do:

- Gradient fills on bars or marks
- Drop shadows or glows on data
- Heavy or dashed gridlines
- Boxed-in chart cards with no breathing room
- 3D or perspective
- **Serif or display face on the hero figure**
- Decorative background gradients that mean nothing
- 🔒 **Mid-dot-separated footnotes or metadata chains**, such as `Source · Date · Sample`. Use line breaks, commas or plain labelled lines instead.
- Icons or emoji used as data marks
- 🔒 **`tabular-nums` on a large standalone number** — equal-width digits read loose

**Motion** — the animated version of the same problem:

- Every element easing in at once
- Bounce on everything
- Count-up animation on stats that aren't the point
- Motion that only makes sense while playing, so the screenshot fails

🔒 Banned titles: "Key Insights", "Data Overview", "By the Numbers".

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
  for research work.

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
- 🔒 Stagger stays in the house band — `check-artifact.py` fails an artifact
  whose `--stagger` sits outside it.

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
