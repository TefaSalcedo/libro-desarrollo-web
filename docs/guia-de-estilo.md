# Guía de estilo del libro

Convenciones de autoría para mantener los 40 capítulos coherentes.

## Idioma

- **Prosa en español.** Títulos, explicaciones, narrativa.
- **Código en inglés.** Identificadores, nombres de archivo, comentarios de
  código, mensajes de error simulados, nombres de commits.

## Estructura fija de capítulo

Todo capítulo sigue estas 11 secciones (en este orden):

1. `## El problema` — una necesidad real, formulada como "necesitamos…"
2. `## Cómo lo resuelve un equipo` — el contexto profesional
3. `## Conceptos nuevos` — lista con etiquetas de concepto
4. `## La explicación visual` — diagrama Mermaid, tabla o esquema
5. `## Implementación` — código en tabset ×3 cuando aplica
6. `## ¿Por qué cada stack lo hace así?` — la comparativa honesta
7. `## Errores comunes`
8. `## Buenas prácticas`
9. `## Ejercicio` — guiado, sobre el proyecto
10. `## Mini reto` — abierto, de razonamiento
11. Soluciones — callout colapsable (ver abajo)
12. `## Lo que deberías saber hacer ahora` — checklist

Capítulos agnósticos (datos, seguridad, ops) pueden omitir el tabset y la
sección 6 si no aplica — pero el patrón "problema primero" nunca se omite.

## Tabsets multi-lenguaje

````markdown
::: {.panel-tabset}

### TypeScript
```ts
// english code
```

### Python
```python
# english code
```

### Go
```go
// english code
```

:::

### ¿Por qué cada stack lo hace así?
````

Reglas:

- Orden siempre: TypeScript → Python → Go.
- El ejemplo debe resolver *el mismo problema* en los tres — no tres
  problemas distintos.
- La sección "¿Por qué cada stack…?" es obligatoria tras un tabset: ahí va la
  lección transferible.
- Si un lenguaje no tiene equivalente directo (p. ej. `Depends` de FastAPI),
  se dice explícitamente y se muestra el patrón manual.

## Etiquetas de concepto

Se escriben como spans con clase CSS (ver `styles.css`):

```markdown
<span class="tag tag-u">U</span> concepto universal
<span class="tag tag-ts">TS</span> solo Node/TypeScript
<span class="tag tag-py">Py</span> solo Python
<span class="tag tag-go">Go</span> solo Go
<span class="tag tag-d">D</span> bases de datos
<span class="tag tag-ops">Ops</span> infra/operación
```

## Ejemplos por sección

Regla: **cada sección lleva al menos un elemento concreto** — snippet,
llamada `curl`, respuesta HTTP de ejemplo, escenario numerado o tabla.
Las secciones narrativas (problema, equipo, errores, prácticas) no se
quedan en abstracto: un ejemplo corto que aterrice la idea.

## Soluciones

Ejercicios y mini retos siempre tienen solución, en un callout colapsable
después de "Mini reto" y antes del checklist:

````markdown
::: {.callout-note collapse="true" title="Soluciones"}

**Ejercicio.** ...solución — tabset ×3 si es de código...

**Mini reto.** ...respuesta modelo...

:::
````

## Diagramas

Mermaid dentro de bloques ejecutables de Quarto:

````markdown
```{mermaid}
flowchart LR
  Client -->|HTTP| Server --> DB
```
````

- Un diagrama por idea; etiquetas cortas en español.
- Comparativas → tablas Markdown, no prosa.

## Tono

- Segunda persona plural de equipo: "necesitamos", "nuestro endpoint".
- Preguntas explícitas constantes: "¿por qué un backend necesita esto?",
  "¿qué pasa si no lo hacemos?".
- Prohibido: re-enseñar conceptos que el lector ya sabe de JS (qué es una
  función, un array, async conceptual). Sí: contrastar diferencias que
  *importan* (modelo de errores de Go, GIL, event loops).
- Honestidad de stack: si Go gana un capítulo (concurrencia, Docker), se
  dice. Si FastAPI hace magia que Express no tiene, se dice.

## Front matter de capítulo

```yaml
---
title: "N. Título del capítulo"
subtitle: "El problema en una frase"
---
```

## Proyectos

- Proyecto contínuo: **Taskflow** (partes 1–8).
- Proyecto final: **Nexus** (workspace colaborativo, parte 9).
- El código de ejemplo usa nombres del dominio: `tasks`, `users`,
  `projects`, `sessions`.
