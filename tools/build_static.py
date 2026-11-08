"""Build the banner and the fare board. Run once; the output is committed."""
from pathlib import Path

from svgtext import path, width

OUT = Path(__file__).resolve().parent.parent / "assets"
BLACK, YELLOW, RED, GREEN, WHITE, AMBER = "#111111", "#ffd23f", "#d62828", "#1b7f3b", "#ffffff", "#ffb000"

W, H = 1000, 420
ROAD = 404

DESTINATIONS = ["PRODUCTION", "WITS", "DATABRICKS", "THE WORLD"]
GREETINGS = ["THOBELA", "DUMELA", "SAWUBONA", "HELLO", "MEI CHOMMIE"]


def cycle_css(cls, n, period):
    """CSS that shows item i of n for period/n seconds, in turn, forever."""
    slot = 100 / n
    css = [
        f".{cls}{{opacity:0;animation:{cls} {period}s infinite}}",
        f"@keyframes {cls}{{0%{{opacity:1}}{slot - 1.5:.2f}%{{opacity:1}}{slot:.2f}%{{opacity:0}}100%{{opacity:0}}}}",
    ]
    for i in range(n):
        css.append(f".{cls}-{i}{{animation-delay:{i * period / n:.2f}s}}")
    return "\n".join(css)


def wheel(cx, cls):
    return (
        f'<g class="{cls}"><circle cx="{cx}" cy="-6" r="17" fill="{BLACK}"/>'
        f'<circle cx="{cx}" cy="-6" r="7" fill="#9a9a9a"/>'
        f'<rect x="{cx - 2}" y="-21" width="4" height="10" fill="#9a9a9a"/></g>'
    )


def minibus():
    """Side view of a Quantum style minibus taxi, 220 wide, wheels resting on y=0."""
    sosha = path("SOSHA", "Bungee-Regular", 12, 78, -58, anchor="middle")
    return f"""<g>
  <path d="M0 -14 V-74 Q0 -86 12 -88 L150 -92 Q172 -92 186 -78 L214 -46 Q220 -40 220 -30 V-14 Z" fill="{WHITE}" stroke="{BLACK}" stroke-width="4"/>
  <rect x="2" y="-40" width="216" height="9" fill="{RED}"/>
  <rect x="2" y="-31" width="216" height="6" fill="{GREEN}"/>
  <path d="M150 -84 Q168 -84 178 -74 L198 -50 H150 Z" fill="{BLACK}"/>
  <rect x="14" y="-80" width="36" height="28" fill="{BLACK}"/>
  <rect x="58" y="-82" width="40" height="30" fill="{BLACK}"/>
  <rect x="104" y="-84" width="40" height="32" fill="{BLACK}"/>
  <rect x="54" y="-72" width="48" height="17" fill="{YELLOW}"/>
  <path d="{sosha}" fill="{BLACK}"/>
  <rect x="204" y="-36" width="14" height="8" fill="{YELLOW}" stroke="{BLACK}" stroke-width="2"/>
  <rect x="-4" y="-18" width="228" height="6" fill="{BLACK}"/>
  {wheel(48, "wheel")}
  {wheel(176, "wheel")}
</g>"""


def arrow(x, y, s, color):
    """Two way arrow drawn by hand, the dot font has no glyph for it."""
    return (
        f'<path d="M{x} {y - s * .3:.1f} h{s} l-{s * .28:.1f} -{s * .28:.1f} '
        f'M{x + s} {y + s * .3:.1f} h-{s} l{s * .28:.1f} {s * .28:.1f}" '
        f'stroke="{color}" stroke-width="{s * .15:.1f}" fill="none" stroke-linecap="square"/>'
    )


def banner():
    dest = "".join(
        f'<path class="dest dest-{i}" d="{path(d, "Doto", 54, 690, 100, wght=900, anchor="middle")}"/>'
        for i, d in enumerate(DESTINATIONS)
    )
    greet = "".join(
        f'<path class="greet greet-{i}" d="{path(g, "Bungee-Regular", 24, 846, 237, anchor="middle")}" fill="{BLACK}"/>'
        for i, g in enumerate(GREETINGS)
    )
    origin = path("SOSHANGUVE", "Doto", 54, 44, 100, wght=900)
    name = path("THABANG MASHININI-SEKGOTO", "Bungee-Regular", 30, 46, 228)
    sub = path("AI systems built here. Open daily.", "WorkSans", 20, 48, 262, wght=600)
    board = f'<g fill="{AMBER}"><path d="{origin}"/>{arrow(414, 82, 44, AMBER)}{dest}</g>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Taxi destination board reading Soshanguve to production. Thabang Mashinini-Sekgoto. AI systems built here. Open daily.">
<style>
{cycle_css("dest", len(DESTINATIONS), 12)}
{cycle_css("greet", len(GREETINGS), 10)}
.drive{{animation:drive 14s linear infinite}}
@keyframes drive{{from{{transform:translate(-260px,{ROAD}px)}}to{{transform:translate({W + 40}px,{ROAD}px)}}}}
.wheel{{transform-box:fill-box;transform-origin:center;animation:spin .6s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.drive,.wheel,.dest,.greet{{animation:none}}.dest-0,.greet-0{{opacity:1}}}}
</style>
<defs>
  <pattern id="dots" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.1" fill="#2c2c2c"/></pattern>
  <g id="board">{board}</g>
  <filter id="glow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.4"/></filter>
</defs>
<rect x="22" y="26" width="960" height="118" fill="{BLACK}" opacity=".3"/>
<rect x="14" y="18" width="960" height="118" fill="{BLACK}"/>
<rect x="24" y="28" width="940" height="98" fill="url(#dots)"/>
<g filter="url(#glow)" opacity=".6"><use href="#board"/></g>
<use href="#board"/>
<rect x="34" y="188" width="610" height="98" fill="{BLACK}"/>
<rect x="26" y="180" width="610" height="98" fill="{YELLOW}" stroke="{BLACK}" stroke-width="5"/>
<path d="{name}" fill="{BLACK}"/>
<path d="{sub}" fill="{BLACK}"/>
<rect x="708" y="207" width="280" height="50" fill="{BLACK}"/>
<rect x="702" y="200" width="280" height="50" fill="{WHITE}" stroke="{BLACK}" stroke-width="5"/>
{greet}
<rect x="0" y="{ROAD}" width="{W}" height="10" fill="#cfcfcf"/>
<line x1="0" y1="{ROAD + 5}" x2="{W}" y2="{ROAD + 5}" stroke="{YELLOW}" stroke-width="2.5" stroke-dasharray="18 12"/>
<g class="drive">{minibus()}</g>
</svg>"""


ROUTES = [
    ("PYTHON", "R10"),
    ("APACHE SPARK", "R15"),
    ("DATABRICKS", "R15"),
    ("PYTORCH", "R12"),
    ("MLFLOW", "R10"),
    ("AIRFLOW", "R10"),
    ("KUBERNETES", "R14"),
    ("TYPESCRIPT", "R10"),
]


def fareboard():
    w, row, top = 1000, 50, 96
    h = top + row * ((len(ROUTES) + 1) // 2) + 70
    parts = []
    for i, (route, fare) in enumerate(ROUTES):
        x0 = 40 + (i % 2) * 476
        y = top + (i // 2) * row + 36
        rw = width(route, "Bungee-Regular", 23)
        parts += [
            f'<path d="{path(route, "Bungee-Regular", 23, x0, y)}" fill="{BLACK}"/>',
            f'<line x1="{x0 + rw + 12:.0f}" y1="{y - 5}" x2="{x0 + 352}" y2="{y - 5}" stroke="{BLACK}" stroke-width="4" stroke-dasharray="1 9" stroke-linecap="round"/>',
            f'<rect x="{x0 + 364}" y="{y - 30}" width="72" height="38" fill="{RED}" stroke="{BLACK}" stroke-width="3"/>',
            f'<path d="{path(fare, "Bungee-Regular", 21, x0 + 400, y - 2, anchor="middle")}" fill="{WHITE}"/>',
        ]
    title = path("ROUTES AND FARES", "Bungee-Regular", 36, 40, 66)
    note = path("Exact change only. Fares are paid in stars and pull requests.", "WorkSans", 19, 40, h - 34, wght=600)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Fare board of the tools I work with: Python, Apache Spark, Databricks, PyTorch, MLflow, Airflow, Kubernetes, TypeScript.">
<rect x="14" y="14" width="{w - 20}" height="{h - 20}" fill="{BLACK}"/>
<rect x="6" y="6" width="{w - 20}" height="{h - 20}" fill="{YELLOW}" stroke="{BLACK}" stroke-width="6"/>
<rect x="6" y="84" width="{w - 20}" height="8" fill="{BLACK}"/>
<path d="{title}" fill="{BLACK}"/>
{"".join(parts)}
<path d="{note}" fill="{BLACK}"/>
</svg>"""


CARDS = [
    ("agent-roadmap-kit", "01", "AGENT ROADMAP KIT", "Six stops to one working AI assistant that answers from your own notes. Free, and it runs offline.", "START HERE", YELLOW, BLACK),
    ("ubunye-engine", "02", "UBUNYE ENGINE", "Describe a Spark pipeline once. Run the same folder on a laptop, Docker, Kubernetes or Databricks.", "PIP INSTALL UBUNYE-ENGINE", BLACK, YELLOW),
    ("tfilterspy", "03", "TFILTERSPY", "Kalman, Particle and Ensemble filters with a scikit learn style API. For sensors that lie.", "BAYESIAN FILTERING", WHITE, BLACK),
    ("ubunye-examples", "04", "UBUNYE EXAMPLES", "Worked pipelines on Databricks. The proof the engine does what it says.", "DATABRICKS", RED, WHITE),
    ("kasilam", "05", "KASILAM", "Young people in townships learn to build with AI by shipping sites for local businesses. I teach, they build.", "COMMUNITY", GREEN, WHITE),
    ("ubunye-org", "06", "ALL ROUTES", "Everything I build in the open lives at Ubunye AI Ecosystems. Open source made in Africa.", "UBUNYE AI ECOSYSTEMS", WHITE, BLACK),
]


def wrap(text, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if width(trial, "WorkSans", size, wght=500) > max_w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def card(num, title, blurb, strip, bg, fg):
    w, h = 480, 210
    ink = BLACK if bg in (YELLOW, WHITE) else WHITE
    badge_bg, badge_fg = (BLACK, YELLOW) if bg != BLACK else (YELLOW, BLACK)
    tsize = 30 if width(title, "Bungee-Regular", 30) < 380 else 24
    parts = [
        f'<rect x="10" y="10" width="{w - 14}" height="{h - 14}" fill="{BLACK}"/>',
        f'<rect x="4" y="4" width="{w - 14}" height="{h - 14}" fill="{bg}" stroke="{BLACK}" stroke-width="4"/>',
        f'<rect x="4" y="4" width="{w - 14}" height="10" fill="{RED if bg != RED else BLACK}"/>',
        f'<rect x="4" y="14" width="{w - 14}" height="6" fill="{GREEN if bg != GREEN else BLACK}"/>',
        f'<rect x="20" y="30" width="98" height="24" fill="{badge_bg}"/>',
        f'<path d="{path(f"ROUTE {num}", "Bungee-Regular", 14, 69, 48, anchor="middle")}" fill="{badge_fg}"/>',
        f'<path d="{path(title, "Bungee-Regular", tsize, 20, 94)}" fill="{fg}"/>',
    ]
    for i, line in enumerate(wrap(blurb, 16, w - 52)[:3]):
        parts.append(f'<path d="{path(line, "WorkSans", 16, 21, 124 + i * 21, wght=500)}" fill="{ink}" opacity=".92"/>')
    parts += [
        f'<rect x="4" y="{h - 42}" width="{w - 14}" height="32" fill="{BLACK}"/>',
        f'<path d="{path(strip, "Doto", 17, 20, h - 20, wght=900)}" fill="{AMBER}"/>',
        f'<path d="{path("HOP ON", "Bungee-Regular", 14, w - 24, h - 20, anchor="end")}" fill="{YELLOW}"/>',
    ]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Route {num}: {title.title()}. {blurb}">
{"".join(parts)}
</svg>"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, svg in (("banner.svg", banner()), ("fareboard.svg", fareboard())):
        (OUT / name).write_text(svg, encoding="utf-8")
        print(name, len(svg))
    for slug, *rest in CARDS:
        (OUT / f"card-{slug}.svg").write_text(card(*rest), encoding="utf-8")
