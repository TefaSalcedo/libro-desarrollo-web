::: {.callout-tip collapse="true" title="Explicación de: deadlock"}
Un **deadlock** es el abrazo mortal: la tx A tiene el lock de la fila 1
y pide la 2; la tx B tiene la 2 y pide la 1. Nadie avanza. La BD mata a
una — por eso los locks se toman siempre en el mismo orden.
:::
