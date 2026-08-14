# Foundation 0.1 release contract

Foundation 0.1 is the programme milestone. The reference-analysis release already occupies 1.9.0, so the distributable Foundation release is version 1.10.0 rather than resetting or reusing semantic version history.

## Outcome

One canonical Editorial Motion plugin must work in Codex and Claude, and must produce deterministic video without Remotion or another video-framework dependency.

## Canonical source

```text
plugins/editorial-motion/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
└── skills/
```

The `skills/` directory is shared. Host-specific manifests and optional `agents/openai.yaml` interface metadata may describe that source, but must not fork its instructions or assets.

## Included in Foundation 0.1

1. Consolidate the ten creative skills and four production skills under the canonical plugin.
2. Replace the Remotion starter and implementation guidance with local HTML, CSS and JavaScript rendered by `motion-system/assets/render.py`.
3. Package the same skill source for Codex and Claude, with automated checks for manifest version agreement and portable skill frontmatter.

## Runtime boundary

| Capability | Foundation 0.1 implementation |
|---|---|
| Planning and contracts | JSON plus Markdown skill guidance |
| Composition | Local HTML, CSS and JavaScript |
| Browser rendering | Chrome DevTools Protocol through stdlib Python |
| Encoding and media inspection | ffmpeg and ffprobe |
| Optional SFX | Local JavaScript synthesis and ffmpeg mixing |
| Package manager | None required |
| Hosted render service | None required |

Chrome and ffmpeg are delivery tools, not framework dependencies. Generated source remains editable and can be rendered locally.

## Compatibility contract

- Every `SKILL.md` uses only `name` and `description` frontmatter.
- Skill names match their directories.
- Both manifests expose the same plugin name and base semantic version.
- Codex cachebuster metadata may be appended during local installation without changing the shared release version.
- Claude and Codex discover the same `skills/` tree.
- Host-specific UI metadata remains optional and does not contain workflow rules.

## Acceptance checks

- `python3 scripts/validate_cross_host.py`
- `python3 build-skills.py --check`
- every skill passes `quick_validate.py`
- the Codex plugin passes `validate_plugin.py`
- the scaffold creates a new project non-destructively and its render preflight passes
- after one browser warm-up, `python3 scripts/test_render_determinism.py` produces
  two visually equivalent H.264 renders with the expected frame schedule,
  dimensions, frame rate, frame count and duration; every corresponding frame
  pair clears 45dB PSNR
- the storyboard validator accepts a valid beat sheet and rejects invalid timing
- the existing linter, eval dry-run and render regression checks remain green

## Explicit non-goals

- Running Remotion alongside Editorial Motion.
- Recreating Remotion's React component API, cloud rendering or editor UI.
- Migrating historical proof projects in this release; they remain examples outside the shipped plugin.
- Adding a hosted service, billing layer, proprietary project format or broad dependency graph.
