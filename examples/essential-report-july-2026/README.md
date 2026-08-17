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

`DATA["hero"]` picks which number that is:

| Value | Hero figure |
|---|---|
| `"level"` | the accent group's own share this month (default) |
| `"gap"` | how far the leading group sits clear of the other |
| `"change"` | the accent group's movement on June |

Beneath it, a hundred dots — one dot per percentage point — so the proportion
is countable against a denominator that is on screen. Right direction and wrong
direction are filled; unsure is drawn as open rings.

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

`hero_label` and `change_line` derive from the numbers if left as `None`. The
takeaway is editorial judgement, so write your own when the month has a better
story than the arithmetic can see.

## Checks this passes

- `check-artifact.py --strict` — clean
- Text contrast on the warm ground: ink 6.73:1, muted 4.85:1. The muted grey is
  one step darker than the `--text-secondary` token, which measures 4.18:1 and
  fails the 4.5:1 floor. The hero figure is set in the accent at 3.27:1, which
  clears the 3:1 large-text floor and nothing smaller may use it
- Greyscale luminance of the marks: ink 78, accent 113, ring 149, field 231
- Legible at 200px wide, and as a still — at thumbnail size the hero figure and
  its label are what survive, which is the point

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
