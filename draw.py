#!/usr/bin/env python3
"""Draw the v3 front page for Thursday 19 November 2026.

A 1024x1024 PNG broadsheet drawn with Pillow: masthead, a full-width
hero on the first-ever Trump-Xi-Putin trilateral, two half-width stories
(ICJ genocide verdict, GTA VI launch) and three third-width stories
(Anthropic IPO, PIF Tower strike, Gaza raid / Crimean Bridge).

Every fact was re-verified against live reporting on 20 November 2026:
  - Shenzhen: first-ever trilateral, 90 minutes at Kylin Villa, joint
    statement the leaders called a "Peace Declaration"; a nuclear war
    "cannot be won and must never be fought" (USA Today, The Times).
  - ICJ: 9-6, first time the court has held a state guilty of genocide;
    reparations ordered (HRW, CNN, Le Monde).
  - GTA VI: Sensor Tower estimates $2.36bn and 24.6m copies on day one,
    the biggest entertainment launch ever (NotebookCheck, CNN).
  - Anthropic: record $81.3bn IPO at $83; opened $111.50, closed $97.17,
    up 17% (WSJ, Reuters, Finnhub).
  - PIF Tower: Houthi missile struck Riyadh's 80-storey PIF Tower,
    windows blown out on 7-8 floors, no injuries (Reuters, WSJ).
  - Gaza/Crimea: Israel concluded its first tank raid past the Yellow
    Line since the October 2025 truce; Ukraine hit the Crimean Bridge
    again, third attack that week (Reuters, BBC).

Deterministic: no network, no clock, no randomness. Running this file
twice writes byte-identical PNGs.

    python3 draw.py            # writes entry.png next to this file
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (22, 35, 63)
NAVY = (21, 38, 66)
NAVY_DARK = (15, 27, 48)
CRIMSON = (163, 22, 33)
GOLD = (201, 154, 38)
GOLD_LIGHT = (217, 165, 33)
TEAL = (15, 118, 110)
GREY = (90, 92, 96)
WHITE = (255, 255, 255)
CREAM = (250, 247, 238)

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF = FONT_DIR / "noto/NotoSerif-Bold.ttf"
SERIF_REG = FONT_DIR / "noto/NotoSerif-Regular.ttf"
SERIF_IT = FONT_DIR / "noto/NotoSerif-Italic.ttf"
SANS = FONT_DIR / "noto/NotoSans-Regular.ttf"
SANS_BOLD = FONT_DIR / "noto/NotoSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (str(path), size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(path), size)
    return _cache[key]


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, bg, size=19, pad_x=12, pad_y=6):
    """A coloured chip with a white bold label; returns its right edge."""
    fnt = font(SANS_BOLD, size)
    tw = text_w(draw, label, fnt)
    w = int(tw) + 2 * pad_x
    h = size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), label, font=fnt, fill=WHITE)
    return x + w


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=CREAM, outline=INK, width=2)


def centre(draw, cx, y, text, fnt, fill):
    tw = text_w(draw, text, fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- flags

def flag_usa(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(30, 58, 95))
    for r in range(5):
        n = 6 if r % 2 == 0 else 5
        for s in range(n):
            sx = x + 6 + s * (cw - 10) / 5.0 + (0 if r % 2 == 0 else (cw - 10) / 10.0)
            sy = y + 5 + r * (ch - 8) / 4.0
            draw.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=WHITE)


def star(draw, cx, cy, r, fill):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.18, y + h * 0.28, h * 0.17, GOLD_LIGHT)
    for sx, sy in [(0.42, 0.12), (0.52, 0.24), (0.50, 0.42), (0.38, 0.48)]:
        star(draw, x + w * sx, y + h * sy, h * 0.07, GOLD_LIGHT)


def flag_russia(draw, x, y, w, h):
    third = h / 3.0
    for i, c in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)


def flag_pole(draw, x, y_top, y_base, flag_fn, fw, fh):
    draw.line([x, y_top, x, y_base], fill=(60, 48, 32), width=4)
    draw.ellipse([x - 4, y_top - 5, x + 4, y_top + 3], fill=GOLD)
    flag_fn(draw, x + 3, y_top + 4, fw, fh)


# ------------------------------------------------------------ hero scene

def hero_scene(draw, x, y, w, h):
    """Three flags over a round table, on a pale sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    # flags
    fw, fh = 104, 62
    flag_pole(draw, x + 34, y + 22, y + h - 118, flag_usa, fw, fh)
    flag_pole(draw, x + w // 2 - 52, y + 10, y + h - 118, flag_china, fw, fh)
    flag_pole(draw, x + w - 142, y + 22, y + h - 118, flag_russia, fw, fh)
    # round table
    ty = y + h - 118
    draw.ellipse([x + 30, ty, x + w - 30, ty + 44], fill=(122, 82, 48))
    draw.ellipse([x + 30, ty, x + w - 30, ty + 26], fill=(150, 104, 62))
    draw.rectangle([x + w // 2 - 8, ty + 30, x + w // 2 + 8, y + h - 42],
                   fill=(90, 60, 34))
    # three seated leaders behind the table (head + shoulders)
    for cx in (x + 86, x + w // 2, x + w - 90):
        draw.ellipse([cx - 13, ty - 72, cx + 13, ty - 46], fill=(31, 42, 68))
        draw.polygon([(cx - 26, ty - 6), (cx - 22, ty - 48),
                      (cx + 22, ty - 48), (cx + 26, ty - 6)],
                     fill=(31, 42, 68))
    centre(draw, x + w // 2, y + h - 32, "KYLIN VILLA \u00b7 SHENZHEN",
           font(SANS_BOLD, 17), TEAL)


# ------------------------------------------------------------ story bands

def icj_band(draw, x, y, w, h):
    """Courthouse columns with a big 9-6 verdict."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # pediment
    draw.polygon([(x + 18, y + 12), (x + w - 18, y + 12),
                  (x + w // 2, y + 34)], fill=GOLD)
    draw.rectangle([x + 18, y + 34, x + w - 18, y + 40], fill=GOLD)
    # columns
    col_w, gap = 16, (w - 36 - 5 * 16) / 4.0
    for i in range(5):
        cx0 = x + 18 + i * (16 + gap)
        draw.rectangle([cx0, y + 40, cx0 + col_w, y + h - 8], fill=(232, 226, 208))
    draw.rectangle([x + 18, y + h - 8, x + w - 18, y + h - 2], fill=GOLD)
    # verdict badge on the right, inside the band
    bx, by = x + w - 82, y + 12
    draw.ellipse([bx, by, bx + 64, by + 64], fill=CRIMSON,
                 outline=WHITE, width=3)
    centre(draw, bx + 32, by + 15, "9\u20136", font(SERIF, 30), WHITE)


def gta_band(draw, x, y, w, h):
    """Sunset skyline with a giant VI and a palm."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(255 + (124 - 255) * t)
        g = int(94 + (58 - 94) * t)
        b = int(60 + (237 - 60) * t)
        draw.line([x, y + i, x + w, y + i], fill=(r, g, b))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 52, 34), (58, 40, 52), (104, 62, 30),
                       (172, 44, 62), (222, 56, 40), (284, 48, 56),
                       (338, 58, 34), (402, 46, 48)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(38, 16, 68))
    # palm
    px = x + w - 66
    draw.line([px, base, px + 14, base - 74], fill=(38, 16, 68), width=5)
    for ang in range(-70, 71, 28):
        import math
        a = math.radians(ang - 90)
        ex = px + 14 + 44 * math.cos(a)
        ey = base - 74 + 44 * math.sin(a) * 0.55
        draw.line([px + 14, base - 74, ex, ey], fill=(38, 16, 68), width=4)
    # giant VI
    draw.text((x + 16, y + 2), "VI", font=font(SERIF, 92), fill=WHITE)


def ipo_band(draw, x, y, w, h):
    """Rising bars with a steep arrow and the raise in big type."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 52, 38))
    draw.text((x + 12, y + 2), "$81.3BN", font=font(SERIF, 30), fill=WHITE)
    draw.text((x + w - 104, y + 8), "ANT +17%", font=font(SANS_BOLD, 17),
              fill=(120, 220, 170))
    base = y + h - 6
    bars = [10, 15, 13, 20, 26, 32]
    bw = 30
    for i, bh in enumerate(bars):
        bx = x + 16 + i * 42
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(46, 160, 110))
    # arrow above the bars
    pts = [(x + 16, base - 12), (x + 62, base - 20), (x + 104, base - 18),
           (x + 152, base - 30), (x + 200, base - 34), (x + 246, base - 46)]
    draw.line(pts, fill=(217, 60, 48), width=4, joint="curve")
    draw.polygon([(x + 246, base - 46), (x + 228, base - 50),
                  (x + 242, base - 32)], fill=(217, 60, 48))


def tower_band(draw, x, y, w, h):
    """The PIF Tower at night, windows blown out, missile arc above."""
    draw.rectangle([x, y, x + w, y + h], fill=(13, 22, 44))
    # stars
    for sx, sy in [(24, 14), (70, 30), (150, 10), (210, 26), (262, 12),
                   (40, 44), (120, 40), (200, 48), (280, 38)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    # missile arc with smoke dots
    import math
    for t in range(0, 21):
        f = t / 20.0
        mx = x + 12 + f * (w - 60)
        my = y + 34 - 22 * math.sin(f * math.pi)
        r = 2 + int(2 * f)
        draw.ellipse([mx - r, my - r, mx + r, my + r],
                     fill=(200, 200, 200) if t % 2 else (150, 150, 150))
    # tower: tapered, lit windows, broken band — fills the band height
    tx, tw = x + w // 2 - 44, 88
    draw.polygon([(tx, y + h), (tx + 10, y + 12), (tx + tw - 10, y + 12),
                  (tx + tw, y + h)], fill=(58, 74, 104))
    for row in range(5):
        wy = y + 20 + row * 11
        for col in range(5):
            wx = tx + 14 + col * 13
            c = (255, 214, 120) if (row + col) % 2 else (140, 160, 190)
            draw.rectangle([wx, wy, wx + 8, wy + 6], fill=c)
    # broken-window band
    by = y + 46
    draw.rectangle([tx + 5, by, tx + tw - 5, by + 16], fill=(30, 30, 34))
    for k in range(6):
        draw.line([tx + 9 + k * 13, by + 3, tx + 15 + k * 13, by + 13],
                  fill=(255, 214, 120), width=2)


def war_band(draw, x, y, w, h):
    """Two mini-scenes: a tank past a yellow line, a bridge under fire."""
    mid = x + w // 2
    # Gaza half
    draw.rectangle([x, y, mid - 1, y + h], fill=(214, 196, 160))
    draw.text((x + 8, y + 4), "GAZA", font=font(SANS_BOLD, 14), fill=(90, 60, 20))
    # tank (shifted right so the barrel clears the GAZA label)
    tx, ty = x + 74, y + 24
    draw.rectangle([tx, ty, tx + 62, ty + 14], fill=(74, 74, 66))
    draw.rectangle([tx + 13, ty - 12, tx + 42, ty], fill=(74, 74, 66))
    draw.line([tx + 40, ty - 8, tx + 72, ty - 14], fill=(74, 74, 66), width=4)
    for wx in range(6):
        draw.ellipse([tx + 3 + wx * 10, ty + 14, tx + 11 + wx * 10, ty + 22],
                     fill=(40, 40, 36))
    # yellow line + label
    for i in range(0, w // 2 - 4, 18):
        draw.rectangle([x + 6 + i, y + 56, x + 14 + i, y + 61],
                       fill=(250, 200, 40))
    draw.text((x + 8, y + 63), "YELLOW LINE", font=font(SANS_BOLD, 11),
              fill=(90, 60, 20))
    # Crimea half
    draw.rectangle([mid + 1, y, x + w, y + h], fill=(24, 48, 84))
    draw.rectangle([mid + 1, y + h - 12, x + w, y + h], fill=(30, 90, 130))
    draw.text((mid + 8, y + 4), "CRIMEA", font=font(SANS_BOLD, 14), fill=WHITE)
    # explosion star above the bridge
    ex, ey = mid + (w // 2) // 2, y + 26
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        draw.line([ex, ey, ex + 18 * math.cos(a), ey + 18 * math.sin(a)],
                  fill=(255, 170, 40), width=4)
    draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 220, 120))
    # bridge deck + posts
    bx0, bx1 = mid + 10, x + w - 10
    by = y + h - 12
    draw.line([bx0, by, bx1, by], fill=(200, 200, 210), width=5)
    for px in range(bx0 + 8, bx1 - 8, 22):
        draw.line([px, by, px, by - 14], fill=(200, 200, 210), width=3)


# ---------------------------------------------------------------- layout

def headline(draw, lines, x, y, max_w, size, leading, fill=INK):
    """Draw serif-bold lines, shrinking until the widest fits max_w."""
    while size > 24:
        fnt = font(SERIF, size)
        if max(text_w(draw, ln, fnt) for ln in lines) <= max_w:
            break
        size -= 2
    fnt = font(SERIF, size)
    return draw_lines(draw, lines, x, y, fnt, fill, leading)


def story_text(draw, x, y, w, kicker_label, kicker_bg, head_lines,
               deck, head_size=33, deck_size=19, kicker_size=16):
    kicker(draw, x, y, kicker_label, kicker_bg, size=kicker_size)
    hy = y + kicker_size + 14
    hy = headline(draw, head_lines, x, hy, w, head_size,
                  head_size + 3)
    dy = hy + 6
    fnt = font(SANS, deck_size)
    lines = wrap(draw, deck, fnt, w)
    draw_lines(draw, lines, x, dy, fnt, (52, 52, 54), deck_size + 3)
    return dy + len(lines) * (deck_size + 3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 112], fill=NAVY)
    centre(d, W // 2, 14, "THE WORLD IN ONE DAY", font(SERIF, 58), WHITE)
    centre(d, W // 2, 76, "THURSDAY \u00b7 19 NOVEMBER 2026",
           font(SANS_BOLD, 26), GOLD_LIGHT)
    d.rectangle([0, 112, W, 117], fill=CRIMSON)

    # ---- standfirst
    centre(d, W // 2, 128,
           "Three nuclear powers at one table, a genocide verdict, and the "
           "biggest launch in entertainment history.",
           font(SERIF_IT, 21), INK)

    # ---- hero: Shenzhen summit
    hx, hy, hw, hh = 24, 160, 976, 300
    panel(d, hx, hy, hw, hh)
    kicker(d, hx + 20, hy + 16, "01 \u00b7 SHENZHEN SUMMIT", CRIMSON, size=19)
    headline(d, ["TRUMP, XI AND PUTIN", "MEET FOR THE FIRST", "TIME"],
             hx + 20, hy + 52, 516, 50, 56)
    deck = ("Ninety minutes at Kylin Villa \u2014 then a joint statement "
            "they called a \u201cPeace Declaration\u201d: a nuclear war "
            "\u201ccannot be won and must never be fought\u201d.")
    fnt = font(SANS, 20)
    draw_lines(d, wrap(d, deck, fnt, 516), hx + 20, hy + 226, fnt,
               (52, 52, 54), 25)
    hero_scene(d, hx + 576, hy + 16, 384, 268)

    # ---- row 2: ICJ + GTA VI
    ry, rh = 472, 260
    # 02 ICJ
    x, w = 24, 476
    panel(d, x, ry, w, rh)
    icj_band(d, x + 8, ry + 8, w - 16, 88)
    story_text(d, x + 16, ry + 104, w - 32, "02 \u00b7 THE HAGUE", NAVY,
               ["MYANMAR GUILTY OF", "GENOCIDE"],
               "The world court ruled 9\u20136 \u2014 the first time it has "
               "ever held a state guilty of genocide.",
               head_size=33, deck_size=19)
    # 03 GTA VI
    x, w = 524, 476
    panel(d, x, ry, w, rh)
    gta_band(d, x + 8, ry + 8, w - 16, 88)
    story_text(d, x + 16, ry + 104, w - 32, "03 \u00b7 ENTERTAINMENT",
               (94, 46, 130),
               ["GTA VI SMASHES EVERY", "RECORD"],
               "An estimated $2.36bn on day one \u2014 24.6m copies. The "
               "biggest entertainment launch ever.",
               head_size=33, deck_size=19)

    # ---- row 3: IPO + PIF Tower + war updates
    ry, rh = 744, 232
    # 04 Anthropic
    x, w = 24, 320
    panel(d, x, ry, w, rh)
    ipo_band(d, x + 8, ry + 8, w - 16, 80)
    story_text(d, x + 14, ry + 94, w - 28, "04 \u00b7 WALL STREET",
               (16, 94, 58),
               ["THE BIGGEST IPO", "EVER"],
               "Record $81.3bn at $83 a share; \u201cANT\u201d closed up "
               "17% at $97.17.",
               head_size=28, deck_size=17, kicker_size=15)
    # 05 PIF Tower
    x, w = 352, 320
    panel(d, x, ry, w, rh)
    tower_band(d, x + 8, ry + 8, w - 16, 80)
    story_text(d, x + 14, ry + 94, w - 28, "05 \u00b7 MIDDLE EAST", CRIMSON,
               ["MISSILE HITS", "RIYADH TOWER"],
               "Houthi missile hit the PIF Tower; 7\u20138 floors damaged. "
               "No injuries.",
               head_size=28, deck_size=17, kicker_size=15)
    # 06 war updates
    x, w = 680, 320
    panel(d, x, ry, w, rh)
    war_band(d, x + 8, ry + 8, w - 16, 80)
    story_text(d, x + 14, ry + 94, w - 28, "06 \u00b7 WAR UPDATES", NAVY,
               ["RAID ENDS; BRIDGE", "HIT AGAIN"],
               "Israel\u2019s Gaza raid ended; Ukraine hit the Crimean "
               "Bridge again.",
               head_size=28, deck_size=17, kicker_size=15)

    # ---- footer
    centre(d, W // 2, 986,
           "Sources: Reuters \u00b7 WSJ \u00b7 CNN \u00b7 Human Rights Watch "
           "\u00b7 Sensor Tower \u00b7 Le Monde \u2014 19 November 2026",
           font(SANS, 15), GREY)
    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    build().save(out, format="PNG", optimize=False)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
