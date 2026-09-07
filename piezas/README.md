# Constructores de los descargables de Tazki

Scripts que generan los archivos Excel que se entregan por formulario.
Se guardan acá porque el contenedor de trabajo es efímero y los scripts se perdían.

**Los .xlsx NO van en este repositorio: es público y los archivos están detrás
de un formulario.** Se generan corriendo el script y se suben a Files de HubSpot.

| Script | Genera | Recurso publicado |
|---|---|---|
| `build_irl.py` | `Formato-IRL-DS44-Tazki.xlsx` | tazki.cl/recursos/formato-irl-ds-44 |
| `build_miper.py` | `Matriz-IPER-DS44-Tazki.xlsx` | tazki.cl/recursos/matriz-iper-ds-44 |
| `build_checklist.py` | `Checklist-DS44-Tazki.xlsx` | pendiente |

Todos contrastan su contenido normativo contra `../normativa/ds44-texto-completo-literal.md`.

Requisito: `pip install openpyxl`.
