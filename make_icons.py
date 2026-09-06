#!/usr/bin/env python3
"""Rebuild the Whitcott icon set from outlined path data. No font needed.

    pip install cairosvg pillow
    python3 make_icons.py            # writes into ./public/
"""
import pathlib, cairosvg
from PIL import Image

OUT = pathlib.Path("public"); OUT.mkdir(exist_ok=True)
SAGE, WHITE = "#4F7260", "#FFFFFF"
D = "M432 -10Q428 -10 424.0 -7.0Q420 -4 418 6L341 316Q340 324 335.0 323.5Q330 323 328 316L242 6Q239 -4 235.5 -7.0Q232 -10 228 -10Q224 -10 219.5 -7.0Q215 -4 213 6L55 640Q48 668 39.5 679.0Q31 690 11 694L-4 697Q-18 700 -18 710Q-18 720 -3 720H158Q172 720 172 709Q172 700 157 697L146 695Q129 692 124.5 683.5Q120 675 125 653L243 165Q245 158 249.5 158.0Q254 158 256 165L301 328Q312 366 312.0 398.0Q312 430 302 469L260 640Q253 668 246.5 680.0Q240 692 229 694L214 697Q200 700 200 710Q200 720 215 720H352Q366 720 366 709Q366 700 351 697L340 695Q327 693 324.5 684.0Q322 675 327 653L361 510Q363 503 367.5 503.0Q372 503 374 510L410 632Q421 670 418.5 682.0Q416 694 407 695L396 697Q381 700 381 709Q381 720 395 720H490Q507 720 507 709Q507 699 490 697L479 696Q466 695 457.5 680.0Q449 665 439 631L401 500Q390 463 389.5 430.5Q389 398 398 359L443 171Q445 164 449.5 164.0Q454 164 455 171L570 632Q584 690 552 695L541 697Q526 700 526 710Q526 720 540 720H652Q669 720 669 709Q669 699 652 697L641 696Q628 695 618.5 680.5Q609 666 601 631L446 6Q444 -4 440.0 -7.0Q436 -10 432 -10Z"

# Glyph bounds in font units, from Instrument Serif "W" (upm 1000)
XMIN, YMIN, XMAX, YMAX = -18, -10, 669, 720

def svg(size, pad, stroke=0.0):
    gw, gh = XMAX - XMIN, YMAX - YMIN
    s = min(size * (1 - 2 * pad) / gw, size * (1 - 2 * pad) / gh)
    tx = size / 2 - (XMIN + gw / 2) * s
    ty = size / 2 + (YMIN + gh / 2) * s
    st = (f' stroke="{SAGE}" stroke-width="{stroke / s:.3f}" stroke-linejoin="round"'
          if stroke else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"'
            f' role="img" aria-label="Whitcott">\n'
            f'  <rect width="{size}" height="{size}" fill="{WHITE}"/>\n'
            f'  <path transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f} -{s:.5f})"'
            f' d="{D}" fill="{SAGE}"{st}/>\n</svg>\n')

# Tab icon: weighted, because Instrument Serif hairlines vanish under ~24px
small = svg(64, 0.07, stroke=1.15)
(OUT / "favicon.svg").write_text(small)

# Large sizes: clean outline, more padding
large_180 = svg(180, 0.19)
large_512 = svg(512, 0.16)

for name, src, px in (
    ("favicon-16x16.png",    small,     16),
    ("favicon-32x32.png",    small,     32),
    ("_f48.png",             small,     48),
    ("apple-touch-icon.png", large_180, 180),
    ("icon-512.png",         large_512, 512),
):
    cairosvg.svg2png(bytestring=src.encode(), write_to=str(OUT / name),
                     output_width=px, output_height=px)

Image.open(OUT / "_f48.png").convert("RGBA").save(
    OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
(OUT / "_f48.png").unlink()

for p in sorted(OUT.glob("*")):
    if p.suffix in {".png", ".ico", ".svg"}:
        print(f"{p.name:24s} {p.stat().st_size:7d} bytes")
