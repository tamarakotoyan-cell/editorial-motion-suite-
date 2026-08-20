#!/usr/bin/env python3
"""Minimal headless Chrome driver over the DevTools pipe. Stdlib only.

Shared by check-static.py (measuring what the page actually renders) and
shoot.py (exporting it). Static analysis of HTML source cannot tell you what
fraction of the canvas is covered, what colour a label resolves to against its
field, or whether two frames have the same shape — all three are the rules that
separate good static work from rejected, so the linter has to render.

Transport lifted from editorial-motion's motion-system/assets/render.py, cut
down to load / evaluate / screenshot. It is deliberately a copy rather than an
import: a cross-plugin relative path resolves in the source tree and dangles
everywhere the skill is installed one at a time, which is the failure
build-skills.py exists to prevent.

--remote-debugging-pipe rather than a port: no websocket client in the stdlib,
no port to allocate, no race between "Chrome printed a URL" and "Chrome is
listening". Chrome reads commands on fd 3 and writes replies on fd 4, placed by
posix_spawn's file actions — subprocess's preexec_fn cannot do it, as it runs
after the child has closed inherited descriptors.
"""

import base64
import json
import os
import select
import shutil
import signal
import sys
import tempfile
import time
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


class CDPError(RuntimeError):
    pass


class ChromeUnavailable(RuntimeError):
    """Chrome is not installed. Callers degrade rather than die."""


def find_chrome(override=None):
    if override:
        if Path(override).exists():
            return override
        raise ChromeUnavailable(f"chrome not found at {override}")
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    raise ChromeUnavailable("Chrome not found. Pass --chrome /path/to/chrome")


class Chrome:
    def __init__(self, binary, width, height, timeout=30.0):
        self.timeout = timeout
        self.profile = tempfile.mkdtemp(prefix="static-design-")
        self._next_id = 0
        self._buf = b""
        self._events = []
        self.session = None

        cmd_r, self._cmd_w = os.pipe()
        self._evt_r, evt_w = os.pipe()
        argv = [binary, "--headless=new", "--remote-debugging-pipe",
                "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                "--no-first-run", "--no-default-browser-check",
                "--force-color-profile=srgb", "--disable-lcd-text",
                f"--user-data-dir={self.profile}", "about:blank"]
        # Chrome is chatty on stderr about mach ports and allocators regardless
        # of --log-level; none of it is actionable and all of it buries the
        # linter's own output.
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
        self.set_viewport(width, height)

    def set_viewport(self, width, height):
        # Not --window-size: an override renders at the size asked for, where
        # headless Chrome silently widens a window under about 500px and would
        # measure the artifact at the wrong breakpoint.
        self.width, self.height = width, height
        self.call("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height,
            "deviceScaleFactor": 1, "mobile": False})

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
            # returns, so the deadline would never be reached and a stall would
            # hang rather than fail.
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
        if self.session:
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

    def evaluate(self, expression):
        result = self.call("Runtime.evaluate", {
            "expression": expression, "returnByValue": True})
        if "exceptionDetails" in result:
            detail = result["exceptionDetails"]
            raise CDPError(detail.get("exception", {}).get(
                "description", detail.get("text", "evaluate failed")))
        return result.get("result", {}).get("value")

    def load(self, path, settle_ms=900):
        url = Path(path).resolve().as_uri()
        self.call("Page.navigate", {"url": url})
        # Webfont metrics settle after first paint; measuring before they do
        # reports the fallback face's geometry, which is the wrong answer for
        # every size and occupancy check downstream.
        time.sleep(settle_ms / 1000)

    def screenshot(self, fmt="png", quality=None):
        params = {"format": fmt, "captureBeyondViewport": False}
        if fmt == "jpeg" and quality is not None:
            params["quality"] = quality
        return base64.b64decode(self.call("Page.captureScreenshot", params)["data"])

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

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
