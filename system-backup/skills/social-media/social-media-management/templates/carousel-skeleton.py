#!/usr/bin/env python3
"""
Carousel skeleton — copy this to start a new brand's carousel generator.

Customize:
  1. BG_COLOR, TEXT_COLOR, ACCENT_COLOR to match brand palette
  2. FONT_PATHS to match available fonts
  3. FONT_SIZE_* to match visual hierarchy
  4. CTA text template
  5. Slide content layout if not centered text
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import argparse

# === BRAND CONSTANTS (customize) ===
BG_COLOR = "#0A0A0A"
TEXT_COLOR = "#F5F5F5"
ACCENT_COLOR = "#C9A94E"
FONT_PATHS = ["C:/Windows/Fonts/Georgia.ttf"]
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
    ft = load_font(FONT_SIZE_TITLE)
    fb = load_font(FONT_SIZE_BODY)
    fc = load_font(FONT_SIZE_CTA)

    if slide_type == "hook":
        lines = textwrap.wrap(text, width=20)
        y = (SLIDE_SIZE[1] - len(lines) * FONT_SIZE_TITLE) // 2
        for line in lines:
            w = draw.textlength(line, font=ft)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=ft, fill=ACCENT_COLOR)
            y += FONT_SIZE_TITLE
    elif slide_type == "cta":
        lines = textwrap.wrap(text, width=25)
        y = SLIDE_SIZE[1] - len(lines) * FONT_SIZE_CTA - 80
        for line in lines:
            w = draw.textlength(line, font=fc)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=fc, fill=TEXT_COLOR)
            y += FONT_SIZE_CTA
    else:
        lines = textwrap.wrap(text, width=22)
        y = (SLIDE_SIZE[1] - len(lines) * FONT_SIZE_BODY) // 2
        for line in lines:
            w = draw.textlength(line, font=fb)
            draw.text(((SLIDE_SIZE[0] - w) // 2, y), line, font=fb, fill=TEXT_COLOR)
            y += FONT_SIZE_BODY
    img.save(output_path)


def generate_carousel(hook, insights, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    create_slide(hook, "hook", os.path.join(output_dir, "slide_01.png"))
    for i, insight in enumerate(insights[:7], start=2):
        create_slide(insight, "body", os.path.join(output_dir, f"slide_{i:02d}.png"))
    create_slide("Conclusion.", "body", os.path.join(output_dir, "slide_09.png"))
    cta = ("Save this.\nFollow @Brand for more.\nWhich resonated?")
    create_slide(cta, "cta", os.path.join(output_dir, "slide_10.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hook", required=True)
    parser.add_argument("--insights", required=True)
    parser.add_argument("--output_dir", default="./output")
    args = parser.parse_args()
    generate_carousel(args.hook, [i.strip() for i in args.insights.split("\n") if i.strip()], args.output_dir)
