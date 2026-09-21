#!/usr/bin/env python3
"""Verificador del Plan de Generación de Demanda de Tazki.

Uso:  python3 plan_check.py <plan.html> --corte 2026-08-06
Sale con código 1 y lista los problemas si algo no cuadra. NO entregar el
archivo a Diego mientras este script no pase.

Qué revisa:
  1. charset utf-8 declarado al inicio (sin él, el teléfono muestra mojibake).
  2. El diccionario D es JSON valido; render headless sin 'undefined', sin HTML
     escapado visible, sin NaN, y sin tablas de JS vacias.
  3. Todas las etiquetas "(al N)" y "agosto al día N" == día del corte.
  4. La fila parcial de contenido "(parcial · X de 7 días)" coherente con el corte
     (semana DOM–SÁB).
  5. Sumas cruzadas: inbTot == suma de inbRows; cc.created/open == totales de la
     matriz de camadas estática; cp == fila de totales de la matriz.
  6. Sin '<span' dentro de los arrays de meses (se renderizan escapados).
  7. (21-sep-2026) pdf_highlights.json: su campo "fecha" dice "corte <día> N" con N == día del corte.
  8. (21-sep-2026) La tarjeta "Estado de los datos" dice "corte: <día> N de <mes>" == corte.
  9. (21-sep-2026) Matriz de camadas (fila "Año 2026", celdas "w / l") y tabla de productividad
     (filas Ganó / Perdió) dicen lo mismo que D.cp, y sus totales cuadran con D.cc.
 10. (21-sep-2026) Ganados y perdidos por ENTRADA A ETAPA: cierres_por_entrada.json (lo escribe la
     rutina desde HubSpot con hs_v2_date_entered_closedlost / _1233212743) tiene el corte del día y
     coincide con D.cp; y el criterio está declarado en la tarjeta de productividad y en la leyenda
     de la matriz (ninguna dice "fecha de cierre" como criterio vigente).
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

    # 4. fila parcial de contenido, semana LUN–DOM
    # (cambiado el 9-ago-2026: Diego pidió unificar TODO el Plan a lunes–domingo.
    #  Antes el bloque de contenido iba DOM–SÁB porque HubSpot corta así; ahora la
    #  tabla se arma agrupando desde datos diarios, igual que SEO y el bloque SEM.)
    m = re.search(r'parcial · (\d+) de 7 días', src)
    if m:
        transcurridos = corte.weekday() + 1  # lun=0 -> 1 día transcurrido
        if int(m.group(1)) != transcurridos:
            errores.append(f"Fila parcial de contenido dice '{m.group(1)} de 7 días'; con corte {corte} (semana lun–dom) debería decir {transcurridos}.")

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

    # 3b. etiquetas "al N de <mes>" sin parentesis (el 31-ago-2026 quedo viva una
    #     que decia "al 23 de agosto" en el bloque 4 y el chequeo de "(al N)" no la vio)
    MES = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
           7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
    # el lookbehind descarta los rangos de semana ("del 3 al 9 de agosto")
    for dia, mes in re.findall(r"(?<!\d )\bal (\d{1,2}) de (%s)\b" % "|".join(MES.values()), src):
        if mes == MES[corte.month] and int(dia) != corte.day:
            errores.append("Etiqueta 'al %s de %s' no coincide con el corte (dia %d)."
                           % (dia, mes, corte.day))

    # 2a. el diccionario D tiene que ser JSON valido
    #     (un D roto no lanza 'undefined' ni acorta el DOM: simplemente deja
    #      TODAS las tablas de JS vacias y el error pasaba desapercibido.
    #      Ocurrio el 31-ago-2026 al insertar mal una entrada de bitacora.)
    mD = re.search(r'const D=\s*\{', src)
    if not mD:
        errores.append("No encontre 'const D={' en el archivo.")
    else:
        i = src.index("{", mD.start())
        depth, k, instr, esc = 0, i, False, False
        fin = None
        while k < len(src):
            c = src[k]
            if instr:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': instr = False
            else:
                if c == '"': instr = True
                elif c == "{": depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        fin = k
                        break
            k += 1
        if fin is None:
            errores.append("El diccionario D no cierra: llaves desbalanceadas.")
        else:
            try:
                json.loads(src[i:fin+1])
            except Exception as e:
                errores.append("El diccionario D NO es JSON valido (%s). "
                               "Con D roto el JS no corre y todas sus tablas quedan vacias." % e)

    # 7. pdf_highlights.json: fecha del resumen ejecutivo == corte (21-sep-2026: el PDF
    #    ejecutivo salió con el resumen del corte anterior y nadie lo vio)
    hl_path = os.path.join(os.path.dirname(os.path.abspath(args.archivo)), "pdf_highlights.json")
    if os.path.exists(hl_path):
        try:
            hl = json.load(open(hl_path, encoding="utf-8"))
            mh = re.search(r"corte (?:domingo|lunes|martes|miércoles|jueves|viernes|sábado) (\d+)", hl.get("fecha", ""))
            if not mh:
                errores.append("pdf_highlights.json: el campo 'fecha' no dice 'corte <día> N'.")
            elif int(mh.group(1)) != corte.day:
                errores.append(f"pdf_highlights.json: dice corte día {mh.group(1)}, el corte es {corte.day}. El resumen ejecutivo del PDF es de otra semana.")
        except Exception as e:
            errores.append(f"pdf_highlights.json no se pudo leer: {e}")
    else:
        errores.append("Falta pdf_highlights.json junto al HTML (lo consume make_pdf_ejecutivo.py).")

    # 8. tarjeta "Estado de los datos" == corte (21-sep-2026: llevaba dos cortes sin actualizar)
    me = re.search(r"Estado de los datos</b>.{0,80}?corte: (?:domingo|lunes|martes|miércoles|jueves|viernes|sábado) (\d+) de (%s)" % "|".join(MES.values()), src, re.S)
    if not me:
        errores.append("Tarjeta 'Estado de los datos': no encontré 'corte: <día> N de <mes>'.")
    elif int(me.group(1)) != corte.day or me.group(2) != MES[corte.month]:
        errores.append(f"Tarjeta 'Estado de los datos' dice corte {me.group(1)} de {me.group(2)}; el corte es {corte.day} de {MES[corte.month]}.")

    # 9. matriz de camadas y productividad dicen lo mismo que D.cp y cuadran con D.cc
    #    (21-sep-2026: la matriz quedó por fecha de cierre y la productividad por entrada a etapa)
    if cp and cc:
        n = len(cp["months"])
        j2 = src.find("qué pasó con cada camada")
        if j2 > 0:
            tabla = src[j2:src.find("</table>", j2)]
            fila = tabla[tabla.find("Año 2026"):]
            pares = re.findall(r'<td class="r num">(\d+) / (\d+)</td>', fila)
            if len(pares) != n:
                errores.append(f"Matriz de camadas: la fila 'Año 2026' tiene {len(pares)} celdas 'w / l', esperaba {n}.")
            else:
                mw = [int(a) for a, b in pares]; ml = [int(b) for a, b in pares]
                if mw != cp["won"] or ml != cp["lost"]:
                    errores.append(f"Matriz de camadas (Año 2026) ganados {mw} / perdidos {ml} != productividad D.cp won {cp['won']} / lost {cp['lost']}. Mismo criterio para las dos.")
        else:
            errores.append("No encontré la matriz de camadas ('qué pasó con cada camada').")
        jp = src.find("Productividad · por mes de cierre")
        if jp > 0:
            tb = src[jp:src.find("</table>", jp)]
            def fila_num(etiqueta):
                f = re.search(etiqueta + r".*?</tr>", tb, re.S)
                return [int(x) for x in re.findall(r'<td class="r num"[^>]*>(?:<b>)?(\d+)', f.group(0))] if f else None
            g = fila_num("Ganó"); pr = fila_num("Perdió")
            if not g or not pr or g[:n] != cp["won"] or pr[:n] != cp["lost"] or g[n] != sum(cp["won"]) or pr[n] != sum(cp["lost"]):
                errores.append(f"Tabla estática de productividad (Ganó {g} / Perdió {pr}) no coincide con D.cp ({cp['won']} / {cp['lost']}).")
        else:
            errores.append("No encontré la tabla 'Productividad · por mes de cierre'.")
        if sum(cc["won"]) != sum(cp["won"]) or sum(cc["lost"]) != sum(cp["lost"]):
            errores.append(f"Totales: camadas cc won {sum(cc['won'])}/lost {sum(cc['lost'])} != productividad cp won {sum(cp['won'])}/lost {sum(cp['lost'])}.")

    # 10. criterio de ENTRADA A ETAPA (decisión de Diego del 17-sep-2026)
    ce_path = os.path.join(os.path.dirname(os.path.abspath(args.archivo)), "cierres_por_entrada.json")
    if not os.path.exists(ce_path):
        errores.append("Falta cierres_por_entrada.json: la rutina debe escribirlo desde HubSpot con ganados/perdidos por mes de ENTRADA a etapa (hs_v2_date_entered_closedlost / hs_v2_date_entered_1233212743).")
    elif cp:
        try:
            ce = json.load(open(ce_path, encoding="utf-8"))
            if ce.get("corte") != args.corte:
                errores.append(f"cierres_por_entrada.json es del corte {ce.get('corte')}, no de {args.corte}: hay que recalcularlo.")
            elif ce.get("won") != cp["won"] or ce.get("lost") != cp["lost"]:
                errores.append(f"D.cp {cp['won']}/{cp['lost']} no coincide con cierres_por_entrada.json {ce.get('won')}/{ce.get('lost')}: la productividad no está por entrada a etapa.")
        except Exception as e:
            errores.append(f"cierres_por_entrada.json no se pudo leer: {e}")
    jp = src.find("Productividad · por mes de cierre")
    if jp > 0 and "entrada a la etapa" not in src[jp:jp+400]:
        errores.append("La tarjeta de productividad no declara el criterio 'entrada a la etapa'.")
    j2 = src.find("qué pasó con cada camada")
    if j2 > 0 and "(fecha de cierre)" in src[j2:j2+9000]:
        errores.append("La leyenda de la matriz de camadas dice '(fecha de cierre)': el criterio vigente es entrada a etapa.")

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
        # 2b. ninguna tabla que llena el JS puede quedar vacia
        ids = sorted(set(re.findall(r'<table id="(t[A-Za-z0-9_]+)"\s*></table>', src)))
        vacias = []
        for tid in ids:
            m = re.search(r'<table id="%s"[^>]*>(.*?)</table>' % tid, dom, re.S)
            if not m or m.group(1).count("<tr") == 0:
                vacias.append(tid)
        if vacias:
            errores.append("Tablas que el JS deja VACIAS en el render: " + ", ".join(vacias))
        if len(dom) < 50000:
            errores.append(f"El render quedó sospechosamente corto ({len(dom)} bytes): ¿JS roto?")
    else:
        errores.append("No encontré el navegador headless para verificar el render.")

    if errores:
        fail(errores)
    print(f"✓ plan_check OK (corte {corte}, {len(src)} bytes)")

if __name__ == "__main__":
    main()
