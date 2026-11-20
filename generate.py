#!/usr/bin/env python3
"""Render the 20 November 2026 world-news magazine cover.

Draws one 1024x1024 PNG with Pillow from the verified headlines in
STORIES.md (workspace, not the repo). Deterministic: fixed text, fixed
geometry, no clock, no randomness, no network. Run: python3 generate.py
writes assets/entry.png next to this file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"
OUT = HERE / "assets" / "entry.png"

W = H = 1024

PAPER = (246, 241, 231)
NAVY = (14, 34, 68)
NAVY_HERO = (18, 41, 77)
NAVY_LINE = (32, 58, 96)
GOLD = (201, 162, 39)
GOLD_SOFT = (226, 196, 110)
RED = (180, 35, 24)
INK = (20, 28, 40)
GRAY = (88, 94, 106)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
CARD_EDGE = (214, 206, 188)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"


def fit(draw, text, fname, size, max_w):
    """Largest font size at or under `size` that fits `text` in max_w."""
    while size > 10:
        f = font(fname, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(fname, 10)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def globe(draw, cx, cy, r):
    """Gold wireframe globe: filled disc, meridians, parallels, equator."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY_LINE)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=6)
    # Parallels (horizontal chords) and meridians (vertical ellipses).
    for frac in (-0.62, -0.31, 0.0, 0.31, 0.62):
        y = cy + frac * r
        half = (r * r - (frac * r) ** 2) ** 0.5
        draw.line([cx - half, y, cx + half, y], fill=GOLD_SOFT, width=3)
    for squish in (0.33, 0.66, 1.0):
        w = r * squish
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=GOLD_SOFT, width=3)
    # Land hint: three small gold discs as abstract continents.
    for ox, oy, rr in ((-0.38, -0.22, 0.16), (0.30, 0.05, 0.20), (-0.05, 0.42, 0.13)):
        draw.ellipse(
            [cx + ox * r - rr * r, cy + oy * r - rr * r,
             cx + ox * r + rr * r, cy + oy * r + rr * r],
            fill=GOLD,
        )


def masthead(draw):
    draw.rectangle([0, 0, W, 132], fill=NAVY)
    draw.rectangle([0, 132, W, 140], fill=GOLD)
    title = fit(draw, "THE WORLD TODAY", BOLD, 78, 660)
    draw.text((36, 34), "THE WORLD TODAY", font=title, fill=WHITE)
    date_f = font(BOLD, 24)
    draw.text((W - 36, 30), "FRIDAY", font=date_f, fill=GOLD_SOFT, anchor="ra")
    draw.text((W - 36, 62), "20 NOVEMBER 2026", font=date_f, fill=WHITE, anchor="ra")


def hero(draw):
    draw.rectangle([28, 156, W - 28, 592], fill=NAVY_HERO)
    draw.rectangle([28, 156, W - 28, 592], outline=GOLD, width=3)
    globe(draw, 210, 372, 138)
    cap = font(BOLD, 24)
    label = "SHENZHEN  •  CHINA"
    tw = draw.textlength(label, font=cap)
    draw.text((210 - tw / 2, 528), label, font=cap, fill=GOLD_SOFT)

    x = 400
    kick = font(BOLD, 30)
    draw.text((x, 186), "THE SUMMIT OF THE CENTURY", font=kick, fill=GOLD)
    big = font(BOLD, 96)
    draw.text((x, 226), "THREE", font=big, fill=WHITE)
    draw.text((x, 322), "LEADERS,", font=big, fill=WHITE)
    draw.text((x, 418), "ONE TABLE", font=big, fill=GOLD_SOFT)
    deck = font(REG, 27)
    lines = wrap(
        draw,
        "Trump, Xi and Putin meet — and sign a joint peace declaration.",
        deck, W - 28 - x - 36,
    )
    y = 524
    for line in lines[:2]:
        draw.text((x, y), line, font=deck, fill=(214, 222, 235))
        y += 34


STRIPS = [
    ("01", RED, "UN COURT: MYANMAR COMMITTED GENOCIDE",
     "Ruling: the army intended to destroy the Rohingya minority"),
    ("02", NAVY, "ANTHROPIC'S $1.5 TRILLION DEBUT",
     "First pure-AI company lists — Wall Street's biggest AI bet yet"),
    ("03", NAVY, "EUROPE READY TO TALK TO RUSSIA",
     "Allies open the door to negotiations to end the Ukraine war"),
    ("04", NAVY, "BOAT SINKS OFF SENEGAL",
     "Dozens missing after a migrant boat goes down"),
]


def strips(draw):
    y = 608
    for num, bar, head, deck in STRIPS:
        draw.rectangle([28, y, W - 28, y + 78], fill=CARD, outline=CARD_EDGE, width=2)
        draw.rectangle([28, y, 40, y + 78], fill=bar)
        nf = font(BOLD, 30)
        draw.text((58, y + 22), num, font=nf, fill=bar)
        hf = fit(draw, head, BOLD, 33, W - 28 - 150)
        draw.text((148, y + 8), head, font=hf, fill=INK)
        df = fit(draw, deck, REG, 25, W - 28 - 150)
        draw.text((148, y + 44), deck, font=df, fill=GRAY)
        y += 90


def footer(draw):
    draw.rectangle([0, 968, W, H], fill=RED)
    f = fit(draw, "ALSO TODAY:  CYCLONE AKVAN BEARS DOWN ON INDIA — 80,000 EVACUATED",
            BOLD, 27, W - 48)
    draw.text((24, 984), "ALSO TODAY:  CYCLONE AKVAN BEARS DOWN ON INDIA — 80,000 EVACUATED",
              font=f, fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    hero(draw)
    strips(draw)
    footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
