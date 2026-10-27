"""Build The Visibility Kit v2: fillable + printable A4 PDF, Kaizen XP black and gold."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = A4
M = 46
CW = W - 2 * M
BOTTOM = 50

BLACK = HexColor('#0d0d0d')
GOLD = HexColor('#c9a84c')
CREAM = HexColor('#f3efe4')
INK = HexColor('#1a1a1a')
BODY = HexColor('#333333')
GREY = HexColor('#666666')
LGREY = HexColor('#9a9a9a')
LINE = HexColor('#d3ccb8')
FIELDINK = HexColor('#1d2b45')
EXINK = HexColor('#2b3f63')

class Overflow(Exception):
    pass


class Kit:
    def __init__(self, path, title='The Visibility Kit', subject=''):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle(title)
        self.c.setAuthor('Kaizen XP')
        self.c.setSubject(subject)
        self.product = title.upper()
        self.page = 0
        self.y = 0
        self.names = set()

    # ---------- basics ----------
    def font(self, name, size, color=INK):
        self.c.setFont(name, size)
        self.c.setFillColor(color)

    def text(self, x, y, s, name='Helvetica', size=8.5, color=INK, align='left', cs=0):
        self.font(name, size, color)
        w = stringWidth(s, name, size) + cs * max(len(s) - 1, 0)
        if align == 'center':
            x = x - w / 2
        elif align == 'right':
            x = x - w
        t = self.c.beginText(x, y)
        t.setFont(name, size)
        t.setCharSpace(cs)
        t.textOut(s)
        self.c.drawText(t)
        return w

    def need(self, h):
        if self.y - h < BOTTOM:
            raise Overflow(f'Page {self.page}: needs {h:.0f}pt, only {self.y - BOTTOM:.0f}pt left')

    def gap(self, g):
        self.y -= g

    def wrap(self, s, name, size, width):
        out = []
        for p in s.split('\n'):
            out += simpleSplit(p, name, size, width) or ['']
        return out

    def para(self, s, size=8.5, name='Helvetica', color=BODY, leading=None, width=CW, x=M, after=7):
        leading = leading or size * 1.45
        lines = self.wrap(s, name, size, width)
        h = leading * len(lines)
        self.need(h)
        for ln in lines:
            self.y -= leading
            self.text(x, self.y + (leading - size) * 0.55, ln, name, size, color)
        self.y -= after
        return h

    # ---------- page furniture ----------
    def chrome(self):
        c = self.c
        c.setFillColor(BLACK)
        c.rect(0, H - 16, W, 16, fill=1, stroke=0)
        c.rect(0, 0, W, 22, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(0, H - 17.5, W, 1.5, fill=1, stroke=0)
        c.rect(0, 22, W, 1.5, fill=1, stroke=0)
        self.text(M, 32, 'KAIZEN XP  |  ' + self.product, 'Helvetica', 6.3, LGREY, cs=0.6)
        self.text(W - M, 32, 'Do what nobody else can be bothered to do.', 'Helvetica-Oblique', 6.3, LGREY, align='right')
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(M, 41, W - M, 41)

    def new_page(self, title, label, subtitle):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.chrome()
        c = self.c
        c.setFillColor(BLACK)
        c.rect(M, H - 66, CW, 28, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(M, H - 68.5, CW, 2.5, fill=1, stroke=0)
        self.text(M + 12, H - 56, title, 'Helvetica-Bold', 11, white, cs=0.3)
        if label:
            self.text(W - M - 12, H - 55.5, label, 'Helvetica-Bold', 6.3, GOLD, align='right', cs=0.8)
        self.text(M, H - 82, subtitle, 'Helvetica-Oblique', 7.6, GREY)
        self.y = H - 92

    # ---------- blocks ----------
    def note(self, title, body, size=8, fill=CREAM, after=10, width=CW, x=M):
        pad = 10
        tl = self.wrap(body, 'Helvetica', size, width - 2 * pad - 4) if body else []
        h = pad + 9 + (len(tl) * size * 1.42) + pad - 2
        self.need(h)
        c = self.c
        top = self.y
        c.setFillColor(fill)
        c.rect(x, top - h, width, h, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(x, top - h, 3, h, fill=1, stroke=0)
        yy = top - pad - 6
        self.text(x + pad + 4, yy, title, 'Helvetica-Bold', 7, INK, cs=0.5)
        yy -= 4
        for ln in tl:
            yy -= size * 1.42
            self.text(x + pad + 4, yy + 2, ln, 'Helvetica', size, BODY)
        self.y = top - h - after
        return h

    def label(self, s, right=None, after=8):
        self.need(16)
        self.y -= 9
        self.text(M, self.y, s, 'Helvetica-Bold', 7.3, INK, cs=0.5)
        if right:
            self.text(W - M, self.y, right, 'Helvetica-Oblique', 6.5, GREY, align='right')
        self.y -= 4
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(0.9)
        self.c.line(M, self.y, W - M, self.y)
        self.y -= after

    def box(self, x, y, w, h, fill=white, stroke=LINE):
        self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(0.6)
        self.c.rect(x, y, w, h, fill=1, stroke=1)

    def _name(self, n):
        assert n not in self.names, n
        self.names.add(n)
        return n

    def tf(self, name, x, y, w, h, multiline=False, tip=None, size=None, fill=white):
        self.box(x, y, w, h, fill=fill)
        size = size or (8 if multiline else 8.5)
        self.c.acroForm.textfield(
            name=self._name(name), tooltip=tip or name, x=x, y=y, width=w, height=h,
            borderWidth=0, fillColor=None, textColor=FIELDINK, fontName='Helvetica', fontSize=size,
            fieldFlags='multiline' if multiline else '', maxlen=2000 if multiline else 200,
            annotationFlags='print')

    def dd(self, name, x, y, w, h, options, tip=None, fill=white):
        self.box(x, y, w, h, fill=fill)
        # small gold arrow so people know it is a list (and prints harmlessly)
        cx, cy = x + w - 8, y + h / 2
        p = self.c.beginPath()
        p.moveTo(cx - 3, cy + 1.6)
        p.lineTo(cx + 3, cy + 1.6)
        p.lineTo(cx, cy - 2)
        p.close()
        self.c.setFillColor(GOLD)
        self.c.drawPath(p, fill=1, stroke=0)
        self.c.acroForm.choice(
            name=self._name(name), tooltip=tip or name, x=x, y=y, width=w - 14, height=h,
            borderWidth=0, fillColor=None, textColor=FIELDINK, fontName='Helvetica', fontSize=8,
            options=[' '] + options, value=' ', fieldFlags='combo', annotationFlags='print')

    def ex(self, x, y, w, h, s, size=8, fill=white):
        """Static example 'filled in' box."""
        self.box(x, y, w, h, fill=fill)
        lines = self.wrap(s, 'Helvetica-Oblique', size, w - 8)
        yy = y + h - size - 3
        for ln in lines:
            self.text(x + 4, yy, ln, 'Helvetica-Oblique', size, EXINK)
            yy -= size * 1.3

    def small(self, x, y, s, color=GREY, size=6.3, bold=True):
        self.text(x, y, s, 'Helvetica-Bold' if bold else 'Helvetica', size, color, cs=0.4)
        return stringWidth(s, 'Helvetica-Bold' if bold else 'Helvetica', size) + 0.4 * (len(s) - 1)

    def bar(self, x, y, w, h, left, right=None, example=False):
        self.c.setFillColor(BLACK)
        self.c.rect(x, y, w, h, fill=1, stroke=0)
        self.text(x + 8, y + h / 2 - 2.3, left, 'Helvetica-Bold', 6.8, GOLD, cs=0.6)
        if example:
            tag = 'WORKED EXAMPLE'
            tw = stringWidth(tag, 'Helvetica-Bold', 5.8) + 0.6 * (len(tag) - 1) + 10
            tx = x + 8 + stringWidth(left, 'Helvetica-Bold', 6.8) + 0.6 * (len(left) - 1) + 8
            self.c.setFillColor(GOLD)
            self.c.roundRect(tx, y + 3, tw, h - 6, 2, fill=1, stroke=0)
            self.text(tx + 5, y + h / 2 - 2, tag, 'Helvetica-Bold', 5.8, BLACK, cs=0.6)

    # ---------- reusable records ----------
    def coaching_record(self, n, example=None):
        h = 141
        self.need(h)
        x, top = M, self.y
        self.box(x, top - h, CW, h)
        self.bar(x, top - 16, CW, 16, f'COACHING RECORD {n}' if not example else 'COACHING RECORD', example=bool(example))
        ix, iw = x + 8, CW - 16
        y = top - 16 - 7 - 16
        e = example or {}
        # row 1
        cx = ix
        cx += self.small(cx, y + 5, 'DATE') + 5
        self._f(e, 'date', f'c{n}_date', cx, y, 62, 16, tip='Coaching date'); cx += 62 + 10
        cx += self.small(cx, y + 5, 'WHO I COACHED') + 5
        self._f(e, 'who', f'c{n}_who', cx, y, 112, 16, tip='Who I coached'); cx += 112 + 10
        cx += self.small(cx, y + 5, 'WHERE ARE THEY NOW?') + 5
        self._d(e, 'now', f'c{n}_now', cx, y, ix + iw - cx, 16,
                ['Can do it alone now', 'Nearly there, one more go', 'Started, more to do'], tip='Where are they now?')
        # row 2
        y -= 22
        cx = ix + self.small(ix, y + 5, 'TASK OR SKILL') + 5
        self._f(e, 'task', f'c{n}_task', cx, y, ix + iw - cx, 16, tip='Task or skill')
        # row 3
        y -= 12
        self.small(ix, y, 'WHAT THEY COULD NOT DO BEFORE / CAN DO NOW')
        y -= 33
        self._f(e, 'before', f'c{n}_before', ix, y, iw, 29, multiline=True, tip='What they could not do before, and can do now')
        # sign strip
        sy = top - h
        self.c.setFillColor(CREAM)
        self.c.rect(x + 0.3, sy + 0.3, CW - 0.6, 26, fill=1, stroke=0)
        self.c.setFillColor(GOLD)
        self.c.rect(x, sy, 3, 26, fill=1, stroke=0)
        fy = sy + 5
        cx = ix + 2
        cx += self.small(cx, fy + 5, 'SIGNED (THEM)') + 5
        self._f(e, 's1', f'c{n}_sig_them', cx, fy, 84, 16, tip='Signed by the person coached', fill=white); cx += 84 + 9
        cx += self.small(cx, fy + 5, 'SIGNED (LINE LEADER)') + 5
        self._f(e, 's2', f'c{n}_sig_leader', cx, fy, 84, 16, tip='Signed by line leader', fill=white); cx += 84 + 9
        cx += self.small(cx, fy + 5, 'SIGN-OFF') + 5
        self._d(e, 'status', f'c{n}_status', cx, fy, ix + iw - cx, 16, ['Signed off', 'Waiting for sign-off'], tip='Sign-off status')
        self.y = top - h - 10

    def improvement_record(self, n, example=None):
        h = 165
        self.need(h)
        x, top = M, self.y
        e = example or {}
        self.box(x, top - h, CW, h)
        self.bar(x, top - 16, CW, 16, f'IMPROVEMENT {n}' if not example else 'IMPROVEMENT', example=bool(example))
        # date on the bar
        dx = x + CW - 8 - 70
        self.text(dx - 6, top - 10.8, 'DATE', 'Helvetica-Bold', 6.3, GOLD, align='right', cs=0.4)
        self._f(e, 'date', f'i{n}_date', dx, top - 14, 70, 12, tip='Improvement date', size=7.5)
        ix, iw = x + 8, CW - 16
        lw = 92
        y = top - 16 - 6
        rows = [('THE PROBLEM', None, 'problem'), ('WHAT I CHANGED', None, 'changed'),
                ('THE RESULT', '(time, waste, cost, safety)', 'result')]
        for lab, sub, key in rows:
            y -= 27
            self.small(ix, y + 18, lab, INK)
            if sub:
                self.text(ix, y + 10, sub, 'Helvetica-Oblique', 6, GREY)
            self._f(e, key, f'i{n}_{key}', ix + lw, y, iw - lw, 25, multiline=True, tip=lab.title())
            y -= 3
        y -= 19
        cx = ix + self.small(ix, y + 5, 'RESULT TYPE', INK) + 5
        cx = ix + lw
        self._d(e, 'type', f'i{n}_type', cx, y, 122, 16,
                ['Time', 'Waste', 'Cost', 'Safety', 'Quality', 'More than one'], tip='Result type')
        cx += 122 + 12
        cx += self.small(cx, y + 5, 'WORTH ROUGHLY', INK) + 5
        self._f(e, 'worth', f'i{n}_worth', cx, y, ix + iw - cx, 16, tip='Worth roughly (hours or pounds, see Put a Number On It)')
        sy = top - h
        self.c.setFillColor(CREAM)
        self.c.rect(x + 0.3, sy + 0.3, CW - 0.6, 26, fill=1, stroke=0)
        self.c.setFillColor(GOLD)
        self.c.rect(x, sy, 3, 26, fill=1, stroke=0)
        fy = sy + 5
        cx = ix + 2
        cx += self.small(cx, fy + 5, 'WHO SAW IT / WHO DID I TELL?', INK) + 6
        self._d(e, 'saw', f'i{n}_saw', cx, fy, 110, 16, ['Line leader', 'Manager', 'Line leader and manager', 'Wider team', 'Nobody yet'], tip='Who saw it')
        cx += 110 + 10
        cx += self.small(cx, fy + 5, 'NAME(S)', INK) + 5
        self._f(e, 'names', f'i{n}_names', cx, fy, ix + iw - cx, 16, tip='Names of who saw it')
        self.y = top - h - 10

    # example-aware field helpers
    def _f(self, e, key, name, x, y, w, h, multiline=False, tip=None, size=None, fill=white):
        if e:
            if key in e:
                self.ex(x, y, w, h, e[key], size=7.6 if (multiline or h > 18) else 7.8, fill=fill)
            else:
                self.box(x, y, w, h, fill=fill)
        else:
            self.tf(name, x, y, w, h, multiline=multiline, tip=tip, size=size, fill=fill)

    def _d(self, e, key, name, x, y, w, h, options, tip=None):
        if e:
            self.ex(x, y, w, h, e.get(key, ''), size=7.8)
        else:
            self.dd(name, x, y, w, h, options, tip=tip)

    # ---------- table ----------
    def table(self, prefix, cols, rows, row_h=20, head_h=18, example_row=None, start=1):
        """cols: list of (header, width, kind, options). kind in text|dd|static"""
        widths = [c[1] for c in cols]
        flex = CW - sum(w for w in widths if w)
        widths = [w if w else flex for w in widths]
        if rows == 'fill':
            rows = int((self.y - BOTTOM - 4 - head_h - (row_h if example_row else 0)) // row_h)
        total = head_h + row_h * (rows + (1 if example_row else 0))
        self.need(total)
        top = self.y
        c = self.c
        c.setFillColor(BLACK)
        c.rect(M, top - head_h, CW, head_h, fill=1, stroke=0)
        x = M
        for (hd, _, _, _), w in zip(cols, widths):
            parts = hd.split('\n')
            yy = top - head_h / 2 + (len(parts) - 1) * 3.6 - 2.2
            for p in parts:
                self.text(x + 6, yy, p, 'Helvetica-Bold', 6.2, GOLD, cs=0.5)
                yy -= 7.2
            x += w
        y = top - head_h
        if example_row:
            y -= row_h
            x = M
            c.setFillColor(CREAM)
            c.rect(M, y, CW, row_h, fill=1, stroke=0)
            for val, w in zip(example_row, widths):
                c.setStrokeColor(LINE); c.setLineWidth(0.6); c.rect(x, y, w, row_h, fill=0, stroke=1)
                ls = self.wrap(val, 'Helvetica-Oblique', 7.4, w - 8)
                yy = y + row_h / 2 + (len(ls) - 1) * 4.4 - 2.6
                for ln in ls:
                    self.text(x + 4, yy, ln, 'Helvetica-Oblique', 7.4, EXINK)
                    yy -= 8.8
                x += w
            self.text(M + CW + 3, y + row_h / 2 - 2, '', 'Helvetica', 6)
        for r in range(rows):
            y -= row_h
            x = M
            for ci, ((hd, _, kind, opts), w) in enumerate(zip(cols, widths)):
                n = f'{prefix}_r{start + r}_c{ci + 1}'
                if kind == 'text':
                    self.tf(n, x, y, w, row_h, tip=f'{hd.replace(chr(10), " ").title()} (row {start + r})', size=8)
                elif kind == 'dd':
                    self.dd(n, x, y, w, row_h, opts, tip=f'{hd.replace(chr(10), " ").title()} (row {start + r})')
                elif kind == 'static':
                    self.box(x, y, w, row_h)
                    self.text(x + 6, y + row_h / 2 - 2.6, opts[r], 'Helvetica-Bold', 7.4, INK)
                x += w
        self.y = y - 10
        self.last_row = start + rows - 1
        return total



def cover(k, title_lines, sub_lines, badge, kicker, audience):
    c = k.c
    k.page = 1
    c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)
    c.setStrokeColor(HexColor('#3a3a3a')); c.setLineWidth(0.5); c.rect(36, 36, W - 72, H - 72, fill=0, stroke=1)
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(W / 2 - 46, H - 228, 92, 56, fill=0, stroke=1)
    k.text(W / 2, H - 209, 'XP', 'Helvetica-Bold', 26, GOLD, align='center')
    k.text(W / 2, H - 258, 'KAIZEN XP', 'Helvetica-Bold', 8.5, GOLD, align='center', cs=4.5)
    c.setStrokeColor(HexColor('#555555')); c.setLineWidth(0.5); c.line(W / 2 - 70, H - 272, W / 2 + 70, H - 272)
    y = H - 330
    for t in title_lines:
        k.text(W / 2, y, t, 'Helvetica-Bold', 32, white, align='center'); y -= 38
    y -= 0
    for t in sub_lines:
        k.text(W / 2, y, t, 'Helvetica', 11.5, GOLD, align='center'); y -= 16
    y -= 22
    bw = stringWidth(badge, 'Helvetica-Bold', 7.5) + 2.2 * len(badge) + 40
    c.setFillColor(GOLD); c.rect(W / 2 - bw / 2, y - 6, bw, 22, fill=1, stroke=0)
    k.text(W / 2, y + 2, badge, 'Helvetica-Bold', 7.5, BLACK, align='center', cs=2.2)
    y -= 26
    k.text(W / 2, y, kicker, 'Helvetica-Bold', 6.6, HexColor('#bdbdbd'), align='center', cs=1.8)
    y -= 32
    c.setStrokeColor(HexColor('#444444')); c.line(90, y, W - 90, y)
    k.text(W / 2, y - 42, '"Do what nobody else can be bothered to do,', 'Helvetica-Oblique', 12, white, align='center')
    k.text(W / 2, y - 60, 'and you\'ll get what nobody else gets."', 'Helvetica-Oblique', 12, white, align='center')
    c.line(90, y - 100, W - 90, y - 100)
    k.text(W / 2, 80, audience, 'Helvetica', 6.8, HexColor('#8a8a8a'), align='center', cs=3)


def back(k, heading, big, gold, items_title, items_desc, items, closer):
    c = k.c
    c.showPage(); k.page += 1
    c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)
    c.setStrokeColor(HexColor('#3a3a3a')); c.setLineWidth(0.5); c.rect(36, 36, W - 72, H - 72, fill=0, stroke=1)
    k.text(W / 2, H - 150, heading, 'Helvetica-Bold', 8.5, GOLD, align='center', cs=4)
    k.text(W / 2, H - 200, big, 'Helvetica-Bold', 24, white, align='center')
    k.text(W / 2, H - 230, gold, 'Helvetica', 14, GOLD, align='center')
    c.setStrokeColor(HexColor('#444444')); c.line(110, H - 262, W - 110, H - 262)
    yy = H - 300
    for t, d in items:
        k.text(W / 2, yy, t, 'Helvetica-Bold', 10.5, white, align='center', cs=1.5)
        k.text(W / 2, yy - 15, d, 'Helvetica', 8.6, HexColor('#c8c8c8'), align='center')
        yy -= 44
    k.text(W / 2, yy - 6, closer, 'Helvetica-Oblique', 8.8, GOLD, align='center')
    k.text(W / 2, yy - 22, 'All available from Kaizen XP.', 'Helvetica', 8.8, HexColor('#c8c8c8'), align='center')
    c.setStrokeColor(HexColor('#444444')); c.line(110, 250, W - 110, 250)
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(W / 2 - 34, 172, 68, 42, fill=0, stroke=1)
    k.text(W / 2, 186, 'XP', 'Helvetica-Bold', 19, GOLD, align='center')
    k.text(W / 2, 150, '"Do what nobody else can be bothered to do, and you\'ll get what nobody else gets."', 'Helvetica-Oblique', 9, white, align='center')
    k.text(W / 2, 62, '\u00a9 2026 Kaizen XP. Licensed for one person\'s use. Please do not share or resell.', 'Helvetica', 6.5, HexColor('#7a7a7a'), align='center')


def strip_box(k, label, name, h, right=None, example=None):
    """Cream label strip + big multiline field (or example text)."""
    k.need(h + 22)
    top = k.y
    c = k.c
    c.setFillColor(CREAM); c.rect(M, top - 15, CW, 15, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(M, top - 15, 3, 15, fill=1, stroke=0)
    k.text(M + 9, top - 10, label, 'Helvetica-Bold', 6.6, INK, cs=0.4)
    if right:
        k.text(W - M - 8, top - 10, right, 'Helvetica-Oblique', 6.3, GREY, align='right')
    if example is not None:
        k.ex(M, top - 15 - h, CW, h, example)
    else:
        k.tf(name, M, top - 15 - h, CW, h, multiline=True, tip=label.capitalize())
    k.y = top - 15 - h - 9


def inline_fields(k, specs, h=16, after=10):
    """specs: list of (label, name, width or 0 for rest, kind, options)"""
    k.need(h + 6)
    k.y -= h
    x = M
    fixed = sum(s[2] for s in specs if s[2]) + sum(stringWidth(s[0], 'Helvetica-Bold', 6.3) + 0.4 * len(s[0]) + 6 for s in specs) + 14 * (len(specs) - 1)
    for lab, name, w, kind, opts in specs:
        x += k.small(x, k.y + 5, lab, INK) + 6
        ww = w or (M + CW - fixed) + 0  # rest
        if not w:
            ww = M + CW - x if specs[-1][1] == name else max(60, M + CW - fixed)
        if kind == 'dd':
            k.dd(name, x, k.y, ww, h, opts, tip=lab.title())
        else:
            k.tf(name, x, k.y, ww, h, tip=lab.title())
        x += ww + 14
    k.y -= after


def checkbox(k, name, x, y, size=11, tip=None):
    k.box(x, y, size, size)
    k.c.acroForm.checkbox(name=k._name(name), tooltip=tip or name, x=x, y=y, size=size, buttonStyle='check',
                          borderWidth=0, fillColor=None, textColor=FIELDINK, forceBorder=False, annotationFlags='print')


HOWTO = ('On screen: open it in the free Adobe Acrobat Reader app (phone or computer), or in Chrome or Edge. Tap a box to type. '
         'Boxes with a small gold arrow open a list to pick from. Save a copy each time you start a new sheet. Some built-in phone PDF '
         'viewers do not show the lists, so use Acrobat Reader if they are missing.\n'
         'On paper: print the pages you need and write straight in the boxes. The lists work as write-in boxes.')

CATALOG = [
    ('THE VISIBILITY KIT', 'Six tools that make sure the work you already do actually gets seen.'),
    ('THE FRONTLINE CI STARTER KIT', 'Five simple tools for spotting problems and making the fix stick.'),
    ('THE RCFA TEMPLATE', 'The full root cause investigation, for faults that keep coming back.'),
    ('THE MTBA ASSIST TRACKER', 'Measure how often a job needs a hand, then prove you fixed it.'),
    ('THE KPI IMPACT CALCULATOR', 'Put a pound sign on any problem in two minutes.'),
    ('THE BREAKDOWN ANALYSIS DASHBOARD', 'MTBF, MTTR and a Pareto of which machine to fix first.'),
]


def catalog_except(name):
    return [c for c in CATALOG if c[0] != name]


def numbered(k, n, title, after=6):
    """Numbered step heading with gold circle."""
    k.need(22)
    cy = k.y - 9
    k.c.setFillColor(GOLD); k.c.circle(M + 8, cy, 8, fill=1, stroke=0)
    k.text(M + 8, cy - 3, str(n), 'Helvetica-Bold', 8.5, BLACK, align='center')
    k.text(M + 24, cy - 3, title, 'Helvetica-Bold', 8.4, INK, cs=0.4)
    k.y -= 20 + after
