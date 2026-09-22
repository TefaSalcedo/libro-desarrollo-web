# Backend para desarrolladores frontend

Un concepto, tres lenguajes: TypeScript, Python y Go.

Libro escrito con [Quarto](https://quarto.org) (`project: book`). Una sola
fuente Markdown (`.qmd`) genera el sitio web buscable, el PDF (vía LaTeX) y
el EPUB.

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

- `_quarto.yml` — índice del libro (partes, capítulos, apéndices, formatos)
- `index.qmd` — prefacio
- `capitulos/` — cap-01 … cap-40 y ap-a … ap-f
- `capitulos/_plantilla.qmd` — plantilla de capítulo (no publicada)
- `docs/guia-de-estilo.md` — convenciones de autoría
- `styles.css` — badges de etiquetas de concepto

## Convenciones rápidas

- Prosa en **español**; código y comentarios de código en **inglés**.
- Ejemplos multi-lenguaje en `::: {.panel-tabset}` con pestañas
  `TypeScript` / `Python` / `Go`.
- Etiquetas de concepto: `[U][TS][Py][Go][D][Ops]` como badges CSS.
- Diagramas en bloques ```` ```{mermaid} ````.
