::: {.callout-tip collapse="true" title="Explicación de: N+1"}
El **N+1** es el bug de rendimiento más común: 1 query para la lista +
N queries (una por ítem) para los detalles = 101 viajes para 100
tareas. Se cura con JOIN o agregación: una sola query que lo trae todo.
:::
