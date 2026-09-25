::: {.callout-tip collapse="true" title="Explicación de: rate limit / 429"}
El **rate limit** es un presupuesto de requests: "5 logins por minuto
por IP". Quien lo excede recibe `429 Too Many Requests`. Frena fuerza
bruta, bugs de loop infinito y abuso.
:::
