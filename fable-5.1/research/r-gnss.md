# Dossier: GNSS and AIS — constellations, what transponders actually contain, GNSS-denied behaviour, and the backups

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the relationship between AIS and satellite navigation: which GNSS and SBAS
exist and when they became usable; what the AIS standards require of the
*electronic position-fixing system* (EPFS) and of the *internal* GNSS receiver by
station class; a survey of 37 transponder/AtoN/SART product documents recording
which constellations and augmentations each vendor actually supports, by
generation; how the position-accuracy and RAIM flags are derived; the behaviour
of each class when GNSS is lost (time-stamp sentinels 61/62/63, cessation of
transmission, sync fallback); DGNSS over AIS (Message 17) and the end of the US
NDGPS service; the GNSS-interference era as seen through AIS data; and the
GNSS-independent backups (R-Mode, eLoran). It feeds **Chapter 25** (GNSS and
AIS) as its primary target, plus **Chapter 20** (station classes), **Chapter 22**
(EPFD type, PA/RAIM flags, time stamp), **Chapter 24** (GNSS as the time source),
**Chapter 33** (hardware), **Chapter 36** (failure modes), **Chapter 47** (data
cleaning: 61–63 and accuracy flags), **Chapter 59** (spoofing detection),
**Chapter 62** (GNSS jamming/spoofing effects and workarounds), **Chapter 65**
(R-Mode), and **Appendix F** (hardware catalog: GNSS column).

> Research-session note. ITU-R M.1371-6 facts were read from the itu.int PDF
> (text-extracted; clause numbers in the "A2-x" form). The datasheet survey was
> performed in this session by reading 33 manufacturer documents verbatim (plus 4
> secondary pages); the full table with exact quotes is in the session scratch
> (`datasheet_survey.md`) and is summarised here. Constellation milestone dates
> come from web-search summaries pointing at official sites (gps.gov, GSA/EUSPA,
> FAA, ESA) and are marked *medium* until the specific official page is read in
> the verification pass. DOIs marked "Crossref-verified" were checked against the
> Crossref API during this session. Nothing was taken from memory without a URL.

## Key questions

1. Which GNSS (GPS, GLONASS, Galileo, BeiDou, QZSS, NavIC) and SBAS (WAAS, EGNOS,
   MSAS, GAGAN, others) exist, and when did each become operational for maritime
   users?
2. What do IMO and ITU require of the AIS position source: resolution, datum,
   which station classes *must* have an internal GNSS, and which may use an
   external EPFS?
3. In practice, which constellations and SBAS do AIS transponders support, by
   vendor and generation? Is "GPS-only" still shipping?
4. How are the position-accuracy (PA) flag and RAIM flag set, and what does the
   "type of EPFD" field tell a data consumer?
5. Do any AIS systems lack GNSS entirely (receivers; AtoN with surveyed
   position; base stations)?
6. What happens, class by class, when the fix is lost: time stamp 61/62/63,
   stop transmitting, sync fallback, reporting-interval changes?
7. How does DGNSS reach AIS (Message 17; RTCM beacon input; SBAS inside the
   receiver), and what happened to the beacon networks?
8. What do jamming and spoofing look like in AIS data, and what has been
   published (Black Sea 2017, Chinese ports 2019, Baltic/Red Sea 2023–)?
9. What are the realistic GNSS-independent workarounds (R-Mode, eLoran/Chayka,
   radar overlay, inertial), and what is their status?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Recommendation ITU-R M.1371-6 | 02/2026 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | EPFD type table; Table 48 PA/RAIM; time-stamp sentinels; Class B CS internal GNSS (A6-3.3); Message 17 (A7-3.15) | Free |
| IMO Resolution MSC.74(69) Annex 3 | 12 May 1998 | https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/MSCResolutions/MSC.74(69).pdf | "a means of processing data from an electronic position-fixing system … one ten thousandth of a minute of arc … WGS-84" | Free |
| IMO Resolution A.1106(29) | 2 Dec 2015 | https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.1106(29).pdf | "GNSS receiver for timing purposes and position redundancy"; §48 DGNSS via AIS | Free |
| IMO Resolution A.1046(27) *Worldwide Radionavigation System* | adopted 30 Nov 2011 | imo.org (resolution index) | IMO policy for recognising GNSS/terrestrial systems | Free (verify URL) |
| IMO Resolution MSC.401(95) *Performance standards for multi-system shipborne radionavigation receivers* (amended by MSC.432(98)) | adopted 8 June 2015; applies to receivers installed on/after 31 Dec 2017 | imo.org (resolution index) | Multi-constellation receiver performance | Free (verify URL) |
| IMO MSC.1/Circ.1575 *Guidelines for shipborne PNT data processing* | 2017 (MSC 98) | imo.org | PNT-DP resilience framework | Free (verify) |
| IMO MSC.1/Circ.1644 (deliberate GNSS interference) | approved MSC 104, Oct 2021 | imo.org | Member-State responsibilities; resilience | Free (verify) |
| IEC 61993-2:2018, 62287-1:2017, 62287-2:2017, 62320-2:2016 | see `r-timing.md` for URLs | webstore.iec.ch; iTeh previews | Internal GNSS requirements by class; AtoN Types | Paid (abstracts/previews free) |
| IEC 61108 series (GNSS receiver equipment) | 61108-1 Ed. 2.0 (GPS), 61108-2 Ed. 1.0 (GLONASS) cited by em-trak; other parts (verify) | https://webstore.iec.ch/ | Receiver performance standards datasheets cite | Paid |
| Federal Register 83 FR 12402, "Discontinuance of the Nationwide Differential Global Positioning System (NDGPS)" | 21 Mar 2018, doc. 2018-05684 | https://www.federalregister.gov/documents/2018/03/21/2018-05684/discontinuance-of-the-nationwide-differential-global-positioning-system-ndgps (text via FR API) | Phased shutdown of 38 maritime DGPS sites, Sept 2018–Sept 2020 | Free |
| GPS.gov | official | https://www.gps.gov/ (SA and FOC pages; several legacy URLs now 404) | GPS milestones; WNRO | Free |
| EUSPA GSC constellation information | live page read 2026-10-05 | https://www.gsc-europa.eu/system-service-status/constellation-information | Galileo satellite status table (IOV/FOC, RAFS/PHM clocks) | Free |
| Androjna, Perkovič, Pavic & Mišković (2021), "AIS Data Vulnerability Indicated by a Spoofing Case-Study", *Applied Sciences* 11(11):5015 | doi:10.3390/app11115015 (Crossref-verified, 2021-05-28) | https://doi.org/10.3390/app11115015 | GNSS spoofing seen in AIS | Free (OA) |
| Spravil, Hemminghaus, von Rechenberg, Padilla & Bauer (2023), "Detecting Maritime GPS Spoofing Attacks Based on NMEA Sentence Integrity Monitoring", *J. Mar. Sci. Eng.* 11(5):928 | doi:10.3390/jmse11050928 (Crossref-verified, 2023-04-26) | https://doi.org/10.3390/jmse11050928 | NMEA-level spoofing detection; MARSIM dataset | Free (OA) |
| US MARAD MSCI Advisory 2017-005A "Black Sea – GPS Interference" | June 2017 | https://www.maritime.dot.gov/msci/2017-005a-black-sea-gps-interference (403 to fetcher) | Novorossiysk-area spoofing report | Free (verify fetch) |
| Rizzi, Grundhöfer, Gewies & Ehlers (2023), *Applied Sciences* 13(3):1872 | doi:10.3390/app13031872 (Crossref-verified) | https://doi.org/10.3390/app13031872 | MF R-Mode 15.1 m / 55.3 m (95 %) | Free (OA) |
| Gewies et al. (2023), ION GNSS+ abstract | elib.dlr.de/200015 | https://elib.dlr.de/200015/ | 10–30 m MF; ~10 m VDES R-Mode | Free |
| Šafář, Grant, Williams & Ward (2019), *J. Navigation* | doi:10.1017/s0373463319000559 (Crossref-verified) | https://doi.org/10.1017/s0373463319000559 | VDES R-Mode ranging bounds | Paid |
| Koch & Gewies (2020), "Worldwide Availability of Maritime Medium-Frequency Radio Infrastructure for R-Mode-Supported Navigation", *JMSE* 8(3):209 | doi:10.3390/jmse8030209 (Crossref-verified) | https://doi.org/10.3390/jmse8030209 | MF beacon inventory for R-Mode | Free (OA) |
| IALA Guideline G1158 *VDES R-Mode* | Ed. 2.0 Dec 2024 (per search; product page dateModified 2025-01-07) | https://www.iala.int/product/g1158/ | R-Mode guidance | Free (registration) |
| Trinity House NtM 27/2015 | 1 Dec 2015 | https://www.trinityhouse.co.uk/notice-to-mariners/27-15-enhanced-loran-discontinued | UK/Ireland eLoran IOC discontinued 31 Dec 2015 | Free |
| Kim, Son, Park, Park & Seo (2021), IEEE TAES (arXiv 2109.08990) | preprint | https://arxiv.org/pdf/2109.08990 | Korean eLoran operational since 1 June 2021 | Free |
| archive.gps.gov Loran-C legislation page | archived | https://archive.gps.gov/policy/legislation/loran-c/ | Loran-C shutdown 2010; NTRSA 2018 | Free |
| Vendor datasheets (33 primary) — see survey table | various | e.g. https://www.em-trak.com/products/a200/ ; https://www.alltekmarine.com/en-global/products/ais-class-a/A750 ; https://static.garmin.com/pumac/Product-Overview_Cortex_1.3_GLOBAL.pdf ; Furuno FA-170 OM (dealer mirror) | Constellations, channels, SBAS, timing statements | Free |

## Verified facts

### What the standards require of the position source

| Fact | Source | Confidence |
|---|---|---|
| IMO performance standard: the AIS should comprise "a means of processing data from an electronic position-fixing system which provides a resolution of one ten thousandth of a minute of arc and uses the WGS-84 datum" — no constellation named, no internal receiver required | MSC.74(69) Annex 3 §3.1.2 | high |
| IMO A.1106(29) annex lists among AIS components "an electronic position-fixing system, Global Navigation Satellite System (GNSS) receiver for timing purposes and position redundancy"; §48 "(D)GNSS corrections may be sent by VTS centres via AIS" | A.1106(29) annex | high |
| M.1371 Class A: position fields are 1/10 000 min (28 bits lon, 27 bits lat); EPFD type (4 bits): 0 n/a; 1 GPS; 2 GLONASS; 3 combined GNSS; 4 Loran; 5 Chayka; 6 INS; 7 manually inputted/surveyed; 8 Galileo; 9 BDS; 10–11 reserved; 12 integrated PNT system; 13 inertial navigation system; 14 terrestrial radio navigation system; 15 internal GNSS | M.1371-6 Tables 49–50 (pp. 108–110) | high |
| Class B CS "should have an internal GNSS receiver as source for position, COG, and SOG … may be capable of being differentially corrected, e.g. by evaluation of Message 17. If the internal GNSS receiver is inoperative, the unit should not transmit Messages 18 and 24 unless interrogated by a base station" | M.1371-6 A6-3.3 (p. 82) | high |
| IEC 62287-2:2017 (Class B SO): "only uses the internal GNSS – no position sensor input is allowed", "requires use of VDL Message 17 for correction of the internal GNSS" | iTeh preview, Scope | high |
| IEC 62287-1:2017 Ed. 3 (Class B CS): receive-only stations are not Class B; new "direct method for synchronisation from an internal UTC source" | IEC webstore 32705 | high |
| IEC 62320-2:2016 Table 1: AtoN positioning device "EPFS and surveyed position" with option "Surveyed position only (no EPFS)"; Type 1 has no VHF receiver; UTC Direct for Types 1/2 | iTeh preview | high |
| Class A (IEC 61993-2) requires an internal GNSS receiver used for UTC and as position backup — stated by vendors (Furuno: "provides UTC reference for system synchronization … also gives position, COG and SOG when the external GPS fails") and by A.1106(29); exact IEC clause (verify) | Furuno FA-170 OM; A.1106(29) | medium (clause) |
| IMO MSC.401(95) (adopted 8 June 2015) sets performance standards for multi-system shipborne radionavigation receivers for installations on/after 31 Dec 2017; amended by MSC.432(98); A.1046(27) (30 Nov 2011) is the WWRNS recognition policy | search summaries (imorules.com, imo.org) | medium (verify dates on imo.org) |
| MSC.1/Circ.1575 (2017) PNT data-processing guidelines; MSC.1/Circ.1644 (Oct 2021) on deliberate GNSS interference reminds Member States "to refrain from interfering with GPS and GNSS signals" and urges resilience | search summaries | medium |

### Position accuracy and RAIM flags (Table 48)

| Fact | Source | Confidence |
|---|---|---|
| PA flag: 1 = high (≤ 10 m), 0 = low (> 10 m), 0 = default | Table 47/49 | high |
| Table 48 logic: RAIM not available & uncorrected → PA 0; RAIM available with expected error ≤ 10 m → PA 1; RAIM available with expected error > 10 m → PA 0; **no RAIM & differentially corrected → PA 1**; corrected + RAIM ≤ 10 m → 1; corrected + RAIM > 10 m → 0. Threshold 10 m; expected RAIM error = √(err_lat² + err_lon²) from the IEC 61162 GBS sentence; correction status from the quality/mode indicator of the position sentences | Table 48 and notes (p. 107) | high |
| RAIM flag: "0 = RAIM not in use = default; 1 = RAIM in use" — set when "The connected GNSS receiver indicates the availability of a RAIM process by a valid sentence of IEC 61162" | Table 47, Table 48 note (1) | high |
| Consequence for data consumers: PA = 1 can mean "SBAS/DGNSS corrected without RAIM", not necessarily a verified ≤ 10 m error; PA/RAIM are set from NMEA sentences the transponder receives and are only as good as the sensor's reporting | derived from Table 48 | high |

### GNSS-denied behaviour by class (M.1371-6)

| Fact | Source | Confidence |
|---|---|---|
| Time stamp 60 = not available (default); 61 = manual input mode; 62 = dead reckoning (estimated); 63 = positioning system inoperative; Class B CS uses only 0–60 | Tables 47, 68 | high |
| Position "not available" sentinels: longitude 181° (0x6791AC0), latitude 91° (0x3412140) | Table 47 | high |
| Class B CS: no internal fix → no Messages 18/24 unless interrogated | A6-3.3 | high |
| Speed lost → Class A reverts to nav-status default interval (Table 1 note 2); Class B to 3-min default (Table 2 note 5) | Annex 1 | high |
| Loss of UTC → sync falls to UTC indirect / base / semaphore (see `r-timing.md`); Class B CS keeps slot-phase sync from received reports for ≥ 30 s then free-runs | A2-3.1; A6-4.3.1.1 | high |
| AtoN Message 21 off-position flag for a fixed aid = "internal GNSS position of the AtoN exceeds the zone parameter set on installation …, i.e. suspected GNSS anomaly" — a built-in GNSS-anomaly detector at a known position | Table 71 (p. 133) | high |
| Vendor statements: Nauticast A2 raises alarm "UTC Sync Invalid" when the internal GPS has no fix; Ocean Signal/ACR FAQ: external GPS cannot replace the internal receiver ("The use of the internal GPS receiver is a requirement of the AIS regulations"); McMurdo M10 and AMEC offer "Dual GPS Backup" (external NMEA position as *backup* only) | Nauticast A2 install guide; oceansignal.com; acrartex.com; SmartFind M10 manual | high |
| No datasheet surveyed states that a unit transmits position reports with *no* GNSS fix ever obtained; Jotron Tron AIS-SART manual: needs to "fix a GPS position (max. 15 mins)" | survey | medium |

### DGNSS over AIS and the beacon networks

| Fact | Source | Confidence |
|---|---|---|
| Message 17 "should be transmitted by a base station, which is connected to a differential global navigation satellite system (DGNSS) reference source"; contents per ITU-R M.823 "excluding preamble and parity formatting"; layout: lon 18 b / lat 17 b in 1/10 min (181°/91° if service unavailable), data 0–736 bits = message type 6, station ID 10, Z count 13 (0.6 s units), sequence 3, N 5 (≤ 29 words), health 3, N × 24-bit words; 80–816 bits total; "transmission of Message 17 should be no more than necessary" | M.1371-6 A7-3.15, Tables 66–67 (pp. 125–127) | high |
| Class A datasheets provide an RTCM SC-104 / ITU-R M.823 beacon input (Furuno FA-170 "DGPS data receiving RTCM SC-104 ver-2.1"; JRC JHS-183 "IEC61162-1/ITU-R M.823-2: 1 port (DGPS)") | survey | high |
| USCG announced discontinuance of "its remaining 38 maritime Differential Global Positioning System (DGPS) sites … a phased reduction in service, which will commence in September of 2018, and conclude by September of 2020"; rationale: un-augmented GPS and WAAS sufficient for ATON positioning | 83 FR 12402 (21 Mar 2018), abstract and body | high |
| Earlier: 37 inland/coastal NDGPS sites decommissioned Aug 2016 (FR notices 2015-20401, 2016-15886) | FR API document list | medium (titles only read) |
| SBAS inside the receiver has replaced beacon DGPS in most current products: Vesper Cortex "SBAS, WAAS, EGNOS"; AMEC A750/N323 "WAAS, EGNOS, MSAS, GAGAN"; Samyung "WAAS, EGNOS, MSAS"; Icom MA-510TR "SBAS function"; True Heading Graphene "DGNSS (EGNOS or WAAS) corrections" selectable | survey | high |

### Constellations and SBAS — milestones

| Fact | Source | Confidence |
|---|---|---|
| GPS Full Operational Capability declared 17 July 1995; Selective Availability discontinued 2 May 2000 | gps.gov / spaceforce.mil (search summaries) | medium (verify page) |
| GPS week-number rollover 23:59:42 UTC 6 Apr 2019; next LNAV rollover 20 Nov 2038 | https://www.gps.gov/news/gps-week-number-rollover | high |
| GLONASS constellation restored to 24 operational satellites in 2011 | eoportal / insidegnss (search summaries) | medium |
| Galileo Initial Services declared 15 Dec 2016; constellation page lists IOV (GSAT01xx) and FOC (GSAT02xx) satellites with RAFS/PHM clocks and per-satellite USABLE/NOT USABLE status | europa.eu/ESA (search); GSC page read | medium (date) / high (page content) |
| BeiDou-3 global system completion announced 31 July 2020 | scio.gov.cn (search) | medium |
| WAAS commissioned 10 July 2003 (FAA); EGNOS Safety-of-Life service declared 2 March 2011; MSAS operational for aviation 27 Sep 2007; GAGAN certified RNP 0.1 in 2013 and APV-1 on 21 Apr 2015 | FAA / ESA / ICAO (search summaries) | medium |
| QZSS and NavIC: named by only two AIS datasheets (AMEC N323 "GPS/QZSS L1C/A"; Samyung SI-70A "GPS / QZSS / GLONASS / BeiDou / Galileo"); no AIS product surveyed names NavIC | survey | high (for the survey) |

### Datasheet survey — what transponders actually contain (37 products; 33 read verbatim)

Summary table (full quotes and URLs in `datasheet_survey.md`; "ch." = GNSS channels as stated):

| Vendor / model | Class | Constellations stated | SBAS/DGNSS | ch. | Generation | Timing statement | Confidence |
|---|---|---|---|---|---|---|---|
| Furuno FA-170 | A | GPS only (L1 C/A) | DGPS via RTCM SC-104 v2.1 | 12 | ≈2014– | **Yes**: "provides UTC reference for system synchronization" | high |
| Furuno FA-70 (FA-40 Rx) | B SO/CS | GPS only | SBAS 2 ch | 12+2 | 2020 brochure | no | high |
| JRC JHS-183 | A | not stated | DGPS beacon port (M.823) | — | ≈2010–18 | no | high (negative) |
| Saab R5 Supreme | A | GPS (L1) | "Ready for DGPS" | 50 | 2011 sheet | no | high |
| Saab R5 Solid | A | GPS | DGPS figure | 50 | ≈2012–18 | no | medium (secondary) |
| Saab R6 Supreme AIS/VDES | A | "multi GNSS"; "GPS and Galileo type-approved" | DGNSS add-on kit | — | ≈2023– | no | high |
| em-trak A200 | A | GPS, GLONASS, BeiDou, Galileo ("two of any combination, three including GPS, Galileo") | IEC 61108-1/-2 cited | 72 | current | no | high |
| em-trak B921/B924/B952–954 | B CS / B SO | same four | — | 72 | current | no | high |
| Vesper/Garmin Cortex M1 | B SO | GPS, GLONASS, BeiDou, Galileo | SBAS, WAAS, EGNOS | 72 | 2020– | no | high |
| Vesper XB-8000 | B CS | GPS | WAAS/EGNOS | 50 | 2012 | no | high |
| Garmin AIS 800 | B SO | not stated ("Built-in GPS") | — | — | 2018 | no | high (negative) |
| Digital Yacht AIT2500 / AIT5000 | B SO | GPS, GLONASS | — | — | ≈2018– | no | high |
| Comar CSB200 | B CS | not stated ("IEC 61108-1 compliant") | — | — | ≈2008–12 | **Yes**: "used for timing of the transmitted time slots" | high |
| AMEC Camino-108 | B CS | GPS | — | 50 | ≈2013–18 | no | medium (secondary) |
| AMEC WideLink B600 | B SO | GPS, Galileo, BeiDou, GLONASS | — | 50 (72?) | ≈2017–23 | no | medium |
| AMEC B650 / B620 | B SO / B CS | GPS, Galileo, BeiDou, GLONASS | — | 72 | 2024–25 | no | high |
| AMEC A750 | A | GPS, GLONASS, BeiDou, Galileo (default GPS & GLONASS) | WAAS, EGNOS, MSAS, GAGAN | 72 | ≈2020– | no | high |
| AMEC N323 | AtoN Type 3 | GPS/QZSS L1C/A, GLONASS L1OF, BeiDou B1I, Galileo E1B/C | WAAS, EGNOS, MSAS, GAGAN | 72 | current | no | high |
| Icom MA-510TR | B CS | GPS | SBAS | 66 | 2020 | no | high |
| Raymarine AIS700 | B SO | GPS, GLONASS | — | 72 | ≈2018– | no | high |
| Simrad NAIS-500 | B CS | not stated | — | 50? | ≈2017– | no | low |
| McMurdo SmartFind M10 | B CS | GPS & Galileo (factory default) | — | 72 | 2016+ hw, 2023 manual | no | high |
| McMurdo SmartFind S5A | AIS-SART | "GNSS" | SBAS | 48 | current | no | high |
| Ocean Signal ATB1 / ACR AISLink CB2 | B SO | "multi-GNSS" (unnamed) | — | 99/33 | ≈2019– | FAQ: internal receiver mandatory | high |
| Weatherdock easyTRX3S | B SO | "GNSS/GPS" (unnamed) | — | 72 | ≈2019– | no | high |
| True Heading CTRX Graphene | B CS | GPS L1 | SBAS (EGNOS/WAAS) selectable | 50 | 2012–17 | no | high |
| Si-Tex MDA-5 | B SO | GPS, GLONASS | — | 72 | ≈2018– | no | high |
| Samyung SI-70A | A | GPS, QZSS, GLONASS, BeiDou, Galileo ("u-blox engine") | WAAS, EGNOS, MSAS | 72 | current | no | high |
| Nauticast A2 | A | GPS (L1) | DGPS figure | 50 | ≈2014–19 | **Yes**: "UTC Sync Invalid" alarm | high |
| Transas T-105 | A | GLONASS/GPS | DGNSS figure | — | ≈2010–15 | no | medium (secondary) |
| Sealite SL-155 AIS AtoN | AtoN 1/3 | GPS | — | — | 2017 | (lantern flash sync only) | high |
| Jotron Tron AIS-SART | AIS-SART | GPS | — | — | current | needs fix (≤ 15 min) | high |
| Standard Horizon GX2400 | VHF + AIS Rx | not readable | — | — | 2021 | n/a | low |

Patterns (high confidence as a description of the surveyed set):

- **Pre-≈2013:** GPS-only L1 C/A, 12–16 channels; DGPS only via beacon input or Message 17.
- **≈2011–2017:** 50-channel GPS(+SBAS) receivers (Saab R5, Nauticast A2, Vesper XB-8000, Camino-108, Graphene); still GPS-only except the Russian-market Transas T-105 (GLONASS/GPS).
- **≈2017–present:** 72-channel multi-GNSS (u-blox M8-class) is the norm; em-trak, Vesper Cortex, AMEC, Samyung name GPS/GLONASS/BeiDou/Galileo; Raymarine, Digital Yacht, Si-Tex say GPS/GLONASS; Ocean Signal/ACR, Weatherdock, Saab R6, Garmin AIS 800 give no list. Icom MA-510TR (2020) is a late GPS+SBAS-only design.
- **Galileo** named by em-trak, Vesper/Garmin Cortex, AMEC, Samyung, Saab R6, McMurdo M10; **BeiDou** by em-trak, Cortex, AMEC, Samyung; **QZSS** by AMEC N323 and Samyung only; **NavIC** by none.
- **Timing** is mentioned explicitly by only three documents (Furuno FA-170, Comar CSB200, Nauticast A2).
- Channel count is a plausible chipset fingerprint (12 → early; 50 → u-blox 6/7; 66/99-33 → MediaTek; 72 → u-blox M8) — **inference, (verify)**.

### GNSS interference seen through AIS

| Fact | Source | Confidence |
|---|---|---|
| June 2017, Black Sea: ships near Novorossiysk reported GPS positions placing them inland (Gelendzhik airport area); US MARAD issued advisory 2017-005A | search summaries citing maritime.dot.gov (page 403 to fetcher) | medium (verify text) |
| 2019, Shanghai and other Chinese ports: AIS positions forming rings ("crop circles") around points ashore; reported by MIT Technology Review and analysed by SkyTruth across >20 sites | search summaries | medium (verify primary articles) |
| Androjna et al. 2021 and Spravil et al. 2023 are real peer-reviewed papers (titles, venues, authors, dates verified via Crossref) | Crossref | high |
| IMO MSC.1/Circ.1644 (2021) addresses deliberate GNSS interference | search summary | medium |
| AIS-visible signatures of GNSS trouble implied by the standards: time stamp 62/63, PA flag changes, EPFD type switching to 15 (internal) on Class A, sync state leaving 0, AtoN off-position flag (fixed aids), and Class B CS going silent | M.1371-6 tables | high (as derivations) |

### GNSS-independent backups

| Fact | Source | Confidence |
|---|---|---|
| R-Mode Baltic (from Oct 2017, DLR-led) and R-Mode Baltic 2 (to ~2022): eight MF beacons with R-Mode modulators and accurate clocks; "accuracies of 10 to 30 m … at day-time"; VDES R-Mode "accuracies of 10 m in areas with good reception conditions" | DLR news 2017-10-20; elib.dlr.de/200015 | high |
| MF R-Mode near Rostock: 15.1 m (95 %) optimal; 55.3 m under night sky-wave | Rizzi et al. 2023 | high |
| "all of the new VDES waveforms provide better ranging performance than the AIS waveform" | Šafář et al. 2019 | high |
| IALA G1158 *VDES R-Mode* exists (Ed. 2.0, Dec 2024 per search; page modified 2025-01-07) | iala.int | medium (edition) |
| eLoran: UK/Ireland IOC discontinued 11:00 UTC 31 Dec 2015 (France/Norway transmitters off-air same day); Korea eLoran testbed operational since 1 June 2021 (≤ 20 m 95 %); US Loran-C shutdown began Feb 2010; National Timing Resilience and Security Act of 2018 (P.L. 115-282 §514) signed 4 Dec 2018; Russian Chayka reportedly still operating (verify) | Trinity House; arXiv 2109.08990; archive.gps.gov | high / low (Chayka) |
| EPFD codes 4 (Loran) and 5 (Chayka) remain in M.1371-6 | Table 49 | high |

## Notes and quotes

- MSC.74(69) Annex 3 §3.1.2 — the whole IMO position requirement: "a means of
  processing data from an electronic position-fixing system which provides a
  resolution of one ten thousandth of a minute of arc and uses the WGS-84
  datum." Nothing about GPS by name; "EPFS" neutrality is deliberate.
- Furuno FA-170 OM: "The internal GPS is a 12-channel all-in-view receiver with
  a differential capability, and provides UTC reference for system
  synchronization to eliminate clash among multiple users. It also gives
  position, COG and SOG when the external GPS fails." — the clearest vendor
  statement of the two roles (time first, position second) and a reminder that
  a Class A in service normally *transmits the ship's external EPFS position*.
- Ocean Signal FAQ: "Can I use an existing GPS receiver or GPS data instead of
  installing an additional GPS antenna for the AIS? No. The use of the internal
  GPS receiver is a requirement of the AIS regulations."
- em-trak's "two of any combination, three including GPS, Galileo" is the
  u-blox M8 concurrency limit leaking into a marine datasheet — useful for
  explaining why "supports four constellations" ≠ "tracks four at once".
- Table 48 subtlety: a differentially corrected fix with *no* RAIM yields PA = 1.
  Data scientists reading PA as "verified ≤ 10 m" are over-trusting it.
- The AtoN off-position flag for *fixed* aids is, in effect, a standards-blessed
  GNSS-spoofing/jamming sensor at a surveyed point (Table 71).
- 83 FR 12402: the USCG decided un-augmented GPS plus WAAS "is sufficient" and
  retired beacon DGPS; Message 17 therefore matters mainly where administrations
  still run beacons or feed corrections from other sources (verify current users).
- Androjna et al. (2021) and Spravil et al. (2023) are the two peer-reviewed
  anchors found for "spoofing as seen in AIS/NMEA"; the popular Black Sea 2017
  and Shanghai 2019 narratives still need their primary documents attached.

## Open questions / (verify)

- (verify) Read the official pages for GPS FOC/SA, Galileo Initial Services,
  BDS-3 completion, GLONASS 2011, WAAS/EGNOS/MSAS/GAGAN dates (gps.gov URLs
  reorganised; several legacy paths now 404).
- (verify) IEC 61993-2:2018 clause requiring the internal GNSS and whether it
  specifies constellations (likely "GNSS per IEC 61108 series"); the IEC 61108
  part numbers for Galileo/BeiDou/multi-system receivers.
- (verify) IMO MSC.401(95)/MSC.432(98), A.1046(27), MSC.1/Circ.1575 and
  MSC.1/Circ.1644 — confirm dates and quote the relevant paragraphs from IMO
  PDFs.
- (verify) Datasheet gaps: JRC JHS-183 internal receiver; Saab R6 constellations
  beyond "GPS and Galileo type-approved"; Garmin AIS 800; Ocean Signal/ACR
  constellations; Weatherdock; Simrad NAIS-500; AMEC B600 50 vs 72 channels;
  McMurdo SmartFind M5 (Class A); em-trak B100; Kongsberg (Saab-OEM) units.
- (verify) MARAD 2017-005A text; MIT Technology Review and SkyTruth articles on
  the 2019 Chinese-port rings; Baltic/Red Sea 2023–25 interference reports from
  primary sources (EASA/EMSA/national administrations).
- (verify) Whether any administration still broadcasts Message 17 at scale
  (e.g., EU/Asian beacon networks via AIS) after the US NDGPS shutdown.
- (verify) Current satellite counts per constellation ("as of" figures) from the
  official status pages before print.
- (verify) Chayka operational status and any AIS EPFD = 5 observations.
- (verify) Whether any transponder documents describe behaviour under GNSS
  *spoofing* (e.g., RAIM-based rejection) rather than mere loss of fix.

## Candidate figures and worked examples

1. **Table 25-A — Constellation and SBAS overview**: system, operator, first
   service / FOC date, frequency bands used by marine L1 receivers, SBAS
   coverage; with "as of" stamps.
2. **Figure 25-1 — Which classes carry their own GNSS?** Class A (internal +
   external EPFS), Class B SO/CS (internal only), AtoN Types 1–3 (internal or
   surveyed), SART/MOB/EPIRB (internal), base station (internal for time),
   receive-only (none) — from M.1371-6, IEC 62287/62320 and A.1106(29).
3. **Figure 25-2 — Datasheet survey timeline**: product year vs channels and
   constellations named (12 → 50 → 66/72 → 99/33), colour by vendor; marks the
   2017 shift to multi-GNSS.
4. **Worked example — Table 48 decision tree**: three fixes (uncorrected no
   RAIM; SBAS-corrected no RAIM; RAIM 12 m error) → PA/RAIM bits; show a
   Message 1 payload difference.
5. **Worked example — resolution**: 1/10 000 min of arc = 0.1852 m of latitude;
   28/27-bit field ranges; 181°/91° sentinels.
6. **Worked example — Message 17 size**: N = 5 RTCM words → 80 + 24 + 120 = 224
   bits → 2 slots? (compute with Table 66/67 and the slot budget from
   `r-link-layer.md`).
7. **Case file (ch. 62)** — Black Sea June 2017 (MARAD advisory) and Chinese
   ports 2019 — once primary texts are attached; include the AIS-visible
   signature list.
8. **Figure 25-3 — GNSS-loss cascade** (shared with ch. 24/62): fix lost → EPFS
   63 / PA 0 → Class A continues on external EPFS or stops updating; Class B CS
   stops 18/24; sync state degrades; AtoN flags off-position.
9. **Table 25-B — Backups**: R-Mode (MF 10–30 m day / 55 m night; VDES ~10 m),
   eLoran (UK off 2015; Korea 2021 ≤ 20 m), radar overlay, inertial, visual —
   status and accuracy with sources.

## Recommended use by chapter

- **Ch. 20:** Figure 25-1 (who has a GNSS) and the Class B SO/CS internal-only
  rule.
- **Ch. 22:** EPFD type table, PA/RAIM Table 48, sentinels 181°/91°, 60–63.
- **Ch. 24:** Furuno/Comar/Nauticast timing quotes; A.1106(29) "timing purposes".
- **Ch. 25 (primary):** everything above; lead with the standards' EPFS
  neutrality, then the survey, then flags, then denial behaviour, then backups.
- **Ch. 33 / App. F:** survey table as the GNSS column of the hardware catalog
  (label secondary sources).
- **Ch. 36 / 47:** time stamp 61–63, PA/RAIM semantics, EPFD 15 as a Class A
  "fell back to internal" indicator; the Table 48 over-trust pitfall.
- **Ch. 54:** Message 17 and the NDGPS shutdown (83 FR 12402).
- **Ch. 59 / 62:** AIS-visible spoofing/jamming signatures; the two Crossref-
  verified papers; MARAD 2017-005A and 2019 rings as case files once verified;
  IMO MSC.1/Circ.1644.
- **Ch. 65:** R-Mode numbers and project history; eLoran status.
- **Ch. 68:** AtoN off-position flag as a GNSS-anomaly sensor; SART GNSS.
