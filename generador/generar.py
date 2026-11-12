"""
Genera los recursos SVG del perfil de GitHub de TheCubick.

Uso:  python generar.py assets                 (usa a Gengar si existe assets/gengar.gif)
      python generar.py assets --mascota cubo   (vuelve al cubo "Cubick")
Todo es SVG: fuente pixel propia, mascota animada y tarjetas.
Para cambiar textos o colores, edita este archivo y vuelve a ejecutarlo.
Para Gengar hace falta Pillow (pip install pillow) y haber generado antes
assets/gengar.gif con sprite_a_gif.py.
"""
import base64
import html
import io
import os
import random
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = args[0] if args else "assets"
os.makedirs(OUT, exist_ok=True)
MASCOTA = "gengar" if os.path.exists(os.path.join(OUT, "gengar.gif")) else "cubo"
if "--mascota" in sys.argv:
    MASCOTA = sys.argv[sys.argv.index("--mascota") + 1]

# ----------------------------------------------------------------- paleta
C = dict(
    bg="#0d1117", bg2="#170f2c", card="#151221", card2="#1d1730", border="#2b2442",
    purple="#8b5cf6", lav="#c4b5fd", lav2="#ede9fe", deep="#6d28d9", ink="#1b1430",
    pink="#f472b6", cyan="#22d3ee", green="#34d399", amber="#fbbf24",
    text="#ece8f7", muted="#9a93b5",
)
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "Consolas,'SFMono-Regular','Liberation Mono',Menlo,monospace"

# ----------------------------------------------------------- fuente pixel
F = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["  ###", "    #", "    #", "    #", "#   #", "#   #", " ### "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["#   #", "#   #", "#   #", "#####", "    #", "    #", "    #"],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    " ": ["   "] * 7,
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    "-": ["    ", "    ", "    ", "####", "    ", "    ", "    "],
    "_": ["     "] * 6 + ["#####"],
    ".": [" "] * 6 + ["#"],
    ",": ["  "] * 5 + [" #", "# "],
    ":": [" ", "#", " ", " ", " ", "#", " "],
    "!": ["#", "#", "#", "#", "#", " ", "#"],
    "¡": ["#", " ", "#", "#", "#", "#", "#"],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    ">": ["#   ", " #  ", "  # ", "   #", "  # ", " #  ", "#   "],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "·": [" ", " ", " ", "#", " ", " ", " "],
}
ACUTE = ["   # ", "  #  "]
TILDE = [" ## #", "#  # "]
ACCENTED = {"Á": ("A", ACUTE), "É": ("E", ACUTE), "Í": ("I", ACUTE), "Ó": ("O", ACUTE),
            "Ú": ("U", ACUTE), "Ñ": ("N", TILDE)}


def glyph(ch):
    """Devuelve 9 filas (2 de acento + 7 de letra)."""
    ch = ch.upper()
    accent = ["", ""]
    if ch in ACCENTED:
        ch, accent = ACCENTED[ch]
    rows = F.get(ch, F["?"])
    w = len(rows[0])
    return [a.ljust(w) for a in accent] + rows, w


def rect(x, y, w, h):
    return f"M{x:g} {y:g}h{w:g}v{h:g}h{-w:g}z"


def ptext_d(text, x, y, s, gap=1):
    """Path 'd' de un texto en fuente pixel. y = parte superior de las mayúsculas."""
    d, cx = [], x
    for ch in text:
        rows, w = glyph(ch)
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                if v == "#":
                    d.append(rect(cx + c * s, y + (r - 2) * s, s, s))
        cx += (w + gap) * s
    return "".join(d), cx - x - gap * s


def ptext_w(text, s, gap=1):
    return sum((glyph(ch)[1] + gap) * s for ch in text) - gap * s


def ptext(text, x, y, s, fill, extra="", gap=1):
    d, _ = ptext_d(text, x, y, s, gap)
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def bitmap(rows, x, y, s, colors, extra=""):
    """Dibuja un bitmap; colors = {caracter: color}."""
    groups = {}
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v in colors:
                groups.setdefault(v, []).append(rect(x + c * s, y + r * s, s, s))
    return "".join(f'<path d="{"".join(d)}" fill="{colors[k]}" {extra}/>' for k, d in groups.items())


def esc(t):
    return html.escape(t, quote=True)


def svg(w, h, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">\n<style>{style}</style>\n{body}\n</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name:28s} {len(content) / 1024:6.1f} KB")


# ------------------------------------------------------------ iconos pixel
ICONS = {
    "smile": ([" ###### ", "########", "##o##o##", "########", "#o####o#", "##oooo##", "########", " ###### "],
              {"#": C["purple"], "o": C["ink"]}),
    "layers": (["  ####  ", "########", "  ####  ", "        ", "  aaaa  ", "aaaaaaaa", "  aaaa  ", "        "],
               {"#": C["lav"], "a": C["purple"]}),
    "folder": (["###     ", "#aa#####", "#aaaaaa#", "#aaaaaa#", "#aaaaaa#", "#aaaaaa#", "########", "        "],
               {"#": C["purple"], "a": C["deep"]}),
    "chart": (["      ##", "      ##", "   aa ##", "   aa ##", "pp aa ##", "pp aa ##", "pp aa ##", "########"],
              {"#": C["purple"], "a": C["lav"], "p": C["pink"]}),
    "mail": (["        ", "########", "#a####a#", "##a##a##", "###aa###", "########", "########", "        "],
             {"#": C["purple"], "a": C["lav2"]}),
    "spark": (["   #    ", "   #    ", "  ###   ", "#######", "  ###   ", "   #    ", "   #    ", "        "],
              {"#": C["pink"]}),
    "qr": (["###.#.###", "#.#..#.#.", "###.#.###", "..#.##...", "#.##..#.#", ".#..#.##.", "###..#.#.",
            "#.#.##..#", "###.#.##."], {"#": C["lav2"]}),
    "hand": (["  # # #  ", "  # # #  ", "  # # # #", "# ##### #", "# #######", "#########", " ########",
              "  ###### ", "   ####  "], {"#": C["lav2"]}),
    "shield": (["#########", "#aaa#aaa#", "#a#aaa#a#", "#aaa#aaa#", "#aaaaaaa#", " #aaaaa# ", "  #aaa#  ",
                "   #a#   ", "    #    "], {"#": C["lav2"], "a": C["purple"]}),
    "build": (["    #    ", "  #####  ", "#########", " #  #  # ", " #  #  # ", " #  #  # ", " #  #  # ",
               "#########", "#########"], {"#": C["lav2"]}),
}

# ------------------------------------------------------------- mascota cubo
def cube_svg_parts(ox, oy, s):
    """Cubo isométrico pixel art 'Cubick'. Devuelve (cuerpo, ojos_abiertos, ojos_cerrados, sombra)."""
    N = 24
    faces = {
        "t": [(12, 2), (21, 6.5), (12, 11), (3, 6.5)],
        "l": [(3, 6.5), (12, 11), (12, 20), (3, 15.5)],
        "r": [(12, 11), (21, 6.5), (21, 15.5), (12, 20)],
    }

    def inside(poly, x, y):
        n, ins = len(poly), False
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                ins = not ins
        return ins

    cells = {}
    for gy in range(N):
        for gx in range(N):
            for k, poly in faces.items():
                if inside(poly, gx + .5, gy + .5):
                    cells[(gx, gy)] = k
                    break
    col = {"t": C["lav"], "l": C["purple"], "r": C["deep"]}
    groups = {}
    for (gx, gy), k in cells.items():
        c = col[k]
        if k == "t" and (gx, gy - 1) not in cells:
            c = C["lav2"]                      # brillo en el borde superior
        if k == "l" and (gx - 1, gy) not in cells:
            c = "#a78bfa"                      # luz lateral izquierda
        if k == "r" and ((gx, gy - 1) in cells and cells[(gx, gy - 1)] == "t"):
            c = "#7c3aed"
        groups.setdefault(c, []).append(rect(ox + gx * s, oy + gy * s, s, s))
    # carita en la cara izquierda (sigue la pendiente isométrica)
    face = {"#2a1f47": [(5, 10), (5, 11), (9, 12), (9, 13)]}
    blush = [(4, 13), (10, 16)]
    mouth = [(6, 14), (7, 15), (8, 15)]
    for (gx, gy) in blush:
        groups.setdefault(C["pink"], []).append(rect(ox + gx * s, oy + gy * s, s, s))
    for (gx, gy) in mouth:
        groups.setdefault("#2a1f47", []).append(rect(ox + gx * s, oy + gy * s, s, s))
    body = "".join(f'<path d="{"".join(d)}" fill="{c}"/>' for c, d in groups.items())
    eyes = "".join(rect(ox + gx * s, oy + gy * s, s, s) for gx, gy in face["#2a1f47"])
    eyes_open = f'<path class="eyes" d="{eyes}" fill="#2a1f47"/>'
    # destello blanco en los ojos
    glint = "".join(rect(ox + gx * s + s * .5, oy + gy * s, s * .5, s * .5) for gx, gy in [(5, 10), (9, 12)])
    eyes_open += f'<path class="eyes" d="{glint}" fill="#ffffff"/>'
    shadow = "".join(rect(ox + gx * s, oy + 22 * s, s, s) for gx in range(6, 18))
    shadow += "".join(rect(ox + gx * s, oy + 23 * s, s, s) for gx in range(8, 16))
    return body, eyes_open, f'<path class="shadow" d="{shadow}" fill="{C["purple"]}" opacity=".22"/>'


CUBE_CSS = """
.bob{animation:bob 2.6s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.shadow{animation:shadow 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes shadow{0%,100%{transform:scaleX(1);opacity:.22}50%{transform:scaleX(.8);opacity:.12}}
.eyes{animation:blink 4.2s infinite;transform-box:fill-box;transform-origin:center}
@keyframes blink{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
.tw{animation:tw 2.4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
"""


def cube(ox, oy, s):
    body, eyes, shadow = cube_svg_parts(ox, oy, s)
    return f'{shadow}<g class="bob">{body}{eyes}</g>'


# ------------------------------------------------------ mascota Gengar (GIF)
_GENGAR = None


def load_gengar():
    """Lee los cuadros de assets/gengar.gif como PNG en base64, con su duración."""
    global _GENGAR
    if _GENGAR is None:
        from PIL import Image
        im = Image.open(os.path.join(OUT, "gengar.gif"))
        frames = []
        for i in range(im.n_frames):
            im.seek(i)
            buf = io.BytesIO()
            im.convert("RGBA").save(buf, "PNG", optimize=True)
            frames.append((base64.b64encode(buf.getvalue()).decode(), im.info.get("duration", 120)))
        _GENGAR = (frames, im.size)
    return _GENGAR


def gengar(cx, bottom, w, uid):
    """Gengar animado cuadro por cuadro y flotando. Devuelve (svg, css)."""
    frames, (gw, gh) = load_gengar()
    h = w * gh / gw
    x, y = cx - w / 2, bottom - h
    total = sum(d for _, d in frames)
    css, imgs, t = [], [], 0
    for i, (b64, d) in enumerate(frames):
        s, e = t / total * 100, (t + d) / total * 100
        t += d
        if i == 0:
            kf = f"0%{{opacity:1}}{e:.2f}%{{opacity:0}}100%{{opacity:0}}"
        else:
            kf = f"0%{{opacity:0}}{s:.2f}%{{opacity:1}}{e:.2f}%{{opacity:0}}100%{{opacity:0}}"
        css.append(f".{uid}{i}{{animation:{uid}{i} {total / 1000:.2f}s step-end infinite}}@keyframes {uid}{i}{{{kf}}}")
        imgs.append(f'<image class="{uid}{i}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                    f'opacity="{1 if i == 0 else 0}" style="image-rendering:pixelated" href="data:image/png;base64,{b64}"/>')
    sw = round(w * .5 / 6) * 6
    shadow = rect(cx - sw / 2, bottom + 2, sw, 6) + rect(cx - sw / 2 + 12, bottom + 8, sw - 24, 6)
    svg_ = (f'<path class="shadow" d="{shadow}" fill="{C["purple"]}" opacity=".22"/>'
            f'<g class="bob">{"".join(imgs)}</g>')
    return svg_, " ".join(css)


def mascot(cx, bottom, w, uid):
    """La mascota elegida: Gengar (GIF) o el cubo pixel art. Devuelve (svg, css)."""
    if MASCOTA == "gengar":
        return gengar(cx, bottom, w, uid)
    s = round(w / 24)
    return cube(cx - 12 * s, bottom - 22 * s, s), ""


def sparkle(x, y, s, color, delay=0.0):
    rows = ["  #  ", "  #  ", "#####", "  #  ", "  #  "]
    return bitmap(rows, x, y, s, {"#": color}, extra=f'class="tw" style="animation-delay:{delay}s"')


# ============================================================== BANNER
def banner():
    W, H = 1200, 340
    rnd = random.Random(7)
    b = [f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg"]}"/><stop offset="1" stop-color="{C["bg2"]}"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".45"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient>
<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{C["purple"]}"/><stop offset=".6" stop-color="{C["pink"]}"/><stop offset="1" stop-color="{C["pink"]}" stop-opacity="0"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>''']
    # estrellas pixel
    for i in range(80):
        x, y = rnd.randint(10, W - 10), rnd.randint(10, H - 70)
        sz = rnd.choice([2, 2, 3, 4])
        colr = rnd.choice([C["lav"], C["lav2"], C["pink"], "#ffffff"])
        tw = f' class="tw" style="animation-delay:{rnd.random() * 2.4:.2f}s"' if i % 3 == 0 else ""
        b.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{colr}" opacity="{rnd.uniform(.25, .8):.2f}"{tw}/>')
    # piso synthwave sutil
    for i, y in enumerate([288, 297, 308, 321, 336]):
        b.append(f'<rect x="0" y="{y}" width="{W}" height="2" fill="{C["purple"]}" opacity="{.10 + i * .03:.2f}"/>')
    for x in range(-600, 1800, 120):
        b.append(f'<line x1="{960 + (x - 960) * .25:.0f}" y1="280" x2="{x}" y2="{H}" stroke="{C["purple"]}" stroke-opacity=".12" stroke-width="2" shape-rendering="auto"/>')
    b.append(f'<rect x="0" y="278" width="{W}" height="3" fill="url(#line)" opacity=".7"/>')
    # textos
    b.append(ptext("> HOLA, SOY", 70, 62, 3, C["pink"]))
    b.append(ptext("PABLO RAMÍREZ", 76, 112, 8, C["deep"]))
    b.append(ptext("PABLO RAMÍREZ", 70, 106, 8, C["text"]))
    sub = "FULL-STACK DEV  //  COMPUTER VISION"
    b.append(ptext(sub, 72, 196, 3, C["lav"]))
    cx = 72 + ptext_w(sub, 3) + 10
    b.append(f'<rect x="{cx}" y="193" width="12" height="24" fill="{C["pink"]}" class="cursor"/>')
    # chips
    chips = [("CHIAPAS, MX", C["muted"], None), ("ING. EN SISTEMAS", C["muted"], None),
             ("ABIERTO A PRÁCTICAS", C["green"], C["green"])]
    x = 72
    for label, colr, dot in chips:
        tw = ptext_w(label, 2)
        pad = 14 + (16 if dot else 0)
        w = tw + pad + 14
        b.append(f'<rect x="{x}" y="232" width="{w}" height="30" rx="8" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>')
        tx = x + 14
        if dot:
            b.append(f'<rect x="{tx}" y="243" width="8" height="8" fill="{dot}" class="pulse"/>')
            tx += 16
        b.append(ptext(label, tx, 240, 2, colr))
        x += w + 12
    # mascota + brillo
    b.append(f'<ellipse cx="985" cy="150" rx="190" ry="150" fill="url(#glow)"/>')
    m_svg, m_css = mascot(985, 226, 224, "gb")
    b.append(m_svg)
    b.append(sparkle(830, 60, 5, C["pink"], 0))
    b.append(sparkle(1110, 40, 4, C["lav"], .8))
    b.append(sparkle(1130, 190, 5, C["cyan"], 1.4))
    b.append(sparkle(845, 205, 3, C["lav2"], 1.9))
    style = CUBE_CSS + m_css + """
.cursor{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}
.pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.25}}
"""
    save("banner.svg", svg(W, H, "\n".join(b), style))


# ======================================================== MASCOTA SOLA
def mascota():
    W, H = 300, 300
    m_svg, m_css = mascot(150, 212, 208, "gm")
    name = "GENGAR" if MASCOTA == "gengar" else "CUBICK"
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<defs><radialGradient id="g" cx=".5" cy=".45" r=".5"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".35"/>'
         f'<stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="150" cy="135" r="125" fill="url(#g)"/>',
         m_svg,
         sparkle(28, 40, 4, C["pink"], 0), sparkle(250, 70, 4, C["lav"], .9), sparkle(240, 200, 3, C["cyan"], 1.6),
         ptext(name, 150 - ptext_w(name, 3) // 2, 262, 3, C["lav"])]
    save("mascota.svg", svg(W, H, "\n".join(b), CUBE_CSS + m_css))


# ================================================ ENCABEZADOS DE SECCIÓN
def header(name, icon, title, subtitle):
    W, H = 1000, 88
    rows, colors = ICONS[icon]
    b = [f'<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{C["purple"]}"/>'
         f'<stop offset=".5" stop-color="{C["pink"]}"/><stop offset="1" stop-color="{C["pink"]}" stop-opacity="0"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="16" fill="{C["card"]}"/>',
         f'<rect x="20" y="16" width="56" height="56" rx="12" fill="{C["card2"]}" stroke="{C["border"]}" stroke-width="2"/>',
         bitmap(rows, 28, 24, 5, colors),
         ptext(title, 98, 27, 5, C["text"])]
    tx = 98 + ptext_w(title, 5) + 22
    b.append(f'<text x="{tx}" y="58" font-family="{MONO}" font-size="18" fill="{C["muted"]}">{esc(subtitle)}</text>')
    b.append(f'<rect x="20" y="{H - 5}" width="{W - 40}" height="3" fill="url(#l)"/>')
    save(f"titulo-{name}.svg", svg(W, H, "\n".join(b)))


# ================================================================ BENTO
def wrap(text, maxc):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + ([cur] if cur else [])


def pills(items, x0, y0, maxw, size=15, h=36, gap=10, stroke=C["purple"], fill="none", color=C["lav"], cw=8.1):
    out, x, y = [], x0, y0
    for it in items:
        w = len(it) * cw + 30
        if x + w > x0 + maxw:
            x, y = x0, y + h + gap
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h // 2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out.append(f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * .35:.0f}" text-anchor="middle" font-family="{SANS}" '
                   f'font-size="{size}" font-weight="600" fill="{color}">{esc(it)}</text>')
        x += w + gap
    return "".join(out)


def bento():
    W, H = 1000, 600
    b = [f'''<defs>
<linearGradient id="mis" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1656"/><stop offset=".55" stop-color="#3b1660"/><stop offset="1" stop-color="#5a1748"/></linearGradient>
<radialGradient id="blob" cx=".85" cy=".2" r=".6"><stop offset="0" stop-color="{C["pink"]}" stop-opacity=".35"/><stop offset="1" stop-color="{C["pink"]}" stop-opacity="0"/></radialGradient>
</defs>''']
    # --- STATUS
    b.append(f'<rect x="0" y="0" width="380" height="270" rx="22" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>')
    b.append(ptext("STATUS", 30, 32, 3, C["muted"]))
    b.append(f'<rect x="30" y="78" width="16" height="16" fill="{C["green"]}" class="pulse"/>')
    b.append(f'<rect x="26" y="74" width="24" height="24" fill="none" stroke="{C["green"]}" stroke-width="2" opacity=".4" class="pulse"/>')
    b.append(ptext("DISPONIBLE", 64, 72, 4, C["green"]))
    b.append(f'<text x="30" y="138" font-family="{SANS}" font-size="19" font-weight="600" fill="{C["text"]}">Buscando prácticas / internship</text>')
    for i, t in enumerate(["Chiapas, México", "Ing. en Sistemas · IESCH", "Full-Stack + Computer Vision"]):
        y = 178 + i * 30
        b.append(f'<rect x="30" y="{y - 11}" width="8" height="8" fill="{C["purple"]}"/>')
        b.append(f'<text x="50" y="{y}" font-family="{MONO}" font-size="16" fill="{C["muted"]}">{esc(t)}</text>')
    # --- SUPERPODERES
    b.append(f'<rect x="400" y="0" width="600" height="270" rx="22" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>')
    b.append(ptext("SUPERPODERES", 430, 32, 3, C["muted"]))
    b.append(bitmap(ICONS["spark"][0], 940, 26, 4, ICONS["spark"][1]))
    b.append(pills(["Full-Stack", "Visión por computadora", "Liderazgo de equipos", "Arquitectura de software",
                    "Sistemas en tiempo real", "UI / UX", "Producto digital", "Docker"], 430, 74, 540))
    # --- MISIÓN
    b.append(f'<rect x="0" y="290" width="1000" height="310" rx="22" fill="url(#mis)"/>')
    b.append(f'<rect x="0" y="290" width="1000" height="310" rx="22" fill="url(#blob)"/>')
    b.append(ptext("MI MISIÓN", 30, 324, 3, C["lav"]))
    b.append(f'<text x="30" y="404" font-family="{SANS}" font-size="34" font-weight="800" fill="#ffffff">'
             f'La tecnología solo es buena si llega a todos.</text>')
    cols = [("hand", "ACCESIBILIDAD", "IA que traduce la Lengua", "de Señas Mexicana"),
            ("qr", "NEGOCIOS LOCALES", "SaaS para restaurantes", "sin cobrar comisiones"),
            ("build", "INSTITUCIONES", "Trámites y accesos,", "por fin digitales")]
    for i, (ic, t, l1, l2) in enumerate(cols):
        x = 30 + i * 320
        b.append(f'<rect x="{x}" y="440" width="300" height="130" rx="16" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".12" stroke-width="2"/>')
        b.append(f'<rect x="{x + 18}" y="458" width="52" height="52" rx="12" fill="{C["ink"]}" fill-opacity=".6"/>')
        b.append(bitmap(ICONS[ic][0], x + 22, 462, 5, ICONS[ic][1]))
        b.append(ptext(t, x + 86, 470, 2, "#ffffff"))
        b.append(f'<text x="{x + 86}" y="510" font-family="{SANS}" font-size="15" fill="{C["lav2"]}" fill-opacity=".85">{esc(l1)}</text>')
        b.append(f'<text x="{x + 86}" y="531" font-family="{SANS}" font-size="15" fill="{C["lav2"]}" fill-opacity=".85">{esc(l2)}</text>')
    style = ".pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.3}}"
    save("bento.svg", svg(W, H, "\n".join(b), style))


# ======================================================= TARJETAS PROYECTO
PROJECTS = [
    ("qrico", "01", "qr", "Q-RICO", ("EN PRODUCCIÓN", C["green"]),
     "SaaS de menús QR para restaurantes. El comensal pide desde su mesa sin instalar nada y el pedido llega al instante a cocina, caja y piso.",
     ["JavaScript", "PWA", "POS / KDS", "Tiempo real"], "qrico-web.onrender.com"),
    ("lsm", "02", "hand", "TRADUCTOR LSM", ("IA · TIEMPO REAL", C["cyan"]),
     "Traduce el alfabeto de la Lengua de Señas Mexicana a texto y voz con una cámara web. Lee dos manos a la vez y gestos del rostro.",
     ["Python", "MediaPipe", "OpenCV", "FastAPI"], "visión por computadora"),
    ("registro", "03", "shield", "REGISTRO Y CONTROL", ("EN DESARROLLO", C["amber"]),
     "App full-stack para registrar y auditar la entrada de personas y vehículos a un edificio, con bitácora de visitas y gafetes.",
     ["Laravel", "React", "Inertia", "PostgreSQL", "Docker"], "full-stack · MVC"),
    ("colegio", "04", "build", "PORTAL COLEGIO", ("LÍDER DE EQUIPO", C["pink"]),
     "Portal institucional del Colegio de Ingenieros Civiles de Tuxtla: trámites, servicios y eventos reunidos en un solo lugar.",
     ["React", "Vite", "Framer Motion", "Router"], "equipo de 5 personas"),
]


def project_card(key, num, icon, title, chip, desc, tags, foot):
    W, H = 500, 310
    rows, colors = ICONS[icon]
    chip_t, chip_c = chip
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<rect x="26" y="26" width="64" height="64" rx="14" fill="{C["card2"]}" stroke="{C["border"]}" stroke-width="2"/>',
         bitmap(rows, 35, 35, 5, colors),
         ptext("PROYECTO " + num, 108, 28, 2, C["muted"]),
         ptext(title, 108, 46, 3, C["text"])]
    cw = len(chip_t) * 8.6 + 40
    b.append(f'<rect x="108" y="74" width="{cw:.0f}" height="26" rx="13" fill="{chip_c}" fill-opacity=".14" stroke="{chip_c}" stroke-opacity=".55" stroke-width="1.5"/>')
    b.append(f'<rect x="120" y="84" width="7" height="7" fill="{chip_c}"/>')
    b.append(f'<text x="134" y="92" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing=".6" fill="{chip_c}">{esc(chip_t)}</text>')
    for i, line in enumerate(wrap(desc, 54)):
        b.append(f'<text x="26" y="{140 + i * 24}" font-family="{SANS}" font-size="16" fill="{C["muted"]}">{esc(line)}</text>')
    b.append(pills(tags, 26, 216, 450, size=13, h=28, gap=8, stroke=C["border"], fill=C["card2"], color=C["lav"], cw=7.2))
    b.append(f'<rect x="26" y="262" width="{W - 52}" height="1.5" fill="{C["border"]}"/>')
    b.append(f'<text x="26" y="290" font-family="{MONO}" font-size="14" fill="{C["muted"]}">{esc(foot)}</text>')
    b.append(f'<text x="{W - 26}" y="290" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{C["pink"]}">ver repo -&gt;</text>')
    save(f"proyecto-{key}.svg", svg(W, H, "\n".join(b)))


# ================================================================ FOOTER
def footer():
    W, H = 1000, 210
    m_svg, m_css = mascot(146, 168, 168, "gf")
    b = [f'<rect width="{W}" height="{H}" rx="22" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<defs><radialGradient id="g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["purple"]}" stop-opacity=".35"/>'
         f'<stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="140" cy="100" r="105" fill="url(#g)"/>',
         m_svg,
         sparkle(40, 30, 3, C["pink"], 0), sparkle(250, 40, 3, C["lav"], 1.1),
         ptext("¡GRACIAS POR VISITAR!", 290, 66, 5, C["text"]),
         f'<text x="292" y="132" font-family="{MONO}" font-size="19" fill="{C["muted"]}">nos vemos en el próximo commit</text>',
         f'<rect x="{292 + 30 * 10.5:.0f}" y="116" width="11" height="20" fill="{C["pink"]}" class="cursor"/>',
         ptext("HECHO EN CHIAPAS, MX", 292, 160, 2, C["purple"])]
    style = CUBE_CSS + m_css + ".cursor{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}"
    save("footer.svg", svg(W, H, "\n".join(b), style))


if __name__ == "__main__":
    print(f"Generando en {OUT}/  (mascota: {MASCOTA})")
    banner()
    mascota()
    header("sobre-mi", "smile", "SOBRE MÍ", "// quién soy")
    header("stack", "layers", "STACK", "// con qué construyo")
    header("proyectos", "folder", "PROYECTOS", "// lo que he lanzado")
    header("stats", "chart", "ACTIVIDAD", "// mi github en números")
    header("contacto", "mail", "CONTACTO", "// hablemos")
    bento()
    for p in PROJECTS:
        project_card(*p)
    footer()
