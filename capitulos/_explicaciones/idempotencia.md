::: {.callout-tip collapse="true" title="Explicación de: idempotencia"}
**Idempotencia** = repetir la operación da el mismo resultado que una
vez. `POST /pay` con `Idempotency-Key: abc` ejecutado dos veces cobra
una. Vital porque clientes y webhooks *siempre* reintentan.
:::
