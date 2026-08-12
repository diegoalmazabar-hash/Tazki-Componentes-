#!/usr/bin/env python3
"""Genera el PDF del Plan de Generación de Demanda.

Uso:  python3 make_pdf.py plan-generacion-demanda.html [salida.pdf]

Qué resuelve: el Plan es una página web con ventanas emergentes (las listas de
palabras clave que aparecen al pasar el mouse en la tabla KWNEW). En un PDF no
existe el hover, así que ese contenido se PERDERÍA. Este script lo saca de los
tooltips y lo imprime como un anexo al final, numerado, y deja en la tabla una
marca que apunta al anexo. Nada de lo que se ve en pantalla queda fuera.

También fuerza el tema claro (el PDF se imprime en papel blanco), evita cortes
de página feos y expande cualquier <details> cerrado.
"""
import glob, os, subprocess, sys, shutil, io

SRC = sys.argv[1] if len(sys.argv) > 1 else "plan-generacion-demanda.html"
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "plan-generacion-demanda.pdf")
TMP = "/tmp/plan/_print.html"

INYECCION = r"""
<style>
  :root{--bg:#F7F9FC !important;--ink:#0C1E50 !important}
  html,body{background:#fff !important;color:#0C1E50 !important}
  .pop{border-bottom:0 !important;cursor:auto !important}
  .pop .pw{display:none !important}          /* el contenido se mueve al anexo */
  .ref{font-size:9px;vertical-align:super;color:#2E5BE6;font-weight:700;margin-left:2px}
  details{display:block !important}
  details>summary{display:none !important}
  #anexo{margin-top:34px;page-break-before:always}
  #anexo h2{font-size:19px;margin:0 0 4px}
  #anexo .grupo{margin-top:18px;page-break-inside:avoid}
  #anexo .tit{font-weight:800;font-size:13px;color:#0C1E50;margin-bottom:6px}
  #anexo .cols{column-count:3;column-gap:18px;font-size:11px;line-height:1.5}
  #anexo .cols div{break-inside:avoid;padding:1px 0;color:#3A4A6B}
  @media print{
    @page{size:A4;margin:14mm 12mm}
    .card,section,table{page-break-inside:avoid}
    section{page-break-after:auto}
    thead{display:table-header-group}
    a[href]:after{content:""}
    .tscroll{overflow:visible !important}
  }
</style>
<script>
window.addEventListener("load", function(){
  setTimeout(function(){
    // 1) abrir todo lo plegable
    document.querySelectorAll("details").forEach(function(d){ d.open = true; });
    // 2) sacar las ventanas emergentes a un anexo
    var pops = document.querySelectorAll(".pop");
    if (pops.length) {
      var an = document.createElement("section");
      an.id = "anexo";
      an.innerHTML = '<div class="sh"><h2>Anexo · listas completas de palabras clave</h2></div>' +
        '<p class="cap-note">En la versión web estas listas aparecen al pasar el mouse sobre los ' +
        'números de la tabla «Palabras clave nuevas». Acá van completas, para que el PDF no pierda nada. ' +
        'Cada bloque lleva la marca con la que aparece referenciado en la tabla.</p>';
      var n = 0;
      pops.forEach(function(p){
        var w = p.querySelector(".pw");
        if (!w) return;
        n++;
        var marca = "A" + n;
        var b = w.querySelector("b");
        var titulo = b ? b.textContent : "Lista " + n;
        var items = Array.prototype.map.call(w.querySelectorAll(".kw"), function(k){
          return "<div>" + k.textContent + "</div>";
        }).join("");
        var g = document.createElement("div");
        g.className = "grupo";
        g.innerHTML = '<div class="tit">' + marca + " · " + titulo + '</div><div class="cols">' + items + "</div>";
        an.appendChild(g);
        var r = document.createElement("span");
        r.className = "ref"; r.textContent = marca;
        p.appendChild(r);
      });
      if (n) document.querySelector(".wrap").appendChild(an);
      document.title = document.title + " · " + n + " listas en anexo";
    }
    document.documentElement.setAttribute("data-print-ready", "1");
  }, 1200);
});
</script>
</head>"""

src = io.open(SRC, encoding="utf-8").read()
# el Plan es un fragmento sin <head>: se inyecta después del primer bloque de estilos
ancla = "</style>" if "</style>" in src else None
assert ancla, "no encontré dónde inyectar (ni </head> ni </style>)"
i = src.index(ancla) + len(ancla)
io.open(TMP, "w", encoding="utf-8").write(src[:i] + INYECCION + src[i:])

shell = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
chrome = shell[0] if shell else "/opt/pw-browsers/chromium/chrome-linux/chrome"
subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--virtual-time-budget=15000",
                "--print-to-pdf=" + OUT, "file://" + TMP],
               check=True, capture_output=True, timeout=180)
kb = os.path.getsize(OUT) // 1024
print("✓ PDF generado:", OUT, "(%d KB)" % kb)
if kb < 40:
    print("⚠️  Sospechosamente liviano: revisa que haya renderizado bien.")
