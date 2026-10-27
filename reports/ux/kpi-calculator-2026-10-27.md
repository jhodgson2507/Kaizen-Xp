# Usability check: The KPI Impact Calculator (2026-10-27)

**Verdict: Ready with fixes.** The Calculator itself works and the worked example is strong, but the Improvement Log contradicts the "save a copy per problem" instruction, a waste-only problem never gets its sentence, and the Etsy listing has not been written yet, so it cannot go on sale until that exists.

File checked: products/kpi-calculator/Kaizen_XP_KPI_Impact_Calculator.xlsx (and listing.md).
How: every tab read in order with openpyxl (values, fonts, lock state, dropdowns), the whole file rendered through LibreOffice to PDF and PNG and looked at page by page, and three fresh test cases typed into copies and recalculated (scratch copies only, repo files untouched).

## Scores by tab

| Tab | Score | Why |
| --- | --- | --- |
| Start Here | 4/5 | Clear, plain and short. The labeller sentence sells the idea in ten seconds. Loses a point for the "save a copy for each problem" advice that breaks the running total. |
| Example | 4/5 | Looks like a real shift (Line 3 nights, Sam, Week 2) and the sentence at the bottom is exactly what a buyer wants. The example boxes are unlocked, so it can be overwritten by accident. |
| Calculator | 3/5 | Good order (how often, what an hour costs, waste, totals, payback, sentence). Lets down a waste-only or sales-only user, and typing "25%" silently makes lost margin 100 times too small. Hints are 8pt and off-screen on a phone. |
| Improvement Log | 2/5 | The idea is the best bit for getting noticed, but it only works if everything lives in one file, the input rows are plain white (not the cream the legend says to type in), the totals are not protected, and it prints across four sheets of paper. |
| Etsy listing | not scored | listing.md says "NOT WRITTEN YET". Buyer 3 (deciding in ten seconds) has nothing to read. |

## Test cases typed in (copies only)

1. Warehouse, scanner batteries dying mid pick: 3 a shift down to 0.5, 10 minutes, 1 person, 10 shifts a week, 50 weeks, £12.21 an hour, fix £180 (spare batteries). Result: 208 hours and £2,544 a year saved, pays back in 4 weeks. Sensible, and the sentence reads well.
2. Retail bakery over-ordering, waste only: 30 to 12 units a week at £1.20, lost sales £200 to £50 a week, margin typed as 25% (stored as 0.25). Result: £1,143 a year saving, but the sentence box still says "Fill in the cream boxes and your sentence appears here." Lost margin came out at £19.50 a year instead of about £1,950.
3. Filler nozzle drips, fix removes it completely (AFTER = 0), downtime £900 an hour, fix cost blank. Result: £120,380 a year, "Straight away". Maths is right, but £117,000 of it is downtime cost on top of staff cost, which will look inflated to a manager.

## Issues, worst first

### 1. The running total in the Improvement Log falls apart if the buyer follows the instructions
- Where: Start Here C15 ("Save a copy of the file for each new problem") against Improvement Log B2 and Start Here C12 ("Log every result on the Improvement Log tab so you have a running total").
- Problem: if you save a new copy of the file for every problem, each copy has its own Improvement Log with one row in it. There is never a running total. A novice will not spot this until month three.
- Who: 4 (Excel novice), 1 (operator on a phone, who will not juggle several files).
- Fix: change Start Here C15 to: "Calculator: your own calculation. When you have finished one, type the result into the Improvement Log, then clear the cream boxes and start the next problem. Keep this one file as your master." Better still, add tabs "Calculator 2" to "Calculator 5" so the last few problems stay on file, and say so on Start Here.

### 2. Waste-only or sales-only problems never get their sentence
- Where: Calculator B44 (and Example B44). The formula only writes the sentence when C13 (times per shift) has a number.
- Problem: a retail or food buyer costing waste or lost sales fills in section 3 only, sees a real saving in E36, then sees "Fill in the cream boxes and your sentence appears here." That reads as "you did it wrong". Tested: £1,143 a year saving with no sentence.
- Who: 4 (Excel novice), and retail and food buyers generally.
- Fix: if C13 is blank but E36 is above zero, write: "I cut the cost of [problem] by about £[E36] a year (waste down from [C24] to [D24] a week)." The "Fill in" text should only show when E36 is zero.

### 3. Typing "25%" in the margin box makes lost margin 100 times too small, with no warning
- Where: Calculator C27 and D27 ("Margin on those sales (%)"), formulas C35 and D35 divide by 100.
- Problem: Excel turns "25%" into 0.25, the formula divides again, and lost margin shrinks from about £2,600 to £26. The box then shows "0.3", which looks like a rounding quirk, not a mistake. Excel novices type the % sign.
- Who: 4 (Excel novice), retail buyers.
- Fix: change C35 and D35 to treat anything under 1 as already a percentage: replace `N(C27)/100` with `IF(N(C27)<1,N(C27),N(C27)/100)`, and format C27 as `0"%"` so 25 shows as "25%". Keep the hint "Type 25 for 25%."

### 4. Help text is 8pt and sits off the right edge on a phone
- Where: Calculator and Example column F (F10, F13 to F17, F20, F21, F24, F26, F27, F31, F39), Example F6, Improvement Log I9, copyright lines B29, B48.
- Problem: 8pt is under the 9pt minimum. Column F starts after about 90 characters of width, so on Excel mobile the hints are a sideways scroll away and nobody sees them. The hint is exactly where "Count it for a week" and "Use your own hourly rate" live.
- Who: 1 (operator on a phone).
- Fix: raise all hint text to 9pt. Add a cell comment or data validation input message to each cream box with the same hint (Excel mobile and Google Sheets show these when the box is tapped). Example for C14: "From the moment it goes wrong to running normally again."

### 5. Improvement Log rows are white, not cream, and the totals can be typed over
- Where: Improvement Log B10:H58 (no fill), E5, E6, F5 (formulas). The sheet is not protected.
- Problem: the legend on Start Here says cream with blue text means "type here". Below the example row everything is white, so a novice is not sure where to type. The running total formulas are unlocked, so pasting a row in the wrong place wipes the headline number. Start Here C22 says "The formulas are locked", which is not true on this tab.
- Who: 4 (Excel novice).
- Fix: fill B9:H58 cream (#f3efe4), unlock those cells only, and protect the sheet with no password, same as Calculator. Start Here C22 then stays true.

### 6. Downtime and staff cost are added together, which can look padded
- Where: Calculator rows 32 and 33, total C36. Test 3 gave £120,380 a year, with £117,000 of it from downtime.
- Problem: many sites' "cost of an hour of downtime" already includes the people. A manager who sees both added together may dismiss the whole number, which kills the point of the tool.
- Who: 3 (buyer who wants to be taken seriously), 4.
- Fix: change the hint in F21 to: "Only if the problem stops a line. If this figure already includes labour, leave Staff cost per hour blank so nothing is counted twice."

### 7. Improvement Log prints across four pages
- Where: Improvement Log print setup (fit to page is off). Rendered: columns B to D on one sheet, E to H on another, the note in I on a third and fourth.
- Problem: the supervisor who prints the log for a review or a team board gets four half-empty sheets.
- Who: 2 (supervisor printing).
- Fix: turn on Fit to page (1 page wide, any height), landscape, set print area B1:H58, and move the "Example row. Overwrite it." note into column H's comment instead of column I.

### 8. The worked example can be overwritten
- Where: Example C6:C10, C13:D17, C20, C21, C24:D27, C39 are unlocked.
- Problem: the novice clicks into the example first (it is the second tab), types their own numbers, and loses the "what good looks like" reference.
- Who: 4.
- Fix: lock all cells on the Example tab. F6 already says "Use the Calculator tab for your own."

### 9. "Main impact" dropdown has no way out and does nothing
- Where: Calculator C10 and Example C10. Options: Downtime, Labour time, Waste, Lost sales, Safety, Quality, More than one.
- Problem: no "Other" (energy, customer complaints, rework, overtime). The choice does not change anything, so the buyer may wonder if they picked wrong.
- Who: 1, 4.
- Fix: add "Rework", "Overtime" and "Other" to the list, and change F10 to "Pick from the list. This is just a label for your log; it does not change the maths."

### 10. Google Sheets loses the protection
- Where: Start Here C22.
- Problem: Excel sheet protection does not carry over when the file is imported into Google Sheets, so "The formulas are locked" is not true there. Everything else (N, TEXT, the dropdowns) imported fine in principle.
- Who: 4 (novice using Google Sheets because they have no Excel).
- Fix: change C22 to: "Works in Microsoft Excel (including the phone app), Google Sheets (File > Import) and Apple Numbers. In Excel the formulas are locked. In Google Sheets they are not, so only type in the cream boxes."

### 11. No Etsy listing yet
- Where: products/kpi-calculator/listing.md.
- Problem: buyer 3 has nothing to judge. Cannot test title, first photo or first two lines.
- Who: 3.
- Fix: listing-optimiser to write it. Suggested first line to test: "Put a pound sign on any problem in two minutes. Turn 'the labeller keeps jamming' into '£4,290 a year, fixed for £25'." Say clearly in the first two lines that it is an Excel file that also works in Google Sheets.

### 12. No back page linking the rest of the range
- Where: whole workbook.
- Problem: the house rule says every product has a back page linking the rest of the range. There is no "More from Kaizen XP" tab.
- Who: 3 (a happy buyer who would buy the next tool).
- Fix: add a final tab "More from Kaizen XP" listing the Visibility Kit, CI Starter Kit, RCFA Template, MTBA Assist Tracker and Breakdown Analysis Dashboard, one line each on what it is for.

## Quick wins (under five minutes each)

- Raise every 8pt hint and the copyright lines to 9pt.
- Rewrite Start Here C15 and C22 as written above.
- Rewrite the F21 hint about double counting.
- Add "Other" to the Main impact dropdown.
- Turn on Fit to page for the Improvement Log.
- Lock the Example tab.

## What works

- The sentence at the bottom ("I reduced ... worth roughly £4,290 a year, for a fix that cost £25") is the product. It turns maths into something a frontline worker can paste into an email. Keep it front and centre.
- BEFORE / AFTER THE FIX side by side, with AFTER falling back to BEFORE when left blank, means a novice cannot get a silly answer by skipping a box. Tested with a fix that removes the problem completely (AFTER = 0) and it handled it correctly.
