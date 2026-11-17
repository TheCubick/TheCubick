"""
Genera los recursos SVG del perfil de GitHub de TheCubick.

Uso:  python generar.py assets                    (mascota por defecto: Squirtle)
      python generar.py assets --mascota gengar    (Gengar, necesita assets/gengar.gif)
      python generar.py assets --mascota cubo      (el cubo "Cubick")
Todo es SVG: fuente pixel propia, mascota animada y tarjetas.
Para cambiar textos o colores, edita este archivo y vuelve a ejecutarlo.
Para Squirtle y Gengar hace falta Pillow (pip install pillow):
  - Squirtle: cuadros PNG en generador/squirtle/ (se crean con gif_a_transparente.py)
  - Gengar:   assets/gengar.gif (se crea con sprite_a_gif.py)
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
HERE = os.path.dirname(os.path.abspath(__file__))
SQUIRTLE_DIR = os.path.join(HERE, "squirtle")
if os.path.isdir(SQUIRTLE_DIR):
    MASCOTA = "squirtle"
elif os.path.exists(os.path.join(OUT, "gengar.gif")):
    MASCOTA = "gengar"
else:
    MASCOTA = "cubo"
if "--mascota" in sys.argv:
    MASCOTA = sys.argv[sys.argv.index("--mascota") + 1]

# ----------------------------------------------------------------- paleta
# Ancho común de todas las piezas: en el móvil de GitHub el README mide ~293 px, así que
# 560 px de diseño (escala ~0.52) con letras grandes se sigue leyendo.
W0 = 560

C = dict(
    # Squirtle sobre fondo azul petróleo: esmeralda (#10b981) y celeste (#38bdf8) como acentos,
    # con el naranja del caparazón solo en detalles pequeños.
    bg="#0d1117", bg2="#0a1216", card="#0d161a", card2="#14242a", border="#1f3a42",
    aqua="#10b981", lav="#9be7cc", lav2="#e6f3f1", deep="#0b6e5a", ink="#081014",
    shell="#f59e42", cyan="#38bdf8", green="#34d399", cream="#f3d98b",
    text="#e6f3f1", muted="#9db6ba",
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
              {"#": C["aqua"], "o": C["ink"]}),
    "layers": (["  ####  ", "########", "  ####  ", "        ", "  aaaa  ", "aaaaaaaa", "  aaaa  ", "        "],
               {"#": C["lav"], "a": C["aqua"]}),
    "folder": (["###     ", "#aa#####", "#aaaaaa#", "#aaaaaa#", "#aaaaaa#", "#aaaaaa#", "########", "        "],
               {"#": C["aqua"], "a": C["deep"]}),
    "chart": (["      ##", "      ##", "   aa ##", "   aa ##", "pp aa ##", "pp aa ##", "pp aa ##", "########"],
              {"#": C["aqua"], "a": C["lav"], "p": C["shell"]}),
    "mail": (["        ", "########", "#a####a#", "##a##a##", "###aa###", "########", "########", "        "],
             {"#": C["aqua"], "a": C["lav2"]}),
    "spark": (["   #    ", "   #    ", "  ###   ", "#######", "  ###   ", "   #    ", "   #    ", "        "],
              {"#": C["shell"]}),
    "qr": (["###.#.###", "#.#..#.#.", "###.#.###", "..#.##...", "#.##..#.#", ".#..#.##.", "###..#.#.",
            "#.#.##..#", "###.#.##."], {"#": C["lav2"]}),
    "hand": (["  # # #  ", "  # # #  ", "  # # # #", "# ##### #", "# #######", "#########", " ########",
              "  ###### ", "   ####  "], {"#": C["lav2"]}),
    "shield": (["#########", "#aaa#aaa#", "#a#aaa#a#", "#aaa#aaa#", "#aaaaaaa#", " #aaaaa# ", "  #aaa#  ",
                "   #a#   ", "    #    "], {"#": C["lav2"], "a": C["aqua"]}),
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
    col = {"t": C["lav"], "l": C["aqua"], "r": C["deep"]}
    groups = {}
    for (gx, gy), k in cells.items():
        c = col[k]
        if k == "t" and (gx, gy - 1) not in cells:
            c = C["lav2"]                      # brillo en el borde superior
        if k == "l" and (gx - 1, gy) not in cells:
            c = "#8fe3d6"                      # luz lateral izquierda
        if k == "r" and ((gx, gy - 1) in cells and cells[(gx, gy - 1)] == "t"):
            c = "#2a9d9d"
        groups.setdefault(c, []).append(rect(ox + gx * s, oy + gy * s, s, s))
    # carita en la cara izquierda (sigue la pendiente isométrica)
    face = {"#1a2e33": [(5, 10), (5, 11), (9, 12), (9, 13)]}
    blush = [(4, 13), (10, 16)]
    mouth = [(6, 14), (7, 15), (8, 15)]
    for (gx, gy) in blush:
        groups.setdefault(C["shell"], []).append(rect(ox + gx * s, oy + gy * s, s, s))
    for (gx, gy) in mouth:
        groups.setdefault("#1a2e33", []).append(rect(ox + gx * s, oy + gy * s, s, s))
    body = "".join(f'<path d="{"".join(d)}" fill="{c}"/>' for c, d in groups.items())
    eyes = "".join(rect(ox + gx * s, oy + gy * s, s, s) for gx, gy in face["#1a2e33"])
    eyes_open = f'<path class="eyes" d="{eyes}" fill="#1a2e33"/>'
    # destello blanco en los ojos
    glint = "".join(rect(ox + gx * s + s * .5, oy + gy * s, s * .5, s * .5) for gx, gy in [(5, 10), (9, 12)])
    eyes_open += f'<path class="eyes" d="{glint}" fill="#ffffff"/>'
    shadow = "".join(rect(ox + gx * s, oy + 22 * s, s, s) for gx in range(6, 18))
    shadow += "".join(rect(ox + gx * s, oy + 23 * s, s, s) for gx in range(8, 16))
    return body, eyes_open, f'<path class="shadow" d="{shadow}" fill="{C["aqua"]}" opacity=".22"/>'


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


def load_squirtle():
    """Lee los PNG de generador/squirtle/ como base64, con la duración de cada cuadro."""
    global _SQUIRTLE
    if _SQUIRTLE is None:
        from PIL import Image
        names = sorted(n for n in os.listdir(SQUIRTLE_DIR) if n.endswith(".png"))
        with open(os.path.join(SQUIRTLE_DIR, "duraciones.txt")) as fh:
            durs = [int(x) for x in fh.read().split()]
        frames = []
        for n, d in zip(names, durs):
            with open(os.path.join(SQUIRTLE_DIR, n), "rb") as fh:
                frames.append((base64.b64encode(fh.read()).decode(), d))
        _SQUIRTLE = (frames, Image.open(os.path.join(SQUIRTLE_DIR, names[0])).size)
    return _SQUIRTLE


_SQUIRTLE = None


def gengar(cx, bottom, w, uid):
    """Mascota en cuadros (Squirtle o Gengar), animada cuadro por cuadro. Devuelve (svg, css)."""
    smooth = MASCOTA == "squirtle"
    frames, (gw, gh) = load_squirtle() if smooth else load_gengar()
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
                    f'opacity="{1 if i == 0 else 0}"{"" if smooth else " style=" + chr(34) + "image-rendering:pixelated" + chr(34)} href="data:image/png;base64,{b64}"/>')
    sw = round(w * .5 / 6) * 6
    shadow = rect(cx - sw / 2, bottom + 2, sw, 6) + rect(cx - sw / 2 + 12, bottom + 8, sw - 24, 6)
    svg_ = (f'<path class="shadow" d="{shadow}" fill="{C["aqua"]}" opacity=".22"/>'
            f'<g{"" if smooth else " class=" + chr(34) + "bob" + chr(34)}>{"".join(imgs)}</g>')
    return svg_, " ".join(css)


def mascot(cx, bottom, w, uid):
    """La mascota elegida: Gengar (GIF) o el cubo pixel art. Devuelve (svg, css)."""
    if MASCOTA in ("squirtle", "gengar"):
        return gengar(cx, bottom, w, uid)
    s = round(w / 24)
    return cube(cx - 12 * s, bottom - 22 * s, s), ""


def sparkle(x, y, s, color, delay=0.0):
    rows = ["  #  ", "  #  ", "#####", "  #  ", "  #  "]
    return bitmap(rows, x, y, s, {"#": color}, extra=f'class="tw" style="animation-delay:{delay}s"')


# ============================================================== BANNER
def chip(x, y, label, color=None, dot=None, size=16):
    w = len(label) * size * .54 + 28 + (18 if dot else 0)
    out = [f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="10" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>']
    tx = x + 14
    if dot:
        out.append(f'<rect x="{tx}" y="{y + 13}" width="8" height="8" fill="{dot}" class="pulse"/>')
        tx += 18
    out.append(f'<text x="{tx}" y="{y + 22}" font-family="{SANS}" font-size="{size}" font-weight="600" fill="{color or C["muted"]}">{esc(label)}</text>')
    return "".join(out), w


def banner():
    W, H = W0, 380
    rnd = random.Random(7)
    b = ['<defs>'
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg2"]}"/><stop offset="1" stop-color="{C["card"]}"/></linearGradient>'
         f'<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["aqua"]}" stop-opacity=".34"/><stop offset="1" stop-color="{C["aqua"]}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{C["aqua"]}"/><stop offset=".6" stop-color="{C["cyan"]}"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></linearGradient>'
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>']
    # estrellas pixel
    for i in range(55):
        x, y = rnd.randint(10, W - 10), rnd.randint(10, H - 90)
        sz = rnd.choice([2, 2, 3, 4])
        colr = rnd.choice([C["lav"], C["lav2"], C["cyan"], "#ffffff"])
        tw = f' class="tw" style="animation-delay:{rnd.random() * 2.4:.2f}s"' if i % 3 == 0 else ""
        b.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{colr}" opacity="{rnd.uniform(.25, .8):.2f}"{tw}/>')
    # piso synthwave sutil
    hz = 336
    for i, y in enumerate([344, 353, 364]):
        b.append(f'<rect x="0" y="{y}" width="{W}" height="2" fill="{C["aqua"]}" opacity="{.12 + i * .04:.2f}"/>')
    for x in range(-500, 1300, 90):
        b.append(f'<line x1="{450 + (x - 450) * .25:.0f}" y1="{hz + 2}" x2="{x}" y2="{H}" stroke="{C["aqua"]}" stroke-opacity=".14" stroke-width="2" shape-rendering="auto"/>')
    b.append(f'<rect x="0" y="{hz - 2}" width="{W}" height="3" fill="url(#line)" opacity=".7"/>')
    # textos (todo en bloques grandes para que se lea en el móvil)
    b.append(ptext("> HOLA, SOY", 40, 32, 3, C["shell"]))
    b.append(ptext("PABLO RAMÍREZ", 46, 82, 6, C["deep"]))
    b.append(ptext("PABLO RAMÍREZ", 40, 76, 6, C["text"]))
    b.append(ptext("FULL-STACK DEV", 40, 150, 3, C["lav"]))
    l2 = "COMPUTER VISION"
    b.append(ptext(l2, 40, 182, 3, C["lav"]))
    b.append(f'<rect x="{40 + ptext_w(l2, 3) + 10}" y="180" width="12" height="25" fill="{C["shell"]}" class="cursor"/>')
    c1, _ = chip(40, 238, "Ing. en Sistemas · Chiapas, MX")
    c2, _ = chip(40, 282, "Abierto a prácticas", C["green"], C["green"])
    b += [c1, c2]
    # mascota + brillo
    b.append(f'<ellipse cx="452" cy="250" rx="150" ry="130" fill="url(#glow)"/>')
    m_svg, m_css = mascot(452, 326, 196, "gb")
    b.append(m_svg)
    b.append(sparkle(350, 146, 5, C["shell"], 0))
    b.append(sparkle(535, 128, 4, C["lav"], .8))
    b.append(sparkle(540, 240, 5, C["cyan"], 1.4))
    b.append(sparkle(362, 300, 3, C["lav2"], 1.9))
    style = CUBE_CSS + m_css + """
.cursor{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}
.pulse{animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.25}}
"""
    save("banner.svg", svg(W, H, "\n".join(b), style))


# ======================================================== MASCOTA SOLA
def mascota():
    W, H = 300, 300
    m_svg, m_css = mascot(150, 212, 208, "gm")
    name = {"squirtle": "SQUIRTLE", "gengar": "GENGAR"}.get(MASCOTA, "CUBICK")
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<defs><radialGradient id="g" cx=".5" cy=".45" r=".5"><stop offset="0" stop-color="{C["aqua"]}" stop-opacity=".35"/>'
         f'<stop offset="1" stop-color="{C["aqua"]}" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="150" cy="135" r="125" fill="url(#g)"/>',
         m_svg,
         sparkle(28, 40, 4, C["shell"], 0), sparkle(250, 70, 4, C["lav"], .9), sparkle(240, 200, 3, C["cyan"], 1.6),
         ptext(name, 150 - ptext_w(name, 3) // 2, 262, 3, C["lav"])]
    save("mascota.svg", svg(W, H, "\n".join(b), CUBE_CSS + m_css))


# ================================================ ENCABEZADOS DE SECCIÓN
def header(name, icon, title, subtitle):
    W, H = W0, 64
    rows, colors = ICONS[icon]
    b = [f'<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{C["aqua"]}"/>'
         f'<stop offset=".5" stop-color="{C["cyan"]}"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="16" fill="{C["card"]}"/>',
         f'<rect x="14" y="9" width="44" height="44" rx="10" fill="{C["card2"]}" stroke="{C["border"]}" stroke-width="2"/>',
         bitmap(rows, 16, 11, 5, colors),
         ptext(title, 72, 24, 4, C["text"])]
    tx = 72 + ptext_w(title, 4) + 20
    b.append(f'<text x="{tx}" y="44" font-family="{MONO}" font-size="16" fill="{C["muted"]}">{esc(subtitle)}</text>')
    b.append(f'<rect x="14" y="{H - 6}" width="{W - 28}" height="3" fill="url(#l)"/>')
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


def pills(items, x0, y0, maxw, size=16, h=36, gap=10, stroke=None, fill="none", color=None, cw=8.8):
    stroke = stroke or C["aqua"]
    color = color or C["lav"]
    out, x, y = [], x0, y0
    for it in items:
        w = len(it) * cw + 30
        if x + w > x0 + maxw and x > x0:
            x, y = x0, y + h + gap
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h // 2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out.append(f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * .35:.0f}" text-anchor="middle" font-family="{SANS}" '
                   f'font-size="{size}" font-weight="600" fill="{color}">{esc(it)}</text>')
        x += w + gap
    return "".join(out), y + h


def bento():
    W = W0
    b = [f'<defs>'
         f'<linearGradient id="mis" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a3a35"/><stop offset=".55" stop-color="#0c4658"/><stop offset="1" stop-color="#6b3b14"/></linearGradient>'
         f'<radialGradient id="blob" cx=".9" cy=".1" r=".6"><stop offset="0" stop-color="{C["shell"]}" stop-opacity=".30"/><stop offset="1" stop-color="{C["shell"]}" stop-opacity="0"/></radialGradient>'
         f'</defs>']
    card = f'fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"'
    # ---- STATUS
    y0, h = 0, 246
    b.append(f'<rect x="1" y="{y0 + 1}" width="{W - 2}" height="{h - 2}" rx="22" {card}/>')
    b.append(ptext("STATUS", 28, 26, 3, C["muted"]))
    b.append(f'<rect x="28" y="72" width="18" height="18" fill="{C["green"]}" class="pulse"/>')
    b.append(f'<rect x="24" y="68" width="26" height="26" fill="none" stroke="{C["green"]}" stroke-width="2" opacity=".4" class="pulse"/>')
    b.append(ptext("DISPONIBLE", 62, 66, 5, C["green"]))
    b.append(f'<text x="28" y="138" font-family="{SANS}" font-size="22" font-weight="700" fill="{C["text"]}">Buscando prácticas / internship</text>')
    for i, t in enumerate(["Chiapas, México", "Ing. en Sistemas · IESCH", "Full-Stack + Computer Vision"]):
        y = 172 + i * 26
        b.append(f'<rect x="28" y="{y - 11}" width="9" height="9" fill="{C["aqua"]}"/>')
        b.append(f'<text x="50" y="{y}" font-family="{MONO}" font-size="17" fill="{C["muted"]}">{esc(t)}</text>')
    # ---- SUPERPODERES
    y0 = h + 16
    b.append(ptext("SUPERPODERES", 28, y0 + 26, 3, C["muted"]))
    b.append(bitmap(ICONS["spark"][0], W - 64, y0 + 20, 4, ICONS["spark"][1]))
    p_svg, p_bot = pills(["Full-Stack", "Visión por computadora", "Liderazgo de equipos", "Arquitectura de software",
                          "Sistemas en tiempo real", "UI / UX", "Producto digital", "Docker"], 28, y0 + 64, W - 56)
    h2 = p_bot - y0 + 22
    b.insert(1, f'<rect x="1" y="{y0 + 1}" width="{W - 2}" height="{h2 - 2}" rx="22" {card}/>')
    b.append(p_svg)
    # ---- MISIÓN
    y0 = y0 + h2 + 16
    cols = [("hand", "ACCESIBILIDAD", "IA que traduce la Lengua", "de Señas Mexicana"),
            ("qr", "NEGOCIOS LOCALES", "SaaS para restaurantes", "sin cobrar comisiones"),
            ("build", "INSTITUCIONES", "Trámites y accesos,", "por fin digitales")]
    h3 = 154 + len(cols) * 108 + 6
    b.append(f'<rect x="0" y="{y0}" width="{W}" height="{h3}" rx="22" fill="url(#mis)"/>')
    b.append(f'<rect x="0" y="{y0}" width="{W}" height="{h3}" rx="22" fill="url(#blob)"/>')
    b.append(ptext("MI MISIÓN", 28, y0 + 28, 3, C["lav"]))
    for i, line in enumerate(["La tecnología solo es buena", "si llega a todos."]):
        b.append(f'<text x="28" y="{y0 + 88 + i * 38}" font-family="{SANS}" font-size="32" font-weight="800" fill="#ffffff">{esc(line)}</text>')
    for i, (ic, t, l1, l2) in enumerate(cols):
        y = y0 + 154 + i * 108
        b.append(f'<rect x="28" y="{y}" width="{W - 56}" height="96" rx="16" fill="#ffffff" fill-opacity=".07" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>')
        b.append(f'<rect x="44" y="{y + 18}" width="60" height="60" rx="12" fill="{C["ink"]}" fill-opacity=".6"/>')
        b.append(bitmap(ICONS[ic][0], 50, y + 24, 5, ICONS[ic][1]))
        b.append(ptext(t, 122, y + 22, 3, "#ffffff"))
        b.append(f'<text x="122" y="{y + 66}" font-family="{SANS}" font-size="17" fill="{C["lav2"]}" fill-opacity=".92">{esc(l1)}</text>')
        b.append(f'<text x="122" y="{y + 87}" font-family="{SANS}" font-size="17" fill="{C["lav2"]}" fill-opacity=".92">{esc(l2)}</text>')
    H = y0 + h3
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
    ("registro", "03", "shield", "REGISTRO Y CONTROL", ("EN DESARROLLO", C["cream"]),
     "App full-stack para registrar y auditar la entrada de personas y vehículos a un edificio, con bitácora de visitas y gafetes.",
     ["Laravel", "React", "Inertia", "PostgreSQL", "Docker"], "full-stack · MVC"),
    ("colegio", "04", "build", "PORTAL COLEGIO", ("LÍDER DE EQUIPO", C["shell"]),
     "Portal institucional del Colegio de Ingenieros Civiles de Tuxtla: trámites, servicios y eventos reunidos en un solo lugar.",
     ["React", "Vite", "Framer Motion", "Router"], "equipo de 5 personas"),
]


def project_card(key, num, icon, title, chip_, desc, tags, foot):
    W = W0
    rows, colors = ICONS[icon]
    chip_t, chip_c = chip_
    lines = wrap(desc, 44)
    desc_y = 142
    last = desc_y + (len(lines) - 1) * 29
    t_svg, t_bot = pills(tags, 26, last + 24, W - 52, size=15, h=32, gap=8, stroke=C["border"],
                         fill=C["card2"], color=C["lav"], cw=8.4)
    sep = t_bot + 24
    H = sep + 62
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<rect x="26" y="26" width="64" height="64" rx="14" fill="{C["card2"]}" stroke="{C["border"]}" stroke-width="2"/>',
         bitmap(rows, 35, 35, 5, colors),
         ptext(title, 108, 32, 3, C["text"])]
    cw = len(chip_t) * 8.8 + 44
    b.append(f'<rect x="108" y="68" width="{cw:.0f}" height="28" rx="14" fill="{chip_c}" fill-opacity=".14" stroke="{chip_c}" stroke-opacity=".6" stroke-width="1.5"/>')
    b.append(f'<rect x="120" y="78" width="8" height="8" fill="{chip_c}"/>')
    b.append(f'<text x="136" y="87" font-family="{SANS}" font-size="15" font-weight="700" letter-spacing=".5" fill="{chip_c}">{esc(chip_t)}</text>')
    for i, line in enumerate(lines):
        b.append(f'<text x="26" y="{desc_y + i * 29}" font-family="{SANS}" font-size="19" fill="{C["text"]}" fill-opacity=".86">{esc(line)}</text>')
    b.append(t_svg)
    b.append(f'<rect x="26" y="{sep}" width="{W - 52}" height="1.5" fill="{C["border"]}"/>')
    b.append(f'<text x="26" y="{sep + 34}" font-family="{MONO}" font-size="16" fill="{C["muted"]}">{esc(foot)}</text>')
    b.append(f'<text x="{W - 26}" y="{sep + 34}" text-anchor="end" font-family="{MONO}" font-size="16" font-weight="700" fill="{C["shell"]}">ver repo -&gt;</text>')
    save(f"proyecto-{key}.svg", svg(W, H, "\n".join(b)))


# ================================================================ FOOTER
def footer():
    W, H = W0, 236
    m_svg, m_css = mascot(112, 198, 150, "gf")
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="{C["card"]}" stroke="{C["border"]}" stroke-width="2"/>',
         f'<defs><radialGradient id="g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{C["aqua"]}" stop-opacity=".30"/>'
         f'<stop offset="1" stop-color="{C["aqua"]}" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="112" cy="122" r="100" fill="url(#g)"/>',
         m_svg,
         sparkle(30, 34, 3, C["shell"], 0), sparkle(168, 44, 3, C["lav"], 1.1),
         ptext("¡GRACIAS", 204, 42, 4, C["text"]),
         ptext("POR VISITAR!", 204, 84, 4, C["text"]),
         f'<text x="206" y="152" font-family="{MONO}" font-size="17" fill="{C["muted"]}">nos vemos en el próximo commit</text>',
         f'<rect x="{206 + 30 * 10.2:.0f}" y="137" width="11" height="20" fill="{C["shell"]}" class="cursor"/>',
         f'<text x="206" y="188" font-family="{MONO}" font-size="16" fill="{C["aqua"]}">hecho en Chiapas, MX</text>']
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
