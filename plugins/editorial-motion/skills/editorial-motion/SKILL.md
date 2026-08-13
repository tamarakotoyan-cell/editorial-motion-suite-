---
name: editorial-motion
description: Start here for any design, motion or visual request — this skill decides which of the editorial-motion skills to load and in what order. Use whenever the work is a chart, graph, data visualisation, infographic, stat tile, slide, deck, poster, social graphic, carousel, report visual, landing page, hero section, product mockup, UI showcase, title sequence, animation, video cut, or any generated HTML artifact whose job is to be looked at. Also use when a piece needs a vertical, square or social version, and when an existing artifact needs checking before it goes out. Dispatches and states precedence; teaches no design rules of its own.
---

# editorial-motion — start here

This skill routes. It decides **which skills to load, in what order, and what
overrides what**; every design decision lives in the skills it names. Load it
first, load what it names, then work.

## Load order

The order is not a preference. Each stage constrains the next, and a decision
made out of order gets made twice.

1. **layout-composition** — always, and first. Grid, focal point, proportion,
   type scale. Settled before anything is placed or styled.
2. **motion-system** — whenever the piece moves, and most pieces should. Easing,
   the two timing registers, stagger, exits, reduced motion.
3. **analog-surface** — whenever there is a physical surface in it: paper,
   documents, maps, screenshots, archival or stock imagery, or a flat colour
   fill that would read better as a ground.
4. **One look skill. Never both** — they are alternatives:
   - **editorial-explainer** when the job is to make a number or a finding
     land. Charts, data stories, report visuals, social data tiles.
   - **premium-product-motion** when the job is to make an object feel
     expensive. Product mockups, app UI showcases, feature reveals, titles.
5. **Additive to either, when the content calls for it:**
   - **imagery-motion** — there is a photo, screenshot, video, cutout or scan.
     Owns the picture.
   - **type-treatment** — text sits on a picture, texture or colour field, or
     the text itself animates. Owns the words on it.
6. **format-adaptation** — last, and only when the piece ships to more than one
   aspect ratio. It re-composes per format; it is not a way to crop a master.

A bare request — "make me a chart about housing affordability" — resolves to
layout-composition → motion-system → analog-surface → editorial-explainer.

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
<meta name="editorial-motion" content="1.6.0">
```

Take the number from the plugin manifest, `.claude-plugin/plugin.json`; if these
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
prefers-reduced-motion block, easing off the house set, sub-100ms travel.
**Errors are not advisory.** A warning may be left in, but only with a reason.

If the piece renders to video, render with the checker on — it refuses a
silently frozen clip rather than writing a plausible-looking file.
