import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from kitlib import *

OUT = sys.argv[1]
k = Kit(OUT, 'The Frontline CI Starter Kit', 'Fillable and printable continuous improvement tools for frontline teams')
c = k.c

cover(k, ['The Frontline', 'CI Starter Kit'], ['Spot problems. Fix them properly.', 'Make the fix stick.'],
      '5 SIMPLE TOOLS. REAL RESULTS.', 'FILLABLE ON SCREEN. PRINTABLE ON PAPER.', 'FOR SHIFT SUPERVISORS AND FRONTLINE TEAMS')

# ---------------- HOW TO USE
k.new_page('HOW TO USE THIS KIT', None, 'Five tools. No jargon. No 40-page manual.')
for p in ['Most people turn up, do the job, and go home. Nothing wrong with that.',
          'But the people who get noticed, who get asked to act up, who get the development and the opportunities, all tend to do one thing differently: they leave the place better than they found it, and they can prove it.',
          'That is all continuous improvement really is. Not a qualification. Not a buzzword. Just spotting problems, fixing them properly, and keeping a record so the fix sticks and the credit lands where it should.',
          'These five tools are the ones that actually get used on a shop floor. No jargon. No 40-page manual. Print them, keep them on the line, fill them in as you go.']:
    k.para(p, size=9.4, after=8)
k.gap(4)
k.label('THE FIVE TOOLS')
for i, (t, d) in enumerate([('Shift Handover Log', 'Stop problems dying at the end of your shift.'),
                            ('5 Whys Worksheet', 'Get to the real cause instead of the obvious one.'),
                            ('Quick Wins Tracker', 'Log small improvements so they add up to something visible.'),
                            ('One-Page RCFA', 'A proper root cause investigation, stripped to what matters.'),
                            ('Daily CI Habit Tracker', 'One improvement a day. That is the whole method.')], 1):
    cy = k.y - 9
    c.setFillColor(GOLD); c.circle(M + 7, cy, 7, fill=1, stroke=0)
    k.text(M + 7, cy - 2.6, str(i), 'Helvetica-Bold', 7.5, BLACK, align='center')
    k.text(M + 22, cy + 1.5, t, 'Helvetica-Bold', 8.6, INK)
    k.text(M + 22, cy - 8.5, d, 'Helvetica', 7.4, GREY)
    k.y -= 29
k.gap(6)
k.note('START HERE', 'Start with the Daily CI Habit Tracker. Use it for two weeks before touching anything else.')
k.note('HOW TO USE THIS PDF', HOWTO, after=0)

# ---------------- TOOL 1 HANDOVER
k.new_page('SHIFT HANDOVER LOG', 'TOOL 1 OF 5', 'Fill this in during the last 20 minutes of your shift. Hand it over in person.')
inline_fields(k, [('DATE', 'h_date', 80, 'text', None), ('SHIFT', 'h_shift', 100, 'dd', ['Days', 'Earlies', 'Lates', 'Nights', 'Weekend']),
                  ('LINE / AREA', 'h_area', 0, 'text', None)])
inline_fields(k, [('HANDED OVER TO', 'h_to', 190, 'text', None), ('HOW', 'h_how', 0, 'dd', ['In person', 'In person and written', 'Written only', 'By phone'])], after=14)
strip_box(k, 'RUNNING NOW / CURRENT STATUS', 'h_status', 70)
strip_box(k, 'PROBLEMS STILL OPEN (WHAT, WHERE, WHAT YOU TRIED)', 'h_open', 100)
strip_box(k, 'WATCH THIS (SOMETHING NOT BROKEN YET, BUT HEADING THAT WAY)', 'h_watch', 80)
# two columns
hh = 90
k.need(hh + 22)
top = k.y
cw2 = (CW - 10) / 2
for i, (lab, n) in enumerate([('PARTS / MATERIALS NEEDED', 'h_parts'), ('ANYTHING THE NEXT SHIFT MUST NOT DO', 'h_mustnot')]):
    x = M + i * (cw2 + 10)
    c.setFillColor(CREAM); c.rect(x, top - 15, cw2, 15, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(x, top - 15, 3, 15, fill=1, stroke=0)
    k.text(x + 9, top - 10, lab, 'Helvetica-Bold', 6.6, INK, cs=0.4)
    k.tf(n, x, top - 15 - hh, cw2, hh, multiline=True, tip=lab.capitalize())
k.y = top - 15 - hh - 10
k.note('WHY THIS MATTERS', 'Most repeat faults are not new. They are old faults that never got handed over properly.', after=0)

# ---------------- TOOL 2 5 WHYS
def five_whys(prefix, example=None):
    e = example or {}
    def box(lab, key, h):
        k.need(h + 22)
        top = k.y
        c.setFillColor(CREAM); c.rect(M, top - 15, CW, 15, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(M, top - 15, 3, 15, fill=1, stroke=0)
        k.text(M + 9, top - 10, lab, 'Helvetica-Bold', 6.6, INK, cs=0.4)
        k._f(e, key, f'{prefix}_{key}', M, top - 15 - h, CW, h, multiline=True, tip=lab.capitalize())
        k.y = top - 15 - h - 10
    box('THE PROBLEM (BE SPECIFIC: WHAT, WHERE, WHEN, HOW OFTEN)', 'problem', 52 if not e else 30)
    for i in range(1, 6):
        h = 42 if not e else 24
        k.need(h + 8)
        top = k.y
        cy = top - h / 2
        c.setFillColor(BLACK); c.circle(M + 13, cy, 11, fill=1, stroke=0)
        k.text(M + 13, cy + 1, str(i), 'Helvetica-Bold', 9, GOLD, align='center')
        k.text(M + 13, cy - 6.5, 'WHY?', 'Helvetica-Bold', 4.6, white, align='center')
        if i < 5:
            c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(M + 13, cy - 11, M + 13, top - h - 8 + 0)
        k._f(e, f'why{i}', f'{prefix}_why{i}', M + 32, top - h, CW - 32, h, multiline=True, tip=f'Why {i}')
        k.y = top - h - 8
    k.gap(2)
    box('ROOT CAUSE (THE LAST ANSWER YOU CAN DO SOMETHING ABOUT)', 'root', 46 if not e else 26)
    box('THE FIX', 'fix', 46 if not e else 26)
    if e:
        k.need(22); k.y -= 16
        x = M + k.small(M, k.y + 5, 'WHO OWNS IT', INK) + 6
        k.ex(x, k.y, 160, 16, e['owner']); x += 176
        x += k.small(x, k.y + 5, 'BY WHEN', INK) + 6
        k.ex(x, k.y, 90, 16, e['when']); x += 106
        x += k.small(x, k.y + 5, 'STATUS', INK) + 6
        k.ex(x, k.y, M + CW - x, 16, e['status'])
        k.y -= 12
    else:
        inline_fields(k, [('WHO OWNS IT', f'{prefix}_owner', 160, 'text', None), ('BY WHEN', f'{prefix}_when', 90, 'text', None),
                          ('STATUS', f'{prefix}_status', 0, 'dd', ['Not started', 'In progress', 'Done', 'Done and checked'])], after=12)

k.new_page('5 WHYS WORKSHEET', 'TOOL 2 OF 5', 'Keep asking why until the answer is something you can actually fix.')
five_whys('w')
k.note('THE RULE', 'If your root cause is a person, you have not gone deep enough. Go again.', after=0)

k.new_page('5 WHYS WORKSHEET: WORKED EXAMPLE', 'TOOL 2 OF 5', 'Notice how each answer becomes the next question. That is the whole trick.')
five_whys('wx', example={
    'problem': 'Line 3 labeller jams at reel changes. About 4 times a shift on nights, 6 minutes lost each time.',
    'why1': 'Why does it jam? The new reel splice catches on the guide roller.',
    'why2': 'Why does it catch? The splice tape is sticking out past the edge of the label web.',
    'why3': 'Why is it sticking out? Each operator applies the splice tape at a different angle.',
    'why4': 'Why is it done differently? Nobody was ever shown one right way. It is picked up by watching.',
    'why5': 'Why was nobody shown? There is no standard or one-point lesson for splicing.',
    'root': 'No standard method for splicing the label reel, so everyone does it their own way.',
    'fix': 'Mark a splice guide on the table. Write a one-point lesson with photos. Show every crew this week.',
    'owner': 'Sam (nights)', 'when': 'Friday 7th', 'status': 'Done and checked'})
k.note('WHY IT WORKS', 'The first answer, "the splice catches", would have led to replacing a roller. Three more whys found a fix that costs nothing and stops it on every shift.', after=0)

# ---------------- TOOL 3 QUICK WINS
k.new_page('QUICK WINS TRACKER', 'TOOL 3 OF 5', 'Small fixes, logged. Twenty of these in a year is a track record nobody can argue with.')
k.note('TAKE THIS TO YOUR NEXT ONE-TO-ONE', 'Do not wait to be asked what you have been doing. Hand this over.')
qcols = [('DATE', 56, 'text', None), ('WHAT I SPOTTED', 0, 'text', None), ('WHAT I DID', 150, 'text', None),
         ('RESULT', 110, 'dd', ['Saved time', 'Less waste', 'Safer', 'Better quality', 'Saved money', 'Easier job'])]
k.table('q', qcols, rows='fill', row_h=22,
        example_row=['Tue 4th', 'Spare reels kept in the store, 10 min walk', 'Moved them next to the labeller', 'Saved time'])
QNEXT = k.last_row + 1
k.new_page('QUICK WINS TRACKER', 'TOOL 3 OF 5  |  CONTINUED', 'Keep going. The list is the proof.')
k.table('q', qcols, rows='fill', row_h=22, start=QNEXT)

# ---------------- TOOL 4 ONE-PAGE RCFA
k.new_page('ONE-PAGE RCFA', 'TOOL 4 OF 5', 'For the faults that keep coming back. Do this properly once, and it stops.')
inline_fields(k, [('DATE RAISED', 'r_date', 76, 'text', None), ('EQUIPMENT / LINE', 'r_equip', 150, 'text', None), ('REF', 'r_ref', 0, 'text', None)])
inline_fields(k, [('RAISED BY', 'r_by', 160, 'text', None), ('IMPACT TYPE', 'r_type', 0, 'dd', ['Downtime', 'Waste', 'Cost', 'Safety', 'Quality', 'More than one'])], after=12)
strip_box(k, '1. WHAT ACTUALLY HAPPENED (FACTS ONLY, NO OPINIONS)', 'r_what', 56)
strip_box(k, '2. IMPACT (DOWNTIME, WASTE, COST, SAFETY, QUALITY)', 'r_impact', 40)
strip_box(k, '3. POSSIBLE CAUSES (LIST EVERYTHING, THEN RULE THEM OUT)', 'r_causes', 62)
strip_box(k, '4. ROOT CAUSE (EVIDENCE, NOT A GUESS)', 'r_root', 44)
hh = 56
k.need(hh + 22)
top = k.y
cw2 = (CW - 10) / 2
for i, (lab, n) in enumerate([('5. CONTAINMENT (STOPS IT TODAY)', 'r_contain'), ('6. PERMANENT FIX (STOPS IT FOREVER)', 'r_fix')]):
    x = M + i * (cw2 + 10)
    c.setFillColor(CREAM); c.rect(x, top - 15, cw2, 15, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(x, top - 15, 3, 15, fill=1, stroke=0)
    k.text(x + 9, top - 10, lab, 'Helvetica-Bold', 6.6, INK, cs=0.4)
    k.tf(n, x, top - 15 - hh, cw2, hh, multiline=True, tip=lab.capitalize())
k.y = top - 15 - hh - 9
strip_box(k, '7. HOW WILL YOU KNOW IT WORKED? (THE CHECK, AND THE DATE YOU WILL CHECK IT)', 'r_check', 36)
inline_fields(k, [('CHECK DATE', 'r_checkdate', 90, 'text', None), ('DID IT WORK?', 'r_worked', 0, 'dd', ['Yes, fixed', 'Partly, keep going', 'No, go again'])], after=8)
k.para('Fault too big for one page? The Kaizen XP RCFA Template takes you through the full eight-step investigation.', size=7.2, name='Helvetica-Oblique', color=GREY, after=0)

# ---------------- TOOL 5 DAILY HABIT
k.new_page('DAILY CI HABIT TRACKER', 'TOOL 5 OF 5', 'One improvement a day. Tick the box. That is the entire method.')
inline_fields(k, [('MONTH', 'd_month', 150, 'text', None), ('AREA', 'd_area', 0, 'text', None)], after=10)
rh = 16.2
top = k.y
k.need(18 + rh * 31)
c.setFillColor(BLACK); c.rect(M, top - 18, CW, 18, fill=1, stroke=0)
k.text(M + 6, top - 11.5, 'DAY', 'Helvetica-Bold', 6.2, GOLD, cs=0.5)
k.text(M + 40, top - 11.5, 'THE ONE THING I IMPROVED TODAY', 'Helvetica-Bold', 6.2, GOLD, cs=0.5)
k.text(M + CW - 22, top - 11.5, 'DONE', 'Helvetica-Bold', 6.2, GOLD, align='center', cs=0.5)
y = top - 18
for d in range(1, 32):
    y -= rh
    k.box(M, y, 34, rh, fill=CREAM)
    k.text(M + 17, y + 5, str(d), 'Helvetica-Bold', 7.2, INK, align='center')
    k.tf(f'd_day{d}', M + 34, y, CW - 34 - 44, rh, tip=f'Day {d}', size=7.8)
    k.box(M + CW - 44, y, 44, rh)
    checkbox(k, f'd_done{d}', M + CW - 22 - 5.5, y + (rh - 11) / 2, 11, tip=f'Day {d} done')
k.y = y - 10
k.note('IT DOES NOT HAVE TO BE BIG', 'A label moved. A tool put back where it lives. One step written down. Small and every day beats big and once a year.', after=0)

back(k, 'FIVE TOOLS IN', 'Now make sure it gets seen.', 'The rest of the Kaizen XP range',
     None, None, catalog_except('THE FRONTLINE CI STARTER KIT'),
     'Every fix you log here belongs in the Visibility Kit.')
c.save()
print('pages', k.page, 'fields', len(k.names))
