::: {.callout-tip collapse="true" title="Explicación de: ORM"}
Un **ORM** (Object-Relational Mapper) traduce entre objetos del código
y filas de la tabla: `task.save()` en vez de `INSERT`. Cómodo para el
CRUD, peligroso si no sabes qué SQL genera (el N+1 nace ahí).
:::
