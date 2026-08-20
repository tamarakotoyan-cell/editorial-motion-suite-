#!/usr/bin/env python3
"""Render a static design artifact to PNG or JPG at exact canvas size.

The plugin produces HTML. Deliverables are images. This walks each frame of an
artifact through headless Chrome at the canvas's real pixel dimensions and
writes one file per frame.

Frames are `[data-frame]`, `.frame` or `.slide` elements. A file with none of
those is treated as a single frame filling the viewport, which is the common
case for a one-off tile.

Why per-frame rather than one tall screenshot: a carousel is delivered as
separate images, and cropping a tall capture reintroduces the off-by-a-pixel
seam that the fixed canvas exists to avoid. Each frame is scrolled to the top of
the viewport and captured on its own.

    python3 shoot.py tile.html                       # -> tile.png
    python3 shoot.py carousel.html -o out/           # -> out/carousel-01.png ...
    python3 shoot.py tile.html --format 1x1
    python3 shoot.py tile.html --jpg --quality 92
    python3 shoot.py tile.html --scale 2             # 2x for print or retina

Exit codes: 0 wrote files, 1 nothing to write or Chrome unavailable, 2 bad usage.
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

FORMATS = {
    "4x5":  (1080, 1350),      # the default — feed posts and carousels
    "1x1":  (1080, 1080),
    "9x16": (1080, 1920),
    "16x9": (1920, 1080),
    "4x3":  (1440, 1080),
}

FRAME_QUERY = "[data-frame], .frame, .slide"


def frame_boxes(browser):
    """Each frame's position and size, in CSS pixels, in document order."""
    return browser.evaluate(f"""
      (() => {{
        const els = [...document.querySelectorAll('{FRAME_QUERY}')];
        if (!els.length) return null;
        return els.map(el => {{
          const r = el.getBoundingClientRect();
          return {{ top: r.top + window.scrollY, left: r.left + window.scrollX,
                   w: Math.round(r.width), h: Math.round(r.height) }};
        }});
      }})()
    """)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", help="HTML artifact")
    parser.add_argument("-o", "--out", default=None,
                        help="output file or directory (default: alongside the input)")
    parser.add_argument("--format", choices=sorted(FORMATS), default="4x5",
                        help="canvas size when the artifact does not declare its own")
    parser.add_argument("--jpg", action="store_true", help="write JPG instead of PNG")
    parser.add_argument("--quality", type=int, default=92, help="JPG quality")
    parser.add_argument("--scale", type=int, default=1,
                        help="device scale factor — 2 for retina or print")
    parser.add_argument("--chrome", help="path to a Chrome or Chromium binary")
    parser.add_argument("--settle", type=int, default=900,
                        help="ms to wait after load for webfonts and layout")
    args = parser.parse_args()

    src = Path(args.path)
    if not src.is_file():
        print(f"FAIL  not a file: {src}")
        return 2

    from _chrome import Chrome, find_chrome, ChromeUnavailable  # noqa: E402
    try:
        binary = find_chrome(args.chrome)
    except ChromeUnavailable as exc:
        print(f"FAIL  {exc}")
        return 1

    width, height = FORMATS[args.format]
    ext = "jpeg" if args.jpg else "png"
    suffix = ".jpg" if args.jpg else ".png"

    with Chrome(binary, width, height) as browser:
        if args.scale != 1:
            browser.call("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": height,
                "deviceScaleFactor": args.scale, "mobile": False})
        browser.load(src, settle_ms=args.settle)

        boxes = frame_boxes(browser)
        # Re-fit the viewport to the artifact's own declared canvas rather than
        # the --format guess. A frame that declares 1080x1080 must not be shot
        # into a 1350-tall viewport with 270px of body showing beneath it.
        if boxes:
            first = boxes[0]
            if (first["w"], first["h"]) != (width, height):
                width, height = first["w"], first["h"]
                browser.set_viewport(width, height)
                if args.scale != 1:
                    browser.call("Emulation.setDeviceMetricsOverride", {
                        "width": width, "height": height,
                        "deviceScaleFactor": args.scale, "mobile": False})
                boxes = frame_boxes(browser)

        multi = bool(boxes) and len(boxes) > 1
        if args.out:
            out = Path(args.out)
            if multi or out.is_dir() or not out.suffix:
                out.mkdir(parents=True, exist_ok=True)
                dest_dir, stem = out, src.stem
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                dest_dir, stem = out.parent, out.stem
        else:
            dest_dir, stem = src.parent, src.stem

        written = []
        if not boxes:
            data = browser.screenshot(ext, args.quality if args.jpg else None)
            dest = dest_dir / f"{stem}{suffix}"
            dest.write_bytes(data)
            written.append(dest)
        else:
            for i, box in enumerate(boxes, start=1):
                browser.evaluate(f"window.scrollTo({box['left']}, {box['top']})")
                data = browser.screenshot(ext, args.quality if args.jpg else None)
                name = f"{stem}-{i:02d}{suffix}" if multi else f"{stem}{suffix}"
                dest = dest_dir / name
                dest.write_bytes(data)
                written.append(dest)

    for dest in written:
        print(f"wrote {dest}  ({width}x{height}"
              f"{f' @{args.scale}x' if args.scale != 1 else ''})")
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
