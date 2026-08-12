# emc-plugins

Essential Media's Claude Code plugin marketplace.

| Plugin | What |
|---|---|
| `editorial-motion` | Eight skills for animated, data-led design — layout, motion, analog surface treatment, data-journalism structure, imagery, type, product motion, multi-format adaptation. Plus the tooling: texture generators, an artifact linter, procedural sound, and an HTML→MP4 renderer. |

## Install

```
/plugin marketplace add tamarakotoyan-cell/emc-plugins
/plugin install editorial-motion@emc-plugins
```

## Maintain

Skills live under `plugins/editorial-motion/skills/` — see the plugin's own
README for the system, precedence and build instructions. `build-skills.py`
generates standalone per-skill zips into `../editorial-motion-dist/`
(deliberately outside this tree) for surfaces that take one skill at a time.

After editing, bump the version in
`plugins/editorial-motion/.claude-plugin/plugin.json`, commit, push — installs
update with `/plugin update editorial-motion@emc-plugins`.
