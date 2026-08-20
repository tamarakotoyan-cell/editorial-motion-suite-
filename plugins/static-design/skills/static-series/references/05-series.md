<!-- Vendored copy. Master: Static design content/static-design-system/principles/05-series.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 05 — Series, carousels and post sets

The rule that separates the good reference set from the rejected one most sharply, because
it is the one that cannot be seen in a single frame.

---

## The carousel is one object

Not a set of slides with a shared style. One object, viewed through a moving window.

The strongest example in the reference set is
`good example: guardian-chart-slide-1.png` and `-slide-2.png`: the same chart runs off
the right edge of slide 1 and continues from that point on slide 2. Nothing is redrawn. The
reader swipes and the object keeps going.

The weakest is `bad example: aiherway-inline-editing.jpg` alongside
`aiherway-label-table.jpg` and `aiherway-dark-quote.jpg` — slides 5, 6 and 7 of one deck,
identical in chrome, margins, headline position and empty middle. Different words, same
frame, three times.

## Hold constant, vary deliberately

**Held constant across every frame in a post — no exceptions:**

- Ground colour and texture
- Type families, scale ratio and register definitions
- Margin value
- Mark position and size
- Accent colour and what it means
- Source-line treatment

**Varied on every frame — no exceptions:**

- The composition. Which third the copy is anchored to, where the image sits, the
  proportion between copy and image.

That is the whole rule. Style is the constant; arrangement is the variable. The rejected
examples invert it: they hold arrangement constant and vary only the words.

> `good example: nyt-multi-quote-stack.png`, `nyt-quote-over-illustration.png` and
> `nyt-illustration-over-headline.png` are three consecutive slides of one carousel. Same
> ground, same faces, same running head, same mark. Three different arrangements: image
> between quotes, image below a quote, image above a headline.

**The test for anti-pattern H:** lay the frames side by side, blur them until the words are
illegible, and look at the shapes. If two frames have the same shape, one of them has not
been composed.

## Continued objects

Where the content allows it, carry one object across the frame boundary:

- **A chart that continues.** Slide 1 ends mid-series; slide 2 resumes it. The y-axis can be
  dropped on the second frame — the reader has already learned it.
- **A sentence that continues.** A headline that ends in an ellipsis on one frame and picks
  up on the next. NYT's running head does exactly this: "TO BUILD MORE HOUSING…" then
  "… on top of public libraries …" then "… and use old ferry boats …".
- **An illustration that grows.** The same object at three scales across three frames.

This is what makes a carousel read as an argument rather than a folder. If two consecutive
frames share *no* element, they are probably two separate posts, and the join between them
is the weakest point in the sequence.

## The frame budget

| Frames | Use |
|---|---|
| 1 | One fact. A stat tile, a quote, an event. |
| 3–5 | The working default. Cover, two or three developments, a close. |
| 6–10 | Only when the content is genuinely enumerable — a list of venues, a set of findings. Each frame still holds one fact. |
| 12+ | Almost always a document pretending to be a carousel. |

**One frame, one fact.** If a frame needs two sentences of explanation, it is two frames.
This is also the cure for the dead-canvas anti-pattern: a frame with too little on it is
usually a frame whose content was split too thin, not a frame that needed more furniture.

## Chrome across a set

**One persistent brand element per frame.** A mark, in a fixed corner, at roughly 3% of
canvas width.

Pagination, handles, running heads and secondary lockups are each a second, third and
fourth. `bad example: aiherway-dark-quote.jpg` carries four and has two pieces of
content.

The serial running head from `02-typography` is the sole permitted addition, and only when
it appears verbatim on three or more consecutive frames.

## The cover frame

The cover has a different job from the frames after it and is allowed to look different:

- It may be centred where the others are not.
- It establishes ground, faces, mark position and accent for the whole set.
- It carries the byline or the attribution the others omit.

It is the only frame that gets these exceptions.

## The last frame

Ends the argument; it does not advertise. A closing statement, the source line at full
size, or the finding restated.

Not a call-to-action pill, not a "link in bio", not a logo sting on an otherwise empty
field. Both rejected infographics end on a subscribe prompt, and both are the weakest frame
of their set.

## Self-check

- Blur every frame. Do any two share a shape?
- Is ground, type, margin, mark and accent identical on every frame?
- Does anything carry across a frame boundary?
- Does each frame hold exactly one fact?
- Is there more than one persistent brand element per frame?
- Is the cover the only centred frame?
- Does the last frame end the argument rather than sell something?
