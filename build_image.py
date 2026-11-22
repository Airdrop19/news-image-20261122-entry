"""Build entry.png: a one-page front page summing up world news of Sunday 22 November 2026.

Drawn with Pillow at 1024x1024. Every headline below was reported on 22 Nov 2026
(One Turn day page + Reuters world summary of that date). Claims are worded as claims.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (20, 33, 61)
MUTED = (90, 96, 110)
RED = (179, 58, 58)
TEAL = (20, 112, 122)
GOLD = (180, 134, 0)
GREEN = (46, 125, 72)
PURPLE = (101, 74, 158)
BROWN = (146, 90, 32)
CARD_BG = (255, 253, 247)
LINE = (205, 198, 180)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text(draw, xy, text, fnt, fill, max_w, line_gap=4, max_lines=3):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


# ---------- simple flat icons (drawn inside a circle of radius r at cx, cy) ----------
def icon_drone(d, cx, cy, r, c):
    d.line([(cx - r * .7, cy - r * .7), (cx + r * .7, cy + r * .7)], fill=c, width=4)
    d.line([(cx - r * .7, cy + r * .7), (cx + r * .7, cy - r * .7)], fill=c, width=4)
    for dx, dy in [(-.7, -.7), (.7, -.7), (-.7, .7), (.7, .7)]:
        d.ellipse([cx + dx * r - 6, cy + dy * r - 6, cx + dx * r + 6, cy + dy * r + 6], fill=c)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=c)


def icon_ship(d, cx, cy, r, c):
    d.polygon([(cx - r * .85, cy + r * .15), (cx + r * .85, cy + r * .15),
               (cx + r * .6, cy + r * .6), (cx - r * .6, cy + r * .6)], fill=c)
    d.rectangle([cx - r * .35, cy - r * .25, cx + r * .2, cy + r * .12], fill=c)
    d.line([(cx + r * .45, cy - r * .7), (cx + r * .45, cy + r * .1)], fill=c, width=5)
    d.polygon([(cx + r * .45, cy - r * .7), (cx + r * .8, cy - r * .5), (cx + r * .45, cy - r * .3)], fill=RED)


def icon_scales(d, cx, cy, r, c):
    d.line([(cx, cy - r * .75), (cx, cy + r * .6)], fill=c, width=5)
    d.line([(cx - r * .75, cy - r * .55), (cx + r * .75, cy - r * .55)], fill=c, width=5)
    for sx in (-1, 1):
        px = cx + sx * r * .75
        d.line([(px, cy - r * .55), (px - r * .3, cy + r * .05)], fill=c, width=3)
        d.line([(px, cy - r * .55), (px + r * .3, cy + r * .05)], fill=c, width=3)
        d.arc([px - r * .32, cy - r * .05, px + r * .32, cy + r * .4], 0, 180, fill=c, width=4)
    d.line([(cx - r * .4, cy + r * .7), (cx + r * .4, cy + r * .7)], fill=c, width=5)


def icon_flame(d, cx, cy, r, c):
    d.polygon([(cx, cy - r * .85), (cx + r * .55, cy + r * .1), (cx + r * .3, cy + r * .7),
               (cx - r * .3, cy + r * .7), (cx - r * .55, cy + r * .1)], fill=RED)
    d.polygon([(cx, cy - r * .25), (cx + r * .28, cy + r * .25), (cx, cy + r * .6),
               (cx - r * .28, cy + r * .25)], fill=(240, 170, 60))


def icon_car(d, cx, cy, r, c):
    d.rounded_rectangle([cx - r * .8, cy - r * .05, cx + r * .8, cy + r * .45], 8, fill=c)
    d.polygon([(cx - r * .5, cy - r * .05), (cx - r * .25, cy - r * .5),
               (cx + r * .3, cy - r * .5), (cx + r * .55, cy - r * .05)], fill=c)
    for wx in (-.45, .45):
        d.ellipse([cx + wx * r - 9, cy + r * .32, cx + wx * r + 9, cy + r * .32 + 18], fill=INK)
    icon_flame(d, cx + r * .55, cy - r * .45, r * .38, c)


def icon_handshake_x(d, cx, cy, r, c):
    d.rectangle([cx - r * .8, cy - r * .15, cx - r * .05, cy + r * .2], fill=c)
    d.rectangle([cx + r * .05, cy - r * .15, cx + r * .8, cy + r * .2], fill=c)
    d.line([(cx - r * .35, cy - r * .7), (cx + r * .35, cy + r * .7)], fill=RED, width=7)
    d.line([(cx - r * .35, cy + r * .7), (cx + r * .35, cy - r * .7)], fill=RED, width=7)


def icon_ballot(d, cx, cy, r, c):
    d.rectangle([cx - r * .7, cy - r * .1, cx + r * .7, cy + r * .7], fill=c)
    d.rectangle([cx - r * .35, cy - r * .85, cx + r * .35, cy - r * .15], fill=(255, 255, 255), outline=c, width=3)
    d.line([(cx - r * .2, cy - r * .55), (cx - r * .02, cy - r * .35), (cx + r * .22, cy - r * .68)], fill=GREEN, width=5)
    d.rectangle([cx - r * .45, cy + r * .18, cx + r * .45, cy + r * .3], fill=PAPER)


def icon_doc_check(d, cx, cy, r, c):
    d.rectangle([cx - r * .5, cy - r * .8, cx + r * .5, cy + r * .8], fill=(255, 255, 255), outline=c, width=4)
    for i, yy in enumerate((-.45, -.15, .15)):
        d.line([(cx - r * .32, cy + yy * r), (cx + r * .32, cy + yy * r)], fill=MUTED, width=3)
    d.line([(cx - r * .25, cy + r * .42), (cx - r * .05, cy + r * .62), (cx + r * .3, cy + r * .3)], fill=GREEN, width=6)


def icon_exam(d, cx, cy, r, c):
    d.rectangle([cx - r * .55, cy - r * .8, cx + r * .55, cy + r * .8], fill=(255, 255, 255), outline=c, width=4)
    d.text((cx - r * .3, cy - r * .55), "AI", font=font(SANS_B, int(r * .8)), fill=RED)
    d.line([(cx - r * .32, cy + r * .1), (cx + r * .32, cy + r * .1)], fill=MUTED, width=3)
    d.line([(cx - r * .32, cy + r * .38), (cx + r * .32, cy + r * .38)], fill=MUTED, width=3)


def icon_dome(d, cx, cy, r, c):
    d.arc([cx - r * .7, cy - r * .75, cx + r * .7, cy + r * .45], 180, 360, fill=c, width=6)
    d.line([(cx, cy - r * .9), (cx, cy - r * .65)], fill=c, width=5)
    d.rectangle([cx - r * .8, cy + r * .05, cx + r * .8, cy + r * .25], fill=c)
    for i in range(-2, 3):
        d.line([(cx + i * r * .3, cy + r * .28), (cx + i * r * .3, cy + r * .6)], fill=c, width=5)
    d.line([(cx - r * .85, cy + r * .68), (cx + r * .85, cy + r * .68)], fill=c, width=5)


def icon_star(d, cx, cy, r, c):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r * .85 if i % 2 == 0 else r * .38
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=c)


def icon_flag(d, cx, cy, r, c):
    d.line([(cx - r * .6, cy - r * .8), (cx - r * .6, cy + r * .8)], fill=c, width=5)
    sq = r * .42
    for row in range(3):
        for col in range(3):
            fill = INK if (row + col) % 2 == 0 else (255, 255, 255)
            x0 = cx - r * .6 + col * sq
            y0 = cy - r * .8 + row * sq
            d.rectangle([x0, y0, x0 + sq, y0 + sq], fill=fill, outline=c, width=1)


def icon_globe(d, cx, cy, r, c):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)
    d.ellipse([cx - r * .45, cy - r, cx + r * .45, cy + r], outline=c, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=c, width=3)
    d.arc([cx - r, cy - r * .55, cx + r, cy + r * .55], 0, 180, fill=c, width=3)
    d.arc([cx - r, cy - r * .55, cx + r, cy + r * .55], 180, 360, fill=c, width=3)


# ---------- layout ----------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=INK)
d.text((28, 14), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52), fill=PAPER)
d.text((28, 74), "Sunday 22 November 2026", font=font(SANS_B, 34), fill=(240, 200, 90))
tag = "23 stories from one day of world news"
d.text((W - 28 - d.textlength(tag, font=font(SANS_R, 19)), 82), tag, font=font(SANS_R, 19), fill=PAPER)

# Lead story: COP31
lead_y0, lead_y1 = 128, 308
d.rounded_rectangle([18, lead_y0, W - 18, lead_y1], 14, fill=(255, 248, 230), outline=GOLD, width=3)
icon_globe(d, 108, (lead_y0 + lead_y1) // 2, 62, TEAL)
d.text((196, lead_y0 + 14), "CLIMATE · ANTALYA, TURKEY", font=font(SANS_B, 18), fill=TEAL)
d.text((196, lead_y0 + 40), "COP31 ENDS WITH NO DEAL", font=font(SERIF_B, 46), fill=INK)
draw_text(d, (196, lead_y0 + 102),
          "EU and about 130 parties reject the draft: it never mentions fossil fuels. "
          "The longest UN climate summit on record ends two days late, with no agreement.",
          font(SANS_R, 21), INK, W - 196 - 250, line_gap=5, max_lines=4)
# NO DEAL stamp
stamp = Image.new("RGBA", (210, 84), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 206, 80], 10, outline=RED, width=6)
sd.text((28, 18), "NO DEAL", font=font(SANS_B, 42), fill=RED)
img.paste(stamp.rotate(12, expand=True), (W - 258, lead_y0 + 96), stamp.rotate(12, expand=True))

# Story cards: (region, color, headline, sublabel, icon)
CARDS = [
    ("EUROPE · UKRAINE", RED, "Drone hits flats near Kyiv",
     "Dymer: 14 missing after a Russian drone partly destroys an apartment block", icon_drone),
    ("EUROPE · LIBYA / FINLAND", TEAL, "Russian ships hit at sea",
     "Suspected Ukrainian sea drone strikes a corvette at Benghazi; Sparta II still burning off Finland", icon_ship),
    ("EUROPE · THE HAGUE", PURPLE, "ICJ: Myanmar genocide ruling",
     "World Court finds Myanmar responsible for genocide against the Rohingya", icon_scales),
    ("MIDDLE EAST · BAHRAIN", RED, "Iran strikes Bahrain site",
     "Industrial site hit, 2 hurt; Gulf states condemn. Iran says it targeted US air defences", icon_flame),
    ("MIDDLE EAST · WEST BANK", BROWN, "Settlers torch cars in villages",
     "Vehicles burnt near Ramallah overnight; Israel opens an inquiry", icon_car),
    ("MIDDLE EAST · ISRAEL", PURPLE, "Coalition talks end with no deal",
     "Likud and Eisenkot's party fail to agree who would lead the next government", icon_handshake_x),
    ("ASIA-PACIFIC · HONG KONG", TEAL, "Hong Kong votes, ~99% turnout",
     "Election Committee poll that picks the city's leader draws record turnout", icon_ballot),
    ("ASIA-PACIFIC · INDONESIA", GREEN, "EU–Indonesia trade deal signed",
     "Agreement after 10 years of talks removes 98.5% of tariffs on EU goods", icon_doc_check),
    ("ASIA-PACIFIC · SOUTH KOREA", BROWN, "Minister quits over AI exam row",
     "Education chief resigns after an AI cheating scandal shakes national exams", icon_exam),
    ("AMERICAS · UNITED STATES", PURPLE, "Democrats' biggest House majority since 1992",
     "At least 258 seats after a North Carolina recount; 4 races still undecided", icon_dome),
    ("AMERICAS · MEXICO", RED, "Mexico captures cartel boss",
     "'El Chapo Isidro', on the FBI most-wanted list, seized by special forces in Sinaloa", icon_star),
    ("SPORT · LAS VEGAS", GOLD, "Verstappen wins Las Vegas GP",
     "Third Vegas win in four years, in a race with 35 lead changes", icon_flag),
]

grid_y0, card_h, gap = 318, 120, 9
col_w = (W - 36 - 2 * gap) // 3
for i, (region, color, head, sub, icon) in enumerate(CARDS):
    col, row = i % 3, i // 3
    x0 = 18 + col * (col_w + gap)
    y0 = grid_y0 + row * (card_h + gap)
    d.rounded_rectangle([x0, y0, x0 + col_w, y0 + card_h], 10, fill=CARD_BG, outline=LINE, width=2)
    d.rectangle([x0, y0, x0 + col_w, y0 + 6], fill=color)
    d.ellipse([x0 + 10, y0 + 34, x0 + 66, y0 + 90], fill=(238, 240, 246))
    icon(d, x0 + 38, y0 + 62, 22, color)
    d.text((x0 + 12, y0 + 12), region, font=font(SANS_B, 13), fill=color)
    hy = draw_text(d, (x0 + 74, y0 + 30), head, font(SANS_B, 19), INK, col_w - 84, line_gap=2, max_lines=2)
    draw_text(d, (x0 + 74, hy + 1), sub, font(SANS_R, 14), MUTED, col_w - 84, line_gap=2, max_lines=3)

# Footer: also today
foot_y0 = grid_y0 + 4 * (card_h + gap) + 2
d.line([(18, foot_y0), (W - 18, foot_y0)], fill=INK, width=3)
d.text((18, foot_y0 + 8), "ALSO TODAY — SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 19), fill=INK)
ALSO = [
    "Sudan: drones hit Khartoum, UN building damaged",
    "Houthis claim Saudi refinery hit; missiles intercepted",
    "Gaza: Israeli strikes continue, civilians killed",
    "BepiColombo probe enters orbit around Mercury",
    "One-time CRISPR therapy cuts bad cholesterol by 52%",
    "AI sell-off: S&P 500 −3.7%, Japan's Nikkei −5.1%",
    "Nigeria: funeral boat capsizes, 24 dead",
    "Indonesia: Banten candy factory fire, 3 dead, dozens missing",
    "Australia: music broadcaster Molly Meldrum dies at 83",
    "Researcher claims AI helped prove the Riemann hypothesis",
]
col2_w = (W - 36 - 24) // 2
for i, line in enumerate(ALSO):
    col, row = i % 2, i // 2
    x = 18 + col * (col2_w + 24)
    y = foot_y0 + 38 + row * 24
    d.ellipse([x, y + 5, x + 9, y + 14], fill=RED)
    d.text((x + 17, y), line, font=font(SANS_R, 17), fill=INK)

note = "All stories happened or were first reported on 22 November 2026. Claims are shown as claims."
d.text((18, H - 30), note, font=font(SANS_R, 15), fill=MUTED)
d.text((W - 18 - d.textlength("22 NOV 2026", font=font(SANS_B, 15)), H - 30),
       "22 NOV 2026", font=font(SANS_B, 15), fill=INK)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
