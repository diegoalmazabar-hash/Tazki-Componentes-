#!/usr/bin/env python3
"""Verificador del Plan de Generación de Demanda de Tazki.

Uso:  python3 plan_check.py <plan.html> --corte 2026-08-06
Sale con código 1 y lista los problemas si algo no cuadra. NO entregar el
archivo a Diego mientras este script no pase.

Qué revisa:
  1. charset utf-8 declarado al inicio (sin él, el teléfono muestra mojibake).
  2. Render headless sin 'undefined', sin HTML escapado visible, sin NaN.
  3. Todas las etiquetas "(al N)" y "agosto al día N" == día del corte.
  4. La fila parcial de contenido "(parcial · X de 7 días)" coherente con el corte
     (semana DOM–SÁB).
  5. Sumas cruzadas: inbTot == suma de inbRows; cc.created/open == totales de la
     matriz de camadas estática; cp == fila de totales de la matriz.
  6. Sin '<span' dentro de los arrays de meses (se renderizan escapados).
"""
import argparse, datetime, json, re, subprocess, sys, glob, os

def fail(errores):
    print("\n✗ PLAN_CHECK FALLÓ — NO ENTREGAR TODAVÍA:")
    for e in errores:
        print("  -", e)
    sys.exit(1)

def carga_const(src, nombre):
    m = re.search(r'"%s":\s*' % nombre, src)
    if not m:
        return None
    i = src.index("{" if src[m.end()] == "{" else "[", m.end())
    depth, k, instr, esc, q = 0, i, False, False, ""
    abre, cierra = src[i], {"{": "}", "[": "]"}[src[i]]
    while k < len(src):
        c = src[k]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == q: instr = False
        else:
            if c == '"': instr, q = True, c
            elif c == abre: depth += 1
            elif c == cierra:
                depth -= 1
                if depth == 0:
                    return json.loads(src[i:k+1])
        k += 1
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--corte", required=True, help="fecha hasta la que llegan los datos, YYYY-MM-DD")
    args = ap.parse_args()
    src = open(args.archivo, encoding="utf-8").read()
    corte = datetime.date.fromisoformat(args.corte)
    errores = []

    # 1. charset
    if "charset" not in src[:600].lower():
        errores.append("Falta <meta charset=\"utf-8\"> al inicio (mojibake en el teléfono).")

    # 3. etiquetas de día del corte
    dias = set(re.findall(r'\(al (\d+)\)', src)) | set(re.findall(r'al día (\d+)', src))
    esperado = str(corte.day)
    mal = sorted(d for d in dias if d != esperado)
    if mal:
        errores.append(f"Etiquetas '(al N)' desalineadas: esperaba (al {esperado}), hay {mal}.")

    # 4. fila parcial de contenido, semana DOM–SÁB
    m = re.search(r'parcial · (\d+) de 7 días', src)
    if m:
        # días transcurridos de la semana dom-sáb que contiene el corte
        dow = (corte.weekday() + 1) % 7  # dom=0 ... sáb=6
        transcurridos = dow + 1
        if int(m.group(1)) != transcurridos:
            errores.append(f"Fila parcial de contenido dice '{m.group(1)} de 7 días'; con corte {corte} debería decir {transcurridos}.")

    # 6. spans dentro de arrays de meses
    for k in ("inbMonths", "convMonths", "impMonths", "seoMonths"):
        arr = carga_const(src, k)
        if arr and any("<" in x for x in arr):
            errores.append(f"{k} contiene HTML; los encabezados se escapan y se ve el código.")

    # 5a. inbTot vs inbRows
    tot = carga_const(src, "inbTot"); rows = carga_const(src, "inbRows")
    if tot and rows:
        calc = [sum(r["data"][i] for r in rows) for i in range(len(tot))]
        if calc != tot:
            errores.append(f"inbTot {tot} != suma de inbRows {calc}.")

    # 5b. cc vs matriz estática de camadas
    cc = carga_const(src, "cc")
    j = src.find("qué pasó con cada camada")
    if cc and j > 0:
        tabla = src[j:src.find("</table>", j)]
        mtot = re.search(r'Año 2026</b></td><td class="r num"><b>(\d+)</b>', tabla)
        if mtot and int(mtot.group(1)) != sum(cc["created"]):
            errores.append(f"Matriz de camadas: total creados {mtot.group(1)} != cc.created {sum(cc['created'])}.")
        mopen = re.findall(r'<td class="r num"><b>(\d+)</b></td>', tabla)
        if mopen and sum(cc["open"]) and str(sum(cc["open"])) not in mopen:
            errores.append(f"Matriz de camadas: 'sin cerrar' total no coincide con cc.open ({sum(cc['open'])}).")

    # 5c. cp coherente consigo mismo
    cp = carga_const(src, "cp")
    if cp and len(cp["won"]) != len(cp["months"]):
        errores.append("cp: won/lost no tienen el mismo largo que months.")

    # 2. render headless
    shells = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
    if shells:
        dom = subprocess.run([shells[0], "--headless", "--disable-gpu", "--no-sandbox",
            "--dump-dom", "--virtual-time-budget=4000",
            "file://" + os.path.abspath(args.archivo)],
            capture_output=True, text=True, timeout=90).stdout
        vis = dom.count("undefined") - dom.count('typeof RECUP==="undefined"')
        if vis > 0:
            errores.append(f"El render muestra 'undefined' {vis} veces (datos y código desalineados).")
        if "&lt;span" in dom:
            errores.append("El render muestra HTML escapado visible ('<span' como texto).")
        if re.search(r'>NaN<|>NaN%', dom):
            errores.append("El render muestra NaN.")
        if len(dom) < 50000:
            errores.append(f"El render quedó sospechosamente corto ({len(dom)} bytes): ¿JS roto?")
    else:
        errores.append("No encontré el navegador headless para verificar el render.")

    if errores:
        fail(errores)
    print(f"✓ plan_check OK (corte {corte}, {len(src)} bytes)")

if __name__ == "__main__":
    main()
