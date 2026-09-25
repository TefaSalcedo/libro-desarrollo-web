::: {.callout-tip collapse="true" title="Explicación de: mock / stub"}
Un **mock** es un doble de pruebas: finge ser el servicio externo
(Stripe, SMTP) para que el test no cobre ni mande emails. Se mockea en
la *frontera* (tu adaptador), nunca la BD — fingir la BD es mentir el
test.
:::
