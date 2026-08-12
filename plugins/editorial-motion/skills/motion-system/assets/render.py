#!/usr/bin/env python3
"""Render an animated HTML artifact to a video file, frame by frame.

The plugin produces HTML. Social and client deliverables are video. This walks
the artifact through virtual time one frame at a time and assembles the result,
so the 12fps stepping the house style calls for is genuinely 12fps rather than
an approximation of it.

How it works, and why this way
------------------------------
Each frame is a separate Chrome launch. A small script is injected into a temp
copy of the page; it reads a timestamp from the query string, pauses every
animation via `document.getAnimations()`, and sets each one's `currentTime` to
that moment. The screenshot is then a still of the composition at exactly that
instant. Same input, same output, every run.

**It does not use `--virtual-time-budget` to drive the animation, and that is
the whole point of the design.** The obvious approach — set the virtual-time
budget to the frame's timestamp — silently does not work: `transform` and
`opacity` animations are promoted to the compositor thread, which runs on real
time and ignores virtual time entirely. Measured on a bar animating
`translateX(0 -> 900px)`, every frame came back at x ~780 with ±10px of random
jitter. The video looked plausible in a file listing and was frozen. Virtual
time is still used, at a fixed budget, but only to let the page finish loading
deterministically.

That jitter also defeated the first version of `--check`, which only asked
whether frames *differed*. It now measures how much they differ, via PSNR, so
"different by a few pixels of noise" no longer passes for "animating".

The cost is a process per frame, so a 5-second clip at 12fps is 60 launches and
roughly a minute. That is the trade for determinism and for needing nothing
installed beyond Chrome.

Audio is not muxed here. sfx.js runs in the browser and virtual time does not
render it; add the cue list with ffmpeg afterwards if the piece needs sound.

Requires Chrome and ffmpeg. Stdlib only otherwise.

Usage
-----
    python3 render.py artifact.html --duration 5 --out clip.mp4
    python3 render.py artifact.html --duration 8 --fps 12 --preset vertical
    python3 render.py https://example.com/board.html --duration 3 --check
    python3 render.py artifact.html --duration 4 --keep-frames
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PRESETS = {
    "square":   (1080, 1080),
    "vertical": (1080, 1920),
    "wide":     (1920, 1080),
    "board":    (1200, 900),
}

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]

# Chrome headless will not open a window narrower than this; anything smaller is
# silently widened, which would render the artifact at the wrong breakpoint.
MIN_CHROME_WIDTH = 500


def find_chrome(override=None):
    if override:
        if Path(override).exists():
            return override
        sys.exit(f"chrome not found at {override}")
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("Chrome not found. Pass --chrome /path/to/chrome")


# Injected into a temp copy of the page. Reads ?t=<ms> and freezes every
# animation at that instant. document.getAnimations() covers CSS animations and
# transitions; re-running it after load and on the next frame catches anything
# started late by script.
FREEZE = """
<script>
(function(){
  var t = parseFloat(new URLSearchParams(location.search).get('t') || '0');
  function freeze(){
    if (!document.getAnimations) return;
    document.getAnimations().forEach(function(a){
      try { a.pause(); a.currentTime = t; } catch (e) {}
    });
  }
  freeze();
  document.addEventListener('DOMContentLoaded', freeze);
  window.addEventListener('load', function(){
    freeze();
    requestAnimationFrame(freeze);
  });
  window.__renderFreeze = freeze;
})();
</script>
"""


def to_url(target):
    if target.startswith(("http://", "https://", "file://")):
        return target
    p = Path(target).resolve()
    if not p.exists():
        sys.exit(f"no such file: {target}")
    return p.as_uri()


def prepare(target, workdir):
    """Return a base URL whose page freezes its animations at ?t=<ms>.

    Local files are copied next to their original directory contents so that
    relative references keep resolving; remote URLs cannot be rewritten, so they
    are returned untouched and the caller falls back to virtual time.
    """
    if target.startswith(("http://", "https://")):
        return target, False
    src = Path(target[7:] if target.startswith("file://") else target).resolve()
    if not src.exists():
        sys.exit(f"no such file: {target}")
    html = src.read_text(encoding="utf-8")
    if "</body>" in html:
        html = html.replace("</body>", FREEZE + "</body>", 1)
    else:
        html += FREEZE
    # Write the temp copy INTO the source directory so relative asset paths,
    # which are the normal case for these artifacts, still resolve.
    tmp = src.parent / f".render-{os.getpid()}-{src.name}"
    tmp.write_text(html, encoding="utf-8")
    workdir.append(tmp)
    return tmp.resolve().as_uri(), True


def shoot(chrome, url, out_path, width, height, timeout, settle_ms=1200):
    cmd = [
        chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check",
        "--force-color-profile=srgb",
        f"--window-size={width},{height}",
        # Fixed budget: this only lets the page finish loading. The animation
        # clock is set by the injected freeze script, not by virtual time.
        f"--virtual-time-budget={settle_ms}",
        f"--screenshot={out_path}",
        url,
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False
    return Path(out_path).exists()


def psnr(ffmpeg, a, b):
    """Average PSNR between two PNGs in dB, or None if it cannot be measured.

    High PSNR means near-identical. Byte comparison is not enough here: the
    first version of this check passed a completely frozen render because
    compositor jitter changed a handful of pixels per frame.
    """
    if not ffmpeg:
        return None
    r = subprocess.run(
        [ffmpeg, "-i", str(a), "-i", str(b), "-lavfi", "psnr", "-f", "null", "-"],
        capture_output=True, text=True)
    for token in r.stderr.split():
        if token.startswith("average:"):
            val = token.split(":", 1)[1]
            if val in ("inf", "-inf"):
                return 99.0
            try:
                return float(val)
            except ValueError:
                return None
    return None


def differ(paths):
    """True if the given frames are not all byte-identical."""
    first = Path(paths[0]).read_bytes()
    return any(Path(p).read_bytes() != first for p in paths[1:])


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Render an animated HTML artifact to video.")
    p.add_argument("target", help="HTML file path or URL")
    p.add_argument("--duration", type=float, required=True,
                   help="seconds to render")
    p.add_argument("--fps", type=int, default=12,
                   help="frame rate (default 12, the house posterize rate)")
    p.add_argument("--preset", choices=sorted(PRESETS),
                   help="canvas size preset")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--out", default="out.mp4")
    p.add_argument("--crf", type=int, default=18,
                   help="x264 quality, lower is better (default 18)")
    p.add_argument("--keep-frames", action="store_true")
    p.add_argument("--frame-timeout", type=float, default=30.0)
    p.add_argument("--chrome")
    p.add_argument("--check", action="store_true",
                   help="probe three frames first and stop if the animation "
                        "does not advance")
    args = p.parse_args(argv)

    if args.duration <= 0:
        p.error("--duration must be positive")
    if args.fps < 1 or args.fps > 60:
        p.error("--fps must be between 1 and 60")

    width, height = PRESETS.get(args.preset, PRESETS["wide"])
    if args.width:
        width = args.width
    if args.height:
        height = args.height
    if width < MIN_CHROME_WIDTH:
        print(f"warning: Chrome headless will not render narrower than "
              f"{MIN_CHROME_WIDTH}px; {width} would be silently widened. "
              f"Rendering at {MIN_CHROME_WIDTH} and letting you crop.",
              file=sys.stderr)
        width = MIN_CHROME_WIDTH

    chrome = find_chrome(args.chrome)
    ffmpeg = shutil.which("ffmpeg")
    frame_ms = 1000.0 / args.fps
    total = int(round(args.duration * args.fps))

    workdir = Path(tempfile.mkdtemp(prefix="render-"))
    frames_dir = workdir / "frames"
    frames_dir.mkdir()
    temps = []

    try:
        base, frozen = prepare(args.target, temps)
        if not frozen:
            print("warning: a remote URL cannot have the freeze script "
                  "injected, so animation timing falls back to virtual time — "
                  "which compositor-driven transforms ignore. Save the page "
                  "locally for a reliable render.", file=sys.stderr)

        def frame_url(ms):
            sep = "&" if "?" in base else "?"
            return f"{base}{sep}t={int(ms)}" if frozen else base

        if args.check:
            probes = []
            for i, ms in enumerate([0, frame_ms * max(1, total // 2),
                                    frame_ms * max(2, total - 1)]):
                path = frames_dir / f"probe{i}.png"
                if not shoot(chrome, frame_url(ms), str(path), width, height,
                             args.frame_timeout):
                    sys.exit(f"probe frame at {int(ms)}ms failed to render")
                probes.append(path)

            score = psnr(ffmpeg, probes[0], probes[-1])
            frozen_still = (score is not None and score > 45) or \
                           (score is None and not differ(probes))
            if frozen_still:
                detail = (f"PSNR {score:.1f} dB between the first and last "
                          f"probe — essentially the same image"
                          if score is not None else
                          "probe frames are byte-identical")
                sys.exit(
                    f"the page does not animate: {detail}.\n"
                    "Common causes: the animation waits on a user gesture, "
                    "prefers-reduced-motion is stopping it, it is driven by "
                    "requestAnimationFrame rather than the Web Animations "
                    "timeline, or the duration requested is shorter than the "
                    "first beat. Rendering would produce a frozen video.")
            print("check: the page advances"
                  + (f" (PSNR {score:.1f} dB first vs last)"
                     if score is not None else ""))
            for path in probes:
                path.unlink()

        print(f"rendering {total} frames at {args.fps}fps, {width}x{height}")
        for i in range(total):
            ms = int(round(i * frame_ms))
            out = frames_dir / f"f{i:05d}.png"
            if not shoot(chrome, frame_url(ms), str(out), width, height,
                         args.frame_timeout):
                sys.exit(f"frame {i} ({ms}ms) failed to render")
            if (i + 1) % 10 == 0 or i + 1 == total:
                print(f"  {i + 1}/{total}")

        if not ffmpeg:
            keep = Path.cwd() / "frames"
            shutil.move(str(frames_dir), str(keep))
            print(f"\nffmpeg not found. Frames are in {keep}. Assemble with:\n"
                  f"  ffmpeg -framerate {args.fps} -i {keep}/f%05d.png "
                  f"-c:v libx264 -crf {args.crf} -pix_fmt yuv420p {args.out}")
            return 0

        # yuv420p for player compatibility; the pad keeps odd dimensions legal
        # for x264, which requires even width and height.
        cmd = [ffmpeg, "-y", "-loglevel", "error",
               "-framerate", str(args.fps),
               "-i", str(frames_dir / "f%05d.png"),
               "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
               "-c:v", "libx264", "-crf", str(args.crf),
               "-pix_fmt", "yuv420p", args.out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"ffmpeg failed:\n{r.stderr}")

        size = Path(args.out).stat().st_size
        print(f"\n{args.out}  {total} frames  {args.duration}s @ {args.fps}fps  "
              f"{size // 1024} KB")

        if args.keep_frames:
            keep = Path.cwd() / "frames"
            if keep.exists():
                shutil.rmtree(keep)
            shutil.move(str(frames_dir), str(keep))
            print(f"frames kept in {keep}")
        return 0

    finally:
        for t in temps:
            try:
                t.unlink()
            except OSError:
                pass
        if workdir.exists():
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
