# editorial-motion

Ten skills that work as one system for animated, data-led design — a router
and the nine it dispatches to.

| Skill | Job |
|---|---|
| `editorial-motion` | The router. Load order, precedence, pre-delivery lint. Teaches no design. |
| `layout-composition` | Grid, focal point, proportion, type scale. Runs first. |
| `motion-system` | Easing, timing, stagger, cutting the curve. Style-agnostic. |
| `design-motion-sound` | Transitional and accent SFX: whooshes, hits, risers, interface cues and licensed comedy sounds. |
| `analog-surface` | Surface / Ink / Life. Paper, ink-in-fibre, screens, grain. |
| `editorial-explainer` | Data-journalism structure, charts, persistent-mark animation. |
| `imagery-motion` | Photographic treatment — torn panels, duotone, selective colour. |
| `type-treatment` | Type against imagery — texture blending, layering registers, kinetic text. |
| `premium-product-motion` | The alternative look: lit objects, depth of field, camera. |
| `format-adaptation` | Re-composes an approved piece for 16:9, 4:5, 1:1 and 9:16. Runs last. |

**Order:** layout → motion → sound when required → analog-surface → a look skill
→ format-adaptation when the piece ships to more than one aspect ratio.
`editorial-explainer` and
`premium-product-motion` are alternatives, not companions. `imagery-motion` and
`type-treatment` are additive to either — imagery owns the picture, type owns
the words on it.

That order, the precedence stack below and the pre-delivery lint step are
restated in `skills/editorial-motion/SKILL.md` — the router — because Claude
does not read plugin READMEs at runtime. This file is for people; the router is
the same content in the one place the model will actually see it. Change one
and change the other.

## Rule ownership

A rule with two homes has two futures. These areas each sit across more than one
skill, so each has **one owner**; everywhere else cites it rather than restating
it. If you are adding a rule, find its area here first.

| Rule area | Owner | Everyone else |
|---|---|---|
| House curve set, timing kit, stagger band, loop lengths | `motion-system/assets/motion.css` — the values, machine-readable | `motion-system` §Easing/§Duration and `house-rules.md` §House timing kit explain *which* to reach for and cite the file for *what* |
| One-ambient-one-accent ceiling, the accent/ambient move vocabulary | `house-rules.md` §The ceiling, §The signature accent move | `motion-system` §The ceiling points at it |
| Kinetic and animated type | `type-treatment` §Type in motion | `motion-system` §Entrance vocabulary owns general entrances and defers text to it; timing and easing still govern |
| Footage homogenisation — whether one shared treatment is required | `analog-surface` §5 | `imagery-motion` §Duotone owns the grading recipe, not the policy |
| Type scale ratios and the maths | `layout-composition` §Type scales | `editorial-explainer` and `type-treatment` cite it |
| Typographic roles in a data piece — display, body, utility, hero figure | `editorial-explainer` §Typography, as roles | `type-treatment` owns styling and layering against imagery, not role assignment |

Two of these were genuine duplicates with the values written out twice, and they
had already drifted: spring overshoot read "~4%" in one document and "~5%" in
the other. That is the argument for the table.

`check-artifact.py` keeps its own copy of the curve set, because it has to lint
artifacts with no plugin around it. CI asserts that copy still matches
`motion.css`, so the duplication cannot drift silently.

## Tooling

Stdlib-only Python and vanilla JS — nothing to install but Chrome and ffmpeg,
and only for the last two.

| Tool | Job |
|---|---|
| `analog-surface/assets/make-paper.py` | Seamless paper surfaces + companion ink mattes |
| `analog-surface/assets/make-grain.py` | Seamless grain plates, single or animated |
| `analog-surface/assets/check-artifact.py` | Lints generated HTML against the mechanically checkable house rules |
| `motion-system/assets/sfx.js` | Procedural sound design, muted by default |
| `design-motion-sound/scripts/mix_sfx.py` | Mix timecoded SFX cues into a video with ffmpeg |
| `motion-system/assets/render.py` | Renders an animated artifact to MP4 at 12fps |

Textures are generated rather than sourced because the stock libraries the
reference tutorials use forbid redistribution inside a plugin — and because at
the 5% strength the house style calls for, generated noise and a photographed
scan are indistinguishable. Hero sheets at full strength want a public-domain
scan instead.

Both `check-artifact.py --self-test` and `sfx-test.html` verify themselves; run
them after touching either.

**Precedence inside the system**
1. The client's brand — `skills/editorial-explainer/references/brand-integration.md`
2. The house ban list — `skills/editorial-explainer/references/house-rules.md`
3. The skill files

Frame-by-frame analysis of every reference — picture *and* sound — is in
`skills/motion-system/references/sources.md`, with the type-specific reference
set in `skills/type-treatment/references/sources.md`. Every rule traces back to
something observed there. Read §14 first if you are adding to it: it records
the provenance limits of the local reference set, and which of its conventions
are craft rather than borrowed format.

## Two ways to use it

**As a Claude Code plugin.** Install from the `emc-plugins` marketplace. The
ten skills load together and cite each other by relative path.

**As standalone skills**, for any surface that takes one skill at a time —
Claude Design among them. Relative cross-references dangle outside the bundle,
so run the builder from the repo root:

```
python3 build-skills.py
```

That writes `dist/<skill>/` and `dist/<skill>.zip` for each of the ten, with
the shared references (`sources.md`, `house-rules.md`) vendored into every
skill that cites them and every path rewritten to be skill-local. It fails
loudly if any referenced path does not resolve. `--check` validates without
writing.

Upload order still matters: `editorial-motion` first, then
`layout-composition`, then `motion-system`, then
`analog-surface` if the piece has any physical surface in it, then one look skill. Load `editorial-explainer` if you want the data-journalism
look, `premium-product-motion` if you want lit objects and camera moves — they
are alternatives, not companions. `imagery-motion` and `type-treatment` are additive to either.

The plugin is the single source of truth. `dist/` is generated — edit the
skills under `plugins/`, never the vendored copies.
