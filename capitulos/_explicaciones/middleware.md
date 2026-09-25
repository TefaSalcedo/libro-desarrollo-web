::: {.callout-tip collapse="true" title="Explicación de: middleware"}
Un **middleware** es un filtro en la cadena del request: pasa por él
antes de llegar a tu handler. Auth es middleware — "verifica el token"
vive una vez y protege todas las rutas, no se copia en cada una.
:::
