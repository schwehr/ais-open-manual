# AGENTS.md — `ais-open-manual/` (repository root)

## What this repository is

**AIS Open Manual** (Kurt Schwehr, CC BY 4.0; `CITATION.cff` v0.0.1): an open,
community-vetted handbook on the maritime Automatic Identification System
(AIS) — hardware, RF, protocol, standards, collection networks, software,
security and analytics. The published site is built from `book/` with
[TeachBooks](https://teachbooks.io/) / Jupyter Book v1 and deployed to GitHub
Pages by `.github/workflows/call-deploy-book.yml`
(https://schwehr.github.io/ais-open-manual/).

The checkout currently contains **three independent trees**:

| Directory | What it is | Status |
|---|---|---|
| [`book/`](book/AGENTS.md) | The TeachBooks/Jupyter Book source that is actually built and deployed. Still the unmodified TeachBooks **template** (tutorial exercises, *Lorem ipsum* sample content, TeachBooks logos). | Publishing target; no AIS content yet. |
| [`fable-5.1/`](fable-5.1/AGENTS.md) | "The AIS Handbook" — a complete AI-drafted manuscript (commit *"A draft AIS handbook by Fable 5.1"*): 69 chapters in ten parts + 10 appendices, each paired with a `.bibtex`; 31 research dossiers; runnable Python companion code; synthetic sample data; generated SVG figures. mdBook layout (`SUMMARY.md`). | Draft source material. |
| [`gemini4/`](gemini4/AGENTS.md) | "The Maritime AIS Handbook / AIS: An Open Manual" — a second complete AI-drafted manuscript (commit *"A draft AIS handbook by Gemini 4"*): 40 chapters in eight parts + 8 appendices + front matter, `MASTER_BIBLIOGRAPHY.bib`, and a Python `unittest` suite. | Draft source material. |

`fable-5.1/` and `gemini4/` are **parallel drafts of the same book produced by
different models**. They do not share files, chapter numbering, style guides,
bibliographies or conventions. Treat them as raw material to be reviewed,
reconciled and migrated into `book/`, not as finished content. Do not assume a
fact, number or citation in one draft agrees with the other.

## Root files

| File | Summary |
|---|---|
| `README.md` | Project abstract, contributor list, CC BY 4.0 reuse terms, and the TeachBooks build recipe (`pip install -r requirements.txt`, `teachbooks build book`, output in `book/_build/`). Second half is still the TeachBooks template feature list. |
| `CITATION.cff` | Citation metadata: title *AIS Open Manual*, version 0.0.1, author Kurt Schwehr (ORCID 0000-0002-5624-8190), CC-BY-4.0, URLs for the GitHub Pages site and repo. |
| `LICENSE` | CC BY 4.0 for the book. |
| `WAIVER` | Contributor waiver. |
| `CODE_OF_CONDUCT.md` | Code of conduct. |
| `requirements.txt` | Build deps for `book/`: `teachbooks` and `git+https://github.com/TeachBooks/TeachBooks-Favourites`. (The drafts have their own, different `requirements.txt`.) |
| `.github/workflows/call-deploy-book.yml` | TeachBooks deploy-book workflow for GitHub Pages. |
| `.gitignore` | Standard Python ignores. |

## Every directory has its own `AGENTS.md`

There are ~45 nested `AGENTS.md` files. **Read the one for the directory you
are editing before changing anything there**; they carry file-level inventories
and directory-specific rules. Hierarchy:

- `book/` → `exercises/`, `extension_exercises/`, `figures/`, `some_content/`, `syntax_exercises/`
- `fable-5.1/` → `appendices/`, `chapters/`, `research/`, `data/`, `data/samples/`, `figures/` (+ `figures/chNN/` for ch01, 12, 21, 27, 28, 30, 31, 39, 42, 48), `code/` (+ `analytics/`, `decode/`, `figures/`, `rf/`, `security/`, `tdma/`, `tests/`, `viz/`)
- `gemini4/` → `book/` (+ `00-front-matter/`, `part1-…`–`part8-…`, `appendices/`), `tests/`

`fable-5.1/AGENTS.md.bak` is a byte-identical copy of `fable-5.1/AGENTS.md`;
ignore it (or delete it) rather than editing it.

## Build, run and test

| Tree | Command (run from that tree's root) | Notes |
|---|---|---|
| `book/` | `pip install -r requirements.txt && teachbooks build book` (from repo root) | Jupyter Book v1; `_toc.yml` is the TOC, `_config.yml` the config; `execute_notebooks: "off"`. |
| `fable-5.1/` | `pip install -r requirements.txt && pytest -q code` (or bare `pytest`, via `pytest.ini`) | 13 smoke tests in `code/tests/test_code.py`; needs `pyais`, `pandas`, `numpy`, `matplotlib`, `geopandas`/`movingpandas`/`duckdb`. `bpy` (Blender) is optional. Scripts resolve the repo root from their own path and default to `data/samples/` inputs — always run from `fable-5.1/`. |
| `gemini4/` | `python -m unittest discover -s tests` | Four self-contained `unittest` modules (bit decoding, Blender rigging math, spatial stats, and a `test_book_integrity.py` that asserts all 80 `TASKS.md` boxes are ticked, all `book/README.md` links resolve, 40 chapters ≥ 450 lines, 8 appendices ≥ 10 kB, and `MASTER_BIBLIOGRAPHY.bib` ↔ Appendix H key parity). |

## Rules that apply everywhere

- **Honesty over completeness.** Never invent citations, DOIs, court cases,
  patents, CVE ids, statistics, standard clause numbers or model numbers. Mark
  anything unconfirmed `(verify)`. Cite accident findings only to the official
  investigation report. Both drafts were machine-written; verify before
  promoting any claim into `book/`.
- **Security content is detection/defence-only.** No AIS transmit
  instructions, spoofing recipes or exploit code. In `fable-5.1/code/`,
  `rf/gmsk_demo.py` writes baseband to a file only and must never gain an SDR
  transmit path; `tdma/sotdma_sim.py` is slot bookkeeping only.
- **Licensing.** Prose, figures, tables → CC BY 4.0. Code in `fable-5.1/code/`
  → Apache-2.0 (see `fable-5.1/LICENSE`). New data files need a provenance
  entry (`fable-5.1/data/samples/PROVENANCE.md` pattern); imported figures must
  be registered in `fable-5.1/figures/LICENSES.md`.
- **Numbers must agree across files.** Shared constants (161.975/162.025 MHz,
  9.6 kbit/s GMSK, 2,250 slots/min, 256-bit / 26.67 ms slots, 12.5 W,
  −107 dBm sensitivity, 4.12·(√h₁+√h₂) km radio horizon, sentinels
  181°/91°/SOG 1023/COG 3600/HDG 511/ROT −128) are repeated in chapters,
  appendices, dossiers, code, figures and tests. Change them everywhere or
  nowhere.
- **Prefer targeted edits.** Many files are 50–160 kB with paragraph-per-line
  lines; use small, exact replacements rather than rewrites.
- **Preserve line endings.** `fable-5.1/appendices/*` and
  `fable-5.1/data/samples/*.csv` are CRLF; everything else is LF. Don't
  produce whole-file diffs by normalising.
- **Don't trust checklists; check the disk.** `fable-5.1/TASKS.md` and
  `gemini4/TASKS.md` are fully ticked but list things that don't exist (see
  below).

## Tree-specific conventions (summary — details in each tree's `AGENTS.md`)

### `book/` (TeachBooks template)
- MyST Markdown + `.ipynb`; one `#` title per file; figures via `{figure}`,
  citations via `{cite}`/`{cite:t}` against `book/references.bib`, rendered
  by `references.md`.
- New pages must be added to `book/_toc.yml` to appear.
- `exercises/007.md` and `syntax_exercises/007.md` share a number; exercise
  numbering in titles has drifted from filenames. Not a problem unless you
  renumber.

### `fable-5.1/` (mdBook-style draft)
- **Everything is paired:** `chapters/chNN-slug.md` ↔ `chNN-slug.bibtex`;
  `appendices/appendix-X-slug.md` ↔ `.bibtex`. Edit both halves together.
  `BIBLIOGRAPHY.bib` (734 entries) is an aggregate said to be generated — the
  generator is absent, so keep it in sync by hand.
- Fixed chapter template from `STYLE_GUIDE.md`: `# Chapter N — Title`, part
  blockquote, `**In this chapter.**`, numbered `## N.x` sections, then in
  order `## Then & now`, optional `## On the wire`, `## Validation,
  uncertainty & data quality`, `## Software`, `## Standards & guides`,
  `## Pitfalls`, `## Key takeaways`, `## References`. Recurring boxes are
  bold-labelled blockquotes (`> **Case file.**`, `> **Threat model.**`, …).
- Citations are author–year prose, **no** `[@key]`/`\cite{}` tokens. BibTeX
  keys: `AuthorYEARkeyword` or `ISSUER_ID_EDITION` (e.g. `ITU_M1371_6`).
- Cross-links are relative (`ch21-slug.md`, `../appendices/…`,
  `../figures/chNN/name.svg`, `../code/…`). Hundreds exist — search before
  renaming any slug.
- `research/r-*.md` dossiers (with confidence levels and `(verify)`) feed the
  chapters; check the dossier when changing a chapter fact and vice versa.
- **Generated, do not hand-edit:** `figures/chNN/*.svg` (from
  `code/figures/make_figures.py`, which also rewrites `figures/LICENSES.md`)
  and `data/samples/*` (from `code/analytics/make_samples.py`, seed 1371).
  Regenerating can break `code/tests/test_code.py` assertions and the quoted
  outputs in `appendices/appendix-i-cookbook.md`. Sample data contains
  *intentional* defects (MMSI `0`, default MMSI `1193046`) — don't "fix" them.
- `code/` has no packages; modules import each other via `sys.path.insert`.
  Renaming modules or public functions (`parse_line`, `decode_file`, `clean`,
  `haversine_nmi`, `fspl_db`, `radio_horizon_km`, `run`, …) or DataFrame
  columns breaks downstream scripts and tests.
- Referenced but **missing** from the checkout: `tools/` (`check_book.py`,
  `check_xrefs.py`, `check_citations.py`, `build_bibliography.py`,
  `make_stubs.py`), `manifest.json`, `book.toml`, `CHANGELOG.md`, some
  dossiers ticked in `TASKS.md`. Don't claim to have run the missing checkers.
- Conventions: `⟨H⟩` = timeline item from `schwehr/gis-history`, `⟨+⟩` =
  added for this book; "as of <Month YYYY>" on fast-moving facts; SI first,
  nmi/kn where mariners use them.

### `gemini4/` (Markdown draft with unittest suite)
- Mandatory 8-section chapter template (`STYLE_GUIDE.md`): Overview →
  `schwehr/gis-history` lineage → mathematical/bit-level foundations →
  hardware/standards/software ecosystem → security/failure modes → runnable
  code walkthrough → key takeaways checklist → cited references.
- Bit indexing is **0-based MSB-first `bits[a:b]`** (libais/`AIVDM.txt`
  style) in prose and code, with 1-based ITU tables noted where relevant;
  conventions live in `book/00-front-matter/notation-and-conventions.md`.
- `book/README.md` is the master TOC; `test_book_integrity.py` requires every
  link in it to resolve and every `MASTER_BIBLIOGRAPHY.bib` key to appear in
  `book/appendices/appendix-h-master-bibliography.md`. Adding a chapter,
  appendix, or bib entry means updating all three or the tests fail.
- `gemini4/AGENTS.md` documents a `scripts/` directory; it does not exist.
- Nested `AGENTS.md` files under `gemini4/book/` are content inventories
  (chapter-by-chapter synopses), useful for finding where a topic is covered.

## Known inconsistencies to keep in mind

- Chapter numbering differs completely between drafts (e.g. link layer /
  TDMA is `fable-5.1` ch21 but `gemini4` ch11/15; message deep dives are
  `fable-5.1` Part V vs `gemini4` Part VIII). Never copy a cross-reference
  from one tree into the other unchanged.
- Bibliographies differ in key style (`ITU_M1371_6` vs `itur2014m1371_5`) and
  edition cited (M.1371-6 vs M.1371-5).
- `fable-5.1` uses author–year prose citations; `gemini4` uses BibTeX-keyed
  references in Appendix H; `book/` (TeachBooks) uses MyST `{cite}` roles.
  Migration into `book/` requires converting citations, not pasting them.
- The root `README.md` and `book/` still describe the TeachBooks template;
  update them when real content lands.
