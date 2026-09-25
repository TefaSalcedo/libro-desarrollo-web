::: {.callout-tip collapse="true" title="Explicación de: paginación"}
**Paginar** es servir la lista en páginas (20 por 20) en vez de las
10 millones. `LIMIT 21` + cursor = la página siguiente se pide con la
última fila vista, no con "salta 40000" (offset, que se degrada).
:::
