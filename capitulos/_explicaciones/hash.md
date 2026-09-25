::: {.callout-tip collapse="true" title="Explicación de: hash / bcrypt"}
Un **hash** es una función de un solo sentido: `contraseña →
`$2b$10$...`. No se puede revertir — por eso las contraseñas se
*hashean*, no se *cifran*. bcrypt es lento a propósito: fuerza bruta
cara para el atacante.
:::
