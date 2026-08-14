---
name: motion-project-scaffold
description: Create a safe, renderer-ready project foundation for editorial videos, social motion, data stories and branded explainers. Use when an agent must turn a motion brief into a consistent folder structure, production contract, asset and rights manifest, delivery variants and a dependency-free HTML motion starter before storyboarding or implementation.
---

# Scaffold a motion project

Create the production boundary before creative implementation. Keep claims, brand inputs, assets, delivery formats and approval status explicit so later skills do not invent or silently change them.

## Workflow

1. Write the production contract using `references/project-contract.md`.
2. Resolve only missing decisions that materially change the output. Otherwise state assumptions.
3. Keep `storyboard.json` renderer-neutral. The default implementation target is the plugin's deterministic HTML renderer.
4. Create the project with `scripts/create_motion_project.py` or copy `assets/html-starter/` when a custom setup is required.
5. Put working assets in `public/assets/`. Preserve originals outside generated derivatives.
6. Record provenance, rights and permitted use in `assets.json` before rendering.
7. Run `python3 scripts/render_project.py --dry-run` in the generated project. Stop on unresolved claims, missing assets or incompatible dimensions.

## Production contract requirements

- Purpose, audience and single takeaway.
- Exact supplied copy and a separate approved screen-copy field.
- Claim source and approval status. Never mark a user-supplied statistic as verified without the underlying source.
- Duration, frame rate, dimensions, platform, sound assumption and delivery codecs.
- Brand source, approved logo, fonts, colour roles and forbidden uses.
- Asset path, creator/source, licence, alteration permission and expiry where relevant.
- Required outputs, including caption-safe and reduced-motion variants.
- Review gates for story, claims, brand, accessibility and final delivery.

## Default output structure

```text
project/
├── production-contract.json
├── storyboard.json
├── assets.json
├── src/
├── scripts/render_project.py
├── tools/
├── public/assets/
├── renders/
└── qa/
```

Do not create format-specific copies of creative source. One composition should accept a format key and recompute its layout from safe-area and aspect-ratio tokens.

## Guardrails

- Do not overwrite an existing project unless the user explicitly approves it.
- Do not upload private client assets to make them reachable by a renderer.
- Do not bake secrets or connector tokens into project files.
- Do not treat a brand-kit thumbnail as a production logo; obtain the approved asset.
- Preserve copy and data exactly in the contract, even when screen copy is shortened.
- Keep renderer choices downstream of the communication plan.

## Handoff

Report the project path, assumptions, unresolved approvals, renderer, format variants and the preflight command. The generated project requires no package install; Chrome and ffmpeg are required only when rendering video.
