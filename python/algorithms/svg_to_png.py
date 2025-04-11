#!/usr/bin/env python3
"""
SVG to PNG Converter with Multi-Color Replacement (Supports Gradients)

Author: Jason Maglangit

Description:
This script converts an SVG (Scalable Vector Graphics) file into a high-resolution PNG file.
It also allows you to replace one or more HEX colors from the SVG with a new color.

It supports:
- Multiple `--from-color` values for mapping gradient and fill/stroke colors
- A single `--to-color` value to replace all matches
- Scaling factor for high-resolution output
- Custom output file names

Typical use cases:
- Converting themed icons (e.g., blue → bronze, silver, gold)
- Color customization for branding
- High-resolution rasterization of SVG assets

Dependencies:
- Python 3
- CairoSVG (install via `pip install cairosvg`)
"""

import os
import sys
import argparse
import cairosvg
import re

def normalize_hex(color):
    """
    Normalize a hex color by removing quotes and converting to lowercase.
    """
    return color.lower().strip().replace('"', '').replace("'", '')

def replace_svg_colors(svg_content, from_colors, to_color):
    """
    Replaces all occurrences of colors in `from_colors` with `to_color`
    inside `fill`, `stroke`, and `stop-color` attributes.
    """
    to_color = normalize_hex(to_color)
    color_attributes = ['fill', 'stroke', 'stop-color']

    for from_color in from_colors:
        from_color = normalize_hex(from_color)
        for attr in color_attributes:
            svg_content = re.sub(
                fr'({attr}\s*=\s*["\']){from_color}(["\'])',
                fr'\1{to_color}\2',
                svg_content,
                flags=re.IGNORECASE
            )

    return svg_content

def convert_svg_to_png(svg_path, output_path=None, scale=1.0, output_width=None, output_height=None, from_colors=None, to_color=None):
    """
    Reads the SVG file, replaces colors if needed, and generates a PNG output.
    """
    if not os.path.exists(svg_path):
        print(f"❌ File not found: {svg_path}")
        return

    if not svg_path.lower().endswith('.svg'):
        print("❌ Input file must be an SVG file.")
        return

    if output_path is None:
        output_path = os.path.splitext(svg_path)[0] + ".png"

    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # Apply color replacements
        if from_colors and to_color:
            svg_content = replace_svg_colors(svg_content, from_colors, to_color)

        # Convert to PNG
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=output_path,
            scale=scale,
            output_width=output_width,
            output_height=output_height
        )
        print(f"✅ Successfully converted to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to convert: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert SVG to high-resolution PNG and optionally replace colors (including gradients)."
    )

    parser.add_argument("svg", help="Path to the input SVG file")
    parser.add_argument("-o", "--output", help="Path to save the output PNG file")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor (e.g., 2.0 for 2x resolution)")
    parser.add_argument("--width", type=int, help="Output width in pixels (overrides scale)")
    parser.add_argument("--height", type=int, help="Output height in pixels (overrides scale)")
    parser.add_argument("--from-color", action="append", help="Hex color(s) to replace (e.g., --from-color #0078d4). Can be used multiple times.")
    parser.add_argument("--to-color", help="Hex color to apply as replacement (e.g., --to-color #cd7f32)")

    args = parser.parse_args()

    convert_svg_to_png(
        svg_path=args.svg,
        output_path=args.output,
        scale=args.scale,
        output_width=args.width,
        output_height=args.height,
        from_colors=args.from_color,
        to_color=args.to_color
    )

if __name__ == "__main__":
    main()
