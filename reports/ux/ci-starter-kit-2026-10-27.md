# Usability check: The Frontline CI Starter Kit (v2)

**Verdict: Ready with fixes.** Five clean, usable sheets, but "CI" and "RCFA" are never explained, three of the five tools have no worked example, labels are below 7pt, and paper users cannot see the dropdown choices. The Etsy listing has not been written yet (listing.md says "NOT WRITTEN YET"), so the product cannot be listed until that is done and checked.

Checked: products/ci-starter-kit/Kaizen_XP_Frontline_CI_Starter_Kit_v2.pdf, all 10 pages rendered at 100 dpi and at 400 px wide (phone), fields read with pypdf, text sizes read with pdfplumber. products/ci-starter-kit/listing.md.

## Scores by page

| Page | What it is | Score | Why |
| --- | --- | --- | --- |
| 1 | Cover | 3/5 | "CI" in the title is jargon to persona 1 and persona 3. Full black page eats toner. |
| 2 | How to use this kit | 3/5 | Good voice, but "No jargon. No 40-page manual." appears twice, "CI" and "RCFA" are never spelled out, and START HERE points to the last tool with no page number. |
| 3 | Shift Handover Log | 4/5 | Prompts are right and boxes are big. No example, Shift list has no "Other". |
| 4 | 5 Whys Worksheet (blank) | 4/5 | Clear. "WHY?" in the circles is 4.6pt. Blank comes before the example. |
| 5 | 5 Whys worked example | 4/5 | Feels like a real shift. "Three more whys" should be four. "One-point lesson" is unexplained. |
| 6 | Quick Wins Tracker | 4/5 | Fast to fill, one example row. Result list has no "More than one". |
| 7 | Quick Wins Tracker continued | 4/5 | As above. |
| 8 | One-Page RCFA | 3/5 | Good steps, but "RCFA" is never explained in this kit and there is no example. |
| 9 | Daily CI Habit Tracker | 3/5 | Simple, but the DONE tick boxes are 11pt (4mm): hard to tap on a phone. No example line. |
| 10 | Back page | 3/5 | Links the whole range, good. Odd kicker "FIVE TOOLS IN", unexplained MTBF, MTTR, Pareto, KPI, no way to find the shop. |

## Issues, worst first

1. **"CI" and "RCFA" are never explained.** Cover, page 2, page 8, page 10. Persona 1 (never heard of RCFA) and persona 3 (deciding in ten seconds) hit this first. Page 2 says "continuous improvement" but never ties it to "CI". Fix:
   - Page 2, third paragraph: "That is all continuous improvement (CI) really is."
   - Page 2, tool 4 description: "RCFA means Root Cause Failure Analysis: finding the real reason a fault keeps coming back. This is it stripped to one page."
   - Page 8 subtitle: "RCFA = Root Cause Failure Analysis. For the faults that keep coming back. Do this properly once, and it stops."

2. **Labels are below the 7pt minimum on every form page, and "WHY?" is 4.6pt.** Field labels 6.3pt, column headers 6.2pt, footer 6.3pt light grey (#9a9a9a). The "WHY?" text in the numbered circles on pages 4 and 5 is 4.6pt white on black. Persona 1 and persona 2. Fix: in kitlib.py raise labels and headers to 7.5pt and darken the footer to #666666; in products/ci-starter-kit/build.py line 78 raise "WHY?" from 4.6 to 6.5pt (grow the circle if needed).

3. **On paper the dropdown choices disappear.** Pages 3 (SHIFT, HOW), 4 (STATUS), 6 and 7 (RESULT), 8 (IMPACT TYPE, DID IT WORK?). Persona 2 sees an empty box with an arrow. Fix: print the choices as a small hint under the label or column header, for example under RESULT: "Saved time / Less waste / Safer / Better quality / Saved money / Easier job"; under STATUS: "Not started / In progress / Done / Done and checked".

4. **Three tools have no worked example.** Shift Handover Log (page 3), One-Page RCFA (page 8), Daily CI Habit Tracker (page 9). CLAUDE.md says every product has a worked example; persona 1 does not know what "good" looks like for a handover or an RCFA. Fix:
   - Page 9: add one filled example row above day 1, styled like the Quick Wins example row: "Ex. | Put the tape gun back on its shadow board and labelled the spot | ticked".
   - Page 3: add grey hint text inside each box, for example RUNNING NOW: "e.g. Line 3 running 500ml, 92% speed, labeller fixed at 04:10"; WATCH THIS: "e.g. Filler head 4 dripping, getting worse since 02:00".
   - Page 8: add a one-line pointer under the subtitle: "See the labeller example on the 5 Whys page: the RCFA uses the same thinking with evidence." Better still, add a filled One-Page RCFA example page using the Line 3 labeller story (the RCFA Template already has the content).

5. **START HERE points to the last tool, with no page number.** Page 2 says "Start with the Daily CI Habit Tracker" which is Tool 5 on page 9, and no page has a printed page number. Persona 1 scrolls through four other tools looking for it. Fix: "Start with Tool 5, the Daily CI Habit Tracker, on page 9." and add "Page X of 10" to the footer (kitlib.py).

6. **DONE tick boxes are too small to tap.** Page 9, 31 checkboxes at 11 x 11pt (about 7 px wide at phone width). Persona 1. Fix: make each checkbox 16 x 16pt (rows are 16pt tall, so grow rows to 18pt; the page has room above the note).

7. **Long entries in table rows vanish when printed.** Pages 6, 7 and 9: single-line cells at a fixed 8pt with up to 200 characters. Text past the cell edge is cut off on print. Persona 1. Fix: set single-line table cells to auto font size (DA "0 Tf").

8. **Dropdowns without a way out.** Page 3 SHIFT (Days / Earlies / Lates / Nights / Weekend) has no "Other" and "Weekend" overlaps with the others; pages 6 and 7 RESULT has no "More than one". Persona 1 working "Afternoons" or "Twilights" has nothing to pick. Fix: SHIFT list "Days / Earlies / Lates / Nights / Other"; RESULT list add "More than one".

9. **Wrong count in the 5 Whys example.** Page 5, WHY IT WORKS: "Three more whys found a fix". There are four more (whys 2 to 5). Fix: "Four more whys found a fix that costs nothing and stops it on every shift."

10. **"One-point lesson" is unexplained.** Page 5, THE FIX. Fix: "Write a one-point lesson (a single sheet with photos showing the one right way) and show every crew this week."

11. **Back page wording.** Page 10: the kicker "FIVE TOOLS IN" reads like a typo; "MTBF, MTTR and a Pareto" and "KPI" mean nothing to persona 1; "Available from Kaizen XP" gives no way to find them. Fix: kicker "ALL FIVE TOOLS DONE"; dashboard line "How often each machine breaks, how long it takes to fix, and which one to fix first."; calculator line "Put a pound sign on any problem in two minutes." (keep, but the name is fine); last line "Search Kaizen XP on Etsy to find them all."

12. **Repeated line.** Page 2: "Five tools. No jargon. No 40-page manual." is the subtitle and then appears again in the fourth paragraph. Fix: cut the fourth paragraph's copy to "These five tools are the ones that actually get used on a shop floor. Print them, keep them on the line, fill them in as you go."

13. **Worked example sits after the blank.** Pages 4 and 5. The Visibility Kit shows the example first. Fix: swap pages 4 and 5 so the buyer sees what good looks like before the blank form.

14. **Phone use.** Every form page needs pinch-zoom on a phone. Persona 1. Fix (page 2 HOW TO USE): add "On a phone, turn it sideways and pinch to zoom on the box you want. In Acrobat Reader, tap a box, then use the arrows above the keyboard to jump to the next one."

15. **Black cover and back page waste ink.** Pages 1 and 10. Persona 2. Fix: add to HOW TO USE "To save ink, print pages 3 to 9 only."

## Quick wins (under five minutes each)

- Page 2: spell out CI and RCFA; START HERE with page number; cut the repeated line.
- Page 5: "Three more whys" to "Four more whys"; explain one-point lesson.
- Page 3: SHIFT list add "Other", drop "Weekend". Pages 6 and 7: RESULT add "More than one".
- Page 10: new kicker and plain-words dashboard line.

## What works well

- The 5 Whys example (Line 3 labeller) is the best teaching page in the kit: each answer becomes the next question, and THE RULE ("If your root cause is a person, you have not gone deep enough") is exactly right.
- The Handover Log prompt "WATCH THIS (SOMETHING NOT BROKEN YET, BUT HEADING THAT WAY)" is a real shop-floor insight. Keep it.

## Listing (persona 3)

listing.md has no title, photo brief or description yet, so the ten-second test cannot be run. For the listing-optimiser: do not lead with "CI". For example "Shift Handover Log, 5 Whys and Root Cause Templates | Continuous Improvement Starter Kit | Fillable PDF". First photo: the 5 Whys worked example, because it shows the method in one look.

## Range consistency (all four PDFs)

| Thing | What the range says now | Use everywhere |
| --- | --- | --- |
| The person you report to | "line leader" (Visibility, RCFA note), "manager" (Visibility p12, RCFA sign-off), "boss" (Visibility p5), "shift leaders" (covers) | "line leader". Keep "Manager" only as a separate sign-off role. |
| Where the work is | LINE / AREA (handover), EQUIPMENT / LINE (One-Page RCFA), AREA (habit tracker), LINE / EQUIPMENT (RCFA Template), LINE / MACHINE / AREA (MTBA) | LINE / MACHINE / AREA |
| Impact or result types | Quick Wins: Saved time, Less waste, Safer, Better quality, Saved money, Easier job. One-Page RCFA: Downtime, Waste, Cost, Safety, Quality, More than one. Visibility: Time, Waste, Cost, Safety, Quality, More than one. RCFA Template: Safety, Quality, Downtime, Waste, Customer, Cost | One list: Downtime or time, Waste, Cost, Safety, Quality, Customer, More than one |
| Action status | CI: Not started / In progress / Done / Done and checked. RCFA: Open / In progress / Done / Done and checked | Not started / In progress / Done / Done and checked |
| Did it work? | CI: Yes, fixed / Partly, keep going / No, go again. RCFA: Fixed / Partly fixed, keep going / Not fixed, reopen | Fixed / Partly fixed, keep going / Not fixed, go again |
| "5 Whys" | "5 Whys" here, "five whys" on Visibility Kit page 2 | "5 Whys" |
| Page numbers | None printed anywhere | Add "Page X of Y" to every footer in kitlib.py |
| Back page | Visibility lists 1 product; the other three list 5 | Same five-product block on all |
