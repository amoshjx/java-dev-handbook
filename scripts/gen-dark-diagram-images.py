#!/usr/bin/env python3
"""Generate dark-theme variants of static diagram PNGs (white text on dark bg)."""

from __future__ import annotations

import colorsys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = (
    "JVM.png",
    "RSS_Count.png",
    "spring-multi-module-project.png",
)


def invert_preserve_hue(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    inv = ImageOps.invert(rgb)
    px = inv.load()
    width, height = inv.size

    for y in range(height):
        for x in range(width):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            h = (h + 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            px[x, y] = (int(r * 255), int(g * 255), int(b * 255))

    return inv


def main() -> None:
    for name in SOURCES:
        src = ROOT / name
        if not src.exists():
            raise SystemExit(f"missing source image: {src}")
        out = ROOT / name.replace(".png", "-dark.png")
        invert_preserve_hue(Image.open(src)).save(out, optimize=True)
        print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
