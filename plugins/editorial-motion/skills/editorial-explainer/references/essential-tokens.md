# Essential design system — working reference

**This file carries no values.** The Essential Design System's `tokens/*.css`
is the only place a colour, size or spacing number exists; this file is the
judgement that sits on top of it — which slot to fill with what, and the house
decisions the token file cannot express.

That split is new, and it was not free. The version of this file that carried
its own value table had drifted into stating `--surface-page` as `#FFFFFF`
when the token file defines it as `#fbf7f5` and the linter fails a pure-white
ground as an *error* — so the reference, the tokens and the checker gave three
different answers to the most common decision in the system. Copies of numbers
do not stay right. Read the token file.

## Role slots

Fill **editorial-explainer**'s slots from these tokens. Take the values from
`tokens/colors.css`; the names are stable, the numbers are not yours to quote.

| Slot | Token |
|---|---|
| ground | `--ground-paper` (the default) |
| ground, alternates | `--ground-paper-deep`, `-sand`, `-rust`, `-moss`, `-plum`, `-ink`, `-orange` — each ships its paired ink as `--on-*` |
| inset surface | `--surface-inset` |
| ink | `--text-primary` |
| muted | `--text-secondary`, `--text-muted` |
| accent | `--color-accent` |
| secondary | `--ess-warm-grey-200` |
| rules/borders | `--border-subtle` |
| dark ground | `--surface-dark` |

**The ground is tinted paper, not white.** `--ground-paper` is the default for
documents, decks, charts and web. Pure white is demoted to an *inset* surface —
cards, input fields, table bodies — and nothing sits on raw white edge to edge.
🔒 `check-artifact.py` fails a pure-white or pure-black ground at error
severity, so this is not a preference you can quietly decline.

**One ground per artefact.** Type sits directly on it; never a card inside a
card. In a sequence — carousel, slide run, spread — the ground identifies the
*piece* and stays constant while only the type block changes.

**Cyan `#00ACED` is Essential Research's colour in brand furniture** — logos,
badges, buttons, sub-brand signalling. Never a general accent.

✅ **Inside data visualisation, cyan is released.** It is the third categorical
hue and the negative pole of the canonical agree/disagree diverging ramp
(`--viz-div-*`). This is a documented, deliberate decision of the design
system, taken because the categorical ramp cannot carry three categories
without it — not a drift. An earlier version of this file banned exactly the
case the design system ships as canon; if you find that instruction anywhere
still, the design system wins.

## Type

- **Archivo** substitutes Berthold Akzidenz Grotesk (not web-licensable). Print
  fallback is **Arial**.
  ⚠️ `tokens/fonts.css` loads Archivo and Newsreader by `@import` from Google
  Fonts, which artifact CSP blocks — so an artifact using it renders in Arial
  with neither brand face present. Arial is the brand's own stated fallback, so
  this degrades rather than breaks, but the poster scale's leading and tracking
  are calibrated for Archivo. For artifact output, inline a subset `woff2` as a
  base64 `@font-face` instead of linking the CDN.
- Working weight pair: **Bold (700) + Light (300)**. Regular for digital body.
- **Two registers, strict division of labour.** The grotesque is the *machine
  layer* — display headlines, UI, body copy, axis and tick labels, the grey
  line naming what is measured. The serif is the *voice layer* — standfirst,
  deck, byline, pull quote, annotation, source note. Nothing crosses over:
  display headlines never take the serif, and the serif never takes body copy
  or UI.
  ⚠️ The system registers both `--font-voice` and `--font-editorial` for that
  serif, scoped slightly differently (`fonts.css` says charts only; the readme
  says the whole voice layer). Unresolved — see `decisions.md`. Until it is,
  use `--font-editorial` inside a chart and ask before setting a standfirst
  outside one.
- Scale: read it from `tokens/typography.css`. It runs from `--fs-caption` up
  through `--fs-display`, and above that a **poster scale**
  (`--fs-poster-sm` / `--fs-poster` / `--fs-poster-lg`) where leading drops
  below 1 (`--lh-poster`) and tracking tightens (`--tracking-poster`). Set a
  poster headline as a *mass*: push the rag so each line nearly fills the
  measure, and let it occupy 35–60% of the frame.
- **Sentence case, left-aligned.** Never title case, never all-caps headings,
  at any size — density comes from weight, leading and rag, never capitals.
  This aligns with the ban on capitalised overlines.

## The brand dot

Essential's full stop is **round**. Archivo renders `.` as a hard square, so
**never type a period at the end of a headline** — use a `border-radius:50%` span
at `0.24em` in the accent colour.

```css
.dot-mark{display:inline-block;width:.24em;height:.24em;border-radius:50%;
  background:var(--color-accent);margin-left:.06em}
```

## The dot pattern

The brand's defining motif — dots resolving left to right from sparse and pale
into dense and saturated. Two forms:

- **The full field**, for covers and section pages. **Use the official artwork
  where the design system is available** — its `dot-pattern.png`, extracted
  from the supplied report title page. It is the real thing; generating a
  lookalike beside it is how a brand motif drifts. That artwork does *not* ship
  with this skill, which is why the generator below still exists.

  Generate the field only when working standalone, without the design system
  to hand, or when the canvas is large enough that resampling the artwork would
  show. Dot radius and opacity both ramp with horizontal position:

  ```js
  /* sparse and pale at the left, dense and saturated at the right */
  for(let c=0;c<COLS;c++){
    const p=c/(COLS-1);                       /* 0 → 1 across the field   */
    const step=lerp(34,13,p);                 /* spacing tightens          */
    for(let y=step/2;y<H;y+=step){
      ctx.globalAlpha=lerp(.14,1,p*p);        /* squared: a slow start     */
      ctx.beginPath();
      ctx.arc(x,y,lerp(1.1,3.2,p),0,6.2832);
      ctx.fillStyle=ACCENT; ctx.fill();
    }
  }
  ```

  Keep the ramp non-linear. A linear ramp reads as a gradient; the squared
  alpha keeps the left end genuinely sparse, which is what makes the right end
  read as arrival.

- The single-rule form — a tight triplet, then gaps widening until one isolated
  dot trails off. Use for accent rules, dividers and header bands. It replaces
  the generic horizontal rule and is a better section divider than anything in
  this skill.

## Branding weight, by format

| Format | Branding |
|---|---|
| Social tile, carousel frame | **The accent dot alone**, at the end of the headline. Nothing else |
| Report visual, deck slide | Wordmark in one fixed corner, plus the full source line |
| Cover frame of a set | Wordmark permitted; the dot alone on every frame after it |

A wordmark on a feed tile reads as an ad and gets scrolled past. The round accent
full stop is enough for anyone who knows the client to recognise the work, which
is the whole test in *Take the brand lightly*. **Never the mark and the dot on
the same frame**, and never the dot-pattern motif as well on a tile that already
has the headline dot.

## The report name appears once

`Essential Report, <month> <year>` goes in **one** place — normally the source
line, which has to carry the base and n anyway. Not also as an eyebrow above the
headline, and not also as a corner date stamp. Repeating it wastes the tightest
band on the frame and reads as an unedited template. If the chart head wants a
right-hand label, give it the unit (`% of all respondents`), not the wave.

## Combined categories get a note

Where two response options are merged into one mark — *neither support nor
oppose* plus *don't know* shown as a single "Undecided" — say so in the footer.
It is one line, it is ordinary research practice, and a merged category with no
note is the kind of thing that gets a chart quoted back at you.

## Other constraints

- **The E. symbol is the default mark**, and the corner anchor on every
  artefact — the design system's `logo-e.png`, or `logo-e-reversed.png` on dark
  grounds. Hold one corner position per artefact across a whole sequence, at
  5–7% of the short edge, on the same optical margin as the text, never in a
  lockup with a title.
  ⚠️ **This skill does not ship the E. symbol** — only the wordmarks,
  `assets/logo-nourl.png` and `assets/logo-primary.png` (with strapline). Take
  the symbol from the design system. If it is not to hand, use the wordmark
  small in the corner and say you substituted; do **not** crop an E out of the
  wordmark yourself.
- The full wordmark is for **mastheads and document footers only** — where the
  brand is introduced rather than signed. **Never reconstruct the mark in
  type**, and never filter it to solid white.
- Tone: clarity above all — precise, jargon-free, conversational but not too
  informal. **No emoji.** No underlined words — emphasis is weight, size, the
  orange dot, or a `Mark` block behind one word, one per headline. No small
  uppercase orange kickers above a headline, in any slot — and no uppercase
  labels anywhere else either, kicker or not. Sentence case throughout.
- Spacing, radii and elevation come from `tokens/spacing.css` and
  `tokens/effects.css`. The shape of the system: an 8px base rhythm, small
  geometric radii plus a pill for chips, restrained warm-neutral shadows. The
  brand leans flat — no large soft corners, no elevation as decoration.
- Components ship as JSX plus a prebuilt browser bundle (`_ds_bundle.js`) for
  static mocks. Prefer real components over reimplementing them.
