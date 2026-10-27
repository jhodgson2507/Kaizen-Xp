"""Build The Visibility Kit v2: fillable + printable A4 PDF, Kaizen XP black and gold."""
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = sys.argv[1]
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
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle('The Visibility Kit')
        self.c.setAuthor('Kaizen XP')
        self.c.setSubject('Fillable and printable career visibility kit for shift workers')
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
        self.text(M, 32, 'KAIZEN XP  |  THE VISIBILITY KIT', 'Helvetica', 6.3, LGREY, cs=0.6)
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
            for (hd, _, kind, opts), w in zip(cols, widths):
                n = f'{prefix}_r{start + r}_{hd.split()[0].lower().strip("?")}'
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


k = Kit(OUT)
c = k.c

# =========================================================== COVER
k.page = 1
c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)
c.setStrokeColor(HexColor('#3a3a3a')); c.setLineWidth(0.5); c.rect(36, 36, W - 72, H - 72, fill=0, stroke=1)
c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(W / 2 - 46, H - 228, 92, 56, fill=0, stroke=1)
k.text(W / 2, H - 209, 'XP', 'Helvetica-Bold', 26, GOLD, align='center')
k.text(W / 2, H - 258, 'KAIZEN XP', 'Helvetica-Bold', 8.5, GOLD, align='center', cs=4.5)
c.setStrokeColor(HexColor('#555555')); c.setLineWidth(0.5); c.line(W / 2 - 70, H - 272, W / 2 + 70, H - 272)
k.text(W / 2, H - 330, 'The Visibility Kit', 'Helvetica-Bold', 32, white, align='center')
k.text(W / 2, H - 362, 'How to make sure the work you already do', 'Helvetica', 11.5, GOLD, align='center')
k.text(W / 2, H - 378, 'actually gets seen.', 'Helvetica', 11.5, GOLD, align='center')
bw = 208
c.setFillColor(GOLD); c.rect(W / 2 - bw / 2, H - 418, bw, 22, fill=1, stroke=0)
k.text(W / 2, H - 410, '6 TOOLS. 90 DAYS. NO FLUFF.', 'Helvetica-Bold', 7.5, BLACK, align='center', cs=2.2)
k.text(W / 2, H - 438, 'FILLABLE ON SCREEN. PRINTABLE ON PAPER.', 'Helvetica-Bold', 6.6, HexColor('#bdbdbd'), align='center', cs=1.8)
c.setStrokeColor(HexColor('#444444')); c.line(90, H - 470, W - 90, H - 470)
k.text(W / 2, H - 512, '"Do what nobody else can be bothered to do,', 'Helvetica-Oblique', 12, white, align='center')
k.text(W / 2, H - 530, 'and you\'ll get what nobody else gets."', 'Helvetica-Oblique', 12, white, align='center')
c.line(90, H - 570, W - 90, H - 570)
k.text(W / 2, 80, 'FOR SHIFT WORKERS WHO WANT TO GO FURTHER', 'Helvetica', 6.8, HexColor('#8a8a8a'), align='center', cs=3)

# =========================================================== READ THIS FIRST
k.new_page('READ THIS FIRST', None, 'Two minutes now saves you ninety days of wondering why nobody noticed.')
for p in [
    'Your workplace already has the tools. Root cause forms, five whys, audit sheets, whatever they call them where you are. You do not need me to sell you those.',
    'Here is the problem nobody tells you about.',
    'You can do brilliant work for years and still get overlooked, because the person who decides what happens to you never actually hears about it. The fix you made at 3am. The colleague you got up to speed. The fault you spotted before it became a breakdown. It happened, it mattered, and then it evaporated.',
    'Meanwhile someone louder, who did less, gets the opportunity.',
    'This kit is not about doing more work. You already do the work. It is about making sure the work leaves a trace, so that when a role comes up, your name is already in the room before you walk into it.',
    'Six tools. Use them for ninety days. Then take the last one into your review and watch how different that conversation goes.',
]:
    k.para(p, size=9.4, after=8)
k.gap(4)
k.label('WHAT IS INSIDE')
items = [
    ('The Weekly Wins Email', 'Three bullets, every Friday. The single highest-return habit in here.'),
    ('The CC Rule', 'When to copy your line leader in, and when it makes you look insecure.'),
    ('Coaching Log & Sign-Off', 'Signed proof you developed someone. Almost nobody keeps this.'),
    ('Colleague Support Tracker', 'The help you give that currently goes unrecorded.'),
    ('Improvement Contribution Log', 'What you changed, what it saved, and who saw it.'),
    ('The 90-Day Review Sheet', 'Everything above, on one page, in front of the person who decides.'),
]
for i, (t, d) in enumerate(items, 1):
    k.need(25)
    cy = k.y - 9
    c.setFillColor(GOLD); c.circle(M + 7, cy, 7, fill=1, stroke=0)
    k.text(M + 7, cy - 2.6, str(i), 'Helvetica-Bold', 7.5, BLACK, align='center')
    k.text(M + 22, cy + 1.5, t, 'Helvetica-Bold', 8.6, INK)
    k.text(M + 22, cy - 8.5, d, 'Helvetica', 7.4, GREY)
    k.y -= 29
k.need(25)
cy = k.y - 9
c.setStrokeColor(GOLD); c.setLineWidth(1); c.circle(M + 7, cy, 7, fill=0, stroke=1)
k.text(M + 7, cy - 2.6, '+', 'Helvetica-Bold', 9, GOLD, align='center')
k.text(M + 22, cy + 1.5, 'Plus: worked examples, a Put a Number On It page, and enough sheets for 90 days', 'Helvetica-Bold', 8.6, INK)
k.text(M + 22, cy - 8.5, 'So you know what good looks like, and never run out of space halfway through.', 'Helvetica', 7.4, GREY)
k.y -= 32
k.note('HOW TO USE THIS PDF',
       'On screen: open it in the free Adobe Acrobat Reader app (phone or computer), or in Chrome or Edge. Tap a box to type. Boxes with a small gold arrow open a list to pick from. Save as you go. Some built-in phone PDF viewers do not show the lists, so use Acrobat Reader if they are missing.\n'
       'On paper: print the pages you need and write straight in the boxes. The lists work as write-in boxes.')

# =========================================================== TOOL 1
k.new_page('THE WEEKLY WINS EMAIL', 'TOOL 1 OF 6', 'Friday, before you go home. Five minutes. Three bullets. Never more.')
k.note('THE RULE', 'Three bullets. No attachments. No essay. Subject line: This week on [your line/area].\n'
       'If you have had a quiet week, send it anyway and say so. Consistency is the point, not volume. A manager who hears from you 40 Fridays a year knows exactly who you are.')
k.label('THE TEMPLATE')
tpl = ['Subject: This week on [line / area]', '', 'Morning [name],', '', 'Quick one from this week:',
       '  - [What went wrong, what I did, what the result was]', '  - [Something I improved or prevented]',
       '  - [Someone I helped, or something worth flagging early]', '', 'Nothing needed from you, just keeping you in the loop.', '', '[Your name]']
th = 12 + len(tpl) * 9.6
k.need(th)
c.setFillColor(HexColor('#faf8f2')); c.setStrokeColor(LINE); c.setLineWidth(0.6)
c.rect(M, k.y - th, CW, th, fill=1, stroke=1)
yy = k.y - 14
for ln in tpl:
    k.text(M + 12, yy, ln, 'Courier', 7.8, BODY)
    yy -= 9.6
k.y -= th + 12
k.label('THIS WEEK\'S THREE')
k.need(20)
k.y -= 16
x = M + k.small(M, k.y + 5, 'WEEK OF', INK) + 6
k.tf('t1_week_of', x, k.y, 110, 16, tip='Week of')
x2 = x + 110 + 16
x2 += k.small(x2, k.y + 5, 'SENT?', INK) + 6
k.dd('t1_sent', x2, k.y, 110, 16, ['Sent', 'Sent late', 'Not yet'], tip='Sent this week?')
k.y -= 10
for i, q in enumerate(['WHAT BROKE, AND WHAT DID I DO ABOUT IT?',
                       'WHAT DID I IMPROVE, PREVENT, OR MAKE EASIER FOR THE NEXT SHIFT?',
                       'WHO DID I HELP, OR WHAT SHOULD THEY HEAR FROM ME BEFORE THEY HEAR IT ELSEWHERE?'], 1):
    k.need(86)
    top = k.y
    c.setFillColor(CREAM); c.rect(M, top - 15, CW, 15, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(M, top - 15, 3, 15, fill=1, stroke=0)
    k.text(M + 9, top - 10, q, 'Helvetica-Bold', 6.6, INK, cs=0.4)
    k.tf(f't1_win{i}', M, top - 15 - 64, CW, 64, multiline=True, tip=q.capitalize())
    k.y = top - 79 - 9
k.gap(2)
k.note('THE LAST LINE MATTERS', '"Nothing needed from you" is what stops this reading as a request or a complaint. You are informing, not asking. That is why people keep reading it week after week.', after=0)

# =========================================================== TOOL 1 example + tracker
k.new_page('THE WEEKLY WINS EMAIL: EXAMPLE & TRACKER', 'TOOL 1 OF 6', 'What a good one looks like, and a tracker so you never miss a Friday.')
k.need(16)
k.y -= 16
k.bar(M, k.y, CW, 16, 'A REAL-WORLD WEEKLY WINS EMAIL', example=True)
eg = ['Subject: This week on Line 3 nights', '', 'Morning Dave,', '', 'Quick one from this week:',
      '  - Labeller jammed at every reel change on Tuesday. Found the splice tape was going',
      '    on at different angles and showed the crew one way to do it. No jams since Wednesday.',
      '  - Moved the spare reels next to the machine instead of the store. Saves a 10-minute',
      '    walk every changeover.',
      '  - Talked Priya through her first solo changeover. She did Thursday\'s on her own.', '',
      'Nothing needed from you, just keeping you in the loop.', '', 'Sam']
eh = 10 + len(eg) * 9.4
k.need(eh)
c.setFillColor(white); c.setStrokeColor(LINE); c.rect(M, k.y - eh, CW, eh, fill=1, stroke=1)
yy = k.y - 13
for ln in eg:
    k.text(M + 12, yy, ln, 'Helvetica-Oblique', 7.8, EXINK)
    yy -= 9.4
k.y -= eh + 8
k.note('WHY IT WORKS',
       'Every bullet ends in a result, not just an activity. It names the colleague you helped, which also goes straight into your Coaching Log. And it asks for nothing, so it never feels like a chore to read.')
k.label('YOUR 13-WEEK STREAK', right='Tick off every Friday. Missed one? Send it Monday and keep going.')
k.table('t1_track', [('WEEK', 38, 'static', [str(i) for i in range(1, 14)]), ('DATE SENT', 72, 'text', None),
                     ('SENT?', 96, 'dd', ['Sent', 'Sent late', 'Missed']), ('BEST WIN THAT WEEK', 0, 'text', None)],
        rows=13, row_h=24)
k.need(26)
k.y -= 12
x = M + k.small(M, k.y + 5, 'TOTAL SENT', INK) + 6
k.tf('t1_total_sent', x, k.y, 40, 16, tip='Total weekly wins emails sent')
k.text(x + 46, k.y + 5, 'out of 13. Copy this onto your 90-Day Review Sheet.', 'Helvetica', 7.4, GREY)
k.y -= 10

# =========================================================== TOOL 2
k.new_page('THE CC RULE', 'TOOL 2 OF 6', 'Getting seen without becoming the person everyone finds exhausting.')
k.para('Copying your line leader into an email is one of the most powerful things you can do, and one of the easiest to get wrong. Done deliberately, it puts your name in front of them again and again, and it builds a paper trail you will be glad of at review time. Done constantly, it reads as insecure, and people start filtering you out.', size=8.6)
k.para('The difference is simple: CC when it is positive or constructive. Do not CC to cover yourself, and do not CC on routine traffic.', size=8.6, after=10)
ins = ['An improvement you made or proposed', 'Positive feedback you are giving a colleague',
       'A problem you spotted early and flagged before it escalated', 'Coaching or training you have delivered to someone',
       'A result, a saving, a fix that held']
outs = ['Routine day-to-day traffic', 'Anything sent purely to cover yourself', 'Complaints about a colleague',
        'Chasing something that is not yours to chase', 'Anything you would be embarrassed to have read out in a room']
colw = (CW - 10) / 2
ch = 18 + 5 * 22 + 6
k.need(ch)
top = k.y
for ci, (head, lst, hc) in enumerate([('CC THEM IN', ins, BLACK), ('LEAVE THEM OUT', outs, HexColor('#3a3a3a'))]):
    x = M + ci * (colw + 10)
    k.box(x, top - ch, colw, ch)
    c.setFillColor(hc); c.rect(x, top - 18, colw, 18, fill=1, stroke=0)
    k.text(x + 8, top - 12, head, 'Helvetica-Bold', 6.8, GOLD if ci == 0 else white, cs=0.6)
    yy = top - 18 - 14
    for item in lst:
        mark = '+' if ci == 0 else '-'
        k.text(x + 9, yy, mark, 'Helvetica-Bold', 8.5, GOLD if ci == 0 else LGREY)
        ls = k.wrap(item, 'Helvetica', 7.8, colw - 30)
        for j, ln in enumerate(ls):
            k.text(x + 20, yy - j * 9.4, ln, 'Helvetica', 7.8, BODY)
        yy -= 22
k.y = top - ch - 12
k.note('THE TEST', 'Before you hit CC, ask: am I sending this so my boss sees the work, or so my boss sees that it was not my fault? The first builds a reputation. The second destroys one.')
k.label('EMAILS I CC\'D THIS MONTH, AND WHY', right='Only the reasons on the left belong in this list.')
k.table('t2_cc', [('DATE', 62, 'text', None), ('WHAT IT WAS ABOUT', 0, 'text', None),
                  ('WHY I CC\'D', 150, 'dd', ['An improvement', 'Positive feedback', 'Problem flagged early',
                                               'Coaching I delivered', 'A result or saving', 'Other'])],
        rows='fill', row_h=22)

# =========================================================== TOOL 3
k.new_page('COACHING LOG & SIGN-OFF', 'TOOL 3 OF 6', 'Signed proof you developed someone. Take this to your review. Nobody else will have one.')
k.note('WHY THIS ONE IS WORTH MORE THAN THE REST',
       'Every development conversation asks the same question: give me an example of when you developed someone. Most people give a vague answer from memory. You will hand over a signed record with names and dates on it. That is not a small difference.')
k.coaching_record(0, example={'date': 'Tue 4th', 'who': 'Priya K', 'now': 'Can do it alone now',
                              'task': 'Running a size changeover on the filler, start to finish',
                              'before': 'Before: had watched it done but never led one. Now: led Thursday\'s changeover on her own, eight minutes quicker than our usual time.',
                              's1': 'Priya K', 's2': 'D. Hughes', 'status': 'Signed off'})
k.coaching_record(1)
k.coaching_record(2)
k.coaching_record(3)

k.new_page('COACHING LOG & SIGN-OFF', 'TOOL 3 OF 6  |  CONTINUED', 'Get it signed the same week. A signature chased three months later is a favour. Same week, it is proof.')
for n in (4, 5, 6, 7):
    k.coaching_record(n)

# =========================================================== TOOL 4
k.new_page('COLLEAGUE SUPPORT TRACKER', 'TOOL 4 OF 6', 'The help you give that currently goes unrecorded. It is more than you think.')
k.para('You do this every shift already. You cover for someone, you talk a new starter through something, you sort a problem that was not yours. None of it gets written down, so none of it exists when someone asks whether you are ready for more responsibility.', size=8.6)
k.para('Write it down. One line. It takes ten seconds.', size=8.6, name='Helvetica-Bold', color=INK, after=10)
cols4 = [('DATE', 56, 'text', None), ('WHO', 86, 'text', None), ('WHAT I DID FOR THEM', 0, 'text', None),
         ('SAVED TIME /\nSTOPPED A PROBLEM?', 118, 'dd', ['Saved time', 'Stopped a problem', 'Both', 'Neither, but it helped'])]
k.table('t4', cols4, rows='fill', row_h=21, head_h=22,
        example_row=['Mon 3rd', 'Tom (days)', 'Stayed 20 mins to finish his clean-down so the line started on time', 'Saved time'])

T4_NEXT = k.last_row + 1
k.new_page('COLLEAGUE SUPPORT TRACKER', 'TOOL 4 OF 6  |  CONTINUED', 'Two lines a week for ninety days is a list nobody else in your team will have.')
k.table('t4', cols4, rows='fill', row_h=21, head_h=22, start=T4_NEXT)

# =========================================================== TOOL 5
k.new_page('IMPROVEMENT CONTRIBUTION LOG', 'TOOL 5 OF 6', 'What you changed, what it was worth, and who knows about it.')
k.note('THE COLUMN PEOPLE FORGET',
       '"Who saw it" is the one that matters. An improvement nobody senior knows about is a favour you did the company. An improvement your line leader knows about is a career.')
k.improvement_record(0, example={
    'date': 'Wed 5th',
    'problem': 'Line 3 labeller jammed at every reel change. About 4 times a shift, 6 minutes lost each time.',
    'changed': 'Found the splice tape was going on at different angles. Marked a guide on the splice table and showed each crew one way to do it.',
    'result': 'Jams down from 4 a shift to 1. That is 18 minutes back every shift.',
    'type': 'Time', 'worth': 'About 234 hours a year (about £3,000)',
    'saw': 'Line leader and manager', 'names': 'D. Hughes, and in my weekly wins email'})
k.improvement_record(1)
k.improvement_record(2)

k.new_page('IMPROVEMENT CONTRIBUTION LOG', 'TOOL 5 OF 6  |  CONTINUED', 'Small counts. Twenty small fixes with a name and a number on each beats one big project nobody remembers.')
for n in (3, 4, 5, 6):
    k.improvement_record(n)

# =========================================================== BONUS calculator
k.new_page('PUT A NUMBER ON IT', 'BONUS  |  GOES WITH TOOL 5', 'Turn "I sorted it" into a number your manager can repeat in meetings you are not in.')
k.para('Managers remember numbers. "I fixed the labeller" gets a nod. "I saved 234 hours a year on Line 3" gets repeated. You do not need finance data. You need four things you can count yourself.', size=8.6, after=10)
calc = [
    ('A', 'Times it happened per shift, before the fix', '4', 'calc_a'),
    ('B', 'Times it happens per shift now', '1', 'calc_b'),
    ('C', 'Minutes lost each time', '6', 'calc_c'),
    ('D', 'Shifts per week it happens on', '15', 'calc_d'),
    ('=', 'Minutes saved per week:  (A minus B) x C x D', '270', 'calc_mins_week'),
    ('=', 'Hours saved per year:  minutes per week, divided by 60, x 52', '234', 'calc_hours_year'),
    ('E', 'What an hour costs (£). See the note below.', '£13', 'calc_e'),
    ('=', 'Worth per year:  hours per year x E', '£3,042', 'calc_worth'),
]
rh = 24
hh = 18
widths = [30, CW - 30 - 110 - 120, 110, 120]
tot = hh + rh * len(calc)
k.need(tot)
top = k.y
c.setFillColor(BLACK); c.rect(M, top - hh, CW, hh, fill=1, stroke=0)
xx = M
for hd, w in zip(['', 'WHAT TO COUNT', 'EXAMPLE: LINE 3 LABELLER', 'YOURS'], widths):
    k.text(xx + 6, top - 11.5, hd, 'Helvetica-Bold', 6.2, GOLD, cs=0.5)
    xx += w
y = top - hh
for step, what, egv, fname in calc:
    y -= rh
    result = step == '='
    rowfill = CREAM if result else white
    xx = M
    for j, w in enumerate(widths):
        k.box(xx, y, w, rh, fill=rowfill)
        xx += w
    if result:
        c.setFillColor(GOLD); c.rect(M, y, 3, rh, fill=1, stroke=0)
    k.text(M + 15, y + rh / 2 - 3.5, step, 'Helvetica-Bold', 11 if result else 9, INK, align='center')
    k.text(M + widths[0] + 7, y + rh / 2 - 2.8, what, 'Helvetica-Bold' if result else 'Helvetica', 7.8, INK)
    k.text(M + widths[0] + widths[1] + 8, y + rh / 2 - 2.8, egv, 'Helvetica-Oblique', 8.2, EXINK)
    fx = M + widths[0] + widths[1] + widths[2]
    k.tf(fname, fx + 4, y + 4, widths[3] - 8, rh - 8, tip=what, fill=white)
k.y = y - 12
k.note('WHAT AN HOUR COSTS (E)',
       'If you do not know, use your own hourly rate. It is the lowest honest number, so nobody can argue with it. If your site tracks what an hour of downtime or lost output costs, use that instead and say so. It will be much bigger.')
k.label('YOUR SENTENCE', right='Use it in your Weekly Wins email, Tool 5 and your 90-Day Review.')
k.para('I reduced [the problem] from [A] to [B] a shift. That is about [hours] hours a year, worth roughly £[worth].', size=8.2, name='Helvetica-Oblique', color=GREY, after=6)
k.need(60)
k.tf('calc_sentence', M, k.y - 54, CW, 54, multiline=True, tip='Your sentence')
k.y -= 66
k.label('QUICK CHECK: MINUTES SAVED A SHIFT, IN HOURS A YEAR', right='Use it to sanity-check your maths.')
qc_cols = ['', '5 MINS', '10 MINS', '15 MINS', '30 MINS', '60 MINS']
qc_rows = [('5 shifts a week', ['22', '43', '65', '130', '260']), ('15 shifts a week', ['65', '130', '195', '390', '780'])]
qw = [CW - 5 * 66] + [66] * 5
qh = 20
k.need(qh * 3)
top = k.y
c.setFillColor(BLACK); c.rect(M, top - qh, CW, qh, fill=1, stroke=0)
xx = M
for hd, w in zip(qc_cols, qw):
    if hd:
        k.text(xx + w / 2, top - 12.5, hd, 'Helvetica-Bold', 6.2, GOLD, align='center', cs=0.5)
    xx += w
yq = top - qh
for lab, vals in qc_rows:
    yq -= qh
    xx = M
    k.box(xx, yq, qw[0], qh, fill=CREAM)
    k.text(xx + 8, yq + 7, lab, 'Helvetica-Bold', 7.4, INK)
    xx += qw[0]
    for v, w in zip(vals, qw[1:]):
        k.box(xx, yq, w, qh)
        k.text(xx + w / 2, yq + 7, v + ' hrs', 'Helvetica', 7.8, INK, align='center')
        xx += w
k.y = yq - 12
k.note('NO £ SIGN? STILL COUNTS',
       'Not every win has a cost. Safety and quality results count, so write what was prevented. "Nobody has slipped there since I moved the hose reel" is a result. So is "zero labels rejected at QA for three weeks."', after=0)

# =========================================================== TOOL 6
k.new_page('THE 90-DAY REVIEW SHEET', 'TOOL 6 OF 6', 'Everything above, on one page, in front of the person who decides.')
k.para('Fill this in from your other sheets. Do not do it from memory, that is the whole point of keeping them. Take it into the meeting printed. Hand a copy across the table.', size=8.6, after=8)
k.need(24)
k.y -= 18
x = M + k.small(M, k.y + 5, 'PERIOD', INK) + 6
k.tf('t6_period', x, k.y, 190, 16, tip='Review period')
x2 = x + 190 + 18
x2 += k.small(x2, k.y + 5, 'REVIEWED WITH', INK) + 6
k.tf('t6_reviewed_with', x2, k.y, M + CW - x2, 16, tip='Reviewed with')
k.y -= 14
# at a glance
glance = [('WEEKLY WINS SENT', 'out of 13, Tool 1', 't6_g_wins'), ('IMPROVEMENTS', 'logged, Tool 5', 't6_g_impr'),
          ('PEOPLE COACHED', 'signed off, Tool 3', 't6_g_coach'), ('TIMES I SUPPORTED', 'the team, Tool 4', 't6_g_support')]
gw = (CW - 3 * 8) / 4
gh = 46
k.need(gh)
top = k.y
for i, (a, b, n) in enumerate(glance):
    x = M + i * (gw + 8)
    k.box(x, top - gh, gw, gh, fill=CREAM, stroke=CREAM)
    c.setFillColor(GOLD); c.rect(x, top - 3, gw, 3, fill=1, stroke=0)
    k.text(x + 8, top - 14, a, 'Helvetica-Bold', 6.3, INK, cs=0.4)
    k.text(x + 8, top - 22, b, 'Helvetica', 6, GREY)
    k.tf(n, x + 8, top - gh + 5, gw - 16, 16, tip=f'{a.title()} ({b})', size=10)
k.y = top - gh - 10
for lab, src, n, hgt in [('IMPROVEMENTS DELIVERED', 'from Tool 5', 't6_improvements', 98),
                         ('PEOPLE I COACHED OR DEVELOPED', 'from Tool 3', 't6_coached', 78),
                         ('WHERE I SUPPORTED THE TEAM BEYOND MY OWN ROLE', 'from Tool 4', 't6_support', 78)]:
    k.need(hgt + 22)
    top = k.y
    c.setFillColor(CREAM); c.rect(M, top - 15, CW, 15, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(M, top - 15, 3, 15, fill=1, stroke=0)
    k.text(M + 9, top - 10, lab, 'Helvetica-Bold', 6.6, INK, cs=0.4)
    k.text(W - M - 8, top - 10, src, 'Helvetica-Oblique', 6.3, GREY, align='right')
    k.tf(n, M, top - 15 - hgt, CW, hgt, multiline=True, tip=lab.capitalize())
    k.y = top - 15 - hgt - 8
k.need(126)
top = k.y
c.setFillColor(CREAM); c.rect(M, top - 15, CW, 15, fill=1, stroke=0)
c.setFillColor(GOLD); c.rect(M, top - 15, 3, 15, fill=1, stroke=0)
k.text(M + 9, top - 10, 'WHAT I WANT NEXT, AND WHAT I NEED FROM YOU TO GET THERE', 'Helvetica-Bold', 6.6, INK, cs=0.4)
y = top - 15 - 22
x = M + 8 + k.small(M + 8, y + 5, 'THE NEXT STEP I AM AIMING FOR', INK) + 6
k.dd('t6_next_step', x, y, 210, 16, ['Act up or cover a senior role', 'Team leader or supervisor', 'Shift manager',
                                     'Specialist or technical role', 'More responsibility in my role',
                                     'A training course or qualification', 'Something else'], tip='The next step I am aiming for')
k.tf('t6_next_detail', x + 218, y, M + CW - x - 218 - 0, 16, tip='Next step details')
k.y = y - 6
k.tf('t6_need', M, k.y - 62, CW, 62, multiline=True, tip='What I need from you to get there')
k.y -= 72
k.note('SAY THIS OUT LOUD', '"This is what I have done. This is where I want to go. What is the gap?"\nMost people never ask. The ones who do are the ones who get told the answer.', after=0)

# =========================================================== BACK PAGE
c.showPage()
k.page += 1
c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.rect(30, 30, W - 60, H - 60, fill=0, stroke=1)
c.setStrokeColor(HexColor('#3a3a3a')); c.setLineWidth(0.5); c.rect(36, 36, W - 72, H - 72, fill=0, stroke=1)
k.text(W / 2, H - 150, 'NINETY DAYS FROM NOW', 'Helvetica-Bold', 8.5, GOLD, align='center', cs=4)
k.text(W / 2, H - 200, 'You will have the record.', 'Helvetica-Bold', 24, white, align='center')
k.text(W / 2, H - 230, 'Want more worth putting in it?', 'Helvetica', 14, GOLD, align='center')
c.setStrokeColor(HexColor('#444444')); c.line(110, H - 262, W - 110, H - 262)
k.text(W / 2, H - 300, 'THE FRONTLINE CI STARTER KIT', 'Helvetica-Bold', 11, white, align='center', cs=2)
k.text(W / 2, H - 318, 'Five simple tools for spotting problems, fixing them properly, and making the fix stick.', 'Helvetica', 8.8, HexColor('#c8c8c8'), align='center')
tools = ['Shift Handover Log', '5 Whys Worksheet', 'Quick Wins Tracker', 'One-Page RCFA', 'Daily CI Habit Tracker']
yy = H - 352
for t in tools:
    c.setFillColor(GOLD); c.circle(W / 2 - 78, yy + 3, 2.2, fill=1, stroke=0)
    k.text(W / 2 - 68, yy, t, 'Helvetica', 9.5, white)
    yy -= 18
k.text(W / 2, yy - 14, 'Every fix you make with it goes straight into Tool 5 of this kit.', 'Helvetica-Oblique', 8.8, GOLD, align='center')
k.text(W / 2, yy - 30, 'Available from Kaizen XP.', 'Helvetica', 8.8, HexColor('#c8c8c8'), align='center')
c.setStrokeColor(HexColor('#444444')); c.line(110, 250, W - 110, 250)
c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(W / 2 - 34, 172, 68, 42, fill=0, stroke=1)
k.text(W / 2, 186, 'XP', 'Helvetica-Bold', 19, GOLD, align='center')
k.text(W / 2, 150, '"Do what nobody else can be bothered to do, and you\'ll get what nobody else gets."', 'Helvetica-Oblique', 9, white, align='center')
k.text(W / 2, 62, '© 2026 Kaizen XP. Licensed for one person\'s use. Please do not share or resell.', 'Helvetica', 6.5, HexColor('#7a7a7a'), align='center')

c.save()
print('pages', k.page, 'fields', len(k.names))
