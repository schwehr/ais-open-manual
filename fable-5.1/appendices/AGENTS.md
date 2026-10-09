# `appendices/`

This directory holds the ten back-matter appendices (A–J) of *The AIS Handbook*,
an open, citable handbook on the maritime Automatic Identification System. Where
the `chapters/` directory carries narrative prose, the appendices are
table-driven reference material: a timeline, a standards register, bit-level
message layouts, code tables, software/hardware/dataset/organization catalogs, a
glossary, and an executable code cookbook. They are the lookup targets that
chapters cross-reference (e.g. `[Appendix C](../appendices/appendix-c-message-bit-layouts.md)`).

Every appendix is a pair of files: `appendix-X-slug.md` (the content) and
`appendix-X-slug.bibtex` (the BibTeX records for the works listed in that
appendix's `## References` section). The repository's `STYLE_GUIDE.md` governs
both chapters and appendices; appendices have no word target but must still end
with a References section.

## Files

| File | Summary |
|---|---|
| `appendix-a-timeline.md` | Chronological register of AIS evolution from antiquity through 2026 in one large table, merging `schwehr/gis-history` milestones (tagged `⟨H⟩`) with handbook-specific milestones (tagged `⟨+⟩`), each row citing its source chapter or the gis-history repo. Ends with References. |
| `appendix-a-timeline.bibtex` | 15 BibTeX entries backing Appendix A: IMO, ITU-R and IEC standards, Håkan Lans's STDMA patent, Swedish Maritime Administration and Global Fishing Watch reports, and the gis-history repository. |
| `appendix-b-standards-register.md` | Master standards register for AIS across eight structural domains: a large table indexing each standard by issuing body, identifier, edition, regulatory status, access terms, scope, and citing chapters, plus a guide to the four-tier standards stack and how to obtain standards. |
| `appendix-b-standards-register.bibtex` | The largest bibliography in the directory (114 entries, ~1,076 lines) covering IMO, ITU-R, IEC TC 80, IALA, NMEA, RTCM, ETSI, IHO, CESNI, 3GPP, FCC and USCG instruments, mostly `@standard` and `@techreport` records. |
| `appendix-c-message-bit-layouts.md` | Bit-level reference for VDL Messages 1–28 per ITU-R M.1371-5/-6: global framing conventions, a summary table of all message types, per-message field/width/sentinel tables, and worked decodes with raw NMEA sentences, hex dumps, bit decompositions and runnable `pyais` snippets. |
| `appendix-c-message-bit-layouts.bibtex` | 16 entries: ITU-R M.1371, M.585, M.2135; IMO AIS/ASM resolutions and circulars; IEC 61993, 62287, 62320; IALA guidance; the GPSD AIVDM protocol document and the `pyais` library. |
| `appendix-d-code-tables.md` | Ten sections (D.1–D.10) of canonical enumerations: MID allocations, MMSI formats, navigational status, ship/cargo types (M.1371-6 vs. legacy), EPFD types, AtoN types, ASM DAC/FI register, NMEA 0183 talkers/formatters, NMEA 2000 PGNs (CANboat mappings), and a master sentinel-value register with parser-failure notes. |
| `appendix-d-code-tables.bibtex` | 13 entries: ITU-R M.1371, M.585, M.2135 and the Radio Regulations, IMO, IEC, IALA and NMEA standards, plus the CANboat NMEA 2000 database and the GPSD AIVDM decoding guide. |
| `appendix-e-software-catalog.md` | Catalog of the AIS software ecosystem in five sections (E.1–E.5) with Tables E.1–E.5: open-source decoders/encoders, SDR and RF tools, trajectory analytics and big-data engines, visualization suites and chartplotters, and government/commercial VTS platforms, each indexed by language, license, maintenance status (as of late 2026), architecture notes and citing chapters. |
| `appendix-e-software-catalog.bibtex` | 24 entries: software packages (libais, pyais, AIS-catcher, OpenCPN, …), IEC/IMO/ITU standards, the AIVDM and Blender manuals, and peer-reviewed papers on AIS security and trajectory analytics. |
| `appendix-f-hardware-catalog.md` | Hardware catalog in seven sections with comparative Tables F.1–F.7: Class A/B transponders, coastal receivers, SDR platforms, antennas and splitters, base stations and SAR beacons, transmit-capable research tools, and type-approval frameworks. |
| `appendix-f-hardware-catalog.bibtex` | 15 entries: ITU, IMO, IEC and ETSI equipment standards, an AIS security paper, and vendor/USCG NAVCEN technical manuals (SRT Marine Systems, Wegmatt). |
| `appendix-g-datasets-providers.md` | Catalog of AIS data sources in three sections: open-access and government datasets (Table G.1, e.g. NOAA Marine Cadastre, DMA, Global Fishing Watch), commercial providers and RF-geolocation vendors (Table G.2, e.g. Spire, Kpler, Windward, HawkEye 360), and ingest protocols/schemas with timestamp, coordinate and parsing traps (Table G.3). |
| `appendix-g-datasets-providers.bibtex` | 13 entries: Science/Nature/Acta Astronautica papers on fisheries, marine activity and space-based AIS; IMF, UNCTAD and EMSA reports; data dictionaries and API docs from NOAA/BOEM, DMA, Kystverket and Fintraffic; a Windward sanctions-evasion analysis. |
| `appendix-h-glossary.md` | Glossary and acronym registry in three table-driven sections: H.1 acronyms and initialisms, H.2 master glossary grouped into five thematic domains, and H.3 the "Definitions that bite" disambiguation register for easily conflated terms. Each term maps to governing standards and handbook chapters; no figures or code. |
| `appendix-h-glossary.bibtex` | 16 `@standard` entries (ITU-R M.1371, M.585, IEC 61993-2, IEC 62287, NMEA 0183, IMO, IALA, IHO, …) underpinning the glossary definitions. |
| `appendix-i-cookbook.md` | Executable code cookbook: Table I.1 indexes 14 recipe scripts under `../code/` (decoding, TAG blocks, link budgets, GMSK, SOTDMA/CSTDMA simulation, DuckDB density maps, MovingPandas trajectories, spoofing triage, Blender/SVG visualization) with chapter links and dependencies; sections I.2–I.7 give the command-line invocation and expected output for each. |
| `appendix-i-cookbook.bibtex` | 11 entries: ITU-R M.1371, IEC 61162-1 and NMEA 0183; pyais, libais, DuckDB, Blender and GPSD AIVDM documentation; AIS cybersecurity and MovingPandas papers; an RF propagation textbook. |
| `appendix-j-organizations.md` | Directory of treaty bodies, intergovernmental agencies, SDOs, national regulators and civil-society groups in the AIS/VDES ecosystem: Table J.1 (mandates and data accessibility), a five-tier Mermaid flowchart of standard propagation from UN bodies to vessel operations, and Table J.2 mapping practitioner tasks (MMSI registration, type approval, spoofing investigations) to responsible entities. |
| `appendix-j-organizations.bibtex` | 29 entries: IMO, ITU, IEC, IALA, IHO, ETSI, CESNI, CCNR, NMEA and RTCM instruments, EU directives and USCG Federal Register rules, the C4ADS GNSS-spoofing report, and the Science global-fisheries paper. |

## Notes for agents

- **Pairs are inseparable.** Each `appendix-X-slug.md` has a matching
  `appendix-X-slug.bibtex`. If you add, rename or remove a reference in the
  `## References` list of the `.md`, update the `.bibtex` in the same change
  (and vice versa). Do not add a new appendix without both halves.
- **Common structure.** Every `.md` opens with `# Appendix X — Title`, one or two
  framing paragraphs, numbered `##` sections (either `X.1`, `X.2`, … or plain
  `1.`, `2.`, … as in Appendix C), and ends with `## References`.
- **References are inline prose, not cite-keys.** The `.md` files contain no
  `[@key]` tokens; the References section is an alphabetical, human-readable
  list (author, year, title, publisher/journal, URL with
  `(accessed YYYY-MM-DD)`, DOI). The `.bibtex` is the machine-readable twin.
  BibTeX keys follow the repo convention `AuthorYEARkeyword` for works and
  `ISSUER_ID_EDITION` for standards (e.g. `IEC_61993_2_2001`); entry types seen
  here include `@standard`, `@techreport`, `@misc`, `@manual`, `@software`,
  `@article`, `@inproceedings`, `@book`, `@patent`.
- **Cross-links are relative.** Link chapters as
  `../chapters/chNN-slug.md` and sibling appendices as
  `appendix-X-slug.md` (some files use `../appendices/appendix-X-slug.md`;
  both resolve). Code recipes are referenced as `../code/...` paths; figures as
  `../figures/chNN/...`.
- **Table-driven, no word target.** Appendices are mostly large Markdown
  tables (some files are 100–160 KB with very long lines). Keep tables as
  Markdown, never images. Prefer editing a single row/cell with a targeted
  replace rather than rewriting the file.
- **Timeline tags.** In Appendix A, `⟨H⟩` marks events sourced from the
  external `schwehr/gis-history` chronicle and `⟨+⟩` marks handbook-originated
  events; keep the Source column consistent with the tag.
- **Code in Appendices C and I must stay runnable.** The pyais worked decodes
  in Appendix C and the recipe invocations/expected outputs in Appendix I
  describe scripts that live in `../code/`; if those scripts or their outputs
  change, re-verify the quoted commands and expected output here.
- **Line endings.** Files are UTF-8 with CRLF line endings; preserve that when
  editing to avoid whole-file diffs.
- **Governing docs.** `../STYLE_GUIDE.md` (appendix rules: `appendices/appendix-X-slug.md`
  + `.bibtex`, table-driven, must end with References) and `../CONTRIBUTING.md`
  apply. The repo-level `../BIBLIOGRAPHY.bib` is a separate aggregate; keep
  per-appendix `.bibtex` files self-contained.
