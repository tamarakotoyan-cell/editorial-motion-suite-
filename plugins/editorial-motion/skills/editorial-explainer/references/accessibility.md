# Accessibility — the layer that outranks house style

**Precedence.** Approved client brand first. **Accessibility second.** Then
documented design decisions, then the ban list, then editorial rules, then
taste. Everything below outranks every aesthetic preference in these skills,
including the ones stated as absolutes.

This file exists because an audit found the system had no accessibility source,
no contract on any component, and no check in the live linter — while the
precedence order put it second of six. Every other layer had all three.

---

## Contrast

Measure against the ground the text actually sits on, not the page default. On
a textured or photographic ground, measure against its lightest region under
the text.

| Content | Floor | Target |
|---|---|---|
| Body copy, labels, source lines | 4.5:1 | 7:1 |
| Text ≥24px, or ≥19px bold | 3:1 | 4.5:1 |
| Icons, chart marks, focus rings, form borders | 3:1 | 4.5:1 |
| Disabled controls | exempt | keep legible anyway |

**A chart mark carrying meaning is not decoration.** If a reader has to tell
two series apart, those two colours need 3:1 against each other as well as
against the ground. This is why direct labelling beats a legend — it stops the
distinction depending on hue at all.

**The known failure.** `--text-muted` is the lightest grey in the palette, and
the mandated source-and-base line is specified as "small and muted". On the
paper ground that pairing does not clear 4.5:1. Two ways out — darken the token
or restrict its use to non-essential text — and both are brand decisions rather
than linter decisions. Logged in `decisions.md`; unresolved. Until it is
resolved, set the source line in `--text-secondary`, which does clear the
floor.

**Never encode meaning in hue alone.** Positive/negative, selected/unselected,
error/valid all need a second channel: position, weight, a mark, a label.
Roughly one in twelve men has some form of colour vision deficiency, and the
house palette's orange-against-warm-grey is one of the harder pairs.

## Focus

- Every interactive element has a **visible** focus state. `outline: none` with
  nothing in its place is a defect, not a style.
- The house focus treatment is the brand orange ring with a soft tint halo. It
  must clear 3:1 against **both** the control and the ground behind it — on an
  orange ground, the ring inverts to the paired ink rather than disappearing.
- Use `:focus-visible` so pointer users do not see rings on click, but never
  fall back to no indicator for keyboard users.
- Focus order follows reading order. If the visual order and the DOM order
  disagree, the DOM is wrong — do not patch it with `tabindex` above 0.

## Keyboard

- Everything operable by mouse is operable by keyboard. A `div` with a click
  handler is not a control; use a `button`.
- Dialogs trap focus while open, return it to the trigger on close, and close
  on `Escape`.
- Tabs, menus and radio groups move with arrow keys, not `Tab` through every
  item.
- No keyboard trap anywhere. Test by tabbing the whole artefact once.

## Motion

- 🔒 Every artefact that animates carries a `prefers-reduced-motion: reduce`
  block. `check-artifact.py` fails a missing one at **error** severity — this
  is the one accessibility rule already enforced.
- Under reduced motion: no travel, no parallax, no autoplaying loop, no
  count-up. Cross-fades and instant state changes are fine. **The piece must
  still make sense** — which is the same requirement as the house rule that a
  tile has to work as a still, arrived at from the other direction.
- Nothing flashes more than three times per second.
- Ambient loops need a pause affordance if they run longer than five seconds
  and sit next to content someone is reading.

## Text and structure

- Real text, not text baked into an image, wherever the format allows it.
- Headings descend without skipping levels; the heading structure is the
  document outline, not a set of sizes.
- Images carry `alt`. A chart's alt text states **the finding**, not the chart
  type — "Trust in the ABC held flat while five other institutions fell" beats
  "line chart of trust over time". Purely decorative texture and grain get
  `alt=""` so screen readers skip them.
- Line length stays near 65 characters for running text; the artefact survives
  200% zoom without content being cut off.
- Language is declared on the root element.

## What is checked, and what is not

| Requirement | Status |
|---|---|
| Reduced-motion block present | 🔒 `check-artifact.py`, error |
| Contrast floors | Rendered tier of `check-static.py` — **not yet in the shared checker** |
| Visible focus state | Not checked. Human review |
| Keyboard order and traps | Not checked. Human review |
| Alt text present and meaningful | Presence is checkable; meaning is not |
| Colour-alone encoding | Human review |

Porting the contrast check into `check-artifact.py` is the next job on this
file. Until it lands, contrast is a review item on every artefact that ships,
and "it looked fine" is not the check — measure it.

## When the brand and access conflict

The brand outranks house style; it does not outrank access. Where an approved
brand colour cannot meet a contrast floor in a given role, do not silently
substitute a different colour and do not silently ship the failure. Keep the
brand colour where it carries identity, move the *text* to a compliant pair,
and record the conflict in `decisions.md` so it reaches whoever owns the brand.
That is the escalation, and it is a short conversation, not a redesign.
