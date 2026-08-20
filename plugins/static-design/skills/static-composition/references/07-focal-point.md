<!-- Vendored copy. Master: Static design content/static-design-system/principles/07-focal-point.md
     Regenerate with sync-static-design.py; do not edit here. -->

# 07 — Focal point

What the eye lands on first, and why it lands there rather than somewhere else.

Settled after `01-layout` has decided where things go and before `03-colour` assigns
values. A frame can pass every other rule in this system and still read flat, and this is
the file that explains why.

---

## The focal point is a contrast of kind, not a contrast of size

**One element differs from every other element in one property. That difference is the
focal point.** Not the biggest thing — the *only* thing.

This is the correction to `01-layout`'s "reading order is created by size". Size creates
order once the eye has landed. It does not decide where the eye lands.

Derived from nine reference covers (Vox, the Atlantic, NYT). Eight of the nine make their
focal point by isolating a property; only two use scale alone, and both of those are
type-only frames with nothing to contrast against.

> `good example: atlas-disc-saturation-isolation.png` — a black line engraving, and
> one concentric disc in fluorescent pink, green and cyan. The disc is not the largest
> element. It is the only saturated one.
>
> **vox-heart-textures** *(not on disk — see `good example: annotations.md`)* — a
> collage of muted browns and greys, and one red heart. Same mechanism, one register up.

## The five carriers

Pick one. Name it out loud before building — if you cannot finish the sentence *"the
focal point is the only ___ thing on this frame"*, there is no focal point yet.

| Carrier | The one element is the only… | Reference |
|---|---|---|
| **Saturation** | saturated thing among muted or neutral ones | Atlas disc; the red heart |
| **Register** | photographic thing among flat ones, or the reverse | Vox "Lazy but effective" — one duotone photographic hand among flat vector speech bubbles |
| **Density** | detailed thing in an empty field, or the reverse | The Orwell head — a dense collage inside a silhouette, on a flat halftone ground |
| **Texture** | worked surface among clean ones | Vox heart — every shape carries its own paper or fabric |
| **Negative space** | lit thing in a dark frame, or the reverse | Vox "Undisciplined trick" — a white light shaft is the largest shape and it points at a tiny black silhouette |

**One carrier per frame.** Two carriers on two different elements is two focal points,
which is none. Two carriers on the *same* element is emphasis and is fine — the Orwell
head is both dense and, in the collage, the only place any photograph appears.

## Isolation is a property of the set, not of the element

A saturated red is not a focal point on a frame of saturated colours. It is one of them.

The move is almost always **suppressing the field, not amplifying the subject.** This is
the mistake worth naming because it is the one that gets made: a frame reads flat, and the
instinct is to make the intended focal element louder. It rarely works, because the thing
drowning it is still there.

> Built this way and corrected: a tile where the hero figure was set in the accent and
> still lost, because the largest fragment on the canvas was a bright saturated block of
> the same colour. The fix was not a brighter figure. It was dropping the fragment to a
> deep, dull value so the figure became the only saturated thing — one ink, two densities.

## Type carries the focal point as readily as picture

Three of the nine references put it in the copy: `03-colour`'s emphasis devices are focal
devices, not decoration. The hero figure in the accent, the one clause that changes
colour, the headline knocked out of a colour field.

Where the frame is a data tile, this is usually the right answer. **The figure is the
finding, so the figure is the only saturated thing on the sheet**, and every picture on it
sits at a lower value.

## The type zone

**On a type-led frame, the copy occupies a zone, not a corner.**

The Vox covers give the headline 35–55% of the canvas as one block of tight caps. A
headline parked in a bottom-left quadrant with the other three quarters loosely filled is
the failure `01-layout` catches as occupancy — but a frame can pass the 60% floor and
still have no type zone, because pictures made up the difference.

Measured as the union of the text bounding boxes against the usable canvas:

| Frame | Floor |
|---|---|
| Type-led — the words are the picture | 28% |
| Picture-led — a photograph, chart or mark field carries it | 18% |

## What the linter can and cannot see

`assets/check-static.py` checks **U** (chroma isolation) and **W** (type-zone share). Both are
partial by construction:

- **U reads CSS colour only.** It cannot sample a photograph, so a frame whose focal point
  is a saturated *picture* against muted marks will report as unfocused. It is a warning,
  not an error, for exactly that reason.
- **Register, density, texture and negative space are invisible to it.** A frame that
  passes U has not been shown to have a focal point; a frame that fails it may have a
  perfectly good one the check cannot reach.

The check exists to catch the common case — a frame where nothing is isolated by anything
— and to force the question. Answer it yourself.

## Self-check

- Can you finish *"the focal point is the only ___ thing on this frame"*?
- Is that true of the **set**, or only of the element in isolation?
- Is exactly one carrier doing the work?
- If the frame reads flat, have you tried suppressing the field rather than amplifying the
  subject?
- On a type-led frame, does the copy own at least 28% of the usable canvas?
