# Essential Report — right direction vs wrong direction, July

An Instagram tile. Portrait 1080×1350, still PNG, built from the data rather
than drawn by eye.

```
python3 build.py            # writes tile.html and tile.png
python3 build.py --no-png   # HTML only
```

Everything that changes month to month is the `DATA` dict at the top of
`build.py`. Nothing else needs touching.

## ⚠️ The figures in `DATA` are placeholders

`"placeholder": True` puts an orange warning bar across the top of the tile and
makes the build print a warning. Replace the July and June percentages, the
fieldwork dates and the base, then set `"placeholder": False` and re-run.

## What the tile does

One frame, one fact — and the hierarchy is the whole design.

The first version set three percentages and three change figures at the same
size. That is eight numbers of equal rank, which is the same as no takeaway:
a reader scrolling past has nothing to carry away. The tile now leads with a
single hero figure, states one movement line beneath it, and demotes everything
else to a small key under the marks. Nothing but the hero is sized to be read
first.

The copy runs as four rungs in descending weight, and each does a different
job:

| Rung | Job | Example |
|---|---|---|
| hero figure | the number | `52%` |
| `hero_label` | what it counts, in the poll's own terms | say the country is heading in the wrong direction |
| `takeaway` | **what it means, in plain terms** | More Australians are feeling negative than positive about the country's future |
| `change_line` | how it moved | superseded by the arrow — see below |

The third rung is the one that stops the tile being a number with no reading.
A percentage and a question wording is a poll result; the sentence a reader
actually repeats is the one that says what the result means. It is a gloss on
the question rather than a second measurement, so it is derived only as far as
which side leads — override `takeaway` whenever the month needs a different
reading, and check it still says what you mean before publishing.

`DATA["hero"]` picks which number the figure is:

| Value | Hero figure |
|---|---|
| `"level"` | the accent group's own share this month (default) |
| `"gap"` | how far the leading group sits clear of the other |
| `"change"` | the accent group's movement on June |

## The arrow

The trend is drawn as a heavy arrow, because a shape registers before any
word does. It is not a stock icon dropped on top — the house list bans icons
used as data marks, and a generic downward arrow asserts a slide the figures
may not support. Every elbow here is a real monthly reading: x is evenly
spaced by month, y is a linear scale over the series, so pixels-per-point is
constant across the whole line. Geometric rather than rounded — miter joins,
butt caps, one flat fill, no gradient or shadow.

Two rules keep it honest:

- **The last two points must equal `june` and `july`.** The build stops if they
  don't, so the arrow can never contradict the key beneath it.
- **Fewer than four readings and it is a straight segment**, which reads as a
  change rather than a trend. Supply real months.

**The arrow's shape is the data's, not the design's.** `DATA["trend"]` currently
holds a placeholder series that happens to decline. If the real readings don't,
the arrow won't, and the tile's premise has to be rethought rather than the
arrow bent to fit.

## The arrow and the accent are the same colour, so they must mean the same thing

A tile gets one accent. The arrow therefore tracks whichever group
`DATA["accent"]` names, and the hero figure reports that group too — otherwise
orange would mean one thing in the figure and another in the line, which is the
fastest way to make a chart lie.

That makes it a single switch with two coherent settings:

| `accent` | Hero | Arrow |
|---|---|---|
| `"right"` | the share saying right direction | **falls** — positive sentiment draining away |
| `"wrong"` | the share saying wrong direction | **climbs** — negativity building |

Same story, different picture. Pick the one that matches the month.

## The dot band

Beneath the arrow, a hundred dots — one dot per percentage point — so the
proportion is countable against a denominator that is on screen. Right
direction and wrong direction are filled; unsure is drawn as open rings. It is
25 × 4 rather than 20 × 5 because the arrow now takes the height the band used
to have: the band is the supporting evidence, the arrow is the impression.

Three further decisions worth knowing about before editing:

**The marks are computed from the data.** `allocate()` turns the published
percentages into exactly 100 dots by largest remainder, and the build fails if
they don't sum to roughly 100. There is no path by which the dots and the
printed numbers can disagree.

**The accent goes on one group only.** `DATA["accent"]` picks it. That is the
editorial decision — the accent belongs on the mark that proves the finding and
on nothing else, so changing it is a change of story, not of styling.

**The third category is separated by form, not just colour.** Essential's orange
sits at L\* 53, between the dark ink (33) and any mid grey light enough to read
against the warm ground (62). No single-accent palette on a light field can hold
all three categories 25 L\* apart, so unsure is drawn as an open ring. Measured
in greyscale the four values come out at 79 / 114 / 167 / 231 — distinct by
luminance as well as by shape.

The copy rungs derive from the numbers if left as `None`. The reading is
editorial judgement, so write your own when the month has a better story than
the arithmetic can see.

The movement sentence is gone from the layout — the arrow states the change
before anyone reads a word, and repeating it in prose was the copy the tile
could most afford to lose.

## Checks this passes

- `check-artifact.py --strict` — clean
- Text contrast on the warm ground: ink 6.73:1, muted 4.85:1. The muted grey is
  one step darker than the `--text-secondary` token, which measures 4.18:1 and
  fails the 4.5:1 floor. The hero figure is set in the accent at 3.27:1, which
  clears the 3:1 large-text floor and nothing smaller may use it
- Greyscale luminance of the marks: ink 78, accent 113, ring 149, field 231
- Legible at 200px wide, and as a still — at thumbnail size the hero figure,
  its label and the arrow's descent are what survive, which is the point. The
  descent still reads with the colour stripped out

## Rendering

The build prefers Chromium's `headless_shell`. Both `chrome --headless` and
`--headless=new` rasterise only about the first 1263px of a 1350px window and
leave the rest unpainted while still writing a full-height PNG — the page
background fills the gap, so the tile looks finished and is quietly missing the
last line of the source block. `verify_png()` checks the bottom margin by pixel
after every build.

Type is Archivo, fetched once into `.fontcache/` and subset into the HTML. It
substitutes Berthold Akzidenz Grotesk, which is not web-licensable. Offline, the
build falls back to Arial, which is the brand's own stated print fallback.
