import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from kitlib import *

OUT = sys.argv[1]
k = Kit(OUT, 'The RCFA Template', 'Fillable and printable root cause failure analysis template')
c = k.c
SIXM = ['People', 'Machine', 'Method', 'Material', 'Measurement', 'Environment']

cover(k, ['The RCFA', 'Template'], ['Root cause analysis for the faults', 'that keep coming back.'],
      '8 STEPS. ONE ROOT CAUSE. NO REPEATS.', 'FILLABLE ON SCREEN. PRINTABLE ON PAPER.', 'FOR TECHNICIANS, ENGINEERS AND SHIFT LEADERS')

# ---------------- READ THIS FIRST
k.new_page('READ THIS FIRST', None, 'Fix the symptom and you will be back here next week. Fix the cause and you never see it again.')
for p in ['RCFA stands for Root Cause Failure Analysis. It sounds like an engineering department thing. It is not. It is a structured way of asking "why did that really happen?" and refusing to stop at the first easy answer.',
          'Most faults get fixed the same way every time: someone resets it, clears it, swaps the part, and the line runs again. Job done, until it happens on the next shift. The fault was never fixed. It was just survived.',
          'This template walks you through eight steps, in order. Do them properly once and the fault stops coming back. Do that a few times and people start bringing their problems to you.']:
    k.para(p, size=9.2, after=8)
k.gap(2)
k.label('THE EIGHT STEPS')
steps = [('Define the problem', 'Exactly what, where, when and how often. Facts, not opinions.'),
         ('Measure the impact', 'Downtime, waste, cost, safety, quality. This is why anyone should care.'),
         ('Contain it', 'Stop it hurting today, while you find the real cause.'),
         ('Build the timeline', 'What happened, in order, and how you know.'),
         ('List every possible cause', 'Use the six categories, then rule them out one by one with evidence.'),
         ('Find the root cause', '5 Whys on what is left. Then prove it.'),
         ('Fix it for good', 'Actions with an owner and a date, aimed at the root cause.'),
         ('Check, lock it in, spread it', 'Prove it worked, make it the standard, and use it everywhere it applies.')]
for i, (t, d) in enumerate(steps, 1):
    cy = k.y - 9
    c.setFillColor(GOLD); c.circle(M + 7, cy, 7, fill=1, stroke=0)
    k.text(M + 7, cy - 2.6, str(i), 'Helvetica-Bold', 7.5, BLACK, align='center')
    k.text(M + 22, cy + 1.5, t, 'Helvetica-Bold', 8.6, INK)
    k.text(M + 22, cy - 8.5, d, 'Helvetica', 7.4, GREY)
    k.y -= 27
k.gap(4)
k.note('THREE RULES', 'One problem per form. If you find two, start a second form.\n'
       'If your root cause is a person ("operator error"), you have not gone deep enough. Ask why the system let it happen.\n'
       'Containment is not a fix. A cone round a leak stops someone slipping. It does not stop the leak.')
k.note('HOW TO USE THIS PDF', HOWTO, after=0)

# ---------------- WORKED EXAMPLE
k.new_page('WORKED EXAMPLE: LINE 3 LABELLER', None, 'One page summary of a real-world style RCFA, so you can see what good looks like at every step.')
ex = [('1. DEFINE', 'Line 3 labeller jams at reel changes on all shifts, worst on nights. About 4 jams a shift since the new label stock started three weeks ago.'),
      ('2. IMPACT', '4 jams x 6 mins x 15 shifts = 6 hours downtime a week. About 40 mislabelled packs scrapped a week. No safety risk found.'),
      ('3. CONTAIN', 'Operator checks every splice before restarting. Spare reels moved next to the machine to speed up recovery.'),
      ('4. TIMELINE', 'Jams always within 2 minutes of a reel change. Started the week new label stock arrived. Fewer on days, when one experienced operator does most changes.'),
      ('5. CAUSES', 'Ruled out: worn guide roller (measured, in spec), label stock width (measured, in spec), sensor (tested, fine). Confirmed: splice tape overhanging the web edge.'),
      ('6. ROOT CAUSE', 'No standard method for splicing, so tape goes on at different angles. New stock is thinner, so overhang now catches. Verified: 20 splices done one way, zero jams.'),
      ('7. FIX', 'Splice guide marked on the table. One-point lesson with photos. Every crew shown in person. Splicing added to the new starter checklist.'),
      ('8. CHECK & SPREAD', 'Two weeks later: 1 jam a shift, down from 4. Splice guide added to Lines 1 and 2, which use the same labeller.')]
for lab, txt in ex:
    lines = k.wrap(txt, 'Helvetica-Oblique', 7.8, CW - 110 - 10)
    h = max(26, 10 + len(lines) * 10.2)
    k.need(h + 6)
    top = k.y
    k.box(M, top - h, 106, h, fill=CREAM)
    c.setFillColor(GOLD); c.rect(M, top - h, 3, h, fill=1, stroke=0)
    k.text(M + 10, top - 14, lab, 'Helvetica-Bold', 6.8, INK, cs=0.4)
    k.ex(M + 106, top - h, CW - 106, h, txt)
    k.y = top - h - 6
k.gap(4)
k.note('WHAT TO NOTICE', 'The first theory, a worn roller, would have cost a part and fixed nothing. Every cause was ruled in or out with a measurement, and the root cause was proven before anyone spent a penny.', after=0)

# ---------------- STEP 1 + 2
k.new_page('STEP 1: DEFINE THE PROBLEM', 'RCFA  |  PAGE 1 OF 5', 'If you cannot describe it exactly, you cannot fix it exactly.')
inline_fields(k, [('REF', 'r_ref', 70, 'text', None), ('DATE RAISED', 'r_date', 80, 'text', None), ('LINE / EQUIPMENT', 'r_equip', 0, 'text', None)])
inline_fields(k, [('LEAD', 'r_lead', 150, 'text', None), ('TEAM', 'r_team', 0, 'text', None)], after=12)
k.label('THE FACTS', right='Write what you saw or measured. Leave opinions for later.')
qs = [('WHAT happened?', 'r_what'), ('WHERE exactly?', 'r_where'), ('WHEN did it start?', 'r_when'),
      ('WHO found it?', 'r_who'), ('WHICH product, part or batch?', 'r_which'), ('HOW does it show up?', 'r_how'), ('HOW MUCH, and HOW OFTEN?', 'r_howmuch')]
rh = 32
k.need(rh * len(qs))
top = k.y
for i, (q, n) in enumerate(qs):
    y = top - (i + 1) * rh
    k.box(M, y, 150, rh, fill=CREAM)
    k.text(M + 8, y + rh / 2 - 3, q, 'Helvetica-Bold', 7.2, INK)
    k.tf(n, M + 150, y, CW - 150, rh, multiline=True, tip=q)
k.y = top - rh * len(qs) - 12
inline_fields(k, [('HOW OFTEN', 'r_freq', 150, 'dd', ['First time', 'Monthly', 'Weekly', 'Daily', 'Every shift', 'Several times a shift']),
                  ('MAIN IMPACT', 'r_main', 0, 'dd', ['Safety', 'Quality', 'Downtime', 'Waste', 'Customer', 'Cost'])], after=10)
strip_box(k, 'PROBLEM STATEMENT (ONE SENTENCE: WHAT, WHERE, WHEN, HOW MUCH)', 'r_statement', 40)
k.gap(4)
k.label('STEP 2: MEASURE THE IMPACT', right='Not sure how to cost it? Use the Kaizen XP KPI Impact Calculator.')
imp = [('DOWNTIME', 'minutes a week', 'r_i_down'), ('WASTE', 'units, kg or packs a week', 'r_i_waste'),
       ('COST', '£ a week, rough is fine', 'r_i_cost'), ('PEOPLE TIME', 'hours spent dealing with it', 'r_i_people')]
gw = (CW - 3 * 8) / 4
gh = 44
k.need(gh)
top = k.y
for i, (a, b, n) in enumerate(imp):
    x = M + i * (gw + 8)
    k.box(x, top - gh, gw, gh, fill=CREAM, stroke=CREAM)
    c.setFillColor(GOLD); c.rect(x, top - 3, gw, 3, fill=1, stroke=0)
    k.text(x + 8, top - 14, a, 'Helvetica-Bold', 6.3, INK, cs=0.4)
    k.text(x + 8, top - 22, b, 'Helvetica', 6, GREY)
    k.tf(n, x + 8, top - gh + 5, gw - 16, 15, tip=f'{a.title()} ({b})')
k.y = top - gh - 10
strip_box(k, 'SAFETY, QUALITY OR CUSTOMER IMPACT', 'r_i_other', 44)

# ---------------- STEP 3 + 4
k.new_page('STEP 3: CONTAIN IT', 'RCFA  |  PAGE 2 OF 5', 'Stop it hurting today. This buys you time. It is not the fix.')
k.table('r_cont', [('CONTAINMENT ACTION', 0, 'text', None), ('OWNER', 100, 'text', None), ('DONE BY', 70, 'text', None),
                   ('STATUS', 96, 'dd', ['Not started', 'In place', 'Removed'])], rows=5, row_h=22)
k.gap(4)
k.label('STEP 4: BUILD THE TIMELINE', right='What happened, in order. Patterns hide in the order of events.')
k.table('r_time', [('DATE / TIME', 80, 'text', None), ('WHAT HAPPENED', 0, 'text', None),
                   ('HOW DO I KNOW?', 118, 'dd', ['Saw it myself', 'Someone told me', 'Machine log or data', 'Paperwork or records'])],
        rows='fill', row_h=22)

# ---------------- STEP 5
k.new_page('STEP 5: LIST EVERY POSSIBLE CAUSE', 'RCFA  |  PAGE 3 OF 5', 'Write down everything, even the unlikely ones. Then rule them out with evidence, not a hunch.')
prompts = {'People': 'Training, experience, shift, handover', 'Machine': 'Wear, settings, sensors, maintenance',
           'Method': 'Standard work, sequence, changeover', 'Material': 'Supplier, batch, spec, storage',
           'Measurement': 'Gauges, checks, data, calibration', 'Environment': 'Heat, damp, dust, lighting, layout'}
gw = (CW - 10) / 2
gh = 84
for row in range(3):
    k.need(gh + 8)
    top = k.y
    for col in range(2):
        m = SIXM[row * 2 + col]
        x = M + col * (gw + 10)
        k.box(x, top - gh, gw, gh)
        c.setFillColor(BLACK); c.rect(x, top - 15, gw, 15, fill=1, stroke=0)
        k.text(x + 8, top - 10, m.upper(), 'Helvetica-Bold', 6.6, GOLD, cs=0.6)
        k.text(x + gw - 8, top - 10, prompts[m], 'Helvetica-Oblique', 6, HexColor('#bbbbbb'), align='right')
        c.acroForm.textfield(name=k._name(f'r_6m_{m.lower()}'), tooltip=f'{m} causes', x=x, y=top - gh, width=gw, height=gh - 15,
                             borderWidth=0, fillColor=None, textColor=FIELDINK, fontName='Helvetica', fontSize=8,
                             fieldFlags='multiline', maxlen=2000, annotationFlags='print')
    k.y = top - gh - 8
k.gap(2)
k.label('RULE THEM OUT', right='Every cause gets checked. "Seems unlikely" is not a check.')
k.table('r_rule', [('POSSIBLE CAUSE', 0, 'text', None), ('HOW I CHECKED IT', 170, 'text', None),
                   ('RESULT', 104, 'dd', ['Ruled out', 'Confirmed', 'Still checking'])], rows='fill', row_h=22)

# ---------------- STEP 6
k.new_page('STEP 6: FIND THE ROOT CAUSE', 'RCFA  |  PAGE 4 OF 5', 'Take what is left after Step 5 and keep asking why until you hit something you can fix.')
strip_box(k, 'STARTING POINT (THE CONFIRMED CAUSE FROM STEP 5)', 'r_start', 30)
for i in range(1, 6):
    h = 36
    k.need(h + 8)
    top = k.y
    cy = top - h / 2
    c.setFillColor(BLACK); c.circle(M + 13, cy, 11, fill=1, stroke=0)
    k.text(M + 13, cy + 1, str(i), 'Helvetica-Bold', 9, GOLD, align='center')
    k.text(M + 13, cy - 6.5, 'WHY?', 'Helvetica-Bold', 4.6, white, align='center')
    if i < 5:
        c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(M + 13, cy - 11, M + 13, top - h - 8)
    k.tf(f'r_why{i}', M + 32, top - h, CW - 32, h, multiline=True, tip=f'Why {i}')
    k.y = top - h - 8
k.gap(2)
strip_box(k, 'ROOT CAUSE', 'r_root', 38)
inline_fields(k, [('CATEGORY', 'r_root_cat', 130, 'dd', SIXM), ('PROVEN?', 'r_root_proven', 0, 'dd', ['Yes, proven with evidence', 'Not yet, still a theory'])], after=10)
strip_box(k, 'HOW I PROVED IT (THE TEST, THE DATA, OR THE TRIAL)', 'r_proof', 40)
k.note('THE TEST', 'If you fix this, does the problem stop? If you are not sure, it is not the root cause yet. If the answer is a person, ask why the system let it happen and go again.', after=0)

# ---------------- STEP 7 + 8
k.new_page('STEP 7: FIX IT FOR GOOD', 'RCFA  |  PAGE 5 OF 5', 'Every action aims at the root cause, has a name next to it, and has a date.')
k.table('r_act', [('PERMANENT ACTION', 0, 'text', None), ('OWNER', 92, 'text', None), ('DUE', 62, 'text', None),
                  ('STATUS', 92, 'dd', ['Open', 'In progress', 'Done', 'Done and checked'])], rows=6, row_h=24)
k.gap(2)
k.label('STEP 8: CHECK, LOCK IT IN, SPREAD IT')
strip_box(k, 'HOW WILL WE KNOW IT WORKED? (THE NUMBER WE WILL CHECK)', 'r_measure', 34)
inline_fields(k, [('CHECK DATE', 'r_checkdate', 90, 'text', None), ('BEFORE', 'r_before', 120, 'text', None), ('AFTER', 'r_after', 0, 'text', None)], after=10)
inline_fields(k, [('RESULT', 'r_result', 160, 'dd', ['Fixed', 'Partly fixed, keep going', 'Not fixed, reopen']),
                  ('LOCKED IN BY', 'r_locked', 0, 'dd', ['Standard work updated', 'Checklist updated', 'One-point lesson', 'Maintenance plan updated', 'Training for every crew', 'Design or layout change'])], after=10)
strip_box(k, 'HOW IT WAS LOCKED IN (THE DETAIL)', 'r_locked_detail', 30)
strip_box(k, 'WHERE ELSE COULD THIS HAPPEN? (OTHER LINES, SHIFTS, SITES, MACHINES)', 'r_spread', 40)
k.label('SIGN-OFF')
inline_fields(k, [('INVESTIGATION LEAD', 'r_sig_lead', 150, 'text', None), ('MANAGER', 'r_sig_mgr', 0, 'text', None)])
inline_fields(k, [('DATE CLOSED', 'r_closed', 90, 'text', None), ('STATUS', 'r_status', 0, 'dd', ['Closed', 'Open, waiting on actions', 'Reopened'])], after=10)
k.note('WHO SAW IT?', 'A finished RCFA nobody senior reads is a favour you did the company. Walk it through with your line leader, and put the result in your Weekly Wins email.', after=0)

back(k, 'ROOT CAUSE FOUND', 'Now make it count.', 'The rest of the Kaizen XP range', None, None,
     catalog_except('THE RCFA TEMPLATE'), 'A closed RCFA is the best entry you will ever put in your Visibility Kit.')
c.save()
print('pages', k.page, 'fields', len(k.names))
