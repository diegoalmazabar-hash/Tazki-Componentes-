#!/usr/bin/env python3
"""Genera el PDF EJECUTIVO del Plan de Generación de Demanda (pedido de Diego, 17-ago-2026).

Uso:  python3 make_pdf_ejecutivo.py plan-generacion-demanda.html [salida.pdf]

En qué se diferencia del make_pdf.py (espejo de la web):
  1. Parte con un RESUMEN EJECUTIVO (se lee de pdf_highlights.json — la rutina de los
     lunes lo reescribe con la semana) y las metas.
  2. SIN letra chica: se ocultan los bloques «Cómo verificar», las notas al pie de las
     tablas (.cap-note), los popups de keywords y la tarjeta «Estado de los datos».
     Ese detalle vive en la versión web; el PDF es para leerse de corrido.
  3. Diseño de página: cada bloque parte en página nueva, tablas con texto que se
     envuelve (no se cortan a lo ancho), tema claro forzado, A4.
  4. La bitácora va completa al final, con todos los días abiertos.
"""
import glob, io, json, os, subprocess, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "plan-generacion-demanda.html"
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "plan-ejecutivo.pdf")
TMP = "/tmp/plan/_print_exec.html"
HL = os.path.join(os.path.dirname(os.path.abspath(SRC)), "pdf_highlights.json")

hl = json.load(io.open(HL, encoding="utf-8"))

def items(lst, cls):
    out = ""
    for x in lst:
        out += ('<div class="hit %s"><div class="hit-t">%s</div><div class="hit-d">%s</div></div>'
                % (cls, x["t"], x["d"]))
    return out

RESUMEN = (
    '<section id="resumen-ejecutivo">'
    '<div class="sh"><div class="badge" style="background:#0C1E50">★</div><h2>Resumen ejecutivo</h2>'
    '<span class="cap">— ' + hl["fecha"] + '</span></div>'
    '<div class="hl-tit">Lo que se movió</div>' + items(hl["highlights"], "ok") +
    '<div class="hl-tit" style="margin-top:14px">En rojo, con fecha</div>' + items(hl["rojo"], "rojo") +
    '</section>'
)

INYECCION = r"""
<style>
  :root{--bg:#FFFFFF !important;--ink:#0C1E50 !important}
  html,body{background:#fff !important;color:#0C1E50 !important}

  /* ---- fuera la letra chica y lo operativo (vive en la web) ---- */
  .verify,.cap-note,.pbtn,.pop .pw{display:none !important}
  #estado-card,.gb-sub-solo{display:none !important}
  .pop{border-bottom:0 !important;cursor:auto !important}

  /* ---- resumen ejecutivo ---- */
  #resumen-ejecutivo{margin-top:26px}
  .hl-tit{font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#2E5BE6;margin:10px 0 8px}
  .hit{border:1px solid #E4E8F0;border-left:4px solid #178A5A;border-radius:10px;padding:9px 12px;margin-bottom:7px;page-break-inside:avoid}
  .hit.rojo{border-left-color:#C0392B}
  .hit-t{font-weight:800;font-size:13.5px}
  .hit-d{font-size:12.5px;color:#33406A;margin-top:2px;line-height:1.5}

  /* ---- diseño de página ---- */
  section{page-break-before:always;margin-top:0 !important;padding-top:10px}
  #resumen-ejecutivo{page-break-before:avoid}
  .goalbanner{page-break-inside:avoid;margin-top:16px !important}
  .card{page-break-inside:avoid}
  .read{page-break-inside:avoid}

  /* ---- tablas que no se cortan a lo ancho ---- */
  table{font-size:10.5px !important;width:100% !important;table-layout:auto}
  th,td{white-space:normal !important;padding:5px 6px !important}
  .tscroll{overflow:visible !important}

  /* ---- bitácora ---- */
  details{display:block !important}
  details>summary{display:block !important;list-style:none !important;cursor:auto !important}
  details>summary::-webkit-details-marker{display:none !important}
  details>summary::marker{content:"" !important}
  .day{page-break-inside:avoid}
  .day>summary{background:#EEF1F6 !important;font-weight:800 !important;color:#0C1E50 !important;border-bottom:1px solid #C7D0E0}

  @media print{
    @page{size:A4;margin:13mm 11mm}
    thead{display:table-header-group}
    a[href]:after{content:""}
  }
</style>
<script>
window.addEventListener("load", function(){
  setTimeout(function(){
    document.querySelectorAll("details").forEach(function(d){ d.open = true; });
    // marcar la tarjeta «Estado de los datos» para ocultarla
    document.querySelectorAll(".card.pad").forEach(function(c){
      if (c.textContent.indexOf("Estado de los datos") >= 0) c.id = "estado-card";
    });
    // ocultar la nota larga bajo la tabla de metas
    document.querySelectorAll(".goalbanner > .gb-sub").forEach(function(s){ s.classList.add("gb-sub-solo"); });
    // insertar el resumen ejecutivo antes de las metas
    var gb = document.querySelector(".goalbanner");
    gb.insertAdjacentHTML("beforebegin", RESUMEN_HTML);
    document.documentElement.setAttribute("data-print-ready", "1");
  }, 1200);
});
var RESUMEN_HTML = __RESUMEN__;
</script>
</head>"""

INYECCION = INYECCION.replace("__RESUMEN__", json.dumps(RESUMEN, ensure_ascii=False))

src = io.open(SRC, encoding="utf-8").read()
ancla = "</style>"
assert ancla in src, "no encontré dónde inyectar"
i = src.index(ancla) + len(ancla)
os.makedirs(os.path.dirname(TMP), exist_ok=True)
io.open(TMP, "w", encoding="utf-8").write(src[:i] + INYECCION + src[i:])

shell = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
chrome = shell[0] if shell else "/opt/pw-browsers/chromium/chrome-linux/chrome"
subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--virtual-time-budget=15000",
                "--print-to-pdf=" + OUT, "file://" + TMP],
               check=True, capture_output=True, timeout=180)
kb = os.path.getsize(OUT) // 1024
print("✓ PDF ejecutivo:", OUT, "(%d KB)" % kb)
if kb < 40:
    print("⚠️  Sospechosamente liviano: revisa que haya renderizado bien.")
