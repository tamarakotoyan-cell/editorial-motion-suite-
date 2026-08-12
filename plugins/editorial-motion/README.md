# editorial-motion

Seven skills that work as one system for animated, data-led design.

| Skill | Job |
|---|---|
| `layout-composition` | Grid, focal point, proportion, type scale. Runs first. |
| `motion-system` | Easing, timing, stagger, cutting the curve. Style-agnostic. |
| `analog-surface` | Surface / Ink / Life. Paper, ink-in-fibre, screens, grain. |
| `editorial-explainer` | Data-journalism structure, charts, persistent-mark animation. |
| `imagery-motion` | Photographic treatment — torn panels, duotone, selective colour. |
| `type-treatment` | Type against imagery — texture blending, layering registers, kinetic text. |
| `premium-product-motion` | The alternative look: lit objects, depth of field, camera. |

**Order:** layout → motion → analog-surface → a look skill. `editorial-explainer` and
`premium-product-motion` are alternatives, not companions. `imagery-motion` and
`type-treatment` are additive to either — imagery owns the picture, type owns
the words on it.

## Tooling

Stdlib-only Python and vanilla JS — nothing to install but Chrome and ffmpeg,
and only for the last two.

| Tool | Job |
|---|---|
| `analog-surface/assets/make-paper.py` | Seamless paper surfaces + companion ink mattes |
| `analog-surface/assets/make-grain.py` | Seamless grain plates, single or animated |
| `analog-surface/assets/check-artifact.py` | Lints generated HTML against the mechanically checkable house rules |
| `motion-system/assets/sfx.js` | Procedural sound design, muted by default |
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
seven skills load together and cite each other by relative path.

**As standalone skills**, for any surface that takes one skill at a time —
Claude Design among them. Relative cross-references dangle outside the bundle,
so run the builder from the repo root:

```
python3 build-skills.py
```

That writes `dist/<skill>/` and `dist/<skill>.zip` for each of the seven, with
the shared references (`sources.md`, `house-rules.md`) vendored into every
skill that cites them and every path rewritten to be skill-local. It fails
loudly if any referenced path does not resolve. `--check` validates without
writing.

Upload order still matters: `layout-composition`, then `motion-system`, then
`analog-surface` if the piece has any physical surface in it, then one look skill. Load `editorial-explainer` if you want the data-journalism
look, `premium-product-motion` if you want lit objects and camera moves — they
are alternatives, not companions. `imagery-motion` and `type-treatment` are additive to either.

The plugin is the single source of truth. `dist/` is generated — edit the
skills under `plugins/`, never the vendored copies.
