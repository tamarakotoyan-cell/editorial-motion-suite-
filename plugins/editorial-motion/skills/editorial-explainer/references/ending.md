# How a piece ends

The rest of this plugin is well developed on how a piece opens and how each
beat is verified, and it stopped before the end. Everything here is measured,
either off the reference clips or off the reference implementation.

---

## Before you study any reference: measure the outro off

Downloaded short-form video carries a platform card after the content. In the
local reference set it is **exactly 4.1s** on eight of nine clips (2.6s on the
ninth). Study the last frame of that card and you are studying TikTok's
design, not the maker's.

Find the boundary by walking backwards from the end and comparing each frame
to the final frame; the first frame that stops resembling it is the last frame
the designer made. Do not look for the largest frame-to-frame jump in the tail
— in half the set the largest jump is an internal hard cut, not the outro.

Designed durations in the local set, once the card is removed: 26.1, 26.4,
27.2, 30.7, 37.3, 38.0, 42.4, 48.5, 61.0 seconds.

---

## The ending does not decelerate to a still

Motion energy — mean per-pixel frame-to-frame difference — measured across the
final second and across a mid-clip window, as a ratio of the two:

| clip | last second ÷ mid-clip | what the final frame is |
|---|---|---|
| 1 | 0.71 | held result card |
| 2 | 0.73 | presenter, caption chip |
| 3 | 1.44 | presenter, caption chip |
| 4 | **0.16** | static profile / CTA card |
| 5 | 2.02 | graph-paper ground, chip |
| 6 | **0.01** | static software timeline |
| 7 | 0.86 | newspaper scan, still dollying |
| 8 | 13.20 | full-frame photograph, punch-in |
| 9 | 5.10 | composited page |

**Rule.** If the last frame is content, the piece is still moving when it
ends — ratio 0.71 to 13.2, median ≈ 1.4. Nothing lands and then sits.
Only the two clips that end on a call-to-action card go still (0.16, 0.01).

So: **stillness at the end is correct only when the final frame is a card —
a CTA, a credit, a logo hand-off. If the final frame carries content, it keeps
its ambient move through the end.** A held photograph keeps its punch-in; a
document keeps its dolly. This is the same rule as "a camera that halts reads
as dead", applied to the one place authors reliably forget it.

**Honest limit on this evidence.** Six of the nine clips are After Effects
tutorials, not finished explainers, and two of the nine endings are tutorial
CTAs. The corpus is strong on *how these makers end a vertical short* and thin
on *how a data explainer resolves an argument*. Treat the motion-energy rule as
well supported and treat anything about editorial resolution below as
reasoning from the house rules, not from the tape.

---

## Budget the finale against what is covering the marks

The reference implementation hid its own payoff. Its final state started at
t=23.1s while the canvas was still hidden behind a torn panel until t=23.45s.
With a 1.2s transition and 0.5s stagger, the leading marks were already **64%
recoloured at the instant they became visible**. The piece's one conclusion —
22 in 100 becoming 63 in 100 — arrived as a pop, and the fastest, most legible
part of the move played behind a photograph.

Measured as a step-by-step canvas difference, the defect is unmistakable: a
single 14.5-unit step at the reveal, then immediate decay. A payoff that works
shows the opposite shape — energy rising to a peak and then settling.

**Rule.** The final state starts **after** whatever covers the marks has
cleared, not when the beat nominally begins. Write the reveal time down, and
start the transition at or after it. Then check the shape: sample the canvas
every 0.1s across the finale and confirm energy **rises to a peak and decays**.
A spike on the first visible frame means the move started behind something.

After the fix, the same finale measured 2.8 → 8.0 → 12.7 → 16.6 → **20.2** →
19.8 → 16.3 → 13.0 → … → 0.01, peaking 0.5s in and settling 1.7s later.

---

## Do not make the finale pay for other beats' furniture

Two rules elsewhere in this plugin are individually right and compound badly:
measure the band from the **tallest** copy block, and **reserve** a permanent
row for anything that appears mid-band. Applied globally, every beat pays the
worst case.

In the reference implementation the finale carried a 57px headline while the
band was sized for a 104px one, and reserved 64px for a trend read-out that
beat does not have. Measured on a 420×747 stage: a **145px** gap between
headline and marks against a **48px** gap below them — 19.4% of frame height
as a hole in the middle of the final composition, **111px of it unused
reservation**.

**Rule.** Measure each beat's band from **that beat's own** copy blocks, and
reserve a row only in the beats that use it. Blocks hidden with `opacity` are
still laid out, so every beat's blocks are measurable at build time regardless
of which beat is showing.

The gain is not only the space. Once each beat has its own band, the marks
**travel** between beats instead of only changing colour — which is what
"marks persist and re-sort" is supposed to buy you, and it is what gives the
finale its rising energy curve rather than a flat recolour in place.

**Floor.** Use an absolute floor (24px), never a fraction of frame height. A
percentage floor can exceed the space available and push marks under the copy,
which is the one thing the band exists to prevent.

---

## Measure the dead tail

After everything has landed, a loop holds a completely unchanging frame until
it wraps. Measure it: drive the clock, sample canvas difference and the
computed style of every animating element, and find the last moment anything
changes.

The reference implementation held **1.3s** of a frozen frame, because its
underline finished drawing at 25.6s and the loop ran to 27.0s. Re-sequencing
the accent to draw *after* the marks settle rather than across them brought
the tail to **0.7s** and gave the finale a legible order: marks travel and
recolour, marks settle, the underline lands under the word, hold, cut.

**Rule.** Target a dead tail under **0.8s**. Past about a second the piece
reads as having stopped rather than having concluded. If you cannot fit it,
trim a middle beat — never the finale.

**Corollary.** The finale's one accent move should follow its one data move,
not run across it. Two things moving at once in the last beat is the one place
the "one ambient plus one accent" ceiling is most often broken, because the
accent is usually timed off the loop and the data off the beat.

---

## The loop wrap is a cut

Nothing in this plugin governs how a looping piece's last frame meets its
first. The ambient-easing rule ("so the loop point is invisible") is about a
gradient drift, not about the narrative.

Treat the wrap as an edit, because that is what it is. Two options only:

- **A hard cut**, which needs the same justification as any other cut in the
  piece: the two frames must differ enough that it reads as deliberate. A dark
  data frame cutting to a full-frame photograph is a cut. A dark data frame
  cutting to a slightly different dark data frame is a glitch.
- **A match**, where the last state and the first share layout so the wrap
  reads as continuous.

What you cannot do is leave it unconsidered, which produces the third thing: a
frame that has been still for over a second and then changes completely.

---

## Verifying a final frame

Two mistakes will make you diagnose a bug that is not there. Both were made
while writing this file.

**Pausing via `getAnimations()` does not survive a repaint.** Setting
`currentTime` on the Animation objects holds only for the current synchronous
block; a later style recalculation hands back fresh objects and the CSS layer
restarts from zero. Any screenshot taken afterwards shows the wrong beat. To
hold a frame across tool calls, freeze declaratively — a negative
`animation-delay` plus a paused `animation-play-state`, injected as a
stylesheet rule, is part of the cascade and survives:

```js
freeze:function(t){
  PAUSED=true;                       /* see below */
  const time=((t%LOOP)+LOOP)%LOOP;
  let s=document.getElementById('__freeze');
  if(!s){ s=document.createElement('style'); s.id='__freeze'; document.head.appendChild(s); }
  s.textContent='.stage *,.stage{animation-delay:-'+time.toFixed(3)+
    's!important;animation-play-state:paused!important}';
  render(time);
}
```

This works because every animation in the piece runs one shared loop length
with no delay, so one rule selects the same frame for all of them. If yours
have individual delays, the rule has to carry them.

**Freezing the CSS does not stop the canvas.** The requestAnimationFrame loop
keeps drawing at wall-clock time, so the marks show one beat while the copy
shows another — which looks exactly like a state-machine bug in the piece.
Gate the loop on the same flag the freeze sets.

Measurement inside a single synchronous block is unaffected by either problem;
only inspection that spans tool calls needs the declarative freeze.

---

## Build robustness the ending depends on

**Refuse a zero-size build, and observe the element.** An element measured
while its pane is hidden reports zero width. A zero-width build leaves a 0×0
canvas, and nothing re-measures it, so the marks never appear at all — the
piece plays as copy over an empty field and the failure is silent. The
reference implementation had exactly this failure because it listened to
`window.resize` only, while the plugin's own example already used a
`ResizeObserver`.

```js
if(r.width<100||r.height<100) return false;   /* refuse; the observer will call again */
...
addEventListener('resize',build);
if(window.ResizeObserver){ new ResizeObserver(function(){build()}).observe(stage); }
if(document.fonts&&document.fonts.ready){ document.fonts.ready.then(function(){build();buildUL()}); }
```

The window never resizes when a pane is revealed, when a parent stops being
`display:none`, or when a webfont finishes loading and reflows the copy blocks
the band is measured from. That last one matters here specifically: the band
is measured from rendered copy, so a font swap after build silently
invalidates the whole layout.

**Ship a doctype.** A file beginning at `<title>` parses in quirks mode. It is
not what broke the layout above — that was tested and ruled out — but it is a
free source of difference between your machine and the viewer's.

---

## Ending checklist

1. Platform outro measured off before any reference claim.
2. Final state starts after whatever covers the marks has cleared.
3. Finale energy rises to a peak and decays — no spike on the first visible frame.
4. Final band measured from the final beat's own copy; no unused reservation.
5. Data move first, accent move after, never across.
6. Dead tail under 0.8s.
7. If the last frame is content it is still moving; if it is a card it is still.
8. The wrap is a cut or a match, and you can say which.
9. Final frame verified from a declaratively frozen render, with the canvas loop gated.
10. Mark totals in the final frame counted from pixels and reconciled against the legend.
