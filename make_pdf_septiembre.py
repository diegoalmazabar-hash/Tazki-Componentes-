#!/usr/bin/env python3
"""Genera el PDF del plan orgánico de septiembre.

Uso:  python3 make_pdf_septiembre.py plan-septiembre.html [salida.pdf]

Fuerza el tema claro (el PDF va a papel blanco), evita que las tarjetas y los
flujos se partan entre páginas, y deja márgenes de impresión razonables.
"""
import glob, io, os, subprocess, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "plan-septiembre.html"
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "plan-septiembre.pdf")
TMP = "/tmp/_sep_print.html"

INY = r"""
<style>
  /* el PDF se imprime en papel: tema claro sí o sí */
  :root{color-scheme:light !important;
    --ground:#FFFFFF !important; --surface:#FFFFFF !important; --surface-2:#F2F5FB !important;
    --ink:#101B3A !important; --ink-2:#47527A !important; --ink-3:#6E7898 !important;
    --line:#D8DEEC !important; --line-soft:#E8ECF5 !important;
    --accent:#1537D1 !important; --accent-soft:#E7EBFC !important;
    --good:#12704F !important; --good-soft:#E2F1EA !important;
    --bad:#A32C22 !important; --bad-soft:#FAE8E5 !important;
    --warn:#8A5D0E !important; --warn-soft:#F8EEDA !important;}
  html,body{background:#fff !important}
  @page{size:A4;margin:12mm 10mm}
  .wrap{max-width:100% !important;padding:0 !important;gap:16px !important}
  h1{font-size:30px !important}
  .goal,.find,.cal,.script,.needs,.flow{break-inside:avoid;page-break-inside:avoid}
  .goal{break-before:auto}
  .step,.mail,.row{break-inside:avoid;page-break-inside:avoid}
  table{font-size:11.5px !important}
  th,td{padding:5px 7px !important}
  .tscroll{overflow:visible !important}
  .sub,.step .body,.say{font-size:13.5px !important}
  .notes p{font-size:11px !important}
</style>
<script>
window.addEventListener("DOMContentLoaded",function(){
  document.documentElement.setAttribute("data-theme","light");
  setTimeout(function(){document.documentElement.setAttribute("data-print-ready","1");},600);
});
</script>
"""

src = io.open(SRC, encoding="utf-8").read()
i = src.rindex("</style>") + len("</style>")
io.open(TMP, "w", encoding="utf-8").write(src[:i] + INY + src[i:])

shell = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
chrome = shell[0] if shell else "/opt/pw-browsers/chromium/chrome-linux/chrome"
subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--virtual-time-budget=12000",
                "--print-to-pdf=" + OUT, "file://" + TMP],
               check=True, capture_output=True, timeout=180)
kb = os.path.getsize(OUT) // 1024
print("✓ PDF generado:", OUT, "(%d KB)" % kb)
if kb < 25:
    print("⚠️  Sospechosamente liviano: revisar el render.")
