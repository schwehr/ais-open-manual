# Dossier: VDES, "AIS 2.0", and other channels used for AIS

**Purpose.** This dossier collects what can be confirmed, as of October 2026,
about the VHF Data Exchange System (VDES): its architecture (AIS + ASM +
VDE-TER + VDE-SAT), the Radio Regulations Appendix 18 channel plan, data
rates and modulations, the satellites that have actually flown VDE-SAT
payloads, the IMO regulatory status (performance standards and SOLAS
amendments adopted at MSC 111 in May 2026), how the marketing phrase
"AIS 2.0" is used, and every channel other than AIS 1/AIS 2 that AIS or its
descendants have used. It feeds **Chapter 69** ("AIS 2.0", VDES, and other
channels: what is real) primarily, and supplies material to **Chapter 12**
(2015–present), **Chapter 28** (RF encoding and channel plan), **Chapter 39**
(satellite AIS — VDE-SAT downlink question), **Chapter 43** (testbeds),
**Chapter 52** (S-100 carriage over VDES), **Chapter 61/64** (VDES security
and authentication), and **Appendix B** (standards register).

> Research-session note. Facts marked *high* were read directly from the
> cited primary page during this session. Facts marked *medium* were
> confirmed by at least two independent web-search summaries that cite the
> named primary sources, but the primary page itself was not opened (IMO's
> site returned HTTP 500 during the session). Items marked *(verify)* could
> not be confirmed.

## Key questions

1. What exactly is VDES, and how do its four components relate to legacy
   AIS? Is AIS "inside" VDES or beside it?
2. Which ITU-R recommendation defines VDES, what are its editions and dates,
   and which edition is current?
3. What is the channel plan — frequencies, channel numbers, bandwidths — for
   AIS 1/2, long-range AIS (75/76), ASM 1/2, VDE-TER and VDE-SAT? Which WRC
   decided what?
4. What data rates and modulations does VDE use, and how does "32× AIS"
   arise?
5. Which satellites have flown VDE-SAT payloads, when, and what did they
   demonstrate? Has any satellite ever transmitted M.1371 AIS downlink
   operationally?
6. What is the IMO carriage status? Is VDES mandated, permitted as an
   alternative to AIS, or neither? What enters into force on 1 Jan 2028?
7. Which IEC test standard will type-approve shipborne VDES equipment?
8. What does "AIS 2.0" mean in vendor marketing vs. in the standards?
9. Which IALA documents are current for VDES (and which were withdrawn)?
10. What security/authentication provisions exist in VDES?
11. What channels, other than AIS 1/2, have ever carried AIS-family traffic
    (regional channels via Message 22, 75/76, ASM 1/2, DSC channel 70 for
    channel management, AMRD channel 2006)?
12. What should a developer or administration design for now?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| ITU-R Recommendation M.2092 landing page | M.2092-0 (10/2015); M.2092-1 (02/2022); **M.2092-2 (02/2026)** | https://www.itu.int/rec/R-REC-M.2092/en | "Technical characteristics for VHF data exchange system in the maritime mobile service"; edition list and dates | Free (ITU-R Recs are free PDFs) |
| ITU-R Recommendation M.1371 landing page | M.1371-5 (02/2014) is the AIS technical characteristics Rec. referenced by VDES | https://www.itu.int/rec/R-REC-M.1371/en | AIS layer definition reused as the VDES AIS component | Free |
| ITU Radio Regulations, Appendix 18 (Ed. 2020/2024) | RR App. 18 incl. footnotes *s)* (ch. 75/76 long-range AIS) and *w)* (VDES channels) | https://www.itu.int/pub/R-REG-RR (volume download) | Table of transmitting frequencies in the VHF maritime mobile band; VDES channels | Free (RR PDF) |
| WRC-15 Resolution 360 (Rev.WRC-15) | Res. 360 | via RR / WRC-15 Final Acts (ITU) | Regulatory provisions for VDES satellite component | Free |
| WRC-19 Final Acts, agenda item 1.9.2 | WRC-19 (Sharm el-Sheikh, Oct–Nov 2019) | https://www.itu.int/pub/R-ACT-WRC.14-2019 | VDE-SAT allocations and App. 18 changes | Free |
| CEPT/ECC summary of App. 18 VDES channels | ECC/CEPT pages | https://www.cept.org/ (ECC maritime pages) | Channel designators 1024/1084/1025/1085/1026/1086, 2024/2084/2025/2085/2026/2086 | Free |
| IMO MSC 111 outcome (13–22 May 2026) | Res. MSC.592(111) (introduction of VDES into IMO framework); Res. MSC.593(111) (Performance standards for shipborne VDES); MSC.1/Circ.1699 (operational guidelines) | https://www.imo.org/en/MediaCentre/MeetingSummaries/Pages/MSC-111th-session.aspx | SOLAS Ch. V amendments permitting VDES as alternative to AIS; entry into force 1 Jan 2028 | Free (summary); IMODOCS for texts |
| DNV / Lloyd's Register / ClassNK / ABS / LISCR statutory summaries of MSC 111 | 2026 | dnv.com, lr.org, classnk.or.jp, eagle.org, liscr.com | Independent restatements of the VDES adoption | Free |
| IALA Guideline G1117 | "VHF Data Exchange System (VDES) Overview" | https://www.iala.int/product/g1117/ | System overview, use cases, shore considerations | Free (IALA docs are free to download with registration) |
| IALA Guideline G1139 | "The Technical Specification of VDES" — **withdrawn/superseded by M.2092** | https://www.iala.int/ (catalogue) | Historical technical spec | Withdrawn |
| IALA Recommendation R1007 | "VDES for shore infrastructure" (verify exact title/edition) | https://www.iala.int/ | Shore-side VDES | Free |
| IALA Guidelines G1192, G1193 | VDES authentication; VDES signal measurement (verify editions) | https://www.iala.int/ | Security and test | Free |
| VDES Alliance | industry association site | https://www.vdes-alliance.org/ | Member list, news on MSC 111, IEC 63514 | Free |
| IEC 63514 (in development as of 2026) | Test standard for shipborne VDES (verify number/stage) | https://webstore.iec.ch/ | Type-approval testing | Paid |
| Space Norway / NSC NorSat-2 | Launched 14 Jul 2017; VDES payload by Kongsberg Seatex; SFL-built | https://www.spacenorway.no/ ; https://www.utias-sfl.net/ | First VDE payload in orbit | Free |
| NorSat-TD | Launched 15 Apr 2023; re-entered May 2025 | https://www.romsenter.no/ | VDES demonstrator, laser comms | Free |
| Sternula-1 | Launched 3 Jan 2023 (Transporter-6); re-entered 7 Jan 2025 | https://sternula.com/ ; https://www.esa.int/ | First commercial VDES satellite (Denmark, MARIOT project) | Free |
| YMIR-1 (AAC Clyde Space / Saab / ORBCOMM) | Launched Nov 2023 (verify exact day) | https://www.aac-clyde.space/ ; https://www.saab.com/ | Bi-directional VDES demo | Free |
| Saab R6 Supreme VDES | product page | https://www.saab.com/ | Class A transponder with ASM/VDE-TER/VDE-SAT | Free |
| CML Microcircuits VDES1000 | product page | https://www.cmlmicro.com/ | SDR module for VDES | Free |

## Verified facts

| Fact | Source (clause/page where possible) | Confidence |
|---|---|---|
| ITU-R M.2092 exists in three editions: M.2092-0 approved 10/2015, M.2092-1 approved 02/2022, M.2092-2 approved 02/2026; managed by ITU-R Study Group 5 (WP 5B). | https://www.itu.int/rec/R-REC-M.2092/en (read directly) | high |
| Title of M.2092: "Technical characteristics for VHF data exchange system in the maritime mobile service". | same | high |
| VDES comprises four functional components: AIS, ASM (application-specific messages), VDE-TER (terrestrial) and VDE-SAT (satellite). | M.2092 scope; IMO MSC 111 summary; IALA G1117 | high |
| AIS 1 = 161.975 MHz (ch. 2087 / "AIS 1"), AIS 2 = 162.025 MHz (ch. 2088 / "AIS 2"). | RR App. 18; M.1371-5 Annex 2 | high |
| ASM 1 = 161.950 MHz (ch. 2027) and ASM 2 = 162.000 MHz (ch. 2028) are designated for application-specific messages, removing ASM load from AIS 1/2. | RR App. 18 (WRC-15 changes); CEPT summary | high |
| Channels 75 (156.775 MHz) and 76 (156.825 MHz) — the guard channels adjacent to ch. 16 — are used for long-range AIS (Message 27) reception by satellites (App. 18 footnote *s)*). | RR App. 18; M.1371-5 Annex 4 | high |
| VDES channels per App. 18 footnote *w)*: 157.1875–157.3375 MHz (lower leg) and 161.7875–161.9375 MHz (upper leg); designators 24/84/25/85/26/86, 1024/1084/1025/1085/1026/1086, 2024/2084/2025/2085/2026/2086; mergeable into 50, 100 or 150 kHz channels. | CEPT/ECC and Iceland (fjarskiptastofa.is) restatements of App. 18 | medium-high |
| Of these, 1026/1086 and 2026/2086 are dedicated to ship↔satellite (VDE-SAT) and not used terrestrially; 1024/1084/1025/1085 and 2024/2084/2025/2085 are terrestrial with VDE-SAT allowed on a no-constraint basis. | same | medium |
| 1024 = 157.200 MHz, 1084 = 157.225 MHz (ship→shore); 2024 = 161.800 MHz, 2084 = 161.825 MHz (shore→ship / ship↔ship). | App. 18 arithmetic (25 kHz raster) and multiple restatements | medium-high |
| WRC-15 Resolution 360 (Rev.WRC-15) set the study framework for a VDES satellite component; WRC-19 agenda item 1.9.2 made the allocations and App. 18 changes enabling VDE-SAT. | ITU WRC pages; IAF/ITU summaries | medium-high |
| Shipboard VHF installations must comply with the revised App. 18 channel arrangement by the first radio survey on or after 1 January 2028 (regional administrations may require earlier). | CEPT; KR / class circulars | medium |
| AIS link rate is 9,600 bit/s GMSK in 25 kHz; VDE-TER supports 25/50/100 kHz channel bandwidths with π/4-QPSK, 8PSK and 16QAM and adaptive modulation/coding; maximum VDE-TER rate ≈ 307.2 kbit/s on a 100 kHz channel, hence the "32× AIS" claim (307.2/9.6 = 32). | M.2092 Annex 2/3 (VDE-TER); IALA G1117; vendor literature | medium-high (rate figure widely quoted; confirm against M.2092-2 tables before print) |
| NorSat-2 launched 14 July 2017; 16 kg microsatellite built by UTIAS/SFL for the Norwegian Space Centre/Space Norway; carried the first VDE payload in orbit (Kongsberg Seatex) and a deployable crossed-Yagi VHF antenna. | SFL and Space Norway pages (via search) | medium-high |
| NorSat-TD launched 15 April 2023 with an upgraded VDES payload and the SmallCAT laser terminal; re-entered May 2025 after elevated solar-activity drag. | Norwegian Space Agency (via search) | medium |
| Sternula-1 launched 3 January 2023 on SpaceX Transporter-6; Denmark's first commercial satellite; 6U; VDES transceiver payload; MARIOT project partners incl. Aalborg University, GateHouse SatCom, Satlab, DMI, Space Inventor; re-entered 7 January 2025. | sternula.com, ESA, ufsn.dk (via search) | medium-high |
| YMIR-1, built by AAC Clyde Space with a Saab VDES payload (ORBCOMM involvement), launched November 2023 to demonstrate bi-directional VDES from orbit. | aac-clyde.space, saab.com (via search) | medium |
| **No satellite has ever operated an M.1371 AIS *downlink* as a service; satellites receive AIS (SAT-AIS) and, since 2017, a handful have transmitted VDE-SAT test downlinks.** | Negative claim; consistent with all sources reviewed; see r-satellite-ais.md | medium (negative) |
| IMO MSC 111 (13–22 May 2026) adopted amendments to SOLAS Chapter V and the HSC Codes permitting **voluntary carriage of VDES as an alternative to AIS**; adopted Res. MSC.592(111) (introduction of VDES into the IMO regulatory framework) and Res. MSC.593(111) "Performance standards for shipborne VHF data exchange system (VDES)"; approved MSC.1/Circ.1699 "Guidelines for the onboard operational use of shipborne VDES". | IMO MSC 111 meeting summary (imo.org, cited by three independent search results); DNV, LR, ClassNK, ABS, LISCR statutory news | medium-high (resolution numbers should be checked against IMODOCS before print) |
| The SOLAS amendments are expected to enter into force **1 January 2028**. | same | medium-high |
| IMO's framing: the AIS component of VDES satisfies the AIS carriage requirement; VDES functionality beyond the AIS component is **not** a substitute for required AIS; references to "AIS" in instruments may be read as "AIS or VDES". | IMO summary; LISCR | medium |
| IEC is developing IEC 63514 as the shipborne VDES test standard to support type approval before 2028. | VDES Alliance news (via search) | medium (verify IEC number and stage) |
| IALA G1117 "VDES Overview" is current; IALA G1139 (technical specification) has been withdrawn as superseded by M.2092-1/-2. | IALA catalogue and e-navigation.nl (via search) | medium |
| IALA has published VDES-specific guidance including G1192 (VDES authentication) and G1193 (VDES signal measurement) and Recommendation R1007 (VDES shore infrastructure). | iala.int (via search) | medium (verify exact titles/editions) |
| "AIS 2.0" is a vendor marketing phrase (notably Sternula, "AIS 2.0/VDES") with no standing in ITU-R, IMO, IEC or IALA documents; the standards term is VDES. | sternula.com; ITU/IMO document titles | high (as a statement about nomenclature) |
| Some vendor copy states VDES "becomes a SOLAS carriage requirement from 1 January 2028"; the IMO decision is **permissive** (alternative to AIS), not a mandate. | Compare vendor summaries vs IMO/DNV/LISCR statements | medium-high |
| Saab R6 Supreme VDES: SDR Class A transponder claimed to support AIS, ASM, VDE-TER, VDE-SAT, DSC and "secure AIS", compliant with M.2092-1, IEC 61162-450 dual LAN. | saab.com product page (via search) | medium |
| CML Microcircuits VDES1000 is an SDR module marketed as the core of a multichannel Class A/ASM/VDE transceiver. | cmlmicro.com (via search) | medium |
| Kongsberg Seatex (now Kongsberg Discovery) supplies VDES base stations (e.g., BS610 family) used in R-Mode and e-navigation trials. | kongsberg.com (via search) | medium (verify model number) |
| AMRD Group B devices (e.g., fishing-gear markers) using AIS technology are directed to **channel 2006 (160.900 MHz)**, not AIS 1/2 (see r-special-ais.md). | ITU-R M.2135-1 (02/2023); RR App. 18 | high |

## Notes and quotes

- **Nomenclature.** ITU-R M.2092 defines VDES as the system; the "AIS" of
  M.1371 is retained unchanged as a component. VDE-TER and VDE-SAT are the new
  high-rate parts; ASM moves application-specific traffic (Messages 6/8/25/26
  content) to its own two channels so that AIS 1/2 are reserved for the
  position/static reports that collision avoidance depends on. Chapter 69
  should make this point first: VDES does not change AIS 1/2.

- **Edition history matters.** The PLAN cites "M.2092-1" throughout. As of
  February 2026 the current edition is **M.2092-2**. Any clause-level citation
  must be checked against -2; the Saab product page still claims -1
  compliance.

- **"Expected to enter into force 1 January 2028"** (IMO summary language for
  MSC 111 SOLAS amendments). This is the tacit-acceptance date; it is not a
  carriage mandate. The relevant sentence from LISCR's summary (paraphrased):
  the amendments permit voluntary carriage of VDES as an alternative to AIS,
  with the understanding that AIS is one of the four components of VDES.

- **IMO on substitution** (paraphrase of IMO MSC 111 summary): any VDES
  functionalities beyond the AIS component are not to be considered a
  substitute for the required AIS equipment. This matters for Chapter 16/69:
  a ship with a VDES transponder is still "carrying AIS".

- **Capacity arithmetic.** 307.2 kbit/s ÷ 9.6 kbit/s = 32. Vendors quote
  "32×"; the honest comparison is per 100 kHz of spectrum vs per 25 kHz
  channel, i.e., a 4× bandwidth increase and an 8× spectral-efficiency increase
  (16QAM with coding vs GMSK). Make this a Worked example.

- **Satellite history (VDE-SAT).** NorSat-2 (2017) was the first VDE payload;
  NorSat-TD (2023) and Sternula-1 (2023) extended the demonstrations; YMIR-1
  (late 2023) added a Saab payload. Both Sternula-1 and NorSat-TD re-entered
  in 2025, so as of this writing the operational VDE-SAT fleet is small and in
  flux. Chapter 69 should carry an "as of October 2026" table.

- **IALA G1139 withdrawal.** IALA used G1139 to carry the detailed VDES
  technical specification while ITU-R work matured; once M.2092-1 contained
  the full specification, IALA withdrew G1139. Cite M.2092 rather than G1139.

- **Channel 2028 arithmetic.** App. 18 channel numbers in the 20xx series
  denote the upper-leg (ship receive) frequency of the former duplex pair,
  e.g., 2027 = 161.950, 2028 = 162.000; the 10xx series denotes the lower leg
  (157.xxx MHz). AIS 1/2 are formally 2087/2088 in this scheme.

- **Other channels AIS has used.** (a) Regional channels via Message 22 /
  DSC channel 70 channel-management commands (M.1371-5 Annex 2 §4.1 and
  Annex 8 Message 22) — e.g., the USCG's 2010 Safety Alert on channel
  management confusion (see NAVCEN FAQ item on Message 22). (b) 75/76 for
  Message 27 long-range. (c) ASM 1/2 for Messages 6/8/25/26 in VDES-era
  equipment. (d) Channel 2006 (160.900 MHz) for AMRD Group B — AIS-technology
  devices that are not navigation safety devices. (e) DSC channel 70
  (156.525 MHz) for AIS channel management (Message 22 equivalent sent by DSC).

## Open questions / (verify)

- Confirm resolution numbers MSC.592(111) and MSC.593(111) and circular
  MSC.1/Circ.1699 directly in IMODOCS; IMO's site was unreachable (HTTP 500)
  during this session. (verify)
- Confirm the exact M.2092-2 tables for VDE-TER maximum user data rate
  (307.2 kbit/s is the widely quoted figure for the 100 kHz 16QAM mode) and
  the VDE-SAT rates. (verify)
- IEC 63514: confirm the number, title and committee stage (CD/CDV/FDIS) in
  2026. (verify)
- YMIR-1 exact launch date (November 2023 per AAC Clyde Space) and its
  current operational status. (verify)
- Whether any VDE-SAT satellite is providing *commercial* service in 2026
  (Sternula's follow-on constellation plans). (verify)
- IALA R1007, G1192, G1193 exact titles and edition dates. (verify)
- WRC-23 outcomes touching VDES (if any) — not confirmed in this session;
  do not state that WRC-23 changed VDES provisions without checking the
  WRC-23 Final Acts. (verify)
- Whether PLAN's statement "VDE channels (verify numbers)" in Chapter 28
  should list the 24/84/25/85/26/86 duplex designators as well as the
  10xx/20xx simplex designators — confirm App. 18 Ed. 2024 text. (verify)

## Candidate figures and worked examples

- **Figure 69-1.** VDES component stack: AIS (M.1371) / ASM / VDE-TER /
  VDE-SAT, with the channel map underneath (156.775–162.025 MHz) showing
  75, 76, 1024–1026, 1084–1086, 2024–2026, 2084–2086, 2027/2028 (ASM),
  2087/2088 (AIS). Redraw from App. 18; do not copy ITU figures.
- **Figure 69-2.** Timeline 2012–2028: IALA/ITU VDES concept → M.2092-0 (2015)
  → NorSat-2 (2017) → WRC-19 VDE-SAT → M.2092-1 (2022) → Sternula-1, NorSat-TD,
  YMIR-1 (2023) → M.2092-2 (Feb 2026) → MSC 111 (May 2026) → SOLAS amendments
  in force (1 Jan 2028).
- **Worked example 69-A.** "32×": compute 307.2/9.6; then normalise per kHz
  to show it is 8× spectral efficiency × 4× bandwidth; discuss that VDE-TER is
  shared and scheduled, not a per-ship rate.
- **Worked example 69-B.** Channel-number arithmetic: from App. 18 channel
  2028 derive 162.000 MHz; from 1024 derive 157.200 MHz; from 75 derive
  156.775 MHz.
- **Table 69-1.** Satellites with VDE-SAT payloads (name, operator, launch,
  payload supplier, status as of Oct 2026).
- **Table 69-2.** "What is real" matrix: claim (e.g., "AIS 2.0 mandatory 2028",
  "32× bandwidth", "authenticated AIS", "global two-way coverage") vs status
  (adopted / permitted / demonstrated / proposed / marketing).
- **Box: Definitions that bite.** "VDES" vs "AIS 2.0" vs "VDE" vs "ASM".

## Recommended use by chapter

- **Ch. 69** — core: architecture, channel plan, data rates, satellites,
  MSC 111 outcome (permissive alternative, 1 Jan 2028), IEC 63514, "AIS 2.0"
  as marketing, other channels list, design guidance ("keep AIS 1/2
  decoding; add ASM 1/2 receive; treat VDE as a separate data bearer").
- **Ch. 12** — add M.2092-2 (Feb 2026) and MSC 111 (May 2026) to the
  2015–present narrative; correct "M.2092, 2015; WRC-15/19/23" to specify
  what each WRC did.
- **Ch. 28** — channel table including ASM 1/2 (161.950/162.000), 75/76
  (156.775/156.825) and the VDE designators; note VDE modulations differ from
  GMSK.
- **Ch. 39** — "have satellites ever transmitted AIS?": no M.1371 downlink;
  VDE-SAT downlink tests from NorSat-2 (2017), NorSat-TD and Sternula-1
  (2023), YMIR-1 (2023).
- **Ch. 43** — VDES testbeds (Norway, Baltic R-Mode base stations, MARIOT).
- **Ch. 52** — S-100 product delivery over VDE as the planned bearer; cite
  IALA G1117.
- **Ch. 61/64** — VDES authentication guidance (IALA G1192) and M.2092
  security provisions; keep claims cautious until texts are read.
- **Ch. 68** — AMRD Group B on channel 2006 (cross-reference r-special-ais).
- **Appendix B** — register entries: M.2092-0/-1/-2; RR App. 18; Res. 360;
  MSC.592(111); MSC.593(111); MSC.1/Circ.1699; IEC 63514; IALA G1117, R1007,
  G1192, G1193 (G1139 withdrawn).
