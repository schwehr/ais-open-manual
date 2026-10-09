# AGENTS.md — `extension_exercises/`

## Directory Overview

The `extension_exercises/` directory contains hands-on MyST Markdown tutorial exercises covering built-in TeachBooks extensions and GitHub Actions automation workflows. These exercises teach users how to configure and use interactive live coding (Thebe), automated multi-branch book deployment, dark-mode image/iframe color inversion, and the bundled `TeachBooks-Favourites` extension suite.

## Subdirectories

None.

## Files in Current Directory

- **`014.md`** (*Live code*): Explains how to create interactive, browser-executable Python code cells (using either `.ipynb` notebooks in JupyterLab/VS Code or Jupytext-enabled MyST `.md` files) and control their execution and visibility using custom TeachBooks cell tags (`disable-execution-cell`, `disable-execution-page`, `auto-execute-page`, `thebe-init`, and `thebe-remove-input-init`).
- **`015.md`** (*Deploy Book Workflow*): Guides users through triggering, monitoring, and customizing the GitHub Actions Deploy Book Workflow (DBW) across `main` and feature branches, configuring repository variables (`PRIMARY_BRANCH`, `BEHAVIOR_PRIMARY`, `BRANCH_ALIASES`, `BRANCHES_TO_DEPLOY`, `BRANCHES_TO_PREPROCESS`, `BRANCHES_ARCHIVED`), and setting up multi-branch deployment workflows for academic cohorts or draft/release pipelines.
- **`016.md`** (*Image and Iframe Dark Mode Colour Inverter*): Covers configuring the `Sphinx-Image-Inverter` extension in `_config.yml` (`inverter_all` and `inverter_saturation`), selectively toggling figure/iframe inversion with `:class: dark-light`, and showing theme-specific HTML text with `only-light` and `only-dark` CSS classes.
- **`017.md`** (*TeachBooks Favourites*): Introduces the `TeachBooks-Favourites` meta-extension (`teachbooks_favourites`), explains how to inspect or replace it in `_config.yml` under `sphinx.extra_extensions` to selectively load individual extensions (such as `sphinx_image_inverter`, `sphinx_iframes`, `teachbooks_sphinx_tippy`, or `sphinx_accessibility`), and outlines how to contribute new extensions to the upstream repository.
