::: {.callout-tip collapse="true" title="Explicación de: lock / bloqueo (FOR UPDATE)"}
Un **lock** de fila (`SELECT ... FOR UPDATE`) dice "esta fila es mía
hasta que mi transacción termine": otros que la pidan esperan. Es como
el candado del probador de ropa — evita que dos editen lo mismo.
:::
