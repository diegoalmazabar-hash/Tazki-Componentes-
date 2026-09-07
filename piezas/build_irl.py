# -*- coding: utf-8 -*-
"""Formato IRL DS 44 - Tazki.
Contenido verificado contra el TEXTO OFICIAL del articulo 15 del DS 44
(BCN/LeyChile, idNorma 1205298), leido el 2-sep-2026. Los cuatro numerales
y sus subliterales se transcriben del decreto, no de un resumen.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

NAVY   = "0C1E50"
COBALT = "1537D1"
LINE   = "C7D0E0"
SOFT   = "EEF2FE"
BAND   = "F4F6FB"
YELLOW = "FFF7D6"

F  = "Arial"
def font(sz=10, b=False, color="0C1E50", it=False):
    return Font(name=F, size=sz, bold=b, color=color, italic=it)

thin = Side(style="thin", color=LINE)
box  = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

# ───────────────────────────── HOJA 1 · FORMATO ─────────────────────────────
ws = wb.active
ws.title = "Formato IRL"
ws.sheet_view.showGridLines = False
widths = {"A":2.5,"B":26,"C":26,"D":26,"E":26,"F":26,"G":2.5}
for k,v in widths.items(): ws.column_dimensions[k].width = v

def merge(rng, value, f=None, fill=None, al=None, h=None, border=True, wrap=True):
    ws.merge_cells(rng)
    c = ws[rng.split(":")[0]]
    c.value = value
    c.font = f or font()
    if fill: c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = al or Alignment(vertical="center", wrap_text=wrap)
    if border:
        r1 = int("".join(ch for ch in rng.split(":")[0] if ch.isdigit()))
        r2 = int("".join(ch for ch in rng.split(":")[1] if ch.isdigit()))
        c1 = ws[rng.split(":")[0]].column
        c2 = ws[rng.split(":")[1]].column
        for r in range(r1, r2+1):
            for cc in range(c1, c2+1):
                ws.cell(row=r, column=cc).border = box
    if h:
        r1 = int("".join(ch for ch in rng.split(":")[0] if ch.isdigit()))
        ws.row_dimensions[r1].height = h
    return c

r = 2
merge(f"B{r}:F{r}", "INFORMACIÓN DE LOS RIESGOS LABORALES (IRL)",
      font(15, True, "FFFFFF"), NAVY, Alignment(vertical="center", horizontal="left", indent=1), 30)
r += 1
merge(f"B{r}:F{r}", "Decreto Supremo N° 44, artículo 15 · Entrega previa al inicio de las labores",
      font(9, False, "FFFFFF"), COBALT, Alignment(vertical="center", horizontal="left", indent=1), 20)

# leyenda
r += 2
merge(f"B{r}:F{r}", "CÓMO USAR ESTE FORMATO", font(9, True, COBALT), None, None, 16, border=False)
r += 1
merge(f"B{r}:F{r}",
 "Complete únicamente las celdas con fondo amarillo. Un formato por cargo o puesto de trabajo: "
 "el contenido debe corresponder a los riesgos reales de esa persona, no a un texto genérico para toda la empresa. "
 "El artículo 15 exige que la información se determine conforme a la matriz de riesgos y al programa de trabajo preventivo. "
 "Si esos dos documentos todavía no existen, el mismo artículo obliga a informar igual los riesgos inherentes a la actividad. "
 "El ejemplo muestra el nivel de detalle esperado; bórrelo antes de usar el formato.",
 font(9), BAND, Alignment(vertical="top", wrap_text=True), 46)

# identificación
r += 2
merge(f"B{r}:F{r}", "1 · IDENTIFICACIÓN", font(11, True, "FFFFFF"), NAVY,
      Alignment(vertical="center", horizontal="left", indent=1), 22)

ident = [
    ("Razón social", "Empresa", "RUT empresa", "RUT"),
    ("Centro de trabajo", "Centro / faena / sucursal", "Área o proceso", "Área"),
    ("Nombre del trabajador", "Nombre completo", "RUT trabajador", "RUT trabajador"),
    ("Cargo o puesto de trabajo", "Cargo", "Fecha de entrega", "Fecha"),
]
for etiqueta, ej1, etiqueta2, ej2 in ident:
    r += 1
    merge(f"B{r}:B{r}", etiqueta, font(9, True), SOFT, Alignment(vertical="center", wrap_text=True), 20)
    merge(f"C{r}:C{r}", None, font(9), YELLOW, Alignment(vertical="center", wrap_text=True))
    merge(f"D{r}:D{r}", etiqueta2, font(9, True), SOFT, Alignment(vertical="center", wrap_text=True))
    merge(f"E{r}:F{r}", None, font(9), YELLOW, Alignment(vertical="center", wrap_text=True))

r += 1
merge(f"B{r}:B{r}", "Motivo de la entrega", font(9, True), SOFT, Alignment(vertical="center", wrap_text=True), 20)
merge(f"C{r}:F{r}", None, font(9), YELLOW, Alignment(vertical="center", wrap_text=True))
dv = DataValidation(
    type="list", allow_blank=True,
    formula1='"Previo al inicio de las labores,Se incorpora a un nuevo proceso productivo,Cambian las tecnologías,Cambian los materiales o sustancias utilizados,Cambio de cargo o de tarea,Actualización de la matriz de riesgos,Otro"')
ws.add_data_validation(dv)
dv.add(ws[f"C{r}"])
MOTIVO_ROW = r

# los 5 contenidos del art. 15
r += 2
merge(f"B{r}:F{r}", "2 · CONTENIDO DE LA INFORMACIÓN", font(11, True, "FFFFFF"), NAVY,
      Alignment(vertical="center", horizontal="left", indent=1), 22)
r += 1
merge(f"B{r}:F{r}",
 "Los cuatro contenidos que el artículo 15 del DS 44 exige entregar como mínimo. Transcritos del texto oficial del decreto.",
 font(9, False, "33406A"), BAND, Alignment(vertical="center", wrap_text=True), 18)

bloques = [
 ("1 · Características mínimas del lugar de trabajo",
  "El artículo 15 pide cuatro cosas: a) espacio de trabajo; b) condiciones ambientales del puesto; "
  "c) condiciones de orden y aseo exigidas en el puesto; d) máquinas y herramientas de trabajo que se deberán emplear."),
 ("2 · Riesgos a los que podría estar expuesta y sus medidas preventivas",
  "Van juntos en un mismo numeral. Debe incluir además los riesgos y las medidas derivados de "
  "emergencias, catástrofes y desastres."),
 ("3 · Procedimientos de trabajo seguro",
  "Los métodos correctos para realizar la tarea, determinados conforme a la matriz de riesgos y al programa de trabajo preventivo."),
 ("4 · Características de los productos y sustancias que se manipularán",
  "Cuando corresponda: nombre, sinónimos, fórmula, aspecto y olor; modo de empleo; límites de exposición permisible; "
  "forma de almacenamiento; uso de elementos de protección personal; y medidas sobre primeros auxilios, "
  "conforme a la ficha técnica de seguridad del producto y a su etiquetado."),
]
for titulo, guia in bloques:
    r += 1
    merge(f"B{r}:F{r}", titulo, font(10, True, COBALT), SOFT, Alignment(vertical="center", indent=1), 18)
    r += 1
    merge(f"B{r}:F{r}", guia, font(8, False, "6B76A0", it=True), None, Alignment(vertical="center", wrap_text=True), 15)
    r += 1
    merge(f"B{r}:F{r}", None, font(9), YELLOW, Alignment(vertical="top", wrap_text=True), 58)

# ejemplo
r += 2
merge(f"B{r}:F{r}", "EJEMPLO — bórrelo antes de usar el formato", font(9, True, "B7791F"), None,
      Alignment(vertical="center"), 16, border=False)
r += 1
merge(f"B{r}:F{r}",
 "Numeral 2 — Operador de bodega. Atropello o golpe por grúa horquilla en zona de "
 "carga (consecuencia: lesión grave o fatal). Caída de carga desde altura al desapilar (consecuencia: "
 "lesión por aplastamiento). Sobreesfuerzo lumbar en manejo manual de carga sobre 25 kg (consecuencia: "
 "enfermedad musculoesquelética). Riesgos tomados de la MIPER del centro, versión vigente.",
 font(8, False, "33406A"), BAND, Alignment(vertical="top", wrap_text=True), 44)

# constancia
r += 2
merge(f"B{r}:F{r}", "3 · CONSTANCIA DE ENTREGA", font(11, True, "FFFFFF"), NAVY,
      Alignment(vertical="center", horizontal="left", indent=1), 22)
r += 1
merge(f"B{r}:F{r}",
 "El DS 44 no define la firma como único medio válido, pero la empresa debe conservar evidencia verificable "
 "de la entrega: qué información recibió la persona, cuándo la recibió y a qué riesgos o tareas correspondía. "
 "Sirve la firma manuscrita, la firma electrónica o una aceptación digital con fecha y trazabilidad.",
 font(8, False, "33406A"), BAND, Alignment(vertical="top", wrap_text=True), 38)
r += 1
merge(f"B{r}:F{r}",
 "Declaro haber recibido la información señalada, haber podido consultar mis dudas y comprender los riesgos "
 "de mi puesto, las medidas preventivas y los procedimientos de trabajo seguro que debo aplicar.",
 font(9), None, Alignment(vertical="center", wrap_text=True), 32)

r += 2
for col, etiqueta in (("B","Nombre del trabajador"), ("D","Nombre de quien entrega la información")):
    merge(f"{col}{r}:{chr(ord(col)+1)}{r}", None, font(9), YELLOW, Alignment(vertical="center"), 30)
r += 1
merge(f"B{r}:C{r}", "Firma del trabajador · Fecha", font(8, False, "6B76A0"), None,
      Alignment(vertical="center", horizontal="center"), 14, border=False)
merge(f"D{r}:E{r}", "Firma de quien entrega · Cargo · Fecha", font(8, False, "6B76A0"), None,
      Alignment(vertical="center", horizontal="center"), border=False)

r += 2
merge(f"B{r}:F{r}",
 "Formato elaborado por Tazki con el texto oficial del artículo 15 del DS 44 a la vista. Es una guía de trabajo "
 "y no reemplaza la asesoría de un experto en prevención de riesgos.",
 font(8, False, "6B76A0", it=True), None, Alignment(vertical="center", wrap_text=True), 26, border=False)

ws.print_area = f"A1:G{r}"
ws.page_setup.orientation = "portrait"
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True

# ───────────────────────────── HOJA 2 · REGISTRO ─────────────────────────────
rg = wb.create_sheet("Registro de entregas")
rg.sheet_view.showGridLines = False
cols = [("A",2.5),("B",22),("C",13),("D",22),("E",20),("F",13),("G",13),("H",26),("I",15),("J",13)]
for k,v in cols: rg.column_dimensions[k].width = v

rg.merge_cells("B2:J2")
c = rg["B2"]; c.value = "REGISTRO DE ENTREGAS DE IRL"
c.font = font(15, True, "FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
c.alignment = Alignment(vertical="center", horizontal="left", indent=1)
rg.row_dimensions[2].height = 30

rg.merge_cells("B3:J3")
c = rg["B3"]
c.value = ("Una fila por entrega. La columna «Estado» se calcula sola: avisa cuando la próxima revisión ya venció. "
           "Complete solo las columnas con fondo amarillo.")
c.font = font(9, False, "33406A"); c.fill = PatternFill("solid", fgColor=BAND)
c.alignment = Alignment(vertical="center", wrap_text=True)
rg.row_dimensions[3].height = 20

headers = ["Trabajador","RUT","Cargo o puesto","Centro de trabajo","Fecha entrega",
           "Próxima revisión","Motivo","Medio de evidencia","Estado"]
HR = 5
for i,h in enumerate(headers):
    cell = rg.cell(row=HR, column=2+i, value=h)
    cell.font = font(9, True, "FFFFFF")
    cell.fill = PatternFill("solid", fgColor=COBALT)
    cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    cell.border = box
rg.row_dimensions[HR].height = 30

ejemplo = ["María Soto Rivas","12.345.678-9","Operadora de bodega","Planta Quilicura",
           "2026-09-01","2027-09-01","Ingreso de un nuevo trabajador","Firma electrónica"]

FIRST, LAST = HR+1, HR+60
for r_ in range(FIRST, LAST+1):
    for i in range(9):
        cell = rg.cell(row=r_, column=2+i)
        cell.border = box
        cell.font = font(9)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if i < 8:
            cell.fill = PatternFill("solid", fgColor=YELLOW)
    if r_ == FIRST:
        for i,v in enumerate(ejemplo):
            rg.cell(row=r_, column=2+i, value=v)
        rg.cell(row=r_, column=2).font = font(9, False, "6B76A0", it=True)
    # F = Fecha entrega (col 6), G = Proxima revision (col 7)
    for col in (6, 7):
        rg.cell(row=r_, column=col).number_format = "yyyy-mm-dd"
    # Estado
    est = rg.cell(row=r_, column=10)
    est.value = (f'=IF(F{r_}="","",'
                 f'IF(G{r_}="","Sin próxima revisión",'
                 f'IF(G{r_}<TODAY(),"Vencida",'
                 f'IF(G{r_}-TODAY()<=30,"Por vencer","Vigente"))))')
    est.alignment = Alignment(vertical="center", horizontal="center")
    est.font = font(9, True)

dv2 = DataValidation(
    type="list", allow_blank=True,
    formula1='"Previo al inicio de las labores,Se incorpora a un nuevo proceso productivo,Cambian las tecnologías,Cambian los materiales o sustancias utilizados,Cambio de cargo o de tarea,Actualización de la matriz de riesgos,Otro"')
rg.add_data_validation(dv2); dv2.add(f"H{FIRST}:H{LAST}")
dv3 = DataValidation(type="list", allow_blank=True,
    formula1='"Firma manuscrita,Firma electrónica,Aceptación digital con fecha,Otro registro trazable"')
rg.add_data_validation(dv3); dv3.add(f"I{FIRST}:I{LAST}")

# resumen
SR = LAST + 2
rg.merge_cells(f"B{SR}:C{SR}")
c = rg[f"B{SR}"]; c.value = "RESUMEN"
c.font = font(10, True, "FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
c.alignment = Alignment(vertical="center", horizontal="left", indent=1)
rg.row_dimensions[SR].height = 20

resumen = [("Entregas registradas", f'=COUNTA(B{FIRST}:B{LAST})'),
           ("Vigentes",            f'=COUNTIF(J{FIRST}:J{LAST},"Vigente")'),
           ("Por vencer (30 días)",f'=COUNTIF(J{FIRST}:J{LAST},"Por vencer")'),
           ("Vencidas",            f'=COUNTIF(J{FIRST}:J{LAST},"Vencida")')]
for i,(lab, f_) in enumerate(resumen):
    rr = SR+1+i
    rg.merge_cells(f"B{rr}:C{rr}")
    a = rg[f"B{rr}"]; a.value = lab; a.font = font(9, True); a.fill = PatternFill("solid", fgColor=SOFT)
    a.alignment = Alignment(vertical="center", indent=1); a.border = box
    for cc in (2,3): rg.cell(row=rr, column=cc).border = box
    b = rg.cell(row=rr, column=4, value=f_)
    b.font = font(10, True, COBALT); b.border = box
    b.alignment = Alignment(vertical="center", horizontal="center")

NOTE = SR + 6
rg.merge_cells(f"B{NOTE}:J{NOTE}")
c = rg[f"B{NOTE}"]
c.value = ("La fila de ejemplo está en gris cursiva: bórrela antes de usar el registro. "
           "⚠️ La columna «Próxima revisión» NO corresponde a una obligación del DS 44: el artículo 15 no fija "
           "ninguna periodicidad. Solo exige entregar la información previo al inicio de las labores y volver a "
           "informar cada vez que la persona se incorpore a un nuevo proceso productivo o cambien las tecnologías, "
           "los materiales o las sustancias utilizados. Use esa columna únicamente si su empresa definió una "
           "política propia de revisión.")
c.font = font(8, False, "6B76A0", it=True)
c.alignment = Alignment(vertical="top", wrap_text=True)
rg.row_dimensions[NOTE].height = 30

rg.freeze_panes = f"B{FIRST}"

wb.save("/tmp/piezas/Formato-IRL-DS44-Tazki.xlsx")
print("guardado")
