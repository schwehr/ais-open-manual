# The Maritime Automatic Identification System (AIS) Handbook
## *From RF Physics, Protocol Internals, and Open-Source Software to Global Surveillance, 3D Visualization, Security, and Spatial Analytics*

---

## Master Table of Contents

### Blueprint & Project Tracking
* [Master Book Plan (`PLAN.md`)](../PLAN.md)
* [Actionable Task Backlog (`TASKS.md`)](../TASKS.md)
* [Authoring & Technical Style Guide (`STYLE_GUIDE.md`)](../STYLE_GUIDE.md)

### Front Matter
* [Notation, Bit-Level Conventions, RF Units, and Coordinate Frames](00-front-matter/notation-and-conventions.md)
* [Chronological Timeline of Navigation, Geodesy, GIS, and AIS (`schwehr/gis-history`)](00-front-matter/ais-and-gis-history-timeline.md)
* [Acronyms and Comprehensive Technical Glossary](00-front-matter/acronyms-and-glossary.md)

---

### Part I: Origins, History, Governance, Standards, Patents, and Law
* **[Chapter 1: Introduction to AIS and the Taxonomy of All AIS Uses](part1-history-governance/ch01-introduction-and-uses.md)**
  * *The Three IMO Pillars, SAR, AtoNs, At-Sea Operations, Environmental Response, Whale Alert, IUU Fishing, Emissions/URN, PORTS®, Commodity Trading, 3D Blender Forensics, and Radio Science*
* **[Chapter 2: Deep History of Maritime Navigation, Geodesy, and the Birth of AIS](part1-history-governance/ch02-history-of-navigation-and-ais.md)**
  * *From Compass, H4 Chronometer, Radar, and LORAN to Exxon Valdez (1989), OPA-90, Håkan Lans STDMA, PAWSS New Orleans (1998), GPS SA Off (2000), September 11, 2001, MTSA 2002, and SOLAS Chapter V*
* **[Chapter 3: Governance, International Organizations, Treaties, Standards, and Patents](part1-history-governance/ch03-governance-standards-and-patents.md)**
  * *IMO, ITU, IALA (2024 IGO), IHO, IEC, RTCM, NMEA; UNCLOS, SOLAS, COLREGs; Master Standards Cross-Reference; Håkan Lans US Patent 5,506,587 (2010 Reexamination Cancellation & Expiration) and Satellite AIS Patents*
* **[Chapter 4: Legal Issues, Admiralty Court Cases, Casualty Forensics, and Privacy](part1-history-governance/ch04-legal-cases-casualties-and-privacy.md)**
  * *The "Alexandra 1" & "Ever Smart" [2021] UKSC 6, Panamax Alexander, CPR Part 61 Reforms, 3D Courtroom Reconstruction in Blender, Deepwater Horizon, Ever Given, MV Dali, OFAC Sanctions Forfeitures, GDPR, and China DSL/PIPL*

---

### Part II: RF Physics, Propagation, Physical Layer, Antennas, SDRs, and Collection Sites
* **[Chapter 5: Maritime VHF RF Fundamentals, Spectrum Allocation, and Shipboard Noise](part2-rf-hardware/ch05-vhf-rf-basics-channels-and-noise.md)**
  * *All AIS/ASM/VDES/AMRD RF Channels, Radio Horizon, Fresnel Zones, Two-Ray Multipath, and Shipboard Noise Sources (LED PWM/SMPS, VFDs, Alternators, Radar & VHF Co-Site Desensitization)*
* **[Chapter 6: AIS RF Propagation Modeling, Atmospheric Ducting, and Network Loading Studies](part2-rf-hardware/ch06-rf-propagation-ducting-and-loading.md)**
  * *ITM/Longley-Rice, ITU-R P.1546/P.528, Parabolic Equation (APM/AREPS), Tropospheric Ducting Inversion for NWP Model Testing, ITU-R M.2287 VDL Loading, and Packet Collision Studies*
* **[Chapter 7: AIS Physical Layer: Bit Encoding, HDLC, GMSK, and Salvaging Corrupted RF Recordings](part2-rf-hardware/ch07-physical-layer-encoding-and-packet-recovery.md)**
  * *256-Bit Slot Anatomy, Bit-Stuffing, CRC-16, NRZI, GMSK Modulation, Soft-Decision Syndrome Recovery, Partial MMSI Forensics, and Successive Interference Cancellation (SIC)*
* **[Chapter 8: Antenna Engineering and Selection Across Platforms](part2-rf-hardware/ch08-antenna-engineering-and-selection.md)**
  * *Gain vs. Vertical Beamwidth Physics; Best Antennas for Large Ships, Small Ships (Sailboat Heeling Penalty), Very Small Systems (MOB/Buoys/UAVs/CubeSats), and Shore Stations*
* **[Chapter 9: Transceiver Hardware, SDRs, and Low-Budget Home AIS Receiver Setup](part2-rf-hardware/ch09-transceiver-hardware-sdrs-and-home-station.md)**
  * *Class A vs. Class B CS/SO Hardware, Receive/Transmit SDRs (RTL-SDR, Airspy, SDRplay, HackRF, USRP), and Complete Step-by-Step Low-Budget Home AIS Station Build Guide*
* **[Chapter 10: Shore and At-Sea Collection Site Engineering and Global Networks](part2-rf-hardware/ch10-shore-and-sea-collection-networks.md)**
  * *Towers, Lighthouses, High-Elevation Multi-Cell Paradox, Places to Avoid (Large Radars & 162.40–162.55 MHz NOAA Weather Radio), At-Sea Buoys/ASVs, and Global Aggregator Networks*

---

### Part III: Timing, GNSS Dependencies, MMSI, Buses, and Protocol Internals
* **[Chapter 11: Timing Signals in AIS: Architecture, Practice, Robustness, and Timing Attacks](part3-timing-protocol/ch11-timing-signals-1pps-and-timing-attacks.md)**
  * *1PPS vs. NMEA Latency, Hardware Without GNSS Timing (SDRs, Class B CS, Atomic/PTP/eLORAN Base Stations), Sync States 0–3, and Breaking an AIS Network via Timing Manipulation*
* **[Chapter 12: GNSS Systems Overview, Support Matrix, GNSS-Denied Locations, and Jamming](part3-timing-protocol/ch12-gnss-systems-denial-and-jamming.md)**
  * *GPS, GLONASS, BeiDou, Galileo, DGNSS Msg 17; Non-GPS AIS Terminals; Sentinel Values (`181°/91°`, `61/62/63`); GNSS Jamming/Spoofing Impacts and Workarounds (R-Mode, eLORAN, CRPA, INS)*
* **[Chapter 13: What Is an MMSI? Deep Dive into Maritime Identity](part3-timing-protocol/ch13-mmsi-and-maritime-identity.md)**
  * *ITU-R M.585-9 Complete Taxonomy (MIDs, Ship, Group, Coast, SAR Aircraft 111, Craft 98, AtoN 99, SART 970, MOB 972, EPIRB 974, AMRD 979), IMO Hull Numbers, and Identity Collisions*
* **[Chapter 14: Standards for Sharing and Logging AIS: NMEA 0183, NMEA 2000, NMEA TAG Blocks, and VDR](part3-timing-protocol/ch14-nmea-0183-nmea-2000-tag-blocks-and-vdr.md)**
  * *IEC 61162-1/2 (`!AIVDM`/`!AIVDO`, 6-Bit Armor, XOR Checksum), NMEA TAG Blocks (`\s:...,c:...\`), NMEA 2000 CAN PGNs, IEC 61162-450 LWE, and Voyage Data Recorders (VDR/S-VDR)*
* **[Chapter 15: Complete AIS Message Catalog (Messages 1 Through 27)](part3-timing-protocol/ch15-complete-ais-message-catalog-1-to-27.md)**
  * *Bit-Level Schemas, Nonlinear ROT Equations, Hull Dimension Antenna Offsets, and SOTDMA/ITDMA Sub-States for All 27 ITU-R M.1371-5 Messages*
* **[Chapter 16: Binary Application-Specific Messages (ASMs), Tides, Marine State, and Area Notices](part3-timing-protocol/ch16-binary-asm-tides-ports-and-area-notices.md)**
  * *Messages 6, 8, 25, 26; IMO Circ.289 DAC 1 FI 11/31 Met/Hydro; NOAA PORTS®; St. Lawrence Seaway; RTCM 12301.1; and Dynamic Area Notices (`ais-area-notice` DAC 1/366 FI 22)*

---

### Part IV: Spaceborne, Airborne, SAR/DF, Fishing Gear, User Hacks, and AIS 2.0 (VDES)
* **[Chapter 17: Satellite AIS (S-AIS): Orbital RF Reception, De-Collision DSP, and Satellite Transmission](part4-space-air-vdes/ch17-satellite-ais-reception-and-transmission.md)**
  * *Orbital Footprint Multi-Cell Collisions, Doppler & Delay Spread, Message 27 (Ch 75/76), SIC De-Collision, and Satellite-to-Ship Transmissions (NorSat-2, NorSat-TD, Sternula-1 VDE-SAT)*
* **[Chapter 18: AIS in Aircraft, Drones (UAVs), Search and Rescue, and Direction Finding](part4-space-air-vdes/ch18-aircraft-drones-sar-and-direction-finding.md)**
  * *Message 9 SAR Aircraft, Airborne ISR (Minotaur, P-8, SeaGuardian, ScanEagle), AIS-SART/MOB/EPIRB, and VHF Direction Finding (RDF) for SAR Homing and AoA Counter-Spoofing*
* **[Chapter 19: AIS for Fishing Gear, Autonomous Maritime Radio Devices (AMRDs), and Unintended User Hacks](part4-space-air-vdes/ch19-fishing-gear-amrds-and-user-hacks.md)**
  * *High-Power Net Pingers/Sun-Buoys, VDL Congestion & Alarm Fatigue, ITU-R M.2135 AMRD Group B (160.900 MHz), and Unintended User Hacks (Msg 5/14 Chat, Track-Art, Dinghy Beacons, VHF DXing, Passive Bistatic Radar)*
* **[Chapter 20: AIS 2.0 (VDES): What Is It, Is It Real, and How Does It Work?](part4-space-air-vdes/ch20-ais-2-0-vdes.md)**
  * *ITU-R M.2092-1, 2028 IMO SOLAS Mandate, 307.2 kbps VDE-TER/VDE-SAT Waveforms, PKI Authentication, and IHO S-100 / SECOM Delivery*

---

### Part V: Charting (ENC/ECDIS/S-100), VTS, Agency Software, Training, and Accidents
* **[Chapter 21: Nautical Charts, ECDIS vs. ENC, and the IHO S-100+ Standards](part5-navigation-vts/ch21-nautical-charts-ecdis-enc-and-s100.md)**
  * *Paper/RNC vs. ENC (S-57/S-101) vs. ECS vs. ECDIS (IEC 61174); S-52 AIS Symbology; and Integration with S-100, S-101, S-102 Bathymetry, S-104 Tides, S-111 Currents, S-124, S-212, and S-421*
* **[Chapter 22: Vessel Traffic Services (VTS), Demonstration Programs, and Government Agency Software](part5-navigation-vts/ch22-vts-demonstration-programs-and-agency-software.md)**
  * *VTS Radar+AIS Kalman Fusion, Demonstration Programs, and Government Software (USCG NAIS, Command21, SeaVision, SAROPS, MISLE, AVIS, Minotaur; NOAA ERMA, MarineCadastre; DoD MSSIS, GCCS-M; EMSA SafeSeaNet, Starboard, Skylight)*
* **[Chapter 23: Mariner Training, At-Sea Operations, and AIS-Assisted Accidents](part5-navigation-vts/ch23-mariner-training-operations-and-accidents.md)**
  * *STCW, IMO Model Course 1.34, TOAR, Commercial Fishing vs. Recreational Training; At-Sea Operations (SAR, Rivers, Towing, Pilot Plug PPUs, Wind Farms, Icebreaking); and AIS-Assisted Collisions*

---

### Part VI: Open-Source Decoders, Post-Processing, 3D Blender Visualization, and Spatial Statistics
* **[Chapter 24: Deep Dive into Open-Source AIS Decoding and Encoding Software and Its History](part6-software-analytics/ch24-open-source-ais-decoders-and-encoders.md)**
  * *`noaadata`, `BitVector` / `bitvector-modern`, `aisparser`, `gpsd` & `AIVDM.txt`, `libais` (2010 Deepwater Horizon), `ais-area-notice`, `pyais`, `AIS-catcher`, and Rust Parsers (`nmea-parser`, `ais`)*
* **[Chapter 25: Software for Processing and Visualizing Decoded AIS Messages (`pandas`, `MovingPandas`, `Blender`, `GateHouse`)](part6-software-analytics/ch25-post-processing-software-and-blender-3d.md)**
  * *Open-Source Stack (`pandas`, `geopandas`, `MovingPandas`, `DuckDB`, `MobilityDB`, `GeoParquet`), 3D/4D Spatiotemporal Visualization & Casualty Reconstruction in **Blender** (`bpy`, `BlenderGIS`, Geometry Nodes, `float32` ENU Centering, Msg 5 Antenna-Offset Hull Rigging), and Proprietary Suites (`GateHouse`, `IWRAP`, `Kongsberg`, `Tidalis`, `Kpler`, `Vortexa`, `Windward`)*
* **[Chapter 26: Spatial Statistics and Trajectory Modeling with AIS Data](part6-software-analytics/ch26-spatial-statistics-and-trajectory-modeling.md)**
  * *Correcting for Dynamic Reporting Intervals (2 s vs. 3 min), Terrain Shadowing, Ducting, VDL Packet Loss, and Moving Receivers via Continuous-Time Trajectory Integration and Horvitz-Thompson Estimators over H3 Grids*

---

### Part VII: Security, Spoofing, RF Forensics, National Security, and Alternative Tracking
* **[Chapter 27: Cybersecurity of AIS: Malicious Data, DoS Attacks, and Failure Modes](part7-security-intelligence/ch27-cybersecurity-malicious-data-dos-and-failures.md)**
  * *Balduzzi et al. (2014), Parser Memory Corruption (Bit-Length Overflows, Fragment Exhaustion, CVE-2025-66217, XSS/SQLi), Target-Table Saturation DoS, Protocol MAC Attacks (Msgs 16/17/20/22/23), and Non-Malicious Hardware/Software Failure Modes*
* **[Chapter 28: AIS Spoofing Techniques and Deep RF-Level Hardware Fingerprinting (SEI)](part7-security-intelligence/ch28-spoofing-techniques-and-rf-fingerprinting.md)**
  * *API vs. RF vs. Dual-Transponder Shadow-Fleet vs. GNSS Spoofing; Specific Emitter Identification (PA Ramp Transients, GMSK Phase Error, CFO/Clock Skew, SDR I/Q Imbalance & LO Leakage)*
* **[Chapter 29: National Security, Blue Force Systems, Encryption, and Dark Ships](part7-security-intelligence/ch29-national-security-blue-force-and-dark-ships.md)**
  * *Naval OPSEC (*USS Fitzgerald* & *USS McCain*), Encrypted AIS (EAIS Msg 6/8 & NATO W-AIS), and Unmasking Dark Ships (2025 Johnny Harris / GFW Investigation, Paolo et al. 2024 *Nature*, SAR/VIIRS/RF Fusion)*
* **[Chapter 30: Alternative Ship Tracking (Mobile Phones, SS7/Diameter, VMS, VOS, LRIT), Commodity Traders, and Whale Alert](part7-security-intelligence/ch30-alternative-tracking-ss7-diameter-traders-and-whales.md)**
  * *Coastal Cell Towers, Cellular-at-Sea Picocells, 2G/3G SS7 MAP & 4G/5G Diameter Exploits, Ad-Tech GPS Leaks; VMS, LRIT, NOAA VOS & AMVER; Commodity Traders & Bloomberg Terminal (`BMAP`, `SHIP`, `VSRC`, `VSTK`, `FLET`); and Listen for Whales / Whale Alert*

---

### Part VIII: Exhaustive Message-by-Message (1–27) and Application-Specific Message (ASM) Subtype Deep Dives
* **[Chapter 31: Deep Dive into Messages 1, 2, and 3: Class A Position Reports (Scheduled, Assigned, and Interrogated)](part8-message-deep-dives/ch31-messages-1-2-3-class-a-position-reports.md)**
  * *168-Bit Anatomy, Nonlinear ROT Compression, SOTDMA vs. ITDMA Sub-Messages, Stale Status & Sensor Pathologies, Message 15/16/23 Triggers, Fishing-Buoy & Spoofing Abuses, and Software Support*
* **[Chapter 32: Deep Dive into Messages 4, 10, and 11: Base Station Reports and UTC/Date Synchronization](part8-message-deep-dives/ch32-messages-4-10-11-base-station-and-utc-time.md)**
  * *Base Station Sync State 2, Surveyed EPFDs, Long-Range Msg 27 Control (`Bit 148`), Msg 10/11 Inquiry-Response Storms, WNRO Bugs, Ducting Probing, Frame-Origin Hijacking, and Software Support*
* **[Chapter 33: Deep Dive into Messages 5 and 24: Class A and Class B Static and Voyage-Related Data](part8-message-deep-dives/ch33-messages-5-and-24-static-and-voyage-data.md)**
  * *424-Bit 2-Slot Msg 5 vs. Single-Slot Msg 24 Part A/B, Hull Dimensions & Antenna Offsets (`A, B, C, D`), Auxiliary Craft MMSI Overload, `CVE-2025-66217`, Manual Entry Garbage, Red Sea Signaling, and Software Support*
* **[Chapter 34: Deep Dive into Messages 9, 18, 19, and 27: SAR Aircraft, Class B Position Reports, and Long-Range Satellite AIS](part8-message-deep-dives/ch34-messages-9-18-19-27-aircraft-class-b-and-satellite.md)**
  * *SAR Aircraft Altitude & High-Speed SOG (Msg 9), Class B CSTDMA `0x349B0` vs. SOTDMA (Msg 18), Why 2-Slot Msg 19 Failed, 96-Bit Satellite Msg 27 on Ch 75/76, Polarity Traps, and Software Support*
* **[Chapter 35: Deep Dive into Safety, Interrogation, AtoN, and Data Link Control Messages (Messages 12, 13, 14, 15, 16, 20, 21, 22, and 23)](part8-message-deep-dives/ch35-messages-12-13-14-15-16-20-21-22-23-safety-aton-and-dlc.md)**
  * *Safety Text & Ack (Msgs 12–14), Interrogation (Msg 15), Assigned Mode (Msg 16), FATDMA Reservations (Msg 20), Real/Synthetic/Virtual AtoNs (Msg 21), Channel Management (Msg 22), Group Quiet Time (Msg 23), MAC DoS Exploits, and Software Support*
* **[Chapter 36: Deep Dive into Binary Message Envelopes and DGNSS Broadcasts (Messages 6, 7, 8, 17, 25, and 26)](part8-message-deep-dives/ch36-messages-6-7-8-17-25-26-binary-envelopes-and-dgnss.md)**
  * *Addressed & Broadcast Binary Envelopes (Msgs 6, 7, 8), RTCM SC-104 DGNSS Corrections & Pseudorange Drift Attacks (Msg 17), Single/Multi-Slot Unstructured & Structured Binary (Msgs 25, 26), and Software Support*
* **[Chapter 37: Deep Dive into International ASM Subtypes (`DAC = 1`), Part 1: System Management & IMO SN/Circ.236 Legacy Messages (`FI = 0–21`)](part8-message-deep-dives/ch37-international-asm-subtypes-dac-1-part-1.md)**
  * *System Capability Handshakes (`FI = 0, 2, 3, 4, 5`), Why Legacy Met/Hydro (`FI = 11`) Had Inverted `(Lat, Lon)` & `0.1 m` Tides Yet Still Dominates Traffic, Dangerous Cargo (`FI = 12`), Tidal Windows (`FI = 14`), Air Draught (`FI = 15`), Persons on Board (`FI = 16`), VTS Radar Targets (`FI = 17`), and `FI = 18–21`*
* **[Chapter 38: Deep Dive into International ASM Subtypes (`DAC = 1`), Part 2: IMO SN.1/Circ.289 & Circ.290 Operational Messages (`FI = 22–32`)](part8-message-deep-dives/ch38-international-asm-subtypes-dac-1-part-2.md)**
  * *Dynamic Area Notices (`FI = 22/23`, `ais-area-notice`), Extended Static Ice Class/Power (`FI = 24`), Dangerous Cargo (`FI = 25`), Modular Sensor Reports (`FI = 26`), Route Information (`FI = 27/28`), Linked Text (`FI = 29/30`), Modern Met/Hydro (`FI = 31`), and Tidal Windows (`FI = 32`)*
* **[Chapter 39: Deep Dive into Regional ASM Subtypes, Part 1: European Inland AIS (`DAC = 200`) and UK/Ireland GLA (`DAC = 232 / 235`)](part8-message-deep-dives/ch39-european-inland-and-gla-asm-subtypes.md)**
  * *Inland Ship Data (`DAC=200, FI=10`: ENI, `0.1 m` Convoy Dimensions, ERI Codes, Hazardous Blue Cones, `0.01 m` Draught), Lock ETA/RTA (`FI=21/22`), EMMA Warnings (`FI=23`), Water Levels (`FI=24`), Bridge/Lock Signals (`FI=40`), Persons on Board (`FI=55`), and UK/Ireland GLA AtoN Telemetry (`DAC=232/235, FI=10`)*
* **[Chapter 40: Deep Dive into Regional ASM Subtypes, Part 2: North American Seaway (`DAC = 316 / 366`), USCG / NOAA PORTS®, Encrypted AIS, and the Master Software Support Matrix](part8-message-deep-dives/ch40-north-american-seaway-uscg-and-vdes-asm-subtypes.md)**
  * *St. Lawrence Seaway Lockage & Flow (`DAC=316/366, FI=1, 2, 32, 33, 34`), USCG Area Notices & Whale Alert (`DAC=366, FI=22/23`), NOAA PORTS® / RTCM 12301.1, USCG/DoD Encrypted AIS (`DAC=366, FI=56/57`), VDES ASM Migration, and the Master Software Support Matrix*

---

### Appendices
* **[Appendix A: Complete ITU-R M.1371-5 Message 1–27 Bit-Layout Reference Tables](appendices/appendix-a-message-1-to-27-bit-tables.md)**
* **[Appendix B: Maritime Identification Digits (MID) and MMSI Prefix Lookup Table](appendices/appendix-b-mid-and-mmsi-prefixes.md)**
* **[Appendix C: NMEA 0183 6-Bit ASCII Armor and Checksum Reference](appendices/appendix-c-nmea-6bit-ascii-and-checksum.md)**
* **[Appendix D: International & Regional Binary Application-Specific Messages (DAC/FI) Registry](appendices/appendix-d-binary-asm-dac-fi-registry.md)**
* **[Appendix E: Master Standards Matrix (ITU, IMO, IEC, IALA, IHO, RTCM, NMEA)](appendices/appendix-e-master-standards-matrix.md)**
* **[Appendix F: Landmark Admiralty Court Cases, Statutes, and AIS Patent Index](appendices/appendix-f-court-cases-statutes-and-patents.md)**
* **[Appendix G: Recommended Low-Budget Home AIS Station BOM, Schematics, and Configs](appendices/appendix-g-home-ais-station-bom-and-configs.md)**
* **[Appendix H: Master Bibliography and Verified Citation Index](appendices/appendix-h-master-bibliography.md)**
