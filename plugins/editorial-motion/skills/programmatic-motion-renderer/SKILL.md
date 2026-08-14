---
name: programmatic-motion-renderer
description: Implement an approved renderer-neutral storyboard as deterministic HTML, CSS and JavaScript video. Use when an agent must turn scene timing into code, create reusable editorial motion primitives, adapt one composition across aspect ratios, render previews or maintain frame-accurate continuity without a framework dependency or copied trade dress.
---

# Render programmatic editorial motion

Translate approved decisions into deterministic browser frames. Use the plugin's renderer as infrastructure; creative decisions remain in the storyboard and companion Editorial Motion skills.

## Preconditions

- Require a production contract and validated storyboard.
- Resolve missing assets, claim approvals and brand tokens before the full render.
- Read `references/html-renderer-contract.md` before implementing a new project.
- Use the companion Editorial Motion skills for visual judgement; this skill owns code, composition registration and rendering reliability.

## Implementation workflow

1. Convert beat boundaries to integer frames once. Never mix seconds and frames inside scene state.
2. Keep one source composition and select format and reduced-motion state through explicit URL parameters or project data.
3. Create format tokens for canvas, safe area, type scale, spacing and crop strategy.
4. Build the opening, densest proof frame and ending as inspectable still states.
5. Implement one representative transition and render it before scaling the system.
6. Keep persistent objects in the DOM across adjacent beats; transform their state rather than replacing them.
7. Use the renderer-controlled animation clock. Seed any noise or particle placement and never use wall-clock randomness.
8. Add sound after muted picture approval.
9. Lint the HTML, run the generated render preflight, render review timecodes, then render the full preview.

## Core implementation rules

- Use CSS animations, the Web Animations API or `requestAnimationFrame`; `render.py` pins all three to an exact timestamp.
- Derive bounded mappings from the controlled timestamp. Use overshoot only when it has a communication role.
- Clamp opacity and crop interpolation. A frame outside a beat must not leak pre- or post-roll content.
- Animate transform, opacity, filter, masks and SVG paths. Avoid per-frame layout mutation.
- Prefer one component that accepts state over several visually similar scene components.
- Cut at peak velocity only when both sides share direction and spatial logic.
- Keep one focal point at every frame, including during transitions.
- Use project-relative assets under `public/assets/`. Do not hotlink production media.
- Keep source data and display formatting separate. A displayed `71%` must originate from numeric `71`, not from duplicated strings.

## Reusable primitives

Maintain a small functional vocabulary:

- staged text reveal;
- image crop with slow deterministic push;
- focal dimming;
- countable percentage field;
- annotation draw-on;
- persistent anchor transition;
- format-aware end card.

Name primitives by communication job, not by a reference or visual trend.

## Reduced motion

Do not implement reduced motion as a universal near-zero duration. Provide an alternative composition that:

- presents the same information in the same order;
- replaces long travel, parallax and velocity cuts with direct state changes or short dissolves;
- preserves meaningful accumulation and comparison through static composition;
- contains no flashes or rapid alternating contrast.

## Guardrails

- Do not add a framework or package dependency without an explicit project need and approval.
- Keep the default runtime to local HTML, CSS, JavaScript, Python, Chrome and ffmpeg; there is no third-party video-framework licence dependency.
- Do not suppress renderer errors to obtain a file.
- Do not substitute an unlicensed font silently.
- Do not encode brand identity inside generic primitives.
- Do not start a long full-resolution render before representative frames and one transition pass review.
