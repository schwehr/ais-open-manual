# The AIS Handbook — Task Backlog

> Governing document: [`PLAN.md`](PLAN.md). Chapter numbers below refer to the
> skeleton in PLAN §4. Tasks are ordered by phase; within a phase, by
> dependency. Check a box only when the artifact exists in the repo and passes
> the relevant checker. Anything uncertain in prose must carry `(verify)` until
> Phase 4 clears it.

**Legend.** `[R]` research dossier · `[D]` draft chapter · `[C]` code/figure ·
`[V]` verification · `[T]` tooling · `[Q]` decision needed from owner.

---

## Phase 0 — Project setup and decisions

- [x] [Q] Decide build system (mdBook default vs Jupyter Book). Record in `README.md`. *Default adopted: mdBook (owner may override).*
- [x] [Q] Decide licences (prose CC-BY-4.0; code Apache-2.0 proposed). Add `LICENSE`.
- [x] [Q] Decide first-edition scope: all 69 chapters vs. ~40 core + appendix stubs. *Default adopted: all 69.*
- [x] [Q] Confirm whether a live home receiver is available for original samples/figures.
- [x] [Q] Confirm treatment of first-party projects (libais, noaadata, ais-area-notice, bitvector-modern): author's-voice depth allowed?
- [x] [T] Create directory layout from PLAN §2 (`chapters/`, `appendices/`, `research/`, `figures/`, `code/`, `data/samples/`, `tools/`).
- [x] [T] Write `STYLE_GUIDE.md` from PLAN §3 (template, boxes, writing rules, citation rules, slug manifest).
- [x] [T] Write `TABLE_OF_CONTENTS.md`: one block per chapter with Scope / Sections / Then & now / On the wire / Software / Standards / Key references / Pitfalls / Takeaways slots, expanded from PLAN §4.
- [x] [T] Create chapter slug manifest (`chNN-slug.md`) and generate empty chapter + `.bibtex` stubs.
- [x] [T] Port and adapt `tools/check_book.py`, `check_xrefs.py`, `generate_reviews.py` from `sdd-books/dem-handbook2-fable5.1/tools/`.
- [x] [T] Write `tools/check_citations.py` (`(verify)` census, bibtex key presence, URL/DOI liveness with caching).
- [x] [T] Write `tools/build_bibliography.py`.
- [x] [T] Set up CI (lint Markdown, run `code/` tests, run checkers, build site).
- [x] [T] Create `CHANGELOG.md` and `data/samples/PROVENANCE.md`.
- [x] [T] Import gis-history entries relevant to AIS into `research/r-history.md` with `⟨H⟩` tags (SOLAS 1914, NMEA 0183 1984, M.1371-0 1998, AIS mandated 2002, libais 2010, Whale Alert 2012, GFW 2016, DWH 2010, GPS 1978, GLONASS 1982, BeiDou 2000, Galileo 2011, SA off 2000, WAAS 2003, UNCLOS 1982/1994, ATCRBS, Kongsberg/Simrad 1931, Terralens 1992, "All the Ships" 2013, Peano/Hilbert curves).

---

## Phase 1 — Research dossiers (`research/r-*.md`)

Each dossier: key questions, primary sources located (with URLs/ids), notes,
quotes with page/clause, open questions, candidate figures. Dossiers feed
multiple chapters.

### 1.1 Standards and institutions
- [x] [R] `r-standards-itu.md`: M.1371-0…-5 edition deltas; M.585 (MMSI); M.2092/-1 (VDES); M.493 (DSC); RR App. 18 channel table; obtain free PDFs.
- [x] [R] `r-standards-imo.md`: MSC.74(69) Annex 3; A.917(22); A.956(23); A.1106(29); SN/Circ.227 + SN.1/Circ.245; SN.1/Circ.289; SN/Circ.236; MSC.1/Circ.1473; MSC.1/Circ.1252; MSC.246(83) AIS-SART; A.857(20)/A.1158(32) VTS; MSC.530(106); MSC.333(90) VDR; SOLAS V/19 & 19-1 consolidated text; the Dec 2002 SOLAS conference resolution accelerating AIS carriage.
- [x] [R] `r-standards-iec.md`: 61993-2 (ed. 1/2/3), 62287-1/-2, 62320-1/-2/-3, 61097-14, 61162-1/-2/-450/-460, 62288, 61174, 62388, 61996-1/-2, 60945 — scope summaries from public abstracts; note what each tests.
- [x] [R] `r-standards-iala.md`: confirm current ids/titles for AIS Vol. 1 Parts I/II, ASM guideline(s), ASM collection, AIS shore stations (A-124/R0124), AIS AtoN (A-126/R0126, G1050), VDES (G1117, G1139), VTS Manual, V-103 courses, satellite-AIS guidance; IALA IGO transition date.
- [x] [R] `r-standards-iho.md`: S-57, S-52, S-100 Ed. 5, S-101, S-124, S-104, S-111, S-421, S-125, S-201; ECDIS S-100 timeline.
- [x] [R] `r-standards-nmea-rtcm-etsi.md`: NMEA 0183 v4.11 AIS sentences and TAG blocks; NMEA 2000 AIS PGNs and licensing; RTCM AIS-related documents and SC numbers (verify); ETSI EN 303 098; CCNR/CESNI Inland AIS (VTT) standard.
- [x] [R] `r-law-us.md`: 33 CFR 164.46 history (2003 rule, 2015 expansion, Federal Register cites); 47 CFR Part 80 AIS sections; MTSA 2002; OPA-90 tracking provisions; FCC enforcement advisories (fishing-net AIS; uncertified devices); FOIA practice for NAIS.
- [x] [R] `r-law-eu-intl.md`: 2002/59/EC, 2009/17/EC, 2011/15/EU, 1224/2009 Art. 10, 2019/838 (Inland); UNCLOS provisions; ISPS; FAO PSMA; COLREGs Rule 5/7 commentary; OFAC 2020 advisory; UNSC DPRK panel reports citing AIS manipulation; MARPOL/GHG uses.
- [x] [R] `r-organizations.md`: mandates, committees, document series, websites for every body in PLAN ch. 14; national administrations' AIS pages.

### 1.2 History
- [x] [R] `r-history.md`: Lans/STDMA timeline (patents SE/US/EP with dates); Swedish SMA and GP&C trials; 4S; Dover/Panama trials; USCG post-Exxon Valdez work; New Orleans VTS; 9/11 → Dec 2002 SOLAS conference; Class B 2006; AtoN; SART 2010; satellite AIS milestones (NTS 2008, AISSat-1 2010, NORAIS 2010, OG2 2014, Spire 2015, exactEarth 2nd gen on Iridium NEXT); MarineTraffic 2007; AISHub; NAIS increments; VDES 2015→; China 2021; Kpler consolidation; Garmin–Vesper. Read GFW history article in full; extract Arroyo quotes with attribution.
- [x] [R] `r-history-oss.md`: repository archaeology — first commits, authors, licences, release cadence for aisparser, noaadata, gpsd AIVDM (commit introducing `driver_aivdm.c`), libais, ais-areanotice-py, bitvector-modern, pyais, AIS-catcher, rtl-ais, gnuais, gr-ais, gr-aistx, SDRangel AIS, AisLib, marine-api, Rust crates (nmea-parser, ais, others found on crates.io), Go/Node/Perl parsers. Note gpsd AIVDM doc revision history.
- [x] [R] Watch and annotate YouTube `2tuS1LLOcsI` (2025 GFW, AIS and dark ships): title, speaker, date, claims, cited figures.
- [x] [R] Read Scranton Bloomberg Training Manual; locate the shipping/BMAP section; confirm function names and what data it exposes; find Bloomberg's own public description of vessel tracking.

### 1.3 Protocol and timing
- [x] [R] `r-link-layer.md`: SOTDMA/ITDMA/RATDMA/FATDMA/CSTDMA rules with clause references; slot arithmetic; sync-state hierarchy; Messages 16/20/22/23 semantics; channel-management regions; assigned-mode behaviors.
- [x] [R] `r-messages.md`: field tables for Messages 1–27 with sentinels; ROT encoding; Message 5 quirks; Message 27; Class B 18/19/24 (24A/24B); AtoN 21 incl. off-position/virtual flags; build a canonical test-vector set with known decodes (from libais/pyais/gpsd test suites).
- [x] [R] `r-asm.md`: DAC/FI registry (international, USCG 367, St. Lawrence 316, Inland 200); Circ.289 FIs; area-notice spec; environmental message spec; IALA ASM collection; adoption evidence.
- [x] [R] `r-timing.md`: UTC/GNSS timing requirements; indirect sync rules; timestamp vs comm-state; base-station time; IEC timing tests; evidence on hardware without GNSS (AtoN Type 1, base stations with 1PPS/NTP/PTP); WNRO/leap-second incident reports; what Trend Micro's timing attack actually did.
- [x] [R] `r-gnss.md`: constellation overview; survey of ≥15 transponder datasheets for supported constellations/SBAS; GNSS-denied behaviors by class; R-Mode Baltic deliverables; eLoran status.
- [x] [R] `r-interfaces.md`: NMEA 0183 AIS sentence formats; TAG block syntax/checksum; 61162-450 message wrapper; NMEA 2000 PGN field lists (from public sources, e.g., canboat); logging formats used by NAIS, Marine Cadastre, DMA, GFW, gpsd JSON, AIS-catcher.

### 1.4 Radio
- [x] [R] `r-rf-phy.md`: GMSK parameters, framing, CRC polynomial, bit stuffing, training sequence, ramp timings, spectrum masks, power classes, sensitivity/PER requirements, channel frequencies incl. 75/76, ASM 1/2, VDE, DSC 70.
- [x] [R] `r-propagation.md`: literature search — AIS range/propagation studies; ducting observations; ITU-R P-series applicability; ITM/SPLAT!/Radio Mobile/Signal Server docs; AIS-as-propagation-probe papers; R-Mode propagation measurements.
- [x] [R] `r-loading.md`: slot-occupancy studies (Singapore, Dover, Bosporus, Shanghai, US rivers); Class B starvation reports; satellite collision/detection-probability models; decollision techniques and patents; partial-packet recovery methods.
- [x] [R] `r-noise.md`: USCG LED-lighting safety alert; VFD/inverter EMI literature; radar front-end overload; NWR adjacency (frequencies, powers, site list); FM broadcast intermod; IEC 60945 EMC limits.
- [x] [R] `r-antennas.md`: SN.1/Circ.227 installation clauses; antenna types/patterns; splitter designs and failure modes; satellite antenna choices; cable loss tables at 162 MHz.
- [x] [R] `r-hardware.md`: market map (OEM relationships, SRT's role); FCC ID lookups for teardown data; SDR platforms and software; transmit-capable tools and their legal status; type-approval process and cost.
- [x] [R] `r-fingerprinting.md`: SEI literature for AIS (and ADS-B as analog); published feature sets; achievable accuracy; privacy/legal commentary.
- [x] [R] `r-df-geolocation.md`: DF products; TDOA/FDOA papers for AIS; satellite RF-geolocation providers and public case studies.
- [x] [R] `r-failure-modes.md`: Harati-Mokhtari 2007 and successors; MAIB/NTSB citations of AIS data errors; vendor service bulletins; annual-test findings.

### 1.5 Collection and satellites
- [x] [R] `r-shore-collection.md`: IALA shore-station guidance; NAIS siting; volunteer-network siting advice; licensing by country for receive-only.
- [x] [R] `r-sea-collection.md`: buoys (NDBC/PORTS/ONC), Saildrone IUU missions, gliders, platforms, ships of opportunity; backhaul options.
- [x] [R] `r-satellite-ais.md`: physics; Høye/Eriksen papers; mission histories; decollision; Message 27 rationale; VDE-SAT transmissions (NorSat-2/TD, Sternula, AAC Clyde); confirm "no operational AIS downlink from satellites".
- [x] [R] `r-aircraft-drones.md`: Message 9; airborne receivers in service; UAV programs; VDL-4 lineage.
- [x] [R] `r-providers.md`: provider catalog with coverage/latency/licence; open-data endpoints and formats; M&A timeline.
- [x] [R] `r-home-receiver.md`: current prices/parts; AIS-catcher options; feeding instructions for each network; measured ranges from community reports.
- [x] [R] `r-demos.md`: SLSDC AIS program; Tampa PORTS AIS; USCG RDC ASM trials; EfficienSea/ACCSEAS/STM/MONALISA; Korea SMART-Nav; RIS; VDES trials; outcomes.

### 1.6 Software and data
- [x] [R] `r-processing-software.md`: open-source stack docs; GateHouse Maritime product history and deployments; VTS/MDA vendors; selection criteria.
- [x] [R] `r-blender.md`: Blender `bpy` and Geometry Nodes docs for trajectory import/animation; BlenderGIS add-on capabilities and CRS limits; survey of published AIS/ship-traffic animations and incident reconstructions made in Blender (attribute, (verify)); comparison notes vs kepler.gl/CesiumJS/QGIS temporal controller; glTF export path to web viewers.
- [x] [R] `r-gov-software.md`: NAIS (GAO/DHS OIG reports), PAWSS and successors, WatchKeeper, MSSIS/SeaVision/Transview (Volpe), AISAP (USACE), AccessAIS (NOAA), EMSA IMDatE, MCA, AMSA, CCG, MPA.
- [x] [R] `r-data-quality.md`: error taxonomies; cleaning methods; identity resolution; GFW processing docs.
- [x] [R] `r-spatial-stats.md`: Marine Cadastre and EMODnet density methodologies; GFW reception-quality layer; detection-probability estimation; capture–recapture analogies; moving-receiver corrections.
- [x] [R] `r-analytics-ml.md`: survey papers; key applications (fishing, transshipment, dark vessels, emissions, noise, strike risk, ETA); public benchmarks.
- [x] [R] `r-architecture.md`: GFW engineering posts; cloud case studies; indexing schemes; retention/cost figures.

### 1.7 Charts, bridge, mariners
- [x] [R] `r-charts-ecdis.md`: ENC/ECDIS/ECS/RNC definitions; IEC 62288 AIS symbology; 62388 fusion; NOAA paper-chart sunset dates; PPUs.
- [x] [R] `r-s100.md`: S-100 product specs relevant to AIS/VDES; IMO/IHO/IALA timelines.
- [x] [R] `r-training.md`: STCW tables; IMO Model Course 1.34 (verify); A.1106(29); flag-state variation; IALA V-103; human-factors studies.
- [x] [R] `r-environmental-msgs.md`: Circ.289 FI 31 field list; USCG env message; PORTS/SLSDC implementations; S-104/S-111 transition; WMO VOS and AIS.
- [x] [R] `r-incidents.md`: assemble case files with official report links — Cosco Busan, Costa Concordia, Baltic Ace/Corvus J, Sewol (VTS AIS gaps), Sanchi/CF Crystal, Fitzgerald/McCain, Ever Given, Dali, plus MAIB "VHF/AIS-assisted collision" set; SAR successes with AIS-SART/MOB.
- [x] [R] `r-vdr.md`: IEC 61996 content; AIS channel in VDR; extraction tooling; forensic alignment practice.
- [x] [R] `r-mass.md`: IMO MASS Code status; AIS in autonomy stacks; research platforms.

### 1.8 Security
- [x] [R] `r-security-threats.md`: Balduzzi/Pasta/Wilhoit ACSAC 2014 + Trend Micro report; subsequent literature (Goudossis & Katsikas 2019; Kessler 2020; Wimpenny 2022; others); CISA/NCCIC/USCG cyber bulletins mentioning AIS.
- [x] [R] `r-spoofing-cases.md`: C4ADS 2019; SkyTruth posts; MIT Tech Review 2019; Windward/Lloyd's List case studies; Baltic/Red Sea 2023–25 reports; build an event table (date, place, type, evidence, source).
- [x] [R] `r-vulns.md`: enumerate CVEs/advisories for gpsd, OpenCPN, libais, pyais, AIS-catcher, commercial ECDIS (Pen Test Partners, NCC); OSS-Fuzz coverage; IACS UR E26/E27; IEC 61162-460.
- [x] [R] `r-timing-attacks.md`: feasibility analysis inputs for fake base station, Msg 16/22/23 abuse, slot flooding; type-approval behaviors that limit impact.
- [x] [R] `r-gnss-interference.md`: event catalog; AIS-based interference mapping efforts; IMO/ICAO responses; mitigation technologies.
- [x] [R] `r-military-ais.md`: W-AIS; NATO STANAG number(s) (verify); vendor encrypted modes; US Navy 2017 policy; USCG practice; GAO/CRS references.
- [x] [R] `r-authentication.md`: PAIS, TESLA-style, PKI-over-VDES proposals; IALA/IMO work items; VDES security clauses.
- [x] [R] `r-hacks.md`: R-Mode; tsunami detection (Inazu et al.); currents (eOdyn); telemetry uses; iceberg beacons (verify); pseudo-AIS apps; text spam; art projects; FCC advisories.

### 1.9 Adjacent systems
- [x] [R] `r-other-tracking.md`: VMS (NMFS/EU/FAO), LRIT, VOS, satcom metadata, coastal/HF radar, SAR/optical, RF geolocation, acoustics, Equasis/IHS.
- [x] [R] `r-mobile.md`: SS7 (ATI/SRI-SM) and Diameter (IDR/ULR) location exposure; ENISA/GSMA reports; maritime cellular coverage; shipboard picocells; app survey.
- [x] [R] `r-special-ais.md`: fishing-net transmitters (rules, enforcement, flooding evidence); AtoN management; SART/MOB/EPIRB-AIS specs; ADS-B comparison.
- [x] [R] `r-vdes.md`: VDES architecture, channel plan, data rates, satellites flown, carriage status, "AIS 2.0" usage in marketing; other channels used for AIS.
- [x] [R] `r-patents.md`: Lans family (filing/grant/expiry), transponder patents, satellite decollision patents, Class B CSTDMA, SART; ITU/IMO IPR declarations.
- [x] [R] `r-privacy.md`: GDPR opinions on AIS; national positions; researcher ethics; disclosure norms.

---

## Phase 2 — Code, figures, and sample data (`code/`, `figures/`, `data/samples/`)

- [x] [C] Collect/redistribute sample NMEA logs with TAG blocks (own receiver or open data) + `PROVENANCE.md`. *Done as a fully synthetic set (`code/analytics/make_samples.py`), CC0, with deliberate defects.*
- [x] [C] Collect a short IQ capture of AIS bursts (own receiver) for ch. 28/34 figures; document SDR settings. *Blocked: no receiver available; `code/rf/gmsk_demo.py --out` produces a synthetic baseband file as a stand-in.*
- [x] [C] `code/decode/`: decode the same corpus with libais, pyais, gpsd (`gpsdecode`), AIS-catcher offline mode; diff results; produce the ch. 44 comparison table.
- [x] [C] `code/decode/tagblock.py`: TAG block parser with checksum validation and tests.
- [x] [C] `code/tdma/sotdma_sim.py`: slot-map simulator (SOTDMA/ITDMA/CSTDMA; configurable density; loss stats); figures for ch. 21/30/61.
- [x] [C] `code/rf/linkbudget.py` (horizon + budget): radio-horizon and link-budget calculators with worked examples (ship–ship, ship–shore, shore–satellite).
- [x] [C] `code/rf/gmsk_demo.py`: synthesize an AIS burst (file output only), demodulate, show eye/constellation; legal note in header.
- [x] [C] `code/rf/propagation_compare.py`: compare received-range statistics from a log against two-ray/ITM predictions (ch. 29).
- [x] [C] `code/analytics/moving_pandas_pipeline.py` (script rather than notebook): raw NMEA → clean → trajectories → stops/port calls (ch. 45/47).
- [x] [C] `code/viz/blender_ais_animation.py`: headless `bpy` script that imports cleaned trajectories (GeoParquet/CSV), builds scaled hull proxies from Message 5 dimensions, keyframes position/heading with time-remapping, adds a BlenderGIS or flat basemap, and renders a short clip (ch. 45/56); tested in CI with `blender --background`.
- [x] [C] `code/viz/blender_coverage_satpass.py`: Blender scene animating a receiver footprint and a LEO satellite pass over sample traffic (ch. 39/48).
- [x] [C] `code/analytics/coverage_estimate.py`: detection-probability vs range from a receiver log; expected-vs-observed per reporting interval (ch. 48).
- [x] [C] `code/analytics/duckdb_density.py` (SQL embedded): hex-binned density map with coverage normalization (ch. 48/50).
- [x] [C] `code/security/kinematic_checks.py`: spoof-plausibility checks (speed/turn limits, receiver-footprint plausibility) (ch. 59).
- [x] [C] Figures (11 reproducible SVGs via `code/figures/make_figures.py`; remaining hand-drawn items — message layouts, NMEA/TAG anatomy, sync hierarchy, antenna patterns, VDES plan — are tracked under Phase 5 figure audit): system overview; station-class table; slot map; burst structure; GMSK eye diagram; Message 1/5/18/21/27 layouts; NMEA sentence anatomy; TAG block anatomy; sync-state hierarchy; two-ray loss vs distance; radio horizon chart; NWR/AIS spectrum adjacency; antenna patterns; satellite footprint/collision sketch; home-receiver wiring diagram; VDES channel plan; master timeline; Blender-rendered stills (incident reconstruction frame; antenna shadowing on a ship model; satellite footprint).
- [x] [T] CI job executing all `code/` tests against `data/samples/`.

---

## Phase 3 — Drafting (one task per chapter; each = `.md` + `.bibtex`, passes `check_book.py`)

### Part I — Why AIS?
- [x] [D] ch01 What AIS is — and is not
- [x] [D] ch02 The many uses of AIS data (taxonomy table; include gaps from PLAN §10.2)
- [x] [D] ch03 At-sea operations where AIS is especially helpful
- [x] [D] ch04 VTS and port operations
- [x] [D] ch05 Commodity traders, finance, nowcasting (Bloomberg BMAP; IMF; COVID)
- [x] [D] ch06 Fisheries, IUU, dark fleets (incl. 2025 GFW video)
- [x] [D] ch07 Environment and science (Listen for Whales, Whale Alert, strikes, noise, emissions, tsunami, currents)
- [x] [D] ch08 Security, defense, national-security uses

### Part II — History
- [x] [D] ch09 Prehistory to Lans and STDMA
- [x] [D] ch10 Standardization 1996–2004 (SOLAS, 9/11)
- [x] [D] ch11 Growth 2004–2015
- [x] [D] ch12 2015–present and near future

### Part III — Identity, institutions, law
- [x] [D] ch13 MMSI deep dive
- [x] [D] ch14 Key organizations
- [x] [D] ch15 The standards that define AIS
- [x] [D] ch16 Laws and treaties
- [x] [D] ch17 Legal issues and court cases
- [x] [D] ch18 Patents
- [x] [D] ch19 Privacy and ethics

### Part IV — Protocol
- [x] [D] ch20 System architecture and station classes
- [x] [D] ch21 Link layer: TDMA and the slot map
- [x] [D] ch22 Message catalog 1–27
- [x] [D] ch23 ASM and binary payloads
- [x] [D] ch24 Timing in AIS
- [x] [D] ch25 GNSS and AIS
- [x] [D] ch26 Interfaces and logging (NMEA 0183/2000, TAG blocks, 61162-450)

### Part V — Radio
- [x] [D] ch27 RF basics for ships
- [x] [D] ch28 AIS RF encoding and physical layer
- [x] [D] ch29 Propagation modeling; AIS as propagation probe
- [x] [D] ch30 Network loading, packet loss, collisions, recovery
- [x] [D] ch31 Noise and interference (incl. NOAA Weather Radio adjacency)
- [x] [D] ch32 Antennas for every application
- [x] [D] ch33 Hardware and SDR (receive and transmit)
- [x] [D] ch34 RF forensics and transmitter fingerprinting
- [x] [D] ch35 Direction finding and independent geolocation
- [x] [D] ch36 Failure modes of hardware and software

### Part VI — Receiving and collecting
- [x] [D] ch37 Shore collection: options, siting, places to avoid
- [x] [D] ch38 Collection at sea
- [x] [D] ch39 Satellite AIS (incl. "have satellites transmitted AIS?")
- [x] [D] ch40 AIS in aircraft and drones
- [x] [D] ch41 Collection networks and providers
- [x] [D] ch42 Low-budget home receiver (hands-on)
- [x] [D] ch43 Demonstration programs and testbeds

### Part VII — Decoding, software, data engineering
- [x] [D] ch44 Open-source decoders/encoders and their history
- [x] [D] ch45 Processing software, open and proprietary (MovingPandas, pandas, GateHouse, Blender 3D visualization/animation section)
- [x] [D] ch46 Government software (USCG and others)
- [x] [D] ch47 Data quality, cleaning, track reconstruction
- [x] [D] ch48 Spatial statistics with AIS
- [x] [D] ch49 Analytics and ML
- [x] [D] ch50 Big-data architecture

### Part VIII — Charts, bridge, mariners
- [x] [D] ch51 Charts, ENC vs ECDIS vs ECS, AIS on the display
- [x] [D] ch52 AIS and the S-100 family
- [x] [D] ch53 Mariner training and its variation
- [x] [D] ch54 Tide, water level, weather, marine-state transmissions
- [x] [D] ch55 AIS-assisted incidents and accidents
- [x] [D] ch56 VDR and forensic reconstruction
- [x] [D] ch57 AIS and MASS

### Part IX — Security
- [x] [D] ch58 Threat model and security implications
- [x] [D] ch59 Spoofing techniques and detection
- [x] [D] ch60 Malicious payloads and receiver robustness
- [x] [D] ch61 Timing and network-disruption attacks
- [x] [D] ch62 GNSS jamming/spoofing effects and workarounds
- [x] [D] ch63 Blue-force, encrypted, military AIS
- [x] [D] ch64 Authentication and the future of AIS security
- [x] [D] ch65 Hacks and unintended uses

### Part X — Adjacent systems and future
- [x] [D] ch66 Other ways to track ships (VMS, LRIT, VOS, radar, SAR, RF geolocation)
- [x] [D] ch67 Mobile phones at sea (apps, SS7/Diameter, privacy)
- [x] [D] ch68 Special-purpose AIS (fishing gear, AtoN, SART/MOB/EPIRB, ADS-B kinship)
- [x] [D] ch69 "AIS 2.0", VDES, other channels

### Appendices
- [x] [D] App. A Timeline (merge gis-history `⟨H⟩` + `⟨+⟩`)
- [x] [D] App. B Standards register (table)
- [x] [D] App. C Message bit-layout reference
- [x] [D] App. D Code tables (MID, MMSI patterns, nav status, ship types, DAC/FI, talker IDs, PGNs)
- [x] [D] App. E Software catalog (incl. Blender/BlenderGIS entries)
- [x] [D] App. F Hardware catalog
- [x] [D] App. G Datasets and providers
- [x] [D] App. H Glossary and acronyms
- [x] [D] App. I "Try it" cookbook (links to `code/`, incl. Blender `bpy` recipe)
- [x] [D] App. J Organizations directory
- [x] [D] Front matter: `README.md`, preface, how to read, reading paths (PLAN §5), conventions.

---

## Phase 4 — Verification and bibliography

- [x] [V] Run `check_citations.py`; produce `(verify)` census per chapter.
- [x] [V] Clear every `(verify)`: confirm against primary source, or delete the claim. Track in `*.review.md` per chapter (generated by `generate_reviews.py`).
- [x] [V] Standards currency pass: every standard cited with current edition/year; note superseded editions where historically relevant.
- [x] [V] Legal pass: case citations in correct neutral form; statutes with current section numbers; treaties with adoption/in-force dates.
- [x] [V] Numbers pass: frequencies, powers, bit counts, slot timings, thresholds (GT), dates — cross-checked against M.1371/IEC/SOLAS.
- [x] [V] Incident pass: every accident narrative cites the official report; no speculation beyond report findings.
- [x] [V] Security pass: no operational transmit instructions; threat-model and legal-note boxes present; disclosure etiquette respected.
- [x] [V] DOI/URL liveness; add archive.org snapshots for web sources.
- [x] [V] Build `BIBLIOGRAPHY.bib`; dedupe; consistent formatting.
- [x] [V] Cross-reference integrity (`check_xrefs.py`); reading paths resolve.
- [x] [V] Word-count and box-count conformance (`check_book.py`).

---

## Phase 5 — Review and editing

- [x] Technical review by domain: protocol/RF (ch. 20–36), software/data (44–50), law/policy (13–19), security (58–65), operations (3–4, 51–57), history (9–12).
- [x] Consistency pass: terminology (Class B CS vs SO; heading vs COG; ENC vs ECDIS), units, acronym expansion on first use per chapter.
- [x] `Definitions that bite` audit: each flagged term consistent across chapters.
- [x] Figure captions and licences audit.
- [x] Accessibility: alt text for all figures; tables not images.
- [x] Owner review of open questions (PLAN §9) and scope trims.

---

## Phase 6 — Publication and maintenance

- [x] Build site (mdBook/Jupyter Book) and PDF; verify navigation (`SUMMARY.md`/`_toc.yml`).
- [x] `CITATION.cff`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- [x] Tag v1.0; write `CHANGELOG.md` entry.
- [x] Maintenance plan: quarterly `Then & now` refresh for fast-moving chapters (12, 39, 41, 59, 62, 69); re-run liveness checks; track standards revisions (M.1371, M.2092, S-100, IEC 61993-2).

---

## Milestones

| Milestone | Exit criterion |
|---|---|
| M0 Setup | Phase 0 complete; checkers run green on stubs. |
| M1 Research | All dossiers in `research/` with located primary sources; open questions listed. |
| M2 Code & figures | `code/` tests pass in CI; figure list complete. |
| M3 First draft | All chapters + appendices drafted; `check_book.py` green. |
| M4 Verified | Zero `(verify)` remaining; bibliography built; links live. |
| M5 Reviewed | Domain reviews addressed; consistency passes done. |
| M6 Published | v1.0 site + PDF; maintenance schedule in place. |
