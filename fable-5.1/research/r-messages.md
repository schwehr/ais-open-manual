# Dossier: The AIS message catalog (Messages 1–28) — field semantics, sentinels, and a verified test-vector set

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the AIS VDL message catalog in Recommendation ITU-R M.1371-6 (February
2026): the field layouts and "not available" sentinels for Messages 1–28, the
rate-of-turn encoding, the Message 5 quirks, Message 27, the Class B family
(18/19/24A/24B), the AtoN report (21, and the new single-slot 28), the binary
containers (6/8/25/26), and the 6-bit ASCII alphabet. It also establishes a
**canonical test-vector set** — 44 sentences drawn from the public test suites of
gpsd, pyais and libais — every one of which was decoded during this session with
pyais 3.2.3 and libais 0.17 in the repository venv, with the decoder outputs
recorded and the discrepancies noted. It feeds **Chapter 22** (message catalog)
as its primary target, **Chapter 20** (which station sends what), **Chapter 23**
(binary containers → ASM; see `r-asm.md`), **Chapter 26** (NMEA framing of the
vectors), **Chapter 36/47** (sentinels and defaults as data-quality signals),
**Chapter 44** (decoder comparison and shared test corpus), **Chapter 68**
(AtoN/SART messages), **Appendix C** (bit layouts) and **Appendix D** (code
tables: nav status, ship type, EPFD, AtoN type).

> Research-session note. Facts marked *high* were read in the M.1371-6 PDF
> (itu.int, text-extracted). Decoder facts marked *high (run)* were produced by
> running the decoders in `.venv` during this session (script preserved in the
> session scratch directory as `decode_vectors.py`, output `vectors_decoded.txt`).
> Clause numbers use the M.1371-6 "A7-" prefix (M.1371-5 called this Annex 8).

## Key questions

1. What are the exact bit widths, units, ranges and "not available" sentinels for
   every field in Messages 1–28?
2. How is rate of turn encoded, and what do ±127 and −128 mean?
3. What do timestamp values 60/61/62/63 mean and how do they interact with the
   AtoN off-position flag and Class B CS?
4. What is specific to Message 5 (two slots, 424 bits, AIS version indicator, IMO
   number ranges, ETA with per-field sentinels, draught, DTE)?
5. What distinguishes Messages 18/19/24A/24B and what fixed value does a Class B
   CS put in the communication-state field?
6. What does Message 21 carry (AtoN type table, off-position, virtual flag, name
   extension) and how does Message 28 compress it?
7. How are the binary containers (6/8/25/26) structured and what are their
   capacities per slot?
8. What is in Message 27 (96 bits, 1/10-min position, no timestamp, repeat
   indicator always 3)?
9. What changed in the catalog in M.1371-6 (ship-type codes 1–19, VDES
   capability bits in 24B, Message 19 deprecated, Message 28, 60–63 reserved)?
10. Which public sentences decode identically in pyais, libais and gpsd, and
    where do the decoders disagree (units, sentinels, polarity)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Recommendation ITU-R M.1371-6, Annex 7 "AIS messages" | 02/2026, in force | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Table 44 message summary; Tables 45–85 field tables for Messages 1–28 (pp. 101–150) | Free |
| Recommendation ITU-R M.1371-5, Annex 8 (superseded) | 02/2014 | https://www.itu.int/rec/R-REC-M.1371-5-201402-S/en | Same catalog without Message 28; the edition most decoders implement | Free |
| gpsd *AIVDM/AIVDO protocol decoding* | version 1.58 (Eric S. Raymond; material contributed by Kurt Schwehr) | https://gpsd.gitlab.io/gpsd/AIVDM.html | Decoder-oriented field tables, NMEA framing, known deviations in the wild | Free |
| gpsd regression corpus `test/sample.aivdm` (+ `.chk`) | gpsd master, read 2026-10-05; "Copyright 2010 by the GPSD project, BSD terms"; data "provided from real data by Kurt Schwehr, Mike Greene, Neal Arundale, and AISHub" | https://gitlab.com/gpsd/gpsd/-/raw/master/test/sample.aivdm | 118 sentences with per-field expected values for Messages 1–27 | Free (BSD) |
| pyais `tests/test_decode.py` | pyais master, read 2026-10-05 (installed package 3.2.3) | https://raw.githubusercontent.com/M0r13n/pyais/master/tests/test_decode.py | Unit tests with sentences for Messages 1–28 incl. 28 dimension variants | Free (MIT) |
| libais `test/data/typeexamples.nmea` | libais master (installed package 0.17) | https://raw.githubusercontent.com/schwehr/libais/master/test/data/typeexamples.nmea | 26 NAIS-format sentences with USCG metadata suffixes | Free (Apache-2.0) |
| IMO Resolution A.1117(30) — IMO ship identification number scheme | 2017 | (IMO docs; cited by M.1371-6 Table 50 footnote) | IMO number used in Message 5 | Free |
| IALA Recommendation R0126 (A-126) — *The Use of AIS in Marine AtoN Services* | Ed. 2.0 (see `r-standards-iala.md`) | iala.int | Message 21 "AtoN status" 8-bit field semantics; AtoN types | Free |
| IEC 61162-1 / NMEA 0183 v4.11 | (see `r-interfaces.md`, `r-standards-nmea-rtcm-etsi.md`) | nmea.org / iec.ch | `!AIVDM`/`!AIVDO` sentence framing of the payloads below | Paid |

## Verified facts

### Catalog-level

| Fact | Source | Confidence |
|---|---|---|
| Table 44 defines Messages 1–28; 29–59 undefined/reserved; 60–63 used only by ITU-R M.2135 (AMRD position/identity/static/ASM) | M.1371-6 Table 44 (pp. 101–103) | high |
| Message 19 "No longer required … For future equipment: this message is not needed and should not be used. All content is covered by Message 18, Messages 24A and 24B." Legacy units send it every 6 min in two slots | Table 44; A7-3.17 (pp. 102, 128–129) | high |
| All positions WGS 84; all fields binary, negative numbers two's complement; character fields use the 6-bit ASCII of Table 45 (`@`=0 … `_`=31, space=32 … `?`=63); unused characters are `@` placed at the end | A7-3; Table 45; A2-3.3.7 (pp. 104–105, 46) | high |
| Message priorities: 1 (1,2,3,4,7,9,13,16,18,19,20,21,22,23,27,28), 2 (12,14,17), 3 (10,11,15), 4 (5,6,8,24,25,26); Message 5 priority 3 when answering an interrogation | Table 44 and note 5 | high |
| Repeat indicator 2 bits: 0 default; 3 = do not repeat any more; Message 27 "Always 3" | Tables 46, 83 | high |
| Position (Messages 1–4, 9, 11, 18, 19, 21): longitude 28 bits in 1/10 000 min, 181° = 6791AC0h = n/a; latitude 27 bits, 91° = 3412140h = n/a | Table 46 | high |
| Low-resolution position (Messages 17, 22, 23, 27, and ASM headers): longitude 18 bits / latitude 17 bits in **1/10 min**; 181°/91° = n/a (Message 27: 1A838h / D548h) | Tables 66, 73, 74, 83 | high |
| COG 12 bits in 1/10°, 0–3 599; 3 600 (E10h) = n/a; 3 601–4 095 "should not be used" | Table 46 | high |
| True heading 9 bits 0–359; 360–510 should not be used; 511 = n/a | Table 46 | high |
| SOG 10 bits in 1/10 kn; 1 023 = n/a; 1 022 = 102.2 kn or higher (Message 9: whole knots, 1 022 = 1 022 kn or higher) | Tables 46, 60 | high |
| Time stamp 6 bits: 0–59 UTC second of the EPFS fix; 60 = n/a (default); 61 = manual input; 62 = dead reckoning; 63 = EPFS inoperative; 61–63 "are not used by 'CS' AIS" | Tables 46, 68 | high |
| Position accuracy 1 bit: 1 = high (≤10 m), 0 = low (>10 m, default), determined per Table 48 from RAIM expected error (√(err_lat² + err_lon²) ≤ 10 m) and differential-correction status | Table 46, Table 48 | high |
| RAIM flag 1 bit: 0 not in use (default), 1 in use | Table 46 | high |
| Nav status (4 bits): 0 under way using engine, 1 at anchor, 2 NUC, 3 RAM, 4 constrained by draught, 5 moored, 6 aground, 7 fishing, 8 under way sailing, 9–10 reserved, 11 towing astern (regional), 12 pushing ahead/towing alongside (regional), 13 reserved, 14 active AIS-SART/MOB/EPIRB-AIS, 15 undefined (default; also devices under test) | Table 46 (pp. 105) | high |
| **ROT encoding (8 bits, two's complement):** 0 … ±126 = turning at up to 708°/min or higher, ROT_AIS = 4.733 √(ROT_sensor) rounded to nearest integer; **+127 / −127 = turning right/left at more than 5° per 30 s with no TI available**; **−128 (80h) = no turn information (default)**; "ROT data should not be derived from COG information" | Table 46 (p. 105) | high |
| Special manoeuvre indicator 2 bits: 0 n/a, 1 not engaged, 2 engaged (regional passing arrangement on inland waterways), 3 regional | Table 46 | high |
| Messages 1/2 carry SOTDMA comm state; Message 3 carries ITDMA comm state (Table 47); layouts in `r-link-layer.md` | Table 47 | high |
| Message 4/11 (168 bits): UTC year 14 (0 n/a), month 4 (0 n/a), day 5 (0 n/a), hour 5 (24 n/a), minute 6 (60 n/a), second 6 (60 n/a); EPFD type 4 bits; **transmission control for Message 27** 1 bit (0 = Class A stops Message 27 inside base-station coverage; 1 = request Class A to transmit it); spare 9; RAIM; SOTDMA comm state. Message 4 is used by mobiles to decide whether they are within 120 nmi for Messages 20/23 | Table 49; A7-3.2 (pp. 107–109) | high |
| EPFD type (Messages 4/5/11/19/21/24B): 0 undefined, 1 GPS, 2 GLONASS, 3 combined GNSS, 4 Loran, 5 Chayka, 6 INS, 7 surveyed/manual, 8 Galileo, **9 BDS, 10–11 not used, 12 integrated PNT, 13 inertial navigation, 14 terrestrial radio navigation, 15 internal GNSS** | Table 49 (p. 108) | high |

### Message 5 (Table 50, 424 bits, two slots)

| Fact | Source | Confidence |
|---|---|---|
| Only Class A (and legacy SAR aircraft) use Message 5; future SAR aircraft use Message 5 or 24A | A7-3.3 (p. 109) | high |
| AIS version indicator 2 bits: 0 = M.1371-1 compliant, 1 = M.1371-3, 2 = M.1371-5, **3 = M.1371-6 or later** | Table 50 | high |
| IMO number 30 bits: 1–999 999 not used; 1 000 000–9 999 999 valid IMO number; 10 000 000–1 073 741 823 "official flag state number"; footnote: per IMO Res. A.1117(30); if no IMO number, use an official flag-state number | Table 50 and footnote (1) | high |
| Call sign 7 × 6-bit (42 bits), `@@@@@@@` = n/a; craft associated with a parent vessel use "A" + last 6 digits of the parent MMSI | Table 50 | high |
| Name 20 × 6-bit (120 bits), `@…@` = n/a, "as shown on the station radio license" | Table 50 | high |
| Type of ship and cargo 8 bits: 0 n/a; 1–99 per Table 51; 100–199 regional; 200–255 future | Table 50 | high |
| **Table 51 in M.1371-6 defines codes 1–19** (01 research vessel, 02 training, 03 government-owned, 04 icebreaker, 05 buoy tender, 06 cable layer, 07 pipe layer, 09 special purpose n.a.i.; 11 FPSO, 12 fish factory, 13 fish-farm support, 14 offshore support, 17 construction, 18 crew boat, 19 support n.a.i.); 20–29 WIG; 30 fishing, 31 towing, 32 towing >200 m/>25 m, 33 dredger, 34 diving, 35 warship/naval auxiliary, 36 sailing, 37 pleasure, **38 trawler, 39 patrol vessel**; 40–49 HSC (45 HSC passengers, 46 HSC ro-ro); 50 pilot, 51 SAR, 52 tug, 53 port/fish tender, 54 anti-pollution/firefighting, 55 law enforcement, 56–57 local spare, 58 medical transport, 59 non-party ship; 60–69 passenger (65 cruise, 66 ferry, 67 excursion); 70–79 cargo (75 bulk, 76 container, 77 ro-ro, 78 landing craft); 80–89 tanker (85 non-hazardous, **86 integrated/articulated tug-barge**); 90–99 other. Second digit 1–4 = DG/HS/MP category X/Y/Z/OS (formerly A/B/C/D) | Table 51 (pp. 111–114) | high |
| In earlier editions (and in gpsd/pyais/libais lookup tables) codes 1–19 and 38/39, 45/46, 65–67, 75–78, 85/86 were "reserved for future use"; M.1371-6 populates them | gpsd AIVDM.html ship-type table (read 2026-10-05) vs Table 51 | medium (verify against the M.1371-5 PDF; gpsd lists 1–19 as reserved) |
| Dimension/reference 30 bits = A (9 bits, to bow), B (9, to stern), C (6, to port), D (6, to starboard) in metres; A=B=C=D=0 = n/a; towing vessels pushing/alongside include the tow | Table 50; A7-3.3.3 Fig. 38 note (p. 115); bit split per gpsd/libais | high (standard) / high (bit split, run) |
| ETA 20 bits MMDDHHMM UTC: month bits 19–16 (0 n/a), day 15–11 (0 n/a), hour 10–6 (24 n/a), minute 5–0 (60 n/a) — each sub-field has its own sentinel | Table 50 | high |
| Maximum present static draught 8 bits in 1/10 m; 255 = 25.5 m or greater; 0 = n/a; "in accordance with IMO Resolution A.851" | Table 50 | high |
| Destination 20 × 6-bit, `@…@` = n/a (IMO SN/Circ.244 recommends UN/LOCODE; see `r-standards-imo.md`) | Table 50 | high |
| DTE 1 bit: 0 = available, 1 = not available (default); indicates a minimum-keyboard-and-display capable station | Table 50; A7-3.3.1 | high |

### Binary containers (Messages 6, 7, 8, 25, 26)

| Fact | Source | Confidence |
|---|---|---|
| Message 6: ID 6, repeat 2, source 30, sequence number 2, destination 30, retransmit flag 1, spare 1, binary data ≤936 (16-bit application identifier + ≤920 application bits); max 1 008 bits; ≤3 slots (≤5 with FATDMA); Class B SO ≤3 slots; Class B CS shall not transmit | Table 52 (pp. 115–116) | high |
| Message 6 slot budget (Table 53): 1 slot 8 bytes, 2 slots 36, 3 slots 64, 4 slots 92, 5 slots 117 — "take bit stuffing into account" | Table 53 (p. 117) | high |
| Message 8: ID 6, repeat 2, source 30, spare 2, binary ≤968 (AI 16 + ≤952); max 1 008 bits; slot budget (Table 56) 12/40/68/96/121 bytes | Tables 55–56 (pp. 118) | high |
| Message 7/13: acknowledge up to four MMSIs (each 30 bits + 2-bit sequence number); same layout | Table 54 (via A7-3.5; libais/pyais decodes) | high (structure) / medium (exact bit count not re-read) |
| Message 25: destination indicator 1, binary-data flag 1, optional destination 30 + spare 2, data max 128 (broadcast, unstructured) / 112 (broadcast with AI) / 96 (addressed) / 80 (addressed with AI); never acknowledged; Class B CS shall not transmit | Tables 79–80 (pp. 142–143) | high |
| Message 26: as 25 plus 4 spare + 1-bit comm-state selector + 19-bit comm state; max 1 064 bits; data up to 1 000 bits over 5 slots (Table 82: 104/328/552/776/1000 broadcast unstructured; 56/280/504/728/952 addressed with AI); never acknowledged | Tables 81–82 (pp. 144–145) | high |
| Messages 12/14 (safety text): same header pattern as 6/8 with 6-bit ASCII text ≤936 / ≤968 bits; max 1 008 bits | A7-3.10, A7-3.12 (pp. 119–121) | high |

### Message 9 (SAR aircraft, 168 bits)

| Fact | Source | Confidence |
|---|---|---|
| Altitude 12 bits in metres, 0–4 094; 4 095 = n/a; 4 094 = 4 094 m or higher; SOG 10 bits in whole knots (1 022 = ≥1 022 kn; 1 023 n/a); altitude sensor 1 bit (0 GNSS, 1 barometric); DTE; assigned-mode flag; comm-state selector + 19-bit comm state | Table 60 (pp. 120–121) | high |

### Class B family (Messages 18, 19, 24)

| Fact | Source | Confidence |
|---|---|---|
| Message 18 (168 bits): spare 8; SOG; PA; lon/lat; COG; heading; time stamp; transmit power 1 bit (0 high default, 1 low); spare 1; **Class B unit flag** (0 SOTDMA, 1 CS); display flag; DSC flag; band flag; Message 22 flag; mode flag (assigned); RAIM; comm-state selector (always 1 for CS); 19-bit comm state | Table 68 (pp. 127–128) | high |
| **Class B CS comm-state fill value is the fixed 19-bit pattern `1100000000000000110`** (= 393 222 decimal) because CS "does not use any Communication State information" | Table 68 (p. 128) | high |
| Message 24A (160 bits): part number 2 (0), name 120; SAR aircraft name "SAR AIRCRAFT NNNNNNN". Part A sent every 6 min alternating channels; "may be used by any AIS station to associate a MMSI with a name" | Table 76; A7-3.22 (pp. 139–140) | high |
| Message 24B (168 bits): part number 1; ship type 8; manufacturer ID 42 (= 3-char NMEA mnemonic 18 bits + unit model code 4 bits + serial 20 bits, Table 78); call sign 42; dimension/reference 30; EPFD 4; **VDES capabilities 2 bits (0 AIS only; 1 VDES ASM; 2 ASM/VDE-TER; 3 ASM/VDE-TER/VDE-SAT)** | Tables 77–78 (pp. 140–142) | high |
| The 2-bit VDES-capabilities field occupies what was a 2-bit spare in M.1371-5 Message 24B | arithmetic (6+2+30+2+8+42+42+30+4 = 166 + 2 = 168) and gpsd layout (spare 2) | medium |
| 24B must follow 24A within 1 min; Class B sends both every 6 min; Class A answers an interrogation for 24 with part B carrying the manufacturer ID only, and "shall send out Message 24B within 12 min after starting up and every 24 h thereafter" | A7-3.22 (p. 140) | high |

### Message 21 / 28 (AtoN)

| Fact | Source | Confidence |
|---|---|---|
| Message 21 (272–360 bits, two slots): AtoN type 5 bits (Table 72, 0–31); name 120; PA; lon/lat; dimension/reference 30; EPFD 4; time stamp 6; **off-position indicator** 1 (only meaningful when time stamp ≤59; floating aid = outside installed zone; fixed aid = internal GNSS outside zone, "suspected GNSS anomaly"); AtoN status 8 (per IALA R0126); RAIM; **virtual AtoN flag** 1; assigned-mode flag 1; spare 1; name extension 0–84 bits in 6-bit steps (not padded; omitted when unused; `@@@` prefix means "portray as label"); spare 0/2/4/6 for byte alignment | Table 71 (pp. 132–134) | high |
| Rr for Message 21 is 3 min autonomously or as assigned; also transmitted immediately after any parameter change; AtoN out of position should also trigger a Message 14 at the authority's discretion (IALA NAVGUIDE quote) | A7-3.19 (p. 132) | high |
| Table 72 AtoN types: 0 default; 1 reference point; 2 RACON or MAtoN; 3 fixed structure (offshore platform, wind farm); 4 emergency wreck-marking buoy; 5–19 fixed AtoN (5 light no sectors … 9–12 cardinal beacons N/E/S/W, 13 port-hand beacon, 14 starboard, 15/16 preferred-channel, 17 isolated danger, 18 safe water, 19 special mark); 20–31 floating (20–23 cardinal N/E/S/W, 24 port, 25 starboard, 26/27 preferred channel, 28 isolated danger, 29 safe water, 30 special mark, 31 light vessel/LANBY/rig) | Table 72 (pp. 135–136) | high |
| AtoN dimensions: fixed/virtual/offshore A points true north; floating aids >2 m × 2 m use a circle A=B=C=D≠0; A=B=C=D=1 for objects ≤2 m × 2 m; virtual AtoN dimensions A=B=C=D=0 | A7-3.19.1 (p. 134) | high |
| Message 28 (168 bits, one slot) exists only in M.1371-6; layout and the "Authentication Flag (IALA G1192)" are recorded in `r-standards-itu.md` | A7-3.26, Tables 84–85 | high |

### Message 27 (Table 83, 96 bits)

| Fact | Source | Confidence |
|---|---|---|
| Fields: ID 6; repeat 2 **always 3**; MMSI 30; PA 1; RAIM 1; nav status 4; longitude 18 (1/10 min; 181° = 1A838h = older than 6 h or n/a); latitude 17 (91° = D548h); SOG 6 in whole knots (62 = ≥62 kn, 63 n/a); COG 9 whole degrees (511 n/a); **position latency 1 (0 = <5 s; 1 = >5 s = default)**; spare 1. "There is no time stamp in this message. The receiving system is expected to provide the time stamp." Footnote: previously named "long range broadcast message" | Table 83 and notes (p. 145) | high |

### Decoder behaviour observed in this session (pyais 3.2.3, libais 0.17)

| Fact | Source | Confidence |
|---|---|---|
| pyais 3.2.3 decodes Message 28 (`msg_type 28`, fields `station_type`, `aid_type`, `iala_mrn`, `dimension`, `auth` …); libais 0.17 raises "message 28 (L) not handled" | run of `!AIVDO,1,1,,A,L1mg=5@@G:uk?S:I0@ph>A5E>L@1,0*43` (pyais test vector) | high (run) |
| **ROT sentinels:** for raw −127 pyais reports `turn: -127.0`; libais reports `rot: -720.003…` (it applies −(127/4.733)² to the sentinel). For raw −128 pyais gives −128.0, libais −731.39. Neither returns a "no TI"/"not available" marker; consumers must test the raw value | gpsd vector `15RTgt0PAso;90TKcjM8h6g208CQ` (ROT −127) and libais typeexamples `15N1u<PP1FJuvSRHOE6QIwwh0HQ6` (ROT −128) | high (run) |
| **1/10-min fields are scaled inconsistently:** Message 17 reference position decodes as lon 1747.8 / lat 3599.2 in pyais (tenths of minutes ÷10 = minutes) but 29.13° / 59.9867° in libais; pyais Message 22 area corners come out as −4410.0/2733.0 (raw 1/10 min) | gpsd Message 17 and 22 vectors | high (run) |
| pyais `radio` for a Class B CS includes the 1-bit comm-state selector: 917 510 = 2¹⁹ + 393 222; libais reports `commstate_flag: 1` and `commstate_cs_fill: 393222` separately | gpsd/pyais Message 18 vectors | high (run) |
| **Message 27 "GNSS/latency" polarity differs:** for `K01;FQh?PbtE3P00` pyais `gnss: False`, libais `gnss: True` (same raw bit) | pyais test vector | high (run); (verify) which maps to Table 83 "0 = latency < 5 s" |
| gpsd vector `KC5E2b@U19PFdLbMuc5=ROv62<7m` (Message 27 padded to 168 bits, as seen from some transponders): pyais decodes it; libais raises `AIS_ERR_BAD_BIT_COUNT` | run | high (run) |
| Inland DAC 200 FI 10 draught: pyais 2.04 m vs libais 20.4 m for the same bits (factor 10) | gpsd vector `83aDChPj2d<dL<uM=hhhI?a@6HP0` | high (run); (verify) correct scale is 1/100 m per the Inland AIS standard (pyais would then be right) |
| DAC 1 FI 22 area notice (`803Ovrh0EP:024`@02PN04da=3V<>N0000,4`): libais decodes sub-areas (circle at −69.865, 42.083, radius 9 260 m, notice type 0 "Caution Area: Marine mammals habitat"), duration 2 min; pyais exposes `duration: 20` and raw `area_data` | run | high (run); (verify) duration units |
| Message 6 with unknown DAC/FI (669:11): pyais returns raw `data`; libais raises `DAC:FI not known` | gpsd vector `6B?n;be:cbapalgc;i6?Ow4,2` | high (run) |
| libais 0.17 does not expose Message 15/16/20 sub-fields through `ais.decode` dicts (only id/mmsi/spare), whereas pyais returns `mmsi1`, `offset1`, `increment1`, `number1`, `timeout1` | run | high (run) |
| gpsd's own expected values for the first Message 1 vector: MMSI 371798000, nav status 0, ROT −127, SOG 12.3, PA 1, lon −123.395383, lat 48.381633, COG 224, HDG 215, timestamp 33, sync state 0, slot time-out 2, "slot offset" 1249 (gpsd labels the sub-message generically; with time-out 2 it is the slot number) | gpsd sample.aivdm comment block; matches pyais/libais | high (run) |

## Canonical test-vector set (decoded 2026-10-05 in `.venv`)

All sentences below are verbatim from the named public corpus. "pyais" and
"libais" columns give the key decoded values; ✓ means both decoders agree on
every listed value. Positions are rounded to 6 decimals. These are offered for
`code/decode/` and Chapter 22/44 "Try it" boxes; the `.chk` file of gpsd gives
the gpsd expected JSON for each gpsd sentence.

| # | Msg | Sentence(s) | Source | Key decoded values (pyais 3.2.3) | libais 0.17 |
|---|---|---|---|---|---|
| 1 | 1 | `!AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A` | gpsd (Schwehr) | MMSI 371798000; status 0; ROT raw −127; SOG 12.3; PA 1; −123.395383, 48.381633; COG 224.0; HDG 215; ts 33; sync 0, timeout 2, slot number 1249 | ✓ (ROT shown as −720.0) |
| 2 | 1 | `!AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0*5C` | pyais | MMSI 366053209; status 3; ROT 0; SOG 0; −122.341618, 37.802118; COG 219.3; HDG 1; ts 59; timeout 0, slot offset 2281 | ✓ |
| 3 | 1 | `!AIVDM,1,1,,A,15N1u<PP1FJuvSRHOE6QIwwh0HQ6,0*30` | libais typeexamples | MMSI 367033650; status 0; ROT raw −128; SOG 8.6; −70.346905, 42.79855; COG 35.9; HDG 511; ts 56; timeout 6, slot number 2118 | ✓ (ROT −731.4) |
| 4 | 2 | `!AIVDM,1,1,,B,25Cjtd0Oj;Jp7ilG7=UkKBoB0<06,0*60` | gpsd | MMSI 356302000; ROT raw +127; SOG 13.9; −71.626143, 40.392358; COG 87.7; HDG 91; ts 41; timeout 3, received stations 6 | ✓ |
| 5 | 3 | `!AIVDM,1,1,,A,38Id705000rRVJhE7cl9n;160000,0*40` | gpsd | MMSI 563808000; status 5 (moored); SOG 0; PA 1; −76.327533, 36.91; COG 252; HDG 352; ts 35; ITDMA increment 0, slots 0, keep 0 | ✓ |
| 6 | 4 | `!AIVDM,1,1,,A,403OviQuMGCqWrRO9>E6fE700@GO,0*4D` | gpsd | MMSI 3669702; 2007-05-14 19:57:39; PA 1; −76.352362, 36.883767; EPFD 7 (surveyed); timeout 4, slot number 1503 | ✓ |
| 7 | 4 | `!AIVDM,1,1,,A,402Fha0000Htt<tSF0l4Q@000d20,0*65` | gpsd | MMSI 2470052; year 0, month 0, day 0, hour 24, minute 60, second 60 (all n/a); lon 181, lat 91 (n/a); EPFD 0; sync state 1, timeout 3, received stations 128 | ✓ |
| 8 | 5 | `!AIVDM,2,1,1,A,55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*1C` + `!AIVDM,2,2,1,A,88888888880,2*25` | gpsd | MMSI 351759000; AIS version 0; IMO 9134270; call sign 3FOF8; name EVER DIADEM; type 70; A 225 B 70 C 1 D 31; EPFD 1; ETA 05-15 14:00; draught 12.2; dest NEW YORK; DTE 0 | ✓ |
| 9 | 5 | `!AIVDM,1,1,1,B,53eaFL02?;fwTPm7V219E@R1@PE8E<622222221@9hG1A7?@NCPSlm3kc5DhH8888888880,2*7F` | libais typeexamples | MMSI 249190000; IMO 9383663; 9HMQ9; RUTH THERESA; type 80; 78/23/1/17; ETA 12-30 16:30; draught 7.8; BOSTON,USA | ✓ |
| 10 | 6 | `!AIVDM,1,1,,B,6B?n;be:cbapalgc;i6?Ow4,2*4A` | gpsd | MMSI 150834090; repeat 1; seq 3; dest 313240222; DAC 669 FI 11; data `eb2f118f7ff1` | libais: DAC:FI not known |
| 11 | 7 | `!AIVDM,1,1,,A,702R5`hwCjq8,0*6B` | gpsd | MMSI 2655651; ack of 265538450 | ✓ (libais shows only mmsi) |
| 12 | 8 | `!AIVDO,1,1,5,A,8>jR06@0Gwli:QQUP3en?wvlFR06EuOwgwl?wnSwe7wvlOwwsAwwnSGmwvh0,0*51` | gpsd | MMSI 992509977; DAC 1 FI 31 (met/hydro); −6.134067, 53.294933; day 29 23:24 | ✓ |
| 13 | 8 | `!AIVDM,1,1,,B,83aDChPj2d<dL<uM=hhhI?a@6HP0,0*40` | gpsd | MMSI 244650946; DAC 200 FI 10 (Inland static); draught 2.04 | libais draught 20.4 (scale differs) |
| 14 | 8 | `!AIVDM,1,1,,B,803Ovrh0EP:024`@02PN04da=3V<>N0000,4*39` | libais typeexamples | MMSI 3669739; DAC 1 FI 22 area notice; link id 10; notice 0; 01-01 05:02 | libais adds circle −69.864983, 42.08295 r 9 260 m |
| 15 | 9 | `!AIVDM,1,1,,B,91b55wi;hbOS@OdQAC062Ch2089h,0*30` | gpsd | MMSI 111232511; alt 303 m; SOG 42; −6.278843, 58.144; COG 154.5; ts 15; DTE 1; timeout 2, slot number 624 | ✓ |
| 16 | 10 | `!AIVDM,1,1,,B,:5MlU41GMK6@,0*6C` | gpsd | MMSI 366814480 → dest 366832740 | ✓ |
| 17 | 11 | `!AIVDM,1,1,,B,;4R33:1uUK2F`q?mOt@@GoQ00000,0*5D` | gpsd | MMSI 304137000; 2009-05-22 02:22:40; PA 1; −94.407683, 28.409117; EPFD 1; timeout 0, offset 0 | ✓ |
| 18 | 12 | `!AIVDM,1,1,,A,<02:oP0kKcv0@<51C5PB5@?BDPD?P:?2?EB7PDB16693P381>>5<PikP,0*37` | gpsd | MMSI 2275200 → 215724000; seq 0; "PLEASE REPORT TO JOBOURG TRAFFIC CHANNEL 13" | ✓ |
| 19 | 13 | `!AIVDM,1,1,,A,=39UOj0jFs9R,0*65` | gpsd | MMSI 211378120; ack of 211217560 | ✓ |
| 20 | 14 | `!AIVDM,1,1,,A,>5?Per18=HB1U:1@E=B0m<L,2*51` | gpsd | MMSI 351809000; "RCVD YR TEST MSG" | ✓ |
| 21 | 15 | `!AIVDM,1,1,,A,?5OP=l00052HD00,2*5B` | gpsd | MMSI 368578000; interrogates 5158 (short/odd vector) | libais: header only |
| 22 | 16 | `!AIVDM,1,1,,A,@01uEO@mMk7P<P00,0*18` | gpsd | MMSI 2053501 assigns 224251000: offset 200, increment 0 (→ 200 reports/10 min = 3 s) | libais: header only |
| 23 | 17 | `!AIVDM,2,1,5,A,A02VqLPA4I6C07h5Ed1h<OrsuBTTwS?r:C?w`?la<gno1RTRwSP9:BcurA8a,0*3A` + `!AIVDM,2,2,5,A,:Oko02TSwu8<:Jbb,0*11` | gpsd | MMSI 2734450; ref. station at 29.13°E, 59.9867°N (libais); pyais shows 1747.8/3599.2 (minutes) | scale differs |
| 24 | 18 | `!AIVDM,1,1,,A,B52K>;h00Fc>jpUlNV@ikwpUoP06,0*4C` | gpsd | MMSI 338087471; SOG 0.1; −74.072132, 40.68454; COG 79.6; HDG 511; ts 49; CS unit; display 0; DSC 1; band 1; msg22 1; RAIM 1; radio 917510 | ✓ |
| 25 | 18 | `!AIVDM,1,1,,A,B5NJ;PP005l4ot5Isbl03wsUkP06,0*76` | pyais | MMSI 367430530; SOG 0; −122.26732, 37.785035; CS unit; comm-state fill 393222 | ✓ |
| 26 | 19 | `!AIVDM,1,1,,B,C5N3SRgPEnJGEBT>NhWAwwo862PaLELTBJ:V00000000S0D:R220,0*0B` | gpsd | MMSI 367059850; SOG 8.7; −88.810392, 29.543695; COG 335.9; name CAPT.J.RIMES; type 70; 5/21/4/4; EPFD 1 | ✓ |
| 27 | 20 | `!AIVDM,1,1,,A,Dh3OvjB8IN>4,0*1D` | gpsd | MMSI 3669705; repeat 3; offset 2182, slots 5, timeout 7, increment 225 | libais: header only |
| 28 | 20 | `!AIVDM,1,1,,B,D030p8@2tN?b<`O6DmQO6D0,2*5D` | gpsd | MMSI 3160097; block 1: offset 47, slots 1, timeout 7, increment 250 (+2 more blocks per gpsd) | libais: header only |
| 29 | 21 | `!AIVDM,2,1,5,B,E1mg=5J1T4W0h97aRh6ba84<h2d;W:Te=eLvH50```q,0*46` + `!AIVDM,2,2,5,B,:D44QDlp0C1DU00,2*36` | gpsd | MMSI 123456789; type 20 (cardinal N); name "CHINA ROSE MURPHY EX" + extension "PRESS ALERT"; −122.698592, 47.920618; 5/5/5/5; EPFD 1; ts 50; off-position 0; virtual 0 | ✓ (libais joins the extension) |
| 30 | 22 | `!AIVDM,1,1,,A,F030ot22N2P6aoQbhe4736L20000,0*1A` | gpsd | MMSI 3160048; channels 2087/2088; txrx 0; power high; broadcast area (corners in 1/10 min) | ✓ |
| 31 | 22 | `!AIVDM,1,1,,A,F@@W>gOP00PH=JrN9l000?wB2HH;,0*44` | gpsd | MMSI 17419965; repeat 1; addressed; channel A 3584, B 8 (nonsense values — a corrupt/odd vector gpsd keeps for regression) | ✓ |
| 32 | 22 | `!AIVDM,1,1,,B,Fe3>>MOD@GDF?ThcoCk02?ioQie4,0*03` | gpsd | repeat 2; MMSI 875794037; addressed; dest 837968222 / 254804543 (gpsd regression for signed-field bug) | ✓ |
| 33 | 23 | `!AIVDM,1,1,,B,G02:Kn01R`sn@291nj600000900,2*12` | gpsd | MMSI 2268120; station type 6 (inland); ship type 0; txrx 0; interval code 9 (next shorter); quiet 0 | ✓ |
| 34 | 24A | `!AIVDM,1,1,,A,H42O55i18tMET00000000000000,2*6D` | gpsd | MMSI 271041815; part 0; name PROGUY | ✓ |
| 35 | 24B | `!AIVDM,1,1,,A,H42O55lti4hhhilD3nink000?050,0*40` | gpsd | MMSI 271041815; part 1; type 60; vendor "1D0" model 12 serial 199796 (libais: vendor_id "1D00014"); call sign TC6163; 0/15/0/5 | ✓ (vendor split differs) |
| 36 | 24B | `!AIVDO,1,1,,A,H8=;nnT000000000000000Wg8Jb0,0*26` | pyais | MMSI 550696666; type 0; 317/456/26/42 (implausible dims — a test fixture) | ✓ |
| 37 | 25 | `!AIVDM,1,1,,A,I6SWo?8P00a3PKpEKEVj0?vNP<65,0*73` | gpsd | MMSI 440006460; addressed to 134218384; unstructured data `e06f855b566c803fe7a0306140` | libais: header only |
| 38 | 26 | `!AIVDM,1,1,,A,J0@00@370>t0Lh3P0000200H:2rN92,4*14` | gpsd | MMSI 16777280; broadcast; data `c700ef00…`; libais: ITDMA sync 3, increment 2530, slots 2 | partial |
| 39 | 27 | `!AIVDM,1,1,,B,KC5E2b@U19PFdLbMuc5=ROv62<7m,0*16` | gpsd | repeat 1; MMSI 206914217; status 2; SOG 57; 137.023333, 4.84; COG 167 (168-bit nonstandard length) | libais: BAD_BIT_COUNT |
| 40 | 27 | `!AIVDM,1,1,,A,KCQ9r=hrFUnH7P00,0*41` | gpsd | repeat 1; MMSI 236091959; status 3; −154.201667, 87.065; SOG 0; COG 0 | ✓ |
| 41 | 27 | `!AIVDO,1,1,,A,K01;FQh?PbtE3P00,0*75` | pyais | MMSI 1234567; −13.368333, −50.121667 (southern/western signs) | ✓ except `gnss` polarity |
| 42 | 28 | `!AIVDO,1,1,,A,L1mg=5@@G:uk?S:I0@ph>A5E>L@1,0*43` | pyais | MMSI 123456789; 10.123712, 54.349133; station type 1; AtoN type 7; MRN 12345; dimension type 1 (A 42, B 1337); charted 1; on-station 1; auth 1 | libais: not handled |
| 43 | 4 | `!AIVDM,1,1,,B,4>O7m7Iu@<9qUfbtm`vSnwvH20S8,0*46` | gpsd | year 10196, lon 205.1169, lat 109.332 — out-of-range values pass through both decoders unflagged | ✓ (both pass garbage) |
| 44 | 18 | `!AIVDO,1,1,,A,B5NJ;PP2aUl4ot5Isbl6GwsUkP06,0*35` | pyais | SOG 67.8 kn Class B — plausibility test fixture | ✓ |

Observations for Chapter 44/47: (i) neither decoder validates ranges (vector 43);
(ii) sentinel handling for ROT and the 1/10-min scaling are the two most common
sources of silent disagreement; (iii) libais is the only one of the two that
decodes IMO/USCG ASM payloads (DAC 1 FI 22 sub-areas) but it lacks Message 28
and the 15/16/20 sub-fields in its Python dict output; (iv) gpsd's corpus
deliberately contains malformed/odd sentences (vectors 21, 31, 32, 39, 43) that
make good robustness tests for Chapter 60.

## Notes and quotes

- Quote (ROT): "ROT data should not be derived from COG information." —
  M.1371-6 Table 46. Relevant to Chapter 47: an ROT of exactly 0 with a visibly
  turning track usually means "no TI" encoded wrongly as 0 instead of −128.
- Quote (Message 27 timing): "There is no time stamp in this message. The
  receiving system is expected to provide the time stamp when this message is
  received." — Table 83 Note 1. Satellite providers therefore attach receive
  time, which can lag the fix by minutes (Chapter 39/47).
- Quote (Message 19): "For future equipment: this message is not needed and
  should not be used. All content is covered by Message 18, Messages 24A and
  24B." — A7-3.17.
- Quote (Message 24A): "Message 24 Part A may be used by any AIS station to
  associate a MMSI with a name." — A7-3.22. (So a Class A, base station or AtoN
  may send 24A; do not infer "Class B" from Message 24 alone.)
- Quote (off-position for fixed aids): "For a fixed aid, it denotes that
  internal GNSS position of the AtoN exceeds the zone parameter set on
  installation when the field value is 1, i.e. suspected GNSS anomaly." —
  Table 71. This is a built-in GNSS-interference detector (Chapter 62).
- **Edition drift in code tables.** M.1371-6 Table 51 fills the formerly
  reserved ship-type codes 1–19 (research vessel, icebreaker, cable layer, FPSO,
  crew boat …) and adds 38 trawler, 39 patrol vessel, 45/46 HSC passenger/ro-ro,
  65–67 cruise/ferry/excursion, 75–78 bulk/container/ro-ro/landing craft,
  85/86. Decoders and analytics code that map 1–19 to "reserved" will mislabel
  new equipment that sets AIS version 3. Chapter 22 and Appendix D must carry
  both the legacy and the -6 table.
- **EPFD code 9 = BDS (BeiDou)** and 12–15 (integrated PNT, inertial,
  terrestrial radio navigation, internal GNSS) exist in -6; gpsd's table ends at
  8 Galileo (verify whether gpsd 3.25 added 9–15).
- **The 1/10-min family.** Messages 17, 22, 23 and 27 and the ASM headers use
  18/17-bit positions in 1/10 arc-minute (≈185 m latitude resolution). Decoders
  disagree on whether to return degrees, minutes, or raw units (vectors 23, 30);
  Chapter 22 should specify "degrees" and Chapter 44 should flag this as a
  conformance item.
- **Class B CS comm state is a constant.** `1100000000000000110` decodes as
  sync state 3, slot increment 0, number of slots 3 (… "7 = 3 slots; offset +
  8 192"), keep flag 0 under the ITDMA interpretation — i.e. deliberately
  meaningless. A fingerprinting cue (Chapter 34): a "Class B" Message 18 whose
  comm state varies is an SO unit (or a spoofer).
- **gpsd's corpus is the de-facto shared regression set** for the open-source
  decoders (libais and pyais tests both reuse sentences from it, and gpsd
  credits Schwehr, Greene, Arundale and AISHub as data sources). Chapter 44
  should say so and link the BSD licence text.
- The gpsd document is at **version 1.58** (read 2026-10-05) and is still
  written against M.1371-4 ("Message type 27 is direct from [ITU1371]
  version 4"); it predates Message 28.

## Open questions / (verify)

- (verify) Which M.1371 edition first populated ship-type codes 1–19 and
  38/39/45/46/65–67/75–78/85/86: this session saw them in -6; confirm they are
  "reserved" in -5 Table 53 (gpsd's table suggests so).
- (verify) Message 7/13 exact layout in -6 (Table 54): four 30-bit MMSIs each
  followed by a 2-bit sequence number, total 72–168 bits — read the table.
- (verify) Message 27 position-latency bit polarity as named by pyais (`gnss`)
  vs libais (`gnss`): they disagree on vector 41; map each to Table 83.
- (verify) Inland DAC 200 FI 10 draught unit (1/100 m) against the CESNI/CCNR
  Inland AIS standard (Ed. 2.0 / ES-TRIN) — pyais 2.04 m vs libais 20.4 m.
- (verify) DAC 1 FI 22 duration units in pyais (20) vs libais (2 min) for
  vector 14 — one of them scales wrongly; check SN.1/Circ.289 Table for FI 22
  ("duration in minutes, 262143 = undefined").
- (verify) Whether gpsd ≥ 3.25 decodes EPFD 9–15, Message 28, and the 24B VDES
  bits; run `gpsdecode` on vectors 36 and 42 (not available in this venv).
- (verify) libais `vendor_id "1D00014"` vs pyais `vendorid "1D0", model 12,
  serial 199796` for vector 35: confirm the Table 78 split (18+4+20 bits) and
  that 12/199796 are the correct model/serial for those bits.
- (verify) M.1371-5 Message 24B had a 2-bit spare where -6 has "VDES
  capabilities" — confirm from the -5 PDF.
- (verify) Message 9 Table 60 complete field order (this session read only the
  key rows).
- (verify) Table 48 note: whether "Differential correction status" is taken
  from the GGA quality indicator or the RMC/GNS mode indicator in practice
  (IEC 61162-1 sentences named in the footnote).
- (verify) AIS version indicator semantics for value 1 ("M.1371-3") — did
  -4 equipment also report 1? gpsd says 1 = "ITU1371-1 … 1 = -3, 2 = -5".

## Candidate figures and worked examples

- **Figure 22-1: Message 1/2/3 bit map** (168 bits) with sentinels annotated
  (ROT −128, SOG 1023, lon 181°, lat 91°, COG 3600, HDG 511, ts 60–63). (App. C)
- **Figure 22-2: Message 5 bit map** (424 bits) with the two-slot boundary at
  bit 168 and the A/B/C/D reference-point diagram (Fig. 38 redrawn). (Ch. 22,
  App. C)
- **Figure 22-3: Message 18 vs 19 vs 24A/24B** — what moved where; the CS
  comm-state constant. (Ch. 20/22)
- **Figure 22-4: Message 21 (272–360 bits) vs Message 28 (168 bits).** (Ch. 68)
- **Figure 22-5: Message 27 (96 bits)** next to Message 1 to show the
  compression (28→18-bit lon, 10→6-bit SOG, no timestamp). (Ch. 39)
- **Figure 22-6: Binary container capacities** — Tables 53/56/80/82 as a bar
  chart of payload bits vs slots. (Ch. 23)
- **Worked example A — hand-decoding vector 1.** `15RTgt0P…`: '1' → 000001
  (type 1); next 2 bits repeat 0; 30 bits → 371798000; … → lon −123.395383°
  (−74 037 230 / 600 000); ROT byte 0x81 → −127 → "turning right? no: left >5°/30 s,
  no TI"; comm state 0b00 010 00010011100001 → sync 0, timeout 2, slot 1249.
  (Ch. 22 "On the wire")
- **Worked example B — ROT encode/decode.** 10°/min → 4.733·√10 = 14.97 → 15;
  decode 15 → (15/4.733)² = 10.04°/min; −126 → −(126/4.733)² = −708.7°/min
  (saturation); −127/+127 and −128 are *not* to be squared. (Ch. 22)
- **Worked example C — position resolution and range.** 1/10 000 min =
  0.1852 m (lat); 28-bit two's complement spans ±134 217 728 units = ±223.7°,
  so 181° (108 600 000) fits as the sentinel; Message 27's 1/10 min = 185.2 m.
  (Ch. 22/39)
- **Worked example D — ETA sentinels.** ETA bits month 0, day 0, hour 24,
  minute 60 → "not available" in every sub-field; month 5 day 15 hour 14 minute 0
  → "05-15 14:00 UTC" (vector 8, EVER DIADEM). (Ch. 22/47)
- **Worked example E — Message 16 rate.** Vector 22: offset 200, increment 0 →
  200 reports per 10 min → every 3 s (cross-check with `r-link-layer.md`
  rounding rules). (Ch. 21/22)
- **Worked example F — reading Message 4 "all n/a".** Vector 7: a base station
  with no UTC and no position (sync state 1 = UTC indirect, lon 181, lat 91) —
  a data-quality signature for Chapter 24/36.
- **Table 22-A: Sentinel register** — one row per field: width, unit, n/a
  value, "or higher" value, who may use it. (App. C)
- **Table 22-B: Code tables** — nav status; ship type (legacy vs -6); EPFD;
  AtoN type (Table 72) and Message 28 types 32–50 (from `r-standards-itu.md`);
  6-bit ASCII (Table 45). (App. D)
- **Try it:** run the 44 vectors through pyais and libais with
  `code/decode/compare_decoders.py` and diff against gpsd's `sample.aivdm.chk`.
  (Ch. 44, App. I)

## Recommended use by chapter

- **Ch. 20** — Table 44 M/B column: which station class may transmit which
  message; Message 19 deprecation; Message 24A "any station".
- **Ch. 22** — field tables and sentinels above (cite "M.1371-6 Annex 7 Table
  46/49/50/68/71/83"); ROT rules; timestamp 60–63; Table 48 PA logic; Message 5
  quirks (AIS version, IMO ranges, ETA sub-field sentinels, draught cap, DTE);
  Class B CS constant comm state; Message 21 off-position/virtual; Message 27
  compression; the 44-vector set with worked example A.
- **Ch. 23** — Message 6/8/25/26 containers and slot budgets (Tables 53/56/80/82);
  the 16-bit application identifier (hand-off to `r-asm.md`).
- **Ch. 24** — Message 4/11 UTC fields and sentinels; vector 7 as the "base
  station without UTC" example.
- **Ch. 25** — EPFD code table incl. BDS and 12–15; Table 48 RAIM logic; AtoN
  off-position as a GNSS-anomaly flag.
- **Ch. 26** — the vectors as NMEA framing examples (multi-sentence 5/17/21; fill
  bits 2/4; `!AIVDO` own-ship sentences; NAIS metadata suffixes in the libais
  typeexamples).
- **Ch. 34** — CS comm-state constant and Message 24B manufacturer ID
  (Table 78) as fingerprinting cues.
- **Ch. 36/47** — sentinels and defaults as error signatures (ROT 0 vs −128;
  heading 511; dims 0; ETA 00-00 24:60; name `@…@`; vector 43 out-of-range
  passthrough).
- **Ch. 39** — Message 27 fields, 3-min rate, no timestamp, latency bit, repeat
  indicator 3; vector 39 (168-bit nonstandard Message 27).
- **Ch. 44** — decoder-discrepancy table (ROT sentinels, 1/10-min scaling,
  Message 28 support, DAC/FI coverage, 15/16/20 sub-fields, Message 27
  polarity); gpsd corpus provenance and licence.
- **Ch. 60** — gpsd's malformed regression vectors as robustness tests.
- **Ch. 68** — Message 21 Table 72 types, dimension conventions, name extension,
  Message 14 on off-position; Message 28 (via `r-standards-itu.md`).
- **App. C/D** — all bit maps and code tables; the sentinel register.
