# Dossier: NMEA, RTCM, ETSI, and CCNR/CESNI Inland AIS standards

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the *interface, regional and device-class* standards that sit beside the
ITU/IMO/IEC core of AIS: the NMEA 0183 serial sentence standard (the `!AIVDM`
sentences every decoder parses, and NMEA 4.10 TAG blocks), NMEA 2000 (the CAN
network and its AIS PGNs) and OneNet; the Radio Technical Commission for
Maritime Services (RTCM) documents that touch AIS (SC 121 standards for ASM
creation, mobile AtoN, internet AIS, MMSI/static-data reset, the MSLD/MOB and
LED-EMC standards); ETSI EN 303 098, the European harmonised standard for AIS
man-overboard devices (read in full this session); and the European Inland AIS
line from the CCNR *Vessel Tracking and Tracing Standard* (2006) through EU
Regulation 2019/838 to CESNI's ES-RIS. It feeds **Chapter 11** (Class B, Inland
AIS 2006, MOB devices), **Chapter 13** (972 MOB identities), **Chapter 14**
(NMEA, RTCM, ETSI, CCNR/CESNI as organisations), **Chapter 15** (standards
narrative), **Chapter 16** (EU inland law), **Chapter 20** (station classes incl.
Inland and MOB), **Chapter 21/24** (the MOB "modified SOTDMA" schedule as a
worked example of comm-state pre-announcement), **Chapter 22/23** (DAC 200
inland messages), **Chapter 26** (the interface chapter — primary consumer),
**Chapter 31** (RTCM 13700.0 LED EMC), **Chapter 44** (decoder history), **Chapter
68** (SART/MOB/AtoN special-purpose AIS), **Appendix B** (register) and
**Appendix D** (talker IDs, PGNs).

> Research-session note. *High* = read directly this session from a primary
> page or PDF (nmea.org NMEA 0183 page; rtcm.org publications page; ETSI EN
> 303 098 V2.2.1 PDF text-extracted; gpsd AIVDM document v1.58; canboat
> `canboat.json` v8.3.0; eCFR 47 CFR Part 80). *Medium* = web-search
> summaries of CESNI/CCNR/EUR-Lex/NMEA pages whose text could not be fetched
> (EUR-Lex and cesni.eu refused automated reads). NMEA 0183 and NMEA 2000 are
> copyrighted and were **not** read; sentence and PGN facts come from gpsd and
> canboat, which are open re-implementations.

## Key questions

1. What is the current NMEA 0183 version, when was 4.11 (the edition the PLAN
   cites) released, and what did each version add that matters to AIS (VDM/VDO
   in v3.x/IEC PAS 61162-100; TAG blocks in 4.10)? What does it cost and who may
   buy it?
2. What is the exact anatomy of `!AIVDM`/`!AIVDO`, the talker-ID set, the
   6-bit "armoring", fill bits, fragments, and the checksum; and how are TAG
   blocks (`\s:…,c:…*hh\`) formed and checksummed?
3. Which NMEA 2000 PGNs carry AIS, how are they framed (Fast Packet), and what
   is the licensing position for developers?
4. Which RTCM special committees and documents concern AIS, with exact ids and
   dates, and which are incorporated into US rules?
5. What does ETSI EN 303 098 require of an AIS-MOB device — identity, power,
   messages, burst schedule, battery life — and what is its version history
   and legal status under the Radio Equipment Directive?
6. What is the Inland AIS standards lineage (CCNR VTT 2006 → EU 415/2007 →
   Test Standard Ed. 2.0 2012 → VTT Ed. 1.2 2013 → EU 2019/838 → CESNI ES-RIS
   2021/1 … 2025/1), and what does Inland AIS add to Class A (ENI, blue sign,
   DAC 200 messages, assigned reporting rates)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| NMEA — NMEA 0183 product page | NMEA 0183 **Version 4.30 (December 2023)**, replacing 4.11 (2018); NMEA 0183-HS in appendix | https://www.nmea.org/nmea-0183.html | Scope statement, version note, pricing tiers, manufacturer mnemonic codes | Page free; standard paid (see facts) |
| NMEA — NMEA 2000 pages | NMEA 2000 (first released 2001); OneNet V1.000 (Nov 2020) | https://www.nmea.org/nmea-2000.html ; https://www.nmea.org/onenet.html (verify exact URLs) | Network standard, certification, licensing contact | Paid; contact-based purchase |
| gpsd "AIVDM/AIVDO protocol decoding" | v1.58, 24 June 2023; Eric S. Raymond, with contributions credited to Kurt Schwehr | https://gpsd.gitlab.io/gpsd/AIVDM.html | Sentence anatomy, talker IDs, armoring table, TAG blocks (incl. IEC 62320-1 vs NMEA 4.10 keys), message field tables | Free |
| canboat PGN database | `docs/canboat.json`, Version 8.3.0 (generated from the YAML database) | https://raw.githubusercontent.com/canboat/canboat/master/docs/canboat.json ; https://canboat.github.io/canboat/canboat.html | Reverse-engineered/open field definitions for all NMEA 2000 AIS PGNs | Free (Apache-2.0 project) |
| RTCM publications page | read 2026-10-05 | https://www.rtcm.org/publications | Current standards list with ids and dates (AIS-related items below) | Page free; standards paid (RTCM store) |
| RTCM 12100.1 | Standard for Creation and Qualification of Application-Specific Messages (ASM), 7 June 2022 | via RTCM store | ASM design/qualification process | Paid |
| RTCM 12110.1 | AIS Mobile Aids to Navigation (MAtoN), 15 June 2026 | via RTCM store | Mobile AtoN stations | Paid |
| RTCM 13300.0 | Standard for Internet-Based AIS Services (AIS-i), 11 July 2019 | via RTCM store | AIS data over IP | Paid |
| RTCM 10160.0 | Procedures for resetting own-ship MMSIs on DSC radios and setting/resetting static data on AIS, 28 November 2025 | via RTCM store | MMSI/static-data reset procedure (ch. 13/36) | Paid |
| RTCM 11901.2 | Standard for Maritime Survivor Locating Devices (MSLD), 14 November 2024 | via RTCM store | MOB devices incl. AIS-based (US counterpart of EN 303 098) | Paid |
| RTCM 13700.0 | EMC requirements for LED devices and other equipment near shipboard antennas, 13 April 2022 | via RTCM store | LED interference to VHF/AIS receivers (ch. 31) | Paid |
| RTCM 12301.1 | Standard for VHF-FM Digital Small Message Services (VDSMS) | via RTCM store | Short messaging on VHF-FM (not AIS; often confused) | Paid |
| RTCM 13900.0 | Maritime Messaging Service Architecture and Protocol, 5 March 2025 | via RTCM store | MMS (e-navigation messaging) | Paid |
| RTCM Paper 56-95/SC101-STD | DSC minimum standards v1.0, 10 Aug 1995 | incorporated by 47 CFR § 80.7(f)(1) | DSC (context for MMSI programming) | Paid |
| ETSI EN 303 098 V2.2.1 (2019-02) | "Maritime low power personal locating devices employing AIS; Harmonised Standard for access to radio spectrum" | https://www.etsi.org/deliver/etsi_en/303000_303099/303098/02.02.01_60/en_303098v020201p.pdf | AIS-MOB device requirements and tests; Annex B burst schedule; Annex A RED 3.2 mapping | **Free PDF** |
| ETSI work item REN/ERM-TGMAR-637 | revision of EN 303 098 as "AMRD Group B locating devices" (early draft 2026) | https://portal.etsi.org/ (work programme) | Successor to V2.2.1 | Free portal (verify status) |
| Directive 2014/53/EU (RED) | Radio Equipment Directive, 16 April 2014 | https://eur-lex.europa.eu/eli/dir/2014/53/oj | Legal basis for ETSI harmonised standards (art. 3.2) | Free |
| Commission Implementing Regulation (EU) 2019/838 | 20 February 2019; OJ 24 May 2019; repeals Reg. (EC) 415/2007 | https://eur-lex.europa.eu/eli/reg_impl/2019/838/oj | Technical specifications for vessel tracking and tracing systems (Inland AIS) under Directive 2005/44/EC art. 5 | Free (EUR-Lex refused automated fetch; open in browser) |
| Regulation (EC) No 415/2007 | 13 March 2007 (repealed) | https://eur-lex.europa.eu/eli/reg/2007/415/oj | First EU VTT/Inland AIS technical specification | Free |
| Directive 2005/44/EC | RIS Directive, 7 September 2005 | https://eur-lex.europa.eu/eli/dir/2005/44/oj | Harmonised River Information Services | Free |
| CCNR Resolution 2006-I-21 | VTT Standard for Inland Navigation Ed. 1.0, adopted 31 May 2006 | https://www.ccr-zkr.org/ (RIS documents; verify deep link) | First Inland AIS standard | Free |
| CCNR Test Standard for Inland AIS Ed. 2.0 | October 2012 (mandatory basis for type approval from 19 Oct 2012) | https://www.ccr-zkr.org/ (verify deep link) | Type-approval tests, tied to IEC 61993-2 Ed. 2 | Free |
| CCNR Resolution 2013-I-23 | VTT Standard Ed. 1.2, adopted 29 May 2013 | https://www.ccr-zkr.org/ (verify deep link) | Revised VTT standard | Free |
| CESNI ES-RIS | Ed. 2021/1 (first); **Ed. 2025/1 adopted 17 Oct 2024 (Res. CESNI 2024-II-2)**; Part II = VTT standard, Part III = Test Standard for Inland AIS (Ed. 3.0) | https://www.cesni.eu/en/ (ES-RIS page; automated fetch returned 404 — verify URL) ; https://ris.cesni.eu/ | Consolidated European RIS standard incl. Inland AIS | Free |
| CESNI ES-TRIN | Ed. 2025/1 (adopted Oct 2024) | https://www.cesni.eu/en/documents/es-trin/ (verify) | Vessel technical requirements incl. Inland AIS carriage/installation | Free |
| 47 CFR § 80.7, § 80.231, § 80.1061 (eCFR) | current 2026-10-01 | https://www.ecfr.gov/current/title-47/part-80 | RTCM documents incorporated by reference (RTCM 11000 EPIRB, SC101 DSC); Class B labelling rule | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| NMEA: "As of December 2023, NMEA has published a new version of NMEA 0183—Version 4.30, which replaces Version 4.11 (2018 Release)"; 4.30 updates the GNSS sentence suite (GPS, GLONASS, Galileo, BDS, QZSS, NavIC), adds talker IDs/formatters, RINEX observation codes, RLM, GIR, GRP, GGC, GCF, GSN, SMV. | https://www.nmea.org/nmea-0183.html, read 2026-10-05 | high |
| NMEA 0183 defines "electrical signal requirements, data transmission protocol and time, and specific sentence formats for a 4800-baud serial data bus. Each bus may have only one talker but many listeners." NMEA 0183-HS (38.4 kbaud) is an appendix of v4.30. | nmea.org NMEA 0183 page | high |
| NMEA 0183 pricing (2026): NMEA manufacturer member US$1,150; Government / Industrial / Testing US$7,500; Consumer Electronics US$10,000; version updates 50 % off; manufacturer mnemonic code US$200 admin fee, companies only; "not sold via an online store" — purchase by request form. | nmea.org NMEA 0183 page | high |
| NMEA states that third-party web explanations of 0183 "in most cases … are very old versions or incorrect interpretations" and that the standard is copyrighted and "available only from NMEA." | nmea.org NMEA 0183 page | high |
| NMEA 0183 4.11 release date: 27 November 2018 (per Wikipedia/NMEA press); version lineage 1.x 1983 → 2.00 1992 → 2.01 1994 → 2.10 1995 → 2.20 1997 → 2.30 1998 → 3.00 2000 → 3.01 2002 → 4.00 2008 → 4.10 2012 → 4.11 2018 → 4.30 2023. | search summary (Wikipedia, nmea.org, trade press) | medium — confirm dates against NMEA's own version list (verify) |
| `!AIVDM` anatomy (gpsd example `!AIVDM,1,1,,B,177KQJ5000G?tO\`K>RA1wUbN0TKH,0*5C`): field 1 fragment count; field 2 fragment number (1-based); field 3 sequential message id (empty for single-fragment); field 4 radio channel (A/B; some receivers emit 1/2); field 5 6-bit armored payload; field 6 fill bits; `*hh` NMEA checksum = XOR of all bytes between `!`/`$` and `*`. | gpsd AIVDM.html §"AIVDM/AIVDO Sentence Layer", read 2026-10-05 | high |
| Payload armoring: each ASCII character carries 6 bits — subtract 48 from the ASCII code; if the result is > 40 subtract 8 more. Valid characters run `0`–`W` and `` ` ``–`w`; `X`–`_` are unused. | gpsd AIVDM.html "Payload Armoring" (citing IEC-PAS 61162-100) | high |
| AIS talker IDs (NMEA 4.0 set): `AB` base station, `AD` dependent base station, `AI` mobile station, `AN` AtoN station, `AR` receiving station, `AS` limited base station, `AT` transmitting station, `AX` repeater, `SA` physical shore station; `BS` (base) deprecated in NMEA 4.0. | gpsd AIVDM.html Table 1 | high |
| TAG blocks: "Beginning with NMEA 4.10, the standard describes a way to intersperse 'tag blocks' with AIS sentences"; format = `\` + comma-separated `key:value` fields + `*` + NMEA checksum + `\`, immediately preceding the sentence. Example: `\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\!AIVDM,1,1,,B,15N4cJ\`005Jrek0H@9n\`DW5608EP,0*13`. | gpsd AIVDM.html "NMEA Tag Blocks" | high |
| TAG block keys (NMEA 4.10): `c` UNIX time (s or ms), `d` destination (≤15 chars), `g` grouping `n-total-id`, `n` line count, `r` relative time, `s` source/station, `t` text (≤15 chars). IEC 62320-1 (NMEA 4.00 era) uses an overlapping but different key set (`c`, `d`, `xGy`, `x`, `s`, `i`). gpsd calls the facility "complex, in some respects poorly specified." | gpsd AIVDM.html Table 67 | high |
| Pre-TAG-block timestamping existed as non-standard comma-suffixed fields after the checksum (e.g., `…,0*63,s1234,d-119,T12.34567123,r003669958,1085889680`), described by gpsd as "semi-obsolescent." | gpsd AIVDM.html | high |
| AIS sentence formatters defined in IEC 61162-1 / NMEA 0183 for AIS equipment include: VDM, VDO, ABM, BBM, ABK, ACA, ACS, AIR, LRF, LRI, LR1/LR2/LR3, SSD, VSD, EPV, SPW, NAK, HBT, VER (plus TXT/ALR/ACK generic). IEC PAS 61162-100 (2002) first carried the AIS sentences before absorption into 61162-1 Ed. 3. | search summaries (SEK/elstandard abstracts, IEC) | medium |
| NMEA 2000 AIS PGNs (canboat v8.3.0 names, all Fast Packet): 129038 Class A Position Report (28 B); 129039 Class B Position Report (27 B); 129040 Class B Extended Position Report (54 B); 129041 Aids to Navigation Report; 129792 DGNSS Broadcast Binary Message; 129793 UTC and Date Report; 129794 Class A Static and Voyage Related Data (76 B); 129795 Addressed Binary Message; 129796 Acknowledge; 129797 Binary Broadcast Message; 129798 SAR Aircraft Position Report; 129800 UTC/Date Inquiry; 129801 Addressed Safety Related Message; 129802 Safety Related Broadcast Message; 129803 Interrogation; 129804 Assignment Mode Command; 129805 Data Link Management; 129806 Channel Management; 129807 Class B Group Assignment; 129809 Class B static data (msg 24 Part A); 129810 Class B static data (msg 24 Part B); 129811 Single Slot Binary Message (deprecated); proprietary 130842 Simnet AIS Class B static/silent mode. | canboat.json v8.3.0, read 2026-10-05 | high (names/lengths as canboat records them); medium that these match the official PGN titles |
| NMEA 2000 is CAN at 250 kbit/s with 29-bit identifiers, derived from SAE J1939/ISO 11783, adds "Fast Packet" transport for >8-byte PGNs; first released 2001 (development from ~1994); IEC adoption is IEC 61162-3:2008. | search summaries (NMEA, Kvaser, Wikipedia) | medium |
| NMEA 2000 documents are copyrighted; purchase and licensing by contacting NMEA (info@nmea.org, +1 410-975-9425); "NMEA 2000 Certified" requires the NMEA certification tool, a manufacturer code and product code. | search summary of nmea.org | medium |
| NMEA OneNet V1.000 released November 2020; IPv6 over IEEE 802.3; encapsulates NMEA 2000 PGNs over IP; first certified products ~2024. | search summary (NMEA press) | medium |
| RTCM SC 121 is "Automatic Identification Systems (AIS) and Digital Messaging"; SC 119 Maritime Survivor Locating Devices; SC 123 Digital Message Services over Maritime Frequencies; SC 129 Portrayal of Navigation-Related Information on Shipboard Displays; SC 137 EMC Requirements for LED Devices; SC 138 R-Mode for VDES; SC 139 Digital Maritime Messaging Service. A joint "SC121 / SC129 Virtual Meeting" is scheduled 29 Oct 2026. | rtcm.org publications page (meeting) high; SC list via search summary of rtcm.org (medium) | medium/high |
| RTCM standard ids and dates (verbatim from rtcm.org): "RTCM 12100.1, Standard for Creation and Qualification of Application-Specific Messages (ASM), June 7, 2022"; "RTCM 12110.1 Automatic Identification System (AIS) Mobile Aids to Navigation (MAtoN), June 15, 2026"; "RTCM 13300.0, Standard for Internet-Based Automatic Identification System Services (AIS-i), July 11, 2019"; "RTCM 10160.0, Standard on the Procedures for the Resetting of Own-Ship Maritime Mobile Service Identities (MMSIs) on DSC Marine Radios, and Setting and Resetting Static Data on Automatic Identification Systems (AIS), November 28, 2025"; "RTCM 11901.2, Standard for Maritime Survivor Locating Devices (MSLD) … November 14, 2024"; "RTCM 13700.0, Standard for Electromagnetic Compatibility Requirements for Light Emitting Diode (LED) Devices and Other Electrical and Electronic Equipment in the Vicinity of Shipboard Antennas for the Protection of Onboard Receivers, April 13, 2022"; "RTCM 13900.0, Standard for Maritime Messaging Service Architecture and Protocol, March 05, 2025". | https://www.rtcm.org/publications, read 2026-10-05 | high |
| RTCM 12301.1 is "Standard for VHF-FM Digital Small Message Services (VDSMS)" — short messaging ship-to-ship/shore; **not** an AIS equipment standard. The PLAN's "RTCM SC 121 et al. (verify)" is resolved: SC 121 is correct; there are no RTCM "Class A/Class B AIS" equipment standards — RTCM defers to IEC 61993-2 / 62287. | rtcm.org publications page | high |
| The only RTCM documents incorporated by reference in 47 CFR Part 80 are RTCM Paper 56-95/SC101-STD (DSC, 1995) and RTCM 11000 (406 MHz EPIRBs); no RTCM AIS document is incorporated. | eCFR § 80.7(f) and § 80.1061, read 2026-10-05 | high |
| ETSI EN 303 098 V2.2.1 (2019-02) title: "Maritime low power personal locating devices employing AIS; Harmonised Standard for access to radio spectrum". Document history: V1.2.1 Sept/Nov 2014 published as EN 303 098-1 and -2; V2.1.1 May 2016; V2.2.0 May 2017 (approval procedure); V2.2.1 vote Dec 2018–Feb 2019, published February 2019. | ETSI PDF "History" table, read 2026-10-05 | high |
| EN 303 098 scope: "specifies technical characteristics and methods of measurements for low power maritime personal locating devices employing AIS … does not cover requirements for the integrated GNSS receiver … both the radiated power and the length of time of operation are limited to enable the equipment to be sufficiently small and light to be worn comfortably at all times and to limit the operating range to a local area." Normative reference [1] is ITU-R M.1371-5 (02/2014). Annex A maps clauses to RED 2014/53/EU art. 3.2. | ETSI PDF §1, §2.1, Annex A | high |
| AIS-MOB identity (§4.4): "The User ID for a personal search and rescue equipment is 972xxyyyy, where xx = manufacturer ID 01 to 99; yyyy = the sequence number 0000 to 9999. Manufacturers IDs are issued by CIRM … except for testing purposes where the ID xx=00 can be used." Identifier not user-changeable; held in non-volatile memory. | ETSI PDF §4.4 | high |
| AIS-MOB transmitter: "transmits using modified SOTDMA on two channels AIS1 and AIS2"; AIS1 = 161,975 MHz, AIS2 = 162,025 MHz; transmitter output power 1 000 mW (ERP by dipole substitution); transmitter settling ≤ 1,0 ms; "AIS TDMA Synchronization shall be UTC direct; the equipment does not require an AIS receiver"; TDMA timing error < ±312 µs; automatic shutdown if keyed > 2 s under fault. | ETSI PDF §5.1, §5.2.0, §5.2.2, Table of nominal values (PH.AIS1/PH.AIS2/PH.TST) | high |
| AIS-MOB messages: Message 1 with Navigational Status = 14 and Message 14 text "MOB ACTIVE" (active mode); Nav Status = 15 and "MOB TEST" (test mode). Burst of 8 messages once per minute alternating AIS1/AIS2; Message 14 nominally every 4 minutes replacing one position report on each channel (1st and 5th bursts); SOTDMA comm-state pre-announces (time-out 7,6,5,4,3,2,1,0 across 8 bursts; sub-message = slot offset / UTC hour-min / increment); the 8th burst's increment to the next burst is random between 2 025 and 2 475 slots. | ETSI PDF §5.2.1, Annex B.1/B.2 | high |
| AIS-MOB start-up: begin transmitting as soon as fix, SOG, COG and UTC lock are available or within 60 s of activation; optional unsynchronised first transmission 10–30 s after activation; synchronised transmission with correct position within 5 min; continue with last known position if fix lost (time stamp 63, sync state 3); default position lon 181°/lat 91° if no fix. | ETSI PDF §5.2.2.1, Annex B.3 | high |
| AIS-MOB battery: ≥ 12 h transmitting at −20 °C ± 3 °C; battery useful life ≥ 2 years; expiry date marked; GNSS may use GPS, GLONASS and/or Galileo; position determined at least every minute. | ETSI PDF §4.7, §5.2.2, §5.2.3 | high |
| A revision of EN 303 098 is in the ETSI work programme as REN/ERM-TGMAR-637 "AMRD Group B locating devices" (early draft, 2026); V2.1.1 has lost presumption of conformity; V2.2.1 remains cited in the OJEU. | search summary (ETSI portal) | medium — (verify) on portal.etsi.org |
| CCNR adopted the "Vessel Tracking and Tracing Standard for Inland Navigation" Edition 1.0 on 31 May 2006 by Resolution 2006-I-21; Edition 1.2 adopted 29 May 2013 by Resolution 2013-I-23; CCNR "Test Standard for Inland AIS" Edition 2.0 adopted October 2012 and mandatory for type approval from 19 October 2012, tied to IEC 61993-2 Ed. 2. | search summaries citing ccr-zkr.org and cesni.eu | medium |
| EU: Regulation (EC) No 415/2007 (13 March 2007) gave the VTT specification EU legal force under RIS Directive 2005/44/EC art. 5; Commission Implementing Regulation (EU) 2019/838 of 20 February 2019 (OJ 24 May 2019) replaced and repealed it. | search summaries citing EUR-Lex | medium (EUR-Lex refused fetch; verify ELI pages) |
| CESNI ES-RIS Ed. 2021/1 was the first consolidated European RIS standard; Part II = Vessel Tracking and Tracing standard; Part III = Test Standard for Inland AIS (Ed. 3.0), mandatory for new installations from 1 January 2024; ES-RIS Ed. 2025/1 adopted 17 October 2024 (Resolution CESNI 2024-II-2) — adds Inland ECDIS tests for AIS AtoN and AIS target display (arts 5.10, 5.18, 8.09), renames "Real AIS AtoN" to "Physical AIS AtoN", clarifies "Inland AIS Application Specific Messages". | search summaries of cesni.eu and ccr-zkr.org | medium |
| Inland AIS = Class A (IEC 61993-2) plus inland extensions: ENI (unique European vessel identification number), ERI ship type, length/beam to 0.1 m, number of blue cones/lights (hazardous cargo), "blue sign" (special manoeuvre indicator) input, loaded/unloaded, draught; Inland-specific ASMs in Message 8 with DAC 200: FI 10 inland static and voyage data, FI 21 ETA at lock/bridge/terminal, FI 22 RTA, FI 23 EMMA warning, FI 24 water level, FI 40 signal status, FI 55 number of persons on board; competent authorities may assign reporting intervals (2 s–10 s moving) via Message 23 group assignment; station must process Message 23. | search summaries (ccr-zkr.org VTT text, UNECE, EU) | medium — (verify) field lists against ES-RIS Part II / 2019/838 Annex |

## Notes and quotes

- **NMEA's own warning is the book's warning.** The nmea.org page says of
  web explanations of 0183: "In most cases they are very old versions or
  incorrect interpretations and should not be depended upon for accuracy." The
  handbook should cite gpsd's AIVDM document as the best *open* description
  while being explicit that it is a re-implementation, not the standard; gpsd's
  own text concedes the TAG-block section "should be considered provisional."
- **Pricing as a barrier.** A consumer-electronics company pays US$10,000 for
  NMEA 0183 v4.30; a government lab US$7,500; individuals cannot buy it at all
  (no associate memberships "specifically to get the member discount"). This
  is the concrete reason open-source decoders were written from ITU-R M.1371
  (free) plus observed sentences, and why TAG-block handling diverges between
  implementations.
- **Two parents of the TAG block.** gpsd: "Confusingly, there is a different
  standard introduced with NMEA 4.00, IEC 62320-1, that uses the same tag block
  format but a slightly different (overlapping) set of field keys." The IEC
  62320-1 Ed. 2 (2015) change note "comment blocks replaced with TAG blocks"
  (see `r-standards-iec.md`) closes the loop: base stations now emit the NMEA
  form. Logs from older shore networks may carry the IEC key set.
- **PGN naming.** canboat records 129809/129810 as "AIS Class B static data
  (msg 24 Part A/B)" and 129811 as deprecated; PLAN ch. 26 lists 129038/39/40/
  41/793/794/798/801/802/809/810 — add 129792, 129795–129797, 129800, 129803–
  129807 for completeness in Appendix D.
- **RTCM's AIS role is "around" AIS, not the transponder.** The publications
  page shows SC 121 producing the ASM creation/qualification standard
  (12100.1), the Mobile AtoN standard (12110.1, June 2026), internet AIS
  (13300.0) and the MMSI/static-data reset procedure (10160.0, Nov 2025). The
  transponder standards remain IEC; the US rules (47 CFR § 80.231/80.275/80.233)
  cite IEC, not RTCM, for AIS. RTCM 11901.2 (MSLD) is the US-market analogue of
  ETSI EN 303 098 for MOB devices (verify whether 11901.2 cites EN 303 098 or
  IEC 61097-14 for the AIS variant). RTCM 13700.0 is the first standard aimed
  squarely at the LED-lighting interference problem (ch. 31).
- **ETSI EN 303 098 is the one free, complete AIS device standard.** Because
  ETSI publishes harmonised standards free of charge, EN 303 098 is the only
  place a reader can see a full AIS transmitter test specification (frequency
  error, conducted power, ERP, transient behaviour, timing) without paying —
  and its Annex B is a compact, concrete illustration of SOTDMA comm-state
  pre-announcement: time-out counting 7→0 across eight one-minute bursts, with
  the increment sub-message selecting the next burst "randomly … between 2 025
  slots and 2 475 slots" (i.e., 54–66 s). Quote from §5.1: "AIS TDMA
  Synchronization shall be UTC direct; the equipment does not require an AIS
  receiver." Quote from the required user warning (§4.6): "WARNING - An AIS-MOB
  Man overboard device is only intended for short range signalling to an AIS
  receiver installed onboard your own vessel. It will not directly alert the
  emergency services or other vessels".
- **MOB identity administration.** 972xx manufacturer codes are issued by
  CIRM (Comité International Radio-Maritime), not by national administrations —
  a useful ch. 13 point: MOB and SART identities are *manufacturer-serialised*,
  not licensed to a user, which is why a 972… MMSI cannot be traced to a person
  through MARS.
- **Inland AIS lineage, in one line.** CCNR VTT Ed. 1.0 (31 May 2006,
  Res. 2006-I-21) → EU Reg. 415/2007 → CCNR Test Standard Ed. 2.0 (Oct 2012,
  after IEC 61993-2 Ed. 2) → VTT Ed. 1.2 (29 May 2013, Res. 2013-I-23) →
  EU Impl. Reg. 2019/838 (20 Feb 2019) → CESNI ES-RIS 2021/1 (Part II VTT,
  Part III Test Standard Ed. 3.0; mandatory for new installs 1 Jan 2024) →
  ES-RIS 2025/1 (adopted 17 Oct 2024). The PLAN's "CCNR VTT 2006; EU 415/2007"
  and "EU 2019/838 (verify)" are confirmed at medium confidence; the ES-RIS
  step was missing from the PLAN and should be added to ch. 11/12/16.
- **Terminology drift worth a "Definitions that bite" box.** ES-RIS 2025/1
  renames "Real AIS AtoN" to "Physical AIS AtoN" (aligning with IALA/IEC 62288
  usage); older Inland and IEC documents say "real".

## Open questions / (verify)

- NMEA 0183 version dates other than 4.30 (Dec 2023) and 4.11 (27 Nov 2018):
  confirm 4.00 = 2008 and 4.10 = 2012 from an NMEA source; confirm in which
  version `!AIVDM`/`!AIVDO` first appeared (IEC PAS 61162-100 in 2002 suggests
  NMEA 0183 v3.01 era) and whether NMEA 4.10 or 4.00 introduced TAG blocks
  (gpsd says 4.10; some vendors say 4.00).
- Official NMEA 2000 PGN titles for the AIS group (canboat names may differ
  slightly from the copyrighted Appendix B titles); confirm 129811 deprecation
  and whether a PGN exists for Message 27 or Message 25/26 multi-slot binary.
- NMEA 2000 licensing cost figures (none found on the public page; the search
  summary gave none). Record "contact NMEA" rather than a number.
- OneNet: confirm release date (Nov 2020 per press) and whether any AIS
  transponder ships with OneNet as of 2026.
- RTCM SC roster: confirm from rtcm.org that SC 121's current title is "AIS and
  Digital Messaging" and list its chair/last meeting if citing the committee.
- RTCM 11901.2 (MSLD): does it define an AIS-based MSLD class by reference to
  EN 303 098 / M.1371 / 972 MMSIs? (Needed for ch. 68.)
- RTCM 10160.0: what procedure does it prescribe for resetting a Class B
  MMSI (relevant to the FCC § 80.231 "no user entry" rule and to MMSI reuse in
  ch. 13/36)?
- ETSI: confirm REN/ERM-TGMAR-637 status and target version number for the
  EN 303 098 successor; confirm current OJEU citation of V2.2.1.
- CCNR/CESNI: fetch the actual PDFs (ccr-zkr.org "RIS" document pages; cesni.eu
  ES-RIS page) to confirm resolution numbers 2006-I-21 and 2013-I-23, the
  19 Oct 2012 test-standard date, ES-RIS 2021/1 adoption date, and the DAC 200
  FI list and field layouts (FI 10 bit layout for ENI, blue cones, loaded flag).
- EU 2019/838: confirm date of entry into force (OJ L 138, 24 May 2019 per
  search) and whether later amendments exist (2024–2026).
- Inland AIS reporting-interval table (2 s/10 s moving; 10 min static?) and the
  exact Message 23 usage — confirm against ES-RIS Part II.
- Whether CESNI publishes an "Inland AIS Test Standard Ed. 3.x" revision after
  M.1371-6 (2026).

## Candidate figures and worked examples

- **On the wire (ch. 26):** annotated `!AIVDM,1,1,,B,177KQJ5000G?tO\`K>RA1wUbN0TKH,0*5C`
  with each field labelled; second panel with the gpsd TAG-block example
  `\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\!AIVDM,…` showing the two
  checksums, the group triple, and the UNIX timestamp (1241544035 =
  2009-05-05T17:20:35Z, checked with Python `datetime` this session).
- **Worked example (ch. 26):** 6-bit armoring by hand: character `1` (ASCII 49)
  → 1 → `000001`; character `w` (ASCII 119) → 71 → 71−8 = 63 → `111111`; show
  the unused `X`–`_` gap.
- **Table (ch. 26 / App. D):** talker IDs (AB, AD, AI, AN, AR, AS, AT, AX, SA;
  BS deprecated) with station type.
- **Table (ch. 26 / App. D):** NMEA 2000 AIS PGNs with canboat byte lengths and
  the M.1371 message(s) each carries (129038 ↔ Msg 1/2/3; 129039 ↔ 18; 129040 ↔
  19; 129041 ↔ 21; 129793 ↔ 4/11; 129794 ↔ 5; 129798 ↔ 9; 129801 ↔ 12; 129802
  ↔ 14; 129809/129810 ↔ 24A/24B; 129806 ↔ 22; 129805 ↔ 20; 129804 ↔ 16;
  129807 ↔ 23; 129803 ↔ 15; 129795/129797 ↔ 6/8; 129796 ↔ 7/13; 129792 ↔ 17;
  129800 ↔ 10).
- **Figure (ch. 21/24/68):** the EN 303 098 Annex B burst timeline — eight
  one-minute bursts of eight messages alternating AIS1/AIS2, time-out 7…0,
  Message 14 in bursts 1 and 5, random 2 025–2 475-slot increment at burst 8.
  A clean, citable illustration of SOTDMA pre-announcement without needing
  M.1371 text.
- **Worked example (ch. 27):** 1 W ERP MOB at sea level (antenna ~0.3 m above
  water when worn) vs a ship receiver at 20 m — radio horizon and link budget
  show why EN 303 098 says "short range signalling … onboard your own vessel".
- **Timeline figure (ch. 11/12/16):** Inland AIS lineage 2006 → 2007 → 2012 →
  2013 → 2019 → 2021 → 2024/2025 (CCNR → EU → CESNI).
- **Table (ch. 23):** DAC 200 FI table (10, 21, 22, 23, 24, 40, 55) with
  purpose and direction (ship→shore / shore→ship) — pending field verification.
- **Table (ch. 14/15):** who publishes what, and what it costs: ITU (free),
  IMO (mostly free circulars), IEC (paid, CHF), NMEA (US$1,150–10,000, companies
  only), RTCM (paid, store), ETSI (free), CCNR/CESNI (free), EUR-Lex (free).

## Recommended use by chapter

- **Ch. 11** — Class B/Inland/MOB milestones: CCNR VTT 31 May 2006; EN 303
  098-1/-2 V1.2.1 (2014) as the first MOB harmonised standard; RTCM AIS-i 2019.
- **Ch. 12** — EU 2019/838 (2019), ES-RIS 2021/1 and 2025/1, RTCM MAtoN 12110.1
  (June 2026), RTCM 10160.0 (Nov 2025), NMEA 0183 v4.30 (Dec 2023), OneNet.
- **Ch. 13** — 972xxyyyy MOB identities issued via CIRM manufacturer codes;
  RTCM 10160.0 reset procedures; FCC § 80.231(b) "no user entry" label text.
- **Ch. 14** — organisation entries for NMEA (standards committee; pricing
  model), RTCM (SC 121/119/129/137/138/139), ETSI (ERM TG MAR), CIRM (MOB
  manufacturer IDs), CCNR and CESNI.
- **Ch. 15** — "what is free, what is paid" paragraph; NMEA's copyright stance;
  gpsd as the open reference; TAG-block dual parentage.
- **Ch. 16** — RED 2014/53/EU art. 3.2 and harmonised standards; Directive
  2005/44/EC, Reg. 415/2007, Impl. Reg. 2019/838; note that 47 CFR cites no
  RTCM AIS document.
- **Ch. 20** — add Inland AIS and AIS-MOB rows (1 W, UTC-direct, no receiver,
  Messages 1/14) to the station-class table.
- **Ch. 21 / 24** — EN 303 098 Annex B as a worked SOTDMA comm-state example;
  "UTC direct" without a receiver as the minimal timing architecture.
- **Ch. 22 / 23** — Nav status 14 = "AIS-SART is active" (and MOB/EPIRB-AIS)
  and 15 = test; DAC 200 inland FIs; ASM qualification via RTCM 12100.1 and
  the IALA ASM collection.
- **Ch. 26** — primary consumer: sentence anatomy, armoring, talker IDs, TAG
  blocks and their checksums, pre-TAG suffix formats, NMEA 2000 PGNs and Fast
  Packet, OneNet; cite gpsd and canboat as open sources and NMEA as the
  authority.
- **Ch. 31** — RTCM 13700.0 (LED EMC near antennas, 2022) alongside the USCG
  safety alert.
- **Ch. 36** — static-data misconfiguration and the RTCM 10160.0 reset
  standard; FCC installer-only programming rule.
- **Ch. 44** — IEC PAS 61162-100 (2002) and NMEA v3.x as the era in which
  `!AIVDM` appeared; why aisparser/noaadata/gpsd/libais parsed from M.1371 and
  observed logs rather than the NMEA text.
- **Ch. 68** — AIS-MOB per EN 303 098 (full requirement set above); RTCM
  11901.2 MSLD as US counterpart; Inland AIS as a Class A variant; Mobile AtoN
  per RTCM 12110.1.
- **Appendix B / D** — register rows for all documents above; talker-ID and
  PGN tables.
