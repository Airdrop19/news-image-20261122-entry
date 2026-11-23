"""Build entry.png v3: a one-page broadsheet summing up world news of Sunday 22 November 2026.

Drawn with Pillow at 1024x1024. Every story below was reported on 22 Nov 2026
(One Turn day page for that date, which aggregates BBC/Reuters/AP/AFP/Al Jazeera
and others). Claims are worded as claims and credited to whoever made them.
Layout follows the classic one-day front-page pattern: masthead, stat strip,
region bar, 13 numbered illustrated cards, a pinned world map, 26 one-line
briefs and a date-check footer. All artwork is original flat drawing.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (18, 22, 32)
MUTED = (92, 96, 104)
RED = (176, 42, 42)
NAVY = (27, 58, 110)
TEAL = (18, 110, 118)
GOLD = (176, 128, 10)
GREEN = (44, 120, 66)
PURPLE = (96, 70, 150)
RUST = (172, 84, 44)
OLIVE = (110, 104, 52)
SLATE = (84, 96, 110)
CARD_BG = (255, 253, 246)
LINE = (206, 198, 178)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
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


def para(draw, xy, text, fnt, fill, max_w, gap=3, max_lines=4):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


# ---------------- flat banner icons ----------------
def ic_gavel(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 28, cy + 10, cx + 28, cy + 24], fill=(240, 200, 90))
    d.line([(cx - 32, cy - 18), (cx + 6, cy + 10)], fill=(240, 200, 90), width=8)
    d.rectangle([cx - 44, cy - 30, cx - 18, cy - 8], fill=(240, 200, 90))
    d.ellipse([cx + 26, cy - 24, cx + 54, cy + 4], fill=(246, 241, 229))


def ic_flame(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx, cy - 24), (cx + 17, cy + 4), (cx + 9, cy + 22), (cx - 9, cy + 22), (cx - 17, cy + 4)], fill=(240, 120, 40))
    d.polygon([(cx, cy - 5), (cx + 8, cy + 9), (cx, cy + 20), (cx - 8, cy + 9)], fill=(250, 200, 80))


def ic_ship(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 32, cy + 5), (cx + 32, cy + 5), (cx + 20, cy + 20), (cx - 20, cy + 20)], fill=(246, 241, 229))
    d.rectangle([cx - 15, cy - 11, cx + 7, cy + 4], fill=(246, 241, 229))
    d.line([(cx + 17, cy - 20), (cx + 17, cy + 4)], fill=(246, 241, 229), width=4)
    d.polygon([(cx + 17, cy - 20), (cx + 31, cy - 12), (cx + 17, cy - 5)], fill=RED)
    d.arc([cx - 38, cy + 15, cx - 8, cy + 29], 0, 180, fill=(150, 200, 220), width=3)
    d.arc([cx + 2, cy + 15, cx + 32, cy + 29], 0, 180, fill=(150, 200, 220), width=3)


def ic_drone(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 22, cy - 14), (cx + 22, cy + 14)], fill=(246, 241, 229), width=4)
    d.line([(cx - 22, cy + 14), (cx + 22, cy - 14)], fill=(246, 241, 229), width=4)
    for dx, dy in [(-22, -14), (22, -14), (-22, 14), (22, 14)]:
        d.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6], fill=(240, 200, 90))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(246, 241, 229))


def ic_dome(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.arc([cx - 24, cy - 22, cx + 24, cy + 14], 180, 360, fill=(246, 241, 229), width=5)
    d.line([(cx, cy - 27), (cx, cy - 18)], fill=(246, 241, 229), width=4)
    d.rectangle([cx - 28, cy + 1, cx + 28, cy + 8], fill=(246, 241, 229))
    for i in range(-2, 3):
        d.line([(cx + i * 10, cy + 10), (cx + i * 10, cy + 20)], fill=(246, 241, 229), width=4)
    d.line([(cx - 30, cy + 23), (cx + 30, cy + 23)], fill=(246, 241, 229), width=4)


def ic_ballot(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 24, cy - 1, cx + 24, cy + 22], fill=(246, 241, 229))
    d.rectangle([cx - 12, cy - 25, cx + 12, cy - 3], fill=(255, 255, 255), outline=(246, 241, 229), width=3)
    d.line([(cx - 6, cy - 16), (cx - 1, cy - 9), (cx + 7, cy - 19)], fill=GREEN, width=4)
    d.rectangle([cx - 15, cy + 5, cx + 15, cy + 10], fill=NAVY)


def ic_scales(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx, cy - 22), (cx, cy + 16)], fill=(246, 241, 229), width=4)
    d.line([(cx - 24, cy - 16), (cx + 24, cy - 16)], fill=(246, 241, 229), width=4)
    for sx in (-1, 1):
        px = cx + sx * 24
        d.line([(px, cy - 16), (px - 9, cy + 1)], fill=(246, 241, 229), width=3)
        d.line([(px, cy - 16), (px + 9, cy + 1)], fill=(246, 241, 229), width=3)
        d.arc([px - 10, cy - 1, px + 10, cy + 12], 0, 180, fill=(240, 200, 90), width=4)
    d.line([(cx - 13, cy + 20), (cx + 13, cy + 20)], fill=(246, 241, 229), width=4)


def ic_chart(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 28, cy - 22), (cx - 28, cy + 22), (cx + 30, cy + 22)], fill=(246, 241, 229), width=4)
    d.line([(cx - 24, cy - 13), (cx - 7, cy - 3), (cx + 6, cy + 2), (cx + 24, cy + 16)], fill=(240, 120, 40), width=5)
    d.polygon([(cx + 24, cy + 16), (cx + 14, cy + 14), (cx + 22, cy + 5)], fill=(240, 120, 40))


def ic_planet(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(200, 170, 130))
    d.ellipse([cx - 7, cy - 11, cx + 2, cy - 2], fill=(160, 130, 95))
    d.ellipse([cx + 4, cy + 3, cx + 12, cy + 11], fill=(160, 130, 95))
    d.arc([cx - 31, cy - 9, cx + 31, cy + 14], 200, 340, fill=(246, 241, 229), width=3)
    d.ellipse([cx + 20, cy - 24, cx + 27, cy - 17], fill=(246, 241, 229))


def ic_flag(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 18, cy - 24), (cx - 18, cy + 24)], fill=(246, 241, 229), width=4)
    sq = 12
    for row in range(3):
        for col in range(3):
            fill = (18, 22, 32) if (row + col) % 2 == 0 else (255, 255, 255)
            d.rectangle([cx - 18 + col * sq, cy - 24 + row * sq,
                         cx - 18 + (col + 1) * sq, cy - 24 + (row + 1) * sq], fill=fill)


def ic_star(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 24 if i % 2 == 0 else 11
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(240, 200, 90))


def ic_doc(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 15, cy - 24, cx + 15, cy + 24], fill=(255, 255, 255), outline=(246, 241, 229), width=3)
    for yy in (-13, -4, 5):
        d.line([(cx - 9, cy + yy), (cx + 9, cy + yy)], fill=MUTED, width=3)
    d.line([(cx - 7, cy + 13), (cx - 2, cy + 18), (cx + 8, cy + 9)], fill=GREEN, width=4)


def ic_cricket(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.text((cx - d.textlength("720/9", font=F(SERIF_B, 30)) / 2, cy - 18), "720/9", font=F(SERIF_B, 30), fill=(246, 241, 229))
    d.ellipse([cx + 44, cy - 16, cx + 58, cy - 2], fill=(240, 120, 40))


def ic_pope(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx, cy - 26), (cx + 14, cy - 6), (cx + 16, cy + 14), (cx - 16, cy + 14), (cx - 14, cy - 6)], fill=(246, 241, 229))
    d.line([(cx, cy - 18), (cx, cy + 2)], fill=GOLD, width=4)
    d.line([(cx - 6, cy - 12), (cx + 6, cy - 12)], fill=GOLD, width=4)
    d.line([(cx - 20, cy + 22), (cx + 20, cy + 22)], fill=(246, 241, 229), width=4)


def ic_globe(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(246, 241, 229), width=4)
    d.ellipse([cx - 10, cy - 22, cx + 10, cy + 22], outline=(246, 241, 229), width=3)
    d.line([(cx - 22, cy), (cx + 22, cy)], fill=(246, 241, 229), width=3)


# ---------------- content ----------------
CARDS = [
    (RED, ic_gavel, "ANTALYA, TURKEY", "CLIMATE TALKS",
     "COP31 ends with no deal at all",
     "The EU and about 130 parties reject the draft: it never mentions fossil fuels. The longest UN climate summit on record closes two days late.",
     "BBC · CBC · The Hindu", (30.7, 36.9)),
    (NAVY, ic_flame, "MANAMA, BAHRAIN", "GULF STRIKES",
     "Iran strikes Bahrain site",
     "Bahrain says an Iranian strike hit an industrial site, wounding two. Iran says it targeted US air defences. Gulf states condemn the attack.",
     "Middle East Eye · France 24", (50.6, 26.2)),
    (TEAL, ic_ship, "BENGHAZI · FINLAND", "WAR AT SEA",
     "Russian warships hit in two seas",
     "A suspected Ukrainian sea drone hits a corvette at Benghazi; a second ship is targeted. Sparta II, hit by drones, is towed from Finnish waters.",
     "France 24 · BBC · Al Jazeera", (20.1, 32.1)),
    (RUST, ic_drone, "DYMER, UKRAINE", "UKRAINE WAR",
     "Drone hits flats; 14 missing",
     "A Russian drone partly destroys a five-storey block in Dymer. Six die across the Kyiv region.",
     "BBC", (30.5, 50.5)),
    (PURPLE, ic_dome, "WASHINGTON, USA", "ELECTIONS",
     "Democrats' biggest majority since 1992",
     "A North Carolina recount gives Democrats at least 258 House seats; four races undecided.",
     "BBC", (-77.0, 38.9)),
    (NAVY, ic_cricket, "WELLINGTON, NEW ZEALAND", "CRICKET",
     "India post 720/9, a New Zealand record",
     "India declare on 720 for 9, the highest Test total ever made in New Zealand. Pant 128, Rahul 136.",
     "AFP", (174.8, -41.3)),
    (PURPLE, ic_scales, "THE HAGUE", "JUSTICE",
     "ICJ: Myanmar committed genocide",
     "The World Court finds Myanmar responsible for genocide against the Rohingya.",
     "El Pais", (4.3, 52.1)),
    (RED, ic_chart, "NEW YORK · TOKYO", "MARKETS",
     "Stocks fall as AI sell-off deepens",
     "The S&P 500 falls 3.7%, the Nikkei 5.06%. Nvidia faces an SEC accounting inquiry.",
     "SCMP", (-74.0, 40.7)),
    (SLATE, ic_planet, "MERCURY ORBIT", "SPACE",
     "BepiColombo reaches Mercury",
     "The European-Japanese probe enters Mercury orbit after eight years. A glitch is reported.",
     "BBC Science", (0, 88)),
    (GOLD, ic_flag, "LAS VEGAS, USA", "FORMULA 1",
     "Verstappen wins in Las Vegas",
     "Verstappen wins the Las Vegas GP for the third time in four years; 35 lead changes.",
     "wire reports", (-115.2, 36.2)),
    (GREEN, ic_star, "GUASAVE, MEXICO", "JUSTICE",
     "Mexico captures 'El Chapo Isidro'",
     "Special forces seize cartel boss Meza Flores, on the FBI most-wanted list.",
     "NPR", (-108.5, 25.6)),
    (GREEN, ic_doc, "JAKARTA, INDONESIA", "TRADE",
     "EU–Indonesia trade deal signed",
     "After ten years of talks, the EU and Indonesia sign deals removing 98.5% of tariffs.",
     "Euronews", (106.8, -6.2)),
    (OLIVE, ic_pope, "VATICAN CITY", "VATICAN",
     "Pope Leo lunches with 1,300 poor guests",
     "Pope Leo XIV shares lunch with about 1,300 poor and vulnerable people in the Paul VI Hall for the 10th World Day of the Poor.",
     "Vatican News", (12.45, 41.9)),
]

BRIEFS = [
    "KHARG ISLAND — Trump dares Iran on blockade",
    "WEST BANK — Settlers torch cars in villages",
    "JERUSALEM — Coalition talks end, no deal",
    "SAUDI ARABIA — Houthis claim refinery hit",
    "SEOUL — Minister quits over AI exam row",
    "BANTEN — Candy factory fire, 3 dead",
    "USA — CRISPR cuts cholesterol 52%",
    "NIGERIA — Funeral boat capsizes, 24 dead",
    "ISTANBUL — Protests over media takeover",
    "WASHINGTON — FBI database reportedly hacked",
    "GENEVA — AI weapons talks: no binding rules",
    "TOKYO — Saudi triples oil stored in Japan",
    "ARGENTINA — $50bn LNG project approved",
    "SHENZHEN — Trump-Xi-Putin summit fallout",
    "BANGLADESH — Garment strikes, factories shut",
    "HORMUZ — Brent near $90 amid Gulf turmoil",
    "CHINA — AI said to help prove Riemann claim",
    "FRANCE · PORTUGAL — Cost-of-living protests",
    "DENMARK — Russian attache expelled over plot",
    "LOS ANGELES — Palisades fire starter convicted",
    "RWANDA — EU deal on deportation centres",
    "BEIRUT — Aoun blames Israel and Iran",
    "GAZA — Israeli strikes continue, civilians die",
    "BRASILIA — Bolsonaro stable in intensive care",
    "HONG KONG — Election Committee votes ~99%",
    "KHARTOUM — Drones hit homes, UN building",
]

STATS = [
    ("258", "US House seats for Democrats, most since 1992"),
    ("720/9", "India's total — biggest Test innings in New Zealand"),
    ("52%", "cut in bad cholesterol from one CRISPR therapy"),
    ("-3.7%", "S&P 500 fall as the AI sell-off deepens"),
    ("1,300", "poor guests at Pope Leo's Sunday lunch"),
    ("98.5%", "of EU tariffs removed by the Indonesia deal"),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.text((18, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 16), fill=RED)
right = "39 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
d.text((W - 18 - d.textlength(right, font=F(SANS_B, 14)), 10), right, font=F(SANS_B, 14), fill=INK)
title = "Sunday 22 November 2026"
tw = d.textlength(title, font=F(SERIF_B, 50))
d.text(((W - tw) / 2, 26), title, font=F(SERIF_B, 50), fill=INK)
ticker = "COP31 ends with no deal · Iran strikes Bahrain · India 720/9 in Wellington · Hong Kong votes · Verstappen wins in Las Vegas"
tw2 = d.textlength(ticker, font=F(SERIF_I, 17))
d.text(((W - tw2) / 2, 82), ticker, font=F(SERIF_I, 17), fill=MUTED)
d.line([(18, 106), (W - 18, 106)], fill=INK, width=3)
d.line([(18, 111), (W - 18, 111)], fill=INK, width=1)

# ---------- stat strip ----------
sy = 118
col_w = (W - 36) // 6
for i, (num, cap) in enumerate(STATS):
    x = 18 + i * col_w
    d.text((x + 4, sy), num, font=F(SERIF_B, 28), fill=RED if i % 2 == 0 else NAVY)
    para(d, (x + 4, sy + 34), cap, F(SANS_R, 11), MUTED, col_w - 10, gap=2, max_lines=3)
    if i:
        d.line([(x - 4, sy + 2), (x - 4, sy + 60)], fill=LINE, width=1)
d.line([(18, sy + 66), (W - 18, sy + 66)], fill=LINE, width=1)

# ---------- region bar ----------
regions = [("EUROPE", 9, NAVY), ("ASIA", 8, RUST), ("MID EAST", 8, OLIVE), ("AFRICA", 4, GREEN),
           ("AMERICAS", 7, PURPLE), ("OCEANIA", 1, TEAL), ("GLOBAL", 2, SLATE)]
total_r = sum(v for _, v, _ in regions)
ry = sy + 74
x = 18
for name, v, color in regions:
    wpx = int((W - 36) * v / total_r)
    d.rectangle([x, ry, x + wpx, ry + 19], fill=color)
    label = f"{name} {v}"
    if wpx > d.textlength(label, font=F(SANS_B, 11.5)) + 8:
        d.text((x + 6, ry + 4), label, font=F(SANS_B, 11.5), fill=(255, 255, 255))
    x += wpx

# ---------- cards ----------
def card(x0, y0, wpx, hpx, idx, banner_h, head_size, body_size, body_lines, show_credit=True):
    color, icon, loc, kicker, head, summ, credit, _pin = CARDS[idx]
    d.rounded_rectangle([x0, y0, x0 + wpx, y0 + hpx], 8, fill=CARD_BG, outline=LINE, width=2)
    d.rectangle([x0, y0, x0 + wpx, y0 + banner_h], fill=color)
    # draw the icon on its own layer so it is clipped to the banner
    layer = Image.new("RGBA", (wpx, banner_h), (0, 0, 0, 0))
    icon(ImageDraw.Draw(layer), [0, 0, wpx, banner_h], color)
    img.paste(layer, (x0, y0), layer)
    d.ellipse([x0 + 8, y0 + banner_h - 13, x0 + 34, y0 + banner_h + 13], fill=NAVY, outline=(255, 255, 255), width=2)
    ns = str(idx + 1)
    d.text((x0 + 21 - d.textlength(ns, font=F(SANS_B, 16)) / 2, y0 + banner_h - 8), ns, font=F(SANS_B, 16), fill=(255, 255, 255))
    d.text((x0 + 42, y0 + banner_h + 3), loc, font=F(SANS_B, 10.5), fill=MUTED)
    ty = y0 + banner_h + 19
    d.text((x0 + 10, ty), kicker, font=F(SANS_B, 11.5), fill=color)
    cw = d.textlength(credit, font=F(SANS_R, 9.5))
    d.text((x0 + wpx - 10 - cw, ty + 2), credit, font=F(SANS_R, 9.5), fill=MUTED)
    ty += 15
    ty = para(d, (x0 + 10, ty), head, F(SERIF_B, head_size), INK, wpx - 20, gap=2, max_lines=2)
    para(d, (x0 + 10, ty + 2), summ, F(SANS_R, body_size), INK, wpx - 20, gap=2, max_lines=body_lines)
    if show_credit:
        d.text((x0 + 10, y0 + hpx - 16), credit, font=F(SANS_R, 10), fill=MUTED)


cy = ry + 27
gap = 8
w3 = (W - 36 - 2 * gap) // 3
for i in range(3):
    card(18 + i * (w3 + gap), cy, w3, 164, i, 48, 18, 12.5, 4, show_credit=False)
cy += 164 + gap
w5 = (W - 36 - 4 * gap) // 5
for r in range(2):
    for i in range(5):
        card(18 + i * (w5 + gap), cy, w5, 150, 3 + r * 5 + i, 38, 15.5, 11.5, 3, show_credit=False)
    cy += 150 + gap

# ---------- bottom: map + briefs ----------
by = cy + 2
d.line([(18, by), (W - 18, by)], fill=INK, width=2)
by += 7
d.text((18, by), "THE 13 DRAWN STORIES, MAPPED", font=F(SANS_B, 13.5), fill=INK)
d.text((430, by), "IN BRIEF — 26 MORE STORIES OF THE DAY", font=F(SANS_B, 13.5), fill=INK)
by += 20

MAP_ROWS = [
    "  ####    ##        #####  #########      ",
    " ########  #   ##  ########################",
    "  #########     ######################### ",
    "   ######       #######  #################",
    "    ####         #####    ############### ",
    "     ##           ###      #############  ",
    "     #             #        ###########   ",
    "      #                     ##########    ",
    "      ##                     ########     ",
    "       ##                     ######  #   ",
    "        #                      ####       ",
    "        #                       ##    #   ",
]
map_x0, map_y0, map_w, map_h = 18, by, 396, 140
d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=(232, 238, 240), outline=LINE, width=1)
cols = max(len(r) for r in MAP_ROWS)
for ri, row in enumerate(MAP_ROWS):
    for ci, ch in enumerate(row):
        if ch == "#":
            px = map_x0 + 6 + ci * (map_w - 12) / cols
            py = map_y0 + 7 + ri * (map_h - 14) / len(MAP_ROWS)
            d.ellipse([px - 2.3, py - 2.3, px + 2.3, py + 2.3], fill=(150, 170, 140))
for i, c in enumerate(CARDS):
    lon, lat = c[7]
    px = map_x0 + (lon + 180) / 360 * map_w
    py = map_y0 + (90 - lat) / 180 * map_h
    px = max(map_x0 + 10, min(map_x0 + map_w - 10, px))
    py = max(map_y0 + 10, min(map_y0 + map_h - 10, py))
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    ns = str(i + 1)
    d.text((px - d.textlength(ns, font=F(SANS_B, 11)) / 2, py - 7), ns, font=F(SANS_B, 11), fill=(255, 255, 255))
para(d, (map_x0, map_y0 + map_h + 5), "Pins match the numbered cards above. Schematic map, not to scale.",
     F(SANS_R, 10.5), MUTED, map_w, gap=2, max_lines=2)

bx = 430
bw = (W - 18 - bx - 14) // 2
for i, line in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    x = bx + col * (bw + 14)
    y = by + row * 14.5
    d.text((x, y), f"{i + 14}", font=F(SANS_B, 11), fill=NAVY)
    d.text((x + 24, y), line, font=F(SANS_R, 11), fill=INK)

# ---------- footer ----------
fy = H - 88
d.rounded_rectangle([18, fy, W - 18, fy + 42], 6, outline=RED, width=2)
d.text((28, fy + 5), "DATE CHECK — NOT SUNDAY'S NEWS, AND NOT COUNTED ABOVE", font=F(SANS_B, 12), fill=RED)
para(d, (28, fy + 22),
     "Older items still circulating (earlier COP drafts, last week's votes, the 2025 Palisades fire itself) are excluded; every story above was reported on Sunday 22 November 2026.",
     F(SANS_R, 11), INK, W - 76, gap=2, max_lines=2)
d.text((18, fy + 50), "Sunday 22 November 2026, in every time zone; claims credited to those who made them.",
       font=F(SANS_R, 11.5), fill=MUTED)
src = "Sources: BBC · Reuters · AP · AFP · Al Jazeera · France 24 · The Guardian · SCMP — artwork original"
d.text((18, fy + 67), src, font=F(SANS_R, 11.5), fill=MUTED)
d.text((W - 18 - d.textlength("22 NOV 2026", font=F(SANS_B, 12.5)), fy + 67), "22 NOV 2026", font=F(SANS_B, 12.5), fill=INK)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
