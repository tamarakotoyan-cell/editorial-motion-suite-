# static-design

Composition, type and imagery craft for **static** design — social tiles, carousels, chart
cards, quote cards, event posters, report visuals. The fixed-canvas counterpart to
`editorial-motion`.

If the piece animates, use `editorial-motion`. If it exports as a PNG or JPG, use this.

## The system

| Skill | Owns |
|---|---|
| `static-design` | Routing, precedence, the version stamp, the lint gate |
| `static-composition` | Where content sits, how much of the frame it fills, ground and colour |
| `static-type-graphics` | The words and the pictures |
| `static-series` | Carousels and post sets |

Load order: `layout-composition` (from `editorial-motion`, when installed) →
`static-composition` → `static-type-graphics` → `static-series` (multi-frame only) →
`format-adaptation` (multi-ratio only).

Both plugins install together cleanly. They share `layout-composition` and
`format-adaptation` and do not otherwise overlap. `static-composition` carries a compact
substitute so this plugin also works alone.

## Precedence

1. The client's brand — colour and typeface come from them.
2. `skills/static-design/references/house-rules-static.md` — the A–M ban list.
3. The skill files, in load order.

## Source of truth

The principle files and the annotated example library are the master, and they live outside
this repo:

```
Pilots/Static design content/static-design-system/
```

`sync-static-design.py` vendors them into the skills' `references/` folders with a
"Vendored copy" header. **Do not edit anything under `references/` directly** — edit the
master and re-run:

```
python3 sync-static-design.py          # vendor + validate
python3 sync-static-design.py --check  # validate only, no writes
```

The master folder doubles as a Claude Design design system: `brand.md` plus `principles/`
as context, `examples/good/` and `examples/bad/` as the example sets, each with an
`annotations.md` that explains what the images are showing.

## Bumping a version

1. Bump `.claude-plugin/plugin.json` **and** add a matching entry at the top of
   `CHANGELOG.md`. CI fails the build if they disagree — that version is what every
   generated artifact gets stamped with.
2. Re-run `sync-static-design.py --check`.
3. Commit and push. Installs update with `/plugin update static-design@emc-plugins`.

## Linting

```
python3 skills/static-design/assets/check-static.py artifact.html
python3 skills/static-design/assets/check-static.py --set out/     # a whole carousel
```

Errors are not advisory. `--set` is required for a carousel: the template-sameness check
cannot run on one frame.
