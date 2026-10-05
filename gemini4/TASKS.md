# Master Actionable Task List: The Maritime Automatic Identification System (AIS) Handbook

> **Governing Blueprint:** [`PLAN.md`](PLAN.md)
> **Scope:** Phased research, authoring, mathematical modeling, code verification, diagram generation, and citation auditing backlog for all Front Matter, 40 Chapters, 8 Appendices, and accompanying test suites.

---

## 1. Execution Phases and Quality Bar Overview

| Phase | Focus Area | Deliverables | Verification Gate |
|---|---|---|---|
| **Phase 0** | **Scaffolding, Conventions & Bibliography Infrastructure** | Repository layout, `STYLE_GUIDE.md`, Front Matter, BibTeX database, CI test runner | Schema validation & build check |
| **Phase 1** | **Part I: History, Uses, Governance, Standards, Patents & Law** | Chapters 1–4 + Appendices E & F | Cross-check against `schwehr/gis-history`, USPTO reexamination records, and admiralty case citations |
| **Phase 2** | **Part II: RF Physics, Propagation, Physical Layer, Antennas, SDRs & Collection** | Chapters 5–10 + Appendix G | Link-budget math check, GMSK/CRC-16 bit-level DSP tests, Home Station BOM verification |
| **Phase 3** | **Part III: Timing/1PPS, GNSS/Jamming, MMSI, NMEA/N2K/VDR & Messages 1–27/ASM** | Chapters 11–16 + Appendices A, B, C, D | Bit-width summation checks (168/424 bits), NMEA checksum & 6-bit armor unit tests |
| **Phase 4** | **Part IV: Satellite AIS, Airborne/UAV, SAR/DF, Fishing Gear AMRDs, Hacks & VDES** | Chapters 17–20 | Orbital Doppler/footprint calculations, VDE-SAT frequency table verification |
| **Phase 5** | **Part V: Charts (ENC/ECDIS/S-100), VTS, Agency Software, Training & Accidents** | Chapters 21–23 | IHO S-100 edition audit, USCG/NOAA/EMSA software inventory verification |
| **Phase 6** | **Part VI: Open-Source Decoders (`libais` etc.), Processing (`MovingPandas`, `Blender`, `GateHouse`) & Spatial Stats** | Chapters 24–26 | Live code execution across `libais`, `pyais`, Rust `nmea-parser`, `pandas`, `MovingPandas`, `DuckDB`, `Blender` (`bpy`) |
| **Phase 7** | **Part VII: Cybersecurity, Spoofing, RF Fingerprinting, Blue Force, Dark Ships, SS7/Diameter, Traders & Whales** | Chapters 27–30 | CVE verification, Bloomberg `BMAP` command check, Whale Alert Area Notice decoding test |
| **Phase 8** | **End-to-End Code, SDR, and Citation Verification Audit** | Full test suite (`tests/`), `MASTER_BIBLIOGRAPHY.bib`, cross-reference link audit | Zero broken links, zero unverified claims, 100% unit test pass rate |
| **Phase 9** | **Part VIII: Message-by-Message (1–27) & All Known ASM (`DAC/FI`) Subtype Deep Dives** | Chapters 31–40 (`book/part8-message-deep-dives/`) | Every Message 1–27 and every known ASM subtype audited across all 6 required dimensions |

---

## 2. Phase 0: Repository Scaffolding, Front Matter, and Reference Infrastructure

- [x] **TASK-001:** Initialize directory hierarchy (`book/00-front-matter/`, `book/part1-history-governance/`, `book/part2-rf-hardware/`, `book/part3-timing-protocol/`, `book/part4-space-air-vdes/`, `book/part5-navigation-vts/`, `book/part6-software-analytics/`, `book/part7-security-intelligence/`, `book/part8-message-deep-dives/`, `book/appendices/`, `tests/`, `scripts/`).
- [x] **TASK-002:** Draft `book/00-front-matter/notation-and-conventions.md` defining:
  - ITU-R M.1371 MSB-first 1-based vs. 0-based bit indexing (`libais` convention),
  - Two's complement signed integer extraction rules for Longitude (28-bit), Latitude (27-bit), and Rate of Turn (8-bit),
  - RF decibel units ($\text{dBm}$, $\text{dBW}$, $\text{dBi}$, $\text{dBd}$ where $\text{dBi} = \text{dBd} + 2.15$),
  - Geodetic coordinate frames (WGS84 realizations, ECEF, local tangent plane ENU/NED, vessel body frame).
- [x] **TASK-003:** Draft `book/00-front-matter/ais-and-gis-history-timeline.md` synthesizing [`https://github.com/schwehr/gis-history`](https://github.com/schwehr/gis-history) with maritime navigation and AIS milestones (from 206 BCE compass, 1569 Mercator, 1761 Harrison H4, 1904 Radar, 1912 *Titanic* / 1914 SOLAS, 1940–1942 Gee/Decca/LORAN, 1960 UTC, 1978 GPS, 1984 NMEA 0183 & WGS84, 1988 Håkan Lans STDMA patent, 1989 *Exxon Valdez* & OPA-90, **1994 Blender initial release**, 1998 ITU-R M.1371-0 & New Orleans PAWSS, 2000 GPS SA off, 9/11 & MTSA 2002, 2002 SOLAS AIS mandate, **2002 Blender open-sourced under GPL**, **2006–2010 CCOM/UNH `Blender` + Python `noaadata`/`libais` 3D AIS & bathymetry animations**, 2010 *Deepwater Horizon* & `libais`, 2012 WhaleAlert, 2013 "All the Ships", 2016 USCG 65-ft rule & Global Fishing Watch, 2018 MovingPandas & DuckDB, 2020–2021 GeoArrow/GeoParquet, 2023 NorSat-TD/Sternula-1 VDES, 2024 Paolo et al. *Nature*, 2025 GFW Dark Zones, through 2028 SOLAS VDES).
- [x] **TASK-004:** Draft `book/00-front-matter/acronyms-and-glossary.md` covering >450 terms across AIS, RF, GNSS, VTS, ECDIS/S-100, and telecom signaling.

---

## 3. Phase 1: Origins, History, Governance, Standards, Patents, and Law (Part I)

### Chapter 1: Introduction to AIS and the Taxonomy of All AIS Uses
- [x] **TASK-101:** Draft Section 1.1 on the three original IMO/ITU pillars of AIS: (1) Ship-to-ship collision avoidance, (2) Coastal state monitoring, and (3) Vessel Traffic Services (VTS).
- [x] **TASK-102:** Draft Sections 1.2–1.4 cataloging **all uses of AIS data** (including items missing from the initial prompt list):
  - Search and Rescue (AIS-SART, AIS-MOB, EPIRB-AIS, SAR Aircraft Msg 9, AMVER),
  - Aids to Navigation (Real, Synthetic, Virtual AtoNs),
  - Complex at-sea operations (towing, pilotage, dredging, cable/pipe laying, offshore wind CTVs, icebreaking, STS lightering),
  - Subsea cable and pipeline protection (anchor-drag kinematic detection),
  - Environmental disaster response (2010 *Deepwater Horizon* / NOAA ERMA),
  - Marine mammal conservation (**Listen for Whales / Whale Alert**, SMA/DMA speed rules),
  - IUU fisheries enforcement and transshipment monitoring (Global Fishing Watch),
  - Ship exhaust emissions modeling ($\text{CO}_2$, $\text{NO}_x$, $\text{SO}_x$, $\text{PM}$, black carbon via STEAM/ICCT) and Underwater Radiated Noise (URN / JOMOPANS),
  - Real-time tide and hydrographic/meteorological broadcasting (NOAA PORTS®),
  - Commodity trading and macroeconomic indicators (Bloomberg `BMAP`, floating storage, draught-based cargo estimation, IMF PortWatch),
  - Admiralty litigation, casualty forensics, and charter-party arbitration,
  - Sanctions enforcement, dark-fleet detection, and naval MDA,
  - Opportunistic radio science (VHF tropospheric ducting inversion and passive bistatic radar),
  - Marine biosecurity (ballast water & hull biofouling network graphs),
  - **3D/4D Spatiotemporal Visualization, Casualty Reconstruction, and Scientific Animation in Blender** (coupling AIS tracks with multibeam bathymetry, tides, acoustic propagation, and bridge viewsheds).

### Chapter 2: Deep History of Maritime Navigation, Geodesy, and the Birth of AIS
- [x] **TASK-103:** Draft Section 2.1 tracing pre-AIS navigation and spatial history from `schwehr/gis-history` (chronometers, datums, radar, hyperbolic systems Gee/Decca/LORAN/CHAYKA, GPS/GLONASS/BeiDou/Galileo, NMEA 0183, WGS84, DGPS, and the May 2000 termination of GPS Selective Availability).
- [x] **TASK-104:** Draft Section 2.2 on the **March 24, 1989 *Exxon Valdez* oil spill**, the **Oil Pollution Act of 1990 (OPA-90)** mandate for Prince William Sound tanker tracking, and the competing 1980s/1990s prototypes:
  - UK Dover Strait VHF DSC "4S" transponder system,
  - Panama Canal Commission UHF CTAN system,
  - Swedish/Finnish Håkan Lans STDMA VHF system.
  - Cite [Cutlip (2017), *AIS for Safety and Tracking: A Brief History*](https://globalfishingwatch.org/article/ais-brief-history/) and USCG Jorge Arroyo historical briefings.
- [x] **TASK-105:** Draft Sections 2.3–2.4 on the 1998 **ITU-R M.1371-0** standardization, USCG **PAWSS** modernization in **New Orleans** (1998), the December 2000 **SOLAS Chapter V Reg 19** adoption, the **September 11, 2001** pivot to homeland security (**MTSA 2002**, DHS, USCG **NAIS**), the **2009 EU 15m fishing vessel rule**, and the **March 2016 USCG 65-ft commercial/fishing vessel rule** (33 CFR § 164.46).

### Chapter 3: Governance, International Organizations, Treaties, Standards, and Patents
- [x] **TASK-106:** Draft Section 3.1 detailing the roles and institutional histories of **IMO**, **ITU (ITU-R)**, **IALA** (noting its August 2024 elevation to an Intergovernmental Organization), **IHO**, **IEC (TC 80)**, **RTCM (SC-121)**, **NMEA**, **EMSA**, **CCNR**, **USCG**, and **FCC**.
- [x] **TASK-107:** Draft Section 3.2 on key treaties and laws: **UNCLOS** (1982/1994 maritime zones & jurisdiction), **SOLAS** (1914 *Titanic* origins, 1974 convention, Reg 19 continuous operation requirement vs. Master's security discretion), **COLREGs** (Rules 5, 7, 8), **STCW**, **OPA-90**, **MTSA 2002**, and **33 CFR § 164.46**.
- [x] **TASK-108:** Draft Section 3.3 & Appendix E compiling the **Master Standards Matrix** across all ITU-R, IMO, IEC, IALA, IHO, RTCM, and NMEA documents that define or impact AIS.
- [x] **TASK-109:** Draft Section 3.4 on **AIS Patents and Their Expiration**:
  - Detail **Håkan Lans / GP&C Systems International AB**'s **US Patent 5,506,587** (*"Position indicating system"*, priority Sept 9, 1988; filed Oct 28, 1992; granted April 9, 1996) and **EP 0 465 532 B1**.
  - Document the ITU/IMO RAND licensing disputes, litigation involving GateHouse and transceiver manufacturers, and the **USPTO Ex Parte Reexamination Certificate (March 30, 2010) cancelling all claims 1–19 of US Patent 5,506,587**, plus natural 20-year term expiration (2012/2013).
  - Catalog second-generation **Satellite AIS (S-AIS) de-collision and beamforming patents** (exactEarth/Spire, ORBCOMM, Kongsberg, LuxSpace) and their 2027–2035 expiration dates.

### Chapter 4: Legal Issues, Admiralty Court Cases, Casualty Forensics, and Privacy
- [x] **TASK-110:** Draft Section 4.1 analyzing key **Admiralty Court Cases and Casualty Litigation** involving AIS, VDR, ECDIS, and **3D Forensic Reconstruction in Blender**:
  - ***Nautical Challenge Ltd v Evergreen Marine (UK) Ltd (The "Alexandra 1" and "Ever Smart")* [2021] UKSC 6** (UK Supreme Court landmark collision case using AIS/VDR track reconstruction),
  - ***Sakizaya Kalon & Osios David v Panamax Alexander* [2020] EWHC 2604 (Admlty)** (AIS/ECDIS as part of a proper lookout under COLREGs Rule 5),
  - **UK Admiralty Court CPR Part 61 (April 2023 reforms)** on compulsory early disclosure of electronic track data,
  - **Courtroom & NTSB/MAIB 3D Casualty Reconstructions in Blender:** Synchronizing AIS position/heading/ROT keyframes, exact hull meshes rigged to Message 5 GNSS antenna offsets, bridge wing viewsheds (container stack blind sectors), COLREGs navigation light sector cones, multibeam channel bathymetry, and VDR bridge audio,
  - Major casualty & sanctions cases: *Deepwater Horizon* (2010), *Costa Concordia* (2012), *USS Fitzgerald* & *USS John S. McCain* (2017), *MV Wakashio* (2020), *Ever Given* Suez grounding (2021), *MV Dali* Key Bridge collapse (2024), and US DOJ forfeiture cases (*M/T Wise Honest*, *Adrian Darya 1*).
- [x] **TASK-111:** Draft Section 4.2 on **Privacy, Data Protection, and National Restrictions**:
  - Public airwaves vs. national telecom secrecy laws (US 47 U.S.C. § 605 exception for broadcasts for use of the general public vs. UK Wireless Telegraphy Act 2006 s.48),
  - EU **GDPR** implications for small fishing vessels and sole-proprietor pleasure craft MMSIs,
  - **China's 2021 Data Security Law (DSL) & Personal Information Protection Law (PIPL)** blocking foreign access to terrestrial Chinese AIS feeds,
  - Superyacht privacy debates and piracy High Risk Area (HRA) AIS switch-off protocols.

---

## 4. Phase 2: RF Physics, Propagation, Physical Layer, Antennas, SDRs, and Collection Sites (Part II)

### Chapter 5: Maritime VHF RF Fundamentals, Spectrum Allocation, and Shipboard Noise
- [x] **TASK-201:** Draft Section 5.1 cataloging **all RF channels used for AIS and related services**:
  - AIS 1 (Ch 87B, $161.975\text{ MHz}$) & AIS 2 (Ch 88B, $162.025\text{ MHz}$),
  - Long-Range Satellite AIS: Ch 75 ($156.775\text{ MHz}$) & Ch 76 ($156.825\text{ MHz}$),
  - Regional Channel Management (Msg 22) across $156.025\text{–}162.025\text{ MHz}$ (ITU RR Appendix 18),
  - ASM 1 (Ch 2027, $161.950\text{ MHz}$) & ASM 2 (Ch 2028, $162.000\text{ MHz}$),
  - VDES Terrestrial & Satellite channels (Ch 1024/2024, 1084/2084, $160.9625\text{–}161.4875\text{ MHz}$),
  - AMRD Group B non-navigation fishing gear channel: Ch 2006 ($160.900\text{ MHz}$, ITU-R M.2135).
- [x] **TASK-202:** Draft Section 5.2 deriving VHF line-of-sight horizon ($d_{\text{NM}} \approx 2.23(\sqrt{h_t} + \sqrt{h_r})$), Fresnel zone clearance over water, and the two-ray sea-surface multipath interference model.
- [x] **TASK-203:** Draft Section 5.3 on **Noise Sources for AIS on Ships**:
  - Unfiltered PWM/SMPS drivers in LED navigation and deck lights ($150\text{–}170\text{ MHz}$ broadband EMI),
  - Variable Frequency Drives (VFDs) on thrusters/winches/chillers and engine alternators,
  - Co-site front-end desensitization from $25\text{ W}$ VHF voice radios (Ch 16/13), marine radar magnetron harmonics, HF SSB transmitters, and rusty-bolt Passive Intermodulation (PIM).

### Chapter 6: AIS RF Propagation Modeling, Atmospheric Ducting, and Network Loading Studies
- [x] **TASK-204:** Draft Section 6.1 comparing marine VHF propagation models: Free-Space, Two-Ray Curved Earth, **Longley-Rice / Irregular Terrain Model (ITM)**, **ITU-R P.1546**, **ITU-R P.528**, and split-step **Parabolic Equation (PE)** models (**US Navy APM / AREPS / TEMPER**).
- [x] **TASK-205:** Draft Section 6.2 explaining how **AIS is used for RF propagation monitoring and weather model testing**:
  - Physics of evaporation ducts, surface-based ducts, and elevated tropospheric ducts ($dM/dz < 0$),
  - Inverting empirical AIS reception range and RSSI time series between ships and shore stations to estimate atmospheric modified refractivity profiles $M(z)$ and validate NWP models (ERA5, GFS, COAMPS).
- [x] **TASK-206:** Draft Section 6.3 reviewing **published studies on AIS RF propagation, network loading, and packet loss**:
  - **ITU-R Report M.2287-0** (*Assessment of the VHF data link loading*),
  - SOTDMA cell shrinking and slot collision probability curves as VDL loading approaches $50\%\text{–}100\%$,
  - Spaceborne packet collision studies (Hoye et al. 2008; Eriksen et al. 2006/2010; Cervera et al. 2011; Last et al. 2014/2015).

### Chapter 7: AIS Physical Layer: Bit Encoding, HDLC, GMSK, and Salvaging Corrupted RF Recordings
- [x] **TASK-207:** Draft Sections 7.1–7.2 detailing the bit-to-RF transmit chain:
  - 256-bit ($26.667\text{ ms}$) slot structure: 8-bit ramp-up, 24-bit `0101...` training sequence, 8-bit HDLC start flag (`0x7E`), 168-bit payload (LSB-first per byte), 16-bit CRC-CCITT FCS ($x^{16}+x^{12}+x^5+1$), 8-bit end flag (`0x7E`), 24-bit guard/stuffing buffer,
  - Zero-bit stuffing after five consecutive `1` bits,
  - NRZI encoding (`0` = transition, `1` = constant),
  - GMSK modulation ($h = 0.5$, $BT = 0.4$ TX / $0.5$ RX, $\Delta f = \pm 2.4\text{ kHz}$ at $9,600\text{ bps}$).
- [x] **TASK-208:** Draft Section 7.3 on **what can be extracted and salvaged from RF recordings with packet corruption and/or collisions**:
  - Soft-decision syndromic bit-flipping for 1–3 bit CRC-16 failures using demodulator eye-opening confidence and Viterbi trellis decoding,
  - Prior-aided header recovery using known local MMSI catalogs,
  - Partial packet forensics (extracting uncorrupted Message ID + 30-bit MMSI from the first $4.2\text{ ms}$ of a burst whose tail collided),
  - Co-channel collision separation in raw IQ recordings via **Successive Interference Cancellation (SIC)**, capture effect subtraction, and joint Doppler/timing/phase separation.

### Chapter 8: Antenna Engineering and Selection Across Platforms
- [x] **TASK-209:** Draft Chapter 8 analyzing the **best antennas for each application and the physics of why**:
  - **Large Ships:** Heavy fiberglass $\frac{1}{2}\lambda$ dipole or moderate-gain collinear ($3\text{–}5\text{ dBi}$, $35^\circ\text{–}65^\circ$ vertical beamwidth, DC-grounded) to balance $30\text{–}60\text{ m}$ bridge height against vessel roll and stack exhaust corrosion,
  - **Small Ships (Sailboats & Powerboats):** Masthead $\frac{1}{2}\lambda$ whip ($3\text{ dBi}$, wide $78^\circ$ vertical lobe) for sailboats so $25^\circ\text{–}35^\circ$ heeling does not point a narrow collinear beam into the ocean/sky; active zero-loss splitters vs. dedicated antennas,
  - **Very Small Systems (Kayaks, MOB, Fishing Buoys, UAVs, CubeSats):** Normal-mode helical stubbies, nitinol quarter-wave whips using seawater counterpoise, UAV blade monopoles, and CubeSat deployable tape-measure dipoles/Yagis,
  - **Shore AIS Collection Stations:** High-gain omnidirectional exposed-dipole/collinear arrays ($6\text{–}9\text{ dBd}$) and directional **Yagi / Corner Reflector** antennas ($9\text{–}12\text{ dBd}$) paired with low-loss Heliax/LMR-400 coax, cavity filters, and masthead LNAs.

### Chapter 9: Transceiver Hardware, SDRs, and Low-Budget Home AIS Receiver Setup
- [x] **TASK-210:** Draft Sections 9.1–9.2 comparing commercial transceiver architectures (Class A, Class B CSTDMA, Class B+ SOTDMA, Shine Micro, Wegmatt dAISy) and SDR platforms for receive and lab transmit (RTL-SDR Blog V3/V4, Airspy Mini/R2, SDRplay RSPdx, HackRF One, bladeRF, PlutoSDR, Ettus USRP B200/B210).
- [x] **TASK-211:** Draft Section 9.3 & Appendix G providing a complete, tested **Low-Budget Home AIS Receiver Setup Guide**:
  - Hardware BOM (Raspberry Pi 4/5 or thin client, RTL-SDR Blog V4 with 0.5 ppm TCXO or dAISy 2+ HAT, **mandatory $162\text{ MHz}$ SAW bandpass filter**, LMR-400 coax, lightning arrestor, and tuned $162\text{ MHz}$ J-pole/collinear antenna),
  - Step-by-step Linux configuration (`systemd` service for **`AIS-catcher`**, `gpsd`, `Signal K`, `OpenCPN`, and local `DuckDB`/Parquet logging).

### Chapter 10: Shore and At-Sea Collection Site Engineering and Global Networks
- [x] **TASK-212:** Draft Sections 10.1–10.2 on **Shore Collection Options and Places to Strictly Avoid**:
  - Evaluating communication towers, lighthouses, and coastal high-rises, including the **excessive-elevation multi-cell collision paradox** on high mountain peaks,
  - **Places to Avoid — Near Large Radar Installations:** Why S-band/X-band port, airport, and military radars saturate LNAs and burn out receiver front ends,
  - **Places to Avoid — Near NOAA Weather Radio (NWR):** Why continuous $100\text{–}1,000\text{ W}$ broadcasts on **$162.400\text{–}162.550\text{ MHz}$** (only $375\text{ kHz}$ above AIS 2 at $162.025\text{ MHz}$!) completely deafen unfiltered SDRs and marine receivers via ADC overload and phase-noise reciprocal mixing, requiring physical distance and high-Q cavity filters.
- [x] **TASK-213:** Draft Sections 10.3–10.4 on **At-Sea Collection Platforms** (NOAA NDBC buoys, USCG AtoN buoys, Wave Gliders, Saildrones, offshore platforms) and the global ecosystem of commercial, community, and government **AIS Collection Networks** (Spire, ORBCOMM, MarineTraffic/Kpler, VesselFinder, AISHub, USCG NAIS, Volpe MSSIS, EMSA SafeSeaNet, MarineCadastre).

---

## 5. Phase 3: Timing, GNSS Dependencies, MMSI, Buses, and Protocol Internals (Part III)

### Chapter 11: Timing Signals in AIS: Architecture, Practice, Robustness, and Timing Attacks
- [x] **TASK-301:** Draft Sections 11.1–11.3 explaining **how timing signals are passed through AIS and used in practice**:
  - 60-second UTC frame = 2,250 time slots ($26.667\text{ ms}$ each),
  - Why serial NMEA 0183 sentences (`$GPZDA`, `$GPRMC`) have too much jitter/latency for TDMA slot edges, requiring an internal GNSS **1PPS** pulse ($\pm 2.6\text{ }\mu\text{s}$),
  - **Does any hardware not actually use GNSS for timing?** Detail receive-only SDRs, Class B CSTDMA carrier-sense fallback, and shore Base Stations synced to Rubidium/Cesium atomic clocks, IEEE 1588 PTP, or eLORAN,
  - The 4 synchronization states (Sync State 0 Direct UTC $\rightarrow$ State 1 UTC Indirect $\rightarrow$ State 2 Base Station $\rightarrow$ State 3 Peer Mobile Station).
- [x] **TASK-302:** Draft Section 11.4 analyzing **how an adversary can cause an AIS dynamic network to fail by messing with timing**:
  - GNSS 1PPS time-walk spoofing (splitting slot boundaries across adjacent slots),
  - Rogue Base Station (Message 4) slot skewing during GNSS jamming,
  - FATDMA slot starvation (Message 20) and Assigned Mode throttling (Message 16/23).

### Chapter 12: GNSS Systems Overview, Support Matrix, GNSS-Denied Locations, and Jamming
- [x] **TASK-303:** Draft Sections 12.1–12.2 providing an **overview of GNSS systems** (GPS, GLONASS, BeiDou, Galileo, SBAS, MF DGNSS beacons / Msg 17) and a **breakdown of what AIS hardware supports each system**, explicitly answering whether any AIS systems omit GPS support (e.g., domestic Chinese BeiDou-only fishing terminals, Russian GLONASS-only configurations, and surveyed fixed Base Stations).
- [x] **TASK-304:** Draft Sections 12.3–12.4 detailing **what happens to AIS in a GNSS-denied location** (`181°`/`91°` sentinel coordinates, `Time Stamp` seconds `61`/`62`/`63`, dead-reckoning INS fallback, Sync State 2/3 transition) and **GNSS jamming/spoofing impacts and workarounds** (Baltic/Black Sea/Red Sea/Eastern Med incidents; **R-Mode** on VHF/VDES and MF beacons, **eLORAN**, **CRPA** anti-jam antennas, and INS/DVL/Radar-matching integration).

### Chapter 13: What Is an MMSI? Deep Dive into Maritime Identity
- [x] **TASK-305:** Draft Chapter 13 & Appendix B covering the complete **ITU-R M.585-9 MMSI specification**:
  - MID country codes (`201–775`), standard ship stations (`MIDxxxxxx`), Inmarsat trailing-zero rules, group call (`0MIDxxxxx`), coast stations (`00MIDxxxx`), SAR aircraft (`111MIDxxx`), parent-ship craft (`98MIDxxxx`), physical/virtual AtoNs (`99MIDxxxx`), AIS-SART (`970xxyyyy`), AIS-MOB (`972xxyyyy`), EPIRB-AIS (`974xxyyyy`), and AMRD Group B (`979zzzzzz`),
  - Contrast MMSI with permanent **7-digit IMO hull numbers** (including the check-digit equation) and analyze default/colliding MMSIs (`000000000`, `123456789`).

### Chapter 14: Standards for Sharing and Logging AIS: NMEA 0183, NMEA 2000, NMEA TAG Blocks, and VDR
- [x] **TASK-306:** Draft Sections 14.1–14.3 & Appendix C detailing:
  - **NMEA 0183 / IEC 61162-1/2:** RS-422 electrical interface, `!AIVDM` vs. `!AIVDO`, talker IDs, multi-sentence fragmentation, 6-bit ASCII armor table, fill bits, and XOR checksum calculation,
  - **NMEA TAG Blocks:** `\s:...,c:...,g:...*HH\` syntax, UNIX timestamps, station provenance, RSSI extensions, and multi-line group reassembly,
  - **NMEA 2000 (IEC 61162-3) & IEC 61162-450 (LWE):** CAN bus PGNs (`129038`–`129810`), Fast-Packet framing, unit-conversion fidelity traps between NMEA 0183 and NMEA 2000, and UDP multicast Lightweight Ethernet.
- [x] **TASK-307:** Draft Section 14.4 on **Voyage Data Recorders (VDR and S-VDR)**:
  - IMO MSC.333(90) and IEC 61996-1/2 requirements, fixed vs. float-free capsules, and forensic extraction of `!AIVDM`/`!AIVDO` streams synchronized with bridge audio and ECDIS screenshots.

### Chapter 15 & Chapter 16: Complete Message Catalog (1–27), Binary ASMs, Tides, and Area Notices
- [x] **TASK-308:** Draft Chapter 15 & Appendix A providing the bit-level specification for **all 27 ITU-R M.1371-5 messages**, including explicit formulas for nonlinear Rate of Turn ($ROT_{\text{AIS}} = 4.733\sqrt{\text{ROT}_{\^\circ/\text{min}}}$), hull dimension antenna offsets, and SOTDMA/ITDMA communication state sub-fields.
- [x] **TASK-309:** Draft Chapter 16 & Appendix D covering **Binary Application-Specific Messages (Msgs 6, 8, 25, 26)**, **Tide and Marine State Transmissions** (IMO SN.1/Circ.289 DAC 1 FI 11 & FI 31 Met/Hydro, **NOAA PORTS®**, St. Lawrence Seaway DAC 316/366, **RTCM 12301.1**), and **Area Notices** (DAC 1 FI 22 / USCG DAC 366 FI 22 sub-area geometry encoding in `ais-area-notice`).

---

## 6. Phase 4: Spaceborne, Airborne, SAR/DF, Fishing Gear, User Hacks, and AIS 2.0/VDES (Part IV)

### Chapter 17: Satellite AIS (S-AIS): Reception, Processing, and Satellite Transmission
- [x] **TASK-401:** Draft Sections 17.1–17.2 analyzing **how satellites receive and process AIS RF**:
  - Orbital footprint geometry ($>2,500\text{ km}$ horizon radius encompassing hundreds of SOTDMA cells), co-channel packet collisions, $\pm 3.8\text{ kHz}$ Doppler shift, $7.2\text{ ms}$ slant-range delay spread, Faraday rotation, **Message 27** on Channels 75/76, and onboard/ground multi-antenna IQ de-collision algorithms.
- [x] **TASK-402:** Draft Section 17.3 answering **"Have satellites ever transmitted AIS?"**:
  - Explain why transmitting standard AIS 1/2 from LEO disrupts terrestrial SOTDMA timing across cells,
  - Document experimental satellite-to-ship ASM broadcast trials (**NorSat-2**, 2017) and operational **two-way VDE-SAT (AIS 2.0)** satellite downlink transmissions aboard **NorSat-TD** and **Sternula-1** (launched 2023).

### Chapter 18: AIS in Aircraft, Drones, Search and Rescue, and Direction Finding
- [x] **TASK-403:** Draft Sections 18.1–18.2 on **AIS in Aircraft and Drones (UAVs)** (Message 9 SAR Aircraft format, USCG Minotaur / Navy P-8 / MQ-9 SeaGuardian / ScanEagle / Camcopter airborne collection, and high-altitude multi-cell collision horizons) and **SAR Beacons** (AIS-SART, AIS-MOB, EPIRB-AIS).
- [x] **TASK-404:** Draft Section 18.3 on **AIS and Direction Finding (DF) Systems**:
  - VHF Doppler and Adcock/Watson-Watt RDF arrays for SAR homing on AIS-SART/MOB and for **counter-spoofing verification** (comparing physical RF Angle-of-Arrival against reported payload coordinates).

### Chapter 19: AIS for Fishing Gear, AMRDs, and Unintended User Hacks
- [x] **TASK-405:** Draft Section 19.1 on **AIS for Fishing Gear**:
  - Proliferation of uncertified high-power net buoys / sun-buoys on longlines, gillnets, and FADs; VDL slot congestion and bridge CPA alarm fatigue; and the **ITU-R M.2135 (AMRD Group A vs. Group B on $160.900\text{ MHz}$ Ch 2006)** regulatory framework.
- [x] **TASK-406:** Draft Section 19.2 cataloging **unintended user hacks of the AIS system**:
  - Free text messaging/status codes in Message 5 `Destination` (`"ARMED GUARDS ON BOARD"`, `"FOR ORDERS"`) and Message 14,
  - Spoofed track-art and geopolitical messages on web aggregators,
  - DIY yacht tender anti-theft tracking and oceanographic drifters,
  - Amateur radio VHF tropospheric ducting ("AIS DXing") monitors,
  - Passive bistatic radar using AIS signals as illuminators of opportunity.

### Chapter 20: AIS 2.0 (VDES): What Is It, Is It Real, and How Does It Work?
- [x] **TASK-407:** Draft Chapter 20 detailing **AIS 2.0 / VDES (ITU-R M.2092-1)**:
  - Confirm its real operational and regulatory status (IMO SOLAS Chapter V amendments entering into force **January 1, 2028**),
  - Detail the 4 VDES sub-systems (AIS + ASM + VDE-TER + VDE-SAT), $\pi/4$-QPSK / 16-QAM modulation up to $307.2\text{ kbps}$, PKI authentication, and IEC 63173-2 (SECOM) S-100 data delivery.

---

## 7. Phase 5: Charting (ENC/ECDIS/S-100), VTS, Agency Software, Training, and Accidents (Part V)

### Chapter 21: Nautical Charts, ECDIS vs. ENC, and the IHO S-100+ Standards
- [x] **TASK-501:** Draft Sections 21.1–21.2 explaining **Nautical Charts** and the legal/technical distinctions between **ENC** (the official S-57/S-101 hydrographic database), **RNC** (raster charts), **ECS** (non-SOLAS chartplotters), and **ECDIS** (the IMO MSC.232(82)/MSC.530(106) & IEC 61174 certified bridge system), plus S-52 AIS target symbology.
- [x] **TASK-502:** Draft Section 21.3 explaining **how AIS works with the new IHO S-100+ standards**:
  - Integration of AIS/VDES with **S-101 (ENC)**, **S-102 (Bathymetric Surface)**, **S-104 (Water Level / Tides)**, **S-111 (Surface Currents)**, **S-124 (Navigational Warnings)**, **S-212 (VTS Digital Service)**, and **S-421 (Route Exchange)** for dynamic Under-Keel Clearance (UKC) and route conflict de-escalation.

### Chapter 22: Vessel Traffic Services (VTS), Demonstration Programs, and Government Software
- [x] **TASK-503:** Draft Sections 22.1–22.2 on **how VTS uses AIS** (IALA G1082 / V-128, INS/TOS/NAS services, Kalman-filtered Radar + AIS target fusion, Virtual AtoN deployment, and Base Station control messages) and **historical/modern AIS demonstration programs** (Panama Canal, Dover Strait, PAWSS New Orleans, St. Lawrence Seaway, NOAA PORTS®, Stellwagen Bank Right Whales, MONALISA/STM, NorSat-TD/Sternula).
- [x] **TASK-504:** Draft Section 22.3 detailing **what software the US Coast Guard and other government agencies use for AIS**:
  - **USCG:** **NAIS**, **Command21 / WatchKeeper**, **SeaVision** (Volpe), **SAROPS**, **MISLE**, **AVIS**, **ECDIS-N**, and **Minotaur** (airborne ISR),
  - **NOAA:** **ERMA®**, **MarineCadastre.gov** (with BOEM), **Whale Alert / CetSound**,
  - **DoD / US Navy / ONI:** **MSSIS** (Volpe global sharing network), **GCCS-M**, **SeaLink**,
  - **International:** **EMSA SafeSeaNet & Integrated Maritime Services (IMS)**, **Starboard Maritime Intelligence** (NZ/Australia/EMSA), Canadian Coast Guard **INNAV**, Australian **AMSA CTS**, and **Skylight**.

### Chapter 23: Mariner Training, At-Sea Operations, and AIS-Assisted Accidents
- [x] **TASK-505:** Draft Sections 23.1–23.2 comparing **how mariners are trained to use AIS and how that training varies** (STCW Table A-II/1, **IMO Model Course 1.34**, IMO 1.27 ECDIS, USCG TOAR for towboats, commercial fishing pragmatism, and untrained recreational Class B users, plus IALA V-103 for VTS operators) and analyzing **at-sea operations where AIS is indispensable** (SAR, inland river bends, tug/tow, pilotage PPUs via Pilot Plug, dredging, cable laying, offshore wind CTVs, icebreaking).
- [x] **TASK-506:** Draft Section 23.3 analyzing **AIS-Assisted Incidents and Accidents**:
  - Case studies of VHF "negotiation by name" contravening COLREGs, over-reliance on stale/unverified AIS COG/SOG vectors instead of ARPA radar plotting and visual bearings, and muted guard-zone alarm fatigue.

---

## 8. Phase 6: Open-Source Decoders, Post-Processing Software, and Spatial Statistics (Part VI)

### Chapter 24: Deep Dive into Open-Source AIS Decoding and Encoding Software and Its History
- [x] **TASK-601:** Draft Sections 24.1–24.3 tracing the history, architecture, and code internals of open-source AIS decoders and encoders:
  - **`noaadata`** (Kurt Schwehr, early pure-Python decoder/encoder for AIS and NOAA PORTS water levels),
  - **`BitVector` & `bitvector-modern`** (bit-array slicing mechanics and why pure-Python bit slicing hit a throughput wall at scale),
  - **`aisparser`** (Brian C. Lane, portable ANSI C parser),
  - **`gpsd` & `AIVDM.txt`** (Eric S. Raymond, Kurt Schwehr, Brian C. Lane, Gary Miller — C daemon decoder and the canonical open specification of AIS bit layouts),
  - **`libais`** (Kurt Schwehr — born during the April 2010 *Deepwater Horizon* oil spill response to decode millions of messages/sec in C++ for NOAA ERMA and later Global Fishing Watch),
  - **`ais-area-notice`** (Kurt Schwehr — IMO SN.1/Circ.289 & USCG Area Notice binary message encoder/decoder and GIS converter),
  - **`pyais`** (Leon Morten Richter) and **`AIS-catcher`** (Jasper Vries).
- [x] **TASK-602:** Draft Sections 24.4–24.5 examining **Rust-Based AIS Parsers** (`nmea-parser` crate, `ais` crate, `nom`/`bitvec` zero-copy parsing, memory safety against malformed bit-lengths, WebAssembly compilation, and PyO3/Arrow batch bindings) and running a reproducible throughput/coverage benchmark across C, C++, Python, and Rust libraries.

### Chapter 25: Software for Processing and Visualizing Decoded AIS Messages (Open Source, 3D/4D Blender, and Proprietary)
- [x] **TASK-603:** Draft Section 25.1 with working code pipelines for the **open-source post-decoding software ecosystem**:
  - **`pandas` & `geopandas`** (vectorized cleaning, kinematic velocity filtering, spatial joins),
  - **`MovingPandas`** (Anita Graser — `TrajectoryCollection`, `StopSplitter`, `ObservationGapSplitter`, `DouglasPeuckerGeneralizer`, `TrajectoryStopDetector`, `TrajectoryAggregator`),
  - **`DuckDB` (Spatial + H3)**, **`PostGIS` / `MobilityDB`**, **`Apache Sedona`**, **`GeoArrow`**, and **`GeoParquet`**.
- [x] **TASK-604:** Draft Section 25.2 on **3D/4D Spatiotemporal Visualization, Casualty Reconstruction, and Scientific Rendering with Blender (`bpy`, `BlenderGIS`, and Geometry Nodes)**:
  - **Historical Context (`schwehr/gis-history`):** Trace Blender's 1994 initial release, its **2002 open-sourcing under the GPL** (the same year as the SOLAS AIS mandate), and Kurt Schwehr's 2006–2010 pioneering work at **UNH CCOM/JHC** coupling Python (`noaadata` / `libais`) with Blender's `bpy` API to animate 3D ship traffic, multibeam bathymetry, and Stellwagen Bank right-whale conservation zones,
  - **Mitigating `float32` Precision Jitter:** Formulate the local tangent plane (ENU) / centered UTM offset transformation $(x' = x - x_0,\; y' = y - y_0,\; z' = z - z_0)$ via `pyproj` and `BlenderGIS` so sub-meter ship kinematics do not jitter in Blender's single-precision `float32` viewport and mesh buffers,
  - **Parametric Hull Scaling & GNSS Antenna-Offset Rigging:** Write a reproducible `bpy` script that reads AIS Message 5 / 24 dimensions (`to_bow` $A$, `to_stern` $B$, `to_port` $C$, `to_starboard` $D$, `draught`), scales a 3D vessel mesh to $L = A+B$ and $W = C+D$, and offsets the mesh vertices relative to the object origin so the pivot point sits at the exact physical GNSS antenna location on the ship,
  - **4D Kinematic Keyframing (COG vs. True Heading Leeway):** Animate translation splines (`BEZIER`/`HERMITE`) from SOG/COG alongside independent yaw (`rotation_euler.z`) from True Heading and Rate of Turn (ROT) to visualize crabbing/leeway angles during cross-current maneuvers and casualties (*Ever Given*, *MV Dali*), plus procedural **Geometry Nodes** instancing for multi-thousand-vessel port scenes,
  - **3D Bridge Viewshed Raycasting, COLREGs Light Arcs, and UKC/Acoustic Volumes:** Configure bridge wing cameras (`bvhtree.ray_cast`) for container-stack blind-sector analysis, boolean cone meshes for COLREGs navigation light sectors ($112.5^\circ$ sidelights, $225^\circ$ masthead, $135^\circ$ stern), 3D Under-Keel Clearance (UKC) visualization over S-102 bathymetry and S-104/PORTS® tides, and volumetric Cycle/EEVEE shaders for underwater radiated noise (URN) and VHF propagation lobes.
- [x] **TASK-605:** Draft Section 25.3 profiling **proprietary AIS processing software**:
  - **GateHouse Maritime:** Deep dive into GateHouse's AIS Base Station Controller, national network mediation/deduplication engine (IALA A-124), **IWRAP Mk II** collision/grounding risk modeling software, and OceanIO,
  - Enterprise VTS, GIS, and intelligence suites: **Kongsberg (C-Scope / K-Sim / TerraLens)**, **Tidalis (Saab/HITT VTMIS)**, **Wärtsilä Transas**, **Esri (ArcGIS Maritime / Velocity)**, **Kpler / MarineTraffic**, **Vortexa**, **Windward**, **Spire Maritime**, and **Starboard**.

### Chapter 26: Spatial Statistics and Trajectory Modeling with AIS Data
- [x] **TASK-606:** Draft Chapter 26 establishing the mathematical framework for **spatial statistics on AIS data**:
  - Formulate corrections for SOTDMA dynamic reporting intervals (2 s vs. 3 min), terrain blockage, anomalous tropospheric ducting, VDL slot collisions, uneven coastal station geometry, and moving satellite/airborne/ASV receivers,
  - Derive **continuous-time trajectory residence-time (vessel-hours)** and **Horvitz-Thompson inverse-probability-of-detection** estimators over equal-area projections and **Uber H3** hexagonal grids, with reproducible Python (`MovingPandas` + `DuckDB` + `h3`) examples.

---

## 9. Phase 7: Security, Spoofing, RF Forensics, National Security, and Alternative Tracking (Part VII)

### Chapter 27: Cybersecurity of AIS: Malicious Data, DoS, and Failure Modes
- [x] **TASK-701:** Draft Sections 27.1–27.2 analyzing **whether malicious data can be sent over AIS to ships and shore systems to cause DoS or corruption, and documenting known issues**:
  - Synthesize **Balduzzi et al. (2014)** (*"A Security Evaluation of AIS"*),
  - Detail **software parser memory corruption & crashes:** payload bit-length truncation/overrun attacks against unchecked C/C++ decoders, multi-sentence fragment queue exhaustion (`!AIVDM,9,1...` floods), **CVE-2025-66217** (heap buffer overflow via integer underflow in `AIS-catcher` < v0.64), and SQLi/XSS payloads embedded in 6-bit ASCII `Vessel Name`/`Destination` fields,
  - Detail **hardware & bridge display DoS:** flooding 500+ fake MMSIs to overflow MKD/ECDIS/ARPA target tables (dropping real ships from the screen),
  - Detail **protocol-level MAC DoS:** forged Base Station **Message 22** (commanding ships in a region to switch to dead VHF channels), **Message 23** (enforcing quiet/silent intervals), **Message 16** (assigned rate throttling), **Message 20** (FATDMA slot reservation starvation), and **Message 17** (DGNSS correction poisoning).
- [x] **TASK-702:** Draft Section 27.3 cataloging **non-malicious failure modes of AIS hardware and software** (high antenna VSWR / corroded coax, blown splitter diodes, TCXO frequency drift, GPS Week Number Rollover [1999/2019/2038], frozen gyro heading inputs, and unentered `0` hull dimensions).

### Chapter 28: AIS Spoofing Techniques and Deep RF-Level Hardware Fingerprinting (SEI)
- [x] **TASK-703:** Draft Section 28.1 categorizing **AIS spoofing techniques** (aggregator UDP/API injection vs. SDR RF transmission, MMSI/IMO identity laundering, dual-transponder "anchor-loop" shadow-fleet spoofing, and GNSS L1 spoofing inducing circular/displaced AIS tracks).
- [x] **TASK-704:** Draft Section 28.2 detailing **techniques for deep diving into the RF level of individual systems (Specific Emitter Identification / RF Fingerprinting)**:
  - Explain how high-sample-rate IQ recordings capture unique hardware signatures: PA turn-on/turn-off transients ($833\text{ }\mu\text{s}$ ramp envelope), GMSK Gaussian filter $BT$ and phase trajectory errors, joint Carrier Frequency Offset (CFO) vs. symbol-clock skew, and direct-conversion SDR I/Q imbalance & LO leakage (distinguishing a HackRF/PlutoSDR spoofer from a certified Furuno/JRC/Saab Class A unit and identifying specific individual transceivers).

### Chapter 29: National Security, Blue Force Systems, Encryption, and Dark Ships
- [x] **TASK-705:** Draft Sections 29.1–29.2 covering **National Security Aspects of AIS**, naval OPSEC lessons from the 2017 *USS Fitzgerald* and *USS McCain* collisions, and **Blue Force Systems & Encrypted AIS (EAIS)** (USCG/DoD Type 1 / AES-256 encrypted payloads encapsulated in Binary Messages 6 and 8, plus NATO Warship AIS tactical MMSI rotation).
- [x] **TASK-706:** Draft Section 29.3 on **Dark Ships and Global Fishing Watch**:
  - Analyze the **2025 Johnny Harris / Global Fishing Watch investigation** ([`https://youtu.be/2tuS1LLOcsI`](https://youtu.be/2tuS1LLOcsI)) and **Paolo et al. (2024, *Nature*)**,
  - Explain gap-analysis modeling (separating RF coverage dropouts from intentional switching-off) and multi-sensor SAR + optical + VIIRS + RF dark-vessel detection.

### Chapter 30: Alternative Ship Tracking (Mobile Phones, SS7/Diameter, VMS, VOS, LRIT), Commodity Traders, and Whale Alert
- [x] **TASK-707:** Draft Section 30.1 on **Tracking Ships via Mobile Phones, RF Emissions, and Telecom Signaling (SS7 and Diameter)**:
  - Coastal cell tower attachments (Timing Advance & AoA) and **onboard Maritime Cellular Networks ("Cellular-at-Sea" picocells)** backhauled via satellite,
  - **2G/3G SS7 MAP exploits** (`AnyTimeInterrogation`, `ProvideSubscriberInfo`, `SendRoutingInfoForSM`) and **4G/5G Diameter exploits** (`S6a`/`S6d` `Insert-Subscriber-Data-Request` / `Location-Information-Request`) returning the visited coastal Cell Global Identity (CGI/ECGI) or shipboard picocell MSC/MME for crew phone numbers,
  - Commercial mobile app **ad-tech SDK (RTB) GPS leaks** from crew smartphones on deck, and airborne/spaceborne cellular/Wi-Fi/satphone RF emission geolocation.
- [x] **TASK-708:** Draft Section 30.2 comparing **VMS (Vessel Monitoring System)** for fisheries, **LRIT (Long-Range Identification and Tracking, SOLAS Reg 19-1)**, and **NOAA VOS (Volunteer Observing Ship) & USCG AMVER** weather/SAR reporting systems.
- [x] **TASK-709:** Draft Section 30.3 providing a **detailed look at Commodity Traders and the Bloomberg Terminal**:
  - Cite and analyze the University of Scranton Alperin Financial Center *Bloomberg Training Manual* ([`https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf`](https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf)),
  - Detail Bloomberg Terminal functions **`BMAP <GO>`**, **`SHIP <GO>`**, **`VSRC <GO>`**, **`VSTK <GO>`**, **`FLET <GO>`**, **`AHOY <GO>`**, and **`FIXS <GO>`**, alongside Kpler and Vortexa algorithms for estimating oil/LNG/grain cargo volumes from AIS draught changes ($\Delta \text{Draught} \times \text{TPC}$), floating storage, and ship-to-ship (STS) transfers.
- [x] **TASK-710:** Draft Section 30.4 on **Listen for Whales / Whale Alert**:
  - Trace the history of Whale Alert (2012 US Congress presentation in `schwehr/gis-history`), acoustic detection buoys (WHOI/Cornell DMONs), **AIS Area Notice (`ais-area-notice` Msg 8 DAC 366/1 FI 22)** broadcasts to shipboard ECDIS and the Whale Alert app, **3D Blender animations of Stellwagen Bank vessel traffic, right-whale foraging dives, and DMON acoustic detection spheres**, and automated AIS enforcement of the 10-knot North Atlantic Right Whale speed rule.

---

## 10. Phase 8: Code Verification Suite and Final Citation Audit

- [x] **TASK-801:** Create `tests/test_nmea_and_bit_decoding.py` verifying NMEA 0183 XOR checksum calculation, 6-bit ASCII armor packing/unpacking, two's complement coordinate decoding, nonlinear ROT conversion, and IMO 7-digit check-digit validation.
- [x] **TASK-802:** Create `tests/test_trajectory_spatial_stats.py` testing time-weighted residence-time integration and Horvitz-Thompson inverse-detection-probability weighting against synthetic multi-rate AIS trajectories.
- [x] **TASK-803:** Create `tests/test_blender_ais_rigging.py` verifying local-tangent-plane (ENU) `float32`-safe coordinate centering, Message 5/24 hull dimension scaling ($L = A+B$, $W = C+D$), GNSS antenna-reference-point pivot offset calculation, and COG vs. True Heading crabbing angle transformation for Blender (`bpy`) scene generation.
- [x] **TASK-804:** Compile `book/appendices/appendix-h-master-bibliography.md` and `MASTER_BIBLIOGRAPHY.bib` ensuring every standard, patent, court case, software repository, video, and peer-reviewed paper cited across all 40 chapters has a verified DOI or canonical URL.

---

## 11. Phase 9: Exhaustive Message-by-Message (1–27) and Application-Specific Message (ASM) Subtype Deep Dives (Part VIII)

- [x] **TASK-901:** Draft **Chapter 31** (`book/part8-message-deep-dives/ch31-messages-1-2-3-class-a-position-reports.md`) providing a deep dive into **Messages 1, 2, and 3 (Class A Position Reports — Scheduled, Assigned, and Interrogated)**:
  - How each message works (168-bit layout, Nav Status `0–15`, nonlinear `ROT` compression $\pm 4.733\sqrt{|\omega|}$, `SOG`, `Lon/Lat`, `COG`, `HDG`, `Time Stamp 0–63`, Inland `Maneuver Indicator`, `RAIM`, and 19-bit SOTDMA vs. ITDMA Communication State sub-messages),
  - Known issues (coordinate quantization jitter, `102.2 kt` SOG ceiling, stale manual Nav Status, disconnected gyro `511` / ROT `-128`, 60-second timestamp ambiguity, and the Message 2 rarity paradox),
  - Relationships to other messages (MMSI join with Msg 5, triggering by Msg 15/16/23, AIS-SART pairing with Msg 14),
  - Known uses and abuses (~65–75% of global VDL traffic, fishing net-buoy squatting, shadow-fleet dual-transponder spoofing, C4ADS GNSS circular spoofing),
  - Where and when used, and complete software support matrix (`libais` `Ais1_2_3`, `gpsd`, `pyais`, `aisparser`, Rust crates, NMEA 2000 PGN `129038`, ECDIS/VTS).
- [x] **TASK-902:** Draft **Chapter 32** (`book/part8-message-deep-dives/ch32-messages-4-10-11-base-station-and-utc-time.md`) providing a deep dive into **Messages 4, 10, and 11 (Base Station Reports and UTC/Date Synchronization)**:
  - How each message works (168-bit Msg 4 & Msg 11 UTC Year/Month/Day/Hour/Min/Sec, Surveyed EPFD `7`, Long-Range Msg 27 Control `Bit 148`, SOTDMA vs. ITDMA state; 72-bit Msg 10 addressed inquiry),
  - Known issues (`0°,0°` unconfigured shore coordinates, GPS WNRO date rollovers, Msg 10/11 VDL inquiry storms),
  - Relationships to other messages (Sync State 2 fallback, Base Station MMSI anchor for Msg 20 FATDMA offsets, Msg 27 suppression via `Bit 148`, Msg 10 $\rightarrow$ Msg 11 pairing),
  - Known uses and abuses (10-second shore cadence, VHF tropospheric ducting probing, rogue Msg 4 frame-origin hijacking and Msg 27 suppression attacks),
  - Where and when used, and complete software support matrix (`libais` `Ais4_11` & `Ais10`, `gpsd`, `pyais`, NMEA 2000 PGNs `129793`/`129804`, chartplotter rendering quirks).
- [x] **TASK-903:** Draft **Chapter 33** (`book/part8-message-deep-dives/ch33-messages-5-and-24-static-and-voyage-data.md`) providing a deep dive into **Messages 5 and 24 (Class A and Class B Static and Voyage-Related Data, Part A & Part B)**:
  - How each message works (424-bit 2-slot Msg 5: `IMO`, `Call Sign`, `Name`, `Ship Type 0–99`, `Dimensions A/B/C/D`, `EPFD`, `ETA`, `Draught`, `Destination`, `DTE`; 160/168-bit single-slot Msg 24 Part A & Part B, including the overloaded `Dimensions / Mothership MMSI` field `bits[132:162]` for `98MIDxxxx` craft),
  - Known issues (unauthenticated multi-fragment `!AIVDM` reassembly collisions, **CVE-2025-66217 `libais` heap overflow on truncated `<420-bit` Msg 5**, manual entry garbage in `Destination`/`Draught`, `25.5 m` draught ceiling, `511 m / 63 m` dimension caps, and ITU-R M.1371-3 vs. M.1371-4/5 Vendor ID bit-width mismatch),
  - Relationships to other messages (stateful MMSI join with Msgs 1/2/3/18/27, Msg 19 legacy equivalence, Msg 15 interrogation response),
  - Known uses and abuses (6-minute cadence, commodity trading draught/destination extraction, 3D Blender hull rigging, Red Sea anti-attack signaling in `Destination`, flag-hopping / IMO-mismatch detection),
  - Where and when used, and complete software support matrix (`libais` `Ais5` & `Ais24`, `gpsd`, `pyais`, Rust crates, NMEA 2000 PGNs `129794`, `129809`, `129810`).
- [x] **TASK-904:** Draft **Chapter 34** (`book/part8-message-deep-dives/ch34-messages-9-18-19-27-aircraft-class-b-and-satellite.md`) providing a deep dive into **Messages 9, 18, 19, and 27 (SAR Aircraft, Class B Standard & Extended Position Reports, and Long-Range Satellite AIS)**:
  - How each message works (168-bit Msg 9 with 12-bit `Altitude 0–4094 m` & whole-knot `SOG 0–1022 kts`; 168-bit Msg 18 with `CS` flag & constant `0x349B0` ITDMA state; 312-bit 2-slot Msg 19; 96-bit $9.6\text{ ms}$ Msg 27 on Ch 75/76),
  - Known issues (Msg 9 `4,094 m` altitude overflow for high-altitude patrol aircraft; Msg 18 lack of `ROT`/`Nav Status` & 30-second stale vector trap; Msg 19 2-slot CSTDMA collision deprecation; Msg 27 `GNSS Position Status` polarity inversion & `185 m` coordinate quantization),
  - Relationships to other messages (Msg 18 + Msg 24 superseding Msg 19; Msg 4 `Bit 148` suppressing Msg 27; Msg 22/23 controlling Class B),
  - Known uses and abuses (USCG/EMSA SAR aircraft `111MIDxxx`, recreational/workboat tracking, uncertified fishing buoys abusing Msg 18/19, satellite open-ocean de-collision via Msg 27),
  - Where and when used, and complete software support matrix (`libais` `Ais9`, `Ais18`, `Ais19`, `Ais27`, `gpsd`, `pyais`, `AIS-catcher`, NMEA 2000 PGNs `129798`, `129039`, `129040`).
- [x] **TASK-905:** Draft **Chapter 35** (`book/part8-message-deep-dives/ch35-messages-12-13-14-15-16-20-21-22-23-safety-aton-and-dlc.md`) providing a deep dive into **Safety, Interrogation, AtoN, and Data Link Control Messages (Messages 12, 13, 14, 15, 16, 20, 21, 22, and 23)**:
  - How each message works (Msgs 12, 13, 14 safety text & ack; Msg 15 interrogation; Msg 16 assigned mode; Msg 20 FATDMA slot reservation; Msg 21 Real/Synthetic/Virtual AtoN `272–360 bits` with `Name Extension`; Msg 22 channel management; Msg 23 group assignment & `Quiet Time`),
  - Known issues (non-6-bit-aligned text lengths, Msg 21 variable-length `Name Extension` parser crashes, unauthenticated MAC control commands),
  - Relationships to other messages (Msg 12 $\leftrightarrow$ Msg 13; AIS-SART Msg 1 + Msg 14; Msg 15 $\rightarrow$ Msg 3/5/24; Msg 16/23 $\rightarrow$ Msg 2; Msg 4 + Msg 20 FATDMA anchoring),
  - Known uses and abuses (SART active text, VTS Virtual AtoN wreck marking, fishing-buoy Msg 21 squatting, Balduzzi et al. fake safety phishing, **FATDMA slot-starvation DoS [Msg 20]**, **Frequency-Hopping Hijack [Msg 22]**, and **Quiet-Time Silencing DoS [Msg 23]**),
  - Where and when used, and complete software support matrix (`libais` `Ais12`–`Ais23`, `gpsd`, `pyais`, NMEA 2000 PGNs `129041`, `129801`, `129802`, ECDIS/VTS).
- [x] **TASK-906:** Draft **Chapter 36** (`book/part8-message-deep-dives/ch36-messages-6-7-8-17-25-26-binary-envelopes-and-dgnss.md`) providing a deep dive into **Binary Message Envelopes and DGNSS Broadcasts (Messages 6, 7, 8, 17, 25, and 26)**:
  - How each message works (Msg 6 addressed binary + Msg 7 ack; Msg 8 broadcast binary up to 5 slots / 1,008 bits with 16-bit `DAC/FI`; Msg 17 DGNSS broadcast encapsulating 24-bit RTCM SC-104 Type 1/9 words; Msg 25 single-slot & Msg 26 multi-slot binary with the 4-mode `Addressed`/`Structured` header matrix and trailing 20-bit Comm State),
  - Known issues (multi-slot VDL and satellite collision vulnerability on 3–5 slot frames, Msg 25/26 header bit-shift complexity, parser misalignments of Msg 26's trailing 20-bit Comm State),
  - Relationships to other messages (Msg 6 $\leftrightarrow$ Msg 7 + `DAC=1, FI=5` application ack; Msg 20 FATDMA protection for multi-slot Msg 8/17; Msg 17 feeding internal EPFD `DGNSS` corrections),
  - Known uses and abuses (carrying all international/regional ASM payloads, coastal sub-meter DGNSS corrections, **spoofed Msg 17 RTCM pseudorange drift attacks**, covert unstructured telemetry in Msg 25, and multi-slot buffer-overflow attacks),
  - Where and when used, and complete software support matrix (`libais` `Ais6`, `Ais7_13`, `Ais8`, `Ais17`, `Ais25`, `Ais26`, `gpsd`, `pyais`, Wireshark, NMEA 2000 PGNs `129792`, `129795`, `129796`, `129797`).
- [x] **TASK-907:** Draft **Chapter 37** (`book/part8-message-deep-dives/ch37-international-asm-subtypes-dac-1-part-1.md`) providing a deep dive into **International ASM Subtypes (`DAC = 1`), Part 1: System Management & IMO SN/Circ.236 Legacy Messages (`FI = 0, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21`)**:
  - How each subtype works (complete bit layouts for `FI=0` text, `FI=2/3/4/5` capability interrogation/reply & app ack, **`FI=11` Legacy Met/Hydro [352 bits]**, `FI=12` Dangerous Cargo, `FI=13` Fairway Closed, `FI=14` Tidal Window, `FI=15` Extended Ship Static [Air Draught], `FI=16` Persons on Board, `FI=17` VTS-Generated/Synthetic Targets, `FI=18` Clearance Time, `FI=19` Marine Traffic Signal, `FI=20` Berthing Data, and `FI=21` Weather Observation from Ship),
  - Known issues (**why `DAC=1, FI=11` had inverted `(Lat, Lon)` order, `0.001 min` mismatch, and coarse `0.1 m` tide steps**, why `FI=12` was withdrawn over piracy/security risks, and why `FI=11` still dominates legacy weather buoy broadcasts despite deprecation!),
  - Relationships to other messages (supersession of `FI=11..15` by IMO Circ.289 `FI=24, 25, 31, 32`; `FI=17` broadcasting non-AIS VTS radar tracks alongside Msg 1/18),
  - Known uses, abuses, where/when used, and complete software support matrix (`libais` `Ais8_1_0`..`Ais8_1_21` & `Ais6_1_*`, `gpsd`, `pyais`, ECDIS).
- [x] **TASK-908:** Draft **Chapter 38** (`book/part8-message-deep-dives/ch38-international-asm-subtypes-dac-1-part-2.md`) providing a deep dive into **International ASM Subtypes (`DAC = 1`), Part 2: IMO SN.1/Circ.289 & Circ.290 Operational Messages (`FI = 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32`)**:
  - How each subtype works (complete bit layouts for **`FI=22` & `FI=23` Area Notice** [87-bit Sub-Areas `Shapes 0–5`], `FI=24` Extended Static [Air Draught + Ice Class + Shaft Power], `FI=25` Dangerous Cargo, **`FI=26` Modular Environmental Sensor Reports** [`Report Types 0–10`, 112 bits each], **`FI=27` & `FI=28` Route Information** [up to 16 waypoints], `FI=29` & `FI=30` Linked Text Descriptions, **`FI=31` Modern Met/Hydro [360 bits, `0.01 m` water level]**, and `FI=32` Tidal Window),
  - Known issues (Area Notice polyline vertex precision & 5-slot ceiling, `FI=26` vs. `FI=31` dual-standard fragmentation, poor commercial ECDIS rendering of `FI=22/27`),
  - Relationships to other messages (`Message Linkage ID` joining `FI=22` $\leftrightarrow$ `FI=29` and `FI=27/28` $\leftrightarrow$ `FI=30`; migration to IHO `S-104`, `S-111`, `S-124`, `S-421` over VDES),
  - Known uses and abuses (Whale Alert dynamic speed zones, Baltic icebreaker route broadcasts, coastal tide/wind stations, spoofed exclusion-zone Area Notices),
  - Where and when used, and complete software support matrix (`libais` `Ais8_1_22`..`Ais8_1_32`, `ais-area-notice`, `noaadata`, `gpsd`, `pyais`, OpenCPN, ECDIS).
- [x] **TASK-909:** Draft **Chapter 39** (`book/part8-message-deep-dives/ch39-european-inland-and-gla-asm-subtypes.md`) providing a deep dive into **Regional ASM Subtypes, Part 1: European Inland AIS (`DAC = 200`, `FI = 10, 21, 22, 23, 24, 40, 55`) and UK/Ireland GLA (`DAC = 232 / 235`, `FI = 10`)**:
  - How each subtype works (complete bit layouts for **`DAC=200, FI=10`** [8-char ENI number, `0.1 m` convoy length/beam, 4-digit ERI code `8000–8490`, ADN hazardous cargo `0–3 blue cones`, `0.01 m` draught, loaded/unloaded status], `FI=21` ETA at Lock/Bridge/Terminal, `FI=22` RTA at Lock/Bridge/Terminal, `FI=23` EMMA Weather Warning, `FI=24` River Water Level Gauge, `FI=40` Inland Bridge/Lock Signal Status, `FI=55` Persons on Board [Crew/Passengers/Personnel], and **`DAC=232/235, FI=10` UK/Ireland GLA AtoN Monitoring Telemetry** [battery/solar voltages, lantern/racon/hatch/off-position status]),
  - Known issues (incompatibility with non-Inland SOLAS ECDIS, stale `Loaded/Unloaded` and `Blue Cone` operator settings, river datum differences in `FI=24`),
  - Relationships to other messages (`DAC=200, FI=10` extending Msg 5 + Msg 1 `Maneuver Indicator` [Blue Sign]; `FI=21` $\leftrightarrow$ `FI=22` lock scheduling handshake; `DAC=235, FI=10` complementing Msg 21 AtoN reports),
  - Known uses, abuses, where/when used (Rhine, Danube, Elbe, Main, Moselle, Dutch/Belgian canals; UK/Irish coasts), and complete software support matrix (`libais` `Ais8_200_*`, `Ais6_200_*`, `Ais8_235_10`, `gpsd`, `pyais`, Inland ECDIS).
- [x] **TASK-910:** Draft **Chapter 40** (`book/part8-message-deep-dives/ch40-north-american-seaway-uscg-and-vdes-asm-subtypes.md`) providing a deep dive into **Regional ASM Subtypes, Part 2: St. Lawrence Seaway (`DAC = 316 / 366`), USCG / NOAA PORTS® / Encrypted AIS (`DAC = 366`), VDES ASM Migration, and the Master Software Support Matrix**:
  - How each subtype works (St. Lawrence Seaway `DAC=316/366` `FI=1` Met/Hydro, `FI=2` Dangerous Cargo, `FI=32` Lockage Order, `FI=33` Estimated Lock Times, `FI=34` Seaway Water Level & Flow Rate; USCG **`DAC=366, FI=22/23` Area Notice** [and exact bit differences vs. IMO `DAC=1, FI=22`]; NOAA PORTS® / RTCM 12301.1 environmental & bridge air-gap broadcasts; and **`DAC=366, FI=56/57` USCG/DoD Encrypted AIS [EAIS]** [64-bit IV + AES-256 / Type 1 ciphertext for Blue Force Tracking]),
  - Panama Canal (`DAC=351`), Australia (`DAC=503`), and South Korea (`DAC=440`) regional ASMs, plus how **VDES ASM (`ITU-R M.2092-1` Ch 2027/2028) and IHO S-100 (`SECOM`)** modernize binary messaging,
  - Known issues, relationships, uses/abuses (Whale Alert Stellwagen Bank right-whale speed zones, Seaway lock scheduling, USCG cutter OPSEC via `FI=56/57`),
  - **The Definitive Master AIS Message (1–27) and ASM (`DAC/FI`) Software Support Matrix** auditing `libais`, `gpsd`, `pyais`, `aisparser`, `noaadata`, `ais-area-notice`, `AIS-catcher`, Rust (`nmea-parser` / `ais`), Wireshark, OpenCPN, Signal K, GateHouse, Kongsberg, USCG NAIS/SeaVision, NOAA ERMA, and SOLAS/Inland ECDIS.

---

## 12. Complete Prompt-to-Plan/Task Traceability Matrix

| User Prompt Topic / Question | Target Chapter(s) & Section(s) in `PLAN.md` | Actionable Task ID(s) in `TASKS.md` |
|---|---|---|
| History of the overall system & components; deep dive into AIS history (`globalfishingwatch.org/article/ais-brief-history/`); Sept 11, 2001; SOLAS | Front Matter Timeline, Ch 2 (§2.1–2.4), Ch 3 (§3.2) | `TASK-003`, `TASK-103`, `TASK-104`, `TASK-105`, `TASK-107` |
| Look through `https://github.com/schwehr/gis-history` for topics and starting points | Front Matter Timeline, Section 4 of `PLAN.md`, Ch 2 (§2.1), Ch 24, Ch 25, Ch 30 | `TASK-003`, `TASK-103`, `TASK-601`, `TASK-603`, `TASK-604`, `TASK-710` |
| Add **Blender** to the plan and tasks (1994/2002 `gis-history` milestones, CCOM/UNH 3D AIS/bathymetry/whale animations, `bpy`/`BlenderGIS`/Geometry Nodes, `float32` ENU centering, Msg 5/24 antenna-offset hull rigging, 3D casualty litigation reconstruction) | Front Matter Timeline, Section 4.1, Ch 1 (§1.4), Ch 4 (§4.1), Ch 25 (§25.2), Ch 30 (§30.4) | `TASK-003`, `TASK-102`, `TASK-110`, `TASK-604`, `TASK-710`, `TASK-803` |
| What are all the uses for AIS data? + Figure out what is missing and include that too | Section 3 (12-point Gap Analysis), Ch 1 (§1.1–1.4), Ch 15–16 | `TASK-101`, `TASK-102`, `TASK-308`, `TASK-309` |
| Deep dive into open-source AIS decoding & encoding software and history (`libais`, `gpsd`, `aisparser`, Rust parsers, `noaadata`, `bitvector-modern`, `ais-area-notice`) | Ch 16 (§16.3), Ch 24 (§24.1–24.5), Ch 31–40 | `TASK-309`, `TASK-601`, `TASK-602`, `TASK-801`, `TASK-901`–`TASK-910` |
| Software for processing decoded AIS messages (open source & proprietary, including `MovingPandas`, `pandas`, `Blender`, `GateHouse`) | Ch 25 (§25.1–25.3) | `TASK-603`, `TASK-604`, `TASK-605` |
| What software does the US Coast Guard and other government agencies use for AIS? | Ch 22 (§22.3: NAIS, SeaVision, Command21, SAROPS, MISLE, AVIS, Minotaur, ERMA, MSSIS, SafeSeaNet, Starboard) | `TASK-504` |
| How do Vessel Traffic Services (VTS) use AIS? | Ch 22 (§22.1) | `TASK-503` |
| How are mariners trained to use AIS? How does that training vary? | Ch 23 (§23.1: STCW, IMO Model Course 1.34, TOAR, fishing, recreational, IALA V-103) | `TASK-505` |
| Security implications of AIS; malicious data sent to ships/shore; documented issues; DoS/corruption in hardware & software | Ch 27 (§27.1–27.2: Balduzzi 2014, CVE-2025-66217, bit-length overflows, fragment floods, target table DoS, Msg 20/22/23 attacks), Ch 31–40 | `TASK-701`, `TASK-901`–`TASK-910` |
| How timing signals are passed through AIS; practical use & robustness; causing AIS dynamic network failure via timing | Ch 11 (§11.1–11.4), Ch 32 | `TASK-301`, `TASK-302`, `TASK-902` |
| External vs. internal timing sources; does any hardware not use GNSS for timing? | Ch 11 (§11.2: 1PPS vs NMEA latency; SDRs, Class B CS, atomic/PTP/eLORAN Base Stations) | `TASK-301` |
| Overview of GNSS systems; do any AIS systems not include support for GPS? Breakdown of support; GNSS-denied locations; GNSS jamming & workarounds | Ch 12 (§12.1–12.4: GPS/GLONASS/BeiDou/Galileo, `181°/91°` & `61/62/63` timestamps, R-Mode, eLORAN, CRPA, INS) | `TASK-303`, `TASK-304` |
| Legal issues with and around AIS; key court cases | Ch 4 (§4.1–4.2), Appendix F (*Alexandra 1 / Ever Smart* [2021] UKSC 6, *Sakizaya Kalon*, CPR Part 61, *Deepwater Horizon*, *Dali*, OFAC forfeitures, GDPR, China PIPL) | `TASK-110`, `TASK-111` |
| Cover Listen for Whales / Whale Alert | Ch 1 (§1.3), Ch 16 (§16.3), Ch 30 (§30.4), Ch 38 (§38.1), Ch 40 (§40.2) | `TASK-102`, `TASK-309`, `TASK-710`, `TASK-908`, `TASK-910` |
| What are all the standard documents that impact / define AIS? | Ch 3 (§3.3), Appendix E (ITU, IMO, IEC, IALA, IHO, RTCM, NMEA) | `TASK-108` |
| What hacks have users come up with to use the AIS system in unintended ways? | Ch 19 (§19.2: Msg 5/14 chat, track-art, dinghy trackers, VHF DXing, passive bistatic radar), Ch 31–40 | `TASK-406`, `TASK-901`–`TASK-910` |
| RF basics for ships; noise sources for AIS on ships; what other RF channels have been used for AIS? | Ch 5 (§5.1–5.3: AIS 1/2, Ch 75/76, Msg 22, ASM, VDES, AMRD Ch 2006; horizon/multipath; LED SMPS, VFDs, radar/VHF desensitization) | `TASK-201`, `TASK-202`, `TASK-203` |
| How can RF be modeled for AIS? Using AIS for RF propagation monitoring & model testing; studies on propagation, network loading, and packet loss | Ch 6 (§6.1–6.3: ITM, P.1546, PE/AREPS, tropospheric ducting inversion, ITU-R M.2287, S-AIS collision studies) | `TASK-204`, `TASK-205`, `TASK-206` |
| AIS RF encoding; what can be used from RF recordings with packet corruption and/or collisions? | Ch 7 (§7.1–7.3: HDLC, bit-stuffing, CRC-16, NRZI, GMSK; soft-bit syndrome recovery, SIC de-collision, partial MMSI extraction) | `TASK-207`, `TASK-208` |
| AIS hardware and SDR for receive & transmit; low-budget home AIS receiver setup hardware & software | Ch 9 (§9.1–9.3), Appendix G | `TASK-210`, `TASK-211` |
| Best antennas for each application and why (large ships, small ships, very small systems, shore collection stations) | Ch 8 (§8.1–8.2) | `TASK-209` |
| Range of options for collecting AIS on shore (towers, lighthouses, buildings), places to avoid (large radar, NOAA weather radio), at sea (buoys, ASVs), and AIS collection networks/providers | Ch 10 (§10.1–10.4) | `TASK-212`, `TASK-213` |
| How does AIS work with the new S-100+ standards of charting? ECDIS vs ENC; Nautical charts | Ch 21 (§21.1–21.3: S-57, S-100, S-101, S-102, S-104, S-111, S-124, S-212, S-421) | `TASK-501`, `TASK-502` |
| Tide and other marine state transmissions | Ch 16 (§16.2: Msg 8 DAC 1 FI 11/31, NOAA PORTS®, St. Lawrence Seaway, RTCM 12301.1), Ch 37–40 | `TASK-309`, `TASK-907`–`TASK-910` |
| What AIS demonstration programs are there? | Ch 22 (§22.2) | `TASK-503` |
| Blue force systems and encryption; National security aspects to AIS | Ch 29 (§29.1–29.2: Encrypted AIS Msg 6/8, W-AIS, naval OPSEC, hybrid warfare), Ch 40 (§40.2) | `TASK-705`, `TASK-910` |
| How satellites receive and process AIS RF; have satellites ever transmitted AIS? | Ch 17 (§17.1–17.3: LEO footprint collisions, Msg 27, NorSat-2 ASM trials, NorSat-TD & Sternula-1 VDE-SAT downlinks), Ch 34 | `TASK-401`, `TASK-402`, `TASK-904` |
| AIS in aircraft and drones; AIS and direction finding systems | Ch 18 (§18.1–18.3: Msg 9, Minotaur/UAVs, SAR beacons, Doppler/Adcock RDF homing & AoA anti-spoofing), Ch 34 | `TASK-403`, `TASK-404`, `TASK-904` |
| AIS for fishing gear | Ch 19 (§19.1: net pingers/sun-buoys, alarm fatigue, ITU-R M.2135 AMRD Group B) | `TASK-405` |
| AIS spoofing techniques; deep diving into RF level to identify manufacturer or specific units (RF fingerprinting / SEI) | Ch 28 (§28.1–28.2: API vs RF vs GNSS spoofing; PA transients, GMSK phase error, CFO/clock skew, I/Q imbalance) | `TASK-703`, `TASK-704` |
| Failure modes of AIS software and hardware; AIS-assisted incidents / accidents | Ch 23 (§23.3), Ch 27 (§27.3), Ch 31–40 | `TASK-506`, `TASK-702`, `TASK-901`–`TASK-910` |
| Bloomberg Terminal (`scranton.edu/.../Bloomberg Training Manual.pdf`) & detailed look at commodity traders | Ch 30 (§30.3: `BMAP`, `SHIP`, `VSRC`, `VSTK`, `FLET`, `FIXS`, draught-to-cargo models, STS transfers) | `TASK-709` |
| 2025 GFW AIS and dark ships (`https://youtu.be/2tuS1LLOcsI`) | Ch 29 (§29.3: Johnny Harris / GFW investigation, Paolo et al. 2024 *Nature*, SAR/AIS fusion) | `TASK-706` |
| Privacy; Other ways to track ships: Mobile phones (apps, emissions, mobile network), Diameter (4G/5G) & SS7 (2G/3G), VMS, NOAA VOS, LRIT | Ch 4 (§4.2), Ch 30 (§30.1–30.2) | `TASK-111`, `TASK-707`, `TASK-708` |
| Key organizations (IMO, RTCM, IALA, IHO, ITU, IEC, NMEA) & key laws/treaties (SOLAS, UNCLOS, COLREGs, OPA-90, MTSA) | Ch 3 (§3.1–3.2) | `TASK-106`, `TASK-107` |
| What types of at-sea operations is AIS especially helpful for? | Ch 23 (§23.2) | `TASK-505` |
| What is an MMSI? Deep dive | Ch 13 (§13.1–13.3), Appendix B | `TASK-305` |
| NMEA 0183, NMEA 2000, NMEA TAG Block — standards for sharing and logging AIS; Voyage Data Recorder (VDR) | Ch 14 (§14.1–14.4), Appendix C | `TASK-306`, `TASK-307` |
| AIS 2.0 (VDES) — what is it? Is it real? | Ch 20 (§20.1–20.3: ITU-R M.2092-1, 2028 SOLAS mandate) | `TASK-407` |
| Spatial statistics with AIS data considering RF propagation constraints, packet loss, and uneven/moving receivers | Ch 26 (§26.1–26.2) | `TASK-606`, `TASK-802` |
| What patents are there for AIS and when do/did they expire? | Ch 3 (§3.4), Appendix F (Håkan Lans US5506587 2010 reexamination cancellation & 2012/2013 expiry; S-AIS patents) | `TASK-109` |
| **Part VIII: Deep dive into each AIS message type (1–27) and all known AIS Application-Specific Message (ASM) subtypes (`DAC/FI`)** — how each works, issues, relationships to other messages, known uses & abuses, where & when used, and software support/non-support | Part VIII, Ch 31–40 (§31.1–§40.4), Appendices A & D | `TASK-901`, `TASK-902`, `TASK-903`, `TASK-904`, `TASK-905`, `TASK-906`, `TASK-907`, `TASK-908`, `TASK-909`, `TASK-910` |


