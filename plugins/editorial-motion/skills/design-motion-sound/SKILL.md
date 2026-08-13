---
name: design-motion-sound
description: Plan, source, edit, synchronise, mix and verify short transitional and accent sound effects for motion graphics and animations. Use for whooshes and swishes, impacts and hits, risers and uplifters, notification pings and interface cues, or licensed meme-inspired and cartoon-style sounds; also use for SFX cue cards, lawful sourcing including from Pixabay, rights logs and mixing supplied SFX into video. Do not use to generate voiceovers, compose music or create general audio beds.
---

# Design motion SFX

Use short sound effects to make movement, state changes, suspense and emphasis
feel more legible and intentional. Do not sound every movement. Make the
animation work silently first, then add only cues that improve how a beat lands.

## Keep the scope narrow

- Work with transitional and accent SFX only.
- Do not generate voiceovers, compose music or create general audio beds.
- Treat supplied dialogue and music as mix constraints to preserve, not creative
  material to generate or replace.

## Build cue cards

Watch once without taking notes, once muted and once for audio only. Build a cue
card for each useful sound event with:

- timecode and visual event;
- cue category and purpose;
- search description based on physical cause, texture, energy and duration;
- sync anchor: launch, velocity peak, crossing, contact, settle, reveal, cut or
  reaction;
- direction, intensity, in/out, gain, fade and optional pitch change;
- source page, contributor, licence snapshot date and local filename.

Use these cue categories:

- `whoosh-swish`: Follow transitions, wipes, slides, zooms and object movement.
  Usually align the cue's strongest point with the movement or velocity peak.
- `impact-hit`: Accentuate contact, landing, emphasis, headline reveals and motion
  settling. Land the transient on the contact, settle or reveal frame.
- `riser-uplifter`: Build suspense or anticipation. End the rise precisely on the
  reveal, cut or following impact.
- `interface`: Signal a real notification or state change with a ping, pop, click,
  tick or toggle. Do not decorate inactive UI.
- `comedy`: Support reactions, reversals and comedic timing with licensed
  meme-inspired or cartoon-style sounds. Preserve the setup and any deliberate
  pause before the cue.

Use one hero sonic idea and a restrained supporting family. Reuse a sound family
when the same object or action returns. Leave deliberate silence before a major
impact or comic reaction. Avoid literal sounds for abstract data unless they
communicate a real relationship.

## Source responsibly

Read `references/pixabay-sourcing.md` before using Pixabay. Its website offers
sound effects under the Pixabay Content License, but the documented public API
currently covers images and videos, not audio. Search and download selected SFX
through the website; do not scrape, mass-download or invent an audio API.

For any source:

- keep the original item page and contributor in the rights log;
- download the file into the project rather than hotlinking it;
- verify the licence at download time and keep a screenshot or text snapshot;
- use licensed, public-domain or originally created equivalents for meme-inspired
  and cartoon-style cues; do not assume a viral clip, film sample or classic
  cartoon recording is cleared;
- flag recognisable brands, voices, samples or other third-party rights;
- never upload sensitive client audio to an external service without approval.

## Prepare cues

- Trim to the useful transient and remove dead air.
- Add 5-20 ms fades to prevent clicks; use longer tails for whooshes and risers.
- High-pass unnecessary low end so multiple cues do not accumulate mud.
- Pitch and layer with restraint. A layer must add a distinct function such as
  transient, body or tail.
- Prefer short lossless working files. Encode only at final delivery.

## Mix into a video

Create a JSON cue file following `references/cue-file-schema.md`, then run:

```bash
python3 scripts/mix_sfx.py input.mp4 cues.json output.mp4
```

The script preserves video, mixes original audio when present, places cues by
timecode, applies gain and fades, and limits the output. Review the result in a
real player. Do not rely on the limiter to repair an overcrowded mix.

## Verify

- Check headphones, laptop speakers and muted playback.
- Confirm supplied dialogue and music remain intelligible and the visual meaning
  survives muted.
- Check whooshes follow the motion, impacts land on the intended frame, risers
  resolve on the reveal, interface cues represent real state changes and comedy
  cues preserve the setup.
- Inspect for clipping, clicks, truncated tails and a noisy dead tail.
- Use the platform or broadcaster's delivery specification when one exists.
  Otherwise report measured loudness and peak rather than claiming a universal
  target.
- Preserve a clean visual-only master so the mix can be revised.

## Deliverables

Return the cue cards, selected-source shortlist, rights log, mixed preview,
unmixed master path, assumptions and any item requiring client or legal review.
