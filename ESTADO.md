# Estado del proyecto — Plan de contenidos Tazki

> Resumen para retomar el trabajo en cualquier sesión futura de Claude Code.
> El trabajo estratégico/operativo (HubSpot, análisis, equipo) se sigue en **Cowork**.
> Esta sesión de Code mantiene los **HTML de gestión y dashboard**.

## ⭐ FUENTE DE VERDAD: Documento Maestro (de Cowork)
`MAESTRO-Maquina-de-Leads-Tazki.pdf` — la guía única y autocontenida (Diego + Axel, 3 jul 2026). Integra baseline real de HubSpot, modelo TOFU/MOFU/BOFU, propiedades, workflows, forms, los 6 pilares, copys, calendario y el backlog (§11). **Cualquier ajuste futuro se alinea a este documento.**

- **`gestion-maquina-leads.html`** — tablero de ejecución generado desde el §11 (41 tareas con checkbox+localStorage, filtros por fase/área/estado, progreso por fase, bloqueo por dependencias, buscador y enlaces a specs).
- Baseline actualizado (maestro §0, HubSpot ene–jun 2026): TOFU casi inexistente (8 leads en el año), MQL cayendo (54→41→29 abr–jun), 90% de las vistas en la home. Página ebook convierte 16% pero sin tráfico.
- Decisión clave: **Julio = piloto ebook DS44 punta a punta** (sin meta; agosto fija meta con datos).
- Deuda técnica: Supermetrics expiró el 1/jul → reconectar Search Console (tarea M4).

## Archivo principal
- `plan-contenidos-tazki.html` — dashboard interactivo autocontenido (HTML+CSS+JS en un solo archivo, funciona offline).
- Rama de trabajo: `claude/hola-920adh`. Todo commiteado y pusheado a GitHub.

## Qué tiene el dashboard hoy (7 pestañas)
1. **Flujo del funnel** — TOFU / MOFU / BOFU, cómo entra el contenido por Carlos (prevencionista).
2. **Matriz de contenidos** — cuadrícula tema × canal (9 temas × 5 canales) + lista filtrable de 40 piezas.
3. **Quick wins SEO** — oportunidades de Search Console (arreglar títulos, empujar a pág. 1, crear páginas).
4. **Arranque 90 días** — plan julio–septiembre.
5. **Medición** — KPIs por etapa y canal (qué mirar, qué ignorar, dónde se lee).
6. **Funnel comercial** — embudo de conversión con baseline al 18-jul (aún en `—%`) + 3 objetivos del trimestre.
7. **Dashboard (Nubox)** — modelo replicado con datos de referencia de Nubox (a reemplazar por Tazki).

## Baseline real encontrado en HubSpot (foto del día de la consulta)
Funnel por etapa (contactos):
- Lead: 9.745 · **MQL: 11 (⚠️)** · SQL: 4 · Opportunity: 1.943 · Customer: 71

Negocios (moneda = CLF = UF):
- Lead Generation: 2.310 negocios · 638,6 UF
- Pipeline de ventas: 1.031 negocios · 17.877 UF
- Clientes (Customer Success): 183 negocios · 3.378,8 UF

MQL por fuente (solo 11): Organic 5 · Direct 4 · Paid Search 1 · Offline 1.

## Hallazgos / pendientes
1. **⚠️ Etapa MQL casi sin usar** (11 MQL vs 9.745 leads y 1.943 oportunidades). Los contactos saltan de Lead → Opportunity sin pasar por MQL. **Prioridad 1:** definir criterio de MQL + Workflow en HubSpot que setee `Lifecycle stage = MQL` automáticamente. Sin esto el funnel no se puede medir bien.
2. **Deal stages desordenadas:** hay una etapa con valor `closedlost` pero etiqueta "Closed Won", y "Meeting Set" duplicado. Limpiar antes de calcular Close Rate.
3. **Baseline al 18-jul:** una vez arreglado el MQL, congelar la foto y cargar los números reales en la pestaña "Funnel comercial" (reemplazar los `—%`) y "Dashboard (Nubox)".
4. **Supermetrics no conecta** desde el entorno web/remoto (requiere login OAuth). HubSpot sí funciona vía conector.
5. **Rebrand pendiente con Tomás** (assets nuevo logo + fecha de salida), ebook, caso Banco Falabella, blog.

## Objetivos del trimestre (contexto comercial)
- **SEO:** revertir caída 150K → 97K keywords.
- **Contenido:** bajar producción de video a ~15% del tiempo de Diego; Diego 50% en lo comercial.
- **Modelo a replicar:** dashboard Nubox 2023 (leads · MQL · tasa conversión · ticket promedio).

## Cómo actualizar el dashboard HTML
Los datos del "Dashboard (Nubox)" están en arrays editables al inicio del `<script>`:
`DASH_FUNNEL`, `DASH_META`, `DASH_CH`, `DASH_TOTAL`. Cambiar esos valores actualiza embudo, semáforo y tabla automáticamente.
