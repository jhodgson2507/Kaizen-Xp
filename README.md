# Kaizen XP: getting started with Claude Code

This folder is the whole Kaizen XP shop: the products, how to rebuild them,
the rules, and a team of ten agents that check, improve and grow it.
You approve everything. The agents do the counting, checking and drafting.

## 1. Install Claude Code (once, about 10 minutes)

You need a paid Claude plan (Pro, Max, Team or Enterprise).

Windows: open PowerShell and run:

    irm https://claude.ai/install.ps1 | iex

Also install Git for Windows (git-scm.com) so Claude Code can run its tools.

Mac: open Terminal and run:

    curl -fsSL https://claude.ai/install.sh | bash

Then open a NEW terminal window and check it worked:

    claude --version

Not keen on the terminal? Claude Code also runs in the Claude desktop app.

## 2. Put this folder somewhere safe

Unzip it to Documents, so you have Documents/kaizen-xp. Back it up to
OneDrive or Google Drive. This is the shop, so do not lose it again.

## 3. Install the Python bits (only needed to rebuild products)

    pip install -r requirements.txt

## 4. Start Claude Code in the folder

    cd Documents/kaizen-xp
    claude

Sign in when it asks. Claude reads CLAUDE.md automatically and finds the
agents in .claude/agents.

## 5. Your first session

Open FIRST-PROMPTS.md and paste the prompts in, one at a time.

## Using the agents

Name them in what you type, for example:

    Use the ci-challenger agent to review this week's listings.

Or type @ and pick one from the list.

| Agent | Use it for |
| --- | --- |
| coordinator | "Run the weekly cycle": the Monday Brief |
| shop-analyst | What is selling, what is not, and why |
| product-qa | Checking a product file before it goes on sale |
| usability-checker | Would a tired first-time buyer get it? |
| ci-challenger | The blunt weekly review: what is wrong and how to fix it |
| listing-optimiser | Titles, tags, descriptions, photo briefs |
| customer-care | Draft replies to messages and reviews |
| market-scout | What to make next, with evidence |
| product-builder | Building new products and making approved fixes |
| traffic-planner | Pinterest pins and Promotion Playbook video ideas |

## Watch them work: the 3D HQ

Run `python hq/server.py --open` in a second terminal and a live 3D office
opens in your browser: one desk per agent, lit up gold while it works, with
a progress panel for products, issues and decisions. See hq/README.md.

## Your week (about 45 minutes)

- Sunday night: drop the Etsy exports into data/exports (see the README there).
- Monday: type "Run the weekly cycle". Read the brief. Make up to three decisions.
- Tuesday: paste the one approved listing change into Etsy. Log it in decisions.md.
- Any day: paste messages into data/inbox and ask customer-care for replies.

## Where things are

- CLAUDE.md: the rules every agent follows. Change prices and rules here.
- decisions.md: every change and whether it worked.
- issues.md: open problems the ci-challenger is tracking.
- products/: each product, its build script, its listing.
- reports/: everything the agents write.
- hq/: the live 3D HQ that shows the agents working.

## Help

Inside Claude Code type /help, or just ask: "how do I...?"
Docs: https://code.claude.com/docs/en/quickstart
