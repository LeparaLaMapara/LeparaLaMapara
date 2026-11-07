"""Draw the last year of contributions as passengers a minibus taxi picks up.

Runs daily in GitHub Actions. Needs GITHUB_TOKEN in the environment.
Writes assets/taxi-light.svg and assets/taxi-dark.svg.
"""
import json
import os
import urllib.request
from pathlib import Path

from build_static import BLACK, YELLOW, minibus
from svgtext import path

LOGIN = os.environ.get("PROFILE_LOGIN", "LeparaLaMapara")
OUT = Path(__file__).resolve().parent.parent / "assets"

CELL, GAP, LEFT, TOP = 15, 3, 20, 20
SCALE = 0.42
PERIOD = 18
TRIP = 0.8

THEMES = {
    "light": {"empty": "#ebedf0", "ramp": ["#fff1b8", "#ffe27a", "#ffd23f", "#f0b400"], "road": "#d0d0d0", "text": BLACK},
    "dark": {"empty": "#1f1f1f", "ramp": ["#5c4a12", "#9c7a17", "#ffd23f", "#ffe27a"], "road": "#2e2e2e", "text": "#f2f2f2"},
}

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{contributionCount weekday}}}}}}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-taxi"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["weekday"], d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def level(count, top):
    if count == 0:
        return -1
    q = count / top
    return 0 if q <= .25 else 1 if q <= .5 else 2 if q <= .75 else 3


def render(total, weeks, theme):
    t = THEMES[theme]
    cols = len(weeks)
    grid_w = cols * (CELL + GAP)
    w = LEFT * 2 + grid_w
    road_y = TOP + 7 * (CELL + GAP) + 40
    h = road_y + 46
    bus_w = 220 * SCALE
    travel = w + bus_w + 40
    top = max([c for wk in weeks for _, c in wk] + [1])

    css = [
        f".bus{{animation:bus {PERIOD}s linear infinite}}",
        f"@keyframes bus{{0%{{transform:translate({-bus_w - 20:.0f}px,{road_y}px) scale({SCALE})}}"
        f"{TRIP * 100:.0f}%{{transform:translate({w + 20:.0f}px,{road_y}px) scale({SCALE})}}"
        f"100%{{transform:translate({w + 20:.0f}px,{road_y}px) scale({SCALE})}}}}",
        ".wheel{transform-box:fill-box;transform-origin:center;animation:spin .5s linear infinite}",
        "@keyframes spin{to{transform:rotate(360deg)}}",
    ]
    cells = []
    for x, wk in enumerate(weeks):
        cx = LEFT + x * (CELL + GAP) + CELL / 2
        # Moment the front of the bus reaches this column, as a share of the period.
        p = TRIP * (cx + 20) / travel * 100
        css.append(
            f"@keyframes c{x}{{0%,{p:.1f}%{{opacity:1;transform:translate(0,0)}}"
            f"{p + 2.5:.1f}%{{opacity:0;transform:translate(0,{road_y - TOP - 40}px)}}"
            f"97%{{opacity:0;transform:translate(0,0)}}100%{{opacity:1}}}}"
        )
        for wd, count in wk:
            lv = level(count, top)
            y = TOP + wd * (CELL + GAP)
            px = LEFT + x * (CELL + GAP)
            cells.append(f'<rect x="{px}" y="{y}" width="{CELL}" height="{CELL}" fill="{t["empty"]}"/>')
            if lv >= 0:
                cells.append(
                    f'<rect class="p" style="animation:c{x} {PERIOD}s ease-in infinite" x="{px}" y="{y}" '
                    f'width="{CELL}" height="{CELL}" fill="{t["ramp"][lv]}"/>'
                )
    css.append("@media (prefers-reduced-motion:reduce){.bus,.wheel,.p{animation:none!important}}")
    caption = path(
        f"{total} contributions picked up in the last year. No standing passengers.",
        "WorkSans", 15, LEFT, h - 6, wght=600,
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Contribution graph: a minibus taxi drives past and picks up {total} contributions from the last year.">
<style>{"".join(css)}</style>
{"".join(cells)}
<rect x="0" y="{road_y}" width="{w}" height="8" fill="{t["road"]}"/>
<line x1="0" y1="{road_y + 4}" x2="{w}" y2="{road_y + 4}" stroke="{YELLOW}" stroke-width="2" stroke-dasharray="14 10"/>
<g class="bus">{minibus()}</g>
<path d="{caption}" fill="{t["text"]}"/>
</svg>"""


if __name__ == "__main__":
    total, weeks = fetch()
    for theme in THEMES:
        (OUT / f"taxi-{theme}.svg").write_text(render(total, weeks, theme), encoding="utf-8")
    print("contributions", total, "weeks", len(weeks))
