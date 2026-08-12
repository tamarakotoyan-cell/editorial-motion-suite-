# Design method

Adapted from Anthropic's `frontend-design` skill. That skill is written for a
studio inventing an identity from nothing. This plugin is written for a house
style serving a client who already has one. Most of `frontend-design` survives
that change; two parts of it do not, and the difference is the whole point of
this file.

**This is a method, not a style.** It does not override the precedence chain:
the client's brand first, then `house-rules.md`, then the style skills. It
governs *how you decide*, not *what you decide*.

---

## The tension, resolved

`frontend-design` says: make deliberate, opinionated choices about palette,
typography and layout specific to this brief, and take one real aesthetic risk.

This plugin says: take one typeface in the right register and one connecting
colour from the client, make everything else neutral, and stop.

Both are right, and they are talking about different budgets.

> **Spend the boldness on the signature, never on the palette or the type.**

Palette and typeface are the client's and are not yours to be interesting
with. The risk `frontend-design` asks for goes into the **device** — the one
technique that carries this particular finding — where it costs the brand
nothing and does all the work. A piece with Essential's orange, Essential's
Archivo and a genuinely surprising way of showing the number is on-brief. A
piece with an invented palette is off-brief no matter how good it looks.

---

## The signature

`frontend-design`'s most useful import, and a concept this plugin did not have:

> the single unique element this page will be remembered by

For a motion explainer the signature is **the one move that only this story
could have**. Not the grid, not the accent, not the texture — those are house.
The signature is the thing a viewer would describe if asked what they saw.

Test it by finishing this sentence in one clause: *"It's the one where …"*

- "…the hundred dots re-sort and two-thirds of them turn orange at once."
- "…the newspaper keeps sliding under the circled name."
- "…the figure counts up while the photograph pushes past it."

If the sentence needs two clauses, you have two signatures and no focal point.
If you cannot finish it at all, the piece is a competent arrangement of house
devices and will be forgotten. That is the failure this file exists to catch —
it is the motion equivalent of the chart that weights everything equally
because nothing decided what the finding was.

**One signature per piece.** It gets the accent move; everything else runs
ambient. This is the same ceiling as one-ambient-plus-one-accent, stated as an
editorial decision rather than a motion budget.

---

## Two passes: plan, critique, then build

Do not open a file until the plan exists and has survived the critique. Both
passes belong in your thinking; show the user the plan only if the brief is
ambiguous enough that the choice is theirs.

**Pass one — the plan.** Five lines, no more:

- **Finding** — the one sentence the piece exists to land. If you cannot write
  it, the piece is not ready. (This is the existing house rule; it is also the
  brief that everything below is critiqued against.)
- **Colour** — the role slots filled with hex values, from the client's system.
- **Type** — the faces per role, from the client's system, with the scale step.
- **Layout** — the grid and the format, in one sentence.
- **Signature** — the one move, in the "it's the one where…" form.

**Pass two — the critique.** Ask of each line: *would I have written this for
any other finding?* Where the answer is yes, that line is a default rather than
a choice. Revise it and note what changed and why. Only then build, deriving
every decision from the revised plan.

The critique is cheap and it is the step that gets skipped. Do it before the
first line of code, not after — a plan is a paragraph to rewrite, a build is
not.

---

## Check your defaults, including ours

`frontend-design` names three looks that AI-generated design falls into
regardless of subject: warm cream with a high-contrast serif and terracotta
accent; near-black with a single acid accent; broadsheet hairline rules with
dense columns. Where a brief pins a direction, follow it — the brief's words
always win. Where it leaves an axis free, do not spend that freedom on a
default.

**Two of those three describe this plugin's own output.** Warm grey ground with
an orange accent is one. Hairline rules, flat fills and newspaper devices are
another. That is not a reason to abandon the house style — it is the house
style, and it is the client's — but it means the usual test is not enough. Ask
the sharper version:

> Would this piece be interchangeable with the last Essential piece if you
> swapped the headline and the numbers?

The palette, the type and the texture are *supposed* to be interchangeable —
that is what makes a family. The **signature** is not. If the last three pieces
all opened on a scatter that settled into a ten-by-ten grid and ended on a
torn panel, the house style has become a template, and the next piece needs a
different device even though it keeps the same brand.

Keep a note of the devices used recently. Repetition across a set is a family;
repetition across every set is a rut.

---

## Then remove one thing

Before shipping, take one element out — the one that is doing the least. A
piece built to this plugin's craft list accumulates devices easily: texture,
grain, torn edge, offset echo, hand-drawn mark, caption chip, progress bar,
ghost layer. Each is defensible on its own and the sum is noise.

If removing it costs nothing, it was decoration. If the piece gets worse,
put it back and remove the next-least thing instead. Something always comes
out.

---

## Writing the copy

Words are design material. The existing rules cover mechanics — sentence case,
no capitalised overline, no typed period on a headline, source and base size
always present. These cover register.

- **Write from the reader's side.** Name things as the audience recognises
  them, not as the instrument recorded them. "More risk than opportunity", not
  "Response category 3".
- **Specific beats clever.** A headline that states the finding beats a
  headline that sets up a reveal the next frame has to pay off.
- **One job per element.** A headline states the finding, a legend names the
  colours, a source line carries provenance. Nothing quietly does double duty —
  a legend that is also the explanation is a headline that failed.
- **Active voice, plain verbs, no filler.** Match the tone to the client and
  the audience, not to the subject's own jargon.
- **Say what changed when the base changes.** A new question or a new sample is
  a fact the reader needs on screen, not a footnote you were hoping they would
  read.

If a chart needs two sentences of explanation, it is two frames. That rule is
about copy as much as it is about composition.

---

## What not to take from `frontend-design`

- **"Pair the display and body faces deliberately, not the same families you
  would reach for on any other project."** No. The typeface is the client's and
  is the same on every project by design. The register decision was made once,
  at brand level.
- **"A characterful display face used with restraint."** No, where the hero is
  a figure. The house ban on serif and display faces on hero figures stands.
- **Its hero-section and page-load framing.** It assumes a scrolling page. A
  fixed-canvas motion piece has beats, not sections, and its "hero" is beat
  one — which still needs to be the most characteristic thing in the subject's
  world, so the principle survives even though the mechanism does not.

---

## Method checklist

1. The finding is one sentence, written down before anything else.
2. The plan is five lines and predates the first line of code.
3. Every line of the plan survived "would I have written this for any brief?"
4. The signature finishes "it's the one where…" in a single clause.
5. The boldness is in the device, not the palette or the type.
6. The piece is not interchangeable with the last one after a content swap.
7. One element was removed before shipping.
8. The copy names things as the reader would.
