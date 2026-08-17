#!/usr/bin/env python3
"""
Hermes Instagram Carousel Generator v3
- Generates original abstract backgrounds (no API, no licensing issues)
- Overlays text with premium brand styling
- Produces 10-slide carousel
- CTA with visual hierarchy (gold → white → grey)

Usage:
  python scripts/carousel_v3.py --hook "..." --insights "..." --post_id "..."

Requirements: Pillow (pip install Pillow)
"""

import argparse
import os
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Brand constants
BG_COLOR = (10, 10, 10)
TEXT_COLOR = "#F5F5F5"
ACCENT_COLOR = "#C9A94E"
SLIDE_SIZE = (1080, 1080)

FONT_PATHS = [
    "C:/Windows/Fonts/Georgia.ttf",
    "/usr/share/fonts/truetype/georgia/georgia.ttf",
    "/System/Library/Fonts/Georgia.ttf",
]

def get_font(size, bold=False):
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_background(width, height, seed=None):
    if seed is not None:
        random.seed(seed)
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    style = random.choice(["gradient", "geometric", "noise", "minimal"])
    if style == "gradient":
        for y in range(height):
            r = max(5, min(30, 10 + int(15 * math.sin(y / 40))))
            g = max(5, min(30, 10 + int(10 * math.sin(y / 60))))
            b = max(5, min(30, 10 + int(12 * math.sin(y / 50))))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    elif style == "geometric":
        for _ in range(random.randint(3, 8)):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            c = random.randint(15, 40)
            draw.line([(x1, y1), (x2, y2)], fill=(c, c, c), width=random.randint(1, 3))
    elif style == "noise":
        for _ in range(3000):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            v = random.randint(12, 35)
            img.putpixel((x, y), (v, v, v))
        img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    else:
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for _ in range(random.randint(2, 5)):
            cx, cy = random.randint(100, width - 100), random.randint(100, height - 100)
            r = random.randint(200, 500)
            alpha = random.randint(5, 18)
            odraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(25, 20, 10, alpha))
        img.paste(overlay, (0, 0), overlay)
    return img

def draw_text_centered(draw, text, font, y_pos, color, max_width=None):
    lines = text.split("\n")
    if max_width:
        new_lines = []
        for line in lines:
            if draw.textlength(line, font=font) > max_width:
                mid = len(line) // 2
                space_idx = line.rfind(" ", 0, mid)
                if space_idx > 0:
                    new_lines.append(line[:space_idx])
                    new_lines.append(line[space_idx+1:])
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        lines = new_lines
    total_h = sum(draw.textlength(l, font=font) for l in lines) // len(lines) * len(lines) if lines else 0
    y = y_pos - (total_h // 2)
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=font, fill=color)
        y += int(draw.textlength(line, font=font) / len(line) * 1.8) if line else 40

def create_slide(bg_img, text, slide_type, output_path):
    img = bg_img.copy().resize(SLIDE_SIZE, Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    if slide_type == "hook":
        font = get_font(64, bold=True)
        draw_text_centered(draw, text, font, SLIDE_SIZE[1] // 2, ACCENT_COLOR, max_width=800)
    elif slide_type == "cta":
        lines = text.split("\n")
        overlay = Image.new("RGBA", (SLIDE_SIZE[0], 280), (0, 0, 0, 200))
        img.paste(overlay, (0, SLIDE_SIZE[1] - 280), overlay)
        draw = ImageDraw.Draw(img)
        if len(lines) >= 1:
            font_p = get_font(54, bold=True)
            w = draw.textlength(lines[0], font=font_p)
            draw.text(((SLIDE_SIZE[0] - w) // 2, SLIDE_SIZE[1] - 230), lines[0], font=font_p, fill=ACCENT_COLOR)
        if len(lines) >= 2:
            font_s = get_font(40, bold=False)
            w = draw.textlength(lines[1], font=font_s)
            draw.text(((SLIDE_SIZE[0] - w) // 2, SLIDE_SIZE[1] - 155), lines[1], font=font_s, fill=TEXT_COLOR)
        if len(lines) >= 3:
            font_t = get_font(36, bold=False)
            w = draw.textlength(lines[2], font=font_t)
            draw.text(((SLIDE_SIZE[0] - w) // 2, SLIDE_SIZE[1] - 95), lines[2], font=font_t, fill="#AAAAAA")
    else:
        font = get_font(50, bold=False)
        draw_text_centered(draw, text, font, SLIDE_SIZE[1] // 2, TEXT_COLOR, max_width=900)
    img.save(output_path, quality=95)
    print(f"  Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Hermes Carousel Generator v3")
    parser.add_argument("--hook", required=True, help="Hook text for slide 1")
    parser.add_argument("--insights", required=True, help="Newline-separated insights")
    parser.add_argument("--post_id", default=None, help="Post ID for folder name")
    args = parser.parse_args()
    insights = [i.strip() for i in args.insights.split("\n") if i.strip()]
    post_id = args.post_id or f"carousel_{int(__import__('time').time())}"
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "posts", post_id)
    os.makedirs(base_dir, exist_ok=True)
    print(f"Hook: {args.hook}")
    print(f"Insights: {len(insights)}")
    print(f"Post ID: {post_id}")
    print("\nGenerating original backgrounds...")
    bg_dir = os.path.join(os.path.dirname(base_dir), ".backgrounds", post_id)
    os.makedirs(bg_dir, exist_ok=True)
    bgs = []
    for i in range(10):
        bg = generate_background(1080, 1080, seed=post_id.__hash__() + i)
        bg_path = os.path.join(bg_dir, f"bg_{i:02d}.png")
        bg.save(bg_path, quality=95)
        bgs.append(bg)
        print(f"  Background {i+1}/10 generated")
    print("\nCreating slides...")
    create_slide(bgs[0], args.hook, "hook", os.path.join(base_dir, "slide_01.png"))
    for idx, insight in enumerate(insights[:7], start=1):
        print(f"  Slide {idx+1:02d}/10: {insight[:40]}...")
        create_slide(bgs[idx], insight, "body", os.path.join(base_dir, f"slide_{idx+1:02d}.png"))
    print("  Slide 09/10: Conclusion")
    create_slide(bgs[8], "Remember this.", "body", os.path.join(base_dir, "slide_09.png"))
    print("  Slide 10/10: CTA")
    cta = "Save this for later\nFollow @Hermes for more insights\nWhich truth resonated most? Comment below!"
    create_slide(bgs[9], cta, "cta", os.path.join(base_dir, "slide_10.png"))
    print(f"\nDone! Carousel saved to: {base_dir}")
    print(f"10 slides generated ({len(insights)} insights + hook + conclusion + CTA)")

if __name__ == "__main__":
    main()
