<!-- Vendored copy. Master: Static design content/static-design-system/principles/03-colour-and-ground.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 03 — Colour and ground

Colour comes from the client. This file governs how many colours do what, never which ones.

---

## Roles, not a palette

Fill these slots from the client's brand system. Do not invent a palette.

| Role | Job | Count |
|---|---|---|
| `ground` | The field everything sits on | 1 per frame |
| `ink` | Headlines, primary marks | 1 |
| `muted` | Attribution, source, axis labels | 1 |
| `accent` | The one thing that proves the point | **exactly 1** |
| `secondary` | The opposing side, diverging data only | 0–1 |

**Minimum viable brand: one typeface in the right register and one colour that connects.
Everything else neutral.** Past that, extra brand assets stop adding recognition and start
making the work look like a guidelines document.

The test: someone who knows the client recognises the work as theirs; someone who does not
sees a clear, well-made graphic. If a brand element is present and you cannot say what job
it does in *this* frame, remove it.

## The ground is never white

Every one of the seventeen good examples sits on a tinted field. NYT cream `#F5F0E6` and
cool bone `#F2F4F7`; Guardian pale pink `#FDECEC` tinted to the story; Vox sage, purple,
rust.

Pure `#FFFFFF` and pure `#000000` are both banned as page fields. White reads as an
unstyled document; pure black crushes every photograph placed on it.

Three ground strategies:

- **Neutral tint** — a warm or cool off-white, or a near-black at `#1A1A1A` or above.
  Carries illustration and photography without competing.
- **Story tint** — a desaturated wash pulled from the subject (Guardian's pink for a
  supermarket price story). Chosen once per post, then frozen.
- **Saturated field** — a full brand colour with content inset against it, margins visible
  on all sides. See below: this is a working mode, not a special case.

**One ground per frame; one ground per set unless the register changes.** A field colour
that changes between slides for variety destroys the family. A field colour that changes
once, at the boundary where a pull quote interrupts a narrative, is a beat marker — see
`good example: nyt-yellow-pullquote.png`.

### Flat field or worked surface — decide which, and commit

Two ground modes, and a frame is one or the other. Mixing them is what produces a texture
that reads as dirt rather than as paper.

| | **Flat field** | **Worked surface** |
|---|---|---|
| What it is | One saturated colour, edge to edge, no texture at all | Four layers — field, tooth, structure, bleed-through |
| Does the branding | Yes, by itself. The colour *is* the identity | No. The stock is neutral; the ink carries the identity |
| Suits | Type-led covers, statement frames, illustration | Collage, cutouts, monochrome sheets, anything torn |
| Reference | Vox yellow, orange and pale cream — five of the nine covers | The Atlantic kraft covers; the Dracula poster |

The flat field was previously described here as "statement frames only, and never
full-bleed data". Too narrow, and the reference set says so: five of nine covers run a
flat saturated field carrying a headline *and* a full-bleed illustration, and they are the
most immediately recognisable frames in the set. A flat field is a legitimate default for
a type-led cover.

What does hold: **a flat field carries no texture.** Grain over a flat saturated ground is
the one combination that always looks like a mistake — neither the clean poster nor the
printed sheet, and it lowers the contrast of everything on top of it. If the frame wants
tooth, it is a worked surface and the field goes neutral.

## One accent, one element class

**The accent rule is the whole system.** One bar in the accent among neutral bars. One
word highlighted. One saturated line among grey lines.

The moment a second element class takes the accent, the frame loses its focal point.

> `bad example: socceroos-canopy.jpg` applies yellow to the rule, the pill fill, the
> second headline line, four bullet dots, the address, the footer dot and the mark. Seven
> element classes. The accent has become a second brand colour and points at nothing.

If two things genuinely matter equally, they are two frames.

Where the brand offers several accents, pick **one per post** and hold it across every
slide. Rotating accents between slides destroys the set.

## Emphasis devices

Exactly one per frame, chosen from:

- **Highlight block behind one word.** A hard-edged fill behind a single word of the
  headline. One word — not a phrase, not a line. Guardian's "August".
- **A colour change on one phrase.** The clause that carries the finding takes the accent;
  everything around it stays ink.
- **A single accent mark.** One coloured object in an otherwise line-only illustration.

Not three colours inside one sentence. `bad example: aiherway-dark-quote.jpg` changes
colour mid-clause with no semantic reason, so the reader looks for a meaning that is not
there.

## Contrast floors — run both

They answer different questions and a palette can pass one while failing the other.

| | Measure | Floor |
|---|---|---|
| Mark vs mark, mark vs field | **ΔL** | ≥ 25 |
| Text below 24px bold / 30px regular | **contrast ratio** | ≥ 4.5:1 |
| Text at or above 24px bold / 30px regular | **contrast ratio** | ≥ 3:1 (WCAG large text) |

The large-text allowance is WCAG's own, not a loosening. It is what makes an accent-coloured
display line legal where the same colour would be illegal on a source line.

ΔL separates marks. It does not make text readable. A muted grey source line on a cream
field can sit at ΔL 30 — comfortably separable — and 2.5:1, which cannot be read.

**This failure is invisible on a large bright display, which is where it gets signed off.**
`bad example: throwback-stat-cards.png` ships an entire footer row at roughly 1.5:1.

Check the marks against the **field** first — a mid-grey mark on a light warm field passes
against the other marks and disappears against the ground.

## Categorical colour

- **Opaque fills, not alpha ramps of one colour.** Reserve alpha for de-emphasis, never for
  category. Two greys that are one colour at 34% and 72% both read as *greyish*.
- **Two categorical neutrals is the ceiling.** A third needs hue, and a second hue breaks
  the accent rule.
- **On a light ground, use fill versus stroke rather than two fills.** A neutral light
  enough to sit ΔL 25 from a warm-grey ground lands within about ΔL 11 of a warm accent, so
  the two categories separate from the field and not from each other. Drawing the remainder
  as an outlined ring and the subject as a solid fill carries the distinction that luminance
  alone cannot — and it keeps the denominator visible, which is the point of the field.

### Three fills plus an accent does not close — and that is arithmetic, not judgement

State this plainly, because the ΔL 25 rule reads as achievable and is not. **No set of
three fills can sit 25 L\* from each other, from the accent, and from the field, on any
ground.**

Work it through on a near-black tile. Field `#17171A` is L\* 7; the Essential accent
`#E2491A` is L\* 53; bone `#EDE9E2` is L\* 92. A third fill must be ≥25 from all three, so
it must be ≥32, and either ≤28 or ≥78, and ≤67. Both branches are empty. Repeat it on the
warm-grey light ground and the same window closes.

The rule is still right — two categorical neutrals plus one accent is genuinely the
ceiling. But a three-category chart is ordinary work, so name the resolutions rather than
leaving people to fudge a hex and say nothing:

1. **A hairline on the offending fill**, in the colour it fails against. This is the
   sanctioned answer and it costs nothing.
2. **Fill versus stroke**, as above, where one category is a remainder.
3. **Adjacency and self-labelling.** ΔL exists so a reader can match a distant mark to a
   swatch. Where the marks touch and each carries its own name, that burden is gone and a
   sub-floor pair is safe. This is a reason to relax the rule, never to skip checking it.

**Whichever you use, write the measured L\* values into a comment beside the tokens, and
say which pair is under the floor and why it is safe.** An undocumented near-miss is
indistinguishable from an accident at the next edit.
- **Never assign colour by rank or position.** A colour per panel, a colour per section, a
  colour per step — all of them repaint when the content reorders, which proves the colour
  was carrying nothing. `bad example: infographic-six-panel.jpg` does this six times.
- **Fix the meaning and hold it across the set.** A colour that changes meaning between
  slides destroys the continuity the set exists to build.

Semantic colour (good / warning / critical) is separate from the accent and does not count
against it.

## Gradients

Banned, with one exception: **a type plate at a frame edge** — a bottom-anchored gradient
sized to the copy block, used when type must sit over a photograph and the photograph has
no dark region. `good example: guardian-portrait-collage.png` is the correct form.

Not a full-frame dim over a photograph. Not a decorative background wash. Not a fill on a
button, a bar or any data mark. A gradient that spans the whole canvas is decoration
standing in for a decision.

## Texture

**This section governs the ground.** Texture on *type* is a separate, opt-in, per-string
decision — see `02-typography`, and the **type-treatment** skill for the taxonomy. Ground
texture is composition-wide and required; a print process on a string is neither. Do not let
one stand in for the other: grain sprayed over everything is not a material cue, it is a
filter.

Flat digital surfaces are the tell. Every reference frame carries at least one texture
layer.

```css
.grain::after{
  content:"";position:absolute;inset:0;pointer-events:none;z-index:99;
  opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

Grain at **4–6%**. At 10% it stops reading as texture and starts reading as a broken image.

Paper scans go **under the marks and copy, above the colour field** — multiply on light
grounds, soft-light on dark, opacity 18–30%. A paper scan over the content darkens every
letterform a crease crosses, unpredictably, on exactly the type you need read.

One texture layer, not three. Check at 200px wide: grain turns to mud at thumbnail size.

## Self-check

- Is the ground tinted rather than white or pure black?
- Is the accent on exactly one element class?
- Is there exactly one emphasis device?
- Does every text/field pair clear 4.5:1? Did you check the smallest text, not the biggest?
- Does every mark clear ΔL 25 against every other mark *and* against the field?
- Is any colour assigned by rank or position?
- Is there a gradient that is not a type plate?
- Does the frame hold at least one texture layer, and only one?
