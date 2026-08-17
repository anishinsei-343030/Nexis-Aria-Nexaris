#!/usr/bin/env python3
"""
Hermes Instagram Carousel Generator

Generates 10-slide carousels for Instagram:
  - Slide 1: Hook (gold accent, centered)
  - Slides 2-8: One insight per slide (white text, centered)
  - Slide 9: "Remember this." conclusion
  - Slide 10: CTA (bottom-aligned)

Usage:
  python scripts/carousel-generator.py \\
    --hook "7 Psychological Truths Most People Learn Too Late" \\
    --insights "1. You don't need to justify your feelings.
2. Loneliness and being alone are not the same.
3. Self-worth comes from within.
4. Not everyone will like you, and that's okay.
5. Growth requires discomfort.
6. You can't change people.
7. Happiness is a choice, not a destination." \\
    --output_dir "content/posts/20260617_psych_truths"

Requirements: Pillow (pip install Pillow)
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Brand constants
BG_COLOR = "#0A0A0A"           # Black
TEXT_COLOR = "#F5F5F5"         # White
ACCENT_COLOR = "#C9A94E"       # Gold
FONT_PATHS = [
    "C:/Windows/Fonts/Georgia.ttf",
    "/usr/share/fonts/truetype/georgia/georgia.ttf",
    "/System/Library/Fonts/Georgia.ttf",
]
FONT_SIZE_TITLE = 60
FONT_SIZE_BODY = 48
FONT_SIZE_CTA = 42
SLIDE_SIZE = (1080, 1080)


def load_font(size):
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def create_slide(text, slide_type="body", output_path="slide.png"):
    img = Image.new("RGB", SLIDE_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = load_font(FONT_SIZE_TITLE)
    font_body = load_font(FONT_SIZE_BODY)
    font_cta = load_font(FONT_SIZE_CTA)

    if slide_type == "hook":
        lines = textwrap.wrap(text, width=20)
        y = (SLIDE_SIZE[1] - len(lines) * FONT_SIZE_TITLE) // 2
        for line in lines:
            w = draw.textlength(line, font=font_title)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=font_title, fill=ACCENT_COLOR)
            y += FONT_SIZE_TITLE
    elif slide_type == "cta":
        lines = textwrap.wrap(text, width=25)
        y = SLIDE_SIZE[1] - len(lines) * FONT_SIZE_CTA - 80
        for line in lines:
            w = draw.textlength(line, font=font_cta)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=font_cta, fill=TEXT_COLOR)
            y += FONT_SIZE_CTA
    else:
        lines = textwrap.wrap(text, width=22)
        y = (SLIDE_SIZE[1] - len(lines) * FONT_SIZE_BODY) // 2
        for line in lines:
            w = draw.textlength(line, font=font_body)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=font_body, fill=TEXT_COLOR)
            y += FONT_SIZE_BODY

    img.save(output_path)
    print(f"  Saved: {output_path}")


def generate_carousel(hook, insights, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    create_slide(hook, "hook", os.path.join(output_dir, "slide_01.png"))
    for i, insight in enumerate(insights[:7], start=2):
        create_slide(insight, "body", os.path.join(output_dir, f"slide_{i:02d}.png"))
    create_slide("Remember this.", "body", os.path.join(output_dir, "slide_09.png"))
    cta = ("Save this for later.\n"
           "Follow @Hermes for more insights.\n"
           "Which one hit you hardest?")
    create_slide(cta, "cta", os.path.join(output_dir, "slide_10.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Hermes Instagram carousel.")
    parser.add_argument("--hook", required=True, help="Hook text for slide 1")
    parser.add_argument("--insights", required=True, help="Newline-separated insights")
    parser.add_argument("--output_dir", default="./output", help="Output directory")
    args = parser.parse_args()
    insights_list = [i.strip() for i in args.insights.split("\n") if i.strip()]
    generate_carousel(args.hook, insights_list, args.output_dir)
