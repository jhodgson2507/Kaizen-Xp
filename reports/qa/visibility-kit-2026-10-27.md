FAIL

# Product QA: The Visibility Kit
File: products/visibility-kit/Kaizen_XP_The_Visibility_Kit_v2.pdf
Checked: 2026-10-27 by product-qa

## What was checked
- 14 pages, A4. All 14 pages rendered with pdftoppm and looked at one by one.
- Text pulled with pdftotext: no em dashes or en dashes, no placeholder text, no typos found.
- Motto on every page (14 times). Copyright line on the back page.
- 461 form fields, all names unique. Every write-in box on pages 3 to 13 has a field.
- Filled all 343 text fields and 118 dropdowns with pypdf, saved a copy to the scratch folder, re-read it: 461 of 461 values held, and every value shows on the rendered filled copy.
- Maths on page 12 checked by hand: (4 - 1) x 6 x 15 = 270 mins a week, 270 / 60 x 52 = 234 hrs, 234 x £13 = £3,042. Quick check table (10 cells) all correct.
- Nothing runs into the footer or off the page. Tables fit their columns. Black and gold style consistent.

## Listing match
listing.md says "Status: NOT WRITTEN YET". There are no promises to check. When the listing is written it must come back through product-qa before Josh publishes. Facts the listing can safely use: 14 pages, 6 tools plus a Put a Number On It page, fillable on screen, printable on paper, worked examples, 13-week tracker.

## Problems

### 1. Back page does not list the rest of the range (BLOCKER)
- Page 14. The back page only lists The Frontline CI Starter Kit. CLAUDE.md says every product has a back page linking the rest of the range. The RCFA Template, The MTBA Assist Tracker, The KPI Impact Calculator and The Breakdown Analysis Dashboard are missing. The other three PDFs already do this properly.
- Fix: in products/visibility-kit/build.py, replace the hand-built back page block (from "# BACK PAGE", around line 715) with the shared kitlib.back() call used by ci-starter-kit/build.py line 171, listing the CI Starter Kit, RCFA Template, MTBA Assist Tracker, KPI Impact Calculator and Breakdown Analysis Dashboard. Keep the closer line "Every fix you make with it goes straight into Tool 5 of this kit." and "All available from Kaizen XP." Rebuild and re-run QA.

### 2. No actual link to the shop (minor, all four PDFs)
- Page 14. "Available from Kaizen XP." has no shop name to search and no clickable link.
- Fix: once Josh confirms the Etsy shop URL, add it as text under "Available from Kaizen XP." and as a link annotation in kitlib.back(). Do not invent a URL.

### 3. "Sent?" options do not match between pages (minor)
- Page 3 dropdown offers Sent / Sent late / Not yet. Page 4 tracker offers Sent / Sent late / Missed.
- Fix: build.py line 457, change 'Not yet' to 'Missed' (or the other way round on page 4) so both match.

### 4. "Tick off every Friday" but there is no tick box (minor)
- Page 4, 13-week streak note. The Sent? column is a dropdown, not a tick.
- Fix: change the note to "Fill it in every Friday. Missed one? Send it Monday and keep going."

### 5. Unlabelled box next to "The next step I am aiming for" (minor)
- Page 13. The text box to the right of the dropdown has no label, so it is not clear what goes in it.
- Fix: add a small label such as "DETAILS" before the box, or a hint "(role, course or area)".

### 6. Courier font in the email template (note only)
- Page 3, The Template box uses Courier. Brand says Helvetica in PDFs. It reads as an email on purpose, so Josh can keep it, but if strict brand is wanted change 'Courier' to 'Helvetica' at build.py line 447.

## Verdict
FAIL on problem 1 only. Fix the back page, rebuild, and it should pass. Problems 2 to 6 can go in the same rebuild.
