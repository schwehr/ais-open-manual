# Contributing to The AIS Handbook

We welcome contributions, corrections, errata, and expansions from the maritime, radiocommunication, software engineering, and scientific communities.

## Code of Conduct

Please engage with professionalism, precision, and courtesy toward all contributors and reviewers.

## Principles of the Handbook

1. **Honesty and Rigor First:** Never invent or fabricate citations, court cases, patents, statistics, CVE identifiers, or equipment model numbers. If a fact cannot be independently verified from primary sources (standards bodies, regulatory filings, official accident investigation boards, or court dockets), it must either be confirmed through documented investigation or phrased with explicit uncertainty.
2. **Detection and Defense Focus:** Security-related topics strictly explore protocol mechanics, forensic detection, and defensive architectural resilience. Do not submit functional exploit scripts, malicious transmission instructions, or offensive denial-of-service code.
3. **Reproducibility:** Code examples, decoder walk-throughs, and sample pipelines must run cleanly using standard open-source tools and the provided test datasets under `data/samples/`.

## How to Propose Changes

1. **Typos & Factual Errata:** Open an issue or submit a pull request modifying the relevant chapter Markdown (`chapters/chNN-slug.md`) and updating the corresponding `.bibtex` file if citations are affected.
2. **Running the Quality Gates:**
   Before submitting changes, ensure all repository linters and cross-reference validators pass:
   ```bash
   python tools/check_book.py --strict
   python tools/check_xrefs.py
   pytest -q code
   ```
3. **Adding References:** Add primary source citations to both the chapter's `## References` section and its accompanying `chapters/chNN-slug.bibtex`. Re-run `python tools/build_bibliography.py` to regenerate `BIBLIOGRAPHY.bib`.
