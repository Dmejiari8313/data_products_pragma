# Quickstart: Dashboard EDA - Página de Overview

**Feature**: 001-eda-overview-dashboard

## Requisitos previos

- `uv` instalado (verificado: uv 0.13.7).
- Python 3.12 (gestionado por `uv`).

## Preparar el entorno

```bash
# Crear el entorno virtual con Python 3.12 (uv)
uv venv --python 3.12

# Instalar dependencias declaradas en pyproject.toml
uv sync
```

> El entorno virtual de `uv` es obligatorio. Nunca se usa el Python global del
> sistema (constitución, Stack Tecnológico).

## Ejecutar el dashboard

```bash
# Ruta por defecto (movies.csv en la raíz del repo)
uv run streamlit run app.py

# Ruta de CSV configurable mediante variable de entorno
# (Windows PowerShell)
$env:MOVIES_CSV_PATH = "C:\ruta\a\mi\movies.csv"; uv run streamlit run app.py
```

## Validación (criterios de éxito)

1. **SC-001**: la app levanta sin errores y la página de overview muestra todos
   los bloques: KPIs, histogramas (`vote_average`, `runtime`, `budget`,
   `revenue`), Top N géneros, Top N idiomas, películas por año, dispersión y panel
   de calidad de datos.
2. **SC-002**: la página renderiza en < 5 s con el dataset completo.
3. **SC-004**: al apuntar a un CSV inexistente, la app muestra un mensaje de error
   claro y no se interrumpe abruptamente.

## Ejecutar pruebas y calidad

```bash
# Pruebas unitarias (capa de lógica)
uv run pytest

# Linter y formateador
uv run ruff check .
uv run ruff format --check .

# Verificación de tipos
uv run mypy src
```

Todas las comprobaciones deben quedar en verde antes de considerar una tarea
terminada (constitución, Puertas de calidad).
