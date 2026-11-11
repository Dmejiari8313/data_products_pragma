# Tasks: Dashboard EDA - Página de Overview

**Input**: Design documents from `/specs/001-eda-overview-dashboard/`

**Prerequisites**: plan.md (required), spec.md (required), data-model.md, quickstart.md

**Tests**: INCLUIDOS Y OBLIGATORIOS. La constitución exige TDD estricto (Principio
II) sobre la capa de lógica: cada módulo de `data/` y `analysis/` se implementa
escribiendo primero su prueba, verificando que falla (Red), implementando el
mínimo (Green) y refactorizando. La capa de presentación (`ui/`, `app.py`) queda
exenta de pruebas unitarias (Principio III).

**Organization**: Las tareas se agrupan por historia de usuario para permitir
implementación y prueba independientes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias).
- **[Story]**: Historia de usuario a la que pertenece (US1, US2, US3).
- Se incluyen rutas de archivo exactas.

## Path Conventions

Single project: `src/movies_eda/` y `tests/unit/` en la raíz del repositorio.
Punto de entrada Streamlit: `app.py` en la raíz.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialización del proyecto y entorno reproducible con uv (Python 3.12).

- [x] T001 Crear `pyproject.toml` en la raíz con metadatos del proyecto, Python 3.12, dependencias runtime (streamlit, pandas, plotly) y de desarrollo (pytest, ruff, mypy), y configuración de herramientas
- [x] T002 Crear el entorno virtual con `uv venv --python 3.12` y generar `uv.lock` con `uv sync`
- [x] T003 [P] Configurar `ruff` (lint + format) y `mypy` (modo estricto sobre `src/`) en `pyproject.toml`
- [x] T004 [P] Crear la estructura de paquetes: `src/movies_eda/__init__.py`, `src/movies_eda/data/__init__.py`, `src/movies_eda/analysis/__init__.py`, `src/movies_eda/ui/__init__.py` y `tests/unit/__init__.py`
- [x] T005 [P] Crear `README.md` en la raíz con instrucciones de entorno y ejecución (basadas en quickstart.md)

**Checkpoint**: Entorno uv listo, dependencias instaladas, estructura creada.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestructura central (configuración y logging) requerida por todas
las historias.

**⚠️ CRITICAL**: Ninguna historia de usuario puede comenzar hasta completar esta fase.

- [x] T006 Implementar `src/movies_eda/logging_config.py`: configuración central de `logging` estándar, nivel por defecto INFO, formato con trazabilidad (timestamp, módulo, nivel, mensaje), con docstrings NumPy y tipado
- [x] T007 Implementar `src/movies_eda/config.py`: resolución de la ruta del CSV configurable (variable de entorno `MOVIES_CSV_PATH` con `movies.csv` de la raíz como valor por defecto) y constantes de defaults (Top N por defecto), tipado y docstrings NumPy
- [x] T008 [P] Crear `tests/unit/conftest.py` con fixtures de pytest: un `DataFrame` de muestra representativo (incluyendo ceros en budget/revenue, fechas inválidas, géneros múltiples y nulos) para las pruebas de la capa de lógica

**Checkpoint**: Configuración y logging disponibles; fixtures de prueba listas.

---

## Phase 3: User Story 1 - Visión general de la distribución (Priority: P1) 🎯 MVP

**Goal**: Mostrar el panel de métricas resumen (KPIs) y los histogramas de
distribución de `vote_average`, `runtime`, `budget` y `revenue`, tratando los
ceros de budget/revenue como faltantes.

**Independent Test**: Levantar la app con `movies.csv` y verificar que se renderizan
el panel de KPIs y los cuatro histogramas sin errores, con los ceros excluidos.

### Tests for User Story 1 (TDD - escribir y ver fallar primero) ⚠️

- [x] T009 [P] [US1] Escribir pruebas de carga en `tests/unit/test_loader.py`: carga correcta del CSV, validación de columnas esperadas y excepción de dominio ante archivo inexistente o columna faltante
- [x] T010 [P] [US1] Escribir pruebas de limpieza en `tests/unit/test_cleaning.py`: ceros de `budget`/`revenue` convertidos a `NaN`, `release_date` inválida -> `NaT`, derivación de `release_year`
- [x] T011 [P] [US1] Escribir pruebas de KPIs en `tests/unit/test_metrics.py`: `total_movies`, promedios de budget/revenue excluyendo faltantes, `avg_runtime`, `min_year`/`max_year`
- [x] T012 [P] [US1] Escribir pruebas de distribuciones en `tests/unit/test_distributions.py`: series de histograma que excluyen faltantes y manejan el caso sin datos

### Implementation for User Story 1

- [x] T013 [US1] Implementar `src/movies_eda/data/loader.py`: `load_movies(path)` con pandas, validación de columnas, excepción de dominio y logging INFO de inicio/fin (hace pasar T009)
- [x] T014 [US1] Implementar `src/movies_eda/data/cleaning.py`: `clean_movies(df)` (ceros->NaN, parseo de fechas, `release_year`) con logging y tipado (hace pasar T010)
- [x] T015 [P] [US1] Implementar `src/movies_eda/analysis/metrics.py`: `compute_summary_metrics(df) -> SummaryMetrics` (dataclass tipada) (hace pasar T011)
- [x] T016 [P] [US1] Implementar `src/movies_eda/analysis/distributions.py`: funciones que devuelven las series para los histogramas excluyendo faltantes (hace pasar T012)
- [x] T017 [US1] Implementar `src/movies_eda/ui/charts.py` (parte US1): funciones que construyen las figuras Plotly de histogramas a partir de las series de lógica
- [x] T018 [US1] Implementar en `app.py` la sección de KPIs y los cuatro histogramas, orquestando carga (con `st.cache_data`), limpieza y charts; manejo de errores con `st.error` y logging (FR-013)

**Checkpoint**: La página muestra KPIs + histogramas funcionando; US1 es un MVP demostrable.

---

## Phase 4: User Story 2 - Rankings de categorías y evolución temporal (Priority: P2)

**Goal**: Mostrar Top N géneros, Top N idiomas y películas por año, con controles
básicos (Top N y rango de años).

**Independent Test**: Verificar que, tras parsear `genres` y agrupar por año, se
renderizan el gráfico de Top N géneros, el de Top N idiomas y el de películas por
año, y que los controles actualizan los gráficos correspondientes.

### Tests for User Story 2 (TDD - escribir y ver fallar primero) ⚠️

- [x] T019 [P] [US2] Escribir pruebas de parseo de géneros en `tests/unit/test_cleaning.py`: `parse_genres` separa la cadena en `list[str]` normalizada y maneja vacíos/nulos
- [x] T020 [P] [US2] Escribir pruebas categóricas en `tests/unit/test_categorical.py`: Top N géneros, Top N idiomas (con N mayor que categorías disponibles -> todas) y conteo por año excluyendo años `NaT`, con filtro de rango de años

### Implementation for User Story 2

- [x] T021 [US2] Añadir `parse_genres` a `src/movies_eda/data/cleaning.py` (hace pasar T019)
- [x] T022 [US2] Implementar `src/movies_eda/analysis/categorical.py`: `top_genres(df, n)`, `top_languages(df, n)` y `movies_per_year(df, year_range)` con tipado y logging (hace pasar T020)
- [x] T023 [US2] Implementar `src/movies_eda/ui/controls.py`: control de Top N (slider) y control de rango de años (slider), con defaults desde `config.py`
- [x] T024 [US2] Añadir a `src/movies_eda/ui/charts.py` las figuras Plotly de barras (Top N géneros, Top N idiomas) y de películas por año
- [x] T025 [US2] Integrar en `app.py` los controles y los tres gráficos de US2, enlazando Top N y rango de años a los gráficos dependientes (FR-011, FR-012)

**Checkpoint**: US1 y US2 funcionan de forma independiente; controles básicos operativos.

---

## Phase 5: User Story 3 - Relaciones entre variables y calidad de datos (Priority: P3)

**Goal**: Mostrar un gráfico de dispersión entre variables numéricas y un panel de
calidad de datos (nulos y ceros por columna).

**Independent Test**: Verificar que se renderiza el scatter (p. ej. budget vs.
revenue) y la tabla/gráfico con el conteo de nulos y ceros por columna.

### Tests for User Story 3 (TDD - escribir y ver fallar primero) ⚠️

- [x] T026 [P] [US3] Escribir pruebas de calidad de datos en `tests/unit/test_quality.py`: `compute_data_quality(df)` devuelve conteo de nulos y de ceros por columna (verificando budget/revenue)

### Implementation for User Story 3

- [x] T027 [US3] Implementar `src/movies_eda/analysis/quality.py`: `compute_data_quality(df) -> DataFrame` (columna, null_count, zero_count) con tipado y logging (hace pasar T026)
- [x] T028 [US3] Añadir a `src/movies_eda/ui/charts.py` la figura de dispersión (budget vs. revenue / popularity vs. vote_count) usando datos sin faltantes
- [x] T029 [US3] Integrar en `app.py` la sección de dispersión y el panel de calidad de datos (FR-009, FR-010)

**Checkpoint**: Las tres historias de usuario quedan independientemente funcionales.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Mejoras transversales y cierre de calidad.

- [ ] T030 [P] Añadir docstrings NumPy faltantes y revisar type hints en toda la capa de lógica
- [ ] T031 Ejecutar `uv run ruff check .` y `uv run ruff format .` y corregir hallazgos
- [ ] T032 Ejecutar `uv run mypy src` y corregir errores de tipos
- [ ] T033 Ejecutar `uv run pytest` y asegurar la suite completa en verde
- [ ] T034 [P] Validar manualmente los criterios de éxito con `quickstart.md` (SC-001, SC-002, SC-004) y ajustar el caché si el render supera 5 s
- [ ] T035 Crear commits atómicos (conventional-commits, prefijos en inglés, contenido en español) para la implementación del spec

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias; puede empezar de inmediato.
- **Foundational (Phase 2)**: depende de Setup; BLOQUEA todas las historias.
- **User Stories (Phase 3+)**: dependen de Foundational. Pueden abordarse en
  paralelo o en orden de prioridad (P1 → P2 → P3).
- **Polish (Phase 6)**: depende de completar las historias deseadas.

### User Story Dependencies

- **US1 (P1)**: arranca tras Foundational. Sin dependencias de otras historias. MVP.
- **US2 (P2)**: arranca tras Foundational. Reutiliza `cleaning.py` (añade
  `parse_genres`) pero es testeable de forma independiente.
- **US3 (P3)**: arranca tras Foundational. Independiente; añade `quality.py` y el
  scatter.

### Within Each User Story

- Los tests se escriben y DEBEN fallar antes de implementar (TDD estricto).
- Orden: datos/limpieza → análisis → charts → integración en `app.py`.

### Parallel Opportunities

- Setup: T003, T004, T005 en paralelo.
- Foundational: T008 en paralelo con T006/T007 (distintos archivos).
- US1: tests T009–T012 en paralelo; luego T015 y T016 en paralelo.
- US2: tests T019–T020 en paralelo.
- Polish: T030 y T034 en paralelo.

---

## Parallel Example: User Story 1

```text
# Lanzar en paralelo las pruebas de US1 (TDD, deben fallar primero):
Task: "Pruebas de carga en tests/unit/test_loader.py"
Task: "Pruebas de limpieza en tests/unit/test_cleaning.py"
Task: "Pruebas de KPIs en tests/unit/test_metrics.py"
Task: "Pruebas de distribuciones en tests/unit/test_distributions.py"

# Tras tener loader y cleaning, implementar en paralelo:
Task: "analysis/metrics.py"
Task: "analysis/distributions.py"
```

---

## Implementation Strategy

### MVP First (solo User Story 1)

1. Completar Phase 1 (Setup) y Phase 2 (Foundational).
2. Completar Phase 3 (US1): KPIs + histogramas.
3. **PARAR y VALIDAR**: probar US1 de forma independiente (MVP demostrable).

### Incremental Delivery

1. Setup + Foundational → base lista.
2. US1 → validar → demo (MVP).
3. US2 → validar → demo.
4. US3 → validar → demo.
5. Polish → calidad en verde y commits atómicos.

---

## Notes

- `[P]` = archivos distintos, sin dependencias.
- La etiqueta `[Story]` mapea cada tarea a su historia para trazabilidad.
- Verificar que los tests fallan antes de implementar (TDD estricto, Principio II).
- A medida que se complete cada tarea, marcarla inmediatamente como completada
  (constitución, Flujo de Trabajo).
- Todo desarrollo ocurre dentro del entorno `uv` (Python 3.12), nunca el Python global.
