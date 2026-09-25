::: {.callout-tip collapse="true" title="Explicación de: hilo / thread / goroutine"}
Un **hilo** (thread) es una línea de ejecución dentro del proceso:
varios hilos = varias cosas "a la vez". Go los hace baratísimos
(goroutines); Node usa un solo hilo con event loop; Python tiene el
GIL que los limita.
:::
