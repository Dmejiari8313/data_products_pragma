# Movies EDA Dashboard

Dashboard de análisis exploratorio (EDA) del dataset `movies.csv`, construido con
Streamlit, pandas y Plotly.

## Requisitos

- [uv](https://docs.astral.sh/uv/) instalado.
- Python 3.12 (gestionado por `uv`).

## Preparar el entorno

```bash
# Crear el entorno virtual con Python 3.12
uv venv --python 3.12

# Instalar dependencias (runtime + desarrollo)
uv sync
```

> El entorno virtual de `uv` es obligatorio. Nunca se usa el Python global del
> sistema.

## Ejecutar el dashboard

```bash
# Ruta por defecto: movies.csv en la raíz del repositorio
uv run streamlit run app.py
```

La ruta del CSV es configurable mediante la variable de entorno `MOVIES_CSV_PATH`:

```powershell
# Windows PowerShell
$env:MOVIES_CSV_PATH = "C:\ruta\a\movies.csv"; uv run streamlit run app.py
```

## Calidad y pruebas

```bash
uv run pytest           # pruebas unitarias (capa de lógica)
uv run ruff check .     # linter
uv run ruff format .    # formateador
uv run mypy src         # verificación de tipos
```

## Estructura

```text
app.py                      # Punto de entrada Streamlit (presentación)
src/movies_eda/
├── config.py               # Ruta del CSV configurable y defaults
├── logging_config.py       # Configuración central de logging (INFO)
├── data/                   # Carga y limpieza (lógica pura, testeable)
├── analysis/               # Métricas, distribuciones, categóricos, calidad
└── ui/                     # Controles Streamlit y figuras Plotly
tests/unit/                 # Pruebas pytest de la capa de lógica
```
