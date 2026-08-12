"""Shared noise and PNG primitives for the texture generators.

Stdlib only — no numpy, no Pillow. A build step that needs a pip install first
is a build step that does not get run.

Everything here is *tileable by construction*: lattice indices wrap modulo the
octave frequency, so a sample at x = size-1 interpolates back toward the cell at
x = 0. That property is the whole point — `type-treatment/assets/example.html`
currently warns that grain must be applied `cover` rather than tiled because "a
tiled texture shows its seams as hard bands", and seamless tiles are what lift
that restriction.
"""

import struct
import zlib
from pathlib import Path


def smoothstep_table(size, freq):
    """Lattice indices and quintic weights for one axis.

    Quintic (6t^5 - 15t^4 + 10t^3) rather than cubic: it has zero first *and*
    second derivative at the cell boundary, so octaves stack without visible
    lattice creases.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if freq <= 0:
        raise ValueError("freq must be greater than 0")

    i0s, i1s, ws = [], [], []
    for x in range(size):
        t = x * freq / size
        cell = int(t)
        f = t - cell
        i0s.append(cell % freq)
        i1s.append((cell + 1) % freq)
        ws.append(f * f * f * (f * (f * 6 - 15) + 10))
    return i0s, i1s, ws


def value_noise(size, fx, fy, rng):
    """Tileable value noise on size x size from an fx by fy lattice.

    Separate fx and fy give anisotropy: high fx against low fy varies fast
    across x and slowly down y, which reads as vertical streaking.
    """
    lattice = [[rng.random() for _ in range(fx)] for _ in range(fy)]
    xi0, xi1, xw = smoothstep_table(size, fx)
    yi0, yi1, yw = smoothstep_table(size, fy)

    out = []
    for y in range(size):
        top_row = lattice[yi0[y]]
        bot_row = lattice[yi1[y]]
        wy = yw[y]
        # Collapse the two lattice rows to one first (fx values), then
        # interpolate across x — one lerp per pixel instead of three.
        blended = [a + (b - a) * wy for a, b in zip(top_row, bot_row)]
        out.extend(
            blended[i0] + (blended[i1] - blended[i0]) * w
            for i0, i1, w in zip(xi0, xi1, xw)
        )
    return out


def fbm(size, base_fx, base_fy, octaves, rng, gain=0.5, lacunarity=2):
    """Fractal sum of value noise, centred on zero."""
    total = [0.0] * (size * size)
    amp = 1.0
    norm = 0.0
    fx, fy = base_fx, base_fy
    for _ in range(octaves):
        if fx > size or fy > size:
            break  # past Nyquist — the octave would be aliasing, not detail
        layer = value_noise(size, max(1, int(fx)), max(1, int(fy)), rng)
        total = [t + (v - 0.5) * amp for t, v in zip(total, layer)]
        norm += amp
        amp *= gain
        fx *= lacunarity
        fy *= lacunarity
    return [t / norm for t in total] if norm else total


def white_noise(size, rng):
    """Per-pixel grain, centred on zero. Uncorrelated, so tileable trivially."""
    return [rng.random() - 0.5 for _ in range(size * size)]


def write_png(path, width, height, pixels, channels):
    """Write an 8-bit PNG. `pixels` is a flat list of ints, row-major.

    Sub filter: these textures are horizontally coherent over a narrow value
    range, so neighbouring deltas sit near zero and deflate does the rest.
    """
    if channels not in (1, 3):
        raise ValueError("channels must be 1 or 3")

    expected = width * height * channels
    if len(pixels) != expected:
        raise ValueError(
            f"invalid pixel buffer length {len(pixels)}; expected {expected}"
        )

    raw = bytearray()
    stride = width * channels
    for y in range(height):
        row = pixels[y * stride:(y + 1) * stride]
        raw.append(1)  # filter type 1: Sub
        for i in range(stride):
            left = row[i - channels] if i >= channels else 0
            raw.append((row[i] - left) & 0xFF)

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8,
                                      0 if channels == 1 else 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(png)
    return len(png)


def seam_ratio(pixels, width, height, channels):
    """Wrap-edge delta versus the deltas immediately either side of it.

    Returns (x_ratio, y_ratio). A correct wrap sits near 1.0 and is biased
    slightly low, because the quintic weighting has zero gradient exactly at a
    lattice boundary and the seam always lands on one.

    Known blind spot: a *centred, symmetric* falloff such as a radial vignette
    passes. Its values match at both edges — what it breaks is the gradient, and
    per-pixel grain swamps any second-difference test by orders of magnitude.
    That is a limit of local pixel statistics, and it is why vignetting is kept
    out of these generators and left to CSS.
    """
    def at(x, y, c):
        return pixels[(y * width + x) * channels + c]

    def mean(vals):
        return sum(vals) / len(vals) if vals else 0.0

    cols = range(channels)
    seam_x = mean([abs(at(width - 1, y, c) - at(0, y, c))
                   for y in range(height) for c in cols])
    local_x = mean([abs(at(width - 2, y, c) - at(width - 1, y, c))
                    for y in range(height) for c in cols]
                   + [abs(at(0, y, c) - at(1, y, c))
                      for y in range(height) for c in cols])
    seam_y = mean([abs(at(x, height - 1, c) - at(x, 0, c))
                   for x in range(width) for c in cols])
    local_y = mean([abs(at(x, height - 2, c) - at(x, height - 1, c))
                    for x in range(width) for c in cols]
                   + [abs(at(x, 0, c) - at(x, 1, c))
                      for x in range(width) for c in cols])

    return (seam_x / local_x if local_x else 0.0,
            seam_y / local_y if local_y else 0.0)
