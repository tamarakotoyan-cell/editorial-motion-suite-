<!-- Vendored copy. Master: Static design content/static-design-system/brand.md
     Regenerate with sync-static-design.py; do not edit here. -->

# Static design system

The house standard for static output — social tiles, carousels, chart cards, event posters,
report visuals. Read this file first, then `principles/`, then the annotated examples.

**Read every file in this folder before generating anything.** The examples are the
argument; the principles are the summary of it.

---

## Precedence

Where two sources disagree, the higher one wins.

1. **The client's brand.** Colour and typeface come from them. Work is produced for many
   clients; Essential is simply the case where the client is Essential.
2. **`principles/06-anti-patterns.md`** — the ban list. It overrides everything below it.
3. **`principles/01`–`05`**, in order.

## Before you build — the five-line plan

Written before the first line of code, every time.

- **Finding** — the one sentence the piece exists to land. If you cannot write it, the
  piece is not ready.
- **Ground** — the field colour, from the client's system.
- **Type** — the two families and the scale ratio, from the client's system.
- **Layout** — grid, format and which third the content anchors to, in one sentence.
- **Signature** — the one device this piece will be remembered by, in the form
  *"it's the one where…"*, finished in a single clause.

Then critique each line: **would I have written this for any other finding?** Where the
answer is yes, that line is a default rather than a choice. Revise it before building.

**Spend the boldness on the signature, never on the palette or the type.** Palette and
typeface are the client's and are not yours to be interesting with. The risk goes into the
device, where it costs the brand nothing and does all the work.

## Role slots

Fill from the client's brand. Do not invent a palette.

| Slot | Job | Count |
|---|---|---|
| `ground` | The field everything sits on — never white, never pure black | 1 per frame |
| `ink` | Headlines, primary marks | 1 |
| `muted` | Attribution, source lines, axis labels | 1 |
| `accent` | The one thing that proves the point | **exactly 1** |
| `secondary` | The opposing side, diverging data only | 0–1 |

### The Essential case

| Slot | Value |
|---|---|
| ground | `#E9E7E5` warm grey, or `#FFFFFF` inset — prefer the warm grey |
| ink | `#4E4E50` |
| muted | `#5F5F62` — see the warning below |
| accent | `#E2491A` (Pantone 1665) |
| secondary | `#D7D4D1` |
| dark ground | `#4E4E50`, statement frames only |

Type: **Archivo** (substitutes Berthold Akzidenz Grotesk; Arial is the brand's own stated
print fallback and is what artifacts render in, since CSP blocks Google Fonts). Working
pair Bold 700 + Light 300. Sentence case, left-aligned, never title case.

⚠️ **The brand's own `--text-secondary` `#6D6D70` fails on the warm-grey ground.** Measured,
it is 4.18:1 against `#E9E7E5` — under the 4.5:1 floor for a source line or an axis label.
`#5F5F62` is the nearest value that passes, at 5.16:1. `--text-muted` `#A7A7A9` is far worse
at 1.95:1 and must never carry text on this ground. This is a finding about the token set,
not about any one artifact: it will recur on every light Essential piece until the tokens
change.

⛔ Cyan `#00ACED` is Essential Research only — never a general accent.

⛔ Archivo renders `.` as a hard square. Essential's full stop is round: never type a
period at the end of a headline; use a `border-radius:50%` span at `0.24em` in the accent.

⛔ Never reconstruct the Essential mark in type.

### Branding weight, by format

The "one persistent brand element" rule sets a ceiling. This sets the right level, which is
lower than people expect:

| Format | Branding |
|---|---|
| Social tile, carousel frame | **The accent dot alone**, at the end of the headline. Nothing else |
| Report visual, deck slide | Wordmark in one fixed corner, plus the full source line |
| Cover frame of a set | Wordmark permitted; then the dot alone on every frame after it |

A wordmark on a feed tile reads as an ad and gets scrolled. The round accent full stop is
enough to make the piece recognisable to anyone who knows the client, which is the whole
test in `03-colour-and-ground`. Never both the mark and the dot on the same frame.

## Canvas set

| Format | Size | Use |
|---|---|---|
| 4:5 | 1080×1350 | **The default.** Feed posts and carousels — ~25% more screen than 1:1 |
| 1:1 | 1080×1080 | Ad units, grid-sensitive sets |
| 9:16 | 1080×1920 | Stories, Reels covers. One statement only |
| 16:9 | 1920×1080 | Slides and decks. Comparison needs width |

Comparison needs width; sequence suits height. Re-compose per format — never scale one
master.

## The rules that fail a build

Full list and reasoning in `principles/06-anti-patterns.md`. In one page:

- Content covers **≥60%** of the canvas.
- Ground is tinted — never `#FFFFFF`, never `#000000`.
- **No containers**: no cards, panels, borders, shadows, glows, or radius above 10px.
- **Two type families**, three registers, every size on one ratio.
- Headline cap-height **8–12%** of canvas height on a type-led frame, **≥4%** where a
  picture carries the canvas; nothing below **1.25%**.
- Nothing runs past a frame edge, and no two text blocks overlap.
- **No text within 150px of the top or bottom edge** — the profile grid crops 4:5 to a
  centre square and carousel dots overlay the foot. Bleed art may cross it; text may not.
- **One accent, one element class.** One emphasis device per frame.
- Text **≥4.5:1** against its field; marks **≥ΔL 25** against each other and the field —
  and where three fills plus an accent make that arithmetically impossible, the hairline
  rescue and the measured L\* values are both written into the file.
- **One persistent brand element** per frame — and on a social tile that element is the
  accent dot, not the wordmark.
- **Hero figure 1.2–2× the display size** on any frame whose job is a number.
- **Nested marks size with flex-grow, never percentages.** Pixel width ÷ value is one
  number across every mark on the rendered file.
- **No value–label list under a chart.** Label inside the mark, or run a leader to it.
- No decorative gradient. The only permitted gradient is a type plate at a frame edge.
- No serif or display face on a hero figure. No `tabular-nums` on one either.
- No caps overline above a single frame's headline.
- **No mid-dot metadata chains** (`Source · Date · Sample`). Line breaks, commas or plain
  labelled lines. One mid-dot is fine; two in a string is a chain.
- **Texture on type is opt-in and per-string**, never global. Ground texture is required and
  composition-wide. They are different decisions.
- Across a set: hold ground, type, margin, mark and accent constant; **vary the composition
  on every frame.**
- One texture layer, grain at 4–6%.
- Source and sample size on any frame carrying data.

## Tone

Clarity above all. Precise, jargon-free, conversational but not too informal.

- **Write from the reader's side.** Name things as the audience recognises them, not as the
  instrument recorded them.
- **Specific beats clever.** A headline that states the finding beats one that sets up a
  reveal.
- **One job per element.** A headline states the finding; a source line carries provenance.
  Nothing does double duty.
- No emoji.

## Before you ship

1. At 200px wide, is the finding still legible?
2. Could someone state the point out loud after two seconds?
3. Would this be interchangeable with the last piece after a content swap? **"Yes" is the
   failure.**
4. Remove the one element doing the least. Something always comes out.
5. Verify against the ban list above — every line, honestly, against the actual output.
   **Where the surface has a linter** (Claude Code, Cowork: `python3 check-static.py
   artifact.html`), run it; errors are not advisory. **Where it does not** (Claude Design,
   chat), the check is read rather than run: work down the ban list, state the number for
   each mechanical rule, and print the result beside the design. A design that ships with
   neither the linter's output nor a printed check is not finished.

Every generated artifact carries the system version in the head:

```html
<meta name="static-design" content="X.Y.Z">
```

Read the number from the plugin manifest at write time — never copy the literal from this
example. A version written into prose goes stale while the linter goes on failing a stale
stamp, so the artifact fails a check that has nothing to do with design.
