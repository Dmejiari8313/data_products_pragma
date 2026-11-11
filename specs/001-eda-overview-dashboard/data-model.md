# Data Model: Dashboard EDA - Página de Overview

**Feature**: 001-eda-overview-dashboard | **Date**: 2026-11-11

Este documento describe las entidades conceptuales y las transformaciones de datos
de la capa de lógica. No define esquemas de base de datos (la fuente es un CSV).

## Fuente de datos

- **Archivo**: `movies.csv` (ruta configurable; por defecto la raíz del repo).
- **Columnas de entrada relevantes** (de 24 totales): `budget`, `revenue`,
  `runtime`, `vote_average`, `vote_count`, `popularity`, `genres`,
  `original_language`, `release_date`, `title`.

## Entidades y transformaciones

### Movie (fila del dataset)

Representa una película. Campos usados en esta entrega y sus reglas:

| Campo | Tipo esperado | Reglas / constraints |
|---|---|---|
| `budget` | int/float | Valor `0` se trata como faltante (`NaN`) en distribuciones. |
| `revenue` | int/float | Valor `0` se trata como faltante (`NaN`) en distribuciones. |
| `runtime` | float (minutos) | Puede ser nulo; se excluye de su distribución si falta. |
| `vote_average` | float [0, 10] | Base del histograma de calidad percibida. |
| `vote_count` | int | Usado en relaciones (scatter). |
| `popularity` | float | Usado en relaciones (scatter). |
| `genres` | string | Lista de géneros separados por espacio (p. ej. "Action Adventure"); se parsea a `list[str]`. |
| `original_language` | string (ISO) | Código de idioma (p. ej. "en"); base del ranking de idiomas. |
| `release_date` | string fecha | Se parsea a datetime; inválida/vacía -> `NaT`. Deriva `release_year` (int). |
| `title` | string | Identificación legible de la película. |

### GenreCount (conteo de género)

- Derivada de parsear `genres` y "explotar" la lista.
- Atributos: `genre` (str), `count` (int).
- Uso: ranking Top N géneros más frecuentes (FR-006).

### LanguageCount (conteo de idioma)

- Derivada de agrupar por `original_language`.
- Atributos: `language` (str), `count` (int).
- Uso: ranking Top N idiomas (FR-007).

### YearlyCount (conteo anual)

- Derivada de `release_year` (desde `release_date`).
- Atributos: `year` (int), `count` (int). Filas con año `NaT` se excluyen.
- Uso: cantidad de películas por año (FR-008); afectada por el control de rango de
  años (FR-012).

### SummaryMetrics (KPIs)

- Atributos: `total_movies` (int), `avg_budget` (float), `avg_revenue` (float),
  `avg_runtime` (float), `min_year` (int), `max_year` (int).
- Reglas: los promedios de `budget`/`revenue` se calculan excluyendo los ceros
  tratados como faltantes.
- Uso: panel de métricas resumen (FR-003).

### DataQualityMetric (métrica de calidad)

- Por cada columna: `column` (str), `null_count` (int), `zero_count` (int).
- `zero_count` se reporta especialmente para `budget` y `revenue` (cero =
  desconocido).
- Uso: panel de calidad de datos (FR-010).

## Reglas transversales

- **Valores faltantes**: ceros en `budget`/`revenue` y fechas inválidas en
  `release_date` se normalizan a `NaN`/`NaT` antes de cualquier agregación de
  distribución o temporal (FR-005).
- **Degradación elegante**: si falta una columna esperada, la función de análisis
  correspondiente debe señalarlo (excepción de dominio) sin romper el resto
  (FR-013).
- **Tipado**: todas las funciones de la capa de lógica reciben y devuelven tipos
  explícitos (`pd.DataFrame`, `pd.Series`, dataclasses o tipos escalares).
