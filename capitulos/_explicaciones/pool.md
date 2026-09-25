::: {.callout-tip collapse="true" title="Explicación de: pool de conexiones"}
Un **pool** es el staff de conexiones a la BD: abrir una conexión por
request es caro, así que el pool mantiene ~10–20 abiertas y las presta.
El request la usa, la devuelve, y la siguiente la reutiliza.
:::
