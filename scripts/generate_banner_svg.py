#!/usr/bin/env python3
"""
Generate an animated horizontal terminal ASCII banner SVG for "WELCOME TO THE HOOD"
Matching the exact GitHub profile terminal window theme (860px width).
"""
import html
import os
import sys
import pyfiglet

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "welcome-banner.svg")

# Dimensions matching heatmap width (860px)
W = 860
H = 200
PAD_X = 26
TITLEBAR_H = 30
ART_W = W - PAD_X * 2  # 808px

# Colors matching profile palette
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
PROMPT_COLOR = "#7d8590"
USER_COLOR = "#58a6ff"
ACCENT = "#22d3ee"
GREEN = "#39d353"
CURSOR = "#22d3ee"

# 1. Render ASCII banner via pyfiglet slant font
f = pyfiglet.Figlet(font="slant", width=120)
ascii_raw = f.renderText("WELCOME TO THE HOOD")
raw_lines = [l for l in ascii_raw.split("\n") if l.strip()]

# Pad all lines to same length
max_len = max(len(l) for l in raw_lines)
lines = [l.ljust(max_len) for l in raw_lines]

# Row positioning
art_top = 66
CELL_H = 16.5
font_size = 14

# Timing
CMD_START = 0.2
CMD_DUR = 0.6
BANNER_START = 0.9
BANNER_DUR = 2.4
BANNER_END = BANNER_START + BANNER_DUR
BOTTOM_START = BANNER_END + 0.1

cmd_text = "mahattva@github:~$ ./welcome.sh"
cmd_w = len(cmd_text) * 8.0

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient>',
    f'<linearGradient id="bannerGrad" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0%" stop-color="{ACCENT}"/>'
    f'<stop offset="100%" stop-color="{GREEN}"/>'
    f'</linearGradient>',
    f'<clipPath id="cmdClip">'
    f'<rect x="{PAD_X}" y="38" width="0" height="22">'
    f'<animate attributeName="width" from="0" to="{cmd_w}" begin="{CMD_START}s" dur="{CMD_DUR}s" fill="freeze"/>'
    f'</rect>'
    f'</clipPath>',
    f'<clipPath id="bannerClip">'
    f'<rect x="{PAD_X}" y="{art_top - 4}" width="0" height="{len(lines) * CELL_H + 8}">'
    f'<animate attributeName="width" from="0" to="{ART_W}" begin="{BANNER_START}s" dur="{BANNER_DUR}s" fill="freeze"/>'
    f'</rect>'
    f'</clipPath>',
    '</defs>',

    # Window frame
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# Mac traffic light dots
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD_X + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">mahattva@github: ~$ ./welcome.sh</text>')

# 2. Command invocation line with typewriter wipe
cmd_rendered = (
    f'<text x="{PAD_X}" y="52" font-size="12">'
    f'<tspan fill="{USER_COLOR}">mahattva@github</tspan>'
    f'<tspan fill="{PROMPT_COLOR}">:~$ </tspan>'
    f'<tspan fill="#e6edf3">./welcome.sh</tspan>'
    f'</text>'
)
parts.append(f'<g clip-path="url(#cmdClip)">{cmd_rendered}</g>')
# Cursor for command line
parts.append(
    f'<rect x="{PAD_X}" y="41" width="7" height="13" fill="{CURSOR}" opacity="0">'
    f'<animate attributeName="x" from="{PAD_X}" to="{PAD_X + cmd_w}" begin="{CMD_START}s" dur="{CMD_DUR}s" fill="freeze"/>'
    f'<set attributeName="opacity" to="0.9" begin="{CMD_START}s"/>'
    f'<set attributeName="opacity" to="0" begin="{CMD_START + CMD_DUR}s"/>'
    f'</rect>'
)

# 3. ASCII banner text (5 lines) revealed left-to-right with tall cursor
banner_group = [f'<g clip-path="url(#bannerClip)">']
for ry, line in enumerate(lines):
    y = art_top + ry * CELL_H + CELL_H * 0.78
    safe = html.escape(line)
    banner_group.append(
        f'<text xml:space="preserve" x="{PAD_X}" y="{y:.1f}" fill="url(#bannerGrad)" '
        f'font-size="{font_size}" font-weight="700" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
    )
banner_group.append('</g>')
parts.extend(banner_group)

# Tall banner cursor riding the wipe edge
banner_total_h = len(lines) * CELL_H + 4
parts.append(
    f'<rect x="{PAD_X}" y="{art_top - 2}" width="10" height="{banner_total_h}" fill="{ACCENT}" opacity="0">'
    f'<animate attributeName="x" from="{PAD_X}" to="{PAD_X + ART_W}" begin="{BANNER_START}s" dur="{BANNER_DUR}s" fill="freeze"/>'
    f'<set attributeName="opacity" to="0.9" begin="{BANNER_START}s"/>'
    f'<set attributeName="opacity" to="0" begin="{BANNER_END}s"/>'
    f'</rect>'
)

# 4. Status divider line
sep_y = art_top + banner_total_h + 8
parts.append(f'<line x1="0" y1="{sep_y:.1f}" x2="{W}" y2="{sep_y:.1f}" stroke="{FRAME}" stroke-opacity="0.4"/>')

# 5. Bottom prompt line with pulsing/blinking cursor
bottom_y = sep_y + 19
status_chars = len("mahattva@github:~$ ACCESS GRANTED ")
parts.append(
    f'<g opacity="0">'
    f'<set attributeName="opacity" to="1" begin="{BOTTOM_START}s"/>'
    f'<text x="{PAD_X}" y="{bottom_y:.1f}" font-size="12">'
    f'<tspan fill="{USER_COLOR}">mahattva@github</tspan>'
    f'<tspan fill="{PROMPT_COLOR}">:~$ </tspan>'
    f'<tspan fill="{GREEN}" font-weight="700">ACCESS GRANTED</tspan>'
    f'<tspan fill="{PROMPT_COLOR}"> · </tspan>'
    f'<tspan fill="{TITLE_TEXT}">session active</tspan>'
    f'</text>'
    f'<rect x="{PAD_X + status_chars * 12 * 0.58:.1f}" y="{bottom_y - 10:.1f}" width="7" height="12" fill="{ACCENT}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
    f'</rect>'
    f'</g>'
)

parts.append("</svg>")
svg = "".join(parts)

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
