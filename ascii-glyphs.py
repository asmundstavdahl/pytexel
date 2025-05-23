#!/usr/bin/env python3
"""
Generate pytexel ascii.png glyph atlas from a monospace TrueType font using Pillow.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from pytexel.texelator import CHARS


def main():
    parser = argparse.ArgumentParser(
        description='Generate ascii.png glyph atlas from a monospace TrueType font.'
    )
    parser.add_argument(
        '-f', '--font', metavar='FONT',
        help='Path to a TrueType font file (monospace).'
    )
    parser.add_argument(
        '-s', '--size', type=int, default=14,
        help='Font size in points (default: 14).'
    )
    parser.add_argument(
        '-o', '--output', metavar='PNG', default='pytexel/ascii.png',
        help='Output path for the generated ascii.png (default: pytexel/ascii.png).'
    )
    args = parser.parse_args()

    font = None
    if args.font:
        font = ImageFont.truetype(args.font, args.size)
    else:
        for name in ('DejaVuSansMono.ttf', 'LiberationMono-Regular.ttf'):
            try:
                font = ImageFont.truetype(name, args.size)
                break
            except (OSError, IOError):
                continue
        if font is None:
            font = ImageFont.load_default()

    measure_img = Image.new('L', (1, 1))
    measure_draw = ImageDraw.Draw(measure_img)
    bboxes = [measure_draw.textbbox((0, 0), c, font=font) for c in CHARS]
    widths = [bx[2] - bx[0] for bx in bboxes]
    heights = [bx[3] - bx[1] for bx in bboxes]
    char_width = max(widths)
    char_height = max(heights)

    img = Image.new('L', (char_width * len(CHARS), char_height), color=255)
    draw = ImageDraw.Draw(img)
    for i, c in enumerate(CHARS):
        bx = bboxes[i]
        w = bx[2] - bx[0]
        h = bx[3] - bx[1]
        x = i * char_width + (char_width - w) // 2 - bx[0]
        y = (char_height - h) // 2 - bx[1]
        draw.text((x, y), c, fill=0, font=font)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f'Generated {out_path} ({char_width}x{char_height} per glyph)')


if __name__ == '__main__':
    main()