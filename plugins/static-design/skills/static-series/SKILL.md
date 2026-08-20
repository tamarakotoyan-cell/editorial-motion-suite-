---
name: static-series
description: Carousels, post sets and multi-frame static work — what is held constant across frames and what must vary. Use whenever a static piece is more than one frame: an Instagram or LinkedIn carousel, a story sequence, a set of tiles posted together, a multi-slide static deck. Covers the carousel as one continuous object, the hold-style-vary-composition rule, continued objects across frame boundaries, the frame budget, chrome limits across a set, the cover frame's exceptions and how the last frame should end. Load after static-composition and static-type-graphics.
---

# Static series — carousels and post sets

The rule that separates good static work from rejected most sharply, because it is the one
that cannot be seen in a single frame.

Full detail: `references/05-series.md`.

---

## The carousel is one object

Not a set of slides with a shared style. One object, viewed through a moving window.

The strongest form in the reference set: a chart runs off the right edge of frame one and
continues from that point on frame two. Nothing is redrawn. The reader swipes and the
object keeps going.

The weakest: three consecutive slides of one deck, identical in chrome, margins, headline
position and empty middle. Different words, same frame, three times.

## Hold constant, vary deliberately

**Held constant across every frame — no exceptions:**

- Ground colour and texture
- Type families, scale ratio, register definitions
- Margin value
- Mark position and size
- Accent colour and what it means
- Source-line treatment

**Varied on every frame — no exceptions:**

- The composition. Which third the copy anchors to, where the image sits, the proportion
  between copy and image.

That is the whole rule. **Style is the constant; arrangement is the variable.** Rejected
work inverts it — holding arrangement constant and varying only the words.

**The test:** lay the frames side by side, blur them until the words are illegible, and
look at the shapes. If two frames have the same shape, one of them has not been composed.
`check-static.py --set` runs this mechanically.

## Continued objects

Where the content allows it, carry one object across a frame boundary:

- **A chart that continues.** Frame one ends mid-series; frame two resumes it. The y-axis
  can be dropped on the second frame — the reader has already learned it.
- **A sentence that continues.** A headline ending in an ellipsis and picking up on the
  next frame. This is also how a serial running head earns its place.
- **An illustration that grows.** The same object at three scales across three frames.

If two consecutive frames share *no* element, they are probably two separate posts, and the
join between them is the weakest point in the sequence.

## The frame budget

| Frames | Use |
|---|---|
| 1 | One fact — a stat tile, a quote, an event |
| 3–5 | **The working default.** Cover, two or three developments, a close |
| 6–10 | Only when the content is genuinely enumerable, each frame still one fact |
| 12+ | Almost always a document pretending to be a carousel |

**One frame, one fact.** If a frame needs two sentences of explanation, it is two frames.
This is also the cure for dead canvas: a frame with too little on it is usually a frame
whose content was split too thin, not one that needed more furniture.

## Chrome across a set

**One persistent brand element per frame** — a mark, in a fixed corner, at roughly 3% of
canvas width. Pagination, handles and secondary lockups are each a second, third and
fourth.

The serial running head (see **static-type-graphics**) is the sole permitted addition, and
only when it appears verbatim on three or more consecutive frames.

## The cover, and the close

The **cover** has a different job and gets the only exceptions in the system: it may be
centred where the others are not, it establishes ground, faces, mark position and accent
for the whole set, and it carries the byline the others omit.

The **last frame** ends the argument. A closing statement, the source line at full size, or
the finding restated. Not a call-to-action pill, not "link in bio", not a logo sting on an
otherwise empty field — both rejected infographics end on a subscribe prompt and both are
the weakest frame of their set.

## Self-check

- Blur every frame. Do any two share a shape?
- Are ground, type, margin, mark and accent identical on every frame?
- Does anything carry across a frame boundary?
- Does each frame hold exactly one fact?
- More than one persistent brand element on any frame?
- Is the cover the only centred frame?
- Does the last frame end the argument rather than sell something?
