---
name: format-adaptation
description: Re-composing one approved motion piece across 16:9, 4:5, 1:1 and 9:16 — the delivery stage, after the master is designed and signed off. Use whenever a piece needs to ship to more than one aspect ratio, whenever someone asks for "the vertical version", "the square cut", "social crops" or "all formats", and whenever a 16:9 master is about to be scaled or centre-cropped into a feed. Covers what stays invariant (tokens, hierarchy, choreography) versus what re-derives per format (layout, element budget, travel axes, focal placement), the space-for-time trade in vertical, platform safe areas, the nested-crop rule for feed previews, per-format type re-derivation, and the first-frame poster rule. Pair with layout-composition for the master's grid and motion-system for its timing; this skill never overrides either.
---

# Format adaptation

A 16:9 master scaled into 9:16 is unwatchable: type at half size, a focal
point buried under platform chrome, side-by-side relationships crushed into a
column. The broadcast habit of **one master, scaled and cropped** is the
single most common way a good piece dies on the way to a feed.

The fix is a different mental model: **what was approved is not a layout — it
is a system.** Colour, type ratios, easing, timing tokens, the beat structure,
the one-accent rule, the voice. That system is the invariant. Each aspect
ratio then gets its own composition *derived from* the system, the way a
print identity produces a poster and a business card without either being a
scaled copy of the other.

**Boundary with layout-composition:** that skill chooses and composes the
*first* canvas — the master. This one derives the siblings. Never redesign
the system mid-adaptation; if adaptation reveals the system is wrong, fix the
master and re-derive.

## Invariant vs re-derived

| Never changes | Re-derives per format |
|---|---|
| Colour tokens, texture treatment | Layout and grid |
| Type *ratios* (the modular scale) | Type *sizes* (re-anchored to format width) |
| Easing curves, timing tokens | Travel distances and axes |
| Beat structure — what happens, in what order | What happens *simultaneously* vs *sequentially* |
| The one accent, and which moment owns it | Where the focal point sits in frame |
| Copy and hierarchy | Element count on screen at once |

If two formats disagree about any left-column item, one of them is wrong.

## The four stages

Each format is a different room, not a different-sized screen.

| | Native px | Where it lives | What it is for |
|---|---|---|---|
| **16:9** | 1920×1080 | YouTube, web, decks | The full argument in *space* — hero, support, annotation, source can coexist |
| **4:5** | 1080×1350 | Feed portrait (IG, LinkedIn) | Hero plus one supporting element. Autoplays muted. The workhorse |
| **1:1** | 1080×1080 | Feed square | The hero alone, with a kicker. Nothing else fits honestly |
| **9:16** | 1080×1920 | Reels, TikTok, Stories, Shorts | The full argument in *time* — one beat per screen-height, stacked |

The 9:16 row is the one that breaks the "smaller = less" instinct. Vertical is
not a small format; it is a narrow format with the viewer's *entire attention*.
It gets the whole argument back — sequentially. **Width is traded for time.**
A 16:9 scene where chart and annotation sit side by side becomes a 9:16
sequence where the chart lands, *then* the annotation arrives on the next
beat. Same beats, same order, same accent; simultaneity becomes sequence.

## Element budget

The discipline that makes small formats work is subtraction, not shrinking:

- **16:9** — full cast on stage at once.
- **4:5** — hero + one support + source line. The annotation layer goes.
- **1:1** — hero + kicker. If the chart cannot survive as a single mark or a
  two-bar comparison, it does not appear; the number carries the frame.
- **9:16** — full cast, one or two at a time. Element budget is per *beat*,
  not per piece: never more than one new idea per screen-height.

Cutting an element is not losing it — feed formats are the hook whose job is
to earn the click through to the format that holds the full argument.

## Safe areas — the chrome eats the frame

Feed and vertical formats are viewed through platform UI. Current conservative
union across TikTok / Reels / Stories (2026 — chrome drifts, re-verify
quarterly against platform specs, and compose as if the bands were solid):

| Format | Top | Bottom | Right | Left |
|---|---|---|---|---|
| 9:16 | 12% | 25% | 13% | 6% |
| 4:5 / 1:1 | 4% | 4% | 4% | 4% |
| 16:9 | — | 8% (scrub bar) | — | — |

The 9:16 numbers are severe: the bottom quarter belongs to captions and the
action rail. Nothing that matters — no text, no data mark, no accent — sits in
the bands. Ambient texture may bleed through them.

**The nested-crop rule.** Feeds preview 9:16 video as its centre 4:5 crop.
So inside every 9:16 composition, the middle 4:5 must read alone — hero and
headline inside it, the stack composed so the crop is a poster, not a wound.
The formats nest: 1:1 lives inside 4:5 lives inside 9:16. Design the vertical
stack with that Russian doll in mind and the feed preview comes free.

## Type re-derives, never scales

Carrying px sizes across formats is the scaling error in miniature. Re-anchor
instead: same modular scale (from layout-composition), base re-derived from
the format's own width so that **characters per line stays roughly constant**
— a headline holds ~8–14 characters per line in every format, body text
45–70ch where body text exists at all. A headline that filled a 16:9 half-
column refills a 9:16 full-width the same way — visually identical *weight*,
different px.

## Motion re-choreography

- **Micro-travel is invariant.** Entrance settles (the 18px rise, blur-ins)
  are perceptual, not compositional — same px everywhere.
- **Macro-travel re-derives.** Anything crossing the stage is a fraction of
  the axis it crosses, not a px value. In CSS: container-query units
  (`cqw`/`cqh`) on a stage with `container-type: size` — see
  `assets/formats.css`.
- **Stagger follows the reading axis.** Left→right in 16:9; top→bottom in
  vertical formats. Arcs flip the same way.
- **Scroll-as-narration is the 9:16 device** (motion-system covers the
  mechanics); its 16:9 equivalent is the lateral dolly. Same continuous-
  movement principle, rotated 90°.
- **Loops:** feed formats (1:1, 4:5) loop at 3–6s, muted, so the keyword-chip
  register replaces anything the voiceover was doing. 9:16 runs the full
  15–60s narrative. Beats stay paced to the copy in every format.

## Every first frame is a poster

Feeds autoplay muted and show frame 1 until they do. Motion-system's "must
work as a still" rule applies **per format, to frame 1 specifically**: hero
legible, composition resolved, nothing mid-entrance. Verify by rendering
frame 0 of each format, not by squinting at the master.

## Implementation contract

One source file, four explicit compositions:

- Stage carries `data-format="16x9|4x5|1x1|9x16"`; tokens live once in
  `:root`; each format gets its own labelled layout block.
- **Explicit blocks, not fluid breakpoints.** Responsive design reflows;
  adaptation recomposes. A media query that smoothly interpolates between
  formats is the scaled-master mistake wearing modern syntax — every one of
  the four compositions is a deliberate, reviewable decision.
- Element triage via visibility utilities (`.fmt-only-*`, `.fmt-not-*`), so
  the DOM stays identical and only the composition differs — one copy edit
  fixes all four formats.
- Safe areas as per-format custom properties, with a debug overlay
  (`data-debug="safe"`) that paints them — turn it on before sign-off.
- Production renders: one format per run through the motion-system skill's
  `render.py` — presets `wide`, `portrait`, `square`, `vertical` match the
  four stages. The frozen-render check runs by default; do not pass
  `--no-check` to silence it.

## Order of work

1. Master approved first — usually 16:9 or 9:16, whichever the brief leads
   with. Never start adaptation on an unapproved system.
2. Adapt to the furthest format from the master next (16:9 ↔ 9:16), because
   it surfaces every weak assumption; the middle formats then fall out.
3. Render all four, frame-0 stills first, then motion.
4. Safe-area overlay on, one pass per format.

## Self-check before delivering

- Could any format be mistaken for a crop or scale of another? (It should
  visibly be its own composition.)
- Same beats, same order, same single accent in all four?
- Does the middle 4:5 of the 9:16 stand alone as a poster?
- Is anything load-bearing inside a chrome band?
- Characters per line roughly constant across formats?
- Does frame 1 of every format work as a still?
- Was anything *shrunk* to fit that should have been *cut*?

## Assets

- `assets/formats.css` — stage scaffolding, per-format safe-area tokens,
  visibility utilities, container-query travel units, debug overlay.
- `assets/example.html` — one composition re-composed across all four
  stages, safe-area overlay demonstrated on the 9:16.
