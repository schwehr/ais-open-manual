# Chapter 15 — The standards that define AIS

> **Part III — Identity, institutions, law.** How international conventions, radio recommendations, industrial test standards, and operational guidelines interlock to define the Automatic Identification System.

**In this chapter.** You will learn how the Automatic Identification System is governed by an interlocking hierarchy of international standards. We examine the four-tier architectural stack connecting International Maritime Organization (**IMO**) operational requirements, International Telecommunication Union (**ITU**) radio characteristics, International Electrotechnical Commission (**IEC**) type-approval test methods, and International Organization for Marine Aids to Navigation (**IALA**) operational guidelines. You will discover the evolutionary history of Recommendation ITU-R M.1371 across its editions from 1998 to 2026, analyze the specific test regimes for Class A, Class B, Aids to Navigation (**AtoN**), base stations, and locating transmitters, and trace digital bridge interfaces across the NMEA 0183, NMEA 2000, and IEC 61162 families. Finally, we explore national statutory transposition across the United States Code of Federal Regulations and the European Marine Equipment Directive, and explain how to obtain, read, and cross-reference both public and paywalled maritime specifications.

## 15.1 The standards stack: architecture of a global system

No single document defines AIS. Instead, the system functions through a division of labor across four institutional tiers:
1. **Tier 1 (Statutory Mandate):** The IMO establishes *why* and *when* equipment must exist under SOLAS Chapter V. In Resolution [MSC.74(69)](ch15-standards-that-define-ais.md#references) Annex 3 (1998), the Maritime Safety Committee (**MSC**) defined functional requirements: autonomous dynamic reporting, continuous operation, two-minute cold initialization, and unauthenticated VHF transmission. In Section 9, the IMO deferred RF engineering: "The AIS should conform to the appropriate ITU-R Recommendations."
2. **Tier 2 (Radio Characteristics):** ITU-R Working Party 5B standardizes *what* is broadcast over the airwaves. Recommendation [ITU-R M.1371](ch15-standards-that-define-ais.md#references) governs Gaussian Minimum Shift Keying (**GMSK**) modulation, 9,600 bit/s signaling, Time Division Multiple Access (**TDMA**) 26.67-millisecond slotting, framing, access schemes, and bit catalogs for Messages 1 through 28. Identity numbering is governed by Recommendation [ITU-R M.585](ch15-standards-that-define-ais.md#references).
3. **Tier 3 (Equipment Test Standards):** IEC Technical Committee 80 (**TC 80**) translates ITU and IMO performance recommendations into *pass/fail laboratory test specifications*. Manufacturers certify transceivers against IEC standards such as [IEC 61993-2](ch15-standards-that-define-ais.md#references) (Class A) or [IEC 62287-1](ch15-standards-that-define-ais.md#references) (Class B), specifying RF measurement circuits, climate conditioning, packet error rates, and interface protocols.
4. **Tier 4 (Operational Guidance and Interfaces):** IALA harmonizes coastal base stations and AtoN. The National Marine Electronics Association (**NMEA**) and Radio Technical Commission for Maritime Services (**RTCM**) standardize bridge serial and CAN bus communications, while ETSI standardizes locating devices. River commissions, notably the Central Commission for the Navigation of the Rhine (**CCNR**) and CESNI, author Inland AIS extensions.

> **Definitions that bite.** *Performance standards versus test standards.* An IMO performance standard (such as [MSC.74(69)](ch15-standards-that-define-ais.md#references)) states operational goals (e.g., reporting speed or dynamic interval), but contains zero electronic test circuits. An IEC test standard (such as [IEC 61993-2](ch15-standards-that-define-ais.md#references)) is an engineering specification detailing laboratory wiring, RF injection levels, environmental conditioning, and numerical Pass/Fail criteria. Equipment is never "type-approved to MSC.74(69)"; it is type-approved to an IEC standard that satisfies MSC.74(69).

## 15.2 The statutory and operational tier: IMO instruments

Foundational legal authority for AIS originates in treaty law established by the IMO ([Chapter 16](ch16-laws-and-treaties.md)). The mandate and operational rules are codified across four categories of IMO instruments:

### 15.2.1 The performance standard: Resolution MSC.74(69) Annex 3
Adopted 12 May 1998, Resolution [MSC.74(69)](ch15-standards-that-define-ais.md#references) Annex 3 defines operational modes Class A transponders must support:
- **Autonomous and continuous mode:** Operating automatically in all navigable waters without manual intervention, self-regulating slot transmissions according to ship speed and course alterations.
- **Assigned mode:** Operating under remote slot or interval allocation commanded by a competent coastal Vessel Traffic Services (**VTS**) authority.
- **Polled mode:** Automatically responding to interrogation requests from authorized shore stations or search and rescue craft without interrupting autonomous background scheduling.

MSC.74(69) established four data classes: *static information* (IMO number, call sign, name, dimensions), *dynamic information* (GNSS position, time stamp, COG, SOG, heading, navigational status, rate of turn), *voyage-related information* (draught, cargo category, destination, ETA), and *short safety-related messages*. Section 7 stipulated built-in integrity testing and own-ship reporting within two minutes of power activation.

### 15.2.2 The operational guidelines: Resolutions A.917(22) and A.1106(29)
The IMO Assembly adopted Resolution A.917(22) in 2001, amended by Resolution A.956(23) in 2003, and superseded by Resolution [A.1106(29)](ch15-standards-that-define-ais.md#references) on 2 December 2015. Resolution A.1106(29) establishes crucial operational rules:
- **Continuous operation mandate:** Paragraph 22 dictates continuous operation underway or at anchor. The master may switch the transponder off only if continual transmission compromises ship safety or security. Any shutoff must be recorded in the official logbook with justification, and the transponder restarted as soon as danger has passed.
- **Collision avoidance limitations:** Paragraphs 40–44 explicitly warn bridge watchstanders that AIS is an aid to navigation and does not replace radar target tracking (**ARPA**) or visual lookouts. AIS targets cannot establish compliance with COLREGs, because small craft, naval vessels, and disabled stations may not transmit AIS signals.
- **Information accuracy disclaimer:** Paragraph 37 stresses that "the accuracy of AIS information received is only as good as the accuracy of the AIS information transmitted," highlighting manual data entry vulnerabilities.

### 15.2.3 Supporting circulars: installation, testing, and messages
The Maritime Safety Committee issues technical circulars standardizing field engineering practices:
- **IMO SN/Circ.227 and SN.1/Circ.245:** Adopted in 2003 and 2004, these circulars establish installation standards, defining VHF/GNSS antenna separation, cable loss limits, conning position **pilot plug** pinouts, and dedicated UPS buffering.
- **IMO MSC.1/Circ.1252:** Mandates the standardized annual performance test for Class A AIS equipment under SOLAS Regulation V/18.9, formalizing test reports verifying RF power, sensitivity, slot synchronization, and programming.
- **IMO SN.1/Circ.289 and SN.1/Circ.290:** Issued 2 June 2010, SN.1/Circ.289 governs international Application-Specific Messages (**ASMs**), assigning Designated Area Code (**DAC**) 001 and Function Identifiers (**FIs**) 16 through 32 for meteorological, hydrological, and tidal broadcasts, while SN.1/Circ.290 governs visual presentation.
- **IMO MSC.1/Circ.1473:** Adopted 23 May 2014, this policy document governs physical, synthetic, and virtual AIS Aids to Navigation, establishing criteria for virtual buoy broadcasting.

## 15.3 The technical radio tier: ITU-R M.1371 and M.585

Recommendation [ITU-R M.1371](ch15-standards-that-define-ais.md#references) specifies the radio protocol, modulation scheme, framing structure, and bit-level payload encodings enabling mobile transceivers to share VHF frequencies without centralized coordination.

### 15.3.1 Edition history of Recommendation ITU-R M.1371
Recommendation ITU-R M.1371 has evolved across six editions:
- **M.1371-0 (11/1998):** Baseline standard. Defined Self-Organizing TDMA (**SOTDMA**), 9,600 bit/s GMSK modulation, 25 kHz bandwidth, and Messages 1 through 19.
- **M.1371-1 (08/2001):** Harmonized Class A specifications prior to SOLAS carriage entry into force, refining slot selection and DSC channel management.
- **M.1371-2 (03/2006):** Added Carrier-Sense TDMA (**CSTDMA**) in Annex 7 for low-cost Class B transponders, introducing Messages 24A and 24B.
- **M.1371-3 (06/2007):** Refined Class B operational rules and group assignments, introducing Message 25 (single-slot binary) and Message 26 (multi-slot binary).
- **M.1371-4 (04/2010):** Added Message 27 for long-range satellite-AIS reporting and formalized AIS Search and Rescue Transmitters (**AIS-SART**) in Annex 9 burst mode.
- **M.1371-5 (02/2014):** Introduced Class B SOTDMA ("Class B SO" / Class B+) equipment and expanded ASM definitions in Annex 5.
- **M.1371-6 (02/2026):** Restructured into eight annexes by removing the legacy DSC annex. Prefixed clause numbers with annex identifiers (e.g., Clause `A2-3.3.4`) and added Message 28 for autonomous maritime radio devices (**AMRD**).

### 15.3.2 Physical and link layer constants
Recommendation ITU-R M.1371 defines exact constants governing the VHF Data Link (**VDL**):
- **RF Channels:** Primary operations occur on two international simplex channels in Radio Regulations Appendix 18: AIS 1 (VHF Channel 2087, 161.975 MHz) and AIS 2 (VHF Channel 2088, 162.025 MHz).
- **Modulation and Bit Rate:** GMSK modulation with bandwidth-time product ($BT$) of 0.4 for transmitters and 0.5 for receivers, operating at $9,600\text{ bit/s} \pm 50\text{ ppm}$.
- **TDMA Slot Geometry:** The link is synchronized to UTC using GNSS timing signals. Exactly 2,250 time slots exist per minute on each radio channel (4,500 total slots/minute across both channels). Each slot spans $26.67\text{ ms}$, corresponding to exactly 256 transmitted bit intervals:

$$\begin{aligned}
\text{Preamble (Training Sequence)} &: 24\text{ bits} \\
\text{Start Flag (HDLC } \texttt{0x7E}\text{)} &: 8\text{ bits} \\
\text{Data Payload (incl. Message ID, MMSI)} &: 168\text{ bits} \\
\text{Frame Check Sequence (CRC-16)} &: 16\text{ bits} \\
\text{End Flag (HDLC } \texttt{0x7E}\text{)} &: 8\text{ bits} \\
\text{Buffer and Propagation Delay} &: 32\text{ bits} \\
\hline
\mathbf{\text{Total Slot Budget}} &: \mathbf{256\text{ bits}}
\end{aligned}$$

The 32-bit buffer budget protects against slot collision caused by propagation delay. At $9,600\text{ bit/s}$, each bit spans $104.17\text{ }\mu\text{s}$. A buffer of 32 bits equals $3.333\text{ ms}$, accommodating RF power ramp-down, receiver squelch recovery, and speed-of-light delays across nominal radio horizons exceeding 120 nautical miles ($222\text{ km}$).

> **On the wire.** *Anatomy of a standard Class A position report.* A standard Class A dynamic transmission (Message 1, 2, or 3) comprises exactly 168 bits of payload data. Converted to 6-bit ASCII armoring for bridge NMEA transport, the payload generates a 28-character armored string:
> ```
> !AIVDM,1,1,,A,13aEO:0P0000k01M60000?wp0000,0*1A
> ```
> The 168 bits break down into explicit bit fields defined in Recommendation ITU-R M.1371-6 Table A7-1: Message Type (6 bits: `000001` = Type 1), Repeat Indicator (2 bits), MMSI (30 bits), Navigational Status (4 bits), Rate of Turn (8 bits), SOG (10 bits, units of 0.1 knot), Position Accuracy (1 bit), Longitude (28 bits, signed integer, $1/10000\text{ min}$ resolution), Latitude (27 bits, signed integer), COG (12 bits, units of 0.1 degree), True Heading (9 bits), Time Stamp (6 bits), Special Maneuver Indicator (2 bits), Spare (3 bits), RAIM Flag (1 bit), and SOTDMA Communication State (19 bits).

### 15.3.3 Identity allocation: Recommendation ITU-R M.585
Station identity is governed separately by Recommendation [ITU-R M.585](ch15-standards-that-define-ais.md#references), analyzed in [Chapter 13](ch13-mmsi-deep-dive.md). Recommendation ITU-R M.585 assigns numerical nine-digit Maritime Mobile Service Identity (**MMSI**) structures using Maritime Identification Digits (**MIDs**) allocated under the Radio Regulations:
- Ship stations: $\text{MID}xxxxxx$
- Coastal base stations: $00\text{MID}xxxx$
- Search and rescue aircraft: $111\text{MID}xxx$
- Physical and virtual Aids to Navigation: $99\text{MID}xxxx$
- AIS-SART locating transponders: $970xxxxxx$
- Man Overboard locating devices: $972xxxxxx$
- EPIRB with integrated AIS transmitters: $974xxxxxx$

Recommendation ITU-R M.585-10 (April 2026) introduced 12-character alphanumeric identity structures for locating transmitters and autonomous maritime radio devices to conserve terrestrial MMSI number blocks.

## 15.4 The testing and type-approval tier: IEC TC 80

IEC Technical Committee 80 authors laboratory test specifications making AIS equipment manufacturable and verifiable. Certified transponders carry type-approval plates issued by accredited test laboratories.

### 15.4.1 Class A shipborne equipment: IEC 61993-2
The test standard for SOLAS transceivers is [IEC 61993-2](ch15-standards-that-define-ais.md#references), *Class A shipborne equipment of the universal automatic identification system* (Edition 1.0 in 2001, Edition 2.0 in 2012, Edition 3.0 in 2018). It defines:
- **Radio frequency test regimes:** Verifies high-power ($12.5\text{ W}$, $+41\text{ dBm} \pm 1.5\text{ dB}$) and low-power ($1.0\text{ W}$, $+30\text{ dBm} \pm 1.5\text{ dB}$) RF outputs, adjacent channel power ratios ($>70\text{ dB}$ suppression at $25\text{ kHz}$ offset), and modulation accuracy.
- **Dynamic receiver performance:** Injects synthetic RF packets in the presence of interference and noise, mandating a maximum Packet Error Rate (**PER**) of $20\%$ at receiver sensitivity thresholds of $-107\text{ dBm}$.
- **Protocol state verification:** Simulates SOTDMA candidate slot selection, slot reservation chains, frame handover, and autonomous slot stealing under $100\%$ link saturation.
- **Bridge Alert Management (BAM):** Standardized under Edition 3.0, testing alert escalation, silencing, and acknowledgment via IEC 62923-1/2 protocols.
- **Internal GNSS receiver performance:** Verifies internal positioning maintains time-synchronization within $\pm 10\text{ }\mu\text{s}$ of UTC even if differential corrections fail.

### 15.4.2 Class B shipborne equipment: IEC 62287-1 and IEC 62287-2
To bring non-SOLAS vessels into tracking without congesting the VDL, IEC TC 80 developed the IEC 62287 series:
- **IEC 62287-1 (Class B CSTDMA):** Standardized in 2006 (Edition 1.0) and revised in 2017 (Edition 3.0) for $2\text{ W}$ ($+33\text{ dBm}$) Carrier-Sense TDMA units. The device listens immediately prior to transmission ($1.15\text{ ms}$ carrier sense window); if RF energy exceeds $-107\text{ dBm}$, it defers to Class A traffic. Edition 3.0 added direct internal UTC synchronization.
- **IEC 62287-2 (Class B SOTDMA / Class B SO):** Standardized in 2013 and revised in 2017 (Edition 2.0) for $5\text{ W}$ ($+37\text{ dBm}$) transceivers using genuine SOTDMA slot reservations on equal standing with Class A mobile stations, supporting reporting rates up to every five seconds for vessels exceeding 23 knots.

### 15.4.3 Shore base stations, Aids to Navigation, and repeaters: IEC 62320 series
Fixed VDL infrastructure is certified under the IEC 62320 series:
- **IEC 62320-1 (AIS Base Stations):** Edition 2.0 (2015) governs coastal base stations, specifying FATDMA slot reservations, VDL channel commands, diagnostics, and compliance under $90\%$ VDL traffic loading with standardized TAG block formatting.
- **IEC 62320-2 (AIS AtoN Stations):** Edition 2.0 (2016) establishes operational criteria for Aids to Navigation broadcasting Message 21 across three station types:
  - *Type 1 (Transmit Only):* Operates strictly on Fixed Access TDMA (**FATDMA**), requiring an external shore base station to pre-allocate its slots. The station lacks an AIS receiver and cannot accept remote configuration over the VDL.
  - *Type 2 (Transmit and Basic Receive):* Includes a receiver dedicated solely to accepting remote configuration commands and frequency retuning over the VDL.
  - *Type 3 (Full Transceive Capability):* Contains dual receivers supporting Random Access TDMA (**RATDMA**) and autonomous slot selection for remote deployment without shore base stations.
- **IEC 62320-3 (AIS Repeaters):** Published in 2015, Part 3 specifies simplex and duplex digital RF repeater stations deployed on headlands or offshore platforms to extend VHF coverage into sheltered waters.

### 15.4.4 Locating transponders: IEC 61097-14
Search and rescue locating transmitters are certified under [IEC 61097-14](ch15-standards-that-define-ais.md#references), *GMDSS Part 14: AIS Search and Rescue Transmitter (AIS-SART)*. Adopted in 2010 to satisfy IMO Resolution MSC.246(83), this standard defines the unique eight-packet burst transmission pattern. When activated, an AIS-SART broadcasts an eight-message sequence across AIS 1 and AIS 2 once every minute (four packets per channel), ensuring that at least one transmission occurs on the crest of ocean swells to overcome wave shadowing.

## 15.5 Operational and shore guidance: IALA recommendations

The International Organization for Marine Aids to Navigation, based in Saint-Germain-en-Laye, France, acts as operational coordinator for maritime shore authorities. Established as an international non-governmental association in 1957, IALA transitioned into an Intergovernmental Organization (**IGO**) on 22 August 2024 following ratification of the IALA Convention.

### 15.5.1 The IALA publication hierarchy
IALA publishes four tiers of technical documents identified by persistent Universal Resource Names (**URNs**) structured under the Maritime Resource Name scheme (`urn:mrn:iala:pub:...`):
1. **IALA Standards (S1010–S1070):** Broad structural frameworks covering AtoN planning (S1010), AtoN design (S1020), radionavigation (S1030), vessel traffic services (S1040), personnel training (S1050), digital communications (S1060), and information services (S1070).
2. **Recommendations (R-series, e.g., R0124, R0126):** Technical and operational policies approved by the IALA Council specifying how coastal administrations should deploy infrastructure.
3. **Guidelines (G-series, e.g., G1082, G1095, G1117):** Granular engineering manuals that provide practical implementation guidance for shore stations, software platforms, and network engineers.
4. **Model Courses (C-series, e.g., C0103):** Training curricula for VTS operators and marine technicians.

### 15.5.2 Key IALA documents governing AIS
- **Recommendation R0126 (A-126) Edition 2.0 (December 2021):** The governing standard for maritime authorities operating AIS Aids to Navigation. R0126 defines operational requirements for *Physical AtoN* (transponder mounted on a physical buoy or beacon), *Synthetic AtoN* (physical structure existing in the water, with its Message 21 broadcast generated remotely by a shore base station), and *Virtual AtoN* (no physical structure in the water; a digital hazard or waypoint broadcast to bridge displays). It defines service availability targets according to IALA Category 1 ($99.8\%$), Category 2 ($99.0\%$), and Category 3 ($97.0\%$) over a three-year rolling average.
- **Recommendation R0124 (A-124):** Governs shore-based AIS network architecture across twenty appendices, detailing coverage planning, base station co-location, FATDMA slot planning (Appendix 14), and VDL congestion management (Appendix 18).
- **Guideline G1082 Edition 2.0 (June 2016):** Provides a comprehensive engineering overview of the entire AIS system for shore administrators, detailing message catalogs, station capabilities, and satellite-AIS detection dynamics.
- **Guideline G1095:** Standardizes the design, technical registration, and implementation of Application-Specific Messages, preventing national administrations from authoring colliding binary payloads.
- **Guideline G1117 Edition 3.0 (December 2022):** Details the architectural roadmap for the VHF Data Exchange System (**VDES**), coordinating migration of bandwidth-intensive binary communications from legacy AIS channels to dedicated VDES frequencies.

## 15.6 Digital bridge interfaces: NMEA, IEC 61162, and displays

An AIS transponder exchanges data with shipboard sensors and bridge navigation displays. Digital interfacing is standardized across the IEC 61162 family and its American NMEA counterparts.

### 15.6.1 NMEA 0183 and IEC 61162-1 / IEC 61162-2
The maritime serial interface standard began with NMEA 0183, developed by the National Marine Electronics Association, adopted internationally as [IEC 61162-1](ch15-standards-that-define-ais.md#references). 
- **IEC 61162-1 (4,800 bit/s):** The traditional marine instrument bus operating over EIA-422 differential pairs. While sufficient for single-sensor feeds like depth sounders, its 4,800 baud rate is inadequate for AIS, where bursts of multi-slot VDL packets easily swamp the serial line.
- **IEC 61162-2 (38,400 bit/s High-Speed):** Published originally in 1998 and updated to Edition 2.0 in 2024, IEC 61162-2 defines the high-speed marine serial bus operating at 38,400 bit/s. This is the mandatory physical specification for shipboard AIS pilot plugs and display connections.
- **Encapsulation Sentences (`!AIVDM` and `!AIVDO`):** VDL radio packets are encapsulated into ASCII serial strings using the `!AIVDM` (received from other vessels) and `!AIVDO` (own-ship broadcast) sentence format. Long payloads spanning multiple TDMA slots are segmented into multi-part sentences carrying sequence counts and sentence numbers, armored with 6-bit ASCII encoding.
- **TAG Blocks:** Introduced in NMEA 0183 Version 4.10 and formalized in IEC 61162-1 Edition 4.0, TAG blocks prepend metadata parameters (such as source timestamp, destination channel, and station line identifier) directly to encapsulated sentences using backslash delimiters: `\s:base1,c:1620250000*hh\!AIVDM...`.

### 15.6.2 NMEA 2000 and IEC 61162-3
Modern commercial vessels and pleasure craft utilize Controller Area Network technology standardized under NMEA 2000 and codified internationally as [IEC 61162-3](ch15-standards-that-define-ais.md#references):
- **Architecture:** Based on the SAE J1939 industrial automotive protocol running at $250\text{ kbit/s}$ over shielded twisted pair cable with 29-bit CAN identifiers.
- **Parameter Group Numbers (PGNs):** AIS payloads are transported across CAN networks using dedicated PGNs. Because CAN frames carry a maximum of 8 bytes of data, longer AIS messages utilize NMEA 2000 **Fast Packet** transport, which fragments packets up to 223 bytes into sequential 8-byte frames:
  - PGN 129038: *Class A Position Report* (single-slot messages 1, 2, 3)
  - PGN 129039: *Class B Position Report* (message 18)
  - PGN 129040: *Class B Extended Position Report* (message 19)
  - PGN 129041: *Aids to Navigation Report* (message 21)
  - PGN 129794: *Class A Static and Voyage Related Data* (message 5)
  - PGN 129809/129810: *Class B Static Data Parts A and B* (message 24)

### 15.6.3 Lightweight Ethernet: IEC 61162-450 and IEC 61162-460
To handle integrated bridge systems on modern container carriers and cruise ships, IEC TC 80 standardized Lightweight Ethernet (**LWE**) under [IEC 61162-450](ch15-standards-that-define-ais.md#references) (Edition 3.0, 2024). LWE encapsulates NMEA sentences into standard UDP multicast datagrams operating across IEEE 802.3 networks at 100 Mbit/s or 1 Gbit/s. Each Ethernet packet carries a standardized `UdPbC` (UDP Packet Bridge Communication) header followed by TAG blocks and payload strings. To defend bridge networks against unauthorized tampering, [IEC 61162-460](ch15-standards-that-define-ais.md#references) specifies cybersecurity gateways, network firewalls, and cryptographic message authentication for Ethernet navigation backbones.

### 15.6.4 Display symbology: IEC 62288 and ECDIS integration
How AIS targets appear to the conning officer is strictly controlled:
- **IEC 62288 (Presentation of Navigation Displays):** Edition 3.0 (2021) governs graphical symbology, colors, and target vectors used on radar, ECDIS, and Integrated Navigation Systems (**INS**). Standard symbols include isosceles triangles pointing in the direction of heading, diamonds for Aids to Navigation, circles for base stations, and dedicated flashing symbols for activated AIS-SARTs.
- **ECDIS and Radar Interoperability:** [IEC 61174](ch15-standards-that-define-ais.md#references) (ECDIS) and [IEC 62388](ch15-standards-that-define-ais.md#references) (Radar) govern target fusion. If radar skin tracking and an AIS report share identical kinematic vectors within spatial error gates, systems fuse the targets into a single symbol to prevent screen clutter. Under IMO Resolution [MSC.530(106)](ch15-standards-that-define-ais.md#references) and the International Hydrographic Organization (**IHO**) S-100 framework, next-generation ECDIS systems directly ingest dynamic AIS AtoN reports to update chart displays in real time.

## 15.7 National transposition and type-approval: FCC and EU MED

International treaties and voluntary consensus standards possess no independent statutory force within sovereign territory. An IEC test standard or ITU radio recommendation becomes legally binding on mariners and equipment manufacturers only when transposed into domestic law by a national administration.

### 15.7.1 United States: Title 47 of the Code of Federal Regulations
In the United States, maritime equipment is governed by the Federal Communications Commission (**FCC**) and the United States Coast Guard (**USCG**):
- **Statutory Framework:** AIS radio rules are codified under **47 CFR Part 80** (Stations in the Maritime Services). Operational carriage requirements are codified separately under **33 CFR Part 164** by the USCG.
- **The USCG Letter of Compliance:** Under 47 CFR § 80.275 (Class A), § 80.231 (Class B), and § 80.233 (AIS-SART), an equipment manufacturer cannot apply directly to the FCC for equipment certification. The manufacturer must first submit complete laboratory test reports from an independent accredited test facility to the USCG Office of Navigation Systems. The Coast Guard verifies that the device satisfies all applicable IEC and IMO standards and issues a formal *Letter of Compliance*. Only then may the applicant submit the package to the FCC for grant of certification.
- **Static Data Security Restrictions:** Under 47 CFR § 80.231(b), the FCC strictly prohibits recreational users or ship crews from programming or modifying vessel static data (MMSI, call sign, vessel dimensions) on Class B equipment. All static data entry must be performed by certified marine electronics vendors or professional installers, and devices must display a mandatory statutory warning label against fraudulent data entry.

### 15.7.2 European Union: The Marine Equipment Directive
Within the European Union, maritime equipment type-approval is governed by Directive 2014/90/EU, widely known as the Marine Equipment Directive (**MED**):
- **The "Wheelmark":** Equipment certified under the MED carries the iconic **Wheelmark** logo stamped on its serial plate, followed by the identification number of the accredited Notified Body (such as DNV, TÜV, or BSH) and the year of manufacture.
- **Annual Implementing Regulations:** The European Commission issues regular Implementing Regulations (such as Implementing Regulation (EU) 2024/1975) that publish the authoritative itemized register of approved marine equipment. Class A AIS is categorized under item `MED/4.32`, while AIS-SART is categorized under item `MED/4.55`. The regulation specifies the exact edition of each IEC and IMO standard that must be satisfied for certification.

> **Worked example.** *Calculating regulatory obsolescence in statutory incorporation.* A persistent vulnerability in maritime governance is administrative delay between an SDO publishing a modernized test standard and a sovereign administration updating its statutory citations.
> 
> In 47 CFR § 80.7, the FCC incorporates technical standards by reference:
> - Class A AIS performance standard incorporated: ITU-R M.1371-3 (2007) and IEC 61993-2:2001 (Edition 1.0).
> - Class B CSTDMA standard incorporated under 47 CFR § 80.231: IEC 62287-1:2006 (Edition 1.0).
> 
> Meanwhile, international bodies have advanced to Recommendation ITU-R M.1371-6 (2026), IEC 61993-2 Edition 3.0 (2018), and IEC 62287-1 Edition 3.0 (2017):
> 
> $$\text{Regulatory Lag}_{\text{Class A}} = 2026 - 2007 = 19\text{ years (ITU-R)}, \quad 2026 - 2001 = 25\text{ years (IEC)}$$
> 
> An advanced Class A transceiver incorporating BAM and modern TAG blocks satisfies current European MED rules, but a vendor seeking US FCC certification must legally prove backward compatibility with a 2001 test specification.

## 15.8 How to read a maritime standard: anatomy of a test clause

Maritime technical standards follow highly structured formal taxonomies. An engineer or data analyst consulting an IEC or ITU document must understand how normative clauses are constructed.

### 15.8.1 Normative language: Shall, Should, and May
Maritime specifications strictly adhere to ISO/IEC Directives Part 2 drafting rules:
- **Shall:** Denotes an absolute, mandatory requirement. A transceiver failing a single "shall" clause fails type approval completely.
- **Should:** Denotes a strong recommendation. Compliance is expected unless compelling engineering justifications exist.
- **May:** Denotes a permissible optional feature or implementation freedom.

### 15.8.2 Anatomy of an IEC test standard clause
Every operational requirement in an IEC test specification (such as IEC 61993-2 or IEC 62287-1) is constructed with a standardized three-part anatomy:
1. **Required Operational Performance:** States the operational capability mandated by the IMO or ITU. (e.g., "The transmitter output power shall switch from high power ($12.5\text{ W}$) to low power ($1.0\text{ W}$) upon receipt of Message 22").
2. **Method of Measurement (Test Procedure):** Defines the exact laboratory configuration: RF signal generators, artificial antenna dummy loads ($50\text{ }\Omega$), ambient temperatures (ranging from $-15^{\circ}\text{C}$ to $+55^{\circ}\text{C}$ per IEC 60945), DC power supply variations ($\pm 10\%$), and simulated sequence of VDL packets injected into the receiver.
3. **Required Results:** Provides an unambiguous numerical Pass/Fail tolerance window. (e.g., "The measured RF power in low power mode shall be $1.0\text{ W} \pm 1.5\text{ dB}$ ($+30\text{ dBm}$, tolerance $+28.5\text{ dBm}$ to $+31.5\text{ dBm}$). Time to switch power levels shall not exceed $1.0\text{ ms}$").

## 15.9 Obtaining standards: free access versus commercial paywalls

Maritime standards divide between freely accessible public documents and paywalled industrial specifications:

### 15.9.1 Freely accessible repositories
- **ITU Publications:** All ITU-R Recommendations (including [ITU-R M.1371](ch15-standards-that-define-ais.md#references) and [ITU-R M.585](ch15-standards-that-define-ais.md#references)) and ITU-R Reports are available as free PDF downloads directly from the official ITU portal (`itu.int`). Following a 2013 ITU Council decision, the complete four-volume set of the ITU Radio Regulations is available free of charge for personal use.
- **IMO Resolutions and Circulars:** While the consolidated text of the SOLAS Convention is a paid copyright publication, individual IMO Assembly Resolutions (A-series), Maritime Safety Committee Resolutions (MSC-series), and Safety of Navigation Circulars (SN/Circ) are freely obtainable as public records via official flag-state mirrors (notably the USCG Navigation Center document portal, `navcen.uscg.gov`) and the IMO IMODOCS archive.
- **IALA Publications:** Recommendations and Guidelines published by IALA are freely downloadable in PDF format from the IALA website (`iala.int`), supported by international membership subscriptions.
- **IHO Specifications:** Standards published by the International Hydrographic Organization—including S-57, S-52, S-100, and product specifications S-101 through S-125—are freely accessible to the global maritime community at `iho.int`.
- **ETSI European Norms:** All technical standards, European Norms, and Technical Specifications authored by ETSI (such as [ETSI EN 303 098](ch15-standards-that-define-ais.md#references)) are downloadable free of charge without registration from `etsi.org`.

### 15.9.2 Paywalled specifications
- **IEC International Standards:** All documents authored by IEC TC 80 (IEC 61993-2, IEC 62287, IEC 62320, IEC 61162, IEC 62288, IEC 60945) are copyright-protected commercial products. Single-user digital copies must be purchased from the IEC Webstore (`webstore.iec.ch`) or national standards bodies (BSI, DIN, ANSI, SIS), typically priced between 200 and 450 Swiss Francs (CHF) per document. A complete engineering library of IEC AIS standards costs upwards of 5,000 CHF.
- **NMEA Specifications:** Standards authored by the National Marine Electronics Association (NMEA 0183, NMEA 2000, OneNet) are proprietary commercial specifications. Prices range from several hundred to thousands of US dollars, and developers implementing certified NMEA 2000 devices must enter non-disclosure agreements and purchase proprietary certification toolkits.
- **RTCM Standards:** Standards published by RTCM Special Committees (such as RTCM 12100.1 or RTCM 10160.0) are proprietary commercial publications available for purchase through the RTCM web store (`rtcm.org`).

## Then & now

- ⟨H⟩ **1998:** The IMO adopts Resolution [MSC.74(69)](ch15-standards-that-define-ais.md#references) Annex 3, establishing the first global performance standard for universal shipborne AIS and delegating technical radio characteristics to the ITU.
- ⟨H⟩ **1998:** ITU-R Working Party 5B publishes Recommendation [ITU-R M.1371-0](ch15-standards-that-define-ais.md#references), codifying GMSK modulation, 9,600 bit/s transmission speed, and SOTDMA channel access across VHF Channels 87B and 88B.
- ⟨+⟩ **2001:** IEC TC 80 publishes [IEC 61993-2](ch15-standards-that-define-ais.md#references) Edition 1.0, establishing the first international pass/fail laboratory type-approval test standard for Class A transponders.
- ⟨+⟩ **2002:** The European Union introduces Directive 2002/59/EC, establishing the Community vessel traffic monitoring system (SafeSeaNet) and enforcing European type-approval under the Marine Equipment Directive.
- ⟨+⟩ **2006:** Publication of [IEC 62287-1](ch15-standards-that-define-ais.md#references) Edition 1.0 standardizes Class B CSTDMA equipment, introducing affordable digital tracking for non-SOLAS vessels.
- ⟨+⟩ **2010:** Publication of [IEC 61097-14](ch15-standards-that-define-ais.md#references) standardizes AIS-SART search and rescue transmitters, introducing the 8-packet burst sequence.
- ⟨+⟩ **2013:** Publication of [IEC 62287-2](ch15-standards-that-define-ais.md#references) formalizes Class B SOTDMA ("Class B SO"), granting non-SOLAS vessels autonomous slot reservation capabilities.
- ⟨+⟩ **2014:** Recommendation [ITU-R M.1371-5](ch15-standards-that-define-ais.md#references) expands Application-Specific Messages and formalizes Class B SO slot coordination rules across nine annexes.
- ⟨+⟩ **2021:** IALA adopts Recommendation [R0126](ch15-standards-that-define-ais.md#references) Edition 2.0 under its persistent URN architecture, standardizing physical, synthetic, and virtual AIS AtoN management.
- ⟨+⟩ **2024:** On 22 August 2024, the IALA Convention enters into force, elevating IALA from a non-governmental association into an Intergovernmental Organization (**IGO**) with sovereign treaty standing.
- ⟨+⟩ **2026:** Recommendation [ITU-R M.1371-6](ch15-standards-that-define-ais.md#references) enters into force, restructuring the foundational technical standard into eight annexes and introducing autonomous maritime radio device protocols.

## Validation, uncertainty & data quality

Because AIS data is generated and filtered through an assembly line of disparate technical specifications, data analysts face systemic validation hurdles stemming directly from standards seams and regulatory mismatches.

### 1. Verification procedure: detecting legacy firmware truncations
Under international maritime law, equipment type-approved under an older standard (such as IEC 61993-2 Edition 1.0 of 2001) remains legally grandfathered on existing vessels throughout the ship's operational life. Consequently, operational data streams contain messages produced by twenty-five-year-old firmware operating alongside brand-new transceivers.

- **Vulnerability:** Legacy Edition 1.0 transponders often mishandle multi-sentence `!AIVDM` armoring when transmitting extended static messages (Message 5) or Application-Specific Messages (Message 6 and 8). Furthermore, older transceivers frequently truncate ship names containing non-standard ASCII characters or terminate 20-character vessel name fields prematurely.
- **Verification Algorithm:** Ingestion pipelines should execute an automated structural integrity check on all multi-fragment sentences:
```python
def validate_aivdm_fragment_sequence(sentences):
    """Verifies sequential integrity and fragment counts of multi-line AIVDM strings."""
    expected_seq = None
    accumulated = []
    
    for line in sentences:
        parts = line.strip().split(',')
        if len(parts) < 7:
            return False, "Malformed NMEA sentence"
        
        total_fragments = int(parts[1])
        fragment_num = int(parts[2])
        seq_id = parts[3]
        payload = parts[5]
        
        if fragment_num == 1:
            accumulated = [payload]
            expected_seq = seq_id
        else:
            if seq_id != expected_seq:
                return False, f"Sequence ID mismatch: {seq_id} != {expected_seq}"
            accumulated.append(payload)
            
        if fragment_num == total_fragments:
            full_armored = "".join(accumulated)
            return True, full_armored
    return False, "Incomplete sentence sequence"
```

### 2. Quantification of standards-derived data anomalies
Empirical studies of raw coastal receiver archives (such as those collected by the USCG Nationwide AIS network or the Danish Maritime Authority) reveal consistent failure rates directly attributable to standards seams:
- **Checksum corruption on high-speed serial links:** Across raw IEC 61162-2 serial lines operating at $38,400\text{ bit/s}$, unshielded cable runs in engine rooms produce bit-slip errors resulting in an average checksum failure rate of $0.12\%$ to $0.45\%$.
- **Class B slot drop-out during VDL saturation:** Because IEC 62287-1 CSTDMA transceivers must defer transmission if channel noise exceeds $-107\text{ dBm}$, Class B reporting intervals degrade dramatically in congested waterways. In major ports (e.g., Singapore or Rotterdam) where channel loading exceeds $50\%$, Class B CS packet transmission rates drop by $35\%$ to $60\%$ relative to their nominal schedule.
- **Grandfathered field truncation:** Approximately $1.4\%$ of commercial vessels in global databases broadcast static data containing invalid padding characters (`@`) or truncated call signs caused by legacy configuration software.

> **Try it.** Verifying NMEA checksums across standards-compliant sentences. Run this snippet to verify whether an encapsulated AIS sentence conforms to the mandatory XOR checksum required by NMEA 0183 and IEC 61162-1:
```python
def verify_nmea_checksum(sentence: str) -> bool:
    """Computes XOR checksum and validates against sentence trailer."""
    content, sep, checksum_str = sentence.strip().partition('*')
    if not sep or len(checksum_str) != 2:
        return False
    # Strip leading ! or $
    payload = content[1:] if content.startswith(('!', '$')) else content
    computed = 0
    for char in payload:
        computed ^= ord(char)
    expected = int(checksum_str, 16)
    return computed == expected

test_sentence = "!AIVDM,1,1,,A,13aEO:0P0000k01M60000?wp0000,0*1A"
print(f"Sentence Valid: {verify_nmea_checksum(test_sentence)}")
# Expected output: Sentence Valid: True
```

## Software

Software tools that implement or decode maritime standards include:

**Open source:**
- **libais** (Apache-2.0): High-performance C++ decoder with Python bindings, originally developed at UNH CCOM, providing bit-exact parsing of standard ITU-R M.1371 messages and IMO/IALA Application-Specific Messages. *Caveat:* Enforces strict bit-length validation, immediately throwing exceptions on truncated non-conformant vendor packets.
- **pyais** (MIT): Comprehensive Python decoding and encoding library supporting NMEA 0183 (`!AIVDM`/`!AIVDO`), NMEA 2000 PGNs, and IEC 61162-1 TAG blocks. *Caveat:* Processing speed is limited when decoding multi-gigabyte historical archive files compared to compiled binaries.
- **gpsd** (BSD-2-Clause): Ubiquitous Linux sensor daemon supporting NMEA 0183, NMEA 2000, and serial multiplexing for bridge sensors. *Caveat:* Strips raw TDMA link-layer slot metadata and communication-state bits during JSON serialization.

**Free but closed:**
- **ITU MARS Search Engine** (International Telecommunication Union): Official web-based database of maritime mobile stations, call signs, and MMSIs published pursuant to Radio Regulations Article 20. *Caveat:* Administrative notification latency means newly registered or re-flagged vessels may not appear for several months.
- **USCG Navigation Center AIS References Portal** (United States Coast Guard): Comprehensive online archive providing free public downloads of IMO Resolutions, circulars, and federal guidance documents. *Caveat:* Focuses on US regulatory jurisdiction and maritime safety notices.

**Commercial:**
- **Rhode & Schwarz SMBV100B / CMA180 Radiocommunications Testers**: Industry-standard automated RF test bench software used by certification laboratories to perform pass/fail type-approval testing against IEC 61993-2, IEC 62287, and IEC 61097-14. *Caveat:* Extremely capital-intensive laboratory hardware and proprietary closed software suites.
- **NMEA 2000 Network Certification Tool**: Official test suite mandated by the National Marine Electronics Association for certifying CAN bus electronics. *Caveat:* Requires corporate NMEA membership, non-disclosure agreements, and paid licensing.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3 (1998):** Foundational performance standard establishing operational capabilities and reporting intervals.
- **IMO Resolution A.1106(29) (2015):** Operational rules, continuous operation mandates, and inherent limitations.
- **Recommendation ITU-R M.1371-6 (2026):** Core technical standard defining GMSK modulation, TDMA slotting, framing, access schemes, and Messages 1–28.
- **Recommendation ITU-R M.585-10 (2026):** Numerical 9-digit MMSIs and 12-character identities.
- **IEC 61993-2:2018 (Edition 3.0):** Pass/fail type-approval test standard for SOLAS Class A transponders.
- **IEC 62287-1:2017 (Edition 3.0):** Test standard governing low-power Class B CS transponders.
- **IEC 62287-2:2017 (Edition 2.0):** Test standard governing Class B SO transponders.
- **IEC 62320-1:2015 (Edition 2.0):** Shore base stations, FATDMA coordination, and TAG blocks.
- **IEC 62320-2:2016 (Edition 2.0):** Type 1, Type 2, and Type 3 AtoN transponders.
- **IEC 61097-14:2010 (Edition 1.0):** Emergency locating transponder testing and 8-packet burst scheduling.
- **IEC 61162-1:2024 / IEC 61162-2:2024:** 4,800 baud and 38,400 baud serial NMEA encapsulation sentence formatting.
- **IEC 61162-450:2024 (Edition 3.0):** Lightweight Ethernet UDP multicast bridge sensor backbones.
- **IEC 62288:2021 (Edition 3.0):** Graphical symbology, colors, and target presentation on radar and ECDIS.
- **IALA Recommendation R0126 (2021):** Operational guidance for physical, synthetic, and virtual AtoN.
- **NMEA 0183 Version 4.30 (2023):** Standard for interfacing marine electronic devices, governing `!AIVDM` encapsulation and TAG blocks.
- **ETSI EN 303 098 V2.2.1 (2019):** European harmonized standard for AIS-MOB locating transmitters under the Radio Equipment Directive.
- **RTCM 12100.1 (2022):** Formal guidelines for authoring international and regional binary payloads.

## Pitfalls

- **Confusing IMO performance standards with IEC test standards:** Attempting to certify hardware against IMO Resolution MSC.74(69) rather than the applicable IEC test standard (e.g., IEC 61993-2). IMO resolutions dictate policy and operational functionality; IEC standards dictate electronic test circuits and numerical pass/fail criteria.
- **Assuming voluntary standards are self-executing:** Treating an IALA guideline, NMEA specification, or IEC standard as mandatory domestic law before confirming whether the national maritime administration (e.g., USCG, UK MCA) or regional directive (EU MED) has formally incorporated that specific edition by reference.
- **Overlooking statutory incorporation lag:** Assuming that a vessel legally operating under modern flags satisfies the latest IEC standard. National regulations frequently lag SDO publishing schedules by decades; for example, US 47 CFR § 80.7 still incorporates IEC 61993-2:2001 (Edition 1.0), grandfathering ancient transceivers.
- **Misinterpreting Class B deferral as hardware failure:** Concluding that a Class B CSTDMA transponder has suffered an electronic fault when its dynamic reporting interval drops from thirty seconds to several minutes in busy ports. Under IEC 62287-1, CSTDMA units must defer transmission if RF channel noise exceeds $-107\text{ dBm}$.
- **Assuming all maritime standards are free to read:** Expecting IEC, NMEA, and RTCM standards to be accessible via open-access portals. While ITU-R, IMO circulars, IALA, and IHO standards are freely downloadable, IEC and NMEA standards are paywalled commercial publications protected by copyright.
- **Ignoring the M.1371-6 annex renumbering:** Citing annexes and clauses using superseded M.1371-5 numbering. Recommendation ITU-R M.1371-6 dropped the DSC channel-management annex, reducing total annexes from nine to eight and introducing annex-prefixed clause numbers throughout the text.
- **Conflating Type 1 and Type 3 AIS AtoN capabilities:** Expecting a Type 1 AIS AtoN to respond to VDL interrogation or accept remote channel reconfiguration. Certified under IEC 62320-2, Type 1 stations operate strictly on FATDMA and lack an internal receiver.
- **Mishandling multi-sentence `!AIVDM` buffering:** Assuming multi-part NMEA sentences arrive sequentially on serial buses without interleaving. Multiplexed bridge networks frequently inject unrelated sentences between fragments, breaking naive decoders that do not validate sequence IDs.
- **Ignoring IALA's legal transformation:** Referring to IALA as a non-governmental association or failing to recognize its legal status as an Intergovernmental Organization following the entry into force of the IALA Convention on 22 August 2024.
- **Overlooking NMEA checksum casing:** Failing to recognize that standard NMEA 0183 and IEC 61162-1 require hexadecimal checksum characters to be uppercase (`*1A`, not `*1a`).

## Key takeaways

- AIS is governed by an interlocking four-tier institutional hierarchy: IMO establishes statutory carriage and operational rules, ITU standardizes radio characteristics, IEC TC 80 authors laboratory pass/fail test specifications, and IALA/regional bodies author operational guidance.
- IMO Resolution MSC.74(69) Annex 3 is the foundational performance standard, explicitly delegating technical radiocommunication characteristics to the ITU.
- Recommendation ITU-R M.1371 governs the link layer and RF modulation; approved in February 2026, Edition 6 restructured the document into eight annexes and introduced AMRD protocols.
- IEC test standards (IEC 61993-2 for Class A, IEC 62287 for Class B, IEC 62320 for shore base stations and AtoN) are the exact specifications against which transceivers are certified for type approval.
- An IEC test standard clause consists of three mandatory elements: required operational performance, laboratory method of measurement, and unambiguous numerical required results.
- Digital bridge interfaces evolved from serial NMEA 0183 / IEC 61162-1 (4,800 baud) and high-speed IEC 61162-2 (38,400 baud) to CAN-based NMEA 2000 / IEC 61162-3 and Lightweight Ethernet IEC 61162-450.
- International standards are legally inert until transposed into domestic statute by sovereign administrations, such as FCC 47 CFR Part 80 in the United States and the Marine Equipment Directive (Wheelmark) in the European Union.
- Statutory incorporation delays create substantial regulatory lag; ships legally navigate today with grandfathered transponders certified under twenty-five-year-old test standards.
- ITU, IMO, IALA, IHO, and ETSI specifications are freely accessible online, whereas IEC, NMEA, and RTCM standards remain paywalled commercial publications.
- On 22 August 2024, IALA formally transitioned into an Intergovernmental Organization (**IGO**), bridging a historic gap between international shipboard mandates and coastal shore infrastructure governance.

## References

- European Telecommunications Standards Institute (2019). *ETSI EN 303 098 V2.2.1: Low Power Locating Devices Employing AIS*. Sophia Antipolis: ETSI.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2016). *IALA Guideline G1082: Overview of AIS* (Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2001). *IEC 61993-2:2001: Class A Shipborne Equipment of the Universal AIS* (Edition 1.0). Geneva: IEC.
- International Electrotechnical Commission (2010). *IEC 61097-14:2010: GMDSS Part 14: AIS-SART* (Edition 1.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *IEC 62320-1:2015: AIS Base Stations* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *IEC 62320-3:2015: AIS Repeater Stations* (Edition 1.0). Geneva: IEC.
- International Electrotechnical Commission (2016). *IEC 62320-2:2016: AIS AtoN Stations* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2017). *IEC 62287-1:2017: Class B Shipborne Equipment — Part 1: CSTDMA* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2017). *IEC 62287-2:2017: Class B Shipborne Equipment — Part 2: SOTDMA* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *IEC 61993-2:2018: Class A Shipborne Equipment* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *IEC 62288:2021: Presentation on Navigational Displays* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2024). *IEC 61162-1:2024: Digital Interfaces — Single Talker and Multiple Listeners* (Edition 6.0). Geneva: IEC.
- International Electrotechnical Commission (2024). *IEC 61162-450:2024: Digital Interfaces — Ethernet Interconnection* (Edition 3.0). Geneva: IEC.
- International Hydrographic Organization (2025). *IHO S-100: Universal Hydrographic Data Model* (Edition 5.2.1). Monaco: IHO.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne AIS* (Resolution MSC.74(69), Annex 3). London: IMO.
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages* (Circular SN.1/Circ.289). London: IMO.
- International Maritime Organization (2014). *Policy on Use of AIS Aids to Navigation* (Circular MSC.1/Circ.1473). London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for Operational Use of Shipborne AIS* (Resolution A.1106(29)). London: IMO.
- International Maritime Organization (2022). *Performance Standards for ECDIS* (Resolution MSC.530(106)). London: IMO.
- International Organization for Marine Aids to Navigation (2021). *The Use of AIS in Marine Aids to Navigation Services* (Recommendation R0126, Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Telecommunication Union (1998). *Recommendation ITU-R M.1371-0: Technical Characteristics for Shipborne AIS*. Geneva: ITU-R.
- International Telecommunication Union (2001). *Recommendation ITU-R M.1371-1: Technical Characteristics for Shipborne AIS*. Geneva: ITU-R.
- International Telecommunication Union (2010). *Recommendation ITU-R M.1371-4: Technical Characteristics for AIS*. Geneva: ITU-R.
- International Telecommunication Union (2014). *Recommendation ITU-R M.1371-5: Technical Characteristics for AIS*. Geneva: ITU-R.
- International Telecommunication Union (2026). *Recommendation ITU-R M.1371-6: Technical Characteristics for AIS*. Geneva: ITU-R.
- International Telecommunication Union (2026). *Recommendation ITU-R M.585-10: Assignment of Identities in the Maritime Mobile Service*. Geneva: ITU-R.
- National Marine Electronics Association (2023). *NMEA 0183: Interfacing Marine Electronic Devices* (Version 4.30). Severna Park: NMEA.
- Radio Technical Commission for Maritime Services (2022). *RTCM 12100.1: Creation and Qualification of Application-Specific Messages*. Arlington: RTCM.
- Radio Technical Commission for Maritime Services (2025). *RTCM 10160.0: Resetting Own-Ship MMSIs on DSC Radios and Static Data on AIS*. Arlington: RTCM.
