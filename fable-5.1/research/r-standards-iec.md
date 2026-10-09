# Dossier: IEC standards for AIS (TC 80 equipment, interface, display, and VDR standards)

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the International Electrotechnical Commission (IEC) standards that turn
the IMO performance standard (MSC.74(69) Annex 3) and the ITU-R M.1371 technical
characteristics into *testable* equipment requirements: IEC 61993-2 (Class A),
IEC 62287-1/-2 (Class B CS / Class B SO), IEC 62320-1/-2/-3 (base stations,
AtoN stations, repeaters), IEC 61097-14 (AIS-SART), the IEC 61162 digital
interface family (-1, -2, -3, -450, -460), IEC 62288 (presentation on displays),
IEC 61174 (ECDIS), IEC 62388 (radar with AIS targets), IEC 61996-1/-2 (VDR /
S-VDR), and IEC 60945 (general requirements / EMC / environmental). It also
records *which editions* the US (47 CFR Part 80) and the EU Marine Equipment
Directive incorporate, because those lag the current IEC editions. It feeds
**Chapter 10** (standardization 1996–2004; 61993-2 Ed. 1 in 2001), **Chapter 11**
(Class B 2006, AtoN 2008, SART 2010), **Chapter 15** (how the standards fit
together), **Chapter 16** (what the law incorporates), **Chapter 20** (station
classes), **Chapter 24/25** (timing and GNSS test requirements), **Chapter 26**
(IEC 61162 interfaces), **Chapter 27/28** (sensitivity and power tests),
**Chapter 31** (IEC 60945 EMC), **Chapter 36** (failure modes caught by test),
**Chapter 51/56** (62288, 61174, 62388, 61996), **Chapter 60** (61162-460),
**Chapter 68** (SART/MOB), and **Appendix B** (standards register).

> Research-session note. IEC does not publish the body of its standards for
> free, and the IEC webstore search API now requires a login, so most abstracts
> and "significant changes" lists below were confirmed through web-search
> summaries of the IEC webstore / national-adopter pages (BSI, SIS, DS, SEK,
> iTeh previews) rather than from the standard text. Those are marked
> *medium*. Items read directly from a primary page in this session (eCFR
> 47 CFR 80.7/80.231/80.233/80.275/80.1101; the gpsd AIVDM document; the ETSI
> EN 303 098 PDF) are marked *high*. The ITU-side facts (M.1371 editions,
> physical-layer constants) live in `r-standards-itu.md` and are not repeated
> here.

## Key questions

1. Which IEC document tests which AIS station class, and what are the current
   editions and publication dates? What did each edition change?
2. What does a "test standard" actually contain (operational requirements,
   methods of test, required results), and how does it relate to MSC.74(69),
   ITU-R M.1371, and IEC 60945?
3. Which specific behaviours that matter to this book are *required by test*
   rather than merely described in M.1371 — internal GNSS, sensitivity/PER,
   power levels, timing, configuration security (SSA sentence), BAM, software
   update, 61162-450 interfaces?
4. How are the IEC 61162 parts organised (serial 4,800 bit/s; 38,400 bit/s;
   NMEA 2000/CAN; Ethernet "LWE"; security gateway), which editions are current
   (several moved to 2024 editions), and where do TAG blocks and the `UdPbC`
   datagram header come from?
5. Which IEC standards govern how AIS targets are *drawn* (62288), fused with
   radar (62388), shown on ECDIS (61174), and recorded (61996)?
6. Which IEC editions do 47 CFR Part 80 and the EU MED actually incorporate by
   reference — and how far behind the current IEC editions are they?
7. Where can a reader obtain these documents and what do they cost?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| IEC 61993-2 Ed. 3.0 | IEC 61993-2:2018, published 2018-07-19 (Ed. 1.0 2001-12; Ed. 2.0 2012-10) | https://webstore.iec.ch/ (search "61993-2") | Class A shipborne AIS — operational and performance requirements, methods of test, required test results | Paid (IEC webstore; CHF pricing) |
| IEC 62287-1 Ed. 3.0 | IEC 62287-1:2017, published 2017-04-05 (Ed. 1.0 2006-03; Ed. 2.0 2010) | https://webstore.iec.ch/ (search "62287-1") | Class B shipborne AIS — Part 1: CSTDMA ("Class B CS") | Paid |
| IEC 62287-2 Ed. 2.0 | IEC 62287-2:2017 (Ed. 1.0 2013) | https://webstore.iec.ch/ (search "62287-2") | Class B shipborne AIS — Part 2: SOTDMA ("Class B SO", marketed as "B+") | Paid |
| IEC 62320-1 Ed. 2.0 | IEC 62320-1:2015 (Ed. 1.0 2007 + AMD1:2008) | https://webstore.iec.ch/ (search "62320-1") | AIS base stations — minimum operational and performance requirements, test methods | Paid |
| IEC 62320-2 Ed. 2.0 | IEC 62320-2:2016 (Ed. 1.0 2008) (verify month; one adopter page says 2017) | https://webstore.iec.ch/ (search "62320-2") | AIS AtoN stations (Types 1, 2, 3; physical/synthetic/virtual AtoN) | Paid |
| IEC 62320-3 Ed. 1.0 | IEC 62320-3:2015 | https://webstore.iec.ch/ (search "62320-3") | AIS repeater stations | Paid |
| IEC 61097-14 Ed. 1.0 | IEC 61097-14:2010, 2010-02 | https://webstore.iec.ch/ (search "61097-14") | GMDSS Part 14: AIS search and rescue transmitter (AIS-SART) | Paid |
| IEC 61162-1 Ed. 6.0 | IEC 61162-1:2024, published 2024-04-04 (Ed. 5.0 2016; Ed. 4.0 2010; Ed. 3.0 2007-04; Ed. 2.0 2000; Ed. 1.0 1995) | https://webstore.iec.ch/ (search "61162-1") | Digital interfaces — single talker, multiple listeners (the IEC twin of NMEA 0183, 4,800 bit/s) | Paid |
| IEC 61162-2 Ed. 2.0 | IEC 61162-2:2024 (Ed. 1.0 1998) | https://webstore.iec.ch/ (search "61162-2") | Single talker, multiple listeners, high-speed (38,400 bit/s; NMEA 0183-HS twin) | Paid |
| IEC 61162-3 Ed. 1.0 + AMD1 + AMD2 | IEC 61162-3:2008 + AMD1:2010 + AMD2:2014 (consolidated 1.2) | https://webstore.iec.ch/ (search "61162-3") | Serial data instrument network (IEC adoption of NMEA 2000 / CAN) | Paid |
| IEC 61162-450 Ed. 3.0 | IEC 61162-450:2024 (Ed. 2.0 2018; Ed. 1.0 2011) | https://webstore.iec.ch/ (search "61162-450") | Multiple talkers and multiple listeners — Ethernet interconnection ("Lightweight Ethernet", UDP multicast) | Paid |
| IEC 61162-460 Ed. 3.0 | IEC 61162-460:2024 (Ed. 2.0 2018 + AMD1:2020; Ed. 1.0 2015) | https://webstore.iec.ch/ (search "61162-460") | Ethernet interconnection — safety and security (460-Gateway, 460-Forwarder, network monitoring) | Paid |
| IEC 62288 Ed. 3.0 | IEC 62288:2021 (+ AMD1:2024 (verify)) (Ed. 2.0 2014; Ed. 1.0 2008) | https://webstore.iec.ch/ (search "62288") | Presentation of navigation-related information on shipborne navigational displays (AIS/ASM/DSC symbology; supports MSC.191(79) as amended by MSC.466(101) and SN.1/Circ.243) | Paid |
| IEC 61174 Ed. 4.0 | IEC 61174:2015, 2015-08 (Ed. 3.0 2008; Ed. 2.0 2001; Ed. 1.0 1998) | https://webstore.iec.ch/ (search "61174") | ECDIS operational and performance requirements (MSC.232(82)); adds radar/AIS overlay, BAM, VDR, route transfer | Paid |
| IEC 62388 Ed. 2.0 | IEC 62388:2013, 2013-06 (Ed. 1.0 2007-12) | https://webstore.iec.ch/ (search "62388") | Shipborne radar (MSC.192(79)) including AIS target integration, lost-target and CPA/TCPA alert tests | Paid |
| IEC 61996-1 Ed. 2.0 | IEC 61996-1:2013 (+ AMD1:2021) | https://webstore.iec.ch/ (search "61996-1") | Voyage data recorder (VDR), performance per MSC.333(90); records "all AIS data" | Paid |
| IEC 61996-2 Ed. 2.0 | IEC 61996-2:2007 | https://webstore.iec.ch/ (search "61996-2") | Simplified VDR (S-VDR), MSC.163(78) | Paid |
| IEC 60945 Ed. 4.0 | IEC 60945:2002, 2002-08 (+ COR1:2008) | https://webstore.iec.ch/ (search "60945") | General requirements — methods of testing and required test results (environmental, EMC, safety) for all marine nav/radio equipment, per A.694(17) | Paid |
| IEC 61993-1 (withdrawn) | IEC 61993-1:1999, withdrawn 2018-12-31 | https://webstore.iec.ch/ (search "61993-1") | Shipborne automatic transponder using VHF DSC — the pre-TDMA "AIS Part 1" | Withdrawn |
| IEC PAS 61162-100 (withdrawn) | IEC PAS 61162-100:2002 | — | Extra 61162-1 requirements for UAIS (first home of the AIS sentences before 61162-1 Ed. 3) | Withdrawn; content absorbed in 61162-1 |
| IEC 62923-1/-2 | IEC 62923-1:2018, IEC 62923-2:2018 | https://webstore.iec.ch/ (search "62923") | Bridge alert management (BAM); referenced by 61993-2 Ed. 3 and 61162-460 Ed. 3 | Paid |
| IEC 61108-1 | IEC 61108-1:2003 (Ed. 2) | https://webstore.iec.ch/ (search "61108-1") | GPS receiver equipment (MSC.112(73)); the GNSS performance baseline cited by AIS/MOB standards | Paid |
| IEC TC 80 committee page | TC 80 "Maritime navigation and radiocommunication equipment and systems" | https://www.iec.ch/dyn/www/f?p=103:7:::::FSP_ORG_ID:1261 (verify exact URL) | Scope, working groups (WG 15 = AIS / e-navigation related) | Free |
| 47 CFR § 80.7 (eCFR) | current as of 2026-10-01 | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-80/subpart-A/section-80.7 | US incorporations by reference: lists exact IEC editions | Free |
| 47 CFR § 80.1101, § 80.231, § 80.233, § 80.275 (eCFR) | current as of 2026-10-01 | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-80/subpart-W/section-80.1101 (and sibling sections) | Which standards Class A, Class B, and AIS-SART must meet in the US; USCG letter procedure | Free |
| gpsd "AIVDM/AIVDO protocol decoding" | v1.58, 24 June 2023, E. S. Raymond (with K. Schwehr contributions) | https://gpsd.gitlab.io/gpsd/AIVDM.html | Open description of the VDM/VDO sentences, talker IDs, armoring, TAG blocks; notes that IEC 62320-1 TAG keys differ from NMEA 4.10 | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| IEC 61993-2:2018 is Edition 3.0, published 19 July 2018; it cancels and replaces Edition 2.0 (2012). | IEC webstore abstract via search (iec.ch, mystandards.biz, nimonik) | medium |
| IEC 61993-2 Edition 1.0 was published December 2001 ("IEC 61993-2:2001(E) First edition, 2001-12") and is the edition still incorporated by reference in 47 CFR § 80.7. | eCFR § 80.7(d)(17), read 2026-10-05 | high |
| 61993-2 full title: "Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the universal automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results". | eCFR § 80.7(d)(17) | high |
| 61993-2 Ed. 3 significant changes (per IEC foreword as summarised): incorporates ITU-R M.1371-5 (2014); introduces "locating device groups" (AIS-SART, AIS-MOB, EPIRB-AIS); adds configuration-input security with a new `SSA` sentence; adds optional IEC 61162-450/-460 interfaces; adds Bridge Alert Management (BAM) requirements; adds extended dimension values for towing vessels; adds a software-update requirement. | IEC abstract via search (iec.ch, nimonik) | medium |
| 61993-2 states that where its requirements differ from IEC 60945, 61993-2 takes precedence; it conforms to MSC.74(69) Annex 3 and takes account of A.694(17). | IEC abstract via search | medium |
| IEC 62287-1:2017 is Edition 3.0, published 5 April 2017; "notable technical change: addition of a direct method for synchronisation from an internal UTC source." Earlier editions: Ed. 1.0 2006-03, Ed. 2.0 2010. | IEC abstract via search; eCFR § 80.7(d)(19) for Ed. 1.0 date | medium (ed. 3 details); high (Ed. 1.0 = 2006-03) |
| 47 CFR § 80.231(a): "Class B Automatic Identification System (AIS) equipment must meet the technical requirements of IEC 62287-1"; § 80.7 incorporates **IEC 62287-1:2006 (First edition, 2006-03)**. § 80.231 does not reference IEC 62287-2 (Class B SO). | eCFR § 80.231 and § 80.7, read 2026-10-05 | high |
| 47 CFR § 80.231(b) requires a Class B device label with the statement: "WARNING: It is a violation of the rules of the Federal Communications Commission to input an MMSI that has not been properly assigned to the end user, or to otherwise input any inaccurate data in this device," and prohibits the end user from entering static data (vendor or qualified installer only). | eCFR § 80.231(b) | high |
| 47 CFR § 80.1101(c)(12) lists the AIS performance standards as ITU-R M.1371-3, IMO Resolution MSC.74(69), IEC 61162-1, IEC 61993-2; § 80.7 fixes those at M.1371-3 (2007) and IEC 61162-1:2007 (Third edition, 2007-04). | eCFR § 80.1101 and § 80.7 | high |
| 47 CFR § 80.233(a): AIS-SART "must meet the technical requirements of IEC 61097-14 and IMO Resolution MSC.246(83)"; § 80.7 incorporates IEC 61097-14 Edition 1.0, 2010-02. | eCFR § 80.233 and § 80.7 | high |
| 47 CFR § 80.275 / § 80.231 / § 80.233 all require a USCG letter (test report submitted to the Commandant) stating the device satisfies the IEC standard before an FCC certification application. | eCFR, read 2026-10-05 | high |
| 47 CFR § 80.1101(b) general requirements incorporate IEC 60945 (IEC 60945:2002, Fourth edition, 2002-08) and § 80.1101(c)(11) incorporates IEC 62388 Edition 1.0 (2007-12) for radar. | eCFR § 80.1101, § 80.7 | high |
| IEC 62287-2:2017 covers Class B "SO" (SOTDMA) shipborne equipment; Ed. 1.0 was 2013. | IEC/iTeh abstracts via search | medium |
| IEC 62320-1:2015 (Ed. 2.0) replaces Ed. 1.0 (2007) + AMD1 (2008); changes: incorporates M.1371-5; BCE/BCF/CAB sentences replaced by BCG/BCL/RST; "comment blocks replaced with TAG blocks"; adds transmission of Messages 24A, 25, 26 and scheduled broadcast of Message 26; adds control for Message 27; removes 12.5 kHz channel operation; adds a 90 % channel-load test (with VSI and TAG blocks enabled); harmonises transmitter intermodulation attenuation with ITU. | IEC abstract via search | medium |
| IEC 62320-2:2016 (Ed. 2.0) replaces Ed. 1.0 (2008); changes: adds cyber-security measures; updates configuration via VDL; requires at least one standard configuration method using PI sentences; updates VDL access-scheme requirements; adds new PI sentences and VDL message structures incl. optional TAG blocks; updates test methods and annexes. AtoN station Types 1/2/3 are defined in this standard (Type 1 = limited, typically FATDMA-only/low-power; Types 2/3 add receive and more access schemes). | IEC abstract via search | medium (type definitions: verify against text) |
| IEC 62320-3:2015 (Ed. 1.0) specifies AIS repeater stations; IEC states it incorporates characteristics from ITU-R M.1371 and IALA Recommendation A-124 and "does not include specifications for the display of AIS data on shore." | IEC abstract via search (iec.ch) | medium |
| IEC 61097-14:2010 (Ed. 1.0, 2010-02) specifies AIS-SART minimum performance, technical characteristics and test methods, incorporating MSC.246(83) and SOLAS Ch. III/IV carriage context; 61097-14 takes precedence over 60945 where they differ. | eCFR § 80.7(d)(14) for id/date (high); abstract via search for content (medium) | high / medium |
| IEC 61162-1:2024 (Ed. 6.0) was published 4 April 2024 and supersedes Ed. 5.0 (2016). Ed. 5.0 "introduced new sentence identifiers and removed certain sentences used solely by shore-based AIS equipment." | IEC webstore via search | medium |
| IEC 61162-2:2024 (Ed. 2.0) supersedes IEC 61162-2:1998 (38,400 bit/s single talker/multiple listeners). | IEC webstore via search | medium |
| IEC 61162-3:2008 is the IEC adoption of NMEA 2000 (CAN, 250 kbit/s) with AMD1:2010 and AMD2:2014. | search summary (IEC webstore) | medium |
| IEC 61162-450:2024 (Ed. 3.0) supersedes Ed. 2.0 (2018), which replaced Ed. 1.0 (2011). Ed. 2.0 added IGMP snooping guidance, traffic balancing and authentication tags. | IEC webstore via search | medium |
| IEC 61162-450 datagrams carrying 61162-1 sentences begin with the null-terminated header `UdPbC\0`, followed by an optional TAG block and the sentence; multicast groups are in 239.192.0.1–239.192.0.16 with UDP ports 60001–60016 (e.g., 239.192.0.3/60003 for satellite-navigation data). Transmission-group names such as MISC, NAVD, VDRD, SATD are used to route traffic. | Secondary sources (gitlab project docs, vendor notes) via search; gpsd doc for TAG blocks | medium — (verify) exact group table against 61162-450 text |
| IEC 61162-460:2024 (Ed. 3.0) changes vs 2018+AMD1:2020: alert management aligned with MSC.302(87) and IEC 62923-1/-2; network-monitoring load alert limit changed from 80 % to 90 %; "application server" renamed "application service"; Annex F removed. Ed. 2.0 (2018) mandated 460-Forwarders between secure and non-secure areas and standardised alert identifiers. | IEC webstore via search | medium |
| IEC 62288:2021 (Ed. 3.0) adds requirements for presentation of AIS data, AIS ASM and DSC (new Annexes J, K, L); supports MSC.191(79) as amended by MSC.466(101) (June 2019), MSC.1/Circ.1609 and SN.1/Circ.289; symbol sets per SN.1/Circ.243 (rev. 2019) incl. sleeping/activated/selected/dangerous AIS targets and physical vs virtual AIS AtoN. | IEC/elstandard abstract via search | medium |
| IEC 61174:2015 (Ed. 4.0, 2015-08) added display of radar and AIS information on ECDIS, interfaces for BNWAS, VDR, BAM, MSI, INS and route transfer, anchor watch, updated IHO test data sets and extended latitude range. | IEC abstract via search (iec.ch, LR) | medium |
| IEC 62388:2013 (Ed. 2.0, 2013-06) requires that radar tracking and AIS target information be presented consistently "as far as practical", and includes tests for lost AIS target criteria and CPA/TCPA alerts. | abstracts via search | medium |
| IEC 61996-1:2013 (Ed. 2.0; AMD1:2021) requires recording of "all AIS data"; fixed and float-free media retain ≥ 48 h, long-term medium ≥ 30 days (720 h), per MSC.333(90). | iTeh preview and IMO resolution via search | medium |
| IEC 60945 Edition 4.0 was published August 2002; COR1 (2008) updated normative references (CISPR 16) without changing requirements. | search summary (VDE, intertek) | medium |
| IEC 61993-1:1999 (DSC-based transponder) was withdrawn 31 December 2018. | IEC webstore via search | medium |
| IEC 62923-1:2018 (BAM) is mandatory under the EU MED for navigation/radio equipment installed after 29 August 2021. | DNV note via search | medium |
| IEC TC 80 scope: "to prepare international standards for maritime navigation and radiocommunication equipment and systems … for use on ships and, where appropriate, on shore"; WG 15 is the AIS-related working group. | iec.ch TC page via search | medium |

## Notes and quotes

- **What "test standard" means.** Each TC 80 equipment standard follows the
  same pattern, visible in the common subtitle: *"Operational and performance
  requirements, methods of test and required test results."* The IMO
  resolution says what the equipment must do; M.1371 says how the radio and
  link layer work; the IEC document says *how a laboratory proves it* and what
  numbers pass. IEC 60945 supplies the environmental/EMC/safety test regime
  shared by all of them. The 61993-2 abstract (as summarised by IEC) says the
  document "specifies the minimum operational and performance requirements,
  methods of testing and required test results … conforms to performance
  standards adopted by IMO in Resolution MSC.74(69):1998, Annex 3 … incorporates
  the applicable technical characteristics … in Recommendation ITU-R M.1371 …
  and takes into account ITU Radio Regulations where applicable."
- **The lag between IEC and law.** 47 CFR § 80.7, read on 2026-10-05, still
  incorporates **IEC 61993-2:2001 (Ed. 1)**, **IEC 62287-1:2006 (Ed. 1)**,
  **IEC 61162-1:2007 (Ed. 3)**, **ITU-R M.1371-3 (2007)** and **IEC 62388 Ed. 1
  (2007-12)**. The current IEC editions are 2018, 2017, 2024, (M.1371-6 2026)
  and 2013 respectively. In practice the FCC/USCG accept test reports against
  current editions (verify: find the USCG CG-ENG-4 policy letter or FCC
  guidance that says so), but the regulation text is a 2001–2007 snapshot. The
  eCFR history line for § 80.1101 shows amendments at 68 FR 46977 (7 Aug 2003),
  69 FR 64680 (8 Nov 2004), 73 FR 4490 (25 Jan 2008), 74 FR 5125 (29 Jan
  2009), 76 FR 67617 (2 Nov 2011) — nothing since 2011.
- **Class B SO has no US rule hook.** § 80.231 names only IEC 62287-1
  (CSTDMA). Class B SO ("B+") devices are sold in the US (verify how they are
  certified — likely under § 80.231 by waiver or under a later FCC order; find
  the FCC DA/FCC number).
- **Internal GNSS.** The book's claim (ch. 24/25) that Class A must carry an
  internal GNSS for timing even when an external EPFS is used comes from
  61993-2 clauses on "internal GNSS receiver" and UTC synchronisation; the
  62287-1 Ed. 3 change note ("direct method for synchronisation from an
  internal UTC source") confirms Class B CS also synchronises from internal
  GNSS. Exact clause numbers (verify) require the paid text.
- **Sensitivity and PER.** The widely quoted Class A receiver figure "−107 dBm
  for 20 % PER" is consistent with M.1371 and with vendor test reports found in
  search (device.report, Government of Canada RSS test docs), but the 61993-2
  clause number was not read in this session (verify). Base stations and
  modern transceivers commonly specify −112 dBm @ 20 % PER.
- **TAG blocks have two parents.** gpsd's AIVDM document notes: "Confusingly,
  there is a different standard introduced with NMEA 4.00, IEC 62320-1, that
  uses the same tag block format but a slightly different (overlapping) set of
  field keys" — and tabulates IEC keys (`c`, `d`, `xGy`, `x`, `s`, `i`) against
  NMEA keys (`c`, `d`, `g`, `n`, `r`, `s`, `t`). The 62320-1 Ed. 2 change note
  "comment blocks replaced with TAG blocks" confirms the base-station standard
  moved from its own "comment block" to the NMEA TAG block.
- **IEC 62288 is where the triangle comes from.** The AIS target symbols
  (sleeping, activated, selected, dangerous, lost), the heading/COG vector
  conventions and the physical-vs-virtual AtoN symbols on type-approved
  displays are specified in 62288 (via SN.1/Circ.243). Ed. 3 (2021) is the
  first to add explicit ASM presentation annexes — relevant to ch. 23's
  discussion of why ASM uptake stayed low (no display standard until 2021).
- **The withdrawn DSC AIS.** IEC 61993-1:1999 standardised the pre-TDMA
  "automatic transponder" using VHF DSC (the system the USCG tanker tracking
  and Dover trials used; see `r-history.md`). Its withdrawal date (31 Dec 2018)
  is a tidy end-point for the DSC-AIS story in ch. 9/10.

## Open questions / (verify)

- Exact publication month of IEC 62320-2 Ed. 2.0 (2016 per IEC search summary;
  one national adopter lists 2017). Check the IEC webstore record.
- Whether IEC 61993-2:2018 has any amendment or corrigendum as of 2026 (search
  found none; confirm on the webstore "Amendments/Corrigenda" tab).
- Clause numbers in IEC 61993-2 Ed. 3 for: internal GNSS/UTC sync; receiver
  sensitivity and PER; transmitter power (12.5 W / 1 W) and tolerance; slot
  timing accuracy; `SSA` password/configuration security; software update;
  BAM; towing-vessel extended dimensions.
- Clause numbers in IEC 62287-1 Ed. 3 for the CSTDMA carrier-sense window and
  the 2 W power level, and in 62287-2 for 5 W.
- AtoN Type 1/2/3 definitions and access-scheme table in IEC 62320-2 (the
  dossier's description is from secondary summaries).
- The 61162-450 transmission-group table (names, multicast addresses, ports)
  and the 61162-450 "SFI" (system function ID) format — confirm against the
  standard before printing in ch. 26.
- IEC 62288:2021 AMD1:2024 — existence and content (mentioned in one search
  result in connection with EU MED citations).
- The EU Marine Equipment Directive implementing regulation number currently
  in force and the MED item number for AIS Class A (search returned
  "MED/4.14" and regulation numbers 2025/1533 and 2026/1434 **without grounding
  citations** — treat as unverified; confirm on EUR-Lex and the MarED database).
- Which IEC TC 80 working group (WG 15 per search) currently maintains the AIS
  standards, and whether a 61993-2 Ed. 4 project aligned to M.1371-6 (2026) is
  open (check the IEC TC 80 work programme).
- US treatment of Class B SO devices (no IEC 62287-2 reference in § 80.231).
- IEC 60945 Ed. 5 status (TC 80 has had a revision project for years; verify).
- IEC 61162-1 Ed. 6 (2024) change list relevant to AIS sentences.
- Price points: capture the CHF price for 61993-2, 62287-1, 61162-1 from the
  webstore for the "where to buy / what it costs" paragraph in ch. 15.

## Candidate figures and worked examples

- **Figure (ch. 15):** "Standards stack" diagram — IMO MSC.74(69) → ITU-R
  M.1371 → IEC 61993-2 / 62287 / 62320 / 61097-14 → IEC 60945 (shared) → IEC
  61162 (interfaces) → IEC 62288 / 61174 / 62388 (display) → IEC 61996
  (recording) → national type approval (47 CFR 80 / EU MED). Annotate each box
  with current edition and year.
- **Table (ch. 15 / App. B):** edition timeline per standard (1995 → 2024),
  with a second column showing the edition incorporated in 47 CFR § 80.7 to
  make the regulatory lag visible.
- **Table (ch. 20):** station class ↔ IEC standard ↔ power ↔ access scheme
  (Class A 61993-2 12.5/1 W SOTDMA/ITDMA/RATDMA/FATDMA; Class B CS 62287-1 2 W
  CSTDMA; Class B SO 62287-2 5 W SOTDMA; base 62320-1; AtoN 62320-2 Types 1–3;
  repeater 62320-3; SART 61097-14 1 W; MOB ETSI EN 303 098 1 W).
- **Worked example (ch. 26):** a 61162-450 UDP datagram: `UdPbC\0` + TAG block
  `\s:AI0001,c:1696500000*hh\` + `!AIVDM,…` — show the two checksums and the
  multicast address/port; contrast with the same sentence on a 4,800 bit/s
  61162-1 line (and why multi-sentence Message 5 at 4,800 bit/s takes ~0.2 s).
- **Worked example (ch. 36):** what the annual test (MSC.1/Circ.1252) checks
  versus what type approval under 61993-2 checked once — e.g., the on-air
  power and VSWR check vs the full receiver sensitivity test.
- **Box (ch. 16, Legal note):** "The CFR cites the 2001 edition" — quote
  § 80.7(d)(17) and § 80.231(b) verbatim.

## Recommended use by chapter

- **Ch. 10** — IEC 61993-2 Ed. 1 (Dec 2001) as the type-approval enabler for
  the July 2002 SOLAS carriage start; IEC 61993-1:1999 as the DSC dead end.
- **Ch. 11** — IEC 62287-1 Ed. 1 (Mar 2006) as the birth of Class B; 62320-1
  (2007) and 62320-2 (2008) for shore/AtoN; 61097-14 (Feb 2010) for AIS-SART;
  62287-2 (2013) for Class B SO; 61162-450 (2011) for LWE.
- **Ch. 12** — 2015–2018 refresh wave (62320-1/-3 2015, 62320-2 2016, 62287
  2017, 61993-2 2018) tracking M.1371-5; 2024 refresh of the 61162 family; the
  question of a 61993-2 Ed. 4 after M.1371-6 (2026).
- **Ch. 15** — standards stack figure; "test standard" definition; where to
  buy and cost; the US/EU lag table; note that IEC text is paywalled while ITU
  and IMO circulars are mostly free.
- **Ch. 16** — eCFR quotations (§ 80.7, § 80.231, § 80.233, § 80.275,
  § 80.1101); MED pointer (verify regulation number).
- **Ch. 20** — class ↔ standard ↔ power table; AtoN Types 1–3 from 62320-2.
- **Ch. 24 / 25** — internal GNSS and UTC-direct sync as *tested* requirements
  (61993-2; 62287-1 Ed. 3 change note).
- **Ch. 26** — 61162-1/-2 serial; 61162-3 = NMEA 2000; 61162-450 `UdPbC`,
  multicast groups, TAG blocks (and the IEC 62320-1 vs NMEA 4.10 key
  divergence); 61162-460 gateways.
- **Ch. 27 / 28** — sensitivity/PER and power-level tests (cite 61993-2
  generally; clause numbers pending).
- **Ch. 31** — IEC 60945 as the EMC/environmental baseline; RTCM 13700.0 (LED
  EMC near antennas) in the companion RTCM dossier.
- **Ch. 36** — failure modes that type approval would and would not catch;
  software-update and BAM requirements added in 2018.
- **Ch. 51 / 52** — IEC 62288 symbology (Ed. 3 2021, ASM annexes); 61174 Ed. 4
  AIS overlay on ECDIS; 62388 radar–AIS consistency.
- **Ch. 56** — IEC 61996-1 "all AIS data", 48 h / 30 d retention.
- **Ch. 60** — IEC 61162-460 as the shipboard network security standard;
  62320-2 Ed. 2 "cyber security measures" for AtoN configuration.
- **Ch. 68** — 61097-14 (SART) and the 61993-2 Ed. 3 "locating device group"
  concept that makes Class A displays treat SART/MOB/EPIRB-AIS alike.
- **Appendix B** — full register rows from the "Primary sources located"
  table, each with edition, date, and status.
