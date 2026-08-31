# -*- coding: utf-8 -*-
import io, json, re

SRC='plan-generacion-demanda.html'
OUT='/tmp/claude-0/-home-user-Tazki-Componentes-/01d59e20-42e3-5b66-b7e9-f853518c19ac/scratchpad/generacion-demanda-tazki.html'
s=io.open(SRC,encoding='utf-8').read()
hl=json.load(io.open('pdf_highlights.json',encoding='utf-8'))

# 1) titulo del artefacto
s=s.replace('<title>Plan de Generación de Demanda · Tazki</title>',
            '<title>Generación de Demanda Tazki</title>',1)

DARK=('--bg:#0A1024;--card:#111A33;--ink:#EAF0FB;--ink-2:#B9C4E0;--ink-3:#8090B8;'
      '--line:#25304C;--line-2:#1B2540;--navy:#DDE6F5;--good:#4FD08B;--good-bg:#12301F;'
      '--bad:#F0796B;--bad-bg:#331612;--warn:#E7B252;--warn-bg:#2E2611;--accent:#6E8BFF;'
      '--pink:#D48CDD;--curbg:#182449;')

# 2) tema: respetar la eleccion explicita del lector (data-theme) ademas del sistema
old_dark=s[s.find('@media (prefers-color-scheme:dark)'):s.find('}}',s.find('@media (prefers-color-scheme:dark)'))+2]
new_dark=('@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){'+DARK+'}}\n'
          ':root[data-theme="dark"]{'+DARK+'}')
s=s.replace(old_dark,new_dark,1)

def items(lst, cls):
    out=''
    for x in lst:
        out+=('<div class="hit %s"><div class="hit-t">%s</div><div class="hit-d">%s</div></div>'
              % (cls, x['t'], x['d']))
    return out

RESUMEN=('<section id="resumen-ejecutivo">'
 '<div class="sh"><div class="badge" style="background:var(--navy);color:var(--card)">★</div>'
 '<h2>Resumen ejecutivo</h2><span class="cap">— '+hl['fecha']+'</span></div>'
 '<div class="hl-grid">'
 '<div><div class="hl-tit">Lo que se movió</div>'+items(hl['highlights'],'ok')+'</div>'
 '<div><div class="hl-tit rojo">En rojo</div>'+items(hl['rojo'],'rojo')+'</div>'
 '</div></section>')

EXTRA=('<style>\n'
 '  /* --- version ejecutiva: fuera la letra chica operativa --- */\n'
 '  .verify,.cap-note{display:none !important}\n'
 '  #resumen-ejecutivo{margin-top:22px}\n'
 '  .hl-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}\n'
 '  @media (max-width:760px){.hl-grid{grid-template-columns:1fr}}\n'
 '  .hl-tit{font-weight:800;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;\n'
 '          color:var(--good);margin:0 0 9px}\n'
 '  .hl-tit.rojo{color:var(--bad)}\n'
 '  .hl-grid>div{display:flex;flex-direction:column;gap:8px}\n'
 '  .hit{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--good);\n'
 '       border-radius:10px;padding:10px 13px}\n'
 '  .hit.rojo{border-left-color:var(--bad)}\n'
 '  .hit-t{font-weight:800;font-size:13.5px;color:var(--navy);text-wrap:balance}\n'
 '  .hit-d{font-size:12.5px;color:var(--ink-2);margin-top:3px;line-height:1.55}\n'
 '  a:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--accent);outline-offset:2px}\n'
 '  @media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important}}\n'
 '</style>\n')

# el resumen abre el documento, justo despues del encabezado
anchor='<div class="card pad" style="margin-top:12px;font-size:12.5px;line-height:1.7">'
assert s.count(anchor)==1
s=s.replace(anchor, RESUMEN+'\n  '+anchor, 1)

# el <style> extra va al final del primer bloque de estilos
k=s.find('</style>')
s=s[:k+8]+'\n'+EXTRA+s[k+8:]

io.open(OUT,'w',encoding='utf-8').write(s)
print('escrito',OUT,len(s))
