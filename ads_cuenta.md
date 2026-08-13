# Cuenta Google Ads Tazki — bitácora técnica

> Este archivo vive en el repositorio a propósito. La carpeta de skills
> (`/root/.claude/skills/gestion-google-ads-tazki/`) se ha borrado tres veces en
> reinicios del contenedor. El repo sobrevive; la skill no. Si algo no calza con
> lo que devuelve la API, manda la API.

Actualizado: 13 de agosto de 2026.

## Estructura

- **Tazki - SST/HSEQ - Search** (`23995581786`) — genérica, la principal. Search pura,
  MAXIMIZE_CONVERSIONS, geo PRESENCE Chile, $24.000 CLP/día, 7 días 06:00–24:00.
  Grupos: A - Sistema Gestión SST (anuncio `819974344713`), B - Software Prevención de
  Riesgos (`815557848862`), C - HSEQ HSE (`815524188918`). Arrancó el 4-jul-2026.
- **Tazki - Marca - Search - v2** (`23886304307`) — $4.000 CLP/día, phrase "tazki*".
- Landing principal: https://soluciones.tazki.cl/software-prevencion-riesgos

## ⚠️ Trampas de la API (no repetir)

1. **`campaign_update` sobre anuncios los BORRA y RECREA en pausa.** Cada reintento genera otro
   duplicado pausado. Editar una vez, pedirle a Diego que active desde la interfaz, nunca
   reintentar el enable por API.
2. **`targeting` reemplaza el bloque completo**, pero en esta cuenta solo contiene
   `negative_keywords`: geo, horario y red viven en `platform_details`. Receta segura: leer con
   `campaign_and_resource_get` (detail FULL), enviar `targeting = existentes + nuevas`, NO enviar
   `ad_groups`, y verificar releyendo.
3. **`ad_groups[].add_keywords` sí es seguro**: agrega sin tocar anuncios (la respuesta confirma
   "existing ads that were not changed").
4. **No reescribir por API anuncios con historial acumulado** — se pierde el historial de CTR.

## Conteo de negativas

**868** en la pestaña «Palabras clave negativas», pero mezcla nivel campaña y nivel grupo. Las 462
del 9-ago eran solo de campaña. Al comparar, mirar SIEMPRE la columna «Nivel». No hubo escritura
masiva: es la misma cuenta contada de dos formas.

## Cómo leer impression share (crítico)

Las tres métricas **suman 100% por construcción**: son una partición de las impresiones
disponibles, no mediciones independientes. Presupuesto y ranking se **turnan**: si el presupuesto
se agota temprano nunca entras a la subasta y la pérdida se anota como presupuesto; si aguanta,
entras y lo que pierdes se anota como ranking.

| Semana (SST/HSEQ) | IS | Ranking | Presupuesto |
|---|---|---|---|
| 6–12 jul | 13,7% | 6,1% | 80,1% |
| 13–19 jul | 20,2% | 59,5% | 20,3% |
| 20–26 jul | 12,1% | 15,4% | 72,8% |
| 27 jul–2 ago | 10,1% | 73,7% | 17,6% |
| 3–9 ago | 11,0% | **88,6%** | 0,4% |
| 10–11 ago | 11,0% | 24,1% | 65,1% |

El IS lleva seis semanas plano en 10–12%: **no hubo derrumbe de calidad**. Pero el 88,6% sí es la
primera medición limpia y es mala. Ponderado de las 6 semanas: IS 12,5%, ranking 61,9%,
presupuesto 25,9% — **los dos problemas son reales**.

⚠️ **La pérdida por ranking BAJA cuando gastas menos.** Recortar mejora el número sin mejorar nada.
Nunca usarlo como semáforo para recortar.
⚠️ Si sube la calidad y se ganan más subastas, se chocará más seguido con el presupuesto. No
prometer que la calidad sola resuelve todo.

| Métrica | Sano | Hoy | Meta 3 meses |
|---|---|---|---|
| Impression share | ≥60% (30–50% ya es fuerte en genérica) | 11% | 30% |
| Perdido por ranking | ≤20% | 89% | 50% |
| Perdido por presupuesto | ≤10% | 0,4% ✅ | — |

Aparte: **Marca tiene IS 19,3%**, muy bajo para campaña de marca propia (debería ir sobre 80%). Sin
investigar.

## Quality Score — diagnóstico del 13-ago (35 keywords, 14-jul a 12-ago)

**Las 26 keywords con nota tienen «Exp. en página de destino: Inferior al promedio». Las 26, sin
excepción, en los tres grupos.** La relevancia del anuncio en cambio sale Superior en 15, Promedio
en 6, Inferior en 5. **El anuncio no es el problema; la landing sí, y es sistémico.**

Cuatro están **«Apto (limitado) — No suele publicarse (Nivel de calidad bajo)»**: la estrella en
frase, su gemela amplia sin tildes, y las dos de `app prevención de riesgos`. `genesis app sst` la
detuvo Google sola.

**La estrella NO arrastra el ranking**: `"sistema de gestión de seguridad y salud en el trabajo"`
pierde 53% contra 57% del promedio de campaña. Las que arrastran: `software gestión sst` (70%),
`"software de prevención de riesgos laborales"` (76%), `software seguridad laboral` (78%).

Economía de la estrella: 19% del gasto, **50% de las conversiones**, CPA $31.138. Sacarla subiría
el CPA de campaña de $83.698 a **$135.944 (+62%)**. QS 1 no es keyword mala, es keyword cara.
La más eficiente de la cuenta es `"software seguridad ocupacional"` ($11.706/conv).

## Concordancia — el corte más limpio

| | Keywords | Costo | Conv. | CPA |
|---|---|---|---|---|
| Amplia | 18 | $230.668 | 1 | $230.668 |
| Frase | 14 | $406.806 | 9 | $45.201 |
| Exacta | 3 | $3.482 | 0 | — |

17 de 18 amplias nunca convirtieron ($201.677). ⚠️ **El corte por grupo y el corte por concordancia
se SOLAPAN $119.300: no sumarlos.** Unión real $320.357, no $439.657.

## PageSpeed — la landing NO es problema técnico (13-ago)

| | Móvil | Escritorio |
|---|---|---|
| **Core Web Vitals (usuarios reales)** | **✅ Aprobado** | **✅ Aprobado** |
| LCP | 1,5 s | 1,1 s |
| CLS | 0 | 0,04 |
| Rendimiento (lab) | 80 | 98 |
| SEO / Prácticas | 100 / 100 | 100 / 100 |

El 80 de móvil es laboratorio con Moto G Power en 4G lento; el campo manda y está verde.
**Por descarte: el «Inferior al promedio» es de RELEVANCIA, no de velocidad.** La landing se titula
«Centraliza tu prevención en una sola plataforma» y la keyword que convierte busca «sistema de
gestión de seguridad y salud en el trabajo». El arreglo de vocabulario del 25-jul no bastó.
Pendientes menores: contraste insuficiente (accesibilidad, en rojo) e imágenes sin width/height.

## Landings: una por grupo de anuncios, NO una por keyword (13-ago)

Una landing por keyword no sirve: Google evalúa la experiencia de la página **por keyword contra la
página de destino del grupo**, y partir el tráfico en 6 páginas deja a cada una sin datos
suficientes para que el algoritmo aprenda. El corte correcto es el grupo de anuncios, porque cada
grupo ya agrupa intenciones equivalentes.

| Grupo | Conversiones | Landing |
|---|---|---|
| A · Sistema Gestión SST | 8 | `soluciones.tazki.cl/es/sistema-gestion-seguridad-salud-trabajo` (creada y publicada 13-ago) |
| B · Software Prevención de Riesgos | 1 | `soluciones.tazki.cl/software-prevencion-riesgos` (ya calzaba) |
| C · HSEQ HSE | 1 | `soluciones.tazki.cl/software-hseq` (ya existía) |

**Landing A — creada el 13-ago como borrador, contentId `219388262058`.** Clon de la B
(`217060324610`), así que hereda tema, estructura y el **mismo formulario**
`07323525-2476-418d-a087-e7a0fbc19275`. Cambios respecto del original:

- H1: «El sistema de gestión de seguridad y salud en el trabajo, en una sola plataforma» — la frase
  exacta que busca la keyword estrella, que en la B no aparecía en el H1.
- `htmlTitle`, meta description, eyebrow, H2 de módulos y checklist reescritos hacia SG-SST,
  DS 44 y Ley 16.744.
- FAQ: primera pregunta ahora es la definicional («¿Qué es un SG-SST?»). **El módulo FAQ acepta
  máximo 8 ítems**; agregar uno obliga a sacar otro.
- Contraste del `headHtml` corregido: `rgba(255,255,255,.4)` → `.78` (era el rojo de accesibilidad
  de PageSpeed).

Ojo: al publicarla, el idioma `es` le antepuso **`/es/`** al slug, a diferencia de las landings B y C
que no lo llevan. No afecta a Ads. Diego la publicó así el 13-ago.

**Para conectarla: NO editar la URL final del anuncio por API** — eso borra el anuncio y lo recrea
en pausa. Se le pone la URL final **a la keyword**, que sobrescribe la del anuncio sin tocarlo.

**Ejecutado el 13-ago:** URL final cargada a las **6 keywords activas del Grupo A** —
`"sistema de gestión de seguridad y salud en el trabajo"` (5,00 conv), `"software seguridad
ocupacional"` (2,00), `"software gestión sst"` (0,67), `"software sst"` (0,33), `[software seguridad
ocupacional]` y `[sistema gestión seguridad laboral]`. A las detenidas no se les puso URL.

## AI Max: marginal

$23.485, **cero conversiones**, 2,6% del gasto. Y NO explica el crecimiento de la subasta: las
impresiones disponibles ya se habían triplicado (3.079 → 8.784) la semana ANTES de activarlo el
22-jul. El crecimiento es rampa de campaña nueva + consolidación de las campañas pausadas el 13-jul.

## Historial de cambios

- **1 ago** — extensiones completas en ambas campañas (6 textos destacados, fragmentos «Servicios»,
  6 vínculos en SST/HSEQ y 6 en Marca). SST/HSEQ tiene imágenes como assets (`338226009506`,
  `338361869895`): siempre reenviarlas al actualizar extensiones.
- **6 ago** — anuncio del Grupo A reescrito con foco SGSST. Dos keywords a exacta.
- **9 ago** — 23 negativas en frase (439 → 462 a nivel campaña) tras el clic de $2.028 en «urbicad».
- **10 ago** — `software seguridad ocupacional` agregada en EXACTA. Resultó la más eficiente.
- **13 ago** — 9 negativas de la familia consultoría/implementación, incluida `[implementacion sg
  sst]` (un clic de **$15.154** sin conversión). NO se negaron `implementacion` como raíz,
  `auditoria`, `capacitacion` ni `gratis` («software sst gratis» convirtió 0,33).
- **13 ago** — `"software hseq"` (frase) pausada: $870, 0 conversiones. Quedó viva en la limpieza.
- **13 ago** — **24 keywords pausadas: $249.844, el 31% del gasto, cero conversiones.** De 35 a 10
  keywords activas SIN perder ninguna conversión (total se mantuvo en 10,00). Se dejaron las 3
  exactas y `plataforma hse` amplia (única amplia que convirtió).

## Pendientes

- **Cambiar la URL final del ANUNCIO del Grupo A a la landing A — pero recién DESPUÉS de la lectura
  del 17-ago.** Hoy no urge: la URL de la keyword manda sobre la del anuncio y las 6 activas ya la
  tienen, así que el 100% del tráfico llega bien. Se posterga porque editar un anuncio lo elimina y
  crea uno nuevo con estadísticas en cero, y ese anuncio se reescribió el 6-ago: cambiarlo ahora
  metería una segunda variable justo cuando estamos midiendo el efecto de la landing.
  ⚠️ Mientras tanto, **toda keyword nueva del Grupo A hereda la URL vieja del anuncio** — hay que
  ponerle la URL final a mano al crearla.
- La landing B (`software-prevencion-riesgos`) NO se toca: sigue siendo la del Grupo B y ahí calza.
- **Lectura del 17-ago: el número que manda es si la estrella sale de «Rara vez se publica (nivel de
  calidad bajo)».** Es la keyword que aporta 5 de 8 conversiones y Google la tiene frenada; la
  landing A se construyó exactamente para eso. Leer también CPA y % de gasto irrelevante.
  La columna «Nivel de calidad» quedó agregada en la pantalla de keywords de Diego.
- Arreglar contraste en la landing B (en la A ya quedó corregido).
- 3 recomendaciones de keywords que la API no muestra: revisarlas con Diego desde su pantalla.

## Rechazadas permanentemente (no volver a proponer)

Red de socios, expansión Display, estrategia de cartera, segmentación por listas de clientes,
aflojar la concordancia de Marca.
