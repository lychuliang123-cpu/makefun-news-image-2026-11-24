#!/usr/bin/env python3
"""Generate the 1024x1024 daily-news infographic for the make.fun
'Sum up 24 November's world news in one image' bounty (news-image-20261124).

Deterministic: same input -> same PNG bytes. Rendered locally with PIL
(no AI image generator, so the text cannot come out garbled).
News lines are the six items from the brief prepared 2026-11-25 07:30.
Run: python3 generate_image.py  ->  writes news.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news.png")

W, H = 1024, 1024
NAVY = (13, 27, 46)        # background
CARD = (22, 40, 63)        # card fill
CARD_EDGE = (36, 64, 95)   # card border
ORANGE = (249, 115, 22)    # header band / number badges (user's favourite colour)
WHITE = (255, 255, 255)
BODY = (199, 210, 222)
MUTED = (148, 163, 184)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (headline, one factual line, <=12 words each)
STORIES = [
    ("Huang returns as Nvidia CEO",
     "Board reinstates him after exit; shares jump ~30%."),
    ("Three tankers hit mines in Hormuz",
     "Iran refuses talks; US naval blockade continues."),
    ("Russian strike hits Zaporizhzhia",
     "Two killed, about 40 wounded, including four children."),
    ("Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel and six others killed in Gaza."),
    ("COP31 climate talks collapse",
     "No deal on fossil fuels; negotiations end empty."),
    ("South Korea pays to catch AI cheaters",
     "$375,000 reward for tips on AI use in exams."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 108], fill=ORANGE)
    f_head = font(FONT_BOLD, 46)
    title = "THE WORLD TODAY \u2014 NOV 24, 2026"
    tw = d.textlength(title, font=f_head)
    d.text(((W - tw) / 2, 28), title, font=f_head, fill=WHITE)
    f_sub = font(FONT_REG, 20)
    sub = "Six stories that defined Tuesday, 24 November 2026"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 132), sub, font=f_sub, fill=MUTED)

    # Grid: 2 cols x 3 rows
    margin, gap = 24, 16
    top = 168
    bottom = 984
    col_w = (W - 2 * margin - gap) // 2
    row_h = (bottom - top - 2 * gap) // 3
    f_num = font(FONT_BOLD, 26)
    f_hl = font(FONT_BOLD, 27)
    f_body = font(FONT_REG, 20)

    for i, (headline, fact) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (col_w + gap)
        y0 = top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                            outline=CARD_EDGE, width=2)
        # Number badge
        cx, cy, r = x0 + 34, y0 + 36, 22
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)
        num = str(i + 1)
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, cy - 18), num, font=f_num, fill=WHITE)
        # Headline (max 2 lines) and fact (max 3 lines)
        tx = x0 + 68
        max_w = x1 - tx - 20
        hl_lines = wrap(d, headline, f_hl, max_w)[:2]
        y = y0 + 18
        for line in hl_lines:
            d.text((tx, y), line, font=f_hl, fill=WHITE)
            y += 34
        y += 6
        for line in wrap(d, fact, f_body, max_w)[:3]:
            d.text((tx, y), line, font=f_body, fill=BODY)
            y += 27

    # Footer
    f_foot = font(FONT_REG, 15)
    foot = "Sources: public news wires, 24 Nov 2026  \u00b7  One image, six stories"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 996), foot, font=f_foot, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
