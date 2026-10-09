# AGENTS.md — `syntax_exercises/`

## Directory Overview

The `syntax_exercises/` directory contains hands-on tutorial exercises teaching Markdown, MyST Markdown, and TeachBooks authoring syntax. Topics progress from basic chapter and heading structure to visual media (figures and videos), LaTeX math equations (including custom color styling), tables, internal and external cross-referencing, admonitions/dropdowns, and BibTeX bibliographies.

## Subdirectories

None.

## Files in Current Directory

- **`007.md`** (*File structure by titles*): Teaches how to create a new `.md` chapter file in `/book`, structure it using a single top-level `#` chapter heading along with `##`–`######` section/subsection headings, add it to `_toc.yml`, and verify how headings map to Table of Contents titles and URLs.
- **`008.md`** (*Add visual media*): Explains how to upload image files to `book/figures/` and embed local or remote images using the `{figure}` directive (with `width`, `align`, and caption options, plus relative path conventions), as well as how to embed online videos (e.g., YouTube) using the `{video}` directive from `sphinx-iframes`.
- **`009.md`** (*Use equations*): Covers writing inline (`$...$`) and block (`$$...$$` and `{math}` directive) TeX/LaTeX equations, common mathematical symbols (`\sqrt`, `\frac`, `\int`, `\sin`, subscripts/superscripts), previewing/debugging syntax errors in GitHub, and coloring equation terms using the `sphinx-named-colors` extension (`\namedcolour{...}` and `\class{hyphen-color}{...}`).
- **`010.md`** (*Create tables*): Demonstrates creating tables using standard pipe-separated Markdown syntax, the MyST `{table}` directive (supporting captions, `:widths:`, and `:align:`), and the `{list-table}` directive (supporting `:header-rows:`).
- **`011.md`** (*Cross-referencing content*): Guides users through linking to other chapters/sections via relative Markdown links (`[text](path/to/file.md)`), local header anchors (`#section`), and MyST target labels (`(label)=`) with `{ref}`, as well as numbering and referencing equations (`(eq:label)` / `{eq}`), tables (`:name:` / `{numref}`), figures (`name:` / `{numref}`), and external URLs.
- **`012.md`** (*Use admonitions*): Covers fixed-title admonitions (`note`, `tip`, `warning`, `attention`, `caution`, `important`, `seealso`, `error`, `hint`, `danger`), custom-titled `{admonition}` and `{dropdown}` blocks, combining style and collapsible `:class:` options (e.g., `:class: important dropdown`), and styling admonitions with CSS/custom colors via `sphinx-named-colors`.
- **`013.md`** (*Adding a Bibliography*): Teaches managing BibTeX entries in `references.bib`, citing sources inline with `{cite:p}`, `{cite:t}`, `{cite:ps}`, and `{cite:ts}`, rendering reference lists with `{bibliography}` (including `:filter: docname in docnames` and `:style:` options `alpha`, `plain`, `unsrt`, `unsrtalpha`), and configuring `bibtex_reference_style` (`author_year`, `label`, `super`, `number`) in `_config.yml`.
