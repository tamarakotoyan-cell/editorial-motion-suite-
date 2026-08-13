# emc-plugins

Essential Media's Claude Code plugin marketplace.

| Plugin | What |
|---|---|
| `editorial-motion` | A router plus eight skills for animated, data-led design — layout, motion, analog surface treatment, data-journalism structure, imagery, type, product motion, multi-format adaptation. Plus the tooling: texture generators, an artifact linter, procedural sound, and an HTML→MP4 renderer. |

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

### Bumping a version

1. Run the golden briefs and read the result. This is the only check that tests
   the *skills* rather than the paths or the linter:

   ```
   python3 evals/run-evals.py
   ```

   It prints pass/fail per brief for the mechanical checks — router first,
   correct load order, no excluded skill, artifact produced, linter clean under
   `--strict` — and writes `rubric.md` for the three-question check, which is
   the half no script can grade. It drives the plugin **in the working tree**,
   so it tests what you just edited. It needs an authenticated `claude` CLI and
   costs tokens; CI only validates that the set is well-formed.
2. Bump the version in `plugins/editorial-motion/.claude-plugin/plugin.json`
   **and add a matching entry at the top of
   `plugins/editorial-motion/CHANGELOG.md`.** CI fails the build if the two
   disagree, because that version is what every generated artifact gets stamped
   with.
3. Commit and push. Installs update with
   `/plugin update editorial-motion@emc-plugins`.
