# Desarrollo web completo

Aprende frontend, backend y nube — un concepto, tres lenguajes, y ningún
prerrequisito.

Libro escrito con [Quarto](https://quarto.org) (`project: book`). Una sola
fuente Markdown (`.qmd`) genera el sitio web buscable, el PDF (vía LaTeX) y
el EPUB.

## Las tres secciones

- **Sección I · Aprende Frontend** (`fe-01`…`fe-07`): el navegador como
  runtime, JS/TS esencial, DOM/estado, frameworks (React/Vue/Angular/
  Svelte), llamadas a APIs, build.
- **Sección II · Aprende Backend y BD juntos** (`cap-00`…`cap-40`): HTTP,
  APIs, validación, PostgreSQL, auth, testing — en TypeScript, Python y Go.
- **Sección III · Aprende Nube** (`nu-01`…`nu-05`, `cap-30`…`cap-35`):
  servidores, Docker, AWS/Azure/GCP, managed services, serverless.

## Requisitos

- [Quarto](https://quarto.org/docs/get-started/) (`winget install Posit.Quarto`)
- Opcional, para PDF: `quarto install tinytex`

## Uso

```bash
# Preview en vivo (http://localhost:4200 aprox., hot reload)
quarto preview

# Render completo -> _book/
quarto render

# Solo un formato
quarto render --to pdf
quarto render --to epub
```

## Estructura

- `_quarto.yml` — índice del libro (secciones, capítulos, apéndices, formatos)
- `index.qmd` — prefacio
- `capitulos/` — fe-01…07, cap-00…40, nu-01…05, ap-a…f
- `capitulos/_plantilla.qmd` — plantilla de capítulo (no publicada)
- `docs/guia-de-estilo.md` — convenciones de autoría
- `styles.css` — badges de etiquetas de concepto

## Convenciones rápidas

- Prosa en **español**; código y comentarios de código en **inglés**.
- Tabsets por **framework** en Sección I, por **lenguaje** (TS/Py/Go) en II.
- "En una frase" al abrir cada capítulo; profundizaciones en callouts
  colapsables; **prompts copiables** en los ejemplos insignia.
- Etiquetas de concepto: `[U][TS][Py][Go][D][Ops]` como badges CSS.
- Diagramas en bloques ```` ```{mermaid} ````.
- Código con resaltado `pygments` + botón de copiar (`code-copy`).
