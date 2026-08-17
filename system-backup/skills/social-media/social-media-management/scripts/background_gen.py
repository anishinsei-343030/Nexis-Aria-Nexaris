#!/usr/bin/env python3
"""
Hermes Background Generator
Creates original abstract backgrounds using pure Python/Pillow.
100% original art — no API calls, no licensing issues.
Generates: gradients, geometric patterns, noise textures, soft glows.

Usage:
  python background_gen.py --count 3 --output_dir "./backgrounds" --seed 123

Requirements: Pillow (pip install Pillow)
"""

import argparse
import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter

def generate_background(width=1080, height=1080, seed=None):
    """Generate a random abstract background. 4 styles, each seed yields different art."""
    if seed is not None:
        random.seed(seed)
    
    img = Image.new("RGB", (width, height), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    style = random.choice(["gradient", "geometric", "noise", "minimal"])

    if style == "gradient":
        # Subtle vertical gradient with slight color variation
        for y in range(height):
            r = max(5, min(30, 10 + int(15 * math.sin(y / 40))))
            g = max(5, min(30, 10 + int(10 * math.sin(y / 60))))
            b = max(5, min(30, 10 + int(12 * math.sin(y / 50))))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

    elif style == "geometric":
        # Thin subtle lines
        for _ in range(random.randint(3, 8)):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            c = random.randint(15, 40)
            draw.line([(x1, y1), (x2, y2)], fill=(c, c, c), width=random.randint(1, 3))

    elif style == "noise":
        # Subtle noise, blurred
        for _ in range(3000):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            v = random.randint(12, 35)
            img.putpixel((x, y), (v, v, v))
        img = img.filter(ImageFilter.GaussianBlur(radius=1.5))

    else:  # minimal — soft glows
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for _ in range(random.randint(2, 5)):
            cx, cy = random.randint(100, width - 100), random.randint(100, height - 100)
            r = random.randint(200, 500)
            alpha = random.randint(5, 18)
            odraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(25, 20, 10, alpha))
        img.paste(overlay, (0, 0), overlay)

    return img

def main():
    parser = argparse.ArgumentParser(description="Generate abstract backgrounds")
    parser.add_argument("--count", type=int, default=3, help="Number of backgrounds")
    parser.add_argument("--output_dir", default="./backgrounds", help="Output directory")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    for i in range(args.count):
        seed = (args.seed or 0) + i
        img = generate_background(1080, 1080, seed=seed)
        path = os.path.join(args.output_dir, f"bg_{i:02d}.png")
        img.save(path, quality=95)
        print(f"Generated: {path}")
    print(f"Done — {args.count} backgrounds in {args.output_dir}")

if __name__ == "__main__":
    main()
