# Dossier: Failure modes of AIS hardware, software, and configuration

**Purpose.** This dossier collects what can be confirmed, as of October 2026,
about the ways AIS stations and the pipelines that consume their output fail:
operator misconfiguration (default/invalid MMSIs, wrong dimensions and
reference points, stale voyage data, heading sensor absent), GNSS and timing
failures (the 2008 PRN-32 incident, the 2019 GPS week-number rollover and
device-specific later rollovers), channel-management mishaps (USCG Safety
Alert 07-10), EMI from LED lighting (USCG Safety Alert 13-18), Class B "CS"
slot starvation, and the published error-rate studies (Harati-Mokhtari et al.
2007 onward). It also records the regulatory testing regime (MSC.1/Circ.1252
annual test; SOLAS V/18.9) and the US verification services (USCG VIVS/AVIS)
that are designed to catch these faults. It feeds **Chapter 36** (Failure modes
of AIS hardware and software) primarily, and supplies material to **Chapter 13**
(invalid MMSIs), **Chapter 24** (timing failures), **Chapter 25** (GNSS-denied
behaviour), **Chapter 31** (noise sources), **Chapter 36/47** (error taxonomy
and data cleaning), **Chapter 53** (mariner training), **Chapter 55** (incidents),
and **Appendix D** (sentinel values).

> Research-session note. Facts marked *high* were read directly from the
> cited URL during this session (2026-10-05) or confirmed through the Crossref
> API record for the DOI shown. Facts marked *medium* come from a search-engine
> summary that quoted the primary document but where the document itself was
> not opened (paywall, PDF not fetched, or 403). Anything else is *(verify)*.

## Key questions

1. What fraction of AIS reports contain erroneous data, by field, and how has
   that changed since the first studies in 2005–2007?
2. Which failure modes are *configuration* faults (human), which are *sensor*
   faults (GNSS, gyro, ROT), which are *RF/hardware* faults (antenna, feeder,
   EMI, desense), and which are *link-layer* effects (Class B CS starvation,
   channel-management mis-commands)?
3. What is the detection signature of each failure in received data
   (sentinels such as heading 511, MMSI patterns, position jumps, missing
   Message 5, stale ETA), so that chapter 36 can give a usable catalogue?
4. What official notices document real-world failures (USCG safety alerts,
   NAVCEN FAQ, MCA MGNs, manufacturer bulletins)?
5. What does the mandatory annual test (MSC.1/Circ.1252) actually check, and
   what does it *not* catch?
6. What firmware/date bugs have hit AIS (GPS PRN-32 in 2008; week-number
   rollover 2019 and vendor-specific epochs later)?
7. What do accident investigators say about AIS data errors in real
   casualties (MAIB Safety Digests, NTSB)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Harati-Mokhtari, Wall, Brooks & Wang | *J. Navig.* 60(3):373–389, 2007, DOI 10.1017/S0373463307004298 | https://doi.org/10.1017/S0373463307004298 | First large published AIS data-reliability study (400,059 reports, 1–17 Mar 2005); human-error framing; recommendation to standardize ship-type/nav-status options | Paid (Cambridge) |
| USCG NAVCEN, "AIS Frequently Asked Questions" | web page, accessed 2026-10-05 | https://www.navcen.uscg.gov/ais-frequently-asked-questions | Invalid MMSIs in use; Nauticast 1193046/"NAUT" default; PRN-32 (2008) failure; LED EMI (Safety Alert 13-18); channel management (Safety Alert 07-10); VIVS verification service; USCG AIS Encoding Guidance; inspection checklist | Free |
| USCG Safety Alert 07-10 | "Caution to AIS Users", 2010 (excerpt PDF linked from FAQ) | https://www.navcen.uscg.gov/sites/default/files/pdf/AIS/USCG_Safety_Alert_07_10_Excerpts.pdf | AIS units inadvertently commanded onto wrong regional channels in the mid-Atlantic; corrective channel-management broadcasts | Free |
| USCG Marine Safety Alert 13-18 | 15 Aug 2018 | (linked from NAVCEN FAQ; USCG safety-alert archive) | LED lighting EMI degrading VHF/DSC/AIS reception; squelch test procedure | Free |
| USCG Safety Alert 5-10 | 2010 | https://www.navcen.uscg.gov/sites/default/files/pdf/AIS/0510.pdf | AIS safety-related text and AIS MOB devices are not monitored as GMDSS alerts | Free |
| IMO MSC.1/Circ.1252 | "Guidelines on annual testing of the Automatic Identification System (AIS)", 22 Oct 2007 | IMO docs (via IMODOCS / flag-state reprints) | Annual test content: installation details, static data, dynamic data from sensors, voyage data, RF measurements, on-air test, model test report form | Free (circular) |
| IMO Res. MSC.308(88) | SOLAS amendments adopted 3 Dec 2010 (verify date), adding SOLAS V/18.9 annual AIS test | IMO | Makes the annual AIS test mandatory (in force 1 Jan 2012 (verify)) | Free |
| GPS.gov, GPS Week Number Rollover | gps.gov page | https://www.gps.gov/support/user/rollover/ | WNRO on 6 Apr 2019; 10-bit week counter; 13-bit in modernized signals | Free |
| JRC news notice on GPS week rollover for JHS-182/JHS-183 AIS | 2023-09-15 notice (verify) | https://www.jrc.co.jp/en/news/2023/0915-1/ | Device-specific rollover on 3 Aug 2025; clock reverts to 23 Jan 2005; positioning unaffected; software upgrade required | Free |
| MCA MGN 324 (M+F) | "Radio: Operational Guidance on the Use of VHF Radio and Automatic Identification Systems (AIS) at Sea" (edition/amendment (verify)) | https://www.gov.uk/government/publications/mgn-324-mf-radio-operational-guidance-on-the-use-of-vhf-radio-and-ais-at-sea | AIS limitations; not all vessels carry AIS; Class B slot behaviour; AIS not a substitute for COLREG lookout | Free |
| Winkler, D. (USCG NAVCEN), "AIS Data Quality and the Authoritative Vessel Identification Service (AVIS)" | presentation to National GMDSS Implementation Task Force, 10 Jan 2012 | (linked from NAVCEN FAQ as "Winkler@GMDSS_TF_(2012-01-11)_AIS_Data_Quality") | US shore-side view of static-data error rates and the AVIS/VIVS correction service | Free (PDF) |
| Last, Hering-Bertram & Linsen | *Ocean Eng.* 100:83–89, 2015, DOI 10.1016/j.oceaneng.2015.03.017 | https://doi.org/10.1016/j.oceaneng.2015.03.017 | How AIS antenna setup affects AIS signal quality (installation as failure cause) | Paid |
| Last, Bahlke, Hering-Bertram & Linsen | *J. Navig.* 67:791–809, 2014, DOI 10.1017/S0373463314000253 | https://doi.org/10.1017/S0373463314000253 | Comprehensive analysis of AIS data quality for movement prediction (field-level error statistics) | Paid |
| Banyś, Noack & Gewies | *Annual of Navigation* 19:5–16, 2012, DOI 10.2478/v10367-012-0001-0 | https://doi.org/10.2478/v10367-012-0001-0 | Assessment of AIS position-report reliability (DLR) | Free |
| Bošnjak, Šimunović & Kavran | *Trans. Marit. Sci.* 1(2):77–84, 2012, DOI 10.7225/toms.v01.n02.002 | https://doi.org/10.7225/toms.v01.n02.002 | AIS error analysis in maritime traffic | Free |
| Iphar, Ray & Napoli | *Expert Syst. Appl.* 147:113219, 2020, DOI 10.1016/j.eswa.2020.113219 | https://doi.org/10.1016/j.eswa.2020.113219 | Data-integrity assessment framework for AIS (field-level consistency rules) | Paid |
| Iphar, Ray & Napoli | OCEANS 2019 Marseille, DOI 10.1109/OCEANSE.2019.8867559 | https://doi.org/10.1109/OCEANSE.2019.8867559 | "Uses and Misuses of the AIS" — taxonomy of errors and falsifications | Paid |
| Emmens, Amrit, Abdi & Ghosh | *Expert Syst. Appl.* 178:114975, 2021, DOI 10.1016/j.eswa.2021.114975 | https://doi.org/10.1016/j.eswa.2021.114975 | "The promises and perils of AIS data" — review of data-quality issues | Paid |
| Mazzarella, Vespe, Alessandrini, Tarchi, Aulicino & Vollero | *Expert Syst. Appl.* 78:110–123, 2017, DOI 10.1016/j.eswa.2017.02.011 | https://doi.org/10.1016/j.eswa.2017.02.011 | Distinguishing intentional AIS on/off switching from reception loss using reception-probability models | Paid |
| Kessler, Craiger & Haass | *TransNav* 12(3):429–437, 2018, DOI 10.12716/1001.12.03.01 | https://doi.org/10.12716/1001.12.03.01 | Taxonomy of AIS failures/attacks (useful to separate fault from attack) | Free |
| Gao Mingju et al. | EIDWT 2013, DOI 10.1109/EIDWT.2013.120 | https://doi.org/10.1109/EIDWT.2013.120 | A packet-error-rate measurement system for AIS messages (test-bench view) | Paid |
| ITU-R M.1371-5 | 2014 | https://www.itu.int/rec/R-REC-M.1371 | Sentinel values (heading 511, SOG 1023, COG 3600, lat 91°, lon 181°, ROT −128, timestamp 60–63), reporting intervals, Class B CS behaviour | Free |
| 33 CFR 164.46 | eCFR current | https://www.ecfr.gov/current/title-33/chapter-I/subchapter-P/part-164/section-164.46 | US duty to keep AIS "in effective operating condition" and broadcasting accurately; penalties | Free |
| 47 CFR 80.231 | eCFR current | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-80/subpart-F/section-80.231 | Class B devices not user-configurable in the US; static data entered by vendor/technician | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Harati-Mokhtari et al. (2007) is in *J. Navig.* vol. 60, issue 3, pp. 373–389, published online 9 Aug 2007, DOI 10.1017/S0373463307004298; authors Harati-Mokhtari A., Wall A., Brooks P., Wang J. | Crossref record for the DOI (read via api.crossref.org) | high |
| The study analysed 400,059 AIS reports collected 1–17 March 2005 and found about 8 % of transmissions contained erroneous data (≈1 in 14) across MMSI, IMO number, position, COG, SOG and other fields; it recommends standardizing ship-type and nav-status options across manufacturers | Search summary of the Cambridge abstract and citing papers (article page returned HTTP 500 during session) | medium |
| USCG NAVCEN lists invalid MMSIs seen on air: 111111111, 123456789, 00000001, US documentation numbers; a valid ship MMSI starts with 2–7; US-assigned MMSIs begin 338, 366, 367, 368 or 369 | https://www.navcen.uscg.gov/ais-frequently-asked-questions (FAQ 12) | high |
| MMSI 1193046 and vessel name "NAUT" are a Nauticast factory default; NAVCEN asks users encountering it to notify the vessel; a Nauticast "AIS-MMSI Technical Bulletin" exists | Same FAQ (FAQ 12) | high |
| Ships using the same MMSI appear as one target "jumping from position-to-position" on ECDIS/radar/MKD displays | Same FAQ (FAQ 12) | high |
| On 27 Feb 2008 the GPS constellation grew to 32 satellites (PRN 32); some older, non-USCG-type-approved AIS units whose GPS did not comply with IS-GPS-200 could not handle PRN 32, lost position and stopped broadcasting valid position reports while still receiving and sending text messages | Same FAQ (FAQ 10) | high |
| USCG operates a Vessel Information Verification Service (VIVS) that cross-references AIS static data received by NAIS in the last 30 days (MMSI, name, call sign, official number, dimensions, draught, ship type) against IMO, FCC ULS and NVDC records and flags discrepancies against the "USCG AIS Encoding Guidance" | Same FAQ (FAQ 2, 11, 12) | high |
| Each USCG type-approved AIS has a built-in integrity tester, so sending "TEST" text messages is unnecessary | Same FAQ (FAQ 2) | high |
| Per 47 CFR 80.231, US-sold Class B devices are not user-configurable; Class A static data is password-protected | Same FAQ (FAQ 2), citing the CFR | high |
| 33 CFR 164.46 requires AIS to be installed per SN/Circ.227 or NMEA 0400 and maintained "in effective operating condition"; failure can incur civil penalties under 46 U.S.C. 70119 | Same FAQ (FAQ 2) | high |
| LED lighting may interfere with AIS and VHF; see USCG Safety Alert 13-18 | Same FAQ (FAQ 13) | high |
| Safety Alert 13-18 was issued 15 Aug 2018, describes degraded VHF/DSC/AIS reception from LED fixtures and gives a squelch-threshold test (turn LEDs off, open squelch to noise, close to threshold, turn LEDs on) | Search summary quoting the alert (Practical Sailor, IMCA reprints) | medium |
| AIS channel-management commands persist until overridden by another command for the same region or manually erased; resetting the unit does not necessarily restore default channels; USCG Safety Alert 07-10 covers an incident where units were mis-commanded | Same FAQ (FAQ 19) and linked PDF title | high (existence), medium (incident detail) |
| Safety Alert 07-10 concerned units in the MD/DE/PA/NJ/NY area that were switched off the default channels by inadvertent Message 22 broadcasts; USCG re-broadcast corrective channel-management messages | Search summary of the alert | medium |
| AIS safety-related text messages and AIS MOB devices are not monitored as GMDSS alerts by the USCG (Safety Alert 5-10); COMSAR/Circ.46 covers AIS SRM in distress | Same FAQ (FAQ 20) | high |
| USCG operates an "AIS Problem Report" form for ghost/fake targets and malfunctions | Same FAQ (FAQ 22) | high |
| Position reports are sent every 2–10 s under way (speed dependent) or every 3 min at anchor; static/voyage reports every 6 min — hence a target often appears without a name for minutes | Same FAQ (FAQ 11) | high |
| MSC.1/Circ.1252 (22 Oct 2007) specifies the annual AIS test: installation details (antenna layout, configuration report, interconnection, power, pilot plug), static information, dynamic information from sensors, voyage data, RF performance measurements, on-air test; report in English/French/Spanish, retained on board | Search summary of the circular text | medium |
| GPS week-number rollover occurred 6 Apr 2019 (10-bit week counter; modernized CNAV uses 13 bits) | https://www.gps.gov/support/user/rollover/ (via search summary) | medium-high |
| JRC published a notice that JHS-182/JHS-183 AIS units have a device-specific rollover on 3 Aug 2025 after which the clock reverts to 23 Jan 2005; positioning unaffected; software upgrade required | Search summary citing https://www.jrc.co.jp/en/news/2023/0915-1/ | medium |
| Papers verifying AIS-reception-based detection of intentional switch-off exist (Mazzarella et al. 2017, DOI 10.1016/j.eswa.2017.02.011) | Crossref record | high |
| Last et al. 2015 (*Ocean Eng.* 100:83–89) studied how antenna setup affects AIS signal quality | Crossref record | high |
| Banyś, Noack & Gewies 2012 (*Annual of Navigation* 19:5–16) assessed AIS position-report reliability | Crossref record | high |
| Bošnjak et al. 2012 (*Trans. Marit. Sci.* 1(2):77–84) published an AIS error analysis | Crossref record | high |
| Iphar, Ray & Napoli 2020 (*ESWA* 147:113219) and 2019 (OCEANS Marseille) exist with the titles given | Crossref record | high |
| Emmens et al. 2021 (*ESWA* 178:114975) exists | Crossref record | high |
| Kessler, Craiger & Haass 2018 (*TransNav* 12(3):429–437) exists | Crossref record | high |

## Notes and quotes

**USCG NAVCEN FAQ (read 2026-10-05).** "AIS users are required to operate
their unit with a valid MMSI, unfortunately, some users neglect to do so (for
example, use: 111111111, 123456789, 00000001, their U.S. documentation number,
etc)." And on the PRN-32 episode: "some (non-USCG type approved) AIS
units—particularly old equipment which is non-compliant with the GPS interface
standard (IS-GPS-200)—cannot recognize this additional satellite and
subsequently are unable to calculate a position and broadcast a valid AIS
Position Report." Also: "AIS by design, is an open, non-proprietary,
unencrypted, unprotected radio system … So technically it can be spoofed—so
trust, but, verify."

**Why the 2008 PRN-32 story matters.** It is the earliest documented case of a
*software* fault in the internal GNSS causing silent loss of AIS position
reporting fleet-wide for a subset of hardware — eleven years before the 2019
WNRO. It establishes the pattern chapter 36 should describe: receive works,
text works, but position reports stop or carry the "not available" sentinels.

**Harati-Mokhtari's framing.** The paper's contribution is less the 8 % figure
than its argument that AIS was "bolted on" to the bridge and that fields that
depend on manual entry (ship type, dimensions, nav status, draught, destination,
ETA) will be wrong at a rate governed by human-factors, not electronics. The
authors adapt the Swiss-cheese accident model to AIS. Later work (Last et al.
2014; Iphar et al. 2020; Emmens et al. 2021) refines the per-field view.

**Class B CS starvation (narrative).** M.1371 requires Class B CS stations to
listen for carrier in a window before their intended slot and to defer if the
slot is in use; Class A SOTDMA stations may also reuse slots. The practical
consequence, stated in MCA MGN 324 and in manufacturer FAQs, is that in very
dense cells a Class B CS unit's reports may be delayed or dropped. Chapter 36
should present this as *designed behaviour*, not a malfunction, and link to
Chapter 21/30 for the slot arithmetic. No peer-reviewed field measurement of
the drop rate as a function of slot occupancy was located in this session —
see Open questions.

**Annual test coverage.** MSC.1/Circ.1252 is a checklist test: it verifies
programming, sensor connections, RF power/frequency, and an on-air exchange.
It does *not* test behaviour under slot congestion, under GNSS loss, EMI
immunity in service, or firmware date handling. Many of the failure modes
below are therefore invisible to the annual test and only show up in
shore-side data (hence VIVS/AVIS in the US).

**Failure catalogue skeleton (for Chapter 36).** Each entry: cause → on-air
signature → how to detect → who can fix.

| # | Failure | On-air signature | Detect with | Fixer |
|---|---|---|---|---|
| 1 | Default/invalid MMSI (0, 1193046, 123456789, 111111111, repeated digits, documentation number) | MMSI fails ITU-R M.585 pattern; many ships share one MMSI; targets "jump" | MMSI regex + MID table; duplicate-MMSI distance test | Installer/vendor (Class B locked in US) |
| 2 | Wrong dimensions / reference point (A,B,C,D) | Length/beam implausible for type; hull drawn off the GNSS position; A=B=C=D=0 | Compare to registry (IMO/Equasis); check footprint vs berth | Installer |
| 3 | Stale destination/ETA/draught/nav status | Destination unchanged across voyages; nav status "under way using engine" while at anchor for days; ETA in the past | Voyage segmentation vs port-call detection | Crew |
| 4 | Heading sensor absent or not connected | True heading = 511 while SOG > a few kn; or heading constant | Count 511 reports per MMSI; heading–COG residual | Installer (gyro/THD interface) |
| 5 | ROT sensor absent / wrong | ROT = −128 (not available) or ±127 (turning > 5°/30 s, no sensor) | Field census | Installer |
| 6 | GNSS fix lost (internal and external) | Position 91°/181°; timestamp 61/62/63; position-accuracy flag 0; eventual cessation of transmission per class rules | Sentinel census; sync-state in comm-state | Crew/service |
| 7 | GNSS firmware bug (PRN-32 2008; WNRO 2019; vendor epochs 2025) | Valid receive, valid text, but no valid position; or date 19.6 years wrong in Message 4/11 or interface | Fleet-wide onset on a known date | Vendor firmware |
| 8 | Channel management mis-command (Safety Alert 07-10) | Unit silent on AIS1/AIS2 but transmitting on regional channels; receivers on default channels see nothing | Compare received message counts before/after Message 22 events | Authority re-broadcast; user manual override |
| 9 | LED / switch-mode EMI (Safety Alert 13-18) | Own-ship reception range collapses with lights on; no change in transmit | Squelch test; spectrum view; range vs lighting state | Owner (fixture replacement, separation) |
| 10 | Antenna/feeder fault (VSWR) | Range asymmetry; Class A VSWR alarm (IEC 61993-2 (verify clause)); many "lost target" alarms | VNA/VSWR check; compare with expected range | Service |
| 11 | Class B CS slot starvation | Irregular report intervals >> 30 s in dense cells; message counts per minute saturate | Interval histograms by cell occupancy | None (design); upgrade to Class B SO/Class A |
| 12 | Silent/receive-only mode left on | Target disappears while clearly present visually/radar | Cross-sensor check | Crew |
| 13 | Pilot-plug / NMEA multiplexer faults | Truncated or interleaved sentences; fragment reassembly failures; checksum errors | Decoder error counters | Service |
| 14 | Shore-network duplication and reordering | Same message from several receivers with different receive timestamps; out-of-order delivery | Dedupe on payload+slot; use message timestamp field | Aggregator |
| 15 | Satellite latency / aliasing | Positions hours old delivered later; apparent teleportation when merged with terrestrial | Keep receive-time vs message-time separately | Analyst |
| 16 | Decoder crash on malformed input | Pipeline stalls on specific sentences | Fuzzing; Balduzzi 2014-style malformed-message tests | Software maintainers |

## Open questions / (verify)

- (verify) Exact text and date of USCG Safety Alert 07-10; obtain the PDF at the
  NAVCEN URL above and quote the affected region list.
- (verify) Exact wording and date (15 Aug 2018) of Marine Safety Alert 13-18;
  obtain from the USCG CG-INV safety-alert archive.
- (verify) Adoption date of MSC.308(88) and entry into force of SOLAS V/18.9
  (annual AIS test). Confirm that Reg. 18.9 is the correct paragraph.
- (verify) Harati-Mokhtari per-field error percentages (the 8 % overall figure
  needs the breakdown table from the paper; also confirm the receiver location,
  which secondary sources give as the UK coast).
- (verify) Does IEC 61993-2 require a VSWR/antenna alarm, and in which clause?
- (verify) Any peer-reviewed measurement of Class B CS report loss vs slot
  occupancy (candidates: EMSA/JRC studies; USCG RDC; Singapore). Not located.
- (verify) Winkler 2012 presentation: obtain the PDF and extract the US
  static-data error rates and the AVIS design.
- (verify) A list of vendor WNRO bulletins for AIS (Furuno FA-150/FA-170,
  Saab R4/R5, Kongsberg, SRT-based Class B). Only the JRC JHS-182/183 notice
  (device-specific 2025-08-03 rollover) was located.
- (verify) MAIB Safety Digest case numbers that describe GPS antenna-offset
  misuse and misconfigured AIS static data; NTSB reports noting heading 511.
- (verify) Whether the USCG "AIS Encoding Guide" PDF is still current and its
  revision date.
- (verify) Nauticast "AIS-MMSI Technical Bulletin" document id and date.

## Candidate figures and worked examples

1. **Failure-signature matrix** (table above) rendered as a two-page spread:
   failure → signature → detector → fixer.
2. **Sentinel census plot**: fraction of position reports per MMSI with
   heading 511, SOG 1023, COG 3600, timestamp ≥ 60, from one day of an open
   dataset (Danish DMA or Marine Cadastre), grouped by Class A/B.
3. **Worked example — detecting a fleet-wide firmware fault**: count of
   distinct MMSIs reporting valid positions per hour across 5–7 Apr 2019
   (WNRO) from an open feed; show whether a step is visible. (If no step is
   visible, that is itself the result: report it honestly.)
4. **Worked example — duplicate MMSI**: two vessels on one MMSI 300 nmi apart;
   compute implied speed between consecutive reports (> 1,000 kn) and show how
   a per-MMSI Kalman gate separates the tracks.
5. **Try it**: a 30-line Python snippet (pyais or libais) that scores a
   message stream against the catalogue: MMSI pattern, dimension plausibility,
   sentinel counts, static-report presence.
6. **Diagram**: what MSC.1/Circ.1252 tests vs the failure catalogue (Venn).
7. **Case file box**: PRN-32 (27 Feb 2008) from the NAVCEN FAQ — a one-paragraph
   narrative with the FAQ as the citation.

## Recommended use by chapter

- **Ch. 36** — build the chapter around the failure catalogue; open with the
  PRN-32 and WNRO stories; cite Harati-Mokhtari 2007 for the 8 % baseline and
  Last 2014/Iphar 2020/Emmens 2021 for later field-level views; end with what
  the annual test (MSC.1/Circ.1252) does and does not catch; recommend VIVS-style
  shore verification.
- **Ch. 13** — invalid/default MMSI list from the NAVCEN FAQ (111111111,
  123456789, 00000001, 1193046/"NAUT", documentation numbers); US MIDs 338,
  366–369.
- **Ch. 24** — PRN-32 (2008) and WNRO (2019; JRC device epoch 2025) as timing/
  date failure cases; note that positioning can survive while date/time fails.
- **Ch. 25** — GNSS-denied signatures (lat 91/lon 181, timestamp 61–63).
- **Ch. 21/30** — Class B CS starvation as designed behaviour; MGN 324.
- **Ch. 31** — LED EMI: Safety Alert 13-18 and its squelch test.
- **Ch. 26** — NMEA multiplexer/fragment reassembly faults.
- **Ch. 47** — error taxonomy; dedupe and reordering; separate receive time
  from message time.
- **Ch. 53** — Harati-Mokhtari human-factors argument; USCG Encoding Guide and
  inspection checklist as training artefacts.
- **Ch. 58/60** — Kessler et al. 2018 taxonomy to separate fault from attack;
  Balduzzi 2014 malformed-input tests.
- **App. D** — sentinel values table.
