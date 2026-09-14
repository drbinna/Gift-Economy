from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

W, H = letter
OUT = "/mnt/user-data/outputs/gift-economy-simple.pdf"

SETS = [
    ("A", colors.HexColor("#1F6FB2"), "circle"),
    ("B", colors.HexColor("#C2392B"), "square"),
    ("C", colors.HexColor("#2E8B57"), "triangle"),
    ("D", colors.HexColor("#7D3C98"), "diamond"),
    ("E", colors.HexColor("#B8860B"), "cross"),
]
INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#6B6B6B")
PRIZE = colors.HexColor("#0F6E4F")


def shape(c, kind, cx, cy, r, col):
    c.saveState()
    c.setFillColor(col)
    if kind == "circle":
        c.circle(cx, cy, r, stroke=0, fill=1)
    elif kind == "square":
        c.rect(cx - r, cy - r, 2 * r, 2 * r, stroke=0, fill=1)
    elif kind == "triangle":
        p = c.beginPath()
        p.moveTo(cx, cy + r); p.lineTo(cx + r, cy - r); p.lineTo(cx - r, cy - r); p.close()
        c.drawPath(p, stroke=0, fill=1)
    elif kind == "diamond":
        p = c.beginPath()
        p.moveTo(cx, cy + r); p.lineTo(cx + r, cy); p.lineTo(cx, cy - r); p.lineTo(cx - r, cy); p.close()
        c.drawPath(p, stroke=0, fill=1)
    elif kind == "cross":
        t = r * 0.45
        c.rect(cx - t, cy - r, 2 * t, 2 * r, stroke=0, fill=1)
        c.rect(cx - r, cy - t, 2 * r, 2 * t, stroke=0, fill=1)
    c.restoreState()


def number_card(c, x, y, w, h, num, letter_, col, kind):
    c.setLineWidth(1.4)
    c.setStrokeColor(col)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 6, stroke=1, fill=1)

    c.setFillColor(col)
    c.rect(x + 2.5, y + h - 16, w - 5, 12, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 7, y + h - 12.5, letter_)
    shape(c, kind, x + w - 10, y + h - 9.5, 3.4, colors.white)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 52)
    c.drawCentredString(x + w / 2, y + h / 2 - 16, str(num))

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(col)
    c.drawString(x + 7, y + h - 30, str(num))
    c.drawRightString(x + w - 7, y + 9, str(num))


def prize_card(c, x, y, w, h, val):
    c.setLineWidth(1.4)
    c.setStrokeColor(PRIZE)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 6, stroke=1, fill=1)

    c.setFillColor(PRIZE)
    c.rect(x + 2.5, y + h - 16, w - 5, 12, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2, y + h - 12.5, "PRIZE")

    c.setFillColor(PRIZE)
    c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(x + w / 2, y + h / 2 - 10, str(val))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x + w / 2, y + h / 2 - 22, "POINTS")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 5.8)
    c.drawCentredString(x + w / 2, y + 16, "Highest unique number")
    c.drawCentredString(x + w / 2, y + 9, "takes this card.")


def grid(cols, rows, cw, ch, gap=5):
    tw = cols * cw + (cols - 1) * gap
    th = rows * ch + (rows - 1) * gap
    x0 = (W - tw) / 2
    y0 = (H - th) / 2 - 8
    return [(x0 + ci * (cw + gap), y0 + (rows - 1 - ri) * (ch + gap))
            for ri in range(rows) for ci in range(cols)]


def wrap(c, text, x, y, width, size, leading, font="Helvetica", col=INK):
    c.setFont(font, size); c.setFillColor(col)
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if c.stringWidth(trial, font, size) <= width:
            line = trial
        else:
            c.drawString(x, y, line); y -= leading; line = word
    if line:
        c.drawString(x, y, line); y -= leading
    return y


def rules_page(c):
    L = 0.9 * inch
    RW = W - 2 * L
    y = H - 1.0 * inch

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(L, y, "THE GIFT ECONOMY")
    y -= 19
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(MUTED)
    c.drawString(L, y, "3-5 players.  10 minutes.  Three rules.")
    y -= 12
    c.setStrokeColor(INK); c.setLineWidth(1.2)
    c.line(L, y, W - L, y)
    y -= 34

    c.setFont("Helvetica-Bold", 12); c.setFillColor(INK)
    c.drawString(L, y, "SETUP")
    y -= 15
    y = wrap(c, "Each player takes one coloured set of cards numbered 1 to 7. That is your hand "
                "all game. Shuffle the nine green Prize cards face down in the middle.",
             L, y, RW, 10, 13.5) - 22

    c.setFont("Helvetica-Bold", 12); c.setFillColor(INK)
    c.drawString(L, y, "EACH ROUND")
    y -= 17

    rules = [
        ("1", "BID.", "Flip the top Prize. Everyone secretly plays one card face down, then all "
                      "reveal at once."),
        ("2", "CANCEL.", "Any number played by more than one player is crossed out. The highest "
                         "number still standing takes the Prize."),
        ("3", "GIVE.", "Everyone passes the card they just played to the player on their left. "
                       "It goes into that player's hand."),
    ]
    for num, bold, text in rules:
        c.setFillColor(colors.HexColor("#DDDDDD"))
        c.circle(L + 8, y + 3, 10, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(L + 8, y, num)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(L + 26, y, bold)
        off = c.stringWidth(bold, "Helvetica-Bold", 10.5) + 5
        # first line starts after the bold label, later lines return to L+26
        c.setFont("Helvetica", 10)
        c.setFillColor(INK)
        words = text.split()
        cx, cw_avail, line = L + 26 + off, RW - 26 - off, ""
        first = True
        for word in words:
            trial = (line + " " + word).strip()
            if c.stringWidth(trial, "Helvetica", 10) <= cw_avail:
                line = trial
            else:
                c.drawString(cx, y, line)
                y -= 13.5
                if first:
                    cx, cw_avail, first = L + 26, RW - 26, False
                line = word
        if line:
            c.drawString(cx, y, line)
            y -= 13.5
        y -= 12

    y -= 6
    c.setFont("Helvetica-Bold", 12); c.setFillColor(INK)
    c.drawString(L, y, "WINNING")
    y -= 15
    y = wrap(c, "After all nine Prizes are gone, add up the points in front of you. Most points wins.",
             L, y, RW, 10, 13.5) - 24

    c.setFillColor(colors.HexColor("#F2F2F2"))
    c.rect(L, y - 52, RW, 62, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(L + 12, y - 4, "THE CATCH")
    yy = y - 19
    wrap(c, "Winning costs you your best card and hands it straight to your neighbour. Playing "
            "a 1 loses the round on purpose, but clogs their hand with junk. And if you are "
            "sure two people will both slam their 7, a 5 wins it outright.",
         L + 12, yy, RW - 24, 9, 12)

    y -= 76
    c.setStrokeColor(MUTED); c.setLineWidth(0.6); c.setDash(2, 2)
    c.line(L, y, W - L, y); c.setDash()
    y -= 18

    c.setFont("Helvetica-Bold", 10.5); c.setFillColor(INK)
    c.drawString(L, y, "PLAYTEST LOG")
    y -= 15
    c.setFont("Helvetica", 8.6); c.setFillColor(MUTED)
    for line in ["Seconds per round ......      Winner ......      Last place ......",
                 "Did anyone dump a 1 or 2 on purpose?   Y / N",
                 "Was the last round still tense?   Y / N"]:
        c.drawString(L + 3, y, line); y -= 13
    y -= 4
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.6)
    c.drawString(L, y, "What broke, and what I changed:")
    y -= 15
    c.setStrokeColor(colors.HexColor("#BBBBBB")); c.setLineWidth(0.5)
    for _ in range(3):
        c.line(L, y, W - L, y); y -= 15

    c.setFont("Helvetica-Oblique", 7.4); c.setFillColor(MUTED)
    c.drawString(L, 0.6 * inch, "Cancel-on-tie bidding comes from Alex Randolph's Raj (1988). "
                                "Passing your spent card to the left is this game's own addition.")
    c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("The Gift Economy - Simple Prototype")
    rules_page(c)

    cw, ch = 1.75 * inch, 2.5 * inch
    slots = grid(4, 4, cw, ch)

    pages = [
        ("Player hands 1 and 2 - cut out, one colour each", [0, 1]),
        ("Player hands 3 and 4 - cut out, one colour each", [2, 3]),
        ("Player hand 5 (only for a 5-player game)  +  the nine Prize cards", [4]),
    ]

    for header, setidx in pages:
        c.setFont("Helvetica", 7.5); c.setFillColor(MUTED)
        c.drawString(0.75 * inch, H - 0.45 * inch, header)
        i = 0
        for si in setidx:
            letter_, col, kind = SETS[si]
            for n in range(1, 8):
                x, y = slots[i]
                number_card(c, x, y, cw, ch, n, letter_, col, kind)
                i += 1
        if len(setidx) == 1:
            for v in range(1, 10):
                x, y = slots[i]
                prize_card(c, x, y, cw, ch, v)
                i += 1
        c.showPage()

    c.save()
    print("wrote", OUT)


build()
