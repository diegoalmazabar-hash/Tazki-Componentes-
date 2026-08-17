# Cuenta Google Ads Tazki — bitácora técnica

> Este archivo vive en el repositorio a propósito. La carpeta de skills
> (`/root/.claude/skills/gestion-google-ads-tazki/`) se ha borrado tres veces en
> reinicios del contenedor. El repo sobrevive; la skill no. Si algo no calza con
> lo que devuelve la API, manda la API.

Actualizado: 13 de agosto de 2026.

## Estructura

- **Tazki - SST/HSEQ - Search** (`23995581786`) — genérica, la principal. Search pura,
  MAXIMIZE_CONVERSIONS, $24.000 CLP/día, 7 días 06:00–24:00. Geo: Chile / Presencia
  **desde el 14-ago** (⚠️ hasta esa fecha estuvo en «Todos los países y territorios» — ver
  historial; una nota anterior de esta bitácora decía "PRESENCE Chile" y estaba ERRADA:
  la opción Presencia era correcta pero la ubicación era el mundo entero).
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
| C · HSEQ HSE | 1 | `soluciones.tazki.cl/software-hseq` (existía, pero el anuncio NO apuntaba ahí) |

**El anuncio del Grupo C apuntaba a `/software-prevencion-riesgos`** — el mismo error que tenía A,
descubierto el 13-ago. Y su URL visible decía `soluciones.tazki.cl/hseq/demo`, o sea ni siquiera
coincidía con lo que el propio anuncio prometía. **Esto explica el diagnóstico completo del Quality
Score: dos de los tres grupos caían en la misma página, escrita para el tercero.** No era un
misterio de contenido, era de cableado. (Lo que queda abierto: la B también sale «Inferior al
promedio» y ella sí estaba en su página correcta — ese grupo tiene un problema propio de contenido.)

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

**Landing C (`214952422274`, «Landing HSEQ») — retocada el 13-ago.** Es la mejor construida de las
tres: barra de cifras, sección de problema con 6 tarjetas, GIF de flujo, tarjeta DT. Diego cambió el
H1 a «Plataforma HSE chilena: centraliza calidad, seguridad, medioambiente y salud» (la única
keyword viva del grupo es `plataforma hse`, sin la Q, y la página solo decía «HSEQ») y reemplazó la
barra de logos de texto por logos reales. Yo agregué: eyebrow `PLATAFORMA HSE · SOFTWARE HSEQ
CHILE`, la FAQ definicional «¿Qué es una plataforma HSE y en qué se diferencia de una HSEQ?», y
título/meta SEO.

⚠️ **La landing C tiene Google Tag Manager (`GTM-5QSBL6BQ`) en su `headHtml`; la B y la A no.** Las
tres landings no miden lo mismo. Las conversiones de Ads no dependen de eso (viajan por el
formulario de HubSpot + importación de GCLID, por eso el Grupo A registró sus 8 sin GTM), pero
cualquier otra cosa de ese contenedor está ciega en dos de tres páginas. Pendiente de definir con
Diego. Por lo mismo NO se tocó el contraste `.4` de esa página: el script de GTM vive en el mismo
bloque y no vale la pena arriesgar el seguimiento por un ajuste cosmético.

**Para conectarla: NO editar la URL final del anuncio por API** — eso borra el anuncio y lo recrea
en pausa. Se le pone la URL final **a la keyword**, que sobrescribe la del anuncio sin tocarlo.

**Ejecutado el 13-ago:** URL final cargada a las **6 keywords activas del Grupo A** —
`"sistema de gestión de seguridad y salud en el trabajo"` (5,00 conv), `"software seguridad
ocupacional"` (2,00), `"software gestión sst"` (0,67), `"software sst"` (0,33), `[software seguridad
ocupacional]` y `[sistema gestión seguridad laboral]`. A las detenidas no se les puso URL.

**Ejecutado el 13-ago en el Grupo C:** URL final `https://soluciones.tazki.cl/software-hseq` cargada
a `plataforma hse`, la **única keyword viva del grupo** (amplia, QS 3/10, 1 conversión a $28.991 —
más barata que el promedio de la cuenta, $83.698).

**Por qué NO reactivar las 9 detenidas del Grupo C todavía.** Todas están en cero conversiones
(`"software hse"` $16.777, `software hseq` $10.576, `sistema gestión hseq` $9.756, `"sistema gestión
hseq"` $2.373, `"plataforma hse"` $1.931, `"software hseq"` $870, `"plataforma hseq"` $561), **pero
todas fueron juzgadas aterrizando en la landing equivocada**: su expediente está contaminado. Eso es
razón para re-probar alguna después, no para reactivarlas ya. El presupuesto es de la CAMPAÑA, no
del grupo: cada peso que vuelve a C se lo quita a A, que convierte 8 veces más. Si el 17-ago sube el
QS de `plataforma hse`, devolver **una sola** — `"plataforma hse"` en frase, la hermana directa de
la que funciona — para medirla limpia.

## AI Max: marginal

$23.485, **cero conversiones**, 2,6% del gasto. Y NO explica el crecimiento de la subasta: las
impresiones disponibles ya se habían triplicado (3.079 → 8.784) la semana ANTES de activarlo el
22-jul. El crecimiento es rampa de campaña nueva + consolidación de las campañas pausadas el 13-jul.

## Criterio de medición inbound (cerrado con Diego el 14-ago)

- **Universo**: `Tipo de negocio = Inbound` + `Pipeline = Pipeline de ventas` (sin ese segundo
  filtro se cuelan 9 de Lead Generation y 9 duplicados del pipeline Clientes). 2026 = 245 negocios.
- **Ganado** = etapa Closed Won (⚠️ valor interno `closedlost`, alguien la renombró) ·
  **Perdido** = Closed Lost (`1233212743`). El criterio "entró a Onboarding" queda DESCARTADO.
- **Dos lentes de fuente**: `Fuente original [i]` (quién abre la puerta; poblada en el 100%) para el
  desglose maestro anual · `Latest Source [i]` (quién convierte; poblada desde junio) para medir los
  MQL de PAGO — captura a los que conocieron Tazki por otro lado y convirtieron con un clic de
  anuncio (ago-2026: 4 de 18, el 22% — Equans 50 UF, Odis 24, IMT 15, Santolaya).
- **⚠️ LAS UF DEL CRM SON MENSUALES** (confirmado por Diego 14-ago). Todo cálculo de recuperación
  usa ingreso recurrente: 1 cliente promedio (23 UF/mes ≈ $920k/mes) recupera los $854k del año de
  Ads en su PRIMER MES.
- **Meeting Set no es señal**: el 91% de los negocios nace con demo agendada (el formulario ES de
  agendar demo). La fuga real está entre la demo y Qualified Prospect.
- **Canal AEO existe**: 2 negocios desde chatgpt.com — SOFTYS (40,48 UF, GANADA, la inbound más
  grande del año) y Dinamo (10 UF, viva). <1% del volumen, 22% del valor ganado inbound.

## Conversiones offline por valor — diseño aprobado, ejecutar LUNES 17-ago

Hoy Google optimiza hacia el MQL (evento «HubSpot - Marketing Qualified Lead», activo desde
29-may, 35 sincronizados, valor CL$1). ⚠️ En Google Ads ese evento se llama «Lead calificado»
pero dispara en el MQL (demo agendada) — trampa de nombre.

Plan (todo en modo SECUNDARIO, la puja NO se toca hasta después del 30-sep):
1. Crear evento «Prospecto calificado (QP)» — deal stage Qualified Prospect (o lifecycle SQL con
   workflow puente si el selector no ofrece etapa de negocio) — valor CL$80.000.
2. Crear evento «Cliente ganado» — lifecycle Customer — valor CL$920.000.
3. Subir el evento MQL de CL$1 a CL$10.000 (proporción 1:8:92).
4. En Google Ads: ambos como acción SECUNDARIA. Verificar semanalmente que cuadren con el CRM.
5. Recién después del 30-sep y con datos cuadrados: puja a «Maximizar valor de conversión» y
   promover eventos a principales (resetea aprendizaje ~2 semanas; hacerlo SOLO, sin otro cambio).
Volumen real: ~4-5 calificados pagados/mes — poco para pujar solo con eso; por eso el diseño en
capas (MQL da volumen, QP da dirección). Piso garantizado: la columna calificados-por-keyword.

## Umbral SEM comprometido con Felipe (14-ago)

- **31-ago**: la estrella sale de «Rara vez se publica» o se rehace el anuncio del Grupo A.
- **30-sep**: ≥3 MQL calificados pagados nuevos desde el arreglo, costo/calificado ≤ ~$78k.
  Si el Grupo C no aporta ninguno → se apaga el Grupo C.
- **30-nov** (fecha justa por ciclo 73-85d de los grandes): primer Closed Won pagado. Si no hay y
  es porque NO califican → se apaga SST/HSEQ (queda Marca). Si califican y no cierran → problema
  comercial, decisión conjunta. Marca NO se toca (4/4 vivos, único negocio en Negotiation).

## Historial de cambios

- **15 ago** — **Misterio de la geo CERRADO con el historial de cambios (CSV 1–14 ago).** No hubo
  reversión: Ubicaciones tiene DOS perillas — la lista de ubicaciones y la opción
  presencia/interés. El 3-ago (vía fecasanov@gmail.com) se corrigió la OPCIÓN a «Presencia», pero
  la LISTA siguió en «Todos los países» desde que la campaña nació el 4-jul. Ninguna fila del
  historial quita Chile jamás. El 14-ago Diego agregó el país: recién ahí quedaron bien las dos.
  Autores del historial: solo Diego, fecasanov@gmail.com y adwords@hubspot.com — cero cambios de
  «Sistema»/auto-aplicados. ⚠️ Los cambios hechos por API se firman como fecasanov@gmail.com
  (la credencial de la conexión): no confundir con cambios manuales de Felipe.
- **14 ago** — **GEO CORREGIDA: la campaña SST/HSEQ estaba en «Todos los países y territorios»**,
  no en Chile. Descubierto por el MQL de Vazquez y Asociados Consultora (Paraguay, dominio .com.py)
  que agendó demo en el calendario de Felipe vía `plataforma hse`. Precedente: existe el motivo de
  pérdida «Empresa Venezolana.» en el CRM. Diego la cambió a Chile/Presencia el mismo día (y revisó
  Marca en el mismo paso). NO se aplicó la recomendación de Google de CPA objetivo.
  Pendiente: cuantificar gasto/impresiones fuera de Chile (Informes → Ubicaciones o API cuando
  vuelva Supermetrics — caída de nuevo con «Anthropic Proxy: Invalid content»).
  ⚠️ La lectura del QS del 17/31-ago lleva DOS variables encima: landing nueva + geo. Si mejora,
  fue el combo; no se podrá separar el aporte de cada una.
- **14 ago** — `plataforma hse` (amplia, Grupo C) acumula **2 leads chatarra**: «asesor»
  (Reagendar) y Vazquez (consultora paraguaya). A favor: 1 conversión real ($28.991). Criterio
  acordado: si la lectura del domingo no muestra mejora y cae un tercer lead de este perfil,
  pasarla de amplia a frase `"plataforma hse"`.

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

- Definir con Diego qué hay en el contenedor GTM de la landing C y si va en las otras dos.
- Arreglar el contraste de la landing C (`.4` → `.78`) con cuidado de no romper el script de GTM.
- **Cambiar la URL final de los ANUNCIOS de los Grupos A y C a su landing — pero recién DESPUÉS de
  la lectura del 17-ago.** Hoy no urge: la URL de la keyword manda sobre la del anuncio y las 6 activas ya la
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

## Reunión con Felipe (14-ago) — acuerdos y contexto

- **Cadencia**: reunión cada 2 semanas. EXTRA el viernes 21-ago con presentación formal.
- **Formato exigido por Felipe**: problema → métrica → acción → resultado esperado → medición.
  Usó el caso del Quality Score de Diego como ejemplo de la estructura correcta. La bitácora
  existe pero NO se mostró (feedback de Axel: mostrarla siempre); falta agregar el "qué quería
  conseguir" ANTES de cada acción.
- **Regla de Axel**: con n chico, decir el crudo antes que el porcentaje ("5 de 8" antes que "62%").
- **Tercer lead por IA**: Felipe habló el 14-ago con una persona que llegó recomendada por ChatGPT
  (además de SOFTYS ganada y Dinamo viva).
- **AEO (módulo HubSpot)**: mide Gemini, ChatGPT y Perplexity (no Claude). Línea base 14-ago:
  50% de visibilidad en el prompt «mejores software de seguridad laboral en Chile». Plan: reporte
  mensual SEO + SEM + AEO.
- **Campaña Marca**: programada desde las 10:00 para evitar clics de inicio de sesión; sus 5
  conversiones están todas vivas.
- **Newsletter por correo**: lanza la semana del 18-ago. El de LinkedIn lleva ~500 suscriptores
  orgánicos; la lista (nombre, cargo, URL) se exporta automatizada para prospección de Boris
  (caso U. de Chile: reunión desde un like).
- **Quedó SIN decir en la reunión** (llevar el 21-ago): la bitácora en pantalla, el umbral SEM con
  fechas (31-ago/30-sep/30-nov), los 27 congelados (~492 UF/mes) con el pedido de dueño y fecha,
  y los motivos de pérdida entrando al reporte.
- Modelo contratista: video + brochure a Drive (14-ago), uso interno con tono de confianza;
  posible hype con acceso por credenciales. Feedback de Carla y Emilio.

## Regla permanente: grabar todo cambio (17-ago-2026, pedido de Diego)
Todo cambio acordado con Diego (criterios, orden de bloques, filas/columnas nuevas, umbrales, definiciones) se graba en el momento en
los archivos de config del repo — informe_demanda_bloques.json, inbounds_config.json, embudo_config.json, seo_config.json y este
archivo — con fecha y quién lo pidió. El repo es la única memoria que sobrevive entre sesiones. Cambio no grabado = cambio que la
próxima corrida deshace. Primero se graba el criterio, después se publica el Plan.

Cambios del 17-ago ya grabados: camadas al universo del diccionario (8 ganados · 4,85%), columna IA en tráfico por fuente (GA4
AI Assistant: jul 11 · ago 23 al 16), bitácora al final del Plan (badges renumerados: LinkedIn 7 · Motivos 8 · Salud 9 · AEO 10 ·
Bitácora 11), fila Valor (UF/mes) en las tablas de inbounds con cobertura declarada.

## plataforma hse — contrapunto a los 2 strikes (17-ago-2026, 16:51 Chile)
Tercer MQL de la keyword amplia «plataforma hse» (campaña SST/HSEQ → landing software-hseq): Macarena Becerra,
Ingeniería y Construcción Nobarzo Ltda (mbecerra@q4ingenieros.cl, +569…), contacto 242592884272. Perfil ICP legítimo
(construcción, Chile). Es el PRIMER MQL de esta keyword DESPUÉS del arreglo de geo del 14-ago — los 2 strikes previos
(asesor + Paraguay) ocurrieron con la campaña en «todos los países». Coherente con su QS 3 y creativo Above average.
LECTURA PARA LA DECISIÓN: el criterio «3er lead chatarra → pasar a frase» NO se gatilla (este no es chatarra); la amplia
confinada a Chile queda en observación normal. Entra a la semana 17–23 (reporte del lunes 24).
