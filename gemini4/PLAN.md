# Comprehensive Plan: The Maritime Automatic Identification System (AIS) Handbook
## *From RF Physics, Protocol Internals, and Open-Source Software to Global Surveillance, Security, and Spatial Analytics*

---

## 1. Executive Summary and Core Philosophy

The **Automatic Identification System (AIS)** began in the late 1980s and 1990s as a localized VHF radio collision-avoidance and Vessel Traffic Services (VTS) tool mandated in the wake of catastrophic oil spills (*Exxon Valdez*, 1989) and accelerated by post-September 11, 2001 maritime homeland security mandates (SOLAS Chapter V, Regulation 19; US MTSA 2002). Over the past three decades, AIS has evolved far beyond bridge-to-bridge navigation into the foundational nervous system of global Maritime Domain Awareness (MDA), supply-chain and commodity intelligence, marine mammal conservation, search and rescue (SAR), environmental response, and open-source geospatial data science.

Yet AIS is frequently misunderstood by both mariners who over-rely on its unauthenticated display vectors and data scientists who treat archived AIS rows as uniform, ground-truth GPS tracks. In reality, **every AIS record is an observation conditioned on**:
1. **Shipboard Sensor & Human Inputs** (GNSS receiver state, gyrocompass, rate-of-turn indicator, and manually entered—often stale or falsified—static voyage fields),
2. **A Distributed Self-Organizing TDMA MAC State Machine** (governed by microsecond-level 1PPS UTC timing synchronization and dynamic reporting rates ranging from 2 seconds to 3 minutes),
3. **A Bit-Stuffed, CRC-16 Protected, GMSK-Modulated VHF Physical Layer** (subject to line-of-sight horizon limits, sea-surface multipath lobing, tropospheric ducting, co-channel slot collisions, shipboard EMI, and nearby high-power transmitters such as NOAA Weather Radio and marine radars),
4. **A Heterogeneous Collection & Transport Pipeline** (shipboard RS-422 NMEA 0183 / CAN-bus NMEA 2000 / UDP IEC 61162-450 TAG blocks, coastal towers, offshore buoys, ASVs, patrol aircraft, and LEO satellite constellations with 3,000+ km footprints), and
5. **An Adversarial Operational Environment** (characterized by intentional transponder disabling ["dark ships"], software/RF spoofing, identity laundering, and widespread regional GNSS jamming and spoofing).

This handbook provides an authoritative, end-to-end reference that spans introductory operational concepts through bit-level protocol anatomy, RF propagation mathematics, software engineering (`libais`, `gpsd`, `aisparser`, Rust parsers, `noaadata`, `bitvector-modern`, `ais-area-notice`, `pandas`, `MovingPandas`, `Blender`, `GateHouse`), hardware/SDR design, legal/patent history, national security, and rigorous spatial statistics.

---

## 2. Pedagogical & Structural Conventions for Every Chapter

To maintain consistent rigor from introductory material to deep technical analysis, every chapter in this handbook follows an eight-part architecture:
1. **Operational & Conceptual Overview:** Accessible introduction explaining *what* the subsystem does, *why* it exists, and how mariners, engineers, and analysts interact with it.
2. **Historical Context & Evolution (`schwehr/gis-history` Integration):** Chronological lineage connecting early navigation, geodesy, computing, and maritime casualties to modern AIS standards and open-source software milestones.
3. **Deep Technical & Mathematical Foundations:** Bit-level schemas, RF link budgets, propagation equations, state-machine diagrams, or statistical estimators.
4. **Hardware, Standards, & Software Ecosystem:** Applicable ITU/IMO/IEC/IALA/IHO/RTCM/NMEA standards alongside both open-source and proprietary hardware/software implementations.
5. **Security, Adversarial Abuse, & Failure Modes:** How the component fails in the wild—hardware degradation, software parser bugs, operator error, RF interference, or deliberate spoofing/jamming.
6. **Practical Engineering / Code Walkthrough:** Reproducible Python, C++, Rust, SQL/DuckDB, Blender (`bpy`), or SDR configurations.
7. **Key Takeaways & Operational Checklist:** Actionable summary for mariners, RF engineers, and spatial analysts.
8. **Cited References & Primary Sources:** Peer-reviewed literature, official regulatory circulars, court decisions, patents, and archival URLs.

---

## 3. Gap Analysis: Critical Topics Missing from the Initial Prompt List (Added to This Plan)

The prompt explicitly instructs: *"Be sure to figure out what is missing from this list and include that too."* A systematic audit of the maritime communications, hydrographic, and spatial data science domains identified **12 essential areas** that were omitted or only implicitly referenced in the initial prompt list and are now fully integrated into the handbook plan:

1. **Exhaustive Bit-Level Catalog of All 27 ITU-R M.1371 Message Types:** Complete bit-width, signed/unsigned encoding, scaling factor, and sentinel ("not available") tables for Messages 1 through 27, including the nuances between Class A (Msgs 1–3, 5), Class B CSTDMA vs. SOTDMA (Msgs 18, 19, 24 Part A/B), SAR Aircraft (Msg 9), Base Station/Data Link Management (Msgs 4, 20, 22, 23), Safety/Interrogation (Msgs 10–16), AtoN (Msg 21), and Long-Range Satellite AIS (Msg 27).
2. **MAC-Layer TDMA Access Schemes & Slot State Machines:** Deep dive into how **SOTDMA** (Self-Organized TDMA), **RATDMA** (Random Access TDMA), **ITDMA** (Incremental TDMA), **FATDMA** (Fixed Access TDMA), and **CSTDMA** (Carrier Sense TDMA) allocate and reserve the 2,250 time slots (26.67 ms each) per 60-second UTC frame across AIS1 and AIS2, including intentional slot reuse (cell shrinking) under high VHF Data Link (VDL) loading.
3. **Taxonomy of AIS Device Classes and Autonomous Variants:** Hardware and regulatory distinctions between Class A, Class B "CS" (2 W), Class B "SO" / Class B+ (5 W), AIS Base Stations, Simplex/Duplex Repeaters, AIS Aids to Navigation (Real, Synthetic Monitored, Synthetic Predicted, and Virtual AtoNs), AIS-SART, AIS-MOB (Man Overboard), EPIRB-AIS, and Autonomous Maritime Radio Devices (AMRD Group A & B).
4. **Inland AIS (European CCNR / UNECE & US Western Rivers):** How Inland Waterways (Rhine, Danube, Mississippi) extend ITU-R M.1371 with Inland-specific Application Specific Messages (DAC 200), Electronic Reporting International (ERI) vessel/convoy type codes, dynamic draught, bridge clearance height, and "Blue Sign" oncoming-meeting status integration.
5. **Vessel Identity Resolution Beyond MMSI (IMO Numbers, Call Signs, and Flag Laundering):** The structural relationship and divergence between the 9-digit MMSI (tied to flag state and radio license), the permanent 7-digit IMO Ship Identification Number (assigned by S&P Global / IHS Markit to the hull at keel laying, verified via check digit), IRCS Call Signs, and entity-resolution algorithms for tracking "zombie ships," flag-hopping, and hull-swap sanctions evasion.
6. **Shipboard Bridge Integration & Sensor Fusion Architecture:** How an AIS transponder physically and logically integrates on a ship's bridge: Gyrocompass (`$HEHDT`), Rate-of-Turn indicator (`$HEROT`), GNSS (`$GPRMC`/`$GPGGA`), ECDIS/ECS, Marine Radar/ARPA target association gates (fusing radar range/bearing with AIS identity under IEC 62388), Minimum Keyboard and Display (MKD), Pilot Plug (AMP 9-pin RS-422 and Wi-Fi), and Bridge Alert Management Systems (BAMS, IEC 62923).
7. **Cloud-Native AIS Data Engineering & Trajectory Compression:** Modern petabyte-scale architectures for storing, indexing, and querying billions of AIS messages using **Apache Arrow**, **GeoArrow**, **GeoParquet**, **DuckDB**, **PostGIS / MobilityDB**, **BigQuery**, and discrete global grid systems (**H3**, **S2**), alongside kinematic outlier filtering (removing speed/teleportation jumps), voyage segmentation (stop/anchorage/transit state detection), and spatio-temporal trajectory simplification (Douglas-Peucker, TD-TR, dead-reckoning threshold compression).
8. **AIS-Based Ship Emissions & Underwater Radiated Noise (URN) Modeling:** Calculating global and port-level greenhouse gas ($\text{CO}_2$, $\text{CH}_4$, $\text{N}_2\text{O}$) and criteria pollutant ($\text{SO}_x$, $\text{NO}_x$, $\text{PM}_{2.5}$, black carbon) inventories by combining AIS speed-over-ground and draught with hull resistance-power curves (Holtrop-Mennen, STEAM model, ICCT, IMO Fourth GHG Study), as well as modeling Underwater Radiated Noise (JOMOPANS-ECHO, RANDI, CetSound) impacting marine mammals.
9. **Multi-Sensor Remote Sensing Fusion (SAR, Optical, VIIRS, and Spaceborne RF):** Algorithmic pipelines for matching AIS trajectories against spaceborne Synthetic Aperture Radar (Sentinel-1, NISAR, ICEYE, Capella), high-resolution optical imagery (Sentinel-2, PlanetScope, WorldView/Maxar), VIIRS nightfire/boat detection ("squid fleet" light fishing), and spaceborne RF emitters (HawkEye 360, Unseenlabs X-band/S-band navigation radar & VHF voice geolocation) to unmask dark vessels and verify spoofing.
10. **Subsea Critical Infrastructure Protection & Anchor-Drag Forensics:** Using high-frequency AIS kinematics (SOG drop, COG yaw, rate-of-turn anomalies, and draught changes) to detect and attribute anchor-dragging incidents over submarine telecommunications cables and gas/power pipelines (e.g., *Newnew Polar Bear* / Balticconnector 2023, *Yi Peng 3* 2024, Red Sea cable cuts).
11. **Epidemiology, Biosecurity, and Invasive Species Vectors:** Using global AIS port-to-port connectivity graphs to model ballast-water invasive species transport, hull biofouling accumulation (residence time in tropical ports), and maritime quarantine/pandemic vectors.
12. **Next-Generation Cryptographic Authentication & Maritime Cybersecurity Standards:** Technical proposals for backward-compatible AIS authentication (Auth-AIS, TESLA broadcast authentication), PKI certificates in VDES (ITU-R M.2092), and IHO S-100 / IEC 63173-2 (SECOM) secure communication channels.

---

## 4. Historical Synthesis: Anchoring AIS in `schwehr/gis-history`

A defining feature of this handbook is situating AIS within the broader sweep of navigation, geodesy, radio physics, computing, and open-source geospatial software documented in [`https://github.com/schwehr/gis-history`](https://github.com/schwehr/gis-history) and Global Fishing Watch's historical overview ([Cutlip, 2017](https://globalfishingwatch.org/article/ais-brief-history/)).

### 4.1 Chronological Backbone (`gis-history` + Maritime AIS Milestones)

| Era / Year | Milestone (`gis-history` & AIS Lineage) | Relevance to the AIS Handbook |
|---|---|---|
| **~206 BCE – 1761** | Magnetic compass (206 BCE), Hipparchus spherical trigonometry (~140 BCE), Mercator projection (1569), Sextant (1731), John Harrison's **H4 marine chronometer** (1761) | Foundations of dead reckoning, celestial latitude/longitude, rhumb-line vs. great-circle navigation, and precise timekeeping as the prerequisite for positioning. |
| **1807 – 1928** | US Survey of the Coast / NOAA precursor (1807), International Meridian Conference (1884), **Radar** foundations (1904), **GEBCO** (1903), ***RMS Titanic* sinking (1912) & SOLAS (1914)**, Sonar (1913), **NAD27** (1927), Universal Time (1928) | Birth of international maritime safety law (SOLAS Chapter V), hydrographic charting, datum realizations, and radio/acoustic detection. |
| **1931 – 1958** | **Simrad / Kongsberg Maritime** founded (1931), **Gee** (1940), **Decca** & **LORAN** (1942), **UTM** (1942), Claude Shannon's **Information Theory** (1948), Atomic clocks (1949/1955), **Kalman Filter** (1958) | Hyperbolic radio navigation, channel capacity limits, atomic frequency standards, and state-space trajectory estimation (Kalman filtering for radar+AIS fusion). |
| **1960 – 1984** | **UTC** starts (1960), **CGIS** first GIS (1963), **CHAYKA** (1969), **Unix time 0** & **NOAA** formed (1970), **C language** (1972), **COLREGs** (1972), **SOLAS 1974**, **LORAN-C** civilian use (1974), **GPS** first launch (1978), **PROJ** (1983), **NMEA 0183** & **WGS84** (1984) | The direct technical stack of AIS: UTC time slots, WGS84 reference ellipsoid, GPS satellite timing/positioning, NMEA 0183 serial sentences, and C/Unix systems. |
| **1988 – 1990** | **Håkan Lans** files priority patent for **STDMA** (Sept 1988); ***Exxon Valdez* oil spill** in Prince William Sound (March 24, 1989); US **Oil Pollution Act of 1990 (OPA-90)** mandates tanker tracking | The twin technological (STDMA) and regulatory (OPA-90) catalysts that launched modern AIS. |
| **1991 – 1997** | **Linux** (1991), **Python** (1992), **R** (1993), **UNCLOS** effective (1994), **Blender** initial release (1994), **OGC** & **PROJ4** (1994), **NumPy** (1995), **DGPS** operational (1996); UK Dover Strait **4S VHF DSC** trials, Panama Canal **UHF CTAN**, Swedish/Finnish **SOTDMA** trials | Competing regional vessel tracking architectures converge at IMO, ITU, and IALA onto Håkan Lans's VHF SOTDMA design. US Patent **5,506,587** granted (1996). |
| **1998 – 2000** | **ITU-R M.1371-0** published (Nov 1998) — first global AIS specification; USCG **PAWSS** modernizes New Orleans VTS with AIS (1998); **GPS Selective Availability (SA) disabled** (May 2000); **SQLite** & **GDAL** (2000); IMO adopts **SOLAS Chapter V Reg 19** AIS mandate (Dec 2000) | Disabling GPS SA immediately improves standalone civil GPS from ~100 m to <10 m accuracy, making unaugmented shipboard AIS viable worldwide. |
| **2001 – 2005** | **SkyTruth** & **PostGIS** (2001); **September 11, 2001 attacks** accelerate US maritime security; **SOLAS AIS mandate** takes effect (July 1, 2002); **Blender** released as open source (2002); US **MTSA 2002** & DHS / USCG **Nationwide AIS (NAIS)**; **GEOS** & **QGIS** (2002); **WAAS** (2003); **OSM** & **Google acquires Keyhole** (2004) | AIS pivots from localized collision avoidance to national homeland security and coastal surveillance networks. Open-source 3D rendering (**Blender**) and GIS (**PostGIS/QGIS**) emerge simultaneously. |
| **2006 – 2010** | **NOAA ERMA** & **OSGeo** (2006); CCOM/UNH pioneers **Blender + Python (`noaadata`)** 3D AIS & bathymetry animations; **IEC 62287-1 Class B CSTDMA** & **LRIT** (2006); **GeoJSON** & **SpatiaLite** (2008); EU mandates AIS on fishing vessels $\ge 15\text{ m}$ (2009); **USPTO cancels Håkan Lans US Patent 5,506,587 claims** on reexamination (March 2010); ***Deepwater Horizon* oil spill** (April 2010); **Kurt Schwehr releases `libais`** (2010) | Open-source high-performance C++/Python AIS decoding (`libais`) born out of the Deepwater Horizon response to feed vessel tracks into NOAA ERMA. |
| **2011 – 2016** | **Galileo** launches (2011); **WhaleAlert** presented to US Congress (2012); **"All the Ships"** Google I/O geospatial talk (2013); **GeoPandas** (2013); **Sentinel-1 SAR** (2014); **ITU-R M.1371-5** & **Balduzzi et al.** AIS security evaluation (2014); **ITU-R M.2092 VDES** (2015); USCG 65-ft & fishing vessel AIS mandate takes effect (March 2016); **Global Fishing Watch** launched (Sept 2016) | Era of global satellite AIS aggregation, cloud big-data analytics, marine mammal dynamic protection, and public unmasking of global industrial fishing. |
| **2017 – 2026+** | **DuckDB** & **MovingPandas** (2018); C4ADS *Above Us Only Stars* GNSS/AIS spoofing report (2019); **GeoArrow** (2020) & **GeoParquet** (2021); **NorSat-TD** & **Sternula-1** launch two-way **VDES** payloads (2023); Paolo et al. *Nature* dark-vessel SAR+AIS study (2024); Johnny Harris / GFW *"Dark Zones"* investigation (2025); IHO **S-100** & IMO **SOLAS VDES** transition (2026–2028) | Convergence of AIS with multi-sensor EO/SAR/RF spaceborne intelligence, cloud-native columnar formats, RF fingerprinting, and two-way authenticated VDES (AIS 2.0). |

---

## 5. Master Architecture of the Handbook (8 Parts, 40 Chapters, 8 Appendices)

### Front Matter
* **`00-front-matter/notation-and-conventions.md`:** Mathematical symbols, bit-indexing conventions (0-based MSB-first ITU bit numbering vs. LSB byte ordering), NMEA 6-bit ASCII armor tables, two's complement signed field rules, RF decibel units ($\text{dBm}$, $\text{dBW}$, $\text{dBi}$, $\text{dBd}$), and coordinate reference frames (WGS84 realizations, ECEF, local tangent plane, ship body frame).
* **`00-front-matter/ais-and-gis-history-timeline.md`:** Comprehensive chronological timeline merging `schwehr/gis-history` with maritime navigation, AIS standards, hardware, satellite launches, casualties, and open-source software releases.
* **`00-front-matter/acronyms-and-glossary.md`:** Exhaustive glossary of >450 maritime, RF, GNSS, hydrographic, telecom, and geospatial terms.

---

### PART I: Origins, History, Governance, and Legal Framework

#### Chapter 1: Introduction to AIS and the Taxonomy of All AIS Uses
* *Scope:* Foundational overview of how AIS works and an exhaustive catalog of every primary, secondary, and unintended use of AIS data.
* **1.1 The Three Original IMO Pillars:**
  1. Ship-to-ship mode for collision avoidance (supplementing marine radar/ARPA and visual lookout).
  2. Littoral state mode for obtaining information about a ship and its cargo in coastal waters.
  3. Vessel Traffic Services (VTS) ship-to-shore traffic management tool.
* **1.2 Safety, Operational, and Infrastructure Uses:**
  * Search and Rescue (AIS-SART, AIS-MOB, EPIRB-AIS, SAR Aircraft Message 9, AMVER coordination).
  * Aids to Navigation (Real, Synthetic, and Virtual AtoNs via Message 21 for marking wrecks, dynamic sandbars, and ice).
  * Complex at-sea operations: tug and tow, pilot boarding, dredging, subsea cable/pipeline laying, offshore wind farm crew transfer vessels (CTVs), icebreaking convoys, ship-to-ship (STS) lightering.
  * Subsea infrastructure protection (real-time geofencing and anchor-drag kinematic alerting over fiber-optic cables and gas pipelines).
  * Port operations, berth scheduling, pilotage/tug dispatch, and canal transit optimization (Panama, Suez, St. Lawrence Seaway).
* **1.3 Environmental, Scientific, and Conservation Uses:**
  * Oil and chemical spill emergency response and damage assessment (e.g., 2010 *Deepwater Horizon* response in NOAA ERMA, dispersant vessel tracking, booming operations).
  * Marine mammal protection and dynamic ocean management (**Listen for Whales / Whale Alert**, North Atlantic Right Whale Seasonal and Dynamic Management Areas, ship-strike risk modeling).
  * Fisheries management and combating Illegal, Unreported, and Unregulated (IUU) fishing (Global Fishing Watch, gear conflict monitoring, MPA enforcement, transshipment detection).
  * Ship exhaust emissions inventories ($\text{CO}_2$, $\text{SO}_x$, $\text{NO}_x$, $\text{PM}$, black carbon via STEAM and ICCT models) and Underwater Radiated Noise (URN) soundscape modeling (JOMOPANS, CetSound).
  * Real-time hydrographic and meteorological broadcasting (NOAA PORTS®, tides, currents, salinity, ice thickness, dynamic Under-Keel Clearance).
  * Radio science: opportunistic VHF tropospheric ducting monitoring, atmospheric refractivity inversion, and passive bistatic radar.
* **1.4 Economic, Financial, Legal, and National Security Uses:**
  * Commodity trading and macroeconomic intelligence (Bloomberg `BMAP`/`SHIP`, Kpler, Vortexa, IMF PortWatch, crude oil floating storage, grain/LNG flow tracking via draught changes).
  * Maritime casualty investigation, VDR reconstruction, 3D courtroom/investigative visualization (e.g., in **Blender**), insurance underwriting, charter-party speed/consumption disputes, and admiralty litigation.
  * Sanctions enforcement, "shadow fleet" / "dark ship" tracking, illicit ship-to-ship transfers, and counter-narcotics/counter-piracy operations.
  * Naval and Coast Guard Maritime Domain Awareness (MDA) and Blue Force Tracking (BFT).
* **1.5 Key References:** IMO Resolution A.1106(29); ITU-R M.1371-5; Cutlip (2017); Kroodsma et al. (2018, *Science*); Paolo et al. (2024, *Nature*); Jalkanen et al. (2009/2012, STEAM).

#### Chapter 2: Deep History of Maritime Navigation, Geodesy, and the Birth of AIS
* *Scope:* Chronological deep dive from ancient navigation and `schwehr/gis-history` milestones to the engineering and political birth of AIS.
* **2.1 Pre-AIS Navigation and Positioning Lineage (`schwehr/gis-history`):**
  * Compass, sextant, Harrison's H4 chronometer (1761), Mercator (1569), Principal Triangulation of Great Britain (1791), US Coast Survey (1807), *Titanic* & SOLAS (1912/1914).
  * Early electronic navigation: Radar (1904/WWII), Gee (1940), Decca (1942), LORAN-A/C (1942/1974), CHAYKA (1969), Transit/NNSS, GPS (1978), GLONASS (1982), WGS84 & NMEA 0183 (1984), Maritime DGPS (1980s/1996), and the disabling of GPS Selective Availability (May 2000).
* **2.2 The Catalyst Disasters and Competing 1980s–1990s Prototypes:**
  * March 24, 1989: ***Exxon Valdez* grounding** on Bligh Reef in Prince William Sound, Alaska, and the **Oil Pollution Act of 1990 (OPA-90)** mandating automated tanker tracking.
  * The competing regional systems (as recounted by USCG's Jorge Arroyo in [Cutlip, 2017](https://globalfishingwatch.org/article/ais-brief-history/)):
    * **UK Dover Strait:** VHF Digital Selective Calling (DSC Channel 70) "4S" (Ship-to-Shore / Ship-to-Ship) transponder trials.
    * **Panama Canal Commission:** UHF-based Vessel Traffic Management / CTAN positioning system.
    * **Sweden & Finland:** Håkan Lans's invention of **STDMA** (Self-Organizing Time Division Multiple Access, priority patent 1988) tested in the Baltic Sea for both maritime and aviation (VDL Mode 4) applications.
* **2.3 International Standardization (1994–2000):**
  * IALA, ITU, and IMO technical working groups evaluate DSC polling vs. SOTDMA broadcast; why SOTDMA won for high-density autonomous ship-to-ship operation.
  * 1998: **ITU-R M.1371-0** ratified; USCG launches **PAWSS** (Ports and Waterways Safety System) designating the Lower Mississippi / **New Orleans** as the first primarily AIS-based VTS.
  * December 2000: IMO adopts revised **SOLAS Chapter V, Regulation 19**, establishing the global AIS carriage schedule starting July 1, 2002.
* **2.4 September 11, 2001 and the Pivot to Homeland Security:**
  * How the 9/11 terrorist attacks transformed AIS from a bridge navigation aid into a pillar of national defense.
  * Passage of the **Maritime Transportation Security Act of 2002 (MTSA)**, creation of the Department of Homeland Security (DHS), and deployment of the USCG **Nationwide AIS (NAIS)** network.
  * Subsequent regulatory expansions: USCG 2003 initial rules vs. industry pushback, the **March 2016 USCG final rule** extending AIS to all commercial vessels $\ge 65\text{ ft}$ (including fishing and passenger vessels) and towing vessels $\ge 26\text{ ft}$ / $\ge 600\text{ hp}$, and the **2009 EU mandate** (Directive 2002/59/EC amendments) for fishing vessels $\ge 15\text{ m}$.
* **2.5 Key References:** Cutlip (2017, Global Fishing Watch); Arroyo (USCG AIS History presentations); OPA-90 (Pub. L. 101-380); MTSA 2002 (Pub. L. 107-295); 33 CFR § 164.46; `schwehr/gis-history`.

#### Chapter 3: Governance, International Organizations, Treaties, Standards, and Patents
* *Scope:* Who governs AIS, what every standard document specifies, and the controversial history of AIS patents.
* **3.1 Key Organizations and Their Roles:**
  * **IMO** (International Maritime Organization — UN specialized agency governing SOLAS, COLREGs, STCW, MSC circulars).
  * **ITU** (International Telecommunication Union — ITU-R Radiocommunication Sector governing radio spectrum Appendix 18, M.1371, M.585 MMSI, M.2092 VDES).
  * **IALA** (International Organization for Marine Aids to Navigation — transitioned from non-governmental association to an **Intergovernmental Organization (IGO) in August 2024**; governs VTS, AtoN, and AIS shore networks via A-124, A-126, G1082).
  * **IHO** (International Hydrographic Organization — governs charting standards S-52, S-57, S-63, and the S-100 framework).
  * **IEC** (International Electrotechnical Commission — Technical Committee 80 governing hardware test & certification standards IEC 61993-2, 62287, 62320, 61162).
  * **RTCM** (Radio Technical Commission for Maritime Services — Special Committee 121 on AIS, DGNSS SC-104, AIS-MOB SC-119).
  * **NMEA** (National Marine Electronics Association — NMEA 0183, NMEA 2000, OneNet).
  * Regional bodies: **EMSA** (European Maritime Safety Agency), **CCNR** (Central Commission for the Navigation of the Rhine — Inland AIS), **USCG** & **FCC** (47 CFR Part 80).
* **3.2 Key Laws and Treaties Impacting AIS:**
  * **UNCLOS** (1982/1994): Innocent passage, territorial seas (12 NM), contiguous zone (24 NM), EEZ (200 NM), high seas freedom of navigation, and flag-state vs. port-state jurisdiction.
  * **SOLAS** (1914 / 1974 / Chapter V Reg 19 & Reg 19-1): Carriage thresholds (300 GT international, 500 GT domestic, all passenger ships), requirement to keep AIS in operation at all times except where international agreements/rules provide for the protection of navigational information (Master's discretion for security/piracy).
  * **COLREGs** (1972): Rule 5 (Look-out), Rule 7 (Risk of collision — "assumptions shall not be made on the basis of scanty information"), Rule 8 (Action to avoid collision), and why VHF voice agreements based on AIS identity frequently violate COLREGs.
* **3.3 Master Cross-Reference of All Standards Defining and Impacting AIS:**
  * Complete technical index of ITU-R (M.1371-0 through -5, M.585-9, M.823, M.1084, M.2092, M.2135, M.2287), IMO (MSC.74(69), A.917(22), A.1106(29), SN.1/Circ.227, SN.1/Circ.289, SN.1/Circ.290, MSC.1/Circ.1252), IEC (61993-2, 62287-1/2, 62320-1/2/3, 61097-14, 63269, 61162-1/2/3/450, 61174, 62388), IALA (A-124, A-126, V-128, G1082, G1117), RTCM (12301.1, 11901.1), and IHO (S-52, S-57, S-100+).
* **3.4 AIS Patents: History, Litigation, Reexamination, and Expiration:**
  * **Håkan Lans & GP&C Systems International AB:** Deep dive into **US Patent 5,506,587** (*"Position indicating system"*, priority Sept 9, 1988; filed Oct 28, 1992; issued April 9, 1996) and European counterpart **EP 0 465 532 B1** covering STDMA.
  * The late-1990s/2000s ITU/IMO patent policy battles (RAND licensing disputes, GP&C demands against AIS hardware manufacturers and shore software providers including GateHouse).
  * **USPTO Ex Parte Reexamination (90/008,299 & 90/008,522):** How prior art challenges led the USPTO to issue an **Ex Parte Reexamination Certificate on March 30, 2010 cancelling all claims (1–19) of US Patent 5,506,587**, alongside the natural 20-year term expiration of the original STDMA patent family in 2012/2013.
  * **Second-Generation AIS Patents (Space-Based AIS & De-Collision):** Survey of patents granted between 2008 and 2020 on satellite AIS co-channel signal separation, Doppler estimation, and multi-antenna beamforming (held by COM DEV / exactEarth / Spire, ORBCOMM, Kongsberg Seatex, LuxSpace — e.g., US7839336B2, US8218670B2, US8761775B2) and their expiration timeline (2027–2035).

#### Chapter 4: Legal Issues, Admiralty Court Cases, Casualty Forensics, and Privacy
* *Scope:* How AIS data is treated in courts of law, 3D demonstrative casualty reconstruction, landmark maritime cases, sanctions seizures, and data privacy statutes.
* **4.1 Transformation of Admiralty & Collision Litigation:**
  * Shift from subjective deck-log narratives to objective digital forensics combining AIS, VDR (Voyage Data Recorder), ECDIS playback, and 3D physical reconstructions in **Blender** (synchronizing true-scale 3D ship hull meshes, GPS antenna offsets, bridge wing sightlines, COLREGs navigation light arcs, bathymetry, and VDR bridge audio for courtroom demonstrative exhibits and NTSB/MAIB casualty boards).
  * **Key Court Cases:**
    * ***Nautical Challenge Ltd v Evergreen Marine (UK) Ltd (The "Alexandra 1" and "Ever Smart")* [2021] UKSC 6:** Landmark UK Supreme Court ruling on the Narrow Channel Rule vs. Crossing Rule in the pilot boarding area off Jebel Ali, reconstructed directly from AIS and VDR tracks.
    * ***Sakizaya Kalon & Osios David v Panamax Alexander* [2020] EWHC 2604 (Admlty):** High Court reconstruction of a three-ship Suez Canal anchorage collision and the legal duty to use electronic aids (AIS/ECDIS) as part of a proper lookout under COLREGs Rule 5.
    * ***MV Hua Sheng Hai v MV Kirrixki* [2024] EWHC (Admlty)** and the **April 2023 UK Admiralty Court CPR Part 61 Reforms** mandating early compulsory disclosure of electronic track data (AIS, ECDIS, VDR).
    * **US Maritime Casualty & Sanctions Cases:** *Deepwater Horizon* (2010 MDL 2179), *USS Fitzgerald* and *USS John S. McCain* collisions (2017), *Ever Given* Suez Canal grounding (2021), *MV Dali* Francis Scott Key Bridge allision (2024), and US DOJ/OFAC asset forfeiture actions against sanctions-evading tankers (*M/T Wise Honest* 2019, *M/T Grace 1 / Adrian Darya 1* 2019, *M/T Skipper* 2025) relying on AIS spoofing/dark-gap evidence.
* **4.2 Privacy, Commercial Confidentiality, and National Data Restrictions:**
  * The legal paradox of AIS: broadcast unencrypted over public radio waves vs. radio communications secrecy acts (e.g., UK Wireless Telegraphy Act 2006 s.48, US Communications Act of 1934 s.705 — why unencrypted public safety/navigation broadcasts intended for general reception are exempt in the US, whereas some jurisdictions restrict re-transmission).
  * **GDPR and Personal Data:** When an MMSI or vessel name on a small artisanal fishing boat or pleasure craft identifies a natural person/sole proprietor in the EU.
  * **National Security Blackouts:** China's **Data Security Law (DSL)** and **Personal Information Protection Law (PIPL)** (November 2021) cutting off commercial terrestrial AIS feeds from Chinese coastal stations.
  * Superyacht privacy, piracy high-risk area (HRA) blackouts, and USCG FOIA exemptions for sensitive law-enforcement/military tracks in NAIS.

---

### PART II: RF Physics, Propagation Modeling, Antennas, and Shipboard/Shore Hardware

#### Chapter 5: Maritime VHF RF Fundamentals, Spectrum Allocation, and Shipboard Noise
* *Scope:* RF basics for ships, frequency channels used by AIS, and electromagnetic interference (EMI) on vessels.
* **5.1 Maritime VHF Band Physics & All Channels Used for AIS:**
  * Wavelength $\lambda = c/f \approx 1.85\text{ m}$ at $162\text{ MHz}$.
  * **Primary Channels:** AIS 1 (Channel 87B, $161.975\text{ MHz}$) and AIS 2 (Channel 88B, $162.025\text{ MHz}$), $25\text{ kHz}$ simplex (or $12.5\text{ kHz}$ narrowband).
  * **Long-Range Satellite Channels:** Channel 75 ($156.775\text{ MHz}$) and Channel 76 ($156.825\text{ MHz}$) for Message 27.
  * **Regional & Alternate Channels:** Dynamic frequency switching across $156.025\text{–}162.025\text{ MHz}$ via Message 22 (Channel Management) under ITU Radio Regulations Appendix 18.
  * **ASM & VDES Channels:** ASM 1 (Ch 2027, $161.950\text{ MHz}$), ASM 2 (Ch 2028, $162.000\text{ MHz}$), VDE-TER/SAT channels (Ch 1024/2024, 1084/2084, etc.).
  * **Autonomous Maritime Radio Devices (AMRD Group B):** Channel 2006 ($160.900\text{ MHz}$) designated by ITU-R M.2135 to offload non-navigational fishing gear pingers from AIS 1/2.
* **5.2 Line-of-Sight, Radio Horizon, Fresnel Zones, and Sea-Surface Multipath:**
  * Optical vs. standard radio horizon ($k = 4/3$ effective Earth radius):
    $$d_{\text{NM}} \approx 2.23 \left(\sqrt{h_{t,\text{m}}} + \sqrt{h_{r,\text{m}}}\right)$$
  * Two-ray sea-surface reflection model: grazing-angle phase reversal ($\Gamma \approx -1$ for vertical polarization at low grazing angles), creating constructive and destructive interference lobes and a $1/d^4$ path-loss roll-off beyond the breakpoint distance.
* **5.3 Shipboard RF Noise Sources and Receiver Desensitization:**
  * **LED Lighting & Switch-Mode Power Supplies (SMPS):** Cheap PWM drivers in LED navigation lights, deck floodlights, and USB chargers radiating broadband hash across $150\text{–}170\text{ MHz}$, raising the noise floor by $10\text{–}30\text{ dB}$ right at the masthead antenna.
  * **Variable Frequency Drives (VFDs) & Alternators:** Bow thrusters, winches, HVAC compressors, and unshielded engine alternators.
  * **Co-Site Interference:** Shipboard $25\text{ W}$ VHF voice radios (Ch 16 at $156.800\text{ MHz}$, Ch 13 at $156.650\text{ MHz}$) causing front-end compression/blocking; X-band ($9.4\text{ GHz}$) and S-band ($3.0\text{ GHz}$) marine radar magnetron out-of-band spikes; MF/HF SSB transmitters; and Passive Intermodulation (PIM / "rusty bolt effect") on corroded stays and rigging.

#### Chapter 6: AIS RF Propagation Modeling, Atmospheric Ducting, and Network Loading Studies
* *Scope:* How RF propagation is modeled for AIS, how AIS serves as an atmospheric sensor, and scientific studies on propagation and VDL packet loss.
* **6.1 RF Propagation Models for the Marine Environment:**
  * Free-Space Path Loss (FSPL), Two-Ray Flat/Curved Earth, **Longley-Rice / Irregular Terrain Model (ITM)** for coastal headlands and islands, **ITU-R P.1546** (terrestrial point-to-area prediction), and **ITU-R P.528** (airborne/satellite).
  * **Parabolic Equation (PE) Models:** US Navy **APM (Advanced Propagation Model)** / **AREPS (Advanced Refractive Effects Prediction System)** and **TEMPER**, solving the Helmholtz wave equation over variable sea-surface roughness and 3D atmospheric refractivity profiles.
* **6.2 Tropospheric Ducting and Using AIS for Propagation Monitoring & Model Testing:**
  * Modified refractivity $M(z) = N(z) + \frac{z}{a_e}\times 10^6 \approx N(z) + 0.157 z$ (where $dM/dz < 0$ creates a trapping layer / duct).
  * Evaporation ducts, surface-based ducts, and elevated ducts carrying $162\text{ MHz}$ AIS signals $300\text{–}1,500+\text{ NM}$ over the horizon (e.g., Hepburn tropospheric ducting forecasts, Mediterranean, Arabian Gulf, California coast, North Sea).
  * **Inverting AIS Observations to Test Weather/RF Models:** Using continuous shore networks receiving known base stations and ships to measure real-time path loss $L(d, t)$ and invert for refractivity profiles $M(z)$ to benchmark Numerical Weather Prediction (NWP) models (ECMWF ERA5, NOAA GFS/HRRR).
* **6.3 Key Studies on AIS Propagation, Network Loading, and Packet Loss:**
  * **ITU-R Report M.2287-0:** *Assessment of the VHF data link loading* — empirical and simulation studies showing SOTDMA degradation when channel loading exceeds $50\%$ (nominal capacity) and severe slot collisions above $80\%$ (e.g., Northern Gulf of Mexico, Singapore/Malacca Strait, English Channel, Yangtze River Estuary).
  * **Spaceborne AIS Collision Modeling:** Hoye et al. (2008, *IEEE T-AES*), Eriksen et al. (2006/2010, FFI Norway), and Cervera et al. (2011) quantifying detection probability $P_d$ as a function of vessel count $N$ within a satellite's footprint.
  * **Terrestrial Coverage & Shadowing Studies:** USCG NAIS coverage modeling, JRC/EMSA coastal gap analyses, and Last et al. (2014/2015) empirical analyses of reporting interval compliance and packet drop rates.

#### Chapter 7: AIS Physical Layer: Bit Encoding, HDLC Framing, GMSK Modulation, and Salvaging Corrupted RF Recordings
* *Scope:* End-to-end RF encoding pipeline and advanced DSP techniques for recovering data from corrupted or colliding packets.
* **7.1 The Over-the-Air AIS Burst Structure ($26.667\text{ ms}$ / 256 bits at $9,600\text{ bps}$):**
  * Ramp-up ($8\text{ bits}$ / $833\text{ }\mu\text{s}$) $\rightarrow$ Training Sequence / Preamble ($24\text{ bits}$ alternating `0101...`) $\rightarrow$ Start Flag ($8\text{ bits}$, HDLC `0x7E` = `01111110`) $\rightarrow$ Data Payload ($168\text{ bits}$ for standard 1-slot message, sent LSB-first per byte) $\rightarrow$ Frame Check Sequence ($16\text{ bits}$ CRC-CCITT polynomial $G(x) = x^{16} + x^{12} + x^5 + 1$, initialized to `0xFFFF`, inverted) $\rightarrow$ End Flag ($8\text{ bits}$ `0x7E`) $\rightarrow$ Buffer ($24\text{ bits}$ for bit-stuffing expansion, propagation delay, and ramp-down).
* **7.2 Bit-Stuffing, NRZI, and GMSK Modulation:**
  * **Zero-bit stuffing:** Transmitter inserts a `0` bit after any five consecutive `1` bits in the data+CRC stream so payload data never mimics the `01111110` (`0x7E`) flag.
  * **NRZI (Non-Return-to-Zero Inverted):** Logical `0` produces a phase/frequency transition; logical `1` produces no transition (making the signal insensitive to $180^\circ$ phase inversion and turning the `010101...` preamble into a maximum-transition tone for clock recovery!).
  * **GMSK (Gaussian Minimum Shift Keying):** Modulation index $h = 0.5$ (peak frequency deviation $\Delta f = \pm 2.4\text{ kHz}$ at $R_b = 9,600\text{ bps}$), Gaussian pre-modulation filter bandwidth-time product $BT = 0.4$ (transmit) / $BT = 0.5$ (receive) for $25\text{ kHz}$ channels.
* **7.3 What Can Be Salvaged from RF Recordings with Packet Corruption and/or Collisions?**
  * **Soft-Decision CRC-16 Error Correction:** When a burst fails CRC by 1 to 3 bits due to thermal noise or impulse interference, identifying the lowest-confidence soft bits from the GMSK demodulator eye diagram and testing bit-flip syndromic candidates (or using Viterbi trellis demodulation of the continuous-phase GMSK memory).
  * **Prior-Aided Header Reconstruction:** Exploiting known active MMSIs in the local region and deterministic fields (Repeat Indicator, Message ID, Navigation Status, UTC Second) to constrain multi-bit error recovery.
  * **Partial Packet Forensics:** Even when the tail of a packet is destroyed by a mid-slot collision, the first $40\text{ bits}$ of the payload (Message ID, Repeat Indicator, and full 30-bit MMSI) arrive in the first $4.2\text{ ms}$ after the start flag and can be extracted with high confidence!
  * **Co-Channel Collision Separation in IQ Recordings:**
    * *Capture Effect:* Demodulating the stronger signal (+6 to +10 dB SINR) directly, then regenerating its clean GMSK waveform, subtracting it from the complex baseband IQ stream (**Successive Interference Cancellation — SIC**), and demodulating the weaker underlying packet.
    * *Timing, Carrier Frequency Offset (CFO), and Phase Separation:* Joint Maximum LikelihoodSequence Estimation (MLSE) and blind source separation exploiting differences in arrival time ($\Delta \tau$), Doppler shift ($\Delta f_d$), and carrier phase ($\Delta \phi$).

#### Chapter 8: Antenna Engineering and Selection Across Platforms
* *Scope:* Best antennas for large ships, small ships, very small systems, and shore collection stations, and the physics of *why*.
* **8.1 Gain vs. Vertical Beamwidth: The Fundamental Maritime Trade-Off:**
  * How collinear arrays achieve higher omnidirectional gain ($6\text{–}9\text{ dBi}$) only by compressing the vertical elevation beamwidth (from $78^\circ$ for a $\frac{1}{2}\lambda$ dipole down to $14^\circ\text{–}20^\circ$).
* **8.2 Best Antennas by Platform and Application:**
  * **Large Commercial Ships (SOLAS Tankers, Container Ships, Bulk Carriers):**
    * *Recommendation:* Heavy-duty fiberglass-radome $\frac{1}{2}\lambda$ coaxial dipole or low-gain collinear ($3\text{–}5\text{ dBi}$, vertical beamwidth $35^\circ\text{–}65^\circ$), DC-grounded at the base for lightning and static dissipation.
    * *Why:* Mounted at $30\text{–}60\text{ m}$ above sea level on the monkey island, height already provides a $15\text{–}20\text{ NM}$ horizon; moderate gain avoids losing link during $\pm 15^\circ$ heavy-weather rolling, while thick fiberglass resists funnel exhaust acids, icing, and vibration.
  * **Small Ships (Sailboats, Trawlers, Yachts, Workboats):**
    * *Recommendation:* Masthead $\frac{1}{2}\lambda$ stainless-steel whip ($3\text{ dBi}$, $78^\circ$ vertical beamwidth) for sailboats, or $3\text{–}6\text{ dBi}$ marine fiberglass whip for powerboats; active zero-loss VHF/AIS splitter if a second masthead run is impossible.
    * *Why:* A sailboat sailing upwind heels $20^\circ\text{–}35^\circ$ continuously; a high-gain $8\text{–}9\text{ dBi}$ collinear antenna on a heeled mast aims its narrow $16^\circ$ main lobe directly into the sea on one side and into the sky on the other, crippling reception!
  * **Very Small Systems (Kayaks, AIS-MOB, Fishing Buoys, Drones/UAVs, CubeSats):**
    * *Recommendation:* Tuned $162\text{ MHz}$ normal-mode helical ("rubber duck") or nitinol shape-memory $\frac{1}{4}\lambda$ whip (~$43\text{ cm}$) using sea water or chassis as a counterpoise (MOB/buoys); blade/monopole on UAVs; deployable tape-measure $\frac{1}{2}\lambda$ dipole, turnstile, or 2/3-element Yagi on LEO CubeSats.
    * *Why:* Size, weight, hydrodynamic drag, and immersion survival dominate; tuning must account for dielectric detuning when a buoy or lifejacket antenna is inches above salt water.
  * **Shore AIS Collection Stations:**
    * *Recommendation:* Commercial-grade exposed-dipole array or high-gain collinear ($6\text{–}9\text{ dBd}$ / $8\text{–}11\text{ dBi}$ omnidirectional) for $360^\circ$ coastal coverage, or vertically polarized **5- to 8-element Yagi-Uda / Corner Reflector** ($9\text{–}12\text{ dBd}$) aimed down narrow straits or harbor approaches, paired with $7/8\text{''}$ Heliax or LMR-400 coax, a tuned $162\text{ MHz}$ cavity/SAW bandpass filter, and a high-IP3 masthead LNA.
    * *Why:* Shore stations do not pitch or roll, allowing narrow vertical beamwidths to focus maximum sensitivity directly onto the distant sea horizon while directional Yagis reject rear-lobe urban RF interference.

#### Chapter 9: Transceiver Hardware, SDRs, and Building a Low-Budget Home AIS Station
* *Scope:* AIS hardware for receive and transmit, SDR architectures, and a complete practical chapter on building a low-budget home AIS receiver.
* **9.1 Shipboard and Shore AIS Hardware Internals:**
  * Class A (12.5 W, dual continuous receivers + 1 DSC receiver, mandatory MKD & pilot plug, IEC 61993-2) vs. Class B CSTDMA (2 W, carrier-sense, IEC 62287-1) vs. Class B SOTDMA / "Class B+" (5 W, guaranteed time-slot reservation, higher speed-dependent reporting rate, IEC 62287-2).
  * Dedicated hardware receivers: dAISy (Wegmatt), Quark-elec, Comar, Digital Yacht, Shine Micro (ultra-high-sensitivity military/USCG receivers).
* **9.2 Software-Defined Radios (SDRs) for AIS Receive and Transmit:**
  * **Receive-Only SDRs:** RTL-SDR Blog V3/V4 (RTL2832U + R828D, 8-bit ADC, 0.5 ppm TCXO), Airspy Mini / R2 (12-bit ADC, high dynamic range), SDRplay RSP1B / RSPdx (14-bit ADC, built-in notch filters).
  * **Transmit-Capable Transceiver SDRs (Lab & Authorized Testing Only):** HackRF One (half-duplex, 8-bit), Great Scott Gadgets / Nuand bladeRF 2.0 micro, Analog Devices ADALM-Pluto (PlutoSDR), Ettus Research USRP B200/B210/N210.
  * *Regulatory & Hardware Warning:* Harmonics of unfiltered SDR transmitters ($324\text{ MHz}$ 2nd harmonic in military UHF satcom band, $486\text{ MHz}$ 3rd harmonic), requirement to test transmit chains exclusively into $50\text{ }\Omega$ dummy loads / shielded RF enclosures with $30\text{–}40\text{ dB}$ attenuators.
* **9.3 Step-by-Step Build Guide: Recommended Low-Budget Home AIS Receiver Setup:**
  * **Hardware Bill of Materials (<$120–$200 total):**
    1. *Compute:* Raspberry Pi 4B / Pi 5, Pi Zero 2 W, or repurposed $40 thin client running Ubuntu/Debian Linux.
    2. *Receiver Option A (SDR):* RTL-SDR Blog V4 ($30, 0.5 ppm TCXO) — supports simultaneous AIS1 + AIS2 reception at $288\text{ kS/s}$ or $1.536\text{ MS/s}$.
    3. *Receiver Option B (Low-Power Dedicated MCU):* Wegmatt dAISy HAT or dAISy 2+ dual-channel receiver (~$65–$90, $<100\text{ mW}$ power draw).
    4. *RF Filter (Crucial!):* $162\text{ MHz}$ SAW bandpass filter (e.g., Sysmocom / Upronics $162\text{ MHz}$ AIS filter) or FM broadcast bandstop filter to prevent ADC overload from $88\text{–}108\text{ MHz}$ FM stations and $162.40\text{–}162.55\text{ MHz}$ NOAA Weather Radio.
    5. *Antenna & Feedline:* Homebrew coaxial collinear / Slim-Jim / $\frac{1}{2}\lambda$ J-pole built from copper pipe or RG-213, or commercial Shakespeare/Tram $162\text{ MHz}$ marine antenna, fed via low-loss LMR-400 or RG-8X coax with a gas-discharge lightning arrestor.
  * **Software Pipeline:**
    * Installing and tuning **`AIS-catcher`** (Jasper Vries — C++ multi-model coherent GMSK demodulator with built-in web GUI, Prometheus metrics, and JSON/NMEA UDP/TCP output) vs. `rtl-ais`.
    * Multiplexing NMEA 0183 + TAG blocks with **`kplex`**, **`gpsd`**, or **`Signal K`**.
    * Local visualization in **`OpenCPN`** or **`AIS-catcher` Web Viewer**, archiving to local **DuckDB / Parquet / SQLite**, and feeding community aggregators (AISHub, MarineTraffic, VesselFinder, APRS.fi).

#### Chapter 10: Shore and At-Sea Collection Site Engineering, Placement, and Global Networks
* *Scope:* Where to place AIS receivers on shore and at sea, places to strictly avoid, and the ecosystem of AIS collection networks.
* **10.1 Shore Collection Site Options and Elevation Trade-Offs:**
  * **Towers, Lighthouses, and Coastal High-Rises:** Utilizing USCG lighthouses, port control towers, coastal hotel/condo roofs, and mountaintop communication sites.
  * **The "Too High" Elevation Paradox:** Why placing a shore receiver on a $1,000\text{ m}$ coastal mountain peak extends the radio horizon beyond $80\text{–}100\text{ NM}$, pulling in 3 to 5 independent SOTDMA cells simultaneously and causing severe co-channel time-slot collisions that *reduce* close-range packet reception unless directional sector antennas are used!
* **10.2 Places to Strictly Avoid When Siting an AIS Receiver:**
  * **Near Large Radar Installations:** Airport surveillance radars (ASR/ARSR), coastal VTS S-band/X-band radars, military phased-array radars, and Nexrad weather radars. High peak-pulse power (kilowatts to megawatts) induces front-end LNA saturation, mixer diode burnout, or intermediate-frequency (IF) breakthrough.
  * **Near NOAA Weather Radio (NWR) Transmitters:** NWR broadcasts *continuously* (100% duty cycle) at $100\text{–}1,000\text{ W}$ on seven channels from **$162.400\text{ MHz}$ to $162.550\text{ MHz}$**—a mere **$375\text{ kHz}$ above AIS 2 ($162.025\text{ MHz}$)**! Standard SDR front-ends and wide ceramic filters cannot reject a $1\text{ kW}$ signal $375\text{ kHz}$ away, resulting in total receiver desensitization, ADC clipping, and reciprocal mixing of transmitter phase noise across AIS1 and AIS2. Requires physical separation and high-Q helical cavity filters.
  * **Other Hostile RF Environments:** Hospital/commercial VHF paging transmitters ($152\text{–}158\text{ MHz}$), high-power FM broadcast farms ($88\text{–}108\text{ MHz}$ third-order intermodulation $2f_1 - f_2 \approx 162\text{ MHz}$), and high-voltage substations (corona discharge noise).
* **10.3 At-Sea Collection Platforms:**
  * **Offshore Buoys & Platforms:** NOAA National Data Buoy Center (NDBC) weather buoys, USCG offshore AtoN buoys, offshore oil/gas rigs, and offshore wind farm substations.
  * **Autonomous Surface Vessels (ASVs) & USVs:** Liquid Robotics **Wave Gliders**, **Saildrone** wind/solar USVs, OceanAero, and SeaTrac platforms acting as mobile persistent maritime picket receivers with Iridium/Starlink backhaul.
* **10.4 Global AIS Collection Networks and Data Providers:**
  * Commercial satellite & terrestrial providers: **Spire Maritime** (formerly exactEarth), **ORBCOMM**, **Kpler / MarineTraffic**, **VesselFinder**, **FleetMon**, **Pole Star**, **Lloyd's List Intelligence**, **S&P Global Market Intelligence**.
  * Open/Community networks: **AISHub**, **APRS.fi**, **PocketMariner**, **Norwegian Coastal Administration (Kystverket) open AIS**, **Danish Maritime Authority (DMA) open archives**, **NOAA/BOEM MarineCadastre.gov**.
  * Government/Defense networks: **USCG NAIS**, **DoD/DOT Volpe MSSIS** (Maritime Safety and Security Information System), **EMSA SafeSeaNet**.

---

### PART III: Timing, GNSS Dependencies, Synchronization, and Protocol Internals

#### Chapter 11: Timing Signals in AIS: Architecture, Practice, Robustness, and Timing Attacks
* *Scope:* How timing signals are passed through AIS, internal vs. external timing, hardware without GNSS, and whether timing manipulation can collapse an AIS dynamic network.
* **11.1 How Timing Signals Are Passed Through the AIS System:**
  * The 60-second UTC frame divided into $2,250\text{ time slots}$ per channel ($\Delta t_{\text{slot}} = \frac{60\text{ s}}{2250} = 26.6667\text{ ms} = 256\text{ bits}$).
  * Required slot boundary synchronization accuracy: jitter $< \pm 104\text{ }\mu\text{s}$ ($\pm 1\text{ bit}$) at the mobile station, and $< \pm 2.6\text{ }\mu\text{s}$ to UTC for Direct UTC stations, accommodated by the 24-bit end-of-slot buffer ($2.5\text{ ms}$ total guard time, supporting $\sim 200\text{ NM}$ propagation delay).
* **11.2 Internal vs. External Timing Sources: Does Any Hardware Not Use GNSS for Timing?**
  * **Why NMEA 0183 Serial Sentences Cannot Synchronize TDMA Slots:** External GNSS sentences (`$GPZDA`, `$GPRMC`, `$GPGGA`) over a $4,800\text{ bps}$ or $38,400\text{ bps}$ serial bus suffer from $50\text{–}500\text{ ms}$ variable serialization latency—thousands of times too slow for microsecond TDMA slot edges!
  * **Internal GNSS 1PPS (One Pulse Per Second):** Consequently, IEC 61993-2 mandates that every Class A transponder contain an **internal GNSS receiver** dedicated to generating a hardware **1PPS timing pulse** aligned to UTC, even when the ship uses an external primary DGNSS receiver on the bridge for its transmitted latitude and longitude.
  * **Hardware That Does Not Use GNSS for Timing:**
    1. *Receive-only AIS receivers and SDRs:* Do not transmit, so they need no TDMA slot clock; they timestamp arrivals using host NTP/PTP system time.
    2. *Class B CSTDMA (IEC 62287-1) in fallback:* Uses Carrier Sense (listening for RSSI below threshold for $1.75\text{ ms}$) aligned to received peer/base-station slot boundaries.
    3. *Shore Base Stations & Repeaters:* Can use external **Rubidium/Cesium atomic clocks**, **IEEE 1588 Precision Time Protocol (PTP)** over fiber, or **eLORAN** 1PPS inputs to maintain Sync State 0 during GNSS outages.
* **11.3 The 4-Tier AIS Synchronization State Hierarchy (ITU-R M.1371 Annex 2):**
  * **Sync State 0 (UTC Direct):** Synchronized directly to an internal/external UTC source (GNSS 1PPS or atomic clock).
  * **Sync State 1 (UTC Indirect):** Synchronized to the slot boundaries of another station that reports Sync State 0.
  * **Sync State 2 (Base Station Sync):** Synchronized to a Base Station broadcasting Message 4.
  * **Sync State 3 (Peer Mobile Station Sync):** Synchronized to the mobile station currently receiving the highest number of other stations ("semaphore" / cluster-head synchronization).
* **11.4 Can You Cause an AIS Dynamic Network to Fail by Messing with the Timing?**
  * **Yes — Detailed Vulnerability & Failure Analysis:**
    1. *GNSS Time-Walk Spoofing:* If an adversary spoofs GNSS signals in a harbor and slews the spoofed 1PPS clock away from true UTC by $5\text{–}15\text{ ms}$, vessels inside the spoofed bubble transmit across the mid-points of two adjacent legitimate time slots of vessels outside the bubble, doubling collision rates and corrupting both slots.
    2. *Rogue Base Station (Message 4) Desynchronization:* Vessels that lose GNSS fall back to Sync State 2 (trusting Message 4). A high-power rogue transmitter broadcasting Message 4 with skewed slot timing and `Sync State = 0` will pull all GNSS-denied transponders onto skewed slot boundaries.
    3. *FATDMA Slot Starvation (Message 20) & Assigned Mode (Message 16) Abuse:* Forging Base Station Message 20 packets to reserve all 2,250 slots across the frame, or sending Message 16/23 to force transponders into 10-minute silent intervals or invalid channels.

#### Chapter 12: GNSS Systems Overview, Support Matrix, GNSS-Denied Operations, and Jamming Workarounds
* *Scope:* Overview of global GNSS systems, which AIS hardware supports which constellation, what happens in GNSS-denied locations, and GNSS jamming workarounds.
* **12.1 Overview of GNSS and Augmentation Systems:**
  * **GPS** (US Space Force, L1 C/A $1575.42\text{ MHz}$), **GLONASS** (Russia, L1OF FDMA/CDMA), **BeiDou / BDS** (China, B1I/B1C), **Galileo** (European Union, E1 OS).
  * **SBAS** (WAAS, EGNOS, MSAS, GAGAN, SDCM) and **Maritime Radio Beacon DGNSS** ($283.5\text{–}325\text{ kHz}$ MF beacons & AIS Message 17 DGNSS corrections).
* **12.2 GNSS Support Breakdown Across AIS Systems: Do Any AIS Systems Not Include Support for GPS?**
  * *Legacy Generation (2000–2012):* GPS-only (single-constellation L1 C/A modules).
  * *Modern Commercial Generation (2013–present):* Multi-GNSS chipsets (u-blox M8/M9/F9, Quectel, Septentrio) supporting GPS + GLONASS + Galileo + BeiDou concurrently, compliant with IMO Resolution MSC.401(95) / MSC.466(101) (Multi-System Shipborne Radionavigation Receiver).
  * *Systems Without GPS or Configured in Non-GPS Modes:*
    * Domestic Chinese fishing fleet **BeiDou-only** terminals (BDS RDSS short-message + B1 positioning transponders subsidized by provincial fisheries bureaus).
    * Russian domestic/Arctic maritime transponders configured in **GLONASS-only** sovereign mode.
    * Fixed **AIS Base Stations** and **Synthetic/Virtual AtoN** generators where static coordinates are surveyed once and hard-coded in firmware.
* **12.3 What Happens to AIS in a GNSS-Denied Location?**
  * **Position Payload Behavior:**
    * If no external fallback sensor is connected, Longitude is set to `181.0°` (`0x6791AC0`), Latitude to `91.0°` (`0x3412140`), SOG to `102.3 kts` (unavailable), COG to `360.0°` (unavailable), and the `Time Stamp` second field switches from `0–59` to **`61` (manual input mode)**, **`62` (dead reckoning / estimated mode)**, or **`63` (positioning system inoperative)**.
    * If integrated with a shipboard INS / Gyrocompass + Doppler Speed Log on an Integrated Navigation System (INS), the transponder continues broadcasting dead-reckoned positions with `Time Stamp = 62` and `Position Accuracy = 0`, drifting with current/wind leeway over time.
  * **TDMA Slot Timing Behavior:** Automatic transition from Sync State 0 $\rightarrow$ Sync State 1 $\rightarrow$ Sync State 2 (Base Station) $\rightarrow$ Sync State 3 (Peer sync), maintaining collision-free VHF transmission even when lat/lon is `181°/91°`!
* **12.4 GNSS Jamming & Spoofing Impacts on AIS and Practical Workarounds:**
  * **Real-World Conflict & Grey-Zone Hotspots:** Baltic Sea ("Baltic Jammer" in Kaliningrad/St. Petersburg), Black Sea & Kerch Strait, Eastern Mediterranean (Cyprus/Levant), Red Sea, Strait of Hormuz, and Chinese port "crop circle" spoofing (documented by C4ADS, 2019).
  * **Technical Workarounds:**
    1. **R-Mode (Ranging Mode):** Measuring Time-of-Arrival (TOA) / Time-Difference-of-Arrival (TDOA) of shore-based AIS Base Station bursts, VDES terrestrial bursts, and MF DGNSS beacon carriers (Baltic R-Mode testbed) to compute horizontal position (~10–15 m accuracy) completely independent of satellites!
    2. **eLORAN (Enhanced LORAN):** High-power ($100\text{–}1,000\text{ kW}$) $100\text{ kHz}$ low-frequency terrestrial navigation and sub-microsecond UTC timing immune to low-power L-band GNSS jammers.
    3. **CRPA (Controlled Reception Pattern Antennas) & Multi-Band GNSS:** Null-steering phased-array GNSS antennas that place spatial nulls toward horizon jammers while preserving zenith satellite signals.
    4. **Inertial / Acoustic / Radar Terrestrial Coupling:** Tightly coupled Fiber-Optic Gyro (FOG) INS + Doppler Velocity Log (DVL) bottom-track + Radar Terrain/Coastline Matching (Radar Map Matching in ECDIS).

#### Chapter 13: What Is an MMSI? Deep Dive into Maritime Identity
* *Scope:* Comprehensive breakdown of Maritime Mobile Service Identities (ITU-R M.585-9), allocation rules, and identity anomalies.
* **13.1 The 9-Digit MMSI Structure and MID (Maritime Identification Digits):**
  * How the 3-digit **MID** (`201` to `775`) maps to flag states and geographical administrations (e.g., `200–399` Europe/North America, `303/338/366–369` USA, `316` Canada, `351–357/370–374` Panama, `412–414` China, `563–566` Singapore, `636` Liberia, `538` Marshall Islands).
* **13.2 Complete Taxonomy of MMSI Categories (ITU-R M.585-9):**
  * **Ship Stations (`MIDxxxxxx`):** Standard 9-digit vessel identity; trailing-zero rules (`MIDxxx000`, `MIDxxxx00`, `MIDxxxxx0`) historically tied to Inmarsat B/C/M satellite dialing routing.
  * **Group Ship Stations (`0MIDxxxxx`):** Addressing fleets or company vessels simultaneously.
  * **Coast / Base Stations (`00MIDxxxx`):** Shore VTS and USCG/national AIS base stations.
  * **Search and Rescue (SAR) Aircraft (`111MIDxxx`):** Fixed-wing (`111MID1xx`) and rotary-wing helicopters (`111MID5xx`).
  * **Craft Associated with a Parent Ship (`98MIDxxxx`):** Lifeboats, tenders, daughter craft, and ship-launched USVs/workboats.
  * **Aids to Navigation — AtoN (`99MIDxxxx`):** Physical (`99MID1xxx`) and virtual (`99MID6xxx`) buoys, beacons, and lighthouses.
  * **Free-Form / Emergency & Autonomous Devices (`97xxxxxxx`):**
    * `970xxyyyy`: **AIS-SART** (Search and Rescue Transmitter, where `xx` = manufacturer ID).
    * `972xxyyyy`: **AIS-MOB** (Man Overboard device).
    * `974xxyyyy`: **EPIRB-AIS** (Emergency Position Indicating Radio Beacon with AIS homing).
    * `979zzzzzz`: **AMRD Group B** (Autonomous Maritime Radio Devices, ITU-R M.2135).
* **13.3 MMSI Failure Modes, Default Collisions, and Identity Laundering:**
  * The curse of unconfigured transponders: `000000000`, `111111111`, `123456789`, `999999999`, or bare MIDs (`366000000`) creating worldwide "teleporting monster tracks" when naive software groups by MMSI alone.
  * Why MMSI changes whenever a ship re-flags, whereas the **7-digit IMO number** ($d_7 = (7d_1 + 6d_2 + 5d_3 + 4d_4 + 3d_5 + 2d_6) \bmod 10$) stays with the hull for life.

#### Chapter 14: Shipboard Buses and Sharing/Logging Standards: NMEA 0183, NMEA 2000, NMEA TAG Blocks, and VDRs
* *Scope:* What are the standards for sharing and logging AIS on ships and shore networks?
* **14.1 NMEA 0183 / IEC 61162-1 & -2 (High-Speed 38,400 bps):**
  * Electrical layer: RS-422 differential signaling (`TX+/TX-`, `RX+/RX-`, opto-isolated inputs) vs. legacy single-ended RS-232 ground-loop hazards.
  * Sentence anatomy: `!AIVDM,1,1,,A,15M67FC000G?ufbE`FepT@3n00Sa,0*5C`
    * Talker IDs: `AI` (Mobile AIS), `AB` (Base Station), `AD` (Dependent Base), `AN` (AtoN), `AR` (Receiving Station), `AS` (Limited Base), `AT` (Transmitting Station), `AX` (Repeater), `BS` (Legacy Base).
    * `VDM` (VHF Data-link Message — received from other vessels) vs. `VDO` (VHF Data-link Own-vessel report — local transponder self-report).
    * Multi-sentence fragmentation (`1..9`), sequential message ID, channel code (`A`/`B`/`1`/`2`), **6-bit ASCII armor payload** (mapping 6-bit values `0–63` to ASCII `0x30–0x57` and `0x60–0x77`), fill bits (`0–5`), and 8-bit XOR checksum (`*HH`).
* **14.2 NMEA TAG Blocks (IEC 61162-1 / IEC 61162-450 / USCG NAIS Format):**
  * Solving the biggest limitation of raw `!AIVDM` (which lacks a full UTC date/year and receiver provenance!).
  * Syntax: `\s:r003669945,c:1712250000,g:1-2-7384*5A\!AIVDM,2,1,3,A,...`
  * Standard parameters: `c:` (UNIX epoch timestamp in seconds or milliseconds), `s:` (source/station identifier), `d:` (destination), `g:` (sentence grouping for multi-line messages), `n:` (line count), `r:` (relative time), `t:` (text), plus vendor extensions for RSSI (`r:`/`S:`), SNR, and frequency offset.
* **14.3 NMEA 2000 (IEC 61162-3) and OneNet / IEC 61162-450 (LWE):**
  * **NMEA 2000:** Controller Area Network (CAN 2.0B, $250\text{ kbps}$, 29-bit CAN ID), Fast-Packet protocol for multi-frame payloads, and AIS Parameter Group Numbers (**PGNs**): `129038` (Class A Position), `129039` (Class B Position), `129040` (Class B Extended), `129041` (AtoN), `129793` (UTC/Date/Base Station), `129794` (Class A Static & Voyage), `129798` (SAR Aircraft), `129802` (Safety Broadcast), `129809` (Class B Static Part A), `129810` (Class B Static Part B).
  * **The NMEA 0183 $\leftrightarrow$ NMEA 2000 Translation Trap:** Why converting `!AIVDM` to NMEA 2000 PGNs and back is not always bit-exact (unit conversions from $1/10\text{ knot}$ and $1/10\text{ deg}$ to SI $\text{m/s}$ and $\text{radians}$, plus unsupported binary ASM PGNs).
  * **IEC 61162-450 (Lightweight Ethernet — LWE):** UDP multicast (`239.192.0.1`–`239.192.0.16`, ports `60001`–`60016`) carrying `UdPbC\0` header + NMEA TAG block + `!AIVDM` sentences across modern integrated ship bridges.
* **14.4 Voyage Data Recorders (VDR and S-VDR):**
  * IMO Resolution MSC.333(90) (revised VDR performance standards, effective July 2014) and IEC 61996-1/2.
  * Architecture: Fixed protective capsule (surviving $1,100^\circ\text{C}$ fire for 1 hour and $6,000\text{ m}$ deep-sea pressure), float-free capsule (EPIRB-integrated, min 48 hours), and long-term internal SSD recording (min 30 days / 720 hours).
  * How VDR logs all incoming (`!AIVDM`) and outgoing (`!AIVDO`) AIS traffic alongside bridge audio microphones, VHF audio, radar/ECDIS image captures (every 15 seconds), and shipboard sensor buses, and how casualty investigators extract and replay VDR AIS archives.

#### Chapter 15: Complete ITU-R M.1371 Message Catalog (Messages 1–27)
* *Scope:* Bit-by-bit technical reference for all 27 standard AIS message types.
* **15.1 Dynamic Position Reports:**
  * **Messages 1, 2, 3 (Class A Position Report):** Navigation Status (0–15), Rate of Turn ($ROT_{\text{AIS}} = 4.733 \sqrt{\text{ROT}_{\^\circ/\text{min}}}$, signed 8-bit `-128` to `+127`), SOG ($0.1\text{ kt}$ resolution), Position Accuracy (1 = $\le 10\text{ m}$ DGNSS, 0 = $>10\text{ m}$), Longitude/Latitude ($1/10,000\text{ min} = 1/600,000^\circ$ in 28/27-bit two's complement, resolution $\sim 0.18\text{ m}$), COG ($0.1^\circ$), True Heading ($0\text{–}359^\circ$, `511` = unavailable), Time Stamp (`0–63`), Maneuver Indicator (blue sign / special maneuver), RAIM flag, and 19-bit SOTDMA/ITDMA communication state.
  * **Messages 18 & 19 (Class B Standard & Extended Position Reports):** Replacing ROT and Navigation Status with Class B CS/SO flags, Display/DSC/Band/Msg22 capability flags.
  * **Message 27 (Long-Range AIS Broadcast Message):** Compact 96-bit (instead of 168-bit) payload with $1/10\text{ min}$ ($\sim 185\text{ m}$) lat/lon resolution, whole-knot SOG, and $1^\circ$ COG designed specifically for zero-reservation satellite reception on Channels 75 and 76.
* **15.2 Static and Voyage Data:**
  * **Message 5 (Class A Static and Voyage Related Data):** 2-slot message (424 bits) carrying AIS Version, IMO Number, Call Sign, 20-char Vessel Name, Ship and Cargo Type (codes 10–99), Dimensions to Bow/Stern/Port/Starboard (encoding GPS antenna reference point offset on the hull!), EPFD type, ETA (Month/Day/Hour/Minute), Maximum Present Static Draught ($0.1\text{ m}$), and 20-char Destination.
  * **Message 24 (Class B Static Data Report):** Split into **Part A** (Vessel Name) and **Part B** (Ship Type, Vendor ID, Unit Model/Serial, Call Sign, and either Hull Dimensions or Mother-Ship MMSI) so each part fits in a single 168-bit slot.
* **15.3 Base Station, Network Control, Safety, and Aids to Navigation:**
  * **Messages 4 & 11 (Base Station Report & UTC/Date Response):** Full UTC Year/Month/Day/Hour/Minute/Second and SOTDMA frame sync.
  * **Message 9 (Standard SAR Aircraft Position Report):** Altitude in meters ($0\text{–}4094\text{ m}$), SOG in whole knots ($0\text{–}1022\text{ kts}$), DTE flag.
  * **Messages 10, 12, 13, 14, 15, 16, 17, 20, 22, 23:** UTC Inquiry (10), Addressed/Broadcast Safety Text & Ack (12/13/14), Interrogation (15), Assigned Mode (16), DGNSS Binary Broadcast (17), Data Link Management / FATDMA reservation (20), Channel Management (22), Group Assignment (23).
  * **Message 21 (Aids-to-Navigation Report):** 272–360 bits; AtoN Type (0–31: cardinal marks, lateral marks, racons, lighthouses, offshore structures), Name + Name Extension, Off-Position Indicator, **Virtual AtoN flag**, and Assigned Mode flag.

#### Chapter 16: Binary Messages, Application-Specific Messages (ASM), Tides/Marine State, and Area Notices
* *Scope:* Deep dive into Messages 6, 7, 8, 25, and 26, environmental/tide transmissions, and Area Notices (`ais-area-notice`).
* **16.1 Architecture of AIS Binary Messages (Msgs 6, 8, 25, 26):**
  * Designated Area Code (**DAC**, 10 bits — `1` = International IMO, `200` = European Inland, `316` = Canada, `366` = USA) + Function Identifier (**FI**, 6 bits).
  * Evolution from IMO SN/Circ.236 (2004 trial messages) to **IMO SN.1/Circ.289** (2010, effective 2013) and the IALA ASM Collection.
* **16.2 Tide, Water Level, Current, and Meteorological/Hydrographic Transmissions:**
  * **IMO Met/Hydro Messages:** Legacy DAC 1 FI 11 (deprecated due to ambiguous wind/current encoding) vs. modern **DAC 1 FI 31** (360 bits: wind speed/gust/direction, air temp, relative humidity, dew point, atmospheric pressure & tendency, horizontal visibility, **water level / tide including trend** with $1\text{ cm}$ resolution, surface & multi-depth current speed/direction, significant wave height/period/direction, swell, sea state Beaufort scale, water temp, precipitation, salinity, and sea ice).
  * **Regional Environmental Broadcasts:**
    * **USCG & NOAA PORTS® (Physical Oceanographic Real-Time System):** Broadcasting real-time tide gauges, bridge air gap, currents, and meteorology over AIS AtoNs and Base Stations in US harbors (Tampa Bay, Columbia River, Chesapeake Bay, New York/New Jersey, San Francisco).
    * **St. Lawrence Seaway & Great Lakes (DAC 316 / DAC 366):** Water level, lock schedules, current/wind, and vessel draft/conveyance messages.
    * **RTCM Standard 12301.1:** Standardizing environmental, tidal, and maritime safety binary payloads in North America.
* **16.3 Area Notice (DAC 1 FI 22 / USCG DAC 366 FI 22) and `ais-area-notice`:**
  * Dynamic broadcasting of geometric regions (circles/points, rectangles, sectors, polylines, polygons, and associated text) with scale factors, start times, and durations for exclusion zones, military firing areas, ice fields, oil spills, and **Whale Alert** right-whale management zones.

---

### PART IV: Spaceborne, Airborne, and Specialized AIS Subsystems

#### Chapter 17: Satellite AIS (S-AIS): Orbital RF Reception, De-Collision DSP, and Satellite Transmission
* *Scope:* How satellites receive and process AIS RF, and whether satellites have ever transmitted AIS.
* **17.1 Physics and Geometry of Spaceborne AIS Reception:**
  * A LEO satellite at $550\text{ km}$ altitude has a slant-range horizon radius of $\sim 2,650\text{ km}$ (covering a circular footprint of $>20\text{ million km}^2$), simultaneously illuminating **hundreds of independent $40\text{ NM}$ terrestrial SOTDMA cells**.
  * Because SOTDMA only coordinates slot reservations locally within line-of-sight ($\sim 40\text{ NM}$), vessels in different cells reuse the exact same time slots, producing **severe co-channel packet collisions** at the satellite antenna.
  * Additional orbital channel impairments:
    * **Doppler Shift & Rate:** Up to $\pm 3.8\text{ kHz}$ carrier offset (exceeding the $\pm 2.4\text{ kHz}$ GMSK modulation deviation!) and $\pm 45\text{ Hz/s}$ Doppler rate.
    * **Time-of-Arrival Spread:** Slant range varies from $550\text{ km}$ (nadir) to $2,700\text{ km}$ (horizon), introducing up to $7.2\text{ ms}$ (~69 bits) of differential propagation delay across the footprint, overflowing the $2\text{ ms}$ terrestrial guard buffer.
    * **Ionospheric Faraday Rotation:** Rotating linear vertical polarization by a frequency- and TEC-dependent angle $\Omega \propto \text{TEC}/f^2$.
* **17.2 Spaceborne De-Collision Architectures and Message 27:**
  * **Dedicated Satellite Channels (Ch 75 & 76, Message 27):** Class A vessels outside coastal base station coverage transmit a $9.6\text{ ms}$ (96-bit) unscheduled burst every 3 minutes on $156.775 / 156.825\text{ MHz}$, slashing burst duration by $64\%$ and eliminating Class B interference.
  * **Onboard vs. Ground-Based Spectrum Processing:** Digitizing raw multi-antenna IQ baseband on the satellite, applying multi-beam phased-array spatial filtering (nulling high-density coastal zones), blind Doppler/delay bank filtering, and iterative Successive Interference Cancellation (SIC).
  * Historical satellite missions: TACSAT-2 (2006), Rubin-7/8, Orbcomm Gen-1/OG2, Norwegian **AISSat-1/2** (2010/2014) and **NorSat-1/2/3/TD**, COM DEV / exactEarth / **Spire Lemur-2** CubeSat constellation.
* **17.3 Have Satellites Ever Transmitted AIS?**
  * **Why Standard Terrestrial AIS1/AIS2 Downlink from Orbit Is Problematic:** A satellite transmitting on $161.975 / 162.025\text{ MHz}$ illuminates thousands of ships across multiple SOTDMA cells with up to $7\text{ ms}$ propagation delay spread, colliding with local ship-to-ship safety traffic and lacking per-cell slot synchronization.
  * **Historical Experiments and Specialized Satellite Transmissions:**
    1. *Experimental Satellite-to-Ship AIS Broadcast/Interrogation Trials:* Early demonstrations (including **NorSat-2** launched in 2017 by the Norwegian Space Agency / FFI with a Kongsberg Seatex VDE-SAT / ASM transmitter payload) tested broadcasting Application Specific Messages (ASM, e.g., ice charts and SAR notices) from LEO to shipboard receivers.
    2. *The Operational Solution — VDE-SAT (AIS 2.0 / ITU-R M.2092):* Modern maritime satellites (**NorSat-TD** and **Sternula-1**, both launched in 2023, followed by Ymir-1 and AOS constellations) actively transmit to ships using the dedicated **VDE-SAT downlink channels** ($160.9625\text{–}161.4875\text{ MHz}$ and $161.950 / 162.000\text{ MHz}$ ASM), providing true two-way satellite-to-ship and ship-to-satellite digital messaging without disrupting AIS1/AIS2 collision avoidance!

#### Chapter 18: AIS in Aircraft, Drones (UAVs), Search and Rescue, and Direction Finding
* *Scope:* Airborne AIS transmission and reception on manned aircraft and drones, SAR transponders, and VHF Direction Finding (DF).
* **18.1 AIS in Manned Aircraft and Unmanned Aerial Vehicles (Drones / UAVs):**
  * **Transmitting from SAR Aircraft (Message 9):** MMSI `111MIDxxx`; transmitting barometric/GNSS altitude (meters), high-speed SOG ($0\text{–}1022\text{ kts}$), and SOTDMA/ITDMA states so surface vessels and Rescue Coordination Centers (RCCs) see the aircraft on ECDIS.
  * **Airborne ISR Collection (Patrol Aircraft & UAVs):** Integration on USCG HC-130J / MH-60T (via Minotaur), US Navy P-8A Poseidon / MQ-4C Triton, Frontex/EMSA patrol aircraft, and tactical maritime UAVs (Insitu ScanEagle, Schiebel Camcopter S-100, General Atomics MQ-9B SeaGuardian, Shield AI V-Bat).
  * **The Airborne Radio Horizon & Multi-Cell Collision Problem:** At $10,000\text{ ft}$ ($3,048\text{ m}$), the radio horizon is $d \approx 2.23\sqrt{3048} \approx 123\text{ NM}$, spanning $\sim 9$ terrestrial SOTDMA cells and requiring high-dynamic-range receivers (e.g., Shine Micro SA161-UA) and de-collision processing.
* **18.2 Search and Rescue AIS Devices (AIS-SART, AIS-MOB, EPIRB-AIS):**
  * **AIS-SART (IEC 61097-14):** Replaces or supplements 9 GHz X-band radar SARTs; MMSI `970xxyyyy`; transmits 8 bursts per minute (4 on AIS1, 4 on AIS2) using Message 1 (with `Navigation Status = 14` [SART active], rendered on ECDIS/MKD as a circle with a cross inside) and Message 14 (`"SART ACTIVE"` or `"SART TEST"`).
  * **AIS-MOB (IEC 63269 / RTCM 11901.1) & EPIRB-AIS:** Lifejacket-mounted Man Overboard beacons (`972xxyyyy`) with DSC distress loop alerting, and 406 MHz Cospas-Sarsat EPIRBs (`974xxyyyy`) with integrated AIS local homing.
* **18.3 AIS and Radio Direction Finding (RDF / DF) Systems:**
  * Combining VHF Doppler / Adcock / Watson-Watt direction-finding antenna arrays (Rohde & Schwarz DDF, Techtest/Cobham SeaHomer, Taiyo Musen, RhoTheta) with AIS packet decoding.
  * **Dual Operational Purpose:**
    1. *SAR Homing:* Providing instantaneous visual relative bearing to an AIS-SART/MOB even before its internal GPS acquires a 3D fix!
    2. *Counter-Spoofing & Dark-Target Verification:* Measuring the physical **Angle of Arrival (AoA)** (and multi-station triangulation line-of-bearing) of every $26.67\text{ ms}$ AIS RF burst and comparing it against the computed bearing to the `(lat, lon)` claimed inside the decoded payload. Any discrepancy immediately flags an RF spoofer!

#### Chapter 19: AIS for Fishing Gear, Autonomous Maritime Radio Devices (AMRDs), and Unintended User Hacks
* *Scope:* Fishing gear net-buoys, spectrum pollution, regulatory responses, and the creative hacks users have invented for AIS.
* **19.1 AIS for Fishing Gear: Utility vs. Spectrum Crisis:**
  * How longline, gillnet, purse-seine, and crab/lobster fleets adopted low-cost ($30–$80) uncertified Chinese AIS "net pingers" / "sun-buoys" to track drifting gear and Fish Aggregating Devices (FADs), broadcasting every 30 seconds to 3 minutes at $2\text{–}10\text{ W}$ using fabricated MMSIs (`190...`, `888...`, `999...`) and Message 1, 18, or 21.
  * **Operational Hazards:** A single longliner may deploy 20 to 100 AIS net buoys spanning $50\text{ NM}$. Commercial ships transiting fishing grounds see hundreds of fake "vessels" or "AtoNs" cluttering ECDIS/radar, overflowing target tables, saturating VDL time slots, and causing bridge officers to mute CPA/TCPA collision alarms!
  * **Regulatory Solution — ITU-R M.2135 (AMRD):** Splitting Autonomous Maritime Radio Devices into **AMRD Group A** (safety-related, e.g., MOB, permitted on AIS 1/2) and **AMRD Group B** (non-navigation gear, e.g., fishing net buoys, ocean drifters), restricting Group B to **Channel 2006 ($160.900\text{ MHz}$)** at $\le 1\text{ W}$ ERP with MMSI prefix `979`.
* **19.2 What Hacks Have Users Come Up With to Use the AIS System in Unintended Ways?**
  * **1. Free Text Messaging & Status Codes in Metadata Fields:** Using Message 5 `Destination` or `Vessel Name` and Message 14 `Safety Broadcast` as a free global SMS/bulletin board: broadcasting `"ARMED GUARDS ON BOARD"` in the Somali Basin/Red Sea to deter pirates, charterers encoding `"FOR ORDERS"` or UN/LOCODE port pairs (`"SGSIN>NLRTM"`), fishermen chatting in code, or crews writing protest messages.
  * **2. Spoofed Track-Art and Geopolitical Trolling:** Drawing giant shapes, text, or fake naval flotillas on public AIS aggregators (e.g., * Ever Given* pre-grounding Red Sea track pattern, Point Reyes / Black Sea spoofed warship tracks).
  * **3. DIY Low-Cost Asset Tracking:** Yachtsmen strapping AIS-MOB beacons to dinghies to prevent tender theft in anchorages; oceanographers repurposing Class B transponders on low-cost surface drifters and wave buoys.
  * **4. Amateur Radio VHF Tropospheric Ducting Monitors ("AIS DXing"):** Ham radio operators using coastal AIS receivers to map real-time VHF over-the-horizon propagation ducts across oceans for 2-meter ($144\text{ MHz}$) DX contests.
  * **5. Passive Bistatic Radar (PBR):** Academic and defense experiments using continuous coastal AIS Base Station / ship transmissions at $162\text{ MHz}$ as illuminators of opportunity to detect non-cooperative (dark) targets via reflected Doppler/range bistatic echoes.

#### Chapter 20: AIS 2.0 (VDES): What Is It, Is It Real, and How Does It Work?
* *Scope:* Deep technical evaluation of the VHF Data Exchange System (VDES) — "AIS 2.0."
* **20.1 Is AIS 2.0 (VDES) Real?**
  * Yes: Standardized in **ITU-R M.2092-1**, **IALA Guideline G1117 / G1139**, and adopted by the **IMO Maritime Safety Committee (MSC)** into **SOLAS Chapter V** (amendments adopted in 2024/2026 entering into force **January 1, 2028**, allowing VDES to fulfill or supplement SOLAS AIS carriage requirements).
* **20.2 VDES Frequency Plan and 4-Component Architecture:**
  * **1. Legacy AIS (AIS 1 & AIS 2):** $2 \times 25\text{ kHz}$ ($161.975 / 162.025\text{ MHz}$, $9.6\text{ kbps}$ GMSK) preserved at highest priority for ship-to-ship collision avoidance.
  * **2. ASM (Application Specific Messages):** $2 \times 25\text{ kHz}$ (Ch 2027 at $161.950\text{ MHz}$ and Ch 2028 at $162.000\text{ MHz}$, $19.2\text{ kbps}$ $\pi/4$-QPSK) offloading binary messages from AIS 1/2.
  * **3. VDE-TER (Terrestrial Wideband Data Exchange):** Contiguous $25\text{ kHz}$, $50\text{ kHz}$, or $100\text{ kHz}$ channels (Ch 1024–1026 / 2024–2026, etc.) using $\pi/4$-QPSK, 8-PSK, and 16-QAM OFDM/single-carrier modulation delivering up to **$307.2\text{ kbps}$** (32$\times$ faster than AIS!).
  * **4. VDE-SAT (Bidirectional Satellite Data Exchange):** Dedicated uplink and downlink spectrum supporting global two-way messaging between vessels and LEO constellations (NorSat-TD, Sternula-1, AOS).
* **20.3 Built-In Security, Authentication, and S-100 Data Delivery:**
  * How VDES incorporates Public Key Infrastructure (PKI), digital signatures, encryption, and **IHO S-100 / IEC 63173-2 (SECOM)** to deliver authenticated S-102 bathymetry, S-104 tides, S-111 currents, S-124 navigational warnings, and S-421 route exchange directly to the ship's ECDIS.

---

### PART V: Navigation, Charting, VTS, Mariner Training, and At-Sea Operations

#### Chapter 21: Nautical Charts, ECDIS vs. ENC, and the IHO S-100+ Ecosystem
* *Scope:* Nautical charting fundamentals, ECDIS vs. ENC distinctions, and how AIS integrates with the new IHO S-100+ standards.
* **21.1 Nautical Charts and the Distinction Between ENC, RNC, ECS, and ECDIS:**
  * **Paper Charts & RNCs (Raster Navigational Charts):** Scanned georeferenced bitmaps (e.g., NOAA BSB/KAP format); cannot trigger automated vector depth-contour safety alarms.
  * **ENC (Electronic Navigational Chart):** The *official vector database* produced by a national Hydrographic Office (HO) conforming to **IHO S-57** (legacy) or **IHO S-101** (new S-100 generation), encrypted/signed via **IHO S-63**.
  * **ECDIS (Electronic Chart Display and Information System):** The *IMO-compliant bridge hardware and software system* certified to **IMO MSC.232(82) / MSC.530(106)** and **IEC 61174**, which legally replaces paper charts under SOLAS Chapter V when loaded with official up-to-date ENCs and connected to redundant GNSS, gyro, speed log, and AIS.
  * **ECS (Electronic Chart System):** Non-type-approved or recreational chartplotters (Garmin, Raymarine, Navionics, OpenCPN) that display charts and AIS targets but do *not* legally satisfy SOLAS paperless carriage requirements.
* **21.2 Symbology of AIS on ECDIS (IHO S-52 & IEC 62288):**
  * Sleeping AIS target (isosceles triangle oriented along heading/COG) vs. Activated target (triangle with COG/SOG vector, heading line, and ROT turn indicator flag) vs. Dangerous target (flashing red bold triangle breaching CPA/TCPA limits) vs. Selected target (dashed square box) vs. Lost target (crossed line) vs. AIS AtoN / SART diamonds and circles.
* **21.3 How AIS Works with the New IHO S-100+ Standards of Charting:**
  * Architecture of **IHO S-100** (Universal Hydrographic Data Model, aligned with ISO 19100 series) and the IMO S-100 ECDIS transition roadmap (2026–2029).
  * **Direct Interplay Between AIS/VDES and S-100 Product Specifications:**
    * **S-101 (ENC):** Enhanced portrayal of AIS targets alongside high-density vector features.
    * **S-102 (Bathymetric Surface) + S-104 (Water Level / Tides) + S-111 (Surface Currents):** Combining real-time tidal/current broadcasts (historically sent via AIS Msg 8 Met/Hydro, transitioning to S-104/S-111 over VDES) with own-ship and target-ship **AIS static draught (Msg 5)** to compute dynamic **Under-Keel Clearance (UKC)** and dynamic "Go / No-Go" safety contours on S-100 ECDIS!
    * **S-124 (Navigational Warnings):** Superseding legacy AIS Area Notice (Msg 8 DAC 1 FI 22) and NAVTEX with structured GML/S-100 polygons displayed natively on ECDIS.
    * **S-212 (VTS Digital Information Service) & S-421 (Route Plan Exchange):** VTS centers and ships exchanging intended trajectories and traffic clearances over VDES/AIS to detect route conflicts minutes before a rudder order is given.

#### Chapter 22: Vessel Traffic Services (VTS), Demonstration Programs, and Government Agency Software
* *Scope:* How VTS uses AIS, what AIS demonstration programs have existed, and what software the US Coast Guard and other government agencies use.
* **22.1 How Vessel Traffic Services (VTS) Use AIS:**
  * Regulatory framework: **IMO Resolution A.1158(32)** (*Guidelines for Vessel Traffic Services*), **IALA Recommendation V-119 / V-128**, and **IALA Guideline G1082** (*An Overview of AIS*).
  * **Multi-Sensor Target Fusion (Radar + AIS):**
    * Why Radar and AIS are complementary: Radar measures independent physical range and bearing to *any* reflective surface (including uncooperative/dark vessels and wooden boats) but suffers from sea clutter, rain clutter, radar shadows behind islands/bridges, and target swapping when two ships pass close; AIS provides positive MMSI/Name/Dimensions/Draught/ROT identity, sees around bends and behind islands via VHF diffraction, and immediately telegraphs rudder turns via Gyro ROT!
    * **Kalman Filter Track-to-Track Association:** Gating radar polar measurements $(r, \theta)$ with AIS geodetic reports $(\phi, \lambda, v, \psi)$, detecting discrepancies (e.g., an AIS target with no radar return = potential spoof or virtual target; a radar target with no AIS = dark vessel or small craft).
  * **Active VTS Base Station Control via AIS:** Broadcasting DGPS corrections (Msg 17), Met/Hydro (Msg 8), Virtual/Synthetic AtoNs (Msg 21) to mark sudden hazards/wrecks, safety messages (Msg 12/14), interrogating silent ships (Msg 15), reserving FATDMA slots (Msg 20), and adjusting reporting rates (Msg 16/23).
* **22.2 Major Historical and Modern AIS Demonstration Programs:**
  * 1990s Panama Canal, Dover Strait, and Swedish/Finnish Baltic SOTDMA demonstrations.
  * 1998 USCG **PAWSS New Orleans / Lower Mississippi** VTS demonstration.
  * **St. Lawrence Seaway AIS Project** (2002–2003 — first mandatory inland/seaway commercial deployment with locks and water-level binary messages).
  * **NOAA / USCG PORTS® AIS Environmental Broadcast Demonstration** (Tampa Bay & Columbia River).
  * **Stellwagen Bank National Marine Sanctuary Right Whale AIS Project** (2007–2012 — leading to Whale Alert).
  * **European MONALISA / STM (Sea Traffic Management) Validation Projects** (2010–2019 — testing route exchange via AIS ASM across ratusan vessels).
  * **Arctic & VDES Demonstration Programs:** Norwegian **AISSat / NorSat-TD** program, **Sternula-1**, and Baltic **R-Mode / TB-VDES** testbeds.
* **22.3 What Software Does the US Coast Guard and Other Government Agencies Use for AIS?**
  * **United States Coast Guard (USCG):**
    * **NAIS (Nationwide Automatic Identification System):** The core USCG shore collection, mediation, and transmission network across US coastal, Great Lakes, and inland waters (built with Northrop Grumman / GateHouse / Shine Micro components).
    * **Command21 / WatchKeeper & CG-COP (Common Operational Picture):** Sector Command Center situational awareness and VTS consoles (using Kongsberg Norcontrol / Transas / Esri stacks).
    * **SeaVision:** Web-based global maritime situational awareness platform developed by the **U.S. Department of Transportation Volpe National Transportation Systems Center** for the US Navy and USCG, shared with international partner nations.
    * **SAROPS (Search and Rescue Optimal Planning System):** Monte Carlo particle-filter drift modeling software integrated with AIS to reconstruct last-known positions and identify nearby Good Samaritan AMVER/AIS vessels.
    * **AVIS (Authoritative Vessel Identification Service) & MISLE (Marine Information for Safety and Law Enforcement):** Correlating AIS tracks with port state control inspections, vessel certificates, and law enforcement histories.
    * **Minotaur:** Multi-agency (USCG, US Navy, CBP) airborne mission system fusing radar, EO/IR, and AIS on HC-130J, MH-60T, and P-3/P-8 aircraft.
  * **NOAA (National Oceanic and Atmospheric Administration):**
    * **ERMA® (Environmental Response Management Application):** Web-GIS incident response tool (famous in Deepwater Horizon) ingesting real-time USCG AIS via `libais`.
    * **MarineCadastre.gov (NOAA Office for Coastal Management & BOEM):** Processing and distributing curated annual US coastal AIS archives and vessel transit counts.
    * **Whale Alert / CetSound:** Right-whale acoustic and speed-restriction enforcement pipelines.
  * **US Department of Defense / US Navy / Intelligence Community:**
    * **MSSIS (Maritime Safety and Security Information System):** Volpe-operated global government-to-government raw NMEA AIS sharing network (>70 participating countries).
    * **GCCS-M (Global Command and Control System – Maritime)** & **MTB (Maritime Tactical Broadcast)**.
    * **NGA / ONI (Office of Naval Intelligence) SeaLink & Odyssey / Maven** multi-INT fusion platforms.
  * **International Government Agencies:**
    * **EMSA (European Maritime Safety Agency):** **SafeSeaNet (SSN)**, **Integrated Maritime Services (IMS)**, and **CleanSeaNet** (fusing Sentinel-1 SAR oil spill/vessel detection with AIS).
    * **United Kingdom:** UK Maritime and Coastguard Agency (MCA) & Joint Maritime Security Centre (JMSC).
    * **Canada:** Canadian Coast Guard **INNAV** (Information System on Marine Navigation) and Maisan.
    * **Australia & New Zealand:** AMSA **CTS (Craft Tracking System)** and **Starboard Maritime Intelligence** (originally developed by Dragonfly Data Science / NZ government, now used by NZ, Australia, EMSA, and Pacific Island nations).
    * **UNODC / Global:** **Skylight** (AI2 / Vulcan maritime intelligence platform provided free to government enforcement agencies worldwide).

#### Chapter 23: Mariner Training, At-Sea Operations, and AIS-Assisted Accidents
* *Scope:* How mariners are trained to use AIS, how training varies, which at-sea operations benefit most from AIS, and the anatomy of AIS-assisted incidents/accidents.
* **23.1 How Are Mariners Trained to Use AIS and How Does That Training Vary?**
  * **International Standards for Commercial Mariners (STCW & IMO Model Courses):**
    * **STCW Code Table A-II/1 & A-II/2:** Mandatory competencies for Officers in Charge of a Navigational Watch (OOW) and Masters.
    * **IMO Model Course 1.34 (*Automatic Identification Systems*):** Dedicated curriculum covering AIS principles, SOTDMA limitations, message types, MKD operation, entering accurate static/voyage data, and critical warnings against over-reliance.
    * **IMO Model Course 1.27 (*Operational Use of ECDIS*) & 1.07 (*Radar Navigation and ARPA*):** Full-mission bridge simulator training in target correlation, sensor failure recognition, and Bridge Resource Management (BRM).
  * **How Training Varies Dramatically Across Maritime Sectors:**
    * *Unlimited Tonnage Deep-Sea Officers:* Formal 4-year maritime academy + STCW simulator certification + company ECDIS type-specific familiarization; high theoretical knowledge, though watch fatigue and complacency remain risks.
    * *Inland & Coastal Towing (Tugs/Towboats):* Practical apprenticeship and **USCG Towing Officer Assessment Record (TOAR)**; heavy operational reliance on AIS around river bends where radar is blocked by trees/levees.
    * *Commercial Fishing Captains:* Frequently exempt from STCW unlimited bridge courses; learn AIS pragmatically on wheelhouse chartplotters (TimeZero / Furuno / Olex), often focusing on gear tracking and avoiding merchant shipping lanes.
    * *Recreational Boaters & Yachtsmen:* **Zero mandatory AIS training** in most jurisdictions; optional short modules from RYA, US Sailing, or US Power Squadrons. Many recreational Class B users do not understand CPA/TCPA vector delays, COG vs. Heading in cross-currents, or how to configure their own hull dimensions/MMSI.
    * *VTS Operators:* Rigorous certification under **IALA Model Courses V-103/1 through V-103/4** on traffic management, radar+AIS discrepancy diagnosis, and allied communication.
* **23.2 What Types of At-Sea Operations Is AIS Especially Helpful For?**
  * **Search and Rescue (SAR):** Instantaneous visibility of all nearby merchant ships, SAR aircraft (Msg 9), and survival craft/MOB beacons (AIS-SART/MOB) on a unified display.
  * **Inland River & Winding Fjord Navigation:** "Seeing around corners" where terrain blocks X-band radar line-of-sight but $162\text{ MHz}$ VHF diffracts over riverbanks.
  * **Tug, Tow, and Escort Operations:** Monitoring composite tow dimensions, barge articulation, and escort tug relative geometry.
  * **Pilot Boarding & Harbor Approaches:** Pilots plugging laptops/iPads into the ship's **AIS Pilot Plug** (or Wi-Fi Dongle) running portable pilot units (PPUs like QPS Qastor, Navicom HarbourPilot, SEAiq Pilot) to monitor centimeter-level docking and passing clearances in narrow channels.
  * **Offshore Wind Farms, Dredging, and Cable/Pipe Laying:** Managing safety guard vessels, Crew Transfer Vessels (CTVs) making 50+ turbine touch-and-go landings per day, and dynamic exclusion zones around restricted-maneuverability (RAM) cable-layers.
  * **Icebreaking Convoys:** Maintaining precise following distances in zero-visibility blizzard/sea-smoke conditions behind an icebreaker.
* **23.3 AIS-Assisted Incidents and Accidents:**
  * **From "Radar-Assisted Collisions" (1956 *Andrea Doria* / *Stockholm*) to "AIS-Assisted Collisions":**
    * **1. VHF "Negotiation by Name" Violating COLREGs:** Before AIS, ships rarely knew the name of a distant radar target and followed strict geometric COLREGs rules. With AIS displaying vessel names, watch officers frequently call the other ship on VHF Ch 16/13 to negotiate ad-hoc port-to-port or starboard-to-starboard passings—leading to language misunderstandings, delayed maneuvers, and collisions (documented repeatedly in UK MAIB and US NTSB casualty reports, e.g., *Rickmers Dubai* / *Walcon Wizard*, *Corvus J* / *Baltic Ace*).
    * **2. Trusting AIS Vectors Over Radar ARPA & Visual Bearings:** Using AIS COG/SOG vectors for collision avoidance when the target ship's GPS antenna offset is misconfigured, its gyro heading is frozen, or its Class B reporting interval is 30–180 seconds stale!
    * **3. Alarm Fatigue and Muted Guard Zones:** Disabling ECDIS/AIS CPA alarms in congested waters or fishing-buoy fields, resulting in watchstanders missing an actual closing vessel.

---

### PART VI: Software Ecosystem — Decoders, Encoders, and Trajectory Analytics

#### Chapter 24: Deep Dive into Open-Source AIS Decoding and Encoding Software and Its History
* *Scope:* Comprehensive technical and historical analysis of open-source AIS parsers, including `noaadata`, `bitvector-modern`, `libais`, `gpsd`, `aisparser`, `ais-area-notice`, `pyais`, and Rust-based AIS parsers.
* **24.1 The Early Era (2004–2009): `noaadata`, `BitVector`, `aisparser`, and `gpsd`:**
  * **`noaadata` (Kurt Schwehr, CCOM/UNH, ~2005–2009):** One of the earliest open-source pure-Python libraries for decoding and encoding AIS messages, encoding water-level/environmental binary messages for NOAA/USCG PORTS®, and generating KML/PostGIS outputs.
  * **`BitVector` and `bitvector-modern`:** How `noaadata` relied on Avinash Kak's pure-Python `BitVector` module (and its modernized packaging **`bitvector-modern`**) to slice arbitrary bit-widths across 6-bit NMEA ASCII armor payloads—providing great pedagogical clarity and rapid prototyping for binary messages, but suffering from Python object-allocation overhead (~100–500 messages/sec) when faced with national-scale USCG archives.
  * **`aisparser` (Brian C. Lane, 2006–2008):** Compact, portable ANSI C library (with Python/Perl bindings) that pioneered clean C struct unpacking of ITU-R M.1371 messages 1–24 for embedded Linux and chartplotter projects.
  * **`gpsd` (Eric S. Raymond, Gary E. Miller, et al.):** Integration of full AIS AIVDM/AIVDO binary and JSON decoding directly into the Unix `gpsd` daemon (`driver_ais.c`), and the creation of **`AIVDM.txt`** (*"AIVDM/AIVDO protocol decoding"* by Eric S. Raymond, with heavy contributions from Kurt Schwehr, Brian C. Lane, and others)—which became the single most influential open documentation specification of the ITU-R M.1371 bit layouts on the internet!
* **24.2 The High-Performance C++ Era (2010–Present): `libais` and `ais-area-notice`:**
  * **The 2010 *Deepwater Horizon* Catalyst:** In April 2010, the *Deepwater Horizon* blowout in the Gulf of Mexico required real-time and historical ingestion of millions of USCG NAIS messages into **NOAA ERMA**. Pure-Python `noaadata`/`BitVector` was orders of magnitude too slow.
  * **`libais` (Kurt Schwehr, started 2010 at UNH / NOAA / Google):**
    * Architecture: High-performance C++11/14/17 bitset/bit-extraction engine (`ais.h`, `ais.cpp`, `ais1_2_3.cpp` ... `ais27.cpp`, plus dozens of DAC/FI binary sub-messages in `ais8_1_22.cpp`, `ais8_1_31.cpp`, `ais8_366_*.cpp`) with CPython C-extension bindings (`ais.stream`).
    * Capable of decoding **hundreds of thousands to millions of messages per second per core**, powering NOAA ERMA, MarineCadastre pipelines, SkyTruth, and **Global Fishing Watch**'s petabyte-scale cloud ingestion.
  * **`ais-area-notice` (Kurt Schwehr):** Reference implementation, encoder/decoder, GeoJSON/KML converter, and test suite for IMO SN.1/Circ.289 (DAC 1 FI 22) and USCG (DAC 366 FI 22) Area Notice dynamic zone broadcasts (used in Whale Alert and right-whale conservation).
* **24.3 Modern Python and SDR Decoders (`pyais`, `AIS-catcher`, `rtl-ais`, `gr-ais`):**
  * **`pyais` (Leon Morten Richter):** Modern type-annotated Python decoder/encoder supporting streaming NMEA, TAG blocks, TCP/UDP sockets, and all 27 message types.
  * **`AIS-catcher` (Jasper Vries):** State-of-the-art C++ SDR demodulator + NMEA/JSON decoder supporting RTL-SDR, Airspy, SDRplay, HackRF, and SpyServer.
* **24.4 The Rust AIS Parser Ecosystem:**
  * Why Rust is ideal for AIS parsing: zero-cost abstractions, memory safety (eliminating C/C++ buffer overruns on malformed NMEA fragments or bit-lengths), `no_std` embedded compatibility for microcontrollers/CubeSats, and WebAssembly (WASM) compilation for browser-based GIS (`deck.gl`) and cloud UDFs.
  * **Key Rust Crates:**
    * **`nmea-parser` ( Timo Saarinen):** Comprehensive Rust crate parsing both GNSS NMEA sentences and AIS `VDM`/`VDO` messages 1–27 using `nom` combinators and `bitvec`.
    * **`ais` crate:** Low-level zero-copy bit-level parser for AIVDM frames in Rust.
    * **Rust bindings & Polars/Arrow integrations:** Writing custom Rust PyO3/Arrow batch decoders that parse raw `!AIVDM` log files directly into **Apache Arrow / GeoArrow** record batches at multi-GB/s throughput.
* **24.5 Side-by-Side Architecture, Coverage, and Performance Benchmark:**
  * Comparative matrix of `noaadata`, `aisparser`, `gpsd`, `libais`, `pyais`, and Rust `nmea-parser`/`ais` across message coverage (Msgs 1–27, DAC/FI binary messages), multi-sentence fragment reassembly, memory safety, and throughput (msgs/sec).

#### Chapter 25: Software for Processing and Visualizing Decoded AIS Messages (Open Source and Proprietary)
* *Scope:* End-to-end software ecosystem for ingesting, cleaning, analyzing, and visualizing decoded AIS data in 2D, 3D, and 4D.
* **25.1 Open-Source Data Science & Spatiotemporal Trajectory Stack:**
  * **`pandas` & `geopandas`:** Vectorized tabular filtering, timestamp normalization, MMSI grouping, kinematic velocity/acceleration differencing, and spatial joins (`sjoin`) with port polygons and EEZ boundaries.
  * **`MovingPandas` (Anita Graser, started Dec 2018):** Built on `geopandas` and `shapely`; provides native `Trajectory` and `TrajectoryCollection` objects for AIS analysis:
    * Trajectory splitting (`ObservationGapSplitter`, `StopSplitter`, `SpeedSplitter`),
    * Trajectory generalization/compression (`DouglasPeuckerGeneralizer`, `TopDownTimeRatioGeneralizer`),
    * Stop/anchorage detection (`TrajectoryStopDetector`),
    * Outlier cleaning (`OutlierCleaner`), and
    * Flow map aggregation (`TrajectoryAggregator`).
  * **Columnar & Database Engines (`DuckDB`, `PostGIS` / `MobilityDB`, `Apache Sedona`, `BigQuery`):**
    * **`DuckDB` (with `spatial` & `h3` extensions):** Out-of-core SQL analytics directly over hundreds of gigabytes of **GeoParquet** AIS archives on a single laptop.
    * **`MobilityDB` (on PostgreSQL/PostGIS):** Temporal-spatial types (`tgeompoint`, `tfloat`) enabling native SQL queries like `nearestApproachDistance(traj1, traj2)` and `atTime(traj, period)`.
    * **`Apache Sedona` / `Dask` / `GeoArrow`:** Distributed cluster processing for global multi-year archives.
  * **Open-Source 2D/Web Visualization:** **QGIS** (Temporal Controller), **`kepler.gl`**, **`deck.gl`** (`TripsLayer`), **OpenCPN**, and **Signal K**.
* **25.2 3D/4D Spatiotemporal Visualization, Casualty Reconstruction, and Scientific Rendering with Blender (`bpy`, `BlenderGIS`, and Geometry Nodes):**
  * **Historical Lineage (`schwehr/gis-history` & CCOM/UNH):**
    * **Blender** (`1994` initial release; `2002` released as open source under the GPL—the exact year the SOLAS AIS carriage mandate took effect).
    * Pioneering work at UNH's Center for Coastal and Ocean Mapping (**CCOM/JHC**, Kurt Schwehr et al., 2005–2012) combining **Blender's Python API (`bpy`)** with `noaadata` / `libais` to animate 3D ship trajectories over high-resolution multibeam bathymetry, visualize right-whale vocalizations and ship-strike hazards in Stellwagen Bank, and export 3D vessel models for Google Earth/Ocean.
  * **Coordinate Reference System (CRS) Engineering & Avoiding `float32` Jitter in Blender:**
    * Why importing raw UTM coordinates ($E \sim 500,000\text{ m}, N \sim 4,700,000\text{ m}$) or ECEF coordinates directly into Blender's single-precision `float32` scene graph causes severe vertex and animation quantization jitter ($\sim 0.25\text{–}0.5\text{ m}$ stepping).
    * Establishing a local tangent plane (**ENU**) origin $(\lambda_0, \phi_0, z_0)$ via `pyproj` or **`BlenderGIS`** so all vessel keyframes $(x - x_0, y - y_0, z - z_0)$ retain millimeter precision near $(0, 0, 0)$.
  * **Parametric Hull Rigging from AIS Message 5 / 24 Antenna Offsets:**
    * Using Message 5 / 24 Part B dimensions (`to_bow`, `to_stern`, `to_port`, `to_starboard`, and `draught`) to scale a 3D vessel mesh ($L_{\text{OA}} = d_{\text{bow}} + d_{\text{stern}}$, $B = d_{\text{port}} + d_{\text{starboard}}$) and **shift the mesh pivot origin to the exact GNSS antenna reference point** on the ship's superstructure!
    * Why this matters for collision/allision forensics: when a $400\text{ m}$ container ship turns with its GNSS antenna near the stern, the bow sweeps laterally by $>100\text{ m}$ even if the GNSS coordinate barely moves.
  * **Animating True Heading vs. Course Over Ground (COG), ROT, and Dynamic UKC:**
    * Keyframing yaw from **True Heading** (`True Heading` in Msg 1/2/3 or VDR gyro) while translating along the **COG/SOG** spline curve to visually expose **crabbing / leeway angles** in strong cross-currents or winds (critical in *Ever Given* Suez grounding and *MV Dali* bridge allision reconstructions).
    * Integrating **IHO S-102** bathymetric meshes and time-varying **IHO S-104 / NOAA PORTS®** tidal surfaces with AIS `draught` to animate **3D Under-Keel Clearance (UKC)** and hull-bottom contact.
  * **Bridge Blind-Sector Raycasting, COLREGs Lighting, and Volumetric RF/Acoustic Fields:**
    * Placing a Blender camera on the ship's bridge wing/conning position to render exact **line-of-sight viewsheds**, container-stack blind zones, fog attenuation, and night-time **COLREGs navigation light sector arcs** ($112.5^\circ$ port/starboard sidelights, $225^\circ$ masthead lights, $135^\circ$ sternlight) synchronized with VDR bridge audio.
    * Using **Blender Geometry Nodes** and Cycles/EEVEE volumetric shaders to render 3D VHF two-ray multipath propagation lobes, island radar shadows, and 3D underwater radiated noise (URN) acoustic spheres beneath moving vessels.
* **25.3 Proprietary & Enterprise AIS Processing Software:**
  * **GateHouse Maritime (Denmark):**
    * Deep dive into GateHouse's industry-standard maritime software stack used by national maritime authorities (Danish Maritime Authority, USCG NAIS components, UK, Australia, Canada):
    * **GateHouse AIS Network Management & Base Station Controller:** Real-time mediation, deduplication, TAG-block enrichment, and remote configuration/health monitoring of hundreds of shore base stations and repeaters in compliance with **IALA Recommendation A-124**.
    * **IWRAP Mk II (IALA Waterway Risk Assessment Program):** Developed with GateHouse and IALA to ingest historical AIS traffic distributions and compute quantitative ship-ship collision and grounding probabilities along waterways.
    * **GateHouse Maritime Data Foundation / OceanIO:** Enterprise maritime data aggregation and anomaly detection APIs.
  * **VTS, Simulation, and Defense Enterprise Suites:**
    * **Kongsberg Maritime / Kongsberg Norcontrol:** **C-Scope VTS**, **K-Sim Navigation** bridge simulators, and **TerraLens** geospatial SDK.
    * **Tidalis (formerly Saab Maritime Traffic Management / HITT Traffic):** **Vessel Traffic Management Information System (VTMIS)** and port management software deployed in over 300 ports and coastal authorities worldwide.
    * **Wärtsilä Voyage (formerly Transas):** **Navi-Harbour VTS**, **Navi-Sailor 4000 ECDIS**, and Fleet Operations Solutions.
    * **Esri:** **ArcGIS Pro**, **ArcGIS Maritime**, **ArcGIS GeoEvent Server**, and **ArcGIS Velocity** for real-time streaming AIS geofencing and space-time cubes.
  * **Commercial Maritime Intelligence & Risk Platforms:**
    * **Kpler (acquired MarineTraffic & FleetMon)**, **Vortexa**, **Windward**, **Pole Star Global (PurpleTRAC)**, **Spire Maritime**, **S&P Global (Sea-web / AISLive)**, and **Starboard Maritime Intelligence**.

#### Chapter 26: Spatial Statistics and Trajectory Modeling with AIS Data
* *Scope:* How spatial statistics must be formulated for AIS data given RF propagation constraints, SOTDMA dynamic reporting intervals, VDL packet loss, and uneven/moving receivers.
* **26.1 Why Naive Point-Counting ("Ping Heatmaps") Is Statistically Invalid for AIS:**
  * **1. Dynamic Reporting Rate Bias:** Under ITU-R M.1371, a Class A ship turning at $>23\text{ kts}$ transmits **every 2 seconds** (1,800 pings/hour), whereas an anchored ship transmits **every 3 minutes** (20 pings/hour) and a Class B CSTDMA sailboat at $<2\text{ kts}$ transmits every 3 minutes. Raw ping counts over-weight fast maneuvering vessels by $90\times$!
  * **2. Spatially Non-Uniform RF Reception Probability $P_{\text{det}}(\mathbf{x}, t)$:** Terrain shadowing behind headlands, distance roll-off from uneven coastal receiver locations, and anomalous tropospheric ducting create massive artificial density gradients.
  * **3. VDL Congestion & Satellite Footprint Saturation:** In high-density ports or within a satellite footprint covering the East China Sea or Gulf of Mexico, co-channel packet collisions drop $50\%\text{–}90\%$ of bursts, making dense traffic appear *sparser* in raw satellite ping counts unless corrected!
  * **4. Moving Receiver Observation Bias:** When AIS is collected by LEO satellites (orbital inclination latitude bias + revisit gaps) or moving patrol ships/ASVs/aircraft, the spatio-temporal sampling window $W(\mathbf{x}, t)$ moves through space-time.
* **26.2 Rigorous Mathematical Estimators for AIS Spatial Statistics:**
  * **Continuous-Time Trajectory Integration (Vessel-Hours & Distance Steamed per Grid Cell):**
    * Reconstructing continuous piecewise-linear or kinematic spline trajectories $\hat{\mathbf{x}}_i(t)$ between validated pings and integrating residence time $T_{i,c} = \int \mathbb{I}(\hat{\mathbf{x}}_i(t) \in \text{Cell } c) \, dt$ or track length $L_{i,c} = \int_{\hat{\mathbf{x}}_i(t) \in c} \|\dot{\hat{\mathbf{x}}}_i(t)\| \, dt$.
  * **Horvitz-Thompson Inverse-Probability-of-Detection Weighting:**
    * Estimating the spatio-temporal detection probability field $\hat{p}(\mathbf{x}, t \mid \text{Class}, h_{\text{ant}})$ using an RF propagation + VDL collision model (or empirical inter-arrival gap distribution $\Delta t_k / \Delta t_{\text{nominal}}$):
      $$\hat{\Lambda}(c) = \sum_{i} \sum_{k \in c} \frac{\Delta t_{\text{nominal}}(v_{i,k}, \omega_{i,k})}{\hat{p}(\mathbf{x}_{i,k}, t_{i,k})}$$
  * **State-Space Filtering & Bridging Data Gaps:** Continuous-time correlated random walk (CTCRW), Interacting Multiple Model (IMM) Kalman smoothing, and Brownian bridge movement models (BBMM) to quantify positional uncertainty ellipses across reception gaps.
  * **Spatial Indexing & Aggregation:** Why equal-area projections or **Uber H3** hexagonal grids (with explicit spherical area normalization) must be used instead of equirectangular Lat/Lon degree bins (`EPSG:4326`) or Web Mercator (`EPSG:3857`).

---

### PART VII: Security, Spoofing, RF Forensics, Intelligence, and Alternative Tracking

#### Chapter 27: Cybersecurity of AIS: Malicious Data, DoS Attacks, and Hardware/Software Failure Modes
* *Scope:* Security implications of AIS, sending malicious data to ships and shore systems, documented CVEs/vulnerabilities, DoS/corruption vectors, and hardware/software failure modes.
* **27.1 Foundational Security Flaws of the AIS Protocol:**
  * Complete absence of cryptographic sender authentication, message integrity codes (CRC-16 detects random noise, not malicious tampering), timestamps in position reports (only UTC seconds `0–59`), or encryption.
  * Review of **Balduzzi, Pasta, and Wilhoit (2014)**, *"A Security Evaluation of AIS"* (Trend Micro / ACSAC / BlackHat) separating **RF/Protocol-layer threats** from **Software/Web-Aggregator implementation threats**.
* **27.2 Can Malicious Data Be Sent Over AIS to Cause DoS or Corruption in Receiving Hardware and Software? (Known Issues & Attack Vectors):**
  * **1. Parser Memory Corruption & Buffer Overflows (Documented CVEs & Bugs):**
    * Bit-length mismatch attacks: Sending an `!AIVDM` payload announcing `Message ID = 1` (expected 168 bits) or `Message ID = 5` (expected 424 bits) but packing only 40 bits or 1,000 bits into the NMEA sentences—triggering out-of-bounds array reads/writes in naive C/C++ decoders that do not validate bit-vector bounds before unpacking fields.
    * **Multi-Sentence Fragment Reassembly Exhaustion:** Flooding a receiver with first fragments (`!AIVDM,9,1,7,A,...`) that never send the final fragment (`9,9`), exhausting fixed-size fragment reassembly buffers in embedded bridge hardware or leaking heap memory in shore servers.
    * **Documented Software Vulnerabilities:** E.g., **CVE-2025-66217** (heap buffer overflow via integer underflow in `AIS-catcher` prior to v0.64), historical `gpsd` / `Wireshark` / chartplotter NMEA parser fuzzing bugs, and SQL injection / Stored XSS in web-based AIS trackers when a malicious vessel broadcasts `<script>...` or SQL payloads encoded inside 6-bit ASCII `Vessel Name` or `Destination` fields.
  * **2. Bridge Display & Target-Table Saturation DoS:**
    * Certified Class A MKDs, older radar ARPA overlays, and recreational chartplotters have finite target table capacities (typically 200 to 1,000 active MMSIs). A low-cost SDR (e.g., HackRF) transmitting 500 spoofed MMSIs in a 30-second burst overflows the receiver's target table, causing the bridge display to **drop real nearby vessels**, freeze its GUI rendering thread, or trigger continuous proximity alarms!
  * **3. Protocol-Level MAC & Control Message Attacks (ITU-R M.1371 Abuse):**
    * **Channel Switching Hijack (Message 22):** Broadcasting a forged Base Station Message 22 command instructing all Class A/B transponders within a geographic bounding box to switch their VHF transceivers from $161.975 / 162.025\text{ MHz}$ to an unused simplex frequency—instantly blinding every ship in a strait!
    * **Silent Mode / Quiet Time Command (Message 23) & Assigned Rate Throttling (Message 16):** Forcing target transponders to stop transmitting for up to 15 minutes at a time or slowing their reporting intervals.
    * **FATDMA Slot Reservation Starvation (Message 20):** Reserving all 2,250 time slots across AIS1 and AIS2 so legitimate SOTDMA/CSTDMA transceivers cannot find open slots.
    * **DGNSS Poisoning (Message 17):** Broadcasting malicious pseudorange corrections over Message 17 to shift the computed DGNSS position of nearby vessels.
* **27.3 Non-Malicious Failure Modes of AIS Hardware and Software:**
  * **Hardware Failures:** High VSWR / corroded PL-259 coax connectors (reducing a 12.5 W Class A unit to $<50\text{ mW}$ radiated power while the bridge officer thinks AIS is working normally!), blown PIN-diode TR switches in antenna splitters, degraded TCXO crystal oscillators drifting off-frequency by $>3\text{ kHz}$, and dead internal GPS backup batteries.
  * **Sensor & Software Failures:** **GPS Week Number Rollover (WNRO)** bugs (10-bit week counter rolling over every 1,024 weeks: Aug 1999, April 6, 2019, Nov 2038), stuck gyrocompass repeaters broadcasting a fixed heading while the ship turns, negative/wrapped SOG/COG values in buggy firmware, and unconfigured static fields (`"@@@@@@@"`, `0` dimensions).

#### Chapter 28: AIS Spoofing Techniques, Deep RF Fingerprinting (SEI), and Counter-Spoofing
* *Scope:* Taxonomy of AIS spoofing techniques and how deep RF-level quirks of SDRs and hardware transceivers can be used to identify manufacturers or specific individual units.
* **28.1 Taxonomy of AIS Spoofing Techniques:**
  * **1. Software / Aggregator API Injection ("Cyber Spoofing"):** Feeding fabricated `!AIVDM` sentences over UDP/TCP into terrestrial community aggregator feeds (MarineTraffic, AISHub) without ever transmitting a single microwatt of RF energy! (Affects web trackers, not shipboard bridges).
  * **2. Over-the-Air RF Spoofing:** Using an SDR (HackRF, USRP, PlutoSDR) or modified VHF radio to broadcast false AIS bursts over $161.975 / 162.025\text{ MHz}$.
  * **3. Identity Laundering & Dual-Transponder Spoofing ("Shadow Fleet" Tactics):**
    * *MMSI/IMO Hijacking:* Two ships simultaneously broadcasting the same MMSI/IMO number in different oceans ("dual-broadcasting") so a sanctioned tanker picking up crude in Venezuela or Iran appears to be idling safely in Malaysia.
    * *Anchor-Loop / Shore-Relay Spoofing:* Leaving a second transponder (or SDR replay box) on a tugboat, barge, or shore apartment broadcasting a stationary or looping track while the real tanker sails dark to conduct a ship-to-ship (STS) transfer.
  * **4. GNSS-Induced AIS Spoofing:** Broadcasting false GPS/GLONASS L1 signals at a ship's GNSS antenna so the ship's own legitimate, unmodified Class A AIS transponder broadcasts false coordinates (e.g., placing warships at onshore airports, or spinning ships in $3\text{ NM}$ circles in Shanghai, Point Reyes, the Black Sea, and the Eastern Med).
* **28.2 Deep Diving into the RF Level: Specific Emitter Identification (SEI) and Hardware Fingerprinting:**
  * *Core Question:* Can quirks of particular SDR and hardware implementations be used to identify the manufacturer or even a specific individual transceiver unit? **Yes.**
  * **Physical-Layer Imperfections Extracted from High-Sample-Rate Baseband IQ Captures ($\ge 1\text{–}10\text{ MS/s}$):**
    1. **Power Amplifier Turn-On and Turn-Off Transients:** During the $833\text{ }\mu\text{s}$ (8-bit) ramp-up and ramp-down window specified by IEC 61993-2, every power amplifier circuit and ALC loop exhibits a characteristic amplitude and phase ringing envelope $A(t), \phi(t)$ dictated by its analog capacitor/inductor tolerances.
    2. **GMSK Modulation Phase Trajectory & $BT$ Filter Impulses:** Differences between analog PLL frequency modulators, DDS chips (e.g., AD9851/ADF7021), and SDR DACs (HackRF 8-bit DAC quantization spurs vs. Furuno/JRC/Saab hardware ASICs) produce measurable deviations in Gaussian filter $BT$ product, modulation index $h = 0.5 \pm \delta h$, and inter-symbol phase error.
    3. **Carrier Frequency Offset (CFO) & Crystal Clock Skew:** Comparing the carrier frequency offset $\Delta f_c$ (at $162\text{ MHz}$) against the symbol-clock bit-rate offset $\Delta R_b$ (at $9,600\text{ bps}$), which are locked to the same internal TCXO oscillator (plus thermal drift curves after key-up).
    4. **I/Q Imbalance and Local Oscillator (LO) Leakage:** Direct-conversion SDR transmitters (like HackRF and PlutoSDR) exhibit characteristic DC carrier leakage and quadrature gain/phase imbalance that are absent in traditional superheterodyne/PLL marine VHF transmitters!
  * **Machine Learning & Signal Processing Pipelines for SEI:** Hilbert-Huang transform, bispectral analysis, cyclic spectral coherence, and complex-valued Convolutional Neural Networks (CV-CNNs) classifying individual AIS transmitters from raw IQ bursts, combined with TDOA/FDOA/AoA physical localization.

#### Chapter 29: National Security, Blue Force Systems, Encryption, and Dark Ships
* *Scope:* National security aspects of AIS, Blue Force Tracking and encryption, and the global "Dark Ships" phenomenon (`https://youtu.be/2tuS1LLOcsI`).
* **29.1 National Security Aspects of AIS:**
  * **The Double-Edged Sword:** AIS gives coastal states unprecedented Maritime Domain Awareness (MDA), but simultaneously creates an Open-Source Intelligence (OSINT) vulnerability for naval, coast guard, and auxiliary logistics vessels.
  * Naval collisions and policy shifts: How the 2017 *USS Fitzgerald* and *USS John S. McCain* collisions forced the US Navy to re-evaluate running completely dark in congested commercial sea lanes, adopting dual-mode/encrypted and receive-only operational doctrines.
  * **Grey-Zone & Hybrid Warfare:** Tracking Russian and Iranian "shadow fleets," weapons smuggling across the Caspian/Black Sea, Chinese maritime militia swarms in the South China Sea, and suspected state-sponsored anchor-dragging attacks on NATO subsea cables and pipelines.
* **29.2 Blue Force Systems and Encrypted AIS (EAIS):**
  * How military and law-enforcement agencies achieve situational awareness without broadcasting cleartext locations to adversaries:
    1. **USCG / DoD Encrypted AIS (EAIS):** Wrapping position and identity payloads inside encrypted AIS Binary Messages (**Message 6 Addressed** and **Message 8 Broadcast**, using NSA Type 1 or AES-256 encryption with tactical keymat via KGV-72 / embedded crypto modules). To civilian receivers, the burst is a valid GMSK AIS frame that prevents SOTDMA slot collisions, but the payload is opaque binary ciphertext; on authorized USCG/Navy Command21/GCCS-M/ECDIS-N displays, it decrypts into a friendly "Blue Force" track!
    2. **NATO Warship AIS (W-AIS) & Tactical MMSI Rotation:** Dynamic pseudonym MMSIs (`000000000` or rotating tactical numbers) paired with secure Link 16 / OTH-Gold / MTB correlation.
* **29.3 Dark Ships, Global Fishing Watch, and Unmasking the Ocean's "Dark Zones":**
  * Case study and deep analysis of the **2025 Johnny Harris / Global Fishing Watch investigation** ([*"What's really happening in the ocean's 'dark zones'"*, `https://youtu.be/2tuS1LLOcsI`](https://youtu.be/2tuS1LLOcsI)) and **Paolo et al. (2024, *Nature*)**, *"Satellite mapping reveals extensive industrial activity at sea"*.
  * **Why Ships Go Dark:** Illegal fishing inside Marine Protected Areas (MPAs, e.g., Galápagos, Argentine Mile 201, North Korean waters), unauthorized transshipment at sea (human trafficking / forced labor abuse and catch laundering), sanctions evasion, and piracy avoidance.
  * **Distinguishing True Intentional Disabling ("Going Dark") from RF Dropouts:**
    * Modeling expected satellite and terrestrial reception probability $P(\text{rx} \mid \text{lon}, \text{lat}, t, \text{class})$ so an AIS gap in a high-VDL-congestion zone is not falsely accused of intentional tampering.
    * Fusing AIS with **Sentinel-1 SAR** (detecting metallic ship hulls through clouds and night — finding that **75% of the world's industrial fishing vessels and 25% of transport/energy vessels are not publicly tracked by AIS**!), **VIIRS** night-lights, and optical imagery.

#### Chapter 30: Other Ways to Track Ships: Mobile Phones, SS7/Diameter, VMS, VOS, LRIT, Commodity Trading, and Whale Alert
* *Scope:* Comprehensive guide to non-AIS ship tracking (including mobile phones and SS7/Diameter telecom signaling), commodity traders (Bloomberg Terminal), and Listen for Whales / Whale Alert.
* **30.1 Mobile Phones and Cellular Telecom Signaling (SS7 for 2G/3G and Diameter for 4G/5G):**
  * **How Mobile Phones Betray "Dark" Ships at Sea and in Port:**
    1. **Coastal Cell Tower Attachment (<15–35 NM from shore):** Crew and passenger phones automatically attach to coastal 2G/3G/4G/5G base stations (eNodeB/gNodeB) along straits (Gibraltar, Hormuz, Malacca, English Channel, Bosporus), generating Timing Advance (TA) range rings and Angle-of-Arrival sector logs at the mobile network operator.
    2. **Onboard Maritime Cellular Networks ("Cellular-at-Sea"):** Cruise ships, merchant vessels, and offshore rigs carry onboard GSM/LTE picocells/femtocells (operated by MCP/Telenor Maritime, Wireless Maritime Services [WMS], etc.) backhauled over VSAT or Starlink. Whenever a crew member's phone registers on the ship's picocell, the shipboard network routes roaming signaling back to the subscriber's home terrestrial carrier!
    3. **SS7 (2G/3G) and Diameter (4G/5G) Signaling Exploits:**
       * In **SS7 MAP** (Mobile Application Part, ITU-T Q.771–Q.775), an entity with access to a global signaling point can send `MAP_SEND_ROUTING_INFO_FOR_SM`, `MAP_PROVIDE_SUBSCRIBER_INFO (PSI)`, or `MAP_ANY_TIME_INTERROGATION (ATI)` using a target crew member's phone number (MSISDN) or IMSI. The visited network returns the **Mobile Switching Center (MSC) Global Title** and **Cell Global Identity (CGI)**—identifying the exact coastal cell tower or the specific shipboard maritime picocell ID!
       * In **4G LTE / 5G NSA Diameter** (RFC 6733 / 3GPP TS 29.272 `S6a`/`S6d` interfaces), equivalent exploits (`Insert-Subscriber-Data-Request [IDR]` with EPS Location Information flag, or `Location-Information-Request [LIR]`) retrieve the visited **MME (Mobility Management Entity)** and **E-UTRAN Cell Global Identifier (ECGI)** when Diameter firewalls are misconfigured.
    4. **Mobile App Ad-Tech Telemetry (RTB Location Brokers):** Weather, prayer, compass, flashlight, and gaming apps on crew smartphones read the phone's internal GPS while on deck (connected to ship Wi-Fi/Starlink) and broadcast `(lat, lon, timestamp, MAID)` to commercial real-time bidding (RTB) ad exchanges—allowing analysts to track dark warships and sanctioned tankers via crew phone GPS leaks!
    5. **Direct RF Emissions Collection:** Airborne and spaceborne SIGINT platforms detecting 800–2600 MHz cellular uplink bursts, 2.4/5 GHz Wi-Fi beacons (BSSIDs), Bluetooth, and Iridium/Thuraya/Inmarsat handset uplinks.
* **30.2 Regulated Non-AIS Maritime Tracking Systems: VMS, LRIT, and NOAA VOS / AMVER:**
  * **VMS (Vessel Monitoring System):** Closed, encrypted, tamper-resistant satellite transceivers (Inmarsat-C, Iridium, Woods Hole Group / CLS Argos) mandated for commercial fishing fleets by national agencies (NOAA Fisheries) and Regional Fisheries Management Organizations (RFMOs). Contrasting VMS (1-to-4-hour polling, confidential government database, high hardware reliability) vs. AIS (2–180 second open broadcast, easily switched off).
  * **LRIT (Long-Range Identification and Tracking):** Adopted by IMO in 2006 (**SOLAS Chapter V, Regulation 19-1**). Uses existing GMDSS Inmarsat-C / Iridium shipboard terminals to transmit point-to-point encrypted position reports **every 6 hours** (adjustable down to 15 minutes during SAR/security events) to National/Regional LRIT Data Centers coordinated by IMSO. Accessible *only* to the Flag State, a Port State the vessel is bound for, or a Coastal State within $1,000\text{ NM}$.
  * **NOAA VOS (Volunteer Observing Ship) Program & AMVER:**
    * **NOAA VOS:** Roughly 1,000+ merchant vessels voluntarily reporting marine meteorological and surface oceanographic observations (WMO FM 13 SHIP synoptic code via SEAS / TurboWin+ / SAMOS over Inmarsat/Iridium). Historically published with ship call signs in WMO GTS / ICOADS, until commercial security/piracy concerns led to generic `"SHIP"` call-sign masking—and how researchers cross-correlate VOS weather reports with AIS tracks!
    * **USCG AMVER (Automated Mutual-Assistance Vessel Rescue):** Voluntary global SAR reporting system founded in 1958.
* **30.3 Detailed Look at Commodity Traders and the Bloomberg Terminal:**
  * How AIS revolutionized global oil, LNG, coal, iron ore, and grain trading by turning physical cargo movements into real-time quantitative signals days or weeks before official customs or EIA/IEA reports.
  * **Inside the Bloomberg Terminal Shipping Suite** (referencing the University of Scranton Kania School of Management Alperin Financial Center *Bloomberg Training Manual*, [`https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf`](https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf)):
    * **`BMAP <GO>` (Bloomberg Map):** Interactive global geospatial terminal displaying live AIS vessel positions, speed vectors, port anchorage queues, pipelines, refineries, LNG terminals, and weather overlays (hurricane tracks).
    * **`SHIP <GO>`:** Master shipping and maritime analytics portal.
    * **`VSRC <GO>` (Vessel Search) & `VSTK <GO>`:** Querying vessels by MMSI, IMO, deadweight tonnage (DWT), hull class (VLCC, Suezmax, Aframax, Panamax, Capesize), and current/historical AIS draught.
    * **`FLET <GO>` (Fleet Analysis) & `AHOY <GO>`:** Tracking fleet-wide speed trends, ballast vs. laden ratios, floating storage accumulation, and port congestion.
    * **`FIXS <GO>` & `BFX <GO>`:** Correlating Baltic Exchange freight indices and charter fixtures with live AIS vessel availability.
  * **Quantitative Trading Algorithms on AIS:** Estimating cargo weight loaded/discharged via $\Delta \text{Draught} \times \text{TPC (Tonnes Per Centimeter immersion)}$, detecting offshore ship-to-ship (STS) crude transfers off Kalamata, Ceuta, Lomé, and Malaysia, and pitfalls of relying on manually entered Message 5 draught!
* **30.4 Listen for Whales / Whale Alert: Dynamic Marine Mammal Conservation:**
  * History and architecture of **Whale Alert** (presented to the US Congress in 2012; see `schwehr/gis-history` and Wiley et al. / Schwehr et al.):
  * **The Sensor-to-Bridge Loop & 3D Acoustic/Vessel Visualization:**
    1. Passive acoustic monitoring (PAM) buoys (WHOI / Cornell Lab of Ornithology DMONs) moored in the Boston Harbor Traffic Separation Scheme / Stellwagen Bank detect North Atlantic Right Whale (*Eubalaena glacialis*) up-calls in real time, combined with NOAA/NEAq aerial and visual sightings.
    2. Detections update **Seasonal Management Areas (SMAs)** and **Dynamic Management Areas (DMAs)** / **Right Whale Slow Zones**.
    3. Status and polygon coordinates are broadcast over **USCG AIS Base Stations using AIS Area Notice (Message 8 DAC 366 FI 22 / IMO DAC 1 FI 22)** (`ais-area-notice`) directly onto ships' ECDIS displays and pushed to the **Whale Alert** iPad/iPhone app (**Listen for Whales** program).
    4. Simultaneously, shore AIS networks track every transiting ship's SOG through the management polygons to grade fleet compliance (NOAA/Oceana speed report cards) and issue NOAA Office of Law Enforcement civil penalties for violating the **10-knot mandatory speed rule** (50 CFR § 224.105).
    5. **3D Visualization in Blender:** Animating 3D whale foraging dives, DMON acoustic detection spheres, Stellwagen Bank bathymetry, and commercial vessel hulls/propeller strike zones using **Blender + Python (`bpy`)** to communicate underwater co-occurrence and acoustic masking to policymakers and mariners.

---

### PART VIII: Exhaustive Message-by-Message & Application-Specific Message (ASM) Deep Dives (`book/part8-message-deep-dives/`)

Every chapter in Part VIII subjects each ITU-R M.1371-5 message type (`Messages 1–27`) and every known international and regional Application-Specific Message (`ASM`) subtype (`DAC/FI`) to a rigorous six-part forensic engineering profile:
1. **How the Message Works:** Exact bit-level layout (0-based `libais` and 1-based ITU-R M.1371-5 indexing), signed/unsigned encoding, scaling factors, sentinel values, TDMA access scheme (`SOTDMA`, `ITDMA`, `RATDMA`, `FATDMA`, `CSTDMA`), slot length (`1–5 slots`), VHF channel behavior, NMEA 0183 fragmentation/fill bits, NMEA 2000 PGN mapping, and state-machine triggers.
2. **Known Protocol & Implementation Issues:** Protocol design flaws, bit-length and byte-alignment quirks, quantization/resolution limits, sentinel ambiguities, integer-overflow/truncation bugs, firmware implementation defects, and multi-slot VDL collision vulnerabilities.
3. **Relationships to Other AIS Messages:** How the message interacts with, triggers, acknowledges, supersedes, or requires joining against other AIS messages (e.g., static-to-dynamic MMSI joins, request/response state machines, Base Station control couplings, legacy-to-modern ASM migrations).
4. **Known Uses and Abuses:** Legitimate operational, scientific, and regulatory uses contrasted against real-world adversarial abuses, spoofing patterns, shadow-fleet manipulation, fishing-buoy squatting, informal text chat, and parser/bridge Denial-of-Service (DoS) exploits.
5. **Where and When the Message Is Used:** Geographic distribution (open ocean vs. coastal VTS vs. inland waterways vs. specific canals/sanctuaries), temporal broadcast cadence, and empirical percentage share of global terrestrial and satellite VDL traffic.
6. **Software Support & Non-Support Matrix:** Detailed support audit across open-source decoders (`libais` C++ classes, `gpsd` `driver_ais.c` / `AIVDM.txt`, `pyais`, `aisparser`, `noaadata`, `ais-area-notice`, `AIS-catcher`, Rust `nmea-parser` & `ais` crates, Wireshark), navigation apps (OpenCPN, Signal K, TimeZero, QPS Qastor, SEAiq), enterprise/government platforms (GateHouse, Kongsberg C-Scope, USCG NAIS/Command21/SeaVision, NOAA ERMA, EMSA SafeSeaNet), and shipboard ECDIS/chartplotters.

#### Chapter 31: Deep Dive into Messages 1, 2, and 3: Class A Position Reports (Scheduled, Assigned, and Interrogated)
* *Scope:* Exhaustive forensic analysis of ITU-R M.1371-5 **Message 1** (*Position Report — Scheduled*), **Message 2** (*Position Report — Assigned Scheduled*), and **Message 3** (*Position Report — Special / Interrogated*).
* **31.1 How Messages 1, 2, and 3 Work:** 168-bit layout, 15 Navigation Status codes (`0–15`), nonlinear Rate-of-Turn (`ROT`) compression ($\pm 4.733\sqrt{|\omega|}$) and TI/no-TI sentinels (`-128`, `±127`), `SOG`, `Position Accuracy`, 28-bit `Longitude` & 27-bit `Latitude` (`1/10,000 min` resolution $\approx 0.185\text{ m}$), `COG`, `True Heading`, `Time Stamp` (`0–59` UTC sec vs. `60–63` fallback status), `Maneuver Indicator` (Inland "Blue Sign"), `RAIM`, and the 19-bit **SOTDMA (Msgs 1 & 2) vs. ITDMA (Msg 3) Communication State** sub-message cycle (`Slot Time-Out 0–7`).
* **31.2 Issues & Pathologies:** `0.185 m` coordinate step jitter at berth, `SOG = 102.2 kts` saturation ceiling, stale manually entered `Navigation Status` (ships sailing at `15 kts` while reporting `At Anchor [1]` or `Moored [5]`), disconnected gyrocompass (`HDG = 511`) and ROT (`-128`), 6-bit UTC second wrap-around ambiguity without TAG blocks, and the **Message 2 rarity paradox** (why Assigned Mode often uses Message 1 or 3 instead of Message 2).
* **31.3 Message Relationships:** Mandatory MMSI join with **Message 5** for static dimensions/identity; triggering of **Message 2** by **Message 16** (*Assigned Mode*) or **Message 23** (*Group Assignment*); triggering of **Message 3** by **Message 15** (*Interrogation*) and during autonomous SOTDMA reporting-rate transitions (`ITDMA` pre-announcement); and **AIS-SART (`970xxyyyy`)** pairing of Message 1 (`Nav Status = 14`) with **Message 14**.
* **31.4 Uses, Abuses, Where/When Used, and Software Support:** Accounts for ~65–75% of global AIS VDL traffic; uncertified fishing net-buoys squatting on Message 1, shadow-fleet dual-transponder spoofing, C4ADS circular GNSS spoofing signatures, and universal support across `libais` (`Ais1_2_3`), `gpsd`, `pyais`, `aisparser`, Rust crates, NMEA 2000 PGN `129038`, and all ECDIS/VTS platforms (plus integer-sign and ROT decoding bugs in naive parsers).

#### Chapter 32: Deep Dive into Messages 4, 10, and 11: Base Station Reports and UTC/Date Synchronization
* *Scope:* Exhaustive forensic analysis of **Message 4** (*Base Station Report*), **Message 10** (*UTC and Date Inquiry*), and **Message 11** (*UTC and Date Response*).
* **32.1 How Messages 4, 10, and 11 Work:** Bit-level anatomy of the 168-bit **Message 4** and **Message 11** frames (UTC Year `1–9999`, Month `1–12`, Day `1–31`, Hour `0–23`, Minute `0–59`, Second `0–59`, Position Accuracy, 28-bit Lon, 27-bit Lat, 4-bit EPFD Type `0–15` [typically `7` = Surveyed], Transmission Control for Long-Range Broadcast Message [`Bit 148`], RAIM, and 19-bit SOTDMA Communication State) and the 72-bit **Message 10** addressed inquiry (`Destination MMSI` at `bits[40:70]`).
* **32.2 Issues & Pathologies:** Coastal Base Stations with misconfigured surveyed coordinates (`0°, 0°` Null Island or inland offsets), GPS Week Number Rollover (WNRO) bugs corrupting UTC Year/Month/Day on legacy shore stations, and VDL congestion when dozens of ships simultaneously transmit Message 10 inquiries to a single Base Station, triggering a flood of ITDMA Message 11 responses.
* **32.3 Message Relationships:** Message 4 provides **Sync State 2 (Base Station Synchronization)** for mobile stations that lose GNSS, advertises the Base Station MMSI (`00MIDxxxx`) needed to interpret relative slot offsets in **Message 20 (FATDMA)**, and controls **Message 27 suppression (`Bit 148`)**; Message 10 (`72 bits`) directly triggers Message 11 (`168 bits`).
* **32.4 Uses, Abuses, Where/When Used, and Software Support:** Message 4 transmitted every `10 s` (6 times/minute alternating AIS 1 and AIS 2) by every coastal VTS/NAIS tower; opportunistic VHF tropospheric ducting measurement using fixed Message 4 links; rogue Message 4 spoofing to hijack harbor TDMA frame synchronization or suppress satellite Message 27; and software support (`libais` `Ais4_11` & `Ais10`, `gpsd`, `pyais`, NMEA 2000 PGNs `129793` & `129804`, and why many consumer chartplotters hide Message 4 icons or misrender Message 11 as a stationary ship!).

#### Chapter 33: Deep Dive into Messages 5 and 24: Class A and Class B Static and Voyage-Related Data
* *Scope:* Exhaustive forensic analysis of **Message 5** (*Static and Voyage Related Data*, 424 bits) and **Message 24** (*Class B Static Data Report*, Part A [160 bits] & Part B [168 bits]).
* **33.1 How Messages 5 and 24 Work:**
  * **Message 5 (`424 bits`, 2 slots, 2 `!AIVDM` sentences):** AIS Version (`0–3`), 30-bit `IMO Number`, 42-bit `Call Sign` (7 chars), 120-bit `Vessel Name` (20 chars), 8-bit `Ship and Cargo Type` (`0–99`), 30-bit **Hull Dimensions / GNSS Antenna Offset** (`A` to bow [9b], `B` to stern [9b], `C` to port [6b], `D` to starboard [6b]), 4-bit `EPFD`, 20-bit `ETA` (`Month`, `Day`, `Hour`, `Minute`), 8-bit `Maximum Present Static Draught` (`0.1 m` steps, `0–25.5 m`), 120-bit `Destination` (20 chars), `DTE`, and Spare.
  * **Message 24 (`160/168 bits`, 1 slot each):** Why Class B "CS" cannot reserve 2 contiguous slots and therefore splits static data into **Part A (`Part Number = 0`, `Vessel Name`)** and **Part B (`Part Number = 1`, `Ship Type`, 42-bit `Vendor ID` + `Unit Model Code` + `Serial Number`, `Call Sign`, and the overloaded `Dimension / Mothership MMSI` field `bits[132:162]`)**!
* **33.2 Issues & Pathologies:** Unauthenticated multi-sentence NMEA fragment reassembly (`seq_id` collisions and out-of-order UDP delivery), **CVE-2025-66217 (`libais` truncated Message 5 heap buffer overflow when `<420 bits`)**, rampant human entry errors in `Destination` and `Draught`, `Draught = 25.5 m` ceiling for ultra-deep platforms, `Dimension` truncation (`A, B = 511 m`, `C, D = 63 m`), and the **Message 24 Part B ITU-R M.1371-3 vs. M.1371-4/5 Vendor ID bit-width change** (7-char vs. 3-char Vendor ID + Model/Serial).
* **33.3 Message Relationships:** Stateful MMSI caching required to enrich **Messages 1, 2, 3, 18, and 27**; **Message 19** as the legacy 312-bit combination of Message 18 + Message 24; triggered on demand by **Message 15** interrogation; and how `98MIDxxxx` auxiliary craft use Message 24 Part B `bits[132:162]` to link to their parent ship's MMSI.
* **33.4 Uses, Abuses, Where/When Used, and Software Support:** Broadcast every 6 minutes (or on parameter change); commodity traders (`Bloomberg VSRC/FLET`, Kpler, Vortexa) extracting `Draught` and `Destination`; **3D Blender hull rigging** from `(A, B, C, D)`; anti-piracy/Red Sea signaling (`"ARMED GUARDS ONBOARD"`, `"CHINESE CREW ALL"`), identity laundering (spoofing MMSI/Name while forgetting to change the hull `IMO Number`), and parser support across `libais` (`Ais5`, `Ais24`), `gpsd`, `pyais`, Rust crates, and NMEA 2000 PGNs `129794`, `129809`, and `129810`.

#### Chapter 34: Deep Dive into Messages 9, 18, 19, and 27: SAR Aircraft, Class B Position Reports, and Long-Range Satellite AIS
* *Scope:* Exhaustive forensic analysis of **Message 9** (*Standard SAR Aircraft Position Report*), **Message 18** (*Standard Class B Equipment Position Report*), **Message 19** (*Extended Class B Equipment Position Report*), and **Message 27** (*Position Report for Long-Range Applications*).
* **34.1 How Messages 9, 18, 19, and 27 Work:**
  * **Message 9 (`168 bits`):** 12-bit `Altitude` (`0–4,094 m`, `4095 = N/A`), whole-knot `SOG` (`0–1,022 kts`), `Assigned Mode`, `DTE`, and `Altitude Sensor` (`0 = GNSS`, `1 = Barometric`) + SOTDMA/ITDMA flag.
  * **Message 18 (`168 bits`):** Replaces `Navigation Status` and `ROT` with 8 reserved bits; adds `CS Unit` flag (`0 = Class B SOTDMA [5W]`, `1 = Class B CSTDMA [2W]`), `Display`, `DSC`, `Band`, `Msg 22` capability flags, and a constant `ITDMA` (`0x349B0` = `1100000000000000110`) communication state when `CS = 1`.
  * **Message 19 (`312 bits`, 2 slots):** Combines Message 18 kinematics with `Vessel Name`, `Ship Type`, and `Dimensions` in a single 2-slot frame.
  * **Message 27 (`96 bits`, $9.6\text{ ms}$ on Ch 75/76):** Compresses `Lon` (18 bits, `1/600 deg` = `0.1 arcmin` $\approx 185\text{ m}$), `Lat` (17 bits, `0.1 arcmin`), `SOG` (6 bits, `0–62 kts`), `COG` (9 bits, `0–359°`), and `GNSS Position Status` (`0 = current GNSS`, `1 = not current`) with zero Communication State bits!
* **34.2 Issues & Pathologies:** Message 9 altitude ceiling (`4,094 m` = `13,431 ft`, overflowing for high-altitude `P-8A` / `MQ-4C Triton` patrol aircraft); Message 18 missing `ROT` and `Nav Status` plus `30 s` / `3 min` stale vector lag; why **Message 19 is deprecated in practice** (2-slot unreserved CSTDMA bursts suffer catastrophic collision rates); and **Message 27's `GNSS Position Status` polarity inversion** (`0` = current vs. `1` = stale, opposite of `Position Accuracy`!) plus `185 m` quantization stair-stepping if mixed naively with Message 1/18 tracks.
* **34.3 Message Relationships:** Message 18 + Message 24 (Part A & B) replaces Message 19; Message 27 is automatically suppressed within coastal range when **Message 4 (`Bit 148 = 0`)** is received; and **Message 22 / 23** manage Class B channels and reporting intervals.
* **34.4 Uses, Abuses, Where/When Used, and Software Support:** USCG/EMSA SAR helicopters (`111MIDxxx`) on Message 9; yachts, workboats, and artisanal fishing boats on Message 18; uncertified Chinese fishing buoys abusing Message 18/19; open-ocean satellite tracking via Message 27; and support across `libais` (`Ais9`, `Ais18`, `Ais19`, `Ais27`), `gpsd`, `pyais`, `AIS-catcher`, and NMEA 2000 PGNs `129798`, `129039`, and `129040`.

#### Chapter 35: Deep Dive into Safety, Interrogation, AtoN, and Data Link Control Messages (Messages 12, 13, 14, 15, 16, 20, 21, 22, and 23)
* *Scope:* Exhaustive forensic analysis of **Messages 12, 13, and 14** (*Safety-Related Text & Ack*), **Message 15** (*Interrogation*), **Message 16** (*Assigned Mode Command*), **Message 20** (*Data Link Management / FATDMA*), **Message 21** (*Aids-to-Navigation Report*), **Message 22** (*Channel Management*), and **Message 23** (*Group Assignment Command*).
* **35.1 Safety-Related Text & Acknowledgment (Messages 12, 13, 14):**
  * Bit layouts of **Message 12** (*Addressed Safety Text*, up to 156 6-bit chars / 1,008 bits with `Sequence Number` & `Retransmit Flag`), **Message 13** (*Safety Acknowledge*, acknowledging up to 4 sender MMSIs + sequence numbers), and **Message 14** (*Broadcast Safety Text*, up to 161 6-bit chars).
  * Uses and abuses: **`AIS-SART` (`"SART ACTIVE"`)**, VTS warnings, mariner bridge-to-bridge text chat, Balduzzi et al. fake distress / Coast Guard eviction phishing, and parser crashes on non-6-bit-aligned text lengths or XSS injection in web dashboards.
* **35.2 Aids-to-Navigation Report (Message 21, `272–360 bits`):**
  * Bit layout: 5-bit `AtoN Type` (`0–31`: Cardinal/Lateral marks, racons, lighthouses, offshore wind turbines), 120-bit `Name`, `Position Accuracy`, `Lon/Lat`, `Dimensions`, `EPFD`, `UTC Second`, **`Off-Position Indicator`**, 8-bit regional `AtoN Status` (lantern/racon health), `RAIM`, **`Virtual AtoN Flag` (`0` = Real/Synthetic, `1` = Virtual)**, `Assigned Mode`, and variable-length `Name Extension` (`0–84 bits`).
  * Issues, uses, and abuses: Distinguishing Real (`Virtual=0`, `99MID1xxx`), Synthetic Monitored, Synthetic Predicted, and Virtual (`Virtual=1`, `99MID6xxx`) AtoNs; rapid VTS Virtual AtoN wreck marking (*Tricolor*); uncertified fishing buoys spoofing Message 21 diamonds on ECDIS; and parser failures on variable-length `Name Extension` padding.
* **35.3 Interrogation and VDL Data Link Control (Messages 15, 16, 20, 22, 23):**
  * **Message 15 (`88–160 bits`):** Shore/ship interrogation requesting 1 or 2 MMSIs to transmit specific message types (commonly Msg 5 or Msg 24) at specified slot offsets.
  * **Message 16 (`96 or 144 bits`):** Base Station command forcing 1 or 2 target MMSIs into an exact transmission interval or slot offset.
  * **Message 20 (`72–160 bits`):** FATDMA slot reservation broadcast by Base Stations (up to 4 reservation blocks of `Offset`, `Number of Slots`, `Time-Out`, `Increment`); critical role in protecting shore VDL bandwidth and catastrophic impact of **FATDMA slot-starvation DoS**.
  * **Message 22 (`168 bits`):** Regional frequency (`Ch A/B` 12-bit ITU channel numbers), `TX/RX Mode`, `Power`, and geographic bounding-box (`NE/SW corners`) or addressed MMSI handover (**St. Lawrence Seaway / USCG regional channel zones** vs. the **Balduzzi et al. frequency-hopping / TX-disable DoS exploit**).
  * **Message 23 (`160 bits`):** Geographic + Ship-Type/Station-Type Group Assignment Command, including the **`Quiet Time` (`1–15 minutes`)** command that silences every transponder in a bounding box!

#### Chapter 36: Deep Dive into Binary Message Envelopes and DGNSS Broadcasts (Messages 6, 7, 8, 17, 25, and 26)
* *Scope:* Exhaustive forensic analysis of all six binary transport and correction message envelopes: **Message 6** (*Addressed Binary Message*), **Message 7** (*Binary Acknowledge*), **Message 8** (*Broadcast Binary Message*), **Message 17** (*DGNSS Broadcast Binary Message*), **Message 25** (*Single-Slot Binary Message*), and **Message 26** (*Multiple-Slot Binary Message with Communications State*).
* **36.1 Addressed and Broadcast Binary Envelopes (Messages 6, 7, and 8):**
  * Bit layouts of **Message 6** (`88-bit` header + up to `920 bits` payload = `1,008 bits` max; `Sequence Number`, `Destination MMSI`, `Retransmit Flag`, `DAC [10b]`, `FI [6b]`), **Message 7** (`72–168 bits` acknowledging up to 4 Message 6 senders), and **Message 8** (`56-bit` header + up to `952 bits` payload = `1,008 bits` max).
  * Why 3-to-5-slot (`576–1,008 bit`) Message 6/8 broadcasts suffer severe packet loss in congested ports and essentially 0% intact reception from LEO satellites without terrestrial Base Station FATDMA reservation (**Message 20**).
* **36.2 DGNSS Broadcast Binary Message (Message 17, `80–816 bits`):**
  * Bit layout: `Lon` (18b, `0.1 min`), `Lat` (17b, `0.1 min`), and encapsulated **RTCM SC-104 Type 1, Type 9, or Type 3/16** differential pseudorange ($PRC$) and range-rate ($RRC$) words (24-bit words stripped of parity).
  * How coastal Base Stations broadcast sub-meter differential GPS corrections directly over the VHF AIS data link to ships lacking a $300\text{ kHz}$ MF radiobeacon receiver—and how a **spoofed Message 17 with extreme $PRC$ values** can walk the internal GNSS position of every vessel in a harbor off course!
* **36.3 Compact and Scheduled Binary Envelopes (Messages 25 and 26):**
  * Bit layouts of **Message 25** (`1 slot`, `≤168 bits`) and **Message 26** (`1–5 slots`, `≤1,004 bits` with trailing 20-bit SOTDMA/ITDMA flag + Communication State).
  * The **`Addressed` (`Bit 38`) and `Structured` (`Bit 39`) 4-mode header matrix** (shifting the start of the binary payload between bit `40`, `56`, `70`, or `86`), why **Message 25 unstructured mode (`Structured=0`)** is a favorite covert/proprietary telemetry channel, and why naive decoders frequently misalign the trailing 20-bit Communication State in **Message 26**!

#### Chapter 37: Deep Dive into International ASM Subtypes (`DAC = 1`), Part 1: System Management & IMO SN/Circ.236 Legacy Messages (`FI = 0–21`)
* *Scope:* Exhaustive subtype-by-subtype analysis of the International (`DAC = 1`) system-management FIs and the first generation of IMO binary messages (**IMO SN/Circ.236**, 2004, and **SN.1/Circ.289**, 2010) across `FI = 0, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, and 21`.
* **37.1 System Management & Capability Discovery Subtypes (`DAC=1`, `FI = 0, 2, 3, 4, 5`):**
  * `FI = 0`: *Text telegram using 6-bit ASCII* (ITU-R M.1371 Annex 5),
  * `FI = 2`: *Interrogation for a specific FM (Functional Message)*,
  * `FI = 3`: *Capability interrogation* (requesting a station's supported `FI` bitmap),
  * `FI = 4`: *Capability interrogation reply* (128-bit bitmap announcing which `FI = 0..63` TX/RX functions a ship supports),
  * `FI = 5`: *Application acknowledgment to an addressed binary message*.
* **37.2 Legacy Met/Hydro (`DAC=1, FI=11`) and Why IMO Deprecated It:**
  * Complete 352-bit layout of **IMO SN/Circ.236 `DAC=1, FI=11`** (*Meteorological and Hydrological Data*).
  * **Why `FI=11` Was Flawed and Replaced by `FI=31`:** Inverted `(Lat, Lon)` field ordering (`Lat` before `Lon`, opposite of every other AIS message!), `0.001 min` coordinate mismatch, coarse **`0.1 m` water-level (tide) resolution** (inadequate for deep-draft UKC!), and wind/pressure sentinel bugs—plus why **`DAC=1, FI=11` still represents the majority of global Met/Hydro AIS traffic today** due to unpatched legacy coastal weather stations!
* **37.3 Dangerous Cargo, Fairway Closed, Tidal Window,Persons on Board, and Berthing/VTS Subtypes (`DAC=1, FI = 12–21`):**
  * `FI = 12` (*Dangerous Cargo Indication*, withdrawn due to cleartext piracy/terrorism risk) & `FI = 13` (*Fairway Closed*),
  * `FI = 14` (*Tidal Window* — up to 3 tidal current prediction windows) & `FI = 15` (*Extended Ship Static and Voyage Related Data — Air Draught / Bridge Clearance Height* in `0.1 m`),
  * `FI = 16` (*Number of Persons on Board*, 13-bit count `0–8,191` used by ferries/cruise ships during SAR),
  * `FI = 17` (*VTS-Generated/Synthetic Targets* — up to 4 shore-radar-tracked non-AIS targets broadcast onto ship ECDIS!),
  * `FI = 18` (*Clearance Time to Enter Port*), `FI = 19` (*Marine Traffic Signal*), `FI = 20` (*Berthing Data*), and `FI = 21` (*Weather Observation Report from Ship* — WMO shipboard synoptic observation vs. NOAA VOS).
* **37.4 Software Support Audit (`libais` `Ais8_1_0`..`Ais8_1_21`, `Ais6_1_*`, `gpsd`, `pyais`, ECDIS):** Exact class-by-class support matrix and bit-padding workarounds.

#### Chapter 38: Deep Dive into International ASM Subtypes (`DAC = 1`), Part 2: IMO SN.1/Circ.289 & Circ.290 Operational Messages (`FI = 22–32`)
* *Scope:* Exhaustive subtype-by-subtype analysis of the modern IMO operational binary suite (**IMO SN.1/Circ.289** & **SN.1/Circ.290**, 2010) across `DAC = 1, FI = 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, and 32`.
* **38.1 Area Notice (`DAC=1, FI=22`) and Text Description (`DAC=1, FI=29`):**
  * Deep forensic dive into **Message 6/8 `DAC=1, FI=22`** (`ais-area-notice`): Message Linkage ID, Notice Description (`0–127`), UTC Month/Day/Hour/Minute, Duration (`18 bits`), and `1–9` chaining 87-bit Sub-Areas (`Shape 0` Circle/Point, `Shape 1` Rectangle, `Shape 2` Sector, `Shape 3` Polyline, `Shape 4` Polygon, `Shape 5` Associated Text), plus how **`DAC=1, FI=29`** attaches extended free-text descriptions via the shared `Message Linkage ID`.
  * Known issues (polyline vertex drift across scale factors, 5-slot VDL limits, ECDIS non-rendering) and abuses (spoofed "Area To Be Avoided" / naval exercise zones).
* **38.2 Route Information (`DAC=1, FI=27` & `FI=28`) and Text (`DAC=1, FI=30`):**
  * Complete bit layouts of **`DAC=1, FI=27`** (*Broadcast Route Information*) and **`DAC=1, FI=28`** (*Addressed Route Information*): Route Type (`1` Mandatory, `2` Recommended, `3` Alternative, `4` Recommended route through ice, `5` Ship route plan), Sender Classification, Start Time, Duration, and up to `16` (`Lon, Lat`) 55-bit waypoints + Turning Radius.
  * Operational deployment in icebreaker convoys (Finnish/Swedish Baltic icebreakers broadcasting safe ice channels to merchant followers), MONALISA/STM trials, and replacement by **IHO S-421** over VDES.
* **38.3 Modern Meteorological and Hydrographic Data (`DAC=1, FI=31`) and Environmental Sensor Reports (`DAC=1, FI=26`):**
  * Compare the 360-bit fixed **`DAC=1, FI=31`** (*Meteorological and Hydrographic Data*, fixing `FI=11`'s coordinate order, adding `1/1,000 min` accuracy and **`0.01 m` water-level resolution** plus WMO station ID bit) against the modular **`DAC=1, FI=26`** (*Environmental* — chaining 1 to 8 self-describing **112-bit Sensor Report records**: `Report Type 0` Site Location, `1` Station ID, `2` Wind, `3` Water Level, `4` 2D Current, `5` 3D Current, `6` Horizontal Current, `7` Sea State, `8` Salinity, `9` Weather, `10` Air Gap / Air Draft!).
* **38.4 Extended Ship Static, Dangerous Cargo, VTS Targets, and Tidal Windows (`DAC=1, FI = 23, 24, 25, 32`):**
  * Complete bit layouts and operational profiles of `FI = 23` (*Area Notice — Addressed*), `FI = 24` (*Extended Ship Static & Voyage Related Data* — adding **`Ice Class`** and **`Shaft Horsepower`** to Air Draught), `FI = 25` (*Dangerous Cargo Indication* — IMDG/IGC/IBC/MARPOL Annex I cargo classes & bunker mass), and `FI = 32` (*Tidal Window* — corrected `Lon/Lat` order).
* **38.5 Software Support Audit (`libais` `Ais8_1_22`..`Ais8_1_32`, `ais-area-notice`, `noaadata`, `gpsd`, `pyais`, OpenCPN, ECDIS):** Detailed verification matrix and runnable Python decoder/encoder test cases.

#### Chapter 39: Deep Dive into Regional ASM Subtypes, Part 1: European Inland AIS (`DAC = 200`) and UK/Ireland GLA (`DAC = 232 / 235`)
* *Scope:* Exhaustive forensic analysis of all European Inland AIS (`DAC = 200`, governed by CCNR / UNECE / CESNI *Inland AIS Test Standard*) and UK/Ireland General Lighthouse Authorities (`DAC = 232 / 235`) binary subtypes.
* **39.1 European Inland AIS Vessel & Voyage Subtypes (`DAC=200`, `FI = 10, 21, 22, 55`):**
  * **`DAC=200, FI=10` (*Inland Ship Static and Voyage Related Data*, 168 bits, Msg 8):**
    * **8-character European Vessel Identification Number (ENI / ERI ID)** (`48 bits`),
    * **High-precision Convoy Length (`0.1 m` steps, `0–800.0 m`) and Beam (`0.1 m` steps, `0–100.0 m`)** (essential for $185\text{ m} \times 11.45\text{ m}$ Rhine locks where standard Message 5 `1 m` integers are too coarse!),
    * **4-digit ERI Ship/Convoy Type Code (`8000–8490`)** distinguishing motor tankers, pushed barge trains, and side-by-side formations,
    * **Hazardous Cargo "Blue Cones / Lights" (`0, 1, 2, 3 cones`, ADN regulations)**,
    * **High-precision Draught (`0.01 m` [centimeter] resolution!)**, **`Loaded / Unloaded` state (`1–2`)**, Speed/Course/Heading sensor quality flags.
  * **`DAC=200, FI=21` (*ETA at Lock/Bridge/Terminal*, Msg 6)** & **`DAC=200, FI=22` (*RTA — Recommended Time of Arrival at Lock/Bridge/Terminal*, Msg 6):** Automated lock-passage negotiation between Rhine/Danube barges and River Information Services (RIS) lockmasters.
  * **`DAC=200, FI=55` (*Number of Persons on Board*, Msg 6/8):** Separate counts of **`Crew` (`0–254`), `Passengers` (`0–8,190`), and `Shipboard Personnel` (`0–254`)** for river cruise ships and passenger ferries.
* **39.2 European Inland Waterway Infrastructure & Environment Subtypes (`DAC=200`, `FI = 23, 24, 40`):**
  * **`DAC=200, FI=23` (*EMMA Warning*, Msg 8):** European Multiservice Meteorological Awareness weather warnings (wind, rain, snow/ice, thunderstorm, fog, extreme temperatures, forest fire, water level) mapped to river kilometer markers.
  * **`DAC=200, FI=24` (*Water Level*, Msg 8):** Real-time river hydrometric gauge heights (`cm` reference difference vs. GlW/RNW datum) for up to 4 gauges per broadcast.
  * **`DAC=200, FI=40` (*Signal Status*, Msg 8):** Real-time optical aspect matrix of inland bridge and lock light signals so skippers see lock entry signals around river bends on **Inland ECDIS**.
* **39.3 United Kingdom & Ireland General Lighthouse Authorities (`DAC = 232 / 235, FI = 10`):**
  * Complete bit layout of **`DAC=235 (or 232), FI=10`** (*GLA Aid to Navigation Monitoring Data*, 168 bits, Msg 6/8): Analogue battery/solar/external voltages (`0.05 V` steps), internal/external light status, racon status, health/off-position/tamper/hatch-open digital input telemetry broadcast by Trinity House, Northern Lighthouse Board (NLB), and Commissioners of Irish Lights (CIL) offshore buoys and lighthouses.
* **39.4 Software Support Audit:** `libais` (`Ais8_200_10`, `Ais6_200_21`, `Ais6_200_22`, `Ais8_200_23`, `Ais8_200_24`, `Ais8_200_40`, `Ais8_200_55`, `Ais8_235_10`), `gpsd`, `pyais`, Inland ECDIS (Periskal, Tresco, Argonics), and why ocean-going SOLAS ECDIS ignores `DAC=200` unless operating in Inland mode.

#### Chapter 40: Deep Dive into Regional ASM Subtypes, Part 2: North American Seaway (`DAC = 316 / 366`), USCG / NOAA PORTS®, Encrypted AIS, and the Master Software Support Matrix
* *Scope:* Exhaustive forensic analysis of St. Lawrence Seaway (`DAC = 316` & `DAC = 366`), USCG / NOAA PORTS® / Whale Alert / Encrypted AIS (`DAC = 366`), Panama Canal (`DAC = 351`), Australia (`DAC = 503`), South Korea (`DAC = 440`), VDES ASM migration (`ITU-R M.2092-1`), and the definitive **Master Message & ASM Software Support Matrix**.
* **40.1 St. Lawrence Seaway & Great Lakes Binational Subtypes (`DAC = 316` [Canada] & `DAC = 366` [USA], `FI = 1, 2, 32, 33, 34`):**
  * Architecture of the binational St. Lawrence Seaway Management Corporation (SLSMC) / Great Lakes St. Lawrence Seaway Development Corporation (GLS) AIS system (`13 locks` between Montreal and Lake Erie):
  * **`FI = 1` (*Meteorological / Hydrological*) & `FI = 2` (*Dangerous Cargo*):** Early Seaway environmental and hazmat messages (`noaadata`).
  * **`FI = 32` (*Lockage Order*, Msg 8):** Broadcasts the scheduled queue of up to 6 vessels (`Vessel Name / MMSI`, `Direction`, `Lock ID`, `Scheduled Time`) approaching a Seaway lock.
  * **`FI = 33` (*Estimated Lock Times*, Msg 6):** Addressed message delivering specific lock arrival/tie-up times to an individual laker or ocean "salty."
  * **`FI = 34` (*Seaway Water Level & Flow Rate*, Msg 8):** Real-time water level and cubic-meter-per-second dam/weir flow rates affecting lock approach crosscurrents.
* **40.2 United States Coast Guard (USCG) & NOAA PORTS® Subtypes (`DAC = 366`, `FI = 22, 23, 56, 57`):**
  * **`DAC=366, FI=22` (Broadcast) & `FI=23` (Addressed) (*USCG Area Notice*):** Historical predecessor to IMO `DAC=1, FI=22` (`ais-area-notice`), operationalized in **Stellwagen Bank / Boston Harbor for Listen for Whales / Whale Alert** right-whale speed zones and USCG security zones; detail the subtle bit-level differences between `DAC=366, FI=22` (USCG) and `DAC=1, FI=22` (IMO SN.1/Circ.289).
  * **NOAA PORTS® (`DAC=1, FI=26 / FI=31` & RTCM Standard 12301.1):** How USCG NAIS broadcasts NOAA tide gauges, currents, winds, and **Bridge Air Gap** clearance measurements across US ports (`noaadata`).
  * **`DAC=366, FI=56` & `FI=57` (*USCG / DoD Encrypted AIS [EAIS] — Blue Force Tracking*):**
    * Deep forensic dive into how USCG cutters, law enforcement boats, and Navy vessels broadcast **encrypted position and identity reports** inside **Message 6 / Message 8 (`DAC=366, FI=56/57`)** using a **64-bit Initialization Vector (IV) + AES-256 / NSA Type 1 ciphertext** (`libais` `Ais8_366_56`).
    * Why EAIS uses an outer cleartext MMSI (often `000000000` or a rotating tactical pseudonym) so civilian transponders still respect the SOTDMA slot reservation, while authorized USCG/DoD **Command21 / SeaVision / GCCS-M** terminals decrypt the inner payload into true Blue Force tracks!
* **40.3 Other Regional ASMs (Panama Canal `DAC=351`, Australia `DAC=503`, South Korea `DAC=440`) and VDES ASM Migration:**
  * How the Panama Canal Authority (ACP), AMSA (Great Barrier Reef REEFVTS), and South Korea MOF use regional ASMs, and how **ITU-R M.2092-1 VDES ASM Channels (`2027` & `2028` at $19.2\text{ kbps}$) and IHO S-100 (`S-104`, `S-111`, `S-124`, `S-421` via SECOM)** replace legacy VHF AIS Message 6/8 binary broadcasts.
* **40.4 The Master AIS Message (1–27) and ASM (`DAC/FI`) Software Support Matrix:**
  * Comprehensive, side-by-side engineering lookup table auditing exact support (`Full Decode`, `Decode + Encode`, `Envelope Only`, `Unsupported / Quirks`) for **every Message 1–27 and every ASM `DAC/FI` subtype** across `libais`, `gpsd`, `pyais`, `aisparser`, `noaadata`, `ais-area-notice`, `AIS-catcher`, Rust (`nmea-parser` / `ais`), Wireshark, OpenCPN, Signal K, GateHouse, Kongsberg, USCG NAIS/SeaVision, NOAA ERMA, and SOLAS/Inland ECDIS.

---

### Appendices
* **Appendix A: Complete ITU-R M.1371-5 Message 1–27 Bit-Layout Reference Tables**
* **Appendix B: Maritime Identification Digits (MID) and MMSI Prefix Lookup Table**
* **Appendix C: NMEA 0183 6-Bit ASCII Armor and Checksum Reference**
* **Appendix D: International & Regional Binary Application-Specific Messages (DAC/FI) Registry**
* **Appendix E: Master Standards Matrix (ITU, IMO, IEC, IALA, IHO, RTCM, NMEA)**
* **Appendix F: Landmark Admiralty Court Cases, Statutes, and AIS Patent Index**
* **Appendix G: Recommended Low-Budget Home AIS Station Schematics, Filter Curves, and Configuration Files**
* **Appendix H: Master Bibliography and Verified Citation Index**

---

## 6. Initial Master Bibliography of Cited Sources and Primary References

1. **Global Fishing Watch / History & Dark Vessels:**
   * Cutlip, K. (2017, updated 2025). *AIS for Safety and Tracking: A Brief History*. Global Fishing Watch. [`https://globalfishingwatch.org/article/ais-brief-history/`](https://globalfishingwatch.org/article/ais-brief-history/)
   * Schwehr, K. (2024–2026). *gis-history: A list of key events in the history of Geographic Information Systems (GIS) and spatial data processing*. GitHub. [`https://github.com/schwehr/gis-history`](https://github.com/schwehr/gis-history)
   * Harris, J., & Global Fishing Watch. (2025). *What's really happening in the ocean's "dark zones"*. YouTube. [`https://youtu.be/2tuS1LLOcsI`](https://youtu.be/2tuS1LLOcsI)
   * Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., ... & Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378), 904–908. [`https://doi.org/10.1126/science.aao5646`](https://doi.org/10.1126/science.aao5646)
   * Paolo, F. S., Kroodsma, D., Raynor, J., Hochberg, T., Davis, P., Cleary, J., ... & Halpern, B. S. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625(7993), 85–91. [`https://doi.org/10.1038/s41586-023-06825-8`](https://doi.org/10.1038/s41586-023-06825-8)
2. **Primary ITU, IMO, IALA, IEC, IHO, and RTCM Standards:**
   * ITU-R. (1998–2014). *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union. [`https://www.itu.int/rec/R-REC-M.1371/`](https://www.itu.int/rec/R-REC-M.1371/)
   * ITU-R. (2022). *Recommendation ITU-R M.585-9: Assignment and use of identities in the maritime mobile service*. Geneva: ITU.
   * ITU-R. (2022). *Recommendation ITU-R M.2092-1: Technical characteristics for a VHF data exchange system in the VHF maritime mobile band (VDES)*. Geneva: ITU.
   * ITU-R. (2019). *Recommendation ITU-R M.2135-0: Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz*. Geneva: ITU.
   * ITU-R. (2013). *Report ITU-R M.2287-0: Assessment of the VHF data link loading*. Geneva: ITU.
   * IMO. (2000/2002). *International Convention for the Safety of Life at Sea (SOLAS), Chapter V, Regulation 19: Carriage requirements for shipborne navigational systems and equipment*. London: International Maritime Organization.
   * IMO. (2015). *Resolution A.1106(29): Revised guidelines for the onboard operational use of shipborne Automatic Identification Systems (AIS)*. London: IMO.
   * IMO. (2010). *SN.1/Circ.289: Guidance on the use of AIS Application-Specific Messages*. London: IMO.
   * IALA. (2016–2024). *Recommendation A-124 (AIS Shore Station and Networking Aspect)*, *Recommendation A-126 (The Use of the Automatic Identification System in Marine Aids to Navigation Services)*, and *Guideline G1082 (An Overview of AIS)*. Saint-Germain-en-Laye: IALA.
   * IHO. (2022–2025). *S-100: Universal Hydrographic Data Model (Ed. 5.x)*, *S-101 (ENC)*, *S-102 (Bathymetric Surface)*, *S-104 (Water Level Information)*, *S-111 (Surface Currents)*, *S-124 (Navigational Warnings)*. Monaco: International Hydrographic Organization.
   * IEC. *IEC 61993-2 (Class A AIS)*, *IEC 62287-1/2 (Class B AIS)*, *IEC 62320-1/2/3 (AIS Base Station, AtoN, Repeater)*, *IEC 61097-14 (AIS-SART)*, *IEC 61162-1/2/3/450 (Digital Interfaces: NMEA 0183, NMEA 2000, LWE)*, *IEC 61996-1 (VDR)*.
3. **Open-Source Software, 3D Visualization, & Trajectory Processing:**
   * Schwehr, K. (2010–present). *libais: C++/Python library for decoding maritime Automatic Identification System messages*. GitHub. [`https://github.com/schwehr/libais`](https://github.com/schwehr/libais)
   * Schwehr, K. (2006–2011). *noaadata: Python library for NOAA/USCG AIS and water level messages*. GitHub. [`https://github.com/schwehr/noaadata`](https://github.com/schwehr/noaadata)
   * Schwehr, K. *ais-area-notice: Reference implementation for IMO Circular 289 AIS Area Notice binary messages*. GitHub. [`https://github.com/schwehr/ais-area-notice`](https://github.com/schwehr/ais-area-notice)
   * Schwehr, K. / Kak, A. *bitvector-modern / BitVector: Python bit-array manipulation*.
   * Blender Online Community. (1994/2002–present). *Blender — a 3D modelling and rendering package*. Blender Foundation, Amsterdam. [`https://www.blender.org`](https://www.blender.org) (and `BlenderGIS`: [`https://github.com/domlysz/BlenderGIS`](https://github.com/domlysz/BlenderGIS)).
   * Raymond, E. S., Schwehr, K., Lane, B. C., et al. *AIVDM/AIVDO protocol decoding*. The `gpsd` Project. [`https://gpsd.gitlab.io/gpsd/AIVDM.html`](https://gpsd.gitlab.io/gpsd/AIVDM.html)
   * Lane, B. C. (2006–present). *aisparser: C library for parsing AIS messages*. GitHub. [`https://github.com/bcl/aisparser`](https://github.com/bcl/aisparser)
   * Vries, J. (2021–present). *AIS-catcher: Multi-platform SDR AIS receiver*. GitHub. [`https://github.com/jvde-github/AIS-catcher`](https://github.com/jvde-github/AIS-catcher)
   * Richter, L. M. (2020–present). *pyais: AIS message decoding and encoding in Python*. GitHub. [`https://github.com/M0r13n/pyais`](https://github.com/M0r13n/pyais)
   * Graser, A. (2019). MovingPandas: Efficient structures for movement data in Python. *GI_Forum*, 2019(1), 54–68. [`https://doi.org/10.1553/giscience2019_01_s54`](https://doi.org/10.1553/giscience2019_01_s54)
4. **Security, Spoofing, RF Fingerprinting, and Patents:**
   * Balduzzi, M., Pasta, A., & Wilhoit, K. (2014). A security evaluation of AIS automated identification system. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC)* (pp. 436–445). ACM. [`https://doi.org/10.1145/2664243.2664257`](https://doi.org/10.1145/2664243.2664257)
   * C4ADS. (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC: Center for Advanced Defense Studies.
   * Lans, H. (1996). *Position indicating system* (U.S. Patent No. 5,506,587; Ex Parte Reexamination Certificate C1 issued March 30, 2010 cancelling all claims). U.S. Patent and Trademark Office.
   * Hoye, G. K., Eriksen, T., Meland, B. J., & Narheim, B. T. (2008). Space-based AIS for global maritime traffic monitoring. *Acta Astronautica*, 62(2-3), 240–245. [`https://doi.org/10.1016/j.actaastro.2007.07.001`](https://doi.org/10.1016/j.actaastro.2007.07.001)
5. **Commodity Trading, Conservation, and Admiralty Law:**
   * University of Scranton, Alperin Financial Center. *Bloomberg Training Manual* (`BMAP`, `SHIP`, `VSRC`, `VSTK`, `FLET`). [`https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf`](https://www.scranton.edu/academics/ksom/alperin/Bloomberg%20Training%20Manual.pdf)
   * Wiley, D. N., Thompson, M., Pace, R. M., & Levenson, J. (2011). Modeling speed restrictions to mitigate lethal collisions between ships and whales in the Stellwagen Bank National Marine Sanctuary, USA. *Biological Conservation*, 144(9), 2377–2381.
   * *Nautical Challenge Ltd v Evergreen Marine (UK) Ltd (The "Alexandra 1" and "Ever Smart")* [2021] UKSC 6.
   * IMO Model Course 1.34. (2019). *Automatic Identification Systems (AIS)*. London: International Maritime Organization.
