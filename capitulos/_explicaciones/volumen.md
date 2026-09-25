::: {.callout-tip collapse="true" title="Explicación de: volumen (Docker)"}
Un **volumen** es almacenamiento que sobrevive al contenedor: el
contenedor muere y renace, el volumen (los datos de Postgres) sigue
ahí. Sin volumen, `docker compose down` borra tu base de datos.
:::
