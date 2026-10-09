# Dossier: AIS RF physical layer — GMSK parameters, framing, CRC, timing masks, power classes, receiver requirements, and the channel plan

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about the AIS physical layer and the parts of the data-link layer that are
visible "on the wire" (packet framing, bit stuffing, CRC, transmission timing),
as specified in Recommendation ITU-R M.1371-6 (02/2026) Annex 2 §A2-2 and
§A2-3.2, Annex 3 (long-range Message 27), Annex 6 (Class B "CS"), and Annex 8
(burst transmitters: AIS-SART, MOB-AIS, EPIRB-AIS), together with the VHF
maritime channel plan in ITU Radio Regulations Appendix 18 (Edition of 2020,
Rev. WRC-19). It is the primary dossier for **Chapter 28** (AIS RF encoding and
the physical layer) and feeds **Chapter 27** (RF basics: sensitivity, noise
floor, link budget inputs), **Chapter 20** (power classes by station type),
**Chapter 21** (slot timing, buffer bits), **Chapter 30** (what survives
corruption: no FEC, CRC-only), **Chapter 33** (SDR receive: BT, bit rate,
frequency tolerance), **Chapter 34** (RF fingerprinting features: ramp
timing, frequency error, modulation accuracy), **Chapter 69** (channel
plan: 75/76, ASM 1/2, VDE, DSC 70), and **Appendix B/C/I**.

> Research-session note. Every fact marked *high* was read in the text extracted
> from the M.1371-6 PDF downloaded from itu.int (page numbers are printed page
> numbers), or from the RR 2020 Appendix 18 PDF downloaded from the ITU History
> Portal (`1.44.48.en.102.pdf`, Appendices volume, pages AP18-1 to AP18-4). The
> M.1371-6 clause numbering uses the "A2-x.y" form; M.1371-5 used identical
> numbering without the annex prefix (e.g., Annex 2 §2.2 Table 5). Facts from
> secondary sources are marked as such. Nothing below was taken from memory
> without checking.

## Key questions

1. What is the modulation exactly — GMSK BT, modulation index, bit rate and
   tolerance, NRZI sense — and which of these differ between Class A, Class B
   "CS", and burst devices?
2. What is the packet structure bit by bit (ramp-up, training sequence, start
   flag, data, FCS, end flag, buffer) and how do bit stuffing and the 24-bit
   buffer interact with slot timing?
3. What CRC is used (polynomial, preset, coverage) and how do open-source
   decoders implement it?
4. What are the transmitter requirements: power classes and tolerances, carrier
   frequency error, slotted modulation (spectrum) mask, modulation accuracy test
   sequence, power-vs-time mask (T0…TG), channel switching time, and the 2 s
   hardware shutdown?
5. What are the receiver requirements: sensitivity (−107 dBm at 20 % PER),
   high-level error behaviour, co-channel/adjacent-channel/spurious/
   intermodulation/blocking figures — and how do they translate into link-budget
   and interference numbers for Chapters 27 and 31?
6. What exactly is the channel plan: AIS 1/2, long-range 75/76, ASM 1/2, VDE
   channels, DSC channel 70; what footnotes in RR Appendix 18 govern them; and
   which stations transmit on which?
7. How is Message 27 (long-range) different physically (96-bit data field, 17 ms
   transmission, 96-bit buffer for 1,000 km orbital altitude)?
8. How do burst devices (AIS-SART/MOB/EPIRB-AIS) differ (1 W e.i.r.p.,
   8-message bursts at 75-slot spacing, no receiver)?
9. What does the Class B "CS" carrier-sense window look like in time and level
   (833–1,979 µs window, threshold = noise + 10 dB, −107 dBm floor, −77 dBm cap,
   transmission starts at 2,083 µs)?
10. Which of the above are stable across editions (M.1371-0 → -6), and which
    numbers do chapter authors most often get wrong?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Recommendation ITU-R M.1371-6 | 02/2026; edition history 1998-2001-2006-2007-2010-2014-2026 (from the PDF's cover) | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Annex 2 §A2-2 physical layer (Tables 3–7), §A2-2.11 transient response (Fig. 2, Table 6), §A2-3.2.2 packet format (Fig. 6–8, Table 12), §A2-4.1 channels; Annex 3 Table 22 (Msg 27 packet); Annex 6 Tables 35–36 and §A6-4.3.1 (Class B CS); Annex 8 Tables 86–89, §A8-5 (burst) | Free |
| Recommendation ITU-R M.1371-5 | 02/2014 (superseded) | https://www.itu.int/rec/R-REC-M.1371-5-201402-S/en | Same clauses without the "A2-" prefix; useful when citing equipment type-approved under IEC 61993-2:2018 (which incorporates M.1371-5) | Free |
| ITU Radio Regulations, Edition of 2020, Appendix 18 (Rev. WRC-19) | Appendices volume | https://search.itu.int/history/HistoryDigitalCollectionDocLibrary/1.44.48.en.102.pdf (ITU History Portal); also https://www.itu.int/pub/R-REG-RR-2020 | Table of transmitting frequencies in the VHF maritime mobile band; footnotes f), j), l), n), p), r), s), w), z), zz) | Free |
| Recommendation ITU-R M.2092 | M.2092-0 (10/2015), M.2092-1 (02/2022), M.2092-2 (02/2026) | https://www.itu.int/rec/R-REC-M.2092/en | VDES technical characteristics incl. ASM channel use and VDE modulation (see `r-vdes.md` for details) | Free |
| IEC 61993-2 | Ed. 3.0, 2018 (replaces Ed. 2.0, 2012; Ed. 1.0, 2001) | https://webstore.iec.ch/ (search "61993-2") | Class A test standard: methods of testing for all Table 5/7 parameters; incorporates M.1371-5 | Paid |
| IEC 62287-1 / 62287-2 | Class B CS / Class B SO test standards (editions: verify) | https://webstore.iec.ch/ | Class B transmitter/receiver tests (Table 35/36 equivalents) | Paid |
| IEC 61097-14 | AIS-SART test standard (Ed. 1.0, 2010 (verify)) | https://webstore.iec.ch/ | Burst-transmitter tests, 1 W e.i.r.p. | Paid |
| ISO/IEC 13239:2002 | HDLC procedures | https://www.iso.org/standard/37010.html | Frame structure, flags, bit stuffing, 16-bit FCS (CRC-CCITT) referenced by M.1371 §A2-3.2.2 | Paid |
| rtl-ais (dgiardini), `aisdecoder/lib/protodec.c` | GitHub master (read 2026-10-05) | https://github.com/dgiardini/rtl-ais/blob/master/aisdecoder/lib/protodec.c | Reference open-source CRC implementation: reflected poly 0x8408, init 0xFFFF, final complement | Free (GPL) |
| IMO COMSAR.1/Circ.32/Rev.3 (as quoted in M.1371-6 Table 7 note) | — | (quoted in M.1371-6 p. 15) | Antenna separation guidance quoted in the receiver table note | Free (IMO docs) |

## Verified facts

| Fact | Source (clause / page) | Confidence |
|---|---|---|
| Channel spacing 25 kHz; AIS 1 = 161.975 MHz; AIS 2 = 162.025 MHz; bit rate 9,600 bit/s; training sequence 24 bits; transmit BT ≈ 0.4; receive BT ≈ 0.5; modulation index ≈ 0.5; transmit output power low setting 1 W, high setting 12.5 W (5 W for Class B "SO"). | M.1371-6 Annex 2 Table 3, p. 12 | high |
| Physical-layer constants: data encoding NRZI; FEC not used; interleaving not used; bit scrambling not used; modulation GMSK/FM. | M.1371-6 Table 4, p. 13; §A2-2.7–2.9, pp. 15–16 | high |
| Shipborne AIS receives on two parallel channels and transmits on four independent channels (AIS 1, AIS 2, ch. 75, ch. 76); shore stations use AIS 1/AIS 2 only; AIS-SART, AIS-MOB and EPIRB-AIS transmit exclusively on AIS 1/AIS 2 and have no receivers. | M.1371-6 §A2-2.1.3, §A2-2.1.4, p. 13 | high |
| Transmitter: carrier power error 1.5 dB; carrier frequency error 500 Hz; slotted modulation mask — 0 dBc within ±10 kHz; straight line from −25 dBc at ±10 kHz to −70 dBc at ±25 kHz; −70 dBc from ±25 kHz to ±62.5 kHz. | M.1371-6 Table 5, p. 13 | high |
| Modulation accuracy (test sequence): < 3,400 Hz deviation for bits 0–1; 2,400 ± 480 Hz for bits 2–3; 2,400 ± 240 Hz for bits 4–31 (normal); bits 32–199: 1,740 ± 175 Hz for pattern 0101, 2,400 ± 240 Hz for pattern 00001111 (normal; ±350/±480 Hz extreme). | M.1371-6 Table 5 (end), p. 14 | high |
| Spurious emissions (transmitter): −36 dBm 9 kHz–1 GHz; −30 dBm 1–4 GHz. Intermodulation attenuation 40 dB (base station only). | M.1371-6 Table 5 (end), p. 14 | high |
| Power-vs-time mask (Table 6): T0 = slot start, power ≤ −50 dB of Pss before T0; TA 0–6 bits (0–0.625 ms) power exceeds −50 dB; TB1 at bit 6 (0.625 ms) within +1.5/−3 dB of Pss; TB2 at bit 8 (0.833 ms) within +1.5/−1 dB (start of training sequence); TE at bit 233 (24.271 ms, includes 1 stuffing bit) end of flat region; TF at bit 241 (25.104 ms) power at −50 dB and stays below; TG at bit 256 (26.667 ms) next slot. | M.1371-6 Table 6, p. 14 | high |
| Receiver (Class A / Table 7): sensitivity 20 % PER at −107 dBm; error at high input 1 % PER at −77 dBm and at −7 dBm; adjacent-channel selectivity 20 % PER at 70 dB; co-channel selectivity 20 % PER at 10 dB; spurious response rejection 70 dB; intermodulation response rejection 74 dB; blocking 86 dB; receiver spurious emissions −57 dBm (9 kHz–1 GHz), −47 dBm (1–4 GHz). | M.1371-6 Table 7, pp. 14–15 | high |
| Table 7 note quotes COMSAR.1/Circ.32/Rev.3 §5.2.8: AIS VHF antenna "directly above or below the ship's primary VHF radiotelephone antenna, with no horizontal separation and with minimum 2 metres vertical separation"; if on the same level, at least 5 metres apart. | M.1371-6 p. 15 note | high |
| GMSK modulator BT "0.4 maximum (highest nominal value)"; demodulator designed for BT "maximum 0.5"; modulation index 0.5; frequency stability ±500 Hz or better; bit rate 9,600 bit/s ± 50 ppm. | M.1371-6 §A2-2.3.1–2.4, p. 15 | high |
| Training sequence: 24 bits alternating 0/1; "may begin with a 1 or a 0 since NRZI encoding is used" (Class A); Class B CS: "always starts with a 0". | M.1371-6 §A2-2.5 p. 15; §A6-4.2.1.4 p. 84 | high |
| NRZI: "a change in the level when a zero (0) is encountered in the bit stream". | M.1371-6 §A2-2.6, p. 15 | high |
| Channel switching time < 25 ms; Tx↔Rx switching must not exceed attack/release time; a station must be able to receive in the slot directly before/after its own transmission; it is not required to transmit on the other AIS channel in the adjacent slot. | M.1371-6 §A2-2.11.1, p. 16 | high |
| Two nominal power levels; default is high; changes by manual means or by base station via Message 22; power setting shown on the MKD. Nominal levels 1 W and 12.5 W, or 1 W and 5 W for Class B "SO"; tolerance 1.5 dB. | M.1371-6 §A2-2.12.1–2.12.2, p. 17 | high |
| Automatic hardware transmitter shutdown, independent of software, if a transmitter transmits for more than 2 s. Station must not be damaged by open- or short-circuited antenna terminals. | M.1371-6 §A2-2.13–2.14, p. 17 | high |
| Data transfer is HDLC (ISO/IEC 13239:2002) I-packets with the control field omitted. | M.1371-6 §A2-3.2.2, p. 23 | high |
| Bit stuffing: after five consecutive 1s a 0 is inserted; applies to all bits between the flags (data + FCS); receiver removes the first 0 after five 1s. Preamble and flags are not stuffed. | M.1371-6 §A2-3.2.2.1, §A2-3.2.2.3–4, pp. 23–24 | high |
| Start/end flag: 8 bits 01111110 (7Eh). Default data field 168 bits. Default packet total 256 bits = one slot. | M.1371-6 §A2-3.2.2.2–2.7, pp. 24–25 | high |
| FCS: 16-bit CRC polynomial per ISO/IEC 13239:2002; CRC bits preset to 1; only the data portion is covered. CRC errors → "no further action by the AIS station". | M.1371-6 §A2-3.2.2.6 p. 25; §A2-3.2.3 p. 26 | high |
| Open-source implementation (rtl-ais `protodec_sdlc_crc`): init 0xFFFF, reflected polynomial 0x8408 (= 0x1021 CRC-CCITT), result complemented (`return ~crc`), i.e., the "CRC-16/X-25" / IBM-SDLC variant. | https://github.com/dgiardini/rtl-ais/blob/master/aisdecoder/lib/protodec.c lines 84–96 (read 2026-10-05) | high (as to that code); the equivalence to ISO 13239 FCS is standard HDLC practice |
| Buffer: 24 bits = 4 bits bit-stuffing allowance (fixed-length messages; 76 % of combinations need ≤ 3) + 14 bits distance delay (= 235.9 NM, "protection for a propagation range of over 120 NM") + 6 bits synchronization jitter. | M.1371-6 §A2-3.2.2.8–8.2, p. 25 and footnote 4 | high |
| Timing jitter: mobile station transmission timing error within 104 µs of sync source (accumulated up to 312 µs = 3 bits); base station within 52 µs (accumulated 104 µs). | M.1371-6 §A2-3.2.2.8.3, p. 25 | high |
| Table 12 packet summary: ramp-up 8 bits; training 24; start flag 8; data 168; CRC 16; end flag 8; buffer 24; total 256. | M.1371-6 Table 12, pp. 25–26 | high |
| Transmission timing (Fig. 8): T0 0.000 ms RF power applied; TTS 0.833 ms training starts; T1 1.000 ms power/frequency stabilised; T2 3.333 ms start flag; Ts 4.167 ms end of start flag/begin data ("slot phase synchronization marker"); T3 24.167 ms end of transmission (zero stuffing); T4 = T3 + 1.000 ms RF power reaches zero; T5 26.667 ms end of slot. No modulation after end of transmission. | M.1371-6 §A2-3.2.2.10, pp. 26–27 | high |
| Long packets: at most five consecutive slots per continuous transmission; overhead (ramp, training, flags, FCS, buffer) applied once; no filler. | M.1371-6 §A2-3.2.2.11, p. 27 | high |
| "Garbled" slot definition: no decodable message and RSSI > 16 dB above background noise (per §A6-4.3.1.3 method); distinction used only in repeaters. | M.1371-6 §A2-3.1.3 slot states, p. 22 | high |
| Four App. 18 frequencies designated for AIS: AIS 1 161.975 MHz; AIS 2 162.025 MHz; channel 75 (156.775 MHz) and channel 76 (156.825 MHz) for Message 27 only. Periodic messages alternate AIS 1/AIS 2 (and 75/76 for Msg 27) transmission by transmission. | M.1371-6 §A2-4.1.1–4.1.2, p. 51 | high |
| Message 27 packet: ramp 8, training 24, start flag 8, **data 96** (168 − 72), CRC 16, end flag 8, long-range buffer 96 (4 stuffing + 3 jitter mobile + 1 jitter satellite + 87 propagation-delay difference + 1 spare); "Only 160 bits are used in the 17 ms transmission"; designed for orbital altitudes up to 1,000 km. | M.1371-6 Annex 3 Table 22, p. 63 | high |
| Msg 27 transmitted by Class A and Class B-SO only; nominal interval 3 min; MSSA access using AIS 1/2 slot map but transmitting on 75/76, alternating so each channel is used once per 6 min; "at the current power setting"; can be disabled by Msg 4 field + Msg 23 (station type 10) within a base-station coverage area, timing out 3 min after last Msg 4. | M.1371-6 §A3-2.2–2.3.4, p. 64 | high |
| Class B "CS" transmitter (Table 35): frequency error ±500 Hz; carrier power 33 dBm ± 1.5 dB conducted (= 2 W); mask −25 dBc at ±10 kHz to **−60 dBc** at ±25 kHz (vs −70 dBc for Class A); transmission delay 2,083 µs; ramp-up ≤ 313 µs; ramp-down ≤ 313 µs; transmission duration ≤ 23,333 µs; spurious −36/−30 dBm. | M.1371-6 Annex 6 Table 35, pp. 84–85 | high |
| Class B "CS" receiver (Table 36): sensitivity 20 % PER at −107 dBm (−104 dBm at ±500 Hz offset); error at high level 2 % PER at −77 dBm, 10 % PER at −7 dBm; co-channel rejection: wanted −101 dBm vs unwanted −111 dBm (10 dB); adjacent-channel: unwanted −31 dBm (70 dB); spurious response −31 dBm; intermodulation −36 dBm (65 dB); blocking −23 dBm (< 5 MHz) / −15 dBm (> 5 MHz). | M.1371-6 Table 36, p. 86 | high |
| CS detection window: 1,146 µs long, from 833 µs to 1,979 µs after T0; first 8 bits excluded "to allow for propagation delays and ramp down periods of other units"; CSTDMA transmission begins 20 bits (TA = 2,083 µs) after T0. | M.1371-6 §A6-4.3.1.2, p. 87 | high |
| CS detection threshold: rolling 60 s per Rx channel; minimum energy (background) + 10 dB; floor −107 dBm; background tracked over ≥ 30 dB so maximum threshold −77 dBm. Footnote 11 example: sample RSSI > 1 kHz, 20 ms sliding average, 4 s minimum, keep 15 intervals, minimum of those + 10 dB. | M.1371-6 §A6-4.3.1.3 and footnote 11, p. 87 | high |
| Class B CS sync jitter ≤ ±3 bits (±312 µs) from the rolling-60 s average of received position reports (Msg 1, 2, 3, 4, 18, repeat indicator 0); holds sync 30 s after loss. | M.1371-6 §A6-4.3.1.1.1, p. 86 | high |
| Burst devices (Annex 8): channels 161.975/162.025; 9,600 bit/s; 24-bit training; settling time 0.833 ms (power within 20 %, frequency within ±1 kHz); ramp-down 1.0 ms; transmission duration ≤ 26.6 ms; nominal 1 W e.i.r.p.; BT 0.4; modulation index 0.5; frequency error 500 Hz normal / ±1,000 Hz extreme. | M.1371-6 Annex 8 Tables 86–89, pp. 151–152 | high |
| Burst access: random first slot; 8 messages per burst with 75-slot increments, alternating AIS 1/AIS 2; no more than once per minute; next burst offset 1 min ± 6 s; Msg 1 and Msg 14 separated by multiples of 75 slots within 450 slots are deemed from the same transmitter; "disruptive to the VDL"; limited to safety-of-life floating devices. | M.1371-6 §A8-1, §A8-5, pp. 150, 153 | high |
| RR App. 18 Table: channel 70 = 156.525 MHz, "Digital selective calling for distress, safety and calling" (note j: exclusively DSC); channels 75/76 = 156.775/156.825 MHz, notes n), s); ASM 1 = 161.950 MHz, ASM 2 = 162.000 MHz, note z); AIS 1 = 161.975, AIS 2 = 162.025, notes f), l), p); channels 1027/1028/87/88 (157.350/157.400/157.375/157.425) single-frequency analogue port operations (note zz, WRC-19). | RR 2020 App. 18 Table, pp. AP18-2/3 | high |
| App. 18 note n): with the exception of AIS, use of 75/76 restricted to navigation-related communications, output power limited to 1 W to protect channel 16 (WRC-12). Note s): 75/76 also allocated to MSS (Earth-to-space) for reception of Message 27 (WRC-12). Note p): AIS 1/2 may be used by MSS (Earth-to-space) for reception of AIS from ships (WRC-07). Note l): AIS 1/2 for worldwide AIS "unless other frequencies are designated on a regional basis" (WRC-07). | RR 2020 App. 18 notes, pp. AP18-3/4 | high |
| App. 18 note f): 156.525 (ch 70), 161.975 (AIS 1) and 162.025 (AIS 2) may also be used by autonomous maritime radio devices Group A (safety-enhancing, DSC and/or AIS) per ITU-R M.2135 (WRC-19). Note r): 160.9 MHz (channel 2006) designated for Group B devices (non-safety, AIS technology), limited to 100 mW e.i.r.p. and antenna ≤ 1 m above sea surface. | RR 2020 App. 18 notes f), r), p. AP18-4 | high |
| App. 18 note w): bands 157.1875–157.3375 MHz and 161.7875–161.9375 MHz (channels 24, 84, 25, 85, 26, 86, 1024, 1084, 1025, 1085, 1026, 1086, 2024, 2084, 2025, 2085, 2026, 2086) identified for VDES per M.2092; "shall not be used for feeder links". Channel 1024 = 157.200 MHz, 2024 = 161.800, 1084 = 157.225, 2084 = 161.825, 1025 = 157.250, 2025 = 161.850, 1085 = 157.275, 2085 = 161.875, 1026 = 157.300, 2026 = 161.900, 1086 = 157.325, 2086 = 161.925 (all 25 kHz). | RR 2020 App. 18 Table and note w) | high |
| App. 18 note e): 12.5 kHz interleaving must not affect AIS 1, AIS 2 (nor channels 06, 13, 15, 16, 17, 70). Notes b)/c): channels 06, 13, 15, 16, 17, 70, 75, 76 excluded from high-speed data/facsimile use. | RR 2020 App. 18 general notes | high |
| M.2092 editions: -0 (10/2015), -1 (02/2022), -2 (02/2026). | https://www.itu.int/rec/R-REC-M.2092/en (read 2026-10-05) | high |
| IEC 61993-2 Ed. 3.0 published 2018; replaces Ed. 2.0 (2012); incorporates M.1371-5; adds locating-device groups (AIS-SART/EPIRB-AIS/MOB-AIS), SSA sentence, optional 61162-450/-460, BAM, software-update requirements. | IEC webstore abstract (via search summary citing iec.ch, read 2026-10-05) | medium (abstract text seen only via search summary; confirm on webstore page) |
| NOAA Weather Radio operates on seven frequencies 162.400–162.550 MHz in 25 kHz steps; transmitter power typically up to 1,000 W. | weather.gov NWR pages via search summary (read 2026-10-05); see `r-noise.md` | medium |

## Notes and quotes

- On FEC: "Forward error correction is not used." (M.1371-6 §A2-2.7). This single
  line is the root of Chapter 30: every bit error that the CRC detects costs the
  whole packet, and there is no soft-decision gain to be had from the standard
  itself — only from receiver design (e.g., multiple demodulators, SIC).
- On the transmission mask: "At the situation where the ramp down of the RF
  power overshoots into the next slot, there should be no modulation of the RF
  after the termination of transmission. This prevents undesired interference,
  due to false locking of receiver modems, with the succeeding transmission in
  the next slot." (§A2-3.2.2.10). Note 1 adds that an overlap into the next slot
  "would occur only in the event of a propagation anomaly" and that the
  receiver's "range discrimination characteristics" cover it.
- On the distance-delay budget: 14 bits ≈ 1.458 ms ≈ 437 km ≈ 235.9 NM one-way;
  the standard says this "provides protection for a propagation range of over
  120 NM", i.e., roughly double the design slot-reuse distance.
- The receiver training sequence is deliberately not stuffed and "may begin
  with a 1 or a 0 since NRZI encoding is used" for Class A, but Class B CS says
  "always starts with a 0". This matters for demodulator preamble correlators
  (a 0101… NRZI pattern becomes a constant-rate toggle, i.e., a 2,400 Hz tone
  in the FM sense — the 1,740 Hz / 2,400 Hz figures in Table 5 are the measured
  frequency deviations for the 0101 and 00001111 test patterns).
- The Class B CS modulation mask is relaxed to −60 dBc at ±25 kHz (Class A:
  −70 dBc). Class B CS power is specified as 33 dBm conducted (2 W), not as a
  low/high pair; Class B SO uses 1 W / 5 W.
- Burst devices are explicitly labelled "disruptive to the VDL" — a useful
  quote for Chapter 68 and for the fishing-gear-buoy discussion.
- The "garbled slot" definition (RSSI > 16 dB above background with no decodable
  message) is the closest thing M.1371 has to an official definition of a
  collision; repeaters are the only stations required to treat it differently
  from "free".
- For Message 27, the shortened 96-bit data field plus a 96-bit guard means the
  burst is ≈ 17 ms long; the extra ~70 bits (~7.3 ms ≈ 2,190 km) of guard time
  absorb the differential path delay across a 1,000 km-altitude footprint.
- RR App. 18 note r) (channel 2006, 160.900 MHz, 100 mW e.i.r.p., ≤ 1 m antenna
  height, "autonomous maritime radio devices Group B … that do not enhance the
  safety of navigation, using AIS technology") is the regulatory home intended
  for fishing-net buoys and similar devices (Chapter 68) — in the WRC-19 text it
  is a designation, not a prohibition on misuse of AIS 1/2.

## Open questions / (verify)

- IEC 61993-2 Ed. 3.0 content: confirm from the IEC webstore page itself (the
  reader tool returned 404 on one URL) the exact publication date (2018-xx) and
  whether an amendment or Ed. 4.0 draft referencing M.1371-6 exists as of 2026
  (verify).
- IEC 62287-1 / 62287-2 current editions and dates (verify); 61097-14 edition
  (2010?) and any amendment (verify).
- The exact HDLC FCS convention (transmit the ones-complement of the register;
  receiver residue 0xF0B8) is standard for ISO 13239 and is what rtl-ais
  implements; confirm AIS-catcher's and gr-ais's implementations by reading
  their current source (GitHub raw fetches failed in this session for those
  repos) (verify).
- Spectrum mask for the ASM channels and VDE channels (from M.2092-2 Annex
  tables) — not read in this session; see `r-vdes.md` and mark VDE rate figures
  (verify) until read from M.2092-2.
- Whether M.1371-6 changed any Table 5/6/7 numbers versus M.1371-5: a diff of
  the two text extracts (`m1371-5.txt` vs `m1371-6.txt` in the research scratch
  directory) should be done before Chapter 28 is finalised (verify); spot
  checks in this session found identical Table 3–7 values.
- The widely-quoted "−107 dBm for 20 % PER" is the M.1371 Table 7 value; IEC
  61993-2 may test at a slightly different level or add a −104 dBm offset-
  frequency case as Table 36 does for Class B CS — check the IEC text (verify).
- Whether Fig. 2 (power-vs-time mask) in M.1371-6 is numerically identical to
  the IEC 61993-2 figure used by test labs (verify).
- AIS-SART e.i.r.p. "1 W" is radiated, not conducted; the test method and the
  reference antenna gain used (IEC 61097-14) should be checked before quoting
  a conducted power (verify).

## Candidate figures and worked examples

1. **Burst anatomy figure (Chapter 28):** 256-bit slot as a horizontal bar with
   the 8/24/8/168/16/8/24 segments, annotated with T0, TTS 0.833 ms, T1 1.000 ms,
   T2 3.333 ms, Ts 4.167 ms, T3 24.167 ms, T4, T5 26.667 ms (from Table 12 and
   Fig. 8 timings). SVG, redraw from numbers (do not copy the ITU figure).
2. **Power-vs-time mask figure:** envelope with TA/TB1/TB2/TE/TF/TG points from
   Table 6; overlay the Class B CS variant (TA = 2,083 µs, ramp ≤ 313 µs, duration
   ≤ 23,333 µs) and the CS detection window (833–1,979 µs).
3. **Spectrum mask figure:** Class A (−25 dBc @ ±10 kHz → −70 dBc @ ±25 kHz) vs
   Class B CS (→ −60 dBc), with a measured GMSK BT = 0.4 spectrum from a NumPy
   synthesis overlaid (code in `code/rf/gmsk_burst.py`, file output only).
4. **Worked example — bit stuffing:** take a real Message 1 payload, show the
   HDLC stuffing pass, count inserted zeros, compare with the 4-bit allowance.
5. **Worked example — CRC:** compute the 16-bit FCS of a 168-bit Message 1 with
   the CRC-16/X-25 parameters (poly 0x1021, init 0xFFFF, reflected, xorout
   0xFFFF), show the receiver residue check.
6. **Worked example — distance-delay budget:** 14 bits × 104.17 µs = 1.458 ms;
   × c = 437 km = 235.9 NM; relate to the 120 NM slot-reuse rule and to
   satellite reception (why Message 27 needs 87 bits).
7. **Table — station classes vs PHY parameters:** Class A (12.5/1 W, −70 dBc),
   Class B SO (5/1 W), Class B CS (2 W, −60 dBc, CS window), AIS-SART/MOB/EPIRB
   (1 W e.i.r.p., bursts), base station (+ 40 dB intermod requirement), AtoN
   (power per IEC 62320-2 — (verify)).
8. **Channel plan table (Chapters 28, 69):** AIS 1/2, 75/76, ASM 1/2, DSC 70,
   VDE 1024–1026/1084–1086/2024–2026/2084–2086, channel 2006 (Group B devices),
   with frequencies and the governing App. 18 footnote letter for each.
9. **Noise-floor arithmetic (Chapter 27):** kTB for 25 kHz = −174 + 44 = −130 dBm;
   with a 6–8 dB receiver noise figure and ~10–12 dB required Eb/N0 for GMSK at
   the PER target, the −107 dBm sensitivity requirement sits ~15 dB above the
   thermal floor — show the arithmetic and note which numbers are standard
   requirements versus engineering assumptions.

## Recommended use by chapter

- **Ch. 20 (station classes):** power table — Class A 12.5/1 W; Class B SO
  5/1 W; Class B CS 2 W (33 dBm); burst devices 1 W e.i.r.p.; power change via
  Msg 22 or manual, default high. Cite Table 3, §A2-2.12, Table 35, Table 89.
- **Ch. 21 (link layer):** the 24-bit buffer decomposition and the 104/312 µs
  jitter limits; slot timing marks T2/Ts as secondary sync sources; "garbled"
  slot definition.
- **Ch. 24 (timing):** Ts (4.167 ms) as "slot phase synchronization marker";
  §A2-3.2.2.10 note that T2 can be a secondary sync source if UTC is lost.
- **Ch. 27 (RF basics):** −107 dBm/20 % PER sensitivity; −77 dBm high-level
  behaviour; 70 dB adjacent-channel; 10 dB co-channel; 86 dB blocking — these
  feed the link-budget and interference-margin worked examples; COMSAR antenna
  separation note.
- **Ch. 28 (PHY):** everything in the Verified facts table; emphasise what is
  identical across editions and the three places where Class B CS differs
  (mask, power spec style, CS window). Use figures 1–3 and worked examples 4–6.
- **Ch. 30 (loading):** no FEC/interleaving/scrambling (Table 4); CRC errors
  cause "no further action"; Message 27 shortening rationale; burst devices
  "disruptive to the VDL".
- **Ch. 33 (hardware/SDR):** BT 0.4/0.5, h = 0.5, ±500 Hz tolerance, ±50 ppm bit
  rate, 25 kHz channels — the parameters an SDR demodulator must match; rtl-ais
  CRC code as a reference.
- **Ch. 34 (fingerprinting):** the tolerances (carrier frequency error 500 Hz,
  power error 1.5 dB, ramp timings, modulation accuracy ±240 Hz) bound the
  manufacturer-to-manufacturer variability an SEI method can exploit.
- **Ch. 39 (satellite):** Table 22 Msg 27 packet; App. 18 notes p) and s)
  giving satellites legal standing to receive AIS 1/2 and 75/76.
- **Ch. 68 (special-purpose):** Annex 8 burst behaviour (8 × 75-slot bursts,
  once per minute); App. 18 note r) channel 2006 for Group B devices; note f)
  Group A devices on AIS 1/2.
- **Ch. 69 (VDES/other channels):** channel table with footnotes; note n) 1 W
  limit on 75/76 for non-AIS use; ASM 1/2 note z).
- **App. B:** M.1371 edition list (1998, 2001, 2006, 2007, 2010, 2014, 2026);
  M.2092 editions (2015, 2022, 2026); IEC 61993-2 editions (2001, 2012, 2018).
- **App. C/I:** packet layout table; CRC and bit-stuffing code.
