"""
gif_a_transparente.py — Quita el fondo liso de un GIF animado (por ejemplo uno de Tenor/Giphy)
y lo guarda como GIF transparente y/o como cuadros PNG con bordes suaves.

Requisito:  pip install pillow

Uso:
    python gif_a_transparente.py entrada.gif --gif salida.gif --frames carpeta_png --paso 2

Opciones:
    --paso 2          conserva 1 de cada 2 cuadros (y duplica su duración): aligera el archivo
    --tolerancia 28   qué tan parecido al fondo debe ser un pixel para volverse transparente
    --ancho 200       ancho final (por defecto, el original)
    --colores 96      colores de cada PNG (menos colores = archivos más ligeros)

Los cuadros conservan su posición relativa (no se re-alinean), así que el movimiento
del baile se mantiene. Todos se recortan al mismo rectángulo.
"""
import argparse
import os
from collections import deque

from PIL import Image, ImageFilter


def dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def remove_bg(frame, bg, tol):
    """Relleno por inundación desde los bordes: solo se borra el fondo conectado al borde."""
    f = frame.convert("RGBA")
    w, h = f.size
    px = f.load()
    seen = bytearray(w * h)
    q = deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] +
              [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if dist(px[x, y][:3], bg) <= tol:
            px[x, y] = (0, 0, 0, 0)
            if x > 0: q.append((x - 1, y))
            if x < w - 1: q.append((x + 1, y))
            if y > 0: q.append((x, y - 1))
            if y < h - 1: q.append((x, y + 1))
    return f


def defringe(f, bg, passes=2, tol=70):
    """Quita el contorno que sigue pareciéndose al fondo (halo del GIF comprimido)."""
    w, h = f.size
    for _ in range(passes):
        px = f.load()
        kill = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a and dist((r, g, b), bg) <= tol:
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                            kill.append((x, y))
                            break
        for x, y in kill:
            px[x, y] = (0, 0, 0, 0)
    return f


def soften(f, radius=0.6):
    """Suaviza el borde del recorte para que no se vea dentado."""
    a = f.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    f = f.copy()
    f.putalpha(a)
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("--gif", default="")
    ap.add_argument("--frames", default="")
    ap.add_argument("--paso", type=int, default=1)
    ap.add_argument("--tolerancia", type=int, default=28)
    ap.add_argument("--ancho", type=int, default=0)
    ap.add_argument("--colores", type=int, default=96)
    a = ap.parse_args()

    im = Image.open(a.entrada)
    raw, durs = [], []
    for i in range(im.n_frames):
        im.seek(i)
        raw.append(im.convert("RGBA"))
        durs.append(im.info.get("duration", 100))
    bg = raw[0].getpixel((0, 0))[:3]
    print(f"{len(raw)} cuadros {raw[0].size}, fondo {bg}")

    frames, delays = [], []
    for i in range(0, len(raw), a.paso):
        f = defringe(remove_bg(raw[i], bg, a.tolerancia), bg)
        frames.append(f)
        delays.append(sum(durs[i:i + a.paso]))

    # un solo rectángulo para todos los cuadros (se conserva el movimiento)
    box = None
    for f in frames:
        b = f.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    pad = 2
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(frames[0].width, box[2] + pad), min(frames[0].height, box[3] + pad))
    frames = [f.crop(box) for f in frames]
    if a.ancho:
        k = a.ancho / frames[0].width
        size = (a.ancho, round(frames[0].height * k))
        frames = [f.resize(size, Image.Resampling.LANCZOS) for f in frames]
    frames = [soften(f) for f in frames]
    print(f"{len(frames)} cuadros finales, {frames[0].size}, {sum(delays)} ms por vuelta")

    if a.frames:
        os.makedirs(a.frames, exist_ok=True)
        total = 0
        for i, f in enumerate(frames):
            p = os.path.join(a.frames, f"{i:03d}.png")
            f.quantize(colors=a.colores, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(p, optimize=True)
            total += os.path.getsize(p)
        with open(os.path.join(a.frames, "duraciones.txt"), "w") as fh:
            fh.write("\n".join(str(d) for d in delays))
        print(f"PNG: {total / 1024:.0f} KB en total en {a.frames}")

    if a.gif:
        seq = []
        for f in frames:
            rgb = Image.new("RGB", f.size, (0, 0, 0))
            rgb.paste(f, mask=f.getchannel("A"))
            p = rgb.quantize(colors=255, dither=Image.Dither.NONE)
            p.paste(255, mask=f.getchannel("A").point(lambda v: 255 if v < 128 else 0))
            seq.append(p)
        seq[0].save(a.gif, save_all=True, append_images=seq[1:], duration=delays, loop=0,
                    disposal=2, transparency=255, optimize=False)
        print(f"GIF: {a.gif} ({os.path.getsize(a.gif) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
