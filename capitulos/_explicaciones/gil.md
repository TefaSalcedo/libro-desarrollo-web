::: {.callout-tip collapse="true" title="Explicación de: GIL"}
El **GIL** (Global Interpreter Lock) es el candado de Python: solo un
hilo ejecuta Python a la vez por proceso. Por eso Python escala con
*procesos* (workers) y `asyncio`, no con hilos de CPU.
:::
