# Usability check: The Breakdown Analysis Dashboard (2026-10-27)

**Verdict: Not ready.** The dashboard looks the part and the sums are right, but a buyer who deletes the sample and starts logging this week gets a blank dashboard with no clue why, typos and odd dates are dropped without a word, and the Etsy listing has not been written. Three fixes (issues 1 to 3) move it to Ready with fixes.

File checked: products/breakdown-dashboard/Kaizen_XP_Breakdown_Analysis_Dashboard.xlsx (and listing.md).
How: every tab read in order with openpyxl (values, fonts, lock state, dropdowns, chart ranges), the file rendered through LibreOffice to PDF and PNG (19 pages) and looked at, and three fresh test cases typed into copies and recalculated (scratch copies only, repo files untouched).

## Scores by tab

| Tab | Score | Why |
| --- | --- | --- |
| Start Here | 4/5 | Plain steps, MTBF and MTTR spelled out, and the breakdown vs assist note is the kind of thing only someone who has worked the shift would write. Loses a point because "RCFA" and "5 Whys" are not explained. |
| Dashboard | 3/5 | Strong at a glance: seven tiles, a FIX FIRST line in plain English, two Paretos with running totals. Let down by the empty-state message, a month chart that shows future months as zero, and 8pt tile labels. |
| Breakdown Log | 2/5 | This is where the buyer spends all their time and it is the weakest tab: no cream boxes, dropdowns that accept typos, dates that can be silently ignored, and it prints across 12 pages. |
| Setup | 3/5 | Short and clear, but sample dates that ended last month, renaming a machine quietly orphans its old rows, and it prints on two pages. |
| Workings | 4/5 | Locked, labelled "Nothing to type here". Fine for a curious buyer. |
| Etsy listing | not scored | listing.md says "NOT WRITTEN YET". Buyer 3 has nothing to read. |

## Test cases typed in (copies only)

1. Crisps bagging line, October 2026: cleared the sample, set Setup to Line 6, 1 to 31 Oct 2026, 22 hours a day, 5 days, £180 an hour, five machines (Bagger, Checkweigher, Metal detector, Case erector, Conveyors). Logged six breakdowns, one with the date typed as text "21/10/2026". Result: Dashboard shows 5 breakdowns, not 6. 4.9 hours down, MTBF 96.4 hours, MTTR 59 minutes, availability 99.0%, £885. FIX FIRST: Bagger (47%). The numbers are right for the five it counted. The sixth vanished with no warning. Month chart shows Oct 26 then eleven empty months to Sep 27.
2. Same six breakdowns, but Setup dates left on the sample (1 Apr to 30 Sep 2026), which is what happens if step 3 is skipped or done later. Result: every tile zero, availability 100%, and the FIX FIRST box says "Log your first breakdown and the machine to fix first shows here", even though six are logged.
3. Sample deleted, nothing else changed: same message, which is correct.

## Issues, worst first

### 1. Breakdowns outside the Setup dates vanish and the dashboard says "Log your first breakdown"
- Where: Setup C7 and C8 (sample period 1 Apr 2026 to 30 Sep 2026, already in the past), Dashboard B10 message, Workings C56.
- Problem: a buyer who opens it today, deletes the sample and logs this week's breakdowns sees zeros everywhere and a message telling them to do what they have just done. They will think it is broken. Same thing next month when the period runs out.
- Who: 4 (Excel novice), 1 (operator on a phone who skips Setup).
- Fix: (a) make Dashboard B10 check for this: if the log has entries but none in the period, show "You have [n] breakdowns logged, but none between [start] and [end]. Change the dates on the Setup tab." (b) Add a line in Setup D7: "Leave the end date blank to include everything up to today", and make the formulas treat a blank end date as TODAY(). (c) Start Here step 2 should say "then go straight to Setup and change the dates" so the two steps are not separated.

### 2. Dropdowns accept anything typed, and anything that does not match is dropped
- Where: Breakdown Log C7:C506, D7:D506, E7:E506, I7:I506, G7:G506. All five data validations have "show error" switched off, so Excel accepts any typing without complaint. The minutes rule already has a good error message ("Type the minutes as a whole number, for example 45.") that never shows.
- Problem: on a phone it is quicker to type "labeler" or "Labeller " than to open a dropdown. That row then counts in the total but not on the machine chart or the FIX FIRST line, so the shares do not add up. "45 mins" in MINUTES DOWN counts as a breakdown with zero minutes.
- Who: 1 (operator on a phone), 4.
- Fix: switch on the error alert for all five validations (style: Stop) with these messages. Machine: "Pick a machine from the list. To add one, type it on the Setup tab first." Failure type: "Pick from the list. Use Other if nothing fits." Shift: "Pick a shift from the list." Minutes: keep the existing message. Root cause: "Pick Yes, No or In progress."

### 3. Dates typed in the wrong format are silently ignored
- Where: Breakdown Log B7:B506 (no validation). Tested with a date stored as text: dropped from every count.
- Problem: on a phone, or in Google Sheets set to US format, "21/10/2026", "21.10.26" or "21st Oct" stays as text and is never counted.
- Who: 1, 4, and anyone using Google Sheets.
- Fix: add a date validation on B7:B506 (between 1 Jan 2024 and 31 Dec 2035, error style Stop) with the message "Type the date like 21/10/26, or press Ctrl and ; for today." Also add a check column K headed "COUNTED?" that shows "Yes", "Not a date", or "Outside Setup dates", so a buyer can see why a row is missing.

### 4. The log has no cream boxes, so the legend does not match
- Where: Breakdown Log B7:J506 (white, blue text). Start Here C23 legend: cream with blue text means "Type here".
- Problem: the one tab where the buyer types the most is the only one that does not follow the colour rule. The novice is not sure if typing in the white rows is allowed.
- Who: 4.
- Fix: fill B7:J506 cream (#f3efe4) with a thin gold border, the same as the Setup boxes. Optionally protect the header rows 1 to 6 with no password so the column titles cannot be typed over.

### 5. Month chart shows future months as zero, which looks like "it got better"
- Where: Dashboard chart "Hours down by month (is it getting better?)", fed by Workings B40:D51 (always 12 months from the start date).
- Problem: with a one-month or one-quarter period, the chart shows months that have not happened as zero bars. Tested: October then eleven empty months to Sep 27. A supervisor glancing at it will read the drop as an improvement.
- Who: 2 (supervisor reviewing), 3.
- Fix: in Workings C40:D51 return NA() for any month that starts after Setup C8 (or after today), and set the chart to show #N/A as a gap. Label E40:E51 as "" for those months.

### 6. Renaming a machine on Setup orphans its old breakdowns
- Where: Setup B15:B29, note in F15 ("Rename them to match your site").
- Problem: if "Labeller" is renamed to "Labeller 2" after logging, every old Labeller row stops counting on the machine chart and table. Nothing warns you.
- Who: 4.
- Fix: change F15 to: "These lists feed the dropdowns and charts. Set them up before you start logging. If you rename one later, change the old rows in the Breakdown Log too (Ctrl+H, Replace)."

### 7. Breakdown Log prints across 12 pages and Setup across 2
- Where: print setup for Breakdown Log and Setup (Fit to page off, portrait). Rendered: the log splits DATE to FAILURE TYPE on one set of pages, WHAT HAPPENED and the rest on others.
- Problem: a supervisor who wants a paper log on the line clipboard, which is how most breakdowns are first written down, cannot get one.
- Who: 2 (supervisor printing).
- Fix: Breakdown Log: landscape, Fit to 1 page wide, repeat rows 6 at the top of each page, print area B1:J506. Setup: Fit to 1 page. Consider adding a "Printable log sheet" tab: 25 blank rows, landscape, 9mm row height for biro writing, same columns.

### 8. Tile labels and help text are under 9pt
- Where: Dashboard B5:N5 tile headings and B46:M46 table headings (8pt gold on black), Setup D7, D8, D9, D11, F15 (8pt), copyright lines on every tab (8pt).
- Problem: gold 8pt on black is hard to read on a phone and on a cheap printer.
- Who: 1, 2.
- Fix: raise all to 9pt minimum; tile headings to 10pt.

### 9. Jargon on the dashboard itself with no explanation there
- Where: Dashboard F5 "MTBF (HOURS)", H5 "MTTR (MINS)", N5 "ROOT CAUSE FOUND", B45 "5 Whys or the Kaizen XP RCFA Template", Breakdown Log J6 "RCFA REF".
- Problem: the explanation is only on Start Here. An operator who goes straight to the Dashboard has never heard of MTBF.
- Who: 1 (night-shift operator who has never heard of MTBF or RCFA).
- Fix: put a plain line under the tiles in row 8: "MTBF = average hours running between breakdowns (higher is better). MTTR = average minutes to fix (lower is better). Root cause found = share of breakdowns marked Yes." Rename J6 to "RCFA REF (root cause report number)". Add to Start Here THE NUMBERS: "RCFA (Root Cause Failure Analysis): a step by step look at why a breakdown really happened, so it does not come back."

### 10. MTBF explanation does not match the maths
- Where: Start Here C14 says "run hours divided by breakdowns". Workings C59 takes off the hours lost first: (run hours minus hours down) divided by breakdowns.
- Problem: a buyer who checks by hand gets a different number and stops trusting the rest.
- Who: 4.
- Fix: change C14 to "MTBF (Mean Time Between Failures): hours the line actually ran, divided by the number of breakdowns. Higher is better."

### 11. Shift dropdown overlaps and has no way out
- Where: Breakdown Log C7:C506. Options: Days, Earlies, Lates, Nights, Weekend.
- Problem: "Days" and "Earlies/Lates" are two different shift patterns mixed together, and "Weekend" overlaps with all of them. No "Other" for 4 on 4 off, 12-hour or split shifts. Sites will name shifts A, B, C, D.
- Who: 1, 2.
- Fix: move the shift list onto Setup (cells H15:H20, "SHIFTS (UP TO 6)") so each site types its own (A shift, B shift, Days, Nights), point the dropdown and the shift chart at it, and add "Other" to the default list.

### 12. Machine list has no "Other", and the chart shows only 10 of the 15
- Where: Setup B15:B29 (no Other), Dashboard machine chart uses Workings J7:J16 (top 10), table shows top 5.
- Problem: a breakdown on a machine not yet listed has nowhere to go. A site with 12 to 15 machines loses the smallest ones from the chart without being told.
- Who: 1, 4.
- Fix: put "Other" in the last machine slot (B29) and say on Setup "Machines (up to 14, plus Other)". Change the chart title to "Downtime by machine, worst 10 (hrs)".

### 13. Deleting the sample is fiddly on a phone
- Where: Start Here C9, Breakdown Log B4 ("select them, press Delete").
- Problem: 132 sample rows. On Excel mobile, selecting B7:J138 is awkward and easy to get wrong (half a row left behind, or the header deleted).
- Who: 1, 4.
- Fix: change B4 to "Click cell B7, hold Shift and click J138, then press Delete. On a phone, do this on a computer first if you can." Better: ship two files in the download, "with sample data" and "blank, ready to use".

### 14. Charts use Calibri, not Arial
- Where: all four Dashboard charts (titles and axis text set to Calibri, 18pt titles).
- Problem: brand says Arial in Excel. The chart titles are also much bigger than anything else on the page.
- Who: 3 (first impression from screenshots).
- Fix: set chart fonts to Arial, titles 11pt bold, axis labels 9pt.

### 15. Google Sheets and phone notes
- Where: Start Here C21.
- Problem: protection does not carry over into Google Sheets, so "locked so formulas cannot be broken" is not true there. The combined bar and running total line charts may lose the line or the second axis after import. On Excel mobile the Dashboard needs pinch and zoom (15 columns plus charts).
- Who: 1, 4.
- Fix: change C21 to: "Works best in Microsoft Excel (computer or phone app). Also opens in Google Sheets (File > Import) and Apple Numbers, but the charts may look different and the formulas are not locked there, so only type in the cream boxes. On a phone, log breakdowns on your phone and look at the Dashboard on a bigger screen."

### 16. No Etsy listing yet, and no back page
- Where: products/breakdown-dashboard/listing.md ("NOT WRITTEN YET"); no "More from Kaizen XP" tab in the workbook.
- Problem: buyer 3 has nothing to judge. The house rule asks for a back page linking the rest of the range.
- Who: 3.
- Fix: listing-optimiser to write the listing. Lead with the FIX FIRST line, for example: "Log every breakdown. The dashboard tells you which machine to fix first." Say in the first two lines that it is an Excel file with sample data so you can see it working. Add a final tab "More from Kaizen XP" with one line for each product, and point the MTBA Assist Tracker and RCFA Template mentions to it.

## Quick wins (under five minutes each)

- Switch on the error alert on all five Breakdown Log dropdowns and the minutes rule.
- Fit to page for Breakdown Log and Setup.
- Raise every 8pt label to 9pt.
- Rewrite Start Here C14 (MTBF) and C21 (Works in).
- Change Setup F15 warning about renaming.
- Add "Other" to the shift list and the last machine slot.
- Fill the log rows cream.

## What works

- The FIX FIRST line ("Bagger. It caused 47% of all downtime...") is the best thing in the file. It answers the only question a line leader actually asks. Keep it and keep it in plain English.
- Shipping with six months of believable sample data, so the buyer sees a full dashboard on first open, sells the product. The sample breakdowns ("Drive chain off sprocket", "Label reel splice failed") read like a real shift.
