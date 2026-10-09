# AGENTS.md — `book/` (Current Directory)

## Directory Overview

This directory (`book/`) contains the source files, configuration, assets, and tutorial exercises for a [TeachBooks](https://teachbooks.io/) / Jupyter Book v1 template book. It includes the global book configuration (`_config.yml`), Table of Contents definition (`_toc.yml`), landing/overview pages, bibliography files, and five subdirectories organizing sample content, branding figures, and progressive exercises on the TeachBooks GitHub workflow, MyST Markdown syntax, and Sphinx extensions.

## Subdirectories

- **`exercises/`** ([`exercises/AGENTS.md`](exercises/AGENTS.md)): Hands-on tutorial exercises introducing the core TeachBooks and GitHub web workflow:
  - `001.md`: *Exercise 1: First file edit* — Editing `book/intro.md` on GitHub, committing to `main`, and checking the deployed book via GitHub Actions.
  - `002.md`: *Exercise 2: Add a new file to the table of contents* — Adding `file_to_be_added_to_toc.md` to `_toc.yml` and verifying the navigation online.
  - `003.md`: *Exercise 3: Change book configuration* — Customizing `author`, `logo.text`, and `repository_url` in `_config.yml`.
  - `004.md`: *Exercise 4: \_Your\_ Version of the Book* — Creating a GitHub Issue, branching (`1-<your_issue_title>`), and previewing branch deployments.
  - `005.md`: *Exercise 5: Merge your version in the original book* — Opening and merging a Pull Request into `main` and deleting the feature branch.
  - `005a.md`: *Exercise 6: Reuse content from another book* — Embedding external book pages via `external:` in `_toc.yml` and the TeachBooks Recombiner.
  - `006.md`: *Exercise 7: Contribute to the book of somebody else* — Collaborative fork-and-pull-request workflow with a partner repository.
  - `007.md`: *Add extensions to your book* — Installing third-party Sphinx extensions (e.g., `sphinx-indexed-definitions`) via `requirements.txt` and `_config.yml`.
  - `summary.md`: *Summary of exercises: All Exercises* — Flowchart and table mapping Exercises 1–7 to the 6-step TeachBooks workflow.
- **`extension_exercises/`** ([`extension_exercises/AGENTS.md`](extension_exercises/AGENTS.md)): Exercises covering built-in TeachBooks extensions and deployment workflows:
  - `014.md`: *Live code* — Creating interactive Python cells (`.ipynb` or Jupytext `.md`) and controlling execution/visibility with custom cell tags (`disable-execution-cell`, `disable-execution-page`, `auto-execute-page`, `thebe-init`, `thebe-remove-input-init`).
  - `015.md`: *Deploy Book Workflow* — Triggering and configuring the GitHub Actions Deploy Book Workflow (DBW) and repository variables (`PRIMARY_BRANCH`, `BEHAVIOR_PRIMARY`, etc.) for multi-branch academic year or draft/release setups.
  - `016.md`: *Image and Iframe Dark Mode Colour Inverter* — Configuring `Sphinx-Image-Inverter` (`inverter_all`, `inverter_saturation`), selective `:class: dark-light` inversion, and `only-light` / `only-dark` HTML classes.
  - `017.md`: *TeachBooks Favourites* — Exploring and customizing the `teachbooks_favourites` extension bundle in `_config.yml`.
- **`figures/`** ([`figures/AGENTS.md`](figures/AGENTS.md)): Static visual and branding assets configured in `_config.yml`:
  - `TB_favicon.ico`: Multi-resolution Windows icon file used as the site favicon.
  - `TeachBooks_logo.svg`: Light-mode TeachBooks SVG vector logo and wordmark.
  - `TeachBooks_logo_inverted.svg`: Dark-mode (inverted) TeachBooks SVG vector logo and wordmark.
- **`some_content/`** ([`some_content/AGENTS.md`](some_content/AGENTS.md)): Sample chapter content demonstrating Markdown and Jupyter Notebook integration:
  - `overview.md`: *Some content* — Placeholder chapter overview page with *Lorem ipsum* text.
  - `text_and_code.ipynb`: *Text and code* — Sample Jupyter Notebook with Markdown instructions for Thebe Live Code and a `print('hello world')` Python code cell.
- **`syntax_exercises/`** ([`syntax_exercises/AGENTS.md`](syntax_exercises/AGENTS.md)): Exercises on Markdown, MyST, and TeachBooks content authoring syntax:
  - `007.md`: *File structure by titles* — Structuring `.md` files with a single `#` chapter title and nested `##`–`######` section headings.
  - `008.md`: *Add visual media* — Uploading figures to `book/figures/`, using the `{figure}` directive for local/remote images, and embedding videos with `{video}` (`sphinx-iframes`).
  - `009.md`: *Use equations* — Writing inline (`$...$`) and block (`$$...$$`, `{math}`) TeX/LaTeX equations and coloring terms with `sphinx-named-colors`.
  - `010.md`: *Create tables* — Authoring Markdown pipe tables, `{table}` directives, and `{list-table}` directives.
  - `011.md`: *Cross-referencing content* — Linking chapters, sections, target labels (`(label)=`), equations (`{eq}`), tables/figures (`{numref}`, `{ref}`), and external URLs.
  - `012.md`: *Use admonitions* — Using fixed-title admonitions (`note`, `tip`, `warning`, etc.), custom-titled `{admonition}` and `{dropdown}` blocks, `:class:` combinations, and custom colors (`sphinx-named-colors`).
  - `013.md`: *Adding a Bibliography* — Managing `references.bib`, inline `{cite}` variants (`{cite:p}`, `{cite:t}`, `{cite:ps}`, `{cite:ts}`), `{bibliography}` directives, and citation/bibliography styles in `_config.yml`.

## Files in Current Directory

- **`_config.yml`**: Comprehensive Jupyter Book v1, Sphinx, MyST, and TeachBooks configuration file. Defines book metadata (`author`, `logo`, `html_favicon`, `repository_url`), notebook execution settings (`execute_notebooks: "off"`), `teachbooks_favourites` and Sphinx extension settings (Thebe live code, MathJax 3, `sphinx-external-toc`, `Sphinx-Image-Inverter`, `Sphinx-Iframes`, `Sphinx-Exercise`, `Sphinx-Named-Colors`, `Sphinx-Proof`, `Sphinx-Code-Examples`, `TeachBooks-Sphinx-Tippy`, `Sphinx-Metadata-Figure`, `Sphinx-Last-Updated-by-Git`, `Sphinx-GitHub-Alerts`), external page attribution settings, `references.bib`, and MyST parser extensions (`colon_fence`, `dollarmath`, `linkify`, `substitution`, `tasklist`).
- **`_toc.yml`**: External Table of Contents (`format: jb-book`, `root: intro.md`) organizing the book into three parts:
  1. *Part with some content* (`some_content/overview.md` and `some_content/text_and_code.ipynb`),
  2. *Exercises* (`exercises.md` with `exercises/001.md`–`006.md` and `exercises/summary`; `syntax_exercises.md` with `syntax_exercises/007.md`–`013.md`; `extensions.md` with `exercises/007.md` and `extension_exercises/017.md`, `014.md`–`016.md`), and
  3. *Miscellaneous* (`references.md`, `changelog.md`, `credits.md`).
- **`changelog.md`** (*Changelog*): Template changelog page with placeholders for tracking version dates, added/modified/deleted files, and GitHub diff links.
- **`credits.md`** (*Credits and License*): Template credits page (`(credits)=`) providing citation templates for the book and individual chapters, instructions on how the book is built (via GitHub Actions `call-deploy-book` or locally with `teachbooks build book`), CC BY 4.0 license details, external resource attribution placeholders (including a sample `{cite:t}` reference to `jason_moore`), and editor/acknowledgement sections.
- **`exercises.md`** (*Exercises TeachBooks workflow*): Introductory chapter page for the TeachBooks workflow exercises (`exercises/001.md`–`006.md`), featuring a self-assessment checklist of 7 workflow questions for users already familiar with Git and GitHub.
- **`extensions.md`** (*Extension exercises*): Introductory chapter page for the Sphinx extension exercises (`exercises/007.md` and `extension_exercises/014.md`–`017.md`), introducing `TeachBooks Favourites` and third-party Sphinx extensions.
- **`file_to_be_added_to_toc.md`** (*Title of the file to be added to the toc*): Unlisted sample Markdown file containing *Lorem ipsum* text, intentionally omitted from `_toc.yml` so learners can practice adding it in Exercise 2 (`exercises/002.md`).
- **`intro.md`** (*Welcome to the Template Book*): Root landing page of the book (`(intro)=`, configured as `root: intro.md` in `_toc.yml`), welcoming students and introducing the TeachBooks template and exercises.
- **`references.bib`**: Shared BibTeX bibliography database containing a starter `@misc{jason_moore, ...}` entry (*Learn Multibody Dynamics, SymPy*, Jason Moore, 2023).
- **`references.md`** (*References*): Bibliography chapter page that renders all cited references using the MyST `:::{bibliography}` directive.
- **`syntax_exercises.md`** (*Syntax exercises*): Introductory chapter page for the MyST Markdown and Jupyter Notebook syntax exercises (`syntax_exercises/007.md`–`013.md`), explaining the role of `.md` and `.ipynb` files for "user type 3" authors and linking to the Jupyter Book v1 cheatsheet.
