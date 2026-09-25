::: {.callout-tip collapse="true" title="Explicación de: event loop"}
El **event loop** es el mecanismo de Node: un solo hilo que toma tareas
de una cola sin parar. Mientras una tarea espera (BD, red), atiende
otra. Por eso Node escala en I/O con un solo hilo — nunca se sienta a
esperar.
:::
