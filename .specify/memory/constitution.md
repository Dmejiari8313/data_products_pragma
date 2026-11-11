# Movies EDA Dashboard Constitution

## Core Principles

### I. Idioma: interacción en español, código en inglés

La comunicación con las personas usuarias (chat, documentos de spec, plan, tareas,
mensajes al usuario) se realiza SIEMPRE en español. El código fuente se escribe
SIEMPRE en inglés: nombres de variables, funciones, clases, módulos, archivos y
docstrings. Los comentarios de código también se escriben en inglés para mantener
la coherencia del código base. Esta separación es innegociable y aplica a todo
artefacto del proyecto.

### II. Test-First / TDD estricto (NO NEGOCIABLE)

El desarrollo sigue TDD estricto sobre la capa de lógica: se escribe la prueba
primero, se verifica que falla (Red), se implementa el mínimo código para que pase
(Green) y se refactoriza (Refactor). No se escribe código de producción de lógica
sin una prueba que lo justifique previamente. Las pruebas se escriben con `pytest`.
El ciclo Red-Green-Refactor se respeta sin excepciones.

### III. Separación de capas: lógica testeable vs. presentación

La lógica de datos (carga, limpieza, transformaciones, agregaciones, cálculos
estadísticos) se encapsula en funciones puras y tipadas, independientes de
Streamlit, ubicadas en módulos de lógica. La capa de presentación (Streamlit)
solo orquesta y renderiza; no contiene lógica de negocio. La cobertura de pruebas
`pytest` es OBLIGATORIA sobre la capa de lógica; la capa de presentación queda
exenta de pruebas unitarias por su naturaleza de UI.

### IV. Calidad de código: tipado, docstrings y funciones específicas

Todo objeto y firma de función está tipado (type hints). Cada función incluye un
docstring en formato **NumPy** que explique su propósito, parámetros, retornos y
excepciones relevantes. Las tareas se encapsulan en funciones específicas y con
responsabilidad única; queda prohibido el código espagueti. Se aplican los
siguientes estándares de calidad de forma obligatoria:

- `ruff` como linter y formateador.
- `mypy` para verificación estática de tipos.
- Docstrings en formato NumPy en cada función.

### V. Observabilidad: logging con trazabilidad

Toda ejecución relevante emite logs mediante el módulo `logging` estándar de
Python. El nivel por defecto es `INFO`. Los logs deben permitir trazabilidad:
registrar inicio/fin de operaciones clave (carga de datos, transformaciones,
errores) con mensajes claros. Queda prohibido el uso de `print` para trazabilidad.

## Stack Tecnológico

El proyecto fija el siguiente stack como estándar innegociable:

- **Lenguaje**: Python 3.12.
- **Gestión de entorno y dependencias**: `uv`. El desarrollo se realiza SIEMPRE
  dentro de un entorno virtual creado con `uv`; NUNCA se usa el Python global del
  sistema. Las dependencias se declaran en `pyproject.toml` y se bloquean con
  `uv.lock`.
- **Manipulación de datos**: `pandas`.
- **Visualización**: `plotly` para gráficos interactivos.
- **Dashboard / UI**: `streamlit`.
- **Pruebas**: `pytest`.
- **Calidad**: `ruff` (lint + formato) y `mypy` (tipos).

Cualquier incorporación de una dependencia nueva debe declararse mediante `uv` y
justificarse frente a los principios de esta constitución.

## Flujo de Trabajo y Control de Versiones

- **Una rama por spec**: cada spec se desarrolla en su propia rama, siguiendo
  la convención de *conventional-branches*. Los prefijos de rama están en inglés
  (p. ej. `feature/`, `fix/`) y el contenido descriptivo en español.
- **Commits atómicos**: al finalizar la implementación de un spec se crean commits
  atómicos siguiendo *conventional-commits*. Los prefijos de commit están en inglés
  (p. ej. `feat:`, `fix:`, `test:`, `docs:`) y el mensaje descriptivo en español.
- **Progreso de tareas**: a medida que se completa una tarea de un plan, se marca
  inmediatamente como completada.
- **Ronda de preguntas obligatoria**: antes de crear una spec o cualquier documento
  potencialmente ambiguo, el agente realiza una ronda de preguntas a la persona
  usuaria. No se avanza hasta que agente y usuaria compartan el mismo entendimiento
  del problema.
- **Puertas de calidad**: antes de considerar una tarea terminada, el código pasa
  `ruff`, `mypy` y la suite de `pytest` en verde.

## Governance

Esta constitución tiene precedencia sobre cualquier otra práctica del proyecto.
Todo plan, spec y tarea debe verificarse contra estos principios antes de darse por
válido. Cualquier desviación debe justificarse explícitamente y acordarse con la
persona usuaria; si no puede justificarse, se rechaza. Las enmiendas a esta
constitución requieren documentación del cambio, aprobación de la persona usuaria y,
cuando aplique, un plan de migración. El versionado de la constitución sigue
versionado semántico (MAJOR.MINOR.PATCH).

**Version**: 1.0.0 | **Ratified**: 2026-11-11 | **Last Amended**: 2026-11-11
