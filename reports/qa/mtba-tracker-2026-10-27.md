FAIL

# Product QA: The MTBA Assist Tracker
File: products/mtba-tracker/Kaizen_XP_MTBA_Assist_Tracker.pdf
Checked: 2026-10-27 by product-qa

## What was checked
- 8 pages, A4. All 8 pages rendered with pdftoppm and looked at one by one.
- Text pulled with pdftotext: no em dashes or en dashes, no placeholder text, no spelling typos found.
- Motto on every page (8 times). Copyright line on the back page.
- Back page (page 8) lists the rest of the range: Visibility Kit, Frontline CI Starter Kit, RCFA Template, KPI Impact Calculator, Breakdown Analysis Dashboard.
- 337 form fields, all names unique: 270 text, 67 dropdowns. Every write-in box on pages 3, 4, 6 and 7 has a field.
- Filled all 337 fields with pypdf, saved a copy, re-read: 337 of 337 values held and show on the rendered copy.
- Page 2 formula example: 480 / 12 = 40, 480 / 4 = 120, three times longer. Correct.
- Page 5 worked example: counts add to 108, minutes add to 508, 6,750 / 108 = 62.5 (shown as 62), 6,750 / 57 = 118, 508 - 232 = 276 mins = 4.6 hours, jams 54% of assists and 68% of minutes. All correct apart from the rank below.
- Nothing runs into the footer or off the page. Tables fit. Black and gold style consistent.

## Listing match
listing.md says "Status: NOT WRITTEN YET". No promises to check. When the listing is written it must come back through product-qa. Safe facts: 8 pages, 2 shift log sheets (27 rows each, first sheet has a worked row), weekly summary, before and after page, worked example, fillable on screen, printable on paper.

## Problems

### 1. Rank in the worked example breaks the product's own rule (BLOCKER)
- Page 5, table. "Reset or restart" (28 mins) is ranked 3 and "Re-handle or re-work" (30 mins) is ranked 4. Page 6 says "The type with the most minutes lost is the one to kill first", so 30 mins must rank above 28.
- Fix: products/mtba-tracker/build.py lines 82 to 83, swap the two rows so the list reads Jam 348 (1), Misfeed 84 (2), Re-handle or re-work 30 (3), Reset or restart 28 (4), Manual adjustment 18 (5). Rebuild.

### 2. Rounding on page 5 (minor)
- Page 5, "MTBA = 6,750 / 108 = 62 minutes". The true answer is 62.5.
- Fix: write "= about 62 minutes" so a buyer checking with a calculator is not thrown.

### 3. One week needs more than two log sheets (minor)
- Page 2 step 1 says log every assist for one week, but there are two shift log sheets (pages 3 and 4). The "How to use this PDF" box does say to save a copy for each new sheet.
- Fix: add one line under step 1 on page 2: "Print or save a fresh log sheet for every shift."

### 4. No actual link to the shop (minor, all four PDFs)
- Page 8. "All available from Kaizen XP." has no shop name to search or clickable link.
- Fix: once Josh confirms the Etsy shop URL, add it in kitlib.back() as text and a link. Do not invent a URL.

## Verdict
FAIL on problem 1 only. Swap two rows, rebuild, and it should pass.
