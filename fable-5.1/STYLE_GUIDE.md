# The AIS Handbook — Style Guide

This file is the governing specification for every chapter and appendix. The
checker `tools/check_book.py` enforces the mechanical parts. The human parts
(honesty, precision, tone) are enforced by review.

## 1. Deliverable per chapter

- `chapters/chNN-slug.md` — the chapter (slugs in `manifest.json`).
- `chapters/chNN-slug.bibtex` — every work cited in the chapter, BibTeX format,
  keys `AuthorYEARkeyword` (e.g., `Balduzzi2014ais`), standards keyed by issuer
  and id (e.g., `ITU_M1371_5`, `IMO_MSC74_69`).
- Target 3,500–7,000 words (hard ceiling 8,500 for chapters 21, 22, 28, 44).
- 2–6 recurring boxes (§3). At least 10 references.
- Appendices: `appendices/appendix-X-slug.md` (+ `.bibtex`); table-driven; no
  word target; must still end with References.

## 2. Chapter template — use exactly these top-level headings, in this order

```markdown
# Chapter N — Title

> **Part X — Part title.** One-sentence placement of the chapter in the book.

**In this chapter.** 120–180-word abstract: what the reader will be able to do.

## N.1 First section title
...numbered sections (N.1, N.2, ...; subsections ### N.1.1) following the
TABLE_OF_CONTENTS block; split/merge freely but keep the substance...

## Then & now
How the systems/processes in this chapter changed over time. Tag items that come
from https://github.com/schwehr/gis-history with ⟨H⟩ and items added for this
book with ⟨+⟩.

## On the wire            ← REQUIRED for chapters 13, 20–28, 30, 34, 39, 44, 59–61, 68, 69;
                            optional elsewhere. Bit layouts, NMEA sentences, slot
                            arithmetic, hex walk-throughs, IQ observations.

## Validation, uncertainty & data quality      ← MANDATORY in every chapter
How errors arise in this chapter's subject, how they propagate, how to detect
them, what to report. Concrete: procedures, numbers, statistics, worked example.

## Software
**Open source:** ... **Free but closed:** ... **Commercial:** ... (name, what it
does for this chapter, one caveat each). Write "None relevant." if truly none.

## Standards & guides
Bulleted list: issuer, document id, title, edition/year, what it governs here.

## Pitfalls
8–15 bullets. Each: the mistake → why it happens → how to detect/avoid it.

## Key takeaways
6–10 bullets; crisp, actionable.

## References
Full citations (authors, year, title, venue/publisher, volume(issue):pages or
issuer + id + edition). DOI/URL only if confident. Mark anything unconfirmed
"(verify)". Never invent papers, cases, patents, or standards.
```

## 3. Recurring boxes (blockquote with a bold label; 2–6 per chapter)

- `> **Case file.**` — a sourced real incident (accident report, court case, paper, news with primary-source backing).
- `> **On the wire.**` — short hex/bit/NMEA walk-through (may appear inside sections in addition to the On-the-wire heading).
- `> **Try it.**` — runnable snippet (Python / shell / SQL / Rust / C++) in a fenced block with expected output. Prefer open tools. Snippets longer than ~25 lines live in `code/` and are referenced.
- `> **Worked example.**` — numeric example with arithmetic shown.
- `> **Definitions that bite.**` — a term whose varying definitions cause errors.
- `> **Threat model.**` — attacker, capability, impact, mitigation. REQUIRED in chapters 33, 58–65, 67.
- `> **Legal note.**` — what is lawful where. REQUIRED in chapters 33, 42, 58–65, 67.
- `> **Rule of thumb.**` — heuristic with limits of validity.

## 4. Writing rules

- **Audience:** mariners, regulators, RF/software engineers, data scientists,
  security researchers, journalists, students. Assume numeracy, not jargon.
  Define and **bold** terms on first use in each chapter.
- **Voice:** direct, concrete; second person acceptable ("check the VSWR").
  No marketing language. Prefer numbers with units and sources over adjectives.
- **Honesty.** Do not fabricate statistics, dates, product specs, case names,
  CVE ids, or citations. If approximate, say "approximately" and cite. If
  unsure, write "(verify)". It is better to omit a number than to invent one.
  Do not invent DOIs. Do not cite papers you have not confirmed exist.
- **Dates and currency.** Fast-moving facts get "as of <Month YYYY>".
- **Units:** SI first. Distances at sea in nmi where mariners use them, with km
  in parentheses on first use. Speeds in kn. Frequencies in MHz, power in W (and
  dBm where RF-relevant), gain in dBi (note dBd if a datasheet uses it).
  Antenna heights in m. Tonnage as GT (gross tonnage), never "tons".
- **Protocol facts** are cited to ITU-R M.1371 by annex/clause where possible;
  interface facts to NMEA 0183 / IEC 61162; test behaviours to IEC 61993-2 /
  62287 / 62320.
- **Security content:** describe attacks at the level needed to detect and
  defend. No step-by-step transmit instructions, no transmit code. Every chapter
  touching transmission or exploitation carries Threat model + Legal note boxes.
- **Accidents:** cite the official investigation report (NTSB, MAIB, TSB,
  DMAIB, BSU, KMST, ATSB, JTSB, etc.). Do not go beyond report findings.
- **Cross-references:** relative Markdown links using the manifest, e.g.
  `[Chapter 21](ch21-link-layer-tdma.md)` from within `chapters/`, and
  `[Appendix C](../appendices/appendix-c-message-bit-layouts.md)`. From
  `appendices/`, link chapters as `../chapters/chNN-slug.md`.
- **Figures:** `![caption](../figures/chNN/name.svg)`; always alt text; licence
  noted in `figures/LICENSES.md`. Tables are Markdown tables, never images.
- Every chapter ends Pitfalls → Key takeaways → References.

## 5. Citation style (in text and in References)

- In text: author–year, e.g., "(Balduzzi, Pasta & Wilhoit 2014)", or standard
  short id, e.g., "(ITU-R M.1371-5, Annex 2 §3.3.4)".
- References: alphabetical. Formats:
  - Paper: Surname, I., Surname, I. (Year). Title. *Venue*, vol(issue):pages. doi:… (only if confirmed)
  - Standard: Issuer (Year). *Id — Title*. Edition. City: Issuer. URL (if public)
  - Report: Agency (Year). *Title* (Report no.). URL
  - Case: *Party v Party* [Year] Court Citation.
  - Web: Author/Org (Year). *Title*. Site. URL (accessed YYYY-MM-DD; archive URL if available)
  - Software: Author(s) (Year–). *Name* (version). URL. Licence.

## 6. ⟨H⟩ / ⟨+⟩ tags

- `⟨H⟩` — entry originates in schwehr/gis-history (keep the gis-history date).
- `⟨+⟩` — entry added for this handbook (must be cited).

## 7. Mechanical checks (what `tools/check_book.py` enforces)

1. First line `# Chapter N — Title` matching `manifest.json`.
2. Part blockquote and **In this chapter.** abstract present.
3. Required headings present and in order; On-the-wire where required.
4. Word count within [3,500, 7,000] (ceiling 8,500 for listed chapters); warn
   below 3,000.
5. Box count in [2, 6]; required Threat model / Legal note boxes present.
6. `(verify)` census reported (must be zero at M4).
7. `.bibtex` exists, parses, ≥ 10 entries; every cite-like token "(Surname YEAR" has
   a plausible key (warn only).
8. All relative links resolve (`tools/check_xrefs.py`).

## 8. Manifest

See `manifest.json` for the authoritative list of chapter numbers, slugs, titles,
parts, and appendix ids. `tools/make_stubs.py` generates stubs and
`SUMMARY.md` from it.
