#!/usr/bin/env python3
"""Recorta la tarjeta del logo desde las paginas exportadas del Canva 'Logos de Tazki'.

Cada archivo de ventas-assets/logos-clientes/N.jpg es la pagina completa del Canva:
fondo navy (12,30,80), la etiqueta de industria arriba y una tarjeta blanca redondeada
con el logo del cliente al centro. Para las piezas comerciales solo sirve la tarjeta.

Deja los recortes en ventas-assets/logos-recortados/N.png y reporta los casos raros
(tarjeta vacia o interior oscuro), que son los que Diego ya tenia detectados.
"""
import os, glob, json
from PIL import Image

RAIZ  = os.path.dirname(os.path.abspath(__file__))
ORIG  = os.path.join(RAIZ, "ventas-assets/logos-clientes")
DEST  = os.path.join(RAIZ, "ventas-assets/logos-recortados")
NAVY  = (12, 30, 80)
TOL   = 42          # distancia al navy para considerar "no es fondo"
CORTE_ETIQUETA = 0.22   # se ignora el 22% superior: ahi va el texto de la industria


def dista(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1]) + abs(p[2]-q[2])


def caja_de_la_tarjeta(im):
    """Bounding box de la tarjeta (lo que no es fondo navy), ignorando la etiqueta."""
    w, h = im.size
    y_ini = int(h * CORTE_ETIQUETA)
    px = im.load()
    paso = 3
    x0, y0, x1, y1 = w, h, 0, 0
    for y in range(y_ini, h, paso):
        for x in range(0, w, paso):
            if dista(px[x, y], NAVY) > TOL:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    if x1 <= x0 or y1 <= y0:
        return None
    return (max(0, x0-2), max(0, y0-2), min(w, x1+3), min(h, y1+3))


def interior_oscuro(im, caja):
    """True si el centro de la tarjeta es oscuro (logo blanco: no se ve sobre fondo claro)."""
    x0, y0, x1, y1 = caja
    cx, cy = (x0+x1)//2, (y0+y1)//2
    r = im.crop((cx-40, cy-40, cx+40, cy+40)).convert("RGB")
    px = list(r.getdata())
    lum = sum(0.299*p[0] + 0.587*p[1] + 0.114*p[2] for p in px) / len(px)
    return lum < 110


def casi_vacia(im, caja):
    """True si la tarjeta no tiene contenido (solo blanco)."""
    x0, y0, x1, y1 = caja
    r = im.crop(caja).convert("RGB").resize((80, 40))
    px = list(r.getdata())
    distintos = sum(1 for p in px if dista(p, (255, 255, 255)) > 60)
    return distintos < 12


def main():
    os.makedirs(DEST, exist_ok=True)
    oscuros, vacias, fallos, ok = [], [], [], 0
    for f in sorted(glob.glob(os.path.join(ORIG, "*.jpg")), key=lambda p: int(os.path.basename(p)[:-4])):
        n = int(os.path.basename(f)[:-4])
        im = Image.open(f).convert("RGB")
        caja = caja_de_la_tarjeta(im)
        if not caja:
            fallos.append(n); continue
        if casi_vacia(im, caja):
            vacias.append(n); continue
        if interior_oscuro(im, caja):
            oscuros.append(n)
        im.crop(caja).save(os.path.join(DEST, f"{n}.png"))
        ok += 1

    reporte = {
        "_que_es": ("Recortes de la tarjeta del logo, sacados de las paginas del Canva. Generados por "
                    "ventas_recortar_logos.py el 18-ago-2026. Se usan en el muro de logos de las piezas comerciales."),
        "recortados_ok": ok,
        "tarjeta_vacia": vacias,
        "interior_oscuro_logo_blanco": oscuros,
        "sin_tarjeta_detectada": fallos,
        "_nota": ("'tarjeta_vacia' = la pagina del Canva no tiene logo cargado. "
                  "'interior_oscuro' = el logo es blanco sobre fondo oscuro; se ve bien sobre tarjeta oscura, "
                  "no sobre blanca. Son los casos que Diego ya tenia identificados en su planilla."),
    }
    json.dump(reporte, open(os.path.join(RAIZ, "ventas-assets/logos-recorte-reporte.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"recortados: {ok}")
    print(f"tarjeta vacía (sin logo): {vacias}")
    print(f"interior oscuro (logo blanco): {oscuros}")
    print(f"sin tarjeta detectada: {fallos}")


if __name__ == "__main__":
    main()
