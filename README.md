# Growth Hub · Tazki

Sitio interno de paneles de growth, publicado con GitHub Pages desde esta rama (`gh-pages`):
**https://diegoalmazabar-hash.github.io/Tazki-Componentes-/**

## Páginas

| Archivo | Página | Datos | Actualización |
|---|---|---|---|
| `index.html` | Panel MQL (funnel + panel de negocios) | HubSpot CRM + DiIO | **AUTOGENERADA** — rutina diaria 8:00 AM (Chile) desde una sesión de Claude Code |
| `maquina-de-leads-tazki.html` | Plan de contenidos (Máquina de Leads) | manual | editar directo |
| `google-ads-tazki.html` | Panel Google Ads | Supermetrics | editar directo |
| `roi.html` | Calculadora ROI | manual | editar directo |

## Reglas para trabajar en este hub (leer antes de editar)

1. **`index.html` NO se edita a mano.** Lo regenera a diario una rutina de Claude Code
   (sesión "Panel MQL") que extrae los negocios MQL de HubSpot, recalcula el funnel,
   el semáforo y los desgloses, y hace push. Cualquier edición manual del contenido
   del panel será sobrescrita en la próxima corrida. Los ajustes al panel MQL se piden
   en la conversación de Claude que mantiene esa rutina.
   - **Excepción**: el bloque entre `<!-- MENU LATERAL TAZKI -->` y
     `<!-- FIN MENU LATERAL TAZKI -->` (todo lo que está entre `<body>` y el
     `<title>` del panel) SÍ se puede editar a mano — el script de publicación lo
     preserva tal cual en cada regeneración. Ahí vive el menú lateral compartido.
2. **Las demás páginas se editan libremente** desde cualquier sesión o a mano.
   La rutina del panel MQL solo toca `index.html` (con `git add index.html`, nunca `-A`).
3. **Menú lateral compartido**: cada página nueva debe (a) agregarse como archivo
   `.html` en esta rama, (b) sumarse al `<nav>` del menú en TODAS las páginas
   (el bloque `MENU LATERAL TAZKI` está copiado en cada archivo), con su
   `data-p` correspondiente en el mapa del script del menú.
4. **Páginas autoactualizables**: para que una página nueva se alimente sola de
   HubSpot/Supermetrics, se crea una rutina programada (scheduled trigger) en la
   sesión de Claude Code que la construyó, con el patrón: extraer datos por MCP →
   regenerar el HTML (datos embebidos como JSON en un `const DATA = [...]`) →
   `git pull` → escribir SOLO su archivo → commit + push a `gh-pages`.
   Siempre `git pull` antes de escribir, y nunca borrar archivos ajenos.
5. **Privacidad**: este repo y el sitio son PÚBLICOS. No publicar aquí datos que no
   deban ser visibles fuera de Tazki sin autorización explícita de Diego.

## Arquitectura del panel MQL (referencia para replicar en otras páginas)

- Los datos van embebidos en el HTML (`const DEALS = [...]`) — sin backend.
- Filtros globales (pipeline, propietario, fuente, sitio, fechas) recalculan todo en JS.
- Fuentes en HubSpot: deals con "MQL" en el nombre; fuente analítica del contacto
  asociado (`hs_analytics_source`); notas y tareas por SQL (`query_crm_data`);
  fechas de entrada por etapa (`fecha_de_ingreso_*`, `hs_v2_date_entered_current_stage`).
- Tema claro/oscuro por tokens CSS; tooltips y tablas accesibles.
