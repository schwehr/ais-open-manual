# AGENTS.md — `exercises/`

## Directory Overview

The `exercises/` directory contains hands-on tutorial exercises in MyST Markdown format that guide users through the fundamental TeachBooks and GitHub web workflow. The exercises cover editing book pages, updating the Table of Contents (`_toc.yml`) and book configuration (`_config.yml`), working with GitHub Issues, branches, pull requests, forks, reusing external content, and installing custom Sphinx extensions.

## Subdirectories

None.

## Files in Current Directory

- **`001.md`** (*Exercise 1: First file edit*): Guides the user through making their first edit to `book/intro.md` directly in the GitHub web interface, committing to the `main` branch, inspecting the GitHub Actions build deployment, and verifying the updated site (including embedded H5P comprehension checks and a video/GIF walkthrough).
- **`002.md`** (*Exercise 2: Add a new file to the table of contents*): Teaches how to add an existing Markdown file (`file_to_be_added_to_toc.md`) to `book/_toc.yml` as a subpage under `some_content/overview.md`, commit the changes, and verify the updated navigation online.
- **`003.md`** (*Exercise 3: Change book configuration*): Explains how to customize book-wide settings in `book/_config.yml`, specifically updating the `author` footer, homepage title (`text`), and `repository_url`, and observing how `_config.yml` changes affect the entire deployed book.
- **`004.md`** (*Exercise 4: \_Your\_ Version of the Book*): Introduces collaborative version control practices on GitHub by walking through creating a GitHub Issue, creating an issue-linked branch (`1-<your_issue_title>`), adding a new page on that branch, and previewing the multi-branch deployment via GitHub Actions.
- **`005.md`** (*Exercise 5: Merge your version in the original book*): Continues from Exercise 4 by guiding the user through opening a Pull Request from their feature branch (`1-<your_issue_title>`) into `main`, linking the issue, merging the Pull Request, deleting the merged branch, and verifying the changes on `main`.
- **`005a.md`** (*Exercise 6: Reuse content from another book*): Demonstrates how to embed pages from external repositories into a book without copying files by using the `external:` key in `_toc.yml` (via the TeachBooks Recombiner or manual raw GitHub URLs) and checking the resulting attribution banner.
- **`006.md`** (*Exercise 7: Contribute to the book of somebody else*): A paired collaborative exercise covering the fork-and-pull-request workflow: opening an issue on a partner's repository, forking their repository, committing changes to the `book/` directory in the fork, submitting a cross-repository Pull Request (`Closes #<issue>`), and reviewing/merging incoming Pull Requests from a partner's fork.
- **`007.md`** (*Add extensions to your book*): Walks through adding an external Sphinx extension (`sphinx-indexed-definitions`) by listing the package in `requirements.txt`, enabling `indexed_definitions` under `sphinx.extra_extensions` in `_config.yml`, and using `{definition}` directives, `{ref}` cross-references, and automatic term indexing in Markdown pages.
- **`summary.md`** (*Summary of exercises: All Exercises*): Summarizes how Exercises 1–7 map to the 6-step TeachBooks workflow (Get an idea, Create your version, Edit the book, Check changes online, Repeat edit and checking, Submit for review) with a workflow flowchart and table.
