# Changelog — editorial-motion

Versions the plugin, not the repo. The newest heading here and the `version`
field in `.claude-plugin/plugin.json` must agree; CI fails the build if they do
not, and generated artifacts carry the same number in a
`<meta name="editorial-motion">` stamp.

Newest first. Dates are the release date, ISO.

---

## 1.13.0

House rule, from client feedback on an Essential Report piece: the small
letter-spaced caps used for legend keys and stat-tile captions read as another
product's interface chrome rather than as a newsroom graphic — specifically,
it is the label register several AI assistants use for their own UI, so on
client work it mis-attributes the piece to the tool that made it.

- **house-rules** — new 🔒 ban: data labels, legend keys, axis labels, chip
  text, table column heads, eyebrows and stat-tile captions are sentence case.
  Separate a label from body copy with size, weight and the muted neutral.
- **editorial-explainer** — the Utility type role no longer prescribes
  uppercase; it prescribes sentence case. The carve-out that previously
  exempted axis labels, chip text and table column heads from the overline ban
  is withdrawn — it was the loophole the banned register lived in. Two
  "small caps label beneath" references reworded.
- **essential-tokens** — the no-uppercase-kickers line now covers labels in
  any slot, not only above a headline.
- **check-artifact.py** — new `sentence-case-labels` error, scoped to
  `text-transform: uppercase` in a block with *positive* tracking, plus
  `small-caps` unconditionally. Caps set large with negative tracking is a
  poster or stamp treatment that type-treatment owns and is left alone.
  Self-test extended to 16 checks.
- Worked examples in analog-surface, type-treatment, format-adaptation and the
  sfx test harness de-capped, so no example demonstrates the banned register.

## 1.12.0

Follows static-design 0.6.0, which adds the third picture structure (layered
editorial, Structure C) and scripts the raster pipeline. Kept in step so the
two systems route imagery the same way.

- **imagery-motion** — the duotone recipe now points at the static-design
  plugin's `halftone.py` for a repeatable pre-render treatment (harden alpha →
  contrast window → duotone with the lightest-pixel test → halftone), and
  states the A/B/C routing in one line: one photograph is A, one cut subject
  with a glyph vocabulary is C, roughly ten cutouts is B, and two to seven is
  the pinboard. The static linter now fails the pinboard; this plugin's does
  not, and the note says so.

## 1.11.0

Follows static-design 0.4.0, which settled four thresholds this plugin also
states. Kept in step so the two systems cannot disagree about a number.

- **layout-composition** — the text floor is **1.25% of canvas height** (~17px
  on a feed tile, ~14px on a slide), down from 1.6%/22px. Every reference
  caption sits between 12 and 17px, so the old floor stood above the set it was
  drawn from, and it collapsed utility and support into a single small size.
- **editorial-explainer** — the hero figure runs **1.2-2x the display**, down
  from 1.5x. The reference tiles run about 1.1x and read stronger: air and
  texture make a figure dominate, not point size.
- **house-rules** — the text floor restated to match.
- **The vendored worked example** rebuilt on a Major Third from base 17. Clean
  under `check-static.py` and `check-artifact.py`.

### From the 2026-08-17 system audit

An audit of this plugin against the Essential Design System found the guardrail
*content* sound and its *distribution* not: partly-divergent copies of the same
rules, the strongest linter in a plugin that was not enabled, and two reference
files instructing work the linter fails.

#### Contradictions — these were costing regenerations
- **`essential-tokens.md` no longer carries values.** It stated the ground as
  `--surface-page: #FFFFFF` where the token file defines `#fbf7f5` and the
  linter fails a pure-white ground at *error* severity — three sources, three
  answers, on the most frequent decision in the system. The file is now the
  judgement layer only; every number is read from `tokens/*.css`.
- **Cyan resolved.** The same file banned cyan as the second colour in a
  diverging chart; the design system ships a cyan–orange diverging ramp as
  canon, with stated reasoning. Settled in favour of the design system — a data
  hue inside charts, Research-only in brand furniture. Logged in
  `decisions.md`.
- **The dot-pattern field** now uses the official `assets/dot-pattern.png`
  where the design system is present, instead of instructing a generated
  lookalike beside it.
- **The E. symbol** is documented as the default mark and corner anchor; the
  file had listed only the wordmarks.
- **The attribution exemplar** in `check-artifact.py` is rewritten as labelled
  lines. It had been a mid-dot chain — the pattern `house-rules.md` bans two
  sections earlier.

#### Enforcement
- **`check-artifact.py --profile`** (`research` / `editorial` / `product` /
  `static`). A missing source and sample-size line is an **error** under
  research and editorial, and stays a warning by default because the checker
  cannot tell a survey finding from a product mockup from the HTML alone.
  Promotion runs after suppression, so an explicit `check-artifact-ignore`
  still wins.
- **`check-artifact.py --rules` / `--rules-json`** print every rule and the
  severity it actually fires at, derived from the known-bad fixture rather than
  a hand-kept table. This is the source for the 🔒 marks in the prose.
- **The 🔒 marks were wrong and are corrected.** One sat on decorative
  background gradients, which the linter never implemented; two sat on
  `source-line` and `stagger-band`, which only warn. Warnings now carry 🔓, and
  the grounds, reduced-motion and version-stamp rules — real errors that
  carried no mark — now carry 🔒. CI fails if the marks exceed what the linter
  can enforce.
- **`build-skills.py --restamp-examples`** points every shipped example's stamp
  at the manifest. All four were stamped 1.9.0 against a 1.11.0 manifest, so
  the CI step that lints them was failing on a rule with nothing to do with
  design. Run it as part of a version bump.

#### New — the shared core
- **`references/accessibility.md`.** The audit found accessibility ranked
  second of six in the precedence order with no source, no component contract
  and no check, while every other layer had all three. Contrast floors, focus,
  keyboard, motion, alt text, and a table of what is enforced versus what is
  human review. Records the one known failure: `--text-muted` does not clear
  4.5:1 on paper, and the source line is specified as muted.
- **`references/decisions.md`.** A dated decision log, so a resolved question
  stops looking like a live one. Carries the settled items above and the open
  ones with named owners.
- Both are vendored by `build-skills.py` into every skill that cites them.

#### Precedence
- **The router states one chain, six levels**, with accessibility at two and
  documented decisions at three. A second, shorter chain had been stated
  elsewhere.
- **The version stamp example no longer carries a literal number.** It showed
  `1.8.0` against a 1.11.0 manifest and a 1.9.0 install, while the linter
  failed a stale stamp as an error. CI now rejects a hard-coded version there.
- **`house-rules.md` declares itself the only copy.** A second copy in the
  design system project had drifted in both directions, each carrying rules the
  other lacked — the exact failure the file's own timing-kit section describes.

#### Evals
- **Cost is reported** — turns, tool calls, input and output tokens and cost
  per brief, with a totals row. Trimming context is a trade, and a shorter
  instruction that costs more turns is not a saving; the two numbers print
  together so the result cannot be read one-sided.
- **Briefs carry a `profile`**, passed through to the linter.
- **New brief `product-ui-states`** — a settings screen with populated, empty,
  loading, error and disabled states, and keyboard requirements. The set had
  nothing exercising components, interaction states or accessibility, which
  were the least-covered layers.

---

## 1.10.0

Derived from a seven-round rebuild of one Essential data tile. Every entry below
fixed something a round had to catch by hand.

### Corrected
- **`editorial-explainer` — the mark-equals-number snippet was wrong for grouped
  marks.** `calc(var(--v) * 1%)` resolves against the parent, so sub-segments
  inside a group render at about a third of their true length: plausible,
  invisible in review, and caught twice on the same chart. Replaced with the
  flex-grow idiom, which is correct by construction.
- **`editorial-explainer` — the DL 25 rule is unsatisfiable for three fills plus
  an accent, and read as achievable.** The arithmetic is now stated, with the
  three sanctioned resolutions and the requirement to write the measured L*
  values into the file.

### Added
- **`layout-composition`** — the 60% occupancy floor, the three fixes for a
  frame the content cannot fill, and the per-format copy budget. On a
  feed-scale canvas the question line *is* the supporting line; a deck as well
  is one layer too many.
- **`layout-composition`** — the type-scale guardrail restated as a floor: no
  text below 1.6% of canvas height. Phrased as a caveat it was read as optional.
- **`editorial-explainer`** — the hero figure runs 1.5-2x the display size. The
  single change that most improved the reference tile.
- **`editorial-explainer`** — direct labelling as a *mechanism*: label inside
  the mark, or run a hairline leader to it. Plus the ban on a value-label list
  under a chart, which is a legend wearing a disguise.
- **`editorial-explainer`** — the span rule and the callout chip as annotation
  devices, alongside the hand-drawn circle.
- **`analog-surface`** — ink on stock for type you set yourself: the
  displacement band (about size/37), the rule that it applies to hero figures
  too, and the caveat that live SVG filters do not survive an Express import.
- **`house-rules.md`** — a typographic section carrying the mid-dot chain ban
  and the text-size floor. The mid-dot rule was previously only in the static
  system, which claimed this one enforced it.
- **`essential-tokens.md`** — branding weight by format (a social tile gets the
  accent dot and nothing else), the report name appears once, and combined
  categories carry a footnote.
- **`editorial-explainer/assets/example-social-tile.html`** — a worked 4:5 tile,
  clean under both linters, with the colour arithmetic and the deliberate
  ratio break commented in place.

## 1.9.0 — 2026-08-14

Reference analysis of a fifth Vox-style author (`sources.md` §16 — Nuclear
Motion, "How to Design Infographics in the Vox Style", measured rather than
read off captions). It corroborated the surface and timing findings and exposed
one hole the pack had never closed: **nothing required a chart's marks to match
its numbers.**

**Added**

- **`editorial-explainer` → "The mark must equal the number".** Length ÷ value
  constant across the series; geometry computed from the datum. Two corollaries:
  no axis without a scale, and a value label is not a substitute for a correct
  mark. Backed by measurement — the reference ships a bar chart whose 85% bar is
  the *shortest on the chart*, and a finished build running at 8.4, 9.2 and 11.0
  px per percent. Both look plausible; neither is catchable by a reader.
  New *Before shipping* check 4 makes it a gate.
- **A contrast-ratio floor for text roles**, alongside the existing ΔL rule for
  marks. The two measure different things: the same reference's source line
  passes ΔL at 30.7 and is unreadable at 2.48:1. ΔL asks whether two things are
  separable; it never asked whether text could be read.
- **Horizontal bars** in the *Charts must move* table, plus the texture-stretch
  trap — `scaleX` on a bar carrying grain or halftone starts the texture
  compressed and relaxes it over the entrance. Reveal with `clip-path` instead.
  The reference does this wrong in the way that is easiest to copy.
- **`analog-surface` → "Broken grid".** A grid masked with the paper's own grain
  tile, so rules fragment where the fibre didn't take ink. The strongest surface
  move in the new reference.
- **`--step-*` tokens in `motion.css`** — the 12fps clock as six named tokens
  instead of per-animation arithmetic. `steps(n)` at duration × 12 is the sum
  everyone gets wrong once, and a mismatched count reads as a bug.
- ***Reveal short, hold long*** in `motion-system`. Measured: a three-bar chart
  resolves in ~2.1s then holds ~3.9s inside a 6.04s loop — 1:2 motion-to-hold,
  landing on `--loop-tile`. A loop animating more than half its length never
  gives the reader the still frame the piece is judged on.

**Changed**

- **The dashed-gridline ban now names its exception.** The ban is on the dash
  *convention* — `stroke-dasharray` is a chart signal that means something. A
  solid hairline eroded by the surface treatment is not a dashed line and is
  encouraged. Previously the rule read literally enough to forbid the best thing
  in the reference material.
- **Stepped time is a property of the piece, not of one element.** The recipe
  applies it over the whole composition; stepping ambient drift while entrances
  stay interpolated runs two clocks at once and reads as bolted on.
- `sources.md` §16 records the new reference, including its failures. The set is
  practitioners demonstrating a *look* — this entry is the clearest evidence
  that look-fidelity and data integrity come apart, and future readers should
  not treat the set as trustworthy on charts.

**Not changed**

- The Vox trade-dress ban. Sampled `#F2F649` lemon highlighter, blue bars,
  high-contrast display serif — exactly what the ban already names. Correctly
  calibrated, left alone.

## 1.8.0 — 2026-08-13

`render.py` rebuilt on the DevTools protocol. Framed as reliability rather than
video quality: it was the component most likely to produce a wrong artefact
without saying so.

**Fixed**

- **Canvas, WebGL and `requestAnimationFrame` artifacts rendered wrong and
  passed the check.** Only the Web Animations timeline was being frozen, so
  anything on rAF was invisible to it. Advancing Chrome's virtual time is not
  sufficient either: it services rAF on its own cadence, and in headless — where
  frames are produced on demand rather than on a display refresh — that cadence
  does not track the budget. Measured on a canvas drawing its own elapsed time,
  a 2-second seek left the page at 1.12s: 54% speed, machine-dependent, and
  moving enough to satisfy a does-it-move check. `render.py` now installs a
  clock shim before page scripts run, so rAF is a queue drained at an exact
  timestamp and `performance.now()` agrees with it. The same canvas now lands on
  2.000s at every seek, identically on every run.
- A stalled protocol read hung the render indefinitely instead of timing out —
  the deadline could never be reached from inside a blocking read.

**Changed**

- **One Chrome for the whole render, over `--remote-debugging-pipe`.** It was one
  process per frame: 60 launches for a 5-second clip. A 5s clip now renders in
  about 7 seconds rather than about a minute. The pipe transport rather than a
  debugging port because there is no websocket client in the stdlib, no port to
  allocate and no race with Chrome's startup.
- **Sound is muxed.** `sfx.js` synthesises in the browser and never sounds in a
  headless render, so cues are logged whether or not they play, each voice is
  rendered offline to a WAV, and `design-motion-sound`'s `mix_sfx.py` places
  them. Levels stay in `sfx.js`, placement stays in the mixer, and `render.py`
  does not reimplement either. `--no-audio` skips the pass.
- Canvas size is set with a device-metrics override, so a piece narrower than
  500px renders at the size asked for. Headless Chrome silently widened the
  window before, producing the artifact at the wrong breakpoint.
- Chrome's stderr is discarded; none of it was actionable and all of it buried
  the render's own output.

## 1.7.0 — 2026-08-13

**Added**

- **`design-motion-sound`**, a focused SFX skill for transitional and accent
  sound. It creates cue cards for whooshes and swishes, impacts and hits, risers
  and uplifters, interface cues, and licensed meme-inspired or cartoon-style
  sounds; it also covers lawful sourcing, rights logging, frame-aware sync,
  mixing and playback checks.
- **A deterministic ffmpeg mixer**, `design-motion-sound/scripts/mix_sfx.py`,
  with a documented JSON cue schema.

**Changed**

- Sound generation is explicitly limited to short SFX. Voiceover generation,
  music composition and general audio beds are out of scope; supplied dialogue
  and music are preserved as mix constraints.

**Fixed**

- Silent input videos now retain their full duration when the final SFX cue
  finishes before the picture.

## 1.6.0 — 2026-08-13

Engineering rigour, not craft. No design rule changed in this release.

**Added**

- **A router skill**, `skills/editorial-motion/`. The load order, the
  precedence stack and the pre-delivery lint step were documented only in the
  plugin README, which Claude does not read at runtime. Each skill stated its
  own precedence, which took effect only if that skill happened to load first.
  The router dispatches — it teaches no design — and it is the only skill whose
  description triggers on any design, motion, chart, slide, tile or visual
  request.
- **Version stamping.** Every generated artifact must carry
  `<meta name="editorial-motion" content="X.Y.Z">`. `check-artifact.py` errors
  when it is absent, malformed, or does not match the plugin manifest, which it
  finds by walking up for `.claude-plugin/plugin.json`. `--version-stamp`
  overrides. In a standalone bundle, with no manifest above the script, the
  stamp is still required but its value is not matched.
- **This changelog**, and a CI step asserting it agrees with `plugin.json`.
- Four shipped `example.html` boards now carry the stamp.
- **A golden brief set** — `evals/briefs.json` and `evals/run-evals.py`. Six
  briefs covering the real work: a stat tile, a multi-panel explainer, a 9:16
  social cut, a report visual, a product mockup, and a chart whose finding is a
  single number. One command checks router-first, load order, exclusivity,
  artifact produced and `check-artifact.py --strict` per brief, and writes a
  rubric for the three-question check. Nothing tested the skills before this.
- **Four rules moved from prose into the linter**, each with a self-test case:
  banned titles, `tabular-nums` on a hero figure, stagger outside the house
  band, and a missing source and sample-size line. The prose they replace is
  deleted; ban-list entries that are machine-enforced are marked 🔒.
- **Loop-length tokens** in `motion.css` — `--loop-line`, `--loop-tile`,
  `--loop-max`.

**Fixed**

- The house timing kit and the one-ambient-one-accent ceiling were each written
  out in two documents, and had drifted: spring overshoot read "~4%" in
  `house-rules.md` and "~5%" in `motion-system`. `motion.css` now owns the
  numbers and both documents cite it. An ownership table in the plugin README
  gives every cross-skill rule area one owner.

**Changed**

- **`render.py` runs its frozen-clip check by default.** It was opt-in, which
  made the guard against the one failure mode invisible in a file listing
  itself opt-in; "always render with `--check`" was prose, and prose is skipped
  under load. `--no-check` opts out for a deliberately static piece. `--check`
  is still accepted, does nothing, and says so.
- `build-skills.py` builds the router alongside the eight, knows how to rewrite
  a citation of `check-artifact.py` for standalone bundles, and carries
  `motion.css` into any bundle that vendors `house-rules.md` — which now names
  the timing tokens without restating their values.
- CI additionally gates the eval set's well-formedness and asserts the linter's
  copy of the house curve set still matches `motion.css`.

## 1.5.0 — 2026-08-12

**Added**

- **`format-adaptation`**, the eighth skill. Re-composes one approved motion
  system for 16:9, 4:5, 1:1 and 9:16 rather than scaling a master into them:
  invariant tokens and choreography against re-derived layout, an element
  budget per format, the space-for-time trade in vertical, platform safe areas
  with a `data-debug="safe"` overlay, the nested-crop rule for feed previews,
  and container-query travel units so macro-distances re-derive per stage.
- An example board that proves the contract mechanically — the inner DOM block
  is byte-identical across all four stages, and only CSS recomposes.
- `render.py` gains the missing 4:5 preset (`portrait`, 1080×1350).

## 1.4.0 — 2026-08-12

First published release, as the `emc-plugins` marketplace.

**Added**

- Seven skills for animated, data-led design: `layout-composition`,
  `motion-system`, `analog-surface`, `editorial-explainer`, `imagery-motion`,
  `type-treatment`, `premium-product-motion`.
- Tooling: seamless texture generators (`make-paper.py`, `make-grain.py`), an
  artifact linter with a self-test (`check-artifact.py`), procedural sound
  design (`sfx.js`), and a deterministic HTML→MP4 renderer (`render.py`).
- `build-skills.py`, moved into the repo from the parent folder, with `SRC` and
  `DIST` adjusted so build output stays outside the marketplace tree.
