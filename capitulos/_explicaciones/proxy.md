::: {.callout-tip collapse="true" title="Explicación de: reverse proxy"}
Un **reverse proxy** (nginx, ALB, Cloudflare) es el portero: recibe
todo el tráfico en el 443, termina TLS y reparte a tu app interna.
La app nunca mira a internet directamente — el proxy la protege.
:::
