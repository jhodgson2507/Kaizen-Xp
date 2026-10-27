PASS

# Product QA: The RCFA Template
File: products/rcfa-template/Kaizen_XP_RCFA_Template.pdf
Checked: 2026-10-27 by product-qa

## What was checked
- 9 pages, A4. All 9 pages rendered with pdftoppm and looked at one by one.
- Text pulled with pdftotext: no em dashes or en dashes, no placeholder text, no spelling typos found.
- Motto on every page (9 times). Copyright line on the back page.
- Back page (page 9) lists the rest of the range: Visibility Kit, Frontline CI Starter Kit, MTBA Assist Tracker, KPI Impact Calculator, Breakdown Analysis Dashboard.
- All 8 steps promised on the cover and page 2 are there (pages 4 to 8), in order.
- 212 form fields, all names unique: 154 text, 58 dropdowns. Every write-in box on pages 4 to 8 has a field. Large boxes are multi-line.
- Filled all 212 fields with pypdf, saved a copy, re-read: 212 of 212 values held and show on the rendered copy.
- Dropdown options make sense for each step (status, evidence source, 6M category, proven yes or no, how it was locked in).
- Worked example maths (page 3): 4 jams x 6 mins x 15 shifts = 360 mins = 6 hours a week. Correct.
- Nothing runs into the footer or off the page. Tables fit. Black and gold style consistent.

## Listing match
listing.md says "Status: NOT WRITTEN YET". No promises to check. When the listing is written it must come back through product-qa. Safe facts: 9 pages, 8 steps, one-page worked example, fillable on screen, printable on paper, 23-row timeline, 17-row cause check.

## Problems (none block sale)

### 1. Downtime units differ between the worked example and the form (minor)
- Page 4, Step 2 "Downtime" box says "minutes a week". Page 3 worked example gives "6 hours downtime a week".
- Fix: in build.py change the Step 2 hint to "minutes or hours a week", or change the worked example to "360 minutes (6 hours) downtime a week".

### 2. No actual link to the shop (minor, all four PDFs)
- Page 9. "All available from Kaizen XP." has no shop name to search or clickable link.
- Fix: once Josh confirms the Etsy shop URL, add it in kitlib.back() as text and a link. Do not invent a URL.

## Verdict
PASS. Ready for usability-checker. The listing still needs writing and its own QA before Josh lists it.
