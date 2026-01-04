# AIS Open Manual

https://img.shields.io/badge/status-draft-orange

[I am actively writing this book]

The maritime Automatic Identification System (AIS), originally established in
the 1990s as a tool for situational awareness for ship bridge crews, has
transformed into a complex global ecosystem. Over the last three decades, its
scope has expanded to encompass sophisticated vessel hardware, radio frequency
communications, international data standards, and vast terrestrial and
satellite collection networks. As AIS data becomes increasingly accessible, it
is fueling a new era of Artificial Intelligence (AI) and Machine Learning (ML)
applications in the maritime domain. However, the efficacy of these
technologies depends entirely on a rigorous understanding of the underlying
system. The AIS Open Manual serves as a comprehensive, community-vetted
repository designed to consolidate the disparate technical and operational
knowledge of AIS into a single, authoritative source. As a living resource,
this manual provides both the high-level overviews necessary for newcomers and
the technical depth required by experts, covering everything from fundamental
protocols to the cutting-edge technologies shaping the future of maritime
data.

## Contributors
- Kurt Schwehr

## Reuse content
Feel free to reuse this content or contribute to it. Please give appropriate credit, provide a link to the license, and indicate if changes were made ([CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/))

The website ([AIS Open Manual](https://schwehr.github.io/ais-open-manual/)) is created using the [TeachBooks Python package](https://github.com/TeachBooks/TeachBooks). To recreate it you have two options (more information in the [TeachBooks manual](https://teachbooks.io/manual/):
- In the GitHub interface: fork this repository, enable Github Pages from the source GitHub actions (Settings - Code and automation - Pages - Build and deployment - Source - GitHub Actions), enable workflows (Actions - I understand my workflows, go ahead and enable them) and run the call-deploy-book workflow (Actions - call-deploy-book - Run workflow - Run workflow). The website is released on the URL as shown on the workflow summary when the workflow has finished (Actions - call-deploy-book - call-deploy-book - Summary).
- On your own computer: clone this repository, install the required packages (`pip install -r requirements.txt`) and build the book (`teachbooks build book`). The website is stored locally in `book/_build/index.html`.

## Features
- A github repository structure  (`/book`) for making a TeachBook: a [Jupyter Book v1](https://github.com/executablebooks/jupyter-book) for educational purposes
- An empty TeachBook containing an intro page on root, an example markdown page, an example jupyter notebook page, an example references page. and an example credits page. (`/book/_toc.yml`, `/book/_config.yml`, `/book/credits.md`, `/book/intro.md`, `/book/references.md`, `/book/some_content/overview.md`, `/book/some_content/text_and_code.ipynb`)
- A file ready for adding references (`references.bib`, `/book/references.md`)
- An example favicon (web browser icon) (`/book/figures/favicon.ico`, `book/_config.yml`.)
- An example logo (`/book/figures/TUDelft_logo_rgb.png`, `/book/config.yml`)
- The configuration files set ready to make your Jupyter Notebooks pages work with [live code using our sphinx-thebe extension](https://teachbooks.io/manual/features/live_code.html) and our recommended settings (`/book/config.yml`)
- An example of setting up preprocessing your table of contents to hide certain draft chapters for eg. students (`_toc.yml`)
- A file containing all the recommended software packages (`requirements.txt`)
- A file containing the recommended license CC BY 4.0 (`LICENSE.md`)
- Our [GitHub workflow for publishing your TeachBook to GitHub Pages](https://github.com/TeachBooks/deploy-book-workflow) (`.github/workflow/call-deploy-book.yml`)
- A gitignore file containing standard python filetype to ignore (`.gitignore`)
- A readme containing information how to use the template, which can adjusted after using the template (`README.md`)
