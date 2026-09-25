::: {.callout-tip collapse="true" title="Explicación de: inyección SQL"}
La **inyección SQL** es el clásico de romper la query: si concatenas
input del usuario en el SQL, el usuario *escribe SQL*. `' OR 1=1--`
borra tablas. La vacuna: queries parametrizadas (`$1`), siempre.
:::
