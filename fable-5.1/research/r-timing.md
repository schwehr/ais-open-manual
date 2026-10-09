# Dossier: Timing in AIS — UTC, GNSS, synchronization hierarchy, base-station time, and what happens when time goes wrong

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about *time* in the AIS: where a station gets UTC, how tightly it must hold slot
timing, the five-level synchronization hierarchy (UTC direct → UTC indirect →
base direct → base indirect → mobile semaphore), how the time-stamp field and
the communication-state UTC sub-message differ, what Messages 4/10/11 carry, how
Class B "CS" sync differs, what the performance/test standards (IMO MSC.74(69),
A.1106(29), IEC 61993-2 / 62287 / 62320) actually say about the time source,
which hardware runs without a VHF receiver or without GNSS, and the evidence on
how timing degrades or can be attacked (the 2005 Saab R3/R4 leap-second fault,
the 2019 GPS week-number rollover, and the 2014 Trend Micro/ACSAC security
evaluation). It feeds **Chapter 24** (Timing in AIS) as its primary target, plus
**Chapter 21** (sync states inside the comm state), **Chapter 22** (time-stamp
sentinels 60–63; Message 4/11 layout), **Chapter 25** (GNSS as the time
source), **Chapter 36** (failure modes: GNSS loss, leap seconds, WNRO),
**Chapter 61** (timing and network-disruption attacks), **Chapter 62** (GNSS
denial and AIS timing), **Chapter 65** (R-Mode), and **Appendix C** (bit
layouts).

> Research-session note. Facts marked *high* from ITU-R M.1371-6 were read in the
> PDF downloaded from itu.int (`R-REC-M.1371-6-202602-I!!PDF-E.pdf`, 156 pp.)
> and text-extracted with `pdftotext`; clause numbers use the M.1371-6 "A2-x.y.z"
> form (M.1371-5 and earlier: same numbers without the annex prefix). IMO
> MSC.74(69) and A.1106(29) were read from the IMO PDFs; IEC 62287-2 and 62320-2
> from iTeh preview PDFs (scope/ToC/Table 1 only); the Trend Micro paper from the
> Trend Micro PDF; the Saab/Norwegian 2005 notices from the Sjøfartsdirektoratet
> scan. Nothing below was taken from memory without a URL or page in hand. A
> fuller working file with longer verbatim quotes is in the session scratch
> (`timing_research.md`).

## Key questions

1. What is the *primary* time source for an AIS station, and what accuracy does
   the standard require of slot timing (jitter budgets for mobile vs base)?
2. What is the synchronization hierarchy, how does a station move down and up it,
   and what are the exact rules for choosing a sync source (two reports in 40 s,
   nine frames, lowest-MMSI tie-break)?
3. What is a *semaphore* station, when does a base or mobile become one, and which
   classes may never be semaphores?
4. How is time carried on the air: the 6-bit **time stamp** in position reports
   (UTC second + sentinels 60/61/62/63), the **UTC hour/minute sub-message** when
   slot time-out = 1, and the full date/time of **Message 4/11**?
5. Do the IMO performance standard and the IEC test standards require an
   *internal* GNSS receiver for timing — even when an external EPFS is connected?
   Where exactly is that written?
6. Which AIS hardware legitimately operates without a VHF receiver or without any
   GNSS (Type 1 AtoN; base stations with 1 PPS/IRIG-B; receive-only units), and
   how do they stay in sync?
7. How does timing degrade when GNSS is lost (indirect sync, semaphore, Class B CS
   sync mode 2) and when must a station stop transmitting?
8. Can an attacker collapse a cell by sending false time or abusing link-management
   messages? What did the 2014 Trend Micro/ACSAC work actually demonstrate?
9. Is there documented real-world AIS breakage from leap seconds or GPS
   week-number rollover?
10. What does this mean for data consumers (timestamp reconciliation; the
    1-minute ambiguity of the time-stamp field; sync-state census as a health
    metric)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Recommendation ITU-R M.1371-6 | 02/2026; approved 2026-02-19; in force | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | A2-3.1 synchronization; A2-3.2.2.8 buffer/jitter; A2-3.2.2.10 Fig. 8 timing; A2-3.3.7.2 comm state; Annex 6 Class B CS sync; Annex 7 Messages 4/10/11, time stamp; A8-4 locating-device sync accuracy | Free |
| ITU-R M.1371 landing page (all editions) | -0 (1998) … -6 (2026) | https://www.itu.int/rec/R-REC-M.1371/en | Edition history | Free |
| IMO Resolution MSC.74(69), Annex 3 | adopted 12 May 1998 | https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/MSCResolutions/MSC.74(69).pdf | AIS performance standard — read in full; contains no UTC/GNSS-timing clause | Free |
| IMO Resolution A.1106(29) | adopted 2 Dec 2015 | https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.1106(29).pdf | Operational guidelines; annex describes "GNSS receiver for timing purposes and position redundancy" | Free |
| IEC 61993-2:2018 | Ed. 3.0, published 2018-07-19, 302 pp. | https://webstore.iec.ch/en/publication/34277 | Class A test standard (abstract read; body paid) | Paid |
| IEC 62287-1:2017 (+AMD1:2022) | Ed. 3.0, 2017-04-05 | https://webstore.iec.ch/en/publication/32705 | Class B CS; "addition of a direct method for synchronisation from an internal UTC source" | Paid (abstract free) |
| IEC 62287-2:2017 | Ed. 2.0 (2017-02) | https://standards.iteh.ai/catalog/standards/sist/466f63b7-1f18-498f-947f-d5fafd97a8cc/iec-62287-2-2017 (preview) | Class B SO; "only uses the internal GNSS"; sync test clauses 12.1.1/12.1.2/12.3 | Paid (preview free) |
| IEC 62320-1:2015 | Ed. 2.0, 2015-01-20, 128 pp. | https://webstore.iec.ch/en/publication/6825 | Base stations; TAG blocks; abstract silent on external time sources | Paid (abstract free) |
| IEC 62320-2:2016 | Ed. 2.0, 2016-10-31 | https://standards.iteh.ai/catalog/standards/sist/5abd42f0-0275-44ae-8dca-56604a8389f3/iec-62320-2-2016 (preview) | AtoN Types 1/2/3 Table 1 incl. receiver and UTC-sync columns | Paid (preview free) |
| IALA R0126 (A-126), G1062, G1050 | titles verified on iala.int | https://www.iala.int/product/r0126/ ; https://www.iala.int/product/g1062/ ; https://www.iala.int/product/g1050/ | AtoN service; establishing AIS AtoN; "Management and Monitoring of AIS Information" (G1050 is **not** an AtoN document) | Free (registration) |
| Saab TransponderTech Announcement PT-05-0078 (2005-09-09) and Norwegian Maritime Directorate Sikkerhetsmelding SM 10/2005 (29 Oct 2005) | scanned notice | https://www.sdir.no/contentassets/8305b35671834e809bc05e86518ba158/20230216134638.pdf | Leap-second timing fault in Saab R3/R4 Class A transponders | Free |
| USCG Marine Safety Alert 5-05 (24 Oct 2005) | same incident | https://www.dco.uscg.mil/Portals/9/DCO%20Documents/5p/CG-5PC/INV/Alerts/0505.pdf (403 to fetcher; content per two search summaries) | Two-slot occupancy description | Free (verify fetch) |
| GPS.gov, "GPS Week Number Rollover" | page | https://www.gps.gov/news/gps-week-number-rollover | Rollover 23:59:42 UTC 6 Apr 2019; next 20 Nov 2038 | Free |
| DHS NCCIC memorandum on GPS WNRO | TLP:WHITE, 2 pp. | https://www.cisa.gov/sites/default/files/documents/Memorandum_on_GPS_2019.pdf | Generic timing advisory; lists no equipment classes | Free |
| UK MCA Safety Bulletin 13 | 19 Feb 2019 | https://www.gov.uk/government/publications/safety-bulletin-13-gps-week-number-rollover/safety-bulletin-13-gps-week-number-rollover | WNRO guidance; AIS not named | Free |
| Furuno (Singapore) "Special Announcement — GPS Rollover on 20th December 2020" | PDF | https://www.furuno.sg/wp-content/uploads/2026/06/GPS-Rollover.pdf | FA-100 date effects only | Free |
| JRC "Notice: GPS Week Number Rollover for equipment" | 2021-12-24 (orig. 12 Jun 2018) | https://www.jrc.co.jp/en/news/2021/1224-1 | Device-specific rollovers 2019/2022 | Free |
| Balduzzi, Wilhoit & Pasta, *A Security Evaluation of AIS* (Trend Micro research paper, Dec 2014) | PDF read in full | https://documents.trendmicro.com/assets/white_papers/wp-a-security-evaluation-of-ais.pdf | Slot starvation, frequency hopping, "timing attack", CPA spoofing, AISTX/USRP B100 | Free |
| Balduzzi, Pasta & Wilhoit (2014), ACSAC '14 | doi:10.1145/2664243.2664257 (Crossref-verified) | https://doi.org/10.1145/2664243.2664257 | Peer-reviewed version | Paid |
| Kessler (2020), "Protected AIS…", *TransNav* 14(2):279–286 | doi:10.12716/1001.14.02.02 | https://www.transnav.eu/Article_Protected_AIS_A_Demonstration_Kessler,54,1002.html | Authentication proposal | Free |
| Wimpenny, Šafář, Grant & Bransby (2022), *J. Navigation* 75(2):333–345 | URL resolves | https://www.cambridge.org/core/journals/journal-of-navigation/article/securing-the-automatic-identification-system-ais-using-public-key-cryptography-to-prevent-spoofing-whilst-retaining-backwards-compatibility/98E18D3253AD985BA7B75185EFB3538A | PKI for AIS | Paid |
| ACCSEAS, *Feasibility Study of R-Mode using AIS Transmissions* Part 1 (Johnson & Swaszek, Issue 1.0, 05/05/2014) | report | https://www.iala.int/content/uploads/2016/08/accseas_r_mode_feasibility_study_ais_transmissions_part_1.pdf | GNSS-independent timing signal for AIS; AIS as signal of opportunity | Free |
| Gewies et al. (2023), "R-Mode – terrestrial navigation for maritime users", ION GNSS+ 2023 | abstract | https://elib.dlr.de/200015/ | 10–30 m MF; ~10 m VDES R-Mode | Free |
| Rizzi et al. (2023), *Applied Sciences* 13(3):1872 | doi:10.3390/app13031872 (Crossref) | https://doi.org/10.3390/app13031872 | 15.1 m (95 %) day / 55.3 m night | Free (OA) |
| Šafář et al. (2019), "Performance Bounds for VDES R-mode", *J. Navigation* | doi:10.1017/s0373463319000559 (Crossref) | https://doi.org/10.1017/s0373463319000559 | AIS waveform ranges worst of VDES waveforms | Paid |
| Saab R60 VDES base-station brochure (7000 120-006 D) | vendor PDF | https://www.themysgroup.com/public/files/6318b0cbd3472.pdf | Internal multi-GNSS; "1PPS and IRIG-B 003" port; NTP server option | Free |
| Saab R40 base-station description | vendor page | https://www.euronav.co.uk/Products/Hardware/AIS/AIS_TX/saab_r40/saab_r40_base_station.html | "internal GPS receiver mainly provides accurate time synchronization" | Free |
| Harati-Mokhtari, Wall, Brooks & Wang (2007), *J. Navigation* 60(3) | doi:10.1017/S0373463307004298 (Crossref) | https://doi.org/10.1017/S0373463307004298 | Baseline AIS data-quality paper | Paid |

## Verified facts

Clause references are to ITU-R M.1371-6 unless stated; "p." is the printed page.

### Frame, slot, and the UTC minute

| Fact | Source | Confidence |
|---|---|---|
| "A frame equals one (1) min and is divided into 2 250 slots. Access to the data link is, by default, given at the start of a slot. The frame start and stop coincide with the UTC minute, when UTC is available." | A2-3.1.2 (p. 18) | high |
| Slot zero is the start of the frame; slots indexed 0–2249 | A2-3.1.4 (p. 22) | high |
| Transmitter events in one slot: T0 0.000 ms RF on; TTS 0.833 ms training; T1 1.000 ms RF stable; T2 3.333 ms start flag ("This event can be used as a secondary synchronization source should the primary source (UTC) be lost"); Ts 4.167 ms end of start flag = slot-phase sync marker; T3 24.167 ms end of Tx (zero stuffing); T4 = T3 + 1.0 ms RF zero; T5 26.667 ms end of slot | A2-3.2.2.10 Fig. 8 table (pp. 26–27) | high |
| 24-bit buffer: bit stuffing 4, distance delay 14 (= 235.9 nmi; "protection for a propagation range of over 120 NM"), synchronization jitter 6 | A2-3.2.2.8–8.2 (p. 25) | high |
| Mobile: "Transmission timing error should be within 104 µs of the synchronization source. Since timing errors are additive, the accumulated timing error can be as much as 312 µs." Base: 52 µs / 104 µs | A2-3.2.2.8.3 (p. 25) | high |
| Locating devices: "During UTC direct synchronization, the transmission timing error, including jitter, of the AIS station should be ±3 bits (±312 µs)." | A8-4 (p. 152) | high |

### Synchronization states and hierarchy (A2-3.1.1, A2-3.1.3)

| Fact | Source | Confidence |
|---|---|---|
| UTC direct: "A station, which has direct access to coordinated universal time (UTC) timing with the required accuracy should indicate this by setting its synchronization state to UTC direct." | A2-3.1.1.1 (p. 17) | high |
| UTC indirect: sync to stations indicating UTC direct; "Only one level of UTC indirect synchronization is allowed." | A2-3.1.1.2 (p. 18) | high |
| Base direct: sync to the base "which indicates the highest number of received stations, provided that two reports have been received from that station in the last 40 s"; drop if fewer than two in 40 s; ties → lowest MMSI; "Only one level of indirect access to the base station is allowed." | A2-3.1.1.3 (p. 18) | high |
| Mobile as semaphore: with no UTC and no base, sync to "the station indicating the highest number of other stations received during the last nine frames, provided that two reports have been received … in the last 40 s"; ties → lowest MMSI | A2-3.1.1.4 (p. 18) | high |
| Priority of sources: (1) internal UTC; (2) a station which has UTC time; (3) a semaphore-qualified base; (4) other stations synced to a base; (5) a semaphore-qualified mobile | A2-3.1.3.4.3 (p. 20) | high |
| Table 9: UTC direct 1/code 0/usable; UTC indirect 2/1/not; Base direct 3/2/usable; Base indirect 4/3/not; Mobile as semaphore 5/3/not — codes 3 are ambiguous on the air | Table 9 (p. 21) | high |
| Semaphore qualification: mobile only if own state ∈ {1,3} and highest received state (excluding own source) = 3 (Table 10); base if own state ∈ {1,2,3} and highest received ∈ {2,3} (Table 11); multiple → highest received-stations count, then lowest MMSI | Tables 10–11 (pp. 21–22) | high |
| Base Message 4 nominal interval 10 s → MAC.SyncBaseRate once per 3⅓ s while semaphore-qualified, until conditions invalid for 3 min; mobile semaphore MAC.SyncMobileRate once per 2 s; "The Class B 'SO' and AIS SAR aircraft station should not act as the semaphore." | A2-3.1.3.3.1–3.3.2; Table 8; Annex 1 Tables 1–2 notes (pp. 9–10, 17, 19) | high |
| Slot-phase sync decided after end flag + valid FCS (T3); frame sync adopts the received slot number from a sub-message with slot time-out 2/4/6 | A2-3.1.3.1–3.1.3.2 (pp. 18–19) | high |
| Stations with direct (indirect) UTC "should continuously re-synchronize" on the UTC source (those UTC sources) | A2-3.1.3.4.1 (p. 20) | high |

### How time rides in the messages

| Fact | Source | Confidence |
|---|---|---|
| SOTDMA comm state (19 b): sync state 2 b (0 UTC direct, 1 UTC indirect, 2 base, 3 other/indirect base); slot time-out 3 b; sub-message 14 b | Table 18 (p. 48) | high |
| Sub-message: time-out 3/5/7 → received stations (0–16 383); 2/4/6 → slot number (0–2 249); **1 → UTC hour (bits 13–9) and minute (bits 8–2), "If the station has access to UTC"**; 0 → slot offset | Table 19 (p. 48) | high |
| ITDMA comm state uses the same 2-bit sync-state code | Table 20 (pp. 49–50) | high |
| Position-report time stamp (6 b): "UTC second when the report was generated by the electronic position system (EPFS) (0-59, or 60 if time stamp is not available, which should also be the default value, or 61 if positioning system is in manual input mode, or 62 if electronic position fixing system operates in estimated (dead reckoning) mode, or 63 if the positioning system is inoperative)" | Table 47 (p. 106) | high |
| Message 18: same coding but "61, 62, 63 are not used by 'CS' AIS" | Table 68 (p. 128) | high |
| Message 21 off-position flag "should only be considered if time stamp is equal to or below 59"; for a fixed aid, off-position = internal GNSS position outside the installed zone, "i.e. suspected GNSS anomaly" | Table 71 (p. 133) | high |
| Message 4/11 layout: UTC year 14 b (0 = n/a), month 4 (0), day 5 (0), hour 5 (24 = n/a), minute 6 (60), second 6 (60); PA; lon/lat; EPFD type; Message-27 transmission control; spare; RAIM; SOTDMA comm state; 168 bits | Table 49 (pp. 108–109) | high |
| "A base station should use Message 4 in its periodical transmissions. Message 4 is used by AIS stations for determining if it is within 120 NM for response to Messages 20 and 23. A mobile station should output Message 11 only in response to interrogation by Message 10." Message 11 also sent by a *limited base station*; reply on the channel where Message 10 was received | A7-3.2 (p. 107) | high |
| Message 10 is the UTC/date inquiry (priority 3, RATDMA) | Table 44; A7-3.8 (pp. 101, 113) | high |
| Binary (functional) messages carry date/time with the same sentinels as Message 4 | A5-3 list (p. 65) | high |
| EPFD type code 15 = "internal GNSS" (also 1 GPS, 2 GLONASS, 3 combined GNSS, 4 Loran, 5 Chayka, 6 INS, 7 surveyed, 8 Galileo, 9 BDS, 12 integrated PNT, 13 INS, 14 terrestrial radionavigation) | Tables 49–50 (pp. 108–110) | high |

### Where the "internal GNSS for timing" requirement really lives

| Fact | Source | Confidence |
|---|---|---|
| **IMO MSC.74(69) Annex 3 contains no clause on UTC synchronization, time slots, TDMA or an internal GNSS receiver.** Its §3.1 equipment list is: communication processor; "a means of processing data from an electronic position-fixing system which provides a resolution of one ten thousandth of a minute of arc and uses the WGS-84 datum"; sensor input; manual input; error checking; BITE. The only time item is dynamic data "Time in UTC*" with footnote "* Date to be established by receiving equipment." §1.4 and §9 delegate technical characteristics to ITU-R Recommendations | MSC.74(69) Annex 3 §§1.4, 3.1, 6.1.2, 9 (PDF read; grep for "synchroni", "GNSS", "slot", "TDMA" negative) | high |
| MSC.74(69) §6.3: "A security mechanism should be provided to detect disabling and to prevent unauthorised alteration of input or transmitted data." §7: operational within 2 min of switch-on | same | high |
| **IMO A.1106(29)** annex "AIS components": an onboard AIS consists of antennas, one VHF transmitter, two multi-channel VHF receivers, one channel-70 receiver, a CPU, "an electronic position-fixing system, Global Navigation Satellite System (GNSS) receiver for timing purposes and position redundancy", sensor interfaces, BIIT, MKD; Figure 1 shows an internal "GNSS-Rx" distinct from the ship's GNSS sensor | A.1106(29) Annex pp. 15–16 | high |
| A.1106(29) §22: AIS may be switched off by the master for safety/security, logged, restarted "as soon as the source of danger has disappeared … Ship's own data will be transmitted after a two-minute initialization period." §§36–38 on sensor quality ("the built-in integrity check cannot validate the contents of the data"); §48 "(D)GNSS corrections may be sent by VTS centres via AIS." | A.1106(29) | high |
| M.1371-6 itself is source-neutral for Class A: it speaks of "direct access to UTC timing with the required accuracy" and the "internal UTC source"; only the Class B CS annex mandates an *internal GNSS* (A6-3.1, A6-3.3) | grep of full M.1371-6 text for "internal" | high |
| **IEC 61993-2:2018 Ed. 3.0** (published 2018-07-19; 302 pp.) "cancels and replaces the second edition published in 2012"; incorporates M.1371-5; adds SSA security sentence, optional 61162-450/460, BAM, extended towing dimensions, software-update requirement. Abstract is silent on internal GNSS/UTC — the requirement and the synchronization tests are in the paid body (clause numbers (verify)) | https://webstore.iec.ch/en/publication/34277 | high (abstract) / low (body clauses) |
| **IEC 62287-1:2017 Ed. 3.0**: "An AIS station intended to operate in receive-only mode is not considered a Class B shipborne mobile AIS station … significant technical change …: in the synchronisation method, addition of a direct method for synchronisation from an internal UTC source." | https://webstore.iec.ch/en/publication/32705 | high |
| **IEC 62287-2:2017 Ed. 2.0** scope: Class B SO "only uses the internal GNSS – no position sensor input is allowed", "requires use of VDL Message 17 for correction of the internal GNSS", 5 W high power, intervals down to 5 s; ToC: 6.3 Internal GNSS receiver for position reporting; 10.4 Internal GNSS receiver; 12.1.1 Synchronisation test using UTC direct and indirect; 12.1.2 Synchronisation test without UTC, EUT receiving semaphore; 12.3 Synchronisation jitter | iTeh preview | high |
| **IEC 62320-2:2016 Ed. 2.0 Table 1** (AtoN station types): VDL receiver — Type 1 "No receiver"; Type 2 "Receiver for query, configuration, or control functions only"; Type 3 "Two receiving processes for autonomous mode (RATDMA)". Access for Message 21 — Type 1/2 FATDMA; Type 3 FATDMA & RATDMA. Positioning — "EPFS and surveyed position" (option "Surveyed position only (no EPFS)"). **UTC synchronisation — Type 1/2 "UTC Direct"; Type 3 adds "UTC indirect or semaphore"**. AtoN "Shall not respond to assignment Messages 16 and 23". ToC 8.2.2 "Synchronisation test without UTC (types 2 and 3)" | iTeh preview, Table 1 (p. 13) and ToC | high |
| Implication: a Type 1 AtoN has no VHF receiver, so it cannot slot-phase sync from the VDL; its only timing source is its own GNSS ("UTC Direct") and its slots must be pre-reserved by a base station (FATDMA) | derived from Table 1; vendor confirmation: Sealite "Type 1 AIS AtoN uses the FATDMA access scheme and can only trans[m]it"; SRT Carbon "Configurable as Type 1 or Type 3 … Integrated GPS antenna" | high |
| **IEC 62320-1:2015 Ed. 2.0** (base stations; 128 pp.) replaced Ed. 1 (2007)+AMD1 (2008); changes include TAG blocks replacing comment blocks, Message 27 control, 90 % channel-load test. Abstract says nothing about 1 PPS/NTP/PTP time inputs | https://webstore.iec.ch/en/publication/6825 | high (abstract) |
| Vendor evidence for base-station timing: Saab R40 — "The internal GPS receiver mainly provides accurate time synchronization." Saab R60 (VDES base) — internal GNSS "GPS, BeiDou, Galileo, GLONASS"; "1PPS and IRIG-B 003 — Via the 9-pin D-sub"; "built in NTP-server option to support local time synchronisation for LAN connected equipment" (NTP is an *output*). **No standard or vendor text was found permitting NTP/PTP as the VDL slot-timing source.** Direction (in/out) of the R60 1 PPS/IRIG-B port is not stated (verify) | Saab R40 page; Saab R60 brochure | high (quotes) / medium (negative) |
| IALA G1050's title is "Management and Monitoring of AIS Information" (not an AtoN document); AtoN types are in R0126 (A-126) and G1062 "Establishment of AIS as an Aid to Navigation" | iala.int product pages | high (titles) |

### GNSS loss and Class B behaviour (M.1371-6)

| Fact | Source | Confidence |
|---|---|---|
| Class B CS: "The Class B 'CS' AIS should have an internal GNSS receiver as source for position, COG, and SOG." "If the internal GNSS receiver is inoperative, the unit should not transmit Messages 18 and 24 unless interrogated by a base station" | A6-3.3 (p. 82) | high |
| Class B CS sync mode 1: sync time periods to received Messages 1/2/3/4/18 (repeat indicator 0), jitter ≤ ±3 bits (±312 µs) from a rolling 60 s average; keep ≥ 30 s after loss; then sync mode 2 = own internal timing; "Other synchronization sources fulfilling the same requirements are allowed (optionally)" (this is the "direct method from an internal UTC source" that IEC 62287-1 Ed. 3 added); base reservations still respected | A6-4.3.1.1.1–1.2 (p. 86) | high |
| CS detection window 1 146 µs from 833 µs to 1 979 µs after T0 — carrier sense needs slot-phase sync but not the slot number | A6-4.3.1.2 (p. 87) | high |
| Speed lost → Class A reverts to nav-status default interval; Class B to the 3-min default | Annex 1 Tables 1–2 notes (2)/(5) (pp. 9–10) | high |

### Incidents: leap seconds and week-number rollover

| Fact | Source | Confidence |
|---|---|---|
| **2005 Saab R3/R4 leap-second fault.** Saab TransponderTech Announcement PT-05-0078 (Version A, 2005-09-09): "UTC time is used as the time base in the AIS system. A leap second will be introduced in UTC time at midnight, 31st December 2005. Announcement on the upcoming change in UTC has been broadcast in the GPS system since early July this year. An error has been observed in the internal GPS receiver in the R3 and R4 transponders. The GPS receiver introduced this leap second immediately, when the announcement was received. The result is that the timing in the transponder is incorrect and will be incorrect until 31st December 2005. There is a slight risk that some messages from the transponder may collide with transmissions from other AIS units. … Additionally we understand that there are some AIS transponders which will not be able to receive such incorrectly timed messages." Fix: software upgrade; "The software upgrade will have no effect after 2005, when the internal GPS receiver itself will provide correct UTC time." | sdir.no scan, p. 2 | high |
| Norwegian Maritime Directorate SM 10/2005 (29 Oct 2005), "Problemer med tidsberegning i Saab AIS R3- og R4-transceivere": timing "har ett sekunds feilvisning" (one second off); "Normalt strekker en AIS-sending seg over én tidsluke. Men, på grunn av den uriktige tidsberegningen kan sendinger fra en Saab AIS R3- og R4-transceiver strekke seg over to tidsluker og derved forårsake kollisjon med sendinger fra andre AIS-enheter." Headed "Feil tidsberegning er en sikkerhetsrisiko" | sdir.no scan, p. 1 | high |
| USCG Marine Safety Alert 5-05 (24 Oct 2005) describes the same fault: transmissions "begin in the middle of a time slot rather than at the beginning, effectively utilizing two time slots instead of one" | dco.uscg.mil 0505.pdf (403 to fetcher; two independent summaries) | medium |
| Arithmetic check: a 1 s offset = 37.5 slots, so the station's start-of-burst falls mid-slot (0.5 slot = 13.3 ms late) — consistent with "two time slots instead of one" | derived (1 s / 26.667 ms = 37.5) | high |
| **GPS WNRO**: "The last GPS Week Number Rollover occurred at 23:59:42 UTC on April 6, 2019. Many GPS-enabled devices that were not properly designed to account for the rollover event exhibited problems on that date. Other equipment became faulty several months before or after that date … GPS devices that use only the C/A code and its legacy navigation message (LNAV) can expect the next rollover on November 20, 2038." First rollover August 1999 | https://www.gps.gov/news/gps-week-number-rollover | high |
| DHS NCCIC memo: 10-bit week number rolls over every 1024 weeks from 6 Jan 1980; "some manufacturer implementations interpret the WN parameter relative to a date other than January 5, 1980 … would experience a similar rollover event 1024 weeks after that firmware creation date." **It names no equipment classes** | cisa.gov PDF | high (content) / medium (2018 date) |
| UK MCA Safety Bulletin 13 (19 Feb 2019): higher risk for "units older than 10 years, and units which have had no firmware updates"; AIS not named | gov.uk | high |
| Furuno FA-100/R (Class A) device-specific rollover 20 Dec 2020: "Rollover will not affect communication function, but it will affect the dates of the AIS internal system (internal GPS, display of own ship dynamic data, logs transmitted, messages received, alarm logs and power on/off logs)"; retrofit to FA-170 recommended | furuno.sg PDF | high |
| Furuno FA-150 device-specific rollover 2 Jan 2022; software v4.07 defers to 2039 | search summary | medium |
| JRC notice: some models roll over 15 May 2022 "turn the clock back 19.6 years (29th September 2002) … no influence on positioning operation"; effects include wrong dates in transmitted data/logs and, for some equipment, stopped scheduled/LRIT/VMS transmissions; discontinued models whose counters started 19 Dec 1999 rolled over 4 Aug 2019. AIS model list (JHS-180/182) only via distributor (verify) | jrc.co.jp | high (text) / medium (AIS models) |
| **Negative findings:** no USCG NAVCEN/MCA/IMO alert specific to AIS and the 2019 WNRO; no AIS-specific incident found for the 30 Jun 2012, 30 Jun 2015 or 31 Dec 2016 leap seconds; 1999 rollover predates AIS carriage | multiple searches | medium |

### Attacks (Trend Micro 2014 / ACSAC 2014)

| Fact | Source | Confidence |
|---|---|---|
| Threat table: spoofing (ship, AtoN, SAR aircraft, SART, weather, CPA), hijacking, and "Availability disruption: Slot starvation / Frequency hopping / Timing attacks" — the availability attacks are RF-only | Trend Micro paper p. 7 | high |
| **Slot starvation**: "we used message types 4 and 20 to simultaneously fake a base station installed at a VTS and allocate AIS transmissions to the entire 'address space' (i.e., time division multiple access [TDMA] slots) in order to consume all of the slots and prevent all nearby stations to further operate" | pp. 8, 19–20 | high |
| **Frequency hopping** (Message 22): "we could immediately switch receivers to nonstandard channel frequencies (i.e., lowered their operating frequencies by 4.950MHz) … our attack succeeded because we specified a geographical region apart from the vessel's current position"; "class-B transponders cannot be manually reset. Users do not even get notified of frequency changes." | pp. 7–8, 17, 19 | high |
| **"Timing attack"** = abuse of assignment commands, *not* clock manipulation: "Attackers can use VTS-reserved assignment command messages to instruct victims to delay transmissions by 15 minutes, allowing the former to perform denial-of-service (DoS) attacks. Inversely, attackers can overload (i.e., flood) marine traffic by requesting existing stations to send AIS updates at a very high rate." The paper never attacks GNSS/UTC synchronization itself | p. 19 | high |
| CPA spoofing triggered a collision alarm on OpenCPN ("collision is expected to occur in 2 seconds"); hijacking by out-powering (120 dB vs 90 dB attenuators, cabled) | pp. 7, 18–19 | high |
| Hardware: AISTX on GNU Radio; Ettus USRP B100 v2 + WBX; receivers incl. Weatherdock EasyTRX2; gr-ais; coverage test with a modified Kenwood TK-762G amplifier ≈ 16.5 km on land at 45.69 N 9.72 E; experiments cabled, "Only harmless test messages"; findings discussed with providers, IMO and ITU-R in September 2013 | pp. 16–21 | high |
| M.1371 bounds relevant to these attacks: Message 23 quiet time 0–15 min; AtoN "shall not respond to assignment Messages 16 and 23" (IEC 62320-2 Table 1); Message 4/23 Message-27 control reverts after 3 min; assigned-mode time-outs per `r-link-layer.md`; a station with UTC direct never re-syncs to a false base (priority 1 = internal UTC) | M.1371-6 A2-3.1.3.4.3; p. 60; `r-link-layer.md` | high |
| Follow-ups verified: Kessler 2020 *TransNav* "Protected AIS"; Wimpenny et al. ION GNSS+ 2018 "Public Key Authentication for AIS and the VHF Data Exchange System (VDES)" and *J. Navigation* 2022; Goudossis & Katsikas 2019 *J. Mar. Sci. Technol.* (medium). **No peer-reviewed demonstration of a UTC/synchronization attack (spoofed Message 4 or GNSS-spoofed slot phase) against type-approved AIS was found** | see sources table | high / medium (negative) |

### R-Mode and GNSS-independent timing (for ch. 24/62/65)

| Fact | Source | Confidence |
|---|---|---|
| ACCSEAS R-Mode feasibility study using AIS transmissions (Johnson & Swaszek, Issue 1.0 Final, 05/05/2014, for WSV Northern Region; EU ERDF part-financed): concept-level evaluation of GMSK time-of-arrival ranging, base-station availability, AIS as signal of opportunity; no field jitter measurements in Part 1 | IALA-hosted PDF | high |
| R-Mode Baltic started October 2017 under DLR lead (Stefan Gewies), modifying DGNSS beacons and AIS base stations in DE/PL/SE/DK; R-Mode Baltic 2 (to ~2022) worked on "R-Mode system self-synchronisation" incl. fibre time transfer to a base station (deliverable 10/01/2022, NIT/RISE/DLR) | DLR news 2017-10-20; keep.eu attachment 30451 | high |
| Results: "Eight maritime radio beacons were equipped with R-Mode ready signal modulators and accurate clocks … accuracies of 10 to 30 m can be achieved at day-time"; "positioning with VDES R-Mode can be achieved with accuracies of 10 m in areas with good reception conditions" | Gewies et al. 2023 abstract (elib.dlr.de/200015) | high |
| MF R-Mode near Rostock: 15.1 m (95 %) optimal, 55.3 m under sky-wave | Rizzi et al. 2023 (Crossref abstract) | high |
| VDES ranging bounds: "all of the new VDES waveforms provide better ranging performance than the AIS waveform" | Šafář et al. 2019 abstract | high |
| eLoran: UK/Ireland IOC prototype discontinued 11:00 UTC 31 Dec 2015 (Trinity House NtM 27/2015); Korean eLoran testbed operational since 1 June 2021 (≤ 20 m 95 %); US Loran-C shut down from Feb 2010; National Timing Resilience and Security Act signed 4 Dec 2018 (P.L. 115-282 §514) | trinityhouse.co.uk; arXiv 2109.08990; archive.gps.gov | high |

## Notes and quotes

- **Two different "times" in a position report.** The 6-bit *time stamp* is the
  UTC second of the EPFS fix; it carries no minute or hour and says nothing
  about the slot. The minute is only recoverable from the receiver's clock, the
  SOTDMA sub-message when slot time-out = 1, or a Message 4/11. Loggers that
  "reconstruct" full timestamps from the field alone are guessing the minute.
- **The internal-GNSS myth, precisely stated.** The IMO *performance standard*
  (MSC.74(69)) never mentions UTC synchronization or an internal receiver; the
  phrase "GNSS receiver for timing purposes and position redundancy" is from the
  *informational* annex of A.1106(29) (likely inherited from A.917(22) —
  verify). The *normative* chain is ITU-R M.1371 ("direct access to UTC timing
  with the required accuracy"; internal GNSS mandated explicitly only for Class
  B CS) plus the IEC test standards (62287-2: "only uses the internal GNSS";
  62320-2 Table 1: Type 1 AtoN "UTC Direct"; 61993-2 body (verify)).
- **Sync state 3 is ambiguous on the air** (base indirect vs mobile semaphore).
- **Jitter arithmetic.** 1 bit = 104.17 µs; 3 bits = 312.5 µs; 6 buffer bits =
  625 µs; 14 bits = 1.458 ms ≈ 437 km. A 1 s error (2005 Saab) = 37.5 slots.
- **Semaphore election is a popularity contest with a tie-break**: highest
  "received stations" count, then lowest MMSI — both fields an attacker can set
  freely, but only stations that have already lost UTC will listen.
- **Class B CS does not keep a slot map** — it needs only slot-phase sync for
  its carrier-sense window; after 30 s without sources it free-runs.
- Quote (Fig. 8, event T2): "This event can be used as a secondary
  synchronization source should the primary source (UTC) be lost."
- Quote (Saab 2005): "It should be noted that users so far have not reported
  this as a problem, not even in the busiest traffic areas." — a useful
  reminder that a 13 ms slot-phase error degrades gracefully in a lightly loaded
  cell.
- Quote (Trend Micro 2014, p. 19): "Attackers can use VTS-reserved assignment
  command messages to instruct victims to delay transmissions by 15 minutes" —
  the "timing attack" is a Message 16/23 abuse, and the chapter should not
  describe it as a clock attack.
- Quote (A.1106(29) §38): "the built-in integrity check cannot validate the
  contents of the data processed by the AIS."

## Open questions / (verify)

- (verify) IEC 61993-2:2018 body: clause numbers for the internal GNSS
  requirement, the UTC-direct/indirect synchronization tests and the jitter
  limit; whether Ed. 3 changed anything about timing vs Ed. 2 (2012).
- (verify) Whether A.917(22) (2001) / A.956(23) (2003) already contained the
  "GNSS receiver for timing purposes and position redundancy" wording, and
  whether SN/Circ.227 says the internal GNSS may back up position.
- (verify) IEC 62320-1 body: any external 1 PPS input or holdover-oscillator
  requirement for base stations; direction of the Saab R60 1 PPS/IRIG-B port.
- (verify) IEC 62320-2: how a Type 1 AtoN with "surveyed position only (no
  EPFS)" obtains UTC (Table 1 still says UTC Direct, implying a GNSS used for
  time only).
- (verify) Fetch USCG Marine Safety Alert 5-05 directly; check whether any
  Class B / AtoN / SART units were affected by the 2019 WNRO.
- (verify) JRC AIS model list (JHS-180/182) for the 2019/2022 rollovers.
- (verify) ACSAC version vs Trend Micro paper differences; HITB 2013 "AIS
  Exposed" slides and the Oct 2013 Trend Micro blog URL.
- (verify) Any published census of sync-state values on a real VDL — none
  found; the book could compute one from a raw NAIS/ORBCOMM archive (Marine
  Cadastre CSV does **not** retain the comm state).
- (verify) R-Mode Baltic deliverables quantifying *AIS* base-station transmit
  time offsets vs UTC (official site is `noindex`; downloads not fetched).
- (verify) Whether any receive-only AIS unit vendors state that timing is
  irrelevant (they need no sync at all since the receive process is not slot
  synchronized, A2-3.1.1) — useful plain-language point for ch. 42.

## Candidate figures and worked examples

1. **Figure 24-1 — The sync hierarchy ladder** (Table 9): five rungs, air codes
   0/1/2/3/3, "usable as source" Yes/No/Yes/No/No; annotate the two
   one-level-of-indirection rules and the semaphore qualification tables.
2. **Figure 24-2 — Where time lives in a slot**: Fig. 8 timeline with the 24-bit
   buffer split 4+14+6 and jitter budgets (104/312 µs mobile; 52/104 µs base)
   drawn as error bars at Ts.
3. **Figure 24-3 — Three clocks in one message**: time-stamp field (second
   only); comm-state sub-message rotating through received-stations / slot
   number / UTC hh:mm / offset as slot time-out counts 7→0; receiver TAG block
   `c:`.
4. **Figure 24-4 — Who is allowed a clock?** Matrix of station types vs
   {VHF receiver, internal GNSS, can be semaphore, can sync indirectly}: Class
   A, Class B SO, Class B CS, SAR aircraft, AtoN Type 1/2/3, base, limited base,
   repeater, SART/MOB/EPIRB, receive-only. Sources: M.1371-6, IEC 62320-2
   Table 1, IEC 62287-1/-2 abstracts.
5. **Worked example — jitter in bits**: 1/9 600 s = 104.17 µs; 3 bits =
   312.5 µs; 14 bits = 1.458 ms → 437 km ≈ 236 nmi (standard says 235.9).
6. **Worked example — semaphore election** among three GNSS-denied stations
   using Tables 10–11 and the tie-breaks.
7. **Case file (ch. 24/36) — Saab R3/R4, 2005**: GPS receiver applied the
   announced leap second early → 1 s = 37.5 slots → bursts start mid-slot →
   two-slot occupancy and non-reception by some receivers; three documents
   (Saab PT-05-0078, Norwegian SM 10/2005, USCG MSA 5-05).
8. **Case file (ch. 61) — what a spoofed base station can and cannot do**: the
   Trend Micro slot-starvation (Msg 4 + 20), frequency-hopping (Msg 22) and
   assignment-delay (Msg 16/23) demonstrations vs the M.1371 limits (UTC-direct
   stations never re-sync to a false base; AtoN ignore 16/23; quiet time ≤ 15
   min; 3-min reversion).
9. **Table 24-A — Timing sentinels**: time stamp 60/61/62/63; Message 4 year 0 /
   month 0 / day 0 / hour 24 / minute 60 / second 60; sync-state codes.
10. **Figure 24-5 — WNRO timeline**: 21/22 Aug 1999; 6 Apr 2019; device-specific
    rollovers (JRC 4 Aug 2019, Furuno FA-100 20 Dec 2020, Furuno FA-150 2 Jan
    2022, JRC 15 May 2022); next LNAV rollover 20 Nov 2038.

## Recommended use by chapter

- **Ch. 21:** comm-state Tables 18–20; sync-state codes; slot-phase vs frame
  sync; semaphore rates (Table 8).
- **Ch. 22:** time-stamp sentinels (Tables 47/68/71); Message 4/11 (Table 49);
  Message 10; EPFD code 15.
- **Ch. 24 (primary):** everything above; open with Figure 24-1/24-2; state the
  "where the requirement lives" finding carefully; use the 2005 Saab case as
  the chapter's Case file; close with the sync-state census idea for data
  consumers.
- **Ch. 25:** EPFD code 15; Class B CS/SO internal-GNSS mandates; R-Mode as a
  timing backup; A.1106(29) "timing purposes and position redundancy".
- **Ch. 36:** time stamp 63 and sync state ≠ 0 as detection signatures; Saab
  2005; Furuno/JRC rollover bulletins (date-only effects); explicit negatives for
  2012/2016 leap seconds and the 2019 WNRO.
- **Ch. 61:** Trend Micro attack taxonomy with exact mechanisms; M.1371 limits;
  "timing attack" ≠ clock attack; no published UTC-sync attack on certified
  hardware.
- **Ch. 62:** cascade on GNSS loss (EPFS 63 → sync state 1/2/3 → semaphore
  election; Class B CS stops Messages 18/24); R-Mode and eLoran status.
- **Ch. 65:** R-Mode Baltic/Baltic 2 facts and numbers.
- **Ch. 68:** AtoN Type 1/2/3 table (IEC 62320-2 Table 1) and SART ±312 µs.
- **Appendix C:** Table 49 layout; comm-state sub-message table.
