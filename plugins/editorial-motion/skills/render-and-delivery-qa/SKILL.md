---
name: render-and-delivery-qa
description: Inspect motion previews and delivery masters for technical compliance, visual integrity, accessibility, claim accuracy and handoff completeness. Use when an agent must verify an MP4, WebM or image sequence, compare output against a production contract, sample critical frames, check duration and codec, find dead tails or clipping, and produce a client-review delivery report.
---

# Verify a motion delivery

Treat a successful render as evidence that frames were encoded, not that the piece is correct. Verify the communication, picture, motion, sound and package separately.

## Inputs

- Production contract and approved storyboard.
- Preview or delivery master.
- Source project and asset manifest.
- Expected formats and approval status.

## Workflow

1. Run `scripts/qa_media.py` to record codec, dimensions, frame rate, duration, audio streams, pixel format and file size.
2. Render or extract the opening, first complete proposition, densest proof, transition peaks, payoff and final frame.
3. Review once normally, once at half speed, once muted and once audio-only when audio exists.
4. Compare every claim, spelling, source line and logo against approved inputs.
5. Inspect safe areas and focal hierarchy for each delivery format.
6. Check motion continuity, flashes, dead frames, dead tail and whether the payoff is visible for its full transition.
7. Check captions, contrast, text size and the reduced-motion composition.
8. Record each result as pass, fail, warning or not tested. Never convert missing evidence into a pass.

## Required checks

Read `references/qa-checklist.md`. At minimum verify:

- exact frame count and duration tolerance;
- expected dimensions, frame rate, codec and pixel format;
- no missing asset, overflow, unintended crop or font fallback;
- one clear focal point at opening, proof and ending;
- source, commissioner and claim language are not conflated;
- the visual meaning survives muted playback;
- audio has no clipping, clicks or truncated tail;
- the final state exists long enough to read and dead tail is intentional;
- reduced-motion output communicates the same sequence;
- source project, editable assets, rights log and delivery report are present.

## Status discipline

- `pass`: directly tested and met.
- `fail`: directly tested and did not meet.
- `warning`: output is usable but risk remains.
- `not_tested`: tool, source or approval was unavailable.

Do not use `pass` for subjective client approval. Use `awaiting_human_review` in the delivery report.

## Deliverables

Return:

- machine-readable media report;
- sampled-frame sheet or frame list;
- concise pass/fail/warning table;
- unresolved human approvals;
- exact output paths and checksums when required;
- recommended fix for each failure, without changing the render unless authorised.
