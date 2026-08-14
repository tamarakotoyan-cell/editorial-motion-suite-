# HTML renderer contract

Editorial Motion's default video path is local HTML, CSS and JavaScript rendered frame by frame with `motion-system/assets/render.py`.

## Runtime boundary

- The source composition is an HTML file with project-relative assets.
- Chrome supplies the layout and graphics engine.
- The renderer controls `performance.now()`, `requestAnimationFrame`, timers, Web Animations and video seeking at each frame timestamp.
- ffmpeg assembles frames as H.264 MP4 and mixes logged SFX cues when present.
- No Node package, React runtime or hosted rendering service is required.

## Composition contract

- Read format from an explicit parameter or project configuration, not browser sniffing.
- Recompute layout for each canvas rather than scaling or centre-cropping a master.
- Preserve semantic scene state in the DOM across beats where continuity matters.
- Keep all production media local and record it in `assets.json`.
- Put `<meta name="editorial-motion" content="X.Y.Z">` in every generated HTML artifact.
- Provide a reduced-motion state with the same information order and no dependence on long travel or velocity cuts.

## Determinism

- Treat the controlled animation timestamp as the only clock.
- Seed noise, particles and procedural placement.
- Avoid network requests, hotlinked fonts and assets whose response can change.
- Decode required imagery before its first visible frame.
- Make every transition valid at its start, peak and end timestamp.

## Verification

Run the artifact linter, then render representative frames and one transition before a full-resolution pass. A deliberately static or reduced-motion composition may use `render.py --no-check`; animated work must keep the frozen-frame check enabled.
