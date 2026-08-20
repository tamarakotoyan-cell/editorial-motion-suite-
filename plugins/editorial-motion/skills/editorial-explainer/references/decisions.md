# Decision log

Dated, so a resolved question stops looking like a live one. The design
system's readme carries a good rejected-pattern register ("Deliberately not in
the system") and a good open-questions list ("Caveats / to confirm"), but
neither is dated or versioned, so there is no way to tell a caveat someone
answered in March from one nobody has looked at.

**Status** is one of: `settled` — decided, cite it and move on. `open` — a real
question with a named owner; ask rather than guess. `deferred` — known, not
worth resolving yet.

---

## Settled

### The ground is tinted paper, not white
`settled` · 2026-08-17 · owner: design system

`--ground-paper` is the default ground for documents, decks, charts and web.
Pure white is an inset surface only. Enforced: `check-artifact.py` fails a
pure-white ground at error severity.

*Why it is logged:* `essential-tokens.md` stated the opposite — ground =
`#FFFFFF` — against a token file defining it as `#fbf7f5` and a linter that
fails it. Three sources, three answers, on the most frequent decision in the
system. Corrected 2026-08-17.

### Cyan is a data hue inside charts, Research-only outside them
`settled` · 2026-08-17 · owner: brand

Inside data visualisation, cyan is the third categorical hue and the negative
pole of the agree/disagree diverging ramp (`--viz-div-*`). In brand furniture —
logos, badges, buttons, sub-brand signalling — it remains Essential Research
only.

*Why:* the categorical ramp cannot carry three categories without it. The
design system took this decision deliberately and documented the reasoning;
`essential-tokens.md` carried a flat ban on exactly the case the system ships
as canon. Resolved in favour of the design system, per the precedence rule that
a documented design decision outranks a derived summary. **If a brand owner
wants to reverse this, the consequence is that the categorical ramp drops to
orange, greys and moss.**

### The 🔒 marks are generated, not maintained
`settled` · 2026-08-17 · owner: system

`check-artifact.py --rules` prints every rule and the severity it actually
fires at. `house-rules.md` is reconciled against that output, and CI fails if
they disagree.

*Why:* three marks were wrong — a 🔒 on decorative background gradients, which
the linter never implemented, and 🔒 on source-line and stagger-band, which only
warn. A false 🔒 is worse than no mark: it tells the reader they can stop
holding the rule in mind.

### A missing source line is an error for research and editorial work
`settled` · 2026-08-17 · owner: system

`check-artifact.py --profile research` (or `editorial`) promotes `source-line`
to an error. It stays a warning by default because the checker cannot tell a
survey finding from a product mockup from the HTML alone.

### The version stamp is read from the manifest, never written in prose
`settled` · 2026-08-17 · owner: system

Three numbers disagreed — manifest `1.11.0`, installed copy `1.9.0`, and a
literal `1.8.0` in the router's worked example — while the linter failed a
stale stamp at error severity. Prose now shows a placeholder; CI asserts the
example contains no literal version.

### Attribution is set as labelled lines, never a mid-dot chain
`settled` · 2026-08-17 · owner: system

```
Essential Report, March 2026
Base: all participants (n=1,002)
```

The linter's own exemplar had been written as a mid-dot chain, which the same
document bans two sections earlier.

---

## Open

### Does `--text-muted` darken, or does its use narrow?
`open` · raised 2026-08-17 · owner: **designer + accessibility**

`--text-muted` is the lightest grey in the palette and does not clear 4.5:1 on
the paper ground. The mandated source-and-base line is specified as "small and
muted", so the system's own non-negotiable currently specifies a contrast
failure. Two ways out, both brand decisions:

1. Darken the token, which changes every existing use.
2. Restrict it to non-essential text and set the source line in
   `--text-secondary`.

**Interim:** option 2, unenforced. See `accessibility.md`.

### `--font-voice` or `--font-editorial` — which owns the serif?
`open` · raised 2026-08-17 · owner: **designer**

Both tokens are registered. `fonts.css` and the design-system `SKILL.md` scope
Newsreader to chart headlines, annotations and source notes, and say "never
slide furniture". The readme assigns the voice layer standfirst, deck, byline
and pull quote — which on a slide *is* slide furniture. Either alias one to the
other and delete the loser, or state the boundary in the typography token file.

**Interim:** `--font-editorial` inside a chart; ask before setting a standfirst
outside one.

### Is `static-design` a permanent profile or a pilot?
`open` · raised 2026-08-17 · owner: **you**

It determines whether the two linters converge into one with per-profile rule
sets, or stay separate. `check-static.py` has a rendered tier —
contrast, accent inflation, dead canvas, focal isolation, template sameness —
that `check-artifact.py` has no equivalent for, and six guardrails currently
exist only there.

### The semantic info colour is a sub-brand-restricted hue
`open` · raised 2026-08-17 · owner: **brand**

`tokens/colors.css` sets `--color-info: var(--ess-cyan)` in a file whose header
reserves cyan for Essential Research. Any core-Essential UI showing an info
state therefore uses the Research hue. Suggest deriving it from the warm
neutrals like the other feedback colours.

---

## Deferred

### Physical move to a `core/` directory
`deferred` · 2026-08-17

`house-rules.md`, `design-method.md`, `brand-integration.md`,
`accessibility.md` and this file are the shared core in everything but
location: they sit under `editorial-explainer/references/` and are cited across
skills by relative path, with `build-skills.py` vendoring them where needed.
Moving them to a real `core/` is correct and is a build-script change, not a
content change. Not yet done — it touches every citation path at once, and the
contradiction fixes were worth landing first.

### Brand caveats awaiting the brand owner
`deferred` · carried from the design-system readme, undated there

Licensed Akzidenz Grotesk webfonts · confirmation of Newsreader as the
editorial serif · official E. symbol artwork to replace the derived crop · a
decision on illustration style, or a commitment to photography only · which
light warm grey is canonical (`#f5f3f3` vs `#e9e7e5`) · the Essential Research
secondary logo · the dot-pattern brand icons for the four service pillars.

*These are inputs from Raine & Makin, not decisions the system can take.*
