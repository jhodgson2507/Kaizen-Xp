# Kaizen XP HQ: watch the agents work

A live 3D office with a desk for each of the ten agents. When an agent is
working, its screen lights up gold, a ring spins over its head and you can
see what it is doing right now ("Reading stats.csv", "Render every page").
Gold orbs fly between desks when one agent hands work to another. The side
panel tracks progress from the files the agents write.

## Start it (two terminals)

Terminal 1, the HQ:

    cd Documents/kaizen-xp
    python hq/server.py --open

Terminal 2, Claude Code as usual:

    cd Documents/kaizen-xp
    claude

Then type "Run the weekly cycle" and watch. The page is at
http://localhost:8765. On a Mac use `python3` instead of `python`.

Want to see it before the agents have done anything? Open
http://localhost:8765/?demo for a made-up weekly cycle.

## What each colour means

| Colour | Meaning |
| --- | --- |
| Grey | Idle |
| Gold, ring spinning | Working. The bar fills as it goes, based on how long its earlier runs took |
| Green | Just finished (stays green for 90 seconds) |
| Amber, blinking | Claude is waiting for you: a permission prompt or a question |

## The progress panel

- **The team**: what each agent is doing, how many reports it has written and when it last wrote one.
- **Product pipeline**: for each product, the latest QA verdict (reports/qa), usability verdict (reports/ux), and whether listing.md and listing-draft.md exist.
- **Issues**: counts by status from issues.md.
- **Decisions**: changes logged in decisions.md, and how many are two weeks old with no result filled in.
- **Shop, latest week**: totals from data/exports/stats.csv.
- **Live feed**: every hand-off, file written and step taken.

## How it works

- `.claude/settings.json` tells Claude Code to run `hq/hook.py` on each step.
- `hook.py` adds one short line to `hq/events.jsonl`: which agent, which tool, and a file name or short label. It never saves file contents, prompts or buyer messages. The log trims itself so it stays small.
- `server.py` streams that log to the page and reads the project files for the progress panel. Python standard library only, and it only listens on this computer.
- `vendor/` holds three.js (MIT licence), so the HQ works with no internet.

If the hooks ever get in the way, delete `.claude/settings.json`. The agents
work exactly the same without it; the HQ just goes quiet.
