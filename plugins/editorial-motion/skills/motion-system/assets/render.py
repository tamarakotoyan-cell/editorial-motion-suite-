#!/usr/bin/env python3
"""Render an animated HTML artifact to a video file, frame by frame.

The plugin produces HTML. Social and client deliverables are video. This walks
the artifact through a controlled clock one frame at a time, so the 12fps
stepping the house style calls for is genuinely 12fps rather than an
approximation of it.

How it works, and why this way
------------------------------
One Chrome, driven over the DevTools protocol for the whole render. Each frame
advances a virtual clock, pins every animation to that instant, and captures the
surface.

**The clock is driven two ways at once, and that is the whole design.** Neither
mechanism is sufficient alone:

- `transform` and `opacity` animations are promoted to the **compositor thread**,
  which runs on real time and ignores `--virtual-time-budget` entirely. Measured
  on a bar animating `translateX(0 -> 900px)`, every frame came back at x ~780
  with ±10px of random jitter — a video that looked plausible in a file listing
  and was frozen. So Web Animations are pinned explicitly, by setting
  `currentTime` on everything `document.getAnimations()` returns.
- That call only covers the Web Animations timeline. Anything driven by
  `requestAnimationFrame`, canvas, WebGL, `setTimeout` or a `<video>` element is
  invisible to it and would render as its first frame forever. **Virtual time
  does drive those**, so each frame advances the virtual clock by exactly one
  frame's worth before pinning.

Together they cover both. `<video>` elements are seeked directly, since they
follow neither.

The previous version launched **a separate Chrome process per frame** — 60
launches for a 5-second clip, around a minute of wall clock, and it froze on any
rAF or canvas artifact without saying so. A persistent connection fixes the
speed and the correctness together.

`--check` measures how much the first and last probe frames differ, via PSNR
rather than byte equality: compositor jitter changed a handful of pixels per
frame, which defeated the first version of the check. It runs by default; the
guard against a failure that is invisible in a file listing should not itself be
opt-in. `--no-check` opts out for a deliberately static piece.

Sound
-----
`sfx.js` synthesises its voices in the browser and there is no user gesture in a
headless render, so nothing sounds. Instead the page's cue log is read back after
the frames, each voice is rendered offline to a WAV, and `mix_sfx.py` places them
against the video. Levels stay in `sfx.js`, placement stays in the mixer.
`--no-audio` skips it.

Requires Chrome and ffmpeg. Stdlib only otherwise — the protocol runs over
Chrome's `--remote-debugging-pipe`, which is newline-delimited JSON on two file
descriptors, so there is no websocket client to install.

Usage
-----
    python3 render.py artifact.html --duration 5 --out clip.mp4
    python3 render.py artifact.html --duration 8 --fps 12 --preset vertical
    python3 render.py https://example.com/board.html --duration 3
    python3 render.py still.html --duration 4 --no-check   # deliberately static
"""

import argparse
import base64
import json
import os
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PRESETS = {
    "square":   (1080, 1080),
    "portrait": (1080, 1350),
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

# Long enough for a voice's tail; the mixer places by timecode, and trailing
# silence in a source file costs nothing.
VOICE_SECONDS = 2.0

# Installed before any page script runs, so the page never sees the real one.
#
# Advancing virtual time is not enough for requestAnimationFrame. Chrome
# services rAF on its own cadence, and in headless — where frames are produced
# on demand rather than on a display's refresh — that cadence does not track the
# budget. Measured on a canvas drawing its own elapsed time: after advancing
# 2000ms in twelfth-of-a-second steps, the page had reached 1.12s. It moved, so
# it passed the frozen-page check, and it was wrong: 54% speed, and different on
# every run because it depended on how fast the machine happened to be.
#
# So rAF becomes a queue this script drains at an exact timestamp, and
# performance.now() reports the same clock. Deterministic, and identical run to
# run — which the eval set needs, since a render that varies cannot be compared
# against a previous version.
CLOCK_SHIM = """
(function(){
  var clock = 0, nextId = 1, pending = new Map();
  window.requestAnimationFrame = function(cb){
    var id = nextId++; pending.set(id, cb); return id;
  };
  window.cancelAnimationFrame = function(id){ pending.delete(id); };
  try { performance.now = function(){ return clock; }; } catch (e) {}
  window.__renderClock = {
    now: function(){ return clock; },
    tick: function(t){
      clock = t;
      /* Cleared before dispatch: a callback that re-registers — which is the
         normal rAF loop — lands in the next tick, not this one. */
      var due = Array.from(pending.values());
      pending.clear();
      due.forEach(function(cb){ try { cb(t); } catch (e) {} });
      return due.length;
    }
  };
})();
"""

# Web Animations follow neither the shim nor virtual time when they are promoted
# to the compositor, and <video> follows nothing at all. Both are set directly.
PIN = """
(function(t){
  var pinned = 0;
  if (window.__renderClock) window.__renderClock.tick(t);
  if (document.getAnimations) {
    document.getAnimations().forEach(function(a){
      try { a.pause(); a.currentTime = t; pinned++; } catch (e) {}
    });
  }
  document.querySelectorAll('video').forEach(function(v){
    try { v.pause(); v.currentTime = t / 1000; } catch (e) {}
  });
  return pinned;
})(%s)
"""


def find_chrome(override=None):
    if override:
        if Path(override).exists():
            return override
        sys.exit(f"chrome not found at {override}")
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("Chrome not found. Pass --chrome /path/to/chrome")


class CDPError(RuntimeError):
    pass


class Chrome:
    """One headless Chrome, spoken to over --remote-debugging-pipe.

    The pipe transport rather than --remote-debugging-port because it needs no
    websocket client (there is none in the stdlib), no port to allocate and no
    race between "Chrome printed a URL" and "Chrome is listening".

    Chrome reads commands on fd 3 and writes replies on fd 4, so the fds are
    placed by posix_spawn's file actions. subprocess's preexec_fn cannot do it:
    it runs after the child has already closed inherited descriptors, and Chrome
    exits with "Remote debugging pipe file descriptors are not open".
    """

    def __init__(self, binary, width, height, timeout=30.0):
        self.timeout = timeout
        self.profile = tempfile.mkdtemp(prefix="render-profile-")
        self._next_id = 0
        self._buf = b""
        self._events = []

        cmd_r, self._cmd_w = os.pipe()
        self._evt_r, evt_w = os.pipe()
        argv = [binary, "--headless=new", "--remote-debugging-pipe",
                "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                "--no-first-run", "--no-default-browser-check",
                "--force-color-profile=srgb", "--disable-lcd-text",
                f"--user-data-dir={self.profile}", "about:blank"]
        # Chrome is chatty on stderr about mach ports, page-load metrics and
        # allocators regardless of --log-level; none of it is actionable here
        # and all of it buries the render's own output.
        self.pid = os.posix_spawn(binary, argv, os.environ, file_actions=[
            (os.POSIX_SPAWN_OPEN, 1, os.devnull, os.O_WRONLY, 0o666),
            (os.POSIX_SPAWN_OPEN, 2, os.devnull, os.O_WRONLY, 0o666),
            (os.POSIX_SPAWN_DUP2, cmd_r, 3),
            (os.POSIX_SPAWN_DUP2, evt_w, 4)])
        os.close(cmd_r)
        os.close(evt_w)

        target = self.call("Target.createTarget", {"url": "about:blank"})
        self.session = self.call("Target.attachToTarget", {
            "targetId": target["targetId"], "flatten": True})["sessionId"]
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height,
            "deviceScaleFactor": 1, "mobile": False})
        # Not --window-size: an override renders at the size asked for, where
        # headless Chrome silently widens a window under about 500px and would
        # have produced the artifact at the wrong breakpoint.

    # -- transport ---------------------------------------------------------
    def _read_message(self, deadline):
        while True:
            if b"\0" in self._buf:
                raw, self._buf = self._buf.split(b"\0", 1)
                return json.loads(raw)
            remaining = deadline - time.time()
            if remaining <= 0:
                raise CDPError("timed out waiting for Chrome")
            # select, not a bare read: a blocking read on a quiet pipe never
            # returns, so the deadline above would never be reached and a stall
            # would hang the render rather than fail it.
            if not select.select([self._evt_r], [], [], remaining)[0]:
                continue
            chunk = os.read(self._evt_r, 1 << 16)
            if not chunk:
                raise CDPError("Chrome closed the protocol pipe (it exited)")
            self._buf += chunk

    def call(self, method, params=None, timeout=None):
        self._next_id += 1
        msg_id = self._next_id
        message = {"id": msg_id, "method": method, "params": params or {}}
        if getattr(self, "session", None):
            message["sessionId"] = self.session
        os.write(self._cmd_w, json.dumps(message).encode() + b"\0")

        deadline = time.time() + (timeout or self.timeout)
        while True:
            msg = self._read_message(deadline)
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise CDPError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})
            if "method" in msg:
                self._events.append(msg)

    def wait_for(self, event, timeout=None):
        deadline = time.time() + (timeout or self.timeout)
        while True:
            for i, msg in enumerate(self._events):
                if msg.get("method") == event:
                    return self._events.pop(i)
            msg = self._read_message(deadline)
            if msg.get("method") == event:
                return msg
            if "method" in msg:
                self._events.append(msg)

    def evaluate(self, expression, await_promise=False):
        result = self.call("Runtime.evaluate", {
            "expression": expression, "returnByValue": True,
            "awaitPromise": await_promise})
        if "exceptionDetails" in result:
            detail = result["exceptionDetails"]
            raise CDPError(detail.get("exception", {}).get(
                "description", detail.get("text", "evaluate failed")))
        return result.get("result", {}).get("value")

    def close(self):
        for fd in (self._cmd_w, self._evt_r):
            try:
                os.close(fd)
            except OSError:
                pass
        try:
            os.kill(self.pid, signal.SIGTERM)
            for _ in range(50):
                if os.waitpid(self.pid, os.WNOHANG)[0]:
                    break
                time.sleep(0.05)
            else:
                os.kill(self.pid, signal.SIGKILL)
                os.waitpid(self.pid, 0)
        except (ProcessLookupError, ChildProcessError):
            pass
        shutil.rmtree(self.profile, ignore_errors=True)

    # -- the clock ---------------------------------------------------------
    def load(self, url, settle_ms=1200):
        """Navigate with the virtual clock running, then stop it at zero."""
        self.call("Page.addScriptToEvaluateOnNewDocument",
                  {"source": CLOCK_SHIM})
        self.call("Emulation.setVirtualTimePolicy", {"policy": "pause"})
        self.call("Page.navigate", {"url": url})
        self.call("Emulation.setVirtualTimePolicy", {
            "policy": "pauseIfNetworkFetchesPending",
            "budget": settle_ms, "waitForNavigation": True})
        self.wait_for("Emulation.virtualTimeBudgetExpired")
        # Loading consumed virtual time; the artifact's timeline starts now.
        self.virtual_ms = 0.0
        self.evaluate(PIN % 0)

    def seek(self, ms):
        """Put every clock the page can read at exactly `ms`.

        Virtual time carries setTimeout, Date.now and network; the shim carries
        rAF and performance.now; PIN carries Web Animations and <video>.
        """
        advance = ms - self.virtual_ms
        if advance > 0:
            self.call("Emulation.setVirtualTimePolicy", {
                "policy": "pauseIfNetworkFetchesPending", "budget": advance})
            self.wait_for("Emulation.virtualTimeBudgetExpired")
            self.virtual_ms = ms
        self.evaluate(PIN % repr(float(ms)))

    def screenshot(self, path):
        data = self.call("Page.captureScreenshot",
                         {"format": "png", "fromSurface": True})["data"]
        Path(path).write_bytes(base64.b64decode(data))


def psnr(ffmpeg, a, b):
    """Average PSNR between two PNGs in dB, or None if it cannot be measured.

    High PSNR means near-identical. Byte comparison is not enough: the first
    version of this check passed a completely frozen render because compositor
    jitter changed a handful of pixels per frame.
    """
    if not ffmpeg:
        return None
    proc = subprocess.run(
        [ffmpeg, "-i", str(a), "-i", str(b), "-lavfi", "psnr", "-f", "null", "-"],
        capture_output=True, text=True)
    for token in proc.stderr.split():
        if token.startswith("average:"):
            value = token.split(":", 1)[1]
            if value in ("inf", "-inf"):
                return 99.0
            try:
                return float(value)
            except ValueError:
                return None
    return None


def differ(paths):
    first = Path(paths[0]).read_bytes()
    return any(Path(p).read_bytes() != first for p in paths[1:])


def to_url(target):
    if target.startswith(("http://", "https://", "file://")):
        return target
    path = Path(target).resolve()
    if not path.exists():
        sys.exit(f"no such file: {target}")
    return path.as_uri()


def collect_audio(browser, workdir):
    """Pull the page's cue log and render each voice to a WAV.

    Returns a cue file path for mix_sfx.py, or None when the artifact has no
    sound. Gains are baked into the WAVs by sfx.js, which owns the level rules,
    so the cue file asks the mixer only for placement.
    """
    raw = browser.evaluate("JSON.stringify(window.__analogSFXCues || [])")
    cues = json.loads(raw or "[]")
    if not cues:
        return None

    # Let the clock run again. Rendering a voice goes through an
    # OfflineAudioContext, whose task queue is frozen along with virtual time —
    # awaiting that promise with the budget exhausted waits forever.
    browser.call("Emulation.setVirtualTimePolicy", {"policy": "advance"})
    if not browser.evaluate("!!(window.__analogSFX && "
                            "window.__analogSFX.renderWav)"):
        print("warning: the page logged sound cues but exposes no renderer; "
              "sfx.js may be an older copy. Rendering silent.", file=sys.stderr)
        return None

    audio_dir = workdir / "audio"
    audio_dir.mkdir(exist_ok=True)
    rendered, entries = {}, []
    for cue in cues:
        key = (cue["sound"], cue.get("gain_db", -14))
        if key not in rendered:
            wav = browser.evaluate(
                f"window.__analogSFX.renderWav({json.dumps(cue['sound'])},"
                f"{float(key[1])},{VOICE_SECONDS})", await_promise=True)
            if not wav:
                continue
            name = f"{cue['sound']}-{len(rendered)}.wav"
            (audio_dir / name).write_bytes(base64.b64decode(wav))
            rendered[key] = f"audio/{name}"
        entries.append({"file": rendered[key],
                        "at": round(cue.get("at", 0) / 1000.0, 4),
                        "gain_db": 0})
    if not entries:
        return None
    cue_file = workdir / "cues.json"
    cue_file.write_text(json.dumps({"cues": entries}, indent=2), encoding="utf-8")
    print(f"sound: {len(entries)} cue(s), {len(rendered)} voice(s) rendered")
    return cue_file


def mux(cue_file, video, out):
    """Hand the cue file to mix_sfx.py rather than reimplementing the mix."""
    mixer = Path(__file__).resolve().parent.parent.parent / \
        "design-motion-sound" / "scripts" / "mix_sfx.py"
    if not mixer.exists():
        print(f"warning: {mixer.name} not found; leaving the video silent",
              file=sys.stderr)
        return False
    proc = subprocess.run([sys.executable, str(mixer), str(video),
                           str(cue_file), str(out)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"warning: mixing failed, leaving the video silent:\n"
              f"{proc.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render an animated HTML artifact to video.")
    parser.add_argument("target", help="HTML file path or URL")
    parser.add_argument("--duration", type=float, required=True,
                        help="seconds to render")
    parser.add_argument("--fps", type=int, default=12,
                        help="frame rate (default 12, the house posterize rate)")
    parser.add_argument("--preset", choices=sorted(PRESETS),
                        help="canvas size preset")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--out", default="out.mp4")
    parser.add_argument("--crf", type=int, default=18,
                        help="x264 quality, lower is better (default 18)")
    parser.add_argument("--keep-frames", action="store_true")
    parser.add_argument("--frame-timeout", type=float, default=30.0)
    parser.add_argument("--chrome")
    parser.add_argument("--no-check", action="store_true",
                        help="skip the pre-flight probe. Only for a piece you "
                             "know is deliberately static")
    parser.add_argument("--no-audio", action="store_true",
                        help="skip the sound cue pass")
    parser.add_argument("--check", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.check:
        print("note: --check is the default now; the flag does nothing. "
              "Use --no-check to skip the probe.", file=sys.stderr)
    if args.duration <= 0:
        parser.error("--duration must be positive")
    if args.fps < 1 or args.fps > 60:
        parser.error("--fps must be between 1 and 60")

    width, height = PRESETS.get(args.preset, PRESETS["wide"])
    if args.width:
        width = args.width
    if args.height:
        height = args.height

    chrome = find_chrome(args.chrome)
    ffmpeg = shutil.which("ffmpeg")
    frame_ms = 1000.0 / args.fps
    total = int(round(args.duration * args.fps))
    url = to_url(args.target)

    workdir = Path(tempfile.mkdtemp(prefix="render-"))
    frames_dir = workdir / "frames"
    frames_dir.mkdir()
    browser = None
    started = time.time()

    try:
        browser = Chrome(chrome, width, height, timeout=args.frame_timeout)
        browser.load(url)

        if not args.no_check:
            probes = []
            for i, ms in enumerate([0, frame_ms * max(1, total // 2),
                                    frame_ms * max(2, total - 1)]):
                path = frames_dir / f"probe{i}.png"
                browser.seek(ms)
                browser.screenshot(path)
                probes.append(path)

            score = psnr(ffmpeg, probes[0], probes[-1])
            frozen = (score is not None and score > 45) or \
                     (score is None and not differ(probes))
            if frozen:
                detail = (f"PSNR {score:.1f} dB between the first and last "
                          f"probe — essentially the same image"
                          if score is not None else
                          "probe frames are byte-identical")
                sys.exit(
                    f"the page does not animate: {detail}.\n"
                    "Common causes: the animation waits on a user gesture, "
                    "prefers-reduced-motion is stopping it, or the duration "
                    "requested is shorter than the first beat.\n"
                    "If the piece is deliberately static, pass --no-check.")
            print("check: the page advances"
                  + (f" (PSNR {score:.1f} dB first vs last)"
                     if score is not None else ""))
            for path in probes:
                path.unlink()
            # The probes ran the clock forward; restart it for the real frames.
            browser.close()
            browser = Chrome(chrome, width, height, timeout=args.frame_timeout)
            browser.load(url)

        print(f"rendering {total} frames at {args.fps}fps, {width}x{height}")
        for i in range(total):
            browser.seek(i * frame_ms)
            browser.screenshot(frames_dir / f"f{i:05d}.png")
            if (i + 1) % 25 == 0 or i + 1 == total:
                print(f"  {i + 1}/{total}")

        cue_file = None if args.no_audio else collect_audio(browser, workdir)

        if not ffmpeg:
            keep = Path.cwd() / "frames"
            shutil.move(str(frames_dir), str(keep))
            print(f"\nffmpeg not found. Frames are in {keep}. Assemble with:\n"
                  f"  ffmpeg -framerate {args.fps} -i {keep}/f%05d.png "
                  f"-c:v libx264 -crf {args.crf} -pix_fmt yuv420p {args.out}")
            return 0

        # yuv420p for player compatibility; the pad keeps odd dimensions legal
        # for x264, which requires even width and height.
        silent = workdir / "silent.mp4" if cue_file else Path(args.out)
        proc = subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error",
             "-framerate", str(args.fps),
             "-i", str(frames_dir / "f%05d.png"),
             "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
             "-c:v", "libx264", "-crf", str(args.crf),
             "-pix_fmt", "yuv420p", str(silent)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            sys.exit(f"ffmpeg failed:\n{proc.stderr}")

        if cue_file and not mux(cue_file, silent, Path(args.out)):
            shutil.copy(silent, args.out)

        size = Path(args.out).stat().st_size
        elapsed = time.time() - started
        print(f"\n{args.out}  {total} frames  {args.duration}s @ {args.fps}fps"
              f"{'  + sound' if cue_file else ''}  {size // 1024} KB  "
              f"in {elapsed:.1f}s")

        if args.keep_frames:
            keep = Path.cwd() / "frames"
            if keep.exists():
                shutil.rmtree(keep)
            shutil.move(str(frames_dir), str(keep))
            print(f"frames kept in {keep}")
        return 0

    except CDPError as exc:
        sys.exit(f"Chrome protocol error: {exc}")
    finally:
        if browser:
            browser.close()
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
