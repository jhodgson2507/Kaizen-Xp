FAIL

# Product QA: The KPI Impact Calculator

File: products/kpi-calculator/Kaizen_XP_KPI_Impact_Calculator.xlsx
Checked: 2026-10-27 by product-qa, on copies only. Nothing in products/ was changed.

## What passed

- Recalculated in LibreOffice headless: 59 formulas, 0 errors.
- The repo file matches what build.py produces today (0 cell differences).
- Worked example (Example tab, Line 3 labeller) checked by hand in Python:
  - People hours a year: 4 x 6 x 1 x 15 x 52 / 60 = 312 before, 78 after, saving 234. Sheet: 312 / 78 / 234. Correct.
  - Staff cost at £13: £4,056 before, £1,014 after, saving £3,042. Correct.
  - Waste: 40 x £0.80 x 52 = £1,664 before, £416 after, saving £1,248. Correct.
  - Total saving £4,290, £82.50 a week, £25 fix pays back "Under a week". Correct.
  - Improvement Log example row (234 hours, £4,290) matches the Example tab.
- Fresh test typed into a copy of the Calculator tab (6 to 2 times a shift, 10 to 5 minutes, 2 to 1 people, 10 shifts, 48 weeks, £15/hr, £300/hr downtime, 20 to 5 units at £2, £500 to £100 lost sales at 30% margin, £10,000 fix). Worked out in Python: £167,520 before, £27,120 after, £140,400 saving, £2,925 a week, 3 weeks payback. The sheet gave exactly the same numbers.
- Example and Calculator tabs: every unlocked cell is cream with blue text, every formula is locked, sheet protection is on.
- No em dashes in the file or build script. Copyright line on Start Here, Example and Calculator. Motto on Start Here. Arial throughout.
- Renders cleanly: Start Here, Example and Calculator each print on one portrait page, nothing cut off.

## Problems (must fix before listing)

1. Improvement Log, B10:H58: input cells have blue text but no cream fill (343 cells). Only the example row 9 is cream. This breaks the "cream boxes with blue text" rule that Start Here teaches.
   Fix in build.py, Improvement Log loop: add `cell.fill = fill(CREAM)` and `cell.protection = Protection(locked=False)` for every cell in rows 9 to 58, columns B to H.

2. Improvement Log, E5, F5, E6: the running total formulas are not protected (the sheet has no protection at all). Start Here row 22 promises "The formulas are locked so they cannot be broken by accident."
   Fix: after making B9:H58 unlocked (problem 1), add `lg.protection.sheet = True` with `formatCells/formatColumns/formatRows = False`, same as the calculator tabs.

3. Calculator, B44 (Your sentence): the sentence is wrong whenever there is no reduction in times per shift. Start Here step 3 tells buyers to fill in BEFORE now and AFTER later, and on that exact path the sheet says "I reduced Conveyor jam from 3 to 3 times a shift. That gives back about 0 people hours a year and is worth roughly £0 a year, for a fix that cost £50." If AFTER is worse it says "I reduced the problem from 3 to 5 times a shift ... worth roughly £-1,248". If the fix only cut the minutes, it still says "from 3 to 3 times". Same formula on Example!B44.
   Fix: branch the formula on E36. When E36 <= 0, show a "cost" sentence instead, for example: `"Right now "&IF(C6="","this problem",C6)&" costs about £"&TEXT(C36,"#,##0")&" a year and ties up about "&TEXT(C30,"#,##0")&" people hours."` Only use "I reduced ..." when E36 > 0, and talk about the saving rather than times per shift when C13 equals the AFTER value.

4. Calculator and Example, B44: grammar "from 4 to 1 times a shift" in the worked example sentence.
   Fix: use `IF(<after>=1," time"," times")` in the sentence formula.

5. Whole workbook: no page or tab linking the rest of the Kaizen XP range. CLAUDE.md says every product has "a back page linking the rest of the range". There is no mention of the Visibility Kit, Starter Kit, RCFA Template, MTBA Tracker or Breakdown Dashboard anywhere.
   Fix: add a final tab "More from Kaizen XP" (or a block at the bottom of Start Here) listing the range, with the motto and copyright line, styled like Start Here.

6. Improvement Log: no copyright line and no print setup. It prints across 5 pages with the running total labels split from their numbers.
   Fix: add the copyright line under row 58 (for example B60), set `lg.print_area = 'A1:I60'`, landscape, `fitToWidth = 1`, `fitToHeight = 0`, `fitToPage = True`.

## Smaller points (fix if cheap)

7. Calculator and Example, C27 (Margin %): if a buyer types 25% (Excel stores 0.25) instead of 25, lost margin is 100 times too small and nothing warns them.
   Fix: add data validation on C27 (decimal between 1 and 100, error message "Type 25 for 25%"), or use `IF(N(C27)<1,N(C27)*100,N(C27))` in C35 and D35.

8. Example tab, all 22 input cells are unlocked, so a buyer can type over the worked example by mistake.
   Fix: in build.py, lock the inputs on the Example sheet only (set `locked=True` after `build_calc(exs, ...)`) so the example stays intact.

9. Calculator, rows 32 and 33: when a downtime cost is filled in, the sheet adds staff cost and downtime cost together. If the buyer's "cost of an hour of lost output" already includes labour, the total is double counted.
   Fix: add to note F21: "Do not include wages here, they are already counted above."

10. Start Here, C22 (Works in): says formulas are locked in Apple Numbers. Numbers does not keep Excel sheet protection.
    Fix: reword to "Formulas are locked in Excel and Google Sheets."

## Listing match

products/kpi-calculator/listing.md says "Status: NOT WRITTEN YET" and price "not set". There are no listing promises to check yet. This product cannot be listed until the listing exists and is checked against this file.

## Evidence

Scratch copies, recalculated files, test files and renders are in
/tmp/claude-0/-home-user-Kaizen-Xp/b17d22de-2ac1-57c1-a9a9-a5a5d4cbe0e7/scratchpad/qa-xlsx/
