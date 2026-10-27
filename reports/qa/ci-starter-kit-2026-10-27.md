FAIL

# Product QA: The Frontline CI Starter Kit
File: products/ci-starter-kit/Kaizen_XP_Frontline_CI_Starter_Kit_v2.pdf
Checked: 2026-10-27 by product-qa

## What was checked
- 10 pages, A4. All 10 pages rendered with pdftoppm and looked at one by one.
- Text pulled with pdftotext: no em dashes or en dashes, no placeholder text, no spelling typos found.
- Motto on every page (10 times). Copyright line on the back page.
- Back page (page 10) lists the rest of the range: Visibility Kit, RCFA Template, MTBA Assist Tracker, KPI Impact Calculator, Breakdown Analysis Dashboard.
- 327 form fields, all names unique: 234 text, 62 dropdowns, 31 tick boxes. Every write-in box on pages 3, 4 and 6 to 9 has a field.
- Filled all text fields and dropdowns with pypdf, saved a copy, re-read: all values held and show on the rendered copy. Ticked all 31 Daily CI Habit boxes in a second copy: all read back as /Yes.
- Worked examples present: 5 Whys (page 5) and the first row of the Quick Wins Tracker (page 6).
- Nothing runs into the footer or off the page. Tables fit. Black and gold style consistent.

## Listing match
listing.md says "Status: NOT WRITTEN YET". No promises to check. When the listing is written it must come back through product-qa. Safe facts: 10 pages, 5 tools, fillable on screen, printable on paper, worked 5 Whys example, 31-day habit tracker, 57 Quick Wins rows.

## Problems

### 1. Wrong count in the 5 Whys worked example (BLOCKER: a factual error a buyer will spot)
- Page 5, "Why it works" box: "Three more whys found a fix". After the first answer there are four more whys (2, 3, 4 and 5) on the page.
- Fix: products/ci-starter-kit/build.py line 114, change "Three more whys" to "Four more whys". Rebuild.

### 2. Tick boxes are flagged as required (minor)
- Page 9, all 31 "Done" tick boxes (d_done1 to d_done31) carry the Required flag. Acrobat can warn that the form is incomplete if a buyer prints or saves with days left blank.
- Fix: in kitlib.py checkbox() (line 459), add fieldFlags='' to the acroForm.checkbox call. This also affects any later product that uses tick boxes.

### 3. Handover log says "in person" but offers phone and written (minor)
- Page 3. Subtitle says "Hand it over in person", the HOW dropdown offers Written only and By phone.
- Fix: either change the subtitle to "Hand it over in person if you can" or leave as is. Josh's call.

### 4. No actual link to the shop (minor, all four PDFs)
- Page 10. "All available from Kaizen XP." has no shop name to search or clickable link.
- Fix: once Josh confirms the Etsy shop URL, add it in kitlib.back() as text and a link. Do not invent a URL.

## Verdict
FAIL on problem 1 only. One word to change, then rebuild and it should pass.
