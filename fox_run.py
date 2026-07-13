#!/usr/bin/env python3
"""
Custom, hand-built contribution-graph animation — a fox running the calendar.
Not a fork of Platane/snk or any other tool: this script pulls real contribution
data straight from GitHub's GraphQL API and renders an original animated SVG,
recolored to the profile's navy/amber palette instead of GitHub green.
"""
import json
import os
import urllib.request

USERNAME = os.environ.get("USERNAME") or os.environ["GITHUB_REPOSITORY_OWNER"]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($userName:String!) {
  user(login:$userName){
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""


def fetch_calendar():
    body = json.dumps({"query": QUERY, "variables": {"userName": USERNAME}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "fox-run-script",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return weeks


def color_for(count):
    if count == 0:
        return "#1a1636"
    if count <= 2:
        return "#4a3a14"
    if count <= 5:
        return "#8a6a1a"
    if count <= 9:
        return "#c99a1f"
    return "#f5b700"


def build_svg(weeks):
    cell = 11
    gap = 3
    pitch = cell + gap
    origin_x, origin_y = 40, 46

    cols = weeks
    n_cols = len(cols)
    n_rows = 7

    width = origin_x + n_cols * pitch + 20
    height = origin_y + n_rows * pitch + 40

    # flatten into a boustrophedon path: down col0, up col1, down col2, ...
    cells = []
    for ci, week in enumerate(cols):
        days = week["contributionDays"]
        row_order = range(len(days)) if ci % 2 == 0 else range(len(days) - 1, -1, -1)
        for ri in row_order:
            day = days[ri]
            cx = origin_x + ci * pitch + cell / 2
            cy = origin_y + ri * pitch + cell / 2
            cells.append({"x": cx, "y": cy, "count": day["contributionCount"]})

    total = len(cells)
    dur = 24.0

    # rects
    rects = []
    for i, c in enumerate(cells):
        dim = "#1a1636"
        lit = color_for(c["count"])
        t = round(i / total, 4)
        rects.append(
            f'<rect x="{c["x"] - cell / 2:.1f}" y="{c["y"] - cell / 2:.1f}" width="{cell}" height="{cell}" '
            f'rx="2" fill="{dim}">'
            f'<animate attributeName="fill" values="{dim};{lit};{dim}" '
            f'keyTimes="0;{t if t > 0 else 0.001};1" dur="{dur}s" repeatCount="indefinite"/>'
            f"</rect>"
        )

    # motion path through cell centers
    path_d = "M " + " L ".join(f'{c["x"]:.1f},{c["y"]:.1f}' for c in cells)

    fox = """
  <symbol id="fox" viewBox="0 0 26 16">
    <path d="M2,11 C2,7 6,4 12,4 L20,3 L17,6 L20,7 L14,8 C18,9 20,11 20,13 C15,15 6,15 2,11 Z" fill="#f5b700"/>
    <path d="M2,11 L-2,8 L0,12 L-2,14 L3,13 Z" fill="#c99a1f"/>
    <circle cx="18" cy="5.5" r="1" fill="#0b0921"/>
    <path d="M12,4 L11,1 L13,3.5 Z" fill="#f5b700"/>
    <path d="M15,3.5 L15,0.5 L17,3 Z" fill="#f5b700"/>
  </symbol>
"""

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="fbg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0921"/>
      <stop offset="100%" stop-color="#1a1636"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#fbg)" rx="10"/>
  <text x="{origin_x}" y="24" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="13" letter-spacing="3" fill="#f5b700" font-weight="700">THE FOX RUNS THE CALENDAR</text>
  <text x="{width - 20}" y="24" text-anchor="end" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="10" fill="#7f7bb0">hand-built · real contribution data · not a fork</text>
  {"".join(rects)}
  {fox}
  <use href="#fox" width="26" height="16" x="-13" y="-8">
    <animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{path_d}"/>
  </use>
</svg>"""
    return svg


def main():
    weeks = fetch_calendar()
    svg = build_svg(weeks)
    os.makedirs("dist", exist_ok=True)
    with open("dist/fox-run.svg", "w") as f:
        f.write(svg)
    print(f"Wrote dist/fox-run.svg from {len(weeks)} weeks of data")


if __name__ == "__main__":
    main()
