# Changelog — editorial-motion

Versions the plugin, not the repo. The newest heading here and the base `version`
in both host manifests must agree; CI fails the build if they do not, and generated artifacts carry the same number in a
`<meta name="editorial-motion">` stamp.

Newest first. Dates are the release date, ISO.

---

## 1.10.0 — 2026-08-14

Foundation 0.1: one standalone production system for Codex and Claude.

**Added**

- A house rule and linter check banning mid-dot-separated footnotes and metadata
  chains such as `Source · Date · Sample`.
- Four production skills for project scaffolding, storyboard and beat planning,
  deterministic implementation, and delivery QA.
- A Codex plugin manifest and repo-local Codex marketplace beside the existing
  Claude packaging. Both hosts discover the same skill source.
- A dependency-free HTML/CSS/JavaScript starter, format-aware render command and
  cross-host release validator.
- An end-to-end CI regression that renders the starter twice through Chrome and
  ffmpeg, verifies the encoded media and frame schedule, and rejects any decoded
  frame pair below 45dB PSNR.

**Changed**

- The router now covers the full production sequence from contract through QA.
- Generated projects copy the existing deterministic Chrome/ffmpeg runtime and
  require no package installation.
- Version stamping and CI accept both host manifests while enforcing one shared
  base version and portable skill frontmatter.

**Fixed**

- The shipped format-adaptation example now follows the mid-dot metadata rule it
  is used to demonstrate and passes the artifact linter.

**Removed**

- The Remotion starter, React implementation guidance and Remotion-specific
  project checker from the shipped workflow.

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
