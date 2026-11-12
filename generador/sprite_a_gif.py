"""
sprite_a_gif.py — Convierte un sprite sheet en cuadrícula en un GIF animado
con fondo transparente, listo para un README de GitHub.

Requisito:  pip install pillow

Uso básico (detecta cada sprite automáticamente, aunque no estén alineados):
    python sprite_a_gif.py hoja.png gengar.gif

Si tu hoja es una cuadrícula perfecta, puedes forzar el modo cuadrícula:
    python sprite_a_gif.py hoja.png gengar.gif --cols 4 --rows 2

Opciones útiles:
    --duracion 120        milisegundos por cuadro
    --pausa 4:500         el cuadro 4 dura 500 ms (se puede repetir: --pausa 1:300 --pausa 4:600)
    --pixel 5.4           tamaño de cada 'pixel' del arte en la hoja; re-pixela y deja bordes nítidos
    --ancho 240           ancho final aproximado del GIF (con --pixel se usa un múltiplo entero)
    --ida-y-vuelta        reproduce 1,2,3,...,n,...,3,2
    --tolerancia 40       qué tan parecido al fondo debe ser un pixel para volverse transparente
    --frames-png carpeta  además guarda cada cuadro como PNG transparente

Cómo funciona:
 1. Modo automático: quita el fondo de toda la hoja y separa cada sprite por su silueta,
    ordenándolos por filas (de izquierda a derecha). Modo cuadrícula: celdas iguales.
 2. Quita el fondo con "relleno por inundación" desde los bordes de cada celda,
    así no se borran los blancos internos (dientes, ojos).
 3. Limpia el halo claro que queda alrededor del contorno.
 4. Recorta cada cuadro y los alinea por abajo al centro (los pies no "saltan").
 5. Usa una sola paleta para todos los cuadros (sin parpadeos) y guarda el GIF en bucle.
"""
import argparse
import os
from collections import deque

from PIL import Image


def color_dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def detect_bg(img):
    """El color más común entre las 4 esquinas."""
    w, h = img.size
    px = img.load()
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    return max(set(c[:3] for c in corners), key=lambda c: sum(1 for k in corners if k[:3] == c))


def remove_background(cell, bg, tol):
    """Relleno por inundación desde los bordes: lo conectado al borde y parecido al fondo se vuelve transparente."""
    cell = cell.convert("RGBA")
    w, h = cell.size
    px = cell.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        q.extend([(0, y), (w - 1, y)])
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, a = px[x, y]
        if a == 0 or color_dist((r, g, b), bg) <= tol:
            px[x, y] = (0, 0, 0, 0)
            if x > 0: q.append((x - 1, y))
            if x < w - 1: q.append((x + 1, y))
            if y > 0: q.append((x, y - 1))
            if y < h - 1: q.append((x, y + 1))
    return cell


def defringe(cell, bg, passes=2, tol=110):
    """Quita los pixeles del borde que siguen pareciéndose al fondo (halo blanco)."""
    w, h = cell.size
    for _ in range(passes):
        px = cell.load()
        kill = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a == 0 or color_dist((r, g, b), bg) > tol:
                    continue
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                        kill.append((x, y))
                        break
        for x, y in kill:
            px[x, y] = (0, 0, 0, 0)
    return cell


def pixelate(cell, block):
    """Reduce el sprite a su resolución 'real' (1 pixel del arte = 1 pixel).
    block puede ser decimal, p. ej. 5.4 si la hoja se escaló a un tamaño no entero."""
    w, h = cell.size
    small = cell.resize((max(1, round(w / block)), max(1, round(h / block))), Image.Resampling.BOX)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    small.putalpha(a)
    return small


def find_sprites(sheet, bg, tol, step=2, grow=1, min_frac=0.01):
    """Detecta sprites como manchas conectadas y devuelve sus cajas en orden de lectura."""
    clean = remove_background(sheet, bg, tol)
    alpha = clean.getchannel("A")
    W, H = clean.size
    gw, gh = W // step + 1, H // step + 1
    a = alpha.load()
    occ = [[False] * gw for _ in range(gh)]
    for y in range(0, H, step):
        for x in range(0, W, step):
            if a[x, y]:
                for dy in range(-grow, grow + 1):
                    for dx in range(-grow, grow + 1):
                        gx, gy = x // step + dx, y // step + dy
                        if 0 <= gx < gw and 0 <= gy < gh:
                            occ[gy][gx] = True
    seen = [[False] * gw for _ in range(gh)]
    boxes = []
    for sy in range(gh):
        for sx in range(gw):
            if not occ[sy][sx] or seen[sy][sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy][sx] = True
            x0 = x1 = sx
            y0 = y1 = sy
            n = 0
            while q:
                x, y = q.popleft()
                n += 1
                x0, x1, y0, y1 = min(x0, x), max(x1, x), min(y0, y), max(y1, y)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < gw and 0 <= ny < gh and occ[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if n * step * step >= min_frac * W * H:
                box = (max(0, x0 * step), max(0, y0 * step), min(W, (x1 + 1) * step), min(H, (y1 + 1) * step))
                inner = alpha.crop(box).getbbox()
                boxes.append((box[0] + inner[0], box[1] + inner[1], box[0] + inner[2], box[1] + inner[3]))
    # orden de lectura: agrupa por filas según el centro vertical
    boxes.sort(key=lambda b: (b[1] + b[3]) / 2)
    rows, med = [], sorted(b[3] - b[1] for b in boxes)[len(boxes) // 2] if boxes else 0
    for b in boxes:
        cy = (b[1] + b[3]) / 2
        if rows and abs(cy - rows[-1][0]) < med / 2:
            rows[-1][1].append(b)
        else:
            rows.append([cy, [b]])
    ordered = [b for _, row in rows for b in sorted(row, key=lambda b: b[0])]
    return clean, ordered


def main():
    ap = argparse.ArgumentParser(description="Sprite sheet en cuadrícula -> GIF animado transparente")
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--cols", type=int, default=0, help="solo para modo cuadrícula")
    ap.add_argument("--rows", type=int, default=0, help="solo para modo cuadrícula")
    ap.add_argument("--duracion", type=int, default=120)
    ap.add_argument("--pausa", action="append", default=[], help="cuadro:ms (empieza en 1)")
    ap.add_argument("--tolerancia", type=int, default=40)
    ap.add_argument("--pixel", type=float, default=0)
    ap.add_argument("--ancho", type=int, default=0)
    ap.add_argument("--ida-y-vuelta", action="store_true")
    ap.add_argument("--frames-png", default="")
    args = ap.parse_args()

    sheet = Image.open(args.entrada).convert("RGBA")
    bg = detect_bg(sheet)
    W, H = sheet.size
    frames = []
    if not (args.cols and args.rows):
        print(f"Hoja {W}x{H}, fondo {bg}, modo automático")
        clean, boxes = find_sprites(sheet, bg, args.tolerancia)
        for i, box in enumerate(boxes, 1):
            f = defringe(clean.crop(box), bg)
            f = f.crop(f.getchannel("A").getbbox())
            frames.append(f)
            print(f"  cuadro {i}: x={box[0]} y={box[1]} {f.width}x{f.height}")
    cw, ch = (W / args.cols, H / args.rows) if args.cols and args.rows else (0, 0)
    if cw:
        print(f"Hoja {W}x{H}, fondo {bg}, celdas {cw:.0f}x{ch:.0f}")
    for r in range(args.rows if cw else 0):
        for c in range(args.cols):
            box = (round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch))
            cell = remove_background(sheet.crop(box), bg, args.tolerancia)
            cell = defringe(cell, bg)
            bbox = cell.getchannel("A").getbbox()
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) if bbox else 0
            if area < 0.02 * cell.width * cell.height:
                print(f"  celda ({r + 1},{c + 1}) vacía, se omite")
                continue
            frames.append(cell.crop(bbox))
            print(f"  cuadro {len(frames)}: celda ({r + 1},{c + 1}) {bbox[2] - bbox[0]}x{bbox[3] - bbox[1]}")

    if not frames:
        raise SystemExit("No se encontraron cuadros.")

    if args.pixel > 1:
        frames = [pixelate(f, args.pixel) for f in frames]
        print(f"  re-pixelado a resolución nativa ~{frames[0].width}x{frames[0].height}")

    # lienzo común, alineado abajo al centro
    fw = max(f.width for f in frames)
    fh = max(f.height for f in frames)
    pad = 1 if args.pixel > 1 else 4
    canvas = []
    for f in frames:
        cv = Image.new("RGBA", (fw + pad * 2, fh + pad * 2), (0, 0, 0, 0))
        cv.paste(f, ((cv.width - f.width) // 2, cv.height - pad - f.height), f)
        canvas.append(cv)

    if args.pixel > 1:
        # escala entera: cada pixel del arte queda como un cuadrado perfecto
        k = max(1, round(args.ancho / canvas[0].width)) if args.ancho else max(1, round(args.pixel))
        canvas = [cv.resize((cv.width * k, cv.height * k), Image.Resampling.NEAREST) for cv in canvas]
    elif args.ancho:
        k = args.ancho / canvas[0].width
        size = (args.ancho, round(canvas[0].height * k))
        canvas = [cv.resize(size, Image.Resampling.NEAREST) for cv in canvas]

    durations = [args.duracion] * len(canvas)
    for p in args.pausa:
        i, ms = p.split(":")
        durations[int(i) - 1] = int(ms)

    order = list(range(len(canvas)))
    if args.ida_y_vuelta and len(order) > 2:
        order += order[-2:0:-1]
    seq = [canvas[i] for i in order]
    seq_d = [durations[i] for i in order]

    if args.frames_png:
        os.makedirs(args.frames_png, exist_ok=True)
        for i, cv in enumerate(canvas, 1):
            cv.save(os.path.join(args.frames_png, f"frame-{i:02d}.png"))

    # una sola paleta para todos los cuadros (índice 255 = transparente)
    strip = Image.new("RGB", (seq[0].width * len(canvas), seq[0].height))
    for i, cv in enumerate(canvas):
        flat = Image.new("RGB", cv.size, (0, 0, 0))
        flat.paste(cv, mask=cv.getchannel("A"))
        strip.paste(flat, (i * cv.width, 0))
    pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)

    gif_frames = []
    for cv in seq:
        rgb = Image.new("RGB", cv.size, (0, 0, 0))
        rgb.paste(cv, mask=cv.getchannel("A"))
        p = rgb.quantize(palette=pal, dither=Image.Dither.NONE)
        transparent = cv.getchannel("A").point(lambda v: 255 if v < 128 else 0)
        p.paste(255, mask=transparent)
        gif_frames.append(p)

    gif_frames[0].save(args.salida, save_all=True, append_images=gif_frames[1:], duration=seq_d,
                       loop=0, disposal=2, transparency=255, optimize=False)
    kb = os.path.getsize(args.salida) / 1024
    print(f"Listo: {args.salida} ({len(seq)} cuadros, {seq[0].width}x{seq[0].height}, {kb:.0f} KB)")


if __name__ == "__main__":
    main()
