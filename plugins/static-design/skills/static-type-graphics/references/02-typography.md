<!-- Vendored copy. Master: Static design content/static-design-system/principles/02-typography.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 02 — Typography

Static work is read at two sizes: thumbnail, and full frame after someone has decided to
stop. Type has to survive both. Everything below follows from that.

---

## Two families, three registers

**Two type families maximum.** One carries the voice, one carries the utility. A third
family is always a decision that was never made — see
`bad example: throwback-stat-cards.png`, which runs a display serif, a serif italic, a
letterspaced monospace and a sans in one frame.

**Three registers maximum per frame:**

| Register | Job | Typical share of frames |
|---|---|---|
| Display | The finding, the headline, the hero figure | Every frame |
| Support | Deck, quote body, answer lines | Most frames |
| Utility | Attribution, source, axis labels, chips | Most frames |

**Count registers, not sizes.** Two sizes within about 20% of each other are one register
set slightly differently, not two — and a hero figure belongs to display alongside the
headline it outranks, because the figure *is* the display, run large. A frame carrying a
202px figure, a 58px headline, a 21px line and a 17px source has four sizes and three
registers, and it is correct. Counting distinct pixel values instead fires the ceiling on
compositions this system elsewhere prescribes.

A fourth register is nearly always a utility line that wanted to be different from the
other utility line. Make them the same.

## The register split, by house

All three reference publications solve the same problem differently, and all three are
valid. Pick one per client and hold it.

- **Serif display + sans utility** (NYT). The serif carries authority; the sans carries
  everything mechanical. Best when the subject is serious and the illustration is light.
- **Single family, weight-differentiated** (Guardian). One family across display and
  support, separated by weight and size alone. The most robust choice when the client's
  brand has one good face and no second.
- **Heavy sans display + serif support** (Vox). The inversion: the sans shouts, the serif
  speaks. Best when the piece is conversational and the illustration is doing the work.

**Never a serif or display face on a hero figure.** A large standalone number is set in the
sans, at whichever weight the brand's display weight is. This holds even when the brand's
display face is a serif.

Nor `tabular-nums` on a hero figure — equal-width digits read loose at display size.

## Size

**On a type-led frame, headline cap-height runs 8–12% of canvas height.** On a 1080×1350
tile that is a 155–230px font size for most faces. A type-led frame is one where the words
are the picture: a cover, a pull quote, a statement tile.

**On a picture-led frame, the floor drops to about 4%.** Where a photograph, illustration,
chart or mark field covers a quarter of the canvas or more, the picture is the picture and
a 12%-cap headline fights it. Guardian's chart headlines measure around 3.5% of canvas
height and are right to.

Applying one band to both is wrong in the direction that matters: it would reject the
reference set's own data frames.

**No text below 1.25% of canvas height.** On the same tile that is a floor of about 17px.
The source line, the attribution and the axis labels all sit above it. This floor is what
makes a frame survive the feed.

It was 1.6% — 22px — and that was too high, not marginally. Every reference caption sits
between 12 and 17px, so the old floor put the house above the entire set it was derived
from, and it did real damage: with utility pinned at 22px and support at 26px the two
registers collapsed into one, and frames came out with a display size and a single
undifferentiated small size beneath it. 17px restores the third register.

The consequence is deliberate: **there is not room for much copy.** A frame holds a
headline, a supporting sentence and an attribution. If it needs more, it is two frames.

### The hero figure outranks the headline

**On a frame whose job is a number, the hero figure runs 1.2–2× the display size.** Not
equal to it, and never below it.

This is the difference people see and cannot name. A 28% set at three-quarters of the
headline reads as a sentence with a chart underneath; the same figure above the headline
reads as data with a sentence introducing it. The reference set is emphatic about this —
Sharratt's pull-quote percentage runs about 4× the body around it.

The floor is 1.2× rather than 1.5× because the reference tiles run about 1.1× and read
stronger than the house's own 1.57× attempts. Point size is not what makes a figure
dominate — the air around it and the texture behind it are, and a floor set high enough to
force the issue was buying scale by spending the space that would have done the job
better. Above 1.2× it is a composition decision, not a rule.

Where the figure is too wide for its block, **set the unit at about half the digit size**
(`28` at 112px, `%` at 58px) rather than shrinking the whole figure. It is a standard
editorial move and it buys roughly 20% of the width back.

### The question and the deck are one slot, not two

A chart frame wants to carry a headline, then a deck, then the question the respondents
were actually asked. That is one text layer too many for a tile, and it is what produces a
dead band between the copy and the chart.

**On 4:5, 1:1 and 9:16, the question line *is* the supporting line.** Write it so it does
both jobs — "If a new data centre were proposed in their local area:" — and drop the deck.
It reads as a set-up for the chart rather than a second sentence competing with the
headline, and it buys back around 200px.

The copy budget for a tile, in full:

| Slot | Allowance |
|---|---|
| Headline | ≤ 2 lines |
| Supporting line | 1 — the question, on a data frame |
| Annotation / callout | 1 short clause |
| Footer | Source and base. Plus one definition note where a category was combined |

16:9 may take a genuine deck as well, because a slide is read at arm's length rather than
at thumbnail size.

## Scale

Every size on one ratio, declared once at the top of the document.

| Ratio | Name | Use |
|---|---|---|
| 1.333 | Perfect Fourth | **The default for static.** Three distinct registers, dramatic jumps |
| 1.618 | Golden Ratio | Type-only frames, pull quotes, single-statement posters |
| 1.25 | Major Third | Chart frames, where axis labels and annotation must coexist quietly |

Major Second (1.125) is a dashboard scale and is almost never right for a feed.

Sizes like `16 / 19 / 27 / 31 / 42` are the signature of a frame nobody structured.

## Case and alignment

**Sentence case for headlines.** Not title case.

All-caps display is permitted where the brand's own voice is caps (Vox does this) — but
then it is caps for *every* headline in the set, never one frame in five.

**Left-aligned by default.** Centred type belongs to the cover frame and the ceremonial
single statement, and then applies to the whole frame, not one line inside it.

Leading at display size runs 0.95–1.05. Anything looser makes a two-line headline read as
two separate lines. Tracking sits slightly tight at display size — `-0.02em` is a good
starting point for a grotesque — and never letter-spaced.

## The overline rule

⛔ **No capitalised letterspaced kicker sitting above a single frame's headline.** It
duplicates what the headline already says and pushes the real heading down the canvas. It
is present in four of the ten rejected examples.

```html
<!-- no -->
<p class="kicker">SUSTAINABILITY IS STRUCTURAL</p>
<h1>We don't make new clothes</h1>

<!-- yes -->
<h1>We don't make new clothes</h1>
<p class="sub">Every piece sold is a piece that was never manufactured.</p>
```

### The one exception: the serial running head

A short caps line **repeated identically across the slides of one carousel** is a chapter
marker, not a kicker, and it is permitted. NYT's "TO BUILD MORE HOUSING…" runs across four
consecutive slides and tells you which section you are in.

The distinction is mechanical, and the linter applies it that way:

- Appears on **one** frame → banned kicker.
- Appears **verbatim on three or more consecutive frames** in a set, and does not restate
  the headline beneath it → permitted running head.

Uppercase letterspaced type remains fine for axis labels, chips and attributions
regardless.

## Punctuation

- No typed full stop at the end of a headline.
- Quotation marks are the quotation mark. A decorative oversized quote glyph above a quote
  that already has them is decoration doing meaning's job.
- Em dashes and ellipses in headlines are fine; they are how a running head continues into
  a slide.

## Texture on type is opt-in

Two different things get called texture, and conflating them is how a frame ends up with
grain on everything and material meaning nowhere.

- **Ground texture is required and composition-wide.** One layer, over the field, under the
  marks. See `03-colour-and-ground`.
- **A print process on type is opt-in and per-string.** It is a feature applied to a
  selected display element, never a property of the type system.

**Regular typeface styling is the default.** Resolve face, size, weight, tracking, leading,
colour and hierarchy first. Only then, if a physical or reproduction cue is editorially
useful, name a process and apply it to one string.

The rules that matter here, and they are not negotiable:

- **Never through a global selector.** Not on `body`, not on a root wrapper, not on a shared
  heading component. Type renders normally unless a class says otherwise.
- **One dominant process per string.** Halftone *or* dry stamp *or* ink bleed — never
  stacked. A shared grain pass may still run over the finished composition.
- **Keep body copy, source lines, chart labels, axis labels and hero figures clean.** They
  are what the treated string is contrasted against. Treat everything and you have treated
  nothing.
- **If no deliberate material cue is needed, stop at regular type styling.** Reaching for a
  process because the type looks flat is the failure the boundary exists to prevent — the
  answer to flat type is usually size, weight and space.

The taxonomy itself — clean print, halftone, dry stamp, ink bleed, photocopy,
misregistration, pattern fill, paper collage — plus the tactile contact stack, the class
contracts and the per-process size limits, live in **type-treatment** (`print-processes.md`
and `type.css`) and are not restated here. One home per rule area.

## Type as the image

When there is nothing to show, the words are the picture. Set them at display size and let
them fill the frame — `good example: nyt-yellow-pullquote.png` gives a 60-word quote two
thirds of the canvas and looks deliberate.

The failure mode is the same passage set at half that size with the remainder left empty:
`bad example: aiherway-dark-quote.jpg`. Type-only frames have the *highest* occupancy
requirement, not the lowest.

## Self-check

- Two families or fewer, three *registers* or fewer — clustering sizes within 20%?
- Is every size on the declared ratio?
- Is the headline's cap-height 8–12% of canvas height?
- Is the smallest text at least 1.25% of canvas height?
- Is the hero figure set in the sans, and is it 1.2–2× the display size?
- Is there a deck *and* a question line, where the question could have done both?
- Is there a caps overline above a single frame's headline?
- Sentence case, left-aligned, unless the whole set says otherwise?
- Is display leading at or below 1.05?
