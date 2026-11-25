"""Build assets/entry.png. Local only — the grader never runs this file."""

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

from stories import stories_by_tier, strapline

W = H = 1024
SCALE = 2
MARGIN = 32

PAPER = (244, 239, 230)
INK = (27, 27, 27)
MUTED = (90, 90, 90)
RULE = (207, 198, 184)
LEAD_BG = (30, 42, 58)
RUSSIA_BG = (110, 59, 59)
FLAG_BLUE = (0, 87, 183)
FLAG_YELLOW = (255, 215, 0)
EUROPE = (43, 95, 168)
MIDDLE_EAST = (181, 70, 46)
AMERICAS = (46, 125, 91)
ASIA = (192, 138, 30)
BUSINESS = (107, 79, 160)
RELIGION = (122, 122, 122)
AFRICA = (138, 90, 43)
OCEANIA = (31, 138, 138)
BRIEF_INK = (51, 51, 51)
STROKE = 3

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "entry.png"
FONTS = Path(r"C:\Windows\Fonts")


def px(value):
    return int(round(value * SCALE))


def font_file(*names):
    for name in names:
        path = FONTS / name
        if path.is_file():
            return str(path)
    raise FileNotFoundError("missing font: " + ", ".join(names))


SERIF_BOLD = font_file("georgiab.ttf", "timesbd.ttf", "arialbd.ttf")
SANS = font_file("segoeui.ttf", "arial.ttf")
SANS_BOLD = font_file("segoeuib.ttf", "arialbd.ttf")


def load_font(path, size):
    return ImageFont.truetype(path, px(size))


def text_size(draw, text, font):
    if not text:
        return 0.0, 0.0
    box = draw.textbbox((0, 0), text, font=font, anchor="lt")
    return (box[2] - box[0]) / SCALE, (box[3] - box[1]) / SCALE


def text_width(draw, text, font):
    return text_size(draw, text, font)[0]


def draw_text(draw, x, y, text, font, fill):
    draw.text((px(x), px(y)), text, font=font, fill=fill, anchor="lt")


def tracked_width(draw, text, font, tracking):
    if not text:
        return 0.0
    width = 0.0
    for index, char in enumerate(text):
        width += text_width(draw, char, font)
        if index != len(text) - 1:
            width += tracking
    return width


def draw_tracked(draw, x, y, text, font, fill, tracking):
    cursor = x
    for char in text:
        draw_text(draw, cursor, y, char, font, fill)
        cursor += text_width(draw, char, font) + tracking


def wrap_text(draw, text, font, max_width):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        if text_width(draw, trial, font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_text(draw, text, font_path, start, minimum, max_width, max_lines):
    size = start
    while size >= minimum:
        font = load_font(font_path, size)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines, size
        size -= 1
    font = load_font(font_path, minimum)
    return font, wrap_text(draw, text, font, max_width), minimum


def accent_for(region):
    upper = region.upper()
    if upper.startswith("MARKETS") or upper.startswith("BUSINESS"):
        return BUSINESS
    if upper.startswith("AFRICA"):
        return AFRICA
    if upper.startswith("OCEANIA"):
        return OCEANIA
    if upper.startswith("CULTURE"):
        return RELIGION
    if "MIDDLE" in upper:
        return MIDDLE_EAST
    if "AMERICAS" in upper:
        return AMERICAS
    if "ASIA" in upper:
        return ASIA
    if "BUSINESS" in upper or "MARKETS" in upper:
        return BUSINESS
    if "RELIGION" in upper:
        return RELIGION
    return EUROPE


def draw_chip(draw, x, y, label, fill):
    font = load_font(SANS_BOLD, 15)
    text_w, text_h = text_size(draw, label, font)
    pad_x, pad_y = 8, 4
    width = text_w + pad_x * 2
    height = text_h + pad_y * 2
    draw.rounded_rectangle(
        [px(x), px(y), px(x + width), px(y + height)],
        radius=px(2),
        fill=fill,
    )
    draw_text(draw, x + pad_x, y + pad_y, label, font, PAPER)
    return width, height


def polygon(draw, points, fill):
    draw.polygon([(px(x), px(y)) for x, y in points], fill=fill)


def polyline(draw, points, fill, width):
    draw.line([(px(x), px(y)) for x, y in points], fill=fill, width=max(1, px(width)))


def rotate(points, cx, cy, degrees):
    angle = math.radians(degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotated = []
    for x, y in points:
        dx = x - cx
        dy = y - cy
        rotated.append((cx + dx * cosine - dy * sine, cy + dx * sine + dy * cosine))
    return rotated


def bezier(p0, p1, p2, p3, steps=48):
    points = []
    for step in range(steps + 1):
        t = step / steps
        u = 1 - t
        x = u ** 3 * p0[0] + 3 * u ** 2 * t * p1[0] + 3 * u * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = u ** 3 * p0[1] + 3 * u ** 2 * t * p1[1] + 3 * u * t ** 2 * p2[1] + t ** 3 * p3[1]
        points.append((x, y))
    return points


def dashed_polyline(draw, points, fill, width, dash, gap):
    if len(points) < 2:
        return
    period = dash + gap
    traveled = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg == 0:
            continue
        ux = (x1 - x0) / seg
        uy = (y1 - y0) / seg
        pos = 0.0
        while pos < seg - 0.01:
            phase = traveled % period
            room = (dash - phase) if phase < dash else (period - phase)
            step = min(room, seg - pos)
            if phase < dash:
                polyline(
                    draw,
                    [(x0 + ux * pos, y0 + uy * pos), (x0 + ux * (pos + step), y0 + uy * (pos + step))],
                    fill,
                    width,
                )
            pos += step
            traveled += step


def arrow_head(draw, start, end, fill, size):
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = angle + math.radians(152)
    right = angle - math.radians(152)
    polygon(
        draw,
        [
            end,
            (end[0] + size * math.cos(left), end[1] + size * math.sin(left)),
            (end[0] + size * math.cos(right), end[1] + size * math.sin(right)),
        ],
        fill,
    )


def wave_points(x0, x1, y, amplitude, step=4):
    points = []
    x = x0
    while x <= x1:
        points.append((x, y + math.sin((x - x0) / 13.0) * amplitude))
        x += step
    return points


def draw_sinking_ship(draw, cx, cy, scale=1.5):
    def place(points):
        scaled = [(x * scale, y * scale) for x, y in points]
        spun = rotate(scaled, 0, 0, 25)
        return [(cx + x, cy + y) for x, y in spun]

    polygon(draw, place([(-72, 7), (48, 12), (76, 2), (50, -8), (-66, -9), (-88, 0)]), PAPER)
    polygon(draw, place([(-64, -9), (-26, -6), (-22, -28), (-66, -26)]), PAPER)
    polygon(draw, place([(-52, -28), (-36, -26), (-36, -42), (-54, -40)]), PAPER)
    for origin in (-56, -42):
        polygon(draw, place([(origin, -22), (origin + 8, -21), (origin + 8, -14), (origin, -15)]), INK)
    polyline(draw, wave_points(cx - 8 * scale, cx + 70 * scale, cy + 8 * scale, 2.4 * scale), PAPER, 2)
    polygon(
        draw,
        [
            (cx + 10 * scale, cy - 20 * scale),
            (cx + 20 * scale, cy - 4 * scale),
            (cx + 10 * scale, cy + 2 * scale),
            (cx + 2 * scale, cy - 6 * scale),
            (cx - 6 * scale, cy + 1 * scale),
            (cx - 2 * scale, cy - 8 * scale),
        ],
        MIDDLE_EAST,
    )
    polygon(
        draw,
        [
            (cx + 8 * scale, cy - 14 * scale),
            (cx + 14 * scale, cy - 4 * scale),
            (cx + 6 * scale, cy - 1 * scale),
            (cx + 1 * scale, cy - 7 * scale),
        ],
        ASIA,
    )
    for ox, oy, radius, color in (
        (6, -16, 6, INK),
        (9, -30, 8, MUTED),
        (5, -44, 10, RELIGION),
    ):
        draw.ellipse(
            [
                px(cx + ox * scale - radius * scale),
                px(cy + oy * scale - radius * scale),
                px(cx + ox * scale + radius * scale),
                px(cy + oy * scale + radius * scale * 0.75),
            ],
            fill=color,
        )


def fill_horizontal_split(image, points, split_y, top_color, bottom_color):
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).polygon([(px(x), px(y)) for x, y in points], fill=255)
    top_band = Image.new("L", image.size, 0)
    ImageDraw.Draw(top_band).rectangle([0, 0, image.size[0], px(split_y)], fill=255)
    bottom_band = Image.new("L", image.size, 0)
    ImageDraw.Draw(bottom_band).rectangle([0, px(split_y), image.size[0], image.size[1]], fill=255)
    top = Image.new("RGB", image.size, top_color)
    bottom = Image.new("RGB", image.size, bottom_color)
    image.paste(top, (0, 0), ImageChops.multiply(mask, top_band))
    image.paste(bottom, (0, 0), ImageChops.multiply(mask, bottom_band))


def draw_label_pill(draw, x, y, text, font):
    text_w, text_h = text_size(draw, text, font)
    pad_x, pad_y = 6, 3
    draw.rounded_rectangle(
        [px(x), px(y), px(x + text_w + pad_x * 2), px(y + text_h + pad_y * 2)],
        radius=px(3),
        fill=INK,
    )
    draw_text(draw, x + pad_x, y + pad_y, text, font, PAPER)
    return text_w + pad_x * 2, text_h + pad_y * 2


def draw_lead_map(image, draw):
    polygon(
        draw,
        [(360, 112), (568, 112), (568, 248), (455, 258), (340, 190), (352, 128)],
        RUSSIA_BG,
    )
    polygon(
        draw,
        [
            (48, 248), (170, 236), (320, 240), (430, 258),
            (455, 300), (430, 356), (110, 358), (44, 312), (42, 268),
        ],
        EUROPE,
    )
    ukraine = [
        (64, 168), (82, 140), (160, 124), (300, 118), (430, 124),
        (488, 142), (504, 172), (492, 198), (450, 210),
        (410, 216), (392, 216), (386, 228), (376, 240), (366, 228), (360, 216),
        (250, 216), (150, 214), (78, 200), (60, 182),
    ]
    fill_horizontal_split(image, ukraine, 168, FLAG_BLUE, FLAG_YELLOW)
    polyline(draw, ukraine + [ukraine[0]], PAPER, 1.25)
    for base in (300, 328):
        polyline(draw, wave_points(90, 400, base, 1.8), PAPER, 2)
    ship = (155, 305)
    ship_scale = 0.72
    draw_sinking_ship(draw, ship[0], ship[1], ship_scale)
    city = (420, 192)
    arcs = [
        ((530, 140), (490, 150), (455, 170), city),
        ((540, 168), (500, 172), (460, 182), (426, 190)),
        ((528, 196), (488, 198), (454, 196), (424, 198)),
    ]
    for p0, p1, p2, p3 in arcs:
        curve = bezier(p0, p1, p2, p3)
        dashed_polyline(draw, curve, FLAG_YELLOW, 2, 7, 5)
        arrow_head(draw, curve[-8], curve[-1], INK, 6)
    draw.ellipse([px(city[0] - 5), px(city[1] - 5), px(city[0] + 5), px(city[1] + 5)], fill=MIDDLE_EAST)
    draw.ellipse([px(city[0] - 2), px(city[1] - 2), px(city[0] + 2), px(city[1] + 2)], fill=PAPER)
    label_font = load_font(SANS_BOLD, 13)
    city_label = "Zaporizhzhia"
    city_w, _city_h = text_size(draw, city_label, label_font)
    draw_text(draw, city[0] - city_w - 6, city[1] - 14, city_label, label_font, INK)
    draw_tracked(draw, 96, 178, "UKRAINE", label_font, INK, 1.2)
    draw_tracked(draw, 470, 128, "RUSSIA", label_font, PAPER, 1.2)
    draw_tracked(draw, 70, 338, "BLACK SEA", label_font, PAPER, 1.0)
    hit_font = load_font(SANS_BOLD, 13)
    smoke_top = ship[1] - 52 * ship_scale
    draw_label_pill(draw, ship[0] - 36, smoke_top - 22, "Russian ship hit", hit_font)


def draw_lead_copy(draw, story):
    x = 548
    width = 420
    top = 116
    bottom = 362
    _tag_w, tag_h = text_size(draw, story["tag"], load_font(SANS_BOLD, 15))
    chip_h = tag_h + 8
    head_font, head_lines, head_size = fit_text(
        draw, story["headline"], SERIF_BOLD, 34, 26, width, 2
    )
    head_advance = head_size * 1.12
    bullets = list(story["points"])
    bullet_size = 17
    wrapped = []
    bullet_advance = 22
    bullet_gap = 6
    while bullet_size >= 15:
        bullet_font = load_font(SANS, bullet_size)
        wrapped = [wrap_text(draw, bullet, bullet_font, width - 16) for bullet in bullets]
        bullet_advance = bullet_size * 1.16
        bullets_h = sum(len(lines) * bullet_advance for lines in wrapped) + bullet_gap * (len(wrapped) - 1)
        block_h = chip_h + 12 + len(head_lines) * head_advance + 14 + bullets_h
        if top + block_h <= bottom:
            break
        bullet_size -= 1
    else:
        bullet_font = load_font(SANS, 15)
    spare = bottom - top - block_h
    y = top + max(0, spare) * 0.28
    draw_chip(draw, x, y, story["tag"], EUROPE)
    y += chip_h + 12
    for line in head_lines:
        draw_text(draw, x, y, line, head_font, PAPER)
        y += head_advance
    y += 8
    for lines in wrapped:
        for index, line in enumerate(lines):
            if index == 0:
                draw.rectangle([px(x), px(y + 6), px(x + 5), px(y + 11)], fill=PAPER)
            draw_text(draw, x + 14, y, line, bullet_font, PAPER)
            y += bullet_advance
        y += bullet_gap
    if y > bottom + 2:
        print(f"lead text ends at {y:.1f}, past {bottom}")
    else:
        print(f"lead headline {head_size}px, bullets {bullet_size}px, end {y:.1f}")


def draw_lead(image, draw):
    draw.rectangle([px(32), px(104), px(992), px(372)], fill=LEAD_BG)
    draw_lead_map(image, draw)
    draw_lead_copy(draw, stories_by_tier("lead")[0])


def icon_hormuz(draw, x, y, w, h):
    polygon(
        draw,
        [
            (x, y),
            (x + w, y),
            (x + w * 0.68, y + h * 0.20),
            (x + w * 0.32, y + h * 0.20),
        ],
        MIDDLE_EAST,
    )
    polygon(
        draw,
        [
            (x, y + h),
            (x + w, y + h),
            (x + w * 0.68, y + h * 0.80),
            (x + w * 0.32, y + h * 0.80),
        ],
        MIDDLE_EAST,
    )
    cy = y + h * 0.42
    polygon(
        draw,
        [
            (x + 4, cy + 7),
            (x + w - 18, cy + 8),
            (x + w - 6, cy + 1),
            (x + w - 18, cy - 7),
            (x + 4, cy - 6),
        ],
        INK,
    )
    draw.rectangle([px(x + 8), px(cy - 24), px(x + 34), px(cy - 6)], fill=INK)
    draw.rectangle([px(x + 14), px(cy - 32), px(x + 24), px(cy - 24)], fill=INK)
    draw.rectangle([px(x + 12), px(cy - 20), px(x + 18), px(cy - 14)], fill=PAPER)
    if h >= 60:
        label = "HORMUZ"
        label_font = load_font(SANS_BOLD, 12)
        label_w, _label_h = text_size(draw, label, label_font)
        draw_text(draw, x + (w - label_w) / 2, cy + 12, label, label_font, INK)


def icon_gaza(draw, x, y, w, h):
    ground = y + h - 4
    blocks = (
        (x + 4, ground - 16, x + 30, ground),
        (x + 32, ground - 30, x + 50, ground),
        (x + 52, ground - 14, x + 80, ground),
        (x + 16, ground - 40, x + 36, ground - 18),
        (x + 64, ground - 28, x + 90, ground - 12),
    )
    for left, top, right, bottom in blocks:
        draw.rectangle([px(left), px(top), px(right), px(bottom)], fill=INK)
    body_y = y + h * 0.28
    cx = x + w * 0.48
    polygon(
        draw,
        [
            (x + w * 0.10, body_y - 2),
            (x + w * 0.90, body_y - 2),
            (x + w * 0.90, body_y + 3),
            (x + w * 0.10, body_y + 3),
        ],
        INK,
    )
    draw.ellipse([px(cx - 14), px(body_y - 7), px(cx + 16), px(body_y + 8)], fill=INK)
    polygon(
        draw,
        [(cx - 14, body_y - 3), (cx - 28, body_y), (cx - 14, body_y + 3)],
        INK,
    )
    polygon(
        draw,
        [(cx + 12, body_y - 4), (cx + 26, body_y - 11), (cx + 26, body_y + 11), (cx + 12, body_y + 4)],
        INK,
    )
    dashed_polyline(draw, [(cx, body_y + 10), (cx + 4, y + h * 0.56)], INK, 2, 4, 3)


def draw_second_card(draw, story, x, y, w, h):
    accent = accent_for(story["region"])
    draw.rounded_rectangle(
        [px(x), px(y), px(x + w), px(y + h)],
        radius=px(4),
        outline=RULE,
        width=px(1),
    )
    draw.rectangle([px(x + 2), px(y + 2), px(x + 8), px(y + h - 2)], fill=accent)
    icon = icon_hormuz if story["icon"] == "hormuz" else icon_gaza
    icon(draw, x + 20, y + 18, 108, 112)
    text_x = x + 140
    text_w = w - 156
    _tag_w, tag_h = draw_chip(draw, text_x, y + 18, story["region"], accent)
    head_font, head_lines, head_size = fit_text(
        draw, story["headline"], SERIF_BOLD, 28, 22, text_w, 2
    )
    head_y = y + 18 + tag_h + 10
    advance = head_size * 1.12
    for line in head_lines:
        draw_text(draw, text_x, head_y, line, head_font, INK)
        head_y += advance
    deck_x = x + 20
    deck_w = w - 36
    deck_top = max(head_y + 8, y + 136)
    deck_font, deck_lines, deck_size = fit_text(
        draw, story["deck"], SANS, 21, 19, deck_w, 4
    )
    deck_advance = deck_size * 1.25
    for line in deck_lines:
        draw_text(draw, deck_x, deck_top, line, deck_font, BRIEF_INK)
        deck_top += deck_advance
    if deck_top > y + h - 8:
        print(f"second card {story['headline']!r} deck ends {deck_top:.1f}, card ends {y + h}")
    else:
        print(f"second {story['icon']} headline {head_size}px, deck {deck_size}px, {len(deck_lines)} lines")


def icon_chart_tile(draw, x, y, w, h):
    inset = 8
    x0, y0 = x + inset, y + h - inset
    x1, y1 = x + w - inset, y + inset
    polyline(draw, [(x0, y1), (x0, y0), (x + w - inset, y0)], INK, 2)
    polyline(draw, [(x0 + 6, y0 - 10), (x + w * 0.45, y + h * 0.42), (x1 - 4, y1 + 6)], BUSINESS, 3)
    arrow_head(draw, (x + w * 0.62, y + h * 0.38), (x1 - 4, y1 + 6), BUSINESS, 7)


def icon_china_tile(draw, x, y, w, h):
    roof_y = y + h * 0.42
    polygon(
        draw,
        [(x + w * 0.5, y + 8), (x + w - 8, roof_y), (x + 8, roof_y)],
        ASIA,
    )
    draw.rectangle([px(x + 16), px(roof_y), px(x + w - 16), px(y + h - 10)], outline=INK, width=px(2))
    draw.rectangle([px(x + w * 0.42), px(y + h * 0.62), px(x + w * 0.58), px(y + h - 10)], fill=INK)


def draw_top_tiles(draw):
    tiles = stories_by_tier("tile")
    gap = 12
    top, height = 382, 138
    width = (W - 2 * MARGIN - gap * (len(tiles) - 1)) / len(tiles)
    icons = {"hormuz": icon_hormuz, "chart": icon_chart_tile, "china": icon_china_tile}
    for index, story in enumerate(tiles):
        x = MARGIN + index * (width + gap)
        draw.rounded_rectangle(
            [px(x), px(top), px(x + width), px(top + height)],
            radius=px(4),
            outline=RULE,
            width=px(1),
        )
        accent = accent_for(story["tag"])
        draw.rectangle([px(x + 2), px(top + 2), px(x + 7), px(top + height - 2)], fill=accent)
        icons[story["icon"]](draw, x + 10, top + 8, 36, 32)
        _tag_w, tag_h = draw_chip(draw, x + 52, top + 10, story["tag"], accent)
        text_w = width - 22
        head_top = top + 46
        head_font = None
        head_size = 20
        placed = []
        head_bottom = head_top
        for head_size in (22, 20):
            head_font = load_font(SERIF_BOLD, head_size)
            head_lines = wrap_text(draw, story["headline"], head_font, text_w)
            if len(head_lines) > 2:
                continue
            cursor = head_top
            placed = []
            for line in head_lines:
                line_h = max(text_size(draw, line, head_font)[1] + 2, head_size * 1.12)
                placed.append((line, cursor))
                cursor += line_h
            head_bottom = cursor
            deck_try = load_font(SANS, 15)
            deck_try_lines = wrap_text(draw, story["deck"], deck_try, text_w)
            deck_try_h = len(deck_try_lines[:2]) * (text_size(draw, "Ag", deck_try)[1] + 3)
            if head_bottom + 8 + deck_try_h <= top + height - 6:
                break
        for line, line_y in placed:
            draw_text(draw, x + 12, line_y, line, head_font, INK)
        deck_y = head_bottom + 8
        deck_font, deck_lines, deck_size = fit_text(
            draw, story["deck"], SANS, 15, 13, text_w, 2
        )
        for line in deck_lines:
            line_h = text_size(draw, line, deck_font)[1]
            draw_text(draw, x + 12, deck_y, line, deck_font, BRIEF_INK)
            deck_y += line_h + 3
        print(
            f"tile {story['icon']} headline {head_size}px/{len(placed)} "
            f"bottom {head_bottom:.0f} deck {deck_size}px/{len(deck_lines)} end {deck_y:.0f}"
        )


def draw_second_row(draw):
    cards = stories_by_tier("second")
    gap = 16
    width = (W - 2 * MARGIN - gap) / 2
    for index, story in enumerate(cards):
        draw_second_card(draw, story, MARGIN + index * (width + gap), 485, width, 215)


def glyph_flame(draw, cx, cy, color):
    polygon(
        draw,
        [
            (cx, cy - 14),
            (cx + 3, cy - 5),
            (cx + 9, cy + 1),
            (cx + 4, cy + 12),
            (cx, cy + 6),
            (cx - 4, cy + 12),
            (cx - 9, cy + 1),
            (cx - 3, cy - 5),
        ],
        PAPER,
    )
    polygon(draw, [(cx, cy - 2), (cx + 3, cy + 5), (cx, cy + 11), (cx - 3, cy + 5)], color)


def glyph_school(draw, cx, cy, color):
    polygon(draw, [(cx - 12, cy - 2), (cx, cy - 13), (cx + 12, cy - 2)], PAPER)
    draw.rectangle([px(cx - 9), px(cy - 2), px(cx + 9), px(cy + 12)], fill=PAPER)
    draw.rectangle([px(cx - 3), px(cy + 4), px(cx + 3), px(cy + 12)], fill=color)
    draw.rectangle([px(cx - 7), px(cy + 1), px(cx - 3), px(cy + 5)], fill=color)
    draw.rectangle([px(cx + 3), px(cy + 1), px(cx + 7), px(cy + 5)], fill=color)


def glyph_factory(draw, cx, cy, color):
    draw.rectangle([px(cx - 12), px(cy - 1), px(cx + 2), px(cy + 12)], fill=PAPER)
    draw.rectangle([px(cx - 4), px(cy - 12), px(cx + 2), px(cy - 1)], fill=PAPER)
    polyline(draw, [(cx + 7, cy + 12), (cx + 7, cy - 4)], PAPER, STROKE)
    draw.rectangle([px(cx + 4), px(cy - 13), px(cx + 14), px(cy - 4)], fill=PAPER)
    polyline(draw, [(cx + 6, cy - 11), (cx + 12, cy - 6)], color, 2)


def glyph_chart(draw, cx, cy, color):
    del color
    polyline(draw, [(cx - 11, cy - 12), (cx - 11, cy + 10), (cx + 12, cy + 10)], PAPER, STROKE)
    polyline(draw, [(cx - 6, cy + 5), (cx + 7, cy - 8)], PAPER, STROKE)
    arrow_head(draw, (cx, cy - 1), (cx + 7, cy - 8), PAPER, 6)


def glyph_plane(draw, cx, cy, color):
    del color
    polygon(
        draw,
        [(cx - 13, cy), (cx + 11, cy - 3), (cx + 8, cy), (cx + 11, cy + 3)],
        INK,
    )
    polygon(
        draw,
        [(cx - 1, cy - 1), (cx + 7, cy - 12), (cx + 3, cy - 1), (cx + 7, cy + 10), (cx - 1, cy + 1)],
        INK,
    )


def glyph_book(draw, cx, cy, color):
    polyline(draw, [(cx, cy - 14), (cx, cy - 5)], PAPER, STROKE)
    polyline(draw, [(cx - 4, cy - 11), (cx + 4, cy - 11)], PAPER, STROKE)
    polygon(draw, [(cx, cy - 3), (cx - 12, cy), (cx - 12, cy + 12), (cx, cy + 8)], PAPER)
    polygon(draw, [(cx, cy - 3), (cx + 12, cy), (cx + 12, cy + 12), (cx, cy + 8)], PAPER)
    polyline(draw, [(cx, cy - 3), (cx, cy + 8)], color, 2)


BRIEF_GLYPHS = {
    "flame": glyph_flame,
    "school": glyph_school,
    "factory": glyph_factory,
    "chart": glyph_chart,
    "plane": glyph_plane,
    "book": glyph_book,
}


def draw_briefs(draw):
    items = stories_by_tier("brief")
    gap_x = 12
    col_w = (W - 2 * MARGIN - 2 * gap_x) / 3
    deck_size = 17
    deck_font = load_font(SANS, deck_size)
    name_font = load_font(SANS_BOLD, 16)
    ascent, _descent = name_font.getmetrics()
    name_ascent = ascent / SCALE
    radius = 22
    text_gap = 8
    advance = deck_size * 1.22
    row_gap = 14
    band_bottom = 960

    def row_span(row_items):
        lines = max(len(wrap_text(draw, item["deck"], deck_font, col_w)) for item in row_items)
        return radius * 2 + text_gap + lines * advance

    rows = [items[:3], items[3:]]
    spans = [row_span(row) for row in rows]
    block = sum(spans) + row_gap
    top = band_bottom - block
    print(f"briefs deck {deck_size}px, top {top:.0f}")
    y = top
    for span, row_items in zip(spans, rows):
        icon_cy = y + radius
        name_y = icon_cy - name_ascent * 0.78
        for column, item in enumerate(row_items):
            x = MARGIN + column * (col_w + gap_x)
            color = accent_for(item["region"])
            cx = x + radius
            draw.ellipse(
                [px(cx - radius), px(icon_cy - radius), px(cx + radius), px(icon_cy + radius)],
                fill=color,
            )
            BRIEF_GLYPHS[item["icon"]](draw, cx, icon_cy, color)
            name_x = x + radius * 2 + 8
            draw_text(draw, name_x, name_y, item["headline"], name_font, INK)
            line_y = y + radius * 2 + text_gap
            for line in wrap_text(draw, item["deck"], deck_font, col_w):
                draw_text(draw, x, line_y, line, deck_font, BRIEF_INK)
                line_y += advance
            if line_y > y + span + 2:
                print(f"brief tile overflow {item['headline']} ends {line_y:.1f}")
        y += span + row_gap


def draw_ticker(draw):
    draw.rectangle([0, px(968), px(W), px(H)], fill=INK)
    parts = [part.strip() for part in stories_by_tier("ticker")[0]["deck"].split("•")]
    lines = [parts[0], " • ".join(parts[1:])]
    size = 15
    font = load_font(SANS_BOLD, size)
    while size > 15 and any(text_width(draw, line, font) > W - 48 for line in lines):
        size -= 1
        font = load_font(SANS_BOLD, size)
    for line in lines:
        if text_width(draw, line, font) > W - 48:
            print(f"ticker overflow {text_width(draw, line, font):.0f}px: {line}")
    advance = size * 1.25
    block = advance * len(lines)
    y = 968 + (56 - block) / 2
    for line in lines:
        width = text_width(draw, line, font)
        draw_text(draw, (W - width) / 2, y, line, font, PAPER)
        y += advance
    print(f"ticker {size}px, {len(lines)} lines")


def draw_masthead(draw):
    title = "THE WORLD IN ONE PAGE"
    title_size = 44
    title_font = load_font(SERIF_BOLD, title_size)
    while text_width(draw, title, title_font) > W - 2 * MARGIN and title_size > 36:
        title_size -= 1
        title_font = load_font(SERIF_BOLD, title_size)
    title_w, _title_h = text_size(draw, title, title_font)
    draw_text(draw, (W - title_w) / 2, 8, title, title_font, INK)

    date_font = load_font(SANS_BOLD, 16)
    tracking = 1.4
    day_left, day_right = "TUESDAY", "24 NOVEMBER 2026"
    left_w = tracked_width(draw, day_left, date_font, tracking)
    right_w = tracked_width(draw, day_right, date_font, tracking)
    dash_gap, dash_w = 10, 14
    date_w = left_w + dash_gap + dash_w + dash_gap + right_w
    date_x = MARGIN
    date_y = 58
    draw_tracked(draw, date_x, date_y, day_left, date_font, INK, tracking)
    _text_w, text_h = text_size(draw, day_left, date_font)
    dash_x = date_x + left_w + dash_gap
    dash_y = date_y + text_h * 0.55
    draw.line(
        [(px(dash_x), px(dash_y)), (px(dash_x + dash_w), px(dash_y))],
        fill=INK,
        width=px(2),
    )
    draw_tracked(draw, dash_x + dash_w + dash_gap, date_y, day_right, date_font, INK, tracking)
    strap = strapline()
    strap_w, _strap_h = text_size(draw, strap, date_font)
    draw_text(draw, W - MARGIN - strap_w, date_y, strap, date_font, INK)

    draw.line([(px(MARGIN), px(86)), (px(W - MARGIN), px(86))], fill=INK, width=px(1))
    draw.line([(px(MARGIN), px(90)), (px(W - MARGIN), px(90))], fill=INK, width=px(1))
    print(f"masthead strap {strap}, title {title_size}px, date block {date_w:.0f}px")


def save(image):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    page = image.resize((W, H), Image.Resampling.LANCZOS)
    page.save(OUT, "PNG", optimize=True)
    if OUT.stat().st_size > 1024 * 1024:
        reduced = page.quantize(
            colors=256,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )
        reduced.save(OUT, "PNG", optimize=True)


def block_color(name):
    return {
        "EUROPE": EUROPE,
        "MIDDLE EAST": MIDDLE_EAST,
        "ASIA": ASIA,
        "AFRICA": AFRICA,
        "AMERICAS": AMERICAS,
        "OCEANIA": OCEANIA,
        "MARKETS": BUSINESS,
        "CULTURE & SCIENCE": RELIGION,
    }[name]


def draw_region_item(draw, x, y, width, story, color, size, line_h=None):
    lead_font = load_font(SANS_BOLD, size)
    body_font = load_font(SANS, size)
    bullet_x = x
    text_x = x + 12
    text_w = width - 12
    lead = story["lead"]
    words = story["text"].split()
    lead_w = text_width(draw, lead, lead_font)
    first = ""
    index = 0
    while index < len(words):
        trial = words[index] if not first else first + " " + words[index]
        gap = text_width(draw, " " + trial, body_font)
        if lead_w + gap <= text_w:
            first = trial
            index += 1
        else:
            break
    draw.ellipse([px(bullet_x), px(y + 4), px(bullet_x + 6), px(y + 10)], fill=color)
    draw_text(draw, text_x, y, lead, lead_font, BRIEF_INK)
    if first:
        draw_text(draw, text_x + lead_w + 4, y, first, body_font, BRIEF_INK)
    if line_h is None:
        line_h = size * 1.2
    lines = 1
    leftover = False
    if index < len(words):
        rest = " ".join(words[index:])
        wrapped = wrap_text(draw, rest, body_font, text_w)
        draw_text(draw, text_x, y + line_h, wrapped[0], body_font, BRIEF_INK)
        lines = 2
        leftover = len(wrapped) > 1
    return lines * line_h, leftover


def item_line_count(draw, width, story, size):
    _used, leftover = draw_region_item(draw, -800, -800, width, story, INK, size)
    return (2 if leftover or _used > size * 1.3 else 1), leftover


def draw_region_grid(draw):
    from stories import BLOCKS, items_in_block

    gap = 12
    columns = 4
    block_w = (W - 2 * MARGIN - gap * (columns - 1)) / columns
    zone_top = 530
    zone_bottom = 996
    rows = [BLOCKS[:columns], BLOCKS[columns:]]
    row_meta = []
    for names in rows:
        blocks = []
        row_lines = 0
        for name in names:
            items = items_in_block(name)
            size = 14
            counts = []
            while size > 13:
                counts = [item_line_count(draw, block_w - 16, item, size) for item in items]
                if not any(flag for _count, flag in counts):
                    break
                size -= 1
            line_count = sum(count for count, _flag in counts)
            natural = 30 + line_count * size * 1.2 + max(0, len(items) - 1) * 10
            blocks.append((name, items, size, line_count, natural))
            row_lines = max(row_lines, line_count)
        row_meta.append((blocks, max(block[4] for block in blocks), row_lines))
    spare = (zone_bottom - zone_top - gap) - sum(row[1] for row in row_meta)
    y = zone_top
    for blocks, natural, _row_lines in row_meta:
        weight = natural / sum(row[1] for row in row_meta)
        row_h = natural + spare * weight
        for name, items, size, line_count, _natural in blocks:
            x = MARGIN + (BLOCKS.index(name) % columns) * (block_w + gap)
            color = block_color(name)
            draw.rectangle([px(x), px(y), px(x + block_w), px(y + 24)], fill=color)
            header_font = load_font(SANS_BOLD, 13)
            draw_text(draw, x + 8, y + 4, name, header_font, PAPER)
            count = str(len(items))
            count_w, _count_h = text_size(draw, count, header_font)
            draw_text(draw, x + block_w - 8 - count_w, y + 4, count, header_font, PAPER)
            rules = max(0, len(items) - 1) * 10
            slack = row_h - 30 - rules
            line_h = slack / line_count if line_count else size * 1.2
            cursor = y + 30
            for item_index, item in enumerate(items):
                used, leftover = draw_region_item(
                    draw, x + 8, cursor, block_w - 16, item, color, size, line_h
                )
                cursor += used
                if leftover:
                    print(f"grid clipped {name}: {item['lead']}")
                if item_index < len(items) - 1:
                    cursor += 3
                    draw.line(
                        [(px(x + 8), px(cursor)), (px(x + block_w - 8), px(cursor))],
                        fill=RULE,
                        width=px(1),
                    )
                    cursor += 5
            print(f"grid {name} {len(items)} items at {size}px, row {row_h:.0f}px, line {line_h:.1f}px")
        y += row_h + gap


def draw_footer(draw):
    font = load_font(SANS, 12)
    line = "Sources: AP, Reuters, AFP, Al Jazeera, BBC, ABC Australia · all stories dated Tue 24 Nov 2026 (UTC)"
    width = text_width(draw, line, font)
    if width > W - 2 * MARGIN:
        font = load_font(SANS, 11)
        width = text_width(draw, line, font)
    draw_text(draw, (W - width) / 2, 1004, line, font, MUTED)


def main():
    image = Image.new("RGB", (px(W), px(H)), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_lead(image, draw)
    draw_top_tiles(draw)
    draw_region_grid(draw)
    draw_footer(draw)
    save(image)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
