::: {.callout-tip collapse="true" title="Explicación de: multi-stage build"}
Un **multi-stage build** compila la imagen en dos fases: una gorda con
todo el toolchain (compila), una flaca que solo recibe el resultado
(corre). La imagen final es chica y sin compiladores ni dev-deps.
:::
