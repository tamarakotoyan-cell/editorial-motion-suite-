# Changelog — editorial-motion

Versions the plugin, not the repo. The newest heading here and the `version`
field in `.claude-plugin/plugin.json` must agree; CI fails the build if they do
not, and generated artifacts carry the same number in a
`<meta name="editorial-motion">` stamp.

Newest first. Dates are the release date, ISO.

---

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

**Changed**

- **`render.py` runs its frozen-clip check by default.** It was opt-in, which
  made the guard against the one failure mode invisible in a file listing
  itself opt-in; "always render with `--check`" was prose, and prose is skipped
  under load. `--no-check` opts out for a deliberately static piece. `--check`
  is still accepted, does nothing, and says so.
- `build-skills.py` builds the router alongside the eight, and knows how to
  rewrite a citation of `check-artifact.py` for standalone bundles.

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
