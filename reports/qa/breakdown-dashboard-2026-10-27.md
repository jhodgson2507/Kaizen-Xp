FAIL

# Product QA: The Breakdown Analysis Dashboard

File: products/breakdown-dashboard/Kaizen_XP_Breakdown_Analysis_Dashboard.xlsx
Checked: 2026-10-27 by product-qa, on copies only. Nothing in products/ was changed.

## What passed

- Recalculated in LibreOffice headless: 333 formulas, 0 errors. Also 0 errors with the sample log fully cleared.
- The repo file matches what build.py produces today (0 cell differences).
- Sample data (132 breakdowns, 1 Apr to 30 Sep 2026) recomputed from the log in pandas:
  - Planned run hours 183 days / 7 x 5 x 21 = 2,745. Sheet: 2,745.
  - Breakdowns 132, hours down 74.3, MTBF 20.2 h, MTTR 34 min, availability 97.3%, downtime cost £18,579, root cause found 35%. All seven tiles match.
  - Machine Pareto (Labeller 1,487 min, 31 breakdowns, 33% then Filler, Case packer, Palletiser...), failure type Pareto (Mechanical 31% first), monthly hours and shift counts all match.
- Fresh test typed into a copy: Setup renamed to "Pack line 2", 1 to 31 Aug 2026, 16 h/day, 5 days, £100/h, machines Bagger and Weigher, 4 breakdowns inside the period and one 600 minute breakdown on 1 Sep outside it. Worked out in Python: 4 breakdowns, 3.0 h, MTBF 87.8 h, MTTR 45 min, availability 99.2%, £300, root cause 50%, Bagger 67%, Electrical top failure type at 50%. The sheet matched exactly and correctly ignored the 1 Sep row.
- Dashboard and Workings are protected with every formula locked. Setup inputs are cream with blue text.
- No em dashes in the file or build script. Motto and copyright on Start Here, copyright on Dashboard. Arial throughout.
- Dashboard renders on one landscape page; tiles, FIX FIRST line, four charts and the worst machines table all readable.

## Problems (must fix before listing)

1. Breakdown Log, B7:J506: all 4,500 input cells have blue text but no cream fill. This is the main input sheet and it breaks the "cream boxes with blue text" rule that Start Here and the legend teach.
   Fix in build.py, LOG loop: add `c.fill = fill(CREAM)` and `c.protection = Protection(locked=False)` for every cell in rows 7 to 506, columns B to J.

2. Setup, C12 (Planned run hours in this period): formula is not protected because the Setup sheet has no protection. One wrong keystroke here breaks MTBF and availability.
   Fix: add `su.protection.sheet = True` (with formatCells/formatColumns/formatRows = False). Setup inputs are already unlocked, so only C12 becomes locked. Also update Start Here C21 to say Setup totals are locked too.

3. Dashboard, E49:L51 (worst machines table): when fewer than 5 machines are in the period, the empty rows show "0", "0.0" and "0%" with no machine name (seen in the fresh test with 2 machines). Looks broken.
   Fix: wrap the BREAKDOWNS, HOURS DOWN and SHARE formulas for rows 47 to 51 in `IF(Workings!H{w}="","",...)`, and the COST formula the same way.

4. Workings D40:D51 and Dashboard chart "Hours down by month": always plots 12 months from the period start, even when the period is shorter. With the sample period (6 months) Oct 26 to Mar 27 show as empty bars. With a one month period, 11 of 12 bars are empty and the labels run to Jul 27. On a "is it getting better?" chart, empty future months read as zero breakdowns.
   Fix: in Workings, set B41:B51 to `=IF(EDATE(B40,1)>Setup!$C$8,"",EDATE(B40,1))` (chained), and make C, D and E return `NA()` / "" when B is blank, so the chart only shows months inside the period.

5. Start Here, C14 (MTBF definition): says "run hours divided by breakdowns". Workings C59 actually uses (planned run hours minus downtime hours) divided by breakdowns. A technician who checks it by hand will get a different number (2,745 / 132 = 20.8, sheet shows 20.2).
   Fix: change the text to "MTBF (Mean Time Between Failures): running hours (planned run hours minus downtime) divided by breakdowns. Higher is better."

6. Dashboard charts "Downtime by machine" and "Downtime by failure type" (data from Workings rows 7 to 16): Setup allows up to 15 machines (Setup B15:B29) but the machine Pareto only charts the top 10. Machines 11 to 15 never appear on the chart.
   Fix: either extend the chart references in build.py to Workings rows 7 to 21, or change the Setup header B14 to "MACHINES (UP TO 15, TOP 10 CHARTED)".

7. Whole workbook: no page or tab linking the rest of the Kaizen XP range. CLAUDE.md says every product has "a back page linking the rest of the range". Only the MTBA Assist Tracker (Start Here C19) and RCFA Template (Dashboard B45) are mentioned in passing.
   Fix: add a final tab "More from Kaizen XP" (or a block at the bottom of Start Here) listing the full range, with the motto and copyright line.

8. Breakdown Log, Setup and Workings: no print setup. The PDF render runs to 19 pages: Breakdown Log alone is 12 pages split across the width, Setup splits the failure type list onto a second page. "Printable on paper" is a house rule.
   Fix: for log, su and wk set `page_setup.orientation = 'landscape'`, `fitToWidth = 1`, `fitToHeight = 0`, `fitToPage = True`; repeat log header row 6 with `log.print_title_rows = '6:6'`.

## Smaller points (fix if cheap)

9. Machine Pareto x axis: unused machine slots plot as empty categories, so with 2 machines the labels squash together ("BaggerWeigher" in the render) and the running total line runs flat across blank slots.
   Fix: return `NA()` instead of 0 in Workings I7:L21 and I26:L35 when H is blank, so charts skip empty slots.

10. Breakdown Log, Setup, Workings: no copyright line. Fix: add the copyright line under each sheet's last used row.

11. Start Here, C21 (Works in): says formulas are locked in Apple Numbers. Numbers does not keep Excel sheet protection.
    Fix: reword to "Formulas are locked in Excel and Google Sheets."

12. Machines renamed on Setup after breakdowns are logged drop out of the Pareto but still count in the tiles, so shares no longer add up to 100%.
    Fix: add a note at Setup F19: "Rename a machine here and in the log at the same time, or old lines drop out of the charts."

## Listing match

products/breakdown-dashboard/listing.md says "Status: NOT WRITTEN YET" (price "about £12.99"). There are no listing promises to check yet. This product cannot be listed until the listing exists and is checked against this file.

## Evidence

Scratch copies, recalculated files, test files and renders are in
/tmp/claude-0/-home-user-Kaizen-Xp/b17d22de-2ac1-57c1-a9a9-a5a5d4cbe0e7/scratchpad/qa-xlsx/
