"""Kaizen XP HQ: a live 3D view of the agent team.

Run it from the kaizen-xp folder, in its own terminal, next to Claude Code:

    python hq/server.py            (then open http://localhost:8765)
    python hq/server.py --open     (opens the browser for you)

It serves the HQ page, streams hq/events.jsonl (written by hq/hook.py while
the agents work) and works out progress from the files the agents write:
reports/, issues.md, decisions.md, products/ and data/exports/stats.csv.
Standard library only. Nothing leaves this computer.
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import sys
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HQ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HQ)
LOG = os.path.join(HQ, "events.jsonl")

# The plan's ten agents: name, desk title, wave, where its output lands.
AGENTS = [
    ("coordinator", "Coordinator", 1, "reports/brief/*.md"),
    ("shop-analyst", "Shop Analyst", 1, "reports/weekly/*.md"),
    ("product-qa", "Product QA", 1, "reports/qa/*.md"),
    ("ci-challenger", "CI Challenger", 1, "reports/ci/*.md"),
    ("usability-checker", "Usability Checker", 1, "reports/ux/*.md"),
    ("listing-optimiser", "Listing Optimiser", 2, "products/*/listing-draft.md"),
    ("customer-care", "Customer Care", 2, "data/inbox/replies-*.md"),
    ("market-scout", "Market Scout", 3, "reports/market/*.md"),
    ("product-builder", "Product Builder", 3, "products/*/*.pdf products/*/*.xlsx"),
    ("traffic-planner", "Traffic Planner", 3, "reports/traffic/*.md"),
]


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def files(patterns):
    out = []
    for pat in patterns.split():
        out += glob.glob(os.path.join(ROOT, pat))
    return sorted(out, key=os.path.getmtime)


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def table_rows(text):
    """Rows of the first markdown table in text, as lists of cells."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header


def verdict(path, words):
    """First verdict word found near the top of a report."""
    head = read(path)[:600].lower()
    for w in words:
        if w.lower() in head:
            return w
    return "See report"


def agent_progress():
    out = []
    for name, title, wave, pattern in AGENTS:
        made = files(pattern)
        if name == "product-builder":
            # Product files ship in the pack; count only ones rebuilt since.
            made = [f for f in made if os.path.getmtime(f) > pack_time()]
        last = made[-1] if made else None
        brief = os.path.join(ROOT, ".claude", "agents", name + ".md")
        out.append({
            "name": name,
            "title": title,
            "wave": wave,
            "installed": os.path.exists(brief),
            "outputs": len(made),
            "last_output": rel(last) if last else None,
            "last_output_at": os.path.getmtime(last) if last else None,
        })
    return out


_pack = None


def pack_time():
    global _pack
    if _pack is None:
        _pack = os.path.getmtime(os.path.join(ROOT, "kitlib.py")) + 60
    return _pack


def product_progress():
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, "products", "*", ""))):
        slug = os.path.basename(os.path.dirname(d))
        product = [f for f in os.listdir(d) if f.endswith((".pdf", ".xlsx"))]
        qa = files("reports/qa/%s*.md" % slug)
        ux = files("reports/ux/%s*.md" % slug)
        out.append({
            "slug": slug,
            "file": product[0] if product else None,
            "qa": verdict(qa[-1], ["FAIL", "PASS"]) if qa else None,
            "ux": verdict(ux[-1], ["Not ready", "Ready with fixes", "Ready"]) if ux else None,
            "listing": os.path.exists(os.path.join(d, "listing.md")),
            "draft": os.path.exists(os.path.join(d, "listing-draft.md")),
        })
    return out


def issue_progress():
    counts = {}
    for row in table_rows(read(os.path.join(ROOT, "issues.md"))):
        if len(row) >= 6 and row[0]:
            status = row[5] or "Open"
            counts[status] = counts.get(status, 0) + 1
    return counts


def decision_progress():
    rows = [r for r in table_rows(read(os.path.join(ROOT, "decisions.md"))) if r and r[0]]
    due = 0
    today = dt.date.today()
    for r in rows:
        try:
            when = dt.date.fromisoformat(r[0])
        except ValueError:
            continue
        if (today - when).days >= 14 and (len(r) < 5 or not r[4]):
            due += 1
    return {"logged": len(rows), "awaiting_result": due}


def shop_numbers():
    path = os.path.join(ROOT, "data", "exports", "stats.csv")
    weeks = {}
    try:
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                w = weeks.setdefault(row.get("week", ""), {"views": 0, "favourites": 0, "orders": 0, "revenue": 0.0})
                for k in ("views", "favourites", "orders"):
                    w[k] += int(float(row.get(k) or 0))
                w["revenue"] += float(row.get("revenue") or 0)
    except (OSError, ValueError):
        return None
    if not weeks:
        return None
    latest = max(weeks)
    return dict(week=latest, **weeks[latest])


def progress():
    return {
        "generated": time.time(),
        "agents": agent_progress(),
        "products": product_progress(),
        "issues": issue_progress(),
        "decisions": decision_progress(),
        "shop": shop_numbers(),
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HQ, **kw)

    def log_message(self, *a):
        pass

    def send_json(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/progress":
            return self.send_json(progress())
        if path == "/api/events":
            return self.stream_events()
        if path.endswith(".jsonl") or path.endswith(".py"):
            self.send_error(404)
            return
        return super().do_GET()

    def stream_events(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        offset = 0
        try:
            # Replay recent history so the HQ starts in the right state.
            if os.path.exists(LOG):
                with open(LOG, "rb") as f:
                    lines = f.readlines()
                    offset = f.tell()
                for line in lines[-400:]:
                    self.send_event(line, replay=True)
            self.wfile.write(b"event: ready\ndata: {}\n\n")
            self.wfile.flush()
            beat = time.time()
            while True:
                size = os.path.getsize(LOG) if os.path.exists(LOG) else 0
                if size < offset:
                    offset = 0  # log was trimmed
                if size > offset:
                    with open(LOG, "rb") as f:
                        f.seek(offset)
                        chunk = f.read()
                    end = chunk.rfind(b"\n") + 1
                    for line in chunk[:end].splitlines():
                        self.send_event(line)
                    offset += end
                if time.time() - beat > 15:
                    self.wfile.write(b": keep-alive\n\n")
                    self.wfile.flush()
                    beat = time.time()
                time.sleep(0.3)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def send_event(self, line, replay=False):
        line = line.strip()
        if not line:
            return
        try:
            ev = json.loads(line)
        except ValueError:
            return
        ev["replay"] = replay
        self.wfile.write(b"data: " + json.dumps(ev).encode() + b"\n\n")
        self.wfile.flush()


def main():
    ap = argparse.ArgumentParser(description="Kaizen XP agent HQ")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--open", action="store_true", help="open the browser")
    args = ap.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    url = "http://localhost:%d" % args.port
    print("Kaizen XP HQ running at %s  (Ctrl+C to stop)" % url)
    print("Demo with made-up activity: %s/?demo" % url)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHQ stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
