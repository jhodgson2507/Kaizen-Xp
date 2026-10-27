# Usability check: The RCFA Template

**Verdict: Ready with fixes.** The eight steps run in the right order, RCFA is explained on page 2, and the worked example is solid. The page tags clash with the real page numbers, several dropdowns have no way out, labels are below 7pt, and it points buyers to tools they may not own. The Etsy listing has not been written yet and the price is not set, so the product cannot be listed until both are done.

Checked: products/rcfa-template/Kaizen_XP_RCFA_Template.pdf, all 9 pages rendered at 100 dpi and at 400 px wide (phone), fields read with pypdf, text sizes read with pdfplumber. products/rcfa-template/listing.md.

## Scores by page

| Page | What it is | Score | Why |
| --- | --- | --- | --- |
| 1 | Cover | 4/5 | Subtitle "Root cause analysis for the faults that keep coming back" saves the jargon title. Black page eats toner. |
| 2 | Read this first | 5/5 | Explains RCFA in plain words, eight steps listed, THREE RULES are spot on. |
| 3 | Worked example: Line 3 labeller | 4/5 | Real-sounding and the maths is right (4 x 6 x 15 = 6 hours). It is a summary, so steps 4 and 5 tables are not shown filled in. |
| 4 | Steps 1 and 2 | 3/5 | Good fact prompts. "HOW OFTEN" dropdown repeats the "HOW MUCH, and HOW OFTEN?" row. Tag says "PAGE 1 OF 5" on PDF page 4. |
| 5 | Steps 3 and 4 | 4/5 | Plenty of timeline rows. "How do I know?" list has no way out. |
| 6 | Step 5 | 4/5 | Six categories with hints, then a rule-out table. "Measurement" and "spec" may lose persona 1. |
| 7 | Step 6 | 4/5 | 5 Whys flows from Step 5. "WHY?" in the circles is 4.6pt. |
| 8 | Steps 7 and 8, sign-off | 3/5 | Covers everything, but "Locked in by" has no "Other", sign-off says "Manager", and the closing note sends buyers to a "Weekly Wins email" they may not have. |
| 9 | Back page | 3/5 | Links all five other products, good. MTBF, MTTR, Pareto, KPI unexplained; no way to find the shop. |

## Issues, worst first

1. **Page tags fight the real page numbers.** Pages 4 to 8 are tagged "RCFA | PAGE 1 OF 5" to "PAGE 5 OF 5", but the PDF viewer shows page 4 of 9 and so on, and no footer shows a page number. Persona 1 on a phone and persona 2 sorting a printed stack both get lost. Fix: change the tags to the steps they hold: "STEPS 1 AND 2", "STEPS 3 AND 4", "STEP 5", "STEP 6", "STEPS 7 AND 8", and add "Page X of 9" to every footer (kitlib.py).

2. **Labels are below the 7pt minimum on every form page, and "WHY?" is 4.6pt.** Field labels 6.3pt, column headers 6.2pt, the category hints on page 6 ("Training, experience, shift, handover") 6.0pt, footer 6.3pt light grey. Page 7 "WHY?" in the circles is 4.6pt. Persona 1 and persona 2. Fix: in kitlib.py raise labels, headers and hints to 7 to 7.5pt and darken the footer to #666666; in products/rcfa-template/build.py line 149 raise "WHY?" from 4.6 to 6.5pt.

3. **On paper the dropdown choices disappear.** Pages 4 (HOW OFTEN, MAIN IMPACT), 5 (STATUS, HOW DO I KNOW?), 6 (RESULT), 7 (CATEGORY, PROVEN?), 8 (STATUS, RESULT, LOCKED IN BY, STATUS). Persona 2 sees empty boxes with arrows. Fix: print the choices as a small hint under each label or header, for example under RESULT on page 6: "Ruled out / Confirmed / Still checking"; under HOW DO I KNOW?: "Saw it / Told / Machine log / Paperwork".

4. **Dropdowns with no way out.**
   - Page 4 MAIN IMPACT (Safety, Quality, Downtime, Waste, Customer, Cost): no "More than one". Fix: add "More than one".
   - Page 5 HOW DO I KNOW? (Saw it myself, Someone told me, Machine log or data, Paperwork or records): no photo or video, no "Other". Fix: add "Photo or video" and "Other".
   - Page 8 LOCKED IN BY (six options): no "Other". Fix: add "Other".
   Persona 1 picks the nearest wrong option or leaves it blank.

5. **"HOW OFTEN" is asked twice.** Page 4: the facts table row "HOW MUCH, and HOW OFTEN?" sits directly above a HOW OFTEN dropdown. Persona 1 fills one and skips the other. Fix: rename the row "HOW MUCH? (minutes lost, units scrapped, £)" and keep the dropdown for how often.

6. **Sends buyers to tools they may not own.** Page 4 Step 2 hint "Use the Kaizen XP KPI Impact Calculator" (price not set, may not be on sale); page 8 note "put the result in your Weekly Wins email" (a Visibility Kit tool). Persona 1 bought only this template and is stuck. Fix: page 4 hint "Not sure how to cost it? Use your own hourly rate as the lowest honest number. The Kaizen XP KPI Impact Calculator can do the sums for you." Page 8 note: "...Walk it through with your line leader, and send them a short email with the result. (The Kaizen XP Visibility Kit has a template for that.)"

7. **"Manager" in the sign-off, "line leader" in the note below it.** Page 8. Fix: keep two roles but name them the range way: "INVESTIGATION LEAD" and "LINE LEADER OR MANAGER".

8. **"TEAM" is unclear.** Page 4, TEAM field next to LEAD. Persona 1 may write their shift team (e.g. "B shift") rather than who helped. Fix: "WHO HELPED".

9. **Jargon a shop floor worker may not use.** Page 6: "Measurement" category, "spec", "calibration"; page 3 "label web", "one-point lesson", "in spec". Fix: page 6 MEASUREMENT hint "Gauges, checks, data: is the reading right?"; MATERIAL hint "Supplier, batch, size or thickness, storage"; page 3 "measured, in spec" to "measured, within limits"; "one-point lesson" to "one-point lesson (a single sheet with photos showing the one right way)".

10. **Long entries in table rows vanish when printed.** Pages 5, 6 and 8: single-line cells at a fixed 8pt with up to 200 characters. Fix: auto font size (DA "0 Tf") for single-line table cells.

11. **Back page wording.** Page 9: "MTBF, MTTR and a Pareto" and "KPI" mean nothing to persona 1; "All available from Kaizen XP" gives no way to find them. Fix: "How often each machine breaks, how long it takes to fix, and which one to fix first." and "Search Kaizen XP on Etsy to find them all."

12. **Phone use and ink.** Every form page needs pinch-zoom; covers are solid black. Fix (page 2 HOW TO USE): add "On a phone, turn it sideways and pinch to zoom. In Acrobat Reader, tap a box, then use the arrows above the keyboard to jump to the next one. To save ink, print pages 4 to 8 only."

## Quick wins (under five minutes each)

- Page tags to step names.
- Add "More than one", "Photo or video", "Other" to the three lists.
- Page 4: rename the HOW MUCH row; TEAM to WHO HELPED.
- Page 8: sign-off label and the Weekly Wins note.
- Page 9: plain-words dashboard line and "Search Kaizen XP on Etsy".

## What works well

- Page 2 is the best plain-English explanation of RCFA in the range ("The fault was never fixed. It was just survived."), and the THREE RULES box should stay word for word.
- Step 5 into Step 6 is well ordered: list causes by category, rule them out with evidence, then 5 Whys only on what is left.

## Listing (persona 3)

listing.md has no title, photo brief or description yet and the price is not set, so the ten-second test cannot be run. For the listing-optimiser: lead with the problem, not the acronym, for example "Root Cause Analysis Template for Repeat Faults | RCFA, 5 Whys, Fishbone Categories | Fillable PDF". First photo: page 3 worked example.

## Range consistency (all four PDFs)

| Thing | What the range says now | Use everywhere |
| --- | --- | --- |
| The person you report to | "line leader" (Visibility, this note), "manager" (this sign-off, Visibility p12), "boss" (Visibility p5) | "line leader". Keep "Manager" only as a separate sign-off role. |
| Where the work is | LINE / EQUIPMENT here; EQUIPMENT / LINE on the CI kit's One-Page RCFA; LINE / MACHINE / AREA in MTBA | LINE / MACHINE / AREA |
| Impact types | Here: Safety, Quality, Downtime, Waste, Customer, Cost. CI One-Page RCFA: Downtime, Waste, Cost, Safety, Quality, More than one. Visibility: Time, Waste, Cost, Safety, Quality, More than one | One list: Downtime or time, Waste, Cost, Safety, Quality, Customer, More than one |
| Action status | Here: Open / In progress / Done / Done and checked. CI 5 Whys: Not started / In progress / Done / Done and checked | Not started / In progress / Done / Done and checked |
| Did it work? | Here: Fixed / Partly fixed, keep going / Not fixed, reopen. CI: Yes, fixed / Partly, keep going / No, go again | Fixed / Partly fixed, keep going / Not fixed, go again |
| Steps | Here 8 steps; CI One-Page RCFA has 7 numbered boxes and says the template is "the full eight-step investigation" | Fine as is; matches |
| Page numbers | None printed anywhere; this file's tags say "PAGE 1 OF 5" | Add "Page X of Y" to every footer in kitlib.py |
| Back page | Visibility lists 1 product; this and the other two list 5 | Same five-product block on all |
