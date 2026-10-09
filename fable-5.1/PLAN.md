# The AIS Handbook — Master Plan

*The maritime Automatic Identification System, from "what is that triangle on my
chartplotter" to the bit timing of a GMSK burst, and from the sinking of the
Titanic to VDES.*

> **Status:** draft 0.1 (planning). Companion backlog: [`TASKS.md`](TASKS.md).
> Conventions follow the sibling handbooks in `sdd-books/` (per-chapter Markdown +
> `.bibtex`, mandatory honesty rule, `(verify)` placeholders, `⟨H⟩` tags for items
> sourced from [schwehr/gis-history](https://github.com/schwehr/gis-history)).

---

## 0. Purpose, audience, scope

**Purpose.** A single, citable reference that explains AIS as a *system*: the
radio physics, the TDMA link layer, the message catalog, the identities, the
standards and law behind it, the hardware and software that produce and consume
it, the people and institutions that depend on it, the ways it fails, the ways it
is attacked, and the many uses (intended and otherwise) that have grown up around
the data. It is explicitly a *handbook*: each chapter must be usable on its own by
a practitioner with a concrete problem.

**Audience.** Mariners and VTS operators; maritime and fisheries regulators;
naval/coast-guard analysts; hydrographers and chart producers; RF and SDR
engineers; software developers writing decoders and pipelines; data scientists
and economists using AIS as a signal; security researchers; journalists and
OSINT practitioners; students. Assume numeracy, not domain jargon. Define terms on
first use.

**Scope.** Basics → deep technical. Everything in the user brief (see the
coverage matrix in §10) plus the gaps identified in §10.2.

**Non-goals.** Not a replacement for ITU-R M.1371 or the IEC test standards; the
book explains and cites them rather than reproducing them. No instructions for
unlicensed transmission. No reproduction of paywalled standards text beyond fair
quotation.

---

## 1. Guiding principles

1. **Honesty over completeness.** Never invent a date, a spec number, a court
   citation, or a paper. If unsure, write `(verify)` and leave it for the
   bibliography pass. It is better to omit a number than to invent one.
2. **Primary sources first.** ITU-R, IMO, IEC, IALA, IHO, NMEA, RTCM, national
   regulations (CFR, EU directives), accident-investigation reports (NTSB, MAIB,
   TSB, DMAIB, BSU), peer-reviewed papers, and the original software repositories.
   Secondary sources (Wikipedia, blogs, vendor pages) are allowed as *pointers*
   but must be backed by a primary source where one exists.
3. **Show the bits.** Where a claim is about the protocol, show the field layout,
   the slot arithmetic, or the NMEA sentence. Where a claim is about radio, show
   the link budget. Where a claim is about data, show the query.
4. **History is evidence.** Every chapter carries a *Then & now* section. Items
   taken from gis-history are tagged `⟨H⟩`; items added for this book are `⟨+⟩`.
5. **Open-source first, proprietary named.** Prefer runnable examples with open
   tools (libais, pyais, gpsd, AIS-catcher, GNU Radio, MovingPandas, DuckDB,
   PostGIS, QGIS). Name commercial systems accurately and neutrally.
6. **Data quality and RF reality are the spine.** Every chapter has a mandatory
   *Validation, uncertainty & data quality* section: what can go wrong in this
   chapter's subject, how to detect it, and what to report.
7. **Security and legality are not an afterthought.** Chapters that touch
   transmission or exploitation carry a *Threat model* and *Legal note* box.

---

## 2. Deliverables and repository layout

```
ais/fable/
├── PLAN.md                     ← this document
├── TASKS.md                    ← phased backlog with checkboxes
├── README.md                   ← how to build, contribute, license
├── STYLE_GUIDE.md              ← chapter template, boxes, citation rules (§3)
├── TABLE_OF_CONTENTS.md        ← detailed per-chapter blocks (expanded from §4)
├── LICENSE                     ← CC-BY-4.0 for prose; code snippets Apache-2.0 (verify choice with owner)
├── chapters/
│   ├── ch01-what-ais-is.md
│   ├── ch01-what-ais-is.bibtex
│   └── ...                     ← one .md + one .bibtex per chapter
├── appendices/
│   ├── appendix-a-timeline.md
│   └── ...
├── research/                   ← per-topic dossiers written before drafting
│   ├── r-history.md
│   ├── r-security.md
│   └── ...
├── figures/                    ← SVG/PNG; one subfolder per chapter
├── code/                       ← runnable "Try it" snippets, tested in CI
│   ├── decode/                 ← libais, pyais, gpsd examples
│   ├── rf/                     ← link budget, radio horizon, GMSK demo
│   ├── tdma/                   ← SOTDMA slot simulator
│   └── analytics/              ← MovingPandas, DuckDB, coverage estimation
├── data/samples/               ← small, redistributable NMEA/IQ samples with provenance
├── tools/
│   ├── check_book.py           ← structure/word-count/box-count checks
│   ├── check_xrefs.py          ← cross-reference and relative-link integrity
│   ├── check_citations.py      ← (verify) census; DOI/URL liveness
│   ├── build_bibliography.py   ← merge per-chapter .bibtex → BIBLIOGRAPHY.bib
│   └── generate_reviews.py     ← emits *.review.md audit stubs per chapter
└── SUMMARY.md / _toc.yml       ← mdBook / Jupyter Book navigation (choose one; see §8)
```

**Chapter size target:** 3,500–7,000 words; 2–6 recurring boxes; ≥ 10 references.
Deep-technical chapters (link layer, RF encoding, message catalog) may run longer
if split into numbered subsections.

---

## 3. Style conventions (summary; full text goes in `STYLE_GUIDE.md`)

### 3.1 Chapter template (top-level headings in this order)

```markdown
# Chapter N — Title
> **Part X — Part title.** One-sentence placement.
**In this chapter.** 120–180-word abstract: what the reader will be able to do.
## N.1 … numbered sections following the TOC block …
## Then & now            ← ⟨H⟩ for gis-history items, ⟨+⟩ for new
## On the wire           ← only where the chapter touches protocol/RF: bit layouts, sentences, slot math
## Validation, uncertainty & data quality     ← MANDATORY
## Software              ← Open source / Free-closed / Commercial, one caveat each
## Standards & guides    ← issuer, document id, edition/year, what it governs here
## Pitfalls              ← 8–15 bullets: mistake → why → how to detect/avoid
## Key takeaways         ← 6–10 bullets
## References            ← full citations; DOI only if confident; "(verify)" otherwise
```

### 3.2 Recurring boxes (blockquote with bold label)

- `> **Case file.**` — a sourced real incident (accident report, court case, paper).
- `> **On the wire.**` — a short hex/bit/NMEA walk-through.
- `> **Try it.**` — runnable snippet (Python/Rust/C++/CLI) with expected output.
- `> **Worked example.**` — numeric example with arithmetic shown (link budget,
  slot arithmetic, detection probability).
- `> **Definitions that bite.**` — a term with conflicting definitions
  (e.g., "heading" vs "COG", "Class B" vs "Class B+", "ECDIS" vs "ECS").
- `> **Threat model.**` — attacker, capability, impact, mitigation (security-touching
  chapters only).
- `> **Legal note.**` — what is lawful where (transmission, data use, privacy).
- `> **Rule of thumb.**` — heuristic with limits of validity.

### 3.3 Writing rules

- Direct, concrete, second person acceptable. No marketing language.
- Units: SI first; nautical miles (nmi), knots (kn), feet for antenna height only
  where a standard uses them. Frequencies in MHz; power in W and dBm; gain in dBi
  (state dBd if a datasheet uses it).
- Cross-references as relative Markdown links (`[Chapter 21](chapters/ch21-link-layer-tdma.md)`).
- Every chapter ends Pitfalls → Key takeaways → References.
- Accident/incident narrative must cite the official investigation report.

---

## 4. Book skeleton

Sixty-nine chapters in ten parts plus ten appendices. Chapter numbers are
continuous so cross-references stay stable. Each block below gives *Scope*,
*Questions from the brief it answers* (→ §10 matrix), and *Seed sources*
(short form; expanded in `TABLE_OF_CONTENTS.md` and the per-chapter `.bibtex`).

**Ordering rationale.** Uses first (why anyone cares) → history (how we got
here) → identity, institutions, law (the social layer) → the protocol (the
technical core) → radio (the physical layer) → receiving and collecting (building
the sensor network) → decoding, software, data engineering → charts, bridges,
mariners (the human/operational layer) → security → adjacent systems and the
future → appendices.

---

### Part I — Why AIS? Uses and users

**1. What AIS is — and is not**
- Scope: one-page system picture (ship ↔ ship, ship ↔ shore, shore ↔ ship,
  satellite); the three original purposes (collision avoidance, VTS, coastal
  surveillance); what AIS cannot do (not radar, not authenticated, not guaranteed
  delivery); station classes at a glance; the data a ship broadcasts and how
  often; "AIS is a cooperative, unauthenticated, broadcast, self-organized TDMA
  radio network."
- Seeds: ITU-R M.1371-5; IMO Res. A.1106(29); GFW "AIS for Safety and Tracking:
  A Brief History" (Cutlip, 2017); USCG NAVCEN AIS pages.

**2. The many uses of AIS data (a taxonomy)**
- Scope: the brief asked "what are *all* the uses" — build a taxonomy and a
  table: safety of navigation; VTS and port ops; search and rescue; security and
  law enforcement; fisheries management and IUU; environmental protection (ship
  strikes, noise, emissions, spills, invasive species, MPAs); science (currents,
  tsunami, meteorology, acoustics); commerce, finance, insurance, logistics;
  hydrography and chart production (traffic-based survey prioritization, route
  verification); marine spatial planning and offshore energy; cable and pipeline
  protection; journalism/OSINT; humanitarian (migrant rescue coordination);
  education and hobbyist; art and culture. For each: who, what message fields,
  what latency, what quality bar, failure consequences.
- Gaps the brief did not list but must be covered: hydrographic survey planning,
  cable protection, autonomy/MASS, port-call analytics and just-in-time arrival,
  pandemic epidemiology (COVID port closures), insurance and P&I claims, academic
  trajectory-mining benchmarks, GNSS-interference sensing, sea-state and current
  retrieval.
- Seeds: Kroodsma et al. 2018 *Science*; Cerdeiro et al. 2020 IMF WP/20/57;
  Jalkanen et al. 2009 *ACP* (STEAM); Wiley et al. 2011 *Biol. Conserv.*;
  Schwehr & McGillivary 2007 *OCEANS* (DWH-era spill tracking precursor) (verify).

**3. At-sea operations where AIS is especially helpful**
- Scope: pilotage and PPUs; towing and pushing; offshore supply and DP ops;
  anchorage management; STS transfers and bunkering; icebreaker escort and convoy;
  canal and lock transits; fishing and gear marking; dredging and survey ops;
  cable laying and seismic; diving and ROV ops; yacht racing (Vendée Globe, Sydney–
  Hobart); naval formation keeping; SAR datum marking; bridge-to-bridge calling
  *by name* (the single most under-appreciated use).
- Seeds: IMO A.1106(29); IALA G1028/G1029 (verify ids); MAIB/NTSB reports on
  VHF-assisted collisions; race notices of race requiring AIS.

**4. Vessel Traffic Services and port operations**
- Scope: what a VTS is (IMO Res. A.857(20) → A.1158(32)); INS/TOS/NAS service
  levels; how AIS replaced/augmented radar and voice; traffic image fusion;
  AIS-based reporting (replacing mandatory voice reports); VTS operator training
  (IALA V-103); case: New Orleans as the first AIS-centric US VTS; PAWSS; VTMIS in
  the EU (SafeSeaNet); port community systems; berth and pilot dispatch.
- Seeds: IALA VTS Manual; IMO A.1158(32); USCG PAWSS documentation (verify);
  GFW history article (New Orleans 1998 plan).

**5. Commodity traders, finance, and economic nowcasting**
- Scope: tanker tracking and floating storage; draught (Message 5) as a cargo
  proxy; destination/ETA as flow predictors; grain, LNG, crude, products; the
  Bloomberg terminal ship-tracking function (BMAP) and the Scranton Bloomberg
  training manual as a teaching artifact; Reuters/LSEG, Kpler, Vortexa,
  ClipperData, Windward, Lloyd's List Intelligence, S&P Global Maritime, Signal
  Ocean, VesselsValue; hedge funds and alternative data; IMF/World Bank/UN
  nowcasting (PortWatch, UN Global Platform AIS); COVID-19 shipping shock;
  limitations (spoofing for sanctions, draught not updated, satellite latency).
- Seeds: Scranton Bloomberg Training Manual (PDF, as supplied); Arslanalp, Marini
  & Tumbarello 2019 IMF WP/19/275; Cerdeiro et al. 2020; Verschuur, Koks & Hall
  2021 (verify venue); IMF PortWatch methodology notes.

**6. Fisheries, IUU fishing, and dark fleets**
- Scope: fishing effort from AIS (CNN classifiers), transshipment detection,
  "AIS gaps" and intentional disabling, dark-vessel detection with SAR/optical
  (Sentinel-1, Paolo et al. 2024), VMS vs AIS, EU >15 m requirement, Chinese
  distant-water fleet, squid fleets, the 2025 GFW talk on AIS and dark ships
  (YouTube 2tuS1LLOcsI — confirm title/speaker), Joint Analytical Cell.
- Seeds: Kroodsma et al. 2018; Paolo et al. 2024 *Nature*; Welch et al. 2022
  *Sci. Adv.* (AIS disabling) (verify); GFW technical docs; EU Reg. 1224/2009
  Art. 10.

**7. Environment and science: Whale Alert, ship strikes, noise, emissions, tsunamis, currents**
- Scope: Listen for Whales / right-whale auto-detection buoys in the Boston TSS
  (Cornell BRP, Excelerate Energy); the AIS binary message for right whales and
  the Whale Alert app (2012; NOAA/IFAW/EarthNC/Conserve.IO; presented to
  Congress ⟨H⟩); Boston TSS shift (2007) and ATBAs; Whale Safe (2020, Santa
  Barbara); speed-rule compliance monitoring; underwater noise maps; emissions
  inventories (IMO GHG studies, STEAM); AIS-derived tsunami detection (Inazu et
  al.) and surface currents (eOdyn) (verify); oil-spill response (DWH 2010 ⟨H⟩).
- Seeds: Wiley et al. 2011; Silber et al. 2012; Schwehr et al. RWAISP reports
  (verify); IMO Fourth GHG Study 2020; Inazu et al. 2016/2018 (verify); Guichoux
  et al. 2016 (verify).

**8. Security, defense, and national-security uses**
- Scope: Maritime Domain Awareness after 9/11; MTSA 2002; NAIS; sanctions
  enforcement (OFAC May 2020 advisory; UN DPRK Panel of Experts); shadow fleets
  (Russia/Iran/Venezuela); naval use and non-use (SOLAS "master may switch off");
  USS *Fitzgerald*/*McCain* 2017 and the Navy's AIS policy change; China's 2021
  data-security law and the collapse of terrestrial feeds; export control of AIS
  data; wartime AIS (Black Sea 2022–); AIS in intelligence fusion.
- Seeds: OFAC/State/USCG Sanctions Advisory (14 May 2020); UNSC S/2019/171 etc.
  (verify); Reuters Nov 2021 on Chinese AIS data; US Navy OPNAV messages 2017
  (verify); C4ADS 2019 *Above Us Only Stars*.

---

### Part II — History

**9. Prehistory: radio, radar, transponders, and the road to a mandate**
- Scope: Titanic (1912) → SOLAS 1914 ⟨H⟩; radio and radar at sea; IFF and
  aviation transponders (ATCRBS ⟨H⟩); racons; Exxon Valdez (1989) → OPA-90 →
  USCG tanker tracking; Dover Strait VHF trials; Panama Canal UHF; Håkan Lans and
  STDMA (Swedish patent 1989; US 5,506,587); Swedish Maritime Administration /
  GP&C trials; "4S" ship–ship/ship–shore transponders; Finland, Germany; VDL
  Mode 4 and the aviation parallel; DGPS beacons as the first digital maritime
  data broadcast.
- Seeds: GFW history article (Arroyo interview); Lans patents; Swedish SMA
  reports (verify); IALA history pages; Wikipedia AIS history as pointer.

**10. Standardization 1996–2004**
- Scope: IMO MSC.74(69) Annex 3 performance standard (May 1998); ITU-R M.1371-0
  (Nov 1998 ⟨H⟩); IEC 61993-2 Ed.1 (2001); SOLAS Ch. V revision (adopted Dec 2000,
  in force 1 Jul 2002 ⟨H⟩); carriage thresholds (300 GT international, 500 GT
  domestic, all passenger ships); 9/11 and the Dec 2002 SOLAS conference
  accelerating carriage to 31 Dec 2004; US MTSA 2002; EU Directive 2002/59/EC;
  IMO A.917(22) guidelines (2001); SN/Circ.227 installation guidance (2003).
- Seeds: IMO documents by number; ITU recommendation pages; Federal Register
  rulemakings (USCG 2003 AIS rule).

**11. Growth 2004–2015**
- Scope: Class B (IEC 62287-1, 2006) and the recreational market; AIS AtoN and
  virtual AtoN; AIS-SART (2010); Inland AIS (CCNR VTT 2006; EU 415/2007);
  M.1371-1/-2/-3/-4 and Message 27 long-range; satellite AIS (NTS/EV-0 2008,
  AISSat-1 2010, NORAIS on ISS 2010, ORBCOMM OG2 2014, Spire 2015); shore networks
  (USCG NAIS; EMSA SafeSeaNet; HELCOM; AMSA); crowdsourcing (MarineTraffic 2007,
  AISHub); open-source decoders (aisparser, noaadata, gpsd, libais 2010 ⟨H⟩);
  ASM policy (SN.1/Circ.289, 2010; MSC.1/Circ.1473, 2014); Whale Alert 2012 ⟨H⟩;
  Costa Concordia 2012; Sewol 2014; the 2013 Trend Micro findings.
- Seeds: as named; Høye et al. 2008 *Acta Astronautica*; Eriksen et al. 2006.

**12. 2015–present and the near future**
- Scope: US AIS rule expansion (2015/2016, 33 CFR 164.46); GFW launch 2016 ⟨H⟩;
  VDES (M.2092, 2015; WRC-15/19/23); GNSS interference era (Black Sea 2017,
  Shanghai 2019, Baltic/Red Sea 2023–); IMO A.1106(29) 2015; S-100 Ed. 5 and
  MSC.530(106); IALA becomes an IGO (2024 (verify)); market consolidation (Garmin–
  Vesper 2022; Kpler–MarineTraffic/FleetMon 2023; Kpler–Spire Maritime 2024/25
  (verify)); China feed collapse 2021; MASS; R-Mode; "AIS 2.0" talk.
- Seeds: Federal Register 80 FR 5282 (2015) (verify); ITU-R M.2092-1; IALA
  convention entry-into-force notice; company press releases.

---

### Part III — Identity, institutions, law

**13. What is an MMSI? A deep dive**
- Scope: ITU-R M.585 structure; MID allocation and regional first digits; ship
  (MIDxxxxxx), group (0MID…), coast station (00MID…), SAR aircraft (111MID…),
  AtoN (99MID…), craft associated with parent (98MID…), handheld DSC (8MID…),
  AIS-SART (970…), MOB (972…), EPIRB-AIS (974…); national assignment (FCC ship
  station licence vs. recreational issuers in the US; other administrations);
  ITU MARS database; MMSI reuse and recycling; invalid and default MMSIs (all
  zeros, 1193046, 123456789, repeated digits); MMSI vs IMO number (check-digit
  algorithm) vs call sign vs ENI vs vessel name; identity fraud and "MMSI
  laundering"; privacy of MMSI registries.
- Seeds: ITU-R M.585-9 (verify edition); 47 CFR 80; ITU MARS; Equasis; IHS
  numbering scheme.

**14. Key organizations and what they do**
- Scope: IMO (MSC, NCSR; former NAV/COMSAR), ITU (ITU-R WP 5B; Radio
  Regulations App. 18), IALA (ENAV, VTS, ARM committees; becoming an IGO), IHO
  (S-100 WG, HSSC), IEC TC 80, RTCM (SC 121 et al. (verify)), NMEA, ETSI, CIRM,
  WMO (VOS), ICAO (VDL-4), NATO; national: USCG (NAVCEN, RDC, VTS), FCC, NOAA
  (OCS, NMFS OLE, Marine Cadastre, NDBC/PORTS), BOEM, USACE, DOT Volpe, US Navy;
  EMSA, EU DG MOVE/MARE, CCNR/CESNI; DMA (Denmark), Kystverket (Norway),
  Sjöfartsverket (Sweden), Traficom (Finland), MCA (UK), AMSA, MPA Singapore,
  JCG/MLIT (Japan), MSA (China), CCG/Transport Canada; NGOs: GFW, SkyTruth,
  Oceana, Pew; academic/lab centers (UNH CCOM, DLR, FFI, MIT LL, NPS).
- Seeds: organization charters and terms of reference; IALA Convention text.

**15. The standards that define AIS (narrative; full register in Appendix B)**
- Scope: how the documents fit together — IMO performance standard → ITU-R
  technical characteristics → IEC test standards → IALA guidance → NMEA/IEC
  interfaces → national type-approval (FCC Part 80, EU MED "wheelmark"); edition
  history; how to read a standard; where to buy/obtain; what is free.
- Seeds: M.1371-5; MSC.74(69); IEC 61993-2, 62287-1/-2, 62320-1/-2/-3, 61097-14,
  61162-1/-2/-450/-460, 62288, 61174, 62388; IALA G1028/G1029/G1082/G1117/G1139,
  R0124/R0126 (verify ids); NMEA 0183 v4.11; NMEA 2000; RTCM AIS-related
  standards (verify); ETSI EN 303 098 (MOB AIS).

**16. Laws and treaties**
- Scope: SOLAS Ch. V Reg. 19.2.4 (carriage) and 19-1 (LRIT); COLREGs 1972 (Rule 5
  and Rule 7 — AIS as "all available means", not a substitute for radar); STCW;
  ITU Radio Regulations (App. 18, Art. 19 identities); UNCLOS (flag state, EEZ,
  innocent passage, AIS switch-off debates); ISPS Code; MTSA 2002; 33 CFR 164.46;
  47 CFR 80.231/80.275 (verify sections); EU 2002/59/EC, 2009/17/EC, 2011/15/EU,
  1224/2009; Inland: EU 2019/838 (verify); FAO PSMA; MARPOL (AIS-based emission
  monitoring); sanctions law (OFAC, UNSCRs on DPRK AIS manipulation); Polar Code.
- Seeds: treaty texts; eCFR; EUR-Lex.

**17. Legal issues and court cases around AIS**
- Scope: (a) Lans/GP&C STDMA patent and the IMO/ITU royalty-free condition;
  Lans's US litigation history and its chilling lesson (verify details);
  (b) collision litigation where AIS/VDR was decisive — *Ever Smart v Alexandra 1*
  [2021] UKSC 6; *Cosco Busan* (2007); *Sanchi/CF Crystal* (2018); *Dali*/Key
  Bridge (2024); (c) *Sewol* (2014) and the disputed VTS AIS recording gaps;
  (d) criminal/sanctions cases relying on AIS manipulation evidence (e.g., M/T
  *Courageous* DPRK case, DOJ 2021–23 (verify)); (e) "AIS off" as evidence in
  IUU prosecutions; (f) admissibility and chain of custody of AIS data;
  (g) data ownership, terms of service, scraping disputes (MarineTraffic etc.);
  (h) GDPR and small-craft owners; (i) FOIA for NAIS data; (j) liability when AIS
  data is wrong.
- Seeds: judgments (BAILII, PACER), NTSB/MAIB/KMST reports, DOJ press releases;
  law-review articles on AIS evidence (verify).

**18. Patents**
- Scope: Lans US 5,506,587 "Position indicating system" (STDMA) and family —
  filing/grant/expiry (verify); Saab/Kongsberg/SRT transponder patents; CSTDMA
  for Class B; satellite-AIS decollision patents (COM DEV/exactEarth, ORBCOMM);
  AIS-SART; antenna splitters; what is expired, what is live; how IMO/ITU handle
  IPR declarations.
- Seeds: Google Patents, USPTO PAIR, EPO; ITU IPR database.

**19. Privacy and ethics**
- Scope: AIS as mandated public self-surveillance; crews, fishers, yacht owners;
  data brokers; de-identification (does not work for ships); Chinese and Russian
  data restrictions as privacy/sovereignty arguments; researcher obligations;
  responsible disclosure for security findings; publishing spoofing evidence.
- Seeds: GDPR opinions (verify), academic ethics literature, GFW data principles.

---

### Part IV — The system: architecture and protocol

**20. System architecture and station classes**
- Scope: Class A; Class B "CS" (CSTDMA) and Class B "SO" (SOTDMA, "B+"); base
  stations and limited base stations; simplex/duplex repeaters; AIS AtoN Types 1,
  2, 3 (real, synthetic, virtual); AIS-SART, MOB, EPIRB-AIS; SAR aircraft;
  Inland AIS; pilot plug; shore network reference architecture (IALA R0124);
  reporting intervals table by class and dynamics; power classes.
- Seeds: M.1371-5 Annexes; IEC family; IALA R0124/R0126; IALA G1050 (verify).

**21. The link layer: TDMA and the slot map**
- Scope: 2,250 slots/min/channel; 26.67 ms slots; 256 bits; SOTDMA (candidate
  slots, slot timeout, slot offset, nominal increment), ITDMA, RATDMA, FATDMA,
  CSTDMA (carrier sense, 1,111-bit window (verify)); communication state fields
  and sync state (UTC direct/indirect/base/number of stations); channel access
  under load; dual-channel alternation; channel management (Message 22) and
  regional operating areas; assigned mode (Messages 16/23); slot reuse distance;
  simulations.
- Seeds: M.1371-5 Annex 2; Lans patent; IALA G1029 (verify); academic
  simulations (e.g., Gaugue? (verify)); open-source SOTDMA simulators.

**22. The message catalog (Messages 1–27)**
- Scope: field-by-field semantics with units and "not available" sentinels;
  position encoding (1/10,000 min), ROT (4.733√ROT encoding), SOG/COG/heading,
  nav status, timestamp semantics (60/61/62/63), RAIM, position-accuracy flag,
  Message 5 (424 bits, two slots, ETA/destination free text, dimensions and
  reference point), Messages 6/8 binary, 7/13 acks, 9 SAR aircraft, 10/11 UTC,
  12/14 safety text, 15 interrogation, 16/23 assignment, 17 DGNSS, 18/19/24
  Class B, 20 data-link management, 21 AtoN, 22 channel management, 25/26
  single/multiple-slot binary, 27 long-range; bit-exact worked decodes.
- Seeds: M.1371-5 Annex 8; gpsd "AIVDM/AIVDO protocol decoding" (Raymond &
  Schwehr); libais/pyais test vectors.

**23. Application-specific messages (ASM) and binary payloads**
- Scope: DAC/FI addressing; IMO SN.1/Circ.289 (2010) international FIs
  (meteorological & hydrographic, dangerous cargo, tidal window, number of
  persons, berthing data, area notice, route information, text description,
  environmental); IMO SN/Circ.236 legacy; IALA ASM Collection (R0124?/G1082
  (verify)); regional: USCG DAC 367 (environmental FI 33 etc.), St. Lawrence
  Seaway DAC 316, EU Inland DAC 200; Messages 12/14 text (and spam); Message 17
  DGNSS corrections; design rules; the `ais-area-notice` library as reference
  implementation; the ASM policy (MSC.1/Circ.1473).
- Seeds: IMO circulars; IALA ASM pages; USCG RDC ASM specs; `schwehr/ais-areanotice-py`.

**24. Timing in AIS**
- Scope: UTC from the internal GNSS drives slot timing; direct vs indirect sync;
  base-station sync and "semaphore" stations; sync-state hierarchy; timestamp
  field vs comm-state UTC hour/minute; Messages 4 and 11; what the IEC tests
  require (internal GNSS mandatory even if external EPFS used); hardware without
  GNSS (receive-only; AtoN Type 1 FATDMA (verify); base stations with 1PPS/
  NTP/PTP); how timing degrades (holdover, drift) and when a station must stop
  transmitting; whether messing with timing can collapse a cell (fake base
  station time, Message 23 quiet-time, Message 16 assignment); real-world
  evidence; leap seconds and GPS week-number rollover bugs (verify incidents).
- Seeds: M.1371-5 §3.1 timing; IEC 61993-2 timing tests; Balduzzi et al. 2014;
  manufacturer service bulletins on WNRO (verify).

**25. GNSS and AIS**
- Scope: overview of GPS, GLONASS, Galileo, BeiDou, QZSS, NavIC, SBAS (WAAS/
  EGNOS/MSAS/GAGAN), DGNSS beacons and Message 17; what AIS equipment supports
  (M.1371 "EPFS" neutral; IEC 61993-2 requires internal GNSS — which
  constellations in practice, by vendor and generation (verify by datasheet
  survey)); do any AIS systems lack GPS? (receivers, some AtoN, legacy); the
  "position accuracy" flag and RAIM; GNSS-denied behavior (manual input 61, dead
  reckoning 62, inoperative 63; indirect sync; cessation); jamming vs spoofing
  signatures in AIS data; workarounds (eLoran, R-Mode on AIS/VDES/MF beacons,
  radar overlay, inertial, visual).
- Seeds: GPS.gov; ESA Navipedia; IEC 61993-2; R-Mode Baltic reports (DLR);
  Johnson & Swaszek R-Mode feasibility (ACCSEAS 2014) (verify).

**26. Interfaces and logging: NMEA 0183, TAG blocks, IEC 61162-450, NMEA 2000**
- Scope: `!AIVDM`/`!AIVDO` anatomy (talker IDs, fragment count/number, sequential
  id, channel, 6-bit payload, fill bits, checksum); multi-sentence reassembly
  hazards; other AIS sentences (ABM, BBM, ABK, ACA, ACS, AIR, LRF/LRI, SSD, VSD,
  TXT, ALR); NMEA 4.10 TAG blocks (`\s:,c:,n:,g:,d:,r:\`) and their checksums;
  IEC 61162-1/-2 electrical; 61162-450 UDP multicast and 61162-460 security
  gateways; NMEA 2000 AIS PGNs (129038/129039/129040/129041/129793/129794/
  129798/129801/129802/129809/129810) and licensing; OneNet; SignalK; logging
  formats in the wild (timestamp suffix, TAG block, gpsd JSON, NAIS, Marine
  Cadastre CSV, DMA CSV, Parquet); best practices (UTC, receiver id, keep raw).
- Seeds: NMEA 0183 v4.11; gpsd docs; IEC 61162 family; NMEA 2000 PGN list.

---

### Part V — Radio

**27. RF basics for ships**
- Scope: the marine VHF band (156–162 MHz) and App. 18 channel plan; wavelength
  (~1.85 m) and antenna size; dB, dBm, dBi/dBd; line of sight and the 4/3-Earth
  radio horizon (`d ≈ 4.12(√h₁+√h₂)` km); free-space and two-ray loss; sea
  reflection; noise floor and receiver sensitivity (−107 dBm typical for 20 %
  PER (verify)); coax loss at 162 MHz by cable type; VSWR; lightning; link
  budget worked examples for ship–ship, ship–shore, shore–satellite.
- Seeds: ITU-R P.525/P.526/P.1546/P.2001; ARRL Antenna Book; IEC 61993-2
  sensitivity requirement.

**28. AIS RF encoding and the physical layer**
- Scope: GMSK (BT 0.4 Tx / 0.5 Rx, h = 0.5), 9,600 bit/s, NRZI, HDLC framing
  (flags 0x7E, bit stuffing), 24-bit training sequence, 16-bit CRC-CCITT, 8-bit
  ramp-up, buffer bits; 25 kHz channel; power levels (12.5 W/1 W Class A; 2 W
  Class B CS; 5 W Class B SO; 1 W SART); frequency tolerance; spectrum mask;
  channel plan (AIS 1 161.975 / AIS 2 162.025; 75/76 for Message 27; ASM 1/2
  161.950/162.000; VDE channels (verify numbers)); transmitter switching times;
  receiver co-channel/adjacent rejection; bit-exact example of a burst from IQ.
- Seeds: M.1371-5 Annex 2; ITU-R M.2092-1; GNU Radio `gr-ais` source;
  AIS-catcher demodulator notes.

**29. Propagation modeling and AIS as a propagation probe**
- Scope: two-ray over sea with tides and sea state; ducting and anomalous
  propagation (observed 500+ km receptions); ITU-R P.1546/P.2001/P.526
  implementations; Longley–Rice/ITM, SPLAT!, Radio Mobile, Signal Server; antenna
  height sensitivity; using received AIS (known Tx position/power) to validate
  propagation models and monitor ducting in near-real time; coverage maps from
  message density; studies of AIS range statistics; shadowing by terrain and
  structures.
- Seeds: ITU-R P-series; Hufford ITM; published AIS propagation papers (e.g.,
  Sturm? Lessing? (verify names)); R-Mode Baltic propagation measurements.

**30. Network loading, packet loss, and collisions**
- Scope: capacity vs. reporting intervals; slot occupancy measurements (Singapore
  Strait, Dover, Bosporus, Shanghai, Mississippi); Class B CS starvation; link-
  management via Message 20; satellite footprint collision problem and detection
  probability vs. density; what survives corruption (partial decode, CRC-fail
  statistics, soft-decision decoding, successive interference cancellation,
  multi-receiver diversity combining, Doppler separation); building a packet-loss
  model; how shore networks dedupe and how satellites decollide.
- Seeds: Høye et al. 2008; satellite-AIS decollision patents; studies of AIS
  loading (e.g., Lázaro et al. 2019 *Ocean Eng.* (verify)); USCG RDC capacity
  reports (verify).

**31. Noise and interference sources, aboard and ashore**
- Scope: LED navigation lights (USCG Marine Safety Alert 2018 (verify)), VFDs
  and inverters, battery chargers, switch-mode supplies, radar (S/X-band
  front-end overload, harmonics, pulse desense), other VHF (DSC, voice),
  Inmarsat/VSAT, FM broadcast intermodulation, pagers and public-safety
  repeaters, NOAA Weather Radio (162.400–162.550 MHz, 1 kW, adjacent to AIS 2),
  cellular sites, power lines; measurement methods (spectrum analyzer, SDR
  waterfall); mitigation (filters, cavity duplexers, LNA placement, grounding,
  cable routing, antenna separation).
- Seeds: USCG safety alerts; NOAA NWR specs; FCC Part 15/18; IEC 60945 EMC.

**32. Antennas for every application**
- Scope: half-wave dipole, 5/8-wave collinear, ground-plane, J-pole, Yagi for
  shore; gain vs. pattern vs. roll (why high-gain whips are bad on small boats);
  tuning for 162 MHz vs. 156 MHz voice; splitters (and their failure modes);
  installation per SN.1/Circ.227 (separation, height, masking); large ships
  (mast top, radar beam avoidance), small craft (masthead vs. rail), very small
  devices (SART/MOB/AtoN chip and helical antennas), shore stations (height vs.
  sector coverage), satellites (circular polarization choices); testing with a
  VNA; cable choice.
- Seeds: SN.1/Circ.227 as amended; manufacturer datasheets; ARRL; IALA G1050.

**33. Hardware and SDR for receive and transmit**
- Scope: transponder market and OEMs (SRT Marine's role as OEM for many brands;
  Saab, Kongsberg, Furuno, JRC, em-trak, Vesper/Garmin, Digital Yacht, Comar,
  AMEC, Icom, Raymarine, McMurdo, Ocean Signal, Weatherdock, True Heading, Si-Tex,
  ACR, L3Harris, Simrad/B&G); dedicated receivers (dAISy, Quark-elec, Comar,
  Shine Micro, SLR series); SDR receive (RTL-SDR, Airspy, SDRplay, HackRF,
  LimeSDR, USRP, PlutoSDR) and software (AIS-catcher, rtl-ais, gnuais, SDRangel,
  gr-ais); SDR transmit (gr-aistx, SDRangel modulator) with a firm legal note;
  type approval and what it costs; teardown notes.
- Seeds: vendor sites; FCC ID database; project READMEs; Balduzzi et al. 2014.

**34. RF forensics and transmitter fingerprinting**
- Scope: capturing IQ around a burst; measuring slot timing offset, frequency
  offset, ramp-up/down shapes, modulation index and BT deviations, power
  stability, bit-stuffing/encoding quirks, undocumented fields, comm-state
  habits; Specific Emitter Identification literature applied to AIS; can you
  tell a manufacturer? a specific unit? (what is published; what is plausible;
  what is unproven); protocol-level fingerprints (message mix, timing of
  Message 5, Class B static report cadence, NMEA quirks); privacy and legal
  implications; a reproducible lab protocol.
- Seeds: SEI/RF-fingerprinting papers on AIS and ADS-B (verify specific AIS
  papers); GNU Radio flowgraphs; FCC test reports.

**35. Direction finding and independent geolocation**
- Scope: shipboard/shore DF for SAR (RHOTHETA RT-500-M, Rohde & Schwarz DDF);
  TDOA/FDOA multi-receiver geolocation of AIS bursts (Papi et al. 2015 (verify));
  satellite RF geolocation (HawkEye 360, Unseenlabs, Kleos) that locates the
  transmitter regardless of claimed position; range-ring checks from receiver
  coverage; AIS + radar correlation; using DF to catch spoofers and relocate
  misreporting AtoNs.
- Seeds: vendor docs; IET RSN papers; HawkEye 360 publications.

**36. Failure modes of AIS hardware and software**
- Scope: a catalog with detection signatures — GNSS loss; antenna/feeder faults
  (VSWR alarms); misconfiguration (MMSI zeros/defaults, wrong dimensions, wrong
  reference point, stale destination/ETA, nav status never changed); heading
  sensor absent (511) or wrong; ROT sensor issues; Class B slot starvation;
  firmware date bugs (WNRO 2019 (verify)); power supply brownouts; transmit
  inhibit/"silent mode" left on; pilot-plug damage; NMEA multiplexer drops and
  fragment reassembly errors; receiver desense during own transmit; duplicate
  and out-of-order delivery in shore networks; satellite latency and
  time-ordering; software crashes on malformed input; annual testing
  (MSC.1/Circ.1252) and what it catches.
- Seeds: Harati-Mokhtari et al. 2007 *J. Navig.*; USCG/MCA notices; MAIB
  reports; vendor bulletins.

---

### Part VI — Receiving and collecting

**37. Shore collection: options, siting, and places to avoid**
- Scope: towers, lighthouses and ATON structures, tall buildings, universities,
  volunteers' homes; siting survey (horizon profile, noise survey, power,
  network, access, lightning); places to avoid — near high-power radar (ATC,
  weather, military), NOAA Weather Radio transmitters, FM broadcast, paging and
  cellular colocations, high-voltage switchyards; licensing (receive-only vs.
  base station); coverage prediction before installation; maintenance.
- Seeds: IALA R0124; USCG NAIS siting notes (verify); AIS-catcher community
  wiki; chapters 29/31.

**38. Collection at sea: buoys, ASVs, gliders, platforms, ships of opportunity**
- Scope: AIS receivers on NDBC/PORTS and research buoys; Saildrone and other
  ASVs for IUU patrol; gliders (surface-only); offshore wind and oil platforms;
  ferries and research vessels as mobile receivers; aircraft; power, data
  backhaul (Iridium, cellular, VDES-SAT future), antenna height limits, motion
  effects; moving-receiver bias in later statistics (→ ch. 48).
- Seeds: Saildrone/NOAA publications; ONC; MBARI; NDBC.

**39. Satellite AIS: how satellites receive and process AIS**
- Scope: footprint geometry (~5,000 km diameter at LEO), Doppler (±4 kHz
  (verify)), path loss, antenna choices, the message-collision problem and
  detection probability by density; Message 27 and long-range channels; on-board
  vs. ground decoding; decollision techniques (Doppler/time/space separation,
  SIC, beamforming); history (NTS/EV-0 2008, AISSat-1 2010, NORAIS/ISS 2010,
  ORBCOMM OG2 2014, Spire 2015–, Iridium NEXT hosted exactEarth 2nd gen (verify));
  latency and revisit; **have satellites ever transmitted AIS?** — no operational
  M.1371 downlink; VDE-SAT downlink tests (NorSat-2 2017, NorSat-TD 2023
  (verify)); satellite collection of GNSS-interference evidence.
- Seeds: Høye et al. 2008; Eriksen et al. 2006; Spire/ORBCOMM technical
  papers; ESA SAT-AIS pages; Norwegian Space Agency.

**40. AIS in aircraft and drones**
- Scope: Message 9 SAR aircraft reports; MMSI 111MID; aircraft-mounted
  receivers (USCG HC-130/HC-144, CBP P-3, maritime patrol); UAVs as coverage
  extenders and inspection platforms; balloons/HAPS; ADS-B comparison and
  shared ancestry (VDL Mode 4); altitude/Doppler effects; legal status.
- Seeds: M.1371 Msg 9; ICAO VDL-4 history; USCG aviation docs (verify).

**41. Collection networks and data providers**
- Scope: government (USCG NAIS, EMSA SafeSeaNet/IMDatE, HELCOM, AMSA,
  Kystverket, Traficom, DMA, CCG, JCG); commercial (Spire/exactEarth, ORBCOMM,
  Kpler incl. MarineTraffic & FleetMon, VesselFinder, Windward, Lloyd's List
  Intelligence, S&P, Unseenlabs/HawkEye 360 for RF); crowdsourced (MarineTraffic
  volunteers, AISHub exchange, ShipPlotter history); open data (NOAA/BOEM Marine
  Cadastre, DMA historic files, Norway live feed, Finland Digitraffic, GFW
  datasets/BigQuery, UN Global Platform); licensing terms; latency/coverage
  comparison; consolidation timeline; how to choose.
- Seeds: provider docs; Marine Cadastre methodology; GFW data policy.

**42. A low-budget home AIS receiver (hands-on chapter)**
- Scope: three tiers — (i) RTL-SDR + AIS-catcher + homemade dipole (~US$50);
  (ii) dAISy/Quark-elec dedicated receiver + Raspberry Pi + marine whip + FM
  notch + LNA (~US$200); (iii) dual-channel receiver, filtered preamp, LMR-400,
  roof mast, lightning arrestor (~US$500); step-by-step: antenna build/tune,
  cable, SDR gain, AIS-catcher flags and web UI, feeding MarineTraffic/AISHub/
  VesselFinder, OpenCPN display, logging with TAG blocks, Docker, remote
  monitoring, safety; expected ranges and how to measure them.
- Seeds: AIS-catcher docs (jvde-github); RTL-SDR blog; dAISy docs; OpenCPN.

**43. Demonstration programs and testbeds**
- Scope: St. Lawrence Seaway AIS (2003; lock orders, water levels); Tampa Bay
  PORTS over AIS; USCG RDC ASM trials; Columbia River; Right-whale AIS project;
  EU EfficienSea/ACCSEAS/MONALISA/STM; IALA e-Navigation testbeds; Korea SMART
  Navigation; Inland RIS; VDES trials (Baltic, Norway); lessons on what
  succeeded and what didn't (and why ASM uptake stayed low).
- Seeds: SLSDC reports; NOAA PORTS; EU project deliverables; IALA testbed registry.

---

### Part VII — Decoding, software, and data engineering

**44. Open-source AIS decoding and encoding software: a history**
- Scope: per-project origin, authors, language, licence, design, test corpus,
  quirks, status — aisparser (Brian C. Lane, C, mid-2000s), noaadata-py (Schwehr,
  UNH CCOM, XML-driven codegen, 2006–), gpsd AIVDM support and the "AIVDM/AIVDO
  protocol decoding" document (E. S. Raymond with K. Schwehr, 2009–), libais
  (Schwehr, 2010, for Deepwater Horizon ⟨H⟩; C++ with Python bindings),
  ais-area-notice / ais-areanotice-py (ASM reference), bitvector-modern (verify
  origin/role), pyais (Python, 2019–), AIS-catcher (C++, SDR, 2021–), rtl-ais,
  gnuais/aisdecoder, gr-ais, gr-aistx, SDRangel plugin, Java (DMA AisLib,
  marine-api), Rust (nmea-parser, `ais` crate, others — survey), Go, Node,
  Perl, MATLAB; encoders; conformance testing and shared test vectors; a
  comparison table (messages supported, ASM support, speed, correctness on a
  common corpus).
- Seeds: repositories and commit histories; gpsd docs; mailing-list archives.

**45. Software for processing decoded AIS**
- Scope: open source — pandas, GeoPandas, MovingPandas, Trackintel,
  scikit-mobility, Shapely/GEOS, PostGIS, QGIS (+ plugins), DuckDB spatial,
  Apache Sedona, GeoMesa, kepler.gl/deck.gl, H3/S2, GFW pipelines, searoute,
  OpenCPN; proprietary — GateHouse Maritime (AIS server/aggregator; national
  networks), Kongsberg Norcontrol, Saab TransponderTech, SRT GeoVS, Wärtsilä
  Transas Navi-Harbour, Frequentis, Indra, Terma, Signalis, Esri Maritime,
  Windward, Kpler, Spire, Oracle/SAP logistics; selection criteria; worked
  pipeline from raw NMEA to trajectories in MovingPandas.
- 3D visualization and animation with **Blender** (⟨H⟩ 1994 initial release,
  2002 open-sourced): why a 3D DCC tool belongs in an AIS toolbox — time-
  accurate traffic animations for incident reconstruction (→ ch. 55/56),
  bridge-view simulation of what a watch officer could see, antenna/radar-
  shadow visualization on ship models (→ ch. 31/32), coverage-footprint and
  satellite-pass animations (→ ch. 39), outreach/journalism renders; the `bpy`
  Python API for importing cleaned trajectories (CSV/GeoParquet → keyframes or
  Geometry Nodes point clouds), BlenderGIS add-on for basemaps/terrain/
  georeferencing, time-remapping (real time vs. playback), dimension/reference-
  point fields from Message 5 for correctly scaled hulls, heading vs. COG for
  hull orientation, Class B irregular cadence and interpolation artifacts in
  animation, exporting glTF for web viewers (CesiumJS/deck.gl); comparison with
  kepler.gl, CesiumJS, QGIS temporal controller, and proprietary 3D VTS displays;
  caveat: Blender is not a GIS — CRS handling and precision at global scale
  (float32 coordinates; local origin shifts).
- Seeds: project docs; GateHouse case studies; vendor brochures; Blender manual
  (`bpy`, Geometry Nodes); BlenderGIS repository; published AIS/ship-traffic
  animations made in Blender (survey; (verify) attributions).

**46. What the US Coast Guard and other governments use**
- Scope: USCG NAIS (architecture, increments, contractors (verify)), VTS
  software (PAWSS, later systems), WatchKeeper/IOCs, Rescue 21 interplay; DOT
  Volpe's MSSIS/SeaVision and Transview; USACE AISAP; NOAA AccessAIS/Marine
  Cadastre, NMFS OLE tools; Navy GCCS-M; DHS/CBP; EMSA IMDatE; UK MCA; AMSA
  Craft Tracking; CCG; Singapore MPA; procurement history and open questions.
- Seeds: GAO reports on NAIS (verify); Volpe publications; agency fact sheets.

**47. Data quality, cleaning, and track reconstruction**
- Scope: error taxonomy (Harati-Mokhtari 2007 and successors); duplicate
  messages; MMSI collisions and reuse; position outliers and jump detection;
  speed-consistency checks; timestamp reconciliation (receiver vs message);
  interpolation and gap handling; voyage segmentation; port/berth/anchorage
  detection; identity resolution (MMSI ↔ IMO ↔ name over time); Class B
  irregular cadence; handling spoofed segments; reproducible cleaning pipeline.
- Seeds: Harati-Mokhtari et al. 2007; GFW data-processing docs; academic
  trajectory-cleaning papers.

**48. Spatial statistics with AIS: coverage, bias, and honest maps**
- Scope: AIS as a sample with heterogeneous, time-varying detection probability;
  receiver footprints (terrestrial fixed, moving ships/ASVs, satellites);
  estimating coverage from data (range-vs-detection curves, expected-vs-observed
  reports per interval, Class A reporting-interval model); bias correction;
  density/transit-count maps done right (Marine Cadastre methodology, EMODnet
  vessel density); hex/grid choices; uncertainty layers; capture–recapture
  analogies; moving-receiver corrections; what to report.
- Seeds: Marine Cadastre & EMODnet method notes; GFW "AIS reception quality";
  ch. 29/30 models.

**49. Analytics and machine learning on AIS**
- Scope: anomaly detection; destination/ETA prediction; fishing-activity
  classification; transshipment; dark-vessel fusion with SAR/optical; port-call
  analytics; emissions (STEAM, IMO GHG); underwater noise; ship-strike risk;
  collision-risk indices; benchmarks and public datasets; pitfalls (coverage
  bias leaking into models, label noise, temporal leakage).
- Seeds: Kroodsma 2018; Paolo 2024; Jalkanen 2009; survey papers on AIS ML.

**50. Big-data architecture for AIS**
- Scope: ingest (UDP/TCP feeds, Kafka), dedup, normalization, storage (Parquet/
  Arrow, BigQuery, PostGIS, DuckDB), spatial-temporal indexing (H3/S2/
  space-filling curves ⟨H⟩), retention and cost, streaming vs batch, public
  cloud datasets, privacy controls, provenance (keep raw NMEA with TAG blocks).
- Seeds: GFW engineering posts; cloud provider case studies.

---

### Part VIII — Charts, bridge systems, and mariners

**51. Nautical charts, ENC vs ECDIS vs ECS vs RNC, and AIS on the display**
- Scope: paper charts → RNC → ENC (S-57 data, S-52 presentation) → ECDIS
  (IEC 61174) vs ECS; NOAA's end of traditional paper charts (2025 (verify));
  AIS target symbology (IEC 62288), sleeping/activated targets, CPA/TCPA
  alarms, radar/AIS target association (IEC 62388); AIS AtoN depiction;
  pilot plugs and PPUs; chartplotters on small craft; alarm fatigue.
- Seeds: IHO S-57/S-52/S-101; IEC 61174/62288/62388; NOAA announcements.

**52. AIS and the S-100 family**
- Scope: S-100 Ed. 5 framework; S-101 ENC; S-124 navigational warnings;
  S-104/S-111 water levels and currents (today over ASM, tomorrow over VDES);
  S-421 route exchange; S-125/S-201 AtoN information and virtual AtoN; IMO
  MSC.530(106) S-100 ECDIS; dual-fuel ECDIS timeline (2026/2029 (verify));
  what AIS/VDES must carry for S-100 services; IALA/IHO/IMO coordination.
- Seeds: IHO S-100 documents; IALA G1117/G1139; IMO MSC.530(106).

**53. How mariners are trained to use AIS (and how it varies)**
- Scope: STCW competences; IMO Model Course 1.34 (AIS) (verify); IMO
  A.1106(29); flag-state differences (USCG licensing vs. MCA vs. others);
  recreational boaters (no training, Class B defaults); pilots; VTS operators
  (IALA V-103 model courses); human-factors research on AIS over-reliance;
  simulator training; what good training looks like.
- Seeds: STCW Code; IMO model courses; IALA V-103; MAIB human-factors reports.

**54. Tide, water level, weather, and marine-state transmissions**
- Scope: IMO Circ.289 FI 31 meteorological & hydrographic; legacy FI 11; USCG
  DAC 367 environmental message; NOAA PORTS over AIS; St. Lawrence Seaway water
  levels; AtoN-carried sensors; display gaps on ECDIS; S-104/S-111 transition;
  WMO VOS and AIS as a met-ocean carrier; quality flags and liability.
- Seeds: IMO SN.1/Circ.289; USCG RDC env message spec; NOAA PORTS docs; WMO.

**55. AIS-assisted incidents and accidents**
- Scope: a case-file chapter — over-reliance (COLREG Rule 7); "VHF/AIS-assisted
  collisions" in MAIB usage; wrong static data causing misidentification;
  heading-not-available confusions; Class B invisibility (filtered targets);
  *Costa Concordia*, *Baltic Ace/Corvus J*, *Sanchi*, *Dali*, *Ever Given*,
  *Sewol*, *Fitzgerald/McCain* (AIS off); and the other side: lives saved by
  AIS-SART/MOB, SAR coordination successes.
- Seeds: NTSB, MAIB, TSB, DMAIB, BSU, KMST, ATSB reports; IMO GISIS casualty module.

**56. Voyage Data Recorders and forensic reconstruction**
- Scope: VDR/S-VDR (IEC 61996-1/-2; MSC.333(90)); AIS as a recorded channel;
  extraction and time alignment; combining VDR, VTS, shore and satellite AIS;
  evidentiary standards; tooling; worked reconstruction, including a 3D
  time-accurate animation in Blender (→ ch. 45) and its evidentiary caveats.
- Seeds: IEC 61996; IMO performance standards; investigation reports.

**57. AIS and autonomous/remotely operated ships (MASS)**
- Scope: AIS as perception input and as a liability for collision-avoidance
  automation; MASS Code status (IMO); Class A obligations for MASS; spoof-
  robustness requirements; research platforms; AIS's role in remote operations
  centres.
- Seeds: IMO MASS regulatory scoping exercise; MASS Code drafts; academic papers.

---

### Part IX — Security

**58. Threat model and security implications of AIS**
- Scope: assets, actors, capabilities (receive-only, SDR transmit, network-
  feed injection, GNSS attacks, firmware); CIA analysis; Balduzzi, Pasta &
  Wilhoit (ACSAC 2014) taxonomy — spoofing (ship, AtoN, SAR aircraft, SART,
  weather, CPA), hijacking, availability (slot starvation, frequency hopping via
  Message 22, timing attacks via Messages 16/23); software-side injection into
  providers; replay; what has actually happened since; threat evolution; defense
  in depth.
- Seeds: Balduzzi et al. 2014; Trend Micro report; Goudossis & Katsikas 2019;
  Kessler 2020 (verify); NCCIC/CISA notes (verify).

**59. AIS spoofing techniques and detection**
- Scope: identity spoofing vs position spoofing vs GNSS spoofing-induced
  errors; ghost ships and fake fleets; fake AtoN and SART; "spoofing-as-a-
  service" for sanctions evasion; detection — physics/kinematics consistency,
  receiver-coverage plausibility, multi-receiver TDOA, RF fingerprints, SAR/
  optical confirmation, satellite vs terrestrial disagreement; documented
  cases (Black Sea 2017, Shanghai 2019, Point Reyes 2019, Elbit 2021 (verify),
  Baltic 2023–25); reporting and disclosure.
- Seeds: C4ADS 2019; SkyTruth posts (Bergman); Windward/Lloyd's List case
  studies; MIT Tech Review (Harris 2019); Bergman 2020 spoofing taxonomy (verify).

**60. Malicious payloads and receiver robustness: can AIS crash things?**
- Scope: attack surface — NMEA parsers, 6-bit payload reassembly, ASM decoders,
  free-text fields, Message 22/23 handlers, ECDIS/chartplotter renderers, web
  front ends of aggregators; known vulnerabilities (gpsd, OpenCPN, libais,
  commercial ECDIS — enumerate CVEs and advisories (verify each)); fuzzing
  results (OSS-Fuzz for libais/gpsd (verify)); DoS via message floods and
  alarm storms; what the standards require (IEC 60945, 61162-460; IACS UR
  E26/E27 cyber); responsible-disclosure history; hardening checklist.
- Seeds: CVE/NVD; project issue trackers; Pen Test Partners ECDIS research;
  IACS URs.

**61. Timing and network-disruption attacks**
- Scope: can a dynamic AIS cell be collapsed? fake base station (Message 4)
  time, Message 23 quiet-time and reporting-interval commands, Message 16
  assignment, Message 22 channel moves, slot starvation by flooding; modeling
  with a SOTDMA simulator; what real transponders do (type-approval behaviors);
  detectability; mitigations in VDES.
- Seeds: Balduzzi 2014; M.1371 sync rules; simulator results (this book).

**62. GNSS jamming and spoofing: effects on AIS and workarounds**
- Scope: jamming (position loss, indirect sync, timestamp 62/63) vs spoofing
  (coherent wrong positions, airport "circles"); event catalog with sources;
  AIS as a global GNSS-interference sensor (mapping efforts (verify
  organizations)); operational workarounds (manual position, radar overlay,
  R-Mode, eLoran, inertial, VDES ranging); regulatory responses (IMO MSC
  circulars, ICAO parallels).
- Seeds: C4ADS; GPSPatron/Spire/Windward reports (verify); R-Mode Baltic;
  IMO MSC.1/Circ. on GNSS interference (verify).

**63. Blue-force, encrypted, and military AIS**
- Scope: W-AIS/Warship AIS; NATO STANAG(s) (verify number); encrypted Class A
  modes from Saab/Kongsberg/L3Harris; US Navy and Coast Guard encrypted AIS
  practice; key management; interoperability with civilian cells (does
  encrypted traffic still occupy slots?); navy policy after 2017; law-enforcement
  covert modes; why "AIS off" is still common.
- Seeds: vendor datasheets; NATO publications (verify access); GAO/CRS reports.

**64. Authentication and the future of AIS security**
- Scope: why AIS cannot be authenticated in place; proposals (PAIS, TESLA-like
  broadcast authentication, PKI over VDES, IALA/IMO work items); VDES security
  provisions (M.2092-1, IALA G1139); data-provider-side trust scoring;
  cost/benefit and migration paths.
- Seeds: Goudossis & Katsikas 2019; Kessler 2020; Wimpenny et al. 2022 (verify);
  IALA ENAV papers.

**65. Hacks and unintended uses of AIS**
- Scope: R-Mode ranging from AIS/VDES base stations (GNSS backup); tsunami
  detection from ship kinematics; surface currents from drift; AIS as a
  telemetry channel (buoys, gliders, iceberg beacons (verify)); race-mark and
  swim-zone AtoNs; pseudo-AIS internet relays from phones (Boat Beacon et al.)
  and why that is contentious; Message 12/14 text spam and religious messages;
  AIS "art" and visualizations (e.g., "All the Ships" ⟨H⟩; Blender renders of
  traffic and dark-fleet activity); amateur long-distance
  reception contests; AIS data as a sea-level/wave proxy; abuse (fishing-net
  buoys with bogus MMSIs); legal lines.
- Seeds: R-Mode papers; Inazu; eOdyn; news items; FCC enforcement advisories.

---

### Part X — Adjacent and complementary systems; the future

**66. Other ways to track ships**
- Scope: VMS (NMFS, EU, FAO; Inmarsat-C/Iridium polling); LRIT (SOLAS V/19-1;
  6-hourly; data centres); WMO/NOAA VOS; Inmarsat-C/FleetBroadband/VSAT
  metadata; coastal and HF over-the-horizon radar; SAR imagery (Sentinel-1,
  RADARSAT, ICEYE); optical (Planet, Maxar); RF geolocation (HawkEye 360,
  Unseenlabs); acoustic; port state and customs records; Equasis/IHS; fusion.
- Seeds: agency docs; GFW SAR work; ESA/Copernicus.

**67. Mobile phones at sea**
- Scope: apps (MarineTraffic, Navionics, Boat Beacon, SailTimer…); cellular
  coverage at sea and shipboard picocells; network-side location (SS7 ATI/SRI
  for 2G/3G; Diameter for 4G/5G; HLR/HSS lookups) and their abuse; IMSI
  catchers; Wi-Fi/Bluetooth; satellite phones; Starlink maritime; privacy and
  law; how this complements or contradicts AIS.
- Seeds: GSMA/3GPP specs; ENISA SS7 reports; academic SS7/Diameter security papers.

**68. Special-purpose AIS: fishing gear, AtoN, SART/MOB/EPIRB, and ADS-B kinship**
- Scope: fishing-net buoys (Class B/AtoN style transmitters, MMSI misuse, FCC
  enforcement advisory (verify), EU/Asia rules, flooding of coastal cells);
  AtoN real/synthetic/virtual and management (IALA G1050); AIS-SART (IEC
  61097-14), MOB (ETSI EN 303 098), EPIRB-AIS (974); ADS-B comparison table
  (modulation, security, authority, history).
- Seeds: IALA; IEC; ETSI; FCC; ICAO.

**69. "AIS 2.0", VDES, and other channels: what is real**
- Scope: VDES components (AIS + ASM + VDE-TER + VDE-SAT); channel plan; data
  rates; M.2092-1; satellites flown (NorSat-2/TD, Sternula, AAC Clyde/Saab,
  others (verify)); SOLAS carriage status (not mandated as of writing (verify));
  what "AIS 2.0" means in marketing vs standards; other channels ever used for
  AIS (regional via Message 22, 75/76 long-range, ASM 1/2, DSC ch 70 for
  management); migration scenarios; what to design for now.
- Seeds: ITU-R M.2092-1; IALA G1117/G1139; WRC resolutions; vendor roadmaps.

---

### Appendices

- **A. Timeline** — merged chronology; `⟨H⟩` from gis-history, `⟨+⟩` added here.
- **B. Standards register** — table: issuer, id, title, edition/year, status,
  free/paid, what it governs, chapters citing it.
- **C. Message bit-layout reference** — Messages 1–27 field tables; sentinel
  values; ASM header; worked hex decodes.
- **D. Code tables** — MID list; MMSI patterns; nav status; ship/cargo type
  codes; EPFS types; AtoN types; DAC/FI registry snapshot; NMEA talker IDs and
  sentence formatters; NMEA 2000 AIS PGNs.
- **E. Software catalog** — decoders/encoders, processing, visualization
  (incl. Blender/BlenderGIS, kepler.gl, CesiumJS),
  simulation; language, licence, status, last-release date, notes.
- **F. Hardware catalog** — transponders, receivers, SDRs, antennas, splitters;
  class, power, GNSS constellations, interfaces, approvals.
- **G. Datasets and providers** — open and commercial; coverage, latency,
  licence, formats, access.
- **H. Glossary and acronyms.**
- **I. "Try it" cookbook** — tested snippets: decode with libais/pyais/gpsd;
  TAG-block parsing; SOTDMA slot simulator; radio-horizon and link-budget
  calculators; GMSK burst synthesis/demod in GNU Radio or NumPy; coverage
  estimation; MovingPandas trajectory pipeline; DuckDB density map; Blender
  `bpy` script animating a cleaned trajectory set with correctly scaled hulls.
- **J. Organizations directory** — contacts, mandates, key documents.

---

## 5. Reading paths

- **Mariner / VTS operator:** 1 → 3 → 4 → 20 → 22 → 51 → 53 → 55 → 36.
- **Regulator / policy:** 1 → 2 → 10 → 14 → 15 → 16 → 17 → 19 → 58 → 69.
- **RF / SDR engineer:** 27 → 28 → 21 → 29 → 30 → 31 → 32 → 33 → 34 → 42.
- **Software developer:** 22 → 23 → 26 → 44 → 45 → 47 → 50 → 60.
- **Data scientist / economist:** 2 → 5 → 41 → 47 → 48 → 49 → 6.
- **Security researcher:** 20 → 21 → 24 → 58 → 59 → 60 → 61 → 62 → 64.
- **Historian / journalist:** 9 → 10 → 11 → 12 → 17 → 18 → 65 → App. A.
- **Hobbyist:** 1 → 42 → 32 → 31 → 44 → 65.

---

## 6. Research sources and citation policy

**Primary document families to acquire or index before drafting**
(see TASKS Phase 1):
ITU-R M.1371 (all editions), M.585, M.2092, M.493, RR App. 18; IMO MSC.74(69),
A.917(22), A.956(23), A.1106(29), SN/Circ.227 (+ amendments), SN.1/Circ.289,
MSC.1/Circ.1473, MSC.1/Circ.1252, MSC.246(83), A.1158(32), MSC.530(106); SOLAS
Ch. V consolidated; IEC 61993-2, 62287-1/-2, 62320-x, 61097-14, 61162-x, 62288,
61174, 62388, 61996, 60945; IALA guidelines/recommendations named above; IHO
S-100/S-101/S-124/S-104/S-111/S-421/S-125/S-201; NMEA 0183 v4.11, NMEA 2000
AIS PGNs; RTCM AIS documents; ETSI EN 303 098; 33 CFR 164.46; 47 CFR Part 80;
EU directives/regulations named above; Lans patents; accident reports named in
ch. 55; the key papers named per chapter; the GFW history article; the Scranton
Bloomberg manual; the 2025 GFW video; schwehr/gis-history.

**Citation rules.** Full citations in each chapter's References and in its
`.bibtex`. DOI only when confirmed. Standards cited by issuer + id + edition +
year. Web sources with access date and, where possible, an archive.org
snapshot. Mark unconfirmed items `(verify)`; the verification pass (TASKS
Phase 4) removes every `(verify)` or deletes the claim.

---

## 7. Figures and code

- Figures as SVG where possible (slot map, burst structure, GMSK eye diagram,
  message layouts, coverage maps, timeline). Photographs only with licence.
- Every `Try it` snippet lives in `code/` and is executed in CI against
  `data/samples/`. Samples must be small, redistributable, and have provenance
  (own receiver logs, or open-data excerpts with licence noted).
- No code that transmits on AIS frequencies is included; GMSK synthesis examples
  write to files only and carry the legal note.

---

## 8. Tooling and build

- Markdown source; build with **mdBook** (fast, simple) or **Jupyter Book**
  (executes notebooks). Decision in TASKS Phase 0; default mdBook with a
  separate `code/` test suite.
- `tools/check_book.py`: template headings present and ordered; word count;
  box count; mandatory section present; `(verify)` census.
- `tools/check_xrefs.py`: relative links resolve; chapter slugs match manifest.
- `tools/check_citations.py`: every in-text citation key exists in the chapter
  `.bibtex`; URL liveness; DOI resolution.
- `tools/build_bibliography.py`: merge to `BIBLIOGRAPHY.bib`, dedupe.
- CI: lint Markdown, run code tests, run checkers, build the site.

---

## 9. Risks and open questions

| Risk | Mitigation |
|---|---|
| Paywalled standards (ITU/IEC/IMO) limit direct quotation | Cite by clause; summarize; use freely available ITU-R recommendations and IMO circulars; flag anything only seen second-hand. |
| Fabricated or mis-remembered citations | Hard `(verify)` rule; dedicated verification phase; no DOI without resolution check. |
| Security chapters could read as a how-to | Threat-model framing, no transmit code, legal notes, focus on detection and defense. |
| Scope creep (69 chapters) | Fixed skeleton; research dossiers before drafting; word ceilings; appendix tables absorb catalogs. |
| Fast-moving topics (VDES, GNSS interference, provider M&A) | "As of <date>" phrasing; `Then & now` sections; a `CHANGELOG.md`. |
| Rights to figures and sample data | Own receiver logs; open-data excerpts with licence; redraw diagrams. |

**Open questions for the owner**
1. Build system: mdBook vs Jupyter Book?
2. Licence for prose and code?
3. Should `bitvector-modern` and other personal projects be treated as
   first-party (author's) material with extra depth?
4. Target length: full 69 chapters, or a first edition of ~40 with the rest as
   appendices?
5. Is live data collection (a home receiver) available to produce original
   figures and samples?

---

## 10. Coverage matrix

### 10.1 Items in the brief → chapters

| Brief item | Chapter(s) |
|---|---|
| All uses of AIS data (+ what's missing) | 2 (+3–8) |
| Open-source decoding/encoding history: libais, gpsd, aisparser, Rust parsers, noaadata, bitvector-modern, ais-area-notice | 44, 23, App. E |
| Processing software, open & proprietary: MovingPandas, pandas, GateHouse | 45 |
| Blender for 3D visualization/animation of AIS | 45, 56, 65, App. E, App. I |
| USCG / government software | 46 |
| VTS use of AIS | 4 |
| Mariner training and its variation | 53 |
| Security implications | 58 |
| Malicious data to ships/shore; DoS/corruption of receivers; documented issues | 60, 58 |
| Timing signals: how passed, used, robustness; can timing attacks break the network | 24, 61 |
| Legal issues and key court cases | 17 |
| Listen for Whales / Whale Alert | 7, 43 |
| All standards documents defining AIS | 15, App. B |
| User hacks / unintended uses | 65 |
| RF basics for ships | 27 |
| RF modeling; AIS for propagation monitoring/model testing | 29 |
| Studies on propagation, network loading, packet loss | 29, 30 |
| What can be recovered from corrupted/colliding packets | 30 |
| AIS RF encoding | 28 |
| Hardware and SDR, receive and transmit | 33 |
| Collection networks and providers | 41 |
| Low-budget home receiver | 42 |
| AIS with S-100+ charting | 52 |
| Tide and marine-state transmissions | 54 |
| Demonstration programs | 43 |
| Blue force and encryption | 63 |
| How satellites receive/process AIS; have satellites transmitted AIS | 39 |
| AIS in aircraft and drones | 40 |
| AIS for fishing gear | 68 |
| Spoofing techniques | 59 |
| RF-level deep dives; SDR/hardware quirks to identify manufacturer/unit | 34 |
| Failure modes of software and hardware | 36 |
| Direction finding | 35 |
| Bloomberg terminal / commodity traders | 5 |
| 2025 GFW AIS and dark ships video | 6 |
| Noise sources on ships | 31 |
| AIS-assisted incidents/accidents | 55 |
| ECDIS vs ENC; nautical charts | 51 |
| Privacy | 19 |
| Other ways to track ships; mobile phones; SS7/Diameter | 66, 67 |
| Key organizations: IMO, RTCM, IALA, IHO | 14, App. J |
| Key laws and treaties; SOLAS | 16, 9–10 |
| At-sea operations where AIS helps | 3 |
| MMSI deep dive | 13 |
| NMEA 0183/2000/TAG block; sharing and logging standards | 26 |
| External timing sources; internal timing; hardware without GNSS | 24 |
| GNSS overview; which systems supported; AIS without GPS; GNSS-denied behavior | 25 |
| Best antennas per application (large/small/very small/collection stations) | 32 |
| Shore collection options: towers, lighthouses, buildings, places to avoid (radar, NOAA weather radio) | 37 |
| At sea: buoys, ASVs | 38 |
| VMS, VOS, LRIT | 66 |
| AIS 2.0 — real? Other RF channels for AIS | 69 |
| GNSS jamming impacts and workarounds | 62, 25 |
| Voyage Data Recorder | 56 |
| Spatial statistics under RF/packet-loss/moving-receiver constraints | 48 |
| Patents and expiry | 18 |
| National security | 8, 63 |
| Deep history; GFW history article; 9/11; SOLAS | 9–12 |
| gis-history topics and starting points | 9–12, App. A, all `Then & now` |

### 10.2 Gaps identified and added

Message catalog and ASM deep dives (22–23); station classes and link layer
(20–21); interfaces/logging (26); data quality and track reconstruction (47);
analytics/ML (49); big-data architecture (50); VDR/forensics (56); MASS (57);
authentication/future security (64); Inland AIS and RIS (20, 43, 16);
hydrographic and cable-protection uses (2); port-call analytics and
just-in-time arrival (4, 49); COVID-era economics (5); AIS-SART/MOB/EPIRB and
ADS-B kinship (68); AtoN management (68); human factors and alarm fatigue
(51, 53); market and provider consolidation (12, 41); ethics of research and
disclosure (19); simulation and type-approval testing (21, 33, 61);
organizations directory, code tables, cookbook (App. D, I, J).
