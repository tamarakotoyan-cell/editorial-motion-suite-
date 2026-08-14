---
name: storyboard-and-beat-sheet
description: Convert an editorial brief, script, research finding or approved copy into a timed beat sheet and renderer-neutral scene specification. Use when a motion project needs narrative beats, information-density control, screen copy, continuity, sound cues, accessibility alternatives and approval gates before animation is built.
---

# Write a storyboard and beat sheet

Plan meaning in time. Do not solve a weak argument with transitions or force spoken prose into simultaneous on-screen text.

## Inputs

- Read `production-contract.json` when present.
- Preserve the full supplied copy in the contract. Create a separate, concise `screen_copy` for each beat.
- Identify the claim, denominator, source, commissioner and CTA. Mark anything unverified.
- Inspect supplied imagery before assigning it to a beat.

## Workflow

1. State the communication job and one-sentence takeaway.
2. Divide the story by function: hook, context, proof, implication and source/ending. Omit functions the story does not need.
3. Assign start and end frames. Time each beat to its own reading load; do not use equal-duration slides.
4. Give each beat one focal point and one fact.
5. Carry at least one meaningful object across adjacent beats when comparison or causality benefits from continuity.
6. Specify entrance, hold, transition, exit and end state separately.
7. Spot sound after the silent sequence reads. Mark minor movement silent by default.
8. Write a reduced-motion alternative that preserves hierarchy and state change without relying on duration collapse.
9. Validate with `scripts/validate_storyboard.py`.

## Timing rules

- Keep the first complete proposition readable within the opening three seconds for short social video.
- Budget roughly 2.5 words per second for unvoiced display copy, then test at the actual size. Short labels may be faster; dense qualifiers need longer.
- Start transitions after the thought is legible, not on a fixed interval.
- Let exits run at roughly 60–70% of the matching entrance when an exit is visible.
- Use stagger to express order. Do not apply it to unrelated elements merely for ornament.
- Keep the designed dead tail under 0.8 seconds unless a deliberate CTA card needs a longer hold.

## Required beat fields

Read `references/storyboard-schema.md` for the full structure. Every beat must name:

- `id`, start/end frame and communication function;
- visible state before and after;
- screen copy and any narration;
- focal object, persistent objects and continuity action;
- motion register, path, distance, duration, stagger and hold;
- image treatment, data encoding and source line where relevant;
- sound role and sync frame;
- reduced-motion substitute;
- evidence/interpretation/recommendation notes and approval status.

## Decision rules

- Use a stat tile, countable marks or an annotated comparison for one headline number. Do not invent a chart with one value.
- Show the denominator for a percentage when the visual encoding implies a share.
- Keep the proof on screen long enough to count or compare.
- Keep source and sample information visible on research claims when supplied.
- Use a static end card only for source, credit, CTA or logo hand-off. If the final frame remains content, retain a quiet ambient move.

## Guardrails

- Do not imply that a commissioner conducted the research.
- Do not replace “opt-in” with “opt-out”; the policy meaning changes.
- Do not infer causality from a survey preference.
- Do not repeat distinctive reference trade dress. Describe functions, not creator styles.
- Keep the storyboard renderer-neutral. React component names belong in implementation notes, not the visual specification.
