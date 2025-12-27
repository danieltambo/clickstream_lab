# Clickstream Component (Streamlit)

Este módulo implementa un componente personalizado de Streamlit para la
captura de interacciones del usuario (clickstream) sobre estímulos HTML.

Su objetivo es registrar eventos conductuales **crudos y temporalmente consistentes**
que puedan ser analizados posteriormente (p. ej. inferencia de patrones de procesamiento).

---

## Arquitectura general

El componente está dividido explícitamente en tres responsabilidades:

1. **Renderer**
   - Renderiza el estímulo HTML dentro del iframe.
   - No contiene lógica de medición ni eventos.
   - Expone una referencia al nodo DOM raíz.

2. **Logger**
   - Instrumenta eventos básicos (`hover`, `click`) sobre elementos marcados con `data-track`.
   - Emite eventos atómicos con timestamps locales.
   - No agrega, interpreta ni deriva métricas.

3. **App / index.tsx**
   - Orquesta el ciclo de vida del componente.
   - Inicializa el logger.
   - Envía eventos al backend de Streamlit.
   - Define el evento inicial de renderizado (`t0`).

La separación es deliberada para:
- evitar acoplamiento entre renderizado y medición
- preservar trazabilidad metodológica
- permitir análisis posterior reproducible

---

## Modelo de eventos

Los eventos emitidos siguen un modelo **mínimo y crudo**:

- `hover_start`
- `hover_end` (con duración)
- `click`

Cada evento incluye:
- `target`: identificador lógico (`data-track`)
- `timestamp`: marca temporal en cliente (`Date.now()`)

No se calculan métricas derivadas en frontend.

---

## Modelo temporal

- Todas las marcas temporales se generan en el cliente usando `Date.now()`
- El evento `render` define el instante `t0`
- Todos los eventos posteriores comparten el mismo reloj

Esto permite:
- reconstrucción secuencial
- cálculo posterior de latencias
- inferencia de patrones temporales

---

## Filosofía de diseño

- Medición explícita (opt-in vía `data-track`)
- Eventos atómicos, no interpretativos
- Separación estricta frontend / backend
- Compatibilidad con análisis probabilísticos posteriores

Este componente **no decide nada** sobre el comportamiento del usuario:
solo lo registra.


## Diagrama de Flujo

[ Streamlit (Python) ]
          |
          |  html
          v
+------------------------+
|  index.tsx (App)      |
|------------------------|
| - setComponentReady() |
| - define t0 (render)  |
| - init logger         |
+-----------+------------+
            |
            v
+------------------------+
|  Renderer              |
|------------------------|
| Render HTML stimulus   |
| Expose DOM reference   |
+-----------+------------+
            |
            v
+------------------------+
|  Logger                |
|------------------------|
| Listen on [data-track]|
| mouseenter / leave    |
| click                 |
+-----------+------------+
            |
            v
+------------------------+
| ClickstreamEvent       |
|------------------------|
| event                 |
| target                |
| timestamp              |
| duration?              |
+-----------+------------+
            |
            v
[ Streamlit backend ]
