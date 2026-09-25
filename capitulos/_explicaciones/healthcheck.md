::: {.callout-tip collapse="true" title="Explicación de: health check"}
Un **health check** es el endpoint `/health` donde la app dice "estoy
viva". El orquestador/load balancer lo consulta cada pocos segundos:
si falla, reinicia la instancia o deja de mandarle tráfico.
:::
