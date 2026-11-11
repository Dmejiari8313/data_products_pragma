# Implementation Plan: Dashboard EDA - Página de Overview

**Branch**: `feature/eda-overview-dashboard` | **Date**: 2026-11-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-eda-overview-dashboard/spec.md`

## Summary

Construir la primera página (overview) de un dashboard de análisis exploratorio
(EDA) con Streamlit sobre `movies.csv`. El enfoque técnico separa estrictamente la
**capa de lógica** (carga del CSV, limpieza, transformaciones, agregaciones y
métricas de calidad — funciones puras, tipadas y testeadas con pytest) de la
**capa de presentación** (Streamlit + Plotly, sin lógica de negocio). La ruta del
CSV es configurable, los ceros de `budget`/`revenue` se tratan como faltantes, y
toda operación clave se registra con `logging` a nivel INFO. Se desarrolla con
TDD estricto bajo un entorno virtual Python 3.12 gestionado con `uv`.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: streamlit, pandas, plotly (runtime); pytest, ruff, mypy
(desarrollo)

**Storage**: Archivo CSV local (`movies.csv`), ruta configurable. Sin base de datos.

**Testing**: pytest (TDD estricto sobre la capa de lógica)

**Target Platform**: Aplicación web local servida por Streamlit en máquina de
desarrollo

**Project Type**: Single project (aplicación de datos / dashboard)

**Performance Goals**: La página de overview renderiza todos sus gráficos en < 5 s
con el dataset completo en una máquina de desarrollo estándar (SC-002). La carga
del CSV se cachea para evitar relecturas en cada interacción.

**Constraints**: Entorno virtual con `uv` obligatorio (nunca el Python global);
logging a nivel INFO; tipado completo; docstrings NumPy; `ruff` y `mypy` en verde.

**Scale/Scope**: Dataset ~4.800 películas, 24 columnas. Una sola página con ~8
bloques de visualización y 2 controles básicos (Top N, rango de años).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio de la constitución | Cumplimiento en este plan |
|---|---|
| I. Interacción en español / código en inglés | Documentos y mensajes en español; código, identificadores y docstrings en inglés. ✅ |
| II. TDD estricto (pytest) | Tareas ordenadas test-first para toda la capa de lógica (Red → Green → Refactor). ✅ |
| III. Separación lógica/presentación | `src/movies_eda/data/` y `src/movies_eda/analysis/` (lógica pura, testeable) separados de `src/movies_eda/ui/` y `app.py` (Streamlit). Tests solo sobre la lógica. ✅ |
| IV. Calidad (tipado, docstrings NumPy, ruff, mypy) | Type hints en todas las firmas; docstrings NumPy; `ruff` y `mypy` configurados como gate. ✅ |
| V. Observabilidad (logging INFO) | Módulo `logging_config` central; logs de inicio/fin de carga y transformaciones; sin `print`. ✅ |
| Stack (Py 3.12 + uv, pandas, plotly, streamlit) | Declarado en `pyproject.toml`, entorno `uv`. ✅ |
| Flujo (rama por spec, commits atómicos, tareas marcadas) | Rama `feature/eda-overview-dashboard`; commits conventional al finalizar. ✅ |

**Resultado del gate**: PASA. No hay violaciones que justificar.

## Project Structure

### Documentation (this feature)

```text
specs/001-eda-overview-dashboard/
├── spec.md              # Especificación (hecho)
├── plan.md              # Este archivo
├── data-model.md        # Entidades y transformaciones (Phase 1)
├── quickstart.md        # Cómo levantar y validar (Phase 1)
└── tasks.md             # Generado por /speckit.tasks
```

### Source Code (repository root)

```text
pyproject.toml           # Metadatos del proyecto y dependencias (uv)
uv.lock                  # Lockfile de uv
README.md                # Instrucciones básicas
app.py                   # Punto de entrada Streamlit (orquesta la UI, sin lógica)
.streamlit/
└── config.toml          # Configuración de Streamlit (opcional)

src/
└── movies_eda/
    ├── __init__.py
    ├── config.py              # Configuración (ruta CSV configurable, defaults)
    ├── logging_config.py      # Configuración central de logging (nivel INFO)
    ├── data/
    │   ├── __init__.py
    │   ├── loader.py          # Carga del CSV (cacheable), validación de columnas
    │   └── cleaning.py        # Limpieza: ceros->NaN, parseo fechas, parseo genres
    ├── analysis/
    │   ├── __init__.py
    │   ├── metrics.py         # KPIs resumen (totales, promedios, rango de años)
    │   ├── distributions.py   # Series para histogramas (excluyendo faltantes)
    │   ├── categorical.py     # Top N géneros / idiomas, conteo por año
    │   └── quality.py         # Conteo de nulos y ceros por columna
    └── ui/
        ├── __init__.py
        ├── controls.py        # Controles básicos (Top N, rango de años)
        └── charts.py          # Construcción de figuras Plotly a partir de datos

tests/
└── unit/
    ├── __init__.py
    ├── conftest.py            # Fixtures (DataFrame de muestra)
    ├── test_loader.py
    ├── test_cleaning.py
    ├── test_metrics.py
    ├── test_distributions.py
    ├── test_categorical.py
    └── test_quality.py
```

**Structure Decision**: Se adopta la opción *Single project* con un paquete
`src/movies_eda`. La separación en subpaquetes `data/`, `analysis/`, `ui/` hace
cumplir el Principio III: `data/` y `analysis/` contienen funciones puras y
tipadas (única parte cubierta por tests), mientras que `ui/` y `app.py` son la
capa de presentación Streamlit/Plotly sin lógica de negocio. Los tests espejan los
módulos de lógica bajo `tests/unit/`.

## Design Notes (Phase 0 / Phase 1 resumen)

- **Carga y caché**: `loader.load_movies(path)` lee el CSV con pandas y valida la
  presencia de columnas esperadas; en `app.py` se envuelve con el caché de
  Streamlit (`st.cache_data`) para cumplir SC-002. La lógica de carga en sí
  permanece pura y testeable (sin dependencias de Streamlit).
- **Limpieza**: `cleaning` convierte ceros de `budget`/`revenue` a `NaN`, parsea
  `release_date` a datetime (fechas inválidas -> NaT) y deriva `release_year`;
  `parse_genres` separa la cadena de géneros en una lista normalizada.
- **Análisis**: funciones que reciben un `DataFrame` y devuelven estructuras
  tipadas (p. ej. `pd.Series`/`pd.DataFrame`/dataclasses) listas para graficar,
  sin tocar Streamlit.
- **Presentación**: `ui/charts.py` transforma esas estructuras en figuras Plotly;
  `app.py` las dispone en la página y aplica los controles de `ui/controls.py`.
- **Errores**: archivo inexistente o columna faltante -> excepción de dominio
  capturada en `app.py`, que muestra `st.error` y registra el evento (FR-013).

## Complexity Tracking

> No aplica. El Constitution Check pasa sin violaciones; no se introducen patrones
> ni proyectos adicionales que requieran justificación.
