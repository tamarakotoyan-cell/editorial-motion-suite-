# Editorial motion pack

| Plugin | What |
|---|---|
| `editorial-motion` | A router plus thirteen skills for planning, designing, rendering and verifying animated, data-led work. Includes a dependency-free HTML→MP4 production path. |

## Install in Claude Code

```
/plugin marketplace add tamarakotoyan-cell/editorial-motion-suite-
/plugin install editorial-motion@emc-plugins
```

## Install in Codex

Clone this repository, then register its root as a local marketplace:

```
codex plugin marketplace add /path/to/emc-plugins
codex plugin install editorial-motion@emc-plugins
```

Both hosts load the same `plugins/editorial-motion/skills/` source. Editorial
Motion does not require Remotion or a Node package install.

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
2. Bump the base version in both plugin manifests
   **and add a matching entry at the top of
   `plugins/editorial-motion/CHANGELOG.md`.** CI fails the build if the two
   disagree, because that version is what every generated artifact gets stamped
   with.
3. Run `python3 scripts/validate_cross_host.py`, commit and push. Claude installs update with
   `/plugin update editorial-motion@emc-plugins`.
