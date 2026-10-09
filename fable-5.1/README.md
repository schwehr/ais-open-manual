# The AIS Handbook

*The maritime Automatic Identification System, from "what is that triangle on my
chartplotter" to the bit timing of a GMSK burst, and from the sinking of the
Titanic to VDES.*

A comprehensive, citable handbook on AIS: radio physics, the TDMA link layer,
the message catalog, identities, standards and law, hardware and software,
users and uses, failure modes, security, and the system's history.

## Layout

- `PLAN.md` — master plan and chapter skeleton; `TASKS.md` — phased backlog.
- `STYLE_GUIDE.md` — governing chapter template and rules; `manifest.json` — chapter list.
- `TABLE_OF_CONTENTS.md` — per-chapter scope blocks.
- `chapters/`, `appendices/` — one `.md` + one `.bibtex` per document.
- `research/` — research dossiers that feed chapters.
- `code/` — tested "Try it" snippets; `data/samples/` — small redistributable samples.
- `tools/` — checkers and builders (see below).

## Build

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python tools/make_stubs.py          # stubs + SUMMARY.md from manifest.json
python tools/check_book.py          # structure checks
python tools/check_xrefs.py         # link checks
python tools/check_citations.py     # (verify) census; add --live for URL/DOI liveness
python tools/build_bibliography.py  # BIBLIOGRAPHY.bib
pytest code                         # run snippet tests
mdbook build                        # if mdBook is installed (book.toml)
```

## Decisions (defaults adopted 2026-10-04; owner may override)

- Build system: **mdBook** (`book.toml`, `SUMMARY.md`); code tested separately with pytest.
- Licence: prose **CC-BY-4.0**; code **Apache-2.0** (see `LICENSE`).
- First edition scope: all 69 chapters + 10 appendices.
- No live receiver assumed; samples come from open data with provenance noted.
- First-party projects (libais, noaadata, ais-area-notice, bitvector-modern) are
  treated neutrally but with implementation-level depth.

## Conventions

- `(verify)` marks an unconfirmed fact; none may remain at milestone M4.
- `⟨H⟩` marks timeline items from [schwehr/gis-history](https://github.com/schwehr/gis-history); `⟨+⟩` marks items added here.
- Security chapters describe attacks only to the depth needed to detect and defend; no transmit code.
