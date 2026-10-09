# Dossier: Application-Specific Messages (ASM)

**Purpose.** This dossier collects the primary-source facts needed to write about AIS *application-specific messages* — the binary payloads carried in Messages 6, 8, 25 and 26 and identified by a 16-bit Application Identifier (DAC + FI). It covers the ITU-R M.1371-6 Annex 4 framework (DAC/FI, International Function Messages 0–5, drafting rules, capacity), the IMO circulars that define the international applications (SN/Circ.236 of 2004, SN.1/Circ.289 of 2010), the regional registries (Inland AIS DAC 200, St. Lawrence Seaway DAC 316/366, USCG DAC 366/367, others) and the IALA ASM Collection that now serves as the de-facto register. It also records what today's open-source decoders actually do with ASM payloads, with test vectors decoded in the repo venv. It feeds PLAN chapters **23 (Application-specific messages)**, **43 (Decoding binary payloads / ASM)**, **54 (Regional and inland AIS)**, **7 (Whale Alert / right-whale area notice case)**, **60 (VDES and the future of ASM)** and Appendices **C (message/field reference)** and **D (DAC/FI register)**. Sibling dossiers `r-messages.md` (container message field tables), `r-standards-imo.md` (circular metadata), `r-standards-iala.md` (G1095, ASM Collection) and `r-link-layer.md` (slot usage) are cross-referenced rather than duplicated.

## Key questions

1. What exactly is an ASM in M.1371 terms, and how is the Application Identifier (DAC + FI) structured and allocated?
2. Which messages carry ASMs, what are their payload capacities in bits/characters/slots, and what are the byte-alignment and spare-bit rules?
3. What are the International Function Messages (IFM 0–5) in Annex 4 and how do interrogation, capability and acknowledgement work?
4. Which international applications exist (SN/Circ.236 → SN.1/Circ.289), what changed between them, and when were the old ones withdrawn?
5. Which regional DACs have published applications (200 Inland Europe, 316/366 Seaway, 366/367 USA, 219 Denmark, 235/250 UK, 265 Sweden, others) and where are they authoritatively documented?
6. Who keeps the register today (IALA ASM Collection), what are its states (proposal/draft/testing/in force/deprecated/replaced/discontinued) and how do entries get in?
7. What does regulation say about ASM use (US 33 CFR 164.46(d)(4))?
8. How well do pyais, libais and gpsd decode ASM payloads, and where do they disagree?
9. What is the actual uptake of ASM on the air, and why has it been limited?
10. How does ASM relate to VDES ASM channels and the VDE-SAT/VDE-TER application identifiers in the same register?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| ITU-R Recommendation M.1371-6, Annex 4 "Application-specific messages" | M.1371-6, approved 2026-02-19 (per ITU page read 2026-10-04); Annex 4 = ASM (was Annex 5 in -5) | https://www.itu.int/rec/R-REC-M.1371/en (PDF read locally: scratch `m1371-6.txt` lines 2371–2960) | AI structure (DAC/FI), Tables 23–33 (IFM 0–5), drafting rules A4-4, capacity Table 29 | Free (ITU-R Recommendations are free PDFs) |
| ITU-R M.1371-6, Annex 5 "Sequencing of transmission packets" | same document | same | Sequence numbers 0–3 for addressed messages, VDL-ACK/PI-ACK flow (Figures 23–31) | Free |
| ITU-R M.1371-6, Annex 7, Tables for Messages 6, 8, 25, 26 | same (Annex 7 = messages, formerly Annex 8) | same | Container messages; see `r-messages.md` for full field tables | Free |
| IMO SN.1/Circ.289 "Guidance on the use of AIS Application-Specific Messages" | 2 June 2010 (circular date); IALA register lists "permitted as from 01/06/2010", area-notice FIs 22/23 from 04/03/2011 | https://www.navcen.uscg.gov/sites/default/files/pdf/IMO_SN1_Circ289_Guidance_on_use_of_AIS_ASM.pdf (URL read for `r-standards-imo.md`; metadata reused here) | Defines international FIs 16–32 under DAC 1; revokes SN/Circ.236 applications from 1 Jan 2013 | Free (USCG mirror) |
| IMO SN/Circ.236 "Guidance on the application of AIS binary messages" | 28 May 2004 (date per `r-standards-imo.md`; register shows FIs permitted 01/05/2004–19/05/2004) | see `r-standards-imo.md` | Trial FIs 11–15 (met/hydro, dangerous cargo, fairway closed, tidal window, extended static), 16–17 (persons on board, pseudo-AIS targets) | Free (IMO docs) |
| IALA ASM Collection (official register) | ongoing; official URL cited on mirror | http://www.iala-aism.org/asm (official; not fetched this session — login/JS) ; mirror https://www.e-navigation.nl/asm (read 2026-10-05) | Register rows: title, physical link, Msg, DAC, FI, sub, version, slots, state, registrant, permitted-from, dates | Free |
| IALA Guideline G1095 "Harmonised Implementation of Application-Specific Messages (ASM)" | Ed. 1.1, 2013 (per `r-standards-iala.md`) | https://www.iala-aism.org/product/g1095/ (verify exact URL) | How administrations should design, register and implement ASM | Free registration |
| IALA Recommendation A-124 / Guidelines G1028 (2002) and G1029 (2004) on AIS binary messages | legacy | see `r-standards-iala.md` | Historical regional binary message guidance; now unmaintained | Free |
| 33 CFR § 164.46(d)(4) | e-CFR, read 2026-10-05 | https://www.law.cornell.edu/cfr/text/33/164.46 | US rule limiting ASM to IMO-adopted or IALA-Collection US/Canada applications, ≤1 ASM per minute | Free |
| gpsd AIVDM/AIVDO protocol decoding (E. S. Raymond) | v1.58 | https://gpsd.gitlab.io/gpsd/AIVDM.html | Community documentation of DAC 1, 200, 235/250, 316/366, 367 payload layouts | Free |
| gpsd test corpus | `test/sample.aivdm` (current main) | https://gitlab.com/gpsd/gpsd/-/raw/master/test/sample.aivdm | Known-good ASM sentences (DAC 1 FI 11, DAC 235 FI 10, etc.) | Free |
| pyais | 3.2.3 (installed in repo venv) | https://github.com/M0r13n/pyais | Decodes DAC 1 FIs 16–31 (Circ.289), DAC 200 FIs 10/21/22/23/24/40/55, DAC 235/250 FI 10 (verify list against source) | Free (MIT) |
| libais | 0.17 (installed in repo venv) | https://github.com/schwehr/libais | Decodes DAC 1 (Circ.236+289), 200, 235/250, 316/366, 367 payloads; rejects unknown DAC/FI | Free (Apache-2.0) |
| ais-area-notice (formerly ais-areanotice-py) | GitHub, 337 commits (page read 2026-10-05) | https://github.com/schwehr/ais-area-notice (old URL `ais-areanotice-py` redirects) | "Reference library for the IMO Circ 289 AIS Binary Message for timed zone messages" | Free |
| CESNI / CCNR Inland AIS standard (ES-TRIN annex, "Vessel Tracking and Tracing Standard for Inland Navigation") | current edition 2.x (verify edition/year) | https://www.cesni.eu/en/documents/es-ri/ (verify) | DAC 200 inland FIs; EU registrant in IALA register | Free |
| St. Lawrence Seaway "AIS Data Messaging Formats and Specifications" | Seaway; register shows DAC 316 & 366 FI 1/2/32 "permitted from 09/03/2002" | https://www.greatlakes-seaway.com (exact PDF URL to verify) | Weather, wind, water level, water flow, lockage order, estimated lock times, version messages | Free |
| USCG RDC ASM specifications (DAC 367 FI 22 Geographic Notice v2, FI 29 Linked Text v1, FI 33 Environmental v3, FI 35 Waterways Management v2) | register states "testing"; registrant USCG RDC | via IALA ASM Collection entries (per-entry pages on iala-aism.org, verify) | US ASM designs that superseded DAC 366 versions | Free |

## Verified facts

| Fact | Source (clause/page) | Confidence |
|---|---|---|
| The application identifier (AI) is 16 bits: a 10-bit Designated Area Code (DAC) followed by a 6-bit Function Identifier (FI). | M.1371-6 A4-1.1 / A4-1.2 (text lines ~2380–2420) | high |
| DAC allocation: 0 = test; 1–9 = international (IAI); 10–999 = regional (RAI), based on the Maritime Identification Digits (MID); 1000–1023 reserved for future use. | M.1371-6 A4-1.2, Table 23 | high |
| Table 24 (IFMs under DAC 001): FI 0 text telegram; FI 1 "discontinued" (was application acknowledgement); FI 2 interrogation on specific IFM; FI 3 capability interrogation; FI 4 capability reply; FI 5 application acknowledgement to an addressed binary message; FI 6–9 reserved for system; FI 10–63 international operational (defined outside M.1371, i.e. by IMO). | M.1371-6 A4-2, Table 24 | high |
| IFM 0 text telegram: 11-bit text sequence number (all zeros = not used), then 6-bit ASCII text (Table 45 alphabet); spare 1/3/5/7 bits to keep byte boundaries; Msg 6/8 application data 80–1 008 bits; Msg 25 text max 66 chars addressed / 96 broadcast; Msg 26 text max 936 chars addressed / 972 broadcast. | M.1371-6 Tables 25–28 (Table 27: "112-168 bits for Addressed, or 80-168 bits for Broadcast"; Table 28: "136-1 064 … or 104-1 064") | high |
| Note in Tables 25–28: when a 7-bit spare is needed, the first 6 bits are read as a valid 6-bit character ("@" for all zeros) — a known trailing-"@" artefact. | M.1371-6 Table 25–28 NOTE 1 | high |
| Table 29 gives estimated maximum 6-bit characters per slot count for Msgs 6, 8, 25, 26; "the number of slots used will be affected by the bit stuffing process". | M.1371-6 text preceding Table 29 (p. 73) | high |
| IFM 4 capability reply (Msg 6, 352 bits, 2 slots): 10-bit DAC code + 128-bit "FI availability" table = 2 bits per FI (FI 0…63, first bit 1 = available, second reserved) + 126 spare. | M.1371-6 A4-5.4, Table 32 | high |
| IFM 5 application acknowledgement (Msg 6, 168 bits, 1 slot): DAC (10) + FI (6) of received message, 11-bit text sequence number (0 = none, 1–2 047), 1-bit "AI available", 3-bit "AI response" (0 unable, 1 acknowledged, 2 response to follow, 3 able but inhibited, 4–7 spare), 49 spare. | M.1371-6 A4-5.5, Table 33 | high |
| "An application should never acknowledge a binary broadcast message." Absence of IFM 5 ⇒ assume no application is attached at the destination PI. | M.1371-6 A4-5.5 | high |
| Addressed binary messages (Msg 6/25/26 addressed) carry a 2-bit sequence number (0–3) which, with message type and destination, forms a unique transaction id; VDL-ACK (Msg 7/13) and PI-ACK flow with retransmission after timeout; Annex 5 example shows 2 retransmissions before PI-ACK(FAIL). | M.1371-6 Annex 5, Figures 23–31 | high |
| Drafting rules (A4-4): position fields in the order position accuracy / longitude / latitude / precision / EPFD / timestamp; UTC fields year 14, month 4, day 5, hour 5, minute 6, second 6 bits; payload should be byte-aligned. | M.1371-6 A4-4 (lines ~2480–2560) | high (field-width values from summary of earlier read; re-check exact ordering text on final pass) |
| SN.1/Circ.289 defines DAC 1 FIs 16 (number of persons on board, Msg 6), 17 (VTS-generated/synthetic targets, Msg 8), 18 (clearance time to enter port, Msg 6), 19 (marine traffic signal, Msg 8), 20 (berthing data, Msg 6), 21 (weather observation report from ship, Msg 8), 22 (area notice broadcast, Msg 8), 23 (area notice addressed, Msg 6), 24 (extended ship static and voyage-related data, Msg 8), 25 (dangerous cargo indication, Msg 6), 26 (environmental, Msg 8), 27 (route information broadcast, Msg 8), 28 (route information addressed, Msg 6), 29 (text description broadcast, Msg 8), 30 (text description addressed, Msg 6), 31 (meteorological and hydrographic data, Msg 8), 32 (tidal window, Msg 6). | `r-standards-imo.md` (Circ.289 Table 1) corroborated by IALA register rows (e-navigation.nl/asm read 2026-10-05): each listed "IMO Circ. 289", state "in force" | high |
| Register "permitted as from" dates: Circ.289 FIs 01/06/2010, except area notice FI 22/23 04/03/2011. | https://www.e-navigation.nl/asm (rows "Area notice … IMO Circ. 289 … 04/03/2011") | medium (mirror; the 2011 date for area notice is unexplained — possibly a corrigendum; verify) |
| SN/Circ.236 (2004) FIs now "deprecated" in register: FI 11 met/hydro (Msg 8), 12 dangerous cargo (Msg 6), 13 fairway closed (Msg 8), 14 tidal window (Msg 6), 15 extended static (Msg 8), 16 persons on board (Msg 6), 17 pseudo-AIS targets (Msg 8). | e-navigation.nl/asm rows marked "IMO Circ. 236 … deprecated" | high |
| Register also shows legacy M.1371-1 (1998) DAC 1 entries still "in force": Msg 6 FI 19 extended ship static, Msg 6 FI 40 number of persons on board, Msg 8 FI 16 VTS targets, Msg 8 FI 18 advice of waypoints; and "deprecated" Msg 6 FI 17/18. | e-navigation.nl/asm rows "ITU-R.M.1371-1 … 01/01/1998" | medium (register content; M.1371-1 itself not re-read) |
| Register columns: Title, Physical link (AIS / ASM / VDE-TER / VDE-SAT), Msg, DAC/VPFI, FI/Message ID, Sub, Version, # slots (max), State, Link to associated ASM, Registrant, Permitted as from, (expiry), created, updated. States observed: proposal, draft, testing, in force, deprecated, replaced, discontinued. | e-navigation.nl/asm header row | high |
| Register banner: "The official collection can be found at http://www.iala-aism.org/asm". | e-navigation.nl/asm page text | high |
| Inland AIS (registrant "EU") DAC 200: Msg 8 FI 10 inland static & voyage (in force, 10/10/2007); Msg 8 FI 11 convoy (2014); Msg 8 FI 23 EMMA warning (**discontinued**); FI 24 water level (**deprecated**, replaced by Msg 8 FI 26 water level v0, 18/10/2020); FI 25 present bridge clearance v1 (18/10/2021); FI 40 signal status (**replaced** by FI 41 Signal Station, 24/11/2016); FI 42 geographic notice and FI 44 ISRS text (Msg 8 proposals 2020; Msg 6 versions in force 18/10/2021); Msg 6 FI 3/4 inland capability interrogation/reply (18/10/2021); Msg 6 FI 21 ETA, FI 22 RTA at lock/bridge/terminal (2007); Msg 6 FI 55 number of persons on board (2007); Msg 8 FI 1 control message (2017). | e-navigation.nl/asm rows with DAC 200 | high (as register content) |
| St. Lawrence Seaway messages are registered under **both** DAC 316 (Canada) and DAC 366 (USA), Msg 6, using a **sub-identifier** column: FI 1 sub 1 weather station, sub 2 wind, sub 3 water level, sub 6 water flow; FI 2 sub 1 lockage order, sub 2 estimated lock times; FI 32 sub 1 version message; all "in force", permitted from 09/03/2002, registrant "Saint Lawrence Seaway Development Corporation". | e-navigation.nl/asm rows DAC 316/366 | high (as register content) |
| USCG RDC entries: DAC 366 Msg 8 FI 22 area notice, FI 33 environmental, FI 35 waterways management (2011) are **deprecated**; replaced by DAC 367 Msg 8 FI 22 Geographic Notice v2 (5 slots), FI 29 Linked Text v1, FI 33 Environmental v3, FI 35 Waterways Management v2 (3 slots), all state **testing**; DAC 367 Msg 6 FI 16 passenger and crew count (draft). | e-navigation.nl/asm rows DAC 366/367 | high (as register content) |
| USCG encrypted "Blue Force"/SAR family under DAC 366 on Msg 25 and Msg 26: e.g. Msg 26 FI 13 SAR pattern report (encrypted), FI 15 trackline report (encrypted), FI 17 text (encrypted), FI 36 area notice (encrypted), FI 37 route info (encrypted), FI 38 SITREP, FI 39 static data (encrypted) — permitted from 12/05/2016 or 21/04/2017, "in force"; unencrypted variants Msg 8 FI 14/16 (2016). | e-navigation.nl/asm rows "USCG … (encrypted)" | high (as register content) |
| USACE DAC 367 Msg 8 FI 23/24/25 "Satellite Ship Weather" (normal/small/tiny) and FI 26 "GPS Jamming and Spoofing Report", all draft, permitted 01/10/2019. | e-navigation.nl/asm | high (as register content) |
| Other regional registrants: Denmark DAC 219 (Msg 8 FI 1 intended route; Msg 6 FI 2/3 route suggestion/reply; FI 4/6 proposals 2015); STM project Sweden DAC 265 Msg 8 FI 1 route message (2016) and Danish DMA DAC 265 FI 6; UK Trinity House DAC 235 and 250 Msg 6 FI 10 AtoN monitoring data (2009); Rijkswaterstaat DAC 246 FI 12 route intention sharing (testing, 07/07/2025); Zeni Lite Buoy DAC 0 Msg 6 FI 0 monitoring AtoN (2002); PETROBRAS DAC 710 FI 11 offshore unit dimensions (draft); Sena and Vans DAC 421 Msg 6 FI 16 collision alarm (testing); China MSA ASM DAC 412 FI 1 meteorological information (testing, 11/09/2023). | e-navigation.nl/asm | high (as register content) |
| The register already holds VDES entries: physical link "VDE-TER"/"VDE-SAT" with DAC 1/2/4 message ids 0–6 (network orbit data, text 6-bit/UTF-8, virtual AtoN, AIS position report retransmit, AIS message authentication, MMTP), state proposal, registrant IALA, 01/12/2022; and "ASM" physical-link rows (STM route message DAC 265 FI 2; China DAC 412). | e-navigation.nl/asm first rows | high |
| US rule: "AIS application-specific messaging (ASM) is permissible, but is limited to applications adopted by the International Maritime Organization (such as IMO SN.1/Circ.289) or those denoted in the … (IALA) ASM Collection for use in the United States or Canada, and to no more than one ASM per minute." | 33 CFR 164.46(d)(4), https://www.law.cornell.edu/cfr/text/33/164.46 | high |
| Same section's note: "Most application-specific messages require interfacing to an external system that is capable of their portrayal, such as equipment certified to meet … (RTCM) electronic chart system (ECS) standard 10900 series." | 33 CFR 164.46 note following (d) | high |
| gpsd `test/sample.aivdm` area-notice vector `!AIVDM,1,1,,B,803Ovrh0EP:024`@02PN04da=3V<>N0000,4*39` decodes (pyais 3.2.3 and libais 0.17, run 2026-10-05) to Msg 8, MMSI 3669739, DAC 1, FI 22, linkage 10, notice type 0, month 1, day 1, 05:02, duration 20 min, one circle sub-area at lon −69.864983, lat 42.08295, precision 4, radius 926 × 10¹ = 9 260 m. | venv run; bit layout hand-checked (see worked example A) | high |
| libais labels notice type 0 as "Caution Area: Marine mammals habitat (implies whales NOT observed)" and reports `duration_minutes: 2` (pyais: 20; raw 18-bit field = 20). | venv run | high (the libais duration value is a bug or unit error — verify against libais source) |
| Area-notice sub-area (circle) bit layout confirmed from the vector: shape 3 bits, scale factor 2 bits (10^n), longitude 25 bits (1/1000 min), latitude 24 bits (1/1000 min), precision 3 bits, radius 12 bits, spare 21 bits = 90 bits per sub-area. | hand decode matching libais output | high |
| DAC 1 FI 31 met/hydro vector (pyais tests) `!AIVDO,1,1,5,A,8>jR06@0Gwli:QQUP3en?wvlFR06EuOwgwl?wnSwe7wvlOwwsAwwnSGmwvh0,0*51` → MMSI 992509977 (an AtoN MMSI), lon −6.134067, lat 53.294933, day 29 23:24, all sensors at "not available" sentinels (wind 127, dir 360, air temp −102.4, humidity 101, dew 50.1, pressure 1310 hPa = 799+511, visibility 12.7, water level 30.01, etc.). | venv run | high |
| Decoder discrepancies on FI 31: libais `air_pres` = 13.11 (pyais 1310 hPa); libais `wave_height` = 255.0 (pyais 25.5). | venv run | high |
| Inland DAC 200 FI 10 vector `!AIVDM,1,1,,B,83aDChPj2d<dL<uM=hhhI?a@6HP0,0*40` → MMSI 244650946, ENI "02103547", length 39.0 m, beam 5.0 m, inland ship type 8010, hazard 0, loaded; **draught pyais 2.04 m vs libais 20.4** (units/scale disagreement). | venv run | high |
| `ais-area-notice` GitHub repo (redirect target of `ais-areanotice-py`) has 337 commits and describes itself as "Reference library for the IMO Circ 289 AIS Binary Message for timed zone messages". | https://github.com/schwehr/ais-area-notice read 2026-10-05 | high |
| Message 8 total length 56–1 008 bits (application data ≤ 952 bits); Message 6 88–1 008 bits (≤ 920 bits data); Message 25 ≤ 168 bits; Message 26 ≤ 1 064 bits incl. 20-bit comm-state tail. | M.1371-6 Annex 7 Tables (see `r-messages.md` for Table numbers) | high |

## Notes and quotes

- **Definition in the standard's own words.** Annex 4 begins (A4-1): the application identifier "should be used to identify the application and the function message" and consists of DAC and FI; the regional DAC "is based on the MID" (quote paraphrased from the extracted text; verify exact wording when quoting in the chapter).
- **Text telegram capacity edge-case.** Tables 25–28, NOTE 1: "When a 7-bit spare is needed to satisfy the 8-bit byte boundary rule, the 6-bit spare will be interpreted as a valid 6-bit character (all zeros is the '@' character). This is the case when the number of characters is: 1, 5, 9, 13, 17, 21, 25, etc." — good sidebar material for the "why do I see trailing @" question.
- **IFM 5 rule.** "An application should never acknowledge a binary broadcast message." (A4-5.5). And: "If the interrogating application does not receive an IFM 5, when requested, then the application should assume that addressed AIS station does not have an application attached to its Presentation Interface (PI)."
- **Capability reply.** Table 32 packs availability as "pair of two consecutive bits … for every FI, in the order FI 0, FI 1, … FI 63" — 128 bits; the message is fixed at 352 bits / 2 slots.
- **Annex 5 sequencing walk-through** (Figures 23–31) is a ready-made narrative: four addressed messages (seq 0–3), B hears 0 and 3, VDL-ACKs; A times out and retransmits 1 and 2; 2 succeeds; 1 fails after two retransmissions → PI-ACK (FAIL). The key takeaway for chapter 23: VDL-ACK (Msg 7/13) proves *link* delivery, IFM 5 proves *application* delivery.
- **The register tells the history.** Reading the IALA collection rows chronologically: 1998 (M.1371-1 built-in FIs), 2002 (Seaway, Zeni Lite), 2004 (SN/Circ.236 trials), 2007 (Inland AIS DAC 200), 2010 (Circ.289), 2011 (USCG RDC DAC 366), 2014–2017 (USCG encrypted DAC 366 on Msg 25/26), 2015–2016 (USCG RDC DAC 367 re-issues, STM/Danish route messages), 2019–2021 (USACE satellite weather, Inland revisions), 2022 (VDES proposals), 2023–2025 (China MSA, Rijkswaterstaat). This chronology is a candidate figure.
- **USCG DAC 366 → 367 shift.** Register rows show the US originally registered under DAC 366 (which is one of the US MIDs) and later re-registered under DAC 367 with version numbers; the DAC 366 versions were marked deprecated. The encrypted "Blue Force" family stayed on DAC 366. Why 367 was chosen over 366 is not stated in the register (verify — possibly to separate RDC research messages from USCG operational ones).
- **Why uptake is low (narrative, to be supported).** 33 CFR 164.46 itself notes that most ASMs "require interfacing to an external system that is capable of their portrayal" — the display gap. Combine with: 1 ASM/min cap in US waters; no carriage requirement for ASM display on ECDIS (IEC 61174 displays only AIS targets — verify); Circ.289 being guidance not mandate; Class B CS units cannot transmit Msg 6/8 at all (M.1371-6 Annex 6 limits Class B CS to Msgs 14, 18, 24 — see `r-link-layer.md`). Do **not** quote adoption percentages without a source; candidates to look for are USCG NAIS statistics or papers from the RTCM SC-121 era (verify).
- **Whale Alert / right whale.** The gpsd area-notice vector (MMSI 3669739, a US coast station MMSI, lon −69.86, lat 42.08 = Cape Cod Bay/Stellwagen Bank area) with notice type 0 "Caution Area: Marine mammals habitat" is exactly the right-whale Dynamic Management Area use case developed by the USCG RDC / NOAA / Cornell "Whale Alert" effort. The vector itself is verifiable; the provenance story (dates, partners) must be sourced separately in `r-case-*` dossiers (verify).
- **gpsd's documentation caveat.** The gpsd AIVDM page (v1.58) remains the most-read ASM layout reference for developers but is written against M.1371-4 and against the *draft* DAC 367 specs of ~2011–2013; the register now shows DAC 367 FI 22 at version 2 and FI 33 at version 3, so gpsd/libais layouts may lag (verify by diffing against current IALA entries).
- **Decoder reality.** pyais decodes a fixed set of DAC/FI into named fields and returns everything else as raw `data` bytes; libais raises `DecodeError` for unknown DAC/FI (the handbook should recommend wrapping libais calls and falling back to raw bits). Neither decoder validates the Table 29 slot budget or byte alignment.

## Open questions / (verify)

- Exact text of M.1371-6 A4-4 drafting rules (ordering of position fields; whether "precision" or "EPFD" comes first; whether byte alignment is "should" or "shall") — re-read lines ~2480–2560 before quoting (verify).
- Why the IALA register gives 04/03/2011 as "permitted as from" for Circ.289 area notice FIs 22/23 while the other Circ.289 FIs show 01/06/2010 — corrigendum, or later-added area-notice annex? (verify via IMO docs or IALA entry page).
- SN.1/Circ.289 date: sibling dossier says 2 June 2010; register says 01/06/2010 (verify against the circular's cover page).
- Official IALA ASM Collection URL on iala-aism.org / iala.int (the mirror cites http://www.iala-aism.org/asm; the current site may use https://www.iala.int/…/asm) — fetch and record the live URL plus per-entry page template (verify).
- IALA G1095 edition/date and whether a newer edition exists after 2013 (verify at iala.int product page).
- CESNI/CCNR Inland AIS standard current edition and year, and whether it now defines DAC 200 FI 26 water level v0, FI 25 v1, FI 41/42/44 (verify).
- St. Lawrence Seaway AIS data messaging specification: exact title, revision, URL (verify at greatlakes-seaway.com).
- USCG RDC DAC 367 specification documents (titles/dates for FI 22 v2, 29 v1, 33 v3, 35 v2) — only register rows were seen (verify).
- Which exact DAC/FI pairs pyais 3.2.3 and libais 0.17 decode into named fields — compile from source (`pyais/messages.py` / `libais/src/libais/ais8_*.cpp`) rather than from memory (verify).
- libais `duration_minutes: 2` for a raw 20-minute field; libais `air_pres` 13.11 vs 1310; libais `wave_height` 255.0 vs 25.5; inland draught 2.04 vs 20.4 — determine which decoder is correct in each case against Circ.289 Table and the Inland standard (verify).
- Any published statistics on real-world ASM traffic share (e.g., fraction of Msg 6/8 in NAIS or ORBCOMM feeds) — none located this session (verify; candidates: USCG NAVCEN, RTCM SC-121 reports, Ocean Engineering/Journal of Navigation papers).
- Whether IEC 61174 (ECDIS) or IEC 62288 require portrayal of any ASM (believed no; verify).
- The relationship between Annex 4 IFM numbering and VDES application identifiers (VPFI column in the register) under ITU-R M.2092 (verify in M.2092 and `r-vdes.md`).
- M.1371-6 Table 24 says FI 1 is "discontinued"; confirm whether M.1371-5 already said so or whether -6 changed it (verify against -5 text).

## Candidate figures and worked examples

**Figure 1 — Anatomy of an ASM.** Container message header (Msg 8: 6+2+30+2 = 40 bits) → 16-bit AI (10-bit DAC, 6-bit FI) → application data (≤ 952 bits) → spare for byte alignment. Repeat for Msg 6 (header 88 bits incl. seq no + destination + retransmit), Msg 25 (no AI when "binary data flag" = 0), Msg 26 (20-bit comm-state tail).

**Figure 2 — DAC space map.** Number line 0…1023: 0 test, 1–9 international, 10–999 regional (MID-based; call out 200 inland Europe, 219 Denmark, 235/250 UK, 265 Sweden, 316 Canada, 366/367 USA, 412 China, 710 Brazil), 1000–1023 reserved.

**Figure 3 — Register timeline 1998–2025** (from the IALA collection "permitted as from" dates; see Notes).

**Figure 4 — Addressed-message sequencing** (redraw of M.1371-6 Annex 5 Figures 23–31 as a sequence diagram: App A → VDL A → VDL B → App B, with VDL-ACK, PI-ACK, timeout/retransmit and IFM 5).

**Figure 5 — Capability reply bitmap** (Table 32: 64 FIs × 2 bits).

**Worked example A — Decoding the gpsd area-notice vector by hand.**
Payload `803Ovrh0EP:024`@02PN04da=3V<>N0000`, fill 4 → 200 bits.

| Bits | Field | Binary | Value |
|---|---|---|---|
| 0–5 | Message ID | 001000 | 8 |
| 6–7 | Repeat | 00 | 0 |
| 8–37 | MMSI | …1101111111111011101011 | 3669739 |
| 38–39 | Spare | 00 | 0 |
| 40–49 | DAC | 0000000001 | 1 |
| 50–55 | FI | 010110 | 22 |
| 56–65 | Message linkage ID | 0000001010 | 10 |
| 66–72 | Notice description | 0000000 | 0 (Caution area: marine mammals habitat) |
| 73–76 / 77–81 / 82–86 / 87–92 | Start month / day / hour / minute | 0001 / 00001 / 00101 / 000010 | 1 Jan 05:02 UTC |
| 93–110 | Duration (min) | 000000000000010100 | 20 |
| 111–113 | Sub-area shape | 000 | 0 = circle |
| 114–115 | Scale factor | 01 | ×10 |
| 116–140 | Longitude (25 b, 1/1000′) | 1110000000000100101100101 | −4 191 899 → −69.864983° |
| 141–164 | Latitude (24 b, 1/1000′) | 001001101000011100110001 | 2 524 977 → 42.082950° |
| 165–167 | Precision | 100 | 4 |
| 168–179 | Radius | 001110011110 | 926 → 9 260 m |
| 180–200 | Spare | 0… | 0 |

Teaching points: (i) the AI is the first 16 bits after the 40-bit Msg 8 header; (ii) area-notice coordinates use 1/1000 arc-minute, *not* the 1/10 000′ used by position reports; (iii) scale factor multiplies radius; (iv) duration 20 min — libais's "2" shows why to cross-check decoders.

**Worked example B — Capacity arithmetic.** Msg 8 one-slot budget: 256-bit slot − 24 ramp/training − 8 start flag − 16 CRC − 8 end flag − 24 buffer = 168 data bits → 40 header + 16 AI = 112 bits of application data in one slot (18 six-bit characters of text telegram after the 11-bit sequence number, before byte alignment). Cross-check against Table 29 and `r-link-layer.md` slot layout (verify numbers against Table 29 before publishing).

**Worked example C — Spare-bit "@" artefact.** Show a 1-character text telegram: 11 + 6 = 17 bits → needs 7-bit spare to reach 24; the first 6 zero bits decode as "@", so naive decoders print "A@".

**Worked example D — IFM 2/3/4/5 round-trip.** Station A sends IFM 3 (capability interrogation) to B; B replies with IFM 4 (bitmap showing FI 22 available); A sends an addressed area notice (Msg 6 FI 23) with "acknowledge required"; B's application returns IFM 5 with AI response = 1. Use Table 32/33 bit widths.

**Worked example E — Met/hydro "all sentinels" vector** (pyais test FI 31): demonstrate how to recognise a station transmitting no live sensor data; list each not-available value and its encoding (e.g., pressure 511 → 1 310 hPa; air temp −1024 → −102.4 °C).

**Worked example F — Inland FI 10.** ENI "02103547", 39.0 × 5.0 m, type 8010; discuss the draught unit disagreement and how to resolve it from the Inland standard.

## Recommended use by chapter

- **Ch. 23 (Application-specific messages):** Figures 1, 2, 4, 5; Verified facts rows 1–11 (Annex 4 structure, IFM 0–5, Annex 5 sequencing); Circ.236 → Circ.289 history with the register "deprecated" evidence; 33 CFR 164.46(d)(4) as the only hard regulatory text found; the "display gap" quote.
- **Ch. 43 (Decoding binary payloads):** Worked examples A, B, C, E; decoder-discrepancy rows (duration, pressure, wave height, inland draught); guidance to treat unknown DAC/FI as raw bits; note gpsd doc v1.58 is against M.1371-4 and drafts of DAC 367.
- **Ch. 54 (Regional and inland AIS):** DAC 200 table (incl. discontinued/replaced FIs 23, 24, 40), Seaway DAC 316/366 sub-identifier scheme, USCG DAC 366→367 story, other registrants list; worked example F.
- **Ch. 7 (Whale Alert case study):** Worked example A as the technical appendix of the case; notice type 0 wording; `ais-area-notice` repo as the reference implementation (337 commits).
- **Ch. 60 (VDES and the future):** register rows showing VDE-TER/VDE-SAT and "ASM" physical-link entries (IALA 2022 proposals, STM route message on ASM, China MSA 412) — ASM identifiers are migrating to a multi-link register.
- **Appendix C:** Msg 6/8/25/26 capacity table and IFM 0–5 field tables (Tables 25–28, 32, 33).
- **Appendix D (DAC/FI register snapshot):** reproduce the register rows captured 2026-10-05 with state and "permitted from" columns; cite the official IALA URL once verified.
- **Corrections to PLAN:** MSC.1/Circ.1473 is the AIS *AtoN* policy, not an ASM document; the ASM circular is SN.1/Circ.289. Cite M.1371-6 "Annex 4" (not Annex 5) for ASM. IALA G1029 is legacy; point to G1095 and the ASM Collection.
