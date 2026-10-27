# Usability check: The Visibility Kit (v2)

**Verdict: Ready with fixes.** The PDF is clear and useful, but the back page breaks the house rule (it only links one product), form labels are below 7pt, and on paper the dropdown choices are invisible. The Etsy listing has not been written yet (listing.md says "NOT WRITTEN YET"), so the product cannot be listed until that is done and checked.

Checked: products/visibility-kit/Kaizen_XP_The_Visibility_Kit_v2.pdf, all 14 pages rendered at 100 dpi and at 400 px wide (phone), fields read with pypdf, text sizes read with pdfplumber. products/visibility-kit/listing.md.

## Scores by page

| Page | What it is | Score | Why |
| --- | --- | --- | --- |
| 1 | Cover | 4/5 | Clear promise. Full black page eats toner when a supervisor prints a stack. |
| 2 | Read this first | 5/5 | Best opening in the range. Speaks to the night-shift worker in their own words. |
| 3 | Weekly Wins Email | 4/5 | Template plus three prompts is easy. Only one week of space; needs "save a copy each week". |
| 4 | Weekly Wins example and 13-week streak | 4/5 | Example reads like a real shift. "Sent?" options differ from page 3. |
| 5 | The CC Rule | 4/5 | Clear in/out lists. Uses "boss" where the rest of the kit says "line leader". |
| 6 | Coaching Log 1 (example plus 3 records) | 4/5 | Strong example. Typed "signature" on a phone is not a signature; no hint on that. |
| 7 | Coaching Log 2 (4 records) | 4/5 | Same layout, plenty of room. |
| 8 | Colleague Support Tracker | 4/5 | One line per entry, fast. Long entries vanish when printed (single-line cells). |
| 9 | Colleague Support Tracker continued | 4/5 | As above. |
| 10 | Improvement Contribution Log (example plus 2) | 3/5 | Write-in boxes only fit two handwritten lines while a third of the page is empty. Date box is tiny. Result hint misses "quality". |
| 11 | Improvement Log continued (4 records) | 3/5 | Same tight boxes, tiny date boxes. |
| 12 | Put a Number On It | 5/5 | Maths checked and correct (270 min, 234 hrs, £3,042; quick-check table right). Plain and honest. |
| 13 | 90-Day Review Sheet | 4/5 | Good one-pager. Unlabelled box next to "The next step I am aiming for". |
| 14 | Back page | 2/5 | Lists only the CI Starter Kit. CLAUDE.md says every back page links the rest of the range. No way to find the shop. |

## Issues, worst first

1. **Back page only links one product.** Page 14. Buyer 3 (and every buyer who finishes the kit) never hears about the RCFA Template, MTBA Assist Tracker, KPI Impact Calculator or Breakdown Analysis Dashboard, which breaks the "back page linking the rest of the range" rule. Fix: replace the single CI Starter Kit block with the same five-product list used on the back pages of the other three PDFs (CI Starter Kit, RCFA Template, MTBA Assist Tracker, KPI Impact Calculator, Breakdown Analysis Dashboard), keep the line "Every fix you make with it goes straight into Tool 5 of this kit." under the CI Starter Kit entry, and change "Available from Kaizen XP." to "Search Kaizen XP on Etsy to find them all."

2. **Labels and hints are below the 7pt minimum on every form page.** All field labels (DATE, WHO I COACHED, RESULT TYPE and so on) are 6.3pt, column headers 6.2pt, the WORKED EXAMPLE badge 5.8pt, hint lines such as "(time, waste, cost, safety)" 6.0pt, footer 6.3pt in light grey (#9a9a9a, low contrast). Hits persona 1 (phone: unreadable without zoom; at phone width these render about 2 to 3 px high) and persona 2 (photocopies blur them). Fix in kitlib.py: field labels and column headers 6.3 to 7.5pt, WORKED EXAMPLE tag 5.8 to 7pt, hint lines 6.0 to 7pt, footer text colour #9a9a9a to #666666. Check pages still fit after the change.

3. **On paper the dropdown choices disappear.** Pages 3, 4, 5, 6, 7, 8, 9, 10, 11, 13. The printed page shows an empty box with a gold arrow, but not the choices behind it. Persona 2 (supervisor with a biro) does not know what "Where are they now?", "Result type" or "Saved time / stopped a problem?" want. Fix: print the choices as a small hint under each dropdown label or column header, for example:
   - Result type: "Time / Waste / Cost / Safety / Quality / More than one"
   - Who saw it: "Line leader / Manager / Both / Wider team / Nobody yet"
   - Where are they now?: "Can do it alone / Nearly there / Started"
   - Saved time / stopped a problem?: "Saved time / Stopped a problem / Both / Neither, but it helped"
   - Why I CC'd: "Improvement / Positive feedback / Problem flagged early / Coaching / Result or saving"

4. **"Boss", "manager" and "line leader" all mean the same person.** Page 5 THE TEST says "so my boss sees the work... so my boss sees that it was not my fault". Page 12 says "your manager". Pages 2, 5, 6 and 10 say "line leader". Persona 1 wonders if these are different people to tell. Fix page 5: "am I sending this so my line leader sees the work, or so my line leader sees that it was not my fault?" Page 12 intro: "Line leaders remember numbers." and subtitle "a number your line leader can repeat in meetings you are not in."

5. **Improvement Log write-in boxes are too small for handwriting.** Pages 10 and 11, THE PROBLEM / WHAT I CHANGED / THE RESULT boxes are about 35pt (12mm) tall: two lines of biro. Page 10 has about 180pt of empty space at the bottom. The DATE box in each black header bar is 12pt (4mm) tall with 7pt text, too small to write in or tap. Persona 2 and persona 1. Fix: on page 10 grow the three boxes to about 50pt each using the empty space; on both pages make the DATE box 16pt tall and move it below the black bar beside RESULT TYPE if it does not fit.

6. **Long entries in table rows vanish when printed.** Pages 4, 5, 8, 9: single-line cells (Best win that week, What it was about, What I did for them) take up to 200 characters at a fixed 8pt. Anything wider than the cell scrolls out of sight on screen and is cut off on print. Persona 1. Fix: set those single-line table fields to auto font size (DA "0 Tf") so long text shrinks to fit, and add to the hint on page 8: "One line. Keep it short."

7. **Weekly Wins only has room for one week, and the save advice is wrong for it.** Page 2 HOW TO USE says "Save as you go." Page 3 is a single week's sheet that will be overwritten next Friday. Persona 1 loses last week's entries. Fix page 2: "Save as you go. For the Weekly Wins page, save a copy of the file each Friday, or print a fresh page 3 each week." (The other three PDFs already say "Save a copy each time you start a new sheet.")

8. **"Sent?" means different things on pages 3 and 4.** Page 3 options: Sent / Sent late / Not yet. Page 4 options: Sent / Sent late / Missed. Fix: use "Sent / Sent late / Not sent yet" on both.

9. **Worked examples disagree with each other.** Page 4 email says "No jams since Wednesday." Page 10 says "Jams down from 4 a shift to 1." Persona 3 reading the preview spots it. Fix page 4 first bullet: "...showed the crew one way to do it. Jams down from 4 a shift to 1 since Wednesday."

10. **Unlabelled box on the 90-Day Review.** Page 13, the box to the right of the "The next step I am aiming for" dropdown has no label (field name t6_next_detail). Fix: add the small label "IN MY OWN WORDS" above it, or a hint "e.g. Team leader on nights".

11. **Typed signatures.** Pages 6 and 7, SIGNED (THEM) and SIGNED (LINE LEADER). On screen these are text boxes, so a phone user types a name and thinks it is signed. Fix: add one line under the page 6 intro: "Print the record and get it signed in ink. On screen, ask them to type their name and the date, then reply to your email to confirm."

12. **Result hint misses Quality.** Pages 10 and 11, THE RESULT hint says "(time, waste, cost, safety)" but the RESULT TYPE list includes Quality. Fix: "(time, waste, cost, safety, quality)".

13. **CC list offers "Other" while saying only the left-hand reasons belong.** Page 5. Fix: remove "Other" from the WHY I CC'D list, or change the note to "Only the reasons on the left belong in this list. If it is none of them, think twice before you CC."

14. **Phone use is hard on every form page.** A4 shrunk to phone width needs pinch-zoom for every box; table rows are about 13 px tall on screen. Persona 1. Fix (wording only, page 2 HOW TO USE): add "On a phone, turn it sideways and pinch to zoom on the box you want. In Acrobat Reader, tap a box, then use the arrows above the keyboard to jump to the next one."

15. **Black cover and back page waste ink.** Pages 1 and 14. Persona 2. Fix: add to HOW TO USE: "To save ink, print pages 2 to 13 only." This needs page numbers in the footer (see Range consistency).

16. **Night shift and "Friday, before you go home".** Page 3 subtitle and "Morning [name]". A night-shift worker finishes on Saturday morning. Fix subtitle: "End of your last shift of the week. Five minutes. Three bullets. Never more."

## Quick wins (under five minutes each)

- Page 5: "boss" to "line leader" (twice). Page 12: "manager" to "line leader".
- Pages 10 and 11: add "quality" to the result hint.
- Page 4: "No jams since Wednesday" to "Jams down from 4 a shift to 1 since Wednesday".
- Page 3 and 4: same "Sent?" options.
- Page 2: new save wording and the phone tip.
- Page 13: label the unlabelled box.
- Tooltips: "People i coached or developed" and "Where i supported..." have a lower-case "i" (screen readers and hover text). Change to "I".

## What works well

- Page 2 and the Put a Number On It page are the strongest writing in the range: frontline, honest ("the lowest honest number"), and the maths is right.
- One worked example story (Line 3 labeller, Sam, Priya, D. Hughes) runs through every tool, so the buyer sees how the sheets feed the 90-Day Review. Keep it.

## Listing (persona 3)

listing.md has no title, photo brief or description yet, so the ten-second test cannot be run. For the listing-optimiser: lead the title with the buyer's words, not the product name, for example "Get Noticed at Work Kit | Weekly Wins Email, Coaching Log, 90-Day Review | Fillable PDF for Shift Workers". First photo should show page 13 (90-Day Review) filled in, because that is the outcome.

## Range consistency (all four PDFs)

| Thing | What the range says now | Use everywhere |
| --- | --- | --- |
| The person you report to | "line leader" (Visibility, RCFA note), "manager" (Visibility p12, RCFA sign-off), "boss" (Visibility p5), "shift leaders" (covers) | "line leader". Keep "Manager" only as a separate sign-off role. |
| Where the work is | LINE / AREA, EQUIPMENT / LINE, LINE / EQUIPMENT, LINE / MACHINE / AREA, AREA | LINE / MACHINE / AREA |
| Impact or result types | Visibility: Time, Waste, Cost, Safety, Quality, More than one. CI Quick Wins: Saved time, Less waste, Safer, Better quality, Saved money, Easier job. CI RCFA: Downtime, Waste, Cost, Safety, Quality, More than one. RCFA Template: Safety, Quality, Downtime, Waste, Customer, Cost | One list: Downtime or time, Waste, Cost, Safety, Quality, Customer, More than one |
| Action status | CI: Not started / In progress / Done / Done and checked. RCFA: Open / In progress / Done / Done and checked | Not started / In progress / Done / Done and checked |
| Did it work? | CI: Yes, fixed / Partly, keep going / No, go again. RCFA: Fixed / Partly fixed, keep going / Not fixed, reopen | Fixed / Partly fixed, keep going / Not fixed, go again |
| Save advice | Visibility: "Save as you go". Others: "Save a copy each time you start a new sheet" | The second, everywhere |
| Page numbers | None printed anywhere, yet MTBA page 2 says "Page 3", "Page 6", "Page 7" and RCFA tags say "PAGE 1 OF 5" on PDF page 4 | Add "Page X of Y" to every footer in kitlib.py |
| Back page | Visibility lists 1 product; the other three list 5 | Same five-product block on all |
| Cross-references to other products | RCFA and MTBA tell buyers to use the "Weekly Wins email" and "improvement log" (Visibility Kit tools they may not own) | Add "(in the Kaizen XP Visibility Kit)" after each mention |
