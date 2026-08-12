# Essential design system — working reference

Read from `Essential Design System.zip` (`essential-design/tokens/*.css`,
`SKILL.md`). The system itself is the authority — this is a quick-reference for
filling **editorial-explainer**'s role slots. If the two disagree, the system wins.

## Role slots, filled

| Slot | Token | Value |
|---|---|---|
| ground | `--surface-page` / `--surface-warm` | `#FFFFFF` / `#E9E7E5` |
| ink | `--text-primary` | `#4E4E50` |
| muted | `--text-secondary` / `--text-muted` | `#6D6D70` / `#A7A7A9` |
| accent | `--color-accent` | `#E2491A` (Pantone 1665) |
| secondary | `--ess-warm-grey-200` | `#D7D4D1` |
| rules/borders | `--border-subtle` | `#D7D4D1` |
| dark ground | `--surface-dark` | `#4E4E50` |

**This is a light warm system.** Default to white or warm-grey surfaces with grey
ink — not the dark editorial ground the reference material uses. A dark ground is
available (`--surface-dark`) for statement frames, used sparingly.

⛔ **Cyan `#00ACED` is Essential Research only.** Never use it as a general
accent or as the second colour in a diverging chart. For diverging data on
Essential (non-Research) work, use orange against warm grey.

## Type

- **Archivo** substitutes Berthold Akzidenz Grotesk (not web-licensable). Print
  fallback is **Arial**. Archivo loads via Google Fonts, which artifact CSP
  blocks — artifacts render in Arial, which is the brand's own stated fallback.
- Working weight pair: **Bold (700) + Light (300)**. Regular for digital body.
- Scale: display 56 / h1 40 / h2 30 / h3 22 / title 17 / body 16 / body-sm 14 /
  caption 12.
- Tracking tight `-0.02em` at display sizes — grotesques sit better slightly tight.
- **Sentence case, left-aligned.** Never title case, never all-caps headings.
  This aligns with the ban on capitalised overlines in SKILL.md.

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

- **The full field**, for covers and section pages. No artwork ships with this
  skill — generate it, so it scales to any canvas instead of being resampled.
  Dot radius and opacity both ramp with horizontal position:

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

## Other constraints

- Logos: `assets/logo-primary.png` (with URL strapline), `assets/logo-nourl.png`
  (wordmark + dot). **Never reconstruct the mark in type.**
- Tone: clarity above all — precise, jargon-free, conversational but not too
  informal. **No emoji.**
- Spacing runs on an 8px base rhythm. Radii are small (3/6/10px) plus a pill for
  chips — the brand reads geometric and clean, so no large soft corners.
- Components ship as JSX plus a prebuilt browser bundle (`_ds_bundle.js`) for
  static mocks. Prefer real components over reimplementing them.
