"""Claude Code hook: logs what the agents are doing so the 3D HQ can show it live.

Claude Code runs this on every hook event set up in .claude/settings.json and
passes the event as JSON on stdin. We append one short line to
hq/events.jsonl. The HQ server streams that file to the browser.

Privacy: only the agent name, the tool name and a short label (a file name or
a search phrase) are logged. Never file contents, never buyer messages.
This script must never block Claude, so it always exits 0.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "events.jsonl")
MAX_BYTES = 2_000_000
KEEP_LINES = 2000


def short_label(tool, inp):
    """A short, safe description of what a tool call is touching."""
    if not isinstance(inp, dict):
        return ""
    if tool in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        return os.path.basename(path)
    if tool in ("Glob", "Grep"):
        return str(inp.get("pattern", ""))[:60]
    if tool == "Bash":
        # The description is written for humans; the command may hold data.
        return str(inp.get("description", "") or "running a command")[:80]
    if tool in ("WebSearch",):
        return str(inp.get("query", ""))[:80]
    if tool in ("WebFetch",):
        return str(inp.get("url", "")).split("?")[0][:80]
    if tool in ("Task", "Agent"):
        return str(inp.get("description", ""))[:80]
    return ""


def build_event(data):
    name = data.get("hook_event_name", "")
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    ev = {
        "ts": time.time(),
        "event": name,
        "session": str(data.get("session_id", ""))[:12],
        # Set by Claude Code when the hook fires inside a subagent.
        "agent": data.get("agent_type") or "",
        "agent_id": data.get("agent_id") or "",
    }
    if tool:
        ev["tool"] = tool
        ev["label"] = short_label(tool, inp)
    if tool in ("Task", "Agent") and isinstance(inp, dict):
        # The main session handing work to a specialist.
        ev["target"] = inp.get("subagent_type", "")
    if name == "PostToolUse" and tool in ("Write", "Edit", "MultiEdit"):
        path = (inp or {}).get("file_path", "")
        rel = os.path.relpath(path, os.path.dirname(HERE)) if path else ""
        ev["path"] = rel.replace(os.sep, "/")
    if name == "Notification":
        ev["label"] = str(data.get("message", ""))[:100]
    return ev


def trim_log():
    try:
        if os.path.getsize(LOG) > MAX_BYTES:
            with open(LOG, encoding="utf-8") as f:
                lines = f.readlines()[-KEEP_LINES:]
            with open(LOG, "w", encoding="utf-8") as f:
                f.writelines(lines)
    except OSError:
        pass


def main():
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        data = json.loads(raw) if raw.strip() else {}
        ev = build_event(data)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev) + "\n")
        trim_log()
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
