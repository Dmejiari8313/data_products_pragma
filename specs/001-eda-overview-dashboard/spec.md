# Feature Specification: Dashboard EDA - Página de Overview

**Feature Branch**: `feature/eda-overview-dashboard`

**Created**: 2026-11-11

**Status**: Approved

**Input**: User description: "Quiero que iniciemos con el dashboard teniendo una página con los gráficos más representativos para entender la naturaleza y distribución de los datos que existen en nuestra base de datos"

## Resumen

Primera entrega del dashboard de análisis exploratorio (EDA) construido con
Streamlit sobre el dataset `movies.csv`. Consiste en **una sola página de
overview** que presenta los gráficos más representativos para entender la
naturaleza y la distribución de los datos: panel de métricas resumen,
distribuciones de las variables numéricas clave, rankings de categorías
(géneros, idiomas), evolución temporal, relaciones entre variables y un panel de
calidad de datos. La página incluye controles básicos (Top N y rango de años) y
no contempla filtros globales complejos ni páginas adicionales, que se abordarán
en specs futuras.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visión general de la distribución de los datos (Priority: P1)

Como persona analista de datos, quiero abrir el dashboard y ver de un vistazo las
métricas resumen y las distribuciones de las variables numéricas clave
(calificación, duración, presupuesto, ingresos) para entender rápidamente la
naturaleza del dataset.

**Why this priority**: Es el valor central de la entrega. Sin las distribuciones
y las métricas resumen no hay análisis exploratorio; esta historia por sí sola ya
constituye un MVP útil.

**Independent Test**: Se puede probar levantando la app, cargando `movies.csv` y
verificando que se renderizan el panel de KPIs y los histogramas de
`vote_average`, `runtime`, `budget` y `revenue` sin errores.

**Acceptance Scenarios**:

1. **Given** el dataset `movies.csv` disponible en la ruta configurada, **When**
   la persona usuaria abre la página de overview, **Then** se muestra un panel de
   métricas resumen con total de películas, presupuesto e ingreso promedio,
   duración media y rango de años.
2. **Given** la página cargada, **When** se renderizan las distribuciones,
   **Then** se muestran histogramas de `vote_average`, `runtime`, `budget` y
   `revenue`.
3. **Given** que `budget` o `revenue` contienen ceros (valor desconocido),
   **When** se construyen los histogramas de esas variables, **Then** los ceros se
   tratan como datos faltantes y se excluyen de la distribución.

---

### User Story 2 - Rankings de categorías y evolución temporal (Priority: P2)

Como persona analista, quiero ver los géneros e idiomas más frecuentes y cómo
evoluciona la cantidad de películas por año para entender la composición
categórica y temporal del dataset.

**Why this priority**: Complementa la visión numérica con la composición
categórica y temporal, aportando contexto clave del dataset. Es valiosa pero
secundaria frente a las distribuciones base.

**Independent Test**: Se puede probar verificando que, tras parsear la columna
`genres` y agrupar por año de `release_date`, se renderizan el gráfico de barras
de Top N géneros, el de Top N idiomas y el de películas por año.

**Acceptance Scenarios**:

1. **Given** la columna `genres` con múltiples géneros por película, **When** se
   procesa, **Then** se muestra un gráfico de barras con los Top N géneros más
   frecuentes.
2. **Given** la columna `original_language`, **When** se procesa, **Then** se
   muestra un gráfico de barras con los Top N idiomas originales más frecuentes.
3. **Given** la columna `release_date`, **When** se agrupa por año, **Then** se
   muestra la cantidad de películas por año.
4. **Given** el control de rango de años, **When** la persona usuaria lo ajusta,
   **Then** los gráficos dependientes del año se actualizan al rango seleccionado.

---

### User Story 3 - Relaciones entre variables y calidad de datos (Priority: P3)

Como persona analista, quiero ver la relación entre variables (p. ej. presupuesto
vs. ingresos, popularidad vs. votos) y un panel de calidad de datos (nulos y
ceros por columna) para evaluar correlaciones y la confiabilidad del dataset.

**Why this priority**: Aporta profundidad analítica y transparencia sobre la
calidad del dato, pero el dashboard ya es útil sin ella.

**Independent Test**: Se puede probar verificando que se renderiza un scatter de
relación entre variables y una tabla/gráfico con el conteo de nulos y ceros por
columna.

**Acceptance Scenarios**:

1. **Given** las columnas `budget` y `revenue` (o `popularity` y `vote_count`),
   **When** se renderiza el gráfico de dispersión, **Then** se muestra la relación
   entre ambas variables.
2. **Given** el dataset completo, **When** se calcula la calidad de datos,
   **Then** se muestra el conteo de valores nulos y de ceros por columna.

---

### Edge Cases

- ¿Qué ocurre si el archivo CSV no existe en la ruta configurada? La app debe
  mostrar un mensaje de error claro y registrar el fallo en los logs, sin romperse.
- ¿Qué ocurre si una columna esperada no está presente en el CSV? La app debe
  degradar con elegancia (omitir el gráfico afectado y advertir) en lugar de fallar.
- ¿Qué ocurre con fechas de `release_date` inválidas o vacías? Se tratan como
  faltantes y se excluyen de los agregados temporales.
- ¿Qué ocurre si tras excluir ceros/nulos una variable queda sin datos para
  graficar? Se muestra un aviso en lugar de un gráfico vacío.
- ¿Qué ocurre si el valor de Top N excede el número de categorías disponibles? Se
  muestran todas las categorías disponibles.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST cargar el dataset desde una ruta de archivo CSV
  configurable, con `movies.csv` en la raíz del repositorio como valor por defecto.
- **FR-002**: El sistema MUST presentar la información en una única página de
  overview dentro de un dashboard Streamlit.
- **FR-003**: El sistema MUST mostrar un panel de métricas resumen (KPIs) con, al
  menos: total de películas, presupuesto promedio, ingreso promedio, duración
  media y rango de años de estreno.
- **FR-004**: El sistema MUST mostrar histogramas de distribución para
  `vote_average`, `runtime`, `budget` y `revenue`.
- **FR-005**: El sistema MUST tratar los valores `0` en `budget` y `revenue` como
  datos faltantes y excluirlos de las visualizaciones de distribución.
- **FR-006**: El sistema MUST parsear la columna `genres` y mostrar un gráfico de
  barras con los Top N géneros más frecuentes.
- **FR-007**: El sistema MUST mostrar un gráfico de barras con los Top N idiomas
  originales (`original_language`) más frecuentes.
- **FR-008**: El sistema MUST derivar el año de estreno desde `release_date` y
  mostrar la cantidad de películas por año.
- **FR-009**: El sistema MUST mostrar al menos un gráfico de dispersión que
  relacione dos variables numéricas (p. ej. `budget` vs. `revenue`).
- **FR-010**: El sistema MUST mostrar un panel de calidad de datos con el conteo
  de valores nulos y de ceros por columna.
- **FR-011**: Los usuarios MUST poder ajustar el valor de "Top N" para los
  rankings de categorías mediante un control básico.
- **FR-012**: Los usuarios MUST poder ajustar un rango de años que afecte a los
  gráficos dependientes del tiempo.
- **FR-013**: El sistema MUST manejar con elegancia la ausencia del archivo o de
  columnas esperadas, mostrando mensajes claros y registrando el evento en los logs.
- **FR-014**: El sistema MUST registrar (logging, nivel INFO por defecto) el
  inicio y fin de las operaciones clave: carga del dataset y transformaciones
  principales, así como los errores.
- **FR-015**: Las visualizaciones deben usar gráficos interactivos (zoom, hover)
  acordes al stack definido (Plotly).

### Key Entities *(include if feature involves data)*

- **Movie (registro de película)**: representa una película del dataset. Atributos
  relevantes para esta página: `budget`, `revenue`, `runtime`, `vote_average`,
  `vote_count`, `popularity`, `genres`, `original_language`, `release_date`,
  `title`. Otros atributos del dataset existen pero no se usan en esta entrega.
- **GenreCount (conteo de género)**: categoría de género derivada del parseo de
  `genres`, con su frecuencia de aparición.
- **YearlyCount (conteo anual)**: año de estreno derivado de `release_date`, con la
  cantidad de películas asociadas.
- **DataQualityMetric (métrica de calidad)**: por columna, el conteo de valores
  nulos y de valores cero (donde cero implica dato desconocido).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La aplicación levanta sin errores y la página de overview renderiza
  todos los gráficos definidos con el dataset completo.
- **SC-002**: La página de overview carga y renderiza sus gráficos en menos de 5
  segundos con el dataset completo (`movies.csv`) en una máquina de desarrollo
  estándar.
- **SC-003**: La capa de lógica (carga de datos y transformaciones:
  parseo de géneros, derivación de año, cálculo de métricas y calidad de datos)
  cuenta con cobertura de pruebas unitarias en `pytest`, con todas las pruebas en
  verde.
- **SC-004**: Ante un archivo inexistente o una columna faltante, la aplicación
  muestra un mensaje de error claro y no se interrumpe abruptamente.
- **SC-005**: El 100% de las variables de distribución excluyen correctamente los
  valores tratados como faltantes (ceros en `budget`/`revenue`, fechas inválidas).

## Assumptions

- `movies.csv` corresponde al dataset TMDB 5000 con las columnas observadas:
  `index, budget, genres, homepage, id, keywords, original_language,
  original_title, overview, popularity, production_companies,
  production_countries, release_date, revenue, runtime, spoken_languages, status,
  tagline, title, vote_average, vote_count, cast, crew, director`.
- Para esta primera página solo se parsea la columna compleja `genres` (además de
  `original_language`). Las columnas `cast`, `crew`, `keywords`,
  `production_companies`, `production_countries` y `spoken_languages` quedan fuera
  del alcance de esta entrega.
- Los valores `0` en `budget` y `revenue` representan "desconocido" y se tratan
  como faltantes en las visualizaciones.
- La página incluye controles básicos (Top N y rango de años); los filtros
  globales complejos y las páginas/tabs adicionales (p. ej. la vista de tabla
  registro a registro) se abordarán en specs futuras.
- El entorno de ejecución es un entorno virtual de Python 3.12 gestionado con
  `uv`, conforme a la constitución del proyecto.
- La ruta del CSV es configurable; `movies.csv` en la raíz del repositorio es el
  valor por defecto.

### Decisiones registradas para la futura spec 002 (tab de tabla)

> Estas decisiones NO forman parte del alcance de esta spec (001). Se registran
> aquí para no perderlas; se formalizarán al crear la spec 002 de la vista de
> tabla registro a registro.

- La vista de tabla será una **nueva tab** del dashboard, sobre la base que entrega
  esta spec 001.
- Funcionalidad por defecto de la tabla (propuesta aceptada): tabla paginada,
  selección de columnas a mostrar, ordenamiento por columna y búsqueda/filtro por
  texto.
- Las columnas pesadas (`cast`, `crew`, `keywords`, `genres`, etc.) se mostrarán
  **tal cual** (texto crudo).
- Se incluirá un **botón para exportar** la vista (filtrada) a CSV.
