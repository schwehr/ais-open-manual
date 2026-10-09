# Dossier: ITU standards for AIS (M.1371, M.585, M.2092, M.493, M.2135, RR Appendix 18)

**Purpose.** This dossier records what could be confirmed, as of 4 October 2026,
about the ITU documents that define AIS at the radio and identity level: the
edition history of Recommendation ITU-R M.1371 (AIS technical characteristics,
now at **M.1371-6, February 2026**), M.585 (maritime identities / MMSI, now at
**M.585-10, April 2026**), M.2092 (VDES), M.493 (DSC), M.2135 (autonomous
maritime radio devices), the Radio Regulations Appendix 18 channel table, and
the ITU MARS database. It feeds **Chapter 10** (standardization 1996–2004),
**Chapter 11/12** (edition history), **Chapter 13** (MMSI deep dive),
**Chapter 14/15** (ITU-R WP 5B; how the documents fit together), **Chapter 16**
(Radio Regulations), **Chapters 20–24** (station classes, link layer, message
catalog, ASM, timing), **Chapter 27/28** (channel plan, PHY constants),
**Chapter 30** (loading reports), **Chapter 39** (Message 27), **Chapter 68**
(AIS-SART/MOB/EPIRB-AIS, AMRD), **Chapter 69** (VDES), and **Appendix B**
(standards register) and **Appendix C/D** (bit layouts, code tables).

> Research-session note. Facts marked *high* were read directly from the
> cited primary document during this session (the M.1371-6 and M.585-10 PDFs
> were downloaded from itu.int and text-extracted; clause numbers below are
> from those PDFs). *Medium* means confirmed from an ITU landing page or table
> of contents but not from the body text. *(verify)* means not confirmed.

## Key questions

1. What are the editions of M.1371, with approval dates, and which is in force?
   What changed in each edition (at least at the level of annexes and message
   types)?
2. How is M.1371-6 organized (annex numbering) and how does that differ from
   M.1371-5, which most existing literature and decoders cite?
3. What are the physical-layer constants (bit rate, BT, modulation index,
   frequency tolerance, power levels, sensitivity, spectrum mask, ramp timing)?
4. What are the link-layer constants (frame, slots, packet size, training
   sequence, flags, CRC, buffer bits, 120 nmi reservation rule)?
5. What are the reporting intervals by station class and dynamic condition?
6. Which messages exist (1–27 plus the new 28; 60–63 reserved for AMRD) and
   what access schemes may carry them?
7. What are the MMSI and "freeform maritime identity" formats (M.585-10),
   including the new 12-character identity for AIS-SART/MOB/EPIRB-AIS?
8. Which VHF channels does AIS use, with Appendix 18 channel numbers?
9. Which ITU-R Reports support AIS engineering (VDL loading, satellite
   detection)?
10. Where are the free PDFs, and what is paywalled?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| ITU-R M.1371 landing page (edition list) | M.1371-0 (11/1998), -1 (08/2001), -2 (03/2006), -3 (06/2007), -4 (04/2010), -5 (02/2014), **-6 (02/2026)** | https://www.itu.int/rec/R-REC-M.1371/en | "Technical characteristics for VHF automatic identification system using time division multiple access in the maritime mobile service" | Free |
| ITU-R M.1371-6 edition page | Approved 2026-02-19; status "In force (Main)" | https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en | PDF/Word download links | Free |
| ITU-R M.1371-6 PDF (156 pp.) | 02/2026 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Full text; Annexes 1–8 | Free |
| ITU-R M.1371-6 table of contents (HTML) | 02/2026 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!TOC-HTM-E.htm | Annex/clause structure | Free |
| ITU-R M.1371-5 table of contents (HTML) | 02/2014 (superseded) | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-5-201402-S!!TOC-HTM-E.htm | Annexes 1–9 structure of the previous edition | Free |
| ITU-R M.1371-4 / -3 / -2 tables of contents | 04/2010, 06/2007, 03/2006 | …/R-REC-M.1371-4-201004-S!!TOC-HTM-E.htm, …-3-200706-S…, …-2-200603-S… | Used to date the appearance of Class B CS annex, Messages 25/26, Message 27, burst annex | Free |
| ITU-R M.585 landing page | M.585-2 (06/1990), -3 (06/2003), -4 (03/2007), -5 (10/2009), -6 (01/2012), -7 (03/2015), -8 (10/2019), -9 (05/2022), **-10 (04/2026)** | https://www.itu.int/rec/R-REC-M.585/en | "Assignment and use of identities in the maritime mobile service" | Free |
| ITU-R M.585-10 PDF (12 pp. body) | Approved 2026-04-16 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.585-10-202604-I!!PDF-E.pdf | MMSI formats; freeform identities; conservation guidance | Free |
| ITU-R M.2092 landing page | M.2092-0 (10/2015), -1 (02/2022), -2 (02/2026) | https://www.itu.int/rec/R-REC-M.2092/en | VDES technical characteristics (see `r-vdes.md`) | Free |
| ITU-R M.493 landing page | M.493-6 (09/1994) … -13 (10/2009), -14 (09/2015), -15 (01/2019), **-16 (12/2023)** | https://www.itu.int/rec/R-REC-M.493/en | Digital selective calling | Free |
| ITU-R M.2135 landing page | M.2135-0 (10/2019), **M.2135-1 (02/2023)** | https://www.itu.int/rec/R-REC-M.2135/en | Autonomous maritime radio devices (AMRD) 156–162.05 MHz; Group A (MOB, mobile AtoN) and Group B | Free |
| ITU Radio Regulations | Editions 2008, 2012, 2016, 2020, **2024** | https://www.itu.int/pub/R-REG-RR | Articles 19 (identities), Appendix 18 (VHF maritime channel table) | Free PDF ("posted free of charge for personal use" per 2013 Council decision, stated on the page) |
| Report ITU-R M.2287 | "Automatic identification system VHF data link loading" (edition/year (verify)) | https://www.itu.int/pub/R-REP-M.2287 | VDL loading studies; cited as related document in M.1371-6 | Free |
| Report ITU-R M.2169 | "Improved satellite detection of AIS" (year (verify)) | https://www.itu.int/pub/R-REP-M.2169 (verify URL) | Cited as related document in M.1371-6 | Free |
| ITU MARS (Maritime mobile Access and Retrieval System) | Ship Station List web app | https://www.itu.int/mmsapp/ | MMSI/call-sign lookup; publication of MMSI assignments under RR No. 20.16 | Free (web) |
| IMO SN.1/Circ.289 | 2010 | (IMO docs; see `r-standards-imo.md`) | International application identifier branch referenced by M.1371-6 *recommends 3*, footnote 1 | Free |

## Verified facts

| Fact | Source (clause/page) | Confidence |
|---|---|---|
| M.1371 editions and dates: -0 11/1998; -1 08/2001; -2 03/2006; -3 06/2007; -4 04/2010; -5 02/2014; -6 02/2026 | https://www.itu.int/rec/R-REC-M.1371/en (edition list) | high |
| M.1371-6 approved 2026-02-19; status "In force (Main)"; free download | https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en | high |
| M.1371-6 revision-year string on the title page: "(1998-2001-2006-2007-2010-2014-2026)"; responds to Question ITU-R 232/5 | M.1371-6 PDF p. 1 | high |
| M.1371-6 PDF is 156 pages (pdfinfo); M.1371-5 (superseded) was longer (page count (verify)) | downloaded PDF metadata | high (for -6) |
| **Annex renumbering in M.1371-6.** M.1371-5 had Annexes 1–9: 1 Operational; 2 Technical; 3 "AIS channel management by DSC messages"; 4 Long-range applications; 5 ASM; 6 Sequencing; 7 Class B CSTDMA; 8 AIS messages; 9 Burst transmissions. M.1371-6 has Annexes 1–8: 1 Operational; 2 Technical; 3 Long-range applications; 4 ASM; 5 Sequencing; 6 Class B CS; 7 AIS messages; 8 Burst transmissions. The DSC channel-management annex was removed. Clause numbering now carries an annex prefix (e.g., "A2-3.3.4", "A7-3.26"). | M.1371-5 TOC vs M.1371-6 TOC (URLs above) | high |
| M.1371-6 *recommends 1*: AIS designed per Annex 1 and Annexes 2, 3, 5, 6, 7, 8; *recommends 2/3*: ASM per Annex 4 and the international application identifier branch "maintained and published by IMO" (footnote: SN.1/Circ.289); *recommends 4*: take into account IALA technical guidelines | M.1371-6 p. 5 | high |
| Related documents listed in M.1371-6: M.585, M.823 (DGNSS beacons), M.1080, M.1084, M.2092 (VDES), M.2135 (AMRD), Report M.2169 (satellite detection), Report M.2287 (VDL loading) | M.1371-6 pp. 4–5 | high |
| Four modes of operation: silent, autonomous, assigned, polled | M.1371-6 A1-1.6 | high |
| Station types in Annex 1: Class A (SOTDMA); Class B "SO" (SOTDMA, Annex 2) and Class B "CS" (CSTDMA, Annex 6); AtoN station incl. mobile AtoN; aircraft station (Message 9 + 24A/24B); repeater; locating devices (AIS-SART, MOB, EPIRB-AIS, all burst mode per Annex 8); AMRD Group B (per M.2135); base station | M.1371-6 A1-2 | high |
| AIS-SART Message 14 text: "SART ACTIVE mpp" / "SART TEST mpp" / "SART OFF mpp"; MOB: "MOB ACTIVE/TEST/OFF/CANCEL mpp"; EPIRB-AIS: "EPIRB ACTIVE/TEST/OFF/CANCEL mpp", where *mpp* = manufacturer ID suffix + serial prefix (12-character identity per M.585). EPIRB-AIS also broadcasts the Cospas-Sarsat 15- or 23-HEX-ID in Message 14, alternating with the text, on AIS 1 and AIS 2. | M.1371-6 A1-2.1.5.1–A1-2.1.5.3 | high |
| "AIS stations should not transmit without an appropriate MMSI." M.1080 (10th digit) not applicable to AIS. | M.1371-6 A1-3 | high |
| Reporting schedule: static every 6 min / on request / on change; voyage-related every 6 min; Message 27 every 3 min | M.1371-6 A1-4 | high |
| Class A nominal reporting intervals (Table 1): anchored/moored ≤3 kn or no speed → 3 min; anchored/moored >3 kn (or anchored with 0.2 < SOG ≤ 3 kn, ΔCOG within ±10°, and 90° < \|COG−HDG\| < 270° averaged over 10 s) → 10 s; 0–14 kn → 10 s; 0–14 kn changing course → 3⅓ s; 14–23 kn → 6 s; 14–23 kn changing course → 2 s; >23 kn → 2 s. Semaphore stations go to 2 s. | M.1371-6 Table 1 (p. 9) | high |
| Table 2 (other stations): Class B SO: ≤2 kn 3 min; 2–14 kn 30 s; 14–23 kn 15 s (modified 30 s); 14–23 kn changing course 5 s (modified 15 s); >23 kn 5 s (modified 15 s). Class B CS: ≤2 kn 3 min; >2 kn 30 s (15 s if >14 kn). Aircraft 10 s (2 s when changing course/speed/altitude). AtoN 3 min; mobile AtoN >2 kn 30 s. Base station 10 s (3⅓ s when stations synchronize to it). Class B SO uses the "modified" interval only when the last four frames each had <50 % free slots and returns when ≥65 % are free. | M.1371-6 Table 2 and notes (pp. 9–10) | high |
| Frequency band: 25 kHz channels per RR Appendix 18; AIS 1 = 161.975 MHz; AIS 2 = 162.025 MHz; channel 75 = 156.775 MHz and channel 76 = 156.825 MHz "for AIS satellite uplink" (Message 27 only) | M.1371-6 A1-5; A2-2.1.3; A3-2.3.4 | high |
| PHY Table 3: channel spacing 25 kHz; bit rate 9 600 bit/s; training sequence 24 bits; Tx BT ≈0.4; Rx BT ≈0.5; modulation index ≈0.5; Tx power low 1 W, high 12.5 W (5 W for Class B SO) | M.1371-6 Table 3 (p. 12) | high |
| PHY constants Table 4: NRZI encoding; FEC not used; interleaving not used; bit scrambling not used; modulation GMSK/FM | M.1371-6 Table 4 (p. 13) | high |
| Shipborne AIS receives on two parallel channels and transmits on four independent channels (one transmitter alternating); AIS-SART/MOB/EPIRB-AIS transmit only on AIS 1/AIS 2 and have no receivers | M.1371-6 A2-2.1.4 | high |
| Transmitter (Table 5): carrier power error ±1.5 dB; carrier frequency error ±500 Hz; slotted modulation mask 0 dBc within ±10 kHz, straight line −25 dBc at ±10 kHz to −70 dBc at ±25 kHz, −70 dBc from ±25 to ±62.5 kHz; spurious −36 dBm (9 kHz–1 GHz), −30 dBm (1–4 GHz); intermodulation attenuation 40 dB (base station only) | M.1371-6 Table 5 (pp. 13–14) | high |
| Tx power-vs-time (Table 6): T0 start; TA 0–6 bits (0–0.625 ms) power exceeds −50 dB of Pss; TB1 at 6 bits (0.625 ms) within +1.5/−3 dB; TB2 at 8 bits (0.833 ms) within +1.5/−1 dB (start of training sequence); TE at 233 bits (24.271 ms); TF at 241 bits (25.104 ms) back below −50 dB; TG at 256 bits (26.667 ms) next slot | M.1371-6 Table 6 (p. 14) | high |
| Receiver (Table 7): sensitivity 20 % PER at −107 dBm; 1 % PER at −77 dBm and at −7 dBm; adjacent-channel selectivity 70 dB; co-channel 10 dB; spurious response rejection 70 dB; intermodulation rejection 74 dB; blocking 86 dB; Rx spurious −57 dBm (9 kHz–1 GHz), −47 dBm (1–4 GHz). (Class B SO: Table 36 applies.) | M.1371-6 Table 7 (pp. 14–15) | high |
| Antenna note quoted from COMSAR.1/Circ.32/Rev.3 §5.2.8: AIS VHF antenna directly above/below the primary VHF antenna, min 2 m vertical separation; if on the same level, ≥5 m apart | M.1371-6 note under Table 7 | high |
| GMSK: NRZI data GMSK-coded then FM; Tx BT 0.4 max; Rx designed for BT 0.5 max; modulation index 0.5; frequency stability ±500 Hz; bit rate 9 600 bit/s ±50 ppm; 24-bit preamble of alternating 0101…; NRZI "change in level when a zero is encountered" | M.1371-6 A2-2.3–A2-2.6 | high |
| Channel switching time <25 ms; must be able to receive in the slot directly before/after own transmission | M.1371-6 A2-2.11.1 | high |
| Two power levels; default high; change by manual means or Message 22; nominal 1 W and 12.5 W (1 W and 5 W for Class B SO), tolerance ±1.5 dB | M.1371-6 A2-2.12 | high |
| Hardware transmitter shutdown, independent of software, if transmission exceeds 2 s | M.1371-6 A2-2.13.1 | high |
| Frame = 1 min = 2 250 slots; default packet 256 bits; packet structure: ramp-up 8 bits, training 24, start flag 8 (7Eh), data 168, CRC 16, end flag 8, buffer 24 (= 256) (field sizes from Table on p. ~28; 168-bit data field confirmed by "Data field is 168 bits for other single-slot AIS messages" in A3-2.1) | M.1371-6 A2-3.1.2; A2-3.2.2; A3-2.1 | high |
| CRC: 16-bit polynomial per ISO/IEC 13239:2002 (HDLC), preset to ones, data portion only; "CRC errors should result in no further action" | M.1371-6 A2-3.2.2.6, A2-3.2.3 | high |
| Slots reserved by a station beyond 120 nautical miles are considered free; FATDMA reservations do not apply beyond 120 nmi from the reserving base station | M.1371-6 A2-3.1.6 (p. ~26); A2-3.3.6 (p. ~37) | high |
| Nominal increment NI = 2 250 / Rr; slot offset = NTSnew − NTScurrent + 2 250 | M.1371-6 A2-3.3.5 (lines around "NI = 2 250/Rr") | high |
| Sync state coding in SOTDMA/ITDMA comm state: 0 = UTC direct; 1 = UTC indirect; 2 = synchronized to base station (base direct); 3 = synchronized to another station based on highest number of received stations (or to a station directly synchronized to a base) | M.1371-6 A2-3.3.7.2.1 (Table at "Sync state 2 bits") | high |
| Semaphore rules: mobile with lowest MMSI among qualified becomes semaphore; Class B SO and SAR aircraft shall not act as semaphore; semaphore status persists until qualifying conditions invalid for 3 min | M.1371-6 A2-3.1.1.4; A2-3.1.3.3.2 | high |
| Class B CS carrier-sense window: 1 146 µs long, from 833 µs to 1 979 µs after slot start T0 (first 8 bits excluded for propagation/ramp-down); CS transmission starts 20 bits (TA = 2 083 µs) after T0; CS threshold = background minimum over rolling 60 s + 10 dB, floor −107 dBm, tracked over ≥30 dB (max threshold −77 dBm) | M.1371-6 A6-4.3.1.2–A6-4.3.1.3 (pp. 87–88) | high |
| Class B CS Tx timing (Table 37): TA 20 bits (2 083 µs); TB1 23 bits; TB2 25 bits; TE 248 bits (25 833 µs); TF 251 bits (26 146 µs) | M.1371-6 Table 37 | high |
| Message 27: 96-bit data field ("Data field is 168 bits for other single-slot AIS messages. This field is …96"), transmitted using MSSA (multi-channel slot selection access) on channels 75/76 only, nominal interval 3 min, normally active, can be disabled by a base station via Message 4 control bit + Message 23; "Satellites with AIS receivers may receive AIS Message 27" | M.1371-6 Annex 3, A3-2.1–A3-2.3.4 (pp. ~62–64) | high |
| Message summary (Table 44, M.1371-6): Messages 1–28 defined; 29–59 undefined/reserved; 60 AMRD position report, 61 AMRD identity report, 62 AMRD static information report, 63 AMRD ASM — "only used in Rec. ITU-R M.2135" | M.1371-6 Table 44 (pp. 101–103) | high |
| Message 19 is marked "No longer required" in Table 44 | M.1371-6 Table 44 | high |
| Message 27 row: "Class A and Class B 'SO' AIS station outside base station coverage", access scheme MSSA | M.1371-6 Table 44 | high |
| **Message 28 (new): "Aid-to-Navigation Report (Single-slot message)"**, 168 bits, one slot; priority 1; RATDMA/ITDMA/CSTDMA/FATDMA; "provides similar information as AIS Message 21, but in one slot versus two"; fields: Message ID 6, Repeat 2, Source ID 30, Time stamp 6, Longitude 28, Latitude 27, Restricted Use Indicator 2, AIS AtoN Station Type 3 (0 physical floating, 1 physical fixed, 2 synthetic predicted, 3 synthetic monitored, 4 virtual, 5 mobile), Types of AtoN 7 (0–127; 32–50 are new mobile-AtoN types, e.g., 32 ODAS, 39 navigation hazard, 44 pollution spill marker, 45 SAR datum mark), IALA AtoN MRN 17 (urn:mrn:iala:aton:…, G1143), AtoN Dimensions Type 4 (0–13: height/structural area, swing circle, mobile AtoN vector, polygon, circle, boundary lines, sector, quadrilateral …), Dimension A 9, Dimension B 11, Additional Data Flag 1, Charted Status 1, On-station Status 4 (0–10 incl. 9 unmarked hazard, 10 unmarked obstruction), AtoN Status bits 8, Spare 1, **Authentication Flag 1 ("authenticated per IALA G1192")**. May be paired with Message 24A for the charted name. | M.1371-6 A7-3.26, Tables 84–85 (pp. 146–150) | high |
| Message 1/2/3 nav status table in -6: 0 under way, 1 at anchor, 2 NUC, 3 RAM, 4 CBD, 5 moored, 6 aground, 7 fishing, 8 sailing, 9–10 reserved for future use, 11 towing astern (regional), 12 pushing ahead/towing alongside (regional), 13 reserved, 14 active AIS-SART/MOB-AIS/EPIRB-AIS, 15 undefined (default; also used by devices under test) | M.1371-6 Table 46 (p. ~106) | high |
| ROT encoding: ROTAIS = 4.733 √(ROTsensor) °/min, rounded to integer; 0 to ±126 = up to 708°/min or higher; ROT not to be derived from COG | M.1371-6 Table 46 | high |
| Position fields: longitude 28 bits in 1/10 000 min, 181° (6791AC0h) = not available; latitude 27 bits, 91° (3412140h) = not available; COG 12 bits in 1/10°, 3 600 (E10h) = n/a; heading 511 = n/a; SOG 1 023 = n/a, 1 022 = 102.2 kn or higher; timestamp 60 n/a, 61 manual input, 62 dead reckoning, 63 EPFS inoperative | M.1371-6 Table 46; Table 84 | high |
| Message 5 draught 8 bits in 1/10 m, 255 = 25.5 m or greater, 0 = n/a; ETA 20 bits MMDDHHMM with 0/0/24/60 as n/a; call sign 7×6-bit; name 20×6-bit, "@" fill = n/a | M.1371-6 Table 49-ish ("Maximum … In 1/10 m, 255 = draught 25.5 m") | high |
| RATDMA limit for Messages 6, 8, 12, 14, 25 from a mobile: ≤20 slots per frame, ≤3 consecutive slots per message; with FATDMA reservations ≤5 consecutive | M.1371-6 Table 44 note (10) | high |
| Dual-channel rule: periodic messages alternate AIS 1/AIS 2; responses on the same channel as the initial message; addressed messages on the channel the addressee was last heard | M.1371-6 Table 44 note (6) | high |
| Burst stations (Annex 8): nominal 1 W e.i.r.p.; settling 0.833 ms; ramp-down 1.0 ms; burst = 8 messages, 75-slot increment, alternating AIS 1/AIS 2, no more than once per minute; first slot random; slot-time-out 7 in first burst; next burst offset random 1 min ± 6 s; sync accuracy ±3 bits (±312 µs); Message 1 and 14 from the same unit are linked if separated by a multiple of 75 slots within 450 slots; association timeout 8 min; test/deactivated mode uses one burst with slot-time-out 0 | M.1371-6 A8-2–A8-5 (pp. 151–153) | high |
| Burst Tx mask is looser than Class A: −20 dBc at ±10 kHz to −40 dBc at ±25 kHz; frequency error ±500 Hz normal / ±1 000 Hz extreme; spurious ≤25 µW in 108–137, 156–161.5, 1 525–1 610 MHz | M.1371-6 Table 89 | high |
| 12-character identity for burst devices: `97 T XX M PP YYYY` (T = 0 SART, 2 MOB, 4 EPIRB-AIS; XX manufacturer 01–99, 00 = test; M = manufacturer suffix; PP = sequence prefix; YYYY sequence). Message 1 carries the 9-digit `97TXXYYYY`; Message 14 appends `MPP`. Manufacturer IDs obtained via CIRM (www.cirm.org). | M.1371-6 A8-6 and footnote 23; M.585-10 Annex 2 §2 ¶4 | high |
| M.585 editions: -2 06/1990; -3 06/2003; -4 03/2007; -5 10/2009; -6 01/2012; -7 03/2015; -8 10/2019; -9 05/2022; -10 04/2026 (approved 2026-04-16, in force). Title-page revision string "(1982-1986-1990-2003-2007-2009-2012-2015-2019-2022-2026)". | https://www.itu.int/rec/R-REC-M.585/en; M.585-10 PDF p. 1 | high |
| M.585-10 structure: Annex 1 MMSI formats (ship, coast, SAR aircraft, AIS AtoN, craft associated with parent ship); Annex 2 identities for other devices (handheld DSC VHF, freeform identities for AIS-SART/MOB/EPIRB-AIS/AMRD-B); Annex 3 assignment/conservation guidance | M.585-10 Scope | high |
| Ship station: `MIDXXXXXX` (9 digits; MID = first three). Group ship: `0MIDXXXXX`. Coast station: `00MIDXXXX`, with optional 6th-digit scheme 00MID1XXX coast, 2 port, 3 pilot, 4 AIS repeater, 5 AIS base station. Group coast `00MID0000` addresses all 00MIDXXXX; `009990000` all-coast-stations identity (VHF only). | M.585-10 Annex 1 §1–§2 | high |
| SAR aircraft: `111MIDXXX` (999 per MID); optional 7th digit 1 = fixed-wing, 5 = helicopter; group `111MID000` | M.585-10 Annex 1 §3 | high |
| AIS AtoN: `99MIDXXXX` (10 000 per MID); optional 6th digit 1 = physical, 6 = virtual, 8 = mobile AtoN; types identified by Message 21 and Message 28; details to be made available to IALA; in MARS | M.585-10 Annex 1 §4 | high |
| Craft associated with parent ship: `98MIDXXXX`; includes first- and second-generation EPIRBs (per M.633); not for AIS-SART | M.585-10 Annex 1 §5 | high |
| Handheld VHF DSC with GNSS: `8MIDXXXXX` (100 000 per MID); registration left to administration; must be accessible to RCC 24/7 | M.585-10 Annex 2 §1; Annex 3 §2 | high |
| Freeform identities: prefixes 970 AIS-SART, 972 MOB, 974 EPIRB-AIS, 979 AMRD Group B. Format `97 T XX YYYY`, manufacturer ID 01–99, 00 = testing; sequence restarts at 0000 after 9999. These "are not necessarily unique and are not MMSI assignments" (considering f). | M.585-10 considering (f); Annex 2 §2 | high |
| AMRD Group B: `979YYYYYY`, Y = pseudorandom permutation of 0–999 999 (Fisher–Yates suggested); duplicates acceptable; Group B operates on channel 2006; Group A on channel 70 (DSC), AIS 1 and AIS 2 | M.585-10 Annex 2 §5 and footnote 4 | high |
| MMSI reuse: an assignment may be reused after absence from two successive editions of List V or two years, whichever is greater; administrations should request another MID when >80 % of the resource is exhausted | M.585-10 Annex 3 §1(d), §2(b) | high |
| M.585 references Resolution 344 (Rev.WRC-19) "Management of the maritime identity numbering resource" and ITU-T E.217 | M.585-10 p. 2 | high |
| M.2092 editions: -0 10/2015; -1 02/2022; -2 02/2026 | https://www.itu.int/rec/R-REC-M.2092/en | high |
| M.493 (DSC) editions: -6 09/1994 … -10 05/2000, -11 05/2004, -12 03/2007, -13 10/2009, -14 09/2015, -15 01/2019, -16 12/2023 (in force) | https://www.itu.int/rec/R-REC-M.493/en | high |
| M.2135 editions: -0 10/2019; -1 02/2023 | https://www.itu.int/rec/R-REC-M.2135/en | high |
| Radio Regulations editions available: 2008, 2012, 2016, 2020, 2024; PDFs free for personal use | https://www.itu.int/pub/R-REG-RR | high |
| Annex 7 "Class B AIS using CSTDMA technology" first appears in the M.1371-2 (03/2006) TOC | M.1371-2 TOC | high |
| Messages 24, 25, 26 appear in the M.1371-3 (06/2007) TOC; the -2 TOC does not list messages individually, so first appearance of 24/25/26 is ≤ -3 | M.1371-3 TOC; M.1371-2 TOC | medium |
| Message 27 and Annex 9 "Requirements for stations using burst transmissions" (AIS-SART) first appear in the M.1371-4 (04/2010) TOC; absent in -3 | M.1371-4 and -3 TOCs | high |
| Appendix 18 channel numbers: AIS 1 = 2087 (161.975 MHz), AIS 2 = 2088 (162.025 MHz), ASM 1 = 2027 (161.950 MHz), ASM 2 = 2028 (162.000 MHz); channels 75/76 (156.775/156.825 MHz) carry footnote *s)* permitting long-range AIS (Message 27) reception by the mobile-satellite service | web-search summary citing itu.int / CEPT / national regulators; cross-checked with M.1371-6 A1-5 for frequencies; see also `r-vdes.md` | medium (frequencies high; channel designators medium — read the RR 2024 App. 18 table to confirm) |

## Notes and quotes

- **The edition that matters changed in February 2026.** Essentially all published
  decoders, textbooks, and the gpsd AIVDM document cite M.1371-5 (2014) or earlier.
  M.1371-6 (approved 19 Feb 2026) renumbers annexes, removes the DSC
  channel-management annex, adds Message 28, reserves 60–63 for AMRD, marks
  Message 19 "no longer required", and adds an *Authentication Flag* bit in
  Message 28 pointing at IALA G1192. Any chapter that cites "M.1371-5 Annex 8"
  for messages must now say "M.1371-6 Annex 7 (formerly Annex 8 in M.1371-5)".
- Quote (scope): "This Recommendation provides the technical characteristics of
  an automatic identification system (AIS) using time division multiple access
  in the very high frequency (VHF) maritime mobile band." — M.1371-6, p. 1.
- Quote (identity): "AIS stations should not transmit without an appropriate
  MMSI." — M.1371-6, A1-3.
- Quote (burst mode is deliberately disruptive): "The burst behaviour channel
  access does not consider the current VDL activity and as such does not conform
  to the self-organizing rules for the VDL. The burst behaviour channel access is
  disruptive to the VDL. This type of channel access should be limited to
  'safety of life' applications which are designed to be floating on the surface
  of the water for a limited duration." — M.1371-6, A8-1.
- Quote (Message 28 purpose): "Message 28 provides similar information as AIS
  Message 21, but in one slot versus two slot, and can be used to report MAtoN
  direction and speed or provide extended information on the AtoN (i.e. its
  height) and what it's marking (i.e. hazardous area)." — M.1371-6, A7-3.26.
- Quote (freeform identities are not MMSIs): "the identities used for other
  maritime devices for special purposes indicated in Annex 2 … are not
  necessarily unique and are not MMSI assignments" — M.585-10, considering (f).
- Quote (CRC): "CRC errors should result in no further action by the AIS
  station." — M.1371-6, A2-3.2.3. (Relevant to Chapter 30 partial-packet recovery:
  the standard forbids *stations* from acting on bad packets; it says nothing
  about what shore/satellite *processing* may attempt.)
- The IPR notice on p. ii of M.1371-6 says ITU "had received notice of
  intellectual property, protected by patents, which may be required to implement
  this Recommendation" and points to the ITU-R patent information page — useful
  for Chapter 18 (the Lans/GP&C declaration history should be checked in that
  database; see `r-patents.md`).
- M.1371-6 Table 1 adds a condition for anchored ships that "swing" (0.2–3 kn with
  stable COG and COG roughly opposite heading) to report at 10 s rather than
  3 min — a change worth a *Then & now* note in Chapter 22 (verify by diffing
  against M.1371-5 Table 1, which had only the ">3 kn while anchored" rule).
- M.1371-6 Table 2 adds explicit VDL-loading hysteresis for Class B SO (<50 %
  free slots in four consecutive frames → modified interval; ≥65 % free → back).
- The M.1371-6 glossary includes BDS (BeiDou) and CHAYKA, indicating the EPFS
  wording is constellation-neutral (relevant to Chapter 25).
- The nav-status codes 9 and 10 are now simply "reserved for future use"; the
  M.1371-5 wording that reserved them for HSC/WIG amendments is gone (verify
  wording of -5).
- Appendix 18 channel designators (2087/2088/2027/2028) are widely quoted but
  this session did not open the RR Appendix 18 table itself; `r-vdes.md`
  covers the VDE channel designators (1024/1084… and 2024/2084…).

## Open questions / (verify)

- (verify) A clause-by-clause diff of M.1371-6 against M.1371-5: beyond the
  structural changes recorded above, which numeric parameters changed? Candidate
  items: Table 1 anchored-swing rule; Table 2 Class B SO hysteresis; nav status 9/10
  wording; Message 21 "Type of AtoN" table extension to 0–31 vs 32–50 (Table 85);
  anything in Annex 4 ASM (international FI 0/2/3/4/5 definitions).
- (verify) Did M.1371-6 add anything on authentication beyond the Message 28
  flag (e.g., a general reference to IALA G1192 or VDES-based signing)? Search
  the PDF for "G1192" and "authenticat".
- (verify) Page count of M.1371-5 PDF for the "how big is the standard" aside.
- (verify) Exact first edition in which Message 24 (Class B static data) and
  Messages 25/26 were added (-2 or -3): obtain the -2 PDF and check Annex 8.
- (verify) Report ITU-R M.2287 edition/year and whether a -1 exists; Report
  M.2169 year and URL.
- (verify) RR Appendix 18 (2024 edition) footnotes: confirm footnote letters for
  AIS 1/2 (historically *f)*/*l)* in older editions), *s)* for 75/76 long-range
  AIS, and the ASM/VDE footnotes; confirm the four-digit designators from the
  RR text rather than secondary summaries.
- (verify) Whether M.585-10 changed anything substantive vs. -9 other than
  adding Message 28 references and AMRD Group A/B wording.
- (verify) M.493-16 (12/2023) changes relevant to AIS (e.g., channel-management
  DSC messages now that M.1371-6 dropped its DSC annex — is DSC channel
  management of AIS formally dead?).
- (verify) Whether IMO Res. MSC.570(109) (Dec 2024) is indeed a revised AIS
  performance standard that M.1371-6 aligns with (a web summary claimed this;
  not confirmed from IMO sources in this session) — belongs to `r-standards-imo.md`.
- (verify) ITU-R Question 232/5 title.

## Candidate figures and worked examples

- **Figure: M.1371 edition timeline 1998→2026** with feature introductions (Class
  B CS annex 2006; Messages 24–26 ≤2007; Message 27 + AIS-SART burst annex 2010;
  Message 28 + AMRD 60–63 + 12-char identities 2026). (Ch. 11/12/15/22)
- **Figure: Annex renumbering map M.1371-5 → M.1371-6** (table with arrows;
  Annex 3 removed). (Ch. 15, App. B)
- **Figure: Transmitter power/time mask** redrawn from Table 6 (T0, TA, TB1, TB2,
  TE, TF, TG with bits and ms). (Ch. 28)
- **Figure: 256-bit packet layout** 8 ramp / 24 training / 8 flag / 168 data / 16
  CRC / 8 flag / 24 buffer. (Ch. 21/28, App. C)
- **Figure: Class B CS carrier-sense timing** (833–1 979 µs window, TA at
  2 083 µs). (Ch. 21)
- **Figure: AIS-SART burst pattern** (8 messages, 75-slot increments, alternating
  channels, 1 min ± 6 s). (Ch. 68)
- **Figure: MMSI/identity format family tree** from M.585-10 (MID…, 0MID, 00MID,
  111MID, 99MID, 98MID, 8MID, 970/972/974/979 + 12-char form). (Ch. 13, App. D)
- **Figure: Message 28 bit layout** (168 bits) next to Message 21 (272 bits) to
  show the single-slot compression. (Ch. 22/68, App. C)
- **Worked example: nominal increment.** Class A at 10 s → Rr = 6/min → NI =
  2 250/6 = 375 slots; at 2 s → Rr = 30 → NI = 75 slots. (Ch. 21)
- **Worked example: slot timing.** 60 s / 2 250 = 26.667 ms per slot; 26.667 ms ×
  9 600 bit/s = 256 bits; TB2 = 8 bits = 0.833 ms. (Ch. 21/28)
- **Worked example: ROT encoding.** Sensor 10°/min → 4.733 × √10 = 14.97 → 15;
  sensor 708°/min → 4.733 × √708 = 125.9 → 126 (saturation). (Ch. 22)
- **Worked example: position resolution.** 1/10 000 arc-minute = 0.1852 m of
  latitude; 28-bit longitude range ±180° = ±108 000 000 units, fits in 2^27. (Ch. 22)
- **Worked example: CS threshold.** Background −110 dBm → threshold clamped to
  −107 dBm; background −80 dBm → −77 dBm (clamp at 30 dB tracking). (Ch. 21/30)
- **Worked example: 12-character identity decode.** `970 01 A 01 1234` → SART,
  manufacturer 01, suffix A, prefix 01, serial 1234; Message 1 shows 970011234,
  Message 14 text "SART ACTIVE A01". (Ch. 13/68)

## Recommended use by chapter

- **Ch. 10** — M.1371-0 approved 11/1998 (gis-history ⟨H⟩ item); cite the ITU
  edition list for the date.
- **Ch. 11** — Class B CS annex (M.1371-2, 2006); Messages 24–26 by -3 (2007);
  Message 27 and AIS-SART burst annex (-4, 2010); M.585 editions -3 (2003)
  onward adding AtoN/aircraft formats (verify which edition added which).
- **Ch. 12** — M.1371-6 (Feb 2026) and M.585-10 (Apr 2026) as the current
  editions; Message 28; AMRD 60–63; authentication flag; VDES M.2092-2 (Feb 2026).
- **Ch. 13** — All M.585-10 formats and the conservation rules (reuse after two
  List V editions or two years); MARS URL; "freeform identities are not MMSIs".
- **Ch. 14/15** — ITU-R WP 5B owns M-series maritime Recs; Recs are free; RR free
  for personal use; how M.1371 *recommends* defer to IMO (SN.1/Circ.289) and IALA.
- **Ch. 16** — RR Article 19 (identities) and Appendix 18; Resolution 344
  (Rev.WRC-19) on identity numbering.
- **Ch. 18** — ITU IPR notice in M.1371-6; ITU-R patent database link.
- **Ch. 20** — Station classes from Annex 1; Tables 1–2 reporting intervals; power
  classes (12.5/1 W Class A; 5/1 W Class B SO; Class B CS carrier power
  **33 dBm ±1.5 dB conducted (= 2 W)** per M.1371-6 Annex 6 Table 35 (high);
  1 W e.i.r.p. burst devices). Note Class B CS training sequence "always starts
  with a 0" (A6-4.2.1.4) whereas Class A may start with 1 or 0.
- **Ch. 21** — Frame/slot constants; NI; 120 nmi rule; sync-state codes;
  semaphore rules; CS window and threshold; RATDMA per-frame limits; dual-channel
  alternation rules (Table 44 notes 6–7).
- **Ch. 22** — Table 44 message summary (incl. 28 and 60–63); field sentinels;
  ROT formula; nav status list; Message 19 "no longer required"; cite as
  "M.1371-6 Annex 7 Table 44/46/84".
- **Ch. 23** — Annex 4 ASM: international FIs 0, 2, 3, 4, 5 defined in A4-5;
  footnote that IMO maintains the international AI branch via SN.1/Circ.289;
  Message 28's note that DAC 1 FI 22 Area Notice should be used for complex
  AtoN areas.
- **Ch. 24** — Sync hierarchy (A2-3.1.1), semaphore qualification, base-station
  RI change to 3⅓ s when stations sync to it; burst-device sync accuracy ±312 µs.
- **Ch. 25** — EPFS neutrality; BDS and CHAYKA in glossary; timestamp 61/62/63.
- **Ch. 27/28** — PHY Tables 3–7, Table 6 mask, GMSK/NRZI/CRC details; channels
  75/76; antenna separation note (COMSAR.1/Circ.32/Rev.3).
- **Ch. 30** — Report ITU-R M.2287 (VDL loading) and M.2169 (satellite
  detection); Class B SO hysteresis thresholds (50 %/65 %).
- **Ch. 39** — Message 27 (96-bit payload, MSSA, 3 min, channels 75/76, base-station
  disable via Message 4 + 23); "Satellites with AIS receivers may receive AIS
  Message 27".
- **Ch. 68** — AIS-SART/MOB/EPIRB-AIS Annex 8 behaviour and Message 14 texts;
  AMRD Group A/B (M.2135-1), channel 2006, 979 identities; Message 28 for mobile
  AtoN / hazard marking.
- **Ch. 69** — M.2092 editions (defer to `r-vdes.md`).
- **App. B** — Register rows for every document in the sources table with
  edition/date/URL/access.
- **App. C/D** — Message 28 layout; Table 85 AtoN types 32–50; nav status;
  identity patterns.
