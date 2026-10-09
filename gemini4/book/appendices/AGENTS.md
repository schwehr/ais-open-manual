# `book/appendices` — Directory Guide for Agents

## Overview
This directory contains the eight normative and engineering reference appendices (`Appendix A` through `Appendix H`) for *Automatic Identification System (AIS): The Open Manual*. These files serve as the authoritative lookup tables for bit-level message schemas, MMSI/MID allocations, NMEA 0183 6-bit armor vs. ITU 6-bit ASCII encodings, Binary Application-Specific Messages (ASMs), international regulatory/technical standards, admiralty case law and patents, home receiver station blueprints, and the master bibliography.

## Subdirectories
None. This is a leaf directory under `book/`.

## Files in This Directory

- **`appendix-a-message-1-to-27-bit-tables.md`**
  - Complete bit-level reference tables (Tables A.1–A.24) for all 27 ITU-R M.1371-5 AIS message types.
  - Every table specifies both 0-based (`libais`/`pyais`) and 1-based (`ITU-R M.1371-5`) inclusive bit ranges, bit width, `libais` C++/Python field name, data type (`uintW`, `intW`, `bool`, `str6`, `raw`), physical scale/units, and sentinel ("not available") values.
  - Includes normative enumeration lookup tables (Tables A.25–A.30) for the 19-bit SOTDMA/ITDMA/CSTDMA Communication State sub-fields, Navigation Status (`0–15`), Electronic Position Fixing Device (EPFD) types (`0–15`), Ship and Cargo Type codes (`0–99`), Aid to Navigation (AtoN) types (`0–31`), and Message 23 Group Assignment reporting intervals.

- **`appendix-b-mid-and-mmsi-prefixes.md`**
  - Comprehensive reference for 9-digit Maritime Mobile Service Identity (MMSI) formatting and 3-digit Maritime Identification Digits (MID) per ITU-R M.585-9 and ITU-R M.2135-0.
  - Details all 11 MMSI structural categories (Standard Ship `MIDxxxxxx`, Group `0MIDxxxxx`, Coast/Base Station `00MIDxxxx`, SAR Aircraft `111MIDxxx`, Handheld VHF `8MIDxxxxx`, AIS-SART `970xxyyyy`, AIS-MOB `972xxyyyy`, EPIRB-AIS `974xxyyyy`, AMRD Group B `979zzzzzz`, Craft Associated with a Parent Ship `98MIDxxxx`, and Physical/Virtual AtoN `99MIDxxxx`), plus common unconfigured/spoofed MMSI patterns seen in the wild (`000000000`, `111111111`, `123456789`, `1193046`).
  - Provides complete regional MID allocation tables (`2xx` Europe, `3xx` North/Central America & Caribbean, `4xx` Asia & Middle East, `5xx` Oceania & SE Asia, `6xx` Africa, `7xx` South America) and a Multi-MID Flag State Consolidation Index for SQL/Python fleet analytics.

- **`appendix-c-nmea-6bit-ascii-and-checksum.md`**
  - Mathematical and tabular reference distinguishing the two distinct 6-bit character encodings in AIS:
    1. **Outer Layer — NMEA 0183 6-Bit ASCII Armor (IEC 61162-1):** Maps 6-bit integers (`0–63`) to printable ASCII characters `'0'`–`'W'` (`48–87`) and `` '`' ``–`'w'` (`96–119`), skipping the 8-character gap `88–95` (`'X'`–`'_'`) reserved for NMEA 0183 v4.0 TAG block delimiters (`\`) and hex escape sequences (`^`).
    2. **Inner Layer — ITU-R M.1371-5 6-Bit ASCII Text (Table 44):** Maps 6-bit integers (`0–63`) inside `str6` bitfields (e.g., Vessel Name, Call Sign, Destination) to uppercase `'@'`–`'_'` (`0–31`) and space/digits/punctuation `' '`–`'?'` (`32–63`).
  - Includes canonical bit lengths and required `fill_bits` for Messages 1–27, step-by-step worked examples of NMEA 0183 and TAG block 8-bit XOR checksum calculation and two-layer unpacking of `"EVER GIVEN"`, and branchless $O(1)$ C/C++ lookup tables (`NMEA_DEARMOR_LUT[256]` and `ITU_6BIT_TEXT_LUT[65]`).

- **`appendix-d-binary-asm-dac-fi-registry.md`**
  - Authoritative registry of Binary Application-Specific Messages (Messages 6, 8, 25, and 26) indexed by 10-bit Designated Area Code (`DAC`), 6-bit Functional Identifier (`FI`), and combined 16-bit Application ID (`AppID = (DAC << 6) | FI`), cross-referenced to `libais` C++ decoders (`ais6.cpp`, `ais8.cpp`, `ais8_1_22.cpp`, `ais8_200.cpp`, `ais8_366.cpp`, `ais8_366_22.cpp`).
  - Covers International IMO payloads (`DAC = 1`, `FI 0`–`40` across SN/Circ.236 and SN.1/Circ.289, including meteorological/hydrographic `FI 11/31` and Area Notice `FI 22`), European Inland AIS (`DAC = 200`, CCNR/CESNI ES-TRIN `FI 10, 21, 22, 23, 24, 40, 44, 55`), Canadian & US St. Lawrence Seaway (`DAC = 316` & `DAC = 366`, `FI 1, 2, 3, 31, 32`), USCG Area Notice & Encrypted AIS (EAIS) Blue Force Tracking (`DAC = 366`, `FI 22, 56, 57`), and UK/Ireland GLA AtoN monitoring (`DAC = 232` & `235`, `FI 10, 20`).

- **`appendix-e-master-standards-matrix.md`**
  - Cross-referenced engineering matrix of over 80 international and national technical standards governing AIS and VDES across seven regulatory families:
    - **ITU-R:** Radio Regulations Appendix 18, M.1371-0 through M.1371-5, M.585-9, M.823-3, M.1084-5, M.2092-1 (VDES), M.2135-0 (AMRD), P.1546-6, P.528-5, M.2287-0.
    - **IMO:** SOLAS Chapter V Regs 19 & 19-1, COLREGs, STCW, MSC.74(69), MSC.434(98), Res. A.1106(29), Res. A.1192(33) (Shadow Fleet), SN/Circ.227, SN.1/Circ.243/Rev.2, SN.1/Circ.289, MSC.1/Circ.1252, Model Course 1.34.
    - **IEC TC 80:** IEC 61993-2 (Class A), 62287-1 (Class B CS), 62287-2 (Class B SO), 62320-1/2/3 (Base Station, AtoN, Repeater), 61097-14 (AIS-SART), 63269 (AIS-MOB), 63173-1/2 (S-421 & SECOM), 61162-1/2/3/450/460 (NMEA/LWE), 60945, 61174 (ECDIS), 62388 (Radar), 61996-1/2 (VDR/S-VDR), 62923-1/2 (BAM).
    - **IALA:** 2024 IGO Convention, Recommendations A-124, A-126, V-128, and Guidelines G1082 & G1117 (VDES).
    - **IHO:** S-52, S-57, S-63, S-100, S-101, S-102, S-104, S-111, S-124, S-129, S-421.
    - **RTCM & NMEA:** RTCM 10402.3, 12101.1, 11901.1, NMEA 0183, NMEA 2000, NMEA OneNet.
    - **Regional/National:** CCNR/CESNI ES-RIS, EU Directive 2002/59/EC, MED 2014/90/EU, OPA-90, MTSA 2002, 33 CFR § 164.46, 47 CFR Part 80.
  - Concludes with a quick-reference "Which Standard Defines What?" engineering lookup table.

- **`appendix-f-court-cases-statutes-and-patents.md`**
  - Three-part legal and intellectual property index:
    1. **Section F.1 (Admiralty Case Law & Casualty Investigations):** Chronological table of 16 landmark cases and official casualty reports (*Deepwater Horizon* 2010, *Costa Concordia* 2012, *USS Fitzgerald* & *USS John S. McCain* 2017, *Wakashio* 2020, *Sakizaya Kalon* [2020] EWHC 2604, *Alexandra 1 v Ever Smart* [2021] UKSC 6, *Ever Given* 2021, *MV Dali* 2024, *Newnew Polar Bear* & *Yi Peng 3* 2023–2024) plus US DOJ sanctions forfeiture actions (*M/V Wise Honest* 2019, *Grace 1* 2019).
    2. **Section F.2 (Treaties, Statutes, Procedural Rules & Privacy Laws):** Summary of 19 statutory regimes including UNCLOS, SOLAS, COLREGs, US 33 CFR § 164.46, UK Civil Procedure Rules Part 61 (Practice Direction 61 § 4.2 mandatory 21-day electronic track disclosure), radio interception statutes (US 47 U.S.C. § 605(a) vs. UK Wireless Telegraphy Act 2006 s. 48), EU GDPR (`2016/679`), and China's Data Security Law (DSL) & Personal Information Protection Law (PIPL).
    3. **Section F.3 (AIS, SOTDMA & Satellite RF Patent Registry):** Complete patent dossier covering First-Generation SOTDMA patents (Håkan Lans / GP&C Systems `SE 8803166`, `EP 0 465 532 B1`, and `US 5,506,587`—all 19 claims cancelled March 30, 2010 via USPTO Ex Parte Reexamination Control No. `90/008,295`) and Second-Generation Satellite AIS de-collision, SIC, Faraday polarization diversity, Doppler anti-spoofing, VDES, and TDOA/FDOA geolocation patents (`US 7,839,336`, `US 8,218,670`, `US 8,761,775`, `US 9,112,590`, `US 8,068,857`, `US 9,419,708`, `US 9,632,175`, `US 10,317,509`).

- **`appendix-g-home-ais-station-bom-and-configs.md`**
  - Turnkey hardware and software deployment guide for building a high-sensitivity 24/7 Home AIS Receiving Station:
    - **Hardware & RF Front-End:** Full RF signal-chain architecture, Tier 1 (~$110) and Tier 2 (~$185) Bills of Materials with exact coax connector genders, $162\text{ MHz}$ coaxial cable attenuation comparison table, dimensional cutting blueprint and NanoVNA tuning procedure for a $162.000\text{ MHz}$ copper-pipe J-pole antenna, and $162\text{ MHz}$ SAW bandpass filter $S_{21}$ frequency-response specifications.
    - **Linux System Configuration:** Kernel DVB-T driver blacklist (`/etc/modprobe.d/blacklist-dvb-ais.conf`), deterministic USB `udev` rules (`/etc/udev/rules.d/50-ais-rtlsdr.rules`), multi-output `AIS-catcher` JSON configuration (`/etc/ais-catcher/ais-catcher.conf`), hardened `systemd` service units, and `gpsd` USB GNSS time synchronization.
    - **Archival Pipeline:** Complete Python daemon (`ais_archiver.py`) that ingests local UDP JSON from `AIS-catcher`, flushes hourly ZSTD-compressed Hive-partitioned GeoParquet files, and maintains a live DuckDB database (`latest_vessels` and `hourly_rf_stats`) with ready-to-run spatial SQL queries.

- **`appendix-h-master-bibliography.md`**
  - Annotated master bibliography index organized across 8 thematic sections (H.1 through H.8), cross-referencing every BibTeX key in the root `MASTER_BIBLIOGRAPHY.bib` file to its full formatted citation, DOI/URL, and the specific book chapters where it is cited.
