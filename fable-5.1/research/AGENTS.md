# `research/`

Per-topic research dossiers for *The AIS Handbook*, an open, citable handbook
on the maritime Automatic Identification System. Each `r-*.md` file records
what could be confirmed about one topic (standards, law, physics, hardware,
history, software, security) from primary sources, with a confidence level per
fact and explicit `(verify)` markers for anything unconfirmed. The dossiers are
written *before* the chapters in `../chapters/` are drafted (see `../PLAN.md`
§6 "Research sources and citation policy" and `../TASKS.md`); each one names
the chapter(s) it primarily feeds and the secondary chapters it supports.

The directory is prose-only (no code, no build step). Facts, quotations,
clause numbers and URLs in these files are the evidence base that chapter
authors cite; the final verification pass is expected to remove every
`(verify)` tag or delete the claim.

## Files

| File | Summary |
|---|---|
| `r-antennas.md` | AIS antenna practice: IMO SN/Circ.227 and COMSAR installation/separation guidance (including the 5 m vs 10 m discrepancy), antenna types and patterns at 162 MHz, active VHF/AIS splitters, coax loss tables, and choices for ships, small craft, tiny devices, shore stations and satellites. Primary dossier for Chapter 32. |
| `r-asm.md` | Application-Specific Messages carried in Messages 6/8/25/26 with 16-bit DAC/FI identifiers per M.1371-6 Annex 4 and IMO circulars; international and regional registries (Inland AIS, St. Lawrence Seaway, USCG), pyais vs libais decoder discrepancies, and a bit-level hand-decode of a right-whale area notice. |
| `r-demos.md` | Demonstration programs and testbeds 2002–2024 that piloted binary ASMs and e-Navigation services (St. Lawrence Seaway, Tampa Bay PORTS, Right Whale AIS, EfficienSea/STM, Korea SMART-Nav, etc.), with a ten-testbed comparison table, timeline, and analysis of why operational ASM uptake stayed limited. |
| `r-df-geolocation.md` | Locating AIS transmitters without trusting their reported position: VHF direction finding, multi-receiver terrestrial TDOA, single/multi-satellite RF geolocation (HawkEye 360, Unseenlabs), and range-ring plausibility checks; includes worked TDOA and Doppler examples and a candidate NumPy least-squares script. Centers on Chapter 35. |
| `r-failure-modes.md` | Failure modes of AIS stations and pipelines: misconfiguration, sensor outages, LED EMI, GNSS timing glitches (2008 PRN-32, week rollovers), Class B carrier-sense starvation; a 16-row failure catalogue (cause / on-air signature / detection / fixer) and a candidate Python stream validator. Primarily Chapter 36. |
| `r-fingerprinting.md` | Physical-layer RF forensics and protocol-level behavioral fingerprinting of AIS transmitters for spoof detection independent of MMSI; literature survey, the open AIS-TSH dataset, channel confounds, privacy implications, burst-anatomy diagram, and a candidate I/Q burst-metrics script. Feeds Chapter 34. |
| `r-gnss.md` | GNSS/SBAS in AIS: per-class receiver mandates, GNSS-denied fallback behavior, R-Mode and eLoran backups, a 37-product vendor survey of constellation support, Table 48 PA/RAIM flag decision logic, and Message 17 sizing calculations. |
| `r-hardware.md` | The AIS hardware and SDR landscape: transponder OEM consolidation (SRT, Garmin/Vesper), receiver tiers, open-source demodulators, transmit-capable research tools, and type-approval regimes; candidate SDR comparison tables, FCC ID teardown and receiver BOM worked examples. |
| `r-history-oss.md` | Repository archaeology of open-source AIS software 2006–2026: origins, commit timelines, licenses and lineages of gpsd, libais, noaadata, pyais, AIS-catcher and others, with a candidate 20-year timeline strip, lineage graph, and multi-decoder differential tests. |
| `r-history.md` | Verified historical milestones of AIS from Håkan Lans's STDMA patents through standardization, satellite constellations and commercial consolidation; tables of patent chronology, standard editions and launch dates, a chronological import from schwehr/gis-history, and a planned master timeline. |
| `r-interfaces.md` | Interface and encapsulation formats for AIS data: NMEA 0183 `AIVDM`/`AIVDO`, talker IDs, TAG blocks, IEC 61162-450/-460 Ethernet, NMEA 2000 PGNs (canboat mappings), and public feed/logging formats; planned sentence-anatomy and 6-bit armoring figures. |
| `r-law-eu-intl.md` | Treaty and EU legal framework for AIS outside US domestic law: SOLAS Ch. V, IMO A.1106(29), Directive 2002/59/EC, and sanctions advisories; verification tables plus planned comparisons of carriage thresholds and "keep it on" rules. |
| `r-law-us.md` | US statutory and regulatory framework: 46 U.S.C. § 70114 (MTSA), USCG carriage/operating rules in 33 CFR § 164.46, and FCC equipment rules in 47 CFR Part 80; proposed carriage matrix, certification flowchart, and worked examples on shore-station transmission bans and recreational MMSI provenance. |
| `r-link-layer.md` | The M.1371-6 data-link layer: SOTDMA, ITDMA, RATDMA, FATDMA, MSSA and CSTDMA access schemes, slot allocation, synchronization hierarchy and link-management messages; tables of frame/slot timing, candidate-slot rules and communication-state bit layouts, with worked nominal-increment and slot-offset examples. |
| `r-loading.md` | VDL channel capacity, congestion behavior and message recovery under heavy loading and satellite reception; satellite detection papers and decollision patents (e.g., CNES US 9,246,575), a port-anchorage loading worked example, and plans for a Python slot simulator. |
| `r-messages.md` | The Message 1–28 catalog under M.1371-6: bit-level field layouts, "not available" sentinels, and decoder differences; includes a 44-sentence canonical test-vector comparison (pyais 3.2.3 vs libais 0.17 vs gpsd expected values) and hand-decoding / rate-of-turn worked examples. |
| `r-noise.md` | RF noise and interference at 162 MHz aboard vessels and at shore receivers: IEC 60945 immunity/emission limits vs FCC Part 15, VHF transmit desensitization and NOAA Weather Radio interference worked examples, and mitigation procedures such as the USCG LED squelch test. |
| `r-organizations.md` | The institutional ecosystem: treaty bodies, standards organizations, national administrations and research institutions; the standards propagation chain (ITU-R WP 5B / IMO NCSR → IEC TC 80 → national type approval), IALA's 2024 intergovernmental conversion, and a table of public government AIS feeds. |
| `r-patents.md` | Patent history: Lans's STDMA/SOTDMA patents, the Johnson/Lesch Class B CSTDMA patent acquired by SRT, and satellite decollision and spoof-detection patents; expiration timelines, 17-vs-20-year term arithmetic, and an "expired vs live" status table. |
| `r-privacy.md` | Privacy, data protection and research ethics of open AIS broadcasts: GDPR applicability, Chinese data-sovereignty law, national open-feed filtering rules (Kystverket, Digitraffic), a re-identification worked example, a GDPR decision tree, and a coordinated-disclosure checklist. |
| `r-propagation.md` | 162 MHz propagation: radio horizon, two-ray sea reflection, anomalous ducting, and AIS as a tropospheric probe; ITU-R P-series references, Baltic and Adriatic receiver campaign data, a proposed radio-horizon nomogram, and planned two-ray/coverage Python scripts. |
| `r-rf-phy.md` | The RF physical layer and on-air framing per M.1371-6 and RR Appendix 18: core PHY parameters, receiver performance thresholds, power-vs-time envelope, packet layout, channel allocations, and CRC implementation references from rtl-ais. |
| `r-sources-gfw-bloomberg.md` | Critical evaluation of three secondary sources — a 2017 Global Fishing Watch history article, Johnny Harris's 2025 dark-fleet documentary, and a 2016 Scranton Bloomberg Terminal manual — documenting what each can and cannot substantiate (e.g., erroneous carriage thresholds; the manual covers energy maps, not AIS). |
| `r-standards-iala.md` | IALA's status (2024 transition to an intergovernmental organization) and AIS-relevant publications (R0126, G1082, G1117, …): shore services, AtoN station types 1/2/3, MMSI numbering, link-budget coverage targets, and the IALA ASM register schema. |
| `r-standards-iec.md` | IEC TC 80 standards: test standards for Class A, Class B, base stations and AtoN, IEC 61162 interfaces and display specs, plus regulatory lag in 47 CFR Part 80 and EU adoption; candidate standards-stack diagram and an IEC 61162-450 UdPbC multicast datagram example. |
| `r-standards-iho.md` | IHO chart and e-navigation data standards: legacy S-57/S-52/S-63, the S-100 family (S-101, S-104, S-111, S-124, S-125, S-201) and the MSC.530(106) transition roadmap; version registry tables, a chart-to-display stack diagram, and an AIS weather report vs S-104 HDF5 comparison. |
| `r-standards-imo.md` | IMO instruments for AIS: MSC.74(69) Annex 3, SOLAS V/19, A.1106(29), and circulars on installation, annual testing and ASMs; a reporting-interval comparison between MSC.74(69) and A.1106(29), a three-layer regulatory stack figure, and slot-allocation worked calculations. |
| `r-standards-itu.md` | Core ITU texts: M.1371-6 (02/2026), M.585-10 (04/2026), M.2092 and RR Appendix 18; PHY/link constants, Class A/B reporting schedules, single-slot Message 28 and AMRD Messages 60–63, and candidate figures for annex renumbering, packet layouts and MMSI formats. |
| `r-standards-nmea-rtcm-etsi.md` | Peripheral interface and device-class standards: NMEA 0183/2000/OneNet, RTCM SC 121/119/137, ETSI EN 303 098 (AIS-MOB), and CCNR/CESNI Inland AIS; `!AIVDM` framing and armoring, TAG block keys, NMEA 2000 PGNs, and the modified-SOTDMA MOB burst timeline. |
| `r-timing.md` | Time in AIS: UTC sourcing, slot timing accuracy, the five-level synchronization hierarchy, timekeeping requirements and GNSS-denied behavior; jitter budgets, sync state transitions, timing sentinels, the 2005 Saab R3/R4 leap-second case, and Trend Micro's link-management attacks. Primary dossier for Chapter 24. |
| `r-vdes.md` | VHF Data Exchange System: the four-component architecture (AIS, ASM, VDE-TER, VDE-SAT), Appendix 18 channel allocations, VDE-SAT missions (NorSat-2/TD, Sternula-1, YMIR-1), and IMO MSC 111 decisions; worked data-rate and channel-numbering checks. |

## Notes for agents

- **Common template.** Every dossier follows the same skeleton: an H1
  `# Dossier: <topic>`, a bold **Purpose.** paragraph stating the as-of date
  and the chapters it feeds (primary target in bold), a `> Research-session
  note.` blockquote describing which sources were read directly vs. via search
  summaries, then the H2 sections `## Key questions` (numbered list),
  `## Primary sources located` (table: Source | Identifier/edition/year | URL
  | What it covers | Access), `## Verified facts` (table: Fact | Source
  (clause/page) | Confidence), `## Notes and quotes`, `## Open questions /
  (verify)`, `## Candidate figures and worked examples`, and `## Recommended
  use by chapter`. Some files add topic-specific H2s (e.g., `r-messages.md`
  has `## Canonical test-vector set`). Keep new or edited dossiers in this
  shape.
- **Confidence and `(verify)`.** Facts carry `high` / `medium-high` /
  `medium` / `low` confidence; `high` means the primary PDF/page was read
  directly. Anything not confirmed is tagged `(verify)` inline. Do not remove a
  `(verify)` tag without actually checking the source, and do not add a claim
  without a source and confidence level.
- **Citation style.** Standards are cited as issuer + id + edition + year
  (e.g., ITU-R M.1371-6 (02/2026)); M.1371-6 clauses use the `A2-x.y.z` form.
  URLs are given for every source; prefer free/official PDFs over
  restatements.
- **Relationship to chapters.** Each dossier's Purpose paragraph and
  `## Recommended use by chapter` section map content to chapter numbers in
  `../PLAN.md` / `../TABLE_OF_CONTENTS.md`. When a chapter in `../chapters/`
  is drafted or changed, check the corresponding dossier(s) here first; when a
  dossier fact changes, the dependent chapters may need updating.
- **Cross-dossier overlap.** Topics intentionally overlap (e.g., timing is
  split across `r-timing.md`, `r-gnss.md`, `r-link-layer.md`; standards across
  `r-standards-*.md`; law across `r-law-us.md`, `r-law-eu-intl.md`,
  `r-privacy.md`). Keep facts consistent across them — the same numeric
  constant should not disagree between files.
- **Scratch material.** Some session notes reference fuller working files
  (e.g., `timing_research.md`) that live in agent scratch space, not in this
  repository; only the `r-*.md` dossiers are canonical.
- **No code to run.** Candidate scripts mentioned in dossiers (TDOA solver,
  stream validator, slot simulator, burst metrics) are proposals; actual code
  belongs in `../code/`, not here.
