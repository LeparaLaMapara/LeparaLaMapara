"""Refresh the rank board section of README.md from public sources.

Runs daily in GitHub Actions. Every source is public; a source that fails keeps
its previous line instead of breaking the page.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
LOGIN = "LeparaLaMapara"
UA = {"User-Agent": "profile-rank-board"}
START, END = "<!-- RANK-BOARD:START -->", "<!-- RANK-BOARD:END -->"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def latest_posts(n=3):
    root = ET.fromstring(get("https://www.tmashininisekgoto.com/feed.xml"))
    items = root.findall("./channel/item")[:n]
    return [f"[{i.findtext('title').strip()}]({i.findtext('link').strip()})" for i in items]


def engine():
    version = json.loads(get("https://pypi.org/pypi/ubunye-engine/json"))["info"]["version"]
    month = json.loads(get("https://pypistats.org/api/packages/ubunye-engine/recent"))["data"]["last_month"]
    return f"[v{version} on PyPI](https://pypi.org/project/ubunye-engine/), {month:,} downloads in the last month"


def last_trip():
    events = json.loads(get(f"https://api.github.com/users/{LOGIN}/events/public?per_page=50"))
    for e in events:
        if e["type"] in ("PushEvent", "PullRequestEvent", "CreateEvent", "ReleaseEvent"):
            repo = e["repo"]["name"]
            day = e["created_at"][:10]
            return f"[{repo}](https://github.com/{repo}) on {day}"
    raise ValueError("no recent public activity")


def old_rows(block):
    rows = {}
    for line in block.splitlines():
        m = re.match(r"\| \*\*(.+?)\*\* \| (.+) \|$", line)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def main():
    text = README.read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    block, tail = rest.split(END, 1)
    previous = old_rows(block)

    def safe(label, fn):
        try:
            return fn()
        except Exception as exc:  # keep yesterday's line if a source is down
            print(f"{label}: {exc}")
            return previous.get(label, "out of service today")

    posts = safe("Latest from the blog", lambda: "<br>".join(latest_posts()))
    rows = [
        ("Latest from the blog", posts),
        ("Ubunye Engine", safe("Ubunye Engine", engine)),
        ("Last public trip", safe("Last public trip", last_trip)),
    ]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["", "| | |", "|---|---|"]
    lines += [f"| **{k}** | {v} |" for k, v in rows]
    lines += ["", f"<sub>The rank marshal updates this board every morning. Last update {stamp}.</sub>", ""]
    README.write_text(head + START + "\n".join(lines) + END + tail, encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
