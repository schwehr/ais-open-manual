# AGENTS.md — Repository Root (`ais-open-manual/gemini4`)

## Directory Overview
This root directory houses *The Maritime Automatic Identification System (AIS) Handbook: From RF Physics, Protocol Internals, and Open-Source Software to Global Surveillance, 3D Visualization, Security, and Spatial Analytics* (*AIS: An Open Manual*). The repository contains the top-level architectural blueprint (`PLAN.md`), authoring conventions (`STYLE_GUIDE.md`), phased 80-task execution backlog (`TASKS.md`), master BibTeX database (`MASTER_BIBLIOGRAPHY.bib`), the complete 40-chapter / 8-appendix manuscript (`book/`), utility script scaffolding (`scripts/`), and the automated Python `unittest` verification suite (`tests/`).

## Files in This Directory

### 1. `MASTER_BIBLIOGRAPHY.bib`
- **Purpose:** Canonical BibTeX citation database (`846 lines`, 80+ verified entries) referenced across all 40 chapters and `book/appendices/appendix-h-master-bibliography.md`.
- **Summary of Sections (`H.1`–`H.8`):**
  - **H.1 Historical Lineage, GIS History, & Global Fishing / Dark-Vessel Studies:** `schwehr2026gishistory` (`schwehr/gis-history`), `cutlip2017aishistory`, `harris2025darkzones` (2025 Johnny Harris / GFW investigation), `kroodsma2018tracking` (*Science*), `paolo2024satellite` (*Nature* 2024 SAR+AIS dark-vessel study), `park2020illuminating`, `welch2022unseen`, `miller2018identifying`, `sobel1995longitude`, `bowditch2019american`.
  - **H.2 Primary International Standards:** `itur2014m1371_5`, `itur2022m585_9`, `itur2022m2092_1` (VDES), `itur2019m2135_0` (AMRD), `itur2013m2287_0` (VDL loading), `itur2006m823_3`, `itur2019p1546_6`, `itur2021p528_5`, `itur2024rr_app18`, `imo2000solas_v19`, `imo2006solas_v19_1` (LRIT), `imo1998msc74_69`, `imo2015a1106_29`, `imo2023a1192_33`, `imo2003sncirc227`, `imo2010sncirc289`, `imo2010sncirc290`, `imo2007msccirc1252`, `imo2019modelcourse134`, `imo1972colregs`, `iec2018_61993_2`, `iec2017_62287_1_2`, `iec2015_62320_1_2_3`, `iec2010_61097_14`, `iec2024_61162_series`, `iec2012_61996_1` (VDR), `iec2022_63173_2` (SECOM), `iala2016a124_a126`, `iho2025s100_series`, `rtcm2015_12301_11901`, `ccnr2019inland_ais`.
  - **H.3 Open-Source Software, 3D Visualization (Blender), & Data Engineering:** `schwehr2010libais`, `schwehr2006noaadata`, `schwehr2009areanotice`, `kak2007bitvector`, `raymond2024gpsd_aivdm`, `lane2006aisparser`, `richter2020pyais`, `vries2021aiscatcher`, `oyrzanowski2020nmeaparser`, `graser2019movingpandas`, `blender2002community`, `domlysz2014blendergis`, `raasveldt2019duckdb`, `zimanyi2020mobilitydb`.
  - **H.4 RF Propagation, S-AIS De-Collision, & Passive Radar:** `hoye2008space`, `eriksen2006maritime`, `eriksen2010tracking`, `cervera2011time`, `last2014how`, `zhang2018tropospheric`, `braca2017maritime`.
  - **H.5 Cybersecurity, Spoofing, RF Fingerprinting, & SS7/Diameter:** `balduzzi2014security`, `cve2025_66217`, `c4ads2019above`, `goudossis2019towards`, `scirocco2023sei_ais`, `3gpp2024ts29002_29272`, `engel2014ss7`, `gsma2023fs11_fs19`.
  - **H.6 Marine Mammal Conservation (Whale Alert), Emissions (STEAM), & URN:** `wiley2011modeling`, `vanderlaan2007vessel`, `conn2013vessel`, `baumgartner2011generalized`, `johnson2003digital`, `jalkanen2012extension`, `macgillivray2019functional`, `freeman2017icoads`.
  - **H.7 Commodity Trading & Bloomberg Terminal:** `scranton2018bloomberg` (Scranton *Bloomberg Training Manual*), `cerdeiro2020world`, `adland2017does`, `schneekluth1998ship`.
  - **H.8 Landmark Admiralty Court Cases, Statutes, & Patents:** `uksc2021alexandra1` (`[2021] UKSC 6`), `ewhc2020sakizaya`, `sdny2022mccain`, `edla2014deepwater`, `sdny2019wisehonest`, `ntsb2024mvdali`, `us1990opa90_mtsa2002`, `lans1996us5506587` (US Patent 5,506,587 & 2010 reexamination cancellation), `mabson2010us7839336`.

### 2. `PLAN.md`
- **Purpose:** Master architectural blueprint (`934 lines`) for the 8-part, 40-chapter, 8-appendix handbook.
- **Summary:**
  - **Section 1 (Executive Summary & Philosophy):** Explains why every AIS record is a conditioned observation shaped by shipboard sensors, the 1PPS-synchronized SOTDMA MAC state machine, the GMSK VHF physical layer, heterogeneous terrestrial/satellite collectors, and adversarial spoofing/jamming.
  - **Section 2 (8-Part Chapter Architecture):** Defines the mandatory 8-section pedagogical template used across chapters.
  - **Section 3 (12-Point Gap Analysis):** Documents 12 critical technical domains added beyond the initial prompt (all 27 ITU message schemas, SOTDMA/ITDMA/FATDMA/RATDMA/CSTDMA state machines, device class taxonomy, Inland AIS `DAC=200`, IMO hull number vs. MMSI entity resolution, bridge sensor fusion, cloud-native GeoParquet/DuckDB/H3 analytics, STEAM emissions & URN modeling, SAR/VIIRS/RF fusion, subsea cable anchor-drag forensics, biosecurity graphs, and VDES/SECOM PKI).
  - **Section 4 (`schwehr/gis-history` Synthesis):** Chronological table (`~206 BCE` to `2026+`) linking geodesy, GIS, Blender (`1994/2002`), and AIS history.
  - **Section 5 (Master Outline of Front Matter, Parts I–VIII [Chapters 1–40], & Appendices A–H):** Detailed section-by-section specification for every chapter and appendix, including the 6-part forensic engineering profile for Part VIII (`Chapters 31–40`).
  - **Section 6 (Initial Master Bibliography):** Categorized primary reference list.

### 3. `STYLE_GUIDE.md`
- **Purpose:** Authoring and technical style guide (`24 lines`) governing the manuscript.
- **Summary:**
  - Defines the dual audience (operational mariners/VTS/policy analysts and deep RF/DSP/software/statistical/security engineers).
  - Enforces the 8-part chapter structure (Overview, `schwehr/gis-history` Lineage, Mathematical/Bit-Level Foundations, Hardware/Standards/Software Ecosystem, Security/Failure Modes, Runnable Code Walkthrough, Key Takeaways Checklist, Cited References).
  - Standardizes bit indexing (**0-based MSB-first** `bits[a:b]` as in `libais`/`AIVDM.txt` vs. **1-based MSB-first** ITU tables; LSB-first over-the-air byte transmission vs. MSB-first 6-bit NMEA armor), two's-complement signed integer extraction and explicit sentinels (`181.0° = 0x6791AC0`, `91.0° = 0x3412140`, `ROT = -128`), RF gain conversion ($\text{dBi} = \text{dBd} + 2.15\text{ dB}$), and WGS84-to-ENU/equal-area projection rules (eliminating cosine-latitude distortion and Blender `float32` vertex jitter).

### 4. `TASKS.md`
- **Purpose:** Phased actionable task backlog (`430 lines`, `80` checked-off tasks `[x]` across Phases 0–9) and prompt-to-chapter traceability matrix.
- **Summary:**
  - **Phase 0 (`TASK-001`–`TASK-004`):** Repository scaffolding, `notation-and-conventions.md`, `ais-and-gis-history-timeline.md`, and `acronyms-and-glossary.md`.
  - **Phase 1 (`TASK-101`–`TASK-111`):** Part I (`Chapters 1–4`) plus Appendices E & F.
  - **Phase 2 (`TASK-201`–`TASK-213`):** Part II (`Chapters 5–10`) plus Appendix G.
  - **Phase 3 (`TASK-301`–`TASK-309`):** Part III (`Chapters 11–16`) plus Appendices A, B, C, & D.
  - **Phase 4 (`TASK-401`–`TASK-407`):** Part IV (`Chapters 17–20`).
  - **Phase 5 (`TASK-501`–`TASK-506`):** Part V (`Chapters 21–23`).
  - **Phase 6 (`TASK-601`–`TASK-606`):** Part VI (`Chapters 24–26`, including C++/Python/Rust parsers, `MovingPandas`, `DuckDB`, `Blender` `bpy`, `GateHouse`, and continuous-time/Horvitz-Thompson spatial statistics).
  - **Phase 7 (`TASK-701`–`TASK-710`):** Part VII (`Chapters 27–30`, including `CVE-2025-66217`, RF SEI fingerprinting, Encrypted AIS, GFW dark vessels, SS7/Diameter mobile tracking, Bloomberg Terminal `BMAP`/`SHIP`/`VSRC`/`VSTK`/`FLET`, and *Listen for Whales* / *Whale Alert*).
  - **Phase 8 (`TASK-801`–`TASK-804`):** Unit test suites (`tests/`) and `MASTER_BIBLIOGRAPHY.bib` / Appendix H parity audit.
  - **Phase 9 (`TASK-901`–`TASK-910`):** Part VIII (`Chapters 31–40`) bit-level deep dives into Messages 1–27, `DAC = 1` (`FI = 0–32`), and Regional ASMs (`DAC = 200, 232/235, 316/366, 351, 503, 440`).
  - **Section 12:** Complete Prompt-to-Plan/Task Traceability Matrix verifying 100% coverage of all user topics.

---

## Subdirectories

### 1. `book/` (see `book/AGENTS.md`)
Contains `book/README.md` (Master Table of Contents) and 10 leaf subdirectories containing all 51 markdown manuscript files:
- **`book/00-front-matter/`** (`book/00-front-matter/AGENTS.md`):
  - `acronyms-and-glossary.md`
  - `ais-and-gis-history-timeline.md`
  - `notation-and-conventions.md`
- **`book/part1-history-governance/`** (`book/part1-history-governance/AGENTS.md`):
  - `ch01-introduction-and-uses.md`
  - `ch02-history-of-navigation-and-ais.md`
  - `ch03-governance-standards-and-patents.md`
  - `ch04-legal-cases-casualties-and-privacy.md`
- **`book/part2-rf-hardware/`** (`book/part2-rf-hardware/AGENTS.md`):
  - `ch05-vhf-rf-basics-channels-and-noise.md`
  - `ch06-rf-propagation-ducting-and-loading.md`
  - `ch07-physical-layer-encoding-and-packet-recovery.md`
  - `ch08-antenna-engineering-and-selection.md`
  - `ch09-transceiver-hardware-sdrs-and-home-station.md`
  - `ch10-shore-and-sea-collection-networks.md`
- **`book/part3-timing-protocol/`** (`book/part3-timing-protocol/AGENTS.md`):
  - `ch11-timing-signals-1pps-and-timing-attacks.md`
  - `ch12-gnss-systems-denial-and-jamming.md`
  - `ch13-mmsi-and-maritime-identity.md`
  - `ch14-nmea-0183-nmea-2000-tag-blocks-and-vdr.md`
  - `ch15-complete-ais-message-catalog-1-to-27.md`
  - `ch16-binary-asm-tides-ports-and-area-notices.md`
- **`book/part4-space-air-vdes/`** (`book/part4-space-air-vdes/AGENTS.md`):
  - `ch17-satellite-ais-reception-and-transmission.md`
  - `ch18-aircraft-drones-sar-and-direction-finding.md`
  - `ch19-fishing-gear-amrds-and-user-hacks.md`
  - `ch20-ais-2-0-vdes.md`
- **`book/part5-navigation-vts/`** (`book/part5-navigation-vts/AGENTS.md`):
  - `ch21-nautical-charts-ecdis-enc-and-s100.md`
  - `ch22-vts-demonstration-programs-and-agency-software.md`
  - `ch23-mariner-training-operations-and-accidents.md`
- **`book/part6-software-analytics/`** (`book/part6-software-analytics/AGENTS.md`):
  - `ch24-open-source-ais-decoders-and-encoders.md`
  - `ch25-post-processing-software-and-blender-3d.md`
  - `ch26-spatial-statistics-and-trajectory-modeling.md`
- **`book/part7-security-intelligence/`** (`book/part7-security-intelligence/AGENTS.md`):
  - `ch27-cybersecurity-malicious-data-dos-and-failures.md`
  - `ch28-spoofing-techniques-and-rf-fingerprinting.md`
  - `ch29-national-security-blue-force-and-dark-ships.md`
  - `ch30-alternative-tracking-ss7-diameter-traders-and-whales.md`
- **`book/part8-message-deep-dives/`** (`book/part8-message-deep-dives/AGENTS.md`):
  - `ch31-messages-01-02-03-class-a-position.md`
  - `ch32-messages-04-10-11-base-station-utc.md`
  - `ch33-messages-05-24-static-voyage-data.md`
  - `ch34-messages-09-18-19-27-sar-class-b-long-range.md`
  - `ch35-messages-12-13-14-15-16-20-21-22-23-safety-aton-vdl-control.md`
  - `ch36-messages-06-07-08-17-25-26-binary-and-dgnss.md`
  - `ch37-dac-001-international-asm-part1.md`
  - `ch38-dac-001-international-asm-part2.md`
  - `ch39-regional-asm-part1-european-inland-and-uk.md`
  - `ch40-regional-asm-part2-seaway-uscg-encrypted-and-support-matrix.md`
- **`book/appendices/`** (`book/appendices/AGENTS.md`):
  - `appendix-a-message-1-to-27-bit-tables.md`
  - `appendix-b-mid-and-mmsi-prefixes.md`
  - `appendix-c-nmea-6bit-ascii-and-checksum.md`
  - `appendix-d-binary-asm-dac-fi-registry.md`
  - `appendix-e-master-standards-matrix.md`
  - `appendix-f-court-cases-statutes-and-patents.md`
  - `appendix-g-home-ais-station-bom-and-configs.md`
  - `appendix-h-master-bibliography.md`

### 2. `scripts/`
Reserved empty directory for standalone build and utility scripts.

### 3. `tests/` (see `tests/AGENTS.md`)
Automated Python `unittest` verification suite:
- **`test_blender_ais_rigging.py`:** Tests WGS84-to-ENU `float32` jitter mitigation, Message 5/24 `A,B,C,D` antenna-offset hull rigging and bow sweep during turns, and $360^\circ$ wraparound crabbing/leeway angles.
- **`test_book_integrity.py`:** Verifies that all 80 tasks in `TASKS.md` are checked off, all links in `book/README.md` resolve, all 40 chapters ($\ge 450\text{ lines}$) and 8 appendices exist, and all 80+ BibTeX keys in `MASTER_BIBLIOGRAPHY.bib` appear in `appendix-h-master-bibliography.md`.
- **`test_nmea_and_bit_decoding.py`:** Tests NMEA 0183 + TAG block XOR checksums, 6-bit ASCII armor packing/unpacking, Message 1 bit extraction, two's-complement sentinels (`181°`, `91°`), non-linear ROT conversion, IMO modulo-10 check digits, and HDLC CRC-CCITT-16 + zero-bit stuffing/unstuffing.
- **`test_trajectory_spatial_stats.py`:** Tests reporting-rate invariance of continuous-time grid residence-time integration vs. naive ping counting ($2\text{ s}$ vs. $25\text{ s}$ cadence) and Horvitz-Thompson inverse-detection-probability weighting.
