# Dossier: The AIS link layer — TDMA access schemes, slot map, synchronization, and link management

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the AIS data-link layer as specified in Recommendation ITU-R M.1371-6
(February 2026, in force): the frame/slot structure, the five channel-access
schemes (SOTDMA, ITDMA, RATDMA, FATDMA, MSSA) plus the Class B "CS" CSTDMA
scheme, the synchronization-state hierarchy, candidate-slot selection and
intentional slot reuse, the communication-state fields, and the link-management
messages (16, 20, 22, 23) with their assigned-mode and channel-management
behaviours. It feeds **Chapter 21** (link layer: TDMA and the slot map) as its
primary target, plus **Chapter 20** (station classes and access schemes),
**Chapter 24** (timing and sync hierarchy), **Chapter 28** (packet structure and
transmission timing), **Chapter 30** (loading, slot reuse, congestion),
**Chapter 61** (timing/network-disruption attacks: what Messages 16/22/23 can
and cannot command), **Chapter 69** (channel management and regional operating
areas), and **Appendix C** (communication-state bit layouts). Clause numbers
below use the M.1371-6 "A2-x.y.z" prefix form; earlier editions (M.1371-5 and
before) used the same numbering without the annex prefix (e.g., Annex 2 §3.3.4.2).

> Research-session note. Every fact marked *high* was read in the M.1371-6 PDF
> downloaded from itu.int and text-extracted during this session (`pdftotext`,
> 156 pages). Page numbers are the printed page numbers in the PDF. Facts from
> secondary sources (gpsd AIVDM document, IALA documents, Wikipedia, vendor pages)
> are marked as such. Nothing below was taken from memory without checking.

## Key questions

1. What is the frame/slot structure (slots per frame, slot duration, bits per
   slot, packet fields) and how do slot indices map to UTC?
2. What are the five access schemes in M.1371-6 Annex 2 (SOTDMA, ITDMA, RATDMA,
   FATDMA, MSSA), when is each used, and what parameters govern each?
3. How does SOTDMA select slots: nominal start slot (NSS), nominal slot (NS),
   nominal increment (NI), selection interval (SI), nominal transmission slot
   (NTS), slot time-out (3–7 frames), slot offset?
4. What exactly is in the SOTDMA and ITDMA communication states (sync state,
   slot time-out, sub-message; slot increment, number of slots, keep flag)?
5. What is the synchronization hierarchy (UTC direct → UTC indirect → base
   direct → base indirect → mobile as semaphore), and when does a station become
   a semaphore?
6. How does a station enter the network, operate continuously, change reporting
   interval, and leave/return from assigned mode?
7. What are the "slot state" definitions (free, internal, external, garbled) and
   the intentional-slot-reuse rules (candidate set of 4, 120 nmi rule, most
   distant station, base-station protection)?
8. What does Class B "CS" (CSTDMA) do differently (carrier-sense window,
   threshold, 10 candidate periods, no slot map)?
9. What can a base station command via Messages 16, 20, 22, 23: assignment of
   report rate or slots, FATDMA reservations, channel management and regional
   operating areas, group assignment and quiet time — and with what time-outs
   and limits?
10. What does the standard say about dual-channel alternation, long packets,
    RATDMA limits per frame, and repeater behaviour?
11. Which of these behaviours matter for security (Chapter 61) and for
    satellite/loading analyses (Chapters 30, 39)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Recommendation ITU-R M.1371-6 | 02/2026; approved 2026-02-19; in force | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Annex 2 (technical characteristics) §A2-3 link layer, §A2-4 network layer; Annex 6 Class B CS; Annex 7 messages 16/20/22/23; Table 44 access schemes per message | Free |
| ITU-R M.1371 landing page | editions -0 (1998) … -6 (2026) | https://www.itu.int/rec/R-REC-M.1371/en | Edition history; superseded PDFs also downloadable | Free |
| Recommendation ITU-R M.1371-5 (superseded) | 02/2014 | https://www.itu.int/rec/R-REC-M.1371-5-201402-S/en | Previous edition; Annex 2 clause numbers without "A2-" prefix; most decoders and papers cite this | Free |
| gpsd "AIVDM/AIVDO protocol decoding" (E. S. Raymond, with contributions incl. K. Schwehr) | living document; read 2026-10-05 | https://gpsd.gitlab.io/gpsd/AIVDM.html | Decoder-oriented description of communication-state fields ("radio status"), message layouts | Free |
| IALA Guideline G1082 *An Overview of AIS* | Ed. 2.0, June 2016 | https://www.navcen.uscg.gov/sites/default/files/pdf/IALA_Guideline_1082_An_Overview_of_AIS.pdf | Plain-language explanation of SOTDMA/ITDMA/RATDMA/FATDMA/CSTDMA, station types, AtoN types 1/2/3 | Free |
| IALA Recommendation R0124 (A-124) *The AIS Service* with Appendices | Ed. 2.2, 2012 (medium; see `r-standards-iala.md`) | iala.int (product pages) | Shore-side planning: App. 14 FATDMA planning, App. 17 channel management, App. 18 VDL load management (titles per `r-standards-iala.md`, medium) | Free (registration) |
| IALA Guidelines G1028/G1029 *AIS Volume 1 Parts I/II* | G1029 Ed. 1.1 (2002); legacy, no longer maintained | Listed at https://www.navcen.uscg.gov/ais-references | Historical IALA technical handbook; the PLAN's "G1029 (verify)" resolves to this legacy document | Historical |
| Report ITU-R M.2287 *Automatic identification system VHF data link loading* | edition/year (verify) | https://www.itu.int/pub/R-REP-M.2287 | VDL loading studies cited as related document by M.1371-6 | Free |
| Håkan Lans, US Patent 5,506,587 "Position indicating system" | granted 1996-04-09 (verify in `r-patents.md`) | https://patents.google.com/patent/US5506587A/en | STDMA origin; see `r-patents.md` for the family | Free |
| IEC 61993-2 (Class A test standard) | Ed. 3.0 (2018) (verify in `r-standards-iec.md`) | https://webstore.iec.ch/ | Tests of link-layer behaviour (slot selection, sync, assigned mode); not read this session | Paid |
| IEC 62287-1 (Class B CS test standard) | Ed. 3.0 (2017) (verify in `r-standards-iec.md`) | https://webstore.iec.ch/ | CSTDMA tests; not read this session | Paid |

## Verified facts

All clause references are to ITU-R M.1371-6 unless stated otherwise. "p." is the
printed page number of the PDF.

### Frame, slot, packet

| Fact | Source (clause/page) | Confidence |
|---|---|---|
| A frame equals one minute and is divided into 2 250 slots; access is given at slot start; frame start/stop coincide with the UTC minute when UTC is available | A2-3.1.2 (p. 18) | high |
| Each slot is identified by its index 0–2249; slot 0 is the start of the frame | A2-3.1.4 (p. 22) | high |
| Default packet is 256 bits = one slot: ramp-up 8, training sequence 24, start flag 8 (7Eh), data 168, CRC 16, end flag 8, buffer 24 | A2-3.2.2.2, A2-3.2.2.9 Table 12 (pp. 23–26) | high |
| Buffer (24 bits) budget: bit stuffing 4 bits (normally; not safety/binary messages), distance delay 14 bits, synchronization jitter 6 bits | A2-3.2.2.8 (p. 25) | high |
| 14-bit distance-delay buffer "is equivalent to 235.9 NM" and "provides protection for a propagation range of over 120 NM" | A2-3.2.2.8.2 and footnote 4 (p. 25) | high |
| Statistical argument for 4 stuffing bits: 76 % of fixed-length-message bit combinations need ≤3 stuffing bits | A2-3.2.2.8.1 (p. 25) | high |
| Synchronization jitter: mobile transmission timing error within 104 µs of sync source, accumulated up to 312 µs (3 bits); base station within 52 µs, accumulated 104 µs | A2-3.2.2.8.3 (p. 25) | high |
| Transmission timing events (one slot): T0 0.000 ms slot start/RF on; TTS 0.833 ms training starts; T1 1.000 ms RF stable; T2 3.333 ms start flag; Ts 4.167 ms end of start flag = slot-phase-sync marker; T3 24.167 ms end of transmission (zero stuffing); T4 = T3 + 1.0 ms RF power zero; T5 26.667 ms end of slot | A2-3.2.2.10 Fig. 8 table (pp. 26–27) | high |
| Long transmission packets: at most five consecutive slots per continuous transmission; a single overhead (ramp, training, flags, FCS, buffer); no filler | A2-3.2.2.11 (p. 27) | high |
| Bit stuffing: after five consecutive 1s insert a 0, applied to data + FCS between flags; preamble and flags are not stuffed | A2-3.2.2.1, A2-3.2.2.3, A2-3.2.2.4 (pp. 23–24) | high |
| HDLC per ISO/IEC 13239:2002; I-packets with control field omitted; CRC-16 preset to ones over data only; "CRC errors should result in no further action by the AIS station" | A2-3.2.2, A2-3.2.2.6, A2-3.2.3 (pp. 23–27) | high |
| Bit ordering: message tables are MSB-first per field; on the VDL data is grouped into 8-bit bytes and each byte is output LSB first; unused bits of the last byte are zero | A2-3.3.7 and Table 17 example (pp. 46–47) | high |
| The TDMA *receiving* process "should not be synchronized to slot boundaries" (receivers must accept packets at any time offset) | A2-3.1.1 (p. 17) | high |

### Slot state and candidate slots

| Fact | Source | Confidence |
|---|---|---|
| Slot states: **Free** (unused in own receiving range; slots reserved by a station beyond 120 nmi are also free; SOTDMA-reserved slots unused for the preceding three frames are free), **Internal allocation**, **External allocation**, **Garbled** (no decodable message and RSSI > 16 dB above background; only distinguished from Free in repeaters) | A2-3.1.6 (p. 23) | high |
| At least four candidate slots in the selection interval unless restricted by loss of position; candidates primarily from free slots, then "available" (externally allocated but reusable) slots; any candidate equally probable | A2-3.3.1.2 (pp. 27–28) | high |
| For multi-slot messages a candidate must be the first slot of a consecutive block of free/available slots; Class B SO candidates for Messages 6/8/12/14 must be free | A2-3.3.1.2 (p. 27–28) | high |
| Adjacent-slot rule: because channel switching takes time (<25 ms, A2-2.11.1), the two slots adjacent to an own-station slot on one channel are not candidates on the other channel | A2-3.3.1.2 (p. 28) | high |
| Intentional slot reuse: only when own position is available; top the candidate set up to 4 using slots of the **most distant** station(s) within the SI; never reuse slots of stations reporting no position; never reuse base-station slots unless the base is >120 nmi away; a station reused once is excluded from further reuse for one frame | A2-4.4.1 (p. 55) | high |
| Reuse priority rules: Rule 1 free on selection channel & available on other; Rule 2 available/free; Rule 3 available/available; Rule 4 free/unavailable; Rule 5 available/unavailable; "Unavailable" = externally allocated and not reusable (e.g., base station within 120 nmi, station without position) | A2-4.4.1 Rules 1–5 and footnotes (pp. 55–56) | high |
| Fig. 20 example legend: F free; I internal; E external (available 2); B base station within 120 nmi or mobile without position (unavailable); T station under way not received for ≥3 min (free 2); D most-distant mobile within 120 nmi (available 1); priorities 1,2,5,6,3,4,7,8; combinations 9–12 forbidden (adjacent-slot, opposite-channel, base-station rules) | A2-4.4.1 Fig. 20 (p. 56) | high |

### Access schemes (Annex 2 §A2-3.3.4)

| Fact | Source | Confidence |
|---|---|---|
| Five access schemes: SOTDMA, ITDMA, RATDMA, MSSA and FATDMA; SOTDMA is the basic scheme for scheduled repetitive transmissions from an autonomous station | A2-3.3.1 (p. 27) | high |
| Schemes "operate continuously, and in parallel, on the same physical data link" | A2-3.3.1.1 (p. 27) | high |
| Four modes of operation: autonomous (default), assigned, polled, silent; simplex repeater has only autonomous and assigned. Footnote 5 cites IMO A.1106(29): AIS should always be in operation under way or at anchor unless the master believes it compromises safety/security | A2-3.3.2 and footnote 5 (pp. 29–30) | high |
| Initialization: monitor the TDMA channels for one minute, build a dynamic directory and frame map, then enter the network | A2-3.3.3, A2-3.3.5.1 (pp. 30, 38) | high |
| **ITDMA** used on four occasions: network entry; temporary changes/transitions of reporting interval; pre-announcement of safety-related messages; periodic transmissions with a report rate of less than two per minute. Parameters: LME.ITINC slot increment 0–8 191; LME.ITSL 1–5 slots; LME.ITKP keep flag | A2-3.3.4.1, Table 13 (pp. 30–31) | high |
| **RATDMA** uses a p-persistent algorithm; "An AIS station should avoid using RATDMA"; SI for RATDMA is 150 slots (4 s); start probability LME.RTPS = 100/LME.RTCSC (max 25 with 4 candidates); increment LME.RTPI = (100 − LME.RTP2)/LME.RTCSC; candidate counter LME.RTCSC 1–150; attempts LME.RTA 0–149; if RTCSC + RTA < 4 the candidate set is replenished | A2-3.3.4.2, Table 14 (pp. 31–33) | high |
| **FATDMA** reservations are made by base stations only, pre-configured by the competent authority; need Message 4 + Message 20 with the same MMSI; apply within 120 nmi; beyond 120 nmi all stations may treat the slots as free; a Message 20 without a Message 4 should be ignored; base stations may reuse FATDMA slots for their own FATDMA but not for RATDMA. Parameters: LME.FTST start slot 0–2 249; LME.FTI increment 0–1 125; LME.FTBS block size 1–5 | A2-3.3.4.3, Table 15 (pp. 33–34) | high |
| **SOTDMA** parameters (Table 16): NSS nominal start slot; NS = NSS + n·NI (one channel) or NSA = NSSA + n·2·NI, NSB = NSSA + NI + n·2·NI (two channels, 0 ≤ n < 0.5 Rr); **NI = 2 250/Rr**, range 75–1 225 (37.5 in assigned report-rate mode; 45 in assigned slot-increment mode); Rr = 60/RI, range 2–30 (60 in assigned mode); **SI = NS − 0.1·NI to NS + 0.1·NI** (width 0.2·NI); NTS; TMO_MIN 3 frames; TMO_MAX 7 frames | A2-3.3.4.4.2, Table 16 and notes (pp. 35–36) | high |
| Network entry: first transmission of a Class A is Message 3; NSS randomly chosen between current slot and NI slots forward; NTS randomly chosen among candidates in the SI and given a random time-out in [TMO_MIN, TMO_MAX]; first-frame phase uses ITDMA with keep flag, ending when increment is set to zero | A2-3.3.5.2–A2-3.3.5.3 (pp. 38–41) | high |
| Continuous operation: at each NTS decrement slot time-out; when zero, pick a new NTS in the SI, **slot offset = NTSnew − NTScurrent + 2 250**, assign a new random time-out 3–7; otherwise slot offset = 0 | A2-3.3.5.4 (pp. 41–43) | high |
| Changing reporting interval: procedure for changes persisting ≥2 frames; temporary changes use ITDMA inserted between SOTDMA transmissions; the station converts the current slot to an ITDMA transmission carrying the offset and keep flag | A2-3.3.5.5 (pp. 43–45) | high |
| **MSSA** (multi-channel slot selection access) is used only for Message 27 on channels 75/76 (see Annex 3 and `r-standards-itu.md`) | Table 44 row 27; A3 | high |

### Communication state (Annex 2 §A2-3.3.7)

| Fact | Source | Confidence |
|---|---|---|
| Source ID = 30-bit MMSI; numbers ≤ 999 999 999 only; the M.1080 tenth digit is not implemented | A2-3.3.7.2.1 (p. 48) | high |
| SOTDMA communication state (19 bits): sync state 2 bits (0 UTC direct, 1 UTC indirect, 2 base direct, 3 "synchronized to another station based on the highest number of received stations or to another mobile station which is directly synchronized to a base station"); slot time-out 3 bits (0 = last transmission in this slot; 1–7 frames remaining); sub-message 14 bits | Table 18 (p. 48) | high |
| Sub-message by slot time-out: 3, 5, 7 → received stations (0–16 383); 2, 4, 6 → slot number (0–2 249); 1 → UTC hour (bits 13–9) and minute (bits 8–2), bits 1–0 unused; 0 → slot offset (0 = de-allocate after transmission) | Table 19 (p. 48) | high |
| "The SOTDMA communication state should apply only to the slot in the channel where the relevant transmission occurs" | A2-3.3.7.2.2 (p. 48) | high |
| ITDMA communication state (19 bits): sync state 2; slot increment 13 (0 = no more transmissions); number of slots 3 (0–4 → 1–5 slots; 5–7 → 1–3 slots with offset = increment + 8 192, "removes the need for RATDMA broadcast for scheduled transmissions up to 6 min intervals"); keep flag 1 | Table 20 (pp. 49–50) | high |
| RATDMA and FATDMA have no scheme-specific communication state; a message with a comm state may be sent by RATDMA at network entry or when repeating | A2-3.3.7.4–A2-3.3.7.5 (p. 50) | high |

### Synchronization hierarchy (Annex 2 §A2-3.1)

| Fact | Source | Confidence |
|---|---|---|
| MAC.SyncBaseRate: base station increases Message 4 rate to once per 3⅓ s when semaphore-qualified; MAC.SyncMobileRate: mobile semaphore reports once per 2 s; both revert after qualifying conditions have been invalid for 3 min | Table 8; A2-3.1.3.3.1–A2-3.1.3.3.2 (pp. 17, 19) | high |
| Priority of sync sources: internal UTC (UTC direct); then a station with UTC time; a semaphore-qualified base station; other stations synchronized to a base station; a semaphore-qualified mobile | A2-3.1.3.4.3 (p. 20) | high |
| Table 9: UTC direct (priority 1, sync state 0, usable as indirect source); UTC indirect (2, state 1, not a source); Base direct (3, state 2, usable); Base indirect (4, state 3, not a source); Mobile as semaphore (5, state 3, not a source). "Only one level of UTC indirect synchronization is allowed"; "Only one level of indirect access to the base station is allowed" | Table 9; A2-3.1.1.2–A2-3.1.1.3 (pp. 18, 21) | high |
| Base-station sync: choose the base indicating the highest number of received stations, provided two reports were received from it in the last 40 s; drop it if fewer than two in the last 40 s; ties → lowest MMSI | A2-3.1.1.3 (p. 18) | high |
| Mobile semaphore: when no UTC and no base is receivable, synchronize to the station indicating the highest number of received stations over the last nine frames (two reports in last 40 s); ties → lowest MMSI; that station "becomes the semaphore" | A2-3.1.1.4 (p. 18) | high |
| Semaphore qualification tables: a mobile qualifies only if its own sync state is 1 or 3 **and** the highest received sync state (excluding its own sync source) is 3 (Table 10); a base qualifies if its own state is 1, 2 or 3 and highest received is 2 or 3 (Table 11). Class B SO and SAR aircraft shall not act as semaphore | Tables 10–11; A2-3.1.3.3.2 (pp. 19–22) | high |
| Slot-phase sync decision is taken after end flag + valid FCS (state T3); frame sync adopts the received slot number from a sub-message with slot time-out 2/4/6 | A2-3.1.3.1–A2-3.1.3.2 (pp. 18–19) | high |

### Assigned mode and base-station control (Annex 2 §A2-3.3.6, §A2-4; Annex 7)

| Fact | Source | Confidence |
|---|---|---|
| Assigned mode is entered by Message 16 or 23; affects only position-report transmissions; non-Class-A mobiles follow the assignment and do not change interval for course/speed; Class A uses the assigned or autonomous interval, **whichever is shorter**, and sends Message 2 instead of Message 1; "Two levels of assignments are possible"; last assignment overwrites | A2-3.3.6 (p. 45) | high |
| Assigned slots use the SOTDMA comm state with time-out 3–7; return to autonomous when time-out reaches zero, re-entering via the network-entry procedure | A2-3.3.6.2.2–A2-3.3.6.2.3 (pp. 45–46) | high |
| Message 16 assignment is tagged with a random time-out of 4–8 min after first transmission; slot assignments alternate between channels with the start slot on the channel carrying Message 16; the base must re-issue before the last frame of the previous assignment to continue | A7-3.14 (p. 124) | high |
| Message 16 layout: ID 6, repeat 2, source 30, spare 2, destination A 30, offset A 12, increment A 10, [destination B 30, offset B 12, increment B 10], spare 0/4; 96 or 144 bits. Increment 0 means report-rate assignment with offset = reports per 10 min (multiples of 20 between 20 and 600; round up; cap 600). Increment codes: 1 = 1 125 slots, 2 = 375, 3 = 225, 4 = 125, 5 = 75, 6 = 45, 7 = undefined (ignore). Class B shall not be assigned < 2 s | Table 65 and text (pp. 125) | high |
| A base station may assign Rr to all mobiles except Class A to resolve congestion; for Class A it may redirect slots into FATDMA-reserved slots | A2-4.4.2 (p. 57) | high |
| Message 20: base stations only; mobiles within 120 nmi reserve the slots until time-out; up to four reservation blocks each with offset 12 bits, number of slots 4 bits (1–15 in the field, but "reservation block should not exceed 5 slots"), time-out 3 bits (minutes), increment 11 bits (0 = once per frame; recommended values 2, 3, 5, 6, 9, 10, 15, 18, 25, 30, 45, 50, 75, 90, 125, 150, 225, 250, 375, 450, 750, 1125); applies only to the channel it is transmitted on; 72–160 bits | A7-3.18, Table 70, footnote 20 (pp. 130–132) | high |
| Message 22 (168 bits): channel A 12 bits (AIS 1 = 2087), channel B 12 bits (AIS 2 = 2088), Tx/Rx mode 4 bits, power 1 bit (0 high default), NE corner lon 18/lat 17 in 1/10 min, SW corner lon 18/lat 17 (or two addressed MMSIs packed into those fields), addressed/broadcast 1 bit, channel A/B bandwidth 1+1 (always 25 kHz), transitional zone size 3 (always default), spare 23; must be accompanied by Message 4 for evaluation within 120 nmi | A7-3.20, Table 73 (pp. 136–137) | high |
| Regional operating areas are Mercator rectangles defined by NE and SW corners (WGS-84, 1/10 min); areas must be fully covered by Message 22 from at least one base station | A2-4.1.3 (p. 51) | high |
| Mobile keeps **eight** regional operating settings; erase any whose nearest boundary is >500 nmi away or older than 24 h; reject PI (presentation-interface) inputs that overlap a Message-22 region received within the last 2 h; an addressed Message 22 is accepted only when the station is inside a stored region; settings cannot be cleared except by inputting a new setting | A2-4.1.6 (pp. 52–53) | high |
| Message 23 (160 bits): NE/SW corners; station type 4 bits (0 all mobiles, 1 Class A, 2 all Class B, 3 SAR aircraft, 4 Class B SO, 5 Class B CS, 6 inland waterways, 7–9 regional, 10 base-station coverage area for Message 27 control, 11–15 future); ship/cargo type 8 bits; Tx/Rx mode 2 bits (0 both, 1 TxA only, 2 TxB only); reporting interval 4 bits per Table 75 (0 autonomous, 1 10 min, 2 6 min, 3 3 min, 4 1 min, 5 30 s, 6 15 s, 7 10 s, 8 5 s, 9 next shorter, 10 next longer, 11 2 s not for Class B); **quiet time 4 bits (0 none; 1–15 min)** | A7-3.21, Tables 74–75 (pp. 137–139) | high |
| Station type 10 (base-station coverage area) is relevant for 3 min after the last Message 4 from the same base MMSI | A7-3.21 (p. 137) | high |
| Class B CS assigned mode (via Message 23): time-out random 4–8 min; first assigned-rate report at a random time to avoid clustering; during quiet time the station keeps scheduling but does not transmit Messages 18/24, still answers interrogations, may still send safety messages; subsequent quiet-time commands during a quiet time are ignored; quiet time overrides a rate command | A6-4.3.3.3.2 and footnote 13 (pp. 94–95) | high |
| Message 15 interrogation: responses on the channel of the interrogation; mobile interrogators must set slot offset 0; only base stations may assign a reply slot; mobile must handle a minimum offset of 10 slots; 88–160 bits; Table 63 shows which messages each station type must answer (Class A: 3, 5, 24; Class B: 18, 24; SAR aircraft: 9, 24; AtoN: 21; base: 4, 24) | A7-3.13, Tables 63–64 (pp. 122–124) | high |

### Dual-channel, priorities, repeaters

| Fact | Source | Confidence |
|---|---|---|
| Default multi-channel mode: receive AIS 1 and AIS 2 in parallel; channel access performed independently per channel; periodic messages alternate channels transmission-by-transmission; responses/acks on the channel of the initial message; addressed messages on the channel the addressee was last heard on; other non-periodic messages alternate | A2-4.1.2; Table 44 note 6 (pp. 51, 103) | high |
| Four priority levels, 1 highest; same priority served FIFO; e.g., position reports 1, safety messages 2, interrogation/UTC 3, static/binary 4 | A2-4.2.3; Table 44 (pp. 53, 101–102) | high |
| RATDMA limit: Messages 6, 8, 12, 14, 25 from a mobile ≤20 slots per frame, ≤3 consecutive slots per message (≤5 with FATDMA reservations) | Table 44 note 10 (p. 103) | high |
| Repeat indicator: mobiles always 0; repeaters increment; a message with repeat indicator 3 is not retransmitted; number of repeats configured as 1 or 2; a base station transmitting on behalf of another MMSI (e.g., virtual AtoN) sets a non-zero repeat indicator | A2-4.6.1 (p. 58) | high |
| Repeaters are store-and-forward (not real time), retransmit on the same channel, and should use RSSI to help slot selection | A2-4.6.2 (pp. 58–59) | high |

### Class B "CS" CSTDMA (Annex 6)

| Fact | Source | Confidence |
|---|---|---|
| Class B CS synchronizes its time periods to received Messages 1, 2, 3, 4, 18 with repeat indicator 0 (sync mode 1), jitter ≤ ±3 bits (±312 µs) from the rolling-60 s average; falls back to internal timing (sync mode 2) 30 s after losing those sources; base-station reservations still respected | A6-4.3.1.1 (pp. 85–86) | high |
| Carrier-sense window 1 146 µs from 833 µs to 1 979 µs after T0; packet transmission starts 20 bits (TA = 2 083 µs) after T0 | A6-4.3.1.2 (p. 87) | high |
| CS threshold = minimum background over rolling 60 s + 10 dB per Rx channel; floor −107 dBm; tracked ≥30 dB → max −77 dBm; example implementation: >1 kHz sampling, 20 ms sliding average, 4 s minima, 15-interval history | A6-4.3.1.3 and footnote 11 (p. 87) | high |
| CS VDL states: FREE, USED, UNAVAILABLE (reserved by base via Message 20 "regardless of their range") | A6-4.3.1.5 (pp. 88–89) | high |
| CSTDMA algorithm: TI = RI/3 or 10 s whichever is less, centred on NTT; randomly define **10 candidate periods** in TI; transmit in the first that is free; abandon if all 10 are used | A6-4.3.3.1, Table 41 (p. 93) | high |
| Unscheduled Class B CS transmissions get an NTT within 25 s; Message 13 ack (if Message 12 supported) with up to 3 retries; interrogation reply within 30 s with one retry after 30 s | A6-4.3.3.2–A6-4.3.3.3.3 (pp. 94–95) | high |
| Class B CS init: monitor one minute to synchronize and set the CS threshold; first transmission is Message 18 | A6-4.3.3.4 (p. 95) | high |
| CS Tx timing (Table 37): TA 20 bits/2 083 µs; TB1 23 bits/2 396 µs; TB2 25 bits/2 604 µs; TE 248 bits/25 833 µs; TF 251 bits/26 146 µs | Table 37 (p. 88) | high |

### Secondary-source cross-checks

| Fact | Source | Confidence |
|---|---|---|
| gpsd's AIVDM document describes the 19-bit "radio status" field of Messages 1–3 and 18 and distinguishes SOTDMA vs ITDMA layouts; Message 3 and Message 18 (when the comm-state selector bit = 1) carry ITDMA state | https://gpsd.gitlab.io/gpsd/AIVDM.html (read 2026-10-05) | medium (decoder documentation, not the standard) |
| IALA G1082 explains the three AtoN station types: Type 1 no receiver (FATDMA slots reserved by a base station); Type 2 receiver for configuration only; Type 3 full receive capability | G1082 Ed. 2.0 via `r-standards-iala.md` | high (for G1082 content) |

## Notes and quotes

- **The link layer is a three-sub-layer stack.** M.1371-6 Annex 2 §A2-3 is
  organized as MAC (sub-layer 1: time, slots, sync), DLS (sub-layer 2: HDLC
  framing, CRC) and LME (sub-layer 3: access schemes, modes, slot selection),
  with §A2-4 "network layer" holding multi-channel operation, regional operating
  areas, priorities, congestion resolution, base-station and repeater duties, and
  §A2-5 "transport layer" holding packet sizing and sequencing. Chapter 21 should
  mirror this structure so clause citations line up.
- Quote (why candidates and time-outs exist): "The purpose of intentionally
  reusing slots and maintaining a minimum of four candidate slots within the same
  probability of being used for transmission is to provide high probability of
  access to the link. To further provide high probability of access, time-out
  characteristics are applied to the use of the slots so that slots will
  continuously become available for new use." — M.1371-6 A2-3.3.1.2, p. 28.
- Quote (RATDMA is discouraged): "An AIS station should avoid using RATDMA. A
  scheduled message should primarily be used to announce a future transmission to
  avoid RATDMA transmissions." — A2-3.3.4.2.1, p. 31.
- Quote (CRC): "CRC errors should result in no further action by the AIS
  station." — A2-3.2.3, p. 27. (Shore/satellite processors are not "AIS stations"
  in this sense; see Chapter 30.)
- Quote (silent mode footnote): "IMO Resolution A.1106 (29) states that AIS should
  always be in operation when a ship is underway or at anchor; unless the master
  believes its continual operation might compromise the safety or security of the
  ship." — footnote 5 to A2-3.3.2.4, p. 30.
- Quote (Class A precedence in assigned mode): "If the autonomous mode requires a
  shorter reporting interval than that directed by Message 16 or 23, the Class A
  AIS station should use the reporting interval of the autonomous mode." —
  A2-3.3.6, p. 45. This is the single most important fact for Chapter 61: a
  base station (or an impostor) **cannot slow a Class A below its autonomous
  rate**; it can only slow Class B/SAR/AtoN stations, impose a quiet time on
  Class B CS, or push Class A into particular slots.
- Quote (Message 20 integrity): "A data link management message (Message 20)
  without a base station report (Message 4) should be ignored." — A2-3.3.4.3.1,
  p. 34. Also footnote 20: the mobile needs Message 4 "so that it can determine
  its distance from the transmitting base station" (the 120 nmi test).
- **Regional operating settings are sticky but bounded.** Eight memories; erased
  at >500 nmi or >24 h; a Message 22 received from a base station blocks
  overlapping PI inputs for two hours; and nothing but a new setting can clear
  them (A2-4.1.6). This bounds the persistence of any channel-management abuse
  (Chapter 61) to about a day or ~500 nmi of travel.
- **Message 23 quiet time is the only "stop transmitting" command in the
  protocol,** and it applies to Class B CS position/static reports (A6-4.3.3.3.2)
  and, via assigned mode, to other non-Class-A mobiles. The Class A clause
  (A2-3.3.6) is silent on quiet time for Class A; the IEC 61993-2 test standard
  governs what Class A equipment actually does with it — (verify) in
  `r-standards-iec.md` / `r-timing-attacks.md`.
- **CSTDMA has no slot map.** A Class B CS unit does not maintain the frame map,
  does not read communication states, and reserves nothing; it listens for ~1.1 ms
  at the start of a slot and transmits if the channel is quiet. Its only
  concession to the base station is that Message 20 reservations are
  UNAVAILABLE "regardless of their range" (A6-4.3.1.5) — stricter than the 120 nmi
  rule for Class A.
- The PLAN's "1,111-bit window (verify)" for CSTDMA is wrong as written: the
  window is **1 146 µs** (about 11 bit periods at 9 600 bit/s), from bit 8 to
  bit 19 of the slot.
- **Where "slot" is called "time period".** Annex 6 consistently says "time
  period" rather than "slot" for Class B CS because the station does not
  participate in the slot map; chapters should note this vocabulary.
- gpsd's document uses the term "radio status" for the communication state and
  was written against M.1371-3/-4; it remains a good decoder-side explanation but
  must not be cited for normative rules.

## Open questions / (verify)

- (verify) What does IEC 61993-2 (Class A) require on receipt of Message 23 quiet
  time, Message 22 with an addressed Tx/Rx mode, and Message 16 with an
  unreasonable assignment? M.1371-6 A2-3.3.6 covers Class A assignment but the
  quiet-time behaviour for Class A is not stated in the clauses read.
- (verify) IEC 62287-1 test cases for the CS detection threshold and the 10
  candidate periods; whether any published measurements show CS units
  transmitting into occupied slots under heavy load (Chapter 30 "Class B
  starvation").
- (verify) Edition and year of Report ITU-R M.2287 (VDL loading) and whether it
  contains empirical slot-occupancy figures usable in Chapter 30.
- (verify) Clause-level diff of Annex 2 §3 between M.1371-5 and -6: this session
  read only -6; prior literature cites -5 numbers (e.g., "Annex 2 §3.3.4.2"). A
  spot check suggests the text is unchanged apart from prefixing, but the Table
  16 footnote values (37.5/45 for assigned NI) and the Class B SO candidate rule
  should be confirmed in -5.
- (verify) IALA R0124 App. 14 (FATDMA planning) and App. 18 (VDL load
  management) contents — titles are from search summaries in `r-standards-iala.md`;
  open the PDFs to extract their planning rules (e.g., recommended FATDMA
  budget per base station).
- (verify) Whether any open-source SOTDMA simulator beyond the repo's own
  `code/tdma/sotdma_sim.py` exists with a citable publication (candidate
  literature search terms: "SOTDMA simulation AIS slot collision"; none
  confirmed this session). The PLAN's "Gaugue? (verify)" was not resolved.
- (verify) Lans US 5,506,587 grant date and claims mapping to NSS/NI/time-out
  concepts — defer to `r-patents.md`.
- (verify) Historical: did M.1371-0 (1998) already contain the 120 nmi reuse
  rule and the 3–7 frame time-out, or were these tuned in -1/-2? Obtain the -0
  PDF from the ITU landing page.

## Candidate figures and worked examples

- **Figure 21-1: The frame.** 2 250 slots per minute per channel; two channels
  → 4 500 slot opportunities per minute; mark slot 0 at the UTC minute. (Ch. 21)
- **Figure 21-2: One slot in time.** T0 0 ms, TTS 0.833, T1 1.0, T2 3.333,
  Ts 4.167, T3 24.167, T4 25.167, T5 26.667 ms, overlaid on the 256-bit packet
  layout. (Ch. 21/28)
- **Figure 21-3: SOTDMA geometry.** NSS, NS = NSS + n·NI, SI = ±0.1·NI, NTS
  chosen inside SI; two-channel variant with NSSB = NSSA + NI. (Ch. 21)
- **Figure 21-4: Slot time-out life cycle.** A slot reserved with time-out 5
  counting down each frame, then slot offset announcing the move. (Ch. 21)
- **Figure 21-5: Sync-state hierarchy** from Table 9 (five levels, which may be
  used as source). (Ch. 21/24)
- **Figure 21-6: Candidate-slot/reuse decision flow** from Rules 1–5 and Fig. 20
  legend. (Ch. 21/30)
- **Figure 21-7: CSTDMA timing.** CS window 833–1 979 µs, TA at 2 083 µs,
  TE/TF; and the 10 candidate periods inside TI. (Ch. 21/20)
- **Figure 21-8: Communication-state bit maps** for SOTDMA (2+3+14) and ITDMA
  (2+13+3+1). (Ch. 21, App. C)
- **Worked example A — nominal increment.** Class A at 10 s: Rr = 6 → NI = 375
  slots; SI = ±37 slots (0.1·NI = 37.5, implementations truncate/round — note
  the standard gives the formula, not the rounding). At 2 s: Rr = 30 → NI = 75;
  SI = ±7.5 slots. At 3 min (Rr = ⅓ < 2): ITDMA is used instead (Table 16
  note 2). (Ch. 21)
- **Worked example B — slot offset arithmetic.** Current NTS = 2 200, new
  NTS = 50 in the next frame: slot offset = 50 − 2 200 + 2 250 = 100; a
  receiver adds 100 to the current slot modulo 2 250 to mark slot 50. (Ch. 21)
- **Worked example C — reading a comm state.** Slot time-out 3 → sub-message is
  "received stations"; a value of 42 means the transmitter hears 42 other
  stations — a free proxy for local density usable in Chapter 30/48 analytics.
  Slot time-out 1 → sub-message is UTC hour/minute (bits 13–9 hour, 8–2 minute).
- **Worked example D — RATDMA p-persistence.** Four candidates: RTPS = 25 %. If
  the first draw fails, RTP2 += (100 − 25)/4 = 18.75 → 43.75 %, and so on; the
  transmission is guaranteed by the fourth candidate if RTCSC stays 4 (the
  increments reach 100 %). (Ch. 21/30)
- **Worked example E — Message 16 rate assignment.** Offset = 120, increment =
  0 → 120 reports per 10 min = one per 5 s; offset = 130 is rounded up to 140;
  offset = 700 is capped at 600 (one per second) — but a Class B may not be
  assigned < 2 s, and a Class A will not go slower than its autonomous rate.
  (Ch. 21/61)
- **Worked example F — Message 20 reservation.** Offset 10, slots 2, time-out 5
  min, increment 375 → six two-slot blocks per frame beginning 10 slots after the
  Message 20 slot; mobiles within 120 nmi of the base treat them as unavailable
  until 5 min after the last refresh. (Ch. 21)
- **Worked example G — regional area persistence.** A ship receives a Message
  22 at 12:00 in a 60 × 60 nmi region; at 15 kn it would need >33 h to be
  500 nmi from the boundary, so the 24 h rule erases it first at 12:00 next
  day (unless refreshed). (Ch. 21/61/69)
- **Table 21-A: Which access scheme for which message** (from Table 44) —
  Message → priority → access schemes → comm state → M/B. (Ch. 21/22, App. C)

## Recommended use by chapter

- **Ch. 20 (station classes)** — Table 44 access-scheme column per message;
  Class B SO vs CS (SOTDMA with Annex 2 vs CSTDMA with Annex 6); AtoN Type 1
  FATDMA from G1082; semaphore exclusion of Class B SO and SAR aircraft.
- **Ch. 21 (link layer)** — the backbone of this dossier: frame/slot/packet
  (A2-3.1.2, Table 12, Fig. 8 timings); slot states (A2-3.1.6); candidate slots
  and the adjacent-slot rule (A2-3.3.1.2); the five access schemes with Tables
  13–16; network entry and continuous operation (A2-3.3.5); comm states (Tables
  18–20); intentional slot reuse (A2-4.4.1); CSTDMA (A6-4.3). Use worked examples
  A–D and figures 21-1…21-8. Correct the PLAN's "1,111-bit window" to 1 146 µs.
- **Ch. 22 (messages)** — bit ordering rule (A2-3.3.7, Table 17); comm-state
  layouts for Messages 1/2/3/4/9/11/18/26; Message 15/16/20/22/23 field tables.
- **Ch. 24 (timing)** — sync hierarchy Tables 8–11; 104/312 µs and 52/104 µs
  jitter budgets; semaphore rules; slot-phase vs frame sync; Class B CS sync
  modes 1/2 and the 30 s hold.
- **Ch. 28 (PHY)** — Fig. 8 timing table; packet overhead; long packets ≤5 slots;
  Class B CS Table 37.
- **Ch. 30 (loading)** — 120 nmi rule and distance-delay buffer (235.9 nmi);
  reuse of the most distant station's slots; "received stations" sub-message as
  density proxy; RATDMA 20-slot/3-slot limits; Class B CS 10-candidate abandonment;
  Report ITU-R M.2287 pointer.
- **Ch. 39 (satellite)** — MSSA for Message 27; station type 10 in Message 23 and
  the 3 min Message 4 window for base-station coverage.
- **Ch. 61 (timing/network attacks)** — bounded reach of Messages 16/22/23
  (4–8 min assignment time-out; 24 h/500 nmi regional erasure; Class A never
  slower than autonomous; Message 20 ignored without Message 4; eight regional
  memories); quiet time as the only "stop" command and its Class B CS semantics.
- **Ch. 69 (channels)** — Message 22 channel fields (2087/2088), Tx/Rx modes,
  regional operating areas; A2-4.1.1 list of the four worldwide AIS frequencies.
- **App. C** — communication-state bit maps; Message 15/16/20/22/23 tables.
- **App. D** — Message 23 station-type and reporting-interval codes; Message 16
  increment codes; Message 20 recommended increments.
