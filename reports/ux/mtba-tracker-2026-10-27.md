# Usability check: The MTBA Assist Tracker

**Verdict: Ready with fixes.** The idea is explained well and the log is quick to fill, but the worked example ranks two assist types in the wrong order, "biggest type" means two different things, "run time" is never defined, and paper users cannot see the assist types. The Etsy listing has not been written yet and the price is not set, so the product cannot be listed until both are done.

Checked: products/mtba-tracker/Kaizen_XP_MTBA_Assist_Tracker.pdf, all 8 pages rendered at 100 dpi and at 400 px wide (phone), fields read with pypdf, text sizes read with pdfplumber, every sum in the worked examples re-done by hand. products/mtba-tracker/listing.md.

## Scores by page

| Page | What it is | Score | Why |
| --- | --- | --- | --- |
| 1 | Cover | 3/5 | "MTBA" in the title means nothing to persona 1 or persona 3 until page 2. Black page eats toner. |
| 2 | Read this first | 4/5 | Plain explanation, formula with an example, four steps with page numbers. "Run time" not defined; page numbers are not printed on the pages. |
| 3 | Shift Assist Log, sheet 1 | 3/5 | Fast to fill and an example row. Assist types invisible on paper; "BIGGEST TYPE: most common today" clashes with the weekly rule. |
| 4 | Shift Assist Log, sheet 2 | 3/5 | As page 3. Only two sheets for "log every assist for one week". |
| 5 | Worked example: one week on Line 3 | 3/5 | Realistic and totals are right, but RANK is wrong for two rows. |
| 6 | Weekly Summary | 4/5 | Clear table and cost line. |
| 7 | Before and After | 4/5 | The page you show people, and it looks like it. "Worth per year" hint points at a number that is not on the page. |
| 8 | Back page | 3/5 | Links all five other products. MTBF, MTTR, Pareto, KPI unexplained; no way to find the shop. |

## Issues, worst first

1. **Worked example ranks are wrong.** Page 5. The page and step 2 on page 2 say rank by minutes lost, but Reset or restart (28 minutes) is ranked 3 and Re-handle or re-work (30 minutes) is ranked 4. Persona 1 copying the example learns the wrong rule; a sharp buyer loses trust. Fix: rank Re-handle or re-work 3 and Reset or restart 4, and list the rows in rank order: Jam or blockage 58 / 348 / 1; Misfeed or misalignment 21 / 84 / 2; Re-handle or re-work 6 / 30 / 3; Reset or restart 14 / 28 / 4; Manual adjustment 9 / 18 / 5. (Everything else checks out: 108 assists, 508 minutes, 6,750 / 108 = 62, 6,750 / 57 = 118, 508 minus 232 = 276 minutes = 4.6 hours.)

2. **"Biggest" means two different things.** Pages 3 and 4, END OF SHIFT "BIGGEST TYPE: most common today"; page 2 step 2 and page 6 say "the type with the most minutes lost". Persona 1 picks the most frequent, then the weekly sheet ranks by minutes. Fix: pages 3 and 4 hint "most minutes lost today".

3. **"Run time" is never defined, and the examples use two different numbers.** Page 2 says "An 8-hour shift is 480 minutes"; page 5 uses 450 minutes a shift without saying why. Persona 1 does not know whether to include breaks or changeovers. Fix: add to page 2 under the formula: "Run time = the minutes the job was meant to be running. Leave out breaks and planned stops. An 8-hour shift with 30 minutes of breaks is 450 minutes." Pages 3 and 4 label: "RUN TIME THIS SHIFT (MINS, NOT COUNTING BREAKS)".

4. **On paper the assist types disappear.** Pages 3 and 4 ASSIST TYPE column, SHIFT, BIGGEST TYPE; page 7 ASSIST TYPE FIXED, WHO SAW IT. Persona 2 (supervisor handing out printed logs) gets everyone writing their own words, so the weekly summary on page 6 cannot be added up. Fix: under the log table on pages 3 and 4 print a key line: "Assist types: Jam or blockage / Misfeed or misalignment / Reset or restart / Manual adjustment / Re-handle or re-work / Material or supply issue / Other". Same idea for WHO SAW IT on page 7: "Line leader / Manager / Both / Wider team / Nobody yet".

5. **Two log sheets for a week of logging, and no instruction to make more.** Page 2 step 1 says log every assist for one week; each sheet is one shift; there are two. Persona 2 running 15 shifts a week, and persona 1 on screen who will overwrite sheet 1. Fix page 2 step 1: "Use one Shift Assist Log per shift. Print as many as you need, or on screen save a copy of the file for each shift. Page 3." Add the same line as a subtitle on page 3.

6. **Labels are below the 7pt minimum on every form page.** Field labels 6.3pt, column headers 6.2pt, hint lines ("count the rows", "run time ÷ assists") 6.0pt, footer 6.3pt light grey. Persona 1 and persona 2. Fix in kitlib.py: labels and headers to 7.5pt, hints to 7pt, footer colour #666666.

7. **Page numbers are quoted but not printed.** Page 2 says "Page 3", "Page 6", "Page 7"; no footer shows a page number. Persona 2 with a printed stack cannot find "page 6". Fix: add "Page X of 8" to every footer (kitlib.py).

8. **Cover title is jargon.** Page 1. Persona 3 sees "The MTBA Assist Tracker" in the thumbnail and does not know what it is. Fix: add a line under the title: "MTBA = Mean Time Between Assists" and keep the gold subtitle.

9. **Divide by zero at end of shift.** Pages 3 and 4, MTBA (MINS) "run time ÷ assists". A shift with no assists has nothing to divide by. Fix hint: "run time ÷ assists (no assists? write FULL SHIFT)".

10. **"Worth per year" hint points at a number that is not on the page.** Page 7, WORTH PER YEAR (£) "cost saved per week x 52". There is no "cost saved per week" box. Fix: "(cost before minus cost after) x 52".

11. **"A minute or two" versus 6 minutes a jam.** Page 2 says each assist "only takes a minute or two"; the example jams take 6 minutes each (348 / 58). Fix page 2: "Each one only takes a few minutes, which is exactly why nobody writes them down."

12. **Example row wording.** Page 3 example "Label web snapped at splice" logged as "Jam or blockage". "Web" is printer jargon and a snap is not a jam. Fix: "Label jammed at the reel splice".

13. **Sends buyers to tools they may not own.** Page 5 THE SENTENCE: "That line goes in your Weekly Wins email, your improvement log and your review" (Visibility Kit tools); page 6: KPI Impact Calculator (price not set). Fix page 5: "That line goes in your next update to your line leader and your review. (The Kaizen XP Visibility Kit has a Weekly Wins email and Improvement Log built for it.)"

14. **SHIFT list has no way out.** Pages 3 and 4: Days / Earlies / Lates / Nights / Weekend. "Weekend" overlaps the others, and there is no "Other". Fix: "Days / Earlies / Lates / Nights / Other".

15. **Back page wording, phone use and ink.** Page 8: explain "MTBF, MTTR and a Pareto" as "How often each machine breaks, how long it takes to fix, and which one to fix first."; replace "All available from Kaizen XP" with "Search Kaizen XP on Etsy to find them all." Page 2 HOW TO USE: add "On a phone, turn it sideways and pinch to zoom. In Acrobat Reader, tap a box, then use the arrows above the keyboard to jump to the next one. To save ink, print pages 3 to 7 only." Single-line table cells (pages 3 and 4, WHAT HAPPENED) should use auto font size (DA "0 Tf") so long text is not cut off when printed.

## Quick wins (under five minutes each)

- Page 5: fix the two ranks and the row order.
- Pages 3 and 4: "most common today" to "most minutes lost today"; zero-assist hint; SHIFT list.
- Page 2: run time definition; "a few minutes"; one log sheet per shift.
- Page 7: "Worth per year" hint.
- Page 3: example row wording.

## What works well

- Page 2 explains MTBA better than most paid training: what an assist is, why nobody logs them, the formula with a worked number, and "MTBA or MTBF?" in one box.
- The Before and After page is exactly the page a technician wants to slide across the table. Keep the black "THE DIFFERENCE" boxes.

## Listing (persona 3)

listing.md has no title, photo brief or description yet and the price is not set, so the ten-second test cannot be run. For the listing-optimiser: lead with the problem in plain words, for example "Minor Stops Tracker | Log Jams, Resets and Small Stoppages | MTBA (Mean Time Between Assists) | Fillable PDF". First photo: the Before and After page filled in with the Line 3 numbers.

## Range consistency (all four PDFs)

| Thing | What the range says now | Use everywhere |
| --- | --- | --- |
| The person you report to | Who-saw-it list here and in Visibility: Line leader, Manager, Line leader and manager, Wider team, Nobody yet (good, matches). Elsewhere: "boss" (Visibility p5), "manager" (RCFA sign-off) | "line leader". Keep "Manager" only as a separate role. |
| Where the work is | LINE / MACHINE / AREA here (best); LINE / AREA, EQUIPMENT / LINE, LINE / EQUIPMENT, AREA elsewhere | LINE / MACHINE / AREA |
| Shift list | Same here and in the CI Handover Log (good), but neither has "Other" | Days / Earlies / Lates / Nights / Other |
| Cost of an hour | Here "COST OF AN HOUR (£)"; Visibility "What an hour costs (£)". Both advise "your own hourly rate as the lowest honest number" (good) | "Cost of an hour (£)" |
| "Biggest" | Here: most common (log) vs most minutes (summary) | Most minutes lost |
| Page numbers | Quoted on page 2, printed nowhere | Add "Page X of Y" to every footer in kitlib.py |
| Back page | Visibility lists 1 product; this and the other two list 5 | Same five-product block on all |
| Worked example story | Line 3 labeller in all four products, with matching numbers (4 jams a shift, 6 minutes each, down to 1). Good, keep it | Keep |
