---
name: editorial-motion
description: Start here for any editorial design, motion, sound-design or visual production request — this skill decides which editorial-motion skills to load and in what order. Use for motion briefs, production contracts, storyboards, beat sheets, programmatic video, delivery QA, charts, data visualisations, infographics, stat tiles, slides, decks, posters, social graphics, report visuals, landing pages, product mockups, UI showcases, title sequences, animations, video cuts, SFX plans, cue sheets, generated HTML artifacts, format adaptation or final checks. Dispatches and states precedence; teaches no design rules of its own.
---

# editorial-motion — start here

This skill routes. It decides **which skills to load, in what order, and what
overrides what**; every design decision lives in the skills it names. Load it
first, load what it names, then work.

## Load order

The order is not a preference. Each stage constrains the next, and a decision
made out of order gets made twice. Skip production stages only when their
approved outputs already exist.

1. **motion-project-scaffold** — first for a new motion job. Captures the
   production contract, claims, assets, formats and review gates.
2. **storyboard-and-beat-sheet** — before visual implementation when timing or
   narrative is not already approved. Produces the renderer-neutral beat plan.
3. **layout-composition** — always before visual implementation. Grid, focal point, proportion,
   type scale. Settled before anything is placed or styled.
4. **motion-system** — whenever the piece moves, and most pieces should. Easing,
   the two timing registers, stagger, exits, reduced motion.
5. **design-motion-sound** — after choreography is settled, whenever the piece
   needs transitional or accent SFX. Whooshes and swishes, impacts and hits,
   risers and uplifters, interface cues and licensed comedy sounds.
6. **analog-surface** — whenever there is a physical surface in it: paper,
   documents, maps, screenshots, archival or stock imagery, or a flat colour
   fill that would read better as a ground.
7. **One look skill. Never both** — they are alternatives:
   - **editorial-explainer** when the job is to make a number or a finding
     land. Charts, data stories, report visuals, social data tiles.
   - **premium-product-motion** when the job is to make an object feel
     expensive. Product mockups, app UI showcases, feature reveals, titles.
8. **Additive to either, when the content calls for it:**
   - **imagery-motion** — there is a photo, screenshot, video, cutout or scan.
     Owns the picture.
   - **type-treatment** — text sits on a picture, texture or colour field, or
     the text itself animates. Owns the words on it.
9. **format-adaptation** — after the master is approved, when the piece ships to
   more than one aspect ratio. It re-composes per format; it is not a way to crop a master.
10. **programmatic-motion-renderer** — after the storyboard and visual system
    are approved. Implements deterministic HTML, CSS and JavaScript frames.
11. **render-and-delivery-qa** — after preview and again after final render.
    Verifies the technical file, communication, accessibility and handoff.

A bare design request — "make me a chart about housing affordability" — resolves
to layout-composition → motion-system → analog-surface → editorial-explainer.
A new video brief resolves to scaffold → storyboard → the design route →
programmatic renderer → delivery QA.

## Precedence

Where two sources disagree, the higher one wins:

1. **The client's brand.** Colour and typeface come from them. Work is produced
   for many clients; Essential is simply the case where the client is Essential.
2. **The house ban list** — `../editorial-explainer/references/house-rules.md`.
   It overrides every style skill, including the reference material they cite.
3. **The skill files**, in the load order above.

## Stamp the output

Every generated artifact carries the version of the system that made it, in the
head:

```html
<meta name="editorial-motion" content="1.10.1">
```

Take the base number from either plugin manifest; if these
skills were installed one at a time and there is no manifest, use the version
they were published under. Without a stamp an output cannot be attributed to a
version, and no change to these skills can be shown to have helped or hurt. The
linter treats a missing, malformed or stale stamp as an error.

## Before delivering

Lint the generated HTML with `../analog-surface/assets/check-artifact.py` and
fix what it reports. This is a required step, not a suggestion:

```
python3 check-artifact.py artifact.html
```

It catches the mechanical failures prose gets wrong under load — pure white or
black grounds, imagery outside a homogenise wrapper, a missing
prefers-reduced-motion block, easing off the house set, sub-100ms travel, a
banned title, `tabular-nums` on a hero figure, stagger outside the house band, a
missing source and sample-size line. **Errors are not advisory.** A warning may
be left in, but only with a reason.

If the piece renders to video, use the programmatic renderer and finish with
render-and-delivery-qa. The default frozen-frame check refuses a silently frozen
clip rather than writing a plausible-looking file.
