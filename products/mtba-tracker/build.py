import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from kitlib import *

OUT = sys.argv[1]
k = Kit(OUT, 'The MTBA Assist Tracker', 'Fillable and printable Mean Time Between Assists tracker')
c = k.c
TYPES = ['Jam or blockage', 'Misfeed or misalignment', 'Reset or restart', 'Manual adjustment', 'Re-handle or re-work', 'Material or supply issue', 'Other']

cover(k, ['The MTBA', 'Assist Tracker'], ['Measure how often a job needs a hand.', 'Then prove you fixed it.'],
      'LOG IT. MEASURE IT. KILL IT.', 'FILLABLE ON SCREEN. PRINTABLE ON PAPER.', 'FOR OPERATORS, TECHNICIANS AND SHIFT LEADERS')

# ---------------- READ THIS FIRST
k.new_page('READ THIS FIRST', None, 'The small stops nobody logs are usually costing more than the big breakdown everyone talks about.')
for p in ['MTBA stands for Mean Time Between Assists. An assist is any time someone has to step in to keep a job running: clearing a jam, nudging a misfeed, resetting a fault, re-handling stock, re-doing work. Each one only takes a minute or two, which is exactly why nobody writes them down.',
          'MTBA is how long, on average, the job runs before it needs one of those hands. The higher the number, the healthier the process. When you remove the cause of an assist, MTBA goes up, and you can prove it.']:
    k.para(p, size=9.2, after=8)
k.need(70)
top = k.y
k.box(M, top - 62, CW, 62, fill=BLACK, stroke=BLACK)
k.text(W / 2, top - 22, 'MTBA  =  RUN TIME  ÷  NUMBER OF ASSISTS', 'Helvetica-Bold', 13, GOLD, align='center', cs=1)
k.text(W / 2, top - 42, 'An 8-hour shift is 480 minutes. 12 assists in that shift means MTBA = 480 ÷ 12 = 40 minutes.', 'Helvetica', 8.6, white, align='center')
k.text(W / 2, top - 54, 'Fix the main cause and get it down to 4 assists, and MTBA becomes 120 minutes: three times longer between hands.', 'Helvetica', 8.6, HexColor('#c8c8c8'), align='center')
k.y = top - 62 - 14
k.label('THE FOUR STEPS')
for i, (t, d) in enumerate([('Log every assist for one week', 'Use the Shift Assist Log. Every single one, however small. Page 3.'),
                            ('Find your biggest one', 'Add up the week on the Weekly Summary. The type with the most minutes lost goes first. Page 6.'),
                            ('Fix the cause, not the symptom', 'Use 5 Whys or the Kaizen XP RCFA Template on that one assist type.'),
                            ('Log again and prove it', 'One more week of logging, then fill in the Before & After page. Page 7.')], 1):
    cy = k.y - 9
    c.setFillColor(GOLD); c.circle(M + 7, cy, 7, fill=1, stroke=0)
    k.text(M + 7, cy - 2.6, str(i), 'Helvetica-Bold', 7.5, BLACK, align='center')
    k.text(M + 22, cy + 1.5, t, 'Helvetica-Bold', 8.6, INK)
    k.text(M + 22, cy - 8.5, d, 'Helvetica', 7.4, GREY)
    k.y -= 29
k.gap(4)
k.note('MTBA OR MTBF?', 'MTBF (Mean Time Between Failures) is for breakdowns that need an engineer. MTBA is for the small stuff the operator fixes in a minute. Track both if you can, but MTBA is where the quick wins hide.')
k.note('HOW TO USE THIS PDF', HOWTO, after=0)

# ---------------- SHIFT LOG
def shift_log(idx, cont=False):
    k.new_page('SHIFT ASSIST LOG', f'LOG SHEET {idx}', 'Every assist, as it happens. If you had to step in, it goes on the list.')
    inline_fields(k, [('DATE', f'l{idx}_date', 80, 'text', None), ('SHIFT', f'l{idx}_shift', 96, 'dd', ['Days', 'Earlies', 'Lates', 'Nights', 'Weekend']),
                      ('LINE / MACHINE / AREA', f'l{idx}_area', 0, 'text', None)])
    inline_fields(k, [('LOGGED BY', f'l{idx}_by', 160, 'text', None), ('RUN TIME THIS SHIFT (MINS)', f'l{idx}_run', 0, 'text', None)], after=10)
    cols = [('TIME', 50, 'text', None), ('WHAT HAPPENED', 0, 'text', None), ('ASSIST TYPE', 136, 'dd', TYPES),
            ('MINS LOST', 50, 'text', None), ('FIXED BY', 76, 'text', None)]
    # leave room for summary block (approx 70)
    saved = k.y
    k.y -= 0
    import kitlib
    old = kitlib.BOTTOM
    kitlib.BOTTOM = old + 78
    k.table(f'l{idx}', cols, rows='fill', row_h=20,
            example_row=['02:14', 'Label web snapped at splice', 'Jam or blockage', '6', 'Sam'] if idx == 1 else None)
    kitlib.BOTTOM = old
    # summary
    k.need(64)
    top = k.y
    k.box(M, top - 58, CW, 58, fill=CREAM, stroke=CREAM)
    c.setFillColor(GOLD); c.rect(M, top - 58, 3, 58, fill=1, stroke=0)
    k.text(M + 10, top - 13, 'END OF SHIFT', 'Helvetica-Bold', 7, INK, cs=0.5)
    gw = (CW - 20 - 3 * 10) / 4
    for i, (a, b, n) in enumerate([('TOTAL ASSISTS', 'count the rows', f'l{idx}_total'), ('MINUTES LOST', 'add up the column', f'l{idx}_mins'),
                                   ('MTBA (MINS)', 'run time ÷ assists', f'l{idx}_mtba'), ('BIGGEST TYPE', 'most common today', f'l{idx}_top')]):
        x = M + 12 + i * (gw + 10)
        k.text(x, top - 26, a, 'Helvetica-Bold', 6.3, INK, cs=0.4)
        k.text(x, top - 34, b, 'Helvetica', 6, GREY)
        if n.endswith('_top'):
            k.dd(n, x, top - 54, gw, 16, TYPES, tip='Biggest assist type today')
        else:
            k.tf(n, x, top - 54, gw, 16, tip=a.title())
    k.y = top - 58 - 6

shift_log(1)
shift_log(2)

# ---------------- WORKED EXAMPLE
k.new_page('WORKED EXAMPLE: ONE WEEK ON LINE 3', None, 'What the numbers look like once you have logged a week and added it up.')
k.para('Line 3 runs 15 shifts a week at 450 minutes of run time each, so 6,750 minutes a week. The team logged every assist for a full week, then added it up.', size=8.8, after=10)
rows = [('Jam or blockage', '58', '348', '1'), ('Misfeed or misalignment', '21', '84', '2'), ('Reset or restart', '14', '28', '3'),
        ('Re-handle or re-work', '6', '30', '4'), ('Manual adjustment', '9', '18', '5')]
k.table('ex_week', [('ASSIST TYPE', 0, 'static', [r[0] for r in rows]), ('HOW MANY', 90, 'static', [r[1] for r in rows]),
                    ('MINUTES LOST', 90, 'static', [r[2] for r in rows]), ('RANK', 70, 'static', [r[3] for r in rows])], rows=5, row_h=20)
k.note('WHAT IT TELLS YOU', 'Total: 108 assists, 508 minutes lost. MTBA = 6,750 ÷ 108 = 62 minutes. Jams are more than half of all assists and two thirds of the lost time, so jams get fixed first. Everything else waits.')
k.label('AFTER THE FIX', right='Same line, two weeks later, after the splicing standard went in.')
k.table('ex_after', [('', 0, 'static', ['Assists a week', 'MTBA', 'Minutes lost a week']), ('BEFORE', 120, 'static', ['108', '62 mins', '508']),
                     ('AFTER', 120, 'static', ['57', '118 mins', '232'])], rows=3, row_h=20)
k.note('THE SENTENCE', '"We nearly doubled MTBA on Line 3, from 62 to 118 minutes, and got back about 4.6 hours of run time a week." That line goes in your Weekly Wins email, your improvement log and your review.', after=0)

# ---------------- WEEKLY SUMMARY
k.new_page('WEEKLY SUMMARY', 'FIND YOUR BIGGEST ONE', 'Add up a week of log sheets. The type with the most minutes lost is the one to kill first.')
inline_fields(k, [('WEEK OF', 'w_week', 110, 'text', None), ('LINE / MACHINE / AREA', 'w_area', 0, 'text', None)], after=12)
k.table('w', [('ASSIST TYPE', 0, 'static', TYPES), ('HOW MANY', 90, 'text', None), ('MINUTES LOST', 90, 'text', None),
              ('RANK', 70, 'dd', ['1', '2', '3', '4', '5', '6', '7'])], rows=len(TYPES), row_h=30)
k.label('THE WEEK IN NUMBERS')
gw = (CW - 3 * 8) / 4
gh = 46
k.need(gh)
top = k.y
for i, (a, b, n) in enumerate([('RUN TIME', 'minutes this week', 'w_run'), ('TOTAL ASSISTS', 'all types', 'w_total'),
                               ('MTBA', 'run time ÷ assists', 'w_mtba'), ('MINUTES LOST', 'all types', 'w_lost')]):
    x = M + i * (gw + 8)
    k.box(x, top - gh, gw, gh, fill=CREAM, stroke=CREAM)
    c.setFillColor(GOLD); c.rect(x, top - 3, gw, 3, fill=1, stroke=0)
    k.text(x + 8, top - 14, a, 'Helvetica-Bold', 6.3, INK, cs=0.4)
    k.text(x + 8, top - 22, b, 'Helvetica', 6, GREY)
    k.tf(n, x + 8, top - gh + 5, gw - 16, 16, tip=f'{a.title()} ({b})', size=10)
k.y = top - gh - 12
inline_fields(k, [('COST OF AN HOUR (£)', 'w_rate', 80, 'text', None), ('COST THIS WEEK (£)', 'w_cost', 90, 'text', None), ('PER YEAR (x 52)', 'w_year', 0, 'text', None)], after=6)
k.para('Cost this week = minutes lost ÷ 60 x cost of an hour. Not sure what an hour costs? Use your own hourly rate as the lowest honest number, or try the Kaizen XP KPI Impact Calculator.', size=7.2, name='Helvetica-Oblique', color=GREY, after=8)
inline_fields(k, [('THE ONE WE FIX FIRST', 'w_first', 200, 'dd', TYPES), ('OWNER', 'w_owner', 0, 'text', None)], after=10)
strip_box(k, 'WHAT WE THINK IS CAUSING IT (THEN PROVE IT WITH 5 WHYS OR AN RCFA)', 'w_cause', 80)

# ---------------- BEFORE AND AFTER
k.new_page('BEFORE & AFTER', 'PROVE IT', 'One week before the fix, one week after. This is the page you show people.')
inline_fields(k, [('LINE / MACHINE / AREA', 'ba_area', 220, 'text', None), ('ASSIST TYPE FIXED', 'ba_type', 0, 'dd', TYPES)], after=12)
measures = [('Week of', 'week'), ('Run time (minutes)', 'run'), ('Number of assists', 'assists'), ('MTBA (minutes)', 'mtba'),
            ('Minutes lost to assists', 'lost'), ('Cost of lost time (£)', 'cost')]
hh = 20
rh = 34
k.need(hh + rh * len(measures))
top = k.y
colw = [CW - 2 * 150, 150, 150]
c.setFillColor(BLACK); c.rect(M, top - hh, CW, hh, fill=1, stroke=0)
k.text(M + colw[0] + 8, top - 13, 'BEFORE THE FIX', 'Helvetica-Bold', 6.6, GOLD, cs=0.5)
k.text(M + colw[0] + colw[1] + 8, top - 13, 'AFTER THE FIX', 'Helvetica-Bold', 6.6, GOLD, cs=0.5)
y = top - hh
for lab, key in measures:
    y -= rh
    hl = key == 'mtba'
    k.box(M, y, colw[0], rh, fill=CREAM)
    if hl:
        c.setFillColor(GOLD); c.rect(M, y, 3, rh, fill=1, stroke=0)
    k.text(M + 10, y + rh / 2 - 3, lab, 'Helvetica-Bold', 7.8, INK)
    k.tf(f'ba_before_{key}', M + colw[0], y, colw[1], rh, tip=f'Before: {lab}', size=10 if hl else 9)
    k.tf(f'ba_after_{key}', M + colw[0] + colw[1], y, colw[2], rh, tip=f'After: {lab}', size=10 if hl else 9)
k.y = y - 14
k.label('THE DIFFERENCE')
gw = (CW - 2 * 8) / 3
gh = 50
k.need(gh)
top = k.y
for i, (a, b, n) in enumerate([('MTBA IS NOW', 'times longer (after ÷ before)', 'ba_times'), ('MINUTES BACK', 'per week (before minus after)', 'ba_mins'),
                               ('WORTH PER YEAR (£)', 'cost saved per week x 52', 'ba_year')]):
    x = M + i * (gw + 8)
    k.box(x, top - gh, gw, gh, fill=BLACK, stroke=BLACK)
    k.text(x + 10, top - 14, a, 'Helvetica-Bold', 6.6, GOLD, cs=0.5)
    k.text(x + 10, top - 23, b, 'Helvetica', 6, HexColor('#bbbbbb'))
    k.tf(n, x + 10, top - gh + 6, gw - 20, 17, tip=f'{a.title()} ({b})', size=11)
k.y = top - gh - 12
strip_box(k, 'WHAT WE CHANGED', 'ba_changed', 80)
inline_fields(k, [('WHO SAW IT?', 'ba_saw', 150, 'dd', ['Line leader', 'Manager', 'Line leader and manager', 'Wider team', 'Nobody yet']),
                  ('NAME(S)', 'ba_names', 0, 'text', None)], after=10)
strip_box(k, 'YOUR SENTENCE: "WE STRETCHED MTBA ON [LINE] FROM [X] TO [Y] MINUTES, AND GOT BACK [Z] A WEEK."', 'ba_sentence', 56)

back(k, 'MTBA STRETCHED', 'Now make sure it gets seen.', 'The rest of the Kaizen XP range', None, None,
     catalog_except('THE MTBA ASSIST TRACKER'), 'A before and after like this is the strongest line on any review.')
c.save()
print('pages', k.page, 'fields', len(k.names))
